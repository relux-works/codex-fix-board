# Review verdict — TASK-260929-1w99it, CR rev 6 — ACCEPTED

Candidate tree 5e160f8ecc84 verified: worktree blobs for arguments.rs / arguments_tests.rs / lib.rs equal the candidate tree blobs.

## Surface table
| Row | Result | Attacks run (public entry: serde_json::from_str into #[derive(Deserialize)] structs with deserialize_with) |
|---|---|---|
| text grammar | held | see below |

Attacks that did NOT reproduce (row held):
- Differential fuzz vs an independent exact reference (u128 sign/coefficient/exponent arithmetic): 3,000,000 random lexemes (sign, 1-4 int digits, 0-22 fraction digits with zero runs, e/E, +/- exponent -25..24) x u64/i64/i32/usize/Option<i64>: 0 mismatches in accept/reject and value.
- Named lexemes: 1.0000000000000001, 9007199254740991.5, 9007199254740993, u64::MAX, u64::MAX+1, 1e20, i32::MAX+1, i64 min/min-1, -0.0, -0e-5, 0e999999999999999999999999, 1e+000..1 (all correct).
- Pathological: 1e<2M nines>, 1e-<2M nines>, 5M-digit integer, 0.<1M zeros>1e1000001 (=1), 1<1M zeros>e-1000000 (=1): all 0.7-4 ms, refused/accepted correctly, no exponent-sized allocation (exponent accumulator capped at raw.len()+32, no loop over exponent).
- Types: string, bool, array, object -> "invalid type ... expected u64"; null non-Option -> invalid type unit; Option null/omission/default retained; duplicate key -> serde "duplicate field".
- Production entry check: all handler call sites of the sibling leaf use serde_json::from_str (core/src/tools/handlers/mod.rs parse_arguments; ext/goal/src/tool.rs:419).

Test run (reproduced): `just test -p codex-tools -E 'test(arguments)'` exit 0, 11/11 pass (log .temp/TASK-260929-1w99it/review-test-01.log).

AC coverage: 6 of 6 rows driven (AC1..AC6 by tests in arguments_tests.rs, each with its refusal test).

## findings
[]

## notes (non-blocking; no failing product reproduction)
1. `mutant-survives-negative-exponent` — narrowing mutants survive the committed suite because no test drives a *non-huge negative exponent* (accept or refuse). Ran in scratch copy:
   - M1: `removed_digits > trailing_zero_digits` -> `> trailing_zero_digits + 1` in the exponent_negative branch: 11/11 pass (would silently admit 15e-1 = 1.5 as 1).
   - M6: drop `fraction_digits` from the negative-exponent removed-digit count: 11/11 pass (would admit 10.0e-1 as 10).
   Killed by the suite: M2 (positive-exponent branch +1), M9 (trailing-zero counter never reset). Current code is correct for these inputs (fuzz above). Recommend adding drivers `600000e-1`->60000, `10.0e-1`->1, `15e-1` refused, `1e-1` refused when the wiring leaf or a later revision touches the test file.
2. `borrowed-rawvalue-input-only` — adapters use `<&RawValue>::deserialize`, so they only work with borrowed-input deserializers (from_str/from_slice). from_reader, from_value, #[serde(flatten)], internally tagged and untagged containers fail even for plain `60000` (verified in scratch). All current production call sites use from_str; the sibling wiring leaf must not put annotated fields behind flatten/untagged/tag or deserialize them from a Value. Not documented in the module doc.
3. Pathological-exponent test asserts is_err only, no time bound; behaviour verified by hand above (bounded by construction).
4. Error text for fractions is "invalid value: a fractional number, expected u64" (serde's invalid value shape) rather than serde's native "invalid type: floating point"; consistent with the AC's "invalid type/value shape".

Verdict: accept_cr.

```verdict-findings
{
  "findings": [],
  "notes": [
    "mutant-survives-negative-exponent: narrowing mutants M1 (removed_digits > trailing_zero_digits + 1 in the exponent_negative branch) and M6 (drop fraction_digits from negative-exponent removed count) survive the 11 committed tests; code itself is correct (3M-case differential fuzz, 0 mismatches). Add drivers 600000e-1, 10.0e-1, 15e-1 (refuse), 1e-1 (refuse).",
    "borrowed-rawvalue-input-only: adapters work only with borrowed-input deserializers (from_str/from_slice); from_reader, from_value, flatten, tag and untagged containers fail even for plain 60000. All current production call sites use from_str; wiring leaf must respect this.",
    "pathological-exponent test asserts is_err without a time bound; bounded by construction (verified 0.7-4 ms at 2M-5M digit inputs).",
    "fraction error text is invalid value: a fractional number, expected T (serde invalid_value shape), not serde native invalid type floating point."
  ],
  "surface_results": [
    {"row": "text grammar", "result": "held"}
  ],
  "free_hunt": []
}
```
