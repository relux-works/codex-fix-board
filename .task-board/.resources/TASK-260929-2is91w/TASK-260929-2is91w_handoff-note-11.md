# TASK-260929-2is91w: hand off the next CR revision on hosted precheck 11

Hosted precheck 11 (`TASK-260929-2is91w_hosted-precheck-11.md`, precondition, run 38152963091, ref relux/ci-next) is fully green, and all 14 mutants are killed by their named tests.
It closes review rev3 finding A3-F1/D3-F1: `discovered_waiting_tools_from_history` now mirrors the normalizer's orphan rule (a completed server `ToolSearchOutput` with `call_id: null` counts; a client output needs a matching call), killed by the new `discovery_requires_server_call_id` mutant.
The tree keeps the orchestrator's test-only fix `TASK-260929-2is91w_orch-test-fix-10.md` (the integration test samples the post-discovery step snapshot on a second turn with a changed approval policy); mention it.
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 11 and the finding it closes. Refresh and re-attach `TASK-260929-2is91w_results.md`.
3. Run `task-board handoff TASK-260929-2is91w --role developer`.
