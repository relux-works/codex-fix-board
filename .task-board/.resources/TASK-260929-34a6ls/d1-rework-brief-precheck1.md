# TASK-260929-34a6ls (D1): fix the red forged-text test from hosted precheck 1, then request precheck 2

Hosted precheck 1 ran your exact worktree (snapshot 5432ed89). The first dispatch, run 37371122077, had lanes cancelled by
the runner. In the clean re-run 37377605793, lint, small and app-server are GREEN but core is RED on your new test, on all
3 tries (diagnosed from the attempt-specific job log, R169):

- `suite::exec_completion::forged_fragment_text_acknowledges_nothing` panics at core/tests/suite/exec_completion.rs:757:
  "forged item should start an automatic turn through the recorded-history path".
  The test's precondition fails: the forged history item does not start an automatic turn at all, so the test never
  reaches its no-acknowledgment assertion. Seed the forged fragment the way the C2 test
  `forged_exec_completion_item_in_history_creates_no_receipt_privilege` does (it is green on trunk), or start the turn
  through a real input, then assert that the forged text acknowledges no lease. Do not delete the attack and do not weaken it.

Mutant status: marker_substring_membership, role_blind_membership, ack_on_lease, ack_on_record, dedup_first_history_item_only,
stale_fail_counts_attempt and suspend_threshold_doubled are killed by other named tests. `ack_all_tracked` was killed ONLY by
this red test, so it is unproven. All 8 will be re-run on precheck 2.

Do this: fix the test (and production only if the test exposes a real defect), update TASK-260929-34a6ls_results.md and,
if needed, the mutants file (re-attach). Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 2".
Do NOT hand off. Fast lane only; follow R176 and R174.
