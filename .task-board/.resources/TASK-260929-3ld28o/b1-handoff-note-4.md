# TASK-260929-3ld28o (P4b-1): hand off on hosted precheck 4

Hosted precheck 4 (`TASK-260929-3ld28o_hosted-precheck-4.md`, precondition) is fully green, and all 10 mutants are killed. Its tree
includes two test-only orchestrator edits (`b1-orch-compile-fix.md`): the E0382 label fix and `#![allow(clippy::expect_used)]` in
ext/goal/tests/state_change_observations.rs. Mention both in your results.
1. Your Story worktree may have been refreshed onto trunk 07c018be (CI-only commits). Compute the tree (temp index:
   `git read-tree HEAD`, `git add -A`, `git write-tree`). It must equal EITHER 3dbcad941982fa04b3bdc899e697cfc4295154e8 (old base 39c264c)
   OR f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0 (refreshed). Do NOT change any file. If it is neither, stop and add a note.
2. Check the open checklist items, citing precheck 4 (run 38013874463). Refresh and re-attach `TASK-260929-3ld28o_results.md`.
   Note the change size (13 files, about 1060 lines, most of them tests) for the reviewers.
3. Run `task-board handoff TASK-260929-3ld28o --role developer`.
