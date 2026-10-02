# TASK-260929-1w99it — coverage map, accepted revision 6

Brief surface table row: `text grammar`.

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| `text grammar` | `integer_valued_decimals_and_exponents_decode_exactly_for_all_targets`; `negative_zero_and_negative_integers_decode_for_signed_targets`; `exact_large_integers_and_destination_boundaries_are_preserved`; `integer_overflow_is_refused_for_each_destination`; `fractional_and_rounded_numeric_lexemes_are_refused_for_every_target`; `unsigned_targets_refuse_negative_nonzero_values`; `optional_integer_adapters_preserve_null_omission_and_serde_defaults`; `optional_integer_adapters_reject_strings_and_booleans`; `invalid_json_types_keep_serde_invalid_type_errors`; `pathological_exponents_and_long_digit_inputs_are_refused`; `duplicate_annotated_fields_keep_serde_rejection` | `admit_exact_1.5` → `fractional_and_rounded_numeric_lexemes_are_refused_for_every_target` fails after a temporary branch admits only raw lexeme `1.5` as integer `1`; all other fraction checks remain active. Expected-red command exited 100; log attached as `TASK-260929-1w99it_fraction-mutant-09.log`. | None. No refusal named by AC1–AC6 is waived. Consumer handler wiring is excluded by the task Scope clause (“No handler wiring (that is the sibling leaf)”), not by a surface or AC waiver. |

## Entry point and bound

Each test deserializes a derived containing struct using `serde_json::from_str` and a field-level `deserialize_with` attribute. Required fields enter through public `arguments::{u64,i64,i32,usize}::deserialize`; optional fields enter through `arguments::option_*::deserialize`. Both paths read borrowed `serde_json::value::RawValue` and reach `parse_raw_integer` / `parse_number` plus exact destination conversion.

Coverage ratios: **1 of 1 surface-table rows attacked; 6 of 6 AC rows driven**. The bounded-exponent test exercises both specified pathological exponents and 10,000-digit exponent/integer inputs. All AC refusal classes are covered. No AC input is declared out of contract.

The only executed mutant was killed; there are no surviving mutants. The full crate suite ran on the unchanged accepted revision 6 candidate (121 passed, 0 skipped).
