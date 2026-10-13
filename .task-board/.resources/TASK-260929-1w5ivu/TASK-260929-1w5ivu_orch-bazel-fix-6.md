# TASK-260929-1w5ivu: orchestrator fix for review-2 A2-F1 (Bazel compile data), before precheck 6

Review rev2 (`TASK-260929-1w5ivu_review-verdict-rev2.md`) is changes_requested on one finding:
- **A2-F1 (regression, placement and size).** `ext/goal/tests/waiting_world_state.rs:11` includes `../src/waiting_world_state.rs`
  through `#[path]`. Bazel builds each integration test with `compile_data = integration_test_files +
  integration_compile_data_extra` (`defs.bzl`). For this crate that list holds `accounting.rs`, `activity.rs` and
  `steering.rs` only, so the Bazel test target cannot read the new file. Cargo is unaffected, and hosted relux-ci does not
  run Bazel, which is why precheck 5 could not see it.

Fix (one line, mechanical): `ext/goal/BUILD.bazel` now also lists `"src/waiting_world_state.rs"` in
`integration_compile_data_extra`, next to the other `#[path]`-included sources. Same class elsewhere in the delta: no other
new `#[path]` include of a `src/` file. The new core suite module is a plain `mod` under `core/tests/suite`, which the
crate's `tests/**` glob already covers. No `include_str!`/`include_bytes!` was added.

A2-N1 (note, not blocking): results.md claimed a serialized snapshot of at most 512 B in the worst case. That holds only for
ASCII names. A name capped at 128 four-byte characters plus the ellipsis gives about 602 B. The fragment bounds (3 KiB /
1,000 tokens) are unaffected. The producer corrects the results text at handoff; no code change.

`cargo fmt --check` exit 0, `git diff --check` clean, all 8 mutants still apply. New candidate tree
`0909471501a910f604164a2bba7b586e2ebf9ba8`.
