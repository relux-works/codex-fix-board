# TASK-260929-309h9n: hand off CR revision 1 on hosted precheck 4

Hosted precheck 4 (`TASK-260929-309h9n_hosted-precheck-4.md`, precondition, run 38160194813, ref relux/ci-next) is fully green, and all 6 mutants are killed by their named tests.
It closes the precheck 3 rework (`b2-rework-brief-precheck3.md`): the entry rule (the first continuation after a human turn, goal set/mutation or resume proceeds immediately; pacing applies only after an automatic predecessor), the pre-existing goal suite regressions, and the new entry-rule mutant.
The tree includes four orchestrator fixes; mention each: `TASK-260929-309h9n_orch-compile-fix-2.md` and `-orch-compile-fix-3.md` (mechanical compile fixes), `-orch-logic-fix-4.md` (the first goal binding keeps the recorded streak; only a different bound goal resets), and `-orch-ci-fix-4.md` (nextest slow-timeout override for the app-server end-to-end pacing test that waits a real 60 s delay).
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 4. In `TASK-260929-309h9n_results.md` list every suite that sets `CODEX_GOAL_PACING_DISABLED` with its reason and the model requests per scenario (AC8); refresh and re-attach it.
3. Run `task-board handoff TASK-260929-309h9n --role developer`.
