# Checkpoint preconditions — TASK-260929-3r7peh (F1) CR rev 1

Candidate tree: dbd39ab8c59adabe27ebb25838003680214c8d14 (accepted CR-TASK-260929-3r7peh-1 rev 1)

## 1. git status --short (31 paths)

```
 M codex-rs/app-server/src/request_processors/thread_processor.rs
 M codex-rs/core/src/thread_manager.rs
 M codex-rs/core/src/thread_manager_tests.rs
 M codex-rs/core/src/tools/context.rs
 M codex-rs/core/src/tools/context_tests.rs
 M codex-rs/core/src/tools/handlers/mod.rs
 M codex-rs/core/src/tools/handlers/shell_spec.rs
 M codex-rs/core/src/tools/handlers/shell_spec_tests.rs
 M codex-rs/core/src/tools/handlers/unified_exec.rs
 M codex-rs/core/src/tools/handlers/unified_exec/exec_command.rs
 M codex-rs/core/src/tools/handlers/unified_exec_tests.rs
 M codex-rs/core/src/tools/spec_plan.rs
 M codex-rs/core/src/tools/spec_plan_tests.rs
 M codex-rs/core/src/unified_exec/async_watcher.rs
 M codex-rs/core/src/unified_exec/completion_receipt.rs
 M codex-rs/core/src/unified_exec/completion_receipt_tests.rs
 M codex-rs/core/src/unified_exec/mod_tests.rs
 M codex-rs/core/src/unified_exec/process_manager.rs
 M codex-rs/core/src/unified_exec/receipt_hooks.rs
 M codex-rs/core/src/unified_exec/receipt_hooks_tests.rs
 M codex-rs/core/src/unified_exec/receipt_output.rs
 M codex-rs/core/tests/suite/goal_background_wait.rs
 M codex-rs/core/tests/suite/mod.rs
 M codex-rs/ext/extension-api/src/lib.rs
 M codex-rs/ext/goal/src/extension.rs
 M codex-rs/ext/goal/tests/goal_extension_backend.rs
?? codex-rs/core/src/tools/handlers/unified_exec/exec_notification.rs
?? codex-rs/core/src/tools/handlers/unified_exec/exec_notification_tests.rs
?? codex-rs/core/tests/suite/exec_notification.rs
?? codex-rs/ext/extension-api/src/async_notification.rs
?? codex-rs/ext/goal/tests/goal_extension_backend/background_wait_activation_tests.rs
```
Count: 31. No other modified/untracked paths.

## 2. Temporary-index write-tree

```
TREE=dbd39ab8c59adabe27ebb25838003680214c8d14
EXPECTED=dbd39ab8c59adabe27ebb25838003680214c8d14
MATCH
```

Command: temp GIT_INDEX_FILE, `git read-tree HEAD`, `git add -A`, `git write-tree`. Exit 0.

## 3. Run discipline

No file edits, no builds, no handoff/checkpoint/integrate commands run. Board left at `integrating` for the runner to checkpoint.