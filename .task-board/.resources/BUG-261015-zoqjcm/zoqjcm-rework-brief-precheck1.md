# Rework brief — BUG-261015-zoqjcm after hosted precheck 1

Hosted precheck 1 (relux-ci run 38796654299, snapshot 07b4bb31fd on ci/BUG-261015-zoqjcm/wip-1):
lint, small and app-server green; all 9 mutants killed; **core red** with one test:

```
suite::current_time_reminder::sleep_tool_uses_configured_time_provider
panicked at core/tests/suite/current_time_reminder.rs:1198:5
left: "number"  right: "integer"
```

That assertion was added by P1 and still expects the integer schema for `clock.sleep duration_ms`.

The orchestrator also found a P1 schema change that both the first brief and your candidate missed: the
**one-shot `exec_command` variant** advertises `timeout_ms` as `JsonSchema::integer` in
`codex-rs/core/src/tools/handlers/unified_exec/exec_command.rs` `one_shot_exec_command_spec` (around line 540).
Upstream 0462dcc has `JsonSchema::number`. The P1 commit message lists "exec_command ... timeout_ms"; the brief
table was incomplete. The one-shot test `one_shot_exec_command_accepts_integral_decimal_timeout_and_rejects_fractional`
in `core/tests/suite/unified_exec.rs` (around line 2087) asserts `"integer"` and passed only because the code
still advertises integer.

## Required

1. Revert the one-shot `timeout_ms` advertised type to exactly upstream (`JsonSchema::number`, same description).
2. Change the two P1 test assertions to the upstream type (`"number"`): `current_time_reminder.rs` (clock.sleep
   duration_ms) and `unified_exec.rs` (one-shot timeout_ms). Keep everything else in those tests: they still prove
   the tolerant parsing (60000.0 accepted, 1.5 refused).
3. Extend the AC3 wire-contract pin to the one-shot `exec_command` variant (full parameters object against literal
   upstream JSON, plus the negative `!= "integer"` check), and add a mutant `oneshot_timeout_integer` that flips it
   back to `JsonSchema::integer`, killed by the new pin. Update the suggested FILTER in your note if the new test
   name does not match `test(reserved_parameters_match_upstream_wire_contract)`.
4. Sweep once more, this time exhaustively: `git show 35af013 | grep -n 'JsonSchema::integer'` and
   `git diff 0462dcc062b822bb8fff16cc31ce6eeab69823b9 -- codex-rs | grep -n 'JsonSchema::integer\|"integer"'`.
   Every advertised `integer` that P1 introduced for an upstream tool must be gone, and every test assertion P1
   added that expects `"integer"` for those parameters must expect the upstream type. List the sweep result in
   your results file (each hit and its verdict). `"integer"` in tools that upstream already defines that way
   (create_goal token_budget, history-notes, agent-message-board, MCP fixtures) stays.

Same rules as before: no cargo builds (about 14 GiB free disk), `just fmt` only, attach updated
`BUG-261015-zoqjcm_results.md` and `BUG-261015-zoqjcm_mutants.json` (all previous mutants plus the new one, rebased
on the new tree), note `HOSTED-PRECHECK-REQUESTED`, end the turn without handoff.
