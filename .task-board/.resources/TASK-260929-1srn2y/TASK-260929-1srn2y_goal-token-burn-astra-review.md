# Independent review of the goal token-burn patch series

Task: TASK-260929-1srn2y — astra-independent-patch-research. Research baseline: upstream `33a0f766a647208b471cfbcad889c67fd324ee04`. Started 2026-09-28 22:20 UTC (2026-09-29 local); 90-minute budget. Research only; no product changes or builds.

Paths are relative to `codex-rs/`; citations refer to pinned Git blobs. Worktree HEAD `88e9a8329d17bd141e4f3f0e7c78d07a7baa8b23` differs from the pin. The article/code table was saved before deliberate P1–P6 comparison; the inlined `research.md` made literally blind exposure impossible.

## 1. Summary

1. Keep P1 first, but normalize known integer fields exactly; do not rewrite arbitrary JSON through floating point.
2. Deliver P5 and P4a together: opt-in completion subscriptions, reliable queued delivery, and goal-specific waiting.
3. Reject an unconditional wake-on-every-yield port and a global suppression of thread-idle events.
4. P2 should cover goal-enabled user turns too; checking only the automatic goal trigger is insufficient.
5. P3 needs capability-conditional wording and a local developer instruction, not only bundled model edits.
6. P4b needs cancellable scheduling with generation checks; current accounting cannot implement the proposed classifier unchanged.
7. Add native-child waiting/waking to the series: current completion messages normally do not start an idle parent.
8. Defer P6; completion subscriptions provide wait-any behavior without another model-facing tool.
9. Account for headless host shutdown, notification bounds, and budgets excluding cached input.
10. Static research supports this revised series; concurrency behavior still needs the integration tests below.

## 2. Independent article coverage (Q1)

| Article mechanism / proposed fix | State and recommendation at the pin | Evidence |
|---|---|---|
| Immediate idle→goal continuation, no backoff | Present. Add goal-specific waiting/scheduling. The reported 30ms is private-session evidence, not a timing guarantee. | `ext/goal/src/extension.rs:180-192`; `ext/goal/src/runtime.rs:425-505` |
| Empty or “waiting” turns spin | Three literal empty automatic finals block. Text, reasoning summary and any tool outcome defeat that guard. | `ext/goal/src/accounting.rs:109-140,163-229` |
| Sleep only on Astra; enabled feature yet absent tool | Catalog widened to Astra/Sol/Luna 6, but model/config registration still restricts it. Add goal-enabled exposure, respect hard disable/policy. | `models-manager/models.json:3-473`; `core/src/tools/spec_plan.rs:1225-1250`; `core/src/tools/handlers/sleep.rs:74-76` |
| Integral floats disable waiting tools | Typed parser remains strict. Fix integer destinations and integer schemas, not arbitrary JSON. | `core/src/tools/handlers/mod.rs:86-92`; `core/src/tools/handlers/sleep.rs:34-43,95` |
| Initial exec yields after 10s/default, 30s/max; stdin waits 5min | Still true with Windows floor and configurable empty-stdin maximum. Yield does not kill the process. Snapshot commands return immediately regardless of timeout. | `core/src/unified_exec/mod.rs:73-82`; `core/src/tools/handlers/unified_exec.rs:62-63`; `core/src/unified_exec/process_manager.rs:631-655,1013-1026` |
| No model completion notification for exec | Watcher emits UI end/failure events only. Add opt-in model delivery. | `core/src/unified_exec/async_watcher.rs:175-242` |
| End-turn cannot be a free goal wait | Goal ignores pending exec work. Gate the goal contributor, not global idle. | `core/src/tasks/lifecycle.rs:58-81`; `ext/goal/src/runtime.rs:425-505` |
| Contract requires a fresh live poll | Present. Replace with acknowledged subscriptions or available blocking waits. | `ext/goal/templates/goals/continuation.md:22-25` |
| User-only pause, three-turn blocker audit | Present. Runtime pacing must not falsely report completion, user pause or a genuine blocker. | `ext/goal/templates/goals/continuation.md:48-56` |
| Multiple external children lack shared wait-any | Native wait tools cannot see arbitrary OS processes. Use completion subscriptions/finite watchers; intermediate remote milestones need an event adapter. | `core/src/tools/handlers/multi_agents/wait.rs:68-102`; `core/src/tools/handlers/multi_agents_v2/wait.rs:52-95` |
| Native children supposedly wake parent | Separate hole: completion defaults to queue-only. Add a registered native-work wake policy. | `core/src/agent/control/completion.rs:30-37,88-114` |
| gpt-5.5 “do not end” prompt | Present; remote catalog can overwrite bundled changes. Use local capability-specific developer/tool guidance. | `models-manager/models.json:1240`; `models-manager/src/manager.rs:572-603` |
| No default token budget | No universal default. Configured cap supplies one, under [goals]; accounting excludes cached input. | `config/src/config_toml.rs:721-725`; `ext/goal/src/tool.rs:204-209`; `ext/goal/src/accounting.rs:527-531` |
| Proposed sleep, pacing, float and contract fixes | All still relevant with corrections P1–P4 below. Sleep/long stdin reduce calls; subscriptions remove idle polls. | Registration, parser, lifecycle and template references above |
| User mitigations: change model, force sleep, single barrier, budget | Available mitigations, not a dispatcher fix. Native barriers cover only native work; numerical parsing still matters after sleep exposure. | Above tool/timeout/budget paths |
| Subscription exhaustion / private rollout measurements | Not independently reproducible from supplied sources. No subscription token-to-percent formula established. | Supplied article, 2026-09-11: https://relux.works/en/blog/codex-goal-token-burn/ |

Relevant history: `0735c51978` (#44320, 2026-09-09) adds the empty-final blocker **before** the article date; the source-session build SHA is unavailable, so whether it contained that guard is unverified. Post-article changes include `d47b9a8c00` (#47665, 2026-09-23: preserve early output in completion events), `4891c4e35f` (#47712, 2026-09-24: atomic output buffer updates), `869b5527cd` (#47814, 2026-09-24: termination-test lost wake), and `f6a4bd81e3` (#48168, 2026-09-25: unique exec-server IDs). None adds model-visible exec-completion input in the inspected watcher. These are reasons to port intent, not apply the old fork diff mechanically.

## 3. Per-patch verdicts

| Patch | Verdict | Required correction |
|---|---|---|
| P1 integral floats | **Modify** | The common parser covers the important wait tools, but is neither universal nor safe for blanket Value rewriting. Use destination-specific exact integer decoding and integer schemas; preserve passthrough arguments. Q2. |
| P2 sleep exposure | **Modify** | The goal trigger is set early enough, but only identifies automatic goal continuations. Prefer availability whenever Goals is enabled, within the SleepTool hard gate and ordinary tool policy. The proposed metadata getter already exists. Q3. |
| P3 contract | **Modify** | Accept an acknowledged runtime subscription as evidence; long blocking waits are alternatives. Never promise a wake merely because a session ID was returned. Conditional replacement text is in Q9. |
| P4a pending-work gate | **Modify** | Goal-owned gate over registered finite-work subscriptions, not every live process. Include completion delivery pending admission, native children, cancellation, and an explicit check-in bypass. Q4/Q7. |
| P4b backoff | **Modify** | Add the missing observations, a single cancellable scheduler and stale-generation protection. Separate empty-final blocking, pacing, and a limit on timer-generated waiting check-ins. Q6. |
| P5 completion notification | **Modify substantially** | Keep the event-driven idea; reject the fork's bool-only race protocol, 8K-token fragment, unconditional prompt, and one-retry delivery recipe. Use serialized ownership, bounded input, host capability and automatic admission. Q5/Q8. |
| P6 exec wait-any/all | **Agree with deferral** | Not necessary for the first vertical slice. A barrier remains useful for explicit in-turn waits or hosts that cannot survive a turn ending; do not add it before evidence that existing blocking waits plus subscriptions are insufficient. Q10. |

Primary-plan omissions: native-parent wake policy, headless lifetime, cached-input exclusion, and config nesting. Existing accounting is insufficient for P4b; the proposed trigger getter already exists. Detailed corrections and evidence follow.

## 4. Detailed answers Q2–Q10

### Q2. Integer arguments: coverage, semantics, and recommended P1

`core/src/tools/handlers/mod.rs:86-92` is a useful shared typed parser, not a universal boundary:

| Path | Actual parsing at the pin |
|---|---|
| Sleep; interactive/one-shot exec; stdin | Shared parser: `core/src/tools/handlers/sleep.rs:95`; `core/src/tools/handlers/unified_exec/exec_command.rs:186,236-245`; `core/src/tools/handlers/unified_exec/write_stdin.rs:81`. The base-path helper only installs a path guard, then uses the same parser (`core/src/tools/handlers/mod.rs:149-157`). |
| Native multi-agent V1/V2 | Shared parser, including both waits: `core/src/tools/handlers/multi_agents/wait.rs:68,291-295`; `core/src/tools/handlers/multi_agents_v2/wait.rs:52,126-130`. Spawn/followup also use it (`core/src/tools/handlers/multi_agents/spawn.rs:65`; `core/src/tools/handlers/multi_agents_v2/spawn.rs:122`; `core/src/tools/handlers/multi_agents_v2/followup_task.rs:40`). |
| Plan | Independent typed from_str, `core/src/tools/handlers/plan.rs:108-111`; no reason to broaden it for waiting fixes. |
| MCP calls/resources | MCP payload reaches an independent Value parser, `core/src/tools/handlers/mcp.rs:235-263`; `core/src/mcp_tool_call.rs:145-165`. Resources have a different local parser with empty/null handling, `core/src/tools/handlers/mcp_resource.rs:373-399`. |
| Dynamic tools | **Does use shared parser**, but target is arbitrary Value, then forwarded externally (`core/src/tools/handlers/dynamic.rs:138-145`). A global rewrite changes these arguments too. |
| Extension tools / goal budget | Payload is forwarded unchanged by the adapter (`core/src/tools/handlers/extension_tools.rs:65-69,207-221`). Goal tools deserialize separately (`ext/goal/src/tool.rs:415-420`). |
| Other Value consumers | Request-permissions parses Value before typed conversion (`core/src/tools/handlers/request_permissions.rs:70-86`); argument-rewrite helpers also use Value (`core/src/tools/handlers/mod.rs:119-135`). These are not justification for altering every number. |

Blanket normalization changes `-0.0`'s sign, Value number type/serialization, and duplicate-key handling. Rounded f64 integrality is not source integrality: `1.0000000000000001` and `9007199254740991.5` defeat the proposed ±2^53 argument.

**Implement:** a small reusable serde integer adapter in `tools/src/arguments.rs` (new), used only on named integer fields. Decode a JSON numeric lexeme with `serde_json::value::RawValue`, recognize decimal/exponent notation, discard only mathematically zero fractional digits, and use checked conversion to the destination integer type. Avoid an f64 intermediary. Keep ordinary integer values across their existing full range; reject strings, nonintegral decimals, overflow and invalid JSON. No new dependency is necessary for RawValue: `tools/Cargo.toml:29-30` already enables it. Preserve each field's defaults, nullability, validation and error prefix.

First P1 fields: sleep `duration_ms`; exec `yield_time_ms`, one-shot `timeout_ms` and `max_output_tokens`; stdin `session_id`, `yield_time_ms`, `max_output_tokens`; both agent-wait `timeout_ms`. Their types are at `core/src/tools/handlers/sleep.rs:34-35`, `core/src/tools/handlers/unified_exec.rs:28-41`, `core/src/tools/handlers/unified_exec/write_stdin.rs:22-31` and the wait references above. Keep goal-budget parsing outside this first patch unless the same adapter is explicitly wired and tested there; do not claim it is already covered.

Use `JsonSchema::integer` for these integer contracts: it already exists (`tools/src/json_schema/types.rs:17-24,124-129`). Relevant current number schemas: `core/src/tools/handlers/sleep.rs:38-43`; `core/src/tools/handlers/shell_spec.rs:54-62,118-141`; `core/src/tools/handlers/multi_agents_spec.rs:849-868`; one-shot timeout `core/src/tools/handlers/unified_exec/exec_command.rs:493-501`. Schema precision complements tolerant decoding; it cannot guarantee model compliance.

### Q3. Sleep availability

The trigger is available before routing: `session/turn_input.rs:172-175,513-515` sets metadata before starting the task; `session/turn.rs:1843-1852` builds the router later (both under `core/src/`). `core/src/turn_metadata.rs:355-356` already exposes `current_turn_trigger`. Timing is not the defect in P2.

The semantic gap is the first user turn creating a goal, later user steering, queued work, and future exec-completion turns: none must have trigger `goal`. A trigger describes why a turn began, not whether a goal is active. The goal extension owns active state in its runtime/database (`ext/goal/src/runtime.rs:47-59,454-468`); the synchronous registration branch currently sees configuration/model data (`core/src/tools/spec_plan.rs:1225-1250`), not that database state.

**Choose the simpler broad policy:** inside the existing SleepTool-enabled outer gate, let ModelDriven register sleep if Goals is enabled **or** the existing model/current-time policy permits it. Preserve explicit SleepTool disable and final tool-policy filtering. This covers the first request without a core→goal dependency or a tool-set change after goal creation. It is a deliberate broader default: both SleepTool and Goals are stable/default-true (`features/src/lib.rs:979-982,1703-1706`). Do not market it as “only active goals.”

If upstream rejects that broader exposure, the clean narrow alternative is an extension-api capability snapshot maintained by goal create/update/clear/resume and consumed by spec planning. That still needs pre-goal exposure on the turn that can create a goal, or accepts a first-turn gap. This is an implementation tradeoff, not another research prerequisite. Do not add a core dependency on the goal crate, which already depends on core (`ext/goal/Cargo.toml:18`).

`clock.sleep` is DirectModelOnly and input-interruptible (`core/src/tools/handlers/sleep.rs:74-76,108-133`); prompt guidance must not suggest calling it as a nested code-mode function.

### Q4. Goal gating, long-lived processes, and fallback

**Put policy in the goal extension.** Leave `emit_thread_idle_lifecycle_if_idle`'s meaning as thread inactivity. Suppressing that callback globally would also suppress dispatch of queued user input (`core/src/tasks/lifecycle.rs:58-81`; `ext/queue/src/service.rs:549-565`). Core can expose a read-only pending-work snapshot/change notification through CodexThread; the goal extension decides whether to continue.

Do not gate on `list_processes()`. It returns all live processes (`core/src/unified_exec/process_manager.rs:1824-1840`), with no promise of completion notification or eventual exit. Dev servers, watchers, tail-following and interactive shells would park goals indefinitely.

**Select opt-in per call:** add `notify_on_exit`, default false, to interactive exec only. Internally use an enum for the policy, not ambiguous positional bools. A live result must explicitly acknowledge that a completion subscription is armed. Tool text says opt in for finite work whose result is needed; do independent work before ending the turn. An ordinary yielded session ID is not evidence of a subscription. Do not silently arm an old process when write_stdin happens to observe it alive. Native children need their own registered work generations, Q7.

The core snapshot must count **armed work plus undelivered terminal completions**, not merely OS liveness. Transition pending→queued atomically before releasing the waiting gate, so an exit cannot create an idle gap in which goal continuation wins ahead of its result. Dispatch queued completion input before an ordinary goal continuation. A user turn always retains normal admission priority.

For a genuinely hung opted-in job, schedule one check-in after 30 minutes, then 60, then 120; at most three timer check-ins until new human input. A check-in is an explicit admission reason allowed to bypass the pending-work gate once. Merely rerunning the same pending-work check after 30 minutes would park forever again. After the limit, remain event-wakeable and report automatic check-ins stopped; do not call the goal achieved, paused by the user, or blocked by a nonexistent external blocker. A real completion remains allowed to wake immediately. Use the cancellation/generation rules in Q6.

This design minimizes idle model calls, but cannot detect arbitrary remote work from a log filename. External jobs need an opted-in local finite watcher that exits on the relevant event, or the paced polling fallback.

### Q5. P5 delivery, ownership and races

Current watcher waits for exit, drained output and interaction lock, then emits an event (`core/src/unified_exec/async_watcher.rs:175-242`). Injection accepts into an active turn or returns the items (`core/src/session/inject.rs:17-37`). Idle start **declines without enqueueing**, with execution-capacity checks (`core/src/codex_thread.rs:374-395,521-532`). Consequently “inject; start; retry inject once” can lose completion if both competing turns finish or admission fails. Injection also accepts a reserved turn whose settings may subsequently fail (`core/src/session/turn_input.rs:431-478`). Existing pending-work scheduling handles inter-agent mail/durable sleep, not arbitrary completions (`core/src/tasks/mod.rs:430-458`).

**Implement a retained inbox, not a one-retry handoff:**
1. New `core/src/unified_exec/completion.rs` owns a process receipt keyed by thread/environment/call/process generation. State: `InitialResponsePending -> InlineConsumed | Armed -> TerminalQueued -> TurnAccepted`, plus cancellation. Exit may precede the initial-response decision.
2. Watcher enqueues terminal data in a bounded session inbox (`core/src/session/async_input.rs`, proposed), then signals activity. Ownership transfers only after actual turn acceptance; failed reservations retain input.
3. Drain active input through the existing queue. Idle delivery uses a narrow controller bridge following `core/src/agent/control.rs:159-179`'s weak-runtime lookup, then CodexThread automatic admission. Preserve lineage, capacity, Plan-mode and shutdown rules. Do not impersonate user authorization or an inter-agent sender.
4. Serialize claims with turn reservation; retry refusals on relevant state transitions, never in a busy loop. Do not auto-resume an unloaded thread.

| Race / condition | Required invariant and evidence |
|---|---|
| Exit during initial yield | Inline terminal result consumes the receipt; a committed live response arms it even if exit was already observed. The process is stored before initial collection and Alive checks separate process state (`core/src/unified_exec/process_manager.rs:594-647,1128-1151`). A bool set after that check can lose a concurrent exit. |
| Concurrent turn start/end | Retain until accepted, including two successive competing turns and failed settings reservation. Test every decline path in `core/src/session/turn_input.rs:395-478`. |
| Terminal write_stdin | Poll and watcher claim one receipt. Poll consumption before delivery suppresses redundant notification; an already-delivered receipt never queues again. Existing locks help, but initial exec needs the same protocol (`core/src/unified_exec/async_watcher.rs:188`; `core/src/unified_exec/process_manager.rs:900`). |
| Terminate / interrupt / shutdown | Structured cancellation suppresses a new wake and releases the wait; unexpected failure/prune produces one terminal result. Arbitrary external kill remains an observed exit, not guessed intent. Shutdown sets shutting_down before termination (`core/src/session/handlers.rs:287-310`). Existing termination APIs need reason propagation (`core/src/unified_exec/process_manager.rs:1796-1811,1843-1874`). |
| Subagent thread | Deliver to the originating live generation under its own capacity/admission rules. Do not revive an interrupted/closed child or route its exec result directly as root user input. |
| Restart/resume | Live-runtime guarantee only. Shutdown kills managed processes; entries are memory state (`core/src/unified_exec/mod.rs:174-194`; `core/src/session/handlers.rs:307-310`). Restore recorded history, discard stale subscriptions; undelivered work is unknown, not terminal success. Crash-exactly-once is unverified/outside this slice. |
| Many exits | Coalesce before idle admission, then drain bounded batches in active work. Test all 64 admitted processes; no duplicate receipt or turn per stdout chunk. Process limit: `core/src/unified_exec/mod.rs:77-82`. |
| Output / delayed network denial | Preserve final output and classification ordering; do not guess exit success or drain another consumer's pending output (`core/src/unified_exec/async_watcher.rs:180-201,459-468`; `core/src/unified_exec/process.rs:60-73`). |
| Admission refused | Keep accepted data through transient capacity/idle races. Plan/draining/pending-user restrictions are not bypassed; wake only on a qualifying state change. |

**Context/storage bounds:** reject the fork's 8K-token fragment: this repository requires manual review above 1K, and the command/markup are additionally unbounded and unescaped. Use a `core/context` ContextualUserFragment with an escaped terminal summary/excerpt. Cap the **whole rendered fragment** at 768 UTF-8 bytes, including identity/markup; correlate using a bounded runtime receipt, retain full IDs internally, and verify tokenizer size. Drain at most eight separate fragments per sampling boundary. Reserve a slot when arming; cap outstanding receipts at 64/thread and explicitly refuse/fall back if full. Retain bounded output until terminal read/ack; do not advertise a retrieval handle after eviction.

**Host lifetime is a release gate:** headless codex exec shuts down on the requested turn's completion and filters by its original turn ID (`exec/src/lib.rs:1280-1319,1639-1651`; `exec/src/event_processor_with_human_output.rs:309-339`; `exec/src/event_processor_with_jsonl_output.rs:513-536`). Expose/acknowledge notifications only for hosts/modes admitting post-final execution; retain blocking guidance otherwise. One-shot exec has distinct timeout/termination semantics despite shared specs (`core/src/tools/handlers/unified_exec/exec_command.rs:70-108,312-319,439-444,484-501`). Do not append notification promises to its description. Headless keep-alive requires a separate host lifecycle change.

### Q6. Backoff definition, cancellation and resume

Current accounting retains booleans, not tool counts, wait categories or file/plan deltas (`ext/goal/src/accounting.rs:40-49,109-140,163-203`). The primary classifier therefore requires new observations.

Use a limited **observable** rule: host-admitted automatic goal turn, no successful completed FileChange, and at most one non-wait leaf-tool attempt. Only clock.sleep/wait_agent are intrinsically waits; exec/stdin are unknown-purpose attempts, not classified by shell-text guessing. Text, reasoning and plan restatements do not certify progress. Capture counts/IDs/source at existing callbacks before finish_turn removes state (`ext/goal/src/extension.rs:284-296,349-363,457-469`; `ext/extension-api/src/contributors/tool_lifecycle.rs:198-214`). Count code-mode leaf calls, not both leaf and wrapper.

For n consecutive low-activity automatic turns, delay `min(30s * 2^(n-1), 30min)`. Keep a 30s floor between other automatic goal turns; human input and real completion events pre-empt it. A user turn can hand off immediately to first useful goal work unless subscribed work is pending. These are proposed constants, not optimized measurements.

**Blind spot:** two short polls can reset this heuristic; in-turn polling never reaches the scheduler. The floor limits churn but does not prove arbitrary polling eliminated. P5/P3 address event-backed waiting; measure model-request counts in tests. A hard bound on arbitrary in-turn requests would require an explicitly designed sampling budget, not a semantic claim inferred from tool count. No additional research leaf is required.

Preserve the existing three-literal-empty-final blocker and evaluate it before scheduling (`ext/goal/src/accounting.rs:216-229`; `ext/goal/src/extension.rs:326-333`). Pacing also covers nonempty “still waiting” turns. Pending subscriptions instead use Q4's 30/60/120-minute check-ins and three-check-in limit.

Use one cancellable scheduler (`ext/goal/src/scheduling.rs`, proposed). Ticket: goal ID/revision, predecessor turn, user-input generation, work generation, due time and reason. Invalidate on user input **including steering**, goal update/clear/status, thread stop and exec/native completion. Abort the old timer, hold no goal permit while sleeping, and revalidate at actual admission, including async settings/capacity windows.

Idle+active-goal checks alone miss a user turn that starts and finishes before an old timer fires. Core already has a predecessor check (`core/src/session/turn_input.rs:438-443`), but the public continuation variant is a recovery path permitting Plan mode (`core/src/codex_thread.rs:398-403`). Extend automatic admission narrowly; do not reuse recovery to bypass policy.

Keep state transient like the current empty counter (`ext/goal/src/accounting.rs:27-36`). Resume discards timers/subscriptions, resets the streak and applies initial pacing; restarting can reset this protection. Persisting cross-restart pacing is a later implementation bound, not a prerequisite.

Claude's official docs describe a separate evaluator, deferral for background work, first check-in after 30m, doubling capped at 4×, and at most three interactive idle check-ins between human prompts. Several toolless turns stop continuation while retaining the goal. Noninteractive check-ins wait for a turn boundary; resume resets accounting/timing. This supports separating event waits, timer checks and loop protection, not necessarily adding an evaluator model to Codex. [Claude Code goal documentation](https://code.claude.com/docs/en/goal).

### Q7. Native subagents

**An ordinary idle parent is not reliably woken.** The V2 terminal router requires a spawned child with an agent path and sets `trigger_turn=false` (`core/src/agent/control/completion.rs:30-37,88-114`). The fallback likewise queues V2 completion; V1 injects a fragment without starting a turn (`core/src/agent/control.rs:443-518`). The session wakes on trigger mail or an outstanding **durable** sleep (`core/src/session/handlers.rs:79-92`). Active clock.sleep is interruptible by input; a separate extension-installed SleepItem permits queue-only mail to wake an idle sleeper (`core/src/tasks/mod.rs:422-458`). Neither exception means every goal parent receives an idle wake.

Add **P4c native-work integration** after the exec vertical slice: register the generation of delegated work the active goal is awaiting; enqueue the child result first, then signal the same goal waiting coordinator. Only that registered completion can pre-empt its wait. Do not turn every child message into trigger_turn=true or park on the existence of any child thread. AgentStatus::Completed describes a turn ending, not a permanent finished child (`core/src/agent/status.rs:6-21`); re-used children and follow-up tasks need generation keys. Interrupted children must release/reclassify the awaited generation. Treat turn completion as new evidence, not proof that a child's active goal is achieved; test that distinction.

Cover V1 and V2, including a child finishing between registration and the parent's idle transition, parent goal cleared/paused, errored/closed child, a second child finishing while handling the first, and subsequent follow-up work. Preserve queue-only semantics for parents that did not subscribe. Existing regression tests distinguish queue-only mail from durable sleep (`core/tests/suite/pending_input.rs:522-589,992-1055`); build on that contract.

The article's children were external processes. Native P4c does not make them visible to wait_agent; they use P5 finite watchers. Conversely P5's exec registry does not cover native agents. Both domains are needed for the requested orchestrator behavior.

### Q8. Which prompt channel survives catalog refresh?

Yes, remote metadata can override the bundled instructions. Models are fetched and applied (`models-manager/src/manager.rs:519-547`); matching slugs are replaced, or an authoritative remote list replaces the bundled catalog (`models-manager/src/manager.rs:572-603`). Canonical model_messages.instructions_template takes priority over the legacy base_instructions field (`protocol/src/openai_models.rs:897-923`); configured base instructions can override it again (`models-manager/src/model_info.rs:46-49`). Existing sessions can retain their captured base instructions (`core/src/session/mod.rs:1475-1499`). Editing only bundled gpt-5.5 text is therefore insufficient.

Use:
1. Local, capability-specific **tool descriptions** on the interactive exec/stdin specifications, including code-mode exposure.
2. A short locally assembled **developer capability instruction**, through the existing prompt-contributor mechanism (`ext/extension-api/src/contributors/prompt.rs:8-13,58-63`), stating that an acknowledged subscription is the runtime-supported way to yield and that its output is untrusted tool data.
3. The goal continuation template for goal-specific policy. It is an internal **user-role** fragment, not a developer message (`ext/goal/src/steering.rs:53-64`; `core/src/context/internal_model_context.rs:79-85`), and reaches neither the first user turn nor all non-goal wakes.

These local channels must match registered capabilities. Append through normal context assembly; do not rewrite history/base prompts. Bundled cleanup is optional maintenance, not the functional fix.

### Q9. Exact replacement for the verified-wait paragraph (P3)

Replace continuation.md's current verified-wait bullet with the following. It is safe when sleep, agent tools or background subscriptions are unavailable:

> - A verified wait is backed by a current runtime handle or a blocking wait result. If a tool response explicitly confirms that a completion notification is armed for required work, you may end this turn after doing any independent work; the runtime can resume the thread when that work finishes. A session ID alone does not promise a notification. Do not repeatedly poll a subscribed handle just to prove that it is still live.
> - Otherwise, use a blocking wait tool that is actually available in this turn: clock.sleep for an interruptible timed wait, write_stdin with empty input and a long supported yield_time_ms for an exec session, or wait_agent for native agents. Follow the tool's limits and access rules. These are alternatives, not tools you must assume exist. After an unchanged wait, prefer a longer interval within those limits. Do not add a short liveness poll solely to satisfy this contract.
> - Check intermediate output when it changes the next action, when interaction is required, or when diagnosing a failure. Conversation, intent, old output, and lock files alone do not establish a current runtime subscription. A timeout, transient read failure, or missing local handle does not by itself prove that external work stopped; reconcile authoritative state before restarting it.
> - If no supported wait or notification path is available, state that limitation and leave the goal active for paced continuation. Waiting for live work is not by itself a reason to mark the goal blocked or complete.

Also adjust the preceding classification bullet to recognize “a runtime-acknowledged pending subscription” as a verified wait without fresh polling. Do not prescribe unconditional interval doubling by the model when the runtime owns notification check-ins; runtime P4 owns that schedule. Keep the existing genuine-blocker audit.

The new paragraph also repairs an article-adjacent hazard: current text treats a missing handle as terminal (`ext/goal/templates/goals/continuation.md:24`), but handle loss after restart does not establish that a remote job has stopped.

### Q10. Other omissions and compatibility

**Budget:** usage subtracts cached input (`ext/goal/src/accounting.rs:527-531`). A 20M goal budget is not a 20M cap on the article's gross input; subscription-percentage conversion remains unknown. Preserve existing semantics, and measure both gross input and current goal-budget usage. A gross-input cap would need explicit accounting semantics and descendant/migration tests.

**Intermediate events:** terminal notifications do not report “needs help” while a job remains alive. A finite external watcher can exit on result/error/needs-input; otherwise paced interruptible polling is still needed. P6 remains deferred; if later required, reuse the subscription mechanism.

**Compatibility:** keep opt-in defaults, no invented goal status or core→goal dependency, correct foreign executor identity, and bounded model context. A process-query/read failure means unknown, never “no pending work.” Headless/code-mode constraints and tests are covered above/below.

Correct interim configuration (illustrative values, not a safe weekly-limit guarantee):

```toml
background_terminal_max_timeout = 1800000

[goals]
max_goal_token_budget = 20000000

[features]
sleep_tool = { mode = "always_on" }
```

This raises empty stdin's limit, not initial exec yield (`core/src/unified_exec/process_manager.rs:1013-1026`); it does not remove continuation spin or create notifications.

## 5. Recommended implementation series

Sizes estimate total changed lines including tests; split before exceeding 800 (prefer <500 for logic-heavy changes). First production consumer: **P1, then P5+P4a together**. Preparatory notification patches remain inactive until delivery and goal gating ship together.

| Order / patch | Principal files (relative to codex-rs) | Required tests | Size / risk |
|---|---|---|---|
| 1 — P1 | New tools/src/arguments.rs; typed wait/exec structs and schemas in core/src/tools/handlers | Adapter: decimal/exponent, signed/unsigned bounds, fractional rejection, duplicate keys, unchanged Value/f64. core/tests/suite: actual sleep/exec/stdin/native wait with decimal integers; direct + code-mode where exposed. | 250–450; medium |
| 2a — P5 state | New core/src/unified_exec/completion.rs; process_manager.rs; async_watcher.rs | Unit race matrix; core/tests/suite/unified_exec_process_events.rs: early exit, terminal stdin, delayed denial, cancellation. Preserve existing output events. | 350–600; high |
| 2b — P5 delivery | New core/src/session/async_input.rs and core/src/context/exec_completion.rs; controller/admission bridges | Inbox units; core/tests/suite/pending_input.rs/new exec_completion.rs: active/idle/reservation races, refusal, bursts, escaped bounds, shutdown and child ownership. | 450–700; high |
| 2c — P5+P4a activation | Exec handler/spec, host capability; new ext/goal/src/waiting.rs; runtime hooks; minimum conditional guidance | Core: acknowledge only supported subscriptions. Real app-server goal: no requests while pending, result wake after exit, queued user input works, opted-out server does not park goal. Headless/one-shot negative cases. | 400–700; high |
| 3 — P2 + full P3 | core/src/tools/spec_plan.rs; goal continuation template; local developer contributor | Registration + request integration: first user-created goal, nonclock model, hard disable, current-time branch, code-mode, stale remote catalog. | 150–300; low/medium |
| 4 — P4c native work | core/src/agent/control/completion.rs and fallback; wait-registration bridge; goal waiting module | Unit generations; core/tests/suite/subagent_notifications.rs/pending_input.rs; app-server two children, V1/V2, follow-up, interruption, paused/cleared parent and nonsubscriber. | 350–650; high |
| 5 — P4b | New ext/goal/src/scheduling.rs; accounting.rs; lifecycle/admission hooks | Fake-clock units: 0/1/2 nonwait calls, file change, stale tickets, floor/cap/check-in bypass. App-server text-only/one-poll loops and preserved 3-empty guard; core predecessor-admission integration. | 400–700; medium/high |
| Deferred — P6 / gross budget | No changes in this series | Add only for demonstrated need; preserve current budget meaning. | 0 now |

Prove **zero new model requests before a controlled exit** and a positive wake afterward; a permanently stalled model would otherwise pass. Narrow the gate in a mutation check (ignore an armed process with no stdout, or omit one awaited child), not only delete it. Test receipt/batch bounds at N/N+1 and record cases covered/total, with headless/crash bounds explicit.

Core primitive integration belongs in core/tests/suite; core cannot depend on its goal extension. Real goal+exec integration belongs in app-server tests, following `app-server/tests/suite/v2/thread_goal_empty_responses.rs:27-80`. Use auto-environment builders and controlled clocks/process barriers (`core/tests/common/test_codex.rs:541-561,600`), not sleep 60 or Unix-only kill loops.

Implementation checks: `just test -p codex-tools`, scoped `just test -p codex-core` suites, `just test -p codex-goal-extension`, relevant `codex-app-server`/`codex-exec` cases. Use nextest filters for bounded runs. Follow repository fmt/fix ordering after functional checks; no full workspace run is authorized here. Config/dependency changes require schema/Bazel lock updates under AGENTS.md.

## 6. Implementation bounds, evidence and logbook

No second research leaf:
- **Host eligibility:** establish the capability source in the first P5 integration test; otherwise retain blocking tools.
- **Admission/ack:** prove retained input through failed reservation and late abort. Prefer extending existing pending input if it satisfies the inbox invariant.
- **Output retention:** define read/ack/eviction with the receipt cap; test oversized output/full queue. No crash-durable promise.
- **Pacing:** measure requests; tool counters cannot prove semantic progress or detect every in-turn loop.
- **External milestones/budgets:** terminal notification is not a general remote event stream; existing budget is not gross input/subscription usage.

Logbook for coordinator import (outcome-scoped; no direct control-root edit):
- Worktree differs from pin; cited changed sources read from pinned Git blobs.
- Empty-final protection predates the article; native completion normally queues without waking.
- Rejected blanket numeric rewriting, global idle suppression and bool-only completion delivery.
- Headless shutdown and cached-input subtraction materially constrain the plan.
- Own coverage table preceded deliberate plan comparison; inlined primary plan prevented literal blind exposure.

Validation: static research, not production-tested. Tool readiness probes exited 0 (`.temp/TASK-260929-1srn2y/tool-readiness-01.log`). Some discovery probes failed on nonexistent candidate paths; corrected paths were subsequently read, and no absence claim relies on those failures. No build/test suite ran. Checks run: `git diff --exit-code` = 0; `git diff --check` = 0; artifact verifier = 0 (111 cited ranges across 61 pinned files; structure and <40,000-byte bound, not semantic proof). HEAD unchanged; no commit/push. Research and packaging took under 40 minutes of the 90-minute budget.
