# Coverage map — TASK-260929-2snjbb goal-background-wait-policy (CR rev 5 handoff on hosted precheck 7)

Filled from `references/coverage-map-template.md` against the brief's
surface table (`surface-table.md`, 3 rows). Round-4 verdict held gate scope
and fairness and check-in tickets and warning, and reported 1 mechanism
(`revision-comparison-not-serialized-with-publication` + its
`revision-recheck-before-await-window` repeat): the rev-4 compare-and-publish
holds `Session.state` while Arm uses only the store mutex, so a cross-thread
Arm can land between comparison and publication. Rework rev5 serializes the
final comparison and the publication under one shared lock set
(`active_turn` → `Session.state` → receipt-store → runtime-mailbox, no await
between), with a multi-thread race regression test and a narrowing mutant.
Hosted precheck 7 (run 37578543875, snapshot `f63366db`, tree
`13972f7d936f6280c9b0cae88749c6f5c1a56a9a`) observed the base green on all
four lanes plus all 16 kills below, 0 survivors.

| Surface row | Attacking tests | Narrowing mutants (16/16 killed on precheck 7) | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| gate scope and fairness | `goal_background_wait_blocks_goal_but_admits_user_and_followup`, `goal_background_wait_ignores_non_goal_triggers` (core `start_if_idle`/`handle`); `goal_background_wait_treats_read_failure_as_wait` (core); `read_failure_never_treated_as_empty` (+ keeps-armed assertion), `disabled_policy_never_gates`, `inactive_or_budget_limited_status_never_gates` (+ registration-cleared assertions), `check_ins_fire_at_30_60_120_minutes_fake_time` (goal `evaluate_continuation`/`check_admission`) | `overgate_non_goal_triggers` (37578682087) → both core fairness tests fail; `treat_read_error_as_empty` (37578790835) → `read_failure_never_treated_as_empty` fails; `gate_only_queued_ignoring_armed` (37578629753) → cap/firing/epoch tests fail | none claimed |
| check-in tickets and warning | `check_ins_fire_at_30_60_120_minutes_fake_time`, `at_most_three_check_ins_per_human_input`, `ticket_bypasses_work_gate_exactly_once`, `ticket_bypass_still_enforces_revision_and_generation`, `warning_emitted_once_after_third_check_in_with_exact_text`, `completion_after_cap_wakes_without_counting_as_human_input` (goal, fake `Duration`) + `check_ins_keep_epoch_across_admitted_turns` + `stalled_subscription_fires_scheduled_checkins` + `scheduled_checkins_fire_through_production_runtime_under_paused_time` (REAL session + goal extension, paused tokio time, production CheckInTimer → GoalRuntimeHandle → Core re-entry, turns marked automatic, production warning once) + `fired_timer_continuation_survives_turn_start_invalidation` + `stale_install_never_replaces_newer_generation_timer` | `reuse_ticket_id` (37578737666); `warning_repeats` (37578825692); `reset_epoch_on_turn_start` (37578719469); `drop_check_in_registration` (37578596335); `drop_timer_spawn` (37578612871); `keep_handle_in_slot_while_firing` (37578646983); `unconditional_slot_replace` (37578808296); `break_runtime_wait_arm_reentry` (37578579179) | none claimed |
| admission recheck and invalidation | `revision_change_between_check_and_start_rejects`, `ticket_bypass_still_enforces_revision_and_generation` (goal); `goal_background_wait_revision_recheck_catches_transition`, `goal_background_wait_allows_when_empty_and_after_release` (core) + `receipt_armed_after_admission_blocks_automatic_start` + `receipt_armed_inside_start_task_blocks_automatic_start` (residual window) + `arm_after_publication_allows_turn_and_keeps_receipt_pending` (post-publish control) + `late_goal_rejection_leaves_thread_settings_unchanged` + `goal_publish_serialized_with_concurrent_arm` (multi-thread: real Arm on a blocking thread forced into the compare→publish window; publication must win the shared sequence, turn Started, receipt stays pending) + `goal_publish_rejects_safe_when_store_contended` + `goal_publish_rejects_safe_when_mailbox_contended` (fail-safe + inversion guards: inner contention rejects safe within 5 s, never deadlocks, never treated as empty); `turn_start_and_steering_invalidate_without_renewing`, `clear_stop_and_resume_reset_transient_wait_state`, `release_invalidates_ticket_and_reassessment_can_proceed`, `evaluations_are_synchronous_and_reentrant_without_holding_state` (goal) + `invalidation_cancels_armed_check_in` | `skip_revision_recheck` (37578755970); `preserve_ticket_across_invalidation` (37578700699); `move_final_check_before_awaits` (37578665024, killed by the race test + residual + settings tests); `apply_goal_settings_before_final_check` (37578561576); `skip_transition_locks_in_publish` (37578773989: race order assertion + both contention tests fail) | none claimed |

3 of 3 surface rows covered; every row has at least one narrowing mutant
killed (16 total, 0 delete-only, 0 survivors on precheck 7). No inputs
refused as out of contract — all 10 AC rows are driven (see
`TASK-260929-2snjbb_results.md` for the per-AC map).
AC-to-row trace: AC1–AC3 → row 1; AC4–AC6 → row 2; AC7–AC10 → row 3.

Linearization-point rule (rev5): the admitted revision is compared and
`last_started_turn_id` is written inside `start_task` while holding
`active_turn` + `Session.state` + receipt-store + runtime-mailbox, with no
await between comparison and write; that publication is the linearization
point (Arm ordered before → observed and rejects effect-free; Arm ordered
after → legitimate post-start work). Contention on the inner locks rejects
safe (never empty, never blocks).
