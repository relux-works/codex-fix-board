# TASK-261002-3k97mc — compact panel execution evidence

Evidence collected October 2, 2026. These are fetched hosted executions, not panel test reruns. All 13 `gh api repos/relux-works/codex/actions/runs/<ID> --jq '{id,status,conclusion}'` commands exited 0. All 13 `gh run view <ID> --repo relux-works/codex --log` commands exited 0. Shell acquisition loops exited 0; each inner command status was also printed separately.

## Hosted green candidate

Run 37002709023: completed / success; workflow dispatch metadata head `ea8899e6f97aea64136159286840c28c955243e8`. Actual checkout must be read from the logs.

```text
app-server	UNKNOWN STEP	2026-10-02T11:45:05.7262767Z   WANT_SHA: 016a4248cf1984b97e786ce8573ad40c9438dfbf
app-server	UNKNOWN STEP	2026-10-02T11:54:53.2826977Z         PASS [   0.984s] ( 768/1829) codex-app-server::all suite::v2::goal_activity::v2_create_goal_exposes_sleep_only_after_committed_success::created
app-server	UNKNOWN STEP	2026-10-02T11:54:54.1787932Z         PASS [   0.897s] ( 769/1829) codex-app-server::all suite::v2::goal_activity::v2_create_goal_exposes_sleep_only_after_committed_success::refused
app-server	UNKNOWN STEP	2026-10-02T12:03:20.2790270Z      Summary [ 674.327s] 1829 tests run: 1829 passed (5 slow), 2 skipped
core	UNKNOWN STEP	2026-10-02T11:45:07.7894787Z   WANT_SHA: 016a4248cf1984b97e786ce8573ad40c9438dfbf
core	UNKNOWN STEP	2026-10-02T11:57:22.1037611Z         PASS [   0.406s] (3221/4874) codex-core::all suite::current_time_reminder::current_time_reminder_sleep_setting_overrides_goal_activity::explicit_false
core	UNKNOWN STEP	2026-10-02T11:57:22.5036568Z         PASS [   0.399s] (3223/4874) codex-core::all suite::current_time_reminder::current_time_reminder_sleep_setting_overrides_goal_activity::explicit_true
core	UNKNOWN STEP	2026-10-02T11:57:22.6952393Z         PASS [   0.388s] (3224/4874) codex-core::all suite::current_time_reminder::current_time_reminder_sleep_setting_overrides_goal_activity::missing_config
core	UNKNOWN STEP	2026-10-02T11:58:12.9296823Z         PASS [   0.543s] (3324/4874) codex-core::all suite::goal_activity::clear_revokes_before_late_create_finish_and_stale_set_effects
core	UNKNOWN STEP	2026-10-02T11:58:13.1558304Z         PASS [   0.861s] (3325/4874) codex-core::all suite::goal_activity::accounting_budget_keeps_sleep_without_automatic_continuation
core	UNKNOWN STEP	2026-10-02T11:58:13.3429651Z         PASS [   0.604s] (3326/4874) codex-core::all suite::goal_activity::create_goal_changes_the_next_sampling_tools::blocked
core	UNKNOWN STEP	2026-10-02T11:58:13.4329062Z         PASS [   0.654s] (3327/4874) codex-core::all suite::goal_activity::create_goal_changes_the_next_sampling_tools::complete
core	UNKNOWN STEP	2026-10-02T11:58:13.5737721Z         PASS [   0.644s] (3328/4874) codex-core::all suite::goal_activity::create_goal_changes_the_next_sampling_tools::paused
core	UNKNOWN STEP	2026-10-02T11:58:13.8165410Z         PASS [   0.661s] (3329/4874) codex-core::all suite::goal_activity::create_goal_changes_the_next_sampling_tools::refused
core	UNKNOWN STEP	2026-10-02T11:58:13.9117678Z         PASS [   0.571s] (3330/4874) codex-core::all suite::goal_activity::disable_mid_turn_removes_sleep_from_next_request
core	UNKNOWN STEP	2026-10-02T11:58:13.9821903Z         PASS [   0.547s] (3331/4874) codex-core::all suite::goal_activity::external_set_and_resume_reconcile_first_request::active
core	UNKNOWN STEP	2026-10-02T11:58:14.1218362Z         PASS [   0.547s] (3332/4874) codex-core::all suite::goal_activity::external_set_and_resume_reconcile_first_request::blocked
core	UNKNOWN STEP	2026-10-02T11:58:14.3383793Z         PASS [   0.521s] (3333/4874) codex-core::all suite::goal_activity::external_set_and_resume_reconcile_first_request::budget_limited
core	UNKNOWN STEP	2026-10-02T11:58:14.4420051Z         PASS [   0.530s] (3334/4874) codex-core::all suite::goal_activity::external_set_and_resume_reconcile_first_request::complete
core	UNKNOWN STEP	2026-10-02T11:58:14.5442580Z         PASS [   0.563s] (3335/4874) codex-core::all suite::goal_activity::external_set_and_resume_reconcile_first_request::paused
core	UNKNOWN STEP	2026-10-02T11:58:14.6649139Z         PASS [   0.544s] (3336/4874) codex-core::all suite::goal_activity::external_set_and_resume_reconcile_first_request::usage_limited
core	UNKNOWN STEP	2026-10-02T11:58:14.9124481Z         PASS [   0.573s] (3337/4874) codex-core::all suite::goal_activity::turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal
core	UNKNOWN STEP	2026-10-02T12:04:43.2649818Z      Summary [ 785.600s] 4874 tests run: 4874 passed (7 slow), 11 skipped
small	UNKNOWN STEP	2026-10-02T11:45:06.0692625Z   WANT_SHA: 016a4248cf1984b97e786ce8573ad40c9438dfbf
small	UNKNOWN STEP	2026-10-02T11:54:26.5363528Z         PASS [   0.007s] ( 20/238) codex-goal-extension::activity_publisher publisher_refuses_stale_revision_and_recovers_unknown_state
small	UNKNOWN STEP	2026-10-02T11:54:26.8734698Z         PASS [   0.174s] ( 27/238) codex-goal-extension::goal_extension_backend goal_activity::automatic_stop_revokes_activity_for_error_and_usage_limit
small	UNKNOWN STEP	2026-10-02T11:54:27.0222607Z         PASS [   0.169s] ( 28/238) codex-goal-extension::goal_extension_backend goal_activity::disable_and_stop_revoke_activity_and_pending_options
small	UNKNOWN STEP	2026-10-02T11:54:27.0268552Z         PASS [   0.167s] ( 29/238) codex-goal-extension::goal_extension_backend goal_activity::read_failure_revokes_activity_and_next_turn_recovers
small	UNKNOWN STEP	2026-10-02T11:54:27.0420706Z         PASS [   0.169s] ( 30/238) codex-goal-extension::goal_extension_backend goal_activity::tool_finish_reconciles_committed_state_independently_of_tool_name
small	UNKNOWN STEP	2026-10-02T11:54:28.7953520Z      Summary [   2.303s] 238 tests run: 238 passed, 0 skipped
lint	UNKNOWN STEP	2026-10-02T11:45:07.7606452Z   WANT_SHA: 016a4248cf1984b97e786ce8573ad40c9438dfbf
```

Local `git rev-parse '016a4248cf1984b97e786ce8573ad40c9438dfbf^{tree}'` exited 0 and returned `4d289590739432aa55c2a3868c2b4a5472b07c92`. Replay read-tree, resource-get, cached apply, write-tree, G1 path equality and candidate diff --check each exited 0. These are the checks rerun by the panel. No cargo/just commands ran.

## Expected-red narrowing mutants

A cancelled overall workflow does not mean its intended lane never failed. The individual test failure and process exit are retained below. Exit 100 is FAIL, expected because each mutation weakens a required gate. No status was synthesized or changed.

| Run | Mutant | Workflow conclusion | Named test failure | Hosted process exit | Retrieval exits |
|---|---|---|---|---:|---|
| 37002732285 | budget_limited_admits_continuation | failure | `accounting_budget_keeps_sleep_without_automatic_continuation` | 100 (expected red) | API 0; logs 0 |
| 37002755500 | cleared_revision_accepts_old_read | cancelled | `publisher_refuses_stale_revision_and_recovers_unknown_state` | 100 (expected red) | API 0; logs 0 |
| 37002777813 | complete_retains_sleep | failure | `create_goal_changes_the_next_sampling_tools` | 100 (expected red) | API 0; logs 0 |
| 37002797120 | create_waits_for_finish | failure | `clear_revokes_before_late_create_finish_and_stale_set_effects` | 100 (expected red) | API 0; logs 0 |
| 37002815598 | disable_preserves_active_marker | cancelled | `disable_and_stop_revoke_activity_and_pending_options` | 100 (expected red) | API 0; logs 0 |
| 37002835428 | disabled_clear_keeps_marker | failure | `clear_revokes_before_late_create_finish_and_stale_set_effects` | 100 (expected red) | API 0; logs 0 |
| 37002855706 | external_set_skips_budget_limited | failure | `external_set_and_resume_reconcile_first_request` | 100 (expected red) | API 0; logs 0 |
| 37002874030 | late_active_set_reinserts_cleared_goal | failure | `clear_revokes_before_late_create_finish_and_stale_set_effects` | 100 (expected red) | API 0; logs 0 |
| 37002893526 | resume_skips_budget_limited | failure | `external_set_and_resume_reconcile_first_request` | 100 (expected red) | API 0; logs 0 |
| 37002912887 | stop_preserves_active_marker | cancelled | `disable_and_stop_revoke_activity_and_pending_options` | 100 (expected red) | API 0; logs 0 |
| 37002931745 | timestamp_read_failure_keeps_known_marker | cancelled | `read_failure_revokes_activity_and_next_turn_recovers` | 100 (expected red) | API 0; logs 0 |
| 37002951066 | turn_start_requires_baseline | failure | `turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal` | 100 (expected red) | API 0; logs 0 |
| 37002970329 | usage_limit_retains_sleep | cancelled | `automatic_stop_revokes_activity_for_error_and_usage_limit` | 100 (expected red) | API 0; logs 0 |

13/13 named narrowing mutations have observed failing final-retry tests and a hosted process exit 100 in their fetched logs; 0 survivors reported in the producer artifact. Mutation patches were not executed by the panel. The panel verified the named red evidence, not all additional failures in each mutated suite.

```text
37002732285
core	UNKNOWN STEP	2026-10-02T12:07:45.2485856Z   TRY 3 FAIL [   0.755s] (3331/4874) codex-core::all suite::goal_activity::accounting_budget_keeps_sleep_without_automatic_continuation
core	UNKNOWN STEP	2026-10-02T12:07:45.2618319Z ##[error]Process completed with exit code 100.
37002755500
small	UNKNOWN STEP	2026-10-02T11:54:25.3244537Z   TRY 3 FAIL [   0.006s] ( 20/238) codex-goal-extension::activity_publisher publisher_refuses_stale_revision_and_recovers_unknown_state
small	UNKNOWN STEP	2026-10-02T11:54:25.3347070Z ##[error]Process completed with exit code 100.
37002777813
core	codex-core tests	2026-10-02T12:11:32.9973696Z   TRY 3 FAIL [   1.545s] (3333/4874) codex-core::all suite::goal_activity::create_goal_changes_the_next_sampling_tools::complete
core	codex-core tests	2026-10-02T12:11:33.0132791Z ##[error]Process completed with exit code 100.
37002797120
core	codex-core tests	2026-10-02T12:12:10.7520724Z   TRY 3 FAIL [   0.466s] (3327/4874) codex-core::all suite::goal_activity::clear_revokes_before_late_create_finish_and_stale_set_effects
core	codex-core tests	2026-10-02T12:12:10.7654455Z ##[error]Process completed with exit code 100.
37002815598
small	UNKNOWN STEP	2026-10-02T11:58:19.3991931Z   TRY 3 FAIL [   0.150s] ( 33/238) codex-goal-extension::goal_extension_backend goal_activity::disable_and_stop_revoke_activity_and_pending_options
small	UNKNOWN STEP	2026-10-02T11:58:19.4141526Z ##[error]Process completed with exit code 100.
37002835428
core	codex-core tests	2026-10-02T12:18:39.4789262Z   TRY 3 FAIL [   1.031s] (3326/4874) codex-core::all suite::goal_activity::clear_revokes_before_late_create_finish_and_stale_set_effects
core	codex-core tests	2026-10-02T12:18:39.4921894Z ##[error]Process completed with exit code 100.
37002855706
core	codex-core tests	2026-10-02T12:20:45.2075859Z   TRY 3 FAIL [   0.243s] (3336/4874) codex-core::all suite::goal_activity::external_set_and_resume_reconcile_first_request::budget_limited
core	codex-core tests	2026-10-02T12:20:45.3993044Z ##[error]Process completed with exit code 100.
37002874030
core	codex-core tests	2026-10-02T12:22:18.7744691Z   TRY 3 FAIL [   0.519s] (3327/4874) codex-core::all suite::goal_activity::clear_revokes_before_late_create_finish_and_stale_set_effects
core	codex-core tests	2026-10-02T12:22:18.7905391Z ##[error]Process completed with exit code 100.
37002893526
core	codex-core tests	2026-10-02T12:27:27.1909611Z   TRY 3 FAIL [   0.698s] (3335/4874) codex-core::all suite::goal_activity::external_set_and_resume_reconcile_first_request::budget_limited
core	codex-core tests	2026-10-02T12:27:27.2883828Z ##[error]Process completed with exit code 100.
37002912887
small	UNKNOWN STEP	2026-10-02T12:09:28.0421721Z   TRY 3 FAIL [   0.170s] ( 35/238) codex-goal-extension::goal_extension_backend goal_activity::disable_and_stop_revoke_activity_and_pending_options
small	UNKNOWN STEP	2026-10-02T12:09:28.0550063Z ##[error]Process completed with exit code 100.
37002931745
small	Small crates tests	2026-10-02T12:13:59.9072478Z   TRY 3 FAIL [   0.235s] ( 36/238) codex-goal-extension::goal_extension_backend goal_activity::read_failure_revokes_activity_and_next_turn_recovers
small	Small crates tests	2026-10-02T12:13:59.9201589Z ##[error]Process completed with exit code 100.
37002951066
core	codex-core tests	2026-10-02T12:27:41.8348030Z   TRY 3 FAIL [   0.242s] (3337/4874) codex-core::all suite::goal_activity::turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal
core	codex-core tests	2026-10-02T12:27:41.8478106Z ##[error]Process completed with exit code 100.
37002970329
small	Small crates tests	2026-10-02T12:15:50.2100983Z   TRY 3 FAIL [   0.150s] ( 32/238) codex-goal-extension::goal_extension_backend goal_activity::automatic_stop_revokes_activity_for_error_and_usage_limit
small	Small crates tests	2026-10-02T12:15:50.2214528Z ##[error]Process completed with exit code 100.
```

## Validation receipt

This compact extraction generator asserts that every mutant has its intended named TRY 3 FAIL and a process exit 100. The generator itself exited 0; this is evidence-integrity validation, not a passing product gate. The verdict-format validator checks exactly one verdict-findings block, valid JSON, one unique surface row, a one-word verdict, and matching pinned G1/candidate references. Its actual exit is recorded in the panel handoff note.

## Logbook

Workflow heads identify dispatch context, not checkout identity. Named failures were found even on cancelled workflows; inspecting only overall conclusions would incorrectly classify that evidence. Full raw logs remain task-scoped scratch, not attached; only bounded relevant lines are persisted as the outcome. No source-task board mutation was made.
