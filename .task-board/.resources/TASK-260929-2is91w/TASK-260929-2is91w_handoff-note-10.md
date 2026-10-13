# TASK-260929-2is91w: hand off the next CR revision on hosted precheck 10

Hosted precheck 10 (`TASK-260929-2is91w_hosted-precheck-10.md`, precondition, run 38142174620, ref relux/ci-next) is fully green, and all 13 mutants are killed by their named tests.
It closes review rev2 finding A2-F1/D-F1 (tool_search discovery must count only call/output pairs that survive prompt normalization).
The tree includes two orchestrator fixes; mention them: `a1-orch-mutant-fix-9` (regenerated the discovery_ignores_call_pairing mutant) and `TASK-260929-2is91w_orch-test-fix-10.md` (test-only: the integration test samples the post-discovery step snapshot on a second turn with a changed approval policy, because turn-context contributors re-run only on turn-context changes; precheck 9 failed on that premise).
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 10 and the finding it closes. Refresh and re-attach `TASK-260929-2is91w_results.md`.
3. Run `task-board handoff TASK-260929-2is91w --role developer`.
