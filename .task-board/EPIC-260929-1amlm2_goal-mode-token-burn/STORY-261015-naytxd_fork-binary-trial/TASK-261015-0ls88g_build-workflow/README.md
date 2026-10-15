# TASK-261015-0ls88g: build-workflow

## Description
Add .github/workflows/relux-build.yml: hosted macos-15 arm64 release build of codex and codex-code-mode-host at an exact sha, uploaded as an artifact. Land via PR.

## Scope
(define task scope)

## Acceptance Criteria
AC1 workflow builds the exact requested sha and verifies HEAD. AC2 artifact contains codex and codex-code-mode-host for aarch64-apple-darwin plus the source sha. AC3 landed signed via PR.
