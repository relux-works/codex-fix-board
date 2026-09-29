# TASK-260929-1w99it: tools-exact-integer-argument-adapter

## Description
Add a reusable Serde adapter module to codex-tools (new codex-rs/tools/src/arguments.rs, tests in a sibling arguments_tests.rs) that deserializes a JSON numeric lexeme through serde_json RawValue (raw_value is already enabled in tools/Cargo.toml) and converts it exactly to u64, i64, i32 and usize, plus Option variants that preserve null/omission. Accept integer-valued decimals and exponents (60000.0, 6e4, 6.0e4, -0.0) inside the destination range; never pass through f64 or serde_json::Value, so integers above 2^53 stay exact. Reject fractions, rounded fractions (1.0000000000000001, 9007199254740991.5), strings, booleans, negatives for unsigned targets, and overflow. Bound exponent handling by checked digit counts, never by exponent-sized allocation. Error text must read like serde's invalid type/value errors so the existing 'failed to parse function arguments' envelope stays meaningful. No other crate changes in this leaf.

## Scope
codex-rs/tools only: new arguments.rs + arguments_tests.rs, lib.rs export. No handler wiring (that is the sibling leaf). Follow codex-rs/AGENTS.md (format! inlining, no bool params, tests in *_tests.rs with #[path]).

## Acceptance Criteria
| # | Requirement | Driving test (production entry) | Negative/refusal |
| - | ----------- | ------------------------------- | ---------------- |
| 1 | 60000.0, 6e4, 6.0e4 and 60000 decode to 60000 for u64/i64/i32/usize targets | arguments_tests.rs decoding a #[derive(Deserialize)] struct via serde_json::from_str | 1.5, 1.0000000000000001 and 9007199254740991.5 refused |
| 2 | -0.0 decodes to 0; negative integral values decode for signed targets | same harness, i64/i32 fields | -1 and -1.0 refused for u64/usize |
| 3 | Integers above 2^53 (e.g. 9007199254740993) and u64::MAX decode exactly | same harness | u64::MAX+1, 1e20 into u64, i32::MAX+1 refused as out of range |
| 4 | Option variants keep null and omission as None and keep serde defaults | struct with #[serde(default)] Option fields | "60000" string and true refused |
| 5 | Pathological exponents are bounded in time and memory | 1e999999999 and 1e-999999999 inputs | refused quickly (no large allocation, no hang) |
| 6 | Duplicate keys keep serde's existing behaviour for the containing struct | struct with a repeated annotated field | duplicate refused as today |
