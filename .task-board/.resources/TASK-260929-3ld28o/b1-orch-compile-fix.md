# TASK-260929-3ld28o: orchestrator compile fix before precheck 2

macmini_codex-fix_orch, 2026-10-10. Precheck 1 (ivanopcode run 38012056631) stopped at the lint gate on ONE compile error:
`ext/goal/tests/state_change_observations.rs:155:65: error[E0382]: borrow of moved value: status` (test
`failed_or_declined_file_change_does_not_set`; the value is moved into `file_change_item(status)`, then formatted in the assert
message). Test-only mechanical fix: render `let label = format!("{status:?}");` before the move and use `{label}` in the
message. No behavior change. New tree: 97244aaf4273df0b38f550b57cc07093a91b30cd (cargo fmt --check exit 0).
Note: clippy aborted at that first error, so later crates were not checked; precheck 2 will show the rest.

Second orchestrator edit (precheck 3, ivanopcode run 38013054180, lint): clippy `expect_used` (workspace deny) at state_change_observations.rs:109 in the new test target. Added `#![allow(clippy::expect_used)]` at the crate root, the convention of the sibling targets goal_extension_backend.rs and activity_publisher.rs. Test-only.
