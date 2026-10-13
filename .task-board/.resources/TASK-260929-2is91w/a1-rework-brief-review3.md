# TASK-260929-2is91w (P3-1): review rev3 changes_requested. Mirror the normalizer's orphan rule exactly, then request precheck 11

The verdict is `TASK-260929-2is91w_review-verdict-rev3.md`: A3-F1 (panel A) and D3-F1 (delta) are the same defect. Panel B accepted.
The rev2 orphan fix (client outputs need a matching call) is correct and stays. Its regression: in
`discovered_waiting_tools_from_history` (`core/src/tools/waiting_capabilities.rs`) the match on `call_id` returns false for every
`None`, so a completed SERVER `ToolSearchOutput` with `call_id: null` (a supported protocol shape:
`protocol::models::tests::tool_search_server_items_allow_null_call_id`) is ignored, although history and `for_prompt` keep it and
the model receives the definition. `native_wait` then stays None while the tool is callable.

## Required

1. Discovery must count exactly the ToolSearchOutputs that `remove_orphan_outputs` (`core/src/context_manager/normalize.rs`, the
   ToolSearchOutput arm) keeps. That arm drops ONLY `call_id: Some(id)` with `execution != "server"` and no `ToolSearchCall` with
   that id anywhere in the history. Everything else (server with any call_id, including None; client with a matching call;
   client with `call_id: None`) is retained, so it must count. Mirror that predicate exactly (same set of call ids: collect all
   ToolSearchCall ids first, as the normalizer does), so the two cannot disagree. Keep it small; no refactor of tool_search.
2. Tests:
   - unit (`waiting_capabilities_tests.rs`): extend `server_tool_search_output_counts_without_call` to cover both
     `Some("server-search-1")` and `/*call_id*/ None` with execution `server`; keep the orphan-client refusal and the paired-client
     acceptance tests; add one case asserting a client output with `None` call_id is treated exactly as the normalizer treats it.
   - integration (`core/tests/suite/search_tool.rs`): `server_null_id_discovery_updates_waiting_capabilities` (name must contain
     `discover`): emit a completed server tool_search_output with `call_id: null` carrying the deferred `multi_agent_v1.wait_agent`
     loadable spec via `response.output_item.done`, finish the response, then a second turn with a changed approval policy (as
     `discovered_native_wait_updates_waiting_capabilities` does, because turn-context contributors run only on turn-context
     changes). Assert the next request carries the definition and the recorder sees `native_wait = Some(actual name)` on the
     second turn and None before.
   - mutant (add to the mutants JSON; keep the other 13 applying to the final tree): require a non-null id for server outputs;
     killers: the extended unit test and the new integration test.
3. Results: state the predicate equivalence with the normalizer arm (file and line) and list the cases.

`mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item` then `--check` must exit 0; no other cargo;
no CODEX_HOME copies; delete temp dirs. Avoid the recurring hosted lint failures (redundant closures, `vec!` where an array works,
single-arm match, cfg(test)-only helpers used from production, unused imports, `/*param*/` comments on positional literals).
Leave everything UNCOMMITTED, report the final tree id after fmt, add the note `HOSTED-PRECHECK-REQUESTED: precheck 11`, and end
your turn without handing off. The mutant filter stays the precheck 10 filter (it already includes `test(discover)` and
`test(search_tool)`).
