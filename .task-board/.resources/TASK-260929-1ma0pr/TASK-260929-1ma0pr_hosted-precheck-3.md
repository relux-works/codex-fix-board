# TASK-260929-1ma0pr hosted precheck 3 (CR rev 2)

Worktree tree: 5b2ea16af484965b3dd34f6ca4198dd903732541. Snapshot commit a743b625. Workflow: relux-ci from ci/relux-ci-queue, which adds codex-queue-extension to the small and lint lanes.

Snapshot runs (all four lanes green in each). The first dispatch was cancelled by the per-SHA concurrency group and is superseded:
- 37317650053: small, core, app-server, lint all success
- 37349767142: all success. Small 260/260, including codex-queue-extension::queue_service forged_exec_completion_payload_is_skipped_without_panic and drain_leaves_persisted_queued_message_for_a_later_start. Core 4967 passed, 0 flaky, including suite::runtime_mailbox::two_runtime_entries_still_start_one_wake_turn
- 37352331583: all success
Race check: two_runtime_entries_still_start_one_wake_turn failed 3/3 tries on rev-1 tree 808000cb (run 37312042951). It is green in all 3 rev-2 runs.

Mutants: 10 total, 10 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| m1-fragment-cap-769 | 37317381008 | core | nine_pending_completions_batch_eight_and_retain_one |
| m10-follow-up-readmits-runtime | 37317410177 | core | in_turn_follow_up_ignores_idle_only_runtime_entries, nine_pending_completions_sample_in_capped_batches_without_loss, two_runtime_entries_still_start_one_wake_turn |
| m2-escape-drops-gt | 37317438139 | core | fragment_escapes_marker_injection_and_newlines |
| m3-classifier-rejects-exec-source | 37317464801 | core | fragment_escapes_marker_injection_and_newlines, fragment_is_classified_as_internal_context_not_user_text, fragment_matcher_requires_the_wrapper_and_the_exec_source |
| m4-batch-cap-9 | 37317490875 | core | nine_pending_completions_batch_eight_and_retain_one, nine_pending_completions_sample_in_capped_batches_without_loss |
| m5-kind-user-prefixed | 37317518170 | core | fragment_is_classified_as_internal_context_not_user_text, fragment_renders_all_fields_inside_the_internal_context_wrapper |
| m6-serialize-admits-empty | 37317545621 | lint,core | exec_completion_variant_refuses_serialization |
| m7-user-input-always-emits-order | 37317574233 | core | user_input_variant_serializes_byte_identically |
| m8-record-persists-trigger-metadata | 37317600437 | core,lint | wake_turn_persists_only_contextual_response_items_and_resume_stays_silent |
| m9-pending-admits-suspended | 37317628533 | core,lint | input_queue_runtime_suspended_entries_never_count_as_trigger, runtime_suspended_entries_are_excluded_from_trigger_and_lease |
