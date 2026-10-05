# TASK-260929-2gp04j (G2): resume and hand off CR revision 3 on hosted precheck 5

Hosted precheck 5 (`TASK-260929-2gp04j_hosted-precheck-5.md`, precondition) ran your exact rev-2 worktree tree
fc288cc9d009923ec84e87428669fc51030712a4 (snapshot 10bc26b, run 37014493254). All lanes are green, and all 20 narrowing
mutants are killed by their intended tests, including the two new accounting/abort read-failure mutants.

1. Confirm the worktree tree still equals fc288cc9d009923ec84e87428669fc51030712a4 (temp index, `git read-tree HEAD`,
   `git add -A`, `git write-tree`). Do NOT change any file; a change invalidates the evidence.
2. Check the open checklist items, citing precheck 5's run ids and test names. Update the results and the coverage map,
   keeping the reviewer notes on `MODULE.bazel.lock` and on the 1334-line size with its two-stage split.
3. Run the busy check. When it prints FREE, run `task-board handoff TASK-260929-2gp04j --role developer`. G2 is the
   Story's final leaf, so this publishes the story_final CR. Only a printed `BUSY ...` line means HOLD.

Refresh and re-attach TASK-260929-2gp04j_results.md before the handoff (a new outcome is required).
