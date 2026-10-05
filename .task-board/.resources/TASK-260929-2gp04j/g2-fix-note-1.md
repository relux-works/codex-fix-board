# TASK-260929-2gp04j (G2): fix what hosted precheck 1 found, then request precheck 2

Hosted precheck 1 (`TASK-260929-2gp04j_hosted-precheck-1.md`, precondition) ran your exact worktree tree and 13 mutants:
1. A real failure on the UNMUTATED candidate. `suite::goal_activity::disable_mid_turn_removes_sleep_from_next_request`
   fails 3/3 at core/tests/suite/goal_activity_tests.rs:203: after the mid-turn feature disable, the marker is still
   `Some(GoalActivity { revision: 2, state: Active })` where the test expects `None`. AC row 6 requires disable to remove
   the marker and goal-owned wait/timer state, and re-enable to reconcile. Find the root cause. Either the disable hook
   does not remove the marker on this path (fix the product code), or the test asserts at the wrong moment (fix the test
   and justify it from the AC; do not weaken the AC).
2. A surviving mutant. `disabled_clear_keeps_marker` (committed clear revokes only while enabled) was NOT killed. Its
   intended test `clear_revokes_before_late_create_finish_and_stale_set_effects` passed under the mutant. Strengthen that
   test, or add one, so that a committed clear with feature enablement already OFF observably removes the marker; the
   mutant must then fail.
The other 12 mutants were killed by their named tests. Keep those tests as they are.

Then, fast lane only (no local codex-core/app-server tests): `just fmt`, clippy for the touched crates and
`just test -p codex-goal-extension -p codex-extension-api`. Refresh `TASK-260929-2gp04j_mutants.json` (keep the 13
mutants, adjusted to the new code if needed) and the results, then add the note `HOSTED-PRECHECK-REQUESTED: precheck 2`
and end your turn without handing off.
Also record two notes in your results for the reviewers: (a) whether `MODULE.bazel.lock` needs `just bazel-lock-update`
after the new dev-dependencies (codex-core dev-dep on codex-goal-extension, goal dev-dep on sqlx); run it if the repo's
rule requires it; (b) the 1334-line size against AGENTS.md's 800-line guidance, with the two-stage split you proposed.
