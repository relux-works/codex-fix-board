# Merged review verdict — TASK-260929-u2i5rr CR revision 5 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261002-2bf97a_panel-verdict.md` (changes_requested), `TASK-261002-e90uy2_panel-verdict.md` (accept), `TASK-261002-1knmn0_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "resolve-initial-response-active-nonreserved-arm-unguarded",
      "row": "concurrency state machine",
      "invariant": "A second or late initial-response decision on an active receipt that is no longer Reserved is refused with InvalidTransition and never overwrites Queued/Leased/Armed state, so a retained or queued exit is never lost.",
      "mechanism": "completion_receipt.rs resolve_initial_response, arm `(phase, _) => return Err(InvalidTransition{actual: phase.status()})`. No test calls resolve_initial_response with the legitimate owner on an Armed, Queued or LeasedToSampling receipt (all owner-matching call sites are on Reserved receipts; the terminal cases go through terminal_error, not this arm). A mutant that turns this arm into `Action::Armed` or `Action::Queued(..)` overwrites Queued(completion) with Armed, silently losing the exit. Static analysis only; not executed.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/unified_exec/completion_receipt_tests.rs",
          "command": "Mutant (static, not run): in resolve_initial_response replace the `(phase, _) => { return Err(...) }` arm body with `Action::Armed`. Then `just test -p codex-core -E 'test(completion_receipt)'`.",
          "expected_failure": "Add a test: after `queued_receipt`, `resolve_initial_response(id, &owner, Arm)` and `(.., InlineResult)` must return Err(InvalidTransition{actual: Queued}); after an Arm, a second Arm and an InlineResult must return Err(InvalidTransition{actual: Armed}); after a lease the same calls return Err(InvalidTransition{actual: LeasedToSampling{..}}); status is unchanged and the lease still acknowledges the original completion. The mutant turns it red; today it survives by reading."
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261002-2bf97a"
      ]
    }
  ],
  "notes": [
    "[TASK-261002-2bf97a] Hosted relux-ci for the exact rev5 tree is attached and green (run 36987452652); local execution was not re-run in this panel.",
    "[TASK-261002-2bf97a] Smaller untested arms, not counted as findings: cancel/publish_exit/lease on an evicted id return UnknownReceipt via the same `terminal_error` None arm, but only `status` asserts UnknownReceipt; a mutant mapping `cancel`'s UnknownReceipt arm to AlreadyTerminal survives by reading. publish_exit on a LeasedToSampling receipt (the `phase =>` arm) is untested but shares the arm with the Queued case that is tested.",
    "[TASK-261002-2bf97a] The sampling race test is ordered by barriers around one mutex, so it proves linearization semantics, not interleaving; sufficient for a single-lock stage-2a leaf.",
    "[TASK-261002-2bf97a] Reserved slots have no timeout (caller contract for B2); `#![allow(dead_code)]` covers the intentionally unwired API; terminal history is bounded at 64 and evicted ids report UnknownReceipt.",
    "[TASK-261002-e90uy2] {'id': 'execution-bound', 'text': 'This panel performed replay, exact-blob inspection and static attacks only. No Rust build, test or mutant was executed. Held means held under the explicitly requested static panel with reused execution evidence, not an observed mutant kill. Current measured mutant executions: 0; statically mapped prior mutant/refusal variants: 11/11.'}",
    "[TASK-261002-e90uy2] {'id': 'hosted-evidence', 'text': 'Reused TASK-260929-u2i5rr_hosted-ci-rev5.md: commit 00726e16afb1f84c81717b3fe404c5965438b170, exact tree 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8, run 36987452652 reports success for lint, small, core and app-server. The panel brief reports 20 passing receipt tests; the attached summary itself contains job conclusions, not individual test rows. No fresh provider query was made. Historical mutant logs in the rev5 archive are not current mutant execution evidence.'}",
    "[TASK-261002-e90uy2] {'id': 'inactive-scope', 'text': 'The store has no non-test runtime caller; git grep finds only its declaration and implementation. This is expressly the inactive B1 scope. Reserve-before-launch, actual prompt membership, output retention, mailbox integration and transport acknowledgment remain B2/later obligations, not attested here.'}",
    "[TASK-261002-e90uy2] {'id': 'size', 'text': 'Candidate has 1534 added lines across exactly three allowed paths, including 998 test lines. This exceeds repository review-size guidance. Implementation is 532 physical lines before its test module, but under 500 nonblank/noncomment lines. Existing single coherent state-machine stage; nonblocking maintainability note, no new split prerequisite requested.'}",
    "[TASK-261002-e90uy2] {'id': 'free-hunt-bounds', 'text': 'Static free hunt checked cloned lease reuse, cancel/ack ordering, reserved-with-retained-exit cancellation, terminal eviction, UUID collision checks, byte-based owner bounds, lock scope and runtime callers. No additional defect found. UUID retry exhaustion is not injected, scheduler interleavings are not exhaustively modeled, and the test using MAX_COMPLETION_RECEIPTS as its loop bound would not detect coordinated changes to both active and terminal constants. These are stated bounds, not claims of absence.'}",
    "[TASK-261002-1knmn0] Replay: write-tree equals expected candidate tree 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8 (exit 0 at every step).",
    "[TASK-261002-1knmn0] Scope: the three out-of-scope upstream lint edits are reverted; candidate touches exactly completion_receipt.rs, completion_receipt_tests.rs and one export line in unified_exec/mod.rs. The prior-round scope notes are resolved.",
    "[TASK-261002-1knmn0] Hosted evidence (run 36987452652, tree 00518744) shows four green jobs; the artifact lists job conclusions only, not per-test names, so the 20-test and named-test claims rest on my static count of 20 completion_receipt_* fns, not on a visible test list.",
    "[TASK-261002-1knmn0] Residual unguarded mutant (non-gate, robustness-level, not reported as finding): cancel() on an evicted/unknown id maps UnknownReceipt through the :504 arm; deleting it would yield AlreadyTerminal and no test calls cancel/lease/resolve/publish on an evicted id (UnknownReceipt is asserted only via status, once). Same for terminal_error's None => UnknownReceipt arm on the non-status paths. Refusal still happens either way; only the error variant differs.",
    "[TASK-261002-1knmn0] Residual: IdGenerationFailed and the id-collision check in reserve() have no test; unreachable without an injection seam (v4 UUID), so it is an accepted bound.",
    "[TASK-261002-1knmn0] Residual (equivalent-mutant candidate): the `*source == lease.source` check in fail_sampling/acknowledge_sampled is redundant given the token; no test forges a lease with matching token and different source. Not counted.",
    "[TASK-261002-1knmn0] Stated bounds carried from earlier rounds: Reserved slots have no timeout (caller contract for sibling B2); evicted terminal ids report UnknownReceipt; module is unwired (#![allow(dead_code)]) by design for stage 2a; barrier tests prove ordering semantics under one mutex, not true interleaving, which is sufficient with a single lock.",
    "[TASK-261002-1knmn0] Size: 535 impl lines (466 non-blank non-comment, under 500) and about 998 lines of tests; test-dominated and a single coherent stage."
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "held",
      "reason": "All 6/6 AC rows have named receipt-API driving and refusal assertions in the exact candidate. Statically attacked early exit/arm ordering, duplicate publication, stale leases, cancellation, 64/65 capacity, foreign owners on active and terminal paths, shared-source claims and lock poisoning. New rev5 assertions defeat each requested mutant by direct control/data-flow inspection. Execution evidence is reused exact-tree hosted CI, not a new panel test run.",
      "evidence": [
        "completion_receipt_tests.rs:70-358",
        "completion_receipt_tests.rs:363-613",
        "completion_receipt_tests.rs:616-997",
        "TASK-260929-u2i5rr_hosted-ci-rev5.md"
      ],
      "reported_by": "TASK-261002-e90uy2"
    }
  ],
  "free_hunt": [
    "[TASK-261002-2bf97a] Slot accounting: retire removes from `active`, so Sampled/InlineResult/Cancelled free the slot; reserve checks `active.len() >= 64`; terminal entries do not consume capacity. Held.",
    "[TASK-261002-2bf97a] ReceiptId collision: reserve checks active and terminal before insert. Held; IdGenerationFailed is not reachable by test.",
    "[TASK-261002-2bf97a] Lease token is a fresh Uuid per lease; clone sharing is refused by token/consumed checks; the redundant `source` equality is an equivalent-mutant candidate.",
    "[TASK-261002-2bf97a] publish_exit after InlineResult or Cancelled returns a structured error rather than silently dropping; the caller owns the consequence in B2.",
    "[TASK-261002-1knmn0] Checked that the foreign-owner test builds its forged leases from a real lease clone with receipt_id and owner overwritten, so fail_sampling/acknowledge_sampled reach terminal_error with a foreign owner for each terminal kind (not just the active path).",
    "[TASK-261002-1knmn0] Checked the eviction test against the capacity bound: it reserves and cancels sequentially so active never exceeds 1, and it uses MAX_COMPLETION_RECEIPTS+1 = 65 outcomes while the code bound is the separate MAX_TERMINAL_RECEIPTS (both 64); changing the code constant in either direction is caught, but a future divergence of the two constants would make the test's 65 count stale, which is a maintenance note only.",
    "[TASK-261002-1knmn0] Checked mutants on retire(): active.remove then push_back; dropping the remove would leak slots and be caught by the capacity and cancel-frees-slot tests; swapping the retired phase kind is caught by the per-kind status assertions in the terminal test.",
    "[TASK-261002-1knmn0] Checked terminal-lookup order: terminal() scans newest-first; no duplicate ids are possible (reserve checks both active and terminal), so rev and find order is equivalent.",
    "[TASK-261002-1knmn0] Checked that the new test never relies on timing or thread scheduling; the only threaded tests use barriers with a forced order.",
    "[TASK-261002-1knmn0] Checked reserve() slot accounting after Inline/Sampled/Cancelled: all three go through retire(), the single path that removes from active."
  ]
}
```
