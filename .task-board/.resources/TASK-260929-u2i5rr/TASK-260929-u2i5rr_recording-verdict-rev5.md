# Recording verdict — TASK-260929-u2i5rr CR revision 5

Verdict: **changes_requested**

Inputs: merged verdict `TASK-260929-u2i5rr_review-verdict-rev5.md` and panel outcomes TASK-261002-2bf97a (changes_requested), TASK-261002-e90uy2 (accept), TASK-261002-1knmn0 (accept). Panel A's finding was reproduced by reading the exact candidate tests (see the note on that finding). Accept is unavailable because not every panel accepted.

Merge check: the single finding was kept. The merged artifact records the surface row as `held`. Under the R132 worst-result rule it is `broken`, and it is corrected below.

Rev4 findings: all five (terminal-history-paths-untested, owner-call-id-boundary-256, terminal-path-owner-gates-unguarded, terminal-history-bound-unguarded, sampling-source-attribution-nondeterministic) are closed. The three panels agree, by static inspection plus hosted CI on tree 00518744 (run 36987452652, all four lanes green). No mutant was executed by any panel, and none in this run.

```verdict-findings
{
  "findings": [
    {
      "id": "resolve-initial-response-active-nonreserved-arm-unguarded",
      "row": "concurrency state machine",
      "invariant": "A second or late initial-response decision on an active receipt that is no longer Reserved is refused with InvalidTransition and never overwrites Queued/Leased/Armed state, so a queued exit is never lost.",
      "mechanism": "completion_receipt.rs resolve_initial_response, arm `(phase, _) => return Err(InvalidTransition{actual: phase.status()})`. In completion_receipt_tests.rs every call by the legitimate owner (lines 59, 83, 152, 191, 220, 279, 293, 390, 401, 531, 678, 891, 919) targets a Reserved receipt; lines 578 and 669 use foreign owners. No test drives Arm or InlineResult onto an Armed, Queued or LeasedToSampling receipt. A mutant replacing the arm body with `Action::Armed` overwrites Queued(completion) with Armed and loses the finalized exit, and all 20 tests stay green.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/unified_exec/completion_receipt_tests.rs",
          "command": "Mutant (apply to a scratch copy, not the candidate): in resolve_initial_response replace the `(phase, _)` arm body with `Action::Armed`; then `just test -p codex-core -E 'test(completion_receipt)'`. Missing test: a Queued receipt must return Err(InvalidTransition{actual: Queued}) for both Arm and InlineResult from its owner.",
          "expected_failure": "Today all 20 tests pass under the mutant (survives). After rework, the new test must fail under it: Queued/Armed/LeasedToSampling receipts refuse Arm and InlineResult with InvalidTransition{actual: <that state>}, status is unchanged, and the lease still acknowledges the original completion.",
          "pinned_blobs": ["sha256:0bb4312c83c60758045bd34dc5dab69c3bd28832b4544eec082751bb88716981", "sha256:7f4f65c176045fa4ea153b568e23cad65eca6a81237a1704ae60568268940ac6"]
        }
      ],
      "severity": "robustness",
      "repeat-of": "rev4/terminal-path-owner-gates-unguarded"
    }
  ],
  "notes": [
    "Smaller untested arms, not counted: cancel/publish_exit/lease on an evicted id return UnknownReceipt via terminal_error's None arm, but only status asserts UnknownReceipt. publish_exit on LeasedToSampling is untested. Both can ride along in the same test.",
    "Barrier tests prove linearization under one mutex, not true interleaving. Sufficient for a single-lock stage-2a leaf.",
    "The `*source == lease.source` check in fail_sampling/acknowledge_sampled is redundant given the token (equivalent-mutant candidate).",
    "IdGenerationFailed and UUID collision handling are unreachable without an injection seam (accepted bound). Reserved slots have no timeout (caller contract for B2).",
    "Size: 535 physical lines in completion_receipt.rs, 466 non-blank non-comment (under 500). The module is unwired by design (#![allow(dead_code)]).",
    "No build, test or mutant was executed in this run; execution evidence is hosted relux-ci on the exact rev5 tree."
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "broken",
      "reason": "One finding (resolve-initial-response-active-nonreserved-arm-unguarded). All other attacks held by static read: exit/decision orders, stale lease, lease failure, cancel from each state, 64/65 capacity, shared-claim race, foreign owners on active and terminal receipts, terminal history bound, 256-byte call id, poisoned lock."
    }
  ],
  "free_hunt": [
    "Read the full implementation against all five rev4 mutants and the rev5 tests; no new product-code defect found. The only gap is test coverage."
  ]
}
```
