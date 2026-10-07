# TASK-260929-2snjbb hosted precheck 4 (CR rev 3)

Worktree tree: 16a538869452dc36d083b8ab3c3e63a1e57c7285. Snapshot commit c7652275, run 37550767559: lanes {'app-server': 'success', 'core': 'success', 'lint': 'success', 'small': 'success'}. All green.

Mutants: 13 total, 13 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| drop_check_in_registration | 37550786061 | small | check_ins_keep_epoch_across_admitted_turns, disabled_policy_never_gates, inactive_or_budget_limited_status_never_gates |
| drop_timer_spawn | 37550804014 | lint,small | fired_timer_continuation_survives_turn_start_invalidation, scheduled_checkins_fire_via_runtime_under_paused_time, stale_install_never_replaces_newer_generation_timer |
| gate_only_queued_ignoring_armed | 37550823483 | small | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, check_ins_keep_epoch_across_admitted_turns |
| keep_handle_in_slot_while_firing | 37550841452 | lint,small | fired_timer_continuation_survives_turn_start_invalidation |
| no_late_recheck | 37550859181 | core,lint | receipt_armed_after_admission_blocks_automatic_start |
| overgate_non_goal_triggers | 37550876321 | lint,core | goal_background_wait_blocks_goal_but_admits_user_and_followup, goal_background_wait_ignores_non_goal_triggers |
| preserve_ticket_across_invalidation | 37550895448 | small | release_invalidates_ticket_and_reassessment_can_proceed, turn_start_and_steering_invalidate_without_renewing |
| reset_epoch_on_turn_start | 37550913595 | small | check_ins_keep_epoch_across_admitted_turns, scheduled_checkins_fire_via_runtime_under_paused_time, stalled_subscription_fires_scheduled_checkins |
| reuse_ticket_id | 37550931976 | small | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, check_ins_keep_epoch_across_admitted_turns |
| skip_revision_recheck | 37550948899 | small | revision_change_between_check_and_start_rejects, ticket_bypass_still_enforces_revision_and_generation |
| treat_read_error_as_empty | 37550965847 | small | read_failure_never_treated_as_empty |
| unconditional_slot_replace | 37550984504 | small,lint | stale_install_never_replaces_newer_generation_timer |
| warning_repeats | 37551004329 | small | completion_after_cap_wakes_without_counting_as_human_input, scheduled_checkins_fire_via_runtime_under_paused_time, stalled_subscription_fires_scheduled_checkins |
