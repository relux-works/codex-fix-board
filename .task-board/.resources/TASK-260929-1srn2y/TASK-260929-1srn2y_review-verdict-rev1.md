# Review verdict — TASK-260929-1srn2y, Change Request CR-TASK-260929-1srn2y-1 revision 1

Reviewer run: RUN-260928-a4ac16 (claude, reviewer archetype). Pinned upstream: `33a0f766a647208b471cfbcad889c67fd324ee04`.
Worktree HEAD `88e9a8329d` is newer than the pin; every code claim below was read from pinned blobs (`git show 33a0f766a6:<path>`).
Candidate under review: `TASK-260929-1srn2y_goal-token-burn-astra-review.md` (39769 bytes) + `research-rev2.md` §5 + orchestrator evidence note.
Sweep window 03:08–03:22 local (well inside the 60-minute marker); free hunt folded into the same window. No tracked file edited, no build, no commit.

## 1. Verdict: `changes_requested`

1. The combined plan is directionally right: opt-in completion subscriptions, a goal-owned wait gate, typed integer decoding, and pacing remove the article's dispatcher spin. Both documents agree on that core and the agreement survives attack.
2. Two mechanisms do not survive contact with the pinned code and block acceptance.
3. F1 (robustness): P5 defines completion ownership as "turn acceptance", but at the pin an injection accepted into a bare idle reservation is discarded, and one accepted into a finishing task is recorded to history without any wake. The plan's race table does not contain either path.
4. F2 (regression): rev2's P2 rule "register sleep when Feature::Goals is enabled" is true in every default session, silently overrides the explicit `current_time_reminder.sleep_tool = false` opt-out, and turns the goal-scoped patch into the article's "weaker alternative". Its stated justification (a first-turn gap) does not hold: tools are rebuilt per sampling step and spec planning already reads thread extension data.
5. Both findings have cheap corrections that also shrink the series: reuse the existing trigger-turn mailbox for P5 delivery, and use a goal-active marker in thread extension data for P2.
6. Six rows held; two rows are broken. Non-blocking notes cover the P4b two-poll blind spot, an unspecified P4c registration API for which an existing durable-sleep primitive is the simpler answer, and the goal `token_budget` float gap.
7. Citations in the candidate spot-check clean (37 ranges verified, listed in §7). The `models.json:1240` citation resolves: the file is pretty-printed at the pin.
8. `repository_delta = empty` is the correct outcome for this leaf (see §2). Rework is to the research document, not to the repository.
9. Route: `analysis` with this artifact as evidence. Next revision must fold F1/F2 corrections into the final patch series table and the P5/P2 designs.
10. Neither verdict claims proof of absence; concurrency behaviour still needs the integration tests the candidate lists.

## 2. Why an empty repository delta is right

The leaf is a read-only research task: its acceptance criteria forbid tracked-file edits, commits, pushes and PRs, and require one outcome document. The candidate tree equals its base and the patch has zero paths, which is exactly what the brief demanded. The deliverable (the outcome document) exists and is substantive. The rejection below is about the content of that document, not about the absence of code.

## 3. Surface table results

| # | Row | Result | Detail |
|---|---|---|---|
| 1 | p5-completion-delivery | **broken** | F1. Attacks run: exit during initial yield (held: receipt state machine covers it), idle admission declined (held: retained inbox), reservation whose settings fail (broken: F1 path a), competing turn ending (broken: F1 path b), terminate/shutdown (held: `shutting_down` set before `terminate_all_processes`, handlers.rs:287-310), subagent ownership (held: delivery to originating generation), burst vs 64 cap (held: receipt slot reservation), output/denial ordering (held: watcher waits for drain and monitor, async_watcher.rs:180-189), headless exec (held: candidate gates it), fragment bound (held, note N3). |
| 2 | p4a-goal-gating | held | Long-lived process: opt-in `notify_on_exit` + 30/60/120-minute check-ins capped at three. Non-opted process: falls to P4b pacing. Completion between gate check and start: armed work counts as pending until accepted. User input: gate is goal-only, user admission untouched. Goal cleared mid-wait: subscription cancelled, completion still wakes as a non-goal turn. Resume: processes die at shutdown (handlers.rs:307-310), stale subscriptions discarded. Read failure: candidate states unknown ≠ no pending work. Notes N4, N9. |
| 3 | p4c-native-subagents | held | Upstream fact reproduced: child completion is queue-only (`trigger_turn=false`, completion.rs:96-106) and an idle parent is not started (tasks/mod.rs:451-457). The candidate accounts for it. Registration API is unspecified; a simpler existing primitive exists (note N2). Not a reproduced defect of the plan. |
| 4 | p1-integer-arguments | held | Dynamic/MCP/extension passthrough untouched by the field-level adapter (dynamic.rs:138 stays `Value`). Exponent/overflow/non-integral handled by the adapter contract. Code-mode path uses the same `parse_arguments`. `session_id: i32` (write_stdin.rs:25) is in the field list. Schema `integer` exists (types.rs:128). Gap: goal `token_budget` (note N5). |
| 5 | p2-p3-capability-consistency | **broken** | F2. P3 text is safe (hedged) but can be made exact (note N6). Headless exec and remote-catalog attacks held (candidate routes guidance through local tool descriptions and a developer contributor; prompt.rs:8-13). |
| 6 | p4b-pacing-scheduler | held | Stale timer after a fast user turn: generation tickets + predecessor check (turn_input.rs:438-443). Steering/goal update/completion pre-emption: listed invalidation set. Existing 3-empty blocker preserved (accounting.rs:215-229). Two-poll reset and in-turn polling: disclosed blind spot, quantified in note N1. |
| 7 | article-coverage-and-evidence | held | Every article mechanism maps to a row in the candidate table; in-turn polling, cached-input exclusion (accounting.rs:527-531), remote catalog override (manager.rs:572-603), queue extension idle dispatch (service.rs:549-565) all present. Citation spot-check in §7. |
| 8 | staging-tests-and-upstream-fit | held | Each stage ≤ 800 lines; 2a/2b are inactive until 2c (acceptable but noted). Goal+exec tests placed in `app-server/tests/suite` because the goal crate depends on core (ext/goal/Cargo.toml:18). Stalled-model false pass addressed ("zero requests before controlled exit"). New inbox duplicates the mailbox (note N8, fixed by F1's correction). |

## 4. Findings

Blocking findings, most severe first. Fields follow the reviewer contract; the machine-readable block in §5 is authoritative.

### F1 `p5-acceptance-without-wake` — row p5-completion-delivery — severity `robustness` — repeat-of `none`

Invariant: every armed completion reaches the owning live thread generation exactly once, or is explicitly cancelled; no loss when idle admission declines.

Mechanism (design statement): the candidate transfers ownership on "actual turn acceptance" (Q5 items 2–4, race table rows "Concurrent turn start/end" and "Admission refused") and tests "every decline path in turn_input.rs:395-478". At the pin, an injection that `Session::inject_if_running` reports as accepted can still end without a wake through two production paths that the race table omits:

- (a) `inject_if_running` accepts into any `active_turn`, including a bare idle reservation whose `task` is `None` (inject.rs:21-37; contrast `inject_hook_context_if_running`, inject.rs:49-55, which refuses that case). If the reservation's settings then fail, `clear_reserved_idle_turn` drops the reservation and its `turn_state` (turn_input.rs:615-624).
- (b) An injection into a running task that finishes before the next sampling request is drained by `take_pending_input_for_turn_state` and recorded to history by `run_hooks_and_record_inputs(.., PersistContext::Standard)` (tasks/mod.rs:668-697). The only post-turn wake, `maybe_start_turn_for_pending_work` (tasks/mod.rs:884), starts a turn solely for mailbox items with `trigger_turn` or an outstanding durable sleep (tasks/mod.rs:451-457). A `ResponseItem` completion is not a mailbox item.

Consequence: in a goal session the P4a gate recovers (b) only if "delivered" is defined as "sampled", which the candidate does not define; in a non-goal session (the fork's primary case and the article's "one message arrives" model) the completion sits in history until the user types. The plan's stated invariant ("retain until accepted") is therefore satisfiable by an implementation that still loses the wake.

Correction: define acceptance as "included in a sampling request", and deliver through the existing trigger-turn mailbox (a new `TurnInput` variant or a runtime-authored communication with `trigger_turn = true`) so that `maybe_start_turn_for_pending_work` owns the idle wake, `has_trigger_turn_mailbox_items` gives the completion priority over a goal continuation (turn_input.rs:395-399, 451-456; lifecycle.rs:70-72), and the `queued_inter_agent_mail_*` / `injected_response_item_reopens_turn_after_final_answer` tests (pending_input.rs:883-1057) become the regression floor. This removes most of stage 2b.

### F2 `p2-goals-feature-overrides-sleep-config` — row p2-p3-capability-consistency — severity `regression` — repeat-of `none`

Invariant (row 5, attack families "SleepTool explicitly disabled" and "first user turn that creates the goal"): sleep exposure honours explicit configuration and does not silently widen beyond goal work.

Mechanism: rev2 §5 adopts "Register sleep when Feature::Goals is on (inside the SleepTool hard gate)"; the candidate's Q3 words it as "let ModelDriven register sleep if Goals is enabled or the existing model/current-time policy permits it". At the pin `Feature::Goals` is `Stage::Stable, default_enabled: true` (features/src/lib.rs:1702-1706), so the rule is true in every default session. When the current-time reminder is enabled, `spec_plan` consults only `config.current_time_reminder.sleep_tool` (spec_plan.rs:1237-1244); that knob is documented as "Whether to expose the input-interruptible `clock.sleep` tool" and defaults to `false` (core/src/config/mod.rs:1311-1316). The `|| goals_enabled` arm overrides that explicit opt-out and adds `clock.sleep` to every model in every session, which is the article's own caveat case (untrained models sleeping or spinning `sleep 1`). The justification given for rejecting the goal-scoped design, "still needs pre-goal exposure on the turn that can create a goal, or accepts a first-turn gap", does not hold: the tool router is captured for every sampling step (turn.rs:424-470, `built_tools` called from session/mod.rs:3916), and spec planning already reads `session.services.thread_extension_data` (spec_plan.rs:137, 341-343). A goal-active marker inserted by the goal extension exposes sleep from the step after `create_goal` succeeds, in every continuation, and nowhere else.

Correction: add a third `ModelDriven` arm `model_has_clock || goal_active`, where `goal_active` is a marker type owned by `codex-extension-api` (or core) in thread extension data, inserted by the goal extension on `create_goal` success (extension.rs:470-486), on `on_turn_start` when the goal is `Active | BudgetLimited` (extension.rs:270-282), and on resume; removed on complete/blocked/paused/clear/thread stop. Keep `features.sleep_tool.enabled = false` as the hard off switch. State the precedence against `current_time_reminder.sleep_tool` explicitly. Required negative test: a non-goal session on a non-clock model does not receive `clock.sleep`; required positive test: the sampling step after `create_goal` does.

## 5. Machine-readable verdict

```verdict-findings
{
  "findings": [
    {
      "id": "p5-acceptance-without-wake",
      "row": "p5-completion-delivery",
      "invariant": "Every armed background-exec completion reaches the owning live thread generation exactly once (active-turn injection or a newly admitted turn), or is explicitly cancelled; no loss when idle admission declines.",
      "mechanism": "Design statement: the plan transfers completion ownership on 'turn acceptance', but at 33a0f766a6 Session::inject_if_running (core/src/session/inject.rs:21-37) accepts into a bare idle reservation that clear_reserved_idle_turn discards (core/src/session/turn_input.rs:615-624), and input accepted into a finishing task is only recorded to history at task end (core/src/tasks/mod.rs:668-697) after which maybe_start_turn_for_pending_work (core/src/tasks/mod.rs:884, 451-457) wakes solely for mailbox items; neither path is in the plan's race table.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/session/inject.rs",
          "command": "git show 33a0f766a6:codex-rs/core/src/session/inject.rs | sed -n '17,55p'",
          "expected_failure": "inject_if_running returns Ok whenever active_turn is Some, including a reservation with task == None; inject_hook_context_if_running (lines 49-55) refuses that same state, so an 'accepted' completion can sit in a reservation that never becomes a task.",
          "pinned_blobs": ["ea999374a39c488a7a619962e39d1702f00cb094"]
        },
        {
          "test_file": "codex-rs/core/src/session/turn_input.rs",
          "command": "git show 33a0f766a6:codex-rs/core/src/session/turn_input.rs | sed -n '451,478p;615,624p'",
          "expected_failure": "Every decline path after reservation calls clear_reserved_idle_turn, which sets active_turn to None and drops the reservation's turn_state together with any pending input injected into it.",
          "pinned_blobs": ["d9a5c6a30abb5a2410828ba89cfacc2bdaa65332"]
        },
        {
          "test_file": "codex-rs/core/src/tasks/mod.rs",
          "command": "git show 33a0f766a6:codex-rs/core/src/tasks/mod.rs | sed -n '445,458p;660,697p;876,886p'",
          "expected_failure": "At task end, unsampled pending input is taken and recorded to history (lines 668-697) and the only follow-up wake, maybe_start_turn_for_pending_work (line 884), returns early unless a mailbox item with trigger_turn or a durable sleep exists (lines 451-457); a ResponseItem completion injected late is recorded without any turn start.",
          "pinned_blobs": ["323c8015a5a947845a24e643b4937ebdaf09b31e"]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none"
    },
    {
      "id": "p2-goals-feature-overrides-sleep-config",
      "row": "p2-p3-capability-consistency",
      "invariant": "Sleep exposure honours explicit sleep-tool configuration and stays scoped to goal work; the model is never handed a tool because of a policy that is unconditionally true.",
      "mechanism": "Design statement: rev2 P2 / candidate Q3 register clock.sleep whenever Feature::Goals is enabled; Goals is Stable and default-enabled (codex-rs/features/src/lib.rs:1702-1706), so the rule holds in every default session and overrides CurrentTimeReminderConfig.sleep_tool (codex-rs/core/src/config/mod.rs:1311-1316, default false) which spec_plan consults exclusively when the reminder feature is on (codex-rs/core/src/tools/spec_plan.rs:1234-1249); the stated reason for rejecting a goal-scoped marker (first-turn gap) fails because tools are captured per sampling step (codex-rs/core/src/session/turn.rs:424-470) and spec planning reads thread extension data (codex-rs/core/src/tools/spec_plan.rs:137,341-343).",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/tools/spec_plan.rs",
          "command": "git show 33a0f766a6:codex-rs/core/src/tools/spec_plan.rs | sed -n '130,140p;338,344p;1225,1251p'",
          "expected_failure": "With the current-time reminder enabled, ModelDriven registers sleep only when config.current_time_reminder.sleep_tool is true; an added '|| goals_enabled' arm bypasses that opt-out. The same function already receives session.services.thread_extension_data, so a goal-active marker is reachable without a core->goal dependency.",
          "pinned_blobs": ["bb1474feb52820424f14089c0b073df7b9d650a1"]
        },
        {
          "test_file": "codex-rs/core/src/config/mod.rs",
          "command": "git show 33a0f766a6:codex-rs/core/src/config/mod.rs | sed -n '1309,1326p'",
          "expected_failure": "sleep_tool: bool is documented as 'Whether to expose the input-interruptible clock.sleep tool' and defaults to false; the plan makes this documented switch inert on every default install.",
          "pinned_blobs": ["60c6f65353453265ad413ce6f4d093b17cbdc625"]
        },
        {
          "test_file": "codex-rs/features/src/lib.rs",
          "command": "git show 33a0f766a6:codex-rs/features/src/lib.rs | sed -n '1702,1707p'",
          "expected_failure": "Feature::Goals is Stage::Stable with default_enabled: true, so 'Goals enabled' is not a goal-scoped condition but an always-on one.",
          "pinned_blobs": ["4b05bdb5bee3345f7aa3e9e20c542adb3fc5aaae"]
        },
        {
          "test_file": "codex-rs/core/src/session/turn.rs",
          "command": "git show 33a0f766a6:codex-rs/core/src/session/turn.rs | sed -n '420,470p'; git grep -n 'built_tools(' 33a0f766a6 -- codex-rs/core/src/session/mod.rs",
          "expected_failure": "The run_turn loop captures a fresh step context (and therefore rebuilds the tool router via built_tools) for every sampling request after the first, so a marker set when create_goal succeeds is visible on the very next step; the 'first-turn gap' used to justify the broad policy does not exist beyond that single step.",
          "pinned_blobs": ["b88b343c1df7e8c7bd0a3b9d34b747b0b03f4576"]
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "N1 (p4b-pacing-scheduler): the low-activity rule 'at most one non-wait leaf-tool attempt' leaves the article's two-process orchestrator turn (look at A, look at B, wait) unpaced beyond the 30s floor: up to 120 continuations per hour, each a full context reread. Disclosed by the candidate as a blind spot. Prefer classifying by absence of state-changing outcomes (FileChange, plan update, successful create/update_goal, agent spawn) regardless of tool count, and measure request counts in the app-server test.",
    "N2 (p4c-native-subagents): the registration API for 'delegated work the goal is awaiting' is unspecified. An existing primitive does the job: Session::has_outstanding_durable_sleep (core/src/tasks/mod.rs:422-428) lets any mailbox mail, including queue-only child completion, wake an idle thread (core/src/session/handlers.rs:88-91; core/src/tasks/mod.rs:451-457), covered by queue_only_agent_mail_wakes_sleeping_root_with_previous_turn_context (core/tests/suite/pending_input.rs:522). No production extension inserts that SleepItem marker at the pin; the goal extension can insert it while it defers and remove it when it continues.",
    "N3 (p5-completion-delivery): a 768-byte fragment cap forces one extra write_stdin read per completion; refresh_process_state removes an exited entry on observation (core/src/unified_exec/process_manager.rs:1136-1143), so retained output must be keyed by receipt, not by store entry. The candidate says this; it is an implementation bound.",
    "N4 (p4a-goal-gating): no model-facing way to release a mis-armed subscription (a dev server armed by mistake) other than killing the process; after the third check-in the goal parks until human input. Safe direction, but the parked state must be surfaced to the user.",
    "N5 (p1-integer-arguments): create_goal.token_budget (ext/goal/src/tool.rs:52-54,204) is parsed by the goal crate's own parse_arguments (tool.rs:415) and stays float-intolerant after P1's first field list; a custom-provider model cannot set a budget. Wire the same adapter there or state the gap in the series table.",
    "N6 (p2-p3-capability-consistency): P3 text hedges with 'actually available in this turn' where the template can be exactly conditional: the runtime already passes update_plan_enabled into the template (ext/goal/src/runtime.rs:474-477); pass sleep and notification capability flags the same way.",
    "N7 (article-coverage-and-evidence): 37 cited ranges spot-checked at the pin all resolve (list in section 7). research.md rev1's 'turn_metadata.rs:190 is private today' was wrong (current_turn_trigger exists at 355) and rev2 corrected it; tekacs-fork-analysis cites fork line numbers (extension.rs:175 vs 180 at the pin), harmless.",
    "N8 (staging-tests-and-upstream-fit): the proposed core/src/session/async_input.rs inbox duplicates InputQueue's mailbox (enqueue_mailbox_communication, has_trigger_turn_mailbox_items, maybe_start_turn_for_pending_work), which already implements retained delivery, idle wake and priority over goal continuation; AGENTS.md asks to leverage existing abstractions. Reusing it is also the F1 correction and shrinks stage 2b.",
    "N9 (p4a-goal-gating / headless): codex exec defers goal continuation on fork (exec/src/lib.rs:1063) and exits at TurnCompleted (exec/src/event_processor_with_human_output.rs:318-331); P5 must be capability-gated there as the candidate states. Bound, not a defect.",
    "N10 (p1-integer-arguments): a visit_f64-with-exactness-check adapter is an acceptable simpler alternative to RawValue lexeme decoding for the named fields; the two pathological lexemes the candidate cites are harmless for millisecond and token fields. Implementation may choose either; the test set is the same."
  ],
  "surface_results": [
    {"row": "p5-completion-delivery", "result": "broken"},
    {"row": "p4a-goal-gating", "result": "held"},
    {"row": "p4c-native-subagents", "result": "held"},
    {"row": "p1-integer-arguments", "result": "held"},
    {"row": "p2-p3-capability-consistency", "result": "broken"},
    {"row": "p4b-pacing-scheduler", "result": "held"},
    {"row": "article-coverage-and-evidence", "result": "held"},
    {"row": "staging-tests-and-upstream-fit", "result": "held"}
  ],
  "free_hunt": [
    "Durable-sleep hook (has_outstanding_durable_sleep) exists in core and is exercised only by tests at the pin; it is an asset for P4a/P4c rather than a defect of the plan (see N2).",
    "inject_if_running vs inject_hook_context_if_running reservation asymmetry (inject.rs:21-37 vs 49-55) is the concrete code shape behind F1(a); any new completion injector must use the task-present form.",
    "Remote catalogs can also replace experimental_supported_tools (manager.rs:572-603), so model_has_clock can change between sessions; the goal-active marker design for P2 is independent of that."
  ]
}
```

## 6. Adjudication: astra review vs research rev2, and where this review disagrees with both

| Point | Astra | Rev2 | Adjudication |
|---|---|---|---|
| P1 shape | Field-level exact adapter + `integer` schemas | Adopted astra | Astra right on scope (dynamic passthrough must stay `Value`, dynamic.rs:138). Adapter implementation detail is free (N10). Add goal `token_budget` (N5). |
| P2 signal | "Goals enabled" broad policy; goal-active marker named but rejected for a first-turn gap | Adopted astra | **Both wrong** (F2). Goal-active marker in thread extension data is implementable and has no gap beyond one step. Rev1's `turn_trigger == "goal"` was also wrong (misses the creating user turn and completion-triggered turns), as astra said. |
| P3 wording | Capability-conditional prose | Adopted | Astra's text is safe; make it exactly conditional (N6). |
| P4a gate location | Goal-owned, over opt-in armed work + undelivered completions | Adopted | Astra right: global idle suppression would starve queued user input (service.rs:549-565) and `list_processes` would park goals on dev servers. |
| P4b classifier | Needs new observations, generation tickets, 30s floor | Adopted | Astra right that accounting keeps booleans only (accounting.rs:40-49). Blind spot quantified in N1. |
| P4c | Registered work generations | Adopted | Both over-engineer: durable sleep + mailbox already wakes on queue-only mail (N2). Not blocking. |
| P5 delivery | Receipt state machine + new retained inbox + controller bridge | Adopted | Receipt state machine right. New inbox is both a duplicate (N8) and under-specified on acceptance (F1). Use the mailbox. |
| P5 fragment / prompts | ≤768 bytes; tool descriptions + developer contributor; bundled edit optional | Adopted | Right on channel (manager.rs:572-603 verified). Byte cap is conservative (N3). |
| P6 | Deferred | Deferred | Agreed. |
| Budget | Excludes cached input; `[goals]` nesting | Adopted (rev2 correction) | Verified (accounting.rs:527-531; config_toml.rs:482,723). |
| Headless exec | Release gate for P5 | Adopted | Verified (event_processor_with_human_output.rs:318-331). |

## 7. Evidence log

Verified at the pin (path:line as cited by the candidate unless noted): extension.rs:180-192, 245, 270-282, 301-363, 457-486; runtime.rs:425-505, 474-477, 482; accounting.rs:27-49, 109-140, 163-229, 527-531; continuation.md:22-25, 48-56; spec_plan.rs:137, 341-343, 1225-1251; sleep.rs:34-43, 74-76, 95, 108-133; handlers/mod.rs:86-92, 124; unified_exec/mod.rs:73-82, 191-197; process_manager.rs:594-647, 1013-1020, 1128-1151, 1723-1800, 1824-1874; async_watcher.rs:158-242; inject.rs:17-55; codex_thread.rs:378-395, 401-416, 545-549, 710-715; turn_input.rs:395-478, 615-624; input_queue.rs:100-175, 240-345; tasks/mod.rs:300-335, 422-458, 478-540, 660-697, 876-886; lifecycle.rs:58-81; session/handlers.rs:79-92, 287-310; completion.rs:96-106; agent/control.rs:159-179, 260-300; turn_metadata.rs:348-356; manager.rs:572-603; openai_models.rs:897-923; prompt.rs:8-63; status.rs:6-21; features/src/lib.rs:979-982, 1702-1706; config/mod.rs:1311-1325; config_toml.rs:478-484, 721-725; goal tool.rs:52-54, 204-209, 415; dynamic.rs:118-150; write_stdin.rs:22-31; unified_exec.rs:28-41, 62-66; shell_spec.rs:55-60, 120-141; multi_agents/wait.rs:95-99, 292-295; json_schema/types.rs:124-129; models.json:1240 (file has 1436 lines at the pin) and the `clock` entries for gpt-6-astra/sol/luna only; exec/src/lib.rs:1063; event_processor_with_human_output.rs:309-339; queue service.rs:549-565; state/runtime/goals.rs:111-152; thread_goal_empty_responses.rs:27-80; test_codex.rs:541-561, 600; pending_input.rs:522, 883-1057; ext/goal/Cargo.toml:18; tools/Cargo.toml:30. History: #44320 = 0735c51978 (2026-09-09), before the article date, as both documents state.

Unverified (not load-bearing for the verdict): exec/src/lib.rs:1280-1319, 1639-1651; event_processor_with_jsonl_output.rs:513-536; unified_exec/process.rs:60-73; mcp.rs:235-263; mcp_tool_call.rs:145-165; mcp_resource.rs:373-399; extension_tools.rs:65-69, 207-221; session/mod.rs:1475-1499; model_info.rs:46-49; internal_model_context.rs:79-85; tool_lifecycle.rs:198-214; plan.rs:108-111.

Method: static reading of pinned blobs only; no build or test run (the brief allows but does not require one, and no finding needed a build to settle). Commands used are the ones in the reproductions.

## 8. Corrections the next revision must make

- **P1**: keep the field-level adapter and `integer` schemas; add `create_goal.token_budget` to the field list or state the gap; record N10 as an allowed implementation choice.
- **P2**: replace "Feature::Goals enabled" with a goal-active marker in thread extension data (type in `codex-extension-api` or core), maintained by the goal extension; keep `features.sleep_tool.enabled = false` as the hard switch; state precedence against `current_time_reminder.sleep_tool`; add the negative test (non-goal session, non-clock model, no sleep) and the positive test (step after `create_goal`).
- **P3**: make the template conditional on the same capability flags the runtime passes for `update_plan_enabled`.
- **P4a**: unchanged, plus a model-facing release for a mis-armed subscription and a user-visible "automatic check-ins stopped" signal.
- **P4b**: classify low activity by absence of state-changing outcomes rather than tool count; keep the 30s floor as a named tunable; add the request-count measurement to the app-server test.
- **P4c**: use the durable-sleep marker while the goal defers; drop registration generations unless a test shows the marker is insufficient.
- **P5**: define acceptance as "included in a sampling request"; deliver through the trigger-turn mailbox (new `TurnInput` variant or runtime-authored communication with `trigger_turn = true`); keep the receipt state machine, fragment bound and headless gating; add the two F1 paths to the race table with tests.
- **Series table**: P1 → P5 (receipt + mailbox delivery) + P4a → P2 (marker) + P3 → P4c (durable sleep) → P4b; re-estimate 2b after the mailbox reuse.

## 9. Logbook entries (outcome-scoped; no control-root edit)

- Tools are rebuilt per sampling step at 33a0f766a6 (turn.rs:424-470 → session/mod.rs:3916 → spec_plan); mid-turn capability changes are visible on the next step. This invalidates the "first-turn gap" argument for broad sleep exposure.
- Unsampled pending input at task end is recorded to history without a wake (tasks/mod.rs:668-697, 884; 451-457). Any "inject into active turn" delivery must define acceptance as sampled.
- `has_outstanding_durable_sleep` is an unused-in-production wake primitive at the pin; it is the cheapest route to waking a waiting goal parent on child completion.
- `current_time_reminder.sleep_tool` (default false) is the only sleep switch when the reminder feature is on; a `Goals`-based rule overrides it silently.
- `models.json` is pretty-printed at the pin (1436 lines); the trimmed fork patch header describing a single-line file refers to the fork's hunk only.
