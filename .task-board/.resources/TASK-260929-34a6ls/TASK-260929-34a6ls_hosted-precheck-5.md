# TASK-260929-34a6ls hosted precheck 5 (CR rev 3, acknowledge at acceptance)

Worktree tree: 62aecbc1f279a26c154f0e371b8c1995bb7e8226. Snapshot commit df5eae26, run 37411010318: lanes {'core': 'success', 'app-server': 'success', 'lint': 'success', 'small': 'success'}. All green.

Mutants: 12 total, 12 killed, 0 survivors. (fail_after_ack_requeues: its lint lane also fails on clippy, but core runs and its intended test runtime_fail_after_acknowledge_is_noop fails, so it is killed.)

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| ack_after_tool_drain | 37411026391 | lint,core | accepted_response_cancelled_after_created_acknowledges_once, accepted_response_eof_after_output_acknowledges_without_resample, accepted_response_failed_after_created_acknowledges_once |
| ack_gated_on_outcome_success | 37411043931 | core,lint | accepted_response_cancelled_after_created_acknowledges_once, accepted_response_eof_after_output_acknowledges_without_resample, accepted_response_failed_after_created_acknowledges_once |
| ack_on_completed_instead_of_acceptance | 37411060741 | lint,core | accepted_response_cancelled_after_created_acknowledges_once, accepted_response_eof_after_output_acknowledges_without_resample, accepted_response_failed_after_created_acknowledges_once |
| ack_on_lease | 37411078103 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| ack_on_record | 37411093954 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| batch_cap_doubled | 37411110839 | core | nine_pending_completions_batch_eight_and_retain_one, nine_pending_completions_sample_in_capped_batches_without_loss, omitted_receipt_sampled_by_later_request |
| dedup_first_history_item_only | 37411129134 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| fail_after_ack_requeues | 37411146346 | lint,core | input_queue_runtime_cancel_removes_leased_and_unleased_entries, runtime_cancel_removes_leased_and_unleased_entries, runtime_fail_after_acknowledge_is_noop |
| marker_substring_membership | 37411163155 | core | forged_fragment_text_acknowledges_nothing, membership_rejects_a_forged_handle, membership_rejects_altered_payload_under_the_real_handle |
| role_blind_membership | 37411178075 | core | membership_ignores_non_user_messages |
| stale_fail_counts_attempt | 37411192889 | core | runtime_stale_fail_counts_no_attempt |
| suspend_threshold_doubled | 37411207981 | core | runtime_failed_attempts_suspend_on_exhaustion_and_stay_retained, runtime_stale_fail_counts_no_attempt |
