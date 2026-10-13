# TASK-260929-3ld28o — state-change-observations recording-review audit, revision 2

Disposition: **changes requested for merge correction; recording the supplied merged verdict refused**.
Route: analysis. This is recoverable evidence rework, not an external blocker. No accept_cr or reject_cr issued.

Scope: recording-only comparison required by TASK-260929-3ld28o_recording-brief-rev2.md. All THREE panel outcomes were read: TASK-261010-1nhjne (changes_requested), TASK-261010-2yblx8 (accept), TASK-261010-1rwut6 (changes_requested). The brief says "two" but lists three; all three were compared. No source review, new implementation finding, code change, build, test, commit or integration action.

## Exact merge correction required

Panel B's B-N1 (severity note, row non-resets) is absent from the merged findings array. Its complete mechanism is retained as a note, but the invariant, reproduction test_file/command/expected_failure, severity and repeat-of metadata are not retained as a finding object. Restore the complete original object, keeping severity note and repeat-of none. Do not promote it to a blocking product finding or change Panel B's accept verdict.

B-N1 is a different row/file/class from A-F1 and D-F1; under the supplied R132 union rule it cannot be omitted. The previous recording-review refusal rev1 identified this same structured-note-loss problem. This is a merge defect, not a new implementation finding.

The original B-N1 object, reproduced verbatim from Panel B for the evidence editor:

```json
{
  "id": "B-N1",
  "row": "non-resets",
  "invariant": "AC2/AC8: every ignored item class stays ignored; a regression that starts recording one is caught.",
  "mechanism": "Ignore-arm execution coverage beyond AC2's five named non-resets is partial: tests feed FileChange(non-completed), AgentMessage, CommandExecution, a CollabAgentToolCall subset, SubAgentActivity(non-started) and ToolFinish-success to the classifier, while McpToolCall, DynamicToolCall, FunctionCallOutput, Plan, Reasoning, WebSearch, ImageView, Extension, ImageGeneration, EnteredReviewMode, ExitedReviewMode, ContextCompaction, UserMessage and HookPrompt never reach record_state_change_for_item in tests, so a regression that starts recording one would go undetected by the suite. Mitigated structurally: the match in ext/goal/src/accounting.rs:289-335 lists every TurnItem variant explicitly with no wildcard arm, so adding a recording arm requires touching the classifier and a new variant forces compile-time handling (non-exhaustive match is a compile error; hosted lint/type-check is green on this exact tree). Same observation class as rev1 panel-B note F3; the rev1 merged verdict carried it as a note, not a finding object, so repeat-of is none.",
  "reproductions": [
    {
      "test_file": "codex-rs/ext/goal/src/accounting.rs (record_state_change_for_item, static read)",
      "command": "static inspection only: git show 568588ed:accounting.rs plus git grep of classifier feeds in the three observation test files; no build or test executed (forbidden by panel brief)",
      "expected_failure": "No failure observed and none claimed as executed: the ignore arm enumerates every TurnItem variant with no wildcard, so uncovered arms are compile-time-guarded. NOT a test execution."
    }
  ],
  "severity": "note",
  "repeat-of": "none"
}
```

## Comparison results

Structured finding preservation: 2/3 original objects (A-F1 and D-F1), all original fields/reproduction values preserved in those two, plus added provenance/pinned blobs. Advisory mechanism retention: 1/1 (B-N1); complete advisory object retention: 0/1.
Original panel notes retained: 25/25 (A 7/7, B 10/10, delta 8/8).
Panel verdict attribution: 3/3 correct.
Surface coverage/order and worst-result selection: 7/7, exactly one merged result per row.

| Row | Panel A | Panel B | Delta | Merged |
|---|---|---|---|---|
| reset sources at committing handlers | broken | held | broken | broken |
| non-resets | held | held | held | held |
| code-mode leaf accounting | held | held | held | held |
| no model-writable bypass | held | held | held | held |
| existing activity and blocker untouched | held | held | held | held |
| transient state | held | held | held | held |
| API surface and placement | held | held | held | held |

These are the supplied panel results, not a fresh technical sweep. One broken row and six held rows are preserved. The two blocking findings both describe the accepted V1 spawn/liveness observation defect; neither was dropped. Their original differing repeat-of values are preserved without adjudication.

After the merge is corrected, the recording reviewer should compare the repaired artifact and issue reject_cr(TASK-260929-3ld28o, revision=2, evidence=TASK-260929-3ld28o_review-verdict-rev2.md). Current aggregate changes_requested direction is justified, but the explicit recording brief forbids recording an incorrect merge.

## Verification and bounds

Initial set_status(reviewing): exit 0. resource get for merged verdict and three panels: exit 0 each. JavaScript parsed each verdict-findings block and compared original fields/reproduction values, note retention and all ordered surface rows successfully. This was artifact verification only. No Rust/CI/mutant execution performed or inferred.
spawn goal: exit 0, run is not goal-bound. spawn directives: exit 0, none.
One unsupported resources projection failed exit 1 and was corrected to outcomeResources. Missing reviewer reference path search exited 2; supplied recording brief/R132 remains the authority. command -v logbook exited 1; schema(operation=logbook) exited 1 (unknown operation). No failed read was treated as absence of a verdict.
No temporary directory or repository file was created. Evidence was attached synchronously through the task-board CLI.

## Task-scoped logbook

2026-10-10: Recording-only rev2 audit found repeated loss of a structured note finding (B-N1). Overall verdict direction and 7/7 row aggregation are correct. Refuse recording the incomplete merge and route analysis for the orchestrator to restore B-N1's complete original object. No human-only decision required. Standalone logbook unavailable; this entry and task notes preserve the anomaly.
