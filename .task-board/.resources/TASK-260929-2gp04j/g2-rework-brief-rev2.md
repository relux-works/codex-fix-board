# Rework brief — TASK-260929-2gp04j (G2), CR revision 2: accounting/abort read-failure path

The round-1 R141 review merged to changes_requested (`TASK-260929-2gp04j_review-verdict-rev1.md`):
- accounting-read-failure-retains-capability (robustness). `ext/goal/src/runtime.rs` (~:660-676) propagates the metrics
  goal read error before publication, `current_goal_status_for_metrics` (~:783-785) propagates get_thread_goal errors,
  and `ext/goal/src/extension.rs` (~:405-417) logs and returns on abort without revoking a previously Known marker. A
  goal-store read failure on the progress-accounting or abort paths therefore leaves a stale GoalActivity marker. AC row
  7 requires that a read failure removes the marker, records reconciliation as unknown, reports the error, and that the
  next lifecycle event reconciles. Panel B noted the same window.

Do this:
1. On every path that reads goal state for accounting, metrics or abort handling, make a read failure revoke the marker
   through the single publisher, then report the error and recover on the next lifecycle event. Keep the publisher the
   only writer.
2. Add a test that drives a read failure through the accounting path (and through the abort path if reachable from a
   public entry) and asserts the marker is gone and later recovers. Add narrowing mutants to
   `TASK-260929-2gp04j_mutants.json` for these paths (for example: the accounting read error keeps the known marker), each
   naming its killing test, and keep the 13 existing mutants, adjusted to the code if needed.
3. Fast lane only: `just fmt`, clippy for the touched crates, `just test -p codex-goal-extension -p codex-extension-api`.
   Then add the note `HOSTED-PRECHECK-REQUESTED: precheck 3` and end your turn without handing off. You will be resumed
   with the hosted evidence.
The reviewers' size note (G2 is about 1385 lines) is NOT a request to split this leaf now: the upstream PR will be
staged later. Do not grow the diff beyond what the fix needs.
