# TASK-260929-309h9n (P4b-2): precheck 5 core red on a racy pacing test. Make both core pacing tests deterministic, then request precheck 6

Precheck 5 (run 38184361813, snapshot b33f8d00, tree 4f7adc61; ref relux/ci-next, same base ba724917 as precheck 4): lint, small
and app-server green; all 6 mutants killed (mutant results stand). Core red on ONE test, and a second is flaky:

- `suite::goal_continuation_pacing::goal_pacing_first_immediate_second_at_60s` FAILED 3/3 at `goal_continuation_pacing.rs:246`
  (`second pacing wait should arm`): `armed_deadline()` was None right after the test's
  `emit_thread_idle_lifecycle_if_idle(Completed)`. The same unchanged test PASSED in precheck 4 on the same base.
- `goal_pacing_empty_blocker_runs_before_rescheduling` FAILED try 1 at :358 (`the n=3 deadline should sit ~120s out, got 2.16s`)
  and PASSED on retry.

## Diagnosis (orchestrator, from the source; confirm or correct it)

Both tests assume that when `EventMsg::TurnComplete` is observed the session is already idle and the pacing evaluation has
not run yet. Neither is guaranteed: `emit_thread_idle_lifecycle_if_idle` (`core/src/tasks/lifecycle.rs:59`) returns early while
`active_turn` is still set, so the test's explicit call can be a no-op (case 1); and the production idle path that runs after
the turn can arm the pacing wait itself, before or after the test's `tokio::time::pause()`/clock reads, so the test can read a
deadline armed against a different clock reading (case 2). This is test synchronization, not an observed production defect.
If you find that production can actually leave a paced goal with NO armed wait after an automatic continuation ends (a lost
schedule), that is a production bug: fix it and say so.

## Required

1. Make the two core tests deterministic without sleeps: after each `TurnComplete`, wait (bounded, e.g. `tokio::time::timeout`
   around a yield loop or an existing `wait_for_*` helper) until the turn is fully idle and the pacing wait is ARMED by the
   production path, then read the deadline. Do not rely on the test's own `emit_thread_idle_lifecycle_if_idle` racing the
   production one; if the production path always arms it, drop the explicit call, otherwise keep it only after idle is proven.
   Pause tokio time so that the clock the deadline is measured against cannot move between arming and reading.
2. Keep every assertion's meaning (immediate first continuation; n=2 ~60 s; n=3 ~120 s; blocker at the third empty turn; no
   further request after advancing past the next delay). The two tests remain the killers of their mutants.
3. Check the app-server pacing test (`goal_pacing_two_polls_first_immediate_second_60s`) for the same pattern and harden it the
   same way if it has it (it passed in precheck 4 and 5).

## Keep

All 6 mutants must still apply to the final tree; no production change unless you found a real lost-schedule bug (then add a
mutant and killer for it). Filter for precheck 6 = `test(pacing) | test(continuation_schedule) | test(goal)`.

`mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item` then `--check` exit 0; no other cargo; no
CODEX_HOME copies; delete temp dirs. Leave everything UNCOMMITTED, report the final tree id after fmt, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 6`, and end your turn without handing off.
