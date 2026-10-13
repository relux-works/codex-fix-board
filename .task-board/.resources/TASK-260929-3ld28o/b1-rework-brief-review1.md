# TASK-260929-3ld28o (P4b-1): review rev1 changes_requested. Fix A-F1 (bypass) and the coverage findings, then request precheck 5

The merged verdict is `TASK-260929-3ld28o_review-verdict-rev1.md` (precondition). Panel A (codex sol high) requested changes;
panel B (muse max) accepted, with robustness findings F1 and F2 that are folded in here. Precheck 4 was fully green and killed
10/10 mutants. `mini-producer-addendum.md` applies (cargo fmt allowed and required; no other cargo). Your Story worktree may
be refreshed onto a newer trunk with CI-only commits; that is fine.

1. A-F1, bypass, MUST fix in production: a REJECTED send_input is counted as a reset. V1 `send_input.rs:95-131` captures a failed
   send, then emits a Completed CollabAgentToolCall built from `get_status` (not from the send result) before propagating
   `result?`. `multi_agents.rs:86-94` maps Running and other non-error statuses to Completed. `AgentControl::send_input` maps
   NotSubmitted to InvalidRequest (`control.rs:130-156`), and a Compact-task child refuses steering while it stays Running
   (`turn_input.rs:718-722, 372`). So `GoalExtension::on_item_completed` (`extension.rs:342-344` -> `accounting.rs:295-304`)
   counts a rejected send. Bind the observation to the DELIVERY RESULT at its committing path, so that a rejected send never
   counts and an accepted send always counts, including when the child errors afterwards. Do not repurpose the presentation
   status as acceptance evidence. Add a test with a refused send (for example, a child in a Compact task) asserting no
   observation, plus a narrowing mutant that counts on status instead of the delivery result.
2. A-F2, code-mode coverage (AC3): the unit test only calls accounting methods on a locally included `accounting.rs`, so it
   never runs code mode. Add an integration test through the real path: `functions.exec` -> CodeModeExecuteHandler ->
   `submit_nested_tool` (`core/src/tools/code_mode/mod.rs:335-412`) with a nested apply_patch. Assert exactly one observation
   for the nested leaf and none for the wrapper, BEFORE `finish_turn` clears the counts. Add a mutant that records the wrapper's
   success for CodeMode, or double-emits the nested completion, and have this test kill it. Fix the results table:
   `code_mode_leaf_counts_once_and_wrapper_adds_none` cannot kill `tool_finish_success_records_mutation` (panel B note).
3. A-F3 and F1, goal mutation coverage: replace the deletion-only `goal_update_does_not_record` with a NARROWING mutant
   (record updates only when `args.status == Complete`). Kill it with tests that go through actual update dispatch for
   `paused` and `blocked` (`tool.rs:280-290`). Drive the external set and clear through their production call sites
   (`runtime.rs` `apply_external_goal_set` / `apply_external_goal_clear`, 388-395 and 439-446) with observation assertions,
   and give each a deletion-surviving-today mutant with a killer.
4. F2: feed `CollabAgentTool::SendMessage` and `FollowupTask` Completed items in tests, and split the bundled
   `spawn_only_spawn_agent_counts` mutant so that dropping exactly SendMessage|FollowupTask is killed by its own test.
5. Size: the change is already about 1060 lines. Keep the additions to tests and the minimal production fix for item 1. Do not
   refactor.
Run cargo fmt plus `--check` (exit 0). Every mutant patch must apply to your final tree. Leave everything UNCOMMITTED, report the
final tree id, add the note `HOSTED-PRECHECK-REQUESTED: precheck 5`, and end your turn without handing off. List any new killer
test names that the CI mutant filter below would miss:
`test(observation) | test(state_change) | test(plan) | test(spawn) | test(code_mode_leaf) | test(empty_blocker) | test(goal_mutation) | test(goal_update) | test(goal_create) | test(file_change) | test(shell_success) | test(tool_lifecycle) | test(tool_finish) | test(agent_message) | test(send_input) | test(model_text)`.
