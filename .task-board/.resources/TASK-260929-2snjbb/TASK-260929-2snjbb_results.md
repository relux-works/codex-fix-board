# TASK-260929-2snjbb: goal-background-wait-policy — results (CR rev 5 handoff on hosted precheck 7)

## This run (handoff-prep per `e2-handoff-note-7.md` — zero code changes)

Hosted precheck 7 (`TASK-260929-2snjbb_hosted-precheck-7.md`) ran the exact
worktree tree `13972f7d936f6280c9b0cae88749c6f5c1a56a9a` (snapshot `f63366db`,
run 37578543875): all four lanes green (small, lint, core, app-server), and all
16 narrowing mutants killed, 0 survivors — including the rev5 regression pair
`skip_transition_locks_in_publish` (run 37578773989) and
`move_final_check_before_awaits` (run 37578665024, killed by
`goal_publish_serialized_with_concurrent_arm`).

This run changed zero files: temp-index tree re-confirmed as
`13972f7d936f6280c9b0cae88749c6f5c1a56a9a` (exit 0), HEAD `e26d2214a1` (sibling
E1 checkpoint), candidate left UNCOMMITTED (22 modified + 6 new paths, same set
as the precheck-7 snapshot). Checklist holds at 17/17 on precheck-7 evidence
(item 8 N/A: typed-snapshot gate, no source-text token). Busy check FREE;
handing off CR rev 5 as the Story final leaf.

## Summary (E2 behavior)

Goal-owned background waiting policy, inactive by default (stage 2e owns
activation). Gates ONLY automatic goal continuation on known pending
exec-completion work (E1 snapshot); user/follow-up input, inter-agent and
trigger mail stay immediately admissible and trigger-mail priority stays
authoritative. Failed snapshot reads wait safely (never treated as empty).
Check-in timers at absolute 30/60/120 minutes from the human-input-anchored
epoch fire through the production timer/runtime/Core path; at most 3 per
human input, each ticket bypassing only the work gate exactly once (no
status/Plan/shutdown/capacity/input/newer-turn bypass). After the third, the
exact warning fires once; the goal stays active and event-wakeable. Tickets
invalidate on steering, turn start, goal mutation, clear, stop, release;
resume discards stale waits. A rejected automatic goal start leaves no
observable effect (no settings commit, no notification, no ownerless
reservation). No semaphore held across delay; fake/paused time, no real sleeps.

Rev5 linearization-point rule (stated): the admitted work revision is
compared and `last_started_turn_id` is written inside `start_task` while
holding `active_turn` + `Session.state` + receipt-store + runtime-mailbox,
with NO await between comparison and write
(`Session::publish_goal_turn_if_revision_matches` in
`core/src/session/goal_admission.rs`, documented in code). That publication
is the linearization point: an Arm totally ordered before it is observed
(its revision bump is visible under the held locks) and the automatic goal
start is rejected effect-free (`NotSubmitted` with `GoalBackgroundWait`); an
Arm ordered after it is, by definition, work arriving after the turn
started, which is legitimate (turn runs, receipt delivered later). Earlier
comparisons are fast-path rejections only.

## Lock order and contention behaviour (reject-safe)

Order: `active_turn` (tokio, outermost, held by the `start_task` caller) →
`Session.state` (tokio) → receipt-store `state` (std) →
runtime mailbox (tokio `try_lock`, innermost). Documented at
`try_with_locked_state`, `try_lock_runtime_for_admission`, and
`publish_goal_turn_if_revision_matches`. Every revision-bumping transition
(store reserve/arm/publish/lease/fail/acknowledge/cancel; mailbox
enqueue/lease/acknowledge/fail/suspend/cancel) needs the store or mailbox
lock, so Arm and publication are totally ordered.

Contention/poisoning rejects safe, never treated as empty: inner locks are
`try_lock` (never block), so a would-be inversion fails safe (reject) instead
of deadlocking, and no `.await` runs while the std guard is held. Proven by
`goal_publish_rejects_safe_when_store_contended` and
`goal_publish_rejects_safe_when_mailbox_contended`: each holds one inner lock
and requires publication to reject (not deadlock) within 5 s; a blocking inner
lock would trip the timeout. Both tests also kill
`skip_transition_locks_in_publish` (run 37578773989), which drops the
transition locks and therefore loses the fail-safe. Full lock audit (store/
mailbox/hooks are leaves, no inversion path) is in the rev5 rework results
superseded by this handoff note; the code and its lock-order comments are
unchanged since.

## Changed files (candidate vs E1 checkpoint `e26d2214a1`)

Modified (22):

- `codex-rs/app-server/src/request_processors/turn_processor.rs` (rev3)
- `codex-rs/core/src/codex_thread.rs` (rev5: +`TestGoalPublishGate` sync gate)
- `codex-rs/core/src/lib.rs` (rev4: export gate)
- `codex-rs/core/src/session/input_queue.rs` (rev5: +`try_lock_runtime_for_admission`)
- `codex-rs/core/src/session/mod.rs` (rev4: `goal_admission` now `pub(crate)`)
- `codex-rs/core/src/session/tests.rs` (rev3)
- `codex-rs/core/src/session/tests/guardian_tests.rs` (rev4: mechanical only)
- `codex-rs/core/src/session/turn_input.rs` (rev4)
- `codex-rs/core/src/session/turn_input_tests.rs` (rev5: +3 tests)
- `codex-rs/core/src/tasks/mod.rs` (rev5: comment now names store+mailbox locks)
- `codex-rs/core/src/tasks/mod_tests.rs` (rev4: mechanical only)
- `codex-rs/core/src/tools/network_approval_tests.rs` (rev4: mechanical only)
- `codex-rs/core/src/unified_exec/completion_receipt.rs` (rev5: +`try_with_locked_state`)
- `codex-rs/core/tests/suite/mod.rs` (rev4: registration)
- `codex-rs/ext/extension-api/src/lib.rs` (rev3)
- `codex-rs/ext/goal/Cargo.toml` (rev3)
- `codex-rs/ext/goal/src/events.rs` (rev3)
- `codex-rs/ext/goal/src/extension.rs` (rev4)
- `codex-rs/ext/goal/src/lib.rs` (rev4)
- `codex-rs/ext/goal/src/runtime.rs` (rev4)
- `codex-rs/ext/goal/src/tool.rs` (rev3)
- `codex-rs/protocol/src/turn_input.rs` (rev3)

New (6):

- `codex-rs/core/src/session/goal_admission.rs` (rev5: serialized publish)
- `codex-rs/core/tests/suite/goal_background_wait.rs` (rev4)
- `codex-rs/ext/extension-api/src/goal_background_wait.rs` (rev3)
- `codex-rs/ext/goal/src/background_wait.rs` (rev3)
- `codex-rs/ext/goal/src/check_in_clock.rs` (rev3)
- `codex-rs/ext/goal/tests/background_wait.rs` (rev3)

Rework diff bounded: rev5 touched only the E2 admission/publication path.
No D/E1 logic, no goal-extension, no check-in/scheduler behavior touched. No
`Cargo.lock`/`MODULE.bazel.lock`/schema changes.

## AC coverage map — 10 of 10 AC rows driven

Production call sites: goal continuation = `GoalRuntimeHandle::continue_if_idle`
via `BackgroundWaitState::evaluate_continuation`; admission = `start_if_idle`
via `goal_admission::check_goal_admission` → fast-path
`recheck_goal_admission_before_start` → authoritative serialized
`publish_goal_turn_if_revision_matches` inside `start_task`; scheduled
re-entry = runtime Wait arm → `CheckInTimer` → re-entry.

| AC | Driving test(s) (production entry) | Refusal / negative test |
|----|-------------------------------------|--------------------------|
| AC1 queue fairness | `goal_background_wait_blocks_goal_but_admits_user_and_followup`, `goal_background_wait_ignores_non_goal_triggers` (core, `handle`/`StartIfIdle`) | `overgate_non_goal_triggers` (precheck-7 kill 37578682087) |
| AC2 read failure never empty | `read_failure_never_treated_as_empty`; `goal_background_wait_treats_read_failure_as_wait` | `treat_read_error_as_empty` (37578790835) |
| AC3 inactive/budget-limited/unopted/server-only | `disabled_policy_never_gates`, `inactive_or_budget_limited_status_never_gates`, `empty_snapshot_proceeds_and_admission_allows_same_revision` | No registration; inactivity tests also kill `drop_check_in_registration` (37578596335) |
| AC4 check-ins 30/60/120, max 3, ticket single-use; production-runtime firing | firing/cap/ticket/epoch/stalled/suite/fired-survives/stale-rejected tests (see coverage map) | 8 mutants incl. `reuse_ticket_id` (37578737666), `reset_epoch_on_turn_start` (37578719469), `break_runtime_wait_arm_reentry` (37578579179) |
| AC5 exact warning once after third; goal stays active/wakeable | `warning_emitted_once_after_third_check_in_with_exact_text`, `completion_after_cap_wakes_without_counting_as_human_input`, stalled + suite tails | `warning_repeats` (37578825692) |
| AC6 completion after cap wakes, not human input | `completion_after_cap_wakes_without_counting_as_human_input` | Used-count/warning preserved; registration cleared |
| AC7 gate-to-start race incl. residual window AND cross-thread publish window | `revision_change_between_check_and_start_rejects`; `goal_background_wait_revision_recheck_catches_transition`; `receipt_armed_after_admission_blocks_automatic_start`; `receipt_armed_inside_start_task_blocks_automatic_start`; `arm_after_publication_allows_turn_and_keeps_receipt_pending`; `goal_publish_serialized_with_concurrent_arm` (multi-thread Arm forced into the compare→publish window; publication must win the shared sequence) | `skip_revision_recheck` (37578755970) + `move_final_check_before_awaits` (37578665024) + `skip_transition_locks_in_publish` (37578773989: race order assertion + both contention tests) |
| AC8 release allows paced continuation without kill | `release_invalidates_ticket_and_reassessment_can_proceed`; `goal_background_wait_allows_when_empty_and_after_release` | Release resets epoch+allowance; reassessment proceeds |
| AC9 invalidation; resume discards | `turn_start_and_steering_invalidate_without_renewing`, `clear_stop_and_resume_reset_transient_wait_state`, `invalidation_cancels_armed_check_in` | `preserve_ticket_across_invalidation` (37578700699) |
| AC10 semaphore never held across delay | `evaluations_are_synchronous_and_reentrant_without_holding_state`; permit only across sync spawn; linearization helper holds only brief non-await locks | Code path: no `.await` between compare and write; inner locks are `try_lock` |

No rows treated as out of contract. All rev2/rev3/rev4 regression tests kept
under original names; base green observed on hosted precheck 7 (run
37578543875, snapshot `f63366db`).

## Surface-table coverage map — 3 of 3 rows

| Surface row | Attacking tests | Narrowing mutants (16/16 killed on precheck 7, 0 survivors) | Out-of-contract |
|---|---|---|---|
| gate scope and fairness | core fairness tests, read-failure tests, inactive/disabled tests | `overgate_non_goal_triggers` (37578682087), `treat_read_error_as_empty` (37578790835), `gate_only_queued_ignoring_armed` (37578629753) | none claimed |
| check-in tickets and warning | firing/cap/ticket/warning/completion/epoch/stalled tests + real-runtime suite test + fired-survives + stale-rejected | `reuse_ticket_id` (37578737666), `warning_repeats` (37578825692), `reset_epoch_on_turn_start` (37578719469), `drop_check_in_registration` (37578596335), `drop_timer_spawn` (37578612871), `keep_handle_in_slot_while_firing` (37578646983), `unconditional_slot_replace` (37578808296), `break_runtime_wait_arm_reentry` (37578579179) | none claimed |
| admission recheck and invalidation | revision tests (goal+core), preparation-window test, residual/post-publish/settings tests, invalidation tests + armed-cancel + serialized-publish race test + 2 contention fail-safe tests | `skip_revision_recheck` (37578755970), `preserve_ticket_across_invalidation` (37578700699), `move_final_check_before_awaits` (37578665024), `apply_goal_settings_before_final_check` (37578561576), `skip_transition_locks_in_publish` (37578773989) | none claimed |

No delete-only mutants: every mutant preserves the gate and weakens exactly
one behavior (the rev5 mutant keeps the gate window and drops only the
transition locks). Full per-row map also in
`TASK-260929-2snjbb_coverage-map.md` (refreshed with precheck-7 run ids).

## Mutant table (16 total; ALL KILLED on hosted precheck 7, 0 survivors)

| Mutant | What it narrows the gate to | Named killing test(s) (precheck-7 run) |
|---|---|---|
| `apply_goal_settings_before_final_check` | Gated goal path commits the supplied delta | `late_goal_rejection_leaves_thread_settings_unchanged` (37578561576, core) |
| `break_runtime_wait_arm_reentry` | Runtime Wait arm never spawns the timer | `scheduled_checkins_fire_through_production_runtime_under_paused_time` (37578579179, lint+core) |
| `drop_check_in_registration` | Wait evaluations never arm a deadline | `check_ins_keep_epoch_across_admitted_turns`, `disabled_policy_never_gates`, `inactive_or_budget_limited_status_never_gates` (37578596335, small+core) |
| `drop_timer_spawn` | `CheckInTimer::spawn` never schedules | `fired_timer_continuation_survives_turn_start_invalidation`, `stale_install_never_replaces_newer_generation_timer`, `scheduled_checkins_fire_through_production_runtime_under_paused_time` (37578612871, lint+small+core) |
| `gate_only_queued_ignoring_armed` | Gate consults Queued/Leased only, Armed looks empty | `at_most_three_check_ins_per_human_input`, `check_ins_fire_at_30_60_120_minutes_fake_time`, `check_ins_keep_epoch_across_admitted_turns` (37578629753, small+core) |
| `keep_handle_in_slot_while_firing` | Fired timer stays cancellable | `fired_timer_continuation_survives_turn_start_invalidation`, `scheduled_checkins_fire_through_production_runtime_under_paused_time` (37578646983, lint+small+core) |
| `move_final_check_before_awaits` | Linearization check runs before `start_task` awaits | `goal_publish_serialized_with_concurrent_arm`, `late_goal_rejection_leaves_thread_settings_unchanged`, `receipt_armed_inside_start_task_blocks_automatic_start` (37578665024, core) |
| `overgate_non_goal_triggers` | Gate consults non-goal automatic triggers too | `goal_background_wait_blocks_goal_but_admits_user_and_followup`, `goal_background_wait_ignores_non_goal_triggers` (37578682087, lint+core) |
| `preserve_ticket_across_invalidation` | Invalidation keeps the outstanding ticket | `release_invalidates_ticket_and_reassessment_can_proceed`, `turn_start_and_steering_invalidate_without_renewing` (37578700699, small) |
| `reset_epoch_on_turn_start` | Turn start clears the epoch | `check_ins_keep_epoch_across_admitted_turns`, `scheduled_checkins_fire_through_production_runtime_under_paused_time` (+ collateral `encrypted_parent_reply_survives_incremental_guardian_reviews`) (37578719469, core+small) |
| `reuse_ticket_id` | Ticket ids never increment (replayable) | `at_most_three_check_ins_per_human_input`, `check_ins_fire_at_30_60_120_minutes_fake_time`, `check_ins_keep_epoch_across_admitted_turns` (37578737666, small+core) |
| `skip_revision_recheck` | Admission ignores revision | `revision_change_between_check_and_start_rejects`, `ticket_bypass_still_enforces_revision_and_generation` (37578755970, small) |
| `skip_transition_locks_in_publish` | Compare+publish hold Session.state only; a racing Arm completes inside the window and publication writes stale (gate window kept) | `goal_publish_serialized_with_concurrent_arm` + `goal_publish_rejects_safe_when_store_contended` + `goal_publish_rejects_safe_when_mailbox_contended` (37578773989, core+lint) |
| `treat_read_error_as_empty` | Read failure yields empty snapshot instead of waiting | `read_failure_never_treated_as_empty` (37578790835, small) |
| `unconditional_slot_replace` | Stale installs clobber the live timer | `stale_install_never_replaces_newer_generation_timer`, `scheduled_checkins_fire_through_production_runtime_under_paused_time` (37578808296, lint+small+core) |
| `warning_repeats` | Warning flag never latches | `scheduled_checkins_fire_through_production_runtime_under_paused_time`, `completion_after_cap_wakes_without_counting_as_human_input`, `stalled_subscription_fires_scheduled_checkins` (37578825692, core+small) |

Note: `reset_epoch_on_turn_start` was additionally killed by
`encrypted_parent_reply_survives_incremental_guardian_reviews` (unrelated
guardian test, collateral kill); the intended epoch tests killed it as well,
so the mutant is covered by its named regression tests regardless.

## Commands with real exit codes (this handoff run)

- `task-board m 'set_status(TASK-260929-2snjbb, status=development)'` → exit 0.
- Temp-index tree (`git read-tree HEAD` + `git add -A` + `git write-tree`) →
  `13972f7d936f6280c9b0cae88749c6f5c1a56a9a`, exit 0; equals the precheck-7
  tree. Zero files changed this run.
- Busy check `python3 .../codex-fix-suite-busy.py --any` → `FREE`, exit 0.
- No cargo/just commands this run: handoff-prep only; all build/test evidence
  is reused from hosted precheck 7 on the identical tree (base run 37578543875
  + 16 mutant runs above), per the reuse rule for an unchanged source/test/
  configuration/environment identity.

## Handoff note

Handing off CR rev 5 (story_final) on hosted precheck 7: base 4 lanes green,
16/16 narrowing mutants killed, 0 survivors. Results + coverage map refreshed
with observed precheck-7 run ids and the stated lock order / reject-safe
contention rule. Candidate UNCOMMITTED on HEAD `e26d2214a1`.
