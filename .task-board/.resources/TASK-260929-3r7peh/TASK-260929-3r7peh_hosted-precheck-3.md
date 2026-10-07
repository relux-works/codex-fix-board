# TASK-260929-3r7peh hosted precheck 3

Worktree tree: dbd39ab8c59adabe27ebb25838003680214c8d14. Snapshot commit 74434fa5, run 37618361186: lanes {'lint': 'success', 'core': 'success', 'app-server': 'success', 'small': 'success'}. All green. Precheck 1 had a red base; in precheck 2 m9 survived and was replaced.

Mutants: 9 total, 9 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| m1_arm_by_default | 37618386393 | app-server,core,small | _disabled_expects, _enabled_expects, _escalated_expects |
| m2_derive_child_from_not_exec | 37618411404 | lint,core | async_notification_child_of_headless_parent_stays_unavailable, async_notification_roots_follow_host_session_source, encrypted_parent_reply_survives_incremental_guardian_reviews |
| m3_accept_opt_in_on_unavailable_host | 37618436832 | lint,core | exec_notification_opt_in_refused_on_headless_exec, notify_on_exit_refused_before_execution_on_unavailable_host |
| m4_release_skips_mailbox_cancel | 37618462152 | core | release_disarms_frees_slot_and_cancels_pending_wake |
| m5_read_skips_owner_verify | 37618487494 | core | notification_owner_resolves_launch_owner_across_tool_calls, read_rejects_foreign_receipt |
| m6_handler_drops_opt_in | 37618514232 | core | exec_notification_capacity_refuses_65th_and_default_still_runs, exec_notification_opt_in_arms_and_read_returns_terminal_output, exec_notification_release_disarms_without_killing |
| m7_goal_never_enables | 37618540192 | small,lint,core | background_wait_activates_only_on_available_hosts, background_wait_activation_gates_goal_but_admits_user_input, scheduled_checkins_fire_through_production_runtime_under_paused_time |
| m8_goal_always_enables | 37618565570 | small,core | background_wait_activates_only_on_available_hosts, background_wait_inactive_on_unavailable_host_auto_continues, scheduled_checkins_fire_through_production_runtime_under_paused_time |
| m9_recheck_skips_retention_drop | 37618590261 | core | enqueue_published_completion_drops_ghost_retention |
