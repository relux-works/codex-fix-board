# TASK-260929-2snjbb (E2): CR revision 5. Serialize the final comparison and publication under the receipt-store lock

Review round 4 (`TASK-260929-2snjbb_review-verdict-rev4.md`, outcome; tb-R209) is **changes_requested** on ONE remaining mechanism.
Gate scope and check-in tickets now HELD. Panel B accepted. Panel A and delta agree:
goal_admission.rs ~:131-137 compares the revision and writes last_started_turn_id while holding Session.state. But receipt Arm
(completion_receipt.rs ~:402-466) takes only CompletionReceiptStore.state and bumps the atomic revision; pending_work.rs ~:51-64
drops its guards before returning. "No await" stops cooperative yielding, NOT another OS thread: an Arm can land between the
comparison and the publication write. The rev-3 awaited-prefix defect IS fixed.

Required design: one serialization point shared by Arm and publication.
1. Make the final comparison and the publication happen while holding the SAME lock that every revision-bumping
   transition holds. Concretely: run the comparison and the publication write inside a closure executed under
   CompletionReceiptStore's state mutex (and the mailbox lock, if mailbox transitions also bump the shared revision). The
   alternative is to make the bump and the publication flag one atomic CAS on a shared word. Either way, Arm and publication
   are totally ordered: an Arm ordered before publication is observed and rejects; one ordered after is post-start (legit).
2. LOCK ORDER: you will now take the receipt-store lock while holding Session.state (and active_turn). Audit every path that
   takes the receipt-store or mailbox lock and prove none of them then acquires Session.state or active_turn (no inversion).
   Write the lock order as a comment at the definition, and add a debug assertion or a test that would catch an inversion.
   If an inversion exists that you cannot remove, stop and report it precisely instead of shipping.
3. Tests: a multi-thread (`flavor = "multi_thread"`) race test where an Arm on another worker thread is forced (latch or
   barrier inside the store-lock section) to hit the window between comparison and publication. With the fix it is either
   rejected or strictly after publication, never accepted-then-published-stale. Narrowing mutant: do the comparison under
   Session.state only (the rev-4 shape). Keep `receipt_armed_inside_start_task_blocks_automatic_start` and all other E2/E1/D tests.
4. No other changes. Gate scope and check-in behavior held, so do not touch them.
Generate patches with `git diff`. Update and re-attach the results and mutants files. Leave the candidate UNCOMMITTED and add the
note "HOSTED-PRECHECK-REQUESTED: precheck 7". Do NOT hand off. local-build-allowance.md applies under all its gates (narrow
core filters: goal_admission, turn_input, pending_work). Follow R176 and R174.
