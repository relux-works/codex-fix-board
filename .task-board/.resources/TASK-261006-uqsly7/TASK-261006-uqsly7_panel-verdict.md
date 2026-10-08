# Panel B — CR-TASK-260929-34a6ls-3 revision 3

accept

Replay tree check: **MATCH**. Base `4a27941d383ba8cdc2575bafdfeeef497b402a25` plus the attached rev3 patch, applied only through a fresh temporary index, yielded exactly `62aecbc1f279a26c154f0e371b8c1995bb7e8226`. No checkout switch, nested worktree, build, test execution, commit, or mutation on TASK-260929-34a6ls.

## Commands and actual exit codes

Run directly, standalone, without tee or status-hiding pipelines:

| Command | Exit | Result |
| --- | ---: | --- |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-uqsly7-replay-01.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Base loaded |
| `task-board resource get TASK-260929-34a6ls TASK-260929-34a6ls_change-request_rev3.patch --output .temp/TASK-260929-34a6ls_change-request_rev3.patch` | 0 | Patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-uqsly7-replay-01.idx" git apply --cached .temp/TASK-260929-34a6ls_change-request_rev3.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-uqsly7-replay-01.idx" git write-tree` | 0 | Expected candidate tree |
| `git diff --check 4a27941d383ba8cdc2575bafdfeeef497b402a25 62aecbc1f279a26c154f0e371b8c1995bb7e8226` | 0 | No whitespace errors |
| `python3 --version` | 0 | Python 3.14.7 readiness |

Administrative first status mutation exited 0 on the panel task. Surface-table, producer-brief, results and hosted-precheck-5 resource reads all succeeded (exit 0). Candidate `git show` and diff reads succeeded. Inspection/setup failures were not gates and are not counted as passing: initial skill search exit 2 (missing agents/skills and .claude/skills); initial board query exit 1 (unsupported resources projection, corrected); several optional role/tool path probes and zsh glob expansions missed paths (rg exit 2, ls exit 1, or shell no-match), corrected using concrete paths. The first replay setup was rejected before execution because it used rm -f; no gate ran there, and a fresh index name avoided deletion. One optional role-file search returned rg exit 1 (no matches). No build or test was run by this panel.

Artifact shape verification: standalone `python3` JSON/fence/row/verdict/size assertion script exited **0**, checking one valid block, exactly three unique expected rows, one-word accept and size below 32 KiB. Artifact creation script exited 0.

## Evidence and coverage

Sources are task resources, not independently rerun CI:
- `TASK-260929-34a6ls_hosted-precheck-5.md`: exact tree above; snapshot `df5eae26`, base run `37411010318`, core/app-server/lint/small reported success. Twelve mutant runs, twelve runtime kills, zero survivors. Some mutant lint lanes also failed; runtime killing tests are explicitly listed, so lint failure alone is not treated as a kill. The report does not give numeric hosted command exit codes; those are **unknown here**, not fabricated as 0.
- `TASK-260929-34a6ls_results.md`: AC/test map, retained-test list and stated bounds. Producer-reported local fmt/fix/clippy and targeted suite exit 0 are accepted as attached evidence, not rerun. The local validation log is capped at 64 KiB; this review relies on the exact-tree hosted report for execution.
- `surface-table.md`: three exact row names swept below. Scoped AC read supplies AC1–AC7. All seven ACs have named production-entry tests in the candidate; this does not certify every attack combination. Surface coverage is **3/3 rows**, with bounded attacks; narrowing mutants **12/12 killed** as reported.

Static attack sources (all paths at candidate tree `62aecbc1...`):
- `codex-rs/core/src/session/turn.rs:2669`: server acceptance hook uses that request's prompt, once, before downstream processing. `exec_completion_ack.rs:112` exhaustively excludes auxiliary/header events; SSE parser `codex-rs/codex-api/src/sse/responses.rs:404` distinguishes Created from failed-stream errors. The older outcome-success acknowledgment mechanism is structurally removed.
- `codex-rs/core/src/session/exec_completion_ack.rs:82`: exact trusted-render and user-role match. Matching only scans leases attached by the record path; forged text alone does not mint a lease. `hook_runtime.rs:786` scans the whole raw history for retry dedup. Unchanged request preparation clears ids/kinds, normalizes image details and sheds optional tool metadata, preserving the InputText checked by this matcher (`client.rs:895,1010,1751`; `client_tool_metadata.rs:12`). WebSocket continuation represents the logical request using previous response plus delta; it does not make an arbitrary prefix omission legitimate.
- `codex-rs/core/src/session/runtime_mailbox.rs:206`: stale tokens refused before counting, exhausting fail suspends, acknowledged entry removed. `tasks/mod.rs:563,641,737,1052` routes pending and recorded leases through fail cleanup before subsequent idle wakes.
- `codex-rs/core/tests/suite/exec_completion.rs:348–1335`: real session start/wake/interrupt tests; rejected submission and accepted-then-failed are separate shapes. No removed negative test or forged receipt authority was inferred from a helper-only positive assertion.

## Bounded free hunt and logbook-relevant observations

Inspected transport formatting, WS incremental continuation, header-versus-body acceptance, first-event cancellation ordering, pending-versus-recorded abort cleanup, failed-after-ack idempotence, resumed-history authority, context bounds and exposed test API. No reproduced blocking issue beyond the table. No CLI/config/app-server schema or rollout receipt persistence change is introduced. Existing fragments remain bounded in core/context (768 bytes each); the new tracker stores runtime leases, not a new model-visible fragment.

The first-event cancellation race is a suspicion needing a deterministic test, not a proven finding. Compaction omission and Windows latch coverage remain stated bounds, and the complete CR is above size guidance. These observations travel in this task-scoped outcome as the logbook record; the control-root logbook was not edited. Nothing was recorded on the reviewed task.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Tracked-then-removed-from-prompt compaction/guardian omission is not integration-attacked. The cap test attacks unleased remainder, and empty-prompt matcher unit coverage is narrower. This is a stated scope bound; request a guardian/compaction omission attack if that surface enters scope.",
    "The two POSIX tool latch integration tests skip on Windows; hosted green is not evidence that those attacks executed on Windows.",
    "Cancellation concurrently with receipt of the first acceptance event remains unmeasured: turn.rs checks cancellation after stream.next and before classification. Request a deterministic first-Created-versus-cancellation latch attack through the production streaming entry point. Existing cancellation test waits for tool start after acceptance; no failing reproduction was established here.",
    "The complete base-to-candidate diff is 1703 insertions and 27 deletions, above the review size guidance, mainly 1056 suite test lines. Revision-local size is not the complete CR size. A future split should isolate transport/latch test scaffolding before the behavioral hook where independently coherent; no functional failure follows from the line count alone."
  ],
  "surface_results": [
    {
      "row": "acknowledgment point",
      "result": "held",
      "detail": "Hosted precheck 5 on exact candidate: HTTP, WS, fallback, preacceptance failure/abort, accepted stream-error/EOF/cancel and budget tests. Killed ack_on_lease, ack_on_record, ack_after_tool_drain, ack_gated_on_outcome_success and ack_on_completed_instead_of_acceptance. Static hook precedes event processing and tool drain; header metadata excluded. Bounds in notes."
    },
    {
      "row": "membership authority",
      "result": "held",
      "detail": "Exact trusted lease render plus user role; no receipt parsing. Hosted forged integration and matcher refusal tests kill marker_substring_membership and role_blind_membership; batch_cap_doubled killed by capped remainder tests. Serialization preserves InputText; compaction omission bound in notes."
    },
    {
      "row": "failure, retry and suspension",
      "result": "held",
      "detail": "Hosted retry/abort tests assert one history append and request counts; fail-after-ack unit checks entry removal. Killed dedup_first_history_item_only, fail_after_ack_requeues, stale_fail_counts_attempt and suspend_threshold_doubled. Static cleanup covers recorded and pending leases; suspension warning and no-trigger state asserted."
    }
  ],
  "free_hunt": []
}
```
