# TASK-260929-csyzcj \u2014 goal-owned-durable-sleep-lease: CR revision 6 review handoff


## Current handoff verification \u2014 2026-10-14

Candidate remains UNCOMMITTED and byte-identical to hosted precheck 19 tree `0b9a8f04e991fd685a0d43a0b3f8a4cc11ddf148`, snapshot `b6f695ece58c262bb6030ad8e7f98d0dc`. Temporary-index `git read-tree HEAD`, `git add -A`, and `git write-tree` each exited 0. The real index was not changed. No source/test/configuration file was changed during this handoff pass; no local build, formatter, test or mutant execution was rerun.

Authoritative reused evidence: `TASK-260929-csyzcj_hosted-precheck-19.md`, [relux-ci run 38476605332](https://github.com/ivanopcode/codex/actions/runs/38476605332), dispatched from relux/ci-next. Live read confirms lint, snapshot small, snapshot core and snapshot app-server all succeeded. The small lane includes protocol/rollout: their named failing mutant tests are present in the retrieved logs. All 15 mutants have named failures on this green candidate; 0 survivors. The mutant lanes intentionally exit 100 on test failure: these are expected-red checks, not passing tests. Full failed-test names, mutant commit identities and observed exit codes are attached in `TASK-260929-csyzcj_precheck19-mutant-evidence.json`.

This evidence closes rev5 `interrupted-item-token-threshold-unreviewed` with the 838-byte whole-item bound, while retaining prior typed-fragment, identity/legacy-resume, envelope and routing fixes. The orchestrator's `config: &*parent.config().await` compile fix and ThreadSpawn legacy-resume fixture fix remain. The V2 catalog fixture correction below is verified by the green hosted run; the short precheck summary's phrase \u201castra rework\u201d is a label, not the implementation: the candidate explicitly overrides gpt-5.5 metadata to V2.

Commands rerun in this pass: tree commands above (0 each); board resource/query reads (0 after correcting an unsupported `resources` projection); `gh run view ... --json jobs` (0); `gh run view ... --log-failed` (0); local `git show -s --format=%s <mutant-sha>` (0 each). An initial scratch-directory existence assertion exited 1 before any tree check, then the temporary directory was created and the tree check succeeded. A direct `gh api .../logs` read exited 1 because terminal escapes require opt-in; the successful `gh run view --log-failed` read supplied the evidence instead. Missing optional skill directories gave rg exit 2; the project-management skill and existing .codex skill catalog were read successfully. None of these exploratory failures is presented as a green gate.

Tool readiness was checked with task-board help, git/rg/gh/Python version output. Scratch evidence was staged only under ignored `.temp/`, attached through board resource mutations, and the task-created scratch files/directories are removed before handoff. No control-root file was edited directly. The remainder records the implementation and previous-pass validation, followed by current hosted mutant results. Declared coverage limits are retained rather than upgraded by a green suite.

## Precheck 18 root cause and fixture correction

Hosted run 38365654460 passed lint, small and app-server; core was 5159/5160 with the dense fixture failing its depth-zero spawn-tool assertion three times. This red baseline does not certify a green candidate or behavioral mutant kills.

The earlier claim that choosing the bundled gpt-6-sol was sufficient was incorrect. Its metadata supplies both `multi_agent_version: v2` AND `tool_mode: code_mode_only` (`models-manager/models.json`). `requested_tool_mode` in `core/src/tools/mod.rs` gives model metadata precedence over feature defaults. `build_model_visible_specs` calls `is_hidden_by_code_mode_only` in `core/src/tools/spec_plan.rs`, hiding collaboration.spawn_agent from direct request tools. This scripted conversation uses direct namespaced calls, not code-mode execution. The depth-zero assertion correctly rejects that fixture. Separately, `collab_tools_enabled` requires explicit V2 metadata for descendants, so returning to unmodified gpt-5.5 would restore the depth-one failure.

Use the existing passing `core/tests/suite/multi_agent_tool_descriptions.rs` pattern: `with_model_info_override("gpt-5.5", |model| model.multi_agent_version = Some(MultiAgentVersion::V2))`. The helper pins the bundled model in config.model_catalog (`core/tests/common/test_codex.rs`), retaining the ordinary direct-tool mode and standard SSE transport. The shared fixture now takes TestCodexBuilder instead of a model string, allowing this one test to specify its capabilities explicitly. Every other fixture call retains `.with_model("gpt-5.5")`. `build_agent_shared_config` clones the config including model_catalog; role configuration likewise clones the config, so descendants inherit this supported fixture capability.

No router/model production defaults or product semantics changed. No assertion weakened, timeout increased, retry added, or matcher changed. All three levels still assert actual submitted spawn exposure, successful production spawn output and canonical path identity before waiting for Running. The Interrupted item assertions still require exactly one notice and exactly 838 bytes (<=1000), with both display envelopes checked. This is a test configuration correction, not a depth/path product workaround.

## Trunk integration and scheduler observation

The previous pacing/World State integration and precheck-18 latch teardown fix remain byte-identical. This pass re-read the tool-mode selection, spec exposure, catalog override and child config inheritance call sites to ensure the fixture drives the merged production routing rules. The detailed retained integration and AC maps below remain applicable.

The unrelated `scheduled_checkins_fire_through_production_runtime_under_paused_time` flake has no assertion/trace in the supplied brief, so its precise cause is UNKNOWN. Source inspection found a potential harness timing weakness: after TurnComplete it waits at most 1000 `yield_now` iterations for the warning rather than awaiting an acknowledged lifecycle/warning signal. TurnComplete precedes the idle callback in tasks/mod.rs. This is an observation, not proof that this was the reported failure. No scheduler test or production code changed outside this leaf.

## Retained rev6 implementation and coverage

The following bound proof, integration table and coverage maps describe the retained implementation. Prior rev6 measurements are carried forward; they were not re-executed during this test-only pass. Current-pass changes and commands are recorded separately above and below.

## Rev5 interrupted-item finding

`interrupted-item-token-threshold-unreviewed`: changed only the interrupted fragment's BODY path cap from 256 to 64 bytes. `AgentPath::MODEL_DISPLAY_MAX_BYTES`, display envelopes, new-identity checks, legacy parsing/resume and stored identities are unchanged.

`INTERRUPTED_ITEM_MAX_BYTES = 1000` documents the byte-level BPE property **tokens <= UTF-8 bytes**. A compile-time assertion connects the calculated body bound and the two existing envelope display bounds to that limit. The body's existing debug assertion remains. Empty fragment markers add no text. Plaintext terminal-turn delivery creates exactly one InputText content part through `InterAgentCommunication::new(..., false).to_model_input_item()`.

The exact worst case for the specified item fields is:

- fixed prose: 142 bytes;
- each body path: at most 64 + 14-byte truncation marker = 78 bytes;
- body: 142 + 2 * 78 = **298 bytes**;
- author and recipient: at most 256 + 14 = **270 bytes each**;
- author + recipient + all content text: **838 bytes**, therefore at most **838 byte-level BPE tokens**, below 1000.

This counts the specified model-visible fields, not JSON serialization or metadata. The old 1222-byte / approximately-306-token claim was invalid and is withdrawn. No tokenizer heuristic is used. The prior rev6 Python arithmetic/fixture measurement gave [270, 270, 298] = 838 for BOTH reviewer fixtures; it is a numerical cross-check, not execution of Rust.

Retained unit `inter_agent_interrupted_dense_item_fits_byte_bound` constructs the real terminal-turn formatter and plaintext communication, calls `to_model_input_item`, sums all text and envelope bytes, asserts <=1000 and exactly 838, and checks stored identities are unchanged. Fixtures: legacy `/root/` + `a1` repeated 150, and a new two-level path with `a1`/`b2` each repeated 64, each with `/worker`. Existing byte-exact short-body test is unchanged; the existing long-body test still uses source-valid paths and derives its expected truncation from the cap.

Retained and repaired integration `goal_wait_dense_paths_interrupted_item_bound` drives three V2 spawn levels (agent_max_depth=3), two 128-byte segments and `/worker`, then sets a goal on the depth-two parent, registers durable sleep through the real idle path, interrupts its Running child through Op::Interrupt, and inspects the actual outbound wake request. It asserts exactly one interrupted AgentMessage, <=1000 / exactly 838 bytes, expected display envelopes, Interrupted child state and turn-start marker removal. Setup children are interrupted only after their ordinary parents have ended their turns, then reused to spawn the next level; this serializes the chain without completion mail racing ancestor sampling. Waits are bounded; response counts distinguish matched spawn-output requests from the recorder's rejected-match observations. The wake stays in a long sleep until assertions finish, preventing a later continuation from repeating historical context in the capture; clear + interrupt releases it.

The pre-existing completion-message content bound remains outside this leaf. Its envelope retains the prior display cap.

## Trunk integration

Relocated symbols and read `git log 33a0f766a6..HEAD -- <intersecting paths>`, the current definitions, and candidate-vs-trunk diffs. Trunk changes include 7e4289e21 (pacing), 67789e1ee / 99533cf03 (per-step capabilities / World State), and earlier activation/accounting changes.

| Intersecting path | Review and disposition |
|---|---|
| core/src/session/mod.rs | The delta only permits Interrupted through terminal-turn dispatch. Current per-step tool/context/World State construction remains intact; no history rewrite or capability override added. |
| core/src/tools/handlers/multi_agents_tests.rs | Both V2 task-name boundary tests remain; neighboring trunk changes are retained. They still drive the real handler before thread creation. |
| ext/goal/src/background_wait.rs | The merged empty-work branch is `snapshot.is_empty() && !native_pending`: capable native work goes to the 30/60/120-minute check-ins before pacing. Existing pacing tickets, deadline claims, revision checks and invalidation logic remain. |
| ext/goal/src/extension.rs | Goal-owned removal precedes note_turn_start; current accounting/pacing note_turn_completed and World State contributors are retained. Found a missing newly required GoalExtensionConfig.continuation_pacing field in the native-wait suite installer: now supplied from Feature::GoalContinuationPacing, explicitly enabled in the fixture. |
| ext/goal/src/lib.rs | Pacing/World State module/export changes and G1 native-wait exports coexist. |
| ext/goal/src/runtime.rs | Kept the mechanical resolution: native inspection/insert/recheck first, then evaluate if background gate OR pacing is enabled. ProceedWithoutGate removes the checker; Normal/Ticket/PacingTicket publish it. Wait keeps the marker and arms the existing scheduler. No production adjustment was needed. |
| core/tests/suite/mod.rs | Both goal_continuation_pacing and goal_native_wait remain registered. |

Concrete interaction decisions and new coverage:

1. Background gate disabled, pacing enabled: runtime does not inspect/subscribe native children, removes any own marker and supplies native_pending=false. An empty exec snapshot therefore follows pacing even if a native child is actually Running. `goal_wait_pacing_without_background_gate_has_no_native_marker` drives real spawn -> disable gate -> set goal -> first actual continuation -> production idle, asserts one continuation and streak=1, armed pacing, empty exec snapshot, live Running child and absent marker. It then clears/interrupts for cleanup.
2. Gate and pacing both enabled: native pending + empty exec snapshot uses check-ins, not the pacing floor. The dense-path integration asserts this on the actual registered parent (pacing enabled, empty exec snapshot, marker retained and deadline >60 seconds). `native_pending_supersedes_pacing_with_checkins` first arms a 60-second pacing deadline, then introduces native work, asserts replacement by the 30-minute check-in, refusal of the stale pacing claim, and successful check-in admission.
3. There is no native durable-sleep registration for a pacing-only wait. When native work exists on a capable host, the native check-in path takes precedence. Turn-start and normal invalidation remain authoritative.

World State review: core/tools/waiting_capabilities.rs captures actual router tools; ext/goal/src/extension.rs passes that snapshot to waiting_world_state.rs, which renders steering.rs's capability sentences and diffs them. G1 does not override that snapshot or tool names, and does not render competing guidance. Native blocking-wait guidance remains conditional on tool availability/discovery; native-mail guidance remains conditioned by the existing host/admission capability. Existing `suite::waiting_guidance` is part of the requested hosted core lane; it was not run locally.

## Coverage map and bounds

**9 of 9 AC rows mapped to named tests driving production entry points; 7 of 7 surface rows mapped to tests and killed narrowing mutants.** Hosted precheck 19 passed all four candidate lanes and killed 15 of 15 mutants on the exact current tree. Prior local evidence ran 8 of 8 goal_native_wait tests. This does not claim a dedicated integration test for every AC subcase; the verification bounds below remain explicit.

| AC | Driving tests / production call site | Negative evidence or remaining bound |
|---|---|---|
| AC1 | goal_wait_registers_marker_and_wakes_on_child_completion; GoalRuntimeHandle::continue_if_idle -> inspect_directly_owned_native_children -> try_register_goal_wait_sleep -> scheduler -> model request | Silence then real wake; ignore_native_pending. |
| AC2 | owned_children_inspection_propagates_failed_lookups; LocalAgentRuntime::inspect_owned_child_ids. pending_native_work_is_only_pending_init_and_running; OwnedChildInspection::is_pending_native_work | skip_failed_lookups; unloaded/unknown/current nonpending statuses. Ordinary parent quiet test drives no-goal negative. |
| AC3 | goal_wait_latch_closes_completion_before_registration; continue_if_idle -> insert -> recheck_pending_work_for_goal_wait | Controlled registration/mail latch; insert_after_mail_check. |
| AC4 | register_never_clobbers_foreign_sleep, conditional_remove_only_removes_owned_id, goal_wait_preserves_foreign_sleep_across_register_and_turn_start; lease helpers / ExtensionData::insert_if/remove_if / on_turn_start | Foreign markers retained; insert_clobbers_one_foreign and unconditional_remove. |
| AC5 | goal_wait_removed_on_clear_release_and_resume; GoalService clear/release/restore paths. Native check-in and exhaustion units -> BackgroundWaitState; wake integrations -> on_turn_start | owned_generation_seven_not_removed targets one owned removal; remaining bound: no dedicated full live-child check-in reinsertion/exhausted-late-wake/disable/stop integration. |
| AC6 | goal_wait_registers_marker_and_wakes_on_child_completion; marker insertion in continue_if_idle | No UI events/history/reminder when disabled; single_child_registration_records_history narrows silence for exactly one owned child. Reminder-enabled schedule has no dedicated assertion. |
| AC7 | real goal/ordinary interrupt tests, dense-path integration; Op::Interrupt -> terminal-turn delivery -> queue-only mail -> actual model wake; typed body/unit composition tests | Duplicate/success/body-cap mutants; global Interrupted non-final test retained. New whole-item bound is 838 bytes. |
| AC8 | pending_native_work_is_only_pending_init_and_running; current-state predicate; latch's slow second child; dense test's reused Interrupted children -> new spawn turn | No explicit non-default inherited-settings assertion or second-child-mid-turn integration; scheduler inheritance is unchanged, not newly proved here. |
| AC9 | goal_wait_removed_on_clear_release_and_resume -> GoalService::restore_thread_runtime_after_resume | Does not restore marker. No dedicated full history-resume fixture combining rendered SleepItem and unloaded child. Legacy AgentPath resume/rollout regressions remain separate named tests. |

Source-bound/resume regression coverage retained: spawn_agent_v2_rejects_overlong_task_name / spawn_agent_v2_accepts_task_name_at_cap -> SpawnAgentHandlerV2 -> thread_spawn_source -> AgentPath::join_new; legacy AgentPath try_from/serde tests; resume_agent_preserves_legacy_overlong_path -> resume_agent_from_rollout with ThreadSpawn source (orchestrator test fix retained); get_rollout_history_preserves_legacy_agent_path -> rollout parsing/history; agent_message_envelope_truncates_legacy_paths_for_display -> to_model_input_item. No production source-text inspection gate was added. V1 notification bridge stays outside G1.

## Hosted precheck 19 mutant evidence

All 15 previously apply-clean patches were executed by hosted CI against the unchanged candidate. The table uses actual TRY 3 FAIL records from run 38476605332, mapped to mutant names using each recorded RUN_SHA and its local commit subject. No mutant is inferred killed from lane status alone. The bound mutants have direct unit assertion failures even where their downstream integration also times out after the formatter assertion.

| Mutant | Narrowed gate / admitted counterexample | Named failing tests (hosted) | Result / survivor bound |
|---|---|---|---|
| skip_failed_lookups | Treat failed/unknown lookups as absent while inspecting successful children | `agent::control::tests::owned_children_inspection_propagates_failed_lookups` | Killed; test command exit 100 (expected red); no survivor. |
| insert_after_mail_check | Keep the marker but check pending mail only before insertion | `suite::goal_native_wait::goal_wait_latch_closes_completion_before_registration` | Killed; test command exit 100 (expected red); no survivor. |
| unconditional_remove | Retain removal but admit foreign marker deletion | `conditional_remove_only_removes_owned_id`; `suite::goal_native_wait::goal_wait_preserves_foreign_sleep_across_register_and_turn_start` | Killed; test command exit 100 (expected red); no survivor. |
| insert_clobbers_one_foreign | Allow replacement of the one foreign id clock-wait-1 | `register_never_clobbers_foreign_sleep`; `suite::goal_native_wait::goal_wait_preserves_foreign_sleep_across_register_and_turn_start` | Killed; test command exit 100 (expected red); no survivor. |
| interrupted_claims_success | Keep the interruption notice but falsely label it successful completion | `context::inter_agent_interrupted_message::tests::inter_agent_interrupted_dense_item_fits_byte_bound`; `context::inter_agent_interrupted_message::tests::interrupted_fragment_renders_exact_notice_body`; `context::inter_agent_interrupted_message::tests::interrupted_fragment_truncates_overlong_paths_to_hard_cap`; `session_prefix::tests::interrupted_notice_is_queue_only_without_claiming_success`; `suite::goal_native_wait::goal_wait_dense_paths_interrupted_item_bound`; `suite::goal_native_wait::goal_wait_registered_parent_gets_single_interrupted_notice` | Killed; test command exit 100 (expected red); no survivor. |
| ignore_native_pending | Gate exec work while treating native-only work as empty | `empty_exec_with_native_pending_waits_and_uses_checkins`; `native_pending_exhausts_checkins_then_waits_without_deadline`; `native_pending_supersedes_pacing_with_checkins`; `suite::goal_native_wait::goal_wait_dense_paths_interrupted_item_bound`; `suite::goal_native_wait::goal_wait_preserves_foreign_sleep_across_register_and_turn_start`; `suite::goal_native_wait::goal_wait_registered_parent_gets_single_interrupted_notice`; `suite::goal_native_wait::goal_wait_registers_marker_and_wakes_on_child_completion` | Killed; test command exit 100 (expected red); no survivor. |
| interrupted_notice_delivered_twice | Keep goal-owned delivery but duplicate an Interrupted transition | `suite::goal_native_wait::goal_wait_dense_paths_interrupted_item_bound`; `suite::goal_native_wait::goal_wait_registered_parent_gets_single_interrupted_notice` | Killed; test command exit 100 (expected red); no survivor. |
| interrupted_sender_path_uncapped | Cap task-name text while letting sender text exceed the bound | `context::inter_agent_interrupted_message::tests::inter_agent_interrupted_dense_item_fits_byte_bound`; `context::inter_agent_interrupted_message::tests::interrupted_fragment_truncates_overlong_paths_to_hard_cap`; `suite::goal_native_wait::goal_wait_dense_paths_interrupted_item_bound` | Killed; test command exit 100 (expected red); no survivor. |
| spawn_task_name_length_unchecked | Keep syntax/total-path validation but accept an over-cap segment | `agent_path::tests::agent_path_join_new_rejects_overlong_segment`; `tools::handlers::multi_agents::tests::spawn_agent_v2_rejects_overlong_task_name` | Killed; test command exit 100 (expected red); no survivor. |
| legacy_paths_rejected_by_shared_parser | Preserve new-identity limits but wrongly reject legacy overlong segments | `agent::control::tests::resume_agent_preserves_legacy_overlong_path`; `agent_path::tests::agent_path_accepts_legacy_overlong_segment`; `agent_path::tests::agent_path_display_truncates_overlong_path`; `context::inter_agent_interrupted_message::tests::inter_agent_interrupted_dense_item_fits_byte_bound`; `protocol::tests::agent_message_envelope_truncates_legacy_paths_for_display`; `recorder::tests::get_rollout_history_preserves_legacy_agent_path` | Killed; test command exit 100 (expected red); no survivor. |
| envelope_author_display_uncapped | Keep recipient display cap but expose full author identity | `context::inter_agent_interrupted_message::tests::inter_agent_interrupted_dense_item_fits_byte_bound`; `protocol::tests::agent_message_envelope_truncates_legacy_paths_for_display`; `suite::goal_native_wait::goal_wait_dense_paths_interrupted_item_bound` | Killed; test command exit 100 (expected red); no survivor. |
| legacy_long_path_rejected_by_shared_parser | Keep valid short legacy identities but reject old total paths over 1024 bytes | `agent_path::tests::agent_path_accepts_legacy_path_over_total_cap` | Killed; test command exit 100 (expected red); no survivor. |
| interrupted_body_path_cap_256 | Keep both truncators but increase body-path allowance to 256 bytes | `context::inter_agent_interrupted_message::tests::inter_agent_interrupted_dense_item_fits_byte_bound`; `context::inter_agent_interrupted_message::tests::interrupted_fragment_truncates_overlong_paths_to_hard_cap`; `suite::goal_native_wait::goal_wait_dense_paths_interrupted_item_bound` | Killed; test command exit 100 (expected red); no survivor. |
| owned_generation_seven_not_removed | Remove owned markers except generation 7 | `conditional_remove_only_removes_owned_id` | Killed; test command exit 100 (expected red); no survivor. |
| single_child_registration_records_history | Remain silent except when exactly one owned child is registered | `suite::goal_native_wait::goal_wait_registers_marker_and_wakes_on_child_completion` | Killed; test command exit 100 (expected red); no survivor. |

Hosted filter (all intended killers are selected; CI also includes test(pacing)):
`test(goal_native_wait) | test(native_wait) | test(owned_children) | test(interrupted) | test(native_pending) | test(foreign_sleep) | test(conditional_remove) | test(task_name) | test(agent_path) | test(spawn) | test(legacy) | test(rollout_history) | test(resume_agent)`.

**Hosted lane identity:** precheck 19 ran from relux/ci-next, including codex-protocol and codex-rollout; their named mutant failures were verified. No CI file was changed in this leaf.


## Previous implementation-pass verification (ivmbp local allowance; retained evidence)

All eight goal_native_wait tests passed on the first attempt, including `goal_wait_dense_paths_interrupted_item_bound` (0.807s) and `goal_wait_latch_closes_completion_before_registration` (3.531s). The dense test actually verified direct V2 spawning at depths 0, 1 and 2, a registered parent with a Running child, interruption delivery in the outbound request, exactly one notice and exactly 838 model-visible bytes. This provides behavioral confirmation of the fixture correction above. This pass adds no production behavior or new test name: it repairs the already-required named regression test.

| Command | Real exit | Evidence |
|---|---:|---|
| task-board m set_status(..., status=development) | 0 | Lifecycle began in development. |
| python3 /Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-fix-suite-busy.py --any | 0 | FREE before the first cargo command. |
| bash /Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-target-guard.sh | 0 | Same checkout, cache kept. |
| cargo fmt -- --config imports_granularity=Item | 0 | Formatting after edits. |
| cargo fmt -- --config imports_granularity=Item --check | 0 | Expected stable-channel imports_granularity warnings. |
| RUST_MIN_STACK=33554432 cargo nextest run -p codex-core --test all -E 'test(goal_native_wait)' | 0 | 8 passed, 2285 skipped; build 4m06s, tests 3.544s. |
| Each of 15 standalone git apply --check - calls | 0 each | Patches apply to the candidate; no local behavioral mutant execution. |
| git diff --check | 0 | Whitespace check. |
| Temporary-index git read-tree HEAD / git add -A / git write-tree | 0 each | Candidate tree above; real index unchanged. |
| git diff --stat a318e16991df9427aa922e9de2cbd8f898dba713 <candidate> | 0 | One test file, 18 additions / 15 deletions. |
| rm -r /Users/iv/Developer/IV/codex-target/debug | 0 | Allowance-required post-test trim. |

The nextest command ran directly without tee/pipes. It inherited shared target/jobs/V8 config and exported only NEXTEST_TEST_THREADS=4, INSTA_UPDATE=no, INSTA_WORKSPACE_ROOT=$PWD (codex-rs), plus the brief's RUST_MIN_STACK. No build ran in parallel, no extra helper binary was explicitly built, no second test run, clippy or full suite ran. At that implementation pass hosted evidence was pending. This handoff now reuses precheck 19 Linux lint/small/core/app-server and mutant execution for the exact tree. Dedicated Windows/foreign-exec lanes remain unverified. Local compilation emitted existing unused-import warnings in tools/registry.rs, tests/suite/openai_file_mcp.rs and tests/suite/scenarios.rs; those files are unchanged.

| Resource gate | Before test | During / after | Required |
|---|---:|---:|---|
| Disk available | 128 GiB | 124 GiB after test; 127 GiB after trim | >=50 GiB before |
| CPU idle | 69.26% | Not a continuous gate | >=25% before |
| Memory free | 91% | 91% at every sampled point through completion | >=30% |

The first trim command using rm -rf was rejected before execution by command review (no shell exit code); the safer non-force rm -r command above succeeded. Exploratory missing-directory/glob reads were not validation gates. No real CODEX_HOME was copied or installed codex binary invoked. No checklist item for full tests/build/mutants was newly marked green.

## Surface coverage map

Each row retains a named negative/mutant witness killed in hosted precheck 19. No row is silently treated as fully proved by marker presence or prose; AC subcase bounds above still apply.

| Surface row | Named driving / refusal test | Narrowing witness |
|---|---|---|
| registration and wake | goal_wait_registers_marker_and_wakes_on_child_completion | ignore_native_pending |
| eligibility and inspection errors | owned_children_inspection_propagates_failed_lookups; goal_wait_ordinary_parent_stays_quiet_on_child_interrupt | skip_failed_lookups |
| completion-before-registration race | goal_wait_latch_closes_completion_before_registration | insert_after_mail_check |
| foreign sleep ownership | goal_wait_preserves_foreign_sleep_across_register_and_turn_start | insert_clobbers_one_foreign; unconditional_remove |
| marker lifecycle | goal_wait_removed_on_clear_release_and_resume; conditional_remove_only_removes_owned_id | owned_generation_seven_not_removed |
| side-effect silence | goal_wait_registers_marker_and_wakes_on_child_completion | single_child_registration_records_history |
| child state transitions | goal_wait_registered_parent_gets_single_interrupted_notice; goal_wait_dense_paths_interrupted_item_bound | interrupted_notice_delivered_twice; interrupted_body_path_cap_256 |

Coverage ratio: 9 of 9 AC rows mapped to named production-entry tests; 7 of 7 surface rows mapped. The previous local pass executed 8 of 8 native-wait integration tests; hosted precheck 19 subsequently passed the snapshot lanes including protocol/goal/rollout and killed all mutants. No tests were rerun in this handoff pass. The specific AC subcases without dedicated coverage remain declared in the retained map. Out of contract: the V1 notification bridge is explicitly excluded by the task description (sibling G2); pre-existing completion-message body bounds are excluded by review2's instruction not to change that type. Missing AC subcase coverage is a stated verification bound, not silently classified out of contract.

## Outcome-scoped logbook and routing

2026-10-13: replaced an insufficient bundled-model selection with the existing explicit V2 catalog fixture pattern. Both the original nested-capability constraint and the code-mode direct-tool constraint now hold in an actual passing depth-three integration. All prior production fixes and regression tests remain. The unexpected neighboring scheduler flake is not reproduced or claimed fixed. Notes and this outcome carry these findings; no control-root logbook file was edited.

2026-10-14 handoff logbook: exact-tree comparison succeeded, all four snapshot lane statuses and 15 named mutant failures verified, and the results/outcome evidence refreshed. Reuse of precheck 19 is justified by exact source/test/configuration identity; no new platform claim or missing subcase coverage is inferred. No code change, local build or commit was made. Open test/mutant/lint/build checklist items are checked citing this hosted run. The developer now requests CR revision 6 handoff; reviewer acceptance remains separate.
