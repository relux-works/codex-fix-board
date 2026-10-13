# TASK-260929-3ld28o — state-change-observations recording-review audit, revision 3

Disposition: **changes requested for merge correction; recording the supplied merged verdict refused**.
Route: analysis. This is recoverable evidence rework, not an external blocker or a new implementation finding. No accept_cr or reject_cr issued.

Scope: recording-only comparison under TASK-260929-3ld28o_recording-brief-rev3.md. Read the merged revision 3 verdict and ALL THREE current attached panel outcomes: TASK-261011-2h80lb, TASK-261011-wcmuu1 and TASK-261011-16oznh. Each recommends accept. The brief says "two" but lists three; all three were compared. No source review, code change, build, test, commit or integration action.

## Exact merge correction required

The merged verdict has an empty findings array. Panel B's B-N1 and the DELTA panel's D-N1 are structured findings at severity note, both row non-resets and repeat-of rev2/B-N1. Their mechanism text survives in notes, but their complete invariant, reproduction (test_file/command/expected_failure), severity and repeat-of metadata are omitted from findings. This violates the recording brief's requirement to preserve every finding and the R132 union/collapse rule.

Restore the complete structured advisory evidence. These share a row/file/class and may collapse into one nonblocking finding with both original IDs/provenance and both reproduction records; alternatively preserve both objects. Do not promote them to blocking product findings or change any panel's accept verdict. Repeated structured-note loss was already documented in recording-review-refusal-rev1.md and recording-review-refusal-rev2.md; DELTA successor recovery explicitly required D-N1 to remain structured.

Original objects, reproduced verbatim from the current attached panel JSON:

```json
{
  "B_N1": {
    "id": "B-N1",
    "row": "non-resets",
    "invariant": "AC2/AC8: every ignored item class stays ignored; a regression that starts recording one is caught.",
    "mechanism": "Ignore-arm execution coverage beyond AC2's five named non-resets is partial: tests feed FileChange(non-completed), AgentMessage, CommandExecution, a CollabAgentToolCall subset, SubAgentActivity(non-started) and ToolFinish-success to the classifier, while McpToolCall, DynamicToolCall, FunctionCallOutput, Plan, Reasoning, WebSearch, ImageView, Extension, ImageGeneration, EnteredReviewMode, ExitedReviewMode, ContextCompaction, UserMessage and HookPrompt never reach record_state_change_for_item in tests, so a regression that starts recording one would go undetected by the suite. Mitigated structurally: the match in ext/goal/src/accounting.rs:290-334 lists every TurnItem variant explicitly with no wildcard arm, so adding a recording arm requires touching the classifier and a new variant forces compile-time handling (non-exhaustive match is a compile error; hosted lint/type-check is green on this exact tree). Classifier file is byte-identical to the rev2 green tree, so this condition is unchanged from rev2 panel-B B-N1.",
    "reproductions": [
      {
        "test_file": "codex-rs/ext/goal/src/accounting.rs (record_state_change_for_item, static read)",
        "command": "static inspection only: git show 486ebfe5:accounting.rs plus git grep of classifier feeds in the observation test files; no build or test executed (forbidden by panel brief)",
        "expected_failure": "No failure observed and none claimed as executed: the ignore arm enumerates every TurnItem variant with no wildcard, so uncovered arms are compile-time-guarded. NOT a test execution."
      }
    ],
    "severity": "note",
    "repeat-of": "rev2/B-N1"
  },
  "D_N1": {
    "id": "D-N1",
    "row": "non-resets",
    "invariant": "AC2/AC8: ignored item classes must remain ignored; execution coverage should expose a regression that starts recording one.",
    "mechanism": "Retained rev2 B-N1 advisory. Classifier-focused tests directly construct 5/19 TurnItem families. Fourteen other ignored families (UserMessage, FunctionCallOutput, HookPrompt, Plan, Reasoning, DynamicToolCall, WebSearch, ImageView, Extension, ImageGeneration, EnteredReviewMode, ExitedReviewMode, McpToolCall, ContextCompaction) lack distinct executed ignore-arm feeds. Production explicitly enumerates every variant without a wildcard, and the five AC2 categories have hosted killers. Exhaustiveness prevents omission of a new variant but cannot prevent recording an existing ignored variant. No executed surviving mutant or observed product failure is claimed.",
    "reproductions": [
      {
        "test_file": "codex-rs/ext/goal/src/accounting.rs:289-335 and classifier-focused observation test files (static inventory)",
        "command": "Static inspection on 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7: git show <candidate>:codex-rs/ext/goal/src/accounting.rs; compare TurnItem inventory and test feeds using the saved source audit. No Rust test executed locally.",
        "expected_failure": "Unknown/unexecuted: to measure the gap, feed each remaining ignored family at the goal callback and narrow the ignore match to record that family; require the corresponding new negative test to fail. Existing suite survival is not asserted."
      }
    ],
    "severity": "note",
    "repeat-of": "rev2/B-N1"
  }
}
```

## Comparison results

Panel verdict attribution: 3/3 correct (all accept).
Ordered surface results: 7/7 preserved, exactly one result per row, each held in all three panels and the merge.
Structured finding preservation: 0/2 source objects; 0/1 advisory mechanism groups retained as a complete finding.
Original panel notes retained as text: 25/25 (A 7/7, B 8/8, DELTA 10/10).
No new implementation finding was added. Prior A-F1/D-F1 closure is accepted as the panels' conclusion, not re-reviewed.

| Row | Panel A | Panel B | DELTA | Merged |
|---|---|---|---|---|
| reset sources at committing handlers | held | held | held | held |
| non-resets | held | held | held | held |
| code-mode leaf accounting | held | held | held | held |
| no model-writable bypass | held | held | held | held |
| existing activity and blocker untouched | held | held | held | held |
| transient state | held | held | held | held |
| API surface and placement | held | held | held | held |

These are supplied panel results, not a fresh technical sweep. Once the merge preserves the structured advisory, the recording reviewer can verify the repaired artifact and run accept_cr(TASK-260929-3ld28o, revision=3, evidence=TASK-260929-3ld28o_review-verdict-rev3.md). The current aggregate accept direction is unanimous, but the explicit recording brief forbids recording an incorrect merge.

## Verification and bounds

set_status(reviewing), narrow task/panel resource queries, each of the four primary resource reads, and the previous refusal read exited 0. JavaScript parsed exactly one verdict-findings block per primary artifact and compared all ordered rows, findings and note retention. This is artifact verification only.
spawn goal exited 0: run is not goal-bound. spawn directives exited 0: none.
The requested project-management skill was read successfully. Its referenced reviewer-role path was missing (cat exit 1); the explicit recording brief supplies the applicable authority. No conclusion relies on that missing read.
Hosted suite/mutant evidence is retained from the panels, not rerun or independently re-attested here.
No temporary directory or repository file was created. All evidence is attached synchronously using task-board.

## Task-scoped logbook

2026-10-11, RUN-261011-580f60: recording-only rev3 merge audit found repeated loss of B-N1/D-N1 structured nonblocking evidence. All three panels accept and all seven rows are held; source rework is not requested. Refuse the incomplete merge and route analysis for evidence correction. Restore the advisory finding metadata and then re-record revision 3 acceptance; no human-only decision is needed.
