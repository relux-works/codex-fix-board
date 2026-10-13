# TASK-260929-309h9n (P4b-2): review rev1 changes_requested. Prove blocker-first on the production path, narrow the test switch, then request precheck 5

The verdict is `TASK-260929-309h9n_review-verdict-rev1.md`. Panel B accepted; panel A requested changes. No production failure
was observed: the source order is correct. The gaps are in the proof. Everything else in rev1 (entry rule, shared timer slot,
PacingTicket, admission recheck under the lock, transient state, no model-visible change, the four orchestrator fixes) stays.

## 1. A-F1 (robustness): the blocker-order mutant does not test blocker order

`pacing_blocker_order_swapped` deletes the `InactiveOrBudgetLimited` early return in `BackgroundWaitState::evaluate_locked`,
which production never reaches (`continue_if_idle` passes Active after its own gate); its only killer is
`pacing_inactive_goal_never_paced`. The real AC5 property lives in `GoalExtension::on_turn_stop` (`extension.rs`): the
empty-response blocker runs, then `note_turn_completed`. Panel B notes that merely swapping those two calls is
behavior-preserving (disjoint state), so the proof must be behavioral, not textual:

- Add the core integration test `goal_pacing_empty_blocker_runs_before_rescheduling` in
  `core/tests/suite/goal_continuation_pacing.rs`, with pacing ENABLED (no `CODEX_GOAL_PACING_DISABLED`), using the existing
  fake-clock helpers there: drive fully empty automatic continuations until the existing three-empty blocker fires. Assert the
  goal ends blocked with the same status/reason as the pre-existing empty-response suite, that no pacing wait is armed after the
  blocking turn, and that the model request count stops (advance the fake clock past the next pacing delay and assert no
  further request). Report the request count.
- Replace the mutant with one that narrows the blocker for paced turns: e.g. in `on_turn_stop`, skip or defer the
  EmptyResponse blocker when the turn was an automatic goal continuation that pacing will reschedule (so pacing re-arms instead
  of blocking). Name it `pacing_blocker_skipped_for_paced_turns`; killer = the new test. Drop `pacing_blocker_order_swapped`
  from the mutants JSON (keep `pacing_inactive_goal_never_paced` as a plain unit test).

## 2. A-N1 (note): narrow the test switch in `app-server/tests/suite/v2/goal_background_wait.rs`

The shared harness sets `CODEX_GOAL_PACING_DISABLED=1` for all four tests. Only
`unopted_server_process_does_not_gate_goal_continuation` and `headless_host_refuses_notify_on_exit_and_promises_no_wake` need
back-to-back automatic continuations. Set the switch only for those two (a harness parameter or a second builder; keep it
small). `notified_exec_exit_wakes_gated_goal_with_receipt_fragment` and
`user_burst_during_background_wait_admitted_without_loss_or_duplication` must run with pacing enabled; they then cover the
event-wake-while-pacing interaction (AC3). If one of them genuinely needs the switch, say why in the results instead.
Update the results' switch inventory.

## 3. F1-blocker-mutant-proxy (note): no action beyond section 1.

## Keep

All other mutants must still apply to the final tree; killer names keep `pacing` (or `goal`) so the filter
`test(pacing) | test(continuation_schedule) | test(goal)` selects them.

`mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item` then `--check` exit 0; no other cargo; no
CODEX_HOME copies; delete temp dirs. Watch for redundant closures, uninlined format args, `vec!` where an array works, and
`/*param*/` comments on positional literals. Leave everything UNCOMMITTED, report the final tree id after fmt, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 5`, and end your turn without handing off.
