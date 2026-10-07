# TASK-260929-36bvsc (E1): CR revision 2. Acknowledge the B receipt in production; drive the real path in tests

Review round 1 (`TASK-260929-36bvsc_review-verdict-rev1.md`, outcome) is **changes_requested**. BOTH panels independently report
the same defect (row "snapshot contents", severity bypass):

- Production acknowledgment (session/exec_completion_ack.rs ~:168-170) calls only InputQueue::acknowledge_runtime_lease
  (input_queue.rs ~:347). That removes the mailbox entry and bumps the revision, but NEVER acknowledges the B receipt:
  UnifiedExecProcessManager::acknowledge_pushed_completion has no production caller. CompletionReceiptStore keeps
  reporting the receipt as Queued.
- pending_work.rs ~:71-80 unions store Queued/Leased receipts that have no mailbox entry. So after real mailbox acceptance,
  the snapshot resurrects the sampled receipt as Queued forever. The E2 goal gate would then wait forever on finished work.
- pending_work_tests.rs ~:167-182 acknowledges both stores by hand, which masks this. Its comment claiming production
  acknowledges both is false.
The other rows (revision and atomicity; read failure and API boundary) held.

Do this:
1. Make the production acknowledgment path acknowledge the B receipt as well, atomically with (or in a defined order
   relative to) the mailbox acknowledgment, with one revision bump. After a real acceptance the receipt is in neither set.
   Keep D1's acknowledgment-at-acceptance semantics and its idempotence: a fail after acknowledgment is a no-op in both stores.
2. Replace the hand-acknowledging test with `production_acknowledgement_removes_pending_work`. It drives the REAL production
   acknowledgment entry point (the one exec_completion_ack.rs uses) and asserts the snapshot no longer reports the receipt.
   Remove or correct the false comment.
3. Narrowing mutant: production acknowledgment skips the B-store acknowledgment. The new test must kill it.
4. Check whether the snapshot's union of store Queued without a mailbox entry is still needed at all (Armed->Queued
   atomicity). If kept, document precisely when such a state is legitimately pending.
5. Run D1's exec_completion acceptance tests too: they must stay green.
Update the results and mutants files (re-attach both). Leave the candidate UNCOMMITTED and add the note
"HOSTED-PRECHECK-REQUESTED: precheck 3". Do NOT hand off. local-build-allowance.md applies under all its gates (narrow filters:
pending_work and exec_completion). Follow R176 and R174.
