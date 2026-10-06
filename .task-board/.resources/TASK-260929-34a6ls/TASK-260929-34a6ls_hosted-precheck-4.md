# TASK-260929-34a6ls hosted precheck 4 (CR rev 2)

Worktree tree: ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe. Snapshot commit 292d2959, run 37399295391: lanes {'core': 'success', 'lint': 'success', 'small': 'success', 'app-server': 'success'}. All green. Precheck 3 had a red base, so its mutant results are void. The first run of marker_substring_membership failed in the runner's 'Free runner disk' step (infrastructure) and was re-run.

Mutants: 9 total, 9 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| ack_after_tool_drain | 37399313769 | core | completed_response_with_blocked_tool_acknowledges_before_interrupt |
| ack_on_lease | 37399333004 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| ack_on_record | 37399354479 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| batch_cap_doubled | 37399374461 | core | conversation_start_audio_text_close_round_trip, nine_pending_completions_batch_eight_and_retain_one, nine_pending_completions_sample_in_capped_batches_without_loss |
| dedup_first_history_item_only | 37399393587 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| marker_substring_membership | 37402888227 | core | forged_fragment_text_acknowledges_nothing, membership_rejects_a_forged_handle, membership_rejects_altered_payload_under_the_real_handle |
| role_blind_membership | 37399446896 | core | membership_ignores_non_user_messages |
| stale_fail_counts_attempt | 37399465757 | core | runtime_stale_fail_counts_no_attempt |
| suspend_threshold_doubled | 37399486308 | core | runtime_failed_attempts_suspend_on_exhaustion_and_stay_retained, runtime_stale_fail_counts_no_attempt |
