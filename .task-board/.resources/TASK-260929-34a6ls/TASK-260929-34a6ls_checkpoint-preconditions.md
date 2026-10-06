# TASK-260929-34a6ls checkpoint preconditions (CR rev 3, accepted)

Candidate tree: 62aecbc1f279a26c154f0e371b8c1995bb7e8226
Accepted CR: CR-TASK-260929-34a6ls-3
Run: RUN-261006-08b09d (integration/checkpoint run, no edits, no builds)

## 1. `git status --short` — exactly the 11 D1 paths

```
M codex-rs/core/src/codex_thread.rs
M codex-rs/core/src/hook_runtime.rs
M codex-rs/core/src/session/input_queue.rs
M codex-rs/core/src/session/mod.rs
M codex-rs/core/src/session/runtime_mailbox.rs
M codex-rs/core/src/session/runtime_mailbox_tests.rs
M codex-rs/core/src/session/turn.rs
M codex-rs/core/src/tasks/mod.rs
M codex-rs/core/tests/suite/exec_completion.rs
?? codex-rs/core/src/session/exec_completion_ack.rs
?? codex-rs/core/src/session/exec_completion_ack_tests.rs
```

9 modified + 2 new = 11 paths. No other entries.

Branch: task-board/story/STORY-260929-3bvsxx
HEAD: 4a27941d38 relux-ci: run codex-queue-extension in the small and lint lanes

## 2. Temporary-index `git write-tree` equals the accepted tree

```
62aecbc1f279a26c154f0e371b8c1995bb7e8226
expected=62aecbc1f279a26c154f0e371b8c1995bb7e8226
```

MATCH. The uncommitted worktree is exactly the accepted CR rev 3 candidate.

## 3. Board status

TASK-260929-34a6ls status: integrating (left untouched for the runner's landing transaction).
