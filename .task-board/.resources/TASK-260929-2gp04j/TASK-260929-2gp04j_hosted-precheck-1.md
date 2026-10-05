# Hosted pre-handoff evidence: TASK-260929-2gp04j (G2 goal-activity-publisher-hooks), precheck 1

## Snapshot of the exact pre-handoff worktree
- commit `0b0ea00e4bc96460459554dfd26821aa02294f10` (signed, never landed), tree `c38cc80263669f4e4ce18c02e13db47aaad488de`
- run https://github.com/relux-works/codex/actions/runs/36996435872: lint, small and app-server **success**; core **FAILURE**
- core: 4874 run, 4873 passed, **1 failed** (deterministic, 3/3 tries):
  `suite::goal_activity::disable_mid_turn_removes_sleep_from_next_request`, which panicked at
  core/tests/suite/goal_activity_tests.rs:203. The test expects the marker to be gone (`None`) after the mid-turn disable,
  but it is still `Some(GoalActivity { revision: 2, state: Active })`. AC row 6 ("thread stop and feature disable remove
  the marker") is therefore NOT met on hosted.

## Narrowing mutants (13; each applied on the snapshot tree; the always-failing test above is ignored)
| mutant | lane | intended killing test failed? | result |
| --- | --- | --- | --- |
| budget_limited_admits_continuation | core | accounting_budget_keeps_sleep_without_automatic_continuation | killed |
| cleared_revision_accepts_old_read | small | publisher_refuses_stale_revision_and_recovers_unknown_state | killed |
| complete_retains_sleep | core | create_goal_changes_the_next_sampling_tools::complete | killed |
| create_waits_for_finish | core | clear_revokes_before_late_create_finish_and_stale_set_effects | killed |
| disable_preserves_active_marker | small | disable_and_stop_revoke_activity_and_pending_options | killed |
| external_set_skips_budget_limited | core | external_set_and_resume_reconcile_first_request::budget_limited | killed |
| late_active_set_reinserts_cleared_goal | core | clear_revokes_before_late_create_finish_and_stale_set_effects | killed |
| resume_skips_budget_limited | core | external_set_and_resume_reconcile_first_request::budget_limited | killed |
| stop_preserves_active_marker | small | disable_and_stop_revoke_activity_and_pending_options | killed |
| timestamp_read_failure_keeps_known_marker | small | read_failure_revokes_activity_and_next_turn_recovers | killed |
| turn_start_requires_baseline | core | turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal | killed |
| usage_limit_retains_sleep | small | automatic_stop_revokes_activity_for_error_and_usage_limit | killed |
| **disabled_clear_keeps_marker** | core | clear_revokes_before_late_create_finish_and_stale_set_effects did **NOT** fail | **SURVIVED** (only the always-failing disable_mid_turn test failed) |

Runs: wip-1 36996435872; mutants 36996455188, 36996474689, 36996493877, 36996511679, 36996530786, 36996550694,
36996569927, 36996590067, 36996608068, 36996625770, 36996644937, 36996665137, 36996684740. Each mutant's remaining lanes
were cancelled once its lane finished.
