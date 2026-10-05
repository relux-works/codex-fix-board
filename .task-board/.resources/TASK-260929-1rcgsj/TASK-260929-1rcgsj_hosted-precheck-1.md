# TASK-260929-1rcgsj hosted precheck 1

Worktree tree: 37fad741767c46d11094adb9be747d5aae83c145. Snapshot commit f2bf01a5, run 37278001051: lanes {'lint': 'success', 'small': 'success', 'app-server': 'success', 'core': 'success'}. All green.

Mutants: 10 total, 10 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| runtime_ack_admits_stale | 37278019338 | core | input_queue_runtime_failed_lease_retries_without_duplicate, runtime_failed_lease_returns_unleased_exactly_once |
| runtime_cancel_admits_leased | 37278038094 | core | input_queue_runtime_cancel_removes_leased_and_unleased_entries, runtime_cancel_removes_leased_and_unleased_entries |
| runtime_enqueue_admits_duplicate | 37278056447 | core | runtime_duplicate_enqueue_does_not_duplicate_delivery |
| runtime_fail_admits_stale | 37278078920 | core | input_queue_runtime_failed_lease_retries_without_duplicate, runtime_failed_lease_returns_unleased_exactly_once |
| runtime_lease_admits_suspended | 37278101178 | core | input_queue_runtime_suspended_entries_never_count_as_trigger, runtime_suspended_entries_are_excluded_from_trigger_and_lease |
| runtime_lease_readmits_leased | 37278122457 | lint,core | input_queue_runtime_entry_survives_drain_as_leased, runtime_duplicate_enqueue_does_not_duplicate_delivery, runtime_entry_survives_lease_until_acknowledged |
| runtime_pending_admits_leased | 37278142989 | lint,core | input_queue_runtime_entry_survives_drain_as_leased, runtime_entry_survives_lease_until_acknowledged |
| runtime_trigger_admits_suspended | 37278163468 | core | input_queue_runtime_suspended_entries_never_count_as_trigger, runtime_suspended_entries_are_excluded_from_trigger_and_lease, runtime_suspended_while_leased_stops_suppressing |
| runtime_wake_fakes_agent_mail | 37278183811 | core | pending_runtime_entry_starts_one_wake_turn_with_exec_completion, two_runtime_entries_still_start_one_wake_turn |
| runtime_wake_omits_trigger | 37278203959 | lint,core | pending_runtime_entry_starts_one_wake_turn_with_exec_completion, two_runtime_entries_still_start_one_wake_turn |
