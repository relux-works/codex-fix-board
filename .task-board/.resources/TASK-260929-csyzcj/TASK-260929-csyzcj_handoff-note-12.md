# TASK-260929-csyzcj: hand off CR rev4 on hosted precheck 12

Hosted precheck 12 (`TASK-260929-csyzcj_hosted-precheck-12.md`, precondition, run 38077935582) is fully green, and all 9 mutants are killed by their named tests (including spawn_task_name_length_unchecked).
The tree includes the orchestrator's test-only fixture fix (g1-orch-test-fix-11.md: source-valid 914-byte paths, since the new AgentPath bound rejects 2006-byte ones); mention it. It closes review rev3's finding with the AgentPath source bound (MAX_SEGMENT_BYTES 128, MAX_PATH_BYTES 1024).
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 12 and the finding it closes. Refresh and re-attach `TASK-260929-csyzcj_results.md`.
3. Run `task-board handoff TASK-260929-csyzcj --role developer` (CR rev4).
