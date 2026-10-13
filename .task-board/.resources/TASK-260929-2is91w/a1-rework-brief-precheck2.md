# TASK-260929-2is91w (P3-1): hosted precheck 2 stopped at the lint gate. The tests do not compile. Fix, then request precheck 3

Production now compiles: the orchestrator's mechanical fix in `a1-orch-compile-fix.md` turned `.and_then(..).unwrap_or(false)` into
`.is_some_and(..)` in `exec_command_advertises_notify_on_exit`; keep it. The codex-core lib TEST target fails with 3 errors
(clippy --tests, ivanopcode/codex precheck 2):
1. `core/src/tools/waiting_capabilities_tests.rs:886:7`: error[E0428]: `excluded_exec_command_disables_exec_notify` is defined twice.
   Remove the duplicate, or rename one if they test different things. Keep exactly one test per behavior.
2. `waiting_capabilities_tests.rs:948:10` and `:975:10`: error[E0599]: there is no method `capture_step_context` on
   `session::session::Session`. Do not invent APIs. Find the real path that captures the final router and produces the
   snapshot (`core/src/session/mod.rs` around 3916-3966 and your `step_context.rs` changes), and drive the test through the
   existing production entry point or a real crate-visible helper that production also uses. Do NOT add a test-only method
   to the main implementation (AGENTS.md: avoid test-only functions in the implementation).
3. Clippy stops at the first failing crate, so more errors may be hiding. Re-read ALL your new and changed test code
   (waiting_capabilities_tests.rs, ext/extension-api/tests/waiting_capabilities.rs, ext/extension-api/tests/registry.rs,
   ext/goal/tests/steering.rs, core/src/session/tests.rs, core/tests/suite/exec_notification.rs) against the real
   signatures. For every function, method and type you call, open its definition and check the name, the visibility from the
   test module, the argument types and the return type. Remember the workspace denies clippy `expect_used` (test crates use
   `#![allow(clippy::expect_used)]` at the root, as their sibling targets do), `redundant_closure`, `needless_borrow`, and
   uninlined format args.
`mini-producer-addendum.md` applies (cargo fmt allowed and required; no other cargo). All 10 mutant patches must apply to your
final tree. Leave everything UNCOMMITTED, report the final tree id, add the note `HOSTED-PRECHECK-REQUESTED: precheck 3`, and end
your turn without handing off.
