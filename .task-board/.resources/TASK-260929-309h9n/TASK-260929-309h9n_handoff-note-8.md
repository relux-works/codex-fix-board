# TASK-260929-309h9n: hand off the next CR revision on hosted precheck 8

Hosted precheck 8 (`TASK-260929-309h9n_hosted-precheck-8.md`, precondition, run 38217778118, ref relux/ci-next, tree eb655488)
is fully green, with all 7 mutants killed by their named tests. It closes review rev2 finding A2-F1 and the same-row notes D-N2
and B2-N2: the ambient `CODEX_GOAL_PACING_DISABLED` switch is gone (grep empty). Pacing is now the explicit production policy
`[features] goal_continuation_pacing` (Stable, on by default). It is read at thread start through
`GoalExtensionConfig.continuation_pacing`, and the new mutant `pacing_feature_flag_ignored` is killed. The P4a core fixture runs
with pacing off (B2-N1 hardening).
Precheck 7 (run 38216547888) failed to compile (E0382, moved `config`). The tree keeps the orchestrator's mechanical fix
`TASK-260929-309h9n_orch-lint-fix-8.md`; mention it.
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 8 and the findings it closes. Refresh and re-attach `TASK-260929-309h9n_results.md`, including the production-policy bounds paragraph (default on, the flag restores immediate continuations, read at thread start only).
3. Run `task-board handoff TASK-260929-309h9n --role developer`.
