# TASK-260929-2gp04j hosted precheck 8 (rev 4 + replace-path test)

Worktree tree: 65ad71d230e7d7ac5923b8f88739a504b0fc1d08. Snapshot commit a37e2ebc, run 37263271056: lanes {'lint': 'success', 'small': 'success', 'core': 'success', 'app-server': 'success'}. All green.

Mutants: 25 total, 25 killed, 0 survivors.

| mutant | run | killing tests |
|---|---|---|
| abort_read_failure_keeps_marker | 37263286435 | turn_abort_accounting_read_failure_revokes_activity_and_next_turn_recovers |
| budget_limited_admits_continuation | 37263301509 | accounting_budget_keeps_sleep_without_automatic_continuation |
| clear_delete_bypasses_guard | 37263317078 | clear_prepare_failure_revokes_activity_and_next_turn_recovers, clear_returning_decode_failure_revokes_activity_and_next_turn_recovers |
| cleared_revision_accepts_old_read | 37263331927 | publisher_refuses_stale_revision_and_recovers_unknown_state |
| complete_retains_sleep | 37263346161 | complete, external_set_post_write_read_failure_revokes_activity_and_next_turn_recovers, created |
| create_waits_for_finish | 37263362618 | clear_revokes_before_late_create_finish_and_stale_set_effects, disable_mid_turn_removes_sleep_from_next_request |
| disable_preserves_active_marker | 37263377567 | disable_and_stop_revoke_activity_and_pending_options, clear_revokes_before_late_create_finish_and_stale_set_effects, disable_mid_turn_removes_sleep_from_next_request |
| disabled_clear_keeps_marker | 37263392780 | clear_revokes_before_late_create_finish_and_stale_set_effects |
| external_set_get_failure_keeps_marker | 37263407731 | encrypted_parent_reply_survives_incremental_guardian_reviews, external_set_get_failure_revokes_activity_and_next_turn_recovers |
| external_set_prepare_failure_keeps_marker | 37263423549 | external_set_prepare_failure_revokes_activity_and_next_turn_recovers |
| external_set_skips_budget_limited | 37263439586 | budget_limited |
| fork_flush_prepare_failure_keeps_marker | 37263454412 | fork_flush_read_failure_revokes_activity_and_next_turn_recovers |
| guard_skips_revocation_on_store_error | 37263469809 | clear_prepare_failure_revokes_activity_and_next_turn_recovers, clear_returning_decode_failure_revokes_activity_and_next_turn_recovers, external_set_post_write_read_failure_revokes_activity_and_next_turn_recovers |
| late_active_set_reinserts_cleared_goal | 37263485560 | clear_revokes_before_late_create_finish_and_stale_set_effects |
| resume_skips_budget_limited | 37263501158 | budget_limited |
| set_objective_update_bypasses_guard | 37263517219 | external_set_post_write_read_failure_revokes_activity_and_next_turn_recovers |
| set_replace_bypasses_guard | 37263531175 | external_set_replace_failure_revokes_activity_and_next_turn_recovers |
| set_status_update_bypasses_guard | 37263544776 | external_set_post_write_read_failure_revokes_activity_and_next_turn_recovers, external_set_prepare_failure_revokes_activity_and_next_turn_recovers |
| stop_preserves_active_marker | 37263560187 | disable_and_stop_revoke_activity_and_pending_options |
| timestamp_read_failure_keeps_known_marker | 37263576096 | clear_returning_decode_failure_revokes_activity_and_next_turn_recovers, external_set_get_failure_revokes_activity_and_next_turn_recovers, external_set_post_write_read_failure_revokes_activity_and_next_turn_recovers |
| tool_finish_accounting_failure_keeps_marker | 37263590894 | tool_finish_accounting_failure_revokes_activity_and_next_turn_recovers |
| turn_error_skips_reconcile_after_stop_failure | 37263605507 | automatic_stop_revokes_activity_for_error_and_usage_limit, turn_error_read_failure_revokes_activity_and_next_turn_recovers |
| turn_start_requires_baseline | 37263619598 | turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal |
| turn_stop_read_failure_keeps_marker | 37263634903 | turn_stop_accounting_read_failure_revokes_activity_and_next_turn_recovers |
| usage_limit_retains_sleep | 37263653941 | automatic_stop_revokes_activity_for_error_and_usage_limit, usage_limited |
