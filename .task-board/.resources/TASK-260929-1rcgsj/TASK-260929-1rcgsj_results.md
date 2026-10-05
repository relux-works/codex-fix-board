# TASK-260929-1rcgsj — input-queue-runtime-leases: results (C1 refresh)

## C1 handoff confirmation (no code change)

This refresh cites hosted precheck 1 (`TASK-260929-1rcgsj_hosted-precheck-1.md`,
precondition) and confirms the candidate tree is unchanged. No file was modified
in this run.

- Worktree tree re-verified in this run via temp index
  (`GIT_INDEX_FILE=$TMPIDX git read-tree HEAD && git add -A && git write-tree`):
  `37fad741767c46d11094adb9be747d5aae83c145` — equals the precheck-1 tree.
- Snapshot commit `f2bf01a5`, relux-ci run `37278001051`:
  lanes `lint=success`, `small=success`, `app-server=success`, `core=success`.
  All green on the exact candidate tree.
- Mutants: 10 total, 10 killed, 0 survivors (each run fails as expected):

| Mutant | Run | Failing lanes | Killing tests |
|--------|-----|---------------|---------------|
| runtime_trigger_admits_suspended | 37278163468 | core | input_queue_runtime_suspended_entries_never_count_as_trigger, runtime_suspended_entries_are_excluded_from_trigger_and_lease, runtime_suspended_while_leased_stops_suppressing |
| runtime_lease_admits_suspended | 37278101178 | core | input_queue_runtime_suspended_entries_never_count_as_trigger, runtime_suspended_entries_are_excluded_from_trigger_and_lease |
| runtime_lease_readmits_leased | 37278122457 | lint,core | input_queue_runtime_entry_survives_drain_as_leased, runtime_duplicate_enqueue_does_not_duplicate_delivery, runtime_entry_survives_lease_until_acknowledged |
| runtime_ack_admits_stale | 37278019338 | core | input_queue_runtime_failed_lease_retries_without_duplicate, runtime_failed_lease_returns_unleased_exactly_once |
| runtime_fail_admits_stale | 37278078920 | core | input_queue_runtime_failed_lease_retries_without_duplicate, runtime_failed_lease_returns_unleased_exactly_once |
| runtime_cancel_admits_leased | 37278038094 | core | input_queue_runtime_cancel_removes_leased_and_unleased_entries, runtime_cancel_removes_leased_and_unleased_entries |
| runtime_wake_omits_trigger | 37278203959 | lint,core | pending_runtime_entry_starts_one_wake_turn_with_exec_completion, two_runtime_entries_still_start_one_wake_turn |
| runtime_pending_admits_leased | 37278142989 | lint,core | input_queue_runtime_entry_survives_drain_as_leased, runtime_entry_survives_lease_until_acknowledged |
| runtime_enqueue_admits_duplicate | 37278056447 | core | runtime_duplicate_enqueue_does_not_duplicate_delivery |
| runtime_wake_fakes_agent_mail | 37278183811 | core | pending_runtime_entry_starts_one_wake_turn_with_exec_completion, two_runtime_entries_still_start_one_wake_turn |

Notes: three mutants also fail the lint lane (dead-code/unused fallout of the
narrowing patch under deny-warnings); every mutant is killed by named core-lane
tests above, so each gate is proven by behavioural tests, not only by lint.
Survivors: none — no survival bounds to state.

Checklist mapping: items 2–7, 9–10 are green on run 37278001051 plus the 10
killed-mutant runs above; item 8 is N/A (no source-text gate in this leaf —
see Bounds 5 of the original report, kept below); item 4 holds (candidate left
uncommitted, branch tip unmoved); item 11 is this refreshed outcome; item 12 —
no logbook-worthy anomaly in this leaf (no forced fit, no regression, no
surprising platform behaviour), so nothing was recorded.

## Summary

Implemented the internal runtime-notification mailbox with leases until
sampling (final plan 5.2, stage 2b leaf 1). `InputQueue` gains a
runtime-notification entry kind carrying a real completion-receipt reference
(`ReceiptId` + `ReceiptOwner` from stage B). Entries are a named internal
type (`RuntimeMailbox` / `PendingRuntimeNotification`), never fake
`InterAgentCommunication`. Drain leases without removing; acknowledgement
removes; failed sampling returns unleased exactly once; cancel removes in any
lease state; suspend excludes from trigger/pending/lease. Trigger queries
(`has_trigger_turn_mailbox_items`, `has_pending_mailbox_items`) include
unsampled non-suspended entries; suspended entries are excluded so they never
block `start_if_idle` or suppress idle contributors (verdict rev3 note 1).
Idle wake in `maybe_start_turn_for_pending_work` leases runtime entries and
starts one turn with trigger `exec_completion`, preserving the thread's
execution settings, inventing no initiating agent/parent lineage, and adding
no user input (no human-quota reset). Inter-agent mail semantics are
unchanged. Out of scope per brief: context fragment + `TurnInput` variant
(leaf 2, C2), sampling-acknowledgement wiring (story D), tool exposure
(story F).

## Changed files

- `codex-rs/core/src/session/runtime_mailbox.rs` (new, ~220 LoC): `RuntimeMailbox`,
  `RuntimeLease`, `EXEC_COMPLETION_TURN_TRIGGER`, lease state machine
  (enqueue / has_pending / has_trigger / lease_available / acknowledge /
  fail / cancel / suspend).
- `codex-rs/core/src/session/runtime_mailbox_tests.rs` (new): 7 unit tests.
- `codex-rs/core/src/session/input_queue.rs`: `InputQueue` gains
  `runtime_notifications`; `has_pending_mailbox_items` /
  `has_trigger_turn_mailbox_items` include runtime; new
  `enqueue/lease/acknowledge/fail/cancel/suspend_runtime_*` methods;
  `drain_mailbox_input_items` stays inter-agent-only (documented); 5 new
  tests in the existing inline module.
- `codex-rs/core/src/session/mod.rs`: `pub(crate) mod runtime_mailbox;`.
- `codex-rs/core/src/session/turn_input_tests.rs`: 2 admission tests (AC2).
- `codex-rs/core/src/tasks/mod.rs`:
  `maybe_start_turn_for_pending_work_with_sub_id` leases runtime entries and
  sets `exec_completion` when no trigger mail is present; settings
  preservation path shared with queue-only wake.
- `codex-rs/core/src/codex_thread.rs`: `#[doc(hidden)] pub`
  `test_enqueue_exec_completion_notification()` test hook (reserves a real
  receipt, arms + publishes exit, enqueues, wakes). Outside the named
  modules; reason: the AC3 suite test needs a public injection path without
  protocol/app-server changes. No production caller.
- `codex-rs/core/tests/suite/runtime_mailbox.rs` (new) +
  `codex-rs/core/tests/suite/mod.rs`: 3 suite tests (AC3 + AC4 negative).

No protocol or app-server changes. No `TurnInput` variant (leaf 2).

## Coverage map — 5 of 5 AC rows driven

| AC | Requirement | Driving test (production entry) | Refusal / negative test |
|----|-------------|----------------------------------|--------------------------|
| 1 | Runtime entry survives drain as leased; second drain does not re-offer; ack removes; fail returns unleased exactly once | `input_queue_runtime_entry_survives_drain_as_leased` via `InputQueue::enqueue_runtime_notification` → `InputQueue::lease_runtime_notifications` (called by `Session::maybe_start_turn_for_pending_work_with_sub_id`, `core/src/tasks/mod.rs`) → `acknowledge_runtime_lease`; plus `runtime_entry_survives_lease_until_acknowledged` at mailbox level | `input_queue_runtime_failed_lease_retries_without_duplicate` (second `fail` refused, old token cannot ack, retry gets a fresh token, never delivered twice) + `runtime_double_acknowledgement_is_refused` (double ack refused) + `runtime_failed_lease_returns_unleased_exactly_once` |
| 2 | Unsampled non-suspended runtime counts as trigger mail, suppresses automatic goal continuation | `runtime_entry_suppresses_automatic_goal_continuation` via `turn_input::handle` + `TurnInputMode::StartIfIdle` (the goal-continuation path, `ext/goal/src/runtime.rs` → `CodexThread::start_turn_if_idle`), asserting `NotSubmitted{PendingTriggerTurn}`; gate is `InputQueue::has_trigger_turn_mailbox_items` (also read by `emit_thread_idle_lifecycle_if_idle`, `core/src/tasks/lifecycle.rs`) | `suspended_runtime_entry_does_not_block_start_if_idle` (suspended → `has_trigger` false → `Started`) + `input_queue_runtime_suspended_entries_never_count_as_trigger` + `runtime_suspended_while_leased_stops_suppressing` |
| 3 | One pending runtime starts exactly one turn via `maybe_start_turn_for_pending_work`, trigger `exec_completion`, thread's current execution settings | `pending_runtime_entry_starts_one_wake_turn_with_exec_completion` (suite, mocked responses): initial turn with `cyber=standard`, `CodexThread::test_enqueue_exec_completion_notification` → `Session::maybe_start_turn_for_pending_work_with_sub_id`, assert 2 requests total (exactly one wake sampling request), both `access_programs.cyber=standard`, wake `turn_trigger=exec_completion`, `root_turn=wake_turn_id`, `parent_turn=None` | `two_runtime_entries_still_start_one_wake_turn` (2 entries → still 2 requests, no second wake); no-InterAgent-author check (`inputs_of_type("agent_message").is_empty()` in both); no-human-quota check (wake user texts == initial user texts, no new user message; P4a allowance does not exist yet at this stage, so preservation is by construction — no `UserInput` is created and `reserve_user_input_order` is never called on this path) |
| 4 | Inter-agent mail behaviour unchanged | Existing `input_queue` unit tests and `pending_input` suite tests (untouched; green in hosted CI run 37278001051) + `input_queue_runtime_and_inter_agent_mail_share_trigger_queries` (mixed mail + runtime: drain removes mail only, runtime trigger preserved, inter-agent order/selection unchanged) | `queue_only_inter_agent_mail_still_never_starts_a_turn_alone` (queue-only mail → still 1 request, no wake without durable sleep) |
| 5 | Cancelling the receipt removes the entry whether leased or not; cancelled never re-offered or sampled | `input_queue_runtime_cancel_removes_leased_and_unleased_entries` via `InputQueue::cancel_runtime_notification` (future story-E call site), covering leased + unleased states; plus `runtime_cancel_removes_leased_and_unleased_entries` at mailbox level | Lease tokens for cancelled entries cannot acknowledge or fail (`assert!(!acknowledge)`, `assert!(!fail)` in both tests); post-cancel `lease_available` empty, `has_pending`/`has_trigger` false |

Coverage ratio: **5 of 5 AC rows driven** through production entry points.
Gating/refusing/validating behaviour (trigger inclusion, suspend exclusion,
lease/fail/ack token checks, cancel removal, duplicate refusal, wake trigger)
is covered by the negative tests above; each names its production call site.

## Narrowing mutants (10, in `TASK-260929-1rcgsj_mutants.json`)

Each mutant keeps the gate present and weakens it to admit exactly one member
of the class it must reject. All patches verified with `git apply --check`.
Hosted-CI kill confirmation is in the C1 table at the top of this document
(runs 37278019338–37278203959): 10/10 killed, 0 survivors.

| Mutant | Narrows | Named test that fails (confirmed in precheck 1) |
|--------|---------|--------------------------------------------------|
| `runtime_trigger_admits_suspended` | `has_trigger` admits suspended | `input_queue_runtime_suspended_entries_never_count_as_trigger` (+2 more) |
| `runtime_lease_admits_suspended` | `lease_available` leases suspended | `runtime_suspended_entries_are_excluded_from_trigger_and_lease` |
| `runtime_lease_readmits_leased` | `lease_available` re-offers leased | `runtime_entry_survives_lease_until_acknowledged` (+2 more) |
| `runtime_ack_admits_stale` | `acknowledge` accepts stale token | `runtime_failed_lease_returns_unleased_exactly_once` |
| `runtime_fail_admits_stale` | `fail` accepts stale token | `runtime_failed_lease_returns_unleased_exactly_once` |
| `runtime_cancel_admits_leased` | `cancel` refuses leased | `runtime_cancel_removes_leased_and_unleased_entries` |
| `runtime_wake_omits_trigger` | wake omits `exec_completion` | `pending_runtime_entry_starts_one_wake_turn_with_exec_completion` |
| `runtime_pending_admits_leased` | `has_pending` counts leased (second wake) | `input_queue_runtime_entry_survives_drain_as_leased` |
| `runtime_enqueue_admits_duplicate` | `enqueue` duplicates receipt | `runtime_duplicate_enqueue_does_not_duplicate_delivery` |
| `runtime_wake_fakes_agent_mail` | wake fabricates `InterAgentCommunication` | `pending_runtime_entry_starts_one_wake_turn_with_exec_completion` |

No delete-only mutants. No source-text gate, so no token-preserving
behavioural mutant is required.

## Commands (exact, with exit codes)

From the Story worktree (FAST lane only, per producer brief):

- `/Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-target-guard.sh` → exit 0
  (`codex-target-guard: cleaned workspace members ...`).
- `python3 .../codex-fix-suite-busy.py --any` → `FREE` (checked before first
  build and before this report).
- `cd codex-rs && just fmt` → exit 0 (run after edits; re-ran after each
  test update).
- `cd codex-rs && just clippy -p codex-core` → exit 0 (final run; only
  pre-existing warnings in untouched files: `tools/registry.rs`,
  `tests/suite/openai_file_mcp.rs`, `tests/suite/scenarios.rs`). Clippy runs
  with `--tests`, so new unit + suite test code type-checks.
- `cd codex-rs && just fix -p codex-core` → exit 0 (4m15s). It auto-removed
  the 3 pre-existing unused imports above; those collateral edits were
  reverted (`git checkout -- <3 files>`) to keep the diff inside scope.
- Mutant patch check: all 10 `git apply --check` → OK.

Hosted CI (precheck 1, run by the orchestrator on snapshot f2bf01a5):

- Run 37278001051 (candidate tree): lint/success, small/success,
  app-server/success, core/success.
- Mutant runs 37278019338, 37278038094, 37278056447, 37278078920,
  37278101178, 37278122457, 37278142989, 37278163468, 37278183811,
  37278203959: each red in the expected lane(s) with the named killing
  tests above (expected-red evidence, not green gates).

NOT run locally (per brief — hosted CI owns them):

- `just test -p codex-core` — executed on hosted CI instead (core lane of
  run 37278001051, success).
- `just test -p codex-app-server` — executed on hosted CI instead
  (app-server lane of run 37278001051, success).
- Full `just test` — never run.

## Unverified / bounds

1. ~~Local execution pending~~ — RESOLVED by precheck 1: all new tests ran
   green on hosted CI (run 37278001051, core lane success) and all 10
   mutants were killed by their intended tests.
2. Human-quota preservation (AC3): the P4a check-in allowance does not exist
   yet (stage 2d), so there is no quota object to assert against. The suite
   test proves the wake adds no user input (user texts identical) and the
   implementation creates no `UserInput` on this path; quota non-reset
   follows by construction. Stated bound, not a gap in this leaf.
3. Initiating-agent absence is proven via `parent_turn=None` (the setter only
   runs under `Some(parent_turn_id)`, `tasks/mod.rs`) plus the empty
   `agent_message` check; `initiating_agent_path` itself is internal turn
   state with no suite-observable surface.
4. Leaf-1 staging: `maybe_start` leases runtime entries for the wake trigger
   but drops the tokens (no `TurnInput` carrier until leaf 2, no sampling
   ack until story D). Leased entries therefore stay leased after the wake
   turn in this stage; `has_pending` excludes leased so no second wake
   follows, while `has_trigger` retains priority. No production enqueue path
   exists yet (story E), so no stuck entries occur outside tests, where
   cancel cleans up.
5. Brief carries no surface table, so the coverage-map precondition row is
   N/A — reported here as a brief gap, not a waiver.
6. Out-of-contract rows: none. All 5 AC rows are in contract; the C2/D/F
   exclusions are stated in the brief's Out-of-scope, not AC rows.
7. Rework diff bounded: N/A (initial implementation, not a rework). The only
   file outside the named modules is the `CodexThread` test hook, reasoned
   above; no protocol/app-server changes.
8. Reviewer tests kept: none pre-exist for this leaf (first implementation).
