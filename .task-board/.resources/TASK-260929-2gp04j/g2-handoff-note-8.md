# TASK-260929-2gp04j (G2): hand off CR rev 4 on hosted precheck 8

Hosted precheck 8 (`TASK-260929-2gp04j_hosted-precheck-8.md`, precondition) ran your exact worktree tree 65ad71d230e7d7ac5923b8f88739a504b0fc1d08
(snapshot a37e2ebc, run 37263271056). All four lanes are green, and all 25 mutants are killed. Your new test
external_set_replace_failure_revokes_activity_and_next_turn_recovers kills set_replace_bypasses_guard.

1. Confirm the worktree tree still equals 65ad71d230e7d7ac5923b8f88739a504b0fc1d08 (temp index, `git read-tree HEAD`, `git add -A`, `git write-tree`).
   Do NOT change any file.
2. Check the open checklist items, citing precheck 8's run ids and test names. Refresh and re-attach
   TASK-260929-2gp04j_results.md and the coverage map (a new outcome is required).
3. Run the busy check (`codex-fix-suite-busy.py --any`). On FREE, run `task-board handoff TASK-260929-2gp04j --role developer`
   to publish the story_final CR rev 4. Only a printed `BUSY ...` line means HOLD.
