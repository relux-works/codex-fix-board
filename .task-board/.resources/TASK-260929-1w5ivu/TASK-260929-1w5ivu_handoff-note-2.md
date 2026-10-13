# TASK-260929-1w5ivu: hand off CR revision 1 on hosted precheck 2

Hosted precheck 2 (`TASK-260929-1w5ivu_hosted-precheck-2.md`, precondition, run 38239371527, ref relux/ci-next, tree
3685fd24) is fully green: lint, small, core and app-server. All 7 mutants are killed by their named tests.
- It closes precheck 1 (run 38223961011, 4 deterministic `waiting_guidance` failures; `a2-rework-brief-precheck1.md`).
- F2 and F3 expectations were corrected on code references.
- For F1, the orchestrator decision is recorded in the task notes: the turn-boundary bound is accepted as the P3-2
  contract, and per-step re-emission is a follow-up. Both bounded windows are pinned in
  `waiting_guidance_tool_created_goal_reacts_at_next_turn`. State this in the results as an accepted, disclosed bound.
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0 for tree 3685fd24. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items (3/4/5), citing precheck 2. Refresh and re-attach `TASK-260929-1w5ivu_results.md`:
   - replace the "DECISION REQUESTED" line with the recorded orchestrator decision;
   - keep the size note (1376 vs 600), the BudgetLimited gate scope, the unit-only coverage for native mail wait and the positive exec sentence, and the deferred no-wait paragraph.
3. Run `task-board handoff TASK-260929-1w5ivu --role developer`.
