# TASK-261006-12rjcb panel B verdict — CR-TASK-260929-csnn3a-1 rev1

accept

Replay: base `4a27941d383ba8cdc2575bafdfeeef497b402a25` plus the attached CR patch gives `3e3f73576ad3ed852711023df46ad5bd2dccda6c`, exactly the expected candidate tree. Rechecked after read-only mutant applicability checks: unchanged. No nested worktree, build, test, commit, branch operation, or mutation on TASK-260929-csnn3a was performed.

This is a non-recording panel recommendation, ready for recording-reviewer consideration. All 3/3 surface rows have exactly one result; `held` means the named attacks held, not proof of absence. No blocking finding reproduced. Unexecuted race suspicion is a note under the reviewer contract.

## Scope and bounded plan

Decision: whether this exact CR is acceptable to the recording reviewer. Frozen precondition: CR rev1/base/tree above; no grammar work. Budget: one static sweep plus a five-minute free hunt, maximum 30 minutes including packaging, one text outcome, zero archives, zero serial prerequisites. Exit: replay matches, all three rows classified, one valid verdict JSON, attached handoff. Consuming slice: recording review of this CR; no additional implementation/research leaf created. Research/reviewer contracts applied inline; PR orchestrator skill is inapplicable to this panel.

## Commands and exit codes

Commands below are validation actually executed here, individually via direct processes; subprocess applicability checks preserve each real exit. No pipes hide validation status.

| Command | Exit | Result |
|---|---:|---|
| `task-board m 'set_status(TASK-261006-12rjcb, status=analysis)'` | 0 | panel lifecycle only |
| `task-board resource get TASK-260929-csnn3a TASK-260929-csnn3a_change-request_rev1.patch --output .temp/TASK-260929-csnn3a_change-request_rev1.patch` | 0 | patch read |
| `GIT_INDEX_FILE=$PWD/.temp/TASK-261006-12rjcb-replay.idx git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | isolated index |
| `GIT_INDEX_FILE=$PWD/.temp/TASK-261006-12rjcb-replay.idx git apply --cached .temp/TASK-260929-csnn3a_change-request_rev1.patch` | 0 | replay |
| `GIT_INDEX_FILE=$PWD/.temp/TASK-261006-12rjcb-replay.idx git write-tree` (initial and closing) | 0 / 0 | expected tree both times |
| `git diff --check BASE TREE` (exact OIDs above) | 0 | no whitespace errors |
| `git apply --cached --check .temp/TASK-261006-12rjcb/<mutant>.patch` with replay index: retain_only_task_present, acknowledge_on_recording, fail_first_tracked_only, ack_skipped_when_websockets_enabled, compact_acks_staged, guardian_prep_drops_exec_fragments, reserved_claim_ignores_identity | 0 each | 7/8 raw mutant patches apply |
| Same check: reserved_claim_ignores_task.patch | 128 | corrupt patch, line 11; missing terminal LF |
| Applicability harness aggregate assertion | 1 | truthfully red because raw check failed |
| Same check: reserved_claim_ignores_task-newline.patch (only added terminal LF) | 0 | normalized replay applies |
| `python3 --version` and JSON shape inspection | 0 each | Python readiness / input parse |

Read-only board downloads for hosted precheck, validation log, and mutant JSON each exited 0. Static `git show`, `git diff --stat`, source/resource reads and task-specific board projections succeeded. Orientation invocations: initial combined skill-path discovery exited 2 because some searched directories are absent; a role-path probe exited 1 because `agents/reviewer.md` does not exist (correct `.roles/reviewer/role.md` then read); early combined projections printed `unknown field resources`, then were replaced with successful `outcomeResources/preconditionResources` projections. No absence inferred from these failed reads. Spawn directives check exited 0: none recorded. These orientation failures are not passing gates.

## Reused execution evidence and sources

Primary board sources (read-only): `surface-table.md`, task AC projection, `producer-brief.md`, `TASK-260929-csnn3a_results.md`, `TASK-260929-csnn3a_mutants.json`, `TASK-260929-csnn3a_hosted-precheck-2.md`, and `TASK-260929-csnn3a_change-request_rev1-validation.log`, all on TASK-260929-csnn3a. Code citations below refer to the exact candidate tree, read with `git show TREE:path`, never assumed from this worktree HEAD.

Hosted precheck binds tree to snapshot `91c90e94`: run `37430403364` reports small/core/lint/app-server `success`; eight narrowing mutants report core failures and named killing tests, zero survivors. This panel accepts those attached results as executed evidence under panel-brief; it did not independently run tests or fetch remote logs. Hosted process exit codes are not given in the precheck summary, so are unknown here; job conclusions are not substituted for numeric exits. Precheck-1 results are explicitly void. The local CR log is bounded/truncated, so only visible guard/fmt exits 0 are usable from it; later command success is established by attached hosted evidence, not inferred from truncation. No full workspace suite was run or claimed.

Production wiring checked: `hook_runtime.rs:779-803` tracks before record and deduplicates against history; `exec_completion_ack.rs:146-191` checks submitted prompt membership and removes acknowledged members; `turn.rs:2669-2680` calls this only at acceptance events; `tasks/mod.rs:781-811` records teardown input then fails unsubmitted entries before wake. RuntimeMailbox failure counts are bounded at three. New model context is rendered through the existing ExecCompletionFragment; no new fragment type or larger bound introduced. Resume persists fragments without runtime receipt metadata. No changed app-server API, raw response event, CLI flag, config type, or rollout wire shape was found in the 15 changed paths.

## Free hunt and logbook

Bounded free hunt inspected post-claim async effects, stale lease failure/ack ordering, exact membership and resume behavior, source compatibility, raw mutant applicability, and CR size. No additional reproduced production defect; `free_hunt` is empty. Suspicions and evidence anomalies are in `notes`, never counted as blocking findings.

Task-scoped logbook entry, carried in this outcome (control root not edited): 2026-10-06 — exact replay held; raw mutant 7/8 applies versus 8/8 after final-LF normalization; producer results cite wrong retain-only run ID; mid-start reservation interval needs a public-entry latch attack before claiming full race coverage. Recording reviewer receives these bounds together with the accept recommendation.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "mid-start-claim-gap",
      "severity": "note",
      "text": "Unexecuted suspicion: tasks/mod.rs:364-390 releases active_turn after recording/draining, activates plugin selection, appends drained input to the old turn state, and awaits BeforeTaskRegistration lifecycle before checking the reservation again. A replacement during this interval can make the second check return false after session/lifecycle effects. Existing reserved_start tests replace/busy the reservation before start_task, so neither hosted claim mutant establishes this interval. Request a latch contributor at BeforeTaskRegistration, launch an exec wake through the real API, replace/interrupt while latched, then release and assert winner plugin state, balanced lifecycle callbacks, eventual mailbox sampling and no duplication. Suggested new core/tests/suite/exec_completion.rs test: exec_completion_reserved_start_replaced_between_claims; hosted command just test -p codex-core exec_completion_reserved_start_replaced_between_claims. Not run; no production finding inferred."
    },
    {
      "id": "mutant-final-newline",
      "severity": "note",
      "text": "Raw reserved_claim_ignores_task payload in TASK-260929-csnn3a_mutants.json has no final LF. On this host Git 2.54.0 git apply --cached --check exits 128, corrupt patch at line 11. Appending only LF in a scratch copy makes the same check exit 0. Raw applies are 7/8, normalized applies 8/8; apply checks do not execute mutants. Hosted precheck names a killing test and core failure for this mutant, but does not document its patch serialization. This portability defect is in auxiliary replay evidence; it does not contradict the hosted test verdict or alter CR candidate tree. Preserve final LF when materializing this mutant."
    },
    {
      "id": "hosted-run-id-correction",
      "severity": "note",
      "text": "Use precondition TASK-260929-csnn3a_hosted-precheck-2.md as authoritative: retain_only_task_present run is 37430576321; results.md section 1 incorrectly lists 37430476321. No source-task write was made."
    },
    {
      "id": "review-size",
      "severity": "note",
      "text": "Exact CR/base diff is 15 paths, +2504/-44, not the results leaf-relative 8 paths +801/-17. The CR includes D1 acknowledgment work and D2 race/test work. For upstream review, first land acknowledgment/tracking/retry changes and their integration tests, then TurnStartClaim and D2 regressions on that base. D2 alone is 818 changed lines by producer count; splitting claim fix and its tests from the remaining regression additions would reduce review size. No schema/config/CLI surface changes found."
    }
  ],
  "surface_results": [
    {
      "row": "F1a cleared reservation",
      "result": "held",
      "attacks": [
        "exec_completion_survives_cleared_idle_reservation (core/tests/suite/exec_completion.rs:1380); retained runtime mail survives the bare drop, two requests, one history fragment",
        "retain_only_task_present hosted run 37430576321 killed the F1a test",
        "reserved_claim_ignores_identity run 37430532942 and reserved_claim_ignores_task run 37430554179 killed named reserved_start tests"
      ],
      "bound": "The public-entry F1a attack ran on the exact candidate per hosted attachment. Reservation helper, actual Plan refusal, and mailbox retention are separate test phases. Replacement/busy attacks are unit tests against start_task, not public-entry races between the two claim points. Held only for these attacks."
    },
    {
      "row": "F1b finishing task",
      "result": "held",
      "attacks": [
        "exec_completion_finishing_task_gets_sampling_wake (core/tests/suite/exec_completion.rs:1518): two tracked leases, rejected request then sampling retry, three requests and two history fragments",
        "acknowledge_on_recording run 37430446385 and fail_first_tracked_only run 37430491098 killed that public-entry test"
      ],
      "bound": "Test drives normal record/failure/finish/re-wake, not a lease left in pending_input until teardown. Static teardown at tasks/mod.rs:781-811 takes pending input, records it, and fails unsubmitted leases before scheduler wake."
    },
    {
      "row": "compaction, guardian and transport",
      "result": "held",
      "attacks": [
        "exec_completion_compaction_omission_keeps_receipt_pending (:1698), compact_acks_staged killed in 37430468861",
        "exec_completion_guardian_prompt_preserves_receipt (:1807), guardian_prep_drops_exec_fragments killed in 37430511988",
        "exec_completion_sampling_ack (:1596), ack_skipped_when_websockets_enabled killed in 37430424561 (also HTTP/WS tests)",
        "persistent_failures_suspend_visibly_without_spin (:708) present in exact-tree core suite: warning, four total requests and one history fragment"
      ],
      "bound": "Guardian preservation is the stated-bound alternative expressly allowed by surface-table, not an executed omission/recovery test. request_budget.rs:67-185 only extends existing prompt.input or errors; input_budget.rs:81-98 rejects pending-review input other than one UserInput. Local summarization is exercised; remote compaction is statically inspected only. Hosted lane/test results reused; no local test execution."
    }
  ],
  "free_hunt": []
}
```
