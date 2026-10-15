# TASK-261015-hoafpy: small-lane-protocol-rollout

## Description
Land relux/ci-next commit 9f8fdf9 on relux/main: the relux-ci small lane and the small mutant lane also run -p codex-protocol -p codex-rollout, because mutants in protocol/ and rollout/ survived when no lane ran those crates. Precheck workflow runs have been dispatched from relux/ci-next with this change since 2026-10-12. Fork-only CI change.

## Scope
(define task scope)

## Acceptance Criteria
AC1 relux-ci.yml on relux/main runs codex-protocol and codex-rollout in the small snapshot lane and the small mutant lane. AC2 relux-ci on the landing head is green (small lane passes with the two added crates). AC3 Landed as a signed commit via PR, fast-forward.
