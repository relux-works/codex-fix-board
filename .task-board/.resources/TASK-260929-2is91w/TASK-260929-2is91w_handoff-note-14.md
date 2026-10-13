# TASK-260929-2is91w: hand off the next CR revision on hosted precheck 14

Hosted precheck 14 (`TASK-260929-2is91w_hosted-precheck-14.md`, precondition, run 38191980780, ref relux/ci-next, tree
afb8c830) is green: lint, small, app-server, and core (core after one rerun of a guardian base flake, documented in the precheck
record). All 15 mutants are killed by their named tests.
It closes the review rev4 recording refusal: the `configuration coverage` (AC5) row was `not-attacked`
(`a1-rework-brief-review4.md`). The new integration test `remote_catalog_replacement_changes_waiting_snapshot` drives
`ModelsManager::apply_remote_models` through both the remote-only path (List cases) and the same-slug merge path (Hide cases,
with merge-proof assertions). It kills `snapshot_ignores_remote_catalog_replacement`.
That mutant survived precheck 12 because the test only reached the remote-only path (`a1-rework-brief-precheck12.md`; the
precheck-12 record's mutant summary predates that finding). The tree keeps both orchestrator fixes: test fix 10
(`TASK-260929-2is91w_orch-test-fix-10.md`) and lint fix 14 (`TASK-260929-2is91w_orch-lint-fix-14.md`, clippy
await_holding_lock in the new test, scoped guard, no assertion change). Mention both.
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 14 and the finding it closes. Refresh and re-attach `TASK-260929-2is91w_results.md`.
3. Run `task-board handoff TASK-260929-2is91w --role developer`.
