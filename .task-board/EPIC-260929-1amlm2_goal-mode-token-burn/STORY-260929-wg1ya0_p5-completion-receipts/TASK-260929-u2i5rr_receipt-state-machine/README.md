# TASK-260929-u2i5rr: receipt-state-machine

## Description
Inactive receipt state machine for opted-in background exec completions (final plan section 5.1 and race table 5.4; stage 2a). New codex-rs/core/src/unified_exec/completion_receipt.rs (tests in completion_receipt_tests.rs): bounded opaque receipt ids tied to owning thread/runtime generation/call; a reservation of one of 64 receipt slots taken before an opted-in launch (refuse when full; separate from the 64-process cap); states Reserved -> InlineResult | Armed; Armed + finalized exit -> Queued -> LeasedToSampling -> Sampled; any unsampled state -> Cancelled(reason); lease failure -> Queued (same receipt, no duplicate). The initial-response decision and exit publication rendezvous under one receipt lock so an exit that precedes arming is either returned inline or retained until arming commits. Terminal stdin output and the pushed completion share one claim. Not wired to tools or the mailbox yet (sibling leaf B2 and later stories); no model-visible change.

## Scope
codex-rs/core/src/unified_exec/completion_receipt.rs + completion_receipt_tests.rs and the unified_exec module export only. Keep it small (<500 LoC excl. tests); no watcher/process-manager hooks (sibling leaf B2).

## Acceptance Criteria
| # | Requirement | Driving test (production entry) | Negative/refusal |
| - | ----------- | ------------------------------- | ---------------- |
| 1 | Reserved -> Armed -> Queued -> LeasedToSampling -> Sampled happy path exposes exactly one sampled claim | completion_receipt_tests.rs through the public receipt API | a second claim after Sampled is refused |
| 2 | Exit published before the initial-response decision resolves to InlineResult or is retained until Armed commits (never lost, never duplicated) | concurrent test with barriers forcing both orders | InlineResult receipt never produces a pushed completion |
| 3 | Lease failure returns the same receipt to Queued without a duplicate | test failing a lease | a stale lease token cannot acknowledge |
| 4 | Cancellation from any unsampled state is terminal with its reason; release frees the slot | tests per state | cancelled receipt cannot be leased or sampled |
| 5 | 64 slots: the 65th reservation is refused before launch; freeing a slot allows a new reservation | capacity test at N and N+1 | reservation beyond capacity refused with a structured error |
| 6 | Terminal stdin output and pushed completion share one claim: whichever is sampled first consumes it | test racing both claims | the loser observes an already-consumed claim |
