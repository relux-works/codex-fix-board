# TASK-260929-csnn3a (D2): CR revision 2. Close the lost-wake hole after reserved-start back-off

Review round 1 (`TASK-260929-csnn3a_review-verdict-rev1.md`, outcome) is **changes_requested**, with one finding,
R141-A-1 (row "F1a cleared reservation"): tasks/mod.rs ~:629-630 returns taken-but-unattached leases after back-off, but
schedules no wake. If the replacement task already finished, and its scheduler pass skipped the entry while it was still
leased, the fail-back leaves the session idle with an unleased pending receipt and no future scheduler pass. That is a lost
completion. The other two rows (F1b; compaction, guardian and transport) held.

Do this:
1. After a back-off returns leases unleased, guarantee a subsequent scheduler pass, for example by re-invoking
   maybe_start_turn_for_pending_work (or the equivalent idle-wake path) once the leases are returned. It must not
   double-wake when the replacement turn is still live and will pick the entries up itself, and must not spin.
2. Add the public-entry test the panel requested, `exec_completion_lost_reservation_after_winner_idle_rewakes`
   (latches, no sleeps): a reserved start loses to a winner turn that finishes and goes idle while the entry is still
   leased; after the back-off the receipt is sampled exactly once. Add a narrowing mutant that removes the post-back-off
   wake, and confirm that test kills it. Keep the reserved_claim_* tests and mutants.
3. Update the results and mutants files (re-attach both). Leave the candidate UNCOMMITTED and add the note
   "HOSTED-PRECHECK-REQUESTED: precheck 3". Do NOT hand off.
LOCAL VERIFICATION ALLOWED (one targeted run, same gates): df >= 50 GiB, CPU idle >= 25%, `memory_pressure | tail -1` free
>= 30% (abort under 30% during the build). Run ONLY `cd codex-rs && RUST_MIN_STACK=33554432 cargo nextest run -p codex-core
--test all -E 'test(exec_completion)'`, then trim codex-target. Record disk before and after, CPU and memory. Nothing in
parallel. Follow R176 and R174.

R205 (tb-arbiter): no load generators. If a stress repro is truly needed, use at most 4 attached busy workers and name them in the results. None are expected for this task; the test uses latches, not load.
