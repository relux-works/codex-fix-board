# TASK-260929-csyzcj hosted precheck 15

CI ivanopcode/codex, slim relux-ci run 38109158922: snapshot = worktree tree b91072a51501101110a4e13061a8c07a242aad6a. Lanes: {'lint': 'success', 'small': 'success', 'app-server': 'success', 'core': 'success'}. All green. Dispatched from relux/ci-next (9f8fdf9a: small lane adds codex-protocol and codex-rollout; workflow-only, not on trunk yet).

Mutants: 12 total, 12 killed, 0 survivors.

| mutant | failing lanes | killing tests |
|---|---|---|
| envelope_author_display_uncapped | small | agent_message_envelope_truncates_legacy_paths_for_display |
| ignore_native_pending | small,core | empty_exec_with_native_pending_waits_and_uses_checkins, native_pending_exhausts_checkins_then_waits_without_deadline, goal_wait_preserves_foreign_sleep_across_register_and_turn_start, goal_wait_registered_parent_gets_single_interrupted_notice, goal_wait_registers_marker_and_wakes_on_child_completion |
| insert_after_mail_check | core | goal_wait_latch_closes_completion_before_registration |
| insert_clobbers_one_foreign | small,core | register_never_clobbers_foreign_sleep, goal_wait_preserves_foreign_sleep_across_register_and_turn_start |
| interrupted_claims_success | core | goal_wait_registered_parent_gets_single_interrupted_notice, interrupted_fragment_renders_exact_notice_body, interrupted_fragment_truncates_overlong_paths_to_hard_cap, interrupted_notice_is_queue_only_without_claiming_success |
| interrupted_notice_delivered_twice | core | goal_wait_registered_parent_gets_single_interrupted_notice |
| interrupted_sender_path_uncapped | core | interrupted_fragment_truncates_overlong_paths_to_hard_cap |
| legacy_long_path_rejected_by_shared_parser | small | agent_path_accepts_legacy_path_over_total_cap |
| legacy_paths_rejected_by_shared_parser | core,small | resume_agent_preserves_legacy_overlong_path, agent_message_envelope_truncates_legacy_paths_for_display, agent_path_accepts_legacy_overlong_segment, agent_path_display_truncates_overlong_path, get_rollout_history_preserves_legacy_agent_path |
| skip_failed_lookups | core | owned_children_inspection_propagates_failed_lookups |
| spawn_task_name_length_unchecked | small,core | agent_path_join_new_rejects_overlong_segment, spawn_agent_v2_rejects_overlong_task_name |
| unconditional_remove | small,core | conditional_remove_only_removes_owned_id, goal_wait_preserves_foreign_sleep_across_register_and_turn_start |
