# TASK-260929-3ld28o — state-change-observations recording-review audit, revision 1

Disposition: **changes requested for merge correction; recording the supplied merged verdict refused**.
Route: `analysis` for correction of the merged evidence. This is recoverable board-evidence rework, not an external blocker. No accept_cr or reject_cr issued by this recording reviewer.

Scope: verification of the merge only, as required by TASK-260929-3ld28o_recording-brief-rev1.md. No new implementation findings, source edits, builds, tests, commits, or integration actions.

Inputs read through task-board resource get (all exit 0):
- TASK-261010-3pnf38_panel-verdict.md: changes_requested.
- TASK-261010-15htrb_panel-verdict.md: accept.
- TASK-260929-3ld28o_review-verdict-rev1.md: changes_requested.

## Merge refusal: exact corrections needed

1. The merged header labels panel B TASK-261010-15htrb as changes_requested; its actual Verdict section says accept. Correct that attribution. Panel A still requests changes, so the aggregate changes_requested direction remains justified.
2. Panel B F3 (severity note, row non-resets) is absent from the merged findings array. Its mechanism is copied into a note, but its invariant, reproduction test_file/command/expected_failure, severity and repeat-of fields are not retained as a finding. Restore the complete panel finding object; preserve its note severity. Invariant: Every non-state-changing item kind is ignored by the classifier (AC2). Reproduction: the proposed McpToolCall widening mutant and missing ignore-arm sweep in codex-rs/ext/goal/tests/state_change_observations.rs.
3. Panel B F4 (severity note, row code-mode leaf accounting) is likewise absent from the merged findings array; only its mechanism survives in a note. Restore its full object with invariant, reproduction and metadata. Invariant: AC8 killer attribution in the results file is accurate. Reproduction: compare tool_finish_success_records_mutation attribution in TASK-260929-3ld28o_results.md against TASK-260929-3ld28o_hosted-precheck-4.md.

Neither F3 nor F4 has identical row/file/class to another retained finding: F3 is the ignore-arm coverage note; F4 is the killer-attribution note. They must remain in the union under the supplied R132 rule. These are merge defects, not new product findings. Do not promote their severity or infer that panel B requested changes.

Preserved finding objects: A-F1, A-F2, A-F3, F1, F2 (5/7). All original field values and reproduction entries within these five are preserved, with added provenance. Note mechanisms retained for F3/F4: 2/2, but full finding objects retained: 0/2.

## Surface-row sweep in required order

| Row | Panel A | Panel B | Merged | Merge result |
|---|---|---|---|---|
| reset sources at committing handlers | broken | held | broken | worst result preserved |
| non-resets | broken | held | broken | worst result preserved |
| code-mode leaf accounting | broken | held | broken | worst result preserved |
| no model-writable bypass | held | held | held | preserved |
| existing activity and blocker untouched | held | held | held | preserved |
| transient state | held | held | held | preserved |
| API surface and placement | held | held | held | preserved |

Surface coverage: 7/7, exactly one merged result per row; 3 broken and 4 held. No implementation re-review was performed. After correction, the recording reviewer can verify the repaired union and call reject_cr with revision=1 and the corrected task-scoped merged verdict evidence.

## Verification and bounds

Python parsed the single verdict-findings JSON block in each artifact, compared finding fields/reproductions, verified identical seven-row ordering and worst-result selection: exit 0. This checks artifact structure and content only, not Rust behavior. No fresh CI or mutant execution is claimed; earlier panel evidence remains attributed to its source.

task-board spawn goal "$TASK_BOARD_RUN_ID": exit 0, run is not goal-bound. spawn directives: exit 0, none. Status analysis dry-run: exit 0. Initial status reviewing: exit 0. Two exploratory resource projections failed (exit 1, unsupported resources field); corrected via resource get, not treated as absence. Reference discovery included missing paths (exit 2); the authoritative merge rule is supplied in the task and merged verdict.

## Task-scoped logbook

2026-10-10: Recording-only audit found incorrect panel-B verdict provenance and loss of two structured note findings. Overall changes-requested direction is unchanged, but the explicit recording brief requires refusal of an incorrect merge. Persist this audit and route analysis for merge correction; no human-only decision is needed. Standalone logbook is unavailable (command -v logbook exit 1), so this logbook entry and board notes preserve the anomaly.
