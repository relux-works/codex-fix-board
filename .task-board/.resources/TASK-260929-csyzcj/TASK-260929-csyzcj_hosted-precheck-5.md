# TASK-260929-csyzcj hosted precheck 5

Worktree tree: e8eef4f44743b4a6d256e610f91527e715ae042b. Snapshot commit fdaacee7 (ci/TASK-260929-csyzcj/wip-5, signed by Ivan Oparin, parent 39c264c3), run 37855177143: lanes {'core': 'success', 'app-server': 'success', 'lint': 'success', 'small': 'success'}. All green.

The candidate equals the producer's precheck-4 tree plus the orchestrator's whitespace-only rustfmt edit (see g1-orch-fmt-edit.md). Precheck 4 (run 37850633304) was green on small, core and app-server; there, lint failed on fmt-check only.

Mutants: 6 total, 6 killed, 0 survivors (killing tests = tests failing on all 3 tries).

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| ignore_native_pending | 37855194303 | core,small | goal_wait_preserves_foreign_sleep_across_register_and_turn_start, goal_wait_registers_marker_and_wakes_on_child_completion, empty_exec_with_native_pending_waits_and_uses_checkins, native_pending_exhausts_checkins_then_waits_without_deadline |
| insert_after_mail_check | 37855212822 | core | goal_wait_latch_closes_completion_before_registration |
| insert_clobbers_one_foreign | 37855230691 | small,core | register_never_clobbers_foreign_sleep, goal_wait_preserves_foreign_sleep_across_register_and_turn_start |
| interrupted_claims_success | 37855247950 | core | interrupted_notice_is_queue_only_without_claiming_success |
| skip_failed_lookups | 37855265071 | core | owned_children_inspection_propagates_failed_lookups |
| unconditional_remove | 37855282786 | small,core | conditional_remove_only_removes_owned_id, goal_wait_preserves_foreign_sleep_across_register_and_turn_start |
