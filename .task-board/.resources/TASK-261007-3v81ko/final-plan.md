# Goal-mode token burn — consolidated implementation plan, revision 2

Task: TASK-260929-1srn2y. Research only; no production changes/tests. Evidence pin: `33a0f766a647208b471cfbcad889c67fd324ee04`. Source citations are relative to `codex-rs/` at the pin, not worktree HEAD `bfdb1571780b326ce978696de12b1d81b5e978f2`. New files, APIs and tests below are proposed.

## 1. Recommendation

1. P1: exact field adapters, including goal budgets; no arbitrary JSON rewrite.
2. P5: receipt state machine through the existing mailbox; acknowledge only sampled input.
3. Activate P5+P4a together: opt-in waits, goal-only gate, bounded check-ins and release.
4. P2: goal-active attachment with existing sleep-switch precedence.
5. P3: no fresh-poll obligation; tool guidance uses actual sampling-step capabilities.
6. P4c: durable-sleep marker plus the V1 mailbox bridge.
7. P4b: pace absence of observed state change, regardless of tool count.
8. Defer P6; no second inbox or budget-accounting change.
9. Tests must prove silence before events and requests/progress afterward.
10. Arbitrary unregistered polling inside one turn remains a stated bound (§11).

## 2. Review findings resolution

This supersedes earlier plans. Preserve the six held rows' direction; resolve the broken rows and notes as follows.

| ID | Decision and resolution |
|---|---|
| F1 `p5-acceptance-without-wake` | Accept: mailbox leases retained until sampling; both reservation-loss and finishing-task paths tested (§5.2–5.4). |
| F2 `p2-goals-feature-overrides-sleep-config` | Accept: goal-active marker, switch precedence, post-create sampling test (§4). |
| N1 | Accept: no-state-change classifier, independent of poll count; measure requests (§8, §11). |
| N2 | Accept: owned SleepItem, all side effects/removal specified; bridge V1 (§7). |
| N3 | Accept: receipt-keyed retained output, independent of process entry (§5.1). |
| N4 | Accept: release without kill; visible stopped-check-ins warning (§5.1, §6). |
| N5 | Accept: adapt goal crate's token_budget field (§3). |
| N6 | Accept with timing correction: exact capabilities from sampling router; conditional developer block (§9). |
| N7 | Accept: getter already exists at `core/src/turn_metadata.rs:355`; fork lines are not upstream evidence. |
| N8 | Accept: no `session/async_input.rs`; extend InputQueue (§5.2). |
| N9 | Accept: deny unsupported/headless hosts and descendants (§5.3). |
| N10 | Reject lossy visit_f64 as equivalent; accept visitors preserving the original decimal. Current typed parsing rejects fractions (`core/src/tools/handlers/mod.rs:86–92`; `ext/goal/src/tool.rs:415–420`); goal budget is i64 (`ext/goal/src/tool.rs:52–54`). Rounded fractions are counterexamples (§12). |

## 3. P1 — scoped integral-decimal compatibility (Q2)

**Verdict: modify.** `parse_arguments<T>` is a useful common parser, not a safe normalization boundary. It directly deserializes the supplied string (`core/src/tools/handlers/mod.rs:86–92`). Dynamic tools deserialize `Value` through it and forward that value (`core/src/tools/handlers/dynamic.rs:138–145`); recursively changing every number changes an integration payload. Separate parsers include plan (`core/src/tools/handlers/plan.rs:108–111`), MCP (`core/src/tools/handlers/mcp.rs:235–263`, `core/src/mcp_tool_call.rs:145–165`), MCP resource null/empty handling (`core/src/tools/handlers/mcp_resource.rs:373–399`), extension forwarding (`core/src/tools/handlers/extension_tools.rs:65–69,207–221`) and goal tools (`ext/goal/src/tool.rs:415–420`). Keep all those envelopes and special cases unchanged.

Put reusable Serde adapters in new `tools/src/arguments.rs`; raw_value is already enabled (`tools/Cargo.toml:29–30`). Deserialize RawValue numeric lexemes only on annotated fields. Accept exact in-range integer-valued JSON decimals/exponents, including 60000.0, 6e4 and -0.0; reject fractions, strings, booleans, unsigned negatives and overflow. Preserve defaults/null/omission and duplicate-field rejection. Never pass through f64/Value: integers above 2^53 remain exact. Bound exponent handling by checked digit counts, not exponent-sized allocation. Preserve the existing argument-error envelope.

Initial field scope is explicit:

| Typed arguments | Annotated integer fields | Existing evidence |
|---|---|---|
| SleepArgs | `duration_ms` | `core/src/tools/handlers/sleep.rs:32–43,95–99` |
| ExecCommandArgs | `yield_time_ms`, `timeout_ms`, `max_output_tokens` | `core/src/tools/handlers/unified_exec.rs:28–41` |
| WriteStdinArgs | `session_id`, `yield_time_ms`, `max_output_tokens` | `core/src/tools/handlers/unified_exec/write_stdin.rs:22–31` |
| Both native wait argument types | `timeout_ms` | `core/src/tools/handlers/multi_agents/wait.rs:291–295`; `core/src/tools/handlers/multi_agents_v2/wait.rs:126–130` |
| CreateGoalRequest | `token_budget` | `ext/goal/src/tool.rs:52–54,204–209` |

Keep range checks/clamps. Use integer schemas for these fields; `JsonSchema::integer` exists (`tools/src/json_schema/types.rs:124–129`), and goal budget already uses it (`ext/goal/src/spec.rs:35–39`). Schema changes help generation, not parsing. Floating fields and unlisted built-in integers remain unchanged.

Test exact decimals/exponents, signed/unsigned boundaries, huge/underflowing exponents, rounded fractions (§12), defaults/null/duplicates. Drive actual handlers and create_goal, including code-mode leaves. Compare forwarded dynamic/MCP/extension payloads unchanged. Put new unit modules in separate files; avoid static-value-only tests.

## 4. P2 — goal-active sleep exposure (Q3, F2)

**Modify.** Trigger=goal misses creating/completion turns; Feature::Goals is stable/default-on (`features/src/lib.rs:1702–1706`). Neither scopes sleep correctly. The existing trigger getter is irrelevant.

Add documented `GoalActivity { identity/revision, Active | BudgetLimited }` in new `ext/extension-api/src/goal_activity.rs`. Core reads this capability marker without depending on goal. Goal owns it through existing ExtensionData insert/remove (`ext/extension-api/src/state.rs:98–132`); spec planning already reads thread attachments (`core/src/tools/spec_plan.rs:137,341–343`). It is not automatic-admission permission or persisted config.

One goal-runtime publisher reconciles committed state under the goal-state permit. Pass it to tool executors. A late successful callback must not reinsert an old goal after clear.

| Transition | Exact integration hook and required action |
|---|---|
| Successful `create_goal` | After the database insert succeeds, before returning its tool result (`ext/goal/src/tool.rs:212–240`), insert Active. `GoalExtension::on_tool_finish` (`ext/goal/src/extension.rs:457–486`) reconciles committed state, not blind insertion based on tool name. |
| Turn start | At `ext/goal/src/extension.rs:228–281`, reconcile the database into Active/BudgetLimited **before** the missing-token-baseline and Plan-mode early returns (237–240,257–263). These are accounting restrictions, not evidence of no goal. |
| Resume / external set | `ext/goal/src/runtime.rs:401–422` and `191–255`: read committed status; insert for Active or BudgetLimited, remove for every other status. Extend resume's currently Active-only branch. External API runtime-effects path is `ext/goal/src/api.rs:76–83`. |
| `update_goal` / automatic stop / accounting limit | Reconcile after each committed status mutation (`ext/goal/src/tool.rs:247–304`; `ext/goal/src/runtime.rs:277–398`; `ext/goal/src/extension.rs:488–528`). Complete, Blocked, Paused and UsageLimited remove; BudgetLimited retains capability but never admits automatic continuation. |
| Clear | `ext/goal/src/runtime.rs:258–268`: remove unconditionally on committed clear, including when feature enablement is already off. |
| Thread stop / feature disable | `ext/goal/src/extension.rs:195–200,204–221`: remove marker and goal-owned wait/timer state before unregistering/returning. Re-enable reconciles state rather than reusing a stale marker. |
| Read failure | Remove the capability marker, record reconciliation as unknown and report the error; absence of the marker must not authorize continuation. Reconcile again on the next legitimate lifecycle event. |

Preserve current precedence (`core/src/tools/spec_plan.rs:1225–1250`):

```text
sleep_available = SleepTool.enabled AND
  match sleep_tool_mode:
    AlwaysOn    => true
    ModelDriven => if CurrentTimeReminder.enabled:
                     current_time_reminder exists AND current_time_reminder.sleep_tool
                   else:
                     model_has_clock OR GoalActivity exists
```

Hard sleep disable wins over AlwaysOn. ModelDriven respects reminder sleep=false (including missing config); AlwaysOn retains today's override. Reminder default=false is documented at `core/src/config/mod.rs:1311–1325`; persistent defaults preserve explicit settings (`core/src/session/time_reminder.rs:17–38`). Do not invent curr_time availability.

Tools are rebuilt each sampling step (`core/src/session/turn.rs:424–470`; `core/src/session/mod.rs:3916–3966`). The first creation request cannot foresee a goal; the next request after successful creation must expose sleep when switches permit.

Tests: non-goal/non-clock/default Goals, ModelDriven and reminder feature off => absent; successful create => next request present; failed create, hard-off or reminder-off => absent; AlwaysOn unchanged; goal completion wake, lifecycle removals, budget-limited/resume, missing accounting baseline, stale callback after clear. Assert actual request tools. Sleep remains direct-only in code mode.

## 5. P5 — completion receipts through the mailbox (Q5, F1)

**Modify.** Preserve watcher ordering: exit, output drain, late network denial, final classification (`core/src/unified_exec/async_watcher.rs:160–242`). It emits UI events only. The fork's bool misses exit-before-arm, and its inject_or_start is absent upstream.

### 5.1 Subscription and receipt contract

Expose opt-in `notify_on_exit: true` only on capable hosts; default false. A session ID alone is not a wake promise. Initial yield must acknowledge a receipt. Never arm automatically on every yield/stdin poll. Use a named internal enum.

Reserve one of 64 receipt slots before opted-in launch; refuse before execution if full. This is separate from the existing 64-process cap (`core/src/unified_exec/mod.rs:78–82`). Use bounded opaque IDs tied to owning thread/runtime generation/call.

State machine, under one synchronization boundary:

```text
Reserved (initial tool response undecided; terminal result may already exist)
  -> InlineResult (terminal result chosen for initial response; no pushed completion)
  -> Armed (yielded subscription acknowledged)
Armed + finalized exit -> Queued -> LeasedToSampling -> Sampled
Any unsampled state -> Cancelled(reason) on explicit release/stop/shutdown
Lease failure before sampling -> Queued (same receipt, no duplicate history append)
```

Initial-response decision and exit publication rendezvous under the receipt lock. An early exit is returned inline or retained until arming commits; independent atomics cannot establish that invariant.

Terminal stdin output and mail share one claim: whichever representation is first sampled consumes it. Cancellation before sampling requeues. A request containing both must deduplicate metadata; later explicit output reads are allowed but cannot create another wake.

Add `exec_notification` with tagged `read {receipt_id,max_output_tokens?}` and `release {receipt_id}`. Read returns terminal output, not a new blocking/liveness poll; release disarms without killing or retires output. Reject stale/foreign/unknown receipts. Retain output by receipt: process exit observation removes its store entry (`core/src/unified_exec/process_manager.rs:1137–1143`). Cap retention at 1MiB head/tail per receipt with truncation indicated, small default reads, <10K tokens per returned item. Free slots on inline delivery, release or shutdown; no silent eviction of advertised handles. Keep process permissions unchanged.

New `core/src/context/exec_completion.rs` implements ContextualUserFragment. Entire escaped fragment ≤768 UTF-8 bytes: receipt/process IDs, exit/failure/timeout and retention state; no command/raw output. Batch ≤8 (6144 bytes), retain remainder. Use the recognized internal-context wrapper/classifier. Text is data; forged markers cannot acknowledge receipts or authorize actions.

### 5.2 Mailbox ownership and sampling acknowledgment

Choose a new **internal runtime-notification mailbox variant**, not fake InterAgentCommunication. Inter-agent mail requires author/recipient paths (`protocol/src/protocol.rs:806–822`), records lineage/events (`core/src/session/mod.rs:3969–4026`) and trigger-turn fork/rollback boundaries (`core/src/thread_rollout_truncation.rs:68–109`). Exec exit is none of these.

Extend mailbox entries (`core/src/session/input_queue.rs:95–104,163–228`) and internal TurnInput (`36–48`) exhaustively. Keep public protocol/RPC variants unchanged. Runtime receipt references refuse public TurnInput serialization; persist only contextual ResponseItems.

Current drain removes entries (`core/src/session/input_queue.rs:191–228`): runtime entries instead remain logically leased until sampled/cancelled. Preserve inter-agent semantics. Trigger-mail queries include unsampled leases, retaining priority over goal continuation (`core/src/session/turn_input.rs:395–399,449–454`; `core/src/tasks/lifecycle.rs:58–81`). No second inbox.

Active delivery obeys task-present/mailbox-phase checks (`core/src/session/input_queue.rs:142–160`). Idle wake belongs to `maybe_start_turn_for_pending_work` (`core/src/tasks/mod.rs:437–534`); extend its trigger/settings selection. Preserve execution settings, set exec_completion trigger, invent no initiating agent and reset no human quota.

Acceptance = **included in a sampling request**. Track trusted IDs through pending input, one history append, final prompt and transport. Verify membership in the actual submitted prompt (`core/src/session/turn.rs:2539–2552`; HTTP/WS selection `core/src/client.rs:2218–2266`). Successful stream submission may acknowledge; reservation, drain or history append cannot. Failed transport uses existing bounded retries; retain/suspend visibly after exhaustion, never spawn endless wake turns.

Compaction/guardian omission leaves the receipt pending. Retry an already-recorded unsampled fragment without appending it twice. Normal history repetition is not duplicate delivery. Guarantee logical notification once per live generation, not exactly-once network transport/crash recovery.

### 5.3 Lifecycle, host capability and persistence

Host-seeded `AsyncNotificationSupport` defaults Unavailable in extension-api. Enable only verified persistent hosts via existing extension init (`core/src/thread_manager.rs:270–310`; `app-server/src/request_processors/thread_processor.rs:1466–1470`). Headless exec shuts down at TurnCompleted (`exec/src/event_processor_with_human_output.rs:309–339`; `exec/src/event_processor_with_jsonl_output.rs:513–536`); it and descendants cannot arm or advertise notification waits. Inherit capability explicitly; “not Exec” is insufficient.

Runtime mailbox admission must share shutdown/Plan/extension/capacity checks (`core/src/session/turn_input.rs:379–478`), preserving inter-agent follow-up semantics. The execution guard increments rather than atomically reserving (`core/src/agent/control/execution.rs:32–58,69–85`); do not bypass V2 capacity. Decline retains mail; retry on idle/admission/capacity signals, not polling. Add a capacity-release wake signal if needed.

Shutdown marks shutting_down before process termination (`core/src/session/handlers.rs:287–310`): cancel claims first. User interrupt cancels wake claims for interrupted work; no resurrection. Process termination shares the terminal claim. Goal clear removes goal timers/gates but not an independently acknowledged exec subscription. Owner stop/shutdown cancels it; never wake a different/unloaded thread.

Receipt/output/timer state is live-generation-only. Resume never rearms from text; old handles become unavailable. Persisted contextual data creates no human/fork boundary (`core/src/context_manager/history.rs:1334–1349`; `core/src/thread_rollout_truncation.rs:68–109`). Preserve ExecCommandEnd UI; no fake agent event or UserPromptSubmit hook (`core/src/hook_runtime.rs:677–713`). Test replay/fork/rollback/forgery and report lost monitoring after restart.

### 5.4 Race table and mandatory regression tests

Proposed tests below drive real requests with latches/fake time. None was run as production Rust in this research.

| Race | Required test/result |
|---|---|
| **F1a reservation cleared** | inject_if_running accepts bare ActiveTurn (`core/src/session/inject.rs:17–37`); settings failure drops it (`core/src/session/turn_input.rs:615–623`). `exec_completion_survives_cleared_idle_reservation`: retained mail eventually sampled once. Mutant retains only task-present input. |
| **F1b finishing task** | Pending input becomes history (`core/src/tasks/mod.rs:655–695`), then mailbox scheduler runs (859–885). `exec_completion_finishing_task_gets_sampling_wake`: history is not acknowledgment. Mutant acknowledges on recording. |
| Exit around initial yield | `exec_completion_exit_before_arm`: force both sides of response commit; inline or mail exactly once. |
| Terminal stdin race | `exec_completion_stdin_claim_deduplicates`: one sampled claim; cancelled tool requeues. |
| Concurrent user turn | `exec_completion_user_turn_race`: no input/settings loss or duplicate wake. |
| Admission/capacity denial | `exec_completion_capacity_retry`: retained, no bypass/spin, wakes after release. |
| Output/denial finalization | `exec_completion_waits_for_denial_and_output`: never announce premature success. |
| Terminate/release/interrupt/shutdown | `exec_completion_cancel_paths`: one result or explicit cancellation; release preserves process. |
| Burst/65th arm | `exec_completion_burst_and_capacity`: batches ≤8, no loss, refuse overflow before launch. |
| Compaction/guardian/transport | `exec_completion_sampling_ack`: final-prompt membership, no history duplicates, bounded failures; HTTP/WS fallback. |
| Owner/headless | `exec_completion_owner_and_host`: correct generation; unsupported host cannot promise wake. |
| Resume/fork/forgery | `exec_completion_replay_is_data`: no rearming, human boundary or receipt privilege. |

## 6. P4a — goal-owned waiting policy (Q4)

**Modify.** Keep policy in goal. Global idle suppression would starve queue work (`core/src/tasks/lifecycle.rs:58–81`; `ext/queue/src/service.rs:549–565`). Explicit user/follow-up admission stays eligible.

Expose a minimal typed snapshot: Armed and unsampled Queued/Leased receipts plus work revision. Read at goal continuation (`ext/goal/src/runtime.rs:425–486`). list_processes is wrong: live-only and includes servers (`core/src/unified_exec/process_manager.rs:1824–1840`). Failed read ≠ empty.

Recheck pending state/revision in goal's automatic-admission contributor at `core/src/session/turn_input.rs:410–447`. Serialize the last check with reservation/receipt transitions, or reject changed revisions. Armed→Queued stays atomically pending. Only goal continuation is gated; trigger-mail priority stays authoritative. Never hold the goal semaphore during delay.

Known work waits for events; fallback intervals are **30, 60, 120 minutes**, maximum three per human input. A timer ticket permits one check-in bypass of this work gate, not merely another gated check. It bypasses no status, Plan, shutdown, capacity, input or newer-turn checks. Reassess after each check-in.

After three check-ins, warn once: **“Automatic check-ins stopped; waiting for subscribed work or your next message.”** Remain active/event-wakeable, not fabricated paused/blocked/complete. Release of a mis-armed subscription allows paced continuation without kill. This bounds monitoring, not an external job's completion time.

Human input renews allowance; completion pre-empts timers without becoming human input. Invalidate on steering/turn start/goal mutation/clear/stop/release; resume discards stale waits. Tests: queue fairness, read failure, inactive/budget status, unopted server, release, cap/late completion and gate-to-start race.

## 7. P4c — native subagent waiting using durable sleep (Q7)

Native V2 completion is queue-only (`core/src/agent/control/completion.rs:96–113`; `core/src/agent/control.rs:491–507`). SleepItem in thread data enables queue-only wake (`core/src/tasks/mod.rs:422–458`; `core/src/session/handlers.rs:79–93`), demonstrated by `core/tests/suite/pending_input.rs:522–589`. External shell children remain P5's concern.

Use SleepItem as goal wait registration, not per-child generations. At goal idle, inspect directly owned native children: loaded PendingInit/Running work permits registration on a persistent host. No marker for non-goal/unloaded/unknown work. Reused children use current state; Completed means turn-ended, not goal-achieved (`core/src/agent/status.rs:8–30`). Apply §6's check-ins. Interrupted is non-final in the existing global status helper (same citation): for a registered wait, existing status watchers must emit a queue-only Interrupted notice once per transition without redefining global is_final or claiming success.

list_agents silently skips failed lookups (`core/src/agent/control.rs:398–416`). Query owned registry entries with typed Loaded/Unloaded/error inspection (`core/src/agent/control/inspection.rs:12–30`); propagate errors. Keep the API narrow/private.

**Bridge V1:** `core/src/agent/control.rs:510–518` directly injects SubagentNotification, bypassing wake. Send the same bounded fragment as queue-only runtime mailbox data; fabricate no AgentPath. SleepItem supplies wake permission; ordinary parents remain quiet. Cover completed/error/closed/interrupted status and another child finishing mid-turn.

Marker ownership/lifecycle:

| Action or side effect | Required behavior and evidence |
|---|---|
| Insert | Goal extension owns an ID such as `goal-wait:<generation>`. Use `insert_if` only if absent or already its own (`ext/extension-api/src/state.rs:107–123`). Do not clobber another contributor's sleep. Install before checking pending mail; then call the existing pending-work scheduler/recheck. This closes completion-before-registration. |
| UI / timer | `SleepItem` is a display shape (`ext/items/src/sleep.rs:6–14`), but storing it emits nothing and schedules nothing (`ext/extension-api/src/state.rs:98–105`). The clock tool separately emits started/completed events and sleeps (`core/src/tools/handlers/sleep.rs:102–135`). Do not emit a fictitious tool call or promise its duration matches an actual clock.sleep call. The goal scheduler owns the timer and warning. |
| Current-time reminder | Insertion itself does not record a history item. Reminders observe user/tool-output boundaries (`core/src/session/time_reminder.rs:49–60`); storing the marker does not turn this feature on or override its configuration. |
| Wake semantics | **Any** mailbox mail can wake durable sleep, including queue-only follow-ups, not only child completion. This is intentional responsiveness; test it and preserve inherited turn settings (`core/src/tasks/mod.rs:487–495`). It does not make arbitrary injected ResponseItems trigger mail. |
| Remove | Goal runtime removes only its owned ID on the next admitted turn start, goal inactive/clear/disable, thread stop or explicit wait release. Use an atomic conditional removal analogous to insert_if; a check-then-unconditional-remove is racy. On a check-in, remove for that admitted turn and reinsert if still waiting when it becomes idle. Keep it while check-ins are exhausted so late queue-only completion can wake. |
| Resume | Marker is in-memory only. Reconcile goal and live child state; never revive it from a rendered old SleepItem or a now-unloaded child. |

Tests: both versions, no-marker negative, early completion, registration race, reused/interrupted/error child, second result midturn, clear/stop, foreign marker preservation, inherited settings, no sleep UI/reminder change. Assert requests, not only marker presence.

## 8. P4b — low-activity pacing (Q6)

**Modify.** Existing booleans/any-tool activity (`ext/goal/src/accounting.rs:27–49,109–140,163–203`) cannot prove state change. Preserve them for existing blockers; add separate compact observations in goal.

Low activity = **no observed state-changing outcome**, regardless of tool count. Reset on applied file change, actual plan transition, committed goal mutation, accepted spawn/follow-up. Failed tools, identical plans, ps/tail success, code-mode wrapper success and model progress claims do not reset. Arbitrary shell side effects remain unknown; conservative pacing is permitted, completion is not inferred.

Record effects at committing handlers/events, not ToolFinish success alone (`ext/goal/src/extension.rs:457–468`). Count code-mode leaves once. Expose no model-writable progress bypass.

New `ext/goal/src/continuation_schedule.rs` owns one cancellable timer. Minimum automatic spacing 30s; low streak delay min(30s*2^(n-1),30min), reset by observed state change. Known subscribed work uses §6 instead. Preserve three-empty-turn blocking first (`ext/goal/src/accounting.rs:216–229`); nonempty “waiting” is paced, not classified empty.

Tickets bind goal identity/revision, predecessor turn, generation/cause. Invalidate on human input/steering, goal change/clear, stop, completion/release and new turn. Recheck at admission with predecessor/pending mail (`core/src/session/turn_input.rs:395–454`). A user turn that starts AND ends before the old deadline still invalidates it. Event wakes pre-empt; no detached sleep accumulation.

Timers/counters are transient: resume reconciles goal and restarts at the floor, never restores stale subscriptions. Completion does not reset human allowance; restart resets transient quotas, a disclosed bound.

[Claude Code's official goal docs](https://code.claude.com/docs/en/goal) describe background deferral, 30/60/120-minute check-ins, maximum three without human input, stopping tool-less loops and resume resets. These are documentation claims, not closed-source verification. Borrow pacing, not its extra evaluator model.

Tests: two polls grow streak; actual mutation resets; failures/wrappers do not; stale timers and all invalidations; empty blocker retained. Measure model requests. In-turn polling remains §11's bound.

## 9. P3 — exact wait contract and prompt channel (Q8–Q9)

**Modify.** Remote catalog replaces bundled entries (`models-manager/src/manager.rs:572–603`); templates affect instructions (`protocol/src/openai_models.rs:897–923`). Bundled gpt-5.5's contrary exec guidance (`models-manager/models.json:1240`) is not a reliable patch channel. Use local tool descriptions and developer capabilities; bundled cleanup is optional.

Current continuation rendering passes update_plan_enabled before sampling (`ext/goal/src/runtime.rs:474–477`; `ext/goal/src/steering.rs:53–93`). Instead compute WaitingCapabilities from the final captured router (`core/src/session/mod.rs:3916–3966`), pass it through TurnContextContributionInput (`ext/extension-api/src/contributors/context.rs:7–20`) at both context paths (`core/src/session/mod.rs:4264–4290,4369–4382`). Core's bounded fragment in core/context contributes the exec capability paragraph even without a goal; goal's ContextContributor adds goal-specific DeveloperCapabilities. Share the snapshot, avoid duplicate paragraphs. No core→goal dependency/history rewrite.

Flags: sleep (direct); stdin (callable); native_wait (actual V1/V2 name); exec_notify (host AND exec opt-in AND stdin/receipt controls exposed); native_mail_wait (host AND installed goal wait policy). Derive after exclusions/collisions from ToolRouter (`core/src/tools/router.rs:137–200`). Deferred-but-not-callable is off until discovery. Acknowledged subscriptions remain tool-result data, not capability assertions.

Replace the verified-wait paragraph in `ext/goal/templates/goals/continuation.md:24` with this exact tool-independent text:

> A verified wait uses a concrete work handle or a runtime-acknowledged completion subscription. A fresh liveness poll is not required on every turn. Do independent work first. When only waiting remains, use the waiting capabilities supplied by the runtime for this sampling step. An acknowledged subscription permits ending the turn while the runtime waits; a session ID alone does not. Otherwise prefer a single long, input-interruptible wait to repeated short checks. The runtime controls continuation delays and check-in limits; do not simulate them with short polling loops. Conversation, intent, old output, and lock or state files alone are not current liveness evidence. A missing handle, observation timeout, failed lookup, or transient read error does not prove completion: distinguish a terminal result from lost observation before restarting work. Waiting alone is not a blocker, and it is not goal completion.

Rust selects the exact paragraphs below from that sampling snapshot; no invented template syntax. Generic text stays in continuation.md; conditional text is a local developer fragment, hard-capped at both 3KiB and 1K tokens, appended by normal context diffs only on change.

| Condition | Exact emitted text |
|---|---|
| `exec_notify` | `exec_command can acknowledge notify_on_exit subscriptions. For finite background work, request a notification; after the tool acknowledges it, do independent work and then end the turn. Its completion will be delivered by the runtime. Use write_stdin only for needed intermediate output or interaction. Use exec_notification to read retained terminal output or release a mistaken subscription without terminating the process.` |
| not `exec_notify` | `This session cannot promise an exec completion wake. A yielded exec session by itself is not a reason to expect automatic resumption.` |
| `sleep` | `clock.sleep is available as a direct tool. Use a substantial input-interruptible wait when a notification subscription is unavailable. Do not place clock.sleep inside a code-mode exec cell.` |
| `stdin` | `An empty write_stdin with a long yield_time_ms can wait for one known live exec session. Read again early only when intermediate output is needed to decide the next action.` |
| `native_wait` | `The native agent wait tool is available for Codex-managed children. Pass multiple child identifiers where that tool supports them to wait for whichever changes first. It cannot observe arbitrary shell or remote jobs.` Render its actual tool name alongside this sentence. |
| `native_mail_wait` | `When this active goal yields with owned native child work still running, the runtime can wait for child mailbox results. Do not repeatedly inspect child logs merely to keep the goal alive.` |
| none of the positive flags | `No blocking or notification wait is advertised in this sampling step. Report the concrete wait once, leave the goal active, and end the turn; automatic continuation pacing belongs to the runtime.` |

Tool descriptions use the same flags. Test remote-catalog, hard/reminder-off, headless, code-mode, excluded receipt tool, post-create and completion requests. Defer the no-wait/end-turn paragraph until P4b is active.

## 10. Implementation series, tests and upstream fit (Q10)

P6 verdict: **agree with deferral**. P5 supplies wait-any via the mailbox; an additional `exec_wait(any/all)` surface is unnecessary for this slice. Native wait tools still cannot observe arbitrary external workers.

Separate stages, estimates including tests. Keep each <800 changed lines, preferably <500 logic; split measured overruns. Preparatory stages remain inactive until paired activation.

| Order | Scope and principal files (new files where appropriate) | Required validation | Estimate / risk |
|---|---|---|---|
| 1 P1 | `tools/src/arguments.rs`; waiting argument structs/schemas; `ext/goal/src/tool.rs` | Adapter units; `core/tests/suite/unified_exec.rs` handler requests/passthrough; app-server goal-create float budget | 350–480 lines; medium |
| 2a P5 state, inactive | `core/src/unified_exec/completion_receipt.rs`, output retention; thin watcher/process-manager hooks | State races, output bounds, inline/stdin competing claims | 350–480; high |
| 2b P5 mailbox, inactive | `core/src/session/input_queue.rs` plus small runtime-mail module; internal TurnInput; context fragment | F1a/F1b units and `core/tests/suite/pending_input.rs`; serialization/fork/rollback | 450–650; high |
| 2c P5 request acknowledgment, inactive | `core/src/session/turn.rs`, client submission hook if needed; mailbox lease completion/retry | Actual HTTP/WS request-body assertions, compaction and finishing-task tests | 350–480; high |
| 2d P4a policy, inactive | `ext/goal/src/background_wait.rs`; narrow thread pending-work API/admission hook; scheduler foundation | Gate TOCTOU, queue starvation negative tests; fake-time check-in/release/cancel | 400–550; high |
| 2e P5+P4a activation | Host extension attachment; exec opt-in/control tool and schema; local descriptions; activate both | `core/tests/suite` owner/headless/capacity tests; `app-server/tests/suite/v2/goal_background_wait.rs (new)` controlled-exit vertical test | 500–750; high |
| 3a P2 | extension-api GoalActivity, goal publisher/hooks, spec-plan gate | Spec units; app-server create→next-sample and removal/config matrix | 350–480; medium |
| 3b P3 capability plumbing | extension-api WaitingCapabilities, router snapshot into context, goal capability renderer | Real request tool/guidance agreement, remote-catalog and code-mode negatives | 350–480; medium |
| 4 P4c | Goal-owned SleepItem lease; V1 bridge; narrow child inspection query | Existing pending-input test extended for both versions; app-server native goal parent tests | 450–650; medium/high |
| 5 P4b + P3 full contract | `ext/goal/src/continuation_schedule.rs`, accounting observations, exact template text | Fake-time scheduler units; app-server two-poll request counts, three-empty blocker; bounded prompt tests | 400–600; medium/high |

Activate P5 and P4a together at 2e. Before stage 5, advertise only acknowledged-subscription release; generic no-wait turn release depends on pacing.

Only process/mailbox/request integration belongs in core; extract focused modules, keep central files orchestration-only. Parsing belongs in codex-tools; contracts in extension-api; scheduling/policy in goal. Goal depends on core (`ext/goal/Cargo.toml:18`), not vice versa: combined tests belong in app-server.

Vertical test: real JSON-RPC/tool dispatch creates goal, launches barrier-controlled notified process, ends turn, proves zero continuation requests before exit, releases barrier, proves one wake with receipt and subsequent progress. Stalled runtime must fail. Add user queue/burst/unopted server. Use remote-tests auto-env helpers and Linux/macOS/Windows/foreign exec fixtures; macOS is relevant locally, not iOS.

Implementation commands: `just test -p codex-tools`, `just test -p codex-core`, `just test -p codex-goal-extension`, scoped app-server tests; fmt/fix and warning insta snapshots per AGENTS. Goal's existing tests are under ext/goal/tests (lib test=false), so extend that harness. No full suite without required permission. Update Bazel compile_data for new embedded templates and schemas only for actual API changes.

## 11. Article coverage and remaining bounds (Q1)

Carry forward revision 1's article-first table; corrections below use pinned sources. Private rollout numbers remain attributed article data, not independently reproduced measurements.

| Article mechanism or recommendation | Upstream at pin; disposition |
|---|---|
| Immediate goal re-entry, measured ~30ms | No delay in `ext/goal/src/extension.rs:180–192` → `ext/goal/src/runtime.rs:425–486`. P4a/P4b change policy. 30ms is article data. |
| Empty automatic turns | Partly addressed by commit `0735c51978`, Sep 9, #44320: three fully empty continuations (`ext/goal/src/accounting.rs:216–229`). This predates Sep 11; activity evades it (`163–203`). Preserve blocker and add low-activity pacing. |
| Poll-only verified-wait contract; cannot self-pause | Still in `ext/goal/templates/goals/continuation.md:22–25,48–56`. P3 removes fresh-poll obligation; no new permission to self-pause/block. |
| Sleep only on Astra; enable for active goals | Bundled clock support now includes gpt-6-astra, gpt-6-sol and gpt-6-luna (`models-manager/models.json:1–474`); custom/older models cannot rely on it. Gate still consults catalog/config (`core/src/tools/spec_plan.rs:1225–1250`). P2 scopes the fix. |
| Integral floats reject every waiting path | Typed parsing remains strict (`core/src/tools/handlers/mod.rs:86–92`; sleep `95–99`; write_stdin `22–31`). P1 covers selected fields/budgets. Stdin yield is now u64, not the old i32 example. |
| Exec default 10s, cap 30s; longer empty stdin | Defaults `core/src/tools/handlers/unified_exec.rs:62–67`, caps `core/src/unified_exec/mod.rs:73–82`; empty stdin uses configurable timeout (`core/src/unified_exec/process_manager.rs:1018–1039`). Yield returns control, **does not kill** the longer shell sleep/job. Keep caps; notification is the fix. |
| No pushed shell completion | Watcher only emits UI events (`core/src/unified_exec/async_watcher.rs:160–242`). P5+P4a deliver/wait together; fork alone cannot fix goal re-entry. |
| Prompt says stay in turn for exec | Bundled gpt-5.5 line `models-manager/models.json:1240`; runtime catalog replacement `models-manager/src/manager.rs:572–603`. Local capabilities/descriptions are the reliable channel (§9). |
| Several child jobs require repeated individual polls | Native wait schema supports multiple native IDs (`core/src/tools/handlers/multi_agents_spec.rs:849–875`); external workers are outside that registry. P5 provides event fan-in, P4c addresses native parent wakes; P6 deferred. |
| Native spawn reported unsupported | Source-session observation, not reproduced here; provider request trace unavailable. During implementation test actual router/code-mode exposure (§9); P5 must work without native agents. |
| Long single-turn polling (439 calls in article) | Inter-turn pacing alone cannot stop it. Acknowledged notifications plus conditional guidance remove the need to poll finite exec/native work. Arbitrary MCP/remote/shell-log polling without a subscription remains a bound, not claimed solved. |
| No budget default; put a budget on every goal | Config is `[goals].max_goal_token_budget`, default and cap (`config/src/config_toml.rs:482,721–725`). Accounting excludes cached input (`ext/goal/src/accounting.rs:527–531`); it does **not** cap the article's gross input. P1 enables fractional-looking budget input; do not change accounting silently. |
| Use Astra/minimal effort, always_on, long waits, barrier | Workarounds: catalog varies; sleep reduces but does not eliminate calls. Longer stdin config does not raise exec's 30s ceiling. Prefer notifications, then long waits. |
| Cache/context growth and subscription-limit exhaustion | Measure sampling requests. Subscription-limit formula is unknown; do not infer it from API cache rules. No cache/history rewrite. |
| Post-article upstream changes | Pinned log includes `d47b9a8c00` Sep 23 (#47665, preserve early output) and `4891c4e35f` Sep 24 (#47712, atomic output reads). Output fixes, not model wake; preserve tests. |

Implementation bounds, not new research leaves:

- Transport: identify/verify HTTP+WS request-submitted acknowledgment; add a narrow callback if stream success is cancellation-ambiguous. Never use queue acceptance.
- Unregistered in-turn polling: no generic semantic shell/MCP classifier was established. Measure the two-process pattern; prefer subscriptions/event adapters. A hard bound on arbitrary in-turn requests requires an explicit request-budget policy, not a claim this scheduler supplies it.
- Hosts: enable only verified persistent owners; confirm daemon/disconnect lifetime during implementation.
- Size/platforms: measure diffs; split >800 lines. Unrun remote/Windows lanes remain unverified.
- Restart: report lost live observation; missing handles cannot establish success.

## 12. Research verification and adversarial coverage

Research checks below execute pinned-anchor assertions and decision-rule counterexamples, not proposed Rust. Each narrowing mutant preserves some valid cases. Production tests must independently kill equivalent mutations before landing.

| Surface row | Counterexample / narrowing mutant | Required production entry test |
|---|---|---|
| p5-completion-delivery | Protect reservations but acknowledge finishing-task history before sampling (F1b); separately retain only task-present reservations (F1a). | Both named F1 tests in §5.4, actual sampled receipt asserted |
| p4a-goal-gating | Gate only live Armed work, allowing Queued/Leased exits or unknown reads to look empty. | Goal idle→admission, receipt transition + queue fairness |
| p4c-native-subagents | Wake V2 mailbox results only, leaving V1 injection outside the marker's wake path. | V1+V2 completion through real parent mailbox |
| p1-integer-arguments | Accept only decimal-point forms, excluding exact integral exponent forms; separately allow f64-rounded fractions. | Real wait/create-goal dispatch plus unchanged passthrough |
| p2-p3-capability-consistency | Restrict to active goal but ignore reminder sleep=false; or grant to any Goals-enabled thread. | Post-create tools request and negative config/non-goal matrix |
| p4b-pacing-scheduler | Pace only ≤1 poll; two read-only polls evade the streak; stale ticket remains invalid even after user turn ends. | Fake-time two-poll requests, fast intervening human turn |
| article-coverage-and-evidence | Audit only uncached tokens while claiming a gross-input bound. | Accounting fixture with large cached input; exact pinned coverage citations |
| staging-tests-and-upstream-fit | Require silence only; a permanently stalled runtime passes without the post-event assertion. | Controlled-exit vertical test must prove wake/progress too |

Numerical counterexamples for N10: exact decimal `1.0000000000000001` is fractional but rounds to `1.0` as f64; `9007199254740991.5` rounds to an integer-valued f64. Current typed integer parsing rejects float tokens. Exactness is cheap to test and should not depend on a “harmless” judgment about a token-budget or time value.

Only this document is a new board outcome. Logs/probes stay in .temp/goal-token-burn-rev2. No builds/production tests; old checklist acceptance does not accept this revision.

### Verification record and outcome-scoped logbook

Research checks: `python3 .temp/goal-token-burn-rev2/research_checks.py` exited 0 (logs 01/15): 186 checks, 117 citation ranges, 17 pinned source anchors. This validates the plan, not Rust behavior. Git diff, cached diff and diff --check each exited 0; status was empty. No commit/push/build.

Each command `python3 …/research_checks.py --mutant NAME` below exited **1**, expected: the narrowed rule violates the named witness (§12). Logs are research-check-NN.log.

| NAME | NN |
|---|---|
| f1_reservation / f1_finishing | 13 / 14 |
| p4a_live_only / p4c_v2_only | 04 / 05 |
| p1_no_exponent / p1_float_rounding | 06 / 07 |
| f2_feature_scope / f2_reminder_override | 08 / 09 |
| p4b_one_poll | 10 |
| article_net_as_gross | 11 |
| staging_silence_only | 12 |

Coverage: **8/8 research rows attacked; 11/11 rule mutants rejected; 0/8 production behaviors executed**. Initial F1 mutants (02/03, exit 1) also changed the sampled case; corrected 13/14 isolate the intended early-acceptance failures. Missing-path exploratory reads failed (git 128 / wrapper 1) and were corrected; none was treated as absence.

Logbook: F1 requires sampled acknowledgment; F2 requires active-goal scope; V1 bypasses the mailbox; SleepItem storage has no UI/timer side effect; goal tests use codex-goal-extension. Rework began 23:40 UTC; packaging at ~00:17 UTC, ~37m this run plus ~31m prior, below 90m. Findings and these bounds travel in this sole outcome, with no control-root file edits.
