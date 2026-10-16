# BUG-261015-zoqjcm: hand off the CR on hosted precheck 2

Hosted precheck 2 (`BUG-261015-zoqjcm_hosted-precheck-2.md`, precondition) ran your exact worktree tree
1e7f995c89c36a718a56f2fe3e05e398927acd7c: lint, small, core and app-server all green, and 10/10 mutants killed by
named test failures.

1. Confirm the worktree tree still equals 1e7f995c89c36a718a56f2fe3e05e398927acd7c (temp index, `git read-tree HEAD`,
   `git add -A`, `git write-tree`). Do NOT change any file.
2. Tick the open checklist items, citing precheck 2 (run 38812946982). Refresh and re-attach
   BUG-261015-zoqjcm_results.md (a new outcome is required).
3. Run `task-board handoff BUG-261015-zoqjcm --role developer`. Do not run local builds for this step.
