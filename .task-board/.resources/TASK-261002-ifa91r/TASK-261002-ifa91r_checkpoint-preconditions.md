# Checkpoint preconditions — TASK-261002-ifa91r (accepted CR rev 1)

Candidate tree (accepted): `5c365d9a68ea6d2cee0488eb58a37a539ce354d4`
Run: RUN-261002-0dcb68 (integration/checkpoint run, no file edits, no builds)

## 1. `git status --short` — exactly the two astra snapshot files modified

```
 M codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_kickoff_remote_compaction_windows.snap
 M codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_plugin_refresh.snap
```

HEAD: `35af013b90 Accept integral decimal integers in waiting-tool arguments`

## 2. `git diff --stat` / `--numstat` — 12 insertions, 12 deletions, nothing else

```
 ...__scenarios__astra_kickoff_remote_compaction_windows.snap | 12 ++++++------
 .../all__suite__scenarios__astra_plugin_refresh.snap         | 12 ++++++------
 2 files changed, 12 insertions(+), 12 deletions(-)
```

```
6	6	codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_kickoff_remote_compaction_windows.snap
6	6	codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_plugin_refresh.snap
```

## 3. Temporary-index `git write-tree` (HEAD + worktree changes)

```
5c365d9a68ea6d2cee0488eb58a37a539ce354d4
```

Matches the accepted candidate tree `5c365d9a68ea6d2cee0488eb58a37a539ce354d4`. Exit 0.

## Conclusion

Both checkpoint preconditions hold: the worktree contains exactly the two
modified astra snapshot files (6/6 lines each), and the worktree tree equals
the accepted CR-TASK-261002-ifa91r-1 candidate tree. Ready for the runner to
checkpoint onto the Story branch.
