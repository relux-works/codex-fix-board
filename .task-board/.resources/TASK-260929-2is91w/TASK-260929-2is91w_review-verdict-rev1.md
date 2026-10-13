# Merged review verdict — TASK-260929-2is91w CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261010-3jnv73_panel-verdict.md` (changes_requested), `TASK-261010-3syszw_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A-F1",
      "row": "flag derivation",
      "invariant": "AC1: native_wait denotes a callable V1 or V2 native agent wait tool and carries that native tool's actual identity; an unrelated callable tool must not satisfy this capability.",
      "mechanism": "find_direct_wait_agent scans every visible function/custom/namespace child for the bare name wait_agent, without checking the selected native backend, configured native identity, or executable runtime provenance. With native agents disabled, a valid, non-deferred dynamic foreign.wait_agent is registered and directly advertised, so the snapshot reports Some(foreign.wait_agent). Executing it reaches DynamicToolHandler/request_dynamic_tool, not either native agent wait handler. The same false capability occurs with V2 wait_agent_enabled=false and an unrelated namespaced wait_agent. Native same-name collision protection does not help: foreign is a different ToolName. Production path: thread/start dynamicTools validation -> TurnContext.dynamic_tools -> build_tool_router -> append_dynamic_tool_runtimes -> final router -> capture_step_context_inner -> derive_waiting_capabilities -> contributor input. Select the configured native identity/provenance from the captured plan before checking its exposure; retain arbitrary valid configured V2 namespaces.",
      "sources": [
        "codex-rs/core/src/tools/waiting_capabilities.rs:45,91-106",
        "codex-rs/core/src/tools/spec_plan.rs:187,569-603,1321-1324,1389-1398,1448-1477",
        "codex-rs/core/src/tools/registry.rs:379-420",
        "codex-rs/core/src/tools/handlers/dynamic.rs:50-82,139-147",
        "codex-rs/app-server/src/request_processors/thread_processor.rs:298-441,1453"
      ],
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/waiting_capabilities.rs (requested new suite; not added in this read-only panel)",
          "command": "just test -p codex-core -E 'test(=suite::waiting_capabilities::dynamic_wait_agent_does_not_claim_native_wait)'",
          "expected_failure": "Requested, NOT EXECUTED. Start a real TestCodex with multi_agent_version Disabled and a recording context contributor; supply dynamicTools=[{type:namespace,name:foreign,description:foreign tools,tools:[{type:function,name:wait_agent,description:external callback,inputSchema:{type:object,properties:{}},deferLoading:false}]}]. Submit a user turn and observe native_wait. The required assertion is None; the candidate name-only selector returns Some(ToolName::namespaced(foreign,wait_agent)). Add the V2 wait_agent_enabled=false variant. Positive control: a real configured V2 agents.wait_agent reports agents.wait_agent. Use build_with_auto_env and the existing recorder pattern from exec_notification.rs.",
          "execution": "requested_not_run",
          "pinned_blobs": [
            "fc18da8f7415a89029a6a0e7bc539e107749984a:codex-rs/core/tests/suite/waiting_capabilities.rs (requested new suite; not added in this read-only panel)"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-3jnv73"
      ]
    },
    {
      "id": "A-F2",
      "row": "final-router derivation",
      "invariant": "AC2: a deferred waiting tool is false before discovery and becomes present when discovery makes the tool callable for the sampling step.",
      "mechanism": "The snapshot sees only ToolRouter.model_visible_specs. build_model_visible_specs drops every non-direct exposure; V1 native tools are registered Deferred whenever tool search is enabled. ToolSearchHandler returns loadable tool definitions through ToolSearchOutput, and the existing public-entry search suite explicitly proves follow-up calls rely on tool_search_output history without injection into the request tools array. Search does not promote registry exposure. Subsequent step capture rebuilds the same deferred plan, and derivation has no history/discovered-tool input, so a successfully discovered multi_agent_v1.wait_agent remains native_wait=None. This is reachable in the normal V1/search-capable model configuration. The newly added deferred_sleep_does_not_count_until_discovered test exercises only the pre-discovery leg: it creates an undiscovered deferred registry and asserts none; it never searches or checks a subsequent step. Account for the discovered callable surface while preserving exclusion/collision and undiscovered-tool refusals.",
      "sources": [
        "codex-rs/core/src/tools/waiting_capabilities.rs:35-45,91-108",
        "codex-rs/core/src/tools/spec_plan.rs:569-581,1421-1442",
        "codex-rs/core/src/tools/handlers/tool_search.rs:195-240",
        "codex-rs/core/src/tools/context.rs:218-254",
        "codex-rs/core/src/session/mod.rs:3944-3992",
        "codex-rs/core/tests/suite/search_tool.rs:554-831,836-925",
        "codex-rs/core/src/tools/waiting_capabilities_tests.rs:203-216"
      ],
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/search_tool.rs (requested additional integration test)",
          "command": "just test -p codex-core -E 'test(=suite::search_tool::discovered_native_wait_updates_waiting_capabilities)'",
          "expected_failure": "Requested, NOT EXECUTED. Extend the existing deferred V1 public-entry search fixture with a recording context contributor. First sampling step must report native_wait=None. Script tool_search for the native wait_agent and assert the next request history includes multi_agent_v1.wait_agent in a completed tool_search_output. Assert that the post-discovery snapshot carries Some(multi_agent_v1.wait_agent), and route a subsequent native wait call as a control. The candidate still reports None because its advertised specs and deferred exposure never change. Add a narrowing mutant that deliberately ignores discovered tools; this new test must kill it.",
          "execution": "requested_not_run",
          "pinned_blobs": [
            "fc18da8f7415a89029a6a0e7bc539e107749984a:codex-rs/core/tests/suite/search_tool.rs (requested additional integration test)"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-3jnv73"
      ]
    }
  ],
  "notes": [
    "[TASK-261010-3jnv73] Evidence identity: replay is exact, but hosted precheck 4 ran snapshot commit d124f818544fdf41b5e5fb2c29e4bcbd27571bca / worktree tree 09975fe220479764649c9eb740f6d71f209d457e, not the reviewed fc18da8f7415a89029a6a0e7bc539e107749984a. Direct tree comparison finds eight arg0/cli/exec changes and zero core/ext changes. The attached mini-hosted-gate log passes an equivalence/replay-on-HEAD check; that is not execution on the rebased full candidate. No exact-candidate runtime attacks are claimed by this panel. Re-run the named integration attacks and mutants on the reworked frozen tree; do not mistake file equality for unchanged full source identity.",
    "[TASK-261010-3jnv73] Hosted evidence independently checked: GitHub run 38040774172 is overall failure because all 10 mutant core jobs fail. Snapshot lint/small/core/app-server jobs succeed. Fetched snapshot core log reports 5106/5106 passed, 11 skipped; fetched mutant-2 core log reports 318/321 passed, 3 failed, shell exit 100. The failures are the expected kills (exec opt-in narrowing), not a green mutant gate. Other nine named kills are accepted from the attached precheck report and independently checked failing job conclusions; their raw logs were not fetched.",
    "[TASK-261010-3jnv73] AC7 attached evidence reports 10/10 mutants killed on the earlier snapshot. Those mutants do not cover A-F1 external provenance or A-F2 the false-before/true-after discovery transition. Killer locations and public-entry reach must be distinguished: most one-conjunct kills are synthetic-router or router-builder tests, not new end-to-end user-turn attacks.",
    "[TASK-261010-3jnv73] Scope staging: runtime.rs/steering.rs update_plan_enabled pass-through remains. No behavior loss is introduced, but the literal scope replacement is deferred to TASK-260929-1w5ivu by producer context. The recording reviewer/orchestrator should make this staging explicit in the merged result.",
    "[TASK-261010-3jnv73] Change size: +1448/-4 across 15 paths exceeds 800-line guidance; ~1012 lines are the new test module, not entirely a mechanical generated delta. Consider consolidating the repeated snapshot matrix or explicitly approving the size exception; do not strip the integration attacks needed for the two findings. No independent blocking style finding added.",
    "[TASK-261010-3jnv73] No fragments or new prompt text are emitted, so no new model-context item or >1k-token fragment is injected by this revision. Adding a field to TurnContextContributionInput is source-breaking for Rust struct-literal consumers; all in-repository constructors are updated, and no app-server wire/CLI/config/session-resume surface changes were found in the bounded sweep.",
    "[TASK-261010-3syszw] update_plan_enabled replacement deferred: the scope asks to replace the pre-sampling pass-through, but the snapshot carries no plan-enabled field and replacement would change prompt text, which the same scope forbids. The producer documented the deferral to TASK-260929-1w5ivu with the vehicle and receiving end in place and zero behavior loss (call sites byte-identical). Treated as an accepted scope boundary, not a defect.",
    "[TASK-261010-3syszw] Hosted evidence transfer: precheck 4 (run 38040774172) executed on snapshot tree 09975fe220479764649c9eb740f6d71f209d457e (commit d124f818544fdf41b5e5fb2c29e4bcbd27571bca verified locally); the candidate differs by exactly 8 committed-trunk files under arg0/cli/exec with an empty core/ext delta, so all 15 task files are byte-identical to the green run. The only in-build-closure dependency delta is codex-arg0 (via core/tests/common and app-server), whose delta is additive-only (new silent_exit module plus re-exports); no existing API behavior changed. Residual risk negligible.",
    "[TASK-261010-3syszw] Change size +1448/-4 across 15 files exceeds the 800-line guidance; about 1012 lines are the AC-mandated named-test matrix plus refusal tests and mutant killers, with production logic around 200 lines. Mechanical-test overrun, accepted."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "broken",
      "finding_ids": [
        "A-F1"
      ],
      "reason": "Static counterexample: unrelated directly advertised dynamic wait_agent satisfies native_wait, including when native wait is disabled. Sleep/stdin direct identities and the four exec_notify/two native_mail_wait conjuncts otherwise match AC1. Existing V1/V2 positive tests never distinguish external tools with the same basename.",
      "attack": "Foreign namespace and disabled-backend substitution; conjunct review.",
      "evidence": "Candidate source citations in A-F1; earlier hosted conjunct mutants are supporting evidence only, not exact-candidate executions.",
      "reported_by": "TASK-261010-3jnv73"
    },
    {
      "row": "final-router derivation",
      "result": "broken",
      "finding_ids": [
        "A-F2"
      ],
      "reason": "Derivation occurs after finalization and correctly excludes nested-only and undiscovered tools, but discovery exposes deferred tools through response history without changing model_visible_specs. Snapshot therefore never observes the discovered callable tool.",
      "attack": "Follow the public tool_search -> ToolSearchOutput -> next-sampling path; check both sides of the discovery boundary.",
      "evidence": "A-F2; candidate search_tool.rs explicitly defends no follow-up tool injection. Existing deferred test has only a false-before assertion.",
      "reported_by": "TASK-261010-3jnv73"
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "finding_ids": [],
      "reason": "Held by static input/data-flow attack: derivation reads only final specs, AsyncNotificationSupport and GoalBackgroundWaitAdmission. PendingWorkProvider/receipts/ack state cannot affect its return. The suite test arms a real receipt and compares all observed snapshots; independently fetched older snapshot log records its PASS. This is a static hold, not a claim that this panel executed the test on the candidate.",
      "attack": "Replace armed/queued/leased work and receipt acknowledgements while keeping router/host/policy fixed.",
      "evidence": "waiting_capabilities.rs:35-58; waiting_capabilities_tests.rs pending_and_acknowledged_work_does_not_flip_flags; core/tests/suite/exec_notification.rs:736-835; hosted snapshot core log PASS for acknowledged_subscription_does_not_flip_waiting_capabilities.",
      "reported_by": "TASK-261010-3jnv73"
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "finding_ids": [],
      "reason": "Held by static reference-identity attack: capture derives once, StepContext owns the result, and both contribution constructors borrow &step_context.waiting_capabilities. The registered GoalExtension ContextContributor forwards that reference to the renderer. No per-path recomputation or cloned snapshot appears. The earlier hosted pointer test passed; the goal renderer test alone is not an installation-path proof.",
      "attack": "Trace allocation and each borrow through initial-context, diff-context, prompt-contributor registration and goal renderer.",
      "evidence": "core/src/session/mod.rs:3971-3992,4291-4310,4406; session/step_context.rs:41-44; ext/goal/src/extension.rs:616-629,767; ext/goal/src/steering.rs:67-73; waiting_capabilities_tests.rs:942-972.",
      "reported_by": "TASK-261010-3jnv73"
    },
    {
      "row": "configuration coverage",
      "result": "not-attacked",
      "finding_ids": [],
      "reason": "The final-router tests statically cover headless markers, sleep switches, code-mode and excluded receipts. The alleged remote-catalog test manually appends clock to an already resolved ModelInfo, bypassing ModelsManager remote catalog fetch/replacement. No attached exact-candidate public-entry remote-replacement attack was found. This gap concerns the exercised entry point and evidence identity, not the local build prohibition.",
      "attack": "Inspected actual catalog resolution versus snapshot_follows_catalog_clock_support fixture; named the missing public-entry attack.",
      "requested_attack": {
        "test_file": "codex-rs/core/tests/suite/waiting_capabilities.rs (requested)",
        "command": "just test -p codex-core -E 'test(=suite::waiting_capabilities::remote_catalog_replacement_changes_waiting_snapshot)'",
        "expected_failure": "Request a mocked remote catalog entry that removes clock from a bundled clock-capable slug, and the reverse control; capture snapshots through real sampling. A mutant forcing bundled entries or bypassing the remote replacement must fail. Run on the reviewed/reworked exact tree. Not executed in this panel."
      },
      "evidence": "waiting_capabilities_tests.rs:677-713; models-manager/src/manager.rs:456-473,577 onward; TASK-260929-2is91w_hosted-precheck-4.md identifies the earlier tree.",
      "reported_by": "TASK-261010-3jnv73"
    },
    {
      "row": "bounded and transient",
      "result": "broken",
      "finding_ids": [
        "A-F1"
      ],
      "reason": "Transience holds statically: no serialization/history/rollout path includes the snapshot and the goal renderer emits nothing. Hard boundedness is compromised by A-F1: any extension namespace String attached to a visible wait_agent is cloned into native_wait with no snapshot length check. size_of<=128 measures String headers, not heap bytes. Native V2 config and app-server dynamic namespace validators cap namespaces at 64, so those paths do not reproduce an oversized native name; extension executor registration has no equivalent bound. Restricting A-F1 to genuine native identities can inherit the existing native namespace limit instead of adding a duplicate name policy.",
      "attack": "Follow ToolName heap ownership, native config validation, app-server validation, and extension-executor registration; inspect persisted turn conversion.",
      "evidence": "ext/extension-api/src/waiting_capabilities.rs:26-41; protocol/src/tool_name.rs:12-16,36-40; waiting_capabilities.rs:106; core/src/config/mod.rs:3148-3202; spec_plan.rs:1499-1525; session/step_context.rs:51 onward; ext/extension-api/tests/waiting_capabilities.rs:40-46.",
      "reported_by": "TASK-261010-3jnv73"
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "finding_ids": [],
      "reason": "Held for static architecture/behavior inspection: one snapshot type lives in extension-api, derivation is isolated in a small core module, goal receives it through ContextContributor, no core->goal dependency is introduced, no wire/config/rollout schema changes occur, and old update_plan_enabled behavior is untouched. Scope qualification: replacement of the old pass-through is staged, not implemented by this revision; producer explicitly assigns that to the guidance leaf. This panel does not silently claim the old callsites were replaced.",
      "attack": "Check changed public types, dependency direction, goal registration, unchanged continuation callsites, Bazel source glob wiring and module size.",
      "evidence": "15-file candidate diff; ext/extension-api/src/contributors/context.rs:21-24; ext/goal/src/extension.rs:616-629,767; ext/goal/src/steering.rs:59-74; core/BUILD.bazel:7; extension-api/BUILD.bazel and goal/BUILD.bazel use codex_rust_crate source defaults. No include_str/include_bytes additions.",
      "reported_by": "TASK-261010-3jnv73"
    }
  ],
  "free_hunt": [
    "[TASK-261010-3jnv73] {\"budget\": \"15 changed candidate paths plus five adjacent concerns: native runtime provenance; history-based discovery; heap bounds/transience; external API/scope staging; evidence identity/build wiring. No builds, tests, worktree mutations of candidate source, or mutations of the reviewed task.\", \"result\": \"Two actionable static findings A-F1/A-F2; boundedness is a secondary consequence of A-F1 rather than a duplicate blocker. Evidence/scope/size limitations are recorded in notes.\", \"coverage\": {\"surface_rows_swept\": 7, \"surface_rows_total\": 7, \"held\": 3, \"broken\": 3, \"not_attacked\": 1, \"exact_candidate_runtime_rows_executed\": 0, \"exact_candidate_runtime_rows_total\": 7, \"earlier_snapshot_core_tests_passed\": 5106, \"earlier_snapshot_core_tests_run\": 5106, \"earlier_snapshot_core_tests_skipped\": 11, \"attached_earlier_snapshot_mutants_killed\": 10, \"attached_earlier_snapshot_mutants_total\": 10, \"raw_mutant_logs_independently_inspected\": 1, \"mutant_core_job_conclusions_independently_checked\": 10}, \"blind_spots\": [\"No dynamic-name or discovered-native-wait runtime reproduction was executed; their production mechanisms were traced statically. Requested tests are new tests, not claims of already failing existing tests.\", \"No real remote catalog replacement -> sampling snapshot test was identified.\", \"Earlier snapshot evidence does not attest the rebased full tree, all platforms, or unexecuted candidate attacks.\"], \"stop_condition\": \"All seven normative rows have exactly one result and the five-concern free hunt is closed; no first-hit exit.\"}",
    "[TASK-261010-3syszw] {\"area\": \"goal contributor wiring\", \"outcome\": \"held\", \"detail\": \"prompt_contributor pushes Arc<dyn ContextContributor> into context_contributors (registry.rs:113), so goal contribute_turn_context runs at both paths; verified, not assumed.\"}",
    "[TASK-261010-3syszw] {\"area\": \"prompt-byte neutrality of the new contributor\", \"outcome\": \"held\", \"detail\": \"Both paths push only per returned fragment with no separators or per-contributor markers; goal returns empty at thread, turn, and world-state points (trait defaults plus the empty renderer). Registration cannot change prompt bytes.\"}",
    "[TASK-261010-3syszw] {\"area\": \"native_wait namespace breadth\", \"outcome\": \"held\", \"detail\": \"Any-namespace matching is required because V2 namespaces are dynamically configured (spec_plan.rs:737), and the actual ToolName is carried so guidance names a real callable tool. V1/V2 distinction is pinned by namespaced-name tests plus the v1_only/v2_only mutant kills.\"}",
    "[TASK-261010-3syszw] {\"area\": \"exec_command shadow order\", \"outcome\": \"dismissed\", \"detail\": \"find() on spec.name() could theoretically hit a same-named namespace before the function; requires an MCP namespace literally named exec_command surviving finalization. No realistic trigger.\"}",
    "[TASK-261010-3syszw] {\"area\": \"native_mail_wait production reachability\", \"outcome\": \"held\", \"detail\": \"Goal runtime inserts admission_checker into the thread store on background-wait continuation (runtime.rs:668), enabled only when the host is available (extension.rs:183). The flag can be true in production and is false without an installed goal (suite asserts).\"}",
    "[TASK-261010-3syszw] {\"area\": \"test-helper consistency\", \"outcome\": \"held\", \"detail\": \"StepContext::for_test uses none() matching its empty router; with_tool_router_for_test re-derives tool flags with default-off markers. Test-only; production capture untouched.\"}"
  ]
}
```

## Recording reviewer audit — 2026-10-10, RUN-261010-eabfdc

Verdict: **changes_requested** for CR-TASK-260929-2is91w-1 revision 1, candidate tree `fc18da8f7415a89029a6a0e7bc539e107749984a`.

Read both task-owned panel outcomes and this merged resource through `task-board resource get --output -` (all three exit 0). Compared their structured verdict-findings blocks: findings preserved 2/2; ordered surface rows present 7/7 in each input and merged output; worst-result merge correct 7/7; notes preserved 9/9; free-hunt entries preserved 7/7. Finding payloads are unchanged except the explicit provenance/pinned-blob annotations and null-to-none repeat normalization. Panel A requests changes; panel B accepts; therefore the merged verdict requests changes.

| Surface row | Recorded result |
|---|---|
| flag derivation | broken (A-F1) |
| final-router derivation | broken (A-F2) |
| subscriptions are not capabilities | held |
| one snapshot, both paths | held |
| configuration coverage | not-attacked |
| bounded and transient | broken (A-F1 consequence) |
| API surface and placement | held |

No new findings or code review were added. No code, index, branch or candidate files were changed; no builds, tests, mutants or hosted gates were rerun. Runtime evidence remains imported from the panel reports with their exact-tree limitations, including 0/7 exact-candidate runtime attacks. The update_plan_enabled migration remains explicitly staged to the guidance leaf as documented in both panels.

Logbook: merge integrity confirmed, including both native-wait defects and the remote-catalog coverage limitation. `task-board spawn goal "$TASK_BOARD_RUN_ID"` exited 0 and reports no goal binding; directives read exited 0 with none present. Reject revision 1 through `reject_cr` with this task-scoped verdict evidence and route to `to-dev`; acceptance is not authorized by the panel merge. No temporary directory or repro was created.
