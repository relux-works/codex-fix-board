# TASK-261011-1grcu4 — R141 DELTA panel, waiting-capabilities-snapshot rev3

changes_requested

Read-only review of CR-TASK-260929-2is91w-3. Replay base:
`e0eff057620104a416080da616256ee7f32bda1b`. Expected and observed candidate tree:
`f8ae85582d54c47b237476e8d88742f942961f3f`. The temporary-index replay matched exactly.

The previous round's A2-F1 orphan-client false positive and D-F1 fabricated positive
fixture are addressed. The rework introduces a false negative for legitimate
server search outputs with a null call ID. These outputs are explicitly supported
by the protocol, survive the request normalizer, and can carry discovered tools,
but the new scan discards them. This is a static finding; no new Rust reproduction
was executed by this panel.

Commands and observed exits:

| Command | Exit / observation |
|---|---|
| `task-board m 'set_status(TASK-261011-1grcu4, status=analysis)'` | 0 |
| Python temporary-directory creation and removal of the task-specific replay index | 0; initial `rm -f` shell request was rejected before execution, so it has no process exit code |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-1grcu4-replay.idx" git read-tree e0eff057620104a416080da616256ee7f32bda1b` | 0 |
| `task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev3.patch --output .temp/TASK-260929-2is91w_change-request_rev3.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-1grcu4-replay.idx" git apply --cached .temp/TASK-260929-2is91w_change-request_rev3.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-1grcu4-replay.idx" git write-tree` | 0; exact expected tree printed |
| Resource downloads: surface-table, merged rev2 verdict, hosted precheck 10, results, producer brief, rework brief | Each download 0 |
| Narrow task queries for description/scope/AC and this panel's checklist; `schema(operation=get)` | 0 |
| Queries using nonexistent fields `resources` and `resource_refs` | Each 1; no resource absence inferred |
| `task-board resource list TASK-260929-2is91w` | 0 but printed help; not a resource inventory |
| Project-management skill read | 0; combined reference read printed a missing reviewer-role file error but returned 0 from the succeeding negative-evidence read; reviewer role was not loaded from that missing file, so the explicit panel contract supplied the review rules |
| Reviewer-role searches | First `rg` 2 (nonexistent search root); second `rg`/filter 1 (no match); subsequent bounded resource-path inventory 0 |
| Python pinned-file extraction | First 1, caused by nested `git show` exit 128 for nonexistent `core/src/tools/discovery.rs`; already extracted files were retained; remaining requested existing files subsequently extracted with exit 0. No absence claim about discovery logic was made from the failed read |
| Pinned `git show`, `git grep`, `git diff --stat`, rev2-to-rev3 diff, `git status --short`, and subsequent targeted `sed`/`rg` reads | 0; pipeline reads were informational, not validation gates |
| `git diff --check e0eff057620104a416080da616256ee7f32bda1b f8ae85582d54c47b237476e8d88742f942961f3f` | 0 |
| `gh run view 38142174620 --repo ivanopcode/codex --json conclusion,headSha,jobs,url` and bounded `--jq` projection | Each 0 |
| `gh run view 38142174620 --repo ivanopcode/codex --job JOB --log` for jobs 114480088920, 114478108334, 114480090925, 114480090701, 114480088943, 114480089960 | Each retrieval 0; retrieval success is not the retrieved gate's exit |
| `gh api repos/ivanopcode/codex/git/commits/SHA --jq ...` for snapshot d772e5c0357c2ae4e00c2e207c16b4a122507f79 and mutant commits 491e20c5e321c07239a2aa3e028c96839e8a14d2 / beaf2b216eeaf3d7a90d8eced55964a7cbd2db76 | Each 0 |
| Python hosted-log extraction | 0; corrected the initial mutant-number assumption using the plan and commit messages before attributing any kill |
| `python3 .temp/TASK-261011-1grcu4-check-verdict.py` | 0; one JSON object and one verdict, 7/7 ordered unique surface rows, required finding fields, cited candidate blobs and exact replay tree verified |
| `task-board spawn directives RUN-261011-54c03a` at safe checkpoints | 0; no directives |

Hosted evidence reused, not rerun: [relux-ci run 38142174620](https://github.com/ivanopcode/codex/actions/runs/38142174620).
The plan and snapshot core checkout identify snapshot commit
`d772e5c0357c2ae4e00c2e207c16b4a122507f79`; the commit API independently returns
the exact replayed candidate tree. The workflow head `9f8fdf9a...` is not this
snapshot. Lint and snapshot small/core/app-server jobs conclude success. The core
log reports **5119/5119 passed, 11 skipped**. Numeric exits for successful hosted
lane commands are not printed in the inspected summary; only successful job
conclusions and the core test summary are claimed.

All 13 mutant core jobs conclude failure. The attached precheck-10 outcome names
13/13 killed mutations. Four raw mutant core logs were inspected: actual mutant-1
(pairing), mutant-9 (discovery), mutant-12 (sleep), mutant-13 (stdin). Each gate
reports **exit 100**, an expected-red test failure. Pairing fails the orphan and
mismatched-ID tests; discovery fails the integrated search test and two discovery
unit/capture tests; sleep and stdin each fail their two named refusal tests. The
remaining nine named kills are accepted from attached precheck evidence plus job
conclusions, not independently inspected raw test failures.

No cargo, just, builds, formatting, new Rust tests, commits, branch changes or
candidate edits were performed. Only this panel's artifact and temporary read
evidence were created. No mutation, resource attachment, acceptance, rejection,
status change or handoff was issued on TASK-260929-2is91w.

Logbook — 2026-10-11: exact replay and hosted snapshot identity verified. Previous
findings addressed; regression D3-F1 concerns supported null-ID server outputs,
not the former orphan-client false positive. Seven surfaces swept: five held,
one broken, one not-attacked. Remote catalog observation remains an explicit
coverage limitation. Route ordinary rework through the orchestrator; no external
blocker or human-only decision is needed.

Successor recovery — 2026-10-11, RUN-261011-def9b1

The command history above and the raw hosted-log inspection are predecessor
RUN-261011-54c03a evidence, reused without claiming a fresh execution. This
successor independently reran the temporary-index replay, diff whitespace gate,
and exact hosted snapshot commit/tree query. All returned exit 0. The replay
again prints f8ae85582d54c47b237476e8d88742f942961f3f.

Fresh reads also verified both previous merged finding IDs (A2-F1, D-F1), the
rev2-to-rev3 three-file delta, supported null-ID protocol inputs, normalization,
stream retention and sampling capture, both contributor paths, bounded public
snapshot fields, goal consumption and remote model replacement. The retained
seven-row verdict and finding are unchanged. The CR3 validation log itself is
readable in full (404 bytes): mini-hosted-gate reports exit 0 for the exact
candidate, required=1/green=1/failed=0/missing=0 exact command shards;
test_case_coverage remains unknown. This is reused gate evidence, not a rerun.

Successor commands and exits (no local Rust commands):

| Command | Real exit / observation |
|---|---|
| Initial own-task analysis mutation | 0 |
| read-tree, patch resource get, apply --cached, write-tree (exact commands above) | Each 0 |
| `git diff --check e0eff057620104a416080da616256ee7f32bda1b f8ae85582d54c47b237476e8d88742f942961f3f` | 0 |
| `gh api repos/ivanopcode/codex/git/commits/d772e5c0357c2ae4e00c2e207c16b4a122507f79 --jq '.tree.sha'` | 0; exact candidate tree |
| `gh run view 38142174620 --repo ivanopcode/codex --json conclusion,jobs --jq '{conclusion, jobs: [.jobs[] \| {name, conclusion}]}'` | 0; four snapshot/lint lane successes, 13/13 mutant core failures; overall workflow failure is expected, not green |
| Four fresh resource gets: surface-table.md, merged rev2 verdict, rev3 validation log, hosted precheck 10 | Each 0 |
| own-task failed handoff log download; targeted task queries using known fields; schema(operation=get) and schema(); skill read; git status and rev-parse; git show/diff; Python pinned-range reads and log/previous-ID inspection | Each 0 |
| Queries with nonexistent resources/attachments fields | Each 1; query errors, no absence inferred |
| `task-board resource list` on either task | Each 0 printing help; no inventory inferred; replaced with preconditionResources/outcomeResources queries |
| Combined skill-reference read | 1: referenced reviewer-role file absent; negative-evidence body read; explicit assigned panel contract applied |
| rg inventory searches including missing roots | Each 2 or 1 as printed; missing search roots/no match, no product-source absence inferred |
| delivery-validation skill reference read | 1: reference file absent; no validation skip inferred from that failed read |
| `task-board spawn directives RUN-261011-def9b1` | 0; no directives |
| `python3 .temp/TASK-261011-1grcu4-check-verdict.py` | 0; replay/tree, exact block, schema and 7/7 row gate rerun by successor |

Recovery logbook: the predecessor's panel handoff gate failed with real exit 1:
tree 9d90dbd88d270c0f7da516fcd21ebe4078e04fe9 had no recorded hosted run.
It included the research verdict as a repository file, not the reviewed CR3
candidate. Preserve that failure as failure. The verdict is now materialized in
ignored .temp and remains an attached text outcome on this panel task. This
keeps the intended read-only research repository delta empty; no source build or
new CI claim is needed. The successor retained the prior task-scoped outcome
and uses resource update to record this attribution and recovery, rather than
silently replacing it. No source-task mutation was issued. Ready for review.

```verdict-findings
{
  "findings": [
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
          "expected_failure": "Requested diagnostic, NOT EXECUTED: replace Some(server-search-1) in the existing server positive test with /*call_id*/ None while preserving execution=server, completed status and the multi_agent_v1.wait_agent loadable definition. Keep the existing expected discovered set. Candidate returns an empty set and fails equality. Retain Some-ID server, paired-client and orphan-client controls. This command against the existing unmodified test is green in hosted evidence; only the requested diagnostic is predicted red."
        },
        {
          "test_file": "codex-rs/core/tests/suite/search_tool.rs (requested server_search_without_call_id_updates_waiting_capabilities)",
          "command": "just test -p codex-core -E 'test(=suite::search_tool::server_search_without_call_id_updates_waiting_capabilities)'",
          "expected_failure": "Requested public-entry regression, NOT EXECUTED: reuse configure_search_capable_model and the recorder. Emit a completed server tool_search_output with call_id:null and a genuine deferred multi_agent_v1.wait_agent loadable spec through response.output_item.done, finish the response, then submit the second turn with changed approval policy as the current integration test does. Assert the next request retains that definition and the contributor snapshot has Some(actual native name). Candidate retains the output but yields None. Add a narrowing mutant rejecting only null-ID server outputs, killed by this test."
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "A2-F1 addressed for orphan/mismatched Some-ID client outputs: the scanner requires an earlier matching call; hosted pairing mutant-1 core job 114480088943 fails the two refusal tests with exit 100. Original malformed-history normalization can still panic by existing design; this CR does not claim to repair unrelated corrupt-history handling.",
    "D-F1 addressed: capture fixture now records a real call/output pair and checks for_prompt survival. New suite::search_tool::discovered_native_wait_updates_waiting_capabilities drives real tool_search and observes None before and Some after discovery. Snapshot core reports it PASS; native_wait_ignores_discovered mutant-9 core job 114480089960 fails it with exit 100. Contributor observation is on the second turn with changed approval policy, not independently on request 2. The rework brief permits this bounded search coverage without a wait-execution control; no wait invocation or resume/fork negative integration was added.",
    "Prior A-F1 native provenance fix still holds: default runtime marker is false; only native V1/V2 wait handlers and the delegating V2 wrapper report true. Registry selection supplies actual configured identity. No bare-name fallback was reintroduced.",
    "Size remains outside guidance: 2260 changed lines (+2254/-6) over 21 files, including 1461 test lines and a separate 303-line derivation module. Rev2-to-rev3 delta is confined to three files. Retain the earlier split/consolidation concern; this panel grants no size exception and adds no style-only blocking finding.",
    "TurnContextContributionInput gains a required public Rust reference field, breaking out-of-tree struct-literal constructors. In-repository construction sites are updated. No app-server wire, CLI, config schema, dependency lockfile or persisted rollout shape changed.",
    "update_plan_enabled replacement remains staged to the guidance leaf as prior review acknowledged; existing signal/rendering stays intact. Goal installs the contributor but emits zero fragments, so no new model-visible token payload, context rewrite or cache-changing prompt text is introduced.",
    "Installed-goal pointer identity is statically wired through the same contributor registry; its test invokes the renderer, while the two-path core test records one borrowed instance. Do not claim an independent installed-goal pointer attack.",
    "Numeric exits for successful hosted lane commands are unknown from the inspected logs; expected-red mutant command exits observed are 100. Local gates rerun here are replay and git diff --check only. Full runtime suite and mutant evidence is hosted Linux evidence; eleven snapshot skips remain skips, not cross-platform coverage."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "finding_ids": [],
      "attack": "Check all five derivations, each host/policy/opt-in/control conjunct, direct-vs-nested visibility and native V1/V2 provenance and configured name. Discovery-history admission is recorded separately in final-router derivation.",
      "evidence": "Pinned waiting_capabilities.rs:43-79,203-300; router.rs:233-239; registry.rs:86-96; native handler and wrapper diff. Exact-tree precheck 10 has named conjunct/provenance kills. Raw sleep mutant-12 and stdin mutant-13 each fail two refusal tests, exit 100. Snapshot core log passes the flag matrix."
    },
    {
      "row": "final-router derivation",
      "result": "broken",
      "finding_ids": ["D3-F1"],
      "attack": "Compare client/server discovery admission to supported protocol inputs and the actual normalized request; sweep orphan IDs, mismatched IDs, legitimate pairs, missing IDs, deferred registry rechecks, exclusions and stale discovery.",
      "evidence": "D3-F1 sources show the null-ID server narrowing. Earlier orphan and positive-fixture defects have exact-tree hosted kills and integrated search coverage. Current registry still prevents absent/excluded/shadowed/nested-only tools from being counted; no additional registry defect established."
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "finding_ids": [],
      "attack": "Trace data dependencies and public exec launch, acknowledgement, idle wake and later-turn snapshot comparisons.",
      "evidence": "waiting_capabilities.rs:64-79 consumes only host and policy markers; pending_and_acknowledged_work_does_not_flip_flags compares whole snapshots. suite/exec_notification.rs:756-835 drives production exec and compares every captured snapshot. Exact snapshot core log records the integrated test PASS (2.706s)."
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "finding_ids": [],
      "attack": "Trace capture ownership, both borrowed contribution inputs and goal contributor installation; inspect pointer-recorder assertions.",
      "evidence": "session/mod.rs:3971-4001,4310-4317,4405-4418; session/step_context.rs:42-47; ext/goal/src/extension.rs:616-630,767; waiting_capabilities_tests.rs:1391-1422. Exact snapshot core logs same_snapshot_instance_reaches_both_context_paths PASS. Goal pointer leg is static evidence as noted."
    },
    {
      "row": "configuration coverage",
      "result": "not-attacked",
      "finding_ids": [],
      "reason": "Partial exact-tree runtime attacks cover sleep switches, headless host, code mode and excluded receipt/exec tools. Remote-catalog-to-snapshot behavior remains unmeasured: snapshot_follows_catalog_clock_support edits already resolved ModelInfo rather than driving remote fetch/replacement. This limitation is independent of the prohibition on local builds.",
      "attack": "Compare the catalog helper test with ModelsManager::apply_remote_models and captured model consumption; inspect the remaining configuration tests.",
      "evidence": "waiting_capabilities_tests.rs:861 onward,942-977; models-manager/src/manager.rs:672-702 replaces matching bundled slugs. No new static remote-catalog defect established; hosted precheck supports the other configuration legs.",
      "requested_attack": {
        "test_file": "codex-rs/core/tests/suite/search_tool.rs or a new waiting-capabilities suite (requested)",
        "command": "just test -p codex-core -E 'test(remote_catalog_replacement_changes_waiting_snapshot)'",
        "expected_failure": "Requested, NOT EXECUTED: mock a remote entry replacing the same bundled slug with clock support removed and the reverse positive control; observe the snapshot during real sampling. A mutant ignoring remote replacement must fail."
      }
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "finding_ids": [],
      "attack": "Inspect snapshot fields, native identity source and heap bound, persistence conversion, prompt builders and empty goal rendering.",
      "evidence": "extension-api/src/waiting_capabilities.rs:24-59 is four booleans and one optional ToolName, no collections or serialization. Native identity is exclusively native runtime configuration; config/mod.rs:3148-3207 limits namespace to 64 ASCII characters. StepContext conversion omits it. Snapshot core passes waiting_snapshot_does_not_persist_to_history_or_rollout; header-size test alone does not establish the heap bound."
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "finding_ids": [],
      "attack": "Inspect public constructors, dependency direction, module size, old plan-enabled signal, schema/lockfile surfaces and Bazel source availability.",
      "evidence": "One exported extension-api snapshot and one borrowed contributor field; private 303-line core derivation module. Goal consumes the API through existing extension registration; no core-to-goal dependency. Core BUILD.bazel source glob includes new files; no new compile-time file reads/dependencies/schema changes. Existing plan signal stays intact under the acknowledged staged scope. Hosted lint/small/app-server conclusions are success; public Rust compatibility and size caveats remain in notes."
    }
  ],
  "free_hunt": {
    "budget": "After both previous findings and all seven rows, bounded hunt across supported search item shapes and normalization, stream recording/resume retention, stale discovery/current registry, native provenance and namespace bounds, context emission and persistence, external API/build wiring, and hosted evidence identity.",
    "result": "One rework regression D3-F1. No other production defect established in this sweep. Output-before-call strictness and malformed spec parsing remain unexecuted shape limits; no separate finding inferred without a supported production trigger.",
    "coverage": {
      "surface_rows_swept": 7,
      "surface_rows_total": 7,
      "held": 5,
      "broken": 1,
      "not_attacked": 1,
      "previous_findings_addressed": 2,
      "previous_findings_total": 2,
      "attached_mutants_killed": 13,
      "attached_mutants_total": 13,
      "mutant_core_job_conclusions_checked": 13,
      "mutant_raw_logs_inspected": 4,
      "snapshot_core_tests_passed": 5119,
      "snapshot_core_tests_run": 5119,
      "snapshot_core_tests_skipped": 11,
      "integrated_client_search_snapshot_attacks_in_hosted_evidence": 1,
      "integrated_null_id_server_snapshot_attacks": 0,
      "integrated_remote_catalog_snapshot_attacks": 0,
      "new_local_rust_attacks_executed": 0
    },
    "blind_spots": [
      "D3-F1 is supported by pinned protocol and production source paths, not a newly executed Rust reproduction. Both requested tests remain unrun.",
      "Remote replacement-to-snapshot observation and installed-goal pointer identity lack independent public-entry runtime attacks.",
      "Nine mutant raw logs were not inspected; their named kills rely on attached precheck 10 evidence plus checked job conclusions.",
      "Linux hosted success does not establish new macOS/Windows execution; skipped tests remain outside measured coverage.",
      "The client-search integration observes the contributor after a second-turn policy change; capability-only in-turn contributor re-emission belongs to the subsequent guidance work."
    ],
    "stop_condition": "Both prior findings checked, their class swept for supported sibling shapes, all seven rows assigned exactly one result, bounded adjacent hunt closed. Nothing recorded on the implementation task."
  }
}
```
