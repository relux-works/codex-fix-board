# TASK-260929-2is91w hosted precheck 8

CI ivanopcode/codex, slim relux-ci run 38092565667: snapshot = worktree tree ef4eb6ff644eee2a950b493b675fb86f7b3301c2. Lanes: {'lint': 'success', 'core': 'success', 'small': 'success', 'app-server': 'success'}. All green.

Mutants: 12 total, 12 killed, 0 survivors.

| mutant | failing lanes | killing tests |
|---|---|---|
| exec_notify_ignores_host | core | exec_notify_requires_available_host, native_mail_wait_requires_available_host |
| exec_notify_ignores_opt_in | core | excluded_exec_command_disables_exec_notify, exec_notify_requires_notify_opt_in, missing_exec_command_schema_disables_exec_notify |
| exec_notify_ignores_receipt | core | excluded_receipt_tool_disables_exec_notify, exec_notify_requires_receipt_control |
| exec_notify_ignores_stdin | core | exec_notify_requires_write_stdin |
| native_mail_wait_ignores_host | core | native_mail_wait_requires_available_host |
| native_mail_wait_ignores_policy | core | acknowledged_subscription_does_not_flip_waiting_capabilities, code_mode_only_hides_nested_waits_but_keeps_direct_sleep, excluded_exec_command_disables_exec_notify, excluded_receipt_tool_disables_exec_notify, exec_notify_requires_notify_opt_in, exec_notify_requires_receipt_control, exec_notify_requires_write_stdin, exec_notify_true_with_host_opt_in_and_controls, missing_exec_command_schema_disables_exec_notify, native_mail_wait_requires_installed_policy, pending_and_acknowledged_work_does_not_flip_flags |
| native_wait_bare_name_match | core | discovered_deferred_v1_wait_counts_with_native_provenance, discovered_v1_wait_updates_next_step_snapshot, foreign_dynamic_wait_agent_does_not_claim_native_wait, foreign_dynamic_wait_agent_with_native_disabled_yields_none, v2_wait_disabled_with_namespaced_decoy_yields_none |
| native_wait_ignores_discovered | core | discovered_deferred_v1_wait_counts_with_native_provenance, discovered_v1_wait_updates_next_step_snapshot |
| native_wait_v1_only | core | custom_v2_namespace_reports_its_configured_name, exec_notify_requires_available_host, exec_notify_requires_notify_opt_in, exec_notify_requires_receipt_control, exec_notify_requires_write_stdin, exec_notify_true_with_host_opt_in_and_controls, missing_exec_command_schema_disables_exec_notify, native_mail_wait_requires_available_host, native_mail_wait_requires_host_and_installed_policy, native_mail_wait_requires_installed_policy, v2_wait_agent_carries_its_configured_name, v2_wait_tool_reports_its_configured_name |
| native_wait_v2_only | core | discovered_deferred_v1_wait_counts_with_native_provenance, discovered_v1_wait_updates_next_step_snapshot, v1_wait_agent_carries_its_namespaced_name, v1_wait_tool_reports_its_namespaced_name |
| sleep_counts_nested_or_deferred | core | deferred_sleep_does_not_count_until_discovered, nested_only_sleep_does_not_count |
| stdin_counts_nested | core | code_mode_only_hides_nested_waits_but_keeps_direct_sleep, nested_only_write_stdin_does_not_count |
