# TASK-260929-2snjbb hosted precheck 7 (CR rev 5)

Worktree tree: 13972f7d936f6280c9b0cae88749c6f5c1a56a9a. Snapshot commit f63366db, run 37578543875: lanes {'small': 'success', 'lint': 'success', 'core': 'success', 'app-server': 'success'}. All green.

Mutants: 16 total, 16 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| apply_goal_settings_before_final_check | 37578561576 | core | late_goal_rejection_leaves_thread_settings_unchanged |
| break_runtime_wait_arm_reentry | 37578579179 | lint,core | scheduled_checkins_fire_through_production_runtime_under_paused_time |
| drop_check_in_registration | 37578596335 | small,core | check_ins_keep_epoch_across_admitted_turns, disabled_policy_never_gates, inactive_or_budget_limited_status_never_gates |
| drop_timer_spawn | 37578612871 | lint,small,core | fired_timer_continuation_survives_turn_start_invalidation, stale_install_never_replaces_newer_generation_timer, scheduled_checkins_fire_through_production_runtime_under_paused_time |
| gate_only_queued_ignoring_armed | 37578629753 | small,core | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, check_ins_keep_epoch_across_admitted_turns |
| keep_handle_in_slot_while_firing | 37578646983 | lint,small,core | fired_timer_continuation_survives_turn_start_invalidation, scheduled_checkins_fire_through_production_runtime_under_paused_time |
| move_final_check_before_awaits | 37578665024 | core | goal_publish_serialized_with_concurrent_arm, late_goal_rejection_leaves_thread_settings_unchanged, receipt_armed_inside_start_task_blocks_automatic_start |
| overgate_non_goal_triggers | 37578682087 | lint,core | goal_background_wait_blocks_goal_but_admits_user_and_followup, goal_background_wait_ignores_non_goal_triggers |
| preserve_ticket_across_invalidation | 37578700699 | small | release_invalidates_ticket_and_reassessment_can_proceed, turn_start_and_steering_invalidate_without_renewing |
| reset_epoch_on_turn_start | 37578719469 | core,small | encrypted_parent_reply_survives_incremental_guardian_reviews, scheduled_checkins_fire_through_production_runtime_under_paused_time, check_ins_keep_epoch_across_admitted_turns |
| reuse_ticket_id | 37578737666 | small,core | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, check_ins_keep_epoch_across_admitted_turns |
| skip_revision_recheck | 37578755970 | small | revision_change_between_check_and_start_rejects, ticket_bypass_still_enforces_revision_and_generation |
| skip_transition_locks_in_publish | 37578773989 | core,lint | goal_publish_rejects_safe_when_mailbox_contended, goal_publish_rejects_safe_when_store_contended, goal_publish_serialized_with_concurrent_arm |
| treat_read_error_as_empty | 37578790835 | small | read_failure_never_treated_as_empty |
| unconditional_slot_replace | 37578808296 | lint,small,core | stale_install_never_replaces_newer_generation_timer, scheduled_checkins_fire_through_production_runtime_under_paused_time |
| warning_repeats | 37578825692 | core,small | scheduled_checkins_fire_through_production_runtime_under_paused_time, completion_after_cap_wakes_without_counting_as_human_input, stalled_subscription_fires_scheduled_checkins |
