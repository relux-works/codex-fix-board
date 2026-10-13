# TASK-260929-csyzcj (G1): hand off CR rev2 on hosted precheck 8

Hosted precheck 8 (`TASK-260929-csyzcj_hosted-precheck-8.md`, precondition) is fully green: core 5085/5085 with no flakes, and 7/7
mutants killed, including interrupted_notice_delivered_twice by an assertion.
1. Your Story worktree may have been refreshed onto a newer trunk (CI-only commits). Compute the tree (temp index:
   `git read-tree HEAD`, `git add -A`, `git write-tree`), then run
   `git diff --name-only 78b49cd71e2ccfc855069cc05f99ec294e383e85 <your tree>`. It must print NOTHING or only paths under
   `.github/`. Do NOT change any file. If any other path appears, stop and add a note.
2. Check the open checklist items, citing precheck 8 (run 38017711768) and the review rev1 finding it closes
   (interrupted-fragment-outside-context). Refresh and re-attach `TASK-260929-csyzcj_results.md`.
3. Run `task-board handoff TASK-260929-csyzcj --role developer` (CR rev2).
