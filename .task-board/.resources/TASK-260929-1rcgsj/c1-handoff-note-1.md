# TASK-260929-1rcgsj (C1): hand off CR rev 1 on hosted precheck 1

Hosted precheck 1 (`TASK-260929-1rcgsj_hosted-precheck-1.md`, precondition) ran your exact worktree tree 37fad741767c46d11094adb9be747d5aae83c145
(snapshot f2bf01a5, run 37278001051). All four lanes are green, and all 10 narrowing mutants are killed by their
intended tests.

1. Confirm the worktree tree still equals 37fad741767c46d11094adb9be747d5aae83c145 (temp index, `git read-tree HEAD`, `git add -A`, `git write-tree`).
   Do NOT change any file; a change invalidates the evidence.
2. Check the open checklist items, citing precheck 1's run ids and test names. Refresh and re-attach
   TASK-260929-1rcgsj_results.md and its coverage map (a new outcome is required).
3. Run the busy check (`codex-fix-suite-busy.py --any`). On FREE, run `task-board handoff TASK-260929-1rcgsj --role developer`.
   Only a printed `BUSY ...` line means HOLD.
