# TASK-260929-3r7peh (F1): one surviving mutant on hosted precheck 2. Close it, then request precheck 3

Hosted precheck 2 (run in `f1-p2.ok`): the snapshot is GREEN on all four lanes, and 8 of 9 mutants are killed. The three earlier
suite failures are fixed. One survivor, with all lanes green:

- `m9_enqueue_skips_live_check` (receipt_hooks.rs ~:347): removes the first `is_live_queued_receipt` gate, including its
  `retention.drop(receipt_id)`. Your intended killer `enqueue_published_completion_skips_disarmed_receipt` did NOT fail. Your
  own note says the later recheck is kept, so the remaining observable difference is that a disarmed or released receipt's
  retained output is no longer dropped. That is an unbounded retention leak, not a duplicate enqueue.
Decide:
 (a) If the first gate is genuinely redundant, remove it, fold the retention drop into the single remaining check, and replace
     m9 with a mutant against that single check; or
 (b) keep both, and make the test assert the observable effect: after the helper runs on a released or disarmed receipt,
     its retained output is gone (read is rejected or empty, and the retention store no longer holds it), and no mailbox
     entry or wake exists. m9 must fail that test.
Either way, no retained output survives a disarm or release. Run the narrow lib filter locally under local-build-allowance.md.
Update the results and mutants files (re-attach). Leave the candidate UNCOMMITTED and add the note
"HOSTED-PRECHECK-REQUESTED: precheck 3". Do NOT hand off. Follow R176 and R174.
