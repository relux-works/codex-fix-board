# Hosted pre-handoff evidence: TASK-260929-2gp04j (G2), precheck 2

## Snapshot of the exact pre-handoff worktree
- commit `016a4248cf1984b97e786ce8573ad40c9438dfbf` (signed, never landed), tree `4d289590739432aa55c2a3868c2b4a5472b07c92`
- run https://github.com/relux-works/codex/actions/runs/37002709023: **success on all lanes** (lint, small, core,
  app-server). Precheck 1's failure `suite::goal_activity::disable_mid_turn_removes_sleep_from_next_request` now passes.

## Narrowing mutants: all 13 killed by their intended tests
| mutant | lane | killing test |
| --- | --- | --- |
| budget_limited_admits_continuation | core | accounting_budget_keeps_sleep_without_automatic_continuation |
| cleared_revision_accepts_old_read | small | publisher_refuses_stale_revision_and_recovers_unknown_state |
| complete_retains_sleep | core | create_goal_changes_the_next_sampling_tools::complete |
| create_waits_for_finish | core | clear_revokes_before_late_create_finish_and_stale_set_effects |
| disable_preserves_active_marker | small | disable_and_stop_revoke_activity_and_pending_options |
| disabled_clear_keeps_marker | core | clear_revokes_before_late_create_finish_and_stale_set_effects (survived in precheck 1; now killed) |
| external_set_skips_budget_limited | core | external_set_and_resume_reconcile_first_request::budget_limited |
| late_active_set_reinserts_cleared_goal | core | clear_revokes_before_late_create_finish_and_stale_set_effects |
| resume_skips_budget_limited | core | external_set_and_resume_reconcile_first_request::budget_limited |
| stop_preserves_active_marker | small | disable_and_stop_revoke_activity_and_pending_options |
| timestamp_read_failure_keeps_known_marker | small | read_failure_revokes_activity_and_next_turn_recovers |
| turn_start_requires_baseline | core | turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal |
| usage_limit_retains_sleep | small | automatic_stop_revokes_activity_for_error_and_usage_limit |

Mutant runs (lanes beyond the needed one cancelled): 37002732285 37002755500 37002777813 37002797120 37002815598 37002835428 37002855706 37002874030 37002893526 37002912887 37002931745 37002951066 37002970329 
