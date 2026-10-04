# Recording reviewer note — TASK-260929-u2i5rr CR rev 5

Verdict: changes_requested (reject_cr, evidence TASK-260929-u2i5rr_review-verdict-rev5.md).

Panels: 2bf97a = changes_requested, e90uy2 = accept, 1knmn0 = accept. Not every panel accepted, so accept is not available.

Merge check:
- Findings: Panel A's single finding (resolve-initial-response-active-nonreserved-arm-unguarded, robustness, repeat-of none) is kept in the merged verdict.
- Panels B and C raised no findings.
- Merge defect, row result: the merged surface_results records row "concurrency state machine" as `held` (reported by e90uy2). Under the R132 rule (each row takes its worst panel result) it must be `broken`, with Panel A's finding attached. The orchestrator's verdict artifact should carry `broken`. The routing result is the same, because the finding blocks.
- Panel A's row text ("held except the one finding") was not carried over.

Independent confirmation (read-only, not executed): in completion_receipt_tests.rs every call to resolve_initial_response by the legitimate owner (lines 59, 83, 152, 191, 220, 279, 293, 390, 401, 531, 678, 891, 919) targets a Reserved receipt. The 390/401 calls arm a Reserved receipt, and 531 is the terminal-owner test. Nothing exercises the `(phase, _) => InvalidTransition` arm of resolve_initial_response on an Armed, Queued or Leased receipt. A mutant turning that arm into `Action::Armed` would overwrite Queued(completion) and lose the exit, and the 20 tests would stay green. This is the same untested-gate class as the rev4 findings.

Requested rework: one test. After `queued_receipt`, both Arm and InlineResult from the legitimate owner must return InvalidTransition{Queued}. The same holds for Armed (second Arm and InlineResult) and for LeasedToSampling. Status must be unchanged, and the lease must still acknowledge the original completion.

Panel A's non-blocking notes: cancel/publish_exit/lease on an evicted id are untested for UnknownReceipt, and publish_exit on LeasedToSampling is untested. These can ride along in the same test.

Bounds: no builds or mutants were executed in this run. Hosted CI on tree 00518744 (run 36987452652) is green, and execution evidence is reused.
