# TASK-260929-1w5ivu: hand off CR revision 2 on hosted precheck 5

Hosted precheck 5 (`TASK-260929-1w5ivu_hosted-precheck-5.md`, precondition, run 38265238386, ref relux/ci-next, tree
786339645058198ba030dffbba8ed1cfbf1e36a9) is fully green: lint, small, core and app-server. All 8 mutants are killed by
their named tests, including `waiting_world_state_always_renders` and `waiting_world_state_no_retraction`.

The candidate is the review-1 rework (World State move) plus two mechanical orchestrator fixes. Both are attached as
preconditions:
- `TASK-260929-1w5ivu_orch-lint-fix-4.md`: precheck 3 failed lint on base drift. The suite fixture needed P4b's
  `continuation_pacing` field.
- `TASK-260929-1w5ivu_orch-test-fix-5.md`: precheck 4 failed 9 suite tests. The section snapshot wrote
  `"native_wait": null`, which core strips before persisting, so the snapshot never compared equal and the fragment
  re-rendered on every step. An absent name is now omitted. One unit pin changed; no suite assertion changed.

1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the
   worktree. It must exit 0 for tree 78633964. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 5. Refresh and re-attach `TASK-260929-1w5ivu_results.md`:
   - retitle it for CR revision 2 on precheck 5;
   - record both orchestrator fixes and the snapshot null round-trip (unit tests compared an unstripped snapshot with
     itself; only the suite exercises core persistence);
   - update the size figures from the actual diff (`waiting_world_state.rs` is now 140 lines);
   - keep the disclosures: size vs the 600 target, BudgetLimited gate scope, compaction covered at unit level, unit-only
     coverage for native mail wait and the positive exec sentence, the deferred no-wait paragraph, and the AC3 amendment
     (one transition retraction).
3. Run `task-board handoff TASK-260929-1w5ivu --role developer`.
