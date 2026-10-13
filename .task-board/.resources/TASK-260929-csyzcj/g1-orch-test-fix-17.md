# Orchestrator test compile fix before precheck 17 (2026-10-13)

Hosted precheck 16 (run 38327475123, tree 8343519c) failed lint before any test lane:
`core/tests/suite/goal_native_wait.rs:1211:26: error[E0308]: mismatched types: expected Config, found Arc<Config>`.
`ThreadStartInput<'a, C>` is generic over `C`, so `&parent.config().await` (an `&Arc<Config>`) is not deref-coerced.

Fix (one line, rev6's new dense-path integration test): `config: &*parent.config().await,`.
`cargo fmt --check` exits 0; all 15 mutants in the rev6 mutants JSON still `git apply --check`. No local build or test.
Precheck 17 re-runs the full lanes and all 15 mutants on the fixed tree.
