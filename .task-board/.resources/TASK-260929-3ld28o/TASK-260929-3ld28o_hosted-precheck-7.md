# TASK-260929-3ld28o hosted precheck 7

CI ivanopcode/codex, slim relux-ci run 38083359851: snapshot = worktree tree 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7. Lanes: {'lint': 'success', 'small': 'success', 'core': 'success', 'app-server': 'success'}. All green.

Mutants: 16 total, 16 killed, 0 survivors.

| mutant | failing lanes | killing tests |
|---|---|---|
| agent_message_counts_as_state_change | small | model_text_claiming_progress_does_not_set, no_model_writable_bypass_sets_observation |
| agent_message_state_keyword_counts | small | model_text_claiming_progress_does_not_set, no_model_writable_bypass_sets_observation |
| code_mode_nested_file_change_emitted_twice | core | code_mode_leaf_applied_patch_delivered_exactly_once |
| command_execution_counts_as_state_change | small | code_mode_leaf_counts_once_and_wrapper_adds_none, shell_success_does_not_set_observation |
| external_goal_clear_does_not_record | small | backend_external_goal_set_and_clear_record_observation |
| external_goal_set_does_not_record | small | backend_external_goal_set_and_clear_record_observation |
| file_completed_requires_auto_approved | small | applied_file_change_sets_observation, backend_file_change_completed_sets_observation, backend_fresh_runtime_carries_no_observation, code_mode_leaf_counts_once_and_wrapper_adds_none |
| file_failed_counts_as_applied | small | backend_file_change_completed_sets_observation, failed_or_declined_file_change_does_not_set |
| goal_update_complete_only_records | small | backend_goal_update_paused_and_blocked_set_observation |
| identical_plan_always_counts | small | backend_plan_transition_sets_and_identical_does_not, identical_plan_resubmission_does_not_set, no_model_writable_bypass_sets_observation |
| plan_transition_ignores_content | small | backend_plan_transition_sets_and_identical_does_not, plan_status_change_counts_as_transition, plan_step_text_change_counts_as_transition |
| send_input_status_ignores_delivery_result | core | send_input_rejected_compaction_emits_failed_item |
| spawn_followup_message_tools_dropped | small | send_message_and_followup_task_completed_set_observation |
| spawn_only_spawn_agent_counts | small | send_input_completed_sets_observation, send_message_and_followup_task_completed_set_observation |
| spawn_status_ignores_delivery_result | core | spawn_agent_accepted_with_errored_child_emits_completed_item |
| tool_finish_success_records_mutation | small | backend_spawn_followup_sets_but_tool_finish_success_does_not |
