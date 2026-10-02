# Review verdict — TASK-260929-17t419 CR rev 2 (reviewer claude-sonnet-5-5)

Verdict: **changes_requested** (route: to-dev). Candidate tree 5cbbc91df22bc0a63d302cd311dfb544f89ffe84 (working tree diff vs HEAD 17886de == CR delta; 35 files).

## Surface table (1 row)

| Row | Result |
|---|---|
| error surface | **broken** — finding `sibling-arg-parser-not-adapted` |

## Findings

```json
{"findings":[
 {"id":"sibling-arg-parser-not-adapted",
  "row":"error surface",
  "invariant":"A waiting-tool call whose integral-decimal number the handler now accepts (session_id/yield_time_ms/max_output_tokens = 1000.0 etc.) must be interpreted identically by every other production consumer of the same raw arguments string; a read failure must not degrade into an absent value.",
  "mechanism":"Handlers were switched to codex_tools::arguments adapters, but two other production parsers of the same wire arguments still use strict/typed-int access: (1) codex-rs/core/src/guardian/permissions.rs:23-27 parses write_stdin arguments to serde_json::Value and calls arguments[\"session_id\"].as_i64(), which is None for 1000.0, so for_tool returns Err(\"missing terminal session id\"); its only production caller core/src/tools/lifecycle.rs:53 does `.ok()`, so every ToolLifecycle contributor's on_tool_start receives permissions=None (environment/permission context silently dropped) for a call the handler accepted and runs. (2) codex-rs/rollout-trace/src/reducer/tool/terminal.rs:580-586 DispatchedWriteStdinArgs types yield_time_ms Option<u64>, max_output_tokens Option<usize> and terminal_id_from_json renders Number 1000.0 as \"1000.0\"; the reducer errors on the dispatch payload, and a session_id float would name a different terminal than the int the exec output reports.",
  "reproductions":[
   {"file":"codex-rs/core/src/tools/handlers/unified_exec_tests.rs (temporary test, reverted)","command":"just test -p codex-core -E 'test(reviewer_repro_guardian)'  # test calls crate::guardian::tool_permission_context on write_stdin invocations","expected_failure":"{\"session_id\":1000,\"chars\":\"\"} => \"terminal session is unavailable\" (parsed, reached process lookup); {\"session_id\":1000.0,\"chars\":\"\"} => \"missing terminal session id\" (rejected at parse). Log .temp/rev/repro-07.log"},
   {"file":"codex-rs/rollout-trace/src/reducer/tool/terminal_tests.rs (temporary copy of dispatch_write_stdin_payload_reduces_to_terminal_operation with 123.0/250.0/2000.0, reverted)","command":"just test -p codex-rollout-trace -E 'test(reviewer_repro_float_args)'","expected_failure":"Error: parse terminal invocation payload ... parse write_stdin dispatch function arguments: invalid type: floating point `2000.0`, expected usize. Log .temp/rev/repro-08.log"}
  ],
  "severity":"bypass",
  "repeat-of":"none"}
],
"notes":[
 "Required fix shape: parse the guardian permission-context session_id through the same exact-integer rule (typed struct with codex_tools::arguments::i32, not Value::as_i64) and add a lifecycle-level test with session_id 1000.0 asserting the same permission context as 1000; make rollout-trace tolerate integral decimals (or document as stated bound) with a float-args reducer test; do not widen the .ok() swallow.",
 "Value round-trip in rewrite_function_arguments (hook updatedInput path) converts decimals through f64; integers above 2^53 written as X.0 could be rounded on that path. Not reproduced against a real range (needs >2^53 ms/tokens); note only.",
 "Refusal tests for exec_command/write_stdin/wait_agent V1/V2 are handler-level unit tests (real handler, existing envelope asserted), not suite-level mocked model calls; acceptable since same production entry (handler.handle).",
 "did not reproduce: none dropped (no analyst reproductions were supplied)."
]}
```

## Verified (held sub-attacks, real exit codes)

| Command | Exit | Result |
|---|---:|---|
| just test -p codex-tools | 0 | 122/122 |
| just test -p codex-goal-extension | 0 | 37/37 incl. create_goal 20000000.0 accepted; 0.5/"20000000"/true refused, no goal row created |
| just test -p codex-core --retries 3 (wait_agent, exec_command_rejects, write_stdin_rejects, shell_spec, multi_agents_spec) | 0 | 50/50 |
| just test -p codex-core --retries 3 (sleep_tool_uses_configured_time_provider, one_shot_exec..., code_mode_only_nested_exec..., dynamic tool_search, suite::unified_exec::, command_lifecycle) | 0 | 51/51 |
| just test -p codex-core --retries 3 scenarios+skills_extension | 100 | 93/95; only the two quarantined astra tests fail (known-baseline-failures.md) |
| cargo fmt --all -- --check | 0 | clean |

- Mutants M1 (`removed_digits > trailing_zero_digits + 1`, negative-exponent branch) and M6 (drop fraction_digits from negative-exponent removed count) both KILLED by `negative_exponent_decimals_are_parsed_exactly` (exit 101 each); arguments.rs restored byte-identical.
- Borrowed-input proof: every production parse of ExecCommandArgs/WriteStdinArgs/SleepArgs/WaitArgs (v1,v2)/CreateGoalRequest is serde_json::from_str via parse_arguments / parse_arguments_with_base_path / memory_usage.rs:46 / ext/goal tool.rs:419; no from_value/flatten/untagged on these structs; code-mode nested calls arrive as ToolPayload::Function{arguments: String} (covered by code_mode_only_nested_exec test). Held.
- Snapshots: 15 changed .snap files contain only hash/args lines of clock, collaboration, exec_command, write_stdin; the two quarantined astra snapshots untouched; no .snap.new/.pending-snap left.
- AC coverage: 6 of 6 rows driven (1 current_time_reminder::sleep_tool_uses_configured_time_provider; 2 suite::unified_exec + handler refusals; 3 multi_agents wait tests V1/V2; 4 goal_extension_backend create_goal test; 5 spec tests + snapshots + suite tool-schema assertions; 6 search_tool dynamic passthrough with is_f64 assertion). No non-annotated schema drift found (grep of remaining JsonSchema::number for these names: none).
- Not run: clippy (`just fix`), full core suite, Windows/foreign-exec lanes.
