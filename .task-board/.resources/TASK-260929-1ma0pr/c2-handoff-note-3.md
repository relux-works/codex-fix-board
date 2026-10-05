# TASK-260929-1ma0pr (C2): hand off CR rev 2 on hosted precheck 3

Hosted precheck 3 (`TASK-260929-1ma0pr_hosted-precheck-3.md`, precondition) ran your exact worktree tree 5b2ea16af484965b3dd34f6ca4198dd903732541 three times,
with the queue crate selected (runs 37317650053, 37349767142, 37352331583). All lanes are green every time, the racy wake test
is green 3/3, and all 10 mutants are killed.

1. Confirm the worktree tree still equals 5b2ea16af484965b3dd34f6ca4198dd903732541 (temp index, `git read-tree HEAD`, `git add -A`, `git write-tree`).
   Do NOT change any file.
2. Check the open checklist items, citing precheck 3's run ids and test names (queue tests from small job of run 37349767142).
   Refresh and re-attach TASK-260929-1ma0pr_results.md (a new outcome is required).
3. Run the busy check (`codex-fix-suite-busy.py --any`). On FREE, run `task-board handoff TASK-260929-1ma0pr --role developer`.
   This publishes story_final CR rev 2. Only a printed `BUSY ...` line means HOLD.
