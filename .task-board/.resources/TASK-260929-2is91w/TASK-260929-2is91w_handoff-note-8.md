# TASK-260929-2is91w: hand off the next CR revision on hosted precheck 8

Hosted precheck 8 (`TASK-260929-2is91w_hosted-precheck-8.md`, precondition, run 38092565667) is fully green, and all 12 mutants are killed by their named tests.
It closes review rev1 findings A-F1 (native wait provenance) and A-F2 (tool_search-discovered tools). The tree includes three orchestrator mechanical fixes (orch-lint-fix-5/6/7: cfg(test) removal on ToolRegistry::tool_exposure, redundant closures, two test clippy lints); mention them.
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 8 and the findings it closes. Refresh and re-attach `TASK-260929-2is91w_results.md`.
3. Run `task-board handoff TASK-260929-2is91w --role developer`.
