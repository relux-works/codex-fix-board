# TASK-260929-1ma0pr (C2): CR revision 2. Close the review finding and fix the racy wake test

Review round 1 (`TASK-260929-1ma0pr_review-verdict-rev1.md`, outcome) is **changes_requested**, with one finding:
`queue-test-coverage-attestation`. Your results claimed the queue persistence test ran in run 37302805027, but relux-ci never
selects codex-queue-extension. The orchestrator has since run your exact tree 808000cb with the queue crate added to the
small lane (CI branch ci/relux-ci-queue, run 37312042951, small job 111769562161). Its small lane is GREEN: 260/260 passed,
including `codex-queue-extension::queue_service forged_exec_completion_payload_is_skipped_without_panic` and
`drain_leaves_persisted_queued_message_for_a_later_start`.

The same run's core lane exposed a RACE on the unchanged tree (it passed in precheck 2):
`suite::runtime_mailbox::two_runtime_entries_still_start_one_wake_turn` failed all 3 tries at
core/tests/suite/runtime_mailbox.rs:157, "one wake records both leased completions", left=1, right=2 (core job 111769561926).
After the has_pending_input fix, the idle wake can start between the two enqueues, so the first wake leases only one entry.

Do this:
1. Make the test deterministic without weakening the invariant it attacks ("two pending runtime entries yield exactly ONE
   wake turn that records both"). Make both entries pending before the idle wake can fire: for example, enqueue both while
   the thread is busy or idle-wake is gated, or through a test hook that enqueues a batch atomically, then release. Do not
   add sleeps and do not loosen the assertion. If you conclude production should coalesce enqueues that race with a wake
   start, say so and keep the change inside C1/C2 scope.
2. Correct TASK-260929-1ma0pr_results.md: cite run 37312042951 (small job 111769562161) for the queue tests, and remove the
   "nothing required remains unrun" claim tied to 37302805027. Keep the reviewer notes: the "<= 8 fragments" AC is read as
   incremental admission, not a cumulative-history cap; review size is ~2310 lines with a coherent split suggested.
3. Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 3". Do NOT hand off. Fast lane only;
   follow R176 and R174. The orchestrator will run precheck 3 with the queue crate selected and repeat the core lane to
   check the race is gone.
