# TASK-260929-1w5ivu: orchestrator fix before precheck 5 (World State snapshot never compared equal)

Precheck 4 (run 38256663093, tree bae5da77) passed lint, small and app-server. Core failed on exactly 9 of the 11
`waiting_guidance` suite tests; the other 5133 core tests passed (one known-flaky hooks test passed on retry). Every failure
counted one guidance fragment too many, for example `EXEC_NEGATIVE_MARKER` 2 instead of 1 on a single-request turn, and the
goal-stop test saw 3 instead of 1.

Cause: `waiting_guidance_snapshot` wrote `"native_wait": null` when no native wait tool is callable. Core's
`ExtensionWorldStateSection::snapshot` (`core/src/context/world_state/mod.rs`, `remove_null_object_fields`) strips null object
fields before it persists the snapshot, because merge-patch reserves null for deletion. So the restored
`PreviousWorldStateSection::Known(previous)` never equalled the fresh snapshot, and the active arm re-rendered the full
fragment on every sampling step: once at turn start and again at the first step. The two tests that passed are exactly the
ones without a null field: the non-goal thread (no section) and the discovered-native-wait test (name present).

Fix (2 hunks, no behaviour change other than the bug):
- `ext/goal/src/waiting_world_state.rs`: an absent native wait is now omitted from the snapshot instead of written as null.
  The doc comment says why.
- `ext/goal/tests/waiting_world_state.rs`: the snapshot unit test that pinned `"native_wait": Value::Null` now pins the
  field as absent, and its comment says why.

No suite assertion changed. `cargo fmt --check` exit 0; all 8 mutants still apply cleanly. New candidate tree
`786339645058198ba030dffbba8ed1cfbf1e36a9`.

Reviewer note: the unit tests compared the contribution's own unstripped snapshot against itself, so they could not see the
persistence round-trip. Only the suite (real core persistence) caught it, which is the integration coverage AC6 asks for.
