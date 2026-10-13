# Merged review verdict — TASK-260929-2is91w CR revision 2 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261011-1zp0ru_panel-verdict.md` (changes_requested), `TASK-261011-2yj58v_panel-verdict.md` (accept), `TASK-261011-1sgzye_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A2-F1",
      "row": "final-router derivation",
      "invariant": "AC2: deferred-not-callable tools remain false until discovery makes them callable for this sampling step. Discovery evidence must survive the normalization used for the actual model request.",
      "mechanism": "capture_step_context_inner scans state.history.raw_items() before request preparation. discovered_waiting_tools_from_history accepts every ToolSearchOutput with a matching name, without checking whether a client output has a corresponding ToolSearchCall. In the release sampling path, HistoryManager::for_prompt removes such orphan client outputs; in debug builds error_or_panic panics instead. Thus an orphan output can enable a deferred native_wait snapshot although its definition is never delivered to the model. The new discovered_v1_wait_updates_next_step_snapshot test supplies exactly this orphan shape (call_id search-wait-1, execution client, no ToolSearchCall), captures the next step and asserts Some, but never builds a sampling request. Resume/fork reconstruction replays ResponseItems into raw history without this normalization, so a validly serialized but interrupted/inconsistent rollout reaches the discrepancy. This is a robustness defect in the new discovery evidence, not a claim that ordinary paired successful searches fail. Preserve legitimate standalone server outputs, which the existing normalizer explicitly allows.",
      "sources": [
        "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/session/mod.rs:3971-3982",
        "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/tools/waiting_capabilities.rs:91-107,175-188",
        "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/context_manager/history.rs:581-603,933-940",
        "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/context_manager/normalize.rs:160-223",
        "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/session/turn.rs:462-520",
        "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/session/rollout_reconstruction.rs:415-425",
        "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/tools/waiting_capabilities_tests.rs:1058-1113",
        "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/util.rs:error_or_panic"
      ],
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/search_tool.rs (requested additional integration test; not added)",
          "command": "just test -p codex-core -E 'test(=suite::search_tool::orphaned_search_output_does_not_enable_native_wait)'",
          "expected_failure": "Requested, NOT EXECUTED. Resume/fork a fixture with a user turn and a completed client ToolSearchOutput loading multi_agent_v1.wait_agent, call_id orphan-search, with no matching ToolSearchCall; retain V1/search-enabled configuration and a recording contributor. Capture the first sampling step and require native_wait=None or an explicit pre-capture refusal of invalid history. Candidate capture yields Some. In release mode, assert the actual outbound request omits the orphan definition; in debug mode the later normalizer panics. Add a real tool_search round-trip positive control with a paired call/output, next-step Some and a subsequent native wait invocation. Do not use raw orphan injection as the positive control.",
          "execution": "requested_not_run",
          "pinned_blobs": [
            "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/tests/suite/search_tool.rs (requested additional integration test; not added)"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261011-1zp0ru"
      ]
    },
    {
      "id": "D-F1",
      "row": "final-router derivation",
      "invariant": "A-F2 rework requires a valid public-entry tool_search -> next sampling regression, with a narrowing mutant killed by that regression. A supplied raw history value that cannot survive prompt normalization does not establish discovery made the tool callable to the model.",
      "mechanism": "discovered_v1_wait_updates_next_step_snapshot constructs a real loadable spec but injects ResponseItem::ToolSearchOutput directly with execution=client and call_id=search-wait-1, never recording the corresponding ToolSearchCall. It calls record_conversation_items and capture_step_context, then stops. Capture scans raw_items and returns Some(native wait). Real run_turn subsequently calls clone_history().for_prompt; ContextManager::normalize_history calls remove_orphan_outputs, whose client-output arm rejects this exact unmatched call_id (debug panic, release removal). Thus the green transition test and its mutant kill attest a fabricated discovery input, not the required actual search/next-request transition. Existing suite::search_tool tests drive real search but do not observe WaitingCapabilities. This is a confirmed fixture/proof defect, not an established production failure for well-formed search history.",
      "sources": [
        "codex-rs/core/src/tools/waiting_capabilities_tests.rs:1058-1114",
        "codex-rs/core/src/session/mod.rs:3971-3981",
        "codex-rs/core/src/session/turn.rs:516-523",
        "codex-rs/core/src/context_manager/history.rs:539-579,580-603,933-941",
        "codex-rs/core/src/context_manager/normalize.rs:201-210",
        "codex-rs/core/src/context_manager/history_tests.rs:2637-2670",
        "codex-rs/core/tests/suite/search_tool.rs:554-834,837 onward"
      ],
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/tools/waiting_capabilities_tests.rs",
          "command": "just test -p codex-core -E 'test(=tools::waiting_capabilities::tests::discovered_v1_wait_updates_next_step_snapshot)'",
          "expected_failure": "Diagnostic extension REQUESTED, NOT RUN: immediately after the second capture, call session.clone_history().await.for_prompt(&second.settings.model_info.input_modalities) and assert that its client tool_search_output with call_id search-wait-1 remains present. Debug builds panic with Orphan tool search output for call id: search-wait-1; release builds remove it and fail the presence assertion. The existing unextended test passes in the hosted log; do not report it as currently failing. The normalization branch and the existing debug should_panic test independently corroborate this static witness.",
          "pinned_blobs": [
            "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/src/tools/waiting_capabilities_tests.rs"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/search_tool.rs (requested integrated regression)",
          "command": "just test -p codex-core -E 'test(=suite::search_tool::discovered_native_wait_updates_waiting_capabilities)'",
          "expected_failure": "REQUESTED, NOT RUN: use build_with_auto_env plus the existing recording-contributor pattern from exec_notification.rs. Script a real tool_search call for deferred multi_agent_v1.wait_agent, require native_wait=None before search and Some(actual name) afterward, assert completed client search output and matching call survive in the next outbound request, and execute the discovered native wait as a control. Re-run native_wait_ignores_discovered against this test on the reworked exact tree; it must fail. Do not satisfy this request solely by inserting a ToolSearchCall beside the fabricated output.",
          "pinned_blobs": [
            "ef4eb6ff644eee2a950b493b675fb86f7b3301c2:codex-rs/core/tests/suite/search_tool.rs (requested integrated regression)"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261011-1sgzye"
      ]
    }
  ],
  "notes": [
    "[TASK-261011-1zp0ru] The replay matches exactly. Reviewed candidate source and adjacent production paths were read from the pinned tree with git show; early adjacent worktree reads were superseded by pinned reads.",
    "[TASK-261011-1zp0ru] Hosted identity independently verified: the workflow dispatch head is base e0eff057..., but the plan and snapshot job check out snapshot commit 7917d62f1cdbcbe68242c61ca01decd925e1a8c3. GitHub commit API identifies its tree as the reviewed ef4eb6ff... . Do not equate the workflow head SHA with the tested snapshot.",
    "[TASK-261011-1zp0ru] GitHub run 38092565667 overall conclusion is FAILURE, as expected for mutant jobs. Lint and snapshot small/core/app-server job conclusions are success; all 12 mutant core jobs are failure. Snapshot core log: 5115/5115 passed, 11 skipped, one flaky test. Four mutant raw logs were inspected: provenance 5 failing tests, discovery 2, sleep 2, stdin 2; each failed gate exited 100. These are expected-red kills, not passing mutant gates. Other eight kills are accepted from the attached precheck report and independently checked job conclusions; their raw logs were not inspected.",
    "[TASK-261011-1zp0ru] Numeric command exits for hosted lint/small/app-server are not present in the attached summary; only their success conclusions are claimed. No build, cargo, just, or test command ran locally in this panel.",
    "[TASK-261011-1zp0ru] Prior A-F1 runtime provenance and prior A-F2 genuine deferred discovery mechanics are addressed. A2-F1 concerns invalid/raw discovery evidence, a distinct new robustness mechanism; it is not a repeated bare-name or direct-only finding.",
    "[TASK-261011-1zp0ru] AC4 installed-goal pointer identity and AC5 real remote replacement are not independently exercised end-to-end by the added tests. Goal registration is statically verified. A public tool_search round-trip must replace the current orphan positive fixture; the original A-F2 request for an end-to-end search test was not implemented.",
    "[TASK-261011-1zp0ru] Change size is 1996 changed lines (+1990/-6 across 20 files), exceeding the 800-line guidance. 1359 lines are in the test module; implementation is separately bounded. Recording reviewer should explicitly assess a split or size exception; no style-only blocking finding is added here.",
    "[TASK-261011-1zp0ru] TurnContextContributionInput adds a required public Rust field, a source-breaking change for out-of-tree struct-literal constructors. In-repository constructors are updated. No app-server wire, CLI, config schema or rollout schema changes were found in the bounded sweep. No new context fragment or model-visible token payload is emitted.",
    "[TASK-261011-1zp0ru] All board writes in this run are restricted to TASK-261011-1zp0ru. Nothing was accepted/rejected, status-changed, handed off, noted or attached on TASK-260929-2is91w.",
    "[TASK-261011-2yj58v] [TASK-261011-2yj58v] Evidence identity: replay is exact (ef4eb6ff), and hosted precheck 8 ran on that exact tree: run 38092565667, lanes lint/small/core/app-server success, 12/12 mutants killed with named killers. This closes the rev1 evidence-identity limitation; 7/7 rows have exact-candidate runtime support where a runtime leg exists.",
    "[TASK-261011-2yj58v] [TASK-261011-2yj58v] Rev1 regressions closed: A-F1 (bare-name native wait) is fixed by registry-provenance selection (CoreToolRuntime::is_native_wait_tool, true only in V1/V2 handlers plus the delegating V2 wrapper) and killed on the exact tree by native_wait_bare_name_match via three foreign/decoy tests. A-F2 (discovered tools invisible) is fixed by discovered_waiting_tools_from_history plus deferred-aware is_callable and killed by native_wait_ignores_discovered via the synthetic and production-capture discovered-V1 tests, including a false-before/true-after production-capture leg built through the real to_loadable_spec conversion.",
    "[TASK-261011-2yj58v] [TASK-261011-2yj58v] Change size 1990 insertions / 6 deletions across 20 paths exceeds the 800-line guidance; 1359 lines are the AC-mandated named-test matrix in waiting_capabilities_tests.rs and 275 are the new derivation module. Mechanical-test overrun in the same accepted pattern as rev1; production deltas outside the new module are small and additive.",
    "[TASK-261011-2yj58v] [TASK-261011-2yj58v] update_plan_enabled replacement staged: runtime.rs call sites are byte-identical to base and steering.rs continuation rendering is untouched (only additive waiting_capability_fragments returning empty). Zero behavior loss; the literal scope replacement stays deferred to the guidance leaf TASK-260929-1w5ivu per the boundary both rev1 panels accepted.",
    "[TASK-261011-2yj58v] [TASK-261011-2yj58v] Remote-catalog residual: snapshot_follows_catalog_clock_support proves both ModelInfo clock legs through the production router builder, and remote/bundled replacement itself is pre-existing models-manager behavior with its own suite (manager_tests.rs) untouched by this CR, but no single test chains a mocked remote fetch into a sampling snapshot. The candidate has no catalog input and no mechanism to ignore remote entries, so the row holds; the chained test is named here as a non-blocking evidence gap.",
    "[TASK-261011-2yj58v] [TASK-261011-2yj58v] V2 namespace length bound: tool_namespace config validates charset plus the reserved functions name but sets no length cap, so native_wait heap is bounded by operator config rather than a constant. Accepted: single transient string, never persisted, operator-controlled input only; foreign/dynamic namespaces can no longer reach the snapshot after the A-F1 fix.",
    "[TASK-261011-2yj58v] [TASK-261011-2yj58v] No model-context injection: the goal contributor returns an empty fragment list for every snapshot value (steering test covers none() and full), both session paths push only returned fragments, and no prompt text, template, or rollout/history schema changed. No item over 1k tokens is introduced.",
    "[TASK-261011-2yj58v] [TASK-261011-2yj58v] TurnContextContributionInput gains a required waiting_capabilities reference: source-breaking for Rust struct-literal constructors. All in-repo constructors are updated (both session paths, extension-api registry test, core recording tests) and hosted lint on the exact tree is green. No app-server wire, CLI, config, or session-resume surface changes: the 20-path diff touches only core session/tools, extension-api, goal, and tests.",
    "[TASK-261011-1sgzye] A-F1 fixed: CoreToolRuntime defaults native provenance to false; only the two native wait handlers and the V2 wrapper report it. ToolRouter reads the final registry. Dynamic/MCP/extension wait_agent decoys cannot mint native provenance. Arbitrary valid V2 namespaces retain their actual identity. Hosted bare-name mutant fails five tests, including foreign/disabled-V2 cases. Native-only provenance also closes the previous oversized foreign-namespace consequence.",
    "[TASK-261011-1sgzye] A-F2 production fix holds statically for well-formed retained search output: deferred names must be discovered AND still deferred in the finalized registry. Undiscovered, excluded, absent and nested-only entries remain false. The discovered-V1 helper and capture tests fail under native_wait_ignores_discovered, but neither dispatches tool_search through a user turn. D-F1 identifies the capture fixture's invalid client history rather than repeating A-F2's old false-negative mechanism; repeat-of is therefore none.",
    "[TASK-261011-1sgzye] Hosted snapshot core log records 5115/5115 passed and 11 skipped, including the discovery fixture, foreign-decoy cases, snapshot pointer test, acknowledged-subscription suite, persistence comparison, and normalize_removes_orphan_client_tool_search_output_panics_in_debug. The expected-panic normalization test passing is evidence that the discovery fixture bypasses a real boundary; it is not a runtime execution of the proposed diagnostic extension.",
    "[TASK-261011-1sgzye] Remote-catalog coverage remains a stated blind spot: snapshot_follows_catalog_clock_support mutates an already resolved ModelInfo, bypassing remote fetch/replacement. Manager apply_remote_models replaces matching slugs, and construct_model_info preserves the selected entry, so no production catalog defect was established statically. No integrated remote-replacement-to-WaitingCapabilities test or corresponding mutant was found.",
    "[TASK-261011-1sgzye] Scope staging remains explicit: update_plan_enabled in goal runtime/steering is unchanged and replacement is assigned to TASK-260929-1w5ivu. This preserves existing behavior but does not satisfy the literal replacement in this leaf by itself; prior merged review already acknowledged that boundary.",
    "[TASK-261011-1sgzye] Full change size is 1996 changed lines across 20 paths, including a 1359-line new test module; delta since revision 1 is 770 changed lines. The full change exceeds repository 800-line guidance and is not wholly mechanical. Recording review should explicitly assess the exception or consolidate repeated test setup without removing the missing integrated regression.",
    "[TASK-261011-1sgzye] TurnContextContributionInput gains a required public Rust field, which is source-breaking for downstream struct literals. All three in-repository constructors are updated. The bounded sweep found no app-server wire, CLI, config-schema, dependency-lockfile, or persisted-session shape change. Goal emits no fragments, so no new model-visible item or history rewrite is introduced.",
    "[TASK-261011-1sgzye] All runtime evidence was reused from the exact frozen candidate, with snapshot commit/tree identity independently verified; no earlier different-tree precheck was used to assert this candidate green. Overall hosted workflow is failure because the mutant jobs correctly fail. Successful log retrieval has exit 0 even when the retrieved test command exits 100."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "finding_ids": [],
      "attack": "Trace every conjunct and native runtime provenance; compare V1/V2/custom namespace and foreign-tool attacks with hosted narrowing failures.",
      "evidence": "waiting_capabilities.rs:44-79,218-275; router.rs:233-238; registry.rs:86-94; both native wait handlers and V2 wrapper. Exact-tree precheck 8 reports 12/12 kills. Independently read native_wait_bare_name_match core job 114333300702: five named tests fail, exit 100. The prior A-F1 name/provenance defect is addressed.",
      "reported_by": "TASK-261011-1zp0ru"
    },
    {
      "row": "final-router derivation",
      "result": "broken",
      "finding_ids": [
        "A2-F1"
      ],
      "attack": "Trace final registry exclusions/collisions and deferred discovery through raw history, normalized request input, resume reconstruction and the positive fixture.",
      "evidence": "A2-F1 sources. A-F2 direct-only defect is addressed for genuine discovered outputs: exact-tree discovery mutant core job 114333300779 fails two tests, exit 100. Its capture test currently treats an orphan as successful discovery and does not exercise normalization.",
      "reported_by": "TASK-261011-1zp0ru"
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "finding_ids": [],
      "attack": "Inspect receipt/pending provider independence and the public user-turn exec notification path.",
      "evidence": "waiting_capabilities.rs:64-79 reads only host/policy markers; tests.rs:666-687 compares pending/ack providers. Exact-tree snapshot core log shows suite::exec_notification::acknowledged_subscription_does_not_flip_waiting_capabilities PASS (2.869s), exercising exec launch, acknowledged receipt, idle completion wake and another user turn.",
      "reported_by": "TASK-261011-1zp0ru"
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "finding_ids": [],
      "attack": "Follow one capture, StepContext field ownership, both contribution inputs and installed goal ContextContributor; inspect pointer recorder test.",
      "evidence": "session/mod.rs:3977-4000,4312-4315,4410-4413; step_context.rs:44-47; ext/goal/src/extension.rs:616-630,767; extension-api/src/registry.rs:113-114. Exact-tree core log reports same_snapshot_instance_reaches_both_context_paths PASS. Goal wiring is verified statically; the goal renderer test calls the empty renderer directly and is not an independent installed-goal pointer attack.",
      "reported_by": "TASK-261011-1zp0ru"
    },
    {
      "row": "configuration coverage",
      "result": "not-attacked",
      "finding_ids": [],
      "reason": "Partial exact-tree attacks cover sleep switches, headless markers, code-mode and excluded receipt/exec tools. The named catalog test mutates an already resolved ModelInfo.experimental_supported_tools, so it bypasses remote catalog fetch and replacement. No snapshot observation through real remote catalog replacement is demonstrated. This is an entry-point coverage limitation, not the local build prohibition.",
      "attack": "Compare snapshot_follows_catalog_clock_support with ModelsManager::apply_remote_models and final router consumption.",
      "evidence": "waiting_capabilities_tests.rs:855-888; models-manager/src/manager.rs:672-702. Snapshot core log reports the helper test PASS. Precheck 8 reports the other configuration tests green.",
      "requested_attack": {
        "test_file": "codex-rs/core/tests/suite/search_tool.rs or a new waiting_capabilities suite (requested)",
        "command": "just test -p codex-core -E 'test(remote_catalog_replacement_changes_waiting_snapshot)'",
        "expected_failure": "Requested, NOT EXECUTED. Mock a remote catalog entry for the same bundled slug that removes clock, plus the reverse control; capture the waiting snapshot in real sampling. A mutant ignoring remote replacement must fail."
      },
      "reported_by": "TASK-261011-1zp0ru"
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "finding_ids": [],
      "attack": "Trace ToolName heap ownership to genuine native config bounds; inspect serialization, turn conversion and prompt construction.",
      "evidence": "extension-api/src/waiting_capabilities.rs:24-59 has four booleans and Option<ToolName>, no collections or serde; config/mod.rs:3148-3202 caps native V2 namespace to 64 ASCII characters. Native provenance closes the prior foreign extension namespace bound issue. StepContext::to_turn_context_item omits the snapshot and goal renders no fragments. Exact-tree hosted core reports waiting_snapshot_does_not_persist_to_history_or_rollout PASS; small lane reports snapshot_stays_small_and_bounded green. size_of checks headers only; the production config bound supplies the heap bound, not that test.",
      "reported_by": "TASK-261011-1zp0ru"
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "finding_ids": [],
      "attack": "Inspect public constructor changes, dependency direction, module placement, old plan signal and Bazel inclusion.",
      "evidence": "One extension-api snapshot type and one borrowed contributor field; derivation is a 275-line separate core module. Goal consumes the extension-api type through existing contributor registration; no core-to-goal dependency is introduced. Source globs include new Rust files; no build-time file inclusion or dependency changes. update_plan_enabled callsites remain as before: replacement is staged to the guidance leaf, as explicitly accepted in merged rev1 review; no behavior loss is claimed.",
      "reported_by": "TASK-261011-1zp0ru"
    }
  ],
  "free_hunt": [
    "[TASK-261011-1zp0ru] {\"budget\": \"Seven surface rows, then five adjacent concerns: normalization/resume discovery, native heap bounds, contributor installation/transience, external/API/build wiring, and hosted evidence identity. No builds or new runtime executions.\", \"result\": \"One new static robustness finding A2-F1; remote replacement has an explicit requested attack. Prior defects have fixes plus named exact-tree mutant kills.\", \"coverage\": {\"surface_rows_swept\": 7, \"surface_rows_total\": 7, \"held\": 5, \"broken\": 1, \"not_attacked\": 1, \"attached_mutants_killed\": 12, \"attached_mutants_total\": 12, \"mutant_core_job_conclusions_checked\": 12, \"mutant_raw_logs_inspected\": 4, \"snapshot_core_tests_passed\": 5115, \"snapshot_core_tests_run\": 5115, \"snapshot_core_tests_skipped\": 11, \"new_runtime_attacks_executed_by_this_panel\": 0}, \"blind_spots\": [\"The new orphan-resume reproduction is requested, not executed. Its mechanism is established by exact source paths and the existing fixture shape.\", \"Remote replacement is not proven by directly setting ModelInfo.\", \"Hosted green lanes do not prove every structural surface or all operating systems; skipped tests stay skipped.\"], \"stop_condition\": \"All seven rows have exactly one result and the bounded free hunt is closed; no first-finding exit.\"}",
    "[TASK-261011-2yj58v] {\"area\": \"exec_command namespace shadow\", \"outcome\": \"dismissed\", \"detail\": \"specs.find(spec.name() == exec_command) could theoretically match a same-named namespace before the function and return false. Requires a namespace literally named exec_command surviving finalization alongside the function; no realistic trigger. Same conclusion as rev1 panel B.\"}",
    "[TASK-261011-2yj58v] {\"area\": \"ToolSearchOutput status unchecked in history scan\", \"outcome\": \"dismissed\", \"detail\": \"discovered_waiting_tools_from_history scans every ToolSearchOutput item without checking status. Handler error paths return Err or empty tools (tool_search.rs: empty query, zero limit, empty index), so only successful searches emit spec-carrying outputs; the deferred-registry re-check backstops any stray name.\"}",
    "[TASK-261011-2yj58v] {\"area\": \"stale discovery across plan changes\", \"outcome\": \"dismissed\", \"detail\": \"Old ToolSearchOutput items persist in history across model or config changes, but every discovered name is re-checked against the current finalized registry exposure, so post-discovery exclusions, collisions, and removals still yield false. Covered by discovered_names_not_in_registry_still_yield_none.\"}",
    "[TASK-261011-2yj58v] {\"area\": \"dual V1 plus V2 native registration\", \"outcome\": \"dismissed\", \"detail\": \"native_wait_tool uses registry .find(); multi_agent_version is a single enum (Disabled/V1/V2) and collab registration branches on it, so at most one native wait runtime exists per plan and selection is deterministic.\"}",
    "[TASK-261011-2yj58v] {\"area\": \"history lock scope during capture\", \"outcome\": \"held\", \"detail\": \"The state lock is held only for the synchronous raw_items scan inside a block scope and released before derive_waiting_capabilities runs; no await under the held guard and no deadlock shape.\"}",
    "[TASK-261011-2yj58v] {\"area\": \"prompt-byte neutrality of the new contributor\", \"outcome\": \"held\", \"detail\": \"Both session paths push only per returned fragment with no per-contributor markers, and goal waiting_capability_fragments returns empty for every snapshot value. Registration cannot change prompt bytes; confirmed by the steering renderer test and the non-persistence test.\"}",
    "[TASK-261011-2yj58v] {\"area\": \"speculative step contexts\", \"outcome\": \"held\", \"detail\": \"capture_speculative_step_context funnels through capture_step_context_inner, so speculative steps derive the same way and share the same StepContext ownership; no second derivation path exists.\"}",
    "[TASK-261011-1sgzye] {\"budget\": \"Bounded to all 10 rework paths and five adjacent concerns: native runtime wrappers/provenance, normalized history/discovery, namespace collisions/exclusions, catalog resolution, and snapshot bounds/persistence/API wiring. No build execution or candidate mutation.\", \"result\": \"One confirmed regression-test proof defect D-F1. No additional production defect established. Normal valid search parsing, native V2 wrapper forwarding, registry exclusions, and default-namespace normalization are consistent under static review.\", \"coverage\": {\"surface_rows_swept\": 7, \"surface_rows_total\": 7, \"held\": 5, \"broken\": 1, \"not_attacked\": 1, \"supplied_mutants_killed\": 12, \"supplied_mutants_total\": 12, \"raw_mutant_logs_inspected\": 4, \"mutant_core_job_conclusions_checked\": 12, \"snapshot_core_tests_passed\": 5115, \"snapshot_core_tests_run\": 5115, \"snapshot_core_tests_skipped\": 11, \"integrated_waiting_discovery_transitions_observed\": 0, \"integrated_waiting_discovery_transitions_required\": 1, \"integrated_remote_catalog_snapshot_attacks_observed\": 0, \"integrated_remote_catalog_snapshot_attacks_requested\": 1, \"local_rust_tests_executed\": 0}, \"blind_spots\": [\"Requested diagnostic extension and integrated discovery regression were not executed; fixture/normalizer contradiction is established statically and corroborated by the existing hosted normalization test.\", \"Remote catalog replacement was not driven through sampling with snapshot observation.\", \"Four raw mutant logs were fetched, rather than all twelve. Other kills rely on attached named-test evidence plus independently read job conclusions.\", \"Hosted execution is Linux evidence, not new macOS/Windows evidence. Structural holds do not claim an independent mutant for pointer identity, persistence, or dependency placement.\"], \"stop_condition\": \"Both previous production findings checked; same-class discovery paths and all seven rows swept once; bounded adjacent hunt closed.\"}"
  ]
}
```

Recording review — 2026-10-11, RUN-261011-827c13

Verdict: changes_requested for CR-TASK-260929-2is91w-2 revision 2, candidate ef4eb6ff644eee2a950b493b675fb86f7b3301c2.

Read all three panel outcomes (TASK-261011-1zp0ru, TASK-261011-2yj58v, TASK-261011-1sgzye) and this merged verdict. Programmatic comparison confirms 2/2 findings retained with unchanged invariant, mechanism, sources, reproduction fields, severity and repeat-of; every panel note and free-hunt entry retained; 7/7 ordered surface rows present exactly once with the worst panel result. Both A2-F1 and D-F1 belong to final-router derivation: one records the raw-history capability mismatch and the other records the invalid positive fixture/missing integrated proof. No new findings and no independent code re-review.

Merged sweep: flag derivation held; final-router derivation broken; subscriptions are not capabilities held; one snapshot, both paths held; configuration coverage not-attacked; bounded and transient held; API surface and placement held. Coverage: 5 held / 1 broken / 1 not-attacked = 7/7 rows. Panel B's accept does not override the two changes_requested panels.

Preserve the panels' rework requests: orphan client search outputs must not enable capabilities; legitimate paired client and standalone server outputs remain supported; replace fabricated discovery evidence with real tool_search-to-next-request coverage and a named narrowing mutant. Remote-catalog-to-snapshot coverage remains unknown; installed-goal identity is statically wired rather than independently exercised end-to-end. Existing exact-candidate hosted results and 12/12 mutant kills are accepted from panel evidence, not rerun here.

Change-size assessment: +1990/-6 across 20 files, including a 1359-line test module and a 275-line derivation module. The panels' split/consolidation concern remains recorded for producer rework; this recording does not grant a size exception or add a blocking finding. Retain the required public-entry regression when consolidating repeated setup. The staged update_plan_enabled replacement and public Rust constructor compatibility notes also remain explicit.

Commands: initial reviewing mutation exit 0; all four resource downloads exit 0; task-scoped board queries and scoped mutation schemas exit 0; in-memory merge checks passed. The combined skill/reference read exited 1 because its reviewer-role reference was absent; the explicit assigned reviewer contract supplied the route. No cargo, just, formatting, builds, tests, commits, code edits, temporary directories or local repro artifacts were created.

Goal check: task-board spawn goal reported this run is not goal-bound (exit 0). Safe-checkpoint directives reported none (exit 0).

Logbook — 2026-10-11: verified the complete three-panel union and conservative seven-row merge. Record changes_requested, attach this updated task-scoped verdict before routing through reject_cr to to-dev. Ordinary implementation/proof rework; no external blocker or human-only decision.

Recording provenance recovery: reject_cr using the pre-existing canonical name exited 1 with change_request_evidence_missing: this run's manifest had no initial digest for that resource. This new task-scoped copy preserves the complete verified canonical verdict and its recording logbook, and provides newly created evidence attributable to RUN-261011-827c13. No finding or surface result changed.
