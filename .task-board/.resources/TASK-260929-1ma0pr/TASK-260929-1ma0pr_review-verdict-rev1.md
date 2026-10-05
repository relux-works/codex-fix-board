# Merged review verdict — TASK-260929-1ma0pr CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261005-3pfuvk_panel-verdict.md` (changes_requested), `TASK-261005-25osjz_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "queue-test-coverage-attestation",
      "row": "internal TurnInput variant and persistence",
      "invariant": "Claimed executed AC4 forged-payload persistence coverage must identify a test actually selected and run on the exact candidate, rather than compiling a dependency or running another package.",
      "mechanism": "TASK-260929-1ma0pr_results.md AC4/surface map and \"Not run anywhere: nothing required remains unrun\" attribute queue_service.rs:1085 to base run 37302805027. The actual run selects core, app-server and four small crates; it never selects codex-queue-extension and contains no PASS entry for the named test. .github/workflows/relux-ci.yml package selections confirm the blind spot.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/queue/tests/queue_service.rs:1085 (coverage audit embedded below)",
          "command": "python3 .temp/TASK-261005-3pfuvk/audit_queue_coverage.py",
          "expected_failure": "Exit 1: QueuePersistenceCoverageError: hosted run 37302805027 does not execute the claimed queue regression. This is an evidence-attestation failure, not a reproduced failure in queue production code.",
          "pinned_blobs": [
            "git-blob:e79341df18d478c650667ab663cb1ae2c5fb7f44",
            "git-blob:5e076dc37d7ef62879cbf55c2256288be82de9dd",
            "sha256:ed599f0fde9ca3777407e0883470363c73537d7579396a57c8d1069a5d4cbc03",
            "sha256:e82d03c48a72f9886038e87d74261bb912efbbdcefba7a5a2caff56fed2a0f87"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261005-3pfuvk"
      ]
    }
  ],
  "notes": [
    "[TASK-261005-3pfuvk] Batch limit is enforced on newly leased fragments. The real suite expects cumulative history of 9 fragments on the second wake (exec_completion.rs:239), so the literal AC wording \"a request never carries more than 8 fragments\" should be clarified as incremental admission. This panel does not infer a total-history cap or require rewriting history.",
    "[TASK-261005-3pfuvk] Sampling acknowledgement, failed/cancelled lease recovery and real process publication are deferred to story D/E by the attached brief; their current lack of production integration is not a defect of this leaf.",
    "[TASK-261005-3pfuvk] Candidate diff against the supplied base is 2310 additions and 16 deletions across 18 files, larger than the producer estimate. It includes the runtime-mailbox foundation. Suggested coherent split, if needed: mailbox foundation; bounded fragment and serde; record/wake wiring with integration coverage. No arbitrary size-only blocking finding.",
    "[TASK-261005-3pfuvk] Hosted mutation results are accepted from the attached hosted-precheck-2 resource (10 killed, 0 surviving). The panel independently fetched the full base-run record and verified selected tests and exact checkout. It did not fetch all mutant logs or execute Rust commands.",
    "[TASK-261005-25osjz] Batch bound is interpreted as newly delivered fragments: final-plan.md section 5.1 says Batch <=8 (6144 bytes), and section 5.2 explicitly permits normal history repetition. core/tests/suite/exec_completion.rs asserts 9 cumulative fragments in the second wake request. Therefore this verdict does not attest a total-request cap of 8 or 6144 bytes across accumulated history. The AC wording request never carries more than 8 fragments should be clarified by the recording reviewer; imposing that literal history cap would conflict with the accepted incremental-history plan.",
    "[TASK-261005-25osjz] Validation log is explicitly truncated (44318 bytes omitted). It proves the visible target-guard/fmt-check exits 0 and visible small-suite tail exit 0; the omitted clippy completion is not independently attested by this log. Lint/core/app-server/small success and mutant failures are accepted from TASK-260929-1ma0pr_hosted-precheck-2.md as allowed by panel-brief.md. Hosted numeric process exit codes are not supplied in that summary and remain unknown. No builds or tests were rerun by this panel.",
    "[TASK-261005-25osjz] Full replay patch is 2310 insertions plus 16 deletions across 18 paths, including runtime mailbox infrastructure from the earlier stage; producer results estimate only the leaf delta at about 1340 lines. Both exceed the 800-line guidance. A coherent split would first introduce mailbox infrastructure, then fragment/serde with tests, then record/wake wiring and integration/queue coverage; preserve dependency order and execute the exact-tree tests at each stage. This is a review-size note, not a reproduced behavior defect.",
    "[TASK-261005-25osjz] Production publication, sampling acknowledgement, cancellation/retry integration, and tool exposure remain staged to stories D/E/F by the accepted plan. Current suite admission uses CodexThread::test_enqueue_exec_completion_notification before entering real idle wake/record/transport/resume paths; this is not proof of a real process publishing a notification. Static free hunt checked lease-drop/abort, idle contributor suppression and public API separation; deferred wiring is not presented as implemented."
  ],
  "surface_results": [
    {
      "row": "exec-completion fragment",
      "result": "held",
      "detail": "Exact-tree base run 37302805027: forged recorded-history/resume public-entry attack passes; injection/classification/cap unit attacks and m1/m2/m3/m5 narrowing attacks are supported by attached precheck 2. Static trace record_pending_input -> ExecCompletionFragment -> record_conversation_items confirms wiring and 768-byte post-escape bound.",
      "reported_by": "TASK-261005-3pfuvk"
    },
    {
      "row": "batching and retention",
      "result": "held",
      "detail": "Base public-entry nine_pending_completions_sample_in_capped_batches_without_loss passes; lease FIFO cap and separate idle/in-turn predicates inspected. m4/m9/m10 killed per precheck 2; exactly-once nine-item rollout asserted. Held for incremental admission, not a cumulative-history bound.",
      "reported_by": "TASK-261005-3pfuvk"
    },
    {
      "row": "internal TurnInput variant and persistence",
      "result": "broken",
      "detail": "Serde refusal and rollout/resume attacks pass in hosted core lane; static public protocol/app-server paths remain separate and fail safely. Coverage-attestation attack reproduces the missing queue execution claimed as satisfied; queue behavioral result remains unknown. See queue-test-coverage-attestation.",
      "reported_by": "TASK-261005-3pfuvk"
    }
  ],
  "free_hunt": []
}
```


Recording-review confirmation

The recording reviewer read both original panel outcomes and this merged verdict.
A structural comparison preserved 1/1 findings (all mandatory fields and reproductions),
8/8 notes, and 3/3 surface rows in the supplied order with the worst panel result.
Panel A requests changes; panel B accepts. The merged changes_requested branch is correct.
No findings were added, no production attacks or Rust tests were rerun, and no code was changed.
The 8-fragment bound is incremental admission, not a cumulative-history cap, as both panels explain.
Later rework/precheck resources do not revise this frozen revision-1 recording decision.

Recording check: `python3 .temp/recording-review-rev1/verify_merge.py`, exit 0.
Both panel resources and the merged resource were materialized via task-board resource get (exit 0).
Run goal read reports not goal-bound. This outcome carries the evidence-attestation anomaly
for the logbook without editing the control root.
