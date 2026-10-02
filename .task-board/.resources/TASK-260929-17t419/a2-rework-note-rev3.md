# Rework note for TASK-260929-17t419 — revision 3 (answers review finding `sibling-arg-parser-not-adapted`)

The reviewer accepted everything else in revision 2 (snapshots, negative-exponent drivers, borrowed-input proof,
AC 6/6). One blocking finding remains (severity bypass). Other production consumers of the same raw
tool-arguments string still read these integers strictly:
1. `codex-rs/core/src/guardian/permissions.rs:23-27` reads the write_stdin `session_id` with `Value::as_i64()`.
   For `1000.0` it returns None, `for_tool` errs, and `core/src/tools/lifecycle.rs:53` swallows the error with
   `.ok()`. Lifecycle contributors then get `permissions=None` for a call the handler accepted.
2. `codex-rs/rollout-trace/src/reducer/tool/terminal.rs:580-586` parses write_stdin dispatch arguments with typed
   integers. `123.0` fails with "invalid type: floating point".

Do:
- **Sweep, do not spot-fix.** Grep the whole `codex-rs` workspace for every consumer that parses these tools'
  arguments or reads these keys: `session_id`, `yield_time_ms`, `timeout_ms`, `max_output_tokens`,
  `duration_ms`, `token_budget`. Cover typed structs, `serde_json::Value` access (`as_i64` / `as_u64` / `as_f64`),
  and `from_value`. This includes core (guardian, lifecycle, hooks), rollout-trace, app-server, tui, exec,
  analytics, and anything else you find. List every hit in your results with its disposition: adapted, already
  exact, or out of scope with the reason.
- Parse through the same exact-integer rule (typed structs with `codex_tools::arguments::*`, not `as_i64`). A read
  failure must not silently degrade into an absent value on these paths.
- Tests:
  - A lifecycle-level test proving `session_id: 1000.0` yields the same permission context as `1000`.
  - A rollout-trace reducer test with integral decimals (`123.0`, `250.0`, `2000.0`) that reduces to the same
    terminal operation as the integer form.
  - Keep fractional values refused.
- Do not widen accepted values beyond integral decimals. Keep all revision-2 work, including snapshots.
- The gate now also runs clippy and tests for `codex-rollout-trace`. Run `just test -p codex-rollout-trace`,
  the affected `codex-core` tests, `just fmt`, and `just fix -p` for each touched crate before handoff.
