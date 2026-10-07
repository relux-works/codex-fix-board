# TASK-260929-2snjbb hosted precheck 3 (CR rev 2)

Worktree tree: 3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214. Snapshot commit ce274182, run 37539907712: lanes {'app-server': 'success', 'small': 'success', 'lint': 'success', 'core': 'success'}. All green.

Mutants: 9 total, 9 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| drop_check_in_registration | 37539932669 | small | check_ins_keep_epoch_across_admitted_turns, disabled_policy_never_gates, inactive_or_budget_limited_status_never_gates |
| gate_only_queued_ignoring_armed | 37539955446 | small | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, check_ins_keep_epoch_across_admitted_turns |
| overgate_non_goal_triggers | 37539976644 | lint,core | goal_background_wait_blocks_goal_but_admits_user_and_followup, goal_background_wait_ignores_non_goal_triggers |
| preserve_ticket_across_invalidation | 37539997698 | small | release_invalidates_ticket_and_reassessment_can_proceed, turn_start_and_steering_invalidate_without_renewing |
| reset_epoch_on_turn_start | 37540019902 | small | check_ins_keep_epoch_across_admitted_turns, stalled_subscription_fires_scheduled_checkins |
| reuse_ticket_id | 37540043763 | small | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, check_ins_keep_epoch_across_admitted_turns |
| skip_revision_recheck | 37540065393 | small | revision_change_between_check_and_start_rejects, ticket_bypass_still_enforces_revision_and_generation |
| treat_read_error_as_empty | 37540085008 | small | read_failure_never_treated_as_empty |
| warning_repeats | 37540106313 | small | completion_after_cap_wakes_without_counting_as_human_input, stalled_subscription_fires_scheduled_checkins, warning_emitted_once_after_third_check_in_with_exact_text |
