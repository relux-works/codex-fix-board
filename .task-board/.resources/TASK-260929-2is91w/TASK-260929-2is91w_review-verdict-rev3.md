# Merged review verdict — TASK-260929-2is91w CR revision 3 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261011-2k0u5i_panel-verdict.md` (changes_requested), `TASK-261011-1fl8hg_panel-verdict.md` (accept), `TASK-261011-1grcu4_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A3-F1",
      "row": "final-router derivation",
      "invariant": "AC2: a registered deferred waiting tool becomes callable after its definition is delivered by supported tool-search output; discovery and actual prompt normalization must agree.",
      "mechanism": "discovered_waiting_tools_from_history first matches call_id, with None => false. This rejects execution=server/call_id=null before the server exemption is evaluated. The protocol explicitly supports server/null search items (tool_search_server_items_allow_null_call_id). OutputItemDone -> handle_output_item_done -> record_completed_response_item_with_finalized_facts records non-dispatched server search outputs in history. HistoryManager::for_prompt retains them: remove_orphan_outputs only rejects Some(call_id) client outputs without a matching call. A server/null output loading the registered deferred multi_agent_v1.wait_agent therefore remains model-visible but capture_step_context_inner computes native_wait=None. Existing server_tool_search_output_counts_without_call covers only Some(\"server-search-1\"). This is under-advertising of a supported discovered tool, not a failure of the paired-client orphan fix.",
      "sources": [
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities.rs:120-130",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/protocol/src/models.rs:4226-4274",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/stream_events_utils.rs:361-398",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/stream_events_utils.rs:82-110",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/context_manager/normalize.rs:201-208",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/context_manager/history.rs:581-603",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/session/mod.rs:3971-3982",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities_tests.rs:433-447"
      ],
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/tools/waiting_capabilities_tests.rs::server_tool_search_output_counts_without_call (requested extension, not modified)",
          "command": "just test -p codex-core -E 'test(server_tool_search_output_counts_without_call)'",
          "expected_failure": "NOT EXECUTED. Extend existing test to loop over [Some(\"server-search-1\"), None] with execution=\"server\" and wait_agent_loadable(\"multi_agent_v1\"), expecting the same singleton discovered set. The None case deterministically returns an empty set in the candidate. Keep orphan/mismatched client refusals. After fixing, add a narrowing mutant requiring a non-null ID for server outputs; the null case must kill it.",
          "pinned_blobs": [
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities.rs (discovered_waiting_tools_from_history)",
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities_tests.rs (server_tool_search_output_counts_without_call)",
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/context_manager/normalize.rs (remove_orphan_outputs tool_search arm)"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/search_tool.rs::server_null_id_discovery_updates_waiting_capabilities (requested new integration test, not added)",
          "command": "just test -p codex-core -E 'test(server_null_id_discovery_updates_waiting_capabilities)'",
          "expected_failure": "NOT EXECUTED. Drive the Responses stream with a completed server ToolSearchOutput with call_id=null loading the deferred native V1 wait tool. Observe its definition in the next sampling input and native_wait=Some(actual tool name) via a contributor on a subsequent turn with a context change (as the existing discovery test does). Candidate retains the definition but reports native_wait=None. Include Some(server ID), paired-client, and orphan-client controls; do not inject only a fabricated unpaired client output.",
          "pinned_blobs": [
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities.rs (discovered_waiting_tools_from_history)",
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities_tests.rs (server_tool_search_output_counts_without_call)",
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/context_manager/normalize.rs (remove_orphan_outputs tool_search arm)"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "requested_change": "Apply the server exemption independently of call_id; continue requiring a prior matching call ID for client outputs. Carry a named null-server regression and narrowing mutant in this leaf. Same discovery-evidence class as rev2 A2-F1, but opposite discrepancy and a new mechanism, hence repeat-of none.",
      "reported_by": [
        "TASK-261011-2k0u5i"
      ]
    },
    {
      "id": "D3-F1",
      "row": "final-router derivation",
      "invariant": "AC2 requires deferred tools to become capabilities when retained discovery makes them callable; the rev2 rework request explicitly preserves server execution as the normalizer treats it.",
      "mechanism": "The new paired match in discovered_waiting_tools_from_history returns false for every None call_id, even when execution is server. This is a supported input, not malformed/orphan client evidence: protocol::models::tests::tool_search_server_items_allow_null_call_id explicitly deserializes a completed server ToolSearchOutput with null call_id. remove_orphan_outputs only removes Some(call_id) client outputs without a call and retains null-ID server outputs. Stream OutputItemDone reaches handle_output_item_done; build_tool_call returns None for this output, and the Ok(None) branch records it. History retains ToolSearchOutput and for_prompt passes it to the next request. With a finalized deferred native wait entry and a server output carrying its actual loadable spec, capture_step_context_inner now produces an empty discovered set and native_wait=None although the retained definition is sent to the model. Revision 2 scanned the tools without this call_id restriction, so this false negative is introduced by the rework. The positive server test uses Some(server-search-1) and misses the valid null shape. Current goal rendering emits no fragments, so this establishes an incorrect new snapshot rather than a demonstrated current user-facing guidance failure.",
      "sources": [
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities.rs:116-127,203-217,256-259",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities_tests.rs:429-445",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/protocol/src/models.rs:1170-1182,4225-4273",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/context_manager/normalize.rs:160-223",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/context_manager/history.rs:933-953,997-1010",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/stream_events_utils.rs:315-394",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/session/mod.rs:3971-3982",
        "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/session/turn.rs:462-534",
        "TASK-260929-2is91w_rework-brief-review2.md: Required 1 and 3"
      ],
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/tools/waiting_capabilities_tests.rs (requested extension of server_tool_search_output_counts_without_call)",
          "command": "just test -p codex-core -E 'test(=tools::waiting_capabilities::tests::server_tool_search_output_counts_without_call)'",
          "expected_failure": "Requested diagnostic, NOT EXECUTED: replace Some(server-search-1) in the existing server positive test with /*call_id*/ None while preserving execution=server, completed status and the multi_agent_v1.wait_agent loadable definition. Keep the existing expected discovered set. Candidate returns an empty set and fails equality. Retain Some-ID server, paired-client and orphan-client controls. This command against the existing unmodified test is green in hosted evidence; only the requested diagnostic is predicted red.",
          "pinned_blobs": [
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities.rs (discovered_waiting_tools_from_history)",
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities_tests.rs (server_tool_search_output_counts_without_call)",
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/context_manager/normalize.rs (remove_orphan_outputs tool_search arm)"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/search_tool.rs (requested server_search_without_call_id_updates_waiting_capabilities)",
          "command": "just test -p codex-core -E 'test(=suite::search_tool::server_search_without_call_id_updates_waiting_capabilities)'",
          "expected_failure": "Requested public-entry regression, NOT EXECUTED: reuse configure_search_capable_model and the recorder. Emit a completed server tool_search_output with call_id:null and a genuine deferred multi_agent_v1.wait_agent loadable spec through response.output_item.done, finish the response, then submit the second turn with changed approval policy as the current integration test does. Assert the next request retains that definition and the contributor snapshot has Some(actual native name). Candidate retains the output but yields None. Add a narrowing mutant rejecting only null-ID server outputs, killed by this test.",
          "pinned_blobs": [
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities.rs (discovered_waiting_tools_from_history)",
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/tools/waiting_capabilities_tests.rs (server_tool_search_output_counts_without_call)",
            "f8ae85582d54c47b237476e8d88742f942961f3f:codex-rs/core/src/context_manager/normalize.rs (remove_orphan_outputs tool_search arm)"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261011-1grcu4"
      ]
    }
  ],
  "notes": [
    "[TASK-261011-2k0u5i] Independent non-recording panel A for CR-TASK-260929-2is91w-3 revision 3. No mutations, outcomes, accept/reject/status/handoff writes were made on TASK-260929-2is91w.",
    "[TASK-261011-2k0u5i] Execution attribution: accepted TASK-260929-2is91w_hosted-precheck-10.md (run 38142174620; exact candidate tree; lint/small/core/app-server success; 13/13 named mutants killed, 0 survivors). CR rev3-validation.log reports mini-hosted-gate.sh exit 0, coverage_unit=exact_command_shard required=1 green=1 failed=0 missing=0 test_case_coverage=unknown. None of these Rust suites or mutants was rerun by this panel; raw hosted logs and per-test skip counts were not independently fetched.",
    "[TASK-261011-2k0u5i] Rev2 A2-F1 paired-client orphan discrepancy and D-F1 fabricated discovery fixture are addressed by the pairing gate, negative tests, for_prompt survival assertion, and real tool_search integration test. The null-server finding is new, not a repeated orphan-admission mechanism. Require same-class regression and narrowing mutant on rework without creating another research/harness task.",
    "[TASK-261011-2k0u5i] Size review: 21 changed files, +2254/-6; new test module 1461 lines. This exceeds the 800-line guidance and complex-change 500-line target. Smallest coherent first stage could be the snapshot/wiring plus direct flag/refusal and receipt integration coverage; discovered deferred-tool support, history parser, and real-search integration belong together in a following stage. Otherwise consolidate repeated fixtures before review. This panel records the size concern as a note, not an additional functional blocker or a granted exception.",
    "[TASK-261011-2k0u5i] Static source checks corroborate predicates and production routes, not executed Rust behavior. Newly requested reproductions and the remote-catalog attack remain unexecuted. Linux-hosted conclusions do not independently establish all-platform coverage.",
    "[TASK-261011-2k0u5i] Prompt emission after an in-turn capability change belongs to the separately scoped guidance/context-change work. This leaf computes each StepContext snapshot but contributors rerun only on full context or TurnContextItem changes. The real-search test correctly observes the post-discovery snapshot on a second turn with changed approval policy.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] Replay is exact: write-tree on base e0eff057 plus the rev3 patch prints f8ae85582d54c47b237476e8d88742f942961f3f. Candidate sources were read from that pinned tree with git show / git archive.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] Hosted identity independently verified: run 38142174620 plan job records snapshot commit d772e5c0357c2ae4e00c2e207c16b4a122507f79, and the commit API reports its tree as f8ae85582d54c47b237476e8d88742f942961f3f, the reviewed candidate. The workflow head 9f8fdf9a is the dispatch head, not the tested tree. Overall run conclusion failure is expected: 13 mutant core jobs fail red while plan, lint, snapshot small, snapshot core and snapshot app-server are success.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] All 13 mutant core jobs were mapped by their ci commit messages (mutant-1 discovery_ignores_call_pairing through mutant-13 stdin_counts_nested) and all 13 conclusions are failure, i.e. expected-red kills. Raw logs independently inspected for mutant-1 (exactly orphan_client_tool_search_output_does_not_count plus mismatched_call_id_tool_search_output_does_not_count fail, 3 attempts each), mutant-9 native_wait_ignores_discovered (exactly the 3 discovery tests fail, including the new integration test), mutant-7 native_mail_wait_ignores_policy (ack suite test fails) and mutant-13 stdin (code_mode plus nested_stdin fail). Remaining kills are accepted from the attached precheck-10 table plus independently checked job conclusions.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] Snapshot core log shows 5119 tests, exactly 5115 plus the 4 new tests (3 orphan unit tests plus the real-search integration test). The new integration test discovered_native_wait_updates_waiting_capabilities PASSES on snapshot (4669/5119) and FAILS under native_wait_ignores_discovered, proving it observes the discovery transition rather than direct visibility. Precheck-9 red to precheck-10 green on the integration premise is further negative evidence that the test executes its assertions.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] Rev2 findings A2-F1/D-F1 are closed by this revision: the pairing rule mirrors remove_orphan_outputs in the safe direction, the capture test records a call plus output pair and pins for_prompt survival, the real-search integration test asserts the paired output inside the outbound request plus a None to Some transition, and the 13th mutant is exactly the pairing narrowing, killed by exactly the 2 orphan tests on this tree.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] Results-doc prose nit (no code impact): the results claim +276 insertions versus the precheck-8 tree, but git diff-tree --numstat ef4eb6ff..f8ae8558 measures +290/-26 (35/7 plus 121/19 plus 134/0). The file set matches and tree identity is verified independently, so this is a reporting error only.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] Change size is 2254 insertions / 6 deletions across 21 files, exceeding the 800-line guidance; the 1461-line test module is the AC-mandated named-test matrix. No split was performed in this exact-tree revision. Recording reviewer should assess the size exception, as in rev2; no blocking finding is added here.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] TurnContextContributionInput still gains a required public Rust field, source-breaking for out-of-tree struct-literal constructors. All in-repo constructors are updated and hosted lint on the exact tree is green. No app-server wire, CLI, config-schema, lockfile, rollout, or prompt-text change was found in the 21-file diff. Noted, non-blocking, same as rev2.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] All board reads and the single outcome attach in this run target TASK-261011-1fl8hg. Nothing was accepted, rejected, status-changed, handed off, noted, or attached on TASK-260929-2is91w. No build or test command ran locally.",
    "[TASK-261011-1grcu4] A2-F1 addressed for orphan/mismatched Some-ID client outputs: the scanner requires an earlier matching call; hosted pairing mutant-1 core job 114480088943 fails the two refusal tests with exit 100. Original malformed-history normalization can still panic by existing design; this CR does not claim to repair unrelated corrupt-history handling.",
    "[TASK-261011-1grcu4] D-F1 addressed: capture fixture now records a real call/output pair and checks for_prompt survival. New suite::search_tool::discovered_native_wait_updates_waiting_capabilities drives real tool_search and observes None before and Some after discovery. Snapshot core reports it PASS; native_wait_ignores_discovered mutant-9 core job 114480089960 fails it with exit 100. Contributor observation is on the second turn with changed approval policy, not independently on request 2. The rework brief permits this bounded search coverage without a wait-execution control; no wait invocation or resume/fork negative integration was added.",
    "[TASK-261011-1grcu4] Prior A-F1 native provenance fix still holds: default runtime marker is false; only native V1/V2 wait handlers and the delegating V2 wrapper report true. Registry selection supplies actual configured identity. No bare-name fallback was reintroduced.",
    "[TASK-261011-1grcu4] Size remains outside guidance: 2260 changed lines (+2254/-6) over 21 files, including 1461 test lines and a separate 303-line derivation module. Rev2-to-rev3 delta is confined to three files. Retain the earlier split/consolidation concern; this panel grants no size exception and adds no style-only blocking finding.",
    "[TASK-261011-1grcu4] TurnContextContributionInput gains a required public Rust reference field, breaking out-of-tree struct-literal constructors. In-repository construction sites are updated. No app-server wire, CLI, config schema, dependency lockfile or persisted rollout shape changed.",
    "[TASK-261011-1grcu4] update_plan_enabled replacement remains staged to the guidance leaf as prior review acknowledged; existing signal/rendering stays intact. Goal installs the contributor but emits zero fragments, so no new model-visible token payload, context rewrite or cache-changing prompt text is introduced.",
    "[TASK-261011-1grcu4] Installed-goal pointer identity is statically wired through the same contributor registry; its test invokes the renderer, while the two-path core test records one borrowed instance. Do not claim an independent installed-goal pointer attack.",
    "[TASK-261011-1grcu4] Numeric exits for successful hosted lane commands are unknown from the inspected logs; expected-red mutant command exits observed are 100. Local gates rerun here are replay and git diff --check only. Full runtime suite and mutant evidence is hosted Linux evidence; eleven snapshot skips remain skips, not cross-platform coverage."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "attack": "Drop individual host/opt-in/control/policy conjuncts; force V1-only or V2-only native identity and foreign wait decoys.",
      "evidence": "Exact-tree hosted precheck 10 reports kills for exec_notify_ignores_host/opt_in/stdin/receipt, native_mail_wait_ignores_host/policy, native_wait_v1_only/v2_only/bare_name_match, sleep_counts_nested_or_deferred, stdin_counts_nested. Derivation lines 46-83 matches the AC1 conjunctions. Native identity comes from the finalized registry and native runtime provenance. This hold is bounded by the discovery defect assigned to final-router derivation.",
      "finding_ids": [],
      "reported_by": "TASK-261011-2k0u5i"
    },
    {
      "row": "final-router derivation",
      "result": "broken",
      "attack": "Attack undiscovered/deferred/nested/excluded tools, foreign wait provenance, orphan/mismatched discovery, and supported server output with null call ID.",
      "evidence": "Hosted real-search discovered_native_wait_updates_waiting_capabilities kills native_wait_ignores_discovered; orphan and mismatched-ID tests kill discovery_ignores_call_pairing. Static trace of the protocol-supported server/null case establishes A3-F1; hosted mutants do not include this case. is_callable checks deferred exposure in the current registry; native_wait_tool checks runtime provenance.",
      "finding_ids": [
        "A3-F1"
      ],
      "reported_by": "TASK-261011-2k0u5i"
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "attack": "Arm a receipt through real exec_command, observe idle wake and subsequent sampling; inject pending/acknowledged providers without host controls.",
      "evidence": "Hosted precheck 10 covers core suite acknowledged_subscription_does_not_flip_waiting_capabilities, which launches notify_on_exit=true, requires an armed receipt, waits for completion wake, and compares all captured snapshots. pending_and_acknowledged_work_does_not_flip_flags tests receipt-only refusal. Derivation reads AsyncNotificationSupport and GoalBackgroundWaitAdmission only, never receipt state.",
      "finding_ids": [],
      "reported_by": "TASK-261011-2k0u5i"
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "attack": "Look for recomputation, copies, independent initial/diff derivation, and disconnected goal registration.",
      "evidence": "capture_step_context_inner owns one value on StepContext; both contributor calls borrow &step_context.waiting_capabilities (session/mod.rs:4315 and 4413). Hosted same_snapshot_instance_reaches_both_context_paths drives capture and both builders, checking pointer identity and equality. GoalExtension registers as a prompt contributor and forwards the same borrowed reference to waiting_capability_fragments. Goal renderer emits zero fragments. Goal installation is statically traced; the pointer test uses a recording contributor, not GoalExtension itself.",
      "finding_ids": [],
      "reported_by": "TASK-261011-2k0u5i"
    },
    {
      "row": "configuration coverage",
      "result": "not-attacked",
      "attack": "Compare model catalog entry-point replacement with the snapshot tests; inspect hard/reminder off, headless, code-mode and receipt exclusions.",
      "evidence": "Hosted snapshot_follows_sleep_switches, headless_exec_host_keeps_exec_but_disables_notification_flags, code_mode_only_hides_nested_waits_but_keeps_direct_sleep, excluded_receipt_tool_disables_exec_notify and excluded_exec_command_disables_exec_notify cover four required configuration families. snapshot_follows_catalog_clock_support directly edits resolved ModelInfo.experimental_supported_tools; it does not fetch/replace a remote entry through ModelsManager. ModelsManager replacement is visible at manager.rs:685-700, but no attached public-entry snapshot attack proves it.",
      "finding_ids": [],
      "reason": "Remote-catalog replacement through its actual entry point remains unknown; this is a fixture coverage bound, not the prohibition on local builds.",
      "requested_attack": {
        "test_file": "codex-rs/core/tests/suite/search_tool.rs or a dedicated waiting_capabilities suite (requested)",
        "command": "just test -p codex-core -E 'test(remote_catalog_replacement_changes_waiting_snapshot)'",
        "expected_failure": "NOT EXECUTED. Mock remote entries for the same bundled model slug removing/adding clock support, sample through the real session, and record the snapshot; require a mutant ignoring the remote replacement to fail. Other configuration legs have attached execution evidence."
      },
      "reported_by": "TASK-261011-2k0u5i"
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "attack": "Trace native ToolName heap bounds rather than trusting size_of; inspect persistence, serialization and prompt-history rewrites.",
      "evidence": "WaitingCapabilities has four booleans plus Option<ToolName>, no collections/serde. The native name is wait_agent; V1 namespace is fixed, V2 config validation caps namespace at 64 ASCII characters (core/src/config/mod.rs:3148-3202). Foreign names cannot enter because of runtime provenance. The public type can be manually constructed with longer strings, so the bound applies to core-derived snapshots. Hosted waiting_snapshot_does_not_persist_to_history_or_rollout compares both context outputs and the persisted turn item; goal emits no text. snapshot_stays_small_and_bounded measures headers only; the config validation supplies the native heap bound.",
      "finding_ids": [],
      "reported_by": "TASK-261011-2k0u5i"
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "attack": "Trace contributor construction, plan-enabled behavior, dependency direction, module size and Bazel source inclusion.",
      "evidence": "One exported extension-api type plus one borrowed input field; all in-tree constructors updated. Goal consumes that API via an existing contributor contract without introducing core->goal dependencies. Core derivation is a separate 303-line module. No dependency/config/schema/build-time file reads changed. Rust source globs cover the new files. update_plan_enabled remains unchanged: merged rev1/rev2 reviews explicitly accept staging its replacement to the guidance leaf, preserving existing prompt behavior. Adding a public Rust struct field is a source compatibility change for external extension implementers, not a new app-server/CLI/config/rollout wire change; hosted workspace callers compile.",
      "finding_ids": [],
      "reported_by": "TASK-261011-2k0u5i"
    }
  ],
  "free_hunt": [
    "[TASK-261011-2k0u5i] {\"budget\": \"After all seven rows: five adjacent concerns (server/null discovery and normalization, stale discovery after exclusions, native namespace heap bounds, prompt emission/goal installation, and API/Bazel/change-size wiring). No builds, product changes or delegation.\", \"result\": \"One static robustness defect A3-F1; no second independent production defect established.\", \"coverage\": {\"surface_rows_swept\": 7, \"surface_rows_total\": 7, \"held\": 5, \"broken\": 1, \"not_attacked\": 1, \"hosted_named_mutants_killed\": 13, \"hosted_named_mutants_total\": 13, \"new_rust_runtime_attacks_executed_by_panel\": 0, \"required_configuration_families_with_attached_router_attacks\": 4, \"required_configuration_families_total\": 5}, \"checks\": [\"Raw server/null output reaches recording and survives prompt normalization, but is discarded by discovery: A3-F1.\", \"Stale discovered names still require current deferred exposure; excluded/missing entries cannot create a capability. No new bypass found.\", \"Native provenance plus validated config bounds the production snapshot heap; size_of alone is insufficient.\", \"Both context builders share one instance; speculative capture delegates to capture_step_context_inner. Goal empty-fragment forwarding does not change prompt bytes.\", \"No new dependencies, schemas, wire payload changes or compile-time assets. Public Rust input-field compatibility and excessive diff size are recorded notes.\"], \"blind_spots\": [\"Null-server repro is source-established, requested but not executed.\", \"Remote catalog fetch/replacement with snapshot observation has no attached entry-point test.\", \"Structural pointer/persistence/dependency properties have inspection/test evidence, not dedicated narrowing mutants.\", \"Hosted outcomes are attached evidence; no raw logs/per-test skip audit or new macOS/Windows execution.\"], \"stop_condition\": \"Seven rows each have exactly one result, prior findings assessed, five adjacent concerns swept; no first-finding exit.\"}",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] {area: pairing strictness deltas, outcome: dismissed} Call-must-be-earlier and None-never-counts both under-advertise only: a genuinely delivered tool could read false, but an undelivered tool can never read true. History is append-ordered (call then output) and resume/fork replays in order; no history rewrite exists in this leaf, so output-before-call has no realistic trigger. None call_id outputs carrying wait specs are degenerate (the server positive control uses Some). Safe direction, documented in code.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] {area: duplicate call ids across searches, outcome: dismissed} calls is a set and discovered is a set of names, so a repeated call id can only re-add an already counted name; pairing existence is monotone and order-stable. No double-count or cross-search leak shape.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] {area: non-client non-server execution values, outcome: dismissed} Candidate counts iff execution equals server or the call is paired; the normalizer removes iff execution differs from server and the call is missing. The two rules agree on every Some call_id row; they differ only on None, which is the documented safe-direction delta above.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] {area: integration second-turn premise, outcome: held} The changed approval policy reruns contributors for the post-discovery sample; first-equals-None plus last-equals-Some is robust to mid-turn reruns because recording is append-ordered. The ignores-discovered kill proves the Some flows through the discovery path, not direct visibility.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] {area: skip_if_no_network on the new integration test, outcome: dismissed} The test demonstrably ran: PASS in snapshot core and kills in the ignores-discovered mutant job. No skip occurred on the evidence path.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] {area: orphan diagnostic never ran red, outcome: noted} The for_prompt diagnostic was added together with the paired fix, so its tripwire property is established statically (normalizer code path plus the existing should_panic orphan test) rather than by a red run. The 13th mutant kill on the exact tree supplies the executed negative proof for the pairing rule itself.",
    "[TASK-261011-1fl8hg] [TASK-261011-1fl8hg] {coverage: 7/7 rows swept once (6 held, 1 not-attacked), 13/13 mutant patches apply --check clean, 13/13 mutant core jobs confirmed failure with 1:1 name mapping, 4 raw mutant logs plus snapshot core log inspected, 0 local builds or tests, 0 findings, verdict accept}",
    "[TASK-261011-1grcu4] {\"budget\": \"After both previous findings and all seven rows, bounded hunt across supported search item shapes and normalization, stream recording/resume retention, stale discovery/current registry, native provenance and namespace bounds, context emission and persistence, external API/build wiring, and hosted evidence identity.\", \"result\": \"One rework regression D3-F1. No other production defect established in this sweep. Output-before-call strictness and malformed spec parsing remain unexecuted shape limits; no separate finding inferred without a supported production trigger.\", \"coverage\": {\"surface_rows_swept\": 7, \"surface_rows_total\": 7, \"held\": 5, \"broken\": 1, \"not_attacked\": 1, \"previous_findings_addressed\": 2, \"previous_findings_total\": 2, \"attached_mutants_killed\": 13, \"attached_mutants_total\": 13, \"mutant_core_job_conclusions_checked\": 13, \"mutant_raw_logs_inspected\": 4, \"snapshot_core_tests_passed\": 5119, \"snapshot_core_tests_run\": 5119, \"snapshot_core_tests_skipped\": 11, \"integrated_client_search_snapshot_attacks_in_hosted_evidence\": 1, \"integrated_null_id_server_snapshot_attacks\": 0, \"integrated_remote_catalog_snapshot_attacks\": 0, \"new_local_rust_attacks_executed\": 0}, \"blind_spots\": [\"D3-F1 is supported by pinned protocol and production source paths, not a newly executed Rust reproduction. Both requested tests remain unrun.\", \"Remote replacement-to-snapshot observation and installed-goal pointer identity lack independent public-entry runtime attacks.\", \"Nine mutant raw logs were not inspected; their named kills rely on attached precheck 10 evidence plus checked job conclusions.\", \"Linux hosted success does not establish new macOS/Windows execution; skipped tests remain outside measured coverage.\", \"The client-search integration observes the contributor after a second-turn policy change; capability-only in-turn contributor re-emission belongs to the subsequent guidance work.\"], \"stop_condition\": \"Both prior findings checked, their class swept for supported sibling shapes, all seven rows assigned exactly one result, bounded adjacent hunt closed. Nothing recorded on the implementation task.\"}"
  ]
}
```


## Recording reviewer confirmation — RUN-261011-288799, 2026-10-11

Verdict: **changes_requested**, CR-TASK-260929-2is91w-3 revision 3, candidate tree f8ae85582d54c47b237476e8d88742f942961f3f.

Compared this merged verdict with all three attached panel outcomes: TASK-261011-2k0u5i_panel-verdict.md, TASK-261011-1fl8hg_panel-verdict.md and TASK-261011-1grcu4_panel-verdict.md. The structured comparison found zero omissions: 2/2 finding records retain every original field and reproduction; 23/23 notes and all 9 free-hunt entries are retained. All three panels enumerate 7/7 rows in the required order, and the merge assigns each row exactly one result equal to the worst panel result: 5 held, 1 broken, 1 not-attacked.

A3-F1 and D3-F1 describe the same null-ID server discovery mechanism; both original IDs, their respective robustness/regression severities, sources and proposed reproductions are preserved. The broken row is final-router derivation. Configuration coverage remains explicitly not-attacked for the remote-catalog entry-point leg. Panel B's accepting position and its strictness dismissal remain in the union; they do not override the other panels' changes_requested verdicts. Prior rev2 findings are reported addressed by the panels.

No independent code review, source changes, local Rust gates, or new reproductions were performed by this recording run. Hosted precheck 10 and mutant results are accepted as attributed panel evidence, not rerun or independently fetched here. Requested null-server regressions remain unexecuted as stated in the original findings.

Logbook: complete three-panel union confirmed with no missing finding or surface row. The defect is ordinary implementation rework, with no external blocker or human-only decision. Record reject_cr for revision 3 using this artifact and route waiting-capabilities-snapshot to to-dev. The run goal query returned no active goal; directives query returned none. No temporary files or directories were created.
