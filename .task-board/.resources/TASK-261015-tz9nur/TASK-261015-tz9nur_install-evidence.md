# TASK-261015-tz9nur — side-by-side install evidence

- Installer: `.temp/goal-token-burn/impl/trial/install-codex-relux.sh <relux-build run id>`; downloads the build artifact,
  verifies the binaries (`codex: OK`, `codex-code-mode-host: OK`) into `~/.local/opt/codex-relux/<sha>/` and moves the
  `current` symlink.
- Installed builds: e063784 (run 38763975745) and f52f28f (run 38825757714); `current -> f52f28fa9cc2...`.
- Wrapper `~/.local/bin/codex-relux`:
  `CODEX_HOME="${CODEX_RELUX_HOME:-$HOME/.codex-relux}" exec "$HOME/.local/opt/codex-relux/current/bin/codex" "$@"`.
- Isolation check: every codex-relux session of 2026-10-16 (smoke 05:39, A/B 05:41 and 05:48 GMT+4) wrote its rollout
  under `~/.codex-relux/sessions/2026/10/16/`; `~/.codex/sessions/2026/10/16/` holds only the board's spawned
  official-codex runs (latest 04:07 GMT+4), none from codex-relux. auth for codex-relux is its own file in ~/.codex-relux.
- Live use: `codex-relux exec ... 'Reply with exactly: relux-ok'` -> `relux-ok`; TUI run -> `relux-tui-ok`
  (see BUG-261015-zoqjcm_post-landing-live.md).
- Baseline twin for A/B: `~/.local/bin/codex-base` (upstream 0462dcc) with CODEX_HOME `~/.codex-base`.
