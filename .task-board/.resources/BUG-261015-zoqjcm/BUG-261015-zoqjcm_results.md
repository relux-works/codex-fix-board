# BUG-261015-zoqjcm — reserved-tool-schema-rejected, hosted precheck 2 handoff

Ready for review on unchanged candidate tree `1e7f995c89c36a718a56f2fe3e05e398927acd7c`. This report supersedes the previous pending-precheck execution status. No source/test/snapshot/configuration file was changed in this handoff run. No local build or Rust test was run, as required by the task-specific no-build brief and handoff-note-2.

## Identity and evidence reuse

- Checkpoint HEAD remains `e063784b0d6eb97e9a4f4761e4f0fbd01969396a`; producer changes remain uncommitted and unstaged.
- A separate temporary index ran `git read-tree HEAD`, `git add -A`, `git write-tree`; every command exited 0, yielding exactly `1e7f995c89c36a718a56f2fe3e05e398927acd7c`. The real index was not staged.
- Persisted precondition `BUG-261015-zoqjcm_hosted-precheck-2.md` binds that tree to signed snapshot `248fc4e3d824`, branch `ci/BUG-261015-zoqjcm/wip-2`, relux-ci run **38812946982**. Lanes lint, small, core and app-server report success; all ten mutants have named killing tests. Accepted from orchestrator-provided hosted evidence; not rerun or independently fetched from GitHub here. Raw per-command hosted exit codes are not included in that summary, so only its success verdicts are reported.
- Upstream wire reference: `0462dcc062b822bb8fff16cc31ce6eeab69823b9`. All snapshots compare byte-identically (direct diff exit 0). No source/test/configuration identity changed since the precheck; hosted environment identity is inherited from that snapshot evidence, not asserted equivalent to the local host.

## Changed scope retained from precheck 2

Paths relative to `codex-rs/`: `core/src/tools/handlers/multi_agents_spec.rs`, `multi_agents_spec_tests.rs`, `shell_spec.rs`, `shell_spec_tests.rs`, `sleep.rs`, new `sleep_tests.rs`, `unified_exec/exec_command.rs`, new `unified_exec/exec_command_tests.rs`; `core/tests/suite/current_time_reminder.rs`, `unified_exec.rs`; `ext/goal/tests/goal_extension_backend.rs`, new `goal_extension_backend/reserved_tool_schema_tests.rs`; and the 17 restored `core/tests/suite/snapshots/*.snap` listed in the attached candidate manifest. Total 29 paths.

Nine advertised numeric constructors restored to upstream number, including the previously missed one-shot timeout. Seven complete parameter JSON pins compare independent upstream literals and check numeric types. Goal token_budget remains upstream integer. Existing schema assertions are restored to number. Parsing implementation, adapters, annotations, guardian/rollout readers and parsing-test behavior remain unchanged; only the two required integration advertised-type expectations changed. No previously committed reviewer test was removed or renamed in this rework. Earlier producer-only schema test rename from integer to number remains as recorded in the previous results.

Rework is confined to the one-shot implementation/sibling test plus the two integration schema assertions explicitly named by rework brief. No README/docs/CI/dependency/generated schema change. No source changes were made during this handoff.

## AC and production-call map

**3 of 4 AC rows driven through production tests**, using hosted precheck 2; **0 of 4 rerun locally**. AC4 remains the explicitly delegated post-landing manual trial. **7 of 7 pins green; 10 of 10 mutants killed; 0 survivors.** Tests are committed in the hosted snapshot; the managed Story worktree remains uncommitted as required.

| AC | Driving tests/evidence | Production call site | Negative check / stated bound |
|---|---|---|---|
| AC1 upstream advertised schema and snapshots | All seven pins below; existing exec_command_tool_matches_expected_spec and write_stdin_tool_matches_expected_spec; 17 scenarios in green core lane; upstream snapshot diff exit 0 | multi_agents/wait.rs::Handler::spec, multi_agents_v2/wait.rs::Handler::spec, unified_exec/exec_command.rs::ExecCommandHandler::spec (both lifetimes), unified_exec/write_stdin.rs::WriteStdinHandler::spec, sleep.rs::SleepHandler::spec, ext/goal/src/tool.rs::GoalToolExecutor::spec | Whole-object equality rejects type/description/required/additionalProperties drift. Capable-host P5 extension explicitly excluded by brief. |
| AC2 tolerant parsing kept | integer_valued_decimals_and_exponents_decode_exactly_for_all_targets; fractional_and_rounded_numeric_lexemes_are_refused_for_every_target; sleep_tool_uses_configured_time_provider; one_shot_exec_command_accepts_integral_decimal_timeout_and_rejects_fractional; wait_agent_accepts_integral_decimal_timeout; multi_agent_v2_wait_agent_accepts_timeout_only_argument; write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact; code_mode_only_nested_exec_applies_integer_argument_validation; create_goal_accepts_integral_decimal_budget_and_rejects_invalid_numbers; boundary/default/duplicate tests in green lanes | tools/src/arguments.rs adapters consumed by SleepArgs, ExecCommandArgs, WriteStdinArgs, both wait Args and CreateGoalRequest, through production dispatch | Valid decimals/exponents paired with fractions, rounded fractions, overflow, unsigned negatives, wrong types and duplicates. Both parser mutants killed. |
| AC3 complete upstream pins | Seven named tests in mutant table below, all green on unmutated snapshot | Serialized schemas from the production handlers/builders listed in AC1 | Explicit != integer for upstream number parameters; goal has upstream integer equality (its mutant changes to number). Intentional static wire-contract test documented in comments. |
| AC4 live release request | Unrun by producer; assigned to orchestrator after landing | Release CLI → actual ChatGPT gpt-6-astra request | Required-change item 4 explicitly delegates this manual trial. Hosted success does not establish live server compatibility. |

## Surface coverage


All **5 of 5 supplied surface rows mapped**, with named killed narrowing mutants from hosted precheck 2, run 38812946982, snapshot 248fc4e3d824, tree 1e7f995c89c36a718a56f2fe3e05e398927acd7c. This run independently matched the worktree tree; no local Rust test or mutant replay occurred. The brief uses task-specific rows rather than catalog labels; that naming gap is retained explicitly and does not omit a supplied row.

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| advertised wire schema | Seven wire pins enumerated in results; existing full-spec tests | wait_v1_integer / wait_v2_integer → corresponding wait pins; exec_yield_integer → exec pin; stdin_session_integer / stdin_description_word → stdin pin; sleep_duration_integer → sleep pin; goal_budget_number → goal pin; oneshot_timeout_integer → one-shot pin | Capable-host P5 additions retained under brief “Out of scope”; base-host parameters pinned. Other configurable host variants are a stated bound. |
| snapshots | Existing 17 scenario snapshot tests in green core lane; direct upstream snapshot diff exit 0 | wait_v1_integer / wait_v2_integer → corresponding wait pins; sleep_duration_integer → sleep pin, detecting the schema drift that changes fingerprints | None for upstream snapshot comparison; no snapshot-file mutant execution claimed. |
| tolerant parsing kept | integer_valued_decimals_and_exponents_decode_exactly_for_all_targets; fractional_and_rounded_numeric_lexemes_are_refused_for_every_target; preserved handler integration tests | parser_refuses_integral_decimal → first named test; parser_admits_rounded_fraction → second named test | No new numeric exclusions; AC2 preserves existing acceptance/refusal. |
| regression pin | Seven whole-parameter JSON pins; numeric negative checks, with upstream integer preserved for goal | All seven type mutants → corresponding pins; stdin_description_word → write_stdin_reserved_parameters_match_upstream_wire_contract | No self-generated expected objects or static source checker used as acceptance. |
| scope and later patches | Preserved parser/handler and P5 tests in green lanes; unchanged candidate identity and source-preservation evidence | parser_refuses_integral_decimal / parser_admits_rounded_fraction → named parser tests above, attacking forbidden parsing changes | P4a/P4c/P5, exec_notification, guardian/rollout readers, README/docs/CI excluded by task “Scope” and brief “Out of scope”. This is not exhaustive mutation proof for those subsystems. |

AC execution: **3 of 4 AC rows driven** on the exact candidate in hosted CI; AC4 live release request explicitly belongs to the orchestrator after landing. **7 of 7 schema pins green; 10 of 10 mutants killed; 0 survivors.** No source-text product gate introduced: checklist source-token condition is inapplicable. Additionally, stdin_description_word preserves numeric schema constructor tokens and is killed by executing serialized-schema behavior.

## Mutant results accepted from hosted precheck 2

| Mutant | Narrowing / drift admitted | Named failing test | Result; survival bound |
|---|---|---|---|
| wait_v1_integer | Changes only v1 timeout to integer | wait_agent_v1_reserved_parameters_match_upstream_wire_contract | Killed; no survivor |
| wait_v2_integer | Changes only v2 timeout to integer | wait_agent_v2_reserved_parameters_match_upstream_wire_contract | Killed; no survivor |
| exec_yield_integer | Changes only interactive exec yield to integer | exec_command_reserved_parameters_match_upstream_wire_contract | Killed; no survivor |
| stdin_session_integer | Changes only stdin session ID to integer | write_stdin_reserved_parameters_match_upstream_wire_contract | Killed; no survivor |
| sleep_duration_integer | Changes only sleep duration to integer | sleep_reserved_parameters_match_upstream_wire_contract | Killed; no survivor |
| goal_budget_number | Changes upstream integer goal budget to number | create_goal_reserved_parameters_match_upstream_wire_contract | Killed; no survivor |
| stdin_description_word | Changes running to active, preserving numeric constructor tokens | write_stdin_reserved_parameters_match_upstream_wire_contract | Killed by serialized-schema behavior; no survivor |
| parser_refuses_integral_decimal | Rejects exactly valid 60000.0, retaining other paths | integer_valued_decimals_and_exponents_decode_exactly_for_all_targets | Killed; no survivor |
| parser_admits_rounded_fraction | Admits fractional 1.0000000000000001 as 1, retaining other refusals | fractional_and_rounded_numeric_lexemes_are_refused_for_every_target | Killed; no survivor |
| oneshot_timeout_integer | Changes only one-shot timeout to integer | one_shot_exec_command_reserved_parameters_match_upstream_wire_contract | Killed; no survivor |

The attached ten-mutant JSON remains unchanged. None applied or replayed locally this turn. The original gate stays present for each narrowing mutant; no delete-only evidence used. Description mutation preserves source tokens, and hosted tests execute actual schema serialization.

## Exhaustive P1 sweep retained from rework


`git show 35af013` was captured and every `JsonSchema::integer` / `"integer"` hit inspected: **17 hits**. The current full `git diff 0462dcc -- codex-rs` has **6 hits**, listed below. The untracked new test files were separately searched because git diff omits them. Logs `p1-rework-integer-hits.log` and `upstream-rework-integer-hits.log` are attached in the rework validation resource.

| P1 diff hit line | Path / parameter | Verdict in revised candidate |
|---:|---|---|
| 190 | multi_agents_spec.rs, v1 timeout_ms | Restored number |
| 199 | multi_agents_spec.rs, v2 timeout_ms | Restored number |
| 370 | shell_spec.rs, exec yield_time_ms | Restored number |
| 375 | shell_spec.rs, exec max_output_tokens | Restored number |
| 384 | shell_spec.rs, stdin session_id | Restored number |
| 393 | shell_spec.rs, stdin yield_time_ms | Restored number |
| 400 | shell_spec.rs, stdin max_output_tokens | Restored number |
| 413 | shell_spec_tests.rs, exec yield_time_ms | Expected number restored |
| 418 | shell_spec_tests.rs, exec max_output_tokens | Expected number restored |
| 427 | shell_spec_tests.rs, stdin session_id | Expected number restored |
| 436 | shell_spec_tests.rs, stdin yield_time_ms | Expected number restored |
| 443 | shell_spec_tests.rs, stdin max_output_tokens | Expected number restored |
| 463 | sleep.rs, duration_ms | Restored number |
| 504 | unified_exec/exec_command.rs, one-shot timeout_ms | Restored number in THIS rework |
| 958 | current_time_reminder.rs, duration_ms assertion | Expected number restored in THIS rework |
| 1435 | suite/unified_exec.rs, one-shot timeout_ms assertion | Expected number restored in THIS rework |
| 1524 | goal_extension_backend.rs, token_budget assertion | Integer retained: upstream already integer; P1 added parsing test, not schema drift |

| Current upstream diff hit line | Path / meaning | Verdict |
|---:|---|---|
| 9218 | multi_agents_spec_tests.rs, v1 `assert_ne!(..., "integer")` | Intentional negative check |
| 9239 | multi_agents_spec_tests.rs, v2 `assert_ne!(..., "integer")` | Intentional negative check |
| 10120 | shell_spec.rs, exec_notification.max_output_tokens constructor | P5-only new tool; explicitly out of scope, retained |
| 10219 | shell_spec_tests.rs, exec negative check | Intentional refusal of integer schema |
| 10255 | shell_spec_tests.rs, stdin negative check | Intentional refusal of integer schema |
| 37018 | goal_extension_backend.rs, token_budget expectation | Correct upstream integer retained |

Untracked tests add three further textual hits: sleep_tests.rs:26 and unified_exec/exec_command_tests.rs:72 are explicit `assert_ne!(..., "integer")`; reserved_tool_schema_tests.rs:28 expects upstream goal budget integer. No other hit in these files. Already-integer upstream tools (history-notes, agent-message-board, MCP fixtures) are not retyped. `multi_agents_spec.rs` and `ext/goal/src/spec.rs` are entirely byte-identical to upstream. The one-shot timeout constructor/description exactly match upstream. Capable-host `notify_on_exit` and suffix are the other known upstream-tool schema delta, retained by explicit scope, not hidden by this numeric sweep.


## This handoff run: commands and real exits

| Command | Exit | Evidence |
|---|---:|---|
| task-board m set_status(..., status=development) | 0 | Required first lifecycle command |
| git read-tree HEAD (temporary index) | 0 | Temporary index only |
| git add -A (same temporary index) | 0 | Does not stage real index |
| git write-tree (same temporary index) | 0 | Exact expected hosted tree |
| git rev-parse HEAD | 0 | Unchanged checkpoint |
| git diff --exit-code 0462dcc062b822bb8fff16cc31ce6eeab69823b9 -- '*.snap' | 0 | Empty across all snapshots |
| git diff --check | 0 | No whitespace errors |
| git diff --cached --exit-code | 0 | Real index empty |
| task-board resource get BUG-261015-zoqjcm BUG-261015-zoqjcm_hosted-precheck-2.md --output - | 0 | Persisted precheck read |
| task-board spawn directives "$TASK_BOARD_RUN_ID" | 0 | No directives |
| rg production spec and pin symbols | 0 | Seven pins and production call sites located |

No cargo, target guard, fix, clippy, test, format or release command was run in this handoff-only turn. Prior `just fmt` and source-preservation/applicability command exits are recorded in `BUG-261015-zoqjcm_rework-validation.log`. Lint/build/test acceptance uses exact-candidate hosted precheck 2, not formatting or patch applicability. Exploratory rg of optional skill directories returned 2 for missing agents/ and .claude/; this was not validation evidence and no absence of task skills was inferred.

## Outcome-scoped logbook and remaining bounds

- Precheck 1 core was red due to a stale sleep schema assertion; the one-shot timeout omission was independently identified. Rework preserved parser behavior, restored both assertions and one-shot constructor, added its full wire pin and narrowing mutant. Precheck 2 now reports all lanes green and all ten named mutant kills.
- This run proved exact tree reuse before ticking checklist entries. Source/config/tests were not edited and no producer commit, branch operation or publication was attempted. Reports were prepared outside the managed worktree and attached using task-board resource CRUD only.
- P5 notify_on_exit is retained in core/src/tools/handlers/shell_spec.rs::create_exec_command_tool_with_environment_id under options.async_notifications_available; the description suffix is appended under the same condition via async_notification_description_suffix. ExecCommandHandler::spec enables it only for capable interactive hosts. Live TUI/server compatibility is AC4's bound, not silently asserted by base-host pins.
- No new product source-text gate exists; conditional source-token checklist item is inapplicable, with behavioral token-preserving description mutation nonetheless killed.
- All five supplied rows mapped; no whole row silently excluded. P4a/P4c/P5 behavior, exec_notification, parser/guardian/rollout changes and README/docs/CI edits are out of scope by the explicit brief clauses. Existing applicable tests are green in hosted lanes; no exhaustive mutation claim for excluded systems.
- AC4 remains unverified by producer and delegated to orchestrator post-landing. Review/acceptance/landing belong to the orchestrator; this lifecycle ends with developer handoff to review.
