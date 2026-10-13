# TASK-260929-2is91w (P3-1): review rev1 changes_requested. Two flag-derivation regressions, then request precheck 5

Verdict `TASK-260929-2is91w_review-verdict-rev1.md`: panel B accepted; panel A found two regressions.

1. A-F1 (flag derivation): `find_direct_wait_agent` matches any visible function/custom/namespace tool named `wait_agent`, without
   checking the native backend, the configured native identity or the runtime provenance. With native agents disabled, a dynamic
   `foreign.wait_agent` (thread/start dynamicTools -> TurnContext.dynamic_tools -> build_tool_router ->
   append_dynamic_tool_runtimes) is advertised as `native_wait = Some(foreign.wait_agent)`, but calling it reaches
   DynamicToolHandler, not a native wait. The same happens with V2 `wait_agent_enabled=false` and an unrelated namespaced
   `wait_agent`. Fix: derive native_wait from the CONFIGURED native identity and provenance in the captured plan (V1 or V2 native
   handler), then check that its exposure is callable. Keep arbitrary valid configured V2 namespaces working. Tests: a foreign
   dynamic wait_agent with native disabled gives None; V2 disabled plus a namespaced wait_agent gives None; the configured V2
   namespace gives Some(actual name). Add a mutant (bare-name match) killed by the foreign-tool test.
2. A-F2 (final-router derivation): the snapshot reads only `ToolRouter.model_visible_specs`, which drops non-direct exposures. With tool
   search on, V1 native tools are Deferred, and after a successful `tool_search` they are CALLABLE through tool_search_output
   history, but the snapshot still reports `native_wait = None` (the same applies to any deferred-then-discovered flag). Fix:
   include the discovered callable surface, meaning tools loaded by tool_search in this thread's history, while keeping the
   exclusion, collision and undiscovered refusals. Tests: undiscovered deferred gives None (existing); after a public-entry
   tool_search that loads the V1 wait tool, the next step's snapshot gives Some(name). Add a mutant (ignore discovered tools)
   killed by the second test.
Keep changes minimal; the change is already about 1440 lines. `mini-producer-addendum.md` applies. Run cargo fmt plus `--check`
(exit 0). All mutants must apply to your final tree. Leave everything UNCOMMITTED, report the final tree id, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 5`, and end your turn without handing off.
