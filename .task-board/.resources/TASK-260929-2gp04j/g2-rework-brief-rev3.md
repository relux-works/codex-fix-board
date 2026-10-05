# Rework brief — TASK-260929-2gp04j (G2), CR revision 3: every goal-state read failure must revoke

Round 2 merged to changes_requested (`TASK-260929-2gp04j_review-verdict-rev2.md`). All three panels, the delta panel
included, found the same class still open. Revision 2 fixed the turn-stop and abort exits, but other read sites still
propagate a read failure with `?` BEFORE the publisher reconciles, so a previously published marker survives:
- `GoalService::set_thread_goal` in `ext/goal/src/api.rs` (~:188-202 and ~:243-251): a preparation or accounting error
  only warns, then a `get_thread_goal` error returns via `?` before `reconcile_live_activity` (~:283);
- `ext/goal/src/runtime.rs` (~:671-673 and ~:735-737): `current_goal_status_for_metrics` read failures propagate before
  publication. The fallible `get_thread_goal` is at ~:790-796, and it is reachable from production through the app-server
  fork path (thread_processor -> thread_goal_processor).

Fix the CLASS, not just these sites:
1. Enumerate EVERY site in ext/goal (api.rs, runtime.rs, extension.rs, tool.rs, activity.rs) that reads goal state and can
   fail. In `TASK-260929-2gp04j_results.md`, add a table listing each site (file:line), what happens on failure, and the
   test that drives that failure. Every failure path that can leave a previously published marker must revoke it through
   the single publisher (record reconciliation unknown, report the error) and recover on the next lifecycle event.
2. Add tests that drive read failures through `set_thread_goal` (external set) and through the metrics/fork path, and add
   narrowing mutants for them to `TASK-260929-2gp04j_mutants.json`, each naming its killing test. Keep the existing 15.
3. Fast lane only: `just fmt`, clippy for the touched crates, `just test -p codex-goal-extension -p codex-extension-api`.
   Then add the note `HOSTED-PRECHECK-REQUESTED: precheck 4` and end your turn without handing off.
