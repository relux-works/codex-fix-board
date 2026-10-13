# TASK-260929-csyzcj — goal-owned-durable-sleep-lease: recording review revision 3

Decision: changes_requested. Record through reject_cr revision=3 with TASK-260929-csyzcj_review-verdict-rev3.md. No acceptance, producer handoff, commit acknowledgement or product-code changes.

Scope: recording-brief-rev3.md only. Read all three panel outcomes and the merged verdict. No new technical review or findings added. Candidate under review: 9ccda9214ac5b9f0ddb5533b77418d0f2045d74b.

Merge audit: 3/3 panels checked; 2/2 finding records preserved with their original fields and reproductions; 25/25 notes and 10/10 free-hunt entries retained. All 7/7 prescribed surface rows appear exactly once in the given order and match the worst panel result:

| Surface row | Merged result |
|---|---|
| registration and wake | held |
| eligibility and inspection errors | held |
| completion-before-registration race | held |
| foreign sleep ownership | held |
| marker lifecycle | held |
| side-effect silence | held |
| child state transitions | broken |

Panel decisions: TASK-261010-25dqo3 changes_requested; TASK-261010-1mz4id accept; TASK-261010-3o3vdy changes_requested. Both blocking records concern the remaining unbounded model-visible author/recipient envelope despite the bounded interruption body. Both P0 records, repeat-of metadata, requested repairs and evidence limits are retained verbatim. Their reports are the same mechanism; this recording run adds none.

Verification run here: in-memory Python resource/JSON comparison exit 0; all four resource-get subprocesses exit 0. Initial comparison exit 1 arose solely from an incorrect hard-coded expectation of 26 notes; actual panels contain 7+10+8=25, all preserved. Corrected comparator derives counts from the panel inputs. One exploratory query with unsupported resources field exited 1 and was repaired with outcomeResources; one optional reviewer-role reference search exited 2 for a missing skill-relative file, without affecting this audit. Merged verdict outcome readback is byte-identical after resource metadata update. No local files or temporary directories were created.

Bound: 7/7 surface rows checked for merge completeness is not 9/9 fully executed acceptance criteria. All panel limitations, source-only reproductions, unknown actual tokenizer/runtime long-path measurements, partial lifecycle/settings/resume coverage and reused hosted evidence remain explicit. No cargo/just/build/test, CI workflow, mutant or static source assay was rerun here. Hosted precheck 10 is panel-cited evidence, not independent execution by this recorder.

Lifecycle checks: set_status(reviewing) exit 0. spawn goal reports not goal-bound, exit 0; directives reports none, exit 0. Existing uncommitted producer changes are present; this run changes no repository source, tests, configuration, index, branch or commit.

Outcome-scoped logbook (2026-10-10): confirmed every panel finding and surface row survives the merge; rejection is required by two changes_requested panel verdicts. Retained the accepting panel's contrary body-only conclusion and all advisory notes without promoting them. Rework stays in the existing leaf; no external blocker or human approval is requested.

Recorded outcome: reject_cr(TASK-260929-csyzcj, revision=3, evidence=TASK-260929-csyzcj_review-verdict-rev3.md) exited 0. CR state changes_requested; task status to-dev; 2 finding records stamped; reviewer RUN-261010-3b1719; no loop signals. Evidence attached before turn end.
