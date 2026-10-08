# TASK-261006-orddz2 panel A verdict — CR-TASK-260929-34a6ls-3

accept

Replay: base `4a27941d383ba8cdc2575bafdfeeef497b402a25` plus the attached revision-3 patch produced `62aecbc1f279a26c154f0e371b8c1995bb7e8226`, exactly the expected candidate tree. This pinned tree, rather than the Story checkout HEAD, is the review subject. No tracked checkout files changed and no source-task mutation was made.

Commands actually executed by this panel (standalone replay/gate processes; real exit codes):

| Command | Exit | Result |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261006-orddz2, status=analysis)'` | 0 | Own-task lifecycle only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-orddz2-replay.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Base loaded |
| `task-board resource get TASK-260929-34a6ls TASK-260929-34a6ls_change-request_rev3.patch --output .temp/TASK-260929-34a6ls_change-request_rev3.patch` | 0 | Patch read |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-orddz2-replay.idx" git apply --cached .temp/TASK-260929-34a6ls_change-request_rev3.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-orddz2-replay.idx" git write-tree` | 0 | Exact candidate match |
| `git diff --stat BASE CANDIDATE`, `git diff --numstat BASE CANDIDATE`, candidate `git show` reads | 0 | Static diff and candidate blobs read |
| `task-board resource get ... surface-table.md`, `... producer-brief.md` | 0 | Review inputs read |
| `task-board q 'get(TASK-260929-34a6ls) { description scope ac }'` | 0 | All seven AC read |
| `git status --porcelain` | 0 | No tracked changes |
| Python scratch JSON generation/append commands | 0 | Ordered row results persisted |
| Python verdict schema check (one fence, JSON object, exact row order/uniqueness, held statuses, empty findings/free hunt, verdict word) | 0 | Valid; 3/3 rows once |

Discovery errors (not validations and never counted as green gates): queries using `resources` and `artifacts` each exited 1 (unknown field); `schema(get)` returned an error object with process exit 0; `resource list` printed help, not a resource inventory. An exploratory `rg` and `sed` on the nonexistent `core/src/tool_metadata.rs` each failed with exit 2; the correct `client_tool_metadata.rs` was located and read from the candidate. No expected-red test was executed locally.

Sources and execution provenance:

- Board resource `TASK-260929-34a6ls_hosted-precheck-5.md`: tree exactly as replayed, snapshot `df5eae26`, base run `37411010318`; core/app-server/lint/small each reported success. This is attached execution evidence, not a local rerun or independently fetched provider log; it does not expose numeric process exits. Twelve mutant runs report intended test failures (12/12 killed); those are expected failures, not green mutant gates.
- Board resource `TASK-260929-34a6ls_results.md`: AC mapping, test names and inherited fast-lane commands (`just fmt`, `just fix -p codex-core`, `just clippy -p codex-core`, targeted suite), reported exit 0 on the identical tree. Local CR validation truncation is not used as proof of an unseen tail; exact-tree hosted lint/small evidence is the stated substitute.
- Board resources `surface-table.md`, `d1-rework-brief-rev3.md`, `TASK-260929-34a6ls_mutants.json`: invariants, previous repeat class and narrowing shapes. Mutants were inspected as evidence context, not run here.
- Candidate source: `core/src/session/turn.rs:2676` acceptance hook; `exec_completion_ack.rs:78-180` trusted render and event classification; `hook_runtime.rs:778-805` track/dedup without acknowledgment; `runtime_mailbox.rs:187-232` token-checked acknowledgment/failure; `tasks/mod.rs:560-660,735-739,1050` abort/terminal cleanup; `core/tests/suite/exec_completion.rs` public-entry attacks. Paths are relative to `codex-rs` in the pinned candidate.

Logbook entry (task-scoped, travels in this outcome; no control-root file edited): rev3 closes the previous success-outcome acknowledgment class at one event-loop hook. Post-acceptance stream/EOF/interrupt/budget failures cannot requeue an acknowledged mailbox entry. Remaining coverage and reviewability limits are listed below. Recommended panel decision: accept with the stated bounds; recording and integration remain the orchestrator/reviewer's responsibility.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Coverage: 7/7 AC rows name driving integration tests; 3/3 surface rows have hosted public-entry attacks. Held means those attacks survived, not exhaustive proof. Hosted evidence was reused; no cargo/just/build/test ran in this panel.",
    "Bound: omitted_receipt_sampled_by_later_request exercises an unleased batch remainder, not a tracked lease later removed by guardian/compaction. Matcher empty-input unit covers nonmembership only. Proposed additional attack: tracked_receipt_removed_from_assembled_prompt_retries_without_duplicate_history through the real guardian preparation boundary; guardian/compaction suite is explicitly outside this leaf scope.",
    "Bound: completed_response_with_blocked_tool_acknowledges_before_interrupt and accepted_response_cancelled_after_created_acknowledges_once skip Windows; latter uses build_with_streaming_server rather than auto-env. No cross-OS cancellation claim follows from these tests.",
    "Bound: role-blind, altered-payload and stale-token narrowing mutants have unit-level kills. Public-entry membership coverage is the forged-fragment test and batch omission; public-entry retry coverage is fail/abort/suspend. Do not relabel unit kills as public-entry executions.",
    "Size note: 1730 changed lines (1703 additions, 27 deletions), including 1289 test additions and 441 production changed lines. Exceeds the usual 800-line total guideline. Smallest coherent stage is the transport-agnostic acknowledgment/cleanup state machine plus HTTP failure/forgery/suspension integration attacks; WS/fallback and post-acceptance regression tests could be separately reviewed, but landing the state machine without the required transport/regression evidence would weaken this leaf. Treat test volume as a reviewability exception requiring recording-reviewer attention.",
    "Artifact anomaly: results says nothing material unverified, while its stated bounds admit tracked-removed omission and Windows skips. This panel retains those bounds and does not inherit that blanket claim.",
    "Free hunt (bounded static pass): traced client request normalization and WS continuation, abort cleanup ordering, model-context persistence, public API/config/rollout compatibility. Image normalization and optional tool-metadata shedding preserve fragment user text; WS continuation carries logical history through previous_response_id. No new fragment shape/config/API/CLI wire change; receipt metadata stays ephemeral, so resume replays data without rearming. The new doc-hidden public test probe expands the crate API; existing probes follow that pattern, but it is a maintainability note."
  ],
  "surface_results": [
    {
      "row": "acknowledgment point",
      "result": "held",
      "detail": "Exact-tree hosted precheck 5 run 37411010318; HTTP/WS/fallback and post-Created failure/EOF/interrupt/budget suite attacks pass. Mutants 37411043931, 37411060741, 37411026391, 37411078103, 37411093954 killed. Static hook turn.rs:2676 precedes fallible event handling."
    },
    {
      "row": "membership authority",
      "result": "held",
      "detail": "Exact-tree base run 37411010318: forged_fragment_text_acknowledges_nothing and omitted_receipt_sampled_by_later_request public-entry attacks pass; marker_substring_membership 37411163155 and batch_cap_doubled 37411110839 killed. role_blind_membership 37411178075 killed by matcher unit test. Static matcher compares exact user InputText against trusted lease rendering, never parses ids."
    },
    {
      "row": "failure, retry and suspension",
      "result": "held",
      "detail": "Exact-tree base run 37411010318: failed_submission_retries_once_without_second_history_append, aborted_submission_retries_and_samples_once and persistent_failures_suspend_visibly_without_spin pass through real turn entry points. dedup mutant 37411129134 killed by public-entry tests; stale-fail 37411192889 and threshold 37411207981 killed by mailbox units; fail-after-ack 37411146346 killed by intended unit despite collateral lint failure. Static stale-token check precedes counting and turn-end cleanup precedes idle wake."
    }
  ],
  "free_hunt": []
}
```
