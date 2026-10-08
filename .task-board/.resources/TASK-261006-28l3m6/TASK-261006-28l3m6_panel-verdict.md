# TASK-261006-28l3m6 — DELTA panel verdict, CR-TASK-260929-34a6ls-3

accept

Replay: base `4a27941d383ba8cdc2575bafdfeeef497b402a25` plus the board rev3 patch, through a temporary index, produced exactly `62aecbc1f279a26c154f0e371b8c1995bb7e8226` (expected candidate). No nested worktree.

Commands actually run by this panel (exit codes):

- `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-28l3m6-replay.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25`: 0.
- `task-board resource get TASK-260929-34a6ls TASK-260929-34a6ls_change-request_rev3.patch --output .temp/TASK-260929-34a6ls_change-request_rev3.patch`: 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-28l3m6-replay.idx" git apply --cached .temp/TASK-260929-34a6ls_change-request_rev3.patch`: 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-28l3m6-replay.idx" git write-tree`: 0, exact tree above.
- `git diff --check 4a27941d383ba8cdc2575bafdfeeef497b402a25 62aecbc1f279a26c154f0e371b8c1995bb7e8226`: 0.
- `python3 .temp/TASK-261006-28l3m6/static_attack.py`: 0. Static assertions only: early guarded acknowledgment, exact user-role member filter, whole-history dedup, unknown/stale fail refusal, bounded attempt comparison and response.failed parsing. Script source below; no dynamic execution claimed.
- `gh run view 37411010318 --repo relux-works/codex --json headSha,conclusion,jobs,url`: 0. `gh run view 37411010318 --repo relux-works/codex --log`: 0. Core-specific `--job` log read: 0.
- `git rev-parse df5eae2617db54b79cf7e2856260ad9071115957^{tree}`: 0, candidate tree. `gh api repos/relux-works/codex/git/commits/df5eae2617db54b79cf7e2856260ad9071115957 --jq '{sha: .sha, tree: .tree.sha}'`: 0, same tree. Workflow dispatch API headSha is the workflow base; actual checkout and WANT_SHA in hosted logs are df5eae2617db54b79cf7e2856260ad9071115957. The checkout, not the API headSha proxy, establishes execution identity.
- `gh run view <ID> --repo relux-works/codex --log`: 0 for each of the 12 IDs listed in the hosted table below. All reads awaited. Hosted core commands themselves failed with exit 100, expected for mutants. Ancillary mutant lint exits: 1 for ack-after-tool-drain, outcome-success and completed-only; 101 for fail-after-ack. Behavioral kills do not rely on lint failures.
- Task-specific source/resource reads and source materialization: 0. Tool probes: task-board successful status read/write; git 2.54.0, rg 15.2.0, Python 3.14.7, gh 2.97.0. No installs.
- Failed discovery attempts (not evidence of absence): projections using `resources` and `attachments` exited 1; `schema(get)` returned a structured argument error with process exit 0; resolved with scoped schema and valid projections. Initial gh lookup against guessed `relux-works/relux-ci` exited 1 (404); short-SHA git-commit API lookup exited 1 (404), resolved using the actual repo and full SHA. A combined source search ended 2 because one guessed path did not exist; the located file was subsequently read. None is reported green.

- `python3 .temp/TASK-261006-28l3m6/validate_verdict.py`: 0; one JSON block, 3/3 unique rows, accept and string-array schema verified.

Reused execution, not rerun: [base hosted run](https://github.com/relux-works/codex/actions/runs/37411010318) checks out exact snapshot df5eae2617db54b79cf7e2856260ad9071115957. Core/app-server/lint/small all success. Core: 4989 passed, 11 skipped; all 16 exec_completion tests PASS. The 64-KiB CR validation log terminates with four green command shards, exit 0, but is truncated; no inference about missing steps. No cargo, just, builds or local Rust tests run by this panel.

| Narrowing attack | Hosted run | Core exit | Intended kill inspected |
|---|---:|---:|---|
| ack_after_tool_drain | 37411026391 | 100 | accepted failed/EOF/cancel, budget, blocked-tool |
| ack_gated_on_outcome_success | 37411043931 | 100 | accepted failed/EOF/cancel and budget |
| ack_on_completed_instead_of_acceptance | 37411060741 | 100 | accepted failed/EOF/cancel |
| ack_on_lease | 37411078103 | 100 | failed/aborted retry, suspension |
| ack_on_record | 37411093954 | 100 | failed/aborted retry, suspension |
| batch_cap_doubled | 37411110839 | 100 | nine-entry batch/remainder |
| dedup_first_history_item_only | 37411129134 | 100 | failed/aborted retry, suspension |
| fail_after_ack_requeues | 37411146346 | 100 | fail-after-ack and cancel units |
| marker_substring_membership | 37411163155 | 100 | forged handle/payload/text, cap/remainder |
| role_blind_membership | 37411178075 | 100 | non-user-role membership |
| stale_fail_counts_attempt | 37411192889 | 100 | stale-fail unit |
| suspend_threshold_doubled | 37411207981 | 100 | threshold/stale-fail units |

Review plan: decision is whether rev3 fixes all prior findings without a new regression; frozen precondition is the exact CR base/patch/tree; bounded static sweep of 3 rows plus adjacent acceptance/wire/abort/context paths; one text outcome, no archive or additional prerequisite. Consumer is the recording reviewer merging panel verdicts, not this non-recording panel. Sources: board surface-table.md, producer-brief.md, results.md, previous rev2 merged verdict, rev3 validation log, hosted-precheck-5.md, mutants.json; candidate files from git show at the exact tree; primary hosted raw logs. Read-only source task throughout.

Pinned key blobs: turn.rs `a7d838140904e8f11b6a01149ecafe8a60e8b4b7`; exec_completion_ack.rs `d8177695f1d3e83b373f619e1f25b66b799a0ab1`; integration suite `5d75e293045843a26fb097b37baf3665173b9daf`.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Previous rev2 merged evidence presents three entries for the same outcome-success mechanism: submission-ack-after-response, completed-budget-error-skips-ack, submission-ack-still-gated-by-response-outcome. All are fixed by the single acceptance hook at turn.rs:2677-2680. It runs before response dispatch, before Completed budget accounting at :2980-2993, and before tool draining. Four exact-tree hosted regression tests passed; outcome-success and completed-only narrowing mutants fail their intended cases.",
    "Executed coverage established from raw hosted logs: 3/3 supplied surface rows; 16/16 exec_completion integration tests PASS, 6/6 matcher/classifier unit tests PASS, fail-after-ack unit PASS. Base core summary: 4989 passed, 11 skipped; all four base jobs success. 12/12 attached narrowing mutants have intended behavioral failures in their core logs, each core command exit 100. These are expected-red attacks, not passing validation.",
    "AC1-AC2: HTTP, WS and HTTP fallback positive entry tests pass. Post-acceptance failed/EOF/cancel/budget regression fixtures are HTTP; no combined WS/fallback post-acceptance negative execution was established. Shared transport-agnostic production hook is statically verified. Request WS_created_then_stream_error_acknowledges and fallback_created_then_cancel_acknowledges if extending this bound.",
    "AC3-AC5: lease/record refusal mutants, retry history dedup, stale token, threshold and fail-after-ack attacks are executed. AC6: forged fragment public-entry test plus exact matcher negatives execute. AC7: batch-cap omission happens before leasing; tracked-then-removed final-prompt omission has 0 established public-entry tests and 0 ack-all-tracked mutants. Static member filtering holds. Request tracked_receipt_omitted_from_submitted_prompt_stays_pending plus acknowledge-all-tracked narrowing mutant; neither was run by this panel.",
    "Header metadata refusal has classifier unit coverage and static parser verification, but 0 established combined public-entry metadata-then-rejected fixtures and 0 metadata-counts-as-acceptance mutants. Request rejected_response_with_headers_retains_receipt with is_acceptance_event metadata narrowing if claiming that combined behavior.",
    "Two POSIX tool-latch cases skip Windows. Streaming cancellation uses build_with_streaming_server rather than build_with_auto_env; foreign-exec and Windows coverage for that test is unknown. No cross-platform execution inferred from Linux hosted results.",
    "Producer precheck table understates outcome-success mutant killing tests: raw log 37411043931 also fails completed_response_budget_exhaustion_acknowledges_receipt. ack_after_tool_drain log also kills the budget and blocked-tool tests. Marker-substring additionally fails cap/remainder entry cases. These strengthen kills; no surviving mutant is inferred. Mutant logs also contain unrelated failures; only intended failures are used as evidence.",
    "No source task mutation, accept/reject/status/handoff action, repository code edit, commit, build or local Rust test performed. CR validation log is exactly 65536 bytes and cannot attest omitted local steps. Its terminal summary reports required=4 green=4 and exit 0; producer local targeted 18/18 is reused as reported evidence, not independently rerun.",
    "RuntimeMailbox removal makes fail-after-ack a no-op, confirmed by its named hosted unit test and mutant. The public mailbox probe reports (false,false) for both acknowledged and suspended state; the post-acceptance tests pair it with request count/history checks. A single failed wake cannot reach the three-attempt suspension threshold, so that probe is not being used alone as proof of removal.",
    "Logbook entry (task-scoped resource, no control-root file edit): rev3 structural acceptance repair verified; previous budget/stream/cancellation defect no longer found; producer kill table omits additional real kills; tracked-omission and cross-platform bounds retained. No unresolved human decision or external blocker."
  ],
  "surface_results": [
    {
      "row": "acknowledgment point",
      "result": "held",
      "reason": "Server acceptance hook precedes fallible response processing; first created/output/completed event triggers exact member acknowledgment once. Metadata events are excluded. Reservation and record paths do not acknowledge. Previous round stream, cancellation, budget and tool-drain findings are fixed. Held within HTTP post-acceptance and shared-hook static bounds, not a universal transport attestation.",
      "evidence": [
        "candidate turn.rs:2677-2680,2980-2993",
        "candidate exec_completion_ack.rs:111-140",
        "base hosted 37411010318: all 16 exec_completion cases and classifier units PASS",
        "mutants 37411043931 and 37411060741: core exit 100, intended accepted-response failures",
        "mutants 37411026391,37411078103,37411093954: core exit 100",
        "python3 .temp/TASK-261006-28l3m6/static_attack.py exit 0"
      ]
    },
    {
      "row": "membership authority",
      "result": "held",
      "reason": "Lease ids and snapshots rerender exact InputText in the user role; only matched tracked leases are acknowledged and token checked. Forged/altered/role cases and capped later delivery hold. Tracked-but-removed final prompt has static filtering and an empty-input unit assertion only; no combined entry-point execution is claimed.",
      "evidence": [
        "candidate exec_completion_ack.rs:81-99,150-174",
        "candidate runtime_mailbox.rs:187-199",
        "base hosted 37411010318: forged/cap/remainder and matcher PASS",
        "mutants 37411163155,37411178075,37411110839: intended failures, core exit 100"
      ],
      "requested_attack": "tracked_receipt_omitted_from_submitted_prompt_stays_pending with acknowledge-all-tracked narrowing mutant; not run"
    },
    {
      "row": "failure, retry and suspension",
      "result": "held",
      "reason": "Unaccepted/aborted submissions fail current leases, whole-history retry dedup avoids another append, only matching current tokens count attempts, attempt three suspends and excludes wakes. Accepted leases are removed and cannot be requeued by later failure. Public tests assert warning and bounded request count; old taskless-warning reachability remains unproved.",
      "evidence": [
        "candidate hook_runtime.rs:786-802",
        "candidate runtime_mailbox.rs:209-235",
        "candidate tasks/mod.rs:568-598,641-660,739,1052",
        "base hosted 37411010318: retry/abort/suspension and fail-after-ack PASS",
        "mutants 37411129134,37411146346,37411192889,37411207981: intended failures, core exit 100"
      ]
    }
  ],
  "free_hunt": [
    "Acceptance synthesis: checked SSE response.failed as Err, response.created/output as ResponseEvent, header emissions before body, and exhaustive auxiliary-event exclusion. No acceptance-on-contact bypass found. Combined metadata-then-rejection test remains requested, not executed.",
    "Wire transformation: client.rs HTTP :1740-1775 and WS :1995-2048 may strip IDs/optional metadata or send an incremental suffix with a valid continuation. client_tool_metadata.rs bounds optional tool observations and preserves ordinary content. No concrete ordinary-fragment removal found. Cached continuation carries logical history; no false duplicate delivery inferred.",
    "Context and compatibility: existing ExecCompletionFragment is a ContextualUserFragment in core/context, bounded 768 bytes each and 8 per batch (6144 bytes). New tracking is internal turn extension state, not new model-visible text. Persisted rollouts omit lease metadata; resume silence test PASS. No app-server wire, CLI, config, dependency or schema delta. Added public hidden mailbox test probe is API-surface debt carried from prior round.",
    "Change size: cumulative 1703 additions + 27 deletions = 1730 changed lines, above 800 guidance; 1056 additions are integration tests. New production module is 252 lines. If splitting, mailbox-attempt accounting with its tests is the smallest independent stage, followed by acknowledgment wiring plus behavioral tests; size alone is not a behavioral defect.",
    "Abort handoff: pending and recorded leases are drained separately, stale fail is refused, post-ack failure cannot recreate an entry. No new concrete regression found. Taskless abort warning absence was already noted in rev2; public exhaustion reachability without a turn context remains unknown."
  ]
}
```

Static probe source (for replay):

```python
import subprocess
TREE = '62aecbc1f279a26c154f0e371b8c1995bb7e8226'
def source(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:codex-rs/{path}'], text=True)
turn = source('core/src/session/turn.rs')
ack = source('core/src/session/exec_completion_ack.rs')
mail = source('core/src/session/runtime_mailbox.rs')
hook = source('core/src/hook_runtime.rs')
sse = source('codex-api/src/sse/responses.rs')
start = turn.index('async fn try_run_sampling_request(')
body = turn[start:]
assert body.count('exec_completion_ack::acknowledge_submitted(') == 1
pos = body.index('exec_completion_ack::acknowledge_submitted(')
assert pos < body.index('match event {\n            ResponseEvent::Created')
assert pos < body.index('.record_token_usage_info(')
assert 'outcome.is_ok()' not in body
assert 'exec_completion_ack::is_acceptance_event(&event)' in body[:pos]
assert 'ServerModel(_)' in ack and 'ModelsEtag(_) => false' in ack
assert 'text == &expected' in ack and 'item_role == role' in ack
assert '.filter(|lease| items_contain_lease(prompt_input.iter(), lease))' in ack
assert 'history_items.iter().copied()' in hook
fail = mail[mail.index('pub(crate) fn fail('):mail.index('pub(crate) fn is_suspended(')]
assert fail.index('return false') < fail.index('entry.attempts =')
assert fail.index('entry.lease != Some(lease.token)') < fail.index('entry.attempts =')
assert 'entry.attempts >= MAX_RUNTIME_SAMPLING_ATTEMPTS;' in fail
assert '"response.failed" => {\n            return Err(' in sse
assert '.acknowledge_runtime_lease(' not in hook
print('PASS: pinned static acceptance placement, exact membership, history dedup, stale/unknown fail refusal, rejection parsing; no runtime execution claimed')
```
