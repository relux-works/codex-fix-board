# Prior analysis: does tekacs/codex 9ffcf8d fix the goal-mode token burn?

Author: primary orchestrator session (Claude Opus 5.5), 2026-09-29. Static reading only: the fork was cloned at
`9ffcf8d` (parent `ba573b4`) and diffed against its own goal extension. Nothing was built or run.

## Verdict

No. The commit fixes a neighbouring defect (in-turn empty polling of background `exec_command` sessions in
ordinary, non-goal sessions) and adds a correct completion-notification primitive, but it does not touch the
goal continuation loop that the article identifies as the root cause.

## What the commit does

1. `wake_on_exit: Arc<AtomicBool>` on `ProcessEntry`; set when `exec_command`/`write_stdin` returns
   `ProcessStatus::Alive`. `spawn_exit_watcher` then builds an `<exec-command-completed call-id process-id
   exit-code>` fragment (output truncated to 8k tokens) and calls `Session::inject_or_start`: inject into the
   active turn, or start a `RegularTask` turn when idle. Duplicate suppressed when the result was returned inline.
2. `exec_command` / `write_stdin` tool descriptions: do not poll, wait for the runtime completion notification,
   end the turn if nothing else to do.
3. `models.json` (gpt-5.5): "Do not end your turn while exec_command sessions ... are still running" replaced by
   fire-and-yield guidance.

## Why the article's defect remains (checked in the fork's code)

| Article cause | In fork 9ffcf8d |
|---|---|
| `on_thread_idle` -> `continue_if_idle()` immediately, 0.02-0.05s, no backoff | Untouched: `ext/goal/src/extension.rs:175`, `ext/goal/src/runtime.rs:399`. `emit_thread_idle_lifecycle_if_idle` (`core/src/tasks/lifecycle.rs`) does not consider live background processes. The only deferral (`thread_goal_continuation_deferrals`) is inserted when a goal is copied on thread fork. |
| Contract: a verified wait must poll a live handle | Untouched: `continuation.md` "A verified wait polls a specific process, session, job, or tool handle confirmed live now." |
| `clock.sleep` gated by model catalog | Untouched: `core/src/tools/spec_plan.rs:1212` |
| Float args rejected | Untouched |

Resulting behaviour in goal mode with the fork: model yields a long command and ends its turn as the new prompt
says; ~30ms later the goal extension starts a continuation whose contract demands polling. The model either
polls (spin continues) or obeys the tool guidance and ends the turn immediately, producing an idle ->
continuation -> empty turn -> idle loop. Each continuation still rereads the full context, so the article's
"checks x context size" cost is unchanged; only output tokens shrink. (Upstream later added a "block goal after
3 fully empty automatic turns" rule, #44320, which would eventually stop the pure-empty variant, but not the
one-poll-per-turn variant.)

## What the fork got right (worth porting)

The completion notification is exactly the Claude Code style "await" the article recommends. Missing piece:
the goal extension must *wait for it* (not start continuations while such processes are pending), and the
contract must accept "ended the turn while a notified background process is pending" as a verified wait.
