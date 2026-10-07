# TASK-260929-2snjbb (E2): CR revision 2. Fixed check-in epoch, and a real scheduled re-entry

Review round 1 (`TASK-260929-2snjbb_review-verdict-rev1.md`, outcome) is **changes_requested**. BOTH panels independently report two
defects (row "check-in tickets and warning"). The other rows (gate scope and fairness; admission recheck and invalidation) held.

1. Epoch reset: background_wait.rs ~:372-378 clears `wait_started_at` on every `note_turn_start` (production hook
   extension.rs ~:246, including the admitted check-in turn) but keeps `check_ins_used`. evaluate_continuation ~:273-279
   then adds the next absolute offset to a NEW epoch, so deadlines drift to 30/90/210 minutes instead of 30/60/120.
   Fix: the check-in epoch is anchored at the last HUMAN input (where the allowance renews). Check-in and other admitted
   automatic turns must not move it; human input, goal mutation, clear, stop and release reset epoch and count together.
   Test `check_ins_keep_epoch_across_admitted_turns` calls note_turn_start for each admitted check-in turn in between and
   asserts 30/60/120 from the original epoch. Add a mutant that resets the epoch on turn start.
2. Deadline discarded: runtime.rs ~:608-624 destructures `next_check_in`, logs it, drops the permit and returns. Nothing is
   scheduled, so a stalled Armed subscription with no further events never reaches a check-in or the warning.
   Fix: add the goal-owned scheduler foundation in stage 2d. Register a cancellable timer or ticket for the deadline that
   re-enters goal continuation through the normal idle/continuation path when it fires. It is cancelled or replaced by
   every invalidation (steering, turn start, goal mutation, clear, stop, release, resume) and by a newer deadline. It must
   not hold the goal semaphore while waiting, and must use injectable time so tests are deterministic. Activation stays
   off by default (stage 2e), but when the policy is enabled the timer must actually fire.
   Test `stalled_subscription_fires_scheduled_checkins` (fake time, no manual evaluate_continuation calls): with an unchanged
   Armed receipt, advancing time alone triggers the 30, 60 and 120 minute check-ins and then the single warning. Add a mutant
   that drops the registration (log-only), killed by that test.
Keep all existing E2 tests green. Update the results and mutants files (generate patches with `git diff` so they apply as
written; re-attach both). Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 3". Do NOT hand
off. local-build-allowance.md applies under all its gates (narrow filters: ext goal background_wait tests and core goal_background_wait).
Follow R176 and R174.
