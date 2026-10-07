# Merged review verdict — TASK-260929-3f6hfg CR revision 1 (tb-R141 / R132 merge)

Verdict: **accept**

Panel outcomes: `TASK-261007-3f3rcp_panel-verdict.md` (accept), `TASK-261007-2ijufn_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [],
  "notes": [
    "[TASK-261007-3f3rcp] {'id': 'user-input-concurrency-bound', 'row': 'negatives', 'text': 'Consecutive turn/start admissions while waiting are exercised, not overlapping submissions or thread/queue. No failing reproduction established; do not infer concurrent-queue coverage.'}",
    "[TASK-261007-3f3rcp] {'id': 'silence-observation-bound', 'row': 'controlled-exit vertical', 'text': 'Armed narrowing mutant is killed by the required wake-fragment assertion at line 357, not the pre-release count. This covers extra continuation through request ordering, with finite observation checkpoints.'}",
    "[TASK-261007-3f3rcp] {'id': 'drop-wake-diagnostic-bound', 'row': 'harness quality', 'text': 'The raw failure reports the wiremock destructor count assertion after the bounded missing-wake wait, not a directly printed timeout. This is a valid kill with less precise diagnostics.'}",
    "[TASK-261007-2ijufn] silence-ignores-armed kills notified_exec at :357 via fragment displacement, not at the :338 pre-release count: the stray continuation lands after the check and displaces the wake request. This empirically confirms the test docstring's own race analysis (inflate pre-release count / displace wake / inflate final count); the gated base tree has no stray continuation, so no flakiness.",
    "[TASK-261007-2ijufn] drop-wake mutant inverts queue_wake rather than purely narrowing (retention/inline outcomes now also enqueue). The kill mechanism on the named tests is exactly the dropped Queued wake; mutant-description imprecision only, no effect on the kill.",
    "[TASK-261007-2ijufn] AC6 queue-API shape (thread/queue/*) is not driven; the burst shape is. The AC allows 'queued or burst' and the queue API is an experimental separate surface, so this is out-of-contract per the AC wording, not a gap.",
    "[TASK-261007-2ijufn] The Windows PowerShell barrier variant is written but unproven on hosted CI (no Windows app-server lane); disclosed in the results. AC7 targets the hosted Linux lane, where all 4 tests demonstrably execute.",
    "[TASK-261007-2ijufn] The local CR validation log is truncated at the 64 KiB board cap (known BUG-260917-38ob0v); its tail is green (exit 0, 267 small-crate tests, 4/4 coverage shards). The hosted lint and small lanes re-ran the same commands on the same tree (base run success)."
  ],
  "surface_results": [
    {
      "row": "controlled-exit vertical",
      "result": "held",
      "evidence": "Exact candidate hosted base passes notified_exec_exit_wakes_gated_goal_with_receipt_fragment. Candidate+narrowing mutants silence-ignores-armed, drop-wake, wake-without-fragment all kill that public JSON-RPC/tool-dispatch test (raw jobs and exact mutant replay trees above). Assertions check Active/2 requests before release, receipt/source/exit code after release, 4 requests and Complete; held only for these named attacks.",
      "reported_by": "TASK-261007-3f3rcp"
    },
    {
      "row": "negatives",
      "result": "held",
      "evidence": "Hosted base passes headless_host_refuses_notify_on_exit_and_promises_no_wake, unopted_server_process_does_not_gate_goal_continuation, user_burst_during_background_wait_admitted_without_loss_or_duplication. Headless direct-call refusal narrowed and killed at line 612; default subscription mutant killed at line 540. User turns are accepted before release and reconstructed exactly once through thread/read. Concurrent submission is outside measured coverage.",
      "reported_by": "TASK-261007-3f3rcp"
    },
    {
      "row": "harness quality",
      "result": "held",
      "evidence": "All four tests execute in native hosted Linux app-server lane; registration and auto-env defaults checked. Five production-only mutants replay to hosted trees and each is killed by a named vertical public-entry test, not solely collateral suites. Release-file barriers and bounded notification/RPC waits avoid timing-based test sleeps. Remote/Wine skips carry reasons; headless test has no skip. Drop-wake diagnostic limitation recorded as a note.",
      "reported_by": "TASK-261007-3f3rcp"
    }
  ],
  "free_hunt": []
}
```

## Recording reviewer attestation — RUN-261007-554bf3

I read both complete panel outcomes and verified their merge against this artifact: both recommend accept; blocking findings union is empty; all 8 notes are preserved with attribution; all 3 surface rows remain held in the required order; panel A row evidence and panel B free-hunt account are preserved. No finding or row was omitted. I accept CR-TASK-260929-3f6hfg-1 revision 1, candidate tree c83869e576d1e024cfdbb5f63cfe8b83c6e969cb, on that panel evidence. This recording run did not rerun behavioral tests or add independent findings.

Merge verification and source hashes: TASK-260929-3f6hfg_recording-review-rev1.md. The run goal query reported not goal-bound. The initial acceptance attempt refused with change_request_evidence_missing because this merged resource predated the run without a manifest digest; this reviewer-authored attestation updates the named evidence through resource CRUD. Acceptance is not integration or landing.

## Preserved panel free-hunt account

[TASK-261007-2ijufn] Swept beyond the table: mod.rs delta is exactly +1 line; candidate tree equals accepted F1 checkpoint aa2768db7f plus the 2 F2 files; barrier determinism argument holds (fresh release path, spawn-before-yield-before-completion ordering, fail-closed 'Process running' assertions); post-completion count assertions cannot pass with a late wake (exact script counts + fail-closed responder); goal/get round-trips need no flush guarantee (late continuations fail via displacement/count, confirmed empirically). No blocking findings; 5 non-blocking notes recorded above.

The panel narrative reports no blocking free-hunt finding. It is preserved here as prose; the acceptance findings schema uses an empty free_hunt array. The original merged resource encoded that narrative as one array entry and was refused by accept_cr_surface_rows_missing. Both panel findings arrays and all eight notes remain unchanged. The legacy run manifest additionally refused the original resource name even after update; this newly attached recording-owned resource supplies the same merged verdict with a compatible evidence schema.
