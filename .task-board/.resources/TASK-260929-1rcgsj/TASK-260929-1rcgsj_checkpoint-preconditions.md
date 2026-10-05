# TASK-260929-1rcgsj checkpoint preconditions (C1, CR rev 1)

CR: CR-TASK-260929-1rcgsj-1, revision 1
Candidate tree: 37fad741767c46d11094adb9be747d5aae83c145
Branch: task-board/story/STORY-260929-11jxjx
HEAD: 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47
Date (UTC): 2026-10-05

## 1. git status --short (exactly 9 C1 paths)

```
 M codex-rs/core/src/codex_thread.rs
 M codex-rs/core/src/session/input_queue.rs
 M codex-rs/core/src/session/mod.rs
 M codex-rs/core/src/session/turn_input_tests.rs
 M codex-rs/core/src/tasks/mod.rs
 M codex-rs/core/tests/suite/mod.rs
?? codex-rs/core/src/session/runtime_mailbox.rs
?? codex-rs/core/src/session/runtime_mailbox_tests.rs
?? codex-rs/core/tests/suite/runtime_mailbox.rs
```

Count: 9 lines (6 modified tracked + 3 untracked). No other paths.

## 2. Temporary-index write-tree

Commands (real index untouched):
```
TMPIDX=/tmp/TASK-260929-1rcgsj-checkpoint-index-<pid>
GIT_INDEX_FILE="$TMPIDX" git read-tree HEAD
GIT_INDEX_FILE="$TMPIDX" git add -A
GIT_INDEX_FILE="$TMPIDX" git write-tree
```

Output:
```
37fad741767c46d11094adb9be747d5aae83c145
exit=0
```

Expected: 37fad741767c46d11094adb9be747d5aae83c145 — MATCH.

## 3. Preconditions verdict

- Worktree tree equals accepted candidate tree: YES
- Status shows exactly the 9 C1 paths: YES
- No file edits made in this run: YES (read-only git checks)
- No builds run in this run: YES (per c1-checkpoint-note.md)
- No handoff / checkpoint / integrate invoked by producer: YES

Runner may checkpoint CR-TASK-260929-1rcgsj-1 onto the Story branch. C1 is not the Story final leaf (C2 TASK-260929-1ma0pr follows).
