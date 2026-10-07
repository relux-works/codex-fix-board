# TASK-260929-2snjbb (E2): CR revision 3. Make the check-in scheduler ownership-safe, and close the recheck window

Review round 2 (`TASK-260929-2snjbb_review-verdict-rev2.md`, outcome) is **changes_requested**: 5 findings, all in the
scheduler added in rev 2 and the admission recheck. Gate scope and fairness held. Three root causes:

A. A fired timer cancels its own continuation (findings timer-aborts-own-admission, fired-timer-aborted-before-admission-reply).
   check_in_clock.rs ~:84-89 keeps the fired task's JoinHandle in the cancellable slot while `on_fire().await` runs, and
   runtime.rs ~:574-582 runs continue_if_idle inside that task. The BeforeTaskRegistration on_turn_start hook
   (extension.rs ~:248 -> background_wait.rs ~:193-204 -> check_in_clock.rs ~:48-52) aborts that slot. The result is an
   ownerless reservation, or a turn that is never marked automatic (accounting.rs ~:219-228).
   Fix: when the timer fires, atomically TAKE it out of the cancellable slot (identity-safe: compare the stored id or
   generation) BEFORE invoking the continuation. Invalidation aborts only a still-sleeping timer and never a fired one. The
   continuation runs detached from the slot (spawned or owned by the runtime), so mark_goal_continuation always runs.
B. A stale install clobbers the current timer (finding stale-timer-install-clobbers-current-registration).
   runtime.rs ~:656-659 drops the permit and then installs, and check_in_clock.rs ~:82-88 cancels the slot unconditionally.
   Fix: install the timer with a compare-and-set on the registration generation. Do it under the goal permit, or make the
   slot reject an install whose generation is older than the current one. A stale install must never cancel or replace a
   newer-generation timer.
C. Revision recheck before the await window (finding revision-recheck-before-await-window).
   turn_input.rs ~:459-464 is the only check. prepare, apply_started, context processing and start_task (~:469-530) are awaited
   after it, and receipt transitions use their own mutex and revision. Fix: carry the admitted revision and re-compare it
   immediately before the automatic goal turn is committed or started (the last point before start_task). On mismatch,
   abandon the automatic start cleanly: no ownerless reservation, ticket handling per AC4.
D. The regression test was a simulation (finding scheduled-checkin-regression-not-exercised). The rev-2 test calls the
   state machine by hand. Replace it with an ASYNC test using the real CheckInClock/CheckInTimer and GoalRuntimeHandle under
   paused tokio time (`tokio::time::pause` and `advance`): an unchanged Armed receipt with time advancing alone fires the
   check-ins through the real runtime re-entry, and the turns are marked automatic.
Tests (latches and paused time, no sleeps), each with a narrowing mutant that it kills:
 - fired_timer_continuation_survives_turn_start_invalidation (mutant: keep the handle in the slot while firing).
 - stale_install_never_replaces_newer_generation_timer (mutant: unconditional slot replace).
 - receipt_armed_after_admission_blocks_automatic_start (arm between the admission check and start_task via a latch in
   preparation; mutant: no late recheck).
 - scheduled_checkins_fire_via_runtime_under_paused_time (mutant: drop timer spawn or runtime re-entry).
Keep all existing E2 tests and D/E1 tests green. Generate mutant patches with `git diff`. Update and re-attach the results
and mutants files. Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 4". Do NOT hand off.
local-build-allowance.md applies under all its gates (narrow filters). Follow R176 and R174.
