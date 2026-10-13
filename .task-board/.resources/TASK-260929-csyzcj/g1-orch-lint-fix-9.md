# TASK-260929-csyzcj: orchestrator lint fix before precheck 10

macmini_codex-fix_orch, 2026-10-10. Precheck 9 (ivanopcode) stopped at the lint gate on one clippy warning:
`core/src/context/inter_agent_interrupted_message.rs:26: constant INTERRUPTED_MESSAGE_MAX_BYTES is never used` (lib build; only the tests used it).
Fix: `body()` now binds the rendered string and `debug_assert!(body.len() <= INTERRUPTED_MESSAGE_MAX_BYTES)` before returning it, so the stated hard cap is also enforced in debug builds. Output is unchanged; cargo fmt --check exit 0.

The edit shifted the body() lines, so the orchestrator regenerated two mutant patches (same mutation, new context): interrupted_claims_success and interrupted_sender_path_uncapped. CI uses impl/p4c/g1-mutants-10.json; all 8 apply.
