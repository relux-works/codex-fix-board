# TASK-260929-309h9n (P4b-2): hosted precheck 3 red. Fix the pacing entry rule and the regressions, then request precheck 4

Precheck 3 (run 38150062342, snapshot 7c2806b6, tree 9751ddd8; ref relux/ci-next): lint green (the orchestrator's compile fixes
2 and 3 are in the tree, see `TASK-260929-309h9n_orch-compile-fix-2.md` / `-3.md`). Snapshot small, core and app-server red.
Mutant results are void.

## 1. small: 4 unit tests (FIXED by the orchestrator; keep it)

`pacing_resume_restarts_at_floor_and_resets_quotas`, `pacing_stale_ticket_rejected_on_predecessor_change`,
`pacing_ticket_binds_goal_revision_predecessor_generation`, `pacing_waiting_turn_is_paced_not_empty` all got a deadline one step
short (e.g. 6030s vs 6060s). Cause: `evaluate_pacing_locked` treated the first goal binding (`pacing_goal_id == None`) as a goal
switch and zeroed the streak and predecessor recorded by `note_turn_completed` before it. The orchestrator changed it to reset
only when a DIFFERENT bound goal is replaced (`TASK-260929-309h9n_orch-logic-fix-4.md`; current tree 2eff387c). Keep that; goal
mutation, clear, stop and resume already reset explicitly.

## 2. core: your own integration test

`suite::goal_continuation_pacing::goal_pacing_two_quiet_continuations_fire_at_30s_then_60s` fails 3/3 at
`core/tests/suite/goal_continuation_pacing.rs:204` (`test_marked_goal_continuations().is_empty()`) and once at :208
(`first pacing wait should arm`): after `set_thread_goal` + `apply_runtime_effects` + idle, a continuation already ran or no
pacing wait was armed. Find which entry path starts the first goal continuation without passing the pacing evaluation
(goal-set runtime effects vs `continue_if_idle`) and make the test and the code agree with the rule in section 3.

## 3. app-server: pre-existing goal suites regressed (5 failed + 1 timed out)

- `suite::v2::code_mode_host::app_server_blocks_goal_after_repeated_code_mode_host_failures` (mock expected 6 requests, got 0)
- `suite::v2::daemon_update_recovery::managed_restart_resumes_loaded_threads_and_goal_without_client`
- `suite::v2::thread_fork::thread_fork_defers_inherited_active_goal_until_next_turn`
- `suite::v2::thread_resume::thread_goal_keeps_original_root_until_external_objective_edit`
- `suite::v2::thread_resume::thread_goal_lifecycle_emits_analytics_and_clear_deletes_goal`
(+1 timeout in the same lane; read the log for its name)

The pacing floor delays continuations those suites expect immediately. Required decision (orchestrator):
- **Entry rule.** AC1 says automatic continuations are at least 30 s APART. The first automatic continuation after a human turn,
  a goal set/mutation, or a resume has no automatic predecessor, so it proceeds WITHOUT a pacing delay. Pacing applies when the
  predecessor turn was itself an automatic goal continuation: floor 30 s at streak 0, then min(30 s * 2^(n-1), 30 min). Update
  the unit tests (`n=0` floor case), AC1/AC2 tests and the results to this rule. This alone should restore most of the suites above.
- For pre-existing suites that still need several back-to-back automatic continuations, do not weaken production behavior.
  Apply the existing test-only switch consistently (the `with_env_overrides` per-process pattern you already use in
  `goal_background_wait.rs` / `thread_goal_empty_responses.rs`) and list every suite that sets it in the results, with the reason.
  Keep the switch's doc comment explicit that production never sets it. Prefer narrowing it to what those suites need.
- Run nothing locally except `cargo fmt` (mini addendum); read every pre-existing app-server and core test that drives more than
  one automatic goal continuation (`rg -l "goal" app-server/tests/suite core/tests/suite`) and decide per suite.

## Keep

Everything else from your design stays (shared timer slot, PacingTicket, admission recheck under the wait-state lock, blocker
first, transient state, no model-visible change). All 5 mutants must still apply to the final tree; add a mutant for the entry
rule (pace the first continuation after a human turn) with its killer. Killer names keep `pacing` in them.

`mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item` then `--check` exit 0; no other cargo; no
CODEX_HOME copies; delete temp dirs. Leave everything UNCOMMITTED, report the final tree id after fmt, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 4`, and end your turn without handing off.
