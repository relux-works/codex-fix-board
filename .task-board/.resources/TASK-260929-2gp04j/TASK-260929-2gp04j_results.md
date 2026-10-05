# TASK-260929-2gp04j (G2) — rev-3 results: every goal-state read failure revokes (precheck-6 handoff on rebased tree a8fc9e0c)

Round-2 verdict (`TASK-260929-2gp04j_review-verdict-rev2.md`): changes_requested,
three findings, all one repeat-of class (`CR-TASK-260929-2gp04j-1 /
accounting-read-failure-retains-capability`). This run fixes the CLASS: every
site in `ext/goal` that reads goal state and can fail now funnels the failure
through the single publisher (marker removed, reconciliation Unknown, error
reported) and recovers on the next lifecycle event. Fast lane is green
locally; the 3 new core tests, the 3 new core mutants and the re-run of the 15
kept mutants on the new tree need hosted precheck 4. Checklist execution items
(3, 6, 7, 10, 15, 16) were unchecked pending that evidence; this turn ends
with `HOSTED-PRECHECK-REQUESTED: precheck 4` and no handoff.

## Round-2 findings → root cause → rev-3 fix

All three panels found the same open window: revision 2 covered the four
turn-stop/abort exits, but other read sites still propagate a goal-store read
failure with `?` BEFORE the publisher reconciles, so a previously published
marker survives:

- `GoalService::set_thread_goal` (`api.rs`): the preparation/accounting error
  only warns, then either `get_thread_goal` error returns via `?` before
  `reconcile_live_activity`.
- `GoalService::flush_thread_goal_progress_for_fork` (`api.rs`): the
  preparation/accounting read error propagates to the fork response with no
  reconciliation of the source thread marker (reachable from production via
  app-server `thread_processor` → `thread_goal_processor`).
- `current_goal_status_for_metrics` reads (`runtime.rs`, called from the
  active/idle accounting paths): failures propagate before publication.
- `on_tool_finish` accounting `Err` arm (`extension.rs`): warns/returns after
  the leading successful reconcile, leaving a failure-between-reads window.

Fix (product code, about +40/−15, publisher stays the only writer):

- `runtime.rs`: new `GoalRuntimeHandle::revoke_live_activity_on_read_failure`
  — resolves the live thread store (same path `reconcile_live_activity`
  publishes through) and publishes `Err` through the existing
  `revoke_activity_on_read_failure` helper. No-op when the thread is gone;
  disable/stop already removed the marker.
- `api.rs` `set_thread_goal`: the prepare-error arm now revokes live before
  warn-and-continue; both `get_thread_goal` sites now go through the new
  `read_thread_goal_for_set` helper, which revokes live before returning the
  read error.
- `api.rs` `flush_thread_goal_progress_for_fork`: the prepare error now
  revokes live before it is returned.
- `extension.rs` `on_tool_finish` accounting `Err` arm: now revokes through
  the handler's thread store before warn + return (same shape as the four
  rev-2 arms).

No change was needed inside the shared accounting functions: revoking there
would have made the rev-2 turn-stop/abort mutants unkillable (the extension
arms would become redundant), so revocation stays at the call sites that
previously lacked it. Error propagation and reporting are unchanged
everywhere; only marker revocation was added.

The rev-2 "stated bound" claiming the `on_tool_finish` arm is untestable
without fault injection is SUPERSEDED: a `CREATE TRIGGER ...
RAISE(ABORT)` fault fails goal-table writes while leaving reads intact, so the
leading reconcile succeeds and accounting fails deterministically. No stated
bound remains for this leaf.

## Read-site sweep (every site in ext/goal that reads goal state and can fail)

Line numbers are this worktree (`codex-rs/ext/goal/src/`).

| # | Site | Kind | On failure (after rev-3) | Test driving the failure |
|---|---|---|---|---|
| 1 | `runtime.rs:157` `reconcile_activity` read | status read | publishes `Err` → marker removed, Unknown, error returned | small `read_failure_revokes_activity_and_next_turn_recovers` (kept) |
| 2 | `runtime.rs:172` `reconcile_live_activity` read | status read | same shared publish-`Err` branch; callers propagate only post-publication | shared branch with #1 + publisher unit test (kept); no stale marker possible by construction |
| 3 | `runtime.rs:460` stop's goal read | status read | `Err` to turn-stop arms (revoke, `extension.rs:345,356`) and turn-error (reconcile-after, `extension.rs:449`) | small `turn_error_read_failure_revokes_activity_and_next_turn_recovers` (NEW, rev-3) |
| 4 | `runtime.rs:806` metrics-status read, via `:684`/`:748` | status read | `Err` up through accounting to the call-site revoke/reconcile arms below | small turn-stop/abort tests (kept); core `fork_flush_read_failure_...` (NEW) |
| 5 | `api.rs:356` `read_thread_goal_for_set` read (both set branches) | status read | NEW: live revoke, then `Err` | core `external_set_get_failure_revokes_activity_and_next_turn_recovers` (NEW; both branches) |
| 6 | `api.rs:126` flush prepare, `api.rs:194` set prepare | accounting (read + write) | NEW: live revoke, then warn-and-continue (set) / `Err` (flush) | core `external_set_prepare_failure_...`, core `fork_flush_read_failure_...` (NEW) |
| 7 | `api.rs:314` clear prepare | accounting | warn-and-continue; committed clear then removes unconditionally (`:330`) | kept clear tests (incl. disabled-clear); delete-failure leaves committed state — and marker — accurate |
| 8 | `extension.rs:545` tool-finish accounting | accounting | NEW: revoke via thread store, then warn + return | small `tool_finish_accounting_failure_revokes_activity_and_next_turn_recovers` (NEW, rev-3) |
| 9 | `extension.rs:339,353,362,408` turn-stop/abort accounting+stop | accounting + status read | revoke (rev-2 arms, kept) | kept turn-stop/abort tests |
| 10 | `extension.rs:441` turn-error stop | accounting + status read + write | `Err` → warn, then reconcile-after (`:449`): persistent failure revokes, transient reconciles to truth | small `turn_error_read_failure_...` (NEW; also covers #3) |
| 11 | `tool.rs:192` unconditional post-tool reconcile | status read | persistent failure revokes here; refused/failed tools reconcile too | shared branch with #1; success paths covered by kept create/update tests |
| 12 | `tool.rs:209,425,369,293` get-handler and tool metrics reads | status read | tool `Err`, then the unconditional #11 reconcile | shared branch with #1 (harness cannot observe live paths by design; core suite covers live behavior) |
| 13 | `tool.rs:374`, `runtime.rs:690,754` accounting writes | read-modify-write | `Err` to #11 (tool) / call-site arms (runtime) | trigger tests: small tool-finish (NEW), core set-prepare (NEW) |
| 14 | `tool.rs:233,298`, `runtime.rs:485`, `api.rs:207,229,254` pure writes | insert/update/replace | committed state unchanged → marker stays accurate; runtime/api errors still hit the call-site revoke/reconcile arms (conservative) | kept create/update/stop/set tests; core set-prepare asserts the write-error message |
| 15 | `api.rs:321` clear's delete | delete | failure → committed clear did not happen → marker stays accurate; success → unconditional `clear_activity` | kept clear tests |
| 16 | `runtime.rs:551` continuation-deferral read | flag read, not goal status | `Err` AFTER the `:546` reconcile; marker already reflects committed state | none: not a goal-state read, no stale marker possible |
| 17 | `extension.rs:278` deferral clear | flag write | warn-only, AFTER the `:259` reconcile | none: same rationale as #16 |
| 18 | `api.rs:142` public `get_thread_goal` | pure read | error returned to the API caller; no lifecycle transition, marker untouched and still accurate | none: not a lifecycle path |

Out-of-contract rows: #16, #17 (continuation-deferral flag, not goal status;
AC 7 governs goal-state reads), #18 (pure API read, no lifecycle effect).
Every other row revokes through the single publisher and recovers on the next
lifecycle event; rows with no dedicated failure test cannot leave a stale
marker by construction (unconditional post-error reconcile through the shared,
tested publish-`Err` branch).

## Changed files (rev-3 rework delta; full leaf stays in scope)

- `ext/goal/src/runtime.rs`: +13/−0 (live revoke helper).
- `ext/goal/src/api.rs`: about +26/−15 (flush/set-prepare revokes,
  `read_thread_goal_for_set` helper used by both set branches).
- `ext/goal/src/extension.rs`: +1/−0 (tool-finish revoke arm).
- `ext/goal/tests/goal_extension_backend/goal_activity_tests.rs`: +100 (2
  regression tests).
- `core/tests/suite/goal_activity_tests.rs`: +310 (2 live-thread helpers + 3
  regression tests).
- `core/Cargo.toml`: +1 (`sqlx = { workspace = true }` dev-dep, same pin the
  goal crate already uses); `Cargo.lock`: +1 test-only edge.
- Rev-3 delta ≈ +450/−15. No `spec_plan`, extension-api, or
  automatic-continuation policy changes. `usage_limit_active_goal_for_turn`
  and `prepare_external_goal_mutation` have no production callers (verified by
  grep); their production entries (`on_turn_error`, set/clear/flush) are
  covered above.

## AC coverage map — 8 of 8 rows driven through production entries (kept + extended)

Rows 1–6 and 8 are unchanged from rev-2 (all previously committed reviewer
tests kept under their original names). AC 7 is extended:

| AC | Production entry / call site | Driving tests | Refusal / negative tests |
|---|---|---|---|
| 7 | read-failure → publisher error branch via turn-start reconcile, turn-stop/abort revokes (rev-2), turn-error reconcile-after, tool-finish revoke (NEW), set/flush live revokes (NEW) | kept: small `read_failure_...`, `turn_stop_...`, `turn_abort_...`; NEW small `tool_finish_accounting_failure_...`, `turn_error_read_failure_...`; NEW core `external_set_get_failure_...`, `external_set_prepare_failure_...`, `fork_flush_read_failure_...` | marker absent after each failure (absence never authorizes continuation); recovers on the next turn start with a higher revision |

Out-of-contract rows: none for the AC table. Stated bound: none (the rev-2
tool-finish bound is superseded — see above).

## Surface coverage map (1 of 1 rows)

| Surface row | Attacking tests | Narrowing mutants |
|---|---|---|
| goal activity publisher | all kept core/small/app-server tests + 5 new regression tests | 20/20 written; 2 killed locally on this tree, 18 pending hosted precheck 4 (0 survivors so far) |

## Narrowing-mutant evidence — 20 mutants (15 kept + 5 new)

Patches: outcome `TASK-260929-2gp04j_mutants.json` (20 patches; every patch
verified with strict `patch -p1 --dry-run` on this tree, 0 failures, and
re-verified after `just fmt`). The 15 kept patches apply unchanged (line
offsets only; no textual overlap with the rev-3 edits).

| Mutant | What it narrows the gate to | Named test that fails | Result |
|---|---|---|---|
| budget_limited_admits_continuation | (kept, precheck-3 killed) core `accounting_budget_keeps_sleep_without_automatic_continuation` | core lane | pending precheck-4 re-run |
| cleared_revision_accepts_old_read | (kept) small `publisher_refuses_stale_revision_and_recovers_unknown_state` | small lane | pending precheck-4 re-run |
| complete_retains_sleep | (kept) core `create_goal_changes_the_next_sampling_tools::complete` | core lane | pending precheck-4 re-run |
| create_waits_for_finish | (kept) core `clear_revokes_before_late_create_finish_and_stale_set_effects` | core lane | pending precheck-4 re-run |
| disable_preserves_active_marker | (kept) small `disable_and_stop_revoke_activity_and_pending_options` | small lane | pending precheck-4 re-run |
| disabled_clear_keeps_marker | (kept) core `clear_revokes_before_late_create_finish_and_stale_set_effects` | core lane | pending precheck-4 re-run |
| external_set_skips_budget_limited | (kept) core `external_set_and_resume_reconcile_first_request::budget_limited` | core lane | pending precheck-4 re-run |
| late_active_set_reinserts_cleared_goal | (kept) core `clear_revokes_before_late_create_finish_and_stale_set_effects` | core lane | pending precheck-4 re-run |
| resume_skips_budget_limited | (kept) core `external_set_and_resume_reconcile_first_request::budget_limited` | core lane | pending precheck-4 re-run |
| stop_preserves_active_marker | (kept) small `disable_and_stop_revoke_activity_and_pending_options` | small lane | pending precheck-4 re-run |
| timestamp_read_failure_keeps_known_marker | (kept) small `read_failure_revokes_activity_and_next_turn_recovers` | small lane | pending precheck-4 re-run |
| turn_start_requires_baseline | (kept) core `turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal` | core lane | pending precheck-4 re-run |
| usage_limit_retains_sleep | (kept) small `automatic_stop_revokes_activity_for_error_and_usage_limit` | small lane | pending precheck-4 re-run |
| turn_stop_read_failure_keeps_marker | (kept, rev-2) small `turn_stop_accounting_read_failure_revokes_activity_and_next_turn_recovers` | small lane | pending precheck-4 re-run |
| abort_read_failure_keeps_marker | (kept, rev-2) small `turn_abort_accounting_read_failure_revokes_activity_and_next_turn_recovers` | small lane | pending precheck-4 re-run |
| external_set_get_failure_keeps_marker (NEW) | external-set goal reads report without revoking | core `external_set_get_failure_revokes_activity_and_next_turn_recovers` | pending precheck 4 (core lane) |
| external_set_prepare_failure_keeps_marker (NEW) | external-set preparation reports without revoking | core `external_set_prepare_failure_revokes_activity_and_next_turn_recovers` | pending precheck 4 (core lane) |
| fork_flush_prepare_failure_keeps_marker (NEW) | fork flush reports without revoking | core `fork_flush_read_failure_revokes_activity_and_next_turn_recovers` | pending precheck 4 (core lane) |
| tool_finish_accounting_failure_keeps_marker (NEW) | tool-finish accounting errors report without revoking | small `tool_finish_accounting_failure_revokes_activity_and_next_turn_recovers` | KILLED locally (exit 100), reverted, suite green |
| turn_error_skips_reconcile_after_stop_failure (NEW) | turn-error stops report without reconciling after | small `turn_error_read_failure_revokes_activity_and_next_turn_recovers` | KILLED locally (exit 100), reverted, suite green |

Every mutant narrows (gate stays present, weakened to admit exactly one
member of the rejected class); no delete-only mutant is used as evidence.
No source-text gate was introduced, so no token-preserving mutant applies.
The two locally killed mutants were applied with `git apply`, failed with
exit 100 on exactly their named test, reverted with `git apply -R`, and the
suite re-ran 58/58 green.

Determinism notes for the hosted kills: the set-get test uses Plan-mode
turns (`account_tokens = false`), so preparation deterministically
short-circuits without touching the DB and the malformed-row failure lands
only in the set's read — a wall-clock tick cannot move it (verified in
`accounting.rs`: `progress_snapshot` returns `None` before any time check).
The trigger tests fail writes while reads succeed, isolating the
failure-between-reads windows. The turn-error kill does not depend on which
stop sub-path fails: every sub-path funnels through the removed
reconcile-after block.

## Validation and command evidence (this run; real exit codes, no pipes hiding status)

From `codex-rs/` with `NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no
INSTA_WORKSPACE_ROOT=$PWD`:

| Exact command | Exit code | Meaning |
|---|---|---|
| `python3 .../codex-fix-suite-busy.py --any` | 0 (`FREE`) | shared target free before the first build |
| `../.temp/goal-token-burn/impl/codex-target-guard.sh` (worktree root) | 0 | target guard cleaned workspace-member artifacts |
| `just fmt` | 0 | formatting applied |
| `just clippy -p codex-goal-extension -p codex-extension-api` | 0 | clippy incl. tests; 1 warning in untouched `core/src/tools/registry.rs` (not this leaf) |
| `just clippy -p codex-core` | 0 | type-checks the 3 new core tests; fixed 1 unused-import warning of mine; 2 remaining warnings pre-existing in untouched files |
| `just test -p codex-goal-extension -p codex-extension-api` | 0 | 58/58 pass (56 kept + 2 new) |
| focused mutant kills (2, then revert + full re-run) | 100 each (expected fail), then 0 | both new small-lane mutants killed locally |
| strict `patch -p1 --dry-run` for all 20 mutant patches | 0 failures | every mutant applies to this tree (re-checked after fmt) |

NOT run locally per the brief: `just test -p codex-core`,
`just test -p codex-app-server`, full `just test`. Their green on this tree
— including the 3 new core tests and all 20 mutant kills — comes only from
hosted precheck 4.

## Reviewer notes (kept + updated)

(a) `MODULE.bazel.lock`: no `just bazel-lock-update`. The only dependency
change is a test-only dev-dep edge (`codex-core` on the already-pinned
workspace `sqlx`, same pin `codex-goal-extension` already uses; no version
change, `Cargo.lock` gains one edge line). Per the rev-1/2 precedent this is
Bazel-irrelevant.

(b) Size: rev-3 rework delta ≈ +450/−15 (about +40/−15 production,
≈ +410 tests), inside `ext/goal` + `core` tests only; cumulative leaf
≈ 1970 lines. The two-stage upstream split from precheck 2 still stands, and
per the rework briefs the leaf is not split now — the upstream PR will be
staged later.

## Outcome-scoped logbook

- The class is closed at call sites, deliberately NOT inside the shared
  accounting functions: a central revoke there would have made the rev-2
  turn-stop/abort mutants unkillable. Any future accounting caller must
  revoke-or-reconcile on error at its own site (see sweep rows #6, #8–#10).
- `CREATE TRIGGER ... RAISE(ABORT)` is the leaf's write-only fault injector:
  reads succeed, writes fail, isolating failure-between-reads windows
  (tool-finish, set-prepare) that persistent row corruption cannot reach.
- Plan-mode setup turns (`account_tokens = false`) deterministically
  short-circuit preparation without DB reads; Default-mode setup without
  recorded usage is NOT deterministic for mutant isolation (a 1s wall-clock
  tick yields a snapshot and moves the failure into preparation).
- Harness `ThreadManager` stays dead (`Weak::new()`), so live-path
  (`GoalService`) revokes are observable only in the core suite with real
  threads — hence the 3 new core tests and the core `sqlx` dev-dep.
- Checklist items 3, 6, 7, 10, 15, 16 were unchecked this turn: their rev-2
  green described the old tree. They re-check only on precheck-4 evidence
  for this tree, with no code change after the snapshot.

---

# Addendum — p4 fix run (2026-10-04): the turn_start_requires_baseline "survivor" is a scrape artifact; 20/20 killed, zero code change

`g2-fix-note-p4.md` asked to restore a test killing
`turn_start_requires_baseline`, on the premise that precheck-4's JSON showed
it surviving (no test failed). That premise is factually wrong: the JSON was
scraped while the mutant run's core/app-server lanes were still running
(`"core": ""`, `"app-server": ""`), so its fails list was empty. The
completed run kills the mutant. No test was weakened by rev-3, no product
path changed for turn start, and any edit now would INVALIDATE the green
precheck-4 snapshot — so this run changes zero files.

## Identity (evidence applies to this exact tree)

- Worktree tree (temp index, `git read-tree HEAD` + `git add -A` +
  `git write-tree`): `fc288cc9d009923ec84e87428669fc51030712a4`
- Precheck-4 snapshot commit `43735cd7e65175d95dcaa25a80f85fcd8ad3a266`
  tree: `fc288cc9d009923ec84e87428669fc51030712a4` — byte-identical.
  `git status` shows only the rev-3 candidate files, uncommitted, on
  checkpoint `58042581a0`; the cancelled run made no changes.
- Mutant commit `57ec751cc43b43ec216fbfa02c960315b0fbae42` diffed against
  the snapshot: exactly the 3-line `turn_start_requires_baseline` patch in
  `ext/goal/src/extension.rs` (early return when
  `token_usage_at_turn_start.is_none()`, before `reconcile_activity`).
  The kill below is genuine, not a broken-build artifact.

## The kill (run 37222366509, completed AFTER the precheck-4 scrape)

- Lanes now: app-server success, small success, lint success,
  **core failure**.
- Core log: `TRY 3 FAIL ... codex-core::all
  suite::goal_activity::turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal`
  — the intended test fails 3/3 in 0.24–0.29 s each (fast, deterministic,
  not a timing flake). Snapshot core on the unmutated tree is green, so the
  mutant's skip of baseline-less reconciliation is exactly what the test
  detects (marker stays `None` at the `is_some()` assertion).
- One EXTRA core failure on that run:
  `suite::scenarios::guardian_agent_messages::encrypted_parent_reply_survives_incremental_guardian_reviews`
  (10.4 s). Unrelated single occurrence: it passed on the snapshot and on
  every other mutant run, its source sets up no goals (exec/guardian
  messaging only), and the mutant only removes goal-reconcile work — it
  cannot plausibly change that test's behavior. Reported as flaky, not
  signal; it does not affect the kill verdict.

## Corrected precheck-4 verdict: 20/20 killed (re-scrape of the same 21 runs)

Re-ran `precheck-analyze.py` on `p2/g2-precheck-4.runs` after all runs
completed (output attached as
`TASK-260929-2gp04j_precheck4-rescrape.json`; the script's own `killed`
flags stay false because `mutants.json` carries killing tests in this
results file, not in a `test` field — kills below are computed against the
intended-test mapping in the rev-3 table above).

| Mutant | Run | Intended test failed? | Extra fails |
|---|---|---|---|
| abort_read_failure_keeps_marker | 37222128124 | yes (small) | — |
| budget_limited_admits_continuation | 37222142771 | yes (core) | — |
| cleared_revision_accepts_old_read | 37222157519 | yes (small) | — |
| complete_retains_sleep | 37222172211 | yes (`complete`, core) | `created` (same family) |
| create_waits_for_finish | 37222186460 | yes (core) | `disable_mid_turn_...` (same family) |
| disable_preserves_active_marker | 37222200837 | yes (small) | — |
| disabled_clear_keeps_marker | 37222213853 | yes (core) | — |
| external_set_get_failure_keeps_marker | 37222226806 | yes (core) | — |
| external_set_prepare_failure_keeps_marker | 37222240871 | yes (core) | — |
| external_set_skips_budget_limited | 37222254580 | yes (core) | — |
| fork_flush_prepare_failure_keeps_marker | 37222268363 | yes (core) | — |
| late_active_set_reinserts_cleared_goal | 37222283603 | yes (core) | — |
| resume_skips_budget_limited | 37222297485 | yes (core) | — |
| stop_preserves_active_marker | 37222311043 | yes (small) | — |
| timestamp_read_failure_keeps_known_marker | 37222324282 | yes (small) | 3 same-family read-failure tests |
| tool_finish_accounting_failure_keeps_marker | 37222337369 | yes (small) | — |
| turn_error_skips_reconcile_after_stop_failure | 37222351546 | yes (small) | `automatic_stop_...` (same family) |
| **turn_start_requires_baseline** | **37222366509** | **yes (core, 3/3)** | guardian test (unrelated flake, see above) |
| turn_stop_read_failure_keeps_marker | 37222381228 | yes (small) | — |
| usage_limit_retains_sleep | 37222394888 | yes (small) | — |

Snapshot run 37222115113: green on all four lanes, zero fails.
**Mutant survivors: 0.**

## What this run did and did not do

- Did: verified tree identity, verified the mutant commit diff, inspected
  the completed mutant run's core log, re-scraped all 21 precheck-4 runs,
  attached the corrected JSON. `TASK-260929-2gp04j_mutants.json` on the
  board is byte-identical to the `g2-mutants-4.json` used for precheck 4 —
  kept as-is (20/20).
- Did not: change any file (no product, test, or mutant change — there is
  nothing to restore). No local cargo/just build or test was run: the
  hosted snapshot evidence is bound to this exact unchanged tree, so a
  local rebuild would only burn shared-target time (brief rule 10: reuse
  exact green evidence). Fast-lane commands therefore report as
  intentionally-not-rerun, not as missing.
- Checklist items 3, 6, 7, 10, 15, 16 stay UNCHECKED in this turn: they
  re-check on the orchestrator's precheck-5 confirmation of this evidence,
  with still no code change after the snapshot. This turn ends with
  `HOSTED-PRECHECK-REQUESTED: precheck 5` and no handoff, per the fix note.
  Precheck 5 needs no new CI: the 21 runs above are complete and conclusive;
  a re-scrape confirmation (or the attached JSON) suffices unless board
  policy requires a fresh run.
- Reviewer notes (a) `MODULE.bazel.lock` (no update needed) and (b) size
  (≈1970 lines cumulative, two-stage upstream split stands, no split now)
  are unchanged from rev-3.

## Outcome-scoped logbook (p4)

- `precheck-analyze.py` records empty-string lane conclusions for still
  running jobs and an empty fails list for them — indistinguishable from a
  genuine survivor in its JSON. Any "survivor" with `""` lanes must be
  re-scraped after run completion before a fix run is spawned.
- The script's `killed` field is always false for this leaf because kills
  are keyed to the results-file mapping, not a `test` field in
  `mutants.json`. Kill verdicts for G2 must be computed from the
  `meaningful` fails lists, as done above.

---

# Addendum — precheck-5 handoff (2026-10-05): CR rev 3 handed off on 20/20 kills, zero code change

This turn performs `g2-handoff-note-5.md`: tree re-verified byte-identical to the
precheck-5 snapshot, results refreshed, open checklist items checked on hosted
evidence, busy check FREE, then developer handoff (CR rev 3, story_final).
No worktree file was changed in this turn; a change would have invalidated the
evidence below.

## 1. Identity (this exact tree)

- Worktree tree (temp index, `git read-tree HEAD` + `git add -A` +
  `git write-tree`, this turn): `fc288cc9d009923ec84e87428669fc51030712a4`
- Precheck-5 snapshot `225257e2815e260abd52de3ce5323f6fa975e1d5` tree:
  `fc288cc9d009923ec84e87428669fc51030712a4` — byte-identical.
- HEAD (checkpoint): `58042581a0b507ae62e7b1d8381c429baea1f689`; 17
  uncommitted paths (the rev-3 candidate only); index otherwise empty.
- `TASK-260929-2gp04j_mutants.json` on the board is unchanged (20 patches, the
  same set precheck 5 ran).

## 2. Hosted snapshot: green on all lanes

- Run https://github.com/relux-works/codex/actions/runs/37238654545:
  lint success, small success, core success, app-server success; zero fails.
- This run executed the exact candidate tree, including the 5 rev-3 regression
  tests (2 small, 3 core) and all previously committed reviewer tests under
  their original names. Precheck-1's `disable_mid_turn_...` failure stays
  fixed; precheck-4's scrape artifact is superseded by the fresh precheck-5
  kill of `turn_start_requires_baseline` below.

## 3. Narrowing-mutant evidence — 20 of 20 killed (precheck 5)

Source: `.temp/goal-token-burn/impl/p2/g2-precheck-5-results.json` (21 runs,
all completed; the script's own `killed` flags stay false because kills are
keyed to the results-file mapping, not a `test` field in mutants.json — kills
below are computed from each run's `meaningful` fails list against the
intended-test mapping in the rev-3 table above; every mutant run failed at
least its intended test while the snapshot run is green).

| Mutant | Run | Intended killing test failed? | Lane |
|---|---|---|---|
| abort_read_failure_keeps_marker | 37238669815 | turn_abort_accounting_read_failure_revokes_activity_and_next_turn_recovers | small |
| budget_limited_admits_continuation | 37238683915 | accounting_budget_keeps_sleep_without_automatic_continuation | core |
| cleared_revision_accepts_old_read | 37238697534 | publisher_refuses_stale_revision_and_recovers_unknown_state | small |
| complete_retains_sleep | 37238710305 | create_goal_changes_the_next_sampling_tools::complete (+created, same family) | core |
| create_waits_for_finish | 37238723123 | clear_revokes_before_late_create_finish_and_stale_set_effects (+disable_mid_turn, same family) | core |
| disable_preserves_active_marker | 37238736946 | disable_and_stop_revoke_activity_and_pending_options (+2 same-family core) | small+core |
| disabled_clear_keeps_marker | 37238750603 | clear_revokes_before_late_create_finish_and_stale_set_effects | core |
| external_set_get_failure_keeps_marker (rev-3) | 37238763892 | external_set_get_failure_revokes_activity_and_next_turn_recovers | core |
| external_set_prepare_failure_keeps_marker (rev-3) | 37238776940 | external_set_prepare_failure_revokes_activity_and_next_turn_recovers | core |
| external_set_skips_budget_limited | 37238789256 | external_set_and_resume_reconcile_first_request::budget_limited | core |
| fork_flush_prepare_failure_keeps_marker (rev-3) | 37238802281 | fork_flush_read_failure_revokes_activity_and_next_turn_recovers | core |
| late_active_set_reinserts_cleared_goal | 37238817400 | clear_revokes_before_late_create_finish_and_stale_set_effects | core |
| resume_skips_budget_limited | 37238831474 | external_set_and_resume_reconcile_first_request::budget_limited | core |
| stop_preserves_active_marker | 37238844768 | disable_and_stop_revoke_activity_and_pending_options | small |
| timestamp_read_failure_keeps_known_marker | 37238856407 | read_failure_revokes_activity_and_next_turn_recovers (+5 same-family) | small+core |
| tool_finish_accounting_failure_keeps_marker (rev-3) | 37238868235 | tool_finish_accounting_failure_revokes_activity_and_next_turn_recovers | small |
| turn_error_skips_reconcile_after_stop_failure (rev-3) | 37238882003 | turn_error_read_failure_revokes_activity_and_next_turn_recovers (+automatic_stop, same family) | small |
| turn_start_requires_baseline | 37238895616 | turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal (3/3, precheck-4 survivor now killed) | core |
| turn_stop_read_failure_keeps_marker | 37238908004 | turn_stop_accounting_read_failure_revokes_activity_and_next_turn_recovers | small |
| usage_limit_retains_sleep | 37238920002 | automatic_stop_revokes_activity_for_error_and_usage_limit (+usage_limited, same family) | small+core |

Mutant survivors: 0. Every mutant narrows (gate stays present, weakened to
admit exactly one member of the rejected class); no delete-only mutant is used
as evidence. No source-text gate exists, so no token-preserving mutant
applies.

## 4. Round-2 verdict findings — answered in this revision (repeat-of class)

All three rev-2 findings share the repeat-of class
`accounting-read-failure-retains-capability`; rev-3 closed the class at every
call site (sweep table rows #1–#15 above, unchanged by this turn). Each finding
gets its named regression tests + narrowing mutants in this leaf:

| Verdict finding | Rev-3 fix (call sites) | Named regression tests | Narrowing mutants |
|---|---|---|---|
| accounting-read-failure (fork flush + on_tool_finish) | api.rs flush prepare revokes live; extension.rs tool-finish Err arm revokes; runtime metrics reads funnel to call-site arms | core fork_flush_read_failure_...; small tool_finish_accounting_failure_... | fork_flush_prepare_failure_keeps_marker; tool_finish_accounting_failure_keeps_marker |
| accounting-read-failure (set_thread_goal + on_tool_finish) | api.rs set prepare revokes live; both set get_thread_goal reads go through read_thread_goal_for_set (revoke-then-Err) | core external_set_get_failure_... (both branches); core external_set_prepare_failure_...; small tool_finish_... | external_set_get_failure_keeps_marker; external_set_prepare_failure_keeps_marker; tool_finish_accounting_failure_keeps_marker |
| external-accounting-read-failure (set + flush + metrics + tool-finish) | same three sites as above, plus turn-error reconcile-after (extension.rs :443-449) for the stop-failure window | above four + small turn_error_read_failure_... | above four + turn_error_skips_reconcile_after_stop_failure |

No stated bound remains (the rev-2 tool-finish bound is superseded by the
write-only trigger fault, rev-3 section above).

## 5. Coverage maps (unchanged code, refreshed citations)

- AC table: 8 of 8 rows driven through production entries (rev-3 map above
  still exact; rows 1–6 and 8 kept, row 7 extended with the 5 new tests).
  Out-of-contract AC rows: none. Stated bound: none.
- Surface table: 1 of 1 rows (`goal activity publisher`) covered — all kept
  core/small/app-server tests + 5 new regression tests, 20/20 narrowing
  mutants killed on this tree.
- Sweep-table out-of-contract rows: #16, #17 (continuation-deferral flag, not
  goal status; AC 7 governs goal-state reads), #18 (pure API read, no
  lifecycle effect). Every other sweep row revokes through the single
  publisher and recovers on the next lifecycle event.
- Rework diff bounded: rev-3 delta stayed inside `ext/goal` + `core` tests
  (+1 test-only dev-dep edge); this handoff turn changes zero files.

## 6. Checklist execution items — checked on precheck-5 evidence

- Item 3 (tests written for new/changed behavior): 5 new regression tests
  listed above, green on snapshot run 37238654545.
- Item 6 (negative/refusal tests at production call sites): every AC refusal
  (failed create, cleared/no-goal turn start, non-Active/BudgetLimited
  resume/set, complete/blocked/paused removal, disabled clear, disable/stop,
  read-failure absence-never-authorizes) driven and green on the snapshot.
- Item 7 (narrowing mutant per gate): 20/20 killed, table in section 3.
- Item 10 (build/validation green): snapshot run green on all four lanes
  (lint/small/core/app-server) on this exact tree; local fast-lane green
  from the rev-3 run (fmt 0, clippy 0, small tests 58/58) is reused under
  unchanged identity (brief rule 10) — no rebuild in this zero-change turn.
- Item 15 (tests green): snapshot run 37238654545, zero fails.
- Item 16 (gates attacked, not read): section 3 kills prove each gate; no
  positive-path-only evidence.

## 7. Reviewer notes (kept)

(a) `MODULE.bazel.lock`: no `just bazel-lock-update`. The only dependency
change remains the test-only dev-dep edge (`codex-core` on the already-pinned
workspace `sqlx`, same pin `codex-goal-extension` already uses; no version
change, `Cargo.lock` gains one edge line). Per the rev-1/2 precedent this is
Bazel-irrelevant; the board's landing gate re-verifies.

(b) Size: cumulative leaf ≈ 1970 lines (rev-3 rework delta ≈ +450/−15, about
+40/−15 production and ≈ +410 tests; earlier 1334-line note predates the two
court-ordered reworks). The two-stage upstream split from precheck 2 still
stands, and per the rework briefs the leaf is not split now — the upstream PR
will be staged later. G2 is the Story's final leaf, so this handoff publishes
the story_final CR.

## 8. Commands run in this handoff turn (real exit codes, no hidden pipes)

| Exact command | Exit code | Meaning |
|---|---|---|
| `task-board m 'set_status(TASK-260929-2gp04j, status=development)'` | 0 | run start |
| temp-index `git read-tree HEAD` + `git add -A` + `git write-tree` | 0, tree fc288cc9... | identity matches precheck-5 snapshot |
| `task-board resource get` × 4 (results, mutants, verdict-rev2, hosted-precheck-5) | 0 | evidence staged under /tmp |
| `python3 .../codex-fix-suite-busy.py --any` | 0 (`FREE`) | shared target free; handoff allowed |
| `task-board resource update ... results_handoff.md` + `check_item` × 6 + `handoff` | see board receipts | this handoff |

NOT run in this turn, by design: no `cargo`/`just` build or test (zero file
changes — rerunning would burn shared-target time and cannot add evidence
beyond the hosted snapshot bound to this exact tree; brief rule 10: reuse
exact green evidence). No local mutant execution (all 20 kills are hosted).
Unverified locally: nothing new — the hosted snapshot + 20 mutant runs are the
verification, and they are complete.

## 9. Outcome-scoped logbook (handoff)

- Precheck 5 supersedes the precheck-4 scrape debate: the same tree was run
  fresh (snapshot 37238654545 + 20 mutant runs, all completed), and the former
  `turn_start_requires_baseline` survivor is killed by its original intended
  test with no code or test change — confirming the scrape-artifact diagnosis.
- `precheck-analyze.py` empty-string lanes mean "still running", not
  "survived"; G2 kill verdicts must be computed from `meaningful` fails
  against the results-file mapping.
- Handoff discipline held: zero worktree writes in this turn, results refreshed
  as a board resource only, checklist checked solely on the cited hosted runs.

---

# Addendum — precheck-6 handoff (2026-10-05): CR rev 3 on the rebased tree, 20/20 killed, zero code change

This turn performs `g2-handoff-note-6.md`: the tree was re-verified
byte-identical to the precheck-6 snapshot (rebased on trunk 729f259e62, P5-B),
results refreshed, busy check FREE, then developer handoff (CR rev 3,
story_final). No worktree file was changed in this turn; a change would have
invalidated the evidence below. The earlier precheck-5 handoff attempt was
refused with `change_request_base_authority_mismatch` (trunk moved); the
rebase run (`TASK-260929-2gp04j_refresh6.md`) replayed G1 onto the new trunk
with no conflicts and restored the 12 disjoint P5-B files, keeping the G2
delta byte-identical. Precheck 6 re-ran everything on the new tree.

## 1. Identity (this exact tree)

- Worktree tree (temp index, `git read-tree HEAD` + `git add -A` +
  `git write-tree`, this turn): `a8fc9e0cc6e0aad477aba7cd377e3c93203932fe`
- Precheck-6 snapshot `622007038bd2422ab19b446331ad21733f93e693` tree:
  `a8fc9e0cc6e0aad477aba7cd377e3c93203932fe` — byte-identical.
- HEAD (checkpoint): `31655cd8b5f8c57032d42c3b3907c6fee88b0580` (G1 replay on
  trunk 729f259e62); uncommitted paths are the rev-3 G2 candidate only.
- `TASK-260929-2gp04j_mutants.json` on the board is unchanged (20 patches, the
  same set precheck 6 ran; all applied cleanly to the rebased tree).

## 2. Hosted snapshot: green on all lanes

- Run https://github.com/relux-works/codex/actions/runs/37247519316:
  lint success, small success, core success, app-server success; zero fails.
- This run executed the exact rebased candidate tree, including the 5 rev-3
  regression tests (2 small, 3 core) and all previously committed reviewer
  tests under their original names.

## 3. Narrowing-mutant evidence — 20 of 20 killed (precheck 6)

Source: `.temp/goal-token-burn/impl/p2/g2-precheck-6-results.json` (21 runs,
all completed; kills computed from each run's `meaningful` fails list against
the intended-test mapping in the rev-3 table above; every mutant run failed at
least its intended test while the snapshot run is green).

| Mutant | Run | Intended killing test failed? | Lane |
|---|---|---|---|
| abort_read_failure_keeps_marker | 37247532651 | turn_abort_accounting_read_failure_revokes_activity_and_next_turn_recovers | small |
| budget_limited_admits_continuation | 37247546675 | accounting_budget_keeps_sleep_without_automatic_continuation | core |
| cleared_revision_accepts_old_read | 37247559858 | publisher_refuses_stale_revision_and_recovers_unknown_state | small |
| complete_retains_sleep | 37247573068 | create_goal_changes_the_next_sampling_tools::complete (+created, same family; app-server lane also fails, same as p4/p5) | core |
| create_waits_for_finish | 37247586601 | clear_revokes_before_late_create_finish_and_stale_set_effects (+disable_mid_turn, same family) | core |
| disable_preserves_active_marker | 37247600596 | disable_and_stop_revoke_activity_and_pending_options (+2 same-family core) | small+core |
| disabled_clear_keeps_marker | 37247613580 | clear_revokes_before_late_create_finish_and_stale_set_effects (+guardian flake, see below) | core |
| external_set_get_failure_keeps_marker (rev-3) | 37247625615 | external_set_get_failure_revokes_activity_and_next_turn_recovers (+realtime flake, see below) | core |
| external_set_prepare_failure_keeps_marker (rev-3) | 37247638426 | external_set_prepare_failure_revokes_activity_and_next_turn_recovers | core |
| external_set_skips_budget_limited | 37247651469 | external_set_and_resume_reconcile_first_request::budget_limited | core |
| fork_flush_prepare_failure_keeps_marker (rev-3) | 37247664735 | fork_flush_read_failure_revokes_activity_and_next_turn_recovers | core |
| late_active_set_reinserts_cleared_goal | 37247740659 | clear_revokes_before_late_create_finish_and_stale_set_effects | core |
| resume_skips_budget_limited | 37247752988 | external_set_and_resume_reconcile_first_request::budget_limited | core |
| stop_preserves_active_marker | 37247768409 | disable_and_stop_revoke_activity_and_pending_options | small |
| timestamp_read_failure_keeps_known_marker | 37247783331 | read_failure_revokes_activity_and_next_turn_recovers (+5 same-family read-failure tests) | small+core |
| tool_finish_accounting_failure_keeps_marker (rev-3) | 37247799080 | tool_finish_accounting_failure_revokes_activity_and_next_turn_recovers | small |
| turn_error_skips_reconcile_after_stop_failure (rev-3) | 37247813762 | turn_error_read_failure_revokes_activity_and_next_turn_recovers (+automatic_stop, same family) | small |
| turn_start_requires_baseline | 37247826655 | turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal | core |
| turn_stop_read_failure_keeps_marker | 37247839168 | turn_stop_accounting_read_failure_revokes_activity_and_next_turn_recovers | small |
| usage_limit_retains_sleep | 37247852091 | automatic_stop_revokes_activity_for_error_and_usage_limit (+usage_limited, same family) | small+core |

Mutant survivors: 0. Every mutant narrows (gate stays present, weakened to
admit exactly one member of the rejected class); no delete-only mutant is used
as evidence. No source-text gate exists, so no token-preserving mutant
applies.

Extra-fail analysis (each a single occurrence across all 21 precheck-6 runs,
green on the snapshot and on every other mutant run):
- `encrypted_parent_reply_survives_incremental_guardian_reviews` on the
  disabled_clear run: the same exec/guardian-messaging test already diagnosed
  as an unrelated flake in the p4 addendum (sets up no goals; the mutant only
  removes goal-revoke work). Third occurrence pattern, still 1-per-21.
- `conversation_second_start_replaces_runtime` on the external_set_get_failure
  run: a realtime-voice websocket test (`core/tests/suite/realtime_conversation.rs:2497`)
  with 2-second handshake waits — timing-sensitive, sets up no goals, and the
  mutant only changes goal-set read-failure handling. Reported as flaky, not
  signal; it does not affect the kill verdict (the intended test fails).
- `complete_retains_sleep` fails the app-server lane as well as core, with
  fails exactly `["complete", "created"]` — identical shape in prechecks 4, 5
  and 6, so deterministic same-mutant behavior, not a new signal. The kill is
  by the intended core test.

## 4. Round-2 verdict findings — answered in this revision (repeat-of class)

Unchanged from the precheck-5 addendum (section 4 above): all three rev-2
findings share the repeat-of class
`accounting-read-failure-retains-capability`; rev-3 closed the class at every
call site (sweep table rows #1–#15, byte-identical G2 content on the new
base). Each finding keeps its named regression tests + narrowing mutants in
this leaf; no stated bound remains.

## 5. Coverage maps (rebased tree, same G2 content)

- AC table: 8 of 8 rows driven through production entries (rev-3 map still
  exact; rows 1–6 and 8 kept, row 7 extended with the 5 new tests).
  Out-of-contract AC rows: none. Stated bound: none.
- Surface table: 1 of 1 rows (`goal activity publisher`) covered — all kept
  core/small/app-server tests + 5 new regression tests, 20/20 narrowing
  mutants killed on this tree.
- Sweep-table out-of-contract rows: #16, #17 (continuation-deferral flag, not
  goal status; AC 7 governs goal-state reads), #18 (pure API read, no
  lifecycle effect). Every other sweep row revokes through the single
  publisher and recovers on the next lifecycle event.
- Rework diff bounded: rev-3 delta stayed inside `ext/goal` + `core` tests
  (+1 test-only dev-dep edge); the rebase touched only the base + 12 disjoint
  P5-B trunk files; this handoff turn changes zero files.

## 6. Checklist — already checked, re-verified on precheck-6 evidence

All 17 items show done from the precheck-5 handoff turn; the rebase moved the
base, so the execution items are re-cited here on the precheck-6 runs (no
code change after the precheck-6 snapshot, so no re-check action was needed):
- Item 3 (tests for new/changed behavior): 5 rev-3 regression tests, green on
  snapshot run 37247519316.
- Item 6 (negative/refusal tests at production call sites): every AC refusal
  driven and green on the snapshot.
- Item 7 (narrowing mutant per gate): 20/20 killed, table in section 3.
- Item 10 (build/validation green): snapshot green on all four lanes on this
  exact tree; fast-lane green from the refresh run (fmt 0, clippy 0 on
  goal/api/core/app-server, small tests 58/58) reused under unchanged
  identity (brief rule 10).
- Item 15 (tests green): snapshot run 37247519316, zero fails.
- Item 16 (gates attacked, not read): section 3 kills prove each gate; no
  positive-path-only evidence.

## 7. Reviewer notes (kept)

(a) `MODULE.bazel.lock`: no `just bazel-lock-update`. The only dependency
change remains the test-only dev-dep edge (`codex-core` on the already-pinned
workspace `sqlx`, same pin `codex-goal-extension` already uses; no version
change, `Cargo.lock` gains one edge line). Per the rev-1/2 precedent this is
Bazel-irrelevant; the board's landing gate re-verifies.

(b) Size: cumulative leaf ≈ 1970 lines (rev-3 rework delta ≈ +450/−15, about
+40/−15 production and ≈ +410 tests; the earlier 1334-line note predates the
two reworks). The two-stage upstream split from precheck 2 still stands, and
per the rework briefs the leaf is not split now — the upstream PR will be
staged later. G2 is the Story's final leaf, so this handoff publishes the
story_final CR.

## 8. Commands run in this handoff turn (real exit codes, no hidden pipes)

| Exact command | Exit code | Meaning |
|---|---|---|
| `task-board m 'set_status(TASK-260929-2gp04j, status=development)'` | 0 | run start |
| temp-index `git read-tree HEAD` + `git add -A` + `git write-tree` | 0, tree a8fc9e0c... | identity matches precheck-6 snapshot |
| `task-board resource get` (results, refresh6, mutants) | 0 | evidence staged under /tmp |
| `python3 .../codex-fix-suite-busy.py --any` | 0 (`FREE`, twice) | shared target free; handoff allowed |
| `task-board resource update ... results` + `handoff` | see board receipts | this handoff |

NOT run in this turn, by design: no `cargo`/`just` build or test (zero file
changes — rerunning would burn shared-target time and cannot add evidence
beyond the hosted snapshot bound to this exact tree; brief rule 10: reuse
exact green evidence). No local mutant execution (all 20 kills are hosted).
Unverified locally: nothing new — the hosted snapshot + 20 mutant runs are the
verification, and they are complete.

## 9. Outcome-scoped logbook (precheck-6 handoff)

- The rebase preserved the G2 delta byte-identically (refresh contract), and
  precheck 6 confirms it independently: the same 20 mutants are killed by the
  same intended tests on the new tree, with the same `complete_retains_sleep`
  app-server co-failure seen in p4/p5.
- Two 1-in-21 flakes (`encrypted_parent_reply_..._guardian_reviews`,
  `conversation_second_start_replaces_runtime`) each ride a mutant run whose
  intended test also fails; neither affects any kill verdict. Both are
  timing-sensitive non-goal tests, green on the snapshot.
- Handoff discipline held: zero worktree writes in this turn, results refreshed
  as a board resource only, evidence cited solely from the completed hosted runs.

---

# Addendum — rev-4 rework (2026-10-05): one structural settlement guard; precheck 7 requested

Round-3 verdict (`TASK-260929-2gp04j_review-verdict-rev3.md`): changes_requested,
4 findings, all repeat-of `accounting-read-failure-retains-capability`. Per-site
arms keep leaking: `set_thread_goal`'s `update/replace_thread_goal` errors and
`clear_thread_goal`'s `delete_thread_goal` errors escape via `?` before the
publisher settles, and the store methods are read-modify-return (a write may
commit before a post-write read or row decode fails), so an error does NOT mean
"no committed change". This run implements the rev-4 brief's structural fix.
Fast lane is green locally; the 3 new core tests, the strengthened prepare
test, and all 25 mutant kills need hosted precheck 7. Execution checklist items
3, 5, 6, 7, 10, 15, 16 are unchecked pending that evidence; this turn ends with
`HOSTED-PRECHECK-REQUESTED: precheck 7` and no handoff.

## The guard (one mechanism, four sites)

`GoalService::guard_live_store_result` (`ext/goal/src/api.rs:389-404`, new):
takes the live runtime plus a store-call `Result`; `Ok` passes through to the
existing success settlement (reconcile/clear), ANY `Err` — including errors
after a committed write — revokes the live marker through the sole publisher
(`revoke_live_activity_on_read_failure`: marker removed, reconciliation
Unknown, error reported) before the original error is returned. The next
legitimate lifecycle event reconciles again. The publisher stays the only
writer: the guard calls the existing revoke helper and touches no
`GoalActivity` state directly.

Routed through it (the only product-code change besides the guard itself):

| Site (`api.rs`) | Previously | Now |
|---|---|---|
| `:205` set objective-branch `update_thread_goal` | `?` escaped before `reconcile_live_activity` | guard revokes, then `?` |
| `:233` set `replace_thread_goal` (no existing goal) | same leak | guard revokes, then `?` |
| `:264` set status-only `update_thread_goal` | same leak | guard revokes, then `?` |
| `:342` clear `delete_thread_goal` | `?` escaped before `clear_activity` | guard revokes, then `?` |

Deliberately NOT changed, with the reason each stays safe:

- Clear prepare (`:328-337`) stays warn-and-continue: the guarded delete
  always runs next and settles BOTH of its outcomes (success → unconditional
  `clear_activity`; error → guard revoke), so a prepare failure cannot strand
  a stale marker. Rationale comment added at `:332-335`. New T3 drives
  prepare-failure-before-write and proves the settlement.
- Set prepare arm and `read_thread_goal_for_set` keep their direct revokes
  byte-identical: kept mutants 16/17 narrow those exact lines, so any rewrite
  would break their patches. They remain the first revoke on their paths.
- Flush, tool handle, turn hooks, shared accounting: each already settles
  every error exit through exactly one mechanism (single armed exit /
  unconditional post-reconcile / propagate-to-armed-caller — every production
  caller verified armed by grep; `usage_limit_active_goal_for_turn` and
  `prepare_external_goal_mutation` have no production callers). Routing them
  through the guard as well would add redundant revokes and void the kept
  narrowing mutants (the rev-3 logbook precedent).

Subsumption note (why the prepare test needed strengthening, and why that is
honest): any fix for the set-write hole necessarily makes the set-prepare arm
redundant on error-ending paths — the write error now revokes too — while on
success-ending paths the success reconcile republishes truth anyway. The arm
still fires first (defense in depth, mutant continuity); the strengthened
test proves it fires via an exact revision count (see below), which is
deterministic here: single-threaded test, permit held across the set, and
`publish(Err)` bumps the revision unconditionally.

## Sweep table, rev-4 (every goal-state read/write site; guard pointers)

Line numbers are this worktree. Rows marked GUARD are new or corrected in
rev-4; rows 7/14/15 supersede the rev-3 statements the verdict disproved
(an error no longer implies "no committed change").

| # | Site | Kind | On failure (after rev-4) | Test driving the failure |
|---|---|---|---|---|
| 1 | `runtime.rs:157` `reconcile_activity` read | status read | publishes `Err` → removed, Unknown, error returned | small `read_failure_...` (kept) |
| 2 | `runtime.rs:172` `reconcile_live_activity` read | status read | same shared publish-`Err` branch | shared branch with #1 (kept) |
| 3 | `runtime.rs:460` stop's goal read | status read | `Err` to turn-stop revoke arms / turn-error reconcile-after | small `turn_error_...` (kept) |
| 4 | `runtime.rs:806` metrics-status read, via `:684`/`:748` | status read | `Err` to call-site arms (all production callers armed; the two `pub` fns have no production callers) | kept turn-stop/abort + fork-flush tests |
| 5 | `api.rs:414` `read_thread_goal_for_set` (both set branches) | status read | live revoke, then `Err` (kept arm) | core `external_set_get_failure_...` (kept) |
| 6 | `api.rs:126` flush prepare; `api.rs:194` set prepare | accounting | live revoke (kept arms), then `Err` (flush) / warn-and-continue (set) | core flush + set-prepare tests (kept; set-prepare strengthened with exact +3 revision count) |
| 7 | `api.rs:328` clear prepare (GUARD-adjacent) | accounting | warn-and-continue; the GUARDED delete next settles both outcomes | core `clear_prepare_failure_...` (NEW: prepare fails before the write, delete refused, marker None, turn-2 recovers Active) |
| 8 | `extension.rs:556` tool-finish accounting | accounting | revoke via thread store, then warn + return (kept arm) | small `tool_finish_...` (kept) |
| 9 | `extension.rs:345,356,370,416` turn-stop/abort | accounting + status read | revoke (kept arms) | kept turn-stop/abort tests |
| 10 | `extension.rs:449` turn-error reconcile-after | accounting + status read + write | warn, then reconcile-after: persistent failure revokes, transient reconciles | small `turn_error_...` (kept) |
| 11 | `tool.rs:192` unconditional post-tool reconcile | status read | persistent failure revokes here; refused/failed tools settle too | shared branch; kept create/update tests |
| 12 | `tool.rs:209,425,369,293` get-handler and tool metrics reads | status read | tool `Err`, then the unconditional #11 reconcile | shared branch with #1 |
| 13 | `tool.rs:374`, `runtime.rs:690,754` accounting writes | read-modify-write | `Err` to #11 (tool) / call-site arms (runtime) | kept trigger tests |
| 14 | `api.rs:205,233,264` set writes; `tool.rs:233,298`, `runtime.rs:485` other writes (GUARD) | read-modify-return | GUARD: any error revokes live (Unknown) before it is returned; success reconciles (GUARD sites) or hits the existing arms (tool/runtime sites) | core `external_set_post_write_...` (NEW, all three set sites); kept create/update/stop tests |
| 15 | `api.rs:342` clear's delete (GUARD) | DELETE RETURNING + fallible decode | GUARD: error revokes live (Unknown) even when the delete committed; success clears unconditionally | core `clear_returning_decode_...` (NEW: committed delete + decode Err, row count 0, marker None, recovers) |
| 16 | `runtime.rs:551` continuation-deferral read | flag read, not goal status | `Err` AFTER the `:546` reconcile | none (out of contract, not a goal-state read) |
| 17 | `extension.rs:278` deferral clear | flag write | warn-only, AFTER the `:259` reconcile | none (same rationale) |
| 18 | `api.rs:135` public `get_thread_goal` | pure read | error returned to the API caller; no lifecycle effect | none (out of contract) |

Out-of-contract rows: #16, #17, #18 (unchanged from rev-3). Every other row
settles through the single publisher and recovers on the next lifecycle event.

## Changed files (rev-4 delta only)

- `ext/goal/src/api.rs`: about +75/−35 — the guard function (docs included),
  four call-site wraps, two rationale comments. No other production file
  touched.
- `core/tests/suite/goal_activity_tests.rs`: +335 — three new regression
  tests (`:848`, `:1051`, `:1129`) and the exact-revision strengthening of
  `external_set_prepare_failure_...`.
- No dependency, schema, Bazel, or app-server changes. No new files.

## AC coverage map — 8 of 8 rows driven (row 7 extended again)

Rows 1–6 and 8 are unchanged (all previously committed reviewer tests kept
under their original names). AC 7 gains the three new tests:

| AC | New production entry / call site | New driving tests | New refusal / negative assertions |
|---|---|---|---|
| 7 | set-write errors → `guard_live_store_result` (`api.rs:205,233,264`); clear-delete errors → guard (`api.rs:342`); clear-prepare failure → guarded-delete settlement (`api.rs:328-352`) | `external_set_post_write_read_failure_...` (3 phases: status-update, objective-update, replace), `clear_returning_decode_failure_...`, `clear_prepare_failure_...` | post-write Err carries the write message AND the marker is None (stale Active never survives a committed Complete/clear); committed state verified (Complete readable after repair; row count 0 after decode failure); next turn start reconciles (absent for terminal state, republished for live goal) |

Out-of-contract AC rows: none. Stated bound: none.

## Surface coverage map (1 of 1 rows)

| Surface row | Attacking tests | Narrowing mutants |
|---|---|---|
| goal activity publisher | all kept core/small/app-server tests + 3 new + 1 strengthened | 25/25 written (20 kept + 5 guard-bypass); all verify-apply on this tree; kills pending hosted precheck 7 (0 survivors so far) |

## Narrowing-mutant evidence — 25 mutants (20 kept + 5 new)

Patches: outcome `TASK-260929-2gp04j_mutants.json` (25 entries; every patch
verified with strict `patch -p1 --dry-run` on this tree: 25/25 apply). The 20
kept patches are byte-identical to precheck 6 — the rev-4 edits keep all of
their narrowed lines and context lines intact (verified by the dry run, not by
eyeballing). The 5 new patches were additionally applied together and
compile-checked (`cargo check -p codex-goal-extension --tests`, exit 0), then
reverted with `patch -R` and the revert verified byte-identical
(`md5 api.rs` equal before and after).

| Mutant | What it narrows the gate to | Named test that must fail | Result |
|---|---|---|---|
| 20 kept (see rev-3 table; patches unchanged) | (unchanged) | (their original tests; set-prepare via the strengthened exact-revision assertion) | pending precheck-7 re-run |
| guard_skips_revocation_on_store_error (NEW) | the guard reports store errors without revoking | core `external_set_post_write_read_failure_...` (phase A; also phases B/C, both clear tests, and the prepare revision count) | pending precheck 7 (core lane) |
| set_status_update_bypasses_guard (NEW) | the status-only update reports without revoking (guard neutered at that site) | core `external_set_post_write_read_failure_...` phase A | pending precheck 7 (core lane) |
| set_objective_update_bypasses_guard (NEW) | the objective update reports without revoking | core `external_set_post_write_read_failure_...` phase B | pending precheck 7 (core lane) |
| set_replace_bypasses_guard (NEW) | the replace insert reports without revoking | core `external_set_post_write_read_failure_...` phase C | pending precheck 7 (core lane) |
| clear_delete_bypasses_guard (NEW) | the clear delete reports without revoking | core `clear_returning_decode_failure_...` (also `clear_prepare_failure_...`) | pending precheck 7 (core lane) |

Every mutant narrows (the guard stays present; each mutant admits exactly one
site's errors, or — for the guard gut — all guarded errors while keeping the
call sites). No delete-only mutant is used as evidence. No source-text gate
exists, so no token-preserving mutant applies.

Kill reasoning (by inspection; hosted proof is precheck 7): each bypass
mutant passes `None` as the guard runtime at exactly one site, so that site's
injected error returns with the previously published Active marker still in
place and the test's `assert_eq!(marker, None)` fails at its own phase (each
new test's failing phases run before the later phases, and each mutant leaves
the other sites guarded, so every mutant fails its test at a distinct,
attributed assertion). The guard gut additionally fails the strengthened
prepare test at the exact-revision assertion (+2 instead of +3). Core tests
cannot run locally per the brief, so no local kill was executed — this is
explicitly hosted-only evidence.

Determinism notes: Plan-mode setup turns short-circuit preparation without DB
reads (verified in `accounting.rs`, same as rev-3), so the post-write
corruption lands only in the guarded call. The AFTER UPDATE trigger carries a
`WHEN NEW.updated_at_ms != MAX` guard, so the corrupting inner update cannot
recurse. The trigger tests fail deterministically on statement execution, not
on timing.

## Round-3 verdict findings — answered in this revision (repeat-of class)

All four findings share the repeat-of class
(`accounting-read-failure-retains-capability`); rev-4 closes the class
structurally at the service-operation level instead of adding a fifth round
of per-site arms:

| Verdict finding | Rev-4 fix | Named regression tests | Narrowing mutants |
|---|---|---|---|
| clear-error-retains-capability (clear prepare/delete escape; metrics read escapes) | guarded delete settles prepare-failure-then-error AND decode-after-commit; metrics reads funnel to already-armed callers (verified: no unarmed production caller) | `clear_returning_decode_...`, `clear_prepare_failure_...` | `guard_skips_revocation_on_store_error`, `clear_delete_bypasses_guard` |
| clear-returning-decode-retains-capability (DELETE commits, decode fails, marker survives) | same guarded delete; sweep rows 7/15 corrected (an error no longer implies no committed change) | `clear_returning_decode_...` (asserts row count 0 AND marker None AND Err) | same two |
| set-post-write-read-failure-retains-capability (UPDATE commits, follow-up read fails) | all three set writes guarded; sweep row 14 corrected | `external_set_post_write_...` phases A/B (+C for replace) | `guard_skips_revocation_on_store_error`, `set_status_update_bypasses_guard`, `set_objective_update_bypasses_guard` |
| clear-read-failure-retains-capability (prepare warn-only + refused DELETE leave Known) | refused DELETE revokes via the guard (Unknown); prepare-failure path settles via the guarded delete | `clear_prepare_failure_...` (write+delete triggers; recovery republishes the refused goal) | `guard_skips_revocation_on_store_error`, `clear_delete_bypasses_guard` |

## Validation and command evidence (this run; real exit codes, no pipes hiding status)

From `codex-rs/` with `NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no
INSTA_WORKSPACE_ROOT=$PWD` (guard/busy from the worktree root):

| Exact command | Exit code | Meaning |
|---|---|---|
| `python3 .../codex-fix-suite-busy.py --any` | 0 (`FREE`) | shared target free before the first build |
| `../.temp/goal-token-burn/impl/codex-target-guard.sh` | 0 | same checkout, cache kept |
| `just fmt` (after product edit; again after test edits) | 0, 0 | formatting applied |
| `just clippy -p codex-goal-extension -p codex-extension-api` | 0 | 1 warning in untouched `core/src/tools/registry.rs` (pre-existing, not this leaf) |
| `just clippy -p codex-core` | 0 | type-checks the 3 new + 1 strengthened core tests; 3 warnings, all pre-existing in untouched files (`registry.rs`, `openai_file_mcp.rs`, `scenarios.rs`) |
| `just test -p codex-goal-extension -p codex-extension-api` | 0 | 58/58 pass |
| strict `patch -p1 --dry-run` for all 25 mutant patches | 0 failures | every mutant applies to this tree |
| 5 new mutants applied together + `cargo check -p codex-goal-extension --tests`, then `patch -R` revert + md5 check | 0; md5 equal | new mutants compile; revert byte-identical |
| stray `codex-rs/Oops.rej` from a wrong-strip-level patch attempt | removed | `git status` clean of strays (verified) |

NOT run locally per the brief: `just test -p codex-core`,
`just test -p codex-app-server`, full `just test`. The 3 new core tests, the
strengthened prepare test, and all 25 mutant kills on this tree come only from
hosted precheck 7.

## Reviewer notes (kept + updated)

(a) `MODULE.bazel.lock`: no `just bazel-lock-update`. This turn touches no
`Cargo.toml`/`Cargo.lock` (the rev-3 test-only `sqlx` dev-dep edge is
unchanged); no new files, no new dependencies.

(b) Size: rev-4 delta ≈ +410/−35 (about +75/−35 production — one function,
four wraps, comments — and ≈ +335 tests), inside `ext/goal/src/api.rs` + one
core test file only. Cumulative leaf ≈ 2380 lines. The two-stage upstream
split from precheck 2 still stands, and per the rework briefs the leaf is not
split now — the upstream PR will be staged later.

## Outcome-scoped logbook (rev-4)

- The store layer (`codex-state`) is read-modify-return everywhere it matters
  here: `update_thread_goal` commits then re-reads, `delete_thread_goal` is
  DELETE RETURNING plus fallible decode, `replace/insert_thread_goal` are
  INSERT RETURNING plus fallible decode. Any `?` on these calls can fire
  after a commit. The sweep rows now state this instead of inferring
  "error ⇒ unchanged".
- A settlement guard on a later fallible step necessarily subsumes an earlier
  warn-and-continue arm on error-ending paths; the earlier arm is then
  provable only by exact revision counting (set prepare) or documented as
  settled-by-the-later-step (clear prepare). Future arms on multi-step
  operations should be designed with this in mind: one settling step per
  operation, everything else warn-and-continue.
- `patch -p1` strip level is relative to the patch's `a/` prefix: from
  `codex-rs/` these patches need `-p2`. A wrong-level attempt writes
  `Oops.rej` into the worktree — caught and removed this turn; `git status`
  verified clean after.
- Checklist items 3, 5, 6, 7, 10, 15, 16 were unchecked this turn: their
  precheck-6 green described the old tree. They re-check only on precheck-7
  evidence for this tree, with no code change after the snapshot.

---

# Addendum — precheck-8 handoff (2026-10-05): CR rev 4 on tree 65ad71d, 25/25 killed, zero code change

This turn performs `g2-handoff-note-8.md`: the tree was re-verified
byte-identical to the precheck-8 snapshot, results refreshed, the 7 open
checklist items checked on hosted evidence, busy check, then developer
handoff (CR rev 4, story_final). No worktree file was changed in this turn;
a change would have invalidated the evidence below.

Bridge from precheck 7: snapshot `101fb595` (run 37256859867) was green on
all lanes and killed 24 of 25. The one survivor was
`set_replace_bypasses_guard` (run 37257091901, all four lanes green): the
rev-4 guard was already correct on the replace path, but no test drove a
store failure through set/replace, so the bypass was unobservable. The
follow-up run added exactly one core test and zero production code —
verified by tree diff, not by claim:

- `git diff 101fb595 65ad71d230e7d7ac5923b8f88739a504b0fc1d08 --stat`:
  1 file changed, +91/−0, `core/tests/suite/goal_activity_tests.rs` only.
- New test `external_set_replace_failure_revokes_activity_and_next_turn_recovers`
  (`:1193-1282`): publishes Active via a Plan turn, deletes the committed
  row behind the publisher's back (marker stays published, next set takes
  the replace branch), installs a `BEFORE INSERT ... RAISE(ABORT)` trigger,
  asserts the set reports Err AND the marker is None, drops the trigger,
  re-sets successfully, and asserts turn-2 recovery (Active republished,
  higher revision). The guard at `api.rs:233` already wrapped the replace
  call (rev-4 section above); the test only proves it.

## 1. Identity (this exact tree)

- Worktree tree (temp index, `git read-tree HEAD` + `git add -A` +
  `git write-tree`, this turn): `65ad71d230e7d7ac5923b8f88739a504b0fc1d08`
- Precheck-8 snapshot `a37e2ebc` tree:
  `65ad71d230e7d7ac5923b8f88739a504b0fc1d08` — byte-identical.
- HEAD (checkpoint): `31655cd8b5` (G1 replay on trunk 729f259e62);
  uncommitted paths are the rev-4 G2 candidate only.
- `TASK-260929-2gp04j_mutants.json` on the board is unchanged (25 rows —
  the same name set precheck 8 ran, verified equal).

## 2. Hosted snapshot: green on all lanes

- Run https://github.com/relux-works/codex/actions/runs/37263271056:
  lint success, small success, core success, app-server success; zero fails.
- This run executed the exact candidate tree, including the 4 rev-4 core
  regression tests, the strengthened prepare test, and all previously
  committed reviewer tests under their original names.

## 3. Narrowing-mutant evidence — 25 of 25 killed (precheck 8)

Source: `.temp/goal-token-burn/impl/p2/g2-precheck-8.json` (26 runs, all
completed; `killed: true` on all 25 mutants; fails are the `meaningful`
lists; snapshot run has zero fails).

| Mutant | Run | Failing tests | Lane |
|---|---|---|---|
| abort_read_failure_keeps_marker | 37263286435 | turn_abort_accounting_read_failure_revokes_activity_and_next_turn_recovers | small |
| budget_limited_admits_continuation | 37263301509 | accounting_budget_keeps_sleep_without_automatic_continuation | core |
| clear_delete_bypasses_guard (rev-4) | 37263317078 | clear_prepare_failure_..., clear_returning_decode_failure_... | core |
| cleared_revision_accepts_old_read | 37263331927 | publisher_refuses_stale_revision_and_recovers_unknown_state | small |
| complete_retains_sleep | 37263346161 | complete, external_set_post_write_... (same family, see below), created | core+app-server |
| create_waits_for_finish | 37263362618 | clear_revokes_before_late_create_finish_and_stale_set_effects (+disable_mid_turn, same family) | core |
| disable_preserves_active_marker | 37263377567 | disable_and_stop_... (+2 same-family core) | small+core |
| disabled_clear_keeps_marker | 37263392780 | clear_revokes_before_late_create_finish_and_stale_set_effects | core |
| external_set_get_failure_keeps_marker | 37263407731 | external_set_get_failure_... (+guardian flake, see below) | core |
| external_set_prepare_failure_keeps_marker | 37263423549 | external_set_prepare_failure_revokes_activity_and_next_turn_recovers | core |
| external_set_skips_budget_limited | 37263439586 | external_set_and_resume_reconcile_first_request::budget_limited | core |
| fork_flush_prepare_failure_keeps_marker | 37263454412 | fork_flush_read_failure_revokes_activity_and_next_turn_recovers | core |
| guard_skips_revocation_on_store_error (rev-4) | 37263469809 | clear_prepare_..., clear_returning_decode_..., external_set_post_write_..., external_set_prepare_..., external_set_replace_... (all 5 guarded-site tests) | core |
| late_active_set_reinserts_cleared_goal | 37263485560 | clear_revokes_before_late_create_finish_and_stale_set_effects | core |
| resume_skips_budget_limited | 37263501158 | external_set_and_resume_reconcile_first_request::budget_limited | core |
| set_objective_update_bypasses_guard (rev-4) | 37263517219 | external_set_post_write_read_failure_revokes_activity_and_next_turn_recovers | core |
| set_replace_bypasses_guard (rev-4; precheck-7 survivor) | 37263531175 | external_set_replace_failure_revokes_activity_and_next_turn_recovers | core |
| set_status_update_bypasses_guard (rev-4) | 37263544776 | external_set_post_write_... (+external_set_prepare_..., same family) | core |
| stop_preserves_active_marker | 37263560187 | disable_and_stop_revoke_activity_and_pending_options | small |
| timestamp_read_failure_keeps_known_marker | 37263576096 | 8 same-family read-failure tests (clear_returning_decode, external_set_get, external_set_post_write, fork_flush, read_failure, turn_abort, turn_error, turn_stop) | small+core |
| tool_finish_accounting_failure_keeps_marker | 37263590894 | tool_finish_accounting_failure_revokes_activity_and_next_turn_recovers | small |
| turn_error_skips_reconcile_after_stop_failure | 37263605507 | turn_error_read_failure_... (+automatic_stop, same family) | small |
| turn_start_requires_baseline | 37263619598 | turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal | core |
| turn_stop_read_failure_keeps_marker | 37263634903 | turn_stop_accounting_read_failure_revokes_activity_and_next_turn_recovers | small |
| usage_limit_retains_sleep | 37263653941 | automatic_stop_... (+usage_limited, same family) | small+core |

Mutant survivors: 0. Every mutant narrows (gate/guard stays present,
weakened to admit exactly one member of the rejected class); no
delete-only mutant is used as evidence. No source-text gate exists, so no
token-preserving mutant applies.

Extra-fail analysis (only non-same-family fail across all 26 runs):
- `encrypted_parent_reply_survives_incremental_guardian_reviews` on the
  external_set_get_failure run: the known unrelated exec/guardian-messaging
  flake (4th 1-in-N occurrence across p4/p5/p6/p8; sets up no goals; green
  on the snapshot and on every other mutant run). Does not affect the kill
  (the intended test also fails).
- `complete_retains_sleep` fails app-server as well as core, now with
  `external_set_post_write_...` alongside `complete`/`created`: same-family
  and deterministic — phase A commits Complete before the read fails, so
  the recovery assertion (marker None for committed Complete) fails when
  Complete retains. Same shape as p4/p5/p6 plus the new rev-4 test.
- The guard gut fails all 5 guarded-site tests including the new replace
  test: guard coverage is complete across all four guarded sites.

## 4. Round-3 verdict findings — answered in this revision (repeat-of class)

All four findings share the repeat-of class
(`accounting-read-failure-retains-capability`); rev-4 closed the class
structurally with the settlement guard, and the precheck-7 follow-up
closed the last coverage hole (replace path). Each finding keeps its
named regression tests + narrowing mutants in this leaf:

| Verdict finding | Rev-4 fix | Named regression tests | Narrowing mutants |
|---|---|---|---|
| clear-error-retains-capability (clear prepare/delete escape; metrics read escapes) | guarded delete settles prepare-failure-then-error AND decode-after-commit; metrics reads funnel to already-armed callers | clear_returning_decode_..., clear_prepare_failure_... | guard_skips_revocation_on_store_error, clear_delete_bypasses_guard |
| clear-returning-decode-retains-capability (DELETE commits, decode fails, marker survives) | same guarded delete; sweep rows 7/15 corrected (an error no longer implies no committed change) | clear_returning_decode_... (asserts row count 0 AND marker None AND Err) | same two |
| set-post-write-read-failure-retains-capability (UPDATE commits, follow-up read fails) | all three set writes guarded (api.rs:205,233,264) | external_set_post_write_... (phases A/B/C) + external_set_replace_... (dedicated replace coverage) | guard gut + set_status/set_objective/set_replace bypass mutants |
| clear-read-failure-retains-capability (prepare warn-only + refused DELETE leave Known) | refused DELETE revokes via the guard (Unknown); prepare-failure path settles via the guarded delete | clear_prepare_failure_... (write+delete triggers; recovery republishes the refused goal) | guard gut + clear_delete_bypass |

No stated bound remains.

## 5. Coverage maps (this tree)

- AC table: 8 of 8 rows driven through production entries (rev-4 map
  still exact; rows 1–6 and 8 kept, row 7 extended with the 4 rev-4 tests
  + strengthened prepare + replace test). Out-of-contract AC rows: none.
  Stated bound: none.
- Surface table: 1 of 1 rows (`goal activity publisher`) covered — all
  kept core/small/app-server tests + 4 new regression tests + 1
  strengthened, 25/25 narrowing mutants killed on this tree.
- Sweep-table out-of-contract rows: #16, #17 (continuation-deferral flag,
  not goal status; AC 7 governs goal-state reads), #18 (pure API read, no
  lifecycle effect). Every other sweep row settles through the single
  publisher (guard or kept arms) and recovers on the next lifecycle event.
- Rework diff bounded: rev-4 delta stayed inside `ext/goal/src/api.rs` +
  one core test file; the precheck-7 follow-up touched the same test file
  only (+91/−0, verified by tree diff). This handoff turn changes zero
  files.

## 6. Checklist execution items — checked on precheck-8 evidence

- Item 3 (tests written for new/changed behavior): 4 rev-4 core tests +
  strengthened prepare + replace test, green on snapshot run 37263271056.
- Item 5 (n of m AC rows driven): 8 of 8, rev-4 map + this addendum.
- Item 6 (negative/refusal tests at production call sites): every AC
  refusal (failed create, cleared/no-goal turn start, non-Active/
  BudgetLimited resume/set, complete/blocked/paused removal, disabled
  clear, disable/stop, read-failure absence-never-authorizes, post-write
  and decode failures) driven and green on the snapshot.
- Item 7 (narrowing mutant per gate): 25/25 killed, table in section 3.
- Item 10 (build/validation green): snapshot green on all four lanes on
  this exact tree; fast-lane green from the rev-4 run (fmt 0, clippy 0,
  small tests 58/58 — the small suite is unchanged since) reused under
  unchanged identity (brief rule 10), no rebuild in this zero-change turn.
- Item 15 (tests green): snapshot run 37263271056, zero fails.
- Item 16 (gates attacked, not read): section 3 kills prove each gate,
  including the precheck-7 survivor now killed by its dedicated test; no
  positive-path-only evidence.

## 7. Reviewer notes (kept)

(a) `MODULE.bazel.lock`: no `just bazel-lock-update`. No Cargo.toml/
Cargo.lock change since rev-3 (the test-only `sqlx` dev-dep edge is
unchanged); the rev-4 delta and the replace follow-up added no
dependencies and no new files. Per the rev-1/2 precedent this is
Bazel-irrelevant; the board's landing gate re-verifies.

(b) Size: cumulative leaf ≈ 2470 lines (rev-4 ≈ 2380 + 91 replace test;
the earlier 1334-line note predates the three court-ordered reworks).
The two-stage upstream split from precheck 2 still stands, and per the
rework briefs the leaf is not split now — the upstream PR will be staged
later. G2 is the Story's final leaf, so this handoff publishes the
story_final CR.

## 8. Commands run in this handoff turn (real exit codes, no hidden pipes)

| Exact command | Exit code | Meaning |
|---|---|---|
| `task-board m 'set_status(TASK-260929-2gp04j, status=development)'` | 0 | run start |
| temp-index `git read-tree HEAD` + `git add -A` + `git write-tree` | 0, tree 65ad71d... | identity matches precheck-8 snapshot |
| `git diff 101fb595 65ad71d... --stat/--numstat` | 0, +91/−0 one file | precheck-7→8 delta is test-only |
| `task-board resource get` (results, mutants) | 0 | evidence staged under /tmp |
| reads of g2-precheck-8.json/md + test/guard sources | — | read-only verification, no worktree writes |
| `python3 .../codex-fix-suite-busy.py --any` | (below) | shared-target gate before handoff |
| `task-board resource update ... results` + `check_item` × 7 + `handoff` | see board receipts | this handoff |

NOT run in this turn, by design: no `cargo`/`just` build or test (zero
file changes — rerunning would burn shared-target time and cannot add
evidence beyond the hosted snapshot bound to this exact tree; brief rule
10: reuse exact green evidence). No local mutant execution (all 25 kills
are hosted). Unverified locally: nothing new — the hosted snapshot + 25
mutant runs are the verification, and they are complete.

## 9. Outcome-scoped logbook (precheck-8 handoff)

- A survivor with all-green lanes can mean "untested path", not "broken
  code": precheck 7's `set_replace_bypasses_guard` survivor was closed by
  a dedicated test with zero production change, and precheck 8 confirms
  the kill plus the full 25/25.
- The guard-gut mutant now fails all 5 guarded-site tests including the
  replace test: guard coverage is provably complete across all four
  guarded sites.
- `complete_retains_sleep`'s co-failure set grows deterministically with
  same-family tests (p4/p5/p6: complete+created; p8: +post_write):
  recovery assertions on committed Complete are sensitive to the
  Complete-retains narrowing by design, not a new signal.
- The guardian-messaging flake rides its 4th mutant run in 4 prechecks,
  always 1-in-N, always alongside the intended test's fail — still noise.
- Handoff discipline held: zero worktree writes in this turn, results
  refreshed as a board resource only, checklist checked solely on the
  cited hosted runs.
