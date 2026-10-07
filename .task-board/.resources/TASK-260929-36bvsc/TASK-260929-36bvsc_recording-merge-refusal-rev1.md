# TASK-260929-36bvsc — recording review merge refusal, revision 1

Decision: refuse recording the supplied merged verdict until its duplicate mechanism is collapsed. Both panels request changes; no acceptance is authorized. Route to `to-dev` as required by the reviewer lifecycle; this is not a fresh code review.

Candidate: `0edaf3a0edd354ef941f7e5d0f92bd0e44ed8f1d`. Sources: `TASK-260929-36bvsc_review-verdict-rev1.md`, `TASK-261006-1z552y_panel-verdict.md`, `TASK-261006-3gh4h9_panel-verdict.md`, all obtained through board resource get.

Verification: 2 of 2 panel findings preserved, including every reproduction and repeat-of field; 3 of 3 surface rows preserved in order. No panel finding or row is missing. The merge is nevertheless invalid under the one-mechanism/one-finding contract: `sampled-receipt-remains-pending` and `acknowledged-store-claim-still-pending` describe the same mailbox-only acknowledgement leaving B-store Queued and the snapshot reintroducing it. Distinct panel IDs do not make two mechanisms. Collapse them to one stable class, retaining both panels' reproductions, attribution, and evidence bounds. Preserve all notes and all three surface results. Then resume the recording reviewer against the corrected resource.

No Rust test, new attack, or source modification performed. Attached hosted results and panel static evidence were inspected, not rerun. No new behavioral finding is asserted. The supplied merged verdict remains attached unchanged; reject_cr is deliberately not invoked with invalid findings.

## Logbook

Recording review identified duplicated finding identity in the orchestrator merge; nothing was dropped. Both panel verdicts remain changes_requested. This refusal concerns verdict normalization, not a new implementation defect and not an external blocker.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "duplicate-mechanism-in-merged-verdict",
      "text": "Recording refusal only: collapse the two existing panel IDs for the same mailbox-only acknowledgement mechanism. No new code finding."
    }
  ],
  "surface_results": [
    {
      "row": "snapshot contents",
      "result": "broken",
      "evidence": "Static production-call trace above confirms acknowledged work is reintroduced from store Queued. Hosted run 37463583436 and narrowing runs 37463702577 (suspended admitted) / 37463635217 (queued excluded) cover membership/dedup but mask production acknowledgement by manually retiring the B receipt. Runtime confirmation of the newly identified path requested, not executed.",
      "reported_by": "TASK-261006-1z552y"
    },
    {
      "row": "revision and atomicity",
      "result": "held",
      "evidence": "Held for executed transition-bump attack: exact-tree hosted base 37463583436 and suspend_skips_revision_bump mutant 37463660857 killed by revision_increases_on_suspend. Store mutations bump while holding state lock; union covers both Armed and Queued. Named fourteen revision tests exist. This result does not attest coherent revision snapshots or genuinely concurrent AC4 execution; both limits are notes above.",
      "reported_by": "TASK-261006-1z552y"
    },
    {
      "row": "read failure and API boundary",
      "result": "held",
      "evidence": "Exact-tree hosted base 37463583436; provider_missing_mapped_to_empty mutant 37463609295 killed in core/small by read_failure_returns_explicit_error_not_empty_snapshot and goal_read_failure_is_explicit_error_not_empty. Static try_read_snapshot propagates both lock failures; read_pending_work preserves ProviderMissing/provider errors. Session installs weak-session provider; no Cargo dependency changes/core-to-goal edge introduced. Production provider contention end-to-end is not directly exercised by the new component tests.",
      "reported_by": "TASK-261006-1z552y"
    }
  ],
  "free_hunt": []
}
```
