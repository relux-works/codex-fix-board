# TASK-260929-36bvsc results — thread pending-work snapshot (CR rev 2 handoff)

## Top finding

Hosted precheck 3 ran the exact worktree tree
`cf567d98480d05428ed9dea58f66306dbf030ff6` (snapshot `9ac368c5`, run
37473988733) and is fully green: all four lanes `success`, all 5 narrowing
mutants killed, 0 survivors. Both rev-1 review findings (same mechanism:
sampled B receipt never retired, snapshot resurrected it as Queued) are fixed
by joint B+mailbox retirement in `acknowledge_submitted`, with the named
regression test `production_acknowledgement_removes_pending_work` and its
narrowing mutant `production_ack_skips_store_retirement` killed by that test
(run 37474019570). No file changed in this handoff pass; tree re-verified
`TREE_MATCH`. Ready for review.

## Evidence pin

- Worktree tree `cf567d98480d05428ed9dea58f66306dbf030ff6`, re-verified in
  this run via temp index (`git read-tree HEAD`, `git add -A`,
  `git write-tree`) — output identical, `TREE_MATCH`, zero changes.
  Candidate UNCOMMITTED on tip `812b8037a8`; `git status` shows only the
  12 candidate paths (8 modified, 4 new).
- Precheck 3 base run 37473988733 (snapshot 9ac368c5): lanes
  `{'core': 'success', 'app-server': 'success', 'lint': 'success',
  'small': 'success'}`. All green.
- Mutant kills (5/5, 0 survivors), from
  `TASK-260929-36bvsc_hosted-precheck-3.md`:

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| production_ack_skips_store_retirement | 37474019570 | core,lint | production_acknowledgement_removes_pending_work |
| provider_missing_mapped_to_empty | 37474048117 | small,core | goal_read_failure_is_explicit_error_not_empty, read_failure_returns_explicit_error_not_empty_snapshot |
| store_queued_excluded_from_snapshot | 37474077806 | core | armed_to_queued_is_atomic_for_concurrent_readers, snapshot_reports_armed_queued_and_leased_only |
| suspend_skips_revision_bump | 37474108222 | core | revision_increases_on_suspend |
| suspended_queued_admitted | 37474137228 | core | snapshot_excludes_suspended_and_cancelled |

## What rev 2 changed vs rev 1 (rework summary, already in tree)

Review round 1 (`TASK-260929-36bvsc_review-verdict-rev1.md`,
changes_requested) reported two findings on row "snapshot contents" (both
severity bypass, same mechanism): `sampled-receipt-remains-pending` and
`acknowledged-store-claim-still-pending`. Production
`acknowledge_submitted` retired only the mailbox entry, never the B receipt,
so `build_snapshot`'s store-Queued union resurrected sampled receipts
forever (the E2 gate would wait forever on finished work). The old test
hand-acknowledged both stores and its comment claiming production did the
same was false.

Fix (production):

- `codex-rs/core/src/session/runtime_mailbox.rs`: `RuntimeLease` carries the
  B receipt `owner` captured at admission, with an `owner()` accessor.
- `codex-rs/core/src/session/exec_completion_ack.rs`:
  `acknowledge_submitted` retires both sides per member in defined order
  (mailbox removal first, gating B `lease_pushed_completion` +
  `acknowledge_pushed_completion`), preserving D1 acknowledgment-at-acceptance
  semantics and fail-after-ack no-op idempotence in both stores.
- `codex-rs/core/src/session/pending_work.rs`: docs only — the store-Queued
  union is kept (still needed for Armed→Queued atomicity and the pre-enqueue
  window); the three legitimate store-without-mailbox windows (pre-enqueue,
  intra-acceptance transient, mailbox-cancel-not-yet-in-store) are stated
  precisely. No logic change.
- `codex-rs/core/src/session/pending_work_tests.rs`: removed the hand-acking
  fixture and its false comment (`snapshot_excludes_suspended_acknowledged_and_cancelled`
  renamed to `snapshot_excludes_suspended_and_cancelled`, suspended +
  cancelled only); added `production_acknowledgement_removes_pending_work`,
  which drives the REAL production path through a real `Session`
  (reserve/arm/publish, enqueue + lease, `note_recorded`,
  `acknowledge_submitted` on a prompt containing the trusted fragment, then
  read via the installed `PendingWorkProvider`) and asserts the receipt is in
  neither set, the B store is `Sampled(PushedCompletion)`, and a later
  mailbox fail is a no-op.

## Changed files (full candidate, rev 1 + rev 2 rework)

Modified (8): `codex-rs/core/src/session/exec_completion_ack.rs`,
`codex-rs/core/src/session/input_queue.rs`,
`codex-rs/core/src/session/mod.rs`,
`codex-rs/core/src/session/runtime_mailbox.rs`,
`codex-rs/core/src/session/session.rs`,
`codex-rs/core/src/unified_exec/completion_receipt.rs`,
`codex-rs/core/src/unified_exec/mod.rs`,
`codex-rs/ext/extension-api/src/lib.rs`.
New (4): `codex-rs/core/src/session/pending_work.rs`,
`codex-rs/core/src/session/pending_work_tests.rs`,
`codex-rs/ext/extension-api/src/pending_work.rs`,
`codex-rs/ext/goal/tests/pending_work.rs`.
No `list_processes` in snapshot paths. No new core→goal dependency
(goal tests use only extension-api types + `ExtensionData`; core installs
the provider into thread extension data).

## AC coverage — 5 of 5 rows driven

Production entries: `codex_extension_api::read_pending_work(&ExtensionData)`
→ provider → `core::session::pending_work::try_read_snapshot(&Session)`;
acceptance via `core::session::exec_completion_ack::acknowledge_submitted`.

| AC | Driving test (committed) | Refusal / negative test | Production call site |
|----|--------------------------|-------------------------|----------------------|
| AC1 Armed+Queued/Leased only, no servers/acked/suspended | `snapshot_reports_armed_queued_and_leased_only` | `snapshot_excludes_suspended_and_cancelled` (suspended/cancelled absent; Reserved absent) + `production_acknowledgement_removes_pending_work` (sampled absent via real acceptance; live servers excluded by construction, no liveness read) | `build_snapshot` in `core/src/session/pending_work.rs`; `acknowledge_submitted` in `core/src/session/exec_completion_ack.rs` |
| AC2 revision strictly increases on arm, queue, lease, fail-back, acknowledge, cancel, suspend, release | `revision_increases_on_arm`, `revision_increases_on_queue_via_publish`, `revision_increases_on_queue_via_mailbox_enqueue`, `revision_increases_on_lease`, `revision_increases_on_store_lease`, `revision_increases_on_fail_back`, `revision_increases_on_store_fail_back`, `revision_increases_on_acknowledge`, `revision_increases_on_store_acknowledge`, `revision_increases_on_cancel`, `revision_increases_on_mailbox_cancel`, `revision_increases_on_suspend`, `revision_increases_on_suspend_via_exhausted_fail`, `revision_increases_on_release` (14 tests, 8 named transitions, both stores where applicable) | N/A (monotonic increase; each asserts `after > before`) | `CompletionReceiptStore::{reserve,resolve_initial_response,publish_exit,lease_for_sampling,fail_sampling,acknowledge_sampled,cancel}` and `RuntimeMailbox::{enqueue,lease_available_up_to,acknowledge,fail,cancel,suspend}` |
| AC3 failed read is explicit error, never empty | `read_failure_returns_explicit_error_not_empty_snapshot` (core), `goal_read_failure_is_explicit_error_not_empty` (goal), `mailbox_contended_read_fails_explicitly_not_empty`, `store_contended_read_fails_explicitly_not_empty` | Same tests assert `Err` and `!= Ok(empty)` | `read_pending_work` in `ext/extension-api/src/pending_work.rs`, `try_read_snapshot` mapping |
| AC4 Armed→Queued atomic, latch-driven | `armed_to_queued_is_atomic_for_concurrent_readers` (tokio barrier, 4 readers × 200 iterations, writer publishes once; exactly one side, never neither nor both) | Same test kills `store_queued_excluded_from_snapshot` | `try_list_pending` single-lock read + union in `build_snapshot` |
| AC5 goal reads via extension API, no new core→goal dep | `goal_reads_pending_work_through_extension_api` (goal test uses only extension-api types + `ExtensionData`) | `goal_read_failure_is_explicit_error_not_empty` | `read_pending_work` + `PendingWorkProvider` in `ext/extension-api`; core installs provider in `session.rs` |

Review findings answered: both rev-1 findings (same mechanism,
`repeat-of: none`) are fixed by the joint retirement;
`production_acknowledgement_removes_pending_work` is the named regression
test for that class, and `production_ack_skips_store_retirement` is its
narrowing mutant, killed on hosted run 37474019570.

Out of contract: the consuming policy (TASK-260929-2snjbb, E2) remains
explicitly out of scope per the task description (acceptance clause "Out of
scope: the policy that consumes it"). All 5 AC rows covered.

## Surface-table coverage map (3 of 3 rows, each with tests + killed mutant)

| Surface row | Tests that exercise it | Narrowing mutant (killed, run) |
|---|---|---|
| snapshot contents | `snapshot_reports_armed_queued_and_leased_only`, `snapshot_excludes_suspended_and_cancelled`, `production_acknowledgement_removes_pending_work` | `suspended_queued_admitted` → `snapshot_excludes_suspended_and_cancelled` (37474137228); `store_queued_excluded_from_snapshot` → `snapshot_reports_armed_queued_and_leased_only` (37474077806); `production_ack_skips_store_retirement` → `production_acknowledgement_removes_pending_work` (37474019570) |
| revision and atomicity | 14 `revision_increases_on_*` tests, `armed_to_queued_is_atomic_for_concurrent_readers` | `suspend_skips_revision_bump` → `revision_increases_on_suspend` (37474108222); `store_queued_excluded_from_snapshot` → `armed_to_queued_is_atomic_for_concurrent_readers` (37474077806) |
| read failure and API boundary | `read_failure_returns_explicit_error_not_empty_snapshot` (core), `goal_read_failure_is_explicit_error_not_empty` (goal), contended-read tests | `provider_missing_mapped_to_empty` → both read-failure tests (37474048117) |

No uncovered surface rows. No survivors.

## Mutant evidence (5 narrowing mutants, 5 killed)

All mutants narrow (gate stays, weakened to admit exactly one rejectable
member). Patches: `TASK-260929-36bvsc_mutants.json` (attached, 5 entries).

| Mutant | What it narrows the gate to | Named test that fails (hosted run) | Survival bound (not observed — all killed) |
|--------|-----------------------------|------------------------------------|--------------------------------------------|
| `production_ack_skips_store_retirement` | Acceptance keeps mailbox removal but skips B lease+ack, admitting sampled receipts as store-Queued | `production_acknowledgement_removes_pending_work` (37474019570, core+lint) | Survival would state sampled work stays pending forever (E2 would wait forever) |
| `provider_missing_mapped_to_empty` | Error-vs-empty admits `ProviderMissing` as `Ok(empty)` but keeps other errors | `read_failure_returns_explicit_error_not_empty_snapshot` (core) and `goal_read_failure_is_explicit_error_not_empty` (goal) (37474048117, small+core) | Survival would state missing provider looks like no work |
| `store_queued_excluded_from_snapshot` | Atomic union admits mailbox-only Queued, dropping store Queued (gap) | `snapshot_reports_armed_queued_and_leased_only` and `armed_to_queued_is_atomic_for_concurrent_readers` (37474077806, core) | Survival would state pre-enqueue exits look like no work |
| `suspend_skips_revision_bump` | Revision gate admits suspend without bump but keeps all other bumps | `revision_increases_on_suspend` (37474108222, core) | Survival would state suspend is invisible to revision watches |
| `suspended_queued_admitted` | Suspended exclusion admits suspended-unleased but still excludes suspended-leased | `snapshot_excludes_suspended_and_cancelled` (37474137228, core) | Survival would state suspended-unleased counts as pending |

## Commands with real exit codes

This handoff pass (no file changed, per e1-handoff-note-3):

- Temp-index tree check (`git read-tree HEAD`, `git add -A`,
  `git write-tree`) → `cf567d98480d05428ed9dea58f66306dbf030ff6`,
  identical to precheck-3 tree, exit 0. `TREE_MATCH`.
- `git status --porcelain` → only the 12 candidate paths, exit 0.
- `git diff --stat HEAD` → 8 modified files shown (untracked 4 new files
  not in diff), exit 0.
- `python3 .../codex-fix-suite-busy.py --any` → `FREE`, exit 0.

Prior passes (cited, not re-run — tree unchanged since precheck 3):

- Rev-2 rework: `just fmt` exit 0; `just clippy -p codex-core` exit 0 (3
  pre-existing warnings only); narrow `nextest -p codex-core --lib -E
  'test(pending_work) or test(exec_completion)'` → 38 passed, exit 0; all 5
  mutant patches `git apply --check` clean; target trimmed.
- Precheck 3 (authoritative): base run 37473988733 all 4 lanes success;
  5 mutant runs above, each failing its intended lanes/tests.

No commands run through pipes that hide exit codes. No builds in this
pass: the tree is byte-identical to the hosted-green snapshot, so local
rebuild would only contend the shared target.

## Unverified

None for this leaf's AC: full core/app-server/small/lint suites and all 5
mutant kills are hosted-verified on the exact candidate tree (precheck 3).
Standing campaign bounds (foreign-exec fixtures, unrun remote/Windows lanes
beyond hosted CI) apply as usual and are not leaf gaps.

## Handoff preconditions (CR rev 2 → review)

1. Coverage map above covers all 3 surface rows, each with tests + a killed
   narrowing mutant (precheck 3 runs cited). No uncovered rows.
2. Landing-gate properties green: precheck 3 base run 37473988733, all 4
   lanes success on the exact tree.
3. Reviewer tests kept: no previously committed reviewer tests exist; the
   renamed producer exclusion test keeps its suspended/cancelled coverage
   under the corrected name, and the new production-path regression test is
   committed under `production_acknowledgement_removes_pending_work`.
4. Out of contract: consuming policy E2 (TASK-260929-2snjbb), explicitly out
   of scope per the task description. All 5 AC rows covered; no silent gaps.
5. Rework diff bounded: rev-2 production changes in
   `session/runtime_mailbox.rs`, `session/exec_completion_ack.rs`,
   `session/pending_work.rs` (docs only), `session/pending_work_tests.rs` —
   all inside the snapshot/ack module area the brief names. Nothing outside.

## Checklist basis (items 13–17, checked this run; 1–12 already checked)

13. Implementation matches AC — 5 of 5 AC rows driven (table above),
    precheck 3 green on this exact tree.
14. Solution fits project architecture — contracts in extension-api,
    policy-free snapshot in core session modules, goal reads via provider
    with no core→goal edge; no `list_processes`; reviewer architecture notes
    from rev 1 were nonblocking.
15. Tests green — precheck 3 run 37473988733: core, app-server, lint, small
    all success.
16. Gate/refusal/validation behavior attacked, not read — exclusion,
    contended-read, error-not-empty, atomicity and production-ack tests;
    5/5 narrowing mutants killed by named tests, 0 survivors.
17. Review verdict routed — rev-1 changes_requested answered: joint
    retirement fix + named regression test + narrowing mutant, precheck 3
    green; this handoff publishes CR rev 2 for re-review.

Candidate is left UNCOMMITTED in the Story worktree for the handoff to
snapshot. Handoff publishes CR revision 2.
