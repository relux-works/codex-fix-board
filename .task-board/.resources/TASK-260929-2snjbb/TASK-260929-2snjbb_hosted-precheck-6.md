# TASK-260929-2snjbb hosted precheck 6 (CR rev 4)

Worktree tree: c7180fab47012a651662cd207a48caafdf7b10db. Snapshot commit 6abf59d5, run 37569076583: lanes {'small': 'success', 'core': 'success', 'app-server': 'success', 'lint': 'success'}. All green. Precheck 5 had a red base, so its mutant results are void.

Mutants: 15 total, 15 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| apply_goal_settings_before_final_check | 37569092438 | core | late_goal_rejection_leaves_thread_settings_unchanged |
| break_runtime_wait_arm_reentry | 37569106946 | lint,core | scheduled_checkins_fire_through_production_runtime_under_paused_time |
| drop_check_in_registration | 37569121979 | small,core | check_ins_keep_epoch_across_admitted_turns, disabled_policy_never_gates, inactive_or_budget_limited_status_never_gates |
| drop_timer_spawn | 37569137077 | lint,core,small | scheduled_checkins_fire_through_production_runtime_under_paused_time, fired_timer_continuation_survives_turn_start_invalidation, stale_install_never_replaces_newer_generation_timer |
| gate_only_queued_ignoring_armed | 37569152218 | core,small | scheduled_checkins_fire_through_production_runtime_under_paused_time, at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time |
| keep_handle_in_slot_while_firing | 37569167785 | small,lint,core | fired_timer_continuation_survives_turn_start_invalidation, scheduled_checkins_fire_through_production_runtime_under_paused_time |
| move_final_check_before_awaits | 37569183037 | core | late_goal_rejection_leaves_thread_settings_unchanged, receipt_armed_inside_start_task_blocks_automatic_start |
| overgate_non_goal_triggers | 37569198182 | lint,core | goal_background_wait_blocks_goal_but_admits_user_and_followup, goal_background_wait_ignores_non_goal_triggers |
| preserve_ticket_across_invalidation | 37569213125 | small | release_invalidates_ticket_and_reassessment_can_proceed, turn_start_and_steering_invalidate_without_renewing |
| reset_epoch_on_turn_start | 37569228520 | small,core | check_ins_keep_epoch_across_admitted_turns, stalled_subscription_fires_scheduled_checkins, scheduled_checkins_fire_through_production_runtime_under_paused_time |
| reuse_ticket_id | 37569243904 | small,core | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, check_ins_keep_epoch_across_admitted_turns |
| skip_revision_recheck | 37569260011 | small | revision_change_between_check_and_start_rejects, ticket_bypass_still_enforces_revision_and_generation |
| treat_read_error_as_empty | 37569275012 | small | read_failure_never_treated_as_empty |
| unconditional_slot_replace | 37569290755 | lint,small | stale_install_never_replaces_newer_generation_timer |
| warning_repeats | 37569305975 | small,core | completion_after_cap_wakes_without_counting_as_human_input, stalled_subscription_fires_scheduled_checkins, warning_emitted_once_after_third_check_in_with_exact_text |
