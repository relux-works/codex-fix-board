# TASK-260929-3rdnra hosted precheck 4

Worktree tree: c57fb1b76d54fff5816a1a264a76d497bb80b50d (equal to the snapshot tree, checked with a temp index). Snapshot f1dd5d5a4d34 (ci/TASK-260929-3rdnra/wip-4, parent 8a9cf9c = relux/main), ivanopcode/codex relux-ci run 38690480458 (dispatched from relux/ci-next): lint, snapshot small, core and app-server all success.

Mutants: 10 total, 10 killed by named test failures (core lane, all three nextest tries), no compile errors, 0 survivors. The small lane passes for every mutant as expected (core-only code).

| Mutant | Killed | Example killing tests |
| --- | --- | --- |
| v1_direct_inject | yes | native_runtime_fragment_records_idle_history_once_and_retains_wake, v1, v1_closed, v1_completed, v1_error |
| v1_drop_midturn | yes | v1 |
| v1_drop_without_wait | yes | native_runtime_fragment_records_idle_history_once_and_retains_wake, spawn_child_completion_notifies_parent_history, subagent_notification_is_included_without_wait, v1_without_wait |
| v1_duplicate_fragment | yes | native_runtime_fragment_records_idle_history_once_and_retains_wake, v1, v1_closed, v1_completed, v1_error |
| v1_fabricated_path | yes | v1_closed, v1_completed, v1_error, v1_interrupted, v1_registered_wait |
| v1_idle_fragment_reappended | yes | native_runtime_fragment_records_idle_history_once_and_retains_wake, v1_without_wait |
| v1_interrupt_without_goal | yes | v1_unregistered |
| v1_ordinary_wake | yes | forked_subagent_replays_parent_applied_global_instructions, fresh_subagent_uses_parent_applied_instructions_without_parent_history, legacy, native_runtime_fragment_records_idle_history_once_and_retains_wake, paginated |
| v1_unbounded_error | yes | error_escaped, error_unicode |
| v2_result_wakes_ordinary | yes | after_final, bounded_retained_root_messages, disabling_fast_mode_updates_active_and_idle_child_work, enabling_fast_mode_updates_active_and_idle_child_work, evicted_role_subagent_uses_root_service_tier_after_reload |

History: precheck 1 (run 38501625154) had the no-wait delivery regression; precheck 2 (run 38680607848) failed lint on an iterator/slice compile error (fixed by the orchestrator, test-only); precheck 3 (run 38681700613) had 5 red core tests: a stamped-history assertion, a wiremock capture-order trap in the new HTTP tests, and the P4a paused-time scheduled check-in test (flaky 2/3 on G1, 3/3 on precheck 3). The precheck-4 rework (RUN-261015-736287) changed tests only: production files are byte-identical to precheck 3. The P4a test now waits on the actual deadline registration and the sink warning, with timeouts.
