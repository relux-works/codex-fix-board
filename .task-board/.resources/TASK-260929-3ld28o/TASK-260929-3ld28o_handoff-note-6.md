# TASK-260929-3ld28o: hand off CR rev2 on hosted precheck 6

Hosted precheck 6 (`TASK-260929-3ld28o_hosted-precheck-6.md`, precondition, run 38047301443) is fully green, and every mutant is killed by its named tests.
It closes review rev1 A-F1..A-F3, F1 and F2. Mention the orchestrator's two test-only edits (b1-orch-compile-fix.md).
1. Compute your tree (temp index: `git read-tree HEAD`, `git add -A`, `git write-tree`), then run
   `git diff --name-only 568588edd89a50d4f259f9e17eb902cd38ae9e8e <your tree>`. It must print nothing or only `.github/` paths (CI-only trunk commits picked up by a
   Story refresh). Do NOT change any file. If any other path appears, stop and add a note.
2. Check the open checklist items, citing precheck 6 and the findings it closes. Refresh and re-attach `TASK-260929-3ld28o_results.md`.
3. Run `task-board handoff TASK-260929-3ld28o --role developer` (CR rev2).
