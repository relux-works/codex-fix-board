# TASK-260929-3ld28o (P4b-1): hosted precheck 5 is RED on one new test. Fix the test's wrapper assumption, then request precheck 6

Precheck 5 (ivanopcode run 38031794436): lint, small and app-server are GREEN, and core has 5078 of 5079 passing. Every one of the 15
mutants failed, but the red snapshot voids them, and several were "killed" only by the failing test. `mini-producer-addendum.md`
applies.

`suite::code_mode::code_mode_leaf_applied_patch_delivered_exactly_once` FAILS 3/3 at `core/tests/suite/code_mode.rs:6947`:
`assert_eq!(wrapper_execs, 1)` got **0**. The FileChange half passes: exactly one Completed FileChange reaches the recorder. So your
assumption that "the wrapper itself arrives as CommandExecution" is false: the code-mode `exec` wrapper does not reach turn
observers as a Completed `CommandExecution` item. Find out from the code how the wrapper IS represented (or that it emits no turn
item at all), in core/src/tools/code_mode/mod.rs and in what `run_code_mode_turn_with_item_recorder` records. Then:
1. Assert the TRUE wrapper representation, and assert that it carries no observation. If the wrapper emits no item, assert that
   and keep the "one FileChange, zero observations from the wrapper" claim on what really arrives. Do not delete the check;
   replace it with the correct one.
2. Re-check `code_mode_leaf_counts_once_and_wrapper_adds_none` and the `command_execution_counts_as_state_change` mutant
   against the same truth. If the wrapper is not a CommandExecution, that mutant's premise about the wrapper may also be
   wrong. Say so in the results.
3. After the fix, `code_mode_nested_file_change_emitted_twice` must still be killed by an assertion on a green candidate.
Run cargo fmt plus `--check` (exit 0). All 15 mutant patches must apply to your final tree. Leave everything UNCOMMITTED, report the
final tree id, add the note `HOSTED-PRECHECK-REQUESTED: precheck 6`, and end your turn without handing off.
