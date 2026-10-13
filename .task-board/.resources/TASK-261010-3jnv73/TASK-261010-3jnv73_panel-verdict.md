# TASK-261010-3jnv73 panel A verdict — CR-TASK-260929-2is91w-1 revision 1

changes_requested

Replay passed: base `e0eff057620104a416080da616256ee7f32bda1b` plus the task-owned rev1 patch, applied through a temporary index, writes exactly `fc18da8f7415a89029a6a0e7bc539e107749984a`. Expected and actual trees are equal. All 15 changed candidate copies were independently checked byte-for-byte against that tree. No nested worktree was created.

The two requested changes concern native-wait provenance and capability refresh after discovery. They are static findings with requested public-entry reproductions; this panel ran no Rust build, lint, test, or mutant. Seven of seven surface rows were swept, followed by a bounded free hunt. Exact-candidate runtime attack coverage is **0/7**; earlier hosted tests are identified separately below.

Commands and observed exit codes (run directly, no tee/piped gates):

| Command / read | Exit / result |
|---|---|
| `task-board m 'set_status(TASK-261010-3jnv73, status=analysis)'` | 0 |
| `mkdir -p .temp` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3jnv73-replay.idx" git read-tree e0eff057620104a416080da616256ee7f32bda1b` | 0 |
| `task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev1.patch --output .temp/TASK-260929-2is91w_change-request_rev1.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3jnv73-replay.idx" git apply --cached .temp/TASK-260929-2is91w_change-request_rev1.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3jnv73-replay.idx" git write-tree` | 0; exact tree above |
| `git diff --check e0eff057620104a416080da616256ee7f32bda1b fc18da8f7415a89029a6a0e7bc539e107749984a` | 0 |
| `git diff --quiet 09975fe220479764649c9eb740f6d71f209d457e fc18da8f7415a89029a6a0e7bc539e107749984a -- codex-rs/core codex-rs/ext` | 0; source equality only, not test execution |
| `git diff --name-status 09975fe220479764649c9eb740f6d71f209d457e fc18da8f7415a89029a6a0e7bc539e107749984a` | 0; eight arg0/cli/exec paths |
| Successful task-board projections: reviewed task `{ description scope ac notes }`, `{ preconditionResources outcomeResources }`; panel task `{ ac }`, `{ checklist }` | each 0 |
| Resource get for `surface-table.md`, `producer-brief.md`, `TASK-260929-2is91w_results.md`, `TASK-260929-2is91w_hosted-precheck-4.md`, rev1 validation log, mutants JSON, into panel-scoped `.temp` files | each 0 |
| `gh api repos/ivanopcode/codex/actions/runs/38040774172 --jq '{id,head_sha,status,conclusion,html_url}'` | 0; completed/failure (expected red mutant jobs) |
| `gh api repos/ivanopcode/codex/actions/runs/38040774172/jobs --paginate --jq '.jobs[] | {name,conclusion,id}'` | 0; four snapshot lanes success, 10 mutant core jobs failure |
| `gh run view 38040774172 --repo ivanopcode/codex --job 114181794408 --log > .temp/TASK-261010-3jnv73-hosted-core.log` | 0 (log retrieval, not a gate rerun) |
| `gh run view 38040774172 --repo ivanopcode/codex --job 114181794438 --log > .temp/TASK-261010-3jnv73-hosted-mutant2.log` | 0 (log retrieval, not a gate rerun) |
| Python source-premise assertions on candidate selector, dynamic admission, direct-spec filter, history-only discovery and pre-discovery-only test | 0; static premises only |
| Python byte identity / normative surface / old-tree delta assertions | 0; 15/15 files identical, 7 rows, 8 old-tree differences |
| Candidate `git show` reads and diff/stat/status reads | 0 except two exploratory nonexistent paths listed below |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 on both checkpoints; no directives |
| `python3 .temp/TASK-261010-3jnv73-validate-verdict.py` | 0; JSON/schema, unique surface set, verdict and replay checks |

No gate failure is hidden: the initial command containing `rm -f` was rejected by the shell tool **before execution**, so it has no process exit code; replay was then run in separate processes without removal. Exploratory board queries using nonexistent `resources`/`attachments` fields exited 1 and were replaced with the supported resource projections (exit 0). An attempted `resource list` printed help (exit 0), not an inventory. The stale skill-relative reviewer role path and exploratory role-file searches did not resolve (exit 1); the installed `/Users/administrator/.roles/reviewer/role.md` was subsequently read (exit 0), and this panel follows the more specific supplied seven-row review contract. Candidate reads of nonexistent `codex-rs/ext/tools/src/tool_name.rs` and `codex-rs/core/src/tools/handlers/multi_agents_v2/wait_agent.rs` returned 128; the real protocol tool-name and native registration sources were read successfully. These are read/setup failures, not passing validation.

Imported execution evidence, **not rerun here**: the CR validation log records `mini-hosted-gate.sh [exit 0]`, required shards 1/1, test-case coverage unknown. GitHub snapshot core job [114181794408](https://github.com/ivanopcode/codex/actions/runs/38040774172/job/114181794408) succeeds and logs 5106 passed / 5106 run, 11 skipped. Mutant-2 core job [114181794438](https://github.com/ivanopcode/codex/actions/runs/38040774172/job/114181794438) actually exits **100**, with 318 passed / 321 run, 3 failed: `exec_notify_requires_notify_opt_in`, `excluded_exec_command_disables_exec_notify`, and `missing_exec_command_schema_disables_exec_notify`. This is an expected failing narrowing mutant, not a passing test command. The other nine numeric shell exits were not independently fetched; their failing job conclusions and named killer table are supporting attached evidence. The snapshot's source tree differs from the reviewed candidate; no exact-tree execution is inferred.

Sources: every code `path:line` below refers to immutable candidate tree `fc18da8f7415a89029a6a0e7bc539e107749984a`, read with `git show <tree>:<path>`. The normative row inventory is [surface-table.md](board-resource://TASK-260929-2is91w/precondition/surface-table.md); AC/scope are the read-only task projection. Supporting evidence is [hosted-precheck-4](board-resource://TASK-260929-2is91w/precondition/TASK-260929-2is91w_hosted-precheck-4.md), [CR validation log](board-resource://TASK-260929-2is91w/outcome/TASK-260929-2is91w_change-request_rev1-validation.log), and [producer results](board-resource://TASK-260929-2is91w/outcome/TASK-260929-2is91w_results.md); producer interpretations are context, not instructions or proof.

Logbook — 2026-10-10, panel A: exact temporary-index replay established; native wait identity is inferred from an unrestricted basename; tool discovery changes history-visible callability without changing advertised specs; prior hosted snapshot is eight paths behind the candidate. Native namespace config really does enforce a 64-character cap, so an oversized native config claim was discarded. Only this panel task receives this outcome/logbook record and lifecycle/checklist writes. No accept/reject/status/handoff, resource, notes, or other mutation was sent to TASK-260929-2is91w.

Recovery audit — successor RUN-261010-53881e (2026-10-10): the prior panel outcome is retained, with both static findings independently rechecked against all 15 byte-verified candidate copies. This turn repeated the temporary-index replay (read-tree, patch retrieval, cached apply and write-tree each exit 0); actual tree is again `fc18da8f7415a89029a6a0e7bc539e107749984a`. It reran `git diff --check <base> <candidate>` (exit 0), `git diff --quiet <hosted-snapshot> <candidate> -- codex-rs/core codex-rs/ext` (exit 0; equality only), and the existing JSON/surface/replay validator (exit 0). The standalone Python source/byte audit exited 0: 15/15 changed copies match immutable candidate blobs; predecessor local and stored verdict bytes match; unrestricted basename selection and history-only discovery premises hold. No Rust commands or hosted tests were rerun; all imported runtime counts above remain predecessor evidence with the stated earlier-tree limitation.

Prior handoff failure is **failing**, not green: its CR validation log records `/Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh`, exit **1**, command shards 0/1 green, with refusal because the research-only source tree `05505c4aa3bc27535d4674185ac53e6bf9ff6e13` had no green hosted run. The cause was the report being stored as an untracked repository path. This successor preserves the report in ignored `.temp/` and updates this task's existing outcome; research evidence introduces no product source delta and does not need a hosted product build. No validation setting or source code was changed.

Additional setup/read outcomes this turn: initial `rm -f` replay setup was rejected before execution (no exit code), then `Path.unlink(missing_ok=True)` setup exited 0. Two unsupported `{ resources }` projections exited 1; supported projections subsequently exited 0. `resource list` printed help with exit 0, not inventory. The missing skill-relative reviewer role read and scoped role-file search exited 1; the actual `/Users/administrator/.roles/reviewer/role.md` read exited 0. Prior validation resource retrieval, surface/producer/precheck reads, task/checklist/resource projections, scoped schema, help and directive reads exited 0. Candidate source/diff/status reads exited 0. These setup/read errors are not validation passes.

Logbook — successor recovery: replay and two findings reaffirmed; prior failed source-validation handoff diagnosed and repaired by retaining research solely as a task outcome. Seven inherited checklist items were audited against the persisted report and successful artifact/replay validation. No write to the reviewed task occurred.

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
          "execution": "requested_not_run"
        }
      ],
      "severity": "regression",
      "repeat-of": null
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
          "execution": "requested_not_run"
        }
      ],
      "severity": "regression",
      "repeat-of": null
    }
  ],
  "notes": [
    "Evidence identity: replay is exact, but hosted precheck 4 ran snapshot commit d124f818544fdf41b5e5fb2c29e4bcbd27571bca / worktree tree 09975fe220479764649c9eb740f6d71f209d457e, not the reviewed fc18da8f7415a89029a6a0e7bc539e107749984a. Direct tree comparison finds eight arg0/cli/exec changes and zero core/ext changes. The attached mini-hosted-gate log passes an equivalence/replay-on-HEAD check; that is not execution on the rebased full candidate. No exact-candidate runtime attacks are claimed by this panel. Re-run the named integration attacks and mutants on the reworked frozen tree; do not mistake file equality for unchanged full source identity.",
    "Hosted evidence independently checked: GitHub run 38040774172 is overall failure because all 10 mutant core jobs fail. Snapshot lint/small/core/app-server jobs succeed. Fetched snapshot core log reports 5106/5106 passed, 11 skipped; fetched mutant-2 core log reports 318/321 passed, 3 failed, shell exit 100. The failures are the expected kills (exec opt-in narrowing), not a green mutant gate. Other nine named kills are accepted from the attached precheck report and independently checked failing job conclusions; their raw logs were not fetched.",
    "AC7 attached evidence reports 10/10 mutants killed on the earlier snapshot. Those mutants do not cover A-F1 external provenance or A-F2 the false-before/true-after discovery transition. Killer locations and public-entry reach must be distinguished: most one-conjunct kills are synthetic-router or router-builder tests, not new end-to-end user-turn attacks.",
    "Scope staging: runtime.rs/steering.rs update_plan_enabled pass-through remains. No behavior loss is introduced, but the literal scope replacement is deferred to TASK-260929-1w5ivu by producer context. The recording reviewer/orchestrator should make this staging explicit in the merged result.",
    "Change size: +1448/-4 across 15 paths exceeds 800-line guidance; ~1012 lines are the new test module, not entirely a mechanical generated delta. Consider consolidating the repeated snapshot matrix or explicitly approving the size exception; do not strip the integration attacks needed for the two findings. No independent blocking style finding added.",
    "No fragments or new prompt text are emitted, so no new model-context item or >1k-token fragment is injected by this revision. Adding a field to TurnContextContributionInput is source-breaking for Rust struct-literal consumers; all in-repository constructors are updated, and no app-server wire/CLI/config/session-resume surface changes were found in the bounded sweep."
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
      "evidence": "Candidate source citations in A-F1; earlier hosted conjunct mutants are supporting evidence only, not exact-candidate executions."
    },
    {
      "row": "final-router derivation",
      "result": "broken",
      "finding_ids": [
        "A-F2"
      ],
      "reason": "Derivation occurs after finalization and correctly excludes nested-only and undiscovered tools, but discovery exposes deferred tools through response history without changing model_visible_specs. Snapshot therefore never observes the discovered callable tool.",
      "attack": "Follow the public tool_search -> ToolSearchOutput -> next-sampling path; check both sides of the discovery boundary.",
      "evidence": "A-F2; candidate search_tool.rs explicitly defends no follow-up tool injection. Existing deferred test has only a false-before assertion."
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "finding_ids": [],
      "reason": "Held by static input/data-flow attack: derivation reads only final specs, AsyncNotificationSupport and GoalBackgroundWaitAdmission. PendingWorkProvider/receipts/ack state cannot affect its return. The suite test arms a real receipt and compares all observed snapshots; independently fetched older snapshot log records its PASS. This is a static hold, not a claim that this panel executed the test on the candidate.",
      "attack": "Replace armed/queued/leased work and receipt acknowledgements while keeping router/host/policy fixed.",
      "evidence": "waiting_capabilities.rs:35-58; waiting_capabilities_tests.rs pending_and_acknowledged_work_does_not_flip_flags; core/tests/suite/exec_notification.rs:736-835; hosted snapshot core log PASS for acknowledged_subscription_does_not_flip_waiting_capabilities."
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "finding_ids": [],
      "reason": "Held by static reference-identity attack: capture derives once, StepContext owns the result, and both contribution constructors borrow &step_context.waiting_capabilities. The registered GoalExtension ContextContributor forwards that reference to the renderer. No per-path recomputation or cloned snapshot appears. The earlier hosted pointer test passed; the goal renderer test alone is not an installation-path proof.",
      "attack": "Trace allocation and each borrow through initial-context, diff-context, prompt-contributor registration and goal renderer.",
      "evidence": "core/src/session/mod.rs:3971-3992,4291-4310,4406; session/step_context.rs:41-44; ext/goal/src/extension.rs:616-629,767; ext/goal/src/steering.rs:67-73; waiting_capabilities_tests.rs:942-972."
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
      "evidence": "waiting_capabilities_tests.rs:677-713; models-manager/src/manager.rs:456-473,577 onward; TASK-260929-2is91w_hosted-precheck-4.md identifies the earlier tree."
    },
    {
      "row": "bounded and transient",
      "result": "broken",
      "finding_ids": [
        "A-F1"
      ],
      "reason": "Transience holds statically: no serialization/history/rollout path includes the snapshot and the goal renderer emits nothing. Hard boundedness is compromised by A-F1: any extension namespace String attached to a visible wait_agent is cloned into native_wait with no snapshot length check. size_of<=128 measures String headers, not heap bytes. Native V2 config and app-server dynamic namespace validators cap namespaces at 64, so those paths do not reproduce an oversized native name; extension executor registration has no equivalent bound. Restricting A-F1 to genuine native identities can inherit the existing native namespace limit instead of adding a duplicate name policy.",
      "attack": "Follow ToolName heap ownership, native config validation, app-server validation, and extension-executor registration; inspect persisted turn conversion.",
      "evidence": "ext/extension-api/src/waiting_capabilities.rs:26-41; protocol/src/tool_name.rs:12-16,36-40; waiting_capabilities.rs:106; core/src/config/mod.rs:3148-3202; spec_plan.rs:1499-1525; session/step_context.rs:51 onward; ext/extension-api/tests/waiting_capabilities.rs:40-46."
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "finding_ids": [],
      "reason": "Held for static architecture/behavior inspection: one snapshot type lives in extension-api, derivation is isolated in a small core module, goal receives it through ContextContributor, no core->goal dependency is introduced, no wire/config/rollout schema changes occur, and old update_plan_enabled behavior is untouched. Scope qualification: replacement of the old pass-through is staged, not implemented by this revision; producer explicitly assigns that to the guidance leaf. This panel does not silently claim the old callsites were replaced.",
      "attack": "Check changed public types, dependency direction, goal registration, unchanged continuation callsites, Bazel source glob wiring and module size.",
      "evidence": "15-file candidate diff; ext/extension-api/src/contributors/context.rs:21-24; ext/goal/src/extension.rs:616-629,767; ext/goal/src/steering.rs:59-74; core/BUILD.bazel:7; extension-api/BUILD.bazel and goal/BUILD.bazel use codex_rust_crate source defaults. No include_str/include_bytes additions."
    }
  ],
  "free_hunt": {
    "budget": "15 changed candidate paths plus five adjacent concerns: native runtime provenance; history-based discovery; heap bounds/transience; external API/scope staging; evidence identity/build wiring. No builds, tests, worktree mutations of candidate source, or mutations of the reviewed task.",
    "result": "Two actionable static findings A-F1/A-F2; boundedness is a secondary consequence of A-F1 rather than a duplicate blocker. Evidence/scope/size limitations are recorded in notes.",
    "coverage": {
      "surface_rows_swept": 7,
      "surface_rows_total": 7,
      "held": 3,
      "broken": 3,
      "not_attacked": 1,
      "exact_candidate_runtime_rows_executed": 0,
      "exact_candidate_runtime_rows_total": 7,
      "earlier_snapshot_core_tests_passed": 5106,
      "earlier_snapshot_core_tests_run": 5106,
      "earlier_snapshot_core_tests_skipped": 11,
      "attached_earlier_snapshot_mutants_killed": 10,
      "attached_earlier_snapshot_mutants_total": 10,
      "raw_mutant_logs_independently_inspected": 1,
      "mutant_core_job_conclusions_independently_checked": 10
    },
    "blind_spots": [
      "No dynamic-name or discovered-native-wait runtime reproduction was executed; their production mechanisms were traced statically. Requested tests are new tests, not claims of already failing existing tests.",
      "No real remote catalog replacement -> sampling snapshot test was identified.",
      "Earlier snapshot evidence does not attest the rebased full tree, all platforms, or unexecuted candidate attacks."
    ],
    "stop_condition": "All seven normative rows have exactly one result and the five-concern free hunt is closed; no first-hit exit."
  }
}
```
