# Goal-mode token burn: patch plan for upstream openai/codex

- Source article: https://relux.works/en/blog/codex-goal-token-burn/
- Upstream base inspected: `33a0f766a6` (main, 2026-09-28)
- Reference fork: tekacs/codex `9ffcf8db` (background exec completion wake)
- Status: research only, nothing implemented or built yet.

## 1. Article problems vs. current upstream state

| # | Problem (article) | Upstream state at 33a0f76 | Evidence |
|---|---|---|---|
| A | Goal continuation restarts ~30ms after idle, no backoff | Still true. `on_thread_idle` -> `continue_if_idle` -> `start_turn_if_idle` immediately | `ext/goal/src/extension.rs` (`on_thread_idle`), `ext/goal/src/runtime.rs:425` |
| A' | "No counter of empty continuations" | Partially fixed by #44320 (2026-09-09): goal is blocked after 3 consecutive *fully empty* automatic turns. A polling turn (one `ps`/`tail` + "still running") counts as activity, so the spin loop is not caught | `ext/goal/src/accounting.rs:163-230` |
| B | `clock.sleep` only for `gpt-6-astra` | Widened: `clock` now on `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna`. Still absent on `gpt-5.6-*`, `gpt-5.5`, daybreak, and every custom-provider model (empty `experimental_supported_tools`) | `models-manager/models.json`, `core/src/tools/spec_plan.rs:1225-1245` |
| C | Contract: a wait only counts if a live process was polled | Still true | `ext/goal/templates/goals/continuation.md:24` |
| D | `60000.0` rejected (`invalid type: floating point, expected u64/i32`) | Still true. All handlers go through `serde_json::from_str` directly. `clock.sleep` even advertises `duration_ms` as JSON `number` but deserializes `u64` | `core/src/tools/handlers/mod.rs:86` (`parse_arguments`, 57 call sites), `core/src/tools/handlers/sleep.rs` |
| E | exec yield capped at 30s | Still true: `MAX_YIELD_TIME_MS = 30_000`; empty `write_stdin` may wait up to `background_terminal_max_timeout` (default 300_000, configurable) | `core/src/unified_exec/mod.rs:73-78`, `process_manager.rs:1018` |
| F | No completion notification for background exec | Still true upstream (tekacs fork has one) | `core/src/unified_exec/async_watcher.rs` `spawn_exit_watcher` only emits `ExecCommandEnd` UI event |
| G | gpt-5.5 prompt: "Do not end your turn while `exec_command` sessions ... are still running" | Still true | `models-manager/models.json` (gpt-5.5 instructions) |
| H | `wait_agent` can't see plain child processes; no N-process barrier | Still true | `core/src/tools/handlers/multi_agents_spec.rs` |
| I | No goal token budget by default | Already configurable: `max_goal_token_budget` is both the cap and the default for new goals | `config/src/config_toml.rs:724` -> config only, no patch needed |

## 2. Patch series (ordered by value / risk)

### P1. Accept integral floats in tool arguments (fixes D, unblocks E for custom providers)

- File: `core/src/tools/handlers/mod.rs` `parse_arguments`.
- Change: parse to `serde_json::Value`, recursively replace every `Number` that is a finite f64 with zero fraction and `|x| <= 2^53` by an integer `Number` (u64 if >= 0, else i64), then `serde_json::from_value::<T>`. Keep the same error prefix.
- Safe for real float fields (serde accepts integers for f64). `deny_unknown_fields` still enforced by `from_value`.
- Optionally also: `sleep.rs` schema `JsonSchema::number` -> integer, so models stop emitting floats in the first place.
- Also covers `wait_agent` `timeout_ms` (i64) and any other integer args.
- Tests: `SleepArgs {duration_ms: 60000.0}`, write_stdin `yield_time_ms: 36429.0`, exec `yield_time_ms: 10000.0`, non-integral `1.5` still rejected for integer fields, float field keeps working.

### P2. Register `clock.sleep` for goal turns regardless of model catalog (fixes B)

- File: `core/src/tools/spec_plan.rs:1234-1250`.
- Precise variant: add `|| is_goal_turn` to the `SleepToolMode::ModelDriven` arm, where `is_goal_turn` = turn trigger is `"goal"`. The goal extension already starts continuations with `turn_trigger: Some("goal")` (`runtime.rs:482`), and `TurnMetadataState::set_turn_trigger` runs before the task starts (`session/turn_input.rs`). Needs a `pub(crate)` getter on `TurnMetadataState` (`turn_metadata.rs:190` is private today).
- Keeps `features.sleep_tool.enabled = false` as the hard off switch.
- Covers custom providers (their catalog entry is empty).
- Weaker alternative (article): default `SleepToolMode::AlwaysOn` when `Feature::Goals` is enabled; simpler but changes non-goal sessions too.

### P3. Rewrite the continuation contract (fixes C)

- File: `ext/goal/templates/goals/continuation.md` (line 24 "A verified wait ...").
- New semantics:
  - A verified wait is any *blocking* wait on a concrete handle confirmed live now: `clock.sleep`, an empty `write_stdin` with a long `yield_time_ms`, `wait_agent`, or ending the turn while a yielded background `exec_command` is pending (its completion notification will resume the goal, after P5).
  - When the only remaining work is waiting, do not issue short liveness checks (`ps`, `pgrep`, `tail`, empty 250ms `write_stdin`). Pick one long blocking wait; if a previous wait found the job still running, at least double the next wait.
  - Keep the rule that stale conversation/lock files are not evidence.
- Must stay consistent with P2 (tool exists) and P5 (notification exists), otherwise the model is told to use tools it doesn't have.

### P4. Continuation gating + backoff in the goal runtime (fixes A)

Two parts, both in `ext/goal/src/runtime.rs` `continue_if_idle` (+ accounting fields):

a. Defer while background work is pending. If the thread owns live yielded unified-exec processes, skip starting the continuation: P5 wakes the thread on completion, and the goal continues after that turn goes idle. Needs a thread-level query, e.g. `CodexThread::has_live_background_processes()` backed by `UnifiedExecProcessManager::list_processes()` (`process_manager.rs:1824`). Add a fallback timer (e.g. 30 min) that re-runs `continue_if_idle` so a hung process can't park the goal forever.

b. Exponential backoff for low-activity automatic turns. Extend `GoalAccountingInner` with `consecutive_low_activity_turns`: an automatic goal turn with no `FileChange`, no plan change, and at most one tool call (or only wait tools) increments it; anything else resets it. `continue_if_idle` then schedules the continuation after `min(30s * 2^(n-1), 30min)` via `tokio::spawn(sleep; continue_if_idle)` instead of starting immediately. The delayed call re-validates goal status and idleness (`start_turn_if_idle` already rejects if not idle), so user input or an exec completion naturally pre-empts it. Optional cap: after K backoff steps without progress, mark the goal `blocked` with a clear reason (mirrors Claude Code's "max check-ins without a human").

Data needed is already recorded: `record_item` and `record_tool_outcome` in `accounting.rs`.

### P5. Background exec completion notification (fixes F; port of tekacs 9ffcf8d)

- `unified_exec/mod.rs` `ProcessEntry`: add `wake_on_exit: Arc<AtomicBool>`.
- `process_manager.rs`: set it when a call returns `ProcessStatus::Alive` (both `exec_command` yield and `write_stdin` poll), leave it false when the terminal result was returned inline (no duplicates).
- `async_watcher.rs` `spawn_exit_watcher`: when the flag is set, build an `<exec-command-completed call-id process-id exit-code>` fragment with truncated output (new `context/exec_completion.rs`, `ContextualUserFragment`) and deliver it.
- Delivery on upstream (fork's `Session::inject_or_start` does not exist here): `session.inject_if_running(items)`; on `Err(items)` resolve the `CodexThread` via `session.services.agent_control` runtime `get_thread(thread_id)` (same pattern as `agent/control.rs:159-170`) and call `start_turn_if_idle` with `turn_trigger: "exec_completion"`. This goes through the submission loop, respects execution capacity, and is rejected cleanly if a turn started meanwhile (then retry `inject_if_running` once).
- Update `exec_command` / `write_stdin` tool descriptions (`tools/handlers/shell_spec.rs`) the same way the fork did, and drop the gpt-5.5 "Do not end your turn while exec_command ..." line in `models.json`. Verify whether the remote model catalog overrides bundled `base_instructions`; if it does, the tool descriptions are the reliable channel.

### P6 (optional). Multi-process barrier (fixes H)

With P5 + P4a each background process produces exactly one wake, so N processes cost N turns instead of a polling loop. A dedicated `exec_wait {session_ids, mode: any|all, timeout_ms}` tool (input-interruptible like `clock.sleep`, capped by `background_terminal_max_timeout`) is only needed if in-turn blocking on several processes is still wanted.

### Config-only (no patch)

```toml
max_goal_token_budget = 20000000      # default + cap per goal (I)
background_terminal_max_timeout = 1800000  # allow 30-min empty write_stdin waits (E)

[features.sleep_tool]
mode = "always_on"                    # interim workaround for B until P2 lands
```

## 3. Expected effect

The article's formula is `waiting cost = number of checks x context size`. P1-P3 cut the check frequency when the model can block (article: gpt-6-astra with sleep 10-15M tokens/h vs 83-188M/h without). P4a + P5 remove checks entirely for exec-backed waits (one turn per completion). P4b bounds everything else.

## 4. Validation plan

- Unit: P1 parse tests; P2 `spec_plan` test that a `turn_trigger = "goal"` turn on a model without `clock` gets `clock.sleep`; P4 accounting tests for counter/backoff schedule; P5 tests ported from the fork (`mod_tests.rs`, `async_watcher_tests.rs`) plus idle-wake test.
- Integration: `core/tests/suite` goal scenario with a mock model that yields a `sleep 60` exec and ends the turn; assert no continuation starts before process exit and exactly one wake after.
- Commands: `cargo test -p codex-core`, `cargo test -p codex-goal-extension` (check crate names in `Cargo.toml`), `just fmt` / `just fix -p ...` per repo AGENTS.md.
