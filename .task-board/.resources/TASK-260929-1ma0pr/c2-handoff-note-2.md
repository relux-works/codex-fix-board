# TASK-260929-1ma0pr (C2): hand off CR rev 1 on hosted precheck 2

Hosted precheck 2 (`TASK-260929-1ma0pr_hosted-precheck-2.md`, precondition) ran your exact worktree tree 808000cbd14914847c7cd418f444dd9232281ddc
(snapshot 34cf97ac, run 37302805027). All four lanes are green, and all 10 narrowing mutants are killed by their intended tests,
including m10 for the has_pending_input fix.

1. Confirm the worktree tree still equals 808000cbd14914847c7cd418f444dd9232281ddc (temp index, `git read-tree HEAD`, `git add -A`, `git write-tree`).
   Do NOT change any file.
2. Check the open checklist items, citing precheck 2's run ids and test names. Refresh and re-attach TASK-260929-1ma0pr_results.md
   (a new outcome is required). Record the has_pending_input production fix (a C1-file change made inside C2's scope) in the results.
3. Run the busy check (`codex-fix-suite-busy.py --any`). On FREE, run `task-board handoff TASK-260929-1ma0pr --role developer`.
   C2 is the Story's final leaf, so this publishes the story_final CR. Only a printed `BUSY ...` line means HOLD.
