# TASK-260929-csnn3a hosted precheck 2

Worktree tree: 3e3f73576ad3ed852711023df46ad5bd2dccda6c. Snapshot commit 91c90e94, run 37430403364: lanes {'small': 'success', 'core': 'success', 'lint': 'success', 'app-server': 'success'}. All green. Precheck 1 had a red base, so its mutant results are void.

Mutants: 8 total, 8 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| ack_skipped_when_websockets_enabled | 37430424561 | core | exec_completion_sampling_ack, http_fallback_submission_acknowledges, websocket_submission_acknowledges |
| acknowledge_on_recording | 37430446385 | core | aborted_submission_retries_and_samples_once, exec_completion_finishing_task_gets_sampling_wake, exec_completion_sampling_ack |
| compact_acks_staged | 37430468861 | core | exec_completion_compaction_omission_keeps_receipt_pending |
| fail_first_tracked_only | 37430491098 | core | exec_completion_finishing_task_gets_sampling_wake |
| guardian_prep_drops_exec_fragments | 37430511988 | core | exec_completion_guardian_prompt_preserves_receipt |
| reserved_claim_ignores_identity | 37430532942 | core | reserved_start_backs_off_when_turn_replaced |
| reserved_claim_ignores_task | 37430554179 | core | reserved_start_backs_off_when_turn_busy |
| retain_only_task_present | 37430576321 | core | exec_completion_survives_cleared_idle_reservation |
