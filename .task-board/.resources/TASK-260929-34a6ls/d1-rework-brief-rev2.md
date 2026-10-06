# TASK-260929-34a6ls (D1): CR revision 2. Acknowledge at submission, not after the turn's tool phase

Review round 1 (`TASK-260929-34a6ls_review-verdict-rev1.md`, outcome) is **changes_requested**, with one finding,
`submission-ack-after-response` (row "acknowledgment point", severity regression):

codex-rs/core/src/session/turn.rs:1694 acknowledges only after `try_run_sampling_request` returns Ok. That happens after
the response completes (~:2939), then tool draining (~:3153), then a possible cancellation (~:3164). So a request that WAS
submitted and sampled can still end as TurnAborted, and tasks/mod.rs:1052 then requeues its lease. The completion is
delivered twice, which breaks "logical notification once per live generation".
The other two rows (membership authority; failure, retry and suspension) held.

Do this:
1. Move the acknowledgment to the point where the request containing the fragment is known to be submitted and sampled
   on the selected transport (HTTP, WS, or fallback). That point is the successful stream submission or response
   completion for THAT request, before tool draining and cancellation. A later abort/cancel of the turn must not requeue
   a lease that is already acknowledged. A failure BEFORE submission still returns the lease unleased (unchanged).
2. Add a public-entry suite test: the sampled request completes, then the turn is cancelled or aborted during tool
   draining (latch, no sleeps). Assert the receipt is acknowledged exactly once and NOT requeued or re-sampled.
   Add a narrowing mutant that restores the post-turn acknowledgment point, and confirm that test kills it.
3. Keep the existing membership and failure tests green. Update TASK-260929-34a6ls_results.md and the mutants file
   (re-attach both). Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 3".
   Do NOT hand off. Fast lane only; follow R176 and R174.
