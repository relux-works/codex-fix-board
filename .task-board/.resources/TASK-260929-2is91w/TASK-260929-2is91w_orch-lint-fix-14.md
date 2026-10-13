# TASK-260929-2is91w: orchestrator lint fix before precheck 14

Precheck 13 (run 38187586739, tree eac03387) failed only the lint lane (mutants and other lanes did not run):
`core/tests/suite/search_tool.rs:1295: error: this MutexGuard is held across an await point` (clippy await_holding_lock) in
`remote_catalog_replacement_case`: the `captures` guard stayed alive across `get_remote_models().await` in the merge-proof block.

Fix (test-only, mechanical, no assertion change): the guard is scoped to a block that asserts the capture list is non-empty and
clones `captures[0]` (`WaitingCapabilities: Clone`); the comparison with `expected` uses the clone. fmt --check exit 0; all 15
mutants `git apply --check` clean. New tree afb8c830d764ba489a9f2f922c0babdf1dbe036e. Keep this change.
