# TASK-260929-2snjbb (E2): rev 4 is almost there. Fix lint and two test-harness failures from hosted precheck 5, then request precheck 6

Hosted precheck 5 (run 37561800573) ran your exact worktree. The design works: the authoritative linearization-point test
`receipt_armed_inside_start_task_blocks_automatic_start` PASSES. small and app-server are GREEN. Three mechanical failures (R169):

1. LINT (job 112600513792): new warnings over the baseline, which fail the warning gate:
   - an unused import `codex_protocol::openai_models::ReasoningEffort` (codex-core lib);
   - an unused import `wiremock::matchers::body_json` (codex-core test "all");
   - `codex-goal-extension` (lib) generated 3 warnings.
   Fix every new warning. Run `just clippy -p codex-core -p codex-goal-extension` and confirm zero warnings beyond the
   3 known upstream-baseline ones (registry.rs, openai_file_mcp.rs, scenarios.rs).
2. `session::turn_input::tests::receipt_armed_after_admission_blocks_automatic_start` panics at turn_input_tests.rs:1527:
   "early admission must run before the latch". Your restructure (final check moved into start_task) changed the ordering
   this older test latches on. Either update its latch to the new ordering so it still attacks the preparation window, or
   remove it if it is fully subsumed by `receipt_armed_inside_start_task_blocks_automatic_start` and the fast-path test. Say
   which in the results, and do not leave a dead test.
3. `suite::goal_background_wait::scheduled_checkins_fire_through_production_runtime_under_paused_time` panics at
   core/tests/suite/goal_background_wait.rs:234: "`time::pause()` requires the `current_thread` Tokio runtime". Use
   `#[tokio::test(flavor = "current_thread", start_paused = true)]`, or an equivalent current-thread runtime with paused time.
   Keep the assertions: production CheckInTimer -> GoalRuntimeHandle re-entry, the turn marked automatic, and the warning once.
All 15 mutant results are void because the base was red.

LOCAL VERIFICATION (local-build-allowance.md, all gates apply): run the narrow core filters this time, since both failing
tests live in codex-core:
`cd codex-rs && RUST_MIN_STACK=33554432 cargo nextest run -p codex-core --lib -E 'test(turn_input)'` and
`cargo nextest run -p codex-core --test all -E 'test(goal_background_wait)'`, plus the clippy above. Run them sequentially,
trim afterwards, and record disk, CPU and memory.
Update the results and mutants files (re-attach). Leave the candidate UNCOMMITTED and add the note
"HOSTED-PRECHECK-REQUESTED: precheck 6". Do NOT hand off. Follow R176 and R174.
