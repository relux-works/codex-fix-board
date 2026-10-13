# TASK-260929-309h9n: hand off CR revision 2 on hosted precheck 6

Hosted precheck 6 (`TASK-260929-309h9n_hosted-precheck-6.md`, precondition, run 38188455502, ref relux/ci-next) is fully green, and all 6 mutants are killed by their named tests.
It closes review rev1 (`b2-rework-brief-review1.md`): A-F1 (production-path blocker test `goal_pacing_empty_blocker_runs_before_rescheduling` with mutant `pacing_blocker_skipped_for_paced_turns`) and A-N1 (pacing switch narrowed to the two goal_background_wait tests that need it), plus the precheck 5 test-synchronization rework (`b2-rework-brief-precheck5.md`). Mention the one flaky P4a test recorded in the precheck note.
The tree keeps the four orchestrator fixes (`-orch-compile-fix-2.md`, `-orch-compile-fix-3.md`, `-orch-logic-fix-4.md`, `-orch-ci-fix-4.md`).
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 6 and the findings it closes. Refresh and re-attach `TASK-260929-309h9n_results.md`.
3. Run `task-board handoff TASK-260929-309h9n --role developer`.
