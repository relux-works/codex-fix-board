# TASK-260929-2is91w: orchestrator compile fix before precheck 2

macmini_codex-fix_orch, 2026-10-10. Precheck 1 (ivanopcode run 38020764336) stopped at the lint gate on one error:
`core/src/tools/waiting_capabilities.rs:121:41: error[E0308]: expected Option<_>, found bool` in
`exec_command_advertises_notify_on_exit`. The closure returns bool, so `.and_then(..).unwrap_or(false)` became `.is_some_and(..)`
(same semantics; an absent exec_command still yields false). Mechanical, no behavior change; cargo fmt --check exit 0.
Clippy aborted at that first error, so later crates were not checked yet.

Second orchestrator edit (precheck 3, lint): the producer reported fmt clean, but CI and local `cargo fmt --check` both flagged waiting_capabilities_tests.rs:49 (a JsonSchema::object call that fits on one line). I ran `cargo fmt`; whitespace only.
