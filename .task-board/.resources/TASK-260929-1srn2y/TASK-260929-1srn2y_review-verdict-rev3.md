# Review verdict — TASK-260929-1srn2y, Change Request CR-TASK-260929-1srn2y-3 revision 3

Reviewer run: RUN-260929-e591f8 (claude-fable-5-1, reviewer archetype). Pinned upstream: `33a0f766a647208b471cfbcad889c67fd324ee04`.
Worktree HEAD `8f6517772b` (= CR base OID) is newer than the pin; every code claim below was read from pinned blobs (`git show 33a0f766a6:<path>`, helper `.temp/review-rev3/pin.sh`).
Candidate under review: `TASK-260929-1srn2y_goal-token-burn-final-plan.md` (44720 bytes, SHA-256 `e25bfd07e8e2559570b67e37d98653c3537a1cac34039ffee938796bd6e0f4a0`, matches the republish note). Candidate tree `271521c1cb` equals base `8f6517772b`; `repository_delta = empty`; patch sha256 is the empty-input digest.
Sweep window 00:23–00:35 UTC (inside the 45-minute marker); free hunt 00:35–00:42 UTC. No tracked file edited, no build, no commit.

## 1. Verdict: `accepted`

1. Both round-1 findings are resolved by mechanisms that exist at the pin, not by restated invariants.
2. F1: acceptance is now "included in a sampling request"; delivery rides the existing trigger-turn mailbox with leased runtime entries; both F1 paths are in the race table with named tests and named narrowing mutants (§5.2–5.4 of the candidate).
3. F2: sleep exposure is scoped by a goal-active marker in thread extension data, with an explicit precedence rule that keeps `features.sleep_tool.enabled = false` and `current_time_reminder.sleep_tool` authoritative; every insert/remove hook resolves to the cited goal-extension lines; negative and positive request-level tests are named (§4).
4. The findings-resolution table covers F1, F2 and N1–N10; each claimed resolution exists in the document and the pinned evidence behind it holds (§3 below). N10 is rejected with a correct exactness argument, which the round-1 note explicitly allowed.
5. All eight surface rows held under attack (§4). The free hunt produced bounds, not findings (§6).
6. Nine non-blocking notes are recorded (§5); none leaves a token-burn mechanism in place, breaks existing behaviour, or is an unhandled failure path the plan does not already name as a bound.
7. `repository_delta = empty` is the correct outcome (§2).
8. The candidate is titled "revision 2" and was republished unchanged as CR revision 3 after a workspace-base converge; the digest matches, so it is an annotation, not new work.
9. Route: `accept_cr(TASK-260929-1srn2y, revision=3, evidence=TASK-260929-1srn2y_review-verdict-rev3.md)`. No `commit_ack`; `done` belongs to the integration transaction.
10. Neither this verdict nor the candidate claims proof of absence: concurrency behaviour is proven only by the integration tests the plan names.

## 2. Why an empty repository delta is right

The leaf's acceptance criteria forbid tracked-file edits, commits, pushes and PRs and require one outcome document (brief.md "Constraints"; DoD "No tracked repository file modified"). The candidate tree equals its base (`git diff 8f6517772b 271521c1cb` is empty), and the deliverable — a 44.7 KB self-contained plan under the 45 KB bound — exists and is substantive. The producer changed exactly what the leaf was for: the research document. No repository change was the right outcome.

## 3. Delta since revision 1: F1 / F2 / N1–N10

### F1 `p5-acceptance-without-wake` — resolved

Claimed mechanism (candidate §5.2–5.4) vs. pinned code:

| Claim | Pinned evidence | Result |
|---|---|---|
| Active delivery obeys task-present and mailbox-phase checks | `core/src/session/input_queue.rs:142-160`: `deliver_mailbox_communication_to_current_turn` filters `turn.task.is_some()` and `accepts_mailbox_delivery_for_current_turn()` (`core/src/state/turn.rs:214-216`). The bare-reservation hole of `inject_if_running` (`core/src/session/inject.rs:21-37`) is not on this path. | holds |
| Current drain removes entries; runtime entries must stay leased until sampled | `input_queue.rs:191-228` `drain_mailbox_input_items` drains the deque; `core/src/tasks/mod.rs:478-485` drains into the reserved turn before `start_task`; `tasks/mod.rs:668-697` records unsampled pending input at task end. The candidate names this exact gap and specifies leases + "same receipt, no duplicate history append". | holds |
| Idle wake belongs to `maybe_start_turn_for_pending_work` | `tasks/mod.rs:437-534`, called from task end at `tasks/mod.rs:884` and from `session/handlers.rs:88-91`. Uses `new_turn_with_default_settings`, so no F1a settings-failure drop exists on this path. | holds |
| Trigger mail keeps priority over goal continuation | `turn_input.rs:395-399, 449-454` refuse `start_if_idle` with `PendingTriggerTurn`; `tasks/lifecycle.rs:70-72` suppresses idle contributors. Goal continuation uses `start_turn_if_idle` (`ext/goal/src/runtime.rs:478-486`; `codex_thread.rs:378-395`). | holds |
| Acceptance = included in a sampling request, verified in the actual prompt | `turn.rs:424-470` drains and records pending input before capture; `turn.rs:2539-2552` submits the prompt; `client.rs:2218-2266` selects WS/HTTP. The candidate keeps the exact ack point as an implementation bound (§11 "Transport"). | holds, bound stated |
| Both F1 paths in the race table with tests | §5.4 rows **F1a** (`exec_completion_survives_cleared_idle_reservation`, mutant "retain only task-present input") and **F1b** (`exec_completion_finishing_task_gets_sampling_wake`, mutant "acknowledge on recording"), citing `inject.rs:17-37`, `turn_input.rs:615-623`, `tasks/mod.rs:655-695, 859-885` — all resolve. | holds |
| Not a fake `InterAgentCommunication` | `protocol/src/protocol.rs:805-822` requires author/recipient `AgentPath`; `session/mod.rs:3969-4026` records lineage metadata; `thread_rollout_truncation.rs:68-109` treats `trigger_turn` mail as a fork boundary. A new internal variant avoids all three. | holds |
| Stage sizes re-estimated | §10: 2b 450–650, 2c 350–480 with the ack hook split out. | holds |

Attack run beyond the claim: a user turn arriving while a leased completion is pending. `start_or_steer` (`turn_input.rs:277-370`) has no mailbox gate: it steers into the active turn or starts a `TurnStartKind::User` turn directly, so the lease cannot starve user input. Held.

### F2 `p2-goals-feature-overrides-sleep-config` — resolved

| Claim | Pinned evidence | Result |
|---|---|---|
| Marker read by spec planning without a core→goal dependency | `core/src/tools/spec_plan.rs:135-147` already lifts a thread-extension marker (`WaitForEnvironmentToolConfig`) into `CoreToolPlanContext`; `338-343` pass thread extension data to contributors. `codex-core` already depends on `codex-extension-api`. | holds |
| Precedence rule | Pinned gate `spec_plan.rs:1225-1250`: `SleepTool` hard gate, `AlwaysOn => true`, `ModelDriven` consults `current_time_reminder.sleep_tool` only when `Feature::CurrentTimeReminder` is enabled, else `model_has_clock`. The candidate adds `OR GoalActivity` only to the `model_has_clock` branch and leaves both switches authoritative. | holds |
| Default sessions actually reach the new arm | `features/src/lib.rs:1733-1737`: `CurrentTimeReminder` is `UnderDevelopment`, `default_enabled: false`. `time_reminder.rs:17-38` auto-enables it (with `sleep_tool: true`) only under `persistent_execution_enabled`, which is `reasoning_effort == Persistent` (`features/src/lib.rs:523-525`; `turn_context.rs:957-962`). So on default efforts the marker is the only route for non-clock models — the fix bites where the article's sessions ran. | holds |
| Marker visible on the step after `create_goal` | `turn.rs:461-495`: after the first step `next_step_context` is `None`, so every later step recaptures via `capture_step_context_with_required_mcp_servers` → `built_tools` (`session/mod.rs:3916-3925`). Insert happens before the tool result returns (`ext/goal/src/tool.rs:212-240`). | holds |
| Every hook in the table resolves | create `tool.rs:212-240`; `on_tool_finish` `extension.rs:457-486`; `on_turn_start` `extension.rs:228-281` with early returns at 237-240 (token baseline) and 257-263 (Plan); resume `runtime.rs:401-422` (Active-only branch 412-418, extended to BudgetLimited); external set `runtime.rs:191-255`, `api.rs:76-83`; update `tool.rs:247-304`; clear `runtime.rs:258-268`; stop/config `extension.rs:195-200, 204-221`. | holds |
| Required tests | §4: non-goal/non-clock/default => absent; successful create => next request present; hard-off, reminder-off, failed create => absent; "Assert actual request tools". | holds |

Attack run beyond the claim: could the marker leak sleep into code mode? `SleepHandler::exposure` is `DirectModelOnly` (`core/src/tools/handlers/sleep.rs:74-76`); the candidate states "Sleep remains direct-only in code mode". Held. Residual precedence edge recorded as note 2.

### Notes N1–N10

| Note | Claimed resolution | Check |
|---|---|---|
| N1 | §8: low activity = no observed state-changing outcome, independent of tool count; request counts measured | Accounting keeps booleans only (`ext/goal/src/accounting.rs:40-49, 163-203`); new observations are proposed in goal. Resolved. |
| N2 | §7: durable-sleep `SleepItem` as goal wait registration, side-effect table, V1 bridge | `tasks/mod.rs:422-458`; `handlers.rs:79-93`; `state.rs:98-132` insert is a plain map write; `sleep.rs:102-135` emits items only from the tool; `control.rs:510-518` V1 injects without wake; test floor `core/tests/suite/pending_input.rs:522`. Resolved. |
| N3 | §5.1: output retained by receipt | `process_manager.rs:1137-1143` removes the exited entry on observation. Resolved. |
| N4 | §5.1/§6: `exec_notification release`; one visible warning after three check-ins | Resolved. |
| N5 | §3: `CreateGoalRequest.token_budget` in the field list | `ext/goal/src/tool.rs:52-54, 204, 415-420`; schema already `integer` (`ext/goal/src/spec.rs:35-39`). Resolved. |
| N6 | §9: capability flags from the final captured router, delivered via `TurnContextContributionInput` | Both context paths exist (`session/mod.rs:4264-4290, 4369-4382`); the input struct (`ext/extension-api/src/contributors/context.rs:7-20`) carries stores, so a snapshot can be attached to `turn_store`. Timing correction is right: `continuation_steering_item` renders before sampling (`runtime.rs:474-477`; `steering.rs:53-93`). Resolved. |
| N7 | accepted | — |
| N8 | §5.2: no `session/async_input.rs`; extend `InputQueue` | Resolved. |
| N9 | §5.3: headless exec and descendants cannot arm | `event_processor_with_human_output.rs:309-339`; `event_processor_with_jsonl_output.rs:513-536`; `exec/src/lib.rs:1063` `defer_goal_continuation`. Resolved. |
| N10 | rejected with counterexamples | `1.0000000000000001` rounds to `1.0` as f64; typed parsing is strict today (`handlers/mod.rs:86-92`). The round-1 note allowed either implementation; a stricter choice with evidence is acceptable. Resolved. |

## 4. Surface table results

| # | Row | Result | Attacks run (all through cited public entry points at the pin) |
|---|---|---|---|
| 1 | p5-completion-delivery | **held** | F1a/F1b (above); exit during initial yield (receipt lock rendezvous, §5.1); idle admission declined (`turn_input.rs:395-478` decline paths all `clear_reserved_idle_turn`; mailbox path uses default settings, `tasks/mod.rs:478-534`); terminate/shutdown (`handlers.rs:287-310` sets `shutting_down` before `terminate_all_processes`); subagent ownership (per-session `unified_exec_manager`); burst vs 64 cap (`unified_exec/mod.rs:82`; separate receipt slots); output/denial ordering (`async_watcher.rs:180-189`); headless host (N9); fragment ≤768 B / batch ≤8 (§5.1); user turn during lease (`start_or_steer`, no gate). Note 1 (suspension) and note 4 (`TurnInput` exposure) are bounds. |
| 2 | p4a-goal-gating | **held** | Long-lived process: opt-in `notify_on_exit`, `list_processes` rejected (`process_manager.rs:1824-1840` is live-only and includes servers); check-ins 30/60/120 min, max three per human input, timer ticket bypasses only the work gate; completion between gate check and start: Armed→Queued atomically pending, revision recheck; user input: goal-only gate, `start_or_steer` ungated; queue extension untouched (`ext/queue/src/service.rs:549-565` still runs on idle unless trigger mail is pending — same as today); goal cleared mid-wait: goal timers removed, acknowledged subscription survives; resume: live-generation-only; read failure ≠ empty (§6). |
| 3 | p4c-native-subagents | **held** | V2 completion is queue-only (`completion.rs:96-113`; `control.rs:491-507`); durable sleep wakes on any mailbox mail (`handlers.rs:88-91`; `tasks/mod.rs:451-457`); completion-before-registration closed by "install marker, then call the pending-work scheduler"; V1 bridge (`control.rs:510-518`) routed through queue-only runtime mail; `Interrupted` non-final (`status.rs:26-31`) handled without redefining `is_final`; `list_agents` skips failed lookups (`control.rs:398-416`) replaced by typed `inspect_agent` (`inspection.rs:12-30`); `insert_if` exists (`state.rs:107-123`). Note 7 (V1 visibility timing) is a bound. |
| 4 | p1-integer-arguments | **held** | Field list verified: `SleepArgs.duration_ms: u64` with `JsonSchema::number` (`sleep.rs:32-43`); `ExecCommandArgs` `yield_time_ms: u64`, `timeout_ms: Option<u64>`, `max_output_tokens: Option<usize>` (`unified_exec.rs:28-41`); `WriteStdinArgs.session_id: i32`, `yield_time_ms: u64` (`write_stdin.rs:22-31`); both `WaitArgs.timeout_ms: Option<i64>` (`multi_agents/wait.rs:291-295`, `multi_agents_v2/wait.rs:126-130`); `CreateGoalRequest.token_budget: Option<i64>` (`tool.rs:52-54`). `JsonSchema::integer` exists (`types.rs:128`); `raw_value` enabled (`tools/Cargo.toml:30`). Dynamic passthrough stays `Value` (`dynamic.rs:138`). Exponent/overflow/fraction/duplicate rules stated; mutants named (§12). Note 3 is a wording inaccuracy in the coverage table, not in the fix. |
| 5 | p2-p3-capability-consistency | **held** | F2 (above). P3 text is tool-independent; conditional paragraphs derive from the captured router after exclusions (`router.rs:137-200`); remote catalog replaces bundled entries (`manager.rs:572-603`; `openai_models.rs:897-923`), so guidance rides local descriptions and a developer fragment capped at 3 KiB / 1K tokens; `models.json:1240` is the gpt-5.5 template line; `clock` appears only at `models.json:132, 305, 473`; code mode: sleep `DirectModelOnly`. Note 2 is the explicit-reminder precedence edge. |
| 6 | p4b-pacing-scheduler | **held** | Stale ticket after a fast user turn: tickets bind predecessor turn and admission rechecks `last_started_turn_id` (`turn_input.rs:438-444`, `Superseded`); three-empty blocker preserved (`accounting.rs:216-229`, ancestor `0735c51978` 2026-09-09); two-poll turn now paced (N1); 30 s floor; invalidation set covers steering, goal change/clear, stop, completion, new turn; resume restarts at the floor (disclosed). |
| 7 | article-coverage-and-evidence | **held** | Every article mechanism maps to a row in §11. Spot-checked at the pin: `extension.rs:180-192`, `runtime.rs:425-486`, `accounting.rs:216-229, 527-531` (cached input subtracted), `continuation.md:22-25, 48-56`, `spec_plan.rs:1225-1250`, `handlers/mod.rs:86-92`, `unified_exec.rs:62-67`, `unified_exec/mod.rs:73-82`, `process_manager.rs:1018-1039`, `async_watcher.rs:160-242`, `manager.rs:572-603`, `multi_agents_spec.rs:849-875`, `config_toml.rs:482, 721-725` (`[goals].max_goal_token_budget`, `NonZeroU64`), `service.rs:549-565`. Post-article commits `d47b9a8c00` (2026-09-23) and `4891c4e35f` (2026-09-24) are ancestors of the pin and are output fixes, as stated. Note 3 records one misattributed example. |
| 8 | staging-tests-and-upstream-fit | **held** | Ten stages, each estimated < 800 lines; 2a–2d inactive until 2e (note 6); parsing in `codex-tools`, contracts in `codex-extension-api`, policy in goal — consistent with AGENTS.md "resist adding code to codex-core"; goal depends on core (`ext/goal/Cargo.toml:18`), so combined tests go to `app-server/tests/suite`; goal lib has `test = false` with `ext/goal/tests/{accounting,goal_extension_backend,steering}.rs` at the pin, as the candidate says; vertical test asserts zero requests before the controlled exit **and** one wake with progress after, killing the stalled-runtime mutant; existing floor `pending_input.rs:522-589, 883+` named. |

## 5. Notes (non-blocking)

1. **Suspended runtime mail vs. the trigger gate (p5 / p4a).** §5.2 says failed transport "retain/suspend visibly after exhaustion, never spawn endless wake turns". If a suspended receipt still counts in `has_trigger_turn_mailbox_items`, `start_if_idle` refuses every automatic start (`turn_input.rs:395-399`, before any kind check, so also `handle_recovery` retries and daemon continuation) and `emit_thread_idle_lifecycle_if_idle` skips all idle contributors (`lifecycle.rs:70-72`) until the mail is consumed. User turns are unaffected (`start_or_steer`). Implementation must exclude suspended receipts from the trigger query or define the retry signal; add a test "suspended receipt does not block goal idle continuation".
2. **Explicit reminder feature precedence (p2).** With `features.current_time_reminder = true` set explicitly and `current_time_reminder` absent or `sleep_tool = false`, the candidate's rule (and the pinned gate `spec_plan.rs:1237-1244`) exposes no sleep even for an active goal. This honours configuration, as F2 demanded, but it leaves mechanism B in place for that explicit, under-development configuration. State it in the P2 tests as intended behaviour.
3. **Coverage wording (article-coverage).** §11 says "Stdin yield is now u64, not the old i32 example". At the pin `WriteStdinArgs.session_id` is `i32` and `yield_time_ms` is `u64` (`write_stdin.rs:22-31`); the article's `36429.0, expected i32` error was the `session_id` field, which is still `i32` and is in P1's field list. Harmless to the fix; fix the sentence.
4. **`TurnInput` is public and persisted (p5 stage 2b).** `codex_core::TurnInput` is `Serialize/Deserialize` and used by app-server (`request_processors.rs:349`; `thread_queue_processor.rs:314-337` persists `UserInput` entries). A new internal variant needs those exhaustive uses updated and a serializer that refuses the variant, as the candidate states; list the app-server touch points in stage 2b.
5. **Automatic-admission contributor is new code.** No goal-specific admission hook exists at the pin; `admit_turn_start` (`ext/extension-api/src/turn_admission.rs:11`) is a generic draining permit. The candidate's "goal's automatic-admission contributor" (§6) is stage-2d code, not an existing surface.
6. **Inactive stages land dead code (staging).** 2a–2d are inactive until 2e; upstream lints will need tests exercising the code or `#[cfg_attr(not(test), allow(dead_code))]`, the pattern `router.rs:152, 165` already uses. Already noted in round 1.
7. **V1 bridge visibility (p4c).** Routing V1 child notifications through queue-only mailbox mail moves the `SubagentNotification` from immediate history injection (`control.rs:510-518`) to the next turn's drain for non-goal parents. Intentional per "ordinary parents remain quiet"; cover it with a test so the transcript change is deliberate.
8. **Receipt slot exhaustion (p5 §5.1).** Slots are freed only on inline delivery, release or shutdown, and advertised handles are never evicted, so a Sampled receipt whose retained output the model never releases holds one of the 64 slots for the rest of the thread generation. After 64 notified completions without releases, `notify_on_exit` is refused before launch (the designed `exec_completion_burst_and_capacity` behaviour) and the model is back to polling for that launch. Bounded and explicit, but a long orchestrator session (the article's Session B waited 92 hours) can reach it. Recommend freeing the slot when a Sampled receipt's output is retired by a bounded LRU (keep the handle-unavailable error explicit), or documenting the cap in the tool description; add a test for the 65th subscription after 64 sampled-and-unreleased receipts.
9. **Two automatic turns per completion in goal mode (p5 + p4a).** A completion wakes a trigger-mail turn (trigger `exec_completion`, no continuation steering item); when that turn goes idle the goal's `on_thread_idle` starts a separate continuation (`ext/goal/src/runtime.rs:425-486`). That is 2N turns for N completions, bounded by P4b pacing when the wake turn produced no state change. Not a spin; consider letting stage 2e attach the continuation context to the wake turn when the thread has an active goal, saving one full-context request per completion.

## 6. Free hunt (beyond the table)

- `start_or_steer` has no mailbox gate (`turn_input.rs:277-370`): leased runtime mail can never starve user input. Asset for rows 1–2.
- `apply_persistent_defaults` (`time_reminder.rs:17-38`) turns on the reminder feature with `sleep_tool: true` only for `ReasoningEffort::Persistent` (`features/src/lib.rs:523-525`; `turn_context.rs:957-962`). On default efforts the goal-active marker is the only sleep route for non-clock models, so P2 is load-bearing.
- `TurnInput` public exposure and the missing goal-specific admission hook are recorded as notes 4 and 5.
- Receipt-slot lifetime after Sampled and the 2N-turn cost per completion are recorded as notes 8 and 9.
- No new blocking mechanism found.

## 7. Machine-readable verdict

```verdict-findings
{
  "findings": [],
  "notes": [
    "N1 (p5-completion-delivery / p4a-goal-gating): a suspended runtime receipt that still counts in has_trigger_turn_mailbox_items would block every automatic start_if_idle (turn_input.rs:395-399) and suppress idle contributors (lifecycle.rs:70-72) until consumed; user turns are unaffected (start_or_steer). Implementation must exclude suspended receipts from the trigger query or define the retry signal, with a test.",
    "N2 (p2-p3-capability-consistency): with features.current_time_reminder explicitly true and current_time_reminder absent or sleep_tool=false, the candidate's precedence (matching spec_plan.rs:1237-1244) exposes no sleep for an active goal; honours config as F2 demanded, but should be stated as intended in the P2 tests.",
    "N3 (article-coverage-and-evidence): 'Stdin yield is now u64, not the old i32 example' misattributes the article's 36429.0/expected-i32 error; at the pin write_stdin.session_id is i32 and yield_time_ms is u64 (write_stdin.rs:22-31); session_id is in P1's field list, so the fix is unaffected.",
    "N4 (p5-completion-delivery, stage 2b): codex_core::TurnInput is public, Serialize/Deserialize, and persisted by app-server (request_processors.rs:349; thread_queue_processor.rs:314-337); a new internal variant must update those exhaustive uses and refuse serialization, as stated; list the touch points.",
    "N5 (p4a-goal-gating): no goal-specific automatic-admission hook exists at the pin; admit_turn_start (ext/extension-api/src/turn_admission.rs:11) is a generic draining permit; the candidate's admission contributor is new stage-2d code.",
    "N6 (staging-tests-and-upstream-fit): inactive stages 2a-2d land dead code until 2e; use tests or the cfg_attr(not(test), allow(dead_code)) pattern already present at router.rs:152,165.",
    "N7 (p4c-native-subagents): the V1 bridge moves SubagentNotification from immediate history injection (control.rs:510-518) to next-turn mailbox drain for non-goal parents; intentional, needs a test.",
    "N8 (p5-completion-delivery): Sampled receipts with unreleased retained output hold one of 64 slots for the thread generation (candidate §5.1 frees slots only on inline delivery, release or shutdown); after 64 such receipts notify_on_exit is refused before launch and the model polls for that launch. Bounded and explicit; recommend LRU retirement of sampled output frees the slot, plus a 65th-subscription test.",
    "N9 (p5-completion-delivery / p4a-goal-gating): in goal mode each completion costs two automatic turns (trigger-mail wake, then on_thread_idle continuation via ext/goal/src/runtime.rs:425-486); bounded by P4b pacing, not a spin; stage 2e could attach the continuation context to the wake turn when a goal is active."
  ],
  "surface_results": [
    {
      "row": "p5-completion-delivery",
      "result": "held"
    },
    {
      "row": "p4a-goal-gating",
      "result": "held"
    },
    {
      "row": "p4c-native-subagents",
      "result": "held"
    },
    {
      "row": "p1-integer-arguments",
      "result": "held"
    },
    {
      "row": "p2-p3-capability-consistency",
      "result": "held"
    },
    {
      "row": "p4b-pacing-scheduler",
      "result": "held"
    },
    {
      "row": "article-coverage-and-evidence",
      "result": "held"
    },
    {
      "row": "staging-tests-and-upstream-fit",
      "result": "held"
    }
  ],
  "free_hunt": []
}
```

## 8. Acceptance-criteria check for the leaf

- Q1–Q10 answered: Q1 §11; Q2 §3; Q3 §4; Q4 §6; Q5 §5; Q6 §8; Q7 §7; Q8–Q9 §9; Q10 §10. Open points are stated bounds (§11), not new research leaves.
- Per-patch verdicts: P1 modify, P2 modify, P3 modify, P4a modify, P4b modify, P4c added, P5 modify, P6 agree with deferral.
- Final series table with order, files, tests, size, risk: §10 (ten stages, each < 800 lines).
- Rev2 requirements: findings-resolution table (§2), P5 on the trigger-turn mailbox with both F1 paths tested (§5), P2 goal-active marker with hooks, precedence and tests (§4), one self-contained document under 45 KB (44720 bytes).
- Reviewer archetype: no `commit_ack` supplied; `done` is left to the integration transaction.

## 9. Evidence log

Pinned blob OIDs of every file read for this verdict (`git rev-parse 33a0f766a6:<path>`):

- `codex-rs/core/src/session/input_queue.rs` 2212dc09f663e874f5bfb03e2869feb321b5ea20
- `codex-rs/core/src/session/turn_input.rs` d9a5c6a30abb5a2410828ba89cfacc2bdaa65332
- `codex-rs/core/src/session/inject.rs` ea999374a39c488a7a619962e39d1702f00cb094
- `codex-rs/core/src/session/turn.rs` b88b343c1df7e8c7bd0a3b9d34b747b0b03f4576
- `codex-rs/core/src/session/mod.rs` 902d18377cb93e6bc378ebac9fc9b740cce65845
- `codex-rs/core/src/session/handlers.rs` 94c47023ead7ab1100ade55d75bb26f30d3c0c05
- `codex-rs/core/src/session/time_reminder.rs` 92c60389fe6532343da42b25f878d3845a4b558b
- `codex-rs/core/src/session/turn_context.rs` 0d7b59d77ea6089bf4c157176a923a8069c1da62
- `codex-rs/core/src/state/turn.rs` 334372019fb52e9e8ac22a9fe8622a223149c5d5
- `codex-rs/core/src/tasks/mod.rs` 323c8015a5a947845a24e643b4937ebdaf09b31e
- `codex-rs/core/src/tasks/lifecycle.rs` 27835be8fc3751d440d7d336c338b04a460320bc
- `codex-rs/core/src/client.rs` f5ac495337fd8f29c08b0be8d5b75ba32185d7d2
- `codex-rs/core/src/codex_thread.rs` 316af05c0881cafa45a7ee862bb7c2f5a132cf9a
- `codex-rs/core/src/tools/spec_plan.rs` bb1474feb52820424f14089c0b073df7b9d650a1
- `codex-rs/core/src/tools/router.rs` d9f1f63eed9cd28b40ac69820e82d6f796ad1dea
- `codex-rs/core/src/tools/handlers/mod.rs` 2d0b6177e10efec4f4352acf9875b4d9e91382b2
- `codex-rs/core/src/tools/handlers/sleep.rs` 45db1a3b5795c7bc89701b6c4af670a2dc2c0dc2
- `codex-rs/core/src/tools/handlers/unified_exec.rs` 9f9f8a8cf1ea9fbd01f01813e9dcf1ccca6ab1e1
- `codex-rs/core/src/tools/handlers/unified_exec/write_stdin.rs` 5f9d9cf8ca424a177d3f79b773a9f4838d10e8ed
- `codex-rs/core/src/tools/handlers/dynamic.rs` f2b7860d06385301ebefa9bdd70eb0a43a8639ad
- `codex-rs/core/src/tools/handlers/multi_agents/wait.rs` 630454042ad1063ac016302774a88756916d7180
- `codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs` d2f92feb8d011bb468dcc1f81b0efc20e756179e
- `codex-rs/core/src/tools/handlers/multi_agents_spec.rs` 52c24f8f0611e3015f3ba907c8861c6169a8abd6
- `codex-rs/core/src/unified_exec/mod.rs` 3645306c27c8157cafe42cde651dcf15ab66607f
- `codex-rs/core/src/unified_exec/async_watcher.rs` f30c750cbb38afef5a7117c41e5e9c26aca0add9
- `codex-rs/core/src/unified_exec/process_manager.rs` 3dc3e97d91245b3326637817570b06ead902db96
- `codex-rs/core/src/agent/control.rs` 565d36519aa5be4fbd9fc4a6d3fc2336f2856a05
- `codex-rs/core/src/agent/control/completion.rs` 0f09257a978c94f0bdd90e91fe3e4c28d0303afc
- `codex-rs/core/src/agent/control/inspection.rs` fdf3cdce35ce822bb24f24c46280b1795eea73f8
- `codex-rs/core/src/agent/control/execution.rs` 084f7c0054e4442c22cbb456f17fabbcf9fc6279
- `codex-rs/core/src/agent/status.rs` 0ec7e96d4be9ab89bc4068451044be40318c2f0a
- `codex-rs/core/src/hook_runtime.rs` 30c4162ffc06307dc0a73189cb4b7944b6a949c2
- `codex-rs/core/src/context_manager/history.rs` 2475e685ea12ff4f3d32cb00a1cfd877969f5673
- `codex-rs/core/src/thread_rollout_truncation.rs` 16f67a47b852c9dd39f295866333b6a23b83401c
- `codex-rs/core/src/thread_manager.rs` 6a0c7d2cb0fe2299b9e094f73bf9f9b542000e1f
- `codex-rs/core/src/config/mod.rs` 60c6f65353453265ad413ce6f4d093b17cbdc625
- `codex-rs/core/tests/suite/pending_input.rs` 0df8b4a20b7ab94625f10bb3635ce7e30e96234f
- `codex-rs/features/src/lib.rs` 4b05bdb5bee3345f7aa3e9e20c542adb3fc5aaae
- `codex-rs/config/src/config_toml.rs` 9915de6b40cb46e207a363af4c7abd02e0c46d43
- `codex-rs/protocol/src/protocol.rs` abc4e90847636bfe51e6275ede528a13616c8573
- `codex-rs/protocol/src/openai_models.rs` cb0c9f0a94693359dcfa3c004e024579d33cf08f
- `codex-rs/models-manager/src/manager.rs` 7b4d613be409bdd5cd60b7509c6e6c9c06dc41ae
- `codex-rs/models-manager/models.json` 29942914e84e9a7ef9c705272ccd4bd3929548fd
- `codex-rs/tools/src/json_schema/types.rs` 0792816fd31c242d3000adcea6cbe8a3ed8f7874
- `codex-rs/tools/Cargo.toml` f47815537ffdd381161130ac0c26bc8d1fd30868
- `codex-rs/ext/extension-api/src/state.rs` 7d6e79dc5872968147c1aba00b4aa08d1efdae4c
- `codex-rs/ext/extension-api/src/contributors/context.rs` 78dd8ae7b5bfe9dee1f292a806d0d485fd6ce15f
- `codex-rs/ext/extension-api/src/turn_admission.rs` 9d5de89fc7fc77045dd39725a1bbc38a5847e7a9
- `codex-rs/ext/items/src/sleep.rs` 4cca51e16e27619ceb459e4b85e6519f480ea069
- `codex-rs/ext/goal/Cargo.toml` 3939da1ab7f1c2e13c1263190abf91b17108fb7c
- `codex-rs/ext/goal/src/tool.rs` ff504060eee9426a38f9095ad5674e90fd6d5b9e
- `codex-rs/ext/goal/src/extension.rs` 1ec9ee6378602988c2bf747433646c7cb32b86de
- `codex-rs/ext/goal/src/runtime.rs` 7d826ac2381df8b0dafa39ef66959b22527a4604
- `codex-rs/ext/goal/src/api.rs` b414e9ccfb04eaefa074059e6e1e2c3a71ed46b7
- `codex-rs/ext/goal/src/accounting.rs` b2a89ce2ed3029c807cfdbed90e11be709a307c9
- `codex-rs/ext/goal/src/steering.rs` 4e623e69b6bbe7e0d84afcee8d5d85cec9a4bfff
- `codex-rs/ext/goal/src/spec.rs` 6d1d7a9230083a554bda372341337108a546c90a
- `codex-rs/ext/goal/templates/goals/continuation.md` 0e0a273389d62226c31e1d28b1bd8dbae0ccbda8
- `codex-rs/ext/queue/src/service.rs` 06aeb63b4cacccf562ee91897bafbcf962bd978c
- `codex-rs/app-server/src/request_processors/thread_processor.rs` 289cb63953662eb5fba00222ec49432dd976b944
- `codex-rs/app-server/src/request_processors/thread_queue_processor.rs` ea6ec7ddab9148b81852644217fe394cb4ebc3e5
- `codex-rs/exec/src/lib.rs` 0bfa07bd5587f6913b21d137874430a982824c15
- `codex-rs/exec/src/event_processor_with_human_output.rs` 222bc485ab425ea4ad0bad8107cc5e2303bd20d9
- `codex-rs/exec/src/event_processor_with_jsonl_output.rs` 73e0c9d911c82aae67c44e6b1a4ce54c7092b6be

Commits checked as ancestors of the pin: 0735c51978 (2026-09-09, #44320), d47b9a8c00 (2026-09-23, #47665), 4891c4e35f (2026-09-24, #47712).

Method: static reading of pinned blobs only; no build or test run (the brief allows but does not require one, and no finding needed a build to settle). All commands are `git show 33a0f766a6:<path> | sed -n`, `git grep <pattern> 33a0f766a6 -- codex-rs`, and `git merge-base --is-ancestor`.

## 10. Logbook entries (outcome-scoped; no control-root edit)

- `start_or_steer` (turn_input.rs:277-370) has no trigger-mail gate at 33a0f766a6; only `start_if_idle` callers (goal, recovery, daemon continuation) yield to pending trigger mail. Any mailbox-based wake design cannot starve user input.
- `Feature::CurrentTimeReminder` is UnderDevelopment/off by default; its sleep_tool=true auto-default applies only at ReasoningEffort::Persistent (time_reminder.rs:17-38; features/src/lib.rs:523-525). On default efforts the goal-active marker is the only sleep route for non-clock models.
- The article's `36429.0, expected i32` error is `write_stdin.session_id`, still i32 at the pin; the plan covers it through the P1 field list.
