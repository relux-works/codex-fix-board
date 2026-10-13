# TASK-260929-2is91w (P3-1): review rev4 not recordable. Attack the remote catalog configuration leg, then request precheck 12

All three rev4 panels accepted with zero findings (`TASK-260929-2is91w_review-verdict-rev4.md`), but the recording reviewer could
not record acceptance (`TASK-260929-2is91w_review-verdict-rev4-recorded-RUN-261011-804f63.md`): the board accepts only when every
surface row is held, and row `configuration coverage` (AC5) is `not-attacked`. 4/5 configuration families have router attacks;
the remote catalog leg does not. Every panel since rev1 has requested the same attack. Nothing else changes: keep every prior fix
and test exactly as it is (normalizer parity, server null-id discovery, provenance, the orchestrator test fix 10).

## Required

1. Integration test `remote_catalog_replacement_changes_waiting_snapshot` in `core/tests/suite/search_tool.rs` (or the suite that
   already hosts `discovered_native_wait_updates_waiting_capabilities`; the name must keep `waiting` so the filter selects it).
   Drive the REAL entry point: serve a remote models catalog from the mock server whose entry has the SAME slug as a bundled model
   and differs only in the clock/sleep tool support that `snapshot_follows_catalog_clock_support` toggles on a resolved
   `ModelInfo` today. Let `ModelsManager` fetch and apply it (`apply_remote_models`, same-slug replacement), start a real session
   on that slug, and assert from the captured step snapshot (the recording contributor pattern the suite already uses) that the
   flag follows the REMOTE entry, in both directions if the fixture allows (remote adds support the bundled entry lacks, and
   remote removes support the bundled entry has). Reuse existing remote-models test helpers (`rg -n "apply_remote_models|models
   endpoint|mount_models" core/tests`) rather than inventing new ones.
2. Mutant `snapshot_ignores_remote_catalog_replacement`: make the snapshot derivation (or the path that feeds it) keep the
   bundled entry instead of the remote replacement. It must be `git apply --check`-clean on the final tree; killer = the new
   test. If the only way to write it touches `ModelsManager` itself, say so in the results and keep it as narrow as possible.
3. Results: update the AC5 row to 5/5 configuration families with the test name; report the request count of the new test.

## Keep

All 14 existing mutants must still apply to the final tree. Hosted filter for precheck 12 = precheck 11's filter plus
`| test(remote_catalog)`.

`mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item` then `--check` exit 0; no other cargo; no
CODEX_HOME copies; delete temp dirs. Watch for redundant closures, uninlined format args, `vec!` where an array works, and
`/*param*/` comments on positional literals. Leave everything UNCOMMITTED, report the final tree id after fmt, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 12`, and end your turn without handing off.
