# BUG-261015-zoqjcm hosted precheck 2

Worktree tree: 1e7f995c89c36a718a56f2fe3e05e398927acd7c (equal to the snapshot tree, checked with a temp index).
Snapshot 248fc4e3d824 (ci/BUG-261015-zoqjcm/wip-2, parent e063784 = relux/main), ivanopcode/codex relux-ci run
38812946982: lint, snapshot small, core and app-server all success. `git diff 0462dcc -- '*.snap'` is empty.

Mutants: 10 total, 10 killed by named test failures, 0 survivors.

| Mutant | Killed | Killing test |
| --- | --- | --- |
| exec_yield_integer | yes | exec_command_reserved_parameters_match_upstream_wire_contract |
| goal_budget_number | yes | create_goal_reserved_parameters_match_upstream_wire_contract |
| oneshot_timeout_integer | yes | one_shot_exec_command_reserved_parameters_match_upstream_wire_contract |
| parser_admits_rounded_fraction | yes | fractional_and_rounded_numeric_lexemes_are_refused_for_every_target |
| parser_refuses_integral_decimal | yes | integer_valued_decimals_and_exponents_decode_exactly_for_all_targets |
| sleep_duration_integer | yes | sleep_reserved_parameters_match_upstream_wire_contract |
| stdin_description_word | yes | write_stdin_reserved_parameters_match_upstream_wire_contract |
| stdin_session_integer | yes | write_stdin_reserved_parameters_match_upstream_wire_contract |
| wait_v1_integer | yes | wait_agent_v1_reserved_parameters_match_upstream_wire_contract |
| wait_v2_integer | yes | wait_agent_v2_reserved_parameters_match_upstream_wire_contract |

History: precheck 1 (run 38796654299) was red in core on
`current_time_reminder::sleep_tool_uses_configured_time_provider` (a P1 assertion still expecting "integer"), and the
orchestrator found the one-shot exec_command `timeout_ms` still advertised as integer. The rework fixed both, added
the one-shot pin and mutant, and recorded an exhaustive sweep of P1 `integer` hits.
