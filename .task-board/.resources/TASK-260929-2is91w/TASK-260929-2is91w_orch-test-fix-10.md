# TASK-260929-2is91w (P3-1): orchestrator test fix before precheck 10

Precheck 9 (run 38135460829, snapshot efeaab62, tree 092dfe4b): lint, small and app-server green; core red on exactly one
test, `suite::search_tool::discovered_native_wait_updates_waiting_capabilities` (3/3 tries):
`expected pre- and post-discovery samples, got 1` (core/tests/suite/search_tool.rs:1038). Mutant results are void.

Cause (test premise, not product): turn-context contributors run only on full initial context
(`build_initial_context_with_world_state`) and when the TurnContextItem changes
(`record_context_updates_and_set_reference_context_item`, `!should_inject_full_context && turn_context_changed`).
The second sampling step of the same turn has an unchanged TurnContextItem, so the recorder never sees the
post-discovery step snapshot. The per-step derivation itself (`session/mod.rs` step context ->
`discovered_waiting_tools_from_history`) is untouched. Re-emission on a flag flip is P3-2 AC6, not this leaf.

Fix (test only, `core/tests/suite/search_tool.rs`): a third mocked response and a second user turn with
`AskForApproval::OnRequest` (a TurnContextItem change), so the contributors run on that turn's first step, whose snapshot
derives from the paired tool_search call/output in history. `requests.len()` is now 3; all other assertions unchanged.
No product code changed. `cargo fmt -- --config imports_granularity=Item --check` exit 0. New tree f8ae85582d54.
All 13 mutants of a1-mutants-9.json apply unchanged (`git apply --check`), reused as a1-mutants-10.json.
