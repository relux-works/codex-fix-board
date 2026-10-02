# TASK-260929-17t419 — developer handoff results (revision 5 recheck)

Candidate remains uncommitted in the Story worktree. The out-of-scope README tooling section from revision 4 was removed; the current tracked delta is 42 files (834 insertions, 114 deletions), matching the prior code candidate. No production source or test content changed during this revision; `tools/src/lib.rs` was touched only to force Cargo to refresh a stale shared-target metadata artifact, and `git diff` remains empty for that file.

## Summary

The waiting-tool and goal-budget fields use the exact integer adapters from `codex-tools`; the requested schemas advertise `integer`. Existing defaults, clamps and range checks remain. Guardian permission-context parsing and rollout-trace reduction now interpret the same integral-decimal `write_stdin` arguments as the handler. The hook `updatedInput` path rewrites only `cmd` and preserves the original raw number lexemes for every other argument. No recursive JSON normalization was added; dynamic, MCP, extension-tool and plan paths remain unchanged.

The rev2 finding `sibling-arg-parser-not-adapted` is covered by `write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact` and `dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions`.

## Changed files and scope

All 42 tracked paths are within `codex-rs/core`, `codex-rs/ext/goal`, `codex-rs/rollout-trace`, `codex-rs/tools`, their Cargo metadata, and the affected core tool-catalog snapshots. No README, docs, CI, or unrelated path remains in the candidate.

- Manifests: `codex-rs/Cargo.lock`, `codex-rs/core/Cargo.toml`, `codex-rs/rollout-trace/Cargo.toml`. `serde_json/raw_value` is enabled for borrowed lexeme parsing, and core/rollout-trace depend on `codex-tools` to share its adapters; `Cargo.lock` was updated, and the scoped `just bazel-lock-update` check found no Bazel lock drift.
- Core production: `core/src/guardian/permissions.rs`; `core/src/tools/handlers/mod.rs`; `multi_agents/wait.rs`; `multi_agents_spec.rs`; `multi_agents_v2/wait.rs`; `shell_spec.rs`; `sleep.rs`; `unified_exec.rs`; `unified_exec/exec_command.rs`; `unified_exec/write_stdin.rs`.
- Core tests: `core/src/tools/handlers/multi_agents_spec_tests.rs`; `multi_agents_tests.rs`; `shell_spec_tests.rs`; `unified_exec_tests.rs`; `core/tests/suite/code_mode.rs`; `command_lifecycle_tests.rs`; `current_time_reminder.rs`; `search_tool.rs`; `unified_exec.rs`.
- Goal and trace: `ext/goal/src/tool.rs`; `ext/goal/tests/goal_extension_backend.rs`; `rollout-trace/src/reducer/tool/terminal.rs`; `terminal_tests.rs`; `tools/src/arguments_tests.rs`.
- Snapshots: `astra_active_environment_selection`, `astra_async_question_and_answer`, `astra_code_mode_call_timing`, `astra_disabled_executor_skills`, `astra_input_interrupts_response`, `astra_input_yields_code_mode_cell`, `astra_settings_release_check_tool_shapes`, `code_mode_catalog_messages`, `guardian_checkpoint_migration`, `guardian_extra_policy__extra_policy_reaches_guardian_review`, `mcp_resource_messages__mcp_resource_messages`, `multi_agent_catalog_parameters`, `skill_catalog_dedup__dedup_before_budgeting`, `subagent_browser_auth`, and `cloud_skills_across_executor_readiness` (all under `core/tests/suite/snapshots/`).

The 948 changed lines exceed the repository's 800-line guidance. This is the coherent waiting-argument stage: separating handler/schema changes from the sibling guardian and reducer fixes would leave an intermediate candidate whose production readers disagree on the same accepted wire arguments. The snapshots are the intentional schema fingerprint updates described below.

## Acceptance coverage — 6 of 6 AC rows driven

| AC | Production entry and driving test | Refusal / unchanged behavior |
|---|---|---|
| 1. `clock.sleep.duration_ms: 1000.0` | `SleepHandler::handle` → `parse_arguments`; `suite::current_time_reminder::sleep_tool_uses_configured_time_provider` drives the mocked function call. | The same handler test rejects `1.5` and wrong types with the existing argument-error output; invalid input does not reach the time provider. |
| 2. Integral `exec_command` / `write_stdin` yields | `ExecCommandHandler::handle` and `WriteStdinHandler::handle`; `suite::unified_exec::exec_command_clamps_model_requested_max_output_tokens_to_policy` and `write_stdin_clamps_model_requested_max_output_tokens_to_policy` drive integral decimals. `one_shot_exec_command_accepts_integral_decimal_timeout_and_rejects_fractional` covers the one-shot timeout. | `exec_command_rejects_fractional_and_wrong_typed_integer_fields` and `write_stdin_rejects_fractional_and_wrong_typed_integer_fields` assert the existing refusal envelope, including a string yield value. Defaults, clamps and limits remain. |
| 3. V1/V2 `wait_agent.timeout_ms: 30000.0` | `WaitAgentHandler::handle` / `WaitAgentHandlerV2::handle`; `wait_agent_accepts_integral_decimal_timeout` and `multi_agent_v2_wait_agent_accepts_integral_decimal_timeout`. | `wait_agent_rejects_fractional_and_wrong_typed_timeouts` and `multi_agent_v2_wait_agent_rejects_fractional_and_wrong_typed_timeouts`; the committed reviewer test `multi_agent_v2_wait_agent_accepts_timeout_only_argument` remains present and green. |
| 4. `create_goal.token_budget: 20000000.0` | Installed goal-tool dispatch → `parse_arguments`; `goal_extension_backend::create_goal_accepts_integral_decimal_budget_and_rejects_invalid_numbers` asserts the created budget. | That production-entry test refuses `0.5` and wrong types and confirms no goal was created. |
| 5. Integer schemas | Sleep, shell/one-shot exec and V1/V2 wait specs; `exec_command_tool_matches_expected_spec`, `write_stdin_tool_matches_expected_spec`, `wait_agent_tool_v1_timeout_schema_is_integer`, and V2 spec coverage assert the changed parameter schemas. | All 15 changed snapshots were inspected: only fingerprints for `clock`, `collaboration`, `exec_command` and `write_stdin` changed. Two quarantined host-global-skills snapshots were not regenerated. No unannotated parameter schema changed. |
| 6. Dynamic payload `1.0` unchanged | Production tool-search discovery and dynamic dispatch; `suite::search_tool::tool_search_returns_deferred_dynamic_tool_and_routes_follow_up_call`. | The forwarded `ratio` remains a floating JSON value and serializes as `1.0`. No generic number walk was introduced. MCP, extension-tool and plan forwarding code is untouched. |

## Review-surface coverage map

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| `error surface` | `sleep_tool_uses_configured_time_provider`; `exec_command_rejects_fractional_and_wrong_typed_integer_fields`; `write_stdin_rejects_fractional_and_wrong_typed_integer_fields`; V1/V2 wait acceptance and refusal tests; `create_goal_accepts_integral_decimal_budget_and_rejects_invalid_numbers`; `write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact`; `dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions`; `tool_search_returns_deferred_dynamic_tool_and_routes_follow_up_call`; full spec assertions and catalog snapshots. | M1 → `negative_exponent_decimals_are_parsed_exactly`; M6 → `negative_exponent_decimals_are_parsed_exactly`; G1 → `write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact`; R1 → `dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions` (freshly rerun against the narrowed parser; see mutant evidence). | None of the surface row is waived. Separate `// @exec` pragma arguments, internal `exec_wait`, `local_shell` timeouts and telemetry/config/session identifiers are distinct payloads outside AC 1–4; their behavior is unchanged. |

There are no out-of-contract surface rows. Integral-valued decimal/exponent lexemes are accepted only on the explicitly annotated fields; fractions, strings, booleans, malformed numbers and destination overflow are refused. Dynamic payload preservation is in contract under AC 6. MCP, extension-tool and plan code paths are unchanged and are not claimed as newly adapted consumers.

## Narrowing mutant evidence

All listed mutants preserve the gate and admit a narrower invalid class. Their expected-red commands exited 100; the surviving implementation passed the restored tests. No tested mutant survived.

| Mutant | Narrowed gate | Named failing test | Evidence / survivor bound |
|---|---|---|---|
| M1 | Negative-exponent removal accepts one extra removed digit, admitting `15e-1`. | `negative_exponent_decimals_are_parsed_exactly` | Killed, expected exit 100; `.temp/TASK-260929-17t419/mutant-M1-01.log`. |
| M6 | Negative-exponent count omits fractional digits, so `10.0e-1` decodes as 10 instead of 1. | `negative_exponent_decimals_are_parsed_exactly` | Killed, expected exit 100; `.temp/TASK-260929-17t419/mutant-M6-01.log`. |
| G1 | Guardian `session_id` parser no longer applies the exact `i32` adapter, dropping permission context for `1000.0`. | `write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact` | Killed, expected exit 100; `.temp/TASK-260929-17t419/guardian-mutant-01.log`. |
| R1 | Rollout-trace yield parsing returns to strict `u64`, refusing `250.0`. | `dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions` | Killed, expected exit 100 by the fresh revision-5 recheck; `.temp/TASK-260929-17t419/rollout-mutant-rev5-01.log` shows `250.0` rejected as `expected u64`. No mutant survived. |

No source-text gate is used. The tests exercise handler, lifecycle, goal-tool and reducer production entries.

## Workspace consumer sweep and dispositions

The sweep covered typed argument structs, `Value` accessors (`as_i64` / `as_u64` / `as_f64`), and owned or typed deserialization across `codex-rs`.

| Production hit | Disposition |
|---|---|
| Core `SleepArgs`, `ExecCommandArgs`, `WriteStdinArgs`, and V1/V2 wait structs | Annotated integer fields use `codex_tools::arguments`; handlers parse borrowed JSON text. |
| `ext/goal/src/tool.rs` `CreateGoalRequest` | `token_budget` uses the exact adapter; goal parser uses `serde_json::from_str`. |
| `core/src/memory_usage.rs` `ExecCommandArgs` parse | Already uses `serde_json::from_str`; it inherits the field adapter. Optional telemetry extraction may omit memory-usage metadata on parse failure, while the main handler refuses invalid arguments. |
| Code Mode nested function calls | Nested arguments become `ToolPayload::Function { arguments: String }`; the nested handler uses the borrowed parser. `code_mode_only_nested_exec_applies_integer_argument_validation` drives this route. |
| `core/src/guardian/permissions.rs` write_stdin session lookup | Adapted to typed `session_id` via exact `i32`; lifecycle test proves integer and decimal permission contexts are equal. |
| `rollout-trace/src/reducer/tool/terminal.rs` write_stdin dispatch | Adapted `session_id`, `yield_time_ms`, and `max_output_tokens`; numeric IDs are exact and canonicalized to integer text, while string IDs remain supported. |
| `core/src/tools/handlers/mod.rs` hook `updatedInput` rewrite | Rewrites `cmd` through a raw JSON map and preserves every untouched number lexeme, including values above 2^53. |
| `core/src/tools/executed_tool_calls.rs`, guardian-v2 observations | They record broader payload data but do not read the annotated keys to dispatch or rewrite them; unchanged. |
| Dynamic tools, MCP, extension-tool forwarding and plan parsing | Their paths remain unchanged. Dynamic `1.0` passthrough is covered by AC 6. No global JSON normalization was added. |
| Code-mode `// @exec` pragma, internal `exec_wait`, `local_shell` timeout | Separate payloads/tools, outside AC 1–4; unchanged. |
| App-server, TUI, exec, analytics, thread-store and state uses of `session_id`, `duration_ms`, `token_budget` | Session identities, telemetry, persisted rows or config values, not raw waiting-tool argument consumers; unchanged. |

No other production reader of the named raw waiting-tool fields was found.

## Borrowed-input proof

The adapters borrow `serde_json::value::RawValue`, so each production deserialization route was checked:

- Core handler `parse_arguments` and `parse_arguments_with_base_path` use `serde_json::from_str` for sleep, exec, stdin and both native wait handlers.
- `core/src/memory_usage.rs` directly uses `serde_json::from_str::<ExecCommandArgs>`.
- Code Mode nested calls carry arguments as a string into the normal borrowed parser; the code-mode integration test exercises it.
- `ext/goal/src/tool.rs`, guardian permissions and rollout-trace use `serde_json::from_str` on the raw argument string.
- No annotated struct is deserialized through `from_value`, `from_reader`, `flatten`, tagged, or untagged containers.

## Snapshot review

All 15 changed snapshots were inspected; only tool hashes/schema fingerprints for the affected integer schemas changed. The two known host-global-skills snapshots remained untouched. No `*.snap.new` or `*.pending-snap` files remain.

## Validation and evidence reuse

Fresh revision-5 commands (all run directly, with the required shared Cargo environment; `INSTA_WORKSPACE_ROOT` was set to this worktree's `codex-rs/`):

| Command | Exit | Result |
|---|---:|---|
| `just test -p codex-rollout-trace` | 0 | 62/62 passed, including integral decimals `123.0`, `250.0`, `2000.0` and fractional refusal. Log: `.temp/TASK-260929-17t419/rollout-trace-rev5-01.log`. |
| `just test -p codex-core --retries 3 -E 'test(write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact)'` (first three attempts) | 101 each | Build stopped in `codex-rollout-trace` with `cannot find arguments in codex_tools`; logs `guardian-lifecycle-rev5-01.log`, `-02.log`, `-03.log`. |
| Same lifecycle command with `--cargo-verbose` | 101 | Log showed `Fresh codex-tools` supplying a stale shared-target rmeta. Log: `guardian-lifecycle-rev5-verbose-01.log`. |
| `cargo check -p codex-core -vv` | 0 | Production dependency graph compiles. Log: `core-cargo-check-verbose-01.log`. |
| `cargo check -p codex-core --tests -vv` | 0 | Test targets compile. Log: `core-cargo-check-tests-verbose-01.log`. |
| Same lifecycle `just test` command after touching unchanged `tools/src/lib.rs` to refresh the stale metadata | 0 | 1/1 passed; 4,889 tests skipped by the filter. Log: `guardian-lifecycle-rev5-04.log`. |
| `just fmt` | 0 | Formatting completed. Log: `fmt-rev5-01.log`. |
| `git diff --check` | 0 | Clean after README restoration and formatting. |
| `find codex-rs/core/tests/suite/snapshots -type f \( -name '*.snap.new' -o -name '*.pending-snap' \) -print` | 0 | No pending snapshots. |

### Revision-5 recheck for this handoff

| Command | Exit | Result |
|---|---:|---|
| `just test -p codex-rollout-trace` | 0 | 62/62 passed, including `dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions`; log `.temp/TASK-260929-17t419/rollout-trace-rev5-02.log`. |
| `just test -p codex-core --retries 3 -E 'test(write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact)'` | 0 | 1/1 passed, 4,889 filtered; log `.temp/TASK-260929-17t419/guardian-lifecycle-rev5-05.log`. |
| Narrowing mutant: removed the exact `u64` adapter only from rollout-trace `yield_time_ms`, then ran `just test -p codex-rollout-trace -E 'test(dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions)'` | 100 (expected red) | Named test failed on `250.0`, `invalid type: floating point`, proving the new test kills R1; log `.temp/TASK-260929-17t419/rollout-mutant-rev5-01.log`. Restored `terminal.rs` from the saved copy and `diff -u` returned 0. |
| `just fmt` | 0 | Log `.temp/TASK-260929-17t419/fmt-rev5-02.log`; no tracked content changed. |
| `git diff --check` | 0 | Log `.temp/TASK-260929-17t419/diffcheck-rev5-01.log`. |
| Snapshot pending-file scan | 0 | No `*.snap.new` or `*.pending-snap` files. |
| `git diff --quiet -- README.md` | 0 | README has no candidate delta. |

The earlier rev5 stale shared-target attempts and their exit 101 are preserved in the attached `TASK-260929-17t419_rev5-verification.log`; the later successful lifecycle run in this table used rebuilt metadata. The candidate source and tests are unchanged from the evidence below; R1's named test was freshly re-attacked after its rename. No tests were run after `just fmt`.

The prior A3/rev4 green evidence is reused because source, tests, Cargo configuration and environment are unchanged after removing only the README delta (the mtime refresh changed no bytes). This includes `just test -p codex-tools` (122/122), `just test -p codex-goal-extension` (37/37), the focused core handler/spec/code-mode/snapshot tests, and the scoped lint run below. Their command/log table is preserved in the prior attached results resource. The known scenario baseline remains: 52/52 scenarios pass when the two documented global-skills snapshot tests are excluded; the unfiltered scenario selection exits 100 on those two quarantined tests. The full workspace `just test` was not run because the repository instructions require approval.

Reused lint and dependency-lock evidence: `just fix -p codex-core -p codex-tools -p codex-goal-extension -p codex-rollout-trace` exited 0 (`fix-final-03.log`); `just bazel-lock-update` exited 0 (`bazel-lock-update-03.log`). Both match the current code/config identity. No tests were rerun after formatting.

Windows and foreign-executor runs were not performed on this macOS arm64 host. No app-server suite was rerun in revision 5.

## Handoff

Coverage ratio: **6 of 6 AC rows driven**; review-surface ratio: **1 of 1 rows covered**. The only surface row is in contract. The candidate remains uncommitted and is ready for the developer-role handoff.

## Revision 6 recheck

The candidate is unchanged from revision 5. `git diff --binary 0462dcc` matched the attached `TASK-260929-17t419_change-request_rev5.patch` byte-for-byte before and after formatting (`cmp -s`, exit 0 both times). The working tree remains uncommitted; no new source, test, or snapshot edits were made in this recheck. `README.md` is at base content.

| Command | Exit | Evidence |
|---|---:|---|
| `/Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-target-guard.sh` | 0 | Same-checkout guard passed; `.temp/TASK-260929-17t419/target-guard-01.log`. |
| `just test -p codex-rollout-trace` | 0 | 62/62 passed, including `dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions`; `.temp/TASK-260929-17t419/rollout-trace-rev6-02.log`. An initial invocation yielded without an exit status; it was not counted, and the command was rerun to completion. |
| `just test -p codex-core --retries 3 -E 'test(write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact)'` | 0 | 1/1 passed, 4,889 filtered; `.temp/TASK-260929-17t419/guardian-lifecycle-rev6-01.log`. |
| `just fmt` | 0 | `.temp/TASK-260929-17t419/fmt-rev6-01.log`; candidate patch remained byte-identical. |
| `git diff --check` | 0 | Clean after formatting. |
| `git diff --quiet -- README.md` | 0 | README unchanged from base. |
| `find codex-rs/core/tests/suite/snapshots -type f \( -name '*.snap.new' -o -name '*.pending-snap' \) -print` | 0 | No `*.snap.new` or `*.pending-snap` files. |

The workspace-wide scoped fix command remains reusable from revision 5 because the candidate patch and validation inputs are byte-identical: `just fix -p codex-core -p codex-tools -p codex-goal-extension -p codex-rollout-trace` exited 0 (`.temp/TASK-260929-17t419/fix-final-03.log`). `just bazel-lock-update` exited 0 and found no Bazel lock drift (`.temp/TASK-260929-17t419/bazel-lock-update-03.log`). The AC test matrix and the 4/4 killed-mutant evidence below are likewise carried forward from the same candidate identity; their exact commands and package counts remain recorded in the preceding sections and attached revision-5 verification log. Full workspace tests were not run because the repository requires approval for that suite. Windows and foreign-executor lanes were not run on this macOS host.

## Review surface coverage map

Coverage ratio: **1 of 1 surface-table rows covered**. The sole row, `error surface`, maps to these production entries: `SleepHandler::handle`/`parse_arguments`; `ExecCommandHandler::handle` and `WriteStdinHandler::handle`; V1 and V2 `WaitAgentHandler::handle`; installed goal-tool dispatch/`parse_arguments`; code-mode nested handler dispatch; guardian `tool_permission_context`; and rollout-trace `dispatch_write_stdin` reduction.

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| `error surface` | `sleep_tool_uses_configured_time_provider`; `exec_command_rejects_fractional_and_wrong_typed_integer_fields`; `write_stdin_rejects_fractional_and_wrong_typed_integer_fields`; `exec_command_clamps_model_requested_max_output_tokens_to_policy`; `write_stdin_clamps_model_requested_max_output_tokens_to_policy`; `one_shot_exec_command_accepts_integral_decimal_timeout_and_rejects_fractional`; `wait_agent_accepts_integral_decimal_timeout`; `wait_agent_rejects_fractional_and_wrong_typed_timeouts`; `multi_agent_v2_wait_agent_accepts_integral_decimal_timeout`; `multi_agent_v2_wait_agent_rejects_fractional_and_wrong_typed_timeouts`; `create_goal_accepts_integral_decimal_budget_and_rejects_invalid_numbers`; `code_mode_only_nested_exec_applies_integer_argument_validation`; `tool_search_returns_deferred_dynamic_tool_and_routes_follow_up_call`; `write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact`; `dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions`; `exec_command_tool_matches_expected_spec`; `write_stdin_tool_matches_expected_spec`; `wait_agent_tool_v1_timeout_schema_is_integer`; `multi_agent_catalog_parameters`. | M1 → `negative_exponent_decimals_are_parsed_exactly`; M6 → `negative_exponent_decimals_are_parsed_exactly`; G1 → `write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact`; R1 → `dispatch_write_stdin_integral_decimals_match_integer_arguments_and_refuse_fractions`. | No named-field input is waived; fractions and wrong types are explicit refusal probes under AC 1–4. Adjacent code-mode `// @exec` pragma fields, internal `exec_wait`, and `local_shell` arguments are separate payloads outside the Task Description's named structs/fields; AC 2 specifically names `exec_command` and `write_stdin`. Telemetry/config/persisted values with similar key names are not raw requests through the AC 1–4 production entries. These adjacent inputs were left unchanged. Dynamic/MCP/extension/plan preservation remains in scope under the Task Description; AC 6 explicitly drives dynamic `1.0`. | 

All four listed mutants narrow a live gate and were killed by their named tests; **0 survivors**. M1/M6, G1, and R1 expected-red commands exited 100 and are recorded in the referenced logs. The revision-2 verdict names `repeat-of: none`; its blocking finding `sibling-arg-parser-not-adapted` is answered by the named guardian and rollout-trace regression tests plus G1/R1. The verdict's other review notes were accepted; this recheck adds no code changes.

No supplied surface-table row is declared out of contract: `error surface` is covered above. Out-of-contract adjacent payload families and their bounds are listed in the map's final column; the named fraction, string, boolean, decimal, and schema cases remain in-contract probes under AC 1–6. In particular, MCP, extension-tool forwarding, and plan parsing are not waived: their production paths were not changed and no general JSON number rewrite was introduced. The dynamic path has the explicit `1.0` passthrough assertion required by AC 6.

## Out-of-contract declaration and bounded diff

| Out-of-contract row or adjacent input | Acceptance-criteria clause that bounds it | Disposition |
|---|---|---|
| Surface-table rows | None. The only row is `error surface`, and it is in contract. | Covered by the test/mutant map above. |
| Code-mode `// @exec` pragma fields, internal `exec_wait`, and `local_shell` arguments | The Task Description enumerates the adapted request structs/fields; AC 2 names only `exec_command` and `write_stdin` for yielded execution. | Distinct payloads, unchanged. |
| Telemetry/config/persisted state values named `session_id`, `duration_ms`, `token_budget`, etc. | AC 1–4 concern raw tool-call arguments through the named production handlers and goal-tool dispatch. | Not raw named-tool payloads; unchanged. |

MCP and extension-tool forwarding, plan parsing, and dynamic payload preservation are explicit unchanged constraints in the Task Description, not out-of-contract rows. AC 6 directly tests dynamic `1.0`; the MCP, extension, and plan production paths remain unchanged.

The original leaf scope names core handlers/specs, the goal extension tool, and their tests. Files outside those named paths are bounded to review carryover and required dependencies: `core/src/guardian/permissions.rs` plus its lifecycle integration test answer `sibling-arg-parser-not-adapted`; `rollout-trace/src/reducer/tool/terminal.rs` plus reducer tests answer the same workspace-consumer finding and its revision-3 sweep; `core/Cargo.toml`, `rollout-trace/Cargo.toml`, and `Cargo.lock` make the shared adapter/raw-lexeme dependencies available; `tools/src/arguments_tests.rs` adds the A1-mandated negative-exponent drivers. The 15 snapshot changes are limited to tool fingerprints/schema lines for the named integer schemas. No README, docs, CI, or unrelated source path is in the candidate.

The task remains **ready for developer handoff**; no reviewer acceptance is claimed.
