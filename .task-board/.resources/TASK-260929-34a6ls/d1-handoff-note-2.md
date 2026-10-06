# TASK-260929-34a6ls (D1): hand off CR rev 1 on hosted precheck 2

Hosted precheck 2 (`TASK-260929-34a6ls_hosted-precheck-2.md`, precondition) ran your exact worktree tree 8e03a0e18d68ac6891de673dd8d55bf0dce5c30e
(snapshot bfbe241e, run 37383604313). All four lanes are green, and all 8 narrowing mutants are killed by their intended tests.

1. Confirm the worktree tree still equals 8e03a0e18d68ac6891de673dd8d55bf0dce5c30e (temp index, `git read-tree HEAD`, `git add -A`, `git write-tree`). Do NOT change any file.
2. Check the open checklist items, citing precheck 2's run ids and test names. Refresh and re-attach TASK-260929-34a6ls_results.md
   (a new outcome is required). If you replaced the ack_all_tracked mutant, say why in the results.
3. Run the busy check (`codex-fix-suite-busy.py --any`). On FREE, run `task-board handoff TASK-260929-34a6ls --role developer`.
   Only a printed `BUSY ...` line means HOLD.
