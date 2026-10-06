# TASK-260929-34a6ls (D1): CR revision 3. Structural fix: acknowledge at server acceptance, unconditionally

Review round 2 (`TASK-260929-34a6ls_review-verdict-rev2.md`, outcome) is **changes_requested**. All three panels independently
report the SAME class as round 1 (repeat-of `submission-ack-after-response`), now at earlier sites:

- turn.rs ~:3150 still gates the only acknowledgment on `outcome.is_ok()` after the response loop.
- After the server accepted the request (ResponseEvent::Created at ~:2673, or the first output), these paths still skip it:
  a stream error or EOF (~:2659-2663), cancellation (~:2632), and a fallible budget accounting step AFTER response.completed
  (record_token_usage_info, ~:2966-2976 -> agent/control/budget.rs:12-14 SessionBudgetExceeded on normal exhaustion).
- tasks/mod.rs:739 / :1052 and exec_completion_ack.rs:145 then fail the still-tracked, already-sampled lease back to unleased,
  so the completion is delivered twice.

Fixing one site per round is not converging. Make it STRUCTURAL:
1. Acknowledge the request's tracked member leases at the single point where the transport reports the server ACCEPTED
   that request (Created, or the earliest equivalent acceptance signal on HTTP, WS and the fallback). Nothing that happens
   later (stream error, EOF, cancellation, budget or accounting error, tool drain, turn abort) may un-acknowledge or fail
   those leases. A failure BEFORE acceptance (connect, send, HTTP error status, WS handshake) still returns them unleased.
2. Make the lease state enforce this: once a lease is acknowledged, a later fail/requeue on it is a no-op. That stops every
   downstream error path from requeuing it, including ones not listed here. Add a unit test for that idempotence.
3. Add public-entry suite tests (latches, no sleeps) for each post-acceptance path: a stream error after Created; EOF after
   output; cancellation after Created; SessionBudgetExceeded raised after response.completed. Each asserts the receipt is
   acknowledged exactly once and never re-sampled. Also add the pre-acceptance failure case (still retried).
4. Narrowing mutants: (a) acknowledgment gated on outcome success again; (b) fail-after-ack requeues; (c) acknowledgment on
   completed instead of acceptance. Each must be killed by a named test.
5. Panel note: an omission test where a receipt is tracked but then removed from the assembled input, if you can drive it.
Update results and mutants (re-attach). Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 5".
Do NOT hand off. The same single targeted local run as last time is allowed under the same gates (df >= 50 GiB, CPU idle >= 25%,
record disk before and after, trim afterwards, nothing in parallel). ADDED GATE (tb-arbiter, tonight): also run
`memory_pressure | tail -1` right before. Do NOT start if the free percentage it reports is under 30%. During the build,
re-check it periodically (for example, poll it in a loop in the background) and STOP the build (kill cargo) if it falls under 30%.
Record the memory readings in the results with the disk/CPU readings. Follow R176 and R174.
