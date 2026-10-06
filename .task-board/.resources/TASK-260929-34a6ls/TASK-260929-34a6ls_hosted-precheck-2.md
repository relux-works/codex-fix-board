# TASK-260929-34a6ls hosted precheck 2

Worktree tree: 8e03a0e18d68ac6891de673dd8d55bf0dce5c30e. Snapshot commit bfbe241e, run 37383604313: lanes {'app-server': 'success', 'small': 'success', 'core': 'success', 'lint': 'success'}. All green, with codex-queue-extension selected on relux/main. Precheck 1 had a red base, so its mutant results are void.

Mutants: 8 total, 8 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| ack_on_lease | 37383628652 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| ack_on_record | 37383653061 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| batch_cap_doubled | 37383676154 | core | nine_pending_completions_batch_eight_and_retain_one, nine_pending_completions_sample_in_capped_batches_without_loss, omitted_receipt_sampled_by_later_request |
| dedup_first_history_item_only | 37383698222 | core | aborted_submission_retries_and_samples_once, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin |
| marker_substring_membership | 37383724007 | core | forged_fragment_text_acknowledges_nothing, membership_rejects_a_forged_handle, membership_rejects_altered_payload_under_the_real_handle |
| role_blind_membership | 37383746703 | core | membership_ignores_non_user_messages |
| stale_fail_counts_attempt | 37383769770 | core | runtime_stale_fail_counts_no_attempt |
| suspend_threshold_doubled | 37383793098 | core | runtime_failed_attempts_suspend_on_exhaustion_and_stay_retained, runtime_stale_fail_counts_no_attempt |
