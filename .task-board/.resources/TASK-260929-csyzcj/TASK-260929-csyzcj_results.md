# TASK-260929-csyzcj — goal-owned-durable-sleep-lease: precheck 18 request

Current authoritative outcome. Candidate UNCOMMITTED; no handoff. Hosted CI must validate the changed tree before checklist acceptance. No local Rust build, clippy, test binary, or mutant ran (R194/R223).

Candidate tree: `a318e16991df9427aa922e9de2cbd8f898dba713`. Checkpoint: `99533cf034007f30e2c49916bcba411d7ffa282d`.
This pass changes only `codex-rs/core/tests/suite/goal_native_wait.rs` relative to precheck 17 snapshot `5adf190a`. All production code, including the whole-item cap, routing/legacy resume fixes, pacing integration and the orchestrator's `config: &*parent.config().await` correction, is unchanged.

## Precheck 17 findings and root causes

Hosted run 38328884035: lint, small and app-server passed; core failed the dense-path test on all three attempts and the latch passed only on its second attempt. All 15 mutants were reported killed, but the candidate was red, so those kills are not accepted evidence for this tree. The two unrelated flaky suites named in the brief are outside this rework.

### Dense-path timeout: test requested nested spawning from a model without native V2 support

Code evidence:

- `core/tests/common/test_codex.rs:951` pins the generic fixture to gpt-5.5.
- `models-manager/models.json:1172-1189` declares gpt-5.5 with `multi_agent_version: null`; gpt-6-sol at lines 178-195 declares `v2`.
- `core/src/tools/spec_plan.rs:687-697`, `collab_tools_enabled`, permits V2 collaboration for a root without an AgentPath, but requires `model_info.multi_agent_version == Some(V2)` for a spawned child.
- `core/src/tools/handlers/multi_agents_v2/spawn.rs:131-153` constructs each child's path from the parent's source; names are 128, 128 and 6 bytes and resulting paths are 134, 263 and 270 bytes, all within `join_new`'s 128/1024 creation caps. V2 routing has no depth-limit rejection at these depths.

Thus level zero can spawn, but when the interrupted depth-one child is reused as a parent, the scripted collaboration.spawn_agent call is unavailable. The old idle mock accepted any function-call output, including the tool error, then the helper waited for a child that did not exist. This is a fixture capability error, not a valid supported depth-three spawn being refused. The earlier failure log did not capture depth/status; the location of the failure follows from this code path, not an invented runtime trace.

Fix: parameterize the shared fixture's model and select the actual bundled gpt-6-sol only for the dense-path test. All other tests explicitly keep their previous gpt-5.5 model. No production router rule or model metadata is changed. At every depth, the test now asserts spawn_agent is in the actual submitted request tools, parses the real spawn output, and compares its canonical task_name to the expected child identity before waiting for Running. A status timeout now prints the depth and last directly-owned child inspections. The 10-second timeout is unchanged; no retries or sleeps were added.

### Latch flake: TurnComplete is earlier than teardown, so two idle passes competed for one release

Code evidence:

- `core/src/tasks/mod.rs:1035-1065` sends TurnComplete, then clears the active turn, runs idle contributors, flushes, and finally checks pending mail. Receiving TurnComplete is not a teardown barrier.
- `ext/goal/src/api.rs`, `GoalService::set_thread_goal`, commits the goal before `GoalSetOutcome::apply_runtime_effects`; `runtime.rs:438-440` later calls continue_if_idle from those effects.
- `ext/goal/src/runtime.rs:689-753` acquires the goal permit, reads committed state and reaches the test registration gate. `native_wait.rs` uses Notify::notify_one for a single release.

A permitted interleaving: the initial turn's still-running idle callback observes the newly committed goal and reaches the gate first; the explicit set's continuation is waiting for its permit. The test releases the first callback, then the set reaches the retained gate a second time. The test awaits the set before sending its second release, causing exactly the reported 'goal set hung after ... released' failure. This pre-existing harness race is independent of the pacing match arms; pacing is evaluated only after the gate. Enabling pacing changes timing but does not create this gate ownership rule.

Fix: use the existing `TestWakeLeaseGate` teardown signal (already used by exec_completion tests), armed before the initial parent turn. This scenario has no exec runtime leases, so it observes teardown without pausing any wake. Await `wait_scheduler_done` with a bounded 10-second timeout before setting the goal, then disarm. This proves the original idle callback AND its subsequent pending-mail scheduler pass returned before registration testing starts. The latter also prevents an old scheduler pass from masking the wrong-order mutant. No new production test hook, timer or scheduling rule is added.

The original registration latch still pauses after inspection and releases only after completion mail is enqueued. The retained gate still prevents post-wake idle reinsertion from racing the removal assertion. A new immediate mailbox-empty assertion after the set returns makes `insert_after_mail_check` fail directly: the mutant leaves the fast child's completion queued. Real wake/model-request and marker-removal assertions remain. No timeout was raised and no retry was added.

## Trunk integration recheck for precheck 18

Read current `collab_tools_enabled`, model catalog, native spawn/path creation, ThreadManager direct-child edges, task teardown and mailbox scheduler, goal external-set / idle / permit-sharing flow, and the prior trunk integration table below. The current failures are test configuration/synchronization errors. No product change to the merged native-pending/pacing behavior is justified. Native pending with empty exec work still uses check-ins; disabled background gate with pacing still does not register a native marker. Waiting-guidance and world-state code is untouched.

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

**9 of 9 AC rows have named tests driving production entry points; 7 of 7 surface rows have tests and a proposed narrowing-mutant witness. Current-tree Rust execution: 0 of 9 AC rows, 0 of 15 mutants executed locally.** Precheck 15 ran the previous tree (12/12 mutants killed), and is historical evidence only. New-tree green coverage and kills are unknown until precheck 18. A row being mapped does not imply all its subcases have independent integration coverage.

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

## Mutants submitted for precheck 18

All patches are rebased onto the current tree, and individually `git apply --check` clean. The prior rev6 native-pending patch already includes context for the new pacing branch; no patch changes were needed this pass. All 12 earlier mutations remain, plus the requested bound regression and two witnesses for the review table's lifecycle/silence rows. None is claimed killed on this tree.

| Mutant | Intended assertion killer / surface |
|---|---|
| skip_failed_lookups | owned_children_inspection_propagates_failed_lookups; eligibility/errors |
| insert_after_mail_check | goal_wait_latch_closes_completion_before_registration; registration race |
| unconditional_remove | conditional_remove_only_removes_owned_id + goal_wait_preserves_foreign_sleep_across_register_and_turn_start; foreign ownership |
| insert_clobbers_one_foreign | register_never_clobbers_foreign_sleep + foreign-sleep integration; foreign ownership |
| interrupted_claims_success | goal_wait_registered_parent_gets_single_interrupted_notice / interrupted_fragment_renders_exact_notice_body; transitions |
| ignore_native_pending | native_pending_supersedes_pacing_with_checkins / empty_exec_with_native_pending_waits_and_uses_checkins / goal_wait_registers_marker_and_wakes_on_child_completion; registration/wake |
| interrupted_notice_delivered_twice | goal_wait_registered_parent_gets_single_interrupted_notice; transitions |
| interrupted_sender_path_uncapped | interrupted_fragment_truncates_overlong_paths_to_hard_cap; transitions/bounds |
| spawn_task_name_length_unchecked | spawn_agent_v2_rejects_overlong_task_name / agent_path_join_new_rejects_overlong_segment; new identity refusal |
| legacy_paths_rejected_by_shared_parser | agent_path_accepts_legacy_overlong_segment / resume_agent_preserves_legacy_overlong_path / get_rollout_history_preserves_legacy_agent_path; legacy compatibility |
| envelope_author_display_uncapped | agent_message_envelope_truncates_legacy_paths_for_display; envelope bound |
| legacy_long_path_rejected_by_shared_parser | agent_path_accepts_legacy_path_over_total_cap; legacy compatibility |
| interrupted_body_path_cap_256 | inter_agent_interrupted_dense_item_fits_byte_bound; new regression. Widens the actual truncator to 256 using a local constant, retaining the declared 64-byte bound and compile-time assertion. This deliberately tests implementation drift rather than relying on a compile failure; the body debug assertion / behavioral bound test must reject it. The dense integration exercises the same formatter. |
| owned_generation_seven_not_removed | conditional_remove_only_removes_owned_id; lifecycle removal. Keeps removal for other owned generations and refusal of foreign markers, but wrongly retains generation 7. |
| single_child_registration_records_history | goal_wait_registers_marker_and_wakes_on_child_completion; silence. Keeps ordinary registration, but injects an assistant history item only when exactly one child is owned; the request's no-goal-wait-text assertion must reject it. |

Suggested hosted filter (all intended killers are selected):
`test(goal_native_wait) | test(native_wait) | test(owned_children) | test(interrupted) | test(native_pending) | test(foreign_sleep) | test(conditional_remove) | test(task_name) | test(agent_path) | test(spawn) | test(legacy) | test(rollout_history) | test(resume_agent)`.

**Hosted lane requirement:** include codex-protocol and codex-rollout tests, as precheck 15's relux/ci-next workflow did. The checked-out trunk workflow's small command does not list them; dispatch the campaign workflow that includes them. Otherwise legacy/parser/envelope mutant results are unverified. No CI file was changed in this leaf.

## Commands and verification for this pass

- Lifecycle start: `task-board m 'set_status(TASK-260929-csyzcj, status=development)'`: exit 0.
- `/Users/administrator/.cargo/bin/cargo fmt -- --config imports_granularity=Item`: exit 0 (three passes while refining the test); stable-channel imports_granularity warnings are expected.
- `/Users/administrator/.cargo/bin/cargo fmt -- --config imports_granularity=Item --check`: exit 0; log attached as TASK-260929-csyzcj_fmt-check-precheck18.log.
- Each of the 15 existing JSON patches: standalone `git apply --check -`, exit 0. They modify production files unchanged by this pass, so the patches are unchanged. No mutant was executed locally; all named killers remain in the supplied hosted filter.
- `git diff --check`: exit 0.
- Temporary-index `git read-tree HEAD`, `git add -A`, `git write-tree`: exit 0 each. Real index untouched; temporary index removed in finally.
- Comparison to precheck 17: `git diff --name-only 5adf190a a318e16991df9427aa922e9de2cbd8f898dba713` exit 0; only goal_native_wait.rs (74 insertions, 17 deletions).

No local Rust builds, checks, clippy, tests, nextest, helper builds or full suite. Hosted precheck 18 must run all lanes (including protocol/rollout) and all 15 mutants against this tree. Current-tree executed coverage is **0 of 9 AC rows; 0 of 15 mutants**. The map remains **9 of 9 AC rows mapped (AC5/8/9 have the stated integration bounds), 7 of 7 surface rows mapped to tests and narrowing mutants**. Mapped coverage is not passing evidence. Precheck 17's green lint/small/app-server lanes and earlier green prechecks are accepted only as historical evidence, not certification of this revision. No passing-test/build/mutant checklist item is newly checked.

Exploratory file searches of guessed paths returned 1/2 and were corrected; they were not validation gates. No temporary directory was created; transient format logs and the temporary Git index are removed after evidence attachment. No real CODEX_HOME was copied, no installed codex binary ran, and no background process is left at turn end. No commit, branch operation or handoff.

## Logbook / routing

2026-10-13: root-only V2 feature exposure is insufficient for nested gpt-5.5 spawns; choose an actual V2-capable model and assert the submitted tools plus the real spawn result. TurnComplete precedes idle and teardown scheduling; synchronize the latch with the existing teardown scheduler signal to keep exactly one registration attempt under test. Both findings are recorded in this outcome and the task note. Previous bounds, source-identity/resume decisions, and the 838-byte whole-item proof remain unchanged.

Next action: **HOSTED-PRECHECK-REQUESTED: precheck 18**. Do not hand off before hosted evidence.
