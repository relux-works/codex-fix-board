# TASK-261011-1zp0ru — R141 panel A waiting-capabilities snapshot, revision 2

changes_requested

Replay check: base `e0eff057620104a416080da616256ee7f32bda1b` plus the revision-2 patch produced **exactly** candidate tree `ef4eb6ff644eee2a950b493b675fb86f7b3301c2` using a temporary index. `git read-tree`, patch retrieval, `git apply --cached`, and `git write-tree` each exited **0**. No worktree checkout, candidate source edits, nested worktree, build or test execution was performed.

The new discovery derivation can count an orphan client search output that the real request normalizer removes. This is one static robustness finding. Every required surface row was swept: **5 held / 1 broken / 1 not-attacked = 7/7**. The unexecuted remote replacement attack is named explicitly below. Prior native-name and direct-only defects have fixes and exact-tree hosted mutant kills.

Evidence sources: [surface table](/Users/administrator/Developer/ReluxWorks/codex-fix-board/.task-board/.resources/TASK-260929-2is91w/surface-table.md), task AC query, task-scoped producer results and `TASK-260929-2is91w_hosted-precheck-8.md`; source citations below are pinned to `ef4eb6ff644eee2a950b493b675fb86f7b3301c2`. Hosted run [38092565667](https://github.com/ivanopcode/codex/actions/runs/38092565667) and snapshot commit [7917d62](https://github.com/ivanopcode/codex/commit/7917d62f1cdbcbe68242c61ca01decd925e1a8c3) were independently checked through the GitHub API.

| Command run directly | Observed exit / result |
|---|---|
| `task-board m 'set_status(TASK-261011-1zp0ru, status=analysis)'` | 0 |
| `mkdir -p .temp && GIT_INDEX_FILE="$PWD/.temp/TASK-261011-1zp0ru-replay.idx" git read-tree e0eff057620104a416080da616256ee7f32bda1b` | 0 |
| `task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev2.patch --output .temp/TASK-260929-2is91w_change-request_rev2.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-1zp0ru-replay.idx" git apply --cached .temp/TASK-260929-2is91w_change-request_rev2.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-1zp0ru-replay.idx" git write-tree` | 0; `ef4eb6ff644eee2a950b493b675fb86f7b3301c2` |
| `task-board q 'get(TASK-260929-2is91w) { description scope ac }'` | 0 |
| `git diff --stat e0eff057620104a416080da616256ee7f32bda1b ef4eb6ff644eee2a950b493b675fb86f7b3301c2` | 0; +1990/-6, 20 paths |
| `git diff --check e0eff057620104a416080da616256ee7f32bda1b ef4eb6ff644eee2a950b493b675fb86f7b3301c2` | 0 |
| `gh api repos/ivanopcode/codex/actions/runs/38092565667 --jq '{id,head_sha,head_branch,status,conclusion,html_url}'` | 0; overall failure (expected-red mutant run) |
| `gh api 'repos/ivanopcode/codex/actions/runs/38092565667/jobs?per_page=100' --jq '.jobs[] \| {id,name,status,conclusion}'` | 0; all snapshot lanes success, 12 mutant core failures |
| `gh api repos/ivanopcode/codex/git/commits/7917d62f1cdbcbe68242c61ca01decd925e1a8c3 --jq '{sha,tree:.tree.sha}'` | 0; exact candidate tree |
| `gh api repos/ivanopcode/codex/actions/jobs/<JOB>/logs > .temp/TASK-261011-1zp0ru-hosted-<LANE>.log` for jobs 114331834641 (plan), 114333299797 (core), 114333301457 (sleep), 114333301440 (stdin), 114333300702 (provenance), 114333300779 (discovery) | Each retrieval exited 0; hosted mutant gate exits are separately 100, not the retrieval exit |
| `gh api repos/ivanopcode/codex/git/commits/<SHA> --jq '{sha,message,tree:.tree.sha}'` for 6cf9fd3f336dc258d888ecdd41c99e7167682a71 and b368ec9c454cdba3b62b5063448c5d4fffe72f1b | Each API call 0; commit messages map provenance/discovery to mutant jobs 7/8 |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0; none |
| `git status --short` | 0; clean |
| `python3 .temp/TASK-261011-1zp0ru_validate-verdict.py` | 0; JSON/schema/7-row sweep/verdict/repository-cleanliness checks passed |

Routine candidate extraction (`git show` via Python, 20 changed files plus 16 adjacent files), source reads, test-name inspection, log summary extraction, checklist reads and artifact writing exited 0. Read-only exploration failures were not gates: two `get(... resources ...)` queries exited 1 (unsupported field; corrected to task-specific projections/source resources); first combined skill read exited 1 because the router package omits `.roles/reviewer/role.md` (negative-evidence file was read); missing-path `rg` calls exited 2; several no-match role/logbook searches exited 1; an optional combined path listing exited 1 for absent guessed paths. Installed reviewer roles were found and read; their installed copies lack the newer review-round section. The panel brief and negative-evidence contract supplied the explicit sweep/attack rules. None of these failures is represented as green validation.


Logbook — 2026-10-11: replay exact; prior A-F1/A-F2 mechanics verified fixed; found raw-versus-normalized discovery evidence discrepancy A2-F1 and a misleading orphan positive fixture; independently verified snapshot identity and expected-red mutant exits. Recommendation: align discovery with the history the model actually receives, add the orphan refusal, and replace the positive fixture with a real paired search round-trip. Preserve standalone server outputs. Record this packet only on the panel task; the recording reviewer/orchestrator owns the reviewed CR decision. No external blocker or product decision is needed.

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
          "execution": "requested_not_run"
        }
      ],
      "severity": "robustness",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "The replay matches exactly. Reviewed candidate source and adjacent production paths were read from the pinned tree with git show; early adjacent worktree reads were superseded by pinned reads.",
    "Hosted identity independently verified: the workflow dispatch head is base e0eff057..., but the plan and snapshot job check out snapshot commit 7917d62f1cdbcbe68242c61ca01decd925e1a8c3. GitHub commit API identifies its tree as the reviewed ef4eb6ff... . Do not equate the workflow head SHA with the tested snapshot.",
    "GitHub run 38092565667 overall conclusion is FAILURE, as expected for mutant jobs. Lint and snapshot small/core/app-server job conclusions are success; all 12 mutant core jobs are failure. Snapshot core log: 5115/5115 passed, 11 skipped, one flaky test. Four mutant raw logs were inspected: provenance 5 failing tests, discovery 2, sleep 2, stdin 2; each failed gate exited 100. These are expected-red kills, not passing mutant gates. Other eight kills are accepted from the attached precheck report and independently checked job conclusions; their raw logs were not inspected.",
    "Numeric command exits for hosted lint/small/app-server are not present in the attached summary; only their success conclusions are claimed. No build, cargo, just, or test command ran locally in this panel.",
    "Prior A-F1 runtime provenance and prior A-F2 genuine deferred discovery mechanics are addressed. A2-F1 concerns invalid/raw discovery evidence, a distinct new robustness mechanism; it is not a repeated bare-name or direct-only finding.",
    "AC4 installed-goal pointer identity and AC5 real remote replacement are not independently exercised end-to-end by the added tests. Goal registration is statically verified. A public tool_search round-trip must replace the current orphan positive fixture; the original A-F2 request for an end-to-end search test was not implemented.",
    "Change size is 1996 changed lines (+1990/-6 across 20 files), exceeding the 800-line guidance. 1359 lines are in the test module; implementation is separately bounded. Recording reviewer should explicitly assess a split or size exception; no style-only blocking finding is added here.",
    "TurnContextContributionInput adds a required public Rust field, a source-breaking change for out-of-tree struct-literal constructors. In-repository constructors are updated. No app-server wire, CLI, config schema or rollout schema changes were found in the bounded sweep. No new context fragment or model-visible token payload is emitted.",
    "All board writes in this run are restricted to TASK-261011-1zp0ru. Nothing was accepted/rejected, status-changed, handed off, noted or attached on TASK-260929-2is91w."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "finding_ids": [],
      "attack": "Trace every conjunct and native runtime provenance; compare V1/V2/custom namespace and foreign-tool attacks with hosted narrowing failures.",
      "evidence": "waiting_capabilities.rs:44-79,218-275; router.rs:233-238; registry.rs:86-94; both native wait handlers and V2 wrapper. Exact-tree precheck 8 reports 12/12 kills. Independently read native_wait_bare_name_match core job 114333300702: five named tests fail, exit 100. The prior A-F1 name/provenance defect is addressed."
    },
    {
      "row": "final-router derivation",
      "result": "broken",
      "finding_ids": [
        "A2-F1"
      ],
      "attack": "Trace final registry exclusions/collisions and deferred discovery through raw history, normalized request input, resume reconstruction and the positive fixture.",
      "evidence": "A2-F1 sources. A-F2 direct-only defect is addressed for genuine discovered outputs: exact-tree discovery mutant core job 114333300779 fails two tests, exit 100. Its capture test currently treats an orphan as successful discovery and does not exercise normalization."
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "finding_ids": [],
      "attack": "Inspect receipt/pending provider independence and the public user-turn exec notification path.",
      "evidence": "waiting_capabilities.rs:64-79 reads only host/policy markers; tests.rs:666-687 compares pending/ack providers. Exact-tree snapshot core log shows suite::exec_notification::acknowledged_subscription_does_not_flip_waiting_capabilities PASS (2.869s), exercising exec launch, acknowledged receipt, idle completion wake and another user turn."
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "finding_ids": [],
      "attack": "Follow one capture, StepContext field ownership, both contribution inputs and installed goal ContextContributor; inspect pointer recorder test.",
      "evidence": "session/mod.rs:3977-4000,4312-4315,4410-4413; step_context.rs:44-47; ext/goal/src/extension.rs:616-630,767; extension-api/src/registry.rs:113-114. Exact-tree core log reports same_snapshot_instance_reaches_both_context_paths PASS. Goal wiring is verified statically; the goal renderer test calls the empty renderer directly and is not an independent installed-goal pointer attack."
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
      }
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "finding_ids": [],
      "attack": "Trace ToolName heap ownership to genuine native config bounds; inspect serialization, turn conversion and prompt construction.",
      "evidence": "extension-api/src/waiting_capabilities.rs:24-59 has four booleans and Option<ToolName>, no collections or serde; config/mod.rs:3148-3202 caps native V2 namespace to 64 ASCII characters. Native provenance closes the prior foreign extension namespace bound issue. StepContext::to_turn_context_item omits the snapshot and goal renders no fragments. Exact-tree hosted core reports waiting_snapshot_does_not_persist_to_history_or_rollout PASS; small lane reports snapshot_stays_small_and_bounded green. size_of checks headers only; the production config bound supplies the heap bound, not that test."
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "finding_ids": [],
      "attack": "Inspect public constructor changes, dependency direction, module placement, old plan signal and Bazel inclusion.",
      "evidence": "One extension-api snapshot type and one borrowed contributor field; derivation is a 275-line separate core module. Goal consumes the extension-api type through existing contributor registration; no core-to-goal dependency is introduced. Source globs include new Rust files; no build-time file inclusion or dependency changes. update_plan_enabled callsites remain as before: replacement is staged to the guidance leaf, as explicitly accepted in merged rev1 review; no behavior loss is claimed."
    }
  ],
  "free_hunt": {
    "budget": "Seven surface rows, then five adjacent concerns: normalization/resume discovery, native heap bounds, contributor installation/transience, external/API/build wiring, and hosted evidence identity. No builds or new runtime executions.",
    "result": "One new static robustness finding A2-F1; remote replacement has an explicit requested attack. Prior defects have fixes plus named exact-tree mutant kills.",
    "coverage": {
      "surface_rows_swept": 7,
      "surface_rows_total": 7,
      "held": 5,
      "broken": 1,
      "not_attacked": 1,
      "attached_mutants_killed": 12,
      "attached_mutants_total": 12,
      "mutant_core_job_conclusions_checked": 12,
      "mutant_raw_logs_inspected": 4,
      "snapshot_core_tests_passed": 5115,
      "snapshot_core_tests_run": 5115,
      "snapshot_core_tests_skipped": 11,
      "new_runtime_attacks_executed_by_this_panel": 0
    },
    "blind_spots": [
      "The new orphan-resume reproduction is requested, not executed. Its mechanism is established by exact source paths and the existing fixture shape.",
      "Remote replacement is not proven by directly setting ModelInfo.",
      "Hosted green lanes do not prove every structural surface or all operating systems; skipped tests stay skipped."
    ],
    "stop_condition": "All seven rows have exactly one result and the bounded free hunt is closed; no first-finding exit."
  }
}
```
