# Checkpoint preconditions — TASK-260929-2fa1hy (G1), accepted CR rev 1

Integration run, 2026-10-02. No file edits, no builds. Candidate tree `403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd` (CR-TASK-260929-2fa1hy-1).

## 1. Worktree status — exactly the 5 G1 paths

`git status --short` (HEAD `ea8899e6f97aea64136159286840c28c955243e8`):

```text
M codex-rs/core/src/tools/spec_plan.rs
M codex-rs/core/tests/suite/current_time_reminder.rs
M codex-rs/ext/extension-api/src/lib.rs
M codex-rs/ext/extension-api/tests/state.rs
?? codex-rs/ext/extension-api/src/goal_activity.rs
```

4 modified tracked files + 1 new untracked file (`goal_activity.rs`) = 5 G1 paths. Nothing else dirty.

## 2. Worktree tree hash matches the accepted candidate

Temporary-index `git read-tree HEAD` + `git add -A` + `git write-tree`:

```text
worktree-tree: 403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd
expected:      403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd
```

MATCH. Real index untouched (temporary `GIT_INDEX_FILE`, removed afterwards).

## 3. Diff stat (tracked files; untracked goal_activity.rs excluded by git)

```text
codex-rs/core/src/tools/spec_plan.rs               |  10 +-
codex-rs/core/tests/suite/current_time_reminder.rs | 240 +++++++++++++++++++++
codex-rs/ext/extension-api/src/lib.rs              |   3 +
codex-rs/ext/extension-api/tests/state.rs          |  15 ++
4 files changed, 267 insertions(+), 1 deletion(-)
```

## Conclusion

Both checkpoint preconditions hold: exactly the 5 G1 paths are present and the worktree tree equals the accepted CR rev 1 candidate tree. Ready for the runner to checkpoint onto the Story branch. No `handoff` / `checkpoint` / `integrate` invoked by this run.
