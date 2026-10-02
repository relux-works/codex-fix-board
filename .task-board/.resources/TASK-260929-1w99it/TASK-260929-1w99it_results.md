# TASK-260929-1w99it — accepted revision 6 revalidation

## Summary

Revision 6's accepted `codex-tools` candidate was revalidated without changing its source. The exact accepted patch still reverse-applies cleanly to this worktree after formatting, clippy/fix, and restoration of the temporary mutant. The crate suite passed 121/121 tests; all 11 adapter tests passed.

The task remains `integrating`. This producer run did not commit, checkpoint, integrate, call generic `handoff`, or change status. The bound runner owns the synchronous landing action after this run exits.

## Landing preconditions checked

- The first required status mutation returned `old_value=integrating`, `new_value=integrating` (idempotent).
- `task-board worktree obligations` reported revision 6 `accepted`, needing `checkpoint`.
- `task-board worktree integrating` classified the candidate as `awaiting_landing`, with a present repository delta and candidate tree not yet on `refs/heads/relux/main` (`0462dcc062b822bb8fff16cc31ce6eeab69823b9`).
- `task-board worktree status STORY-260929-2urftk` reported the workspace lease held by this run and exactly three candidate paths. The Story branch remains at the recorded base commit; no producer commit was created.
- `git apply --reverse --check` against the accepted revision 6 patch exited 0 before and after validation. After the temporary mutant was restored, `cmp -s` against the saved source copy also exited 0.
- The worktree integration view reports board debt as indeterminate because the task-board directory is outside the repository control root. This producer did not attempt a landing command; the assigned runner owns that transaction and any typed refusal.

## Candidate paths and scope

- `codex-rs/tools/src/arguments.rs` — exact RawValue-based integer adapters and parser.
- `codex-rs/tools/src/arguments_tests.rs` — sibling tests registered with `#[path]`.
- `codex-rs/tools/src/lib.rs` — public module export.

The accepted patch is 774 lines across these three paths (491 implementation, 282 tests, one export), within the task's 800-line ceiling. `tools/Cargo.toml` already enables `serde_json/raw_value`; no dependency, lockfile, schema, handler, or other crate changes are present. `arguments.rs` contains no `f64` or `serde_json::Value` intermediary; the bounded `rg` check returned exit 1 because there were no matches.

## Acceptance-criteria coverage

Coverage ratio: **6 of 6 AC rows driven**. Tests deserialize derived structs through `serde_json::from_str` and field-level `deserialize_with`, reaching the public adapters and their RawValue parser.

| AC | Driving test | Refusal test | Production path |
|---|---|---|---|
| 1. Integral decimal/exponent and integer forms for all targets | `integer_valued_decimals_and_exponents_decode_exactly_for_all_targets` | `fractional_and_rounded_numeric_lexemes_are_refused_for_every_target` | `arguments::{u64,i64,i32,usize}::deserialize` → `deserialize_required` → `parse_raw_integer` / `parse_number` |
| 2. Negative zero and signed negatives | `negative_zero_and_negative_integers_decode_for_signed_targets` | `unsigned_targets_refuse_negative_nonzero_values` | Required signed/unsigned adapters → exact sign/magnitude conversion |
| 3. Exact values above 2^53 and destination boundaries | `exact_large_integers_and_destination_boundaries_are_preserved` | `integer_overflow_is_refused_for_each_destination` | Required adapters → checked `u64` magnitude and destination conversion |
| 4. Option null, omission, defaults, and integer values | `optional_integer_adapters_preserve_null_omission_and_serde_defaults` | `optional_integer_adapters_reject_strings_and_booleans`; `invalid_json_types_keep_serde_invalid_type_errors` | `arguments::option_*::deserialize` → `deserialize_option` |
| 5. Bounded exponent handling | `integer_valued_decimals_and_exponents_decode_exactly_for_all_targets` | `pathological_exponents_and_long_digit_inputs_are_refused` | Required/optional adapters → checked exponent digit accumulation; no exponent-sized allocation |
| 6. Duplicate-field behavior | `integer_valued_decimals_and_exponents_decode_exactly_for_all_targets` | `duplicate_annotated_fields_keep_serde_rejection` | Containing struct's normal Serde field deserializer |

No AC input is declared out of contract. Consumer handler wiring is excluded by the task Scope clause, “No handler wiring (that is the sibling leaf)”; the adapter input contract is JSON numeric lexemes per the task Description. These exclusions waive no AC1–AC6 behavior.

## Surface coverage and mutant evidence

Surface coverage ratio: **1 of 1 surface-table rows attacked**. The attached `TASK-260929-1w99it_coverage-map.md` maps `text grammar` to all 11 adapter tests and the narrowing mutant.

| Mutant | What it narrows the gate to | Named test that fails | Result |
|---|---|---|---|
| `admit_exact_1.5` | Adds a branch in `parse_number` that accepts only raw lexeme `1.5` as integer `1`; all other fraction checks remain active | `arguments::tests::fractional_and_rounded_numeric_lexemes_are_refused_for_every_target` | Killed; expected-red command exited 100. The test received `U64Field { value: 1 }` where it required an error. Log: `TASK-260929-1w99it_fraction-mutant-09.log`. |

Surviving mutants: **none**. The temporary branch was restored from a saved copy; byte comparison and accepted-patch reverse check both passed. The mutant changes no delivered source.

## Reviewer-test preservation

The accepted revision 6 patch is unchanged and the complete `codex-tools` suite ran on it, so every test in the scoped crate was exercised. All 11 adapter test functions are present and green. The prior revision 6 handoff record reported no separate reviewer-added test identified in the attached revision resources; no test was removed or renamed in this revalidation.

## Validation evidence

Tool versions: `just 1.58.0`, `cargo 1.91.0`, `rustc 1.91.0`. Cargo/just commands used the producer-brief environment: `CARGO_TARGET_DIR=/Users/iv/Developer/IV/codex-target`, `CARGO_BUILD_JOBS=4`, `CARGO_INCREMENTAL=0`, the specified aarch64-apple-darwin Rusty V8 archive/binding paths, `NEXTEST_TEST_THREADS=4`, and `INSTA_UPDATE=no`.

| Command | Exit | Evidence |
|---|---:|---|
| `just test -p codex-tools` | 0 | 121 passed, 0 skipped; includes all 11 adapter tests. `TASK-260929-1w99it_codex-tools-test-09.log`. |
| `just test -p codex-tools -E 'test(fractional_and_rounded_numeric_lexemes_are_refused_for_every_target)'` with temporary `admit_exact_1.5` mutant | 100 | Expected red; named refusal test failed on the admitted `1.5`. `TASK-260929-1w99it_fraction-mutant-09.log`. |
| `just fmt` | 0 | Formatter emitted no stdout/stderr; execution record is `TASK-260929-1w99it_fmt-09.log`. |
| `just fix -p codex-tools` | 0 | Scoped lint/fix check completed; `TASK-260929-1w99it_fix-09.log`. |
| `git apply --reverse --check .temp/TASK-260929-1w99it/accepted-revision-6.patch` | 0 | Candidate still matches the accepted patch after validation and mutant restoration. |
| `cmp -s .temp/TASK-260929-1w99it/arguments.rs.pre-mutant-01 codex-rs/tools/src/arguments.rs` | 0 | Restored implementation equals the saved pre-mutant copy. |
| `git diff --check` | 0 | No whitespace errors. |
| `rg -n 'f64|serde_json::Value' codex-rs/tools/src/arguments.rs` | 1 | Expected no-match exit: neither intermediary is used. |

The first full-suite invocation had a log-path redirection error and exited 1 before `just` started; it is recorded in `TASK-260929-1w99it_gate-setup-01.log`. The corrected direct invocation above ran the full suite and exited 0. The full suite ran before `just fmt` and `just fix`, following the repository workflow. The post-fix mutant run was isolated to the temporary mutant; the accepted source was restored and compared afterward.

Host validation was on the configured macOS ARM toolchain. Linux, Windows, and 32-bit `usize` executions were not run in this revalidation.
