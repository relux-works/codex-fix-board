# TASK-261015-tz9nur: side-by-side-install

## Description
Install the artifact under ~/.local/opt/codex-relux with a codex-relux wrapper that sets CODEX_HOME=~/.codex-relux, so it never touches the official ~/.codex state, auth or sqlite DBs.

## Scope
(define task scope)

## Acceptance Criteria
AC1 codex-relux --version runs. AC2 official codex is unchanged. AC3 separate login, minimal config.
