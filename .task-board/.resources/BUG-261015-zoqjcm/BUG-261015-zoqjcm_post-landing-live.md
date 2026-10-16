# BUG-261015-zoqjcm — post-landing live verification (AC4)

Landed: ivanopcode/codex PR #22, relux/main = f52f28fa9cc273b0311b674b0e903e10f57d8540 (2026-10-16T01:36:43Z).
Build: relux-build run 38825757714, installed as ~/.local/opt/codex-relux/current -> f52f28f.

| Check | Command | Result |
|---|---|---|
| exec smoke | `codex-relux exec --skip-git-repo-check -m gpt-6-astra 'Reply with exactly: relux-ok'` | `relux-ok`, 9,455 tokens, no 400 |
| live TUI + tool call | tmux `ab-relux`: `codex-relux --no-daemon -m gpt-6-astra 'Run the shell command: echo tui-alive. Then reply with exactly: relux-tui-ok'` | ran `echo tui-alive`, replied `relux-tui-ok` in 8s, no 400 |

Before the fix the same e063784 build returned 400 "Function 'collaboration.wait_agent' is reserved for use by this model and must match the configured schema" on every request.

Open risk from the bugfix (P5 `notify_on_exit` on `exec_command` in TUI-capable hosts): the live TUI request with a
tool call was accepted. The rollout does not record the advertised tool specs, so whether `notify_on_exit` was in that
request is not proven here; the TUI is the only host path that enables it, and no 400 appeared. Revisit only if a
reserved-schema 400 shows up on exec_command.
