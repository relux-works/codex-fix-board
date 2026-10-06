# TASK-260929-csnn3a (D2): hand off CR rev 1 on hosted precheck 2

Hosted precheck 2 (`TASK-260929-csnn3a_hosted-precheck-2.md`, precondition) ran your exact worktree tree 3e3f73576ad3ed852711023df46ad5bd2dccda6c (snapshot 91c90e94, run 37430403364).
All four lanes are green, and all 8 mutants are killed by their intended tests.

1. Confirm the worktree tree still equals 3e3f73576ad3ed852711023df46ad5bd2dccda6c (temp index, `git read-tree HEAD`, `git add -A`, `git write-tree`). Do NOT change any file.
2. Check the open checklist items, citing precheck 2's run ids and test names. Refresh and re-attach TASK-260929-csnn3a_results.md (a new outcome is required).
   State the AC3 guardian bound with its code citation, and describe any production change made for F1a.
3. Run the busy check (`codex-fix-suite-busy.py --any`). On FREE, run `task-board handoff TASK-260929-csnn3a --role developer`. D2 is the Story's final leaf,
   so this publishes the story_final CR. Only a printed `BUSY ...` line means HOLD.
