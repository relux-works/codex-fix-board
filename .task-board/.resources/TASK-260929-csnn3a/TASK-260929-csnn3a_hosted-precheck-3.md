# TASK-260929-csnn3a hosted precheck 3 (CR rev 2)

Worktree tree: f0cf63cd9fc511340d23e680f43e846403157f62. Snapshot commit 53c4e843, run 37441567186: lanes {'small': 'success', 'app-server': 'success', 'core': 'success', 'lint': 'success'}. All green.

Mutants: 9 total, 9 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| ack_skipped_when_websockets_enabled | 37441591474 | core | exec_completion_sampling_ack, http_fallback_submission_acknowledges, websocket_submission_acknowledges |
| acknowledge_on_recording | 37441615109 | core | aborted_submission_retries_and_samples_once, exec_completion_finishing_task_gets_sampling_wake, exec_completion_sampling_ack |
| backoff_skips_post_failback_rewake | 37441638357 | core | exec_completion_lost_reservation_after_winner_idle_rewakes |
| compact_acks_staged | 37441663087 | core | exec_completion_compaction_omission_keeps_receipt_pending |
| fail_first_tracked_only | 37441688497 | core | exec_completion_finishing_task_gets_sampling_wake |
| guardian_prep_drops_exec_fragments | 37441714373 | core | exec_completion_guardian_prompt_preserves_receipt |
| reserved_claim_ignores_identity | 37441739252 | core | reserved_start_backs_off_when_turn_replaced |
| reserved_claim_ignores_task | 37441762646 | core | reserved_start_backs_off_when_turn_busy |
| retain_only_task_present | 37441786360 | core | exec_completion_survives_cleared_idle_reservation |
