# Review verdict — TASK-260929-u2i5rr, CR rev1 (candidate tree e50a3e72…, base 0462dcc0)

Verdict: **changes_requested** -> `to-dev`.

Candidate behavior held under every attack I ran. The blocking findings are all about gates that the named tests do not guard: narrowing mutants survive the 13-test suite. The candidate source itself was not reproduced broken.

## Evidence I ran myself
- `just test -p codex-core -E 'test(completion_receipt)'` from codex-rs: exit 0, 13 of 13 passed (log .temp/TASK-u2i5rr-review-test-01.log).
- `cargo clippy -p codex-core --lib --tests -- -D warnings`: no diagnostics mentioning completion_receipt (output filtered; overall exit not captured, so treat lint as not fully verified).
- Module size: 469 non-blank/non-comment lines excl. tests (< 500). OK.
- Mutant harness: standalone scratch crate (.temp/TASK-u2i5rr-mutant) that compiles the exact candidate blobs `completion_receipt.rs` and `completion_receipt_tests.rs` (path dep on codex-protocol). Unmutated: 13/13 pass. Each mutant is a perl edit of src/cr.rs, run with `cargo test --offline`, via `./run.sh NAME 'perl -0pi -e ...'`.

## AC coverage (n of m rows driven through the public store API): 6 of 6 have a named driving test and a refusal test
1 happy path / second claim refused; 2 exit-vs-decision both orders (barriers) / inline never queued; 3 lease failure requeue / stale token ack; 4 cancel per state; 5 capacity 64/65; 6 shared claim race. The rows are driven. The gap is gate-by-gate coverage (below), not row coverage.

## Surface table
| Row | Result |
|---|---|
| concurrency state machine | **broken** (test-guard findings F1–F3); behavioral attacks held |

Behavioral attacks that held: exit before/after decision (both orders), duplicate publish on Queued, exit after InlineResult, lease while leased, double lease race, ack after cancel, stale-token ack after requeue, cancel per state, 64/65 capacity and slot reuse after cancel, foreign thread/generation/call on status/publish/cancel, poisoned lock -> LockPoisoned.

## Findings
```json
[
 {"id":"owner-gate-unguarded-on-lease-and-resolve","row":"concurrency state machine","severity":"bypass","repeat-of":"none",
  "invariant":"A receipt is usable only by its owning thread/runtime generation/call on EVERY entry point (AC: ids tied to owner; AC2/AC6 claim entry points).",
  "mechanism":"completion_receipt.rs lease_for_sampling (line ~412) and resolve_initial_response (line ~316) carry the ForeignOwner refusal; completion_receipt_foreign_runtime_generation_is_refused exercises only status, publish_exit, cancel.",
  "reproductions":[
   {"test":"completion_receipt_tests.rs (whole suite)","command":"cd .temp/TASK-u2i5rr-mutant && ./run.sh M1_lease_owner \"perl -0pi -e 's/(pub\\(crate\\) fn lease_for_sampling.*?)Some\\(record\\) if record.owner != \\*owner => return Err\\(ReceiptError::ForeignOwner\\),\\n/\\$1/s'\"","expected_failure":"a foreign-owner lease must be refused; observed: 13 passed, 0 failed (mutant survives; a foreign generation could consume another call's completion)"},
   {"test":"same","command":"./run.sh M2_resolve_owner (same shape on resolve_initial_response)","expected_failure":"observed 13 passed (survives; a foreign owner could inline-consume or arm another call's receipt)"}]},
 {"id":"stale-lease-fail-unguarded","row":"concurrency state machine","severity":"bypass","repeat-of":"none",
  "invariant":"A stale lease token cannot act on the receipt (AC3 'stale lease token cannot acknowledge'; same token gate must hold for fail_sampling).",
  "mechanism":"fail_sampling checks `*token == lease.token`; only acknowledge_sampled is tested with a stale lease (completion_receipt_failed_lease_requeues_same_receipt_and_rejects_stale_token). A stale holder calling fail_sampling would silently requeue the live lease, enabling a duplicate lease/delivery.",
  "reproductions":[{"test":"suite","command":"./run.sh M4_fail_token (drop token comparison in fail_sampling, keep source check)","expected_failure":"a stale first_lease.fail_sampling must return StaleLease; observed 13 passed (survives)"},
   {"test":"suite","command":"./run.sh M11_fail_source / M10_ack_source (drop the source comparison in fail_sampling / acknowledge_sampled)","expected_failure":"observed 13 passed (source check untested; note token still binds, so these two are equivalent-mutant candidates and are NOT counted as blocking)"}]},
 {"id":"duplicate-exit-while-reserved-unguarded","row":"concurrency state machine","severity":"bypass","repeat-of":"none",
  "invariant":"Exactly one exit per receipt: a second publish_exit before the initial-response decision must be refused, not overwrite the retained completion (AC2 'never lost, never duplicated').",
  "mechanism":"publish_exit's `Reserved { completion: stored } if stored.is_none()` guard; completion_receipt_refuses_duplicate_exit_publication only tests a duplicate on Queued.",
  "reproductions":[{"test":"suite","command":"./run.sh M7_publish_overwrite \"perl -0pi -e 's/ReceiptPhase::Reserved \\{ completion: stored \\} if stored.is_none\\(\\) =>/ReceiptPhase::Reserved { completion: stored } =>/'\"","expected_failure":"second publish on Reserved must return InvalidTransition and keep the first completion; observed 13 passed (survives, first exit silently lost)"}]}
]
```
Killed mutants (gate is tested): M5 ack token dropped -> `..._rejects_stale_token` fails; M9 capacity `>=`→`>` -> `..._capacity_refuses_the_65th...` fails.

## Notes (non-blocking)
- The "race" tests use barriers to force ordering around a single mutex; both orders are genuinely forced, but the stdin/pushed race asserts loser as AlreadyLeased|AlreadyConsumed, which is correct given the second barrier.
- Terminal history is capped at 64; an evicted receipt reports UnknownReceipt instead of AlreadyConsumed. Bounded and documented in the error text; fine for a stage-2a leaf.
- Reserved slots have no timeout; a caller that never decides leaks a slot until cancel. Caller contract for B2, stated bound.
- Producer outcome artifact (`_results.md` with mutant evidence) was not visible on the element at review time; I could not confirm it was attached.

## Requested rework (one round, all three findings)
Add named tests that fail against M1, M2, M4, M7: foreign owner (thread, generation, call) on lease_for_sampling and resolve_initial_response, and on fail_sampling/acknowledge via a lease built for a different owner if reachable; stale first lease calling fail_sampling after re-lease must return StaleLease and leave the second lease intact; duplicate publish_exit while Reserved returns InvalidTransition and the first completion is what InlineResult/Queued later yields. Attach mutant results (NARROWING mutants, with failing test names) in the `_results.md`.
