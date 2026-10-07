# TASK-260929-2snjbb hosted precheck 2

Worktree tree: ffa1c230e68efdb2a7de81099ce670927c825c02. Snapshot commit 3ea2ac72, run 37530053147: lanes {'small': 'success', 'lint': 'success', 'app-server': 'success', 'core': 'success'}. All green. Precheck 1 had a red base, so its mutant results are void.

Mutants: 7 total, 7 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| gate_only_queued_ignoring_armed | 37530082819 | small | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, clear_stop_and_resume_reset_transient_wait_state |
| overgate_non_goal_triggers | 37530108526 | core,lint | goal_background_wait_blocks_goal_but_admits_user_and_followup, goal_background_wait_ignores_non_goal_triggers |
| preserve_ticket_across_invalidation | 37530135461 | small | release_invalidates_ticket_and_reassessment_can_proceed, turn_start_and_steering_invalidate_without_renewing |
| reuse_ticket_id | 37530162208 | small | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, completion_after_cap_wakes_without_counting_as_human_input |
| skip_revision_recheck | 37530189584 | small | revision_change_between_check_and_start_rejects, ticket_bypass_still_enforces_revision_and_generation |
| treat_read_error_as_empty | 37530215463 | small | read_failure_never_treated_as_empty |
| warning_repeats | 37530240516 | small | completion_after_cap_wakes_without_counting_as_human_input, warning_emitted_once_after_third_check_in_with_exact_text |
