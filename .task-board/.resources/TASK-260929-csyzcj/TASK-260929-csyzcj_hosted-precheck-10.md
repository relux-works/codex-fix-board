# TASK-260929-csyzcj hosted precheck 10

CI ivanopcode/codex, slim relux-ci run 38053090893: snapshot = worktree tree 9ccda9214ac5b9f0ddb5533b77418d0f2045d74b. Lanes: {'lint': 'success', 'core': 'success', 'small': 'success', 'app-server': 'success'}. All green.

Mutants: 8 total, 8 killed, 0 survivors.

| mutant | failing lanes | killing tests |
|---|---|---|
| ignore_native_pending | small,core | empty_exec_with_native_pending_waits_and_uses_checkins, native_pending_exhausts_checkins_then_waits_without_deadline, goal_wait_preserves_foreign_sleep_across_register_and_turn_start, goal_wait_registered_parent_gets_single_interrupted_notice, goal_wait_registers_marker_and_wakes_on_child_completion |
| insert_after_mail_check | core | goal_wait_latch_closes_completion_before_registration |
| insert_clobbers_one_foreign | core,small | goal_wait_preserves_foreign_sleep_across_register_and_turn_start, register_never_clobbers_foreign_sleep |
| interrupted_claims_success | core | goal_wait_registered_parent_gets_single_interrupted_notice, interrupted_fragment_renders_exact_notice_body, interrupted_fragment_truncates_overlong_paths_to_hard_cap, interrupted_notice_is_queue_only_without_claiming_success |
| interrupted_notice_delivered_twice | core | goal_wait_registered_parent_gets_single_interrupted_notice |
| interrupted_sender_path_uncapped | core | interrupted_fragment_truncates_overlong_paths_to_hard_cap |
| skip_failed_lookups | core | owned_children_inspection_propagates_failed_lookups |
| unconditional_remove | small,core | conditional_remove_only_removes_owned_id, goal_wait_preserves_foreign_sleep_across_register_and_turn_start |
