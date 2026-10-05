# TASK-260929-1ma0pr hosted precheck 2

Worktree tree: 808000cbd14914847c7cd418f444dd9232281ddc. Snapshot commit 34cf97ac, run 37302805027: lanes {'app-server': 'success', 'lint': 'success', 'core': 'success', 'small': 'success'}. All green. (Precheck 1 had a red base; its mutant results are void.)

Mutants: 10 total, 10 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| m1-fragment-cap-769 | 37302828071 | core | nine_pending_completions_batch_eight_and_retain_one |
| m10-follow-up-readmits-runtime | 37302850331 | core | in_turn_follow_up_ignores_idle_only_runtime_entries, nine_pending_completions_sample_in_capped_batches_without_loss |
| m2-escape-drops-gt | 37302873701 | core | fragment_escapes_marker_injection_and_newlines, two_runtime_entries_still_start_one_wake_turn |
| m3-classifier-rejects-exec-source | 37302897088 | core | conversation_start_audio_text_close_round_trip, fragment_escapes_marker_injection_and_newlines, fragment_is_classified_as_internal_context_not_user_text |
| m4-batch-cap-9 | 37302920627 | core | nine_pending_completions_batch_eight_and_retain_one, two_runtime_entries_still_start_one_wake_turn |
| m5-kind-user-prefixed | 37302942434 | core | fragment_is_classified_as_internal_context_not_user_text, fragment_renders_all_fields_inside_the_internal_context_wrapper, two_runtime_entries_still_start_one_wake_turn |
| m6-serialize-admits-empty | 37302964089 | core,lint | exec_completion_variant_refuses_serialization |
| m7-user-input-always-emits-order | 37302986386 | core | two_runtime_entries_still_start_one_wake_turn, user_input_variant_serializes_byte_identically |
| m8-record-persists-trigger-metadata | 37303009610 | lint,core | wake_turn_persists_only_contextual_response_items_and_resume_stays_silent |
| m9-pending-admits-suspended | 37303033462 | lint,core | input_queue_runtime_suspended_entries_never_count_as_trigger, runtime_suspended_entries_are_excluded_from_trigger_and_lease |
