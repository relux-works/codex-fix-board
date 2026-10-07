# Recording review — TASK-260929-3r7peh, notify-on-exit-and-exec-notification-tool

Subject: CR-TASK-260929-3r7peh-1 revision 1; candidate tree `dbd39ab8c59adabe27ebb25838003680214c8d14`; repository delta present.

Recording recommendation: accepted. Both independent panels explicitly say `accept`. The merged verdict preserves all panel findings (0), every surface result (4/4 held in each panel; 4/4 held in the merge), all nine notes and all five nonblocking free-hunt entries. No panel findings were silently dropped. The merged opt-in evidence retains panel A's explicit bound on incomplete m1 killer identities rather than repeating panel B's stronger attribution.

Evidence read through resource get:
- TASK-260929-3r7peh_review-verdict-rev1.md
- TASK-261007-2468l9_panel-verdict.md
- TASK-261007-j2lf0k_panel-verdict.md

Checks personally run: board lifecycle start (exit 0); spawn goal read (exit 0, run not goal-bound); resource get for all three outcomes (exit 0 each); Python comparison of verdict JSON, panel verdicts, ordered unique rows, findings, notes and free-hunt preservation (exit 0). The initial board projection used unknown field `resources` (exit 1); corrected to `outcomeResources` (exit 0). No failed read was treated as absence.

Per recording-brief-rev1.md, no fresh code review, product test, build or attack was run. Hosted checks and attacks remain panel-cited evidence, not personal executions. Producer coverage is reported by panel A as 8/8 AC rows mapped; 9/9 mutants killed is attached hosted evidence. The two unconfirmed retention-order suspicions remain notes, not reproduced findings. Free hunt has no blocking findings; its five entries describe nonblocking investigated shapes. Acceptance does not assert proof of absence.

Logbook: panel merge verified against all three materialized resources; no code or control-root files edited. Acceptance uses the existing merged verdict resource and routes to integrating, not done or landed.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Recording-only verification; all panel notes remain in the merged verdict referenced above."
  ],
  "surface_results": [
    {
      "row": "host capability",
      "result": "held",
      "evidence": "Both independent panel outcomes and the merged verdict; no attack rerun by recording reviewer."
    },
    {
      "row": "opt-in and receipts",
      "result": "held",
      "evidence": "Both independent panel outcomes and the merged verdict; no attack rerun by recording reviewer."
    },
    {
      "row": "exec_notification read and release",
      "result": "held",
      "evidence": "Both independent panel outcomes and the merged verdict; no attack rerun by recording reviewer."
    },
    {
      "row": "activation",
      "result": "held",
      "evidence": "Both independent panel outcomes and the merged verdict; no attack rerun by recording reviewer."
    }
  ],
  "free_hunt": []
}
```

## Acceptance evidence provenance

Two attempts to accept with the requested pre-existing merged resource returned exit 1, `change_request_evidence_missing`: this run manifest has no starting digest for that resource. Adding the recording attestation by resource update did not remove that provenance refusal. The installed Change Request contract permits a newly created task-scoped reviewer outcome, so this recording outcome is the acceptance evidence owned by this run. The merged verdict was read and fully compared before this outcome was created. This changes only the evidence name, not the reviewed revision, identity, candidate, recommendation or findings. Its surface results inherit the panels' named attacks; its empty free_hunt means no reproduced blocking free-hunt findings, while all five benign investigations remain preserved in the merged verdict.
