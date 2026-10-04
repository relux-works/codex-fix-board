# Checkpoint preconditions — TASK-260929-u2i5rr (B1), accepted CR rev 6

Candidate tree: `4a456609f6f928d331d327e167114e71abade872`
HEAD: `0462dcc062b822bb8fff16cc31ce6eeab69823b9`
Branch: `task-board/story/STORY-260929-wg1ya0`

## 1. Worktree paths (exactly the 3 B1 paths)

```
 M codex-rs/core/src/unified_exec/mod.rs
?? codex-rs/core/src/unified_exec/completion_receipt.rs
?? codex-rs/core/src/unified_exec/completion_receipt_tests.rs
```

Command: `git status --short` — exit 0. No other modified, staged, or untracked paths.

## 2. Candidate tree match

Temporary-index `git write-tree` of the worktree (read-tree HEAD + add -A into
`GIT_INDEX_FILE` temp index, real index untouched):

```
4a456609f6f928d331d327e167114e71abade872
```

Matches the accepted CR-TASK-260929-u2i5rr-6 candidate tree exactly.

## 3. Integration route

B1 is NOT the Story's final leaf (B2 follows) — runner CHECKPOINTS after this run exits.
No file edits, no builds, no `task-board handoff`, no `worktree checkpoint/integrate` run here.
Board status left at `integrating` for the integration transaction.
