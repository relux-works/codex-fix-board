# TASK-260929-csyzcj hosted precheck 8

CI ivanopcode/codex, slim relux-ci run 38017711768: snapshot wip-8 6b718428 = worktree tree 78b49cd71e2ccfc855069cc05f99ec294e383e85 (base 39c264c). Lanes: {'lint': 'success', 'app-server': 'success', 'small': 'success', 'core': 'success'}. All green; codex-core 5085/5085 with no flaky tests (goal_wait_latch_closes_completion_before_registration passed on try 1).

Rebased-equivalent tree after the Story refresh onto trunk 07c018be: 9d9354c0a3be138d539cbbf90eba1075f24ebf66 (= green + exactly the CI-only trunk delta), recorded green.

Mutants: 7 total, 7 killed, 0 survivors.

| mutant | failing lanes | killing tests |
|---|---|---|
| ignore_native_pending | small,core | empty_exec_with_native_pending_waits_and_uses_checkins, native_pending_exhausts_checkins_then_waits_without_deadline, goal_wait_preserves_foreign_sleep_across_register_and_turn_start, goal_wait_registered_parent_gets_single_interrupted_notice, goal_wait_registers_marker_and_wakes_on_child_completion |
| insert_after_mail_check | core | goal_wait_latch_closes_completion_before_registration |
| insert_clobbers_one_foreign | small,core | register_never_clobbers_foreign_sleep, goal_wait_preserves_foreign_sleep_across_register_and_turn_start |
| interrupted_claims_success | core | goal_wait_registered_parent_gets_single_interrupted_notice, interrupted_fragment_renders_exact_notice_body, interrupted_notice_is_queue_only_without_claiming_success |
| interrupted_notice_delivered_twice | core | goal_wait_registered_parent_gets_single_interrupted_notice |
| skip_failed_lookups | core | owned_children_inspection_propagates_failed_lookups |
| unconditional_remove | small,core | conditional_remove_only_removes_owned_id, goal_wait_preserves_foreign_sleep_across_register_and_turn_start |
