# TASK-260929-17t419: wire-integer-arguments-into-waiting-tools

## Description
Apply the codex-tools exact integer deserializers to the named fields and switch their advertised JSON schemas to integer: SleepArgs.duration_ms (core/src/tools/handlers/sleep.rs), ExecCommandArgs.yield_time_ms/timeout_ms/max_output_tokens (core/src/tools/handlers/unified_exec.rs), WriteStdinArgs.session_id/yield_time_ms/max_output_tokens (unified_exec/write_stdin.rs), both native wait_agent timeout_ms (multi_agents/wait.rs, multi_agents_v2/wait.rs) and CreateGoalRequest.token_budget (ext/goal/src/tool.rs). Use JsonSchema::integer (tools/src/json_schema/types.rs) for those parameters in sleep.rs, shell_spec.rs, multi_agents_spec.rs and the one-shot exec timeout schema. Keep defaults, clamps and range checks. Dynamic tools, MCP, extension-tool forwarding and plan parsing stay byte-for-byte unchanged.

## Scope
Touches codex-core handlers/specs, codex-goal-extension tool.rs and their tests only. Integration tests in core/tests/suite (test_codex + core_test_support::responses mocks) and ext/goal/tests. Snapshot updates if tool-spec snapshots change.

## Acceptance Criteria
| # | Requirement | Driving test (production entry) | Negative/refusal |
| - | ----------- | ------------------------------- | ---------------- |
| 1 | A model call clock.sleep {duration_ms: 1000.0} runs the sleep | core/tests/suite test driving a mocked function call through the sleep handler | {duration_ms: 1.5} returns the existing argument-error output |
| 2 | exec_command {yield_time_ms: 10000.0} and write_stdin {yield_time_ms: 5000.0} are accepted | core/tests/suite unified exec tests with mocked calls | {yield_time_ms: "10000"} refused with the existing envelope |
| 3 | wait_agent {timeout_ms: 30000.0} accepted on V1 and V2 | multi-agent wait tests | {timeout_ms: 1.5} refused |
| 4 | create_goal {token_budget: 20000000.0} creates a goal with budget 20000000 | ext/goal/tests goal tool test | {token_budget: 0.5} refused |
| 5 | Advertised schemas for the annotated parameters are integer | existing spec tests / snapshots updated | no non-annotated parameter schema changes |
| 6 | Dynamic tool arguments containing 1.0 are forwarded unchanged | dynamic tool test asserting the forwarded payload | forwarded payload is not rewritten to 1 |
