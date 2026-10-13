# TASK-260929-2is91w (P3-1): review rev2 changes_requested. Count only REAL tool_search discoveries, then request precheck 9

The verdict is `TASK-260929-2is91w_review-verdict-rev2.md` (A2-F1 from panel A and D-F1 from the delta reviewer: the same defect).
A-F1 (native provenance) is closed. A-F2 is not:
- `discovered_waiting_tools_from_history` accepts any `ResponseItem::ToolSearchOutput` with a matching tool name. It does not check
  that a client-executed output has a corresponding `ToolSearchCall`. `HistoryManager::for_prompt` / `ContextManager::normalize_history`
  -> `remove_orphan_outputs` removes such orphan client outputs before sampling (debug: error_or_panic). So an orphan output can turn
  on a deferred native_wait / sleep flag although the model never receives that tool definition.
- `discovered_v1_wait_updates_next_step_snapshot` injects exactly that orphan (call_id search-wait-1, execution client, no
  ToolSearchCall) and never builds a sampling request, so it proves a fabricated input.

Required:
1. Discovery must use only tool_search outputs that survive prompt normalization: for client execution, require the matching
   `ToolSearchCall` (same call_id) earlier in history; server execution as the normalizer treats it. Prefer deriving from the same
   normalized view the request uses (or reuse the normalizer's orphan rule) rather than a second hand-written rule; keep it small.
2. Tests:
   - unit: an orphan client ToolSearchOutput does NOT count; a call+output pair does (waiting_capabilities_tests.rs);
   - fix `discovered_v1_wait_updates_next_step_snapshot` to record the ToolSearchCall + output pair;
   - one integration test in `core/tests/suite/search_tool.rs` (name containing `waiting_capabilit` or `discover`) that drives a REAL
     tool_search via the mock responses server, then asserts the NEXT request exposes the discovered wait tool AND the step's
     WaitingCapabilities reports it (and that before discovery it is None);
   - mutant: one that drops the call/output pairing check, killed by the orphan unit test and/or the integration test.
3. Keep existing behavior otherwise; no refactor of tool_search.
`mini-producer-addendum.md` applies (cargo fmt required, no other cargo, no real CODEX_HOME copies, delete temp dirs). Also avoid the
clippy lints the orchestrator fixed by hand last round (redundant closures, useless vec!, single-arm match, cfg(test)-only helpers
used from production). All mutant patches must apply to the final tree. Leave everything UNCOMMITTED, report the final tree id AFTER
fmt, add the note `HOSTED-PRECHECK-REQUESTED: precheck 9`, and end your turn without handing off.
The mutant filter adds `test(search_tool) | test(orphan) | test(tool_search)`.
