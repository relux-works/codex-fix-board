# TASK-260929-3f6hfg hosted precheck 1

Worktree tree: c83869e576d1e024cfdbb5f63cfe8b83c6e969cb. Snapshot commit 542a2e5c, run 37633617318: lanes {'core': 'success', 'app-server': 'success', 'lint': 'success', 'small': 'success'}. All green.

Mutants: 5 total, 5 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| allow-notify-on-incapable-host | 37633645894 | core,lint,app-server | encrypted_parent_reply_survives_incremental_guardian_reviews, exec_notification_opt_in_refused_on_headless_exec, notify_on_exit_refused_before_execution_on_unavailable_host, headless_host_refuses_notify_on_exit_and_promises_no_wake |
| always-subscribe | 37633676266 | app-server,core | unopted_server_process_does_not_gate_goal_continuation, captured_step_controls_exec_completion_and_write_stdin_output, encrypted_parent_reply_survives_incremental_guardian_reviews, exec_notification_capacity_refuses_65th_and_default_still_runs |
| drop-wake | 37633707303 | app-server,core | notified_exec_exit_wakes_gated_goal_with_receipt_fragment, user_burst_during_background_wait_admitted_without_loss_or_duplication, exec_notification_opt_in_arms_and_read_returns_terminal_output, opted_in_exit_enqueues_wake_without_turn |
| silence-ignores-armed | 37633736582 | small,core,app-server | at_most_three_check_ins_per_human_input, check_ins_fire_at_30_60_120_minutes_fake_time, check_ins_keep_epoch_across_admitted_turns, clear_stop_and_resume_reset_transient_wait_state |
| wake-without-fragment | 37633768227 | core,app-server | aborted_submission_retries_and_samples_once, accepted_response_cancelled_after_created_acknowledges_once, accepted_response_eof_after_output_acknowledges_without_resample, accepted_response_failed_after_created_acknowledges_once |
