# R141 panel B — TASK-261006-793s3d

accept

Read-only, non-recording disposition of CR-TASK-260929-csnn3a-2 revision 2. No mutation, verdict recording, status change, or handoff was performed on TASK-260929-csnn3a. No repository code was changed, and no build or test was run locally.

Replay tree check: base `4a27941d383ba8cdc2575bafdfeeef497b402a25` plus the attached rev2 patch produces exactly `f0cf63cd9fc511340d23e680f43e846403157f62`. `git write-tree` exited 0 and printed that tree. Candidate reads below use that tree, not the worktree contents. Worktree HEAD is the replay base; `git rev-list --count HEAD..main` returned 0 (exit 0), with no inference that local main represents current remote trunk.

## Executed commands and exit codes

All replay and validation commands ran as standalone subprocesses, without tee or a pipeline hiding their exit status. Scratch material is under `.temp/TASK-261006-793s3d/`; the temporary index is `.temp/TASK-261006-793s3d-replay.idx`.

| Command | Exit | Result |
|---|---:|---|
| `task-board m 'set_status(TASK-261006-793s3d, status=analysis)'` | 0 | Panel lifecycle only |
| `git --version` / `python3 --version` | 0 / 0 | Git 2.54.0; Python 3.14.7 readiness |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-793s3d-replay.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Base index loaded |
| `task-board resource get TASK-260929-csnn3a TASK-260929-csnn3a_change-request_rev2.patch --output .temp/TASK-260929-csnn3a_change-request_rev2.patch` | 0 | Canonical input patch |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-793s3d-replay.idx" git apply --cached .temp/TASK-260929-csnn3a_change-request_rev2.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-793s3d-replay.idx" git write-tree` | 0 | Exact expected candidate tree |
| `git diff --check 4a27941d383ba8cdc2575bafdfeeef497b402a25 f0cf63cd9fc511340d23e680f43e846403157f62` | 0 | Whitespace check |
| `task-board resource get TASK-260929-csnn3a <resource> --output .temp/TASK-261006-793s3d/<local-name>` | 0 each | surface-table.md, results.md, hosted.md, producer.md, validation.log, mutants.json (canonical names in Sources below) |
| `git show f0cf63cd9fc511340d23e680f43e846403157f62:<path>`; candidate/base diff, diff-stat, diff-numstat, name-only reads | 0 each | Static candidate inspection |
| `task-board q 'get(TASK-260929-csnn3a) { description scope ac }'` and corrected resources/notes projection | 0 each | AC and attached evidence reads |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives; run not goal-bound |
| `git status --short` | 0 | No tracked/untracked repository delta |

Each of the following was independently run as `git apply --cached --check .temp/TASK-261006-793s3d/<name>.patch` with GIT_INDEX_FILE pointing to the replayed candidate index. Python subprocess.run captured the real exit code; the driver also exited 0. These are applicability checks, NOT locally executed mutant tests.

| Mutant name | Apply-check exit |
|---|---:|
| retain_only_task_present | 0 |
| acknowledge_on_recording | 0 |
| fail_first_tracked_only | 0 |
| ack_skipped_when_websockets_enabled | 0 |
| compact_acks_staged | 0 |
| guardian_prep_drops_exec_fragments | 0 |
| reserved_claim_ignores_identity | 0 |
| reserved_claim_ignores_task | 0 |
| backoff_skips_post_failback_rewake | 0 |

Operational failures are not passing gates: initial combined skill search exited 2 because some directories were absent; two queries using unknown `resources`/`attachments` fields exited 1 and were replaced by valid `preconditionResources outcomeResources` projections after schema inspection; a zsh unmatched skill glob exited 1. The initial read-tree invocation containing `rm -f` was rejected before launch by tool approval review, so has no process exit code; the index was absent and the standalone read-tree above succeeded without deletion. Reading a nonexistent reviewer-role path failed (cat exit 1; its combined shell command ended 0); the actual role file was subsequently read successfully from `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md`. None is execution evidence for a product gate.

Artifact validation: Python JSON/fence/row/verdict assertions exited 0; exactly one object, three unique required rows, no blocking findings, and no repository delta.

## Evidence and surface sweep

Attached hosted precheck 3 binds snapshot `53c4e843`, run `37441567186`, to the exact replay tree. Baseline small/core/app-server/lint lanes are recorded as success. Nine of nine mutant runs are recorded as killed, zero survivors. These executions are reused evidence, not rerun by this panel. The summary supplies lane outcomes and named failing tests, not numerical hosted subprocess exit codes; those numerical codes are unknown here. The bounded local CR validation log ends during compilation and cannot establish the last command passed. Its target-guard and fmt-check exits 0 are visible; lint/test conclusions come from hosted precheck 3 instead.

Coverage: 3/3 surface rows attacked with hosted public-entry evidence; 6/6 AC rows have named tests, with the AC3 guardian clause classified under the explicitly permitted preservation bound. Held means the named attacks did not reproduce on the baseline, not proof of absence.

1. **F1a cleared reservation — held.** `core/tests/suite/exec_completion.rs:1380` exercises public inject and Plan-mode refusal, then retained receipt recovery. The rev2 test at :1518 gates a wake after leasing, lets the winner finish with the receipt still leased, releases the failed reserved start, and asserts exactly two requests and one history fragment. Production `tasks/mod.rs:293-300` checks both reservation identity and vacancy; :342 and the second claim guard prevent starting on a replacement turn. :642-652 fails leases back and schedules again. If the winner remains active the pass returns; if already idle, it reserves and re-leases. Stale fail-back is a no-op; suspended entries are excluded. Hosted runs 37441786360 and 37441638357 kill the bare-input narrowing and omitted post-failback wake. The two claim mutants are unit-entry attacks, not claimed as public-entry coverage. R141-A-1's named lost-wake mechanism is addressed.

2. **F1b finishing task — held.** Suite :1613 stages two receipts, observes a rejected wake request, then two fragments in the retry with exactly two history entries. `hook_runtime.rs:779-805` tracks before recording and deduplicates recorded fragments; `exec_completion_ack.rs:188-232` returns every unsampled lease. `tasks/mod.rs` teardown records pending input before failing the tracked remainder and scheduling. Hosted acknowledge-on-recording and first-only-fail-back runs (37441615109, 37441688497) kill premature acknowledgment and partial recovery.

3. **Compaction, guardian and transport — held.** Suite :1793 pins a staged receipt across a real Compact submission and proves absence in the summarization request, followed by exactly one fragment in the wake. Suite :1902 drives guardian prompt preparation and asserts preserved sampling. `guardian/request_budget.rs:67-184` adds restored evidence rather than filtering existing input; `guardian/input_budget.rs:81-98` refuses non-UserInput pending review composition, and `guardian/review_session.rs:677-742` scopes that context to the reviewer session. This supports the stated preservation bound; it does not execute guardian omission. Suite :1691 asserts an actual WS handshake and HTTP fallback, failure then accepted resubmission, and one history fragment. `session/turn.rs:2669-2679` acknowledges exact submitted members only on acceptance events; `exec_completion_ack.rs:96-136` excludes auxiliary metadata; mailbox stale tokens cannot requeue acknowledged receipts. Kept suite :708 asserts three failed sampling attempts, visible warning, four total requests including the initial turn, and no continued wake. Hosted compact/guardian/WS-config mutants (37441663087, 37441714373, 37441591474) fail at the named tests.

## Bounded free hunt and scope

After the sweep, static attacks considered re-wake recursion with an active winner versus suspended receipts; stale lease fail-back after acknowledgment; fixture gates accidentally affecting normal execution; forged/resumed history causing acknowledgment without tracked leases; acknowledgment on header metadata rather than response acceptance; and external CLI/config/API changes. The reserved re-wake requires pending non-suspended work, an idle active-turn slot, and a valid claim. Acknowledgment needs trusted tracked leases, exact fragment membership and an acceptance event. New test gate hooks have no effect without an inserted gate. No additional reproduced defect was established. No new external wire/config surface or dependency change appears in the patch. No build, local product test, browser access, or hosted-run rerun was performed.

Plan: unblock the rev2 disposition, frozen input is the supplied base/patch/tree; budget is one bounded inline static sweep plus a short free hunt, one text outcome, zero serial prerequisite tasks. Consuming action is the orchestrator's merged verdict and recording review. Exit criteria are exact replay, one result per surface row, and a valid verdict artifact.

## Logbook handoff

2026-10-06: R141 panel B verified exact rev2 replay and independently checked all nine mutant patches apply to it. R141-A-1 recovery is covered by the focused regression plus hosted narrowing-mutant kill. Preserve the guardian evidence bound and the cumulative-diff size note when merging panel verdicts. No target-task writes were made. This task-scoped entry travels in the outcome; no control-root LOGBOOK.md was edited.

## Sources

All code citations above refer to tree `f0cf63cd9fc511340d23e680f43e846403157f62` and paths under `codex-rs/`. Evidence is sourced from TASK-260929-csnn3a resources: `surface-table.md`, `producer-brief.md`, `TASK-260929-csnn3a_results.md`, `TASK-260929-csnn3a_hosted-precheck-3.md`, `TASK-260929-csnn3a_mutants.json`, `TASK-260929-csnn3a_change-request_rev2-validation.log`, and `TASK-260929-csnn3a_change-request_rev2.patch`. Findings are verified against those artifacts and candidate source, without claiming a separate remote-provider audit. The review-round and verdict-format contracts were read from project-management's reviewer role and references/file-formats.md; repository testing/context/breaking-change/size skills were read and applied within this read-only scope.

```verdict-findings
{
  "findings": [],
  "notes": [
    "AC3 guardian coverage is preservation plus the stated bound, not an omission-then-later-sampling execution. prepare_prompt only extends existing input; finalize requires a single UserInput when PendingReviewContext exists; review context is installed and cleared on the separate review session. Do not generalize this evidence to guardian/parent overlap races (outside this leaf).",
    "F1a settings-failure, bare injection and retained-mail recovery are tested in separate phases. Recovery in the original F1a test follows a user turn; it does not prove that clearing every bare reservation itself immediately starts a wake. The new rev2 test does prove automatic recovery for the lost reserved wake after a winner has already gone idle.",
    "Change-size bound: the supplied CR is cumulative (2727 additions/44 deletions from its replay base); D2 reports 1024 additions/17 deletions over its intra-story base. The focused rev2 delta is 223 additions in four files. Preserve the focused rework as a reviewable stage; this verdict is not a waiver for a future oversized upstream PR.",
    "New public doc-hidden test hooks and TestWakeLeaseGate increase the crate API. No blocking API break reproduced; their production paths are inert unless explicitly armed. Keeping test API growth contained is advisable."
  ],
  "surface_results": [
    {
      "row": "F1a cleared reservation",
      "result": "held",
      "detail": "Hosted public-entry F1a and lost-reservation-after-winner-idle tests pass on f0cf63cd; retain_only_task_present (37441786360) and post-failback-rewake (37441638357) mutants fail. Identity/vacancy unit mutants also fail (37441739252, 37441762646). Static replay traces both claim points and the post-failback scheduling pass."
    },
    {
      "row": "F1b finishing task",
      "result": "held",
      "detail": "Hosted public-entry exec_completion_finishing_task_gets_sampling_wake passes; acknowledge_on_recording (37441615109) and fail_first_tracked_only (37441688497) fail. Two receipts are resubmitted and history contains two fragments, not four."
    },
    {
      "row": "compaction, guardian and transport",
      "result": "held",
      "detail": "Hosted public-entry compaction, guardian preservation and sampling_ack tests pass. compact_acks_staged (37441663087), guardian_prep_drops_exec_fragments (37441714373), ack_skipped_when_websockets_enabled (37441591474) fail. Kept persistent-failure and HTTP/WS tests cover bounded retries, visible suspension and submitting-transport acknowledgment; guardian omission is a stated structural bound, not an executed omission test."
    }
  ],
  "free_hunt": []
}
```
