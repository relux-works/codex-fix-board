# Carry-over from the TASK-260929-1w99it review (claude-sonnet-5-5, accepted rev 6)

The adapter in `codex-rs/tools/src/arguments.rs` was accepted with two notes that this leaf must close:

1. **Surviving mutants in the negative-exponent branch.** No committed test drives a non-huge negative exponent.
   Add drivers to `codex-rs/tools/src/arguments_tests.rs`: `600000e-1` -> 60000, `10.0e-1` -> 1, `60000.0e0` -> 60000,
   and refusals `15e-1`, `1e-1`, `1.5e0`. They must kill mutants M1 (`removed_digits > trailing_zero_digits + 1`
   in the exponent_negative branch) and M6 (drop `fraction_digits` from the negative-exponent removed count).
2. **Borrowed-input only.** The adapters use `<&RawValue>::deserialize`, so they work only with borrowed-input
   deserializers (`serde_json::from_str` / `from_slice`). `from_value`, `from_reader`, `#[serde(flatten)]`, and
   tagged/untagged containers fail even for a plain `60000`. Before wiring each annotated struct, prove every
   production path that deserializes it uses a borrowed-input deserializer, including code-mode nested tool calls,
   `parse_arguments` in `core/src/tools/handlers/mod.rs`, and the goal crate's parser (`ext/goal/src/tool.rs`).
   If any path uses an owned deserializer, fix it at the adapter (keep exactness; no f64 round-trip for values
   above 2^53) and add a test for that path. Record the proof in your results.
