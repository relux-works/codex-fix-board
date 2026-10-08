# R141 panel A — CR-TASK-260929-csnn3a-1 revision 1

changes_requested

Replay: base `4a27941d383ba8cdc2575bafdfeeef497b402a25` plus the attached revision-1 patch yields `3e3f73576ad3ed852711023df46ad5bd2dccda6c`, exactly the expected candidate tree. All source citations below refer to that tree, not this worktree's HEAD.

Commands personally run (real exit codes):

| Command | Exit | Evidence |
|---|---:|---|
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-t3wcgu-replay.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Base loaded into temporary index |
| `task-board resource get TASK-260929-csnn3a TASK-260929-csnn3a_change-request_rev1.patch --output .temp/TASK-260929-csnn3a_change-request_rev1.patch` | 0 | Revision-1 patch retrieved |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-t3wcgu-replay.idx" git apply --cached .temp/TASK-260929-csnn3a_change-request_rev1.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-t3wcgu-replay.idx" git write-tree` | 0 | Exact candidate tree above |
| `git diff --check 4a27941d383ba8cdc2575bafdfeeef497b402a25 3e3f73576ad3ed852711023df46ad5bd2dccda6c` | 0 | No whitespace errors; this is not a behavioral test |
| `git diff --stat` / `git diff --numstat` with those two OIDs | 0 | CR is 15 paths, +2504/-44; includes D1 and D2 |
| `task-board resource get TASK-260929-csnn3a <name> --output .temp/TASK-261006-t3wcgu/<name>` | 0 each | Six reads: surface-table.md, producer-brief.md, results.md, hosted-precheck-2.md, revision-1-validation.log, mutants.json (task-prefixed names as attached) |
| `task-board q 'get(TASK-260929-csnn3a) { description scope ac }'` | 0 | AC1–AC6 read without mutation |

No cargo, just, build, test or mutant command was executed by this panel. The proposed reproduction below is NOT executed evidence. Other read/setup diagnostics: unsupported query field `resources` returned 1; `schema(element)` returned 1; skill inventory with absent directories returned 2. A temporary-index cleanup command was rejected before execution (no process exit code); the unused index was loaded directly instead. These are tooling diagnostics, not passing gates.

## Sources and evidence boundary

Read-only board resources on TASK-260929-csnn3a: `surface-table.md`, `producer-brief.md`, `TASK-260929-csnn3a_results.md`, `TASK-260929-csnn3a_hosted-precheck-2.md`, `TASK-260929-csnn3a_mutants.json`, and `TASK-260929-csnn3a_change-request_rev1-validation.log`. Hosted precheck 2 binds snapshot `91c90e94`, run `37430403364`, to the replayed tree and reports small/core/lint/app-server success and 8/8 mutants killed. Those are reused execution results, not reruns. The attachment provides statuses and killing test names, not numeric hosted process exit codes; those exit codes remain unknown here. The truncated local log explicitly contains guard and fmt-check exit 0; its truncated clippy output is not independently a full passing log. Hosted lint is the cited replacement evidence.

The precheck table assigns retain-only-task-present to run `37430576321`; the results resource says `37430476321`. Use the precheck table's identifier pending coordinator reconciliation. This discrepancy does not erase the reported kill, but the latter identifier is not independently verified.

## Static attack: R141-A-1

`codex-rs/core/src/tasks/mod.rs:629–630`: back-off fails leases but never schedules pending work again. A concrete allowed ordering is:

1. Wake W reserves bare turn R, leases receipt L at lines 549–553, then waits in turn setup (lines 570–578), before attaching L to R at lines 605–612.
2. A user submission replaces R. The abort scans R's pending input, which contains no L yet. Replacement turn U runs and finishes while W is still paused.
3. U's finish scheduler (line 998) sees only the leased L. `RuntimeMailbox::has_pending` excludes leased entries (`session/runtime_mailbox.rs:141–145`), so the idle scheduler returns at `tasks/mod.rs:516–520`.
4. Resume W. It attaches to detached R, fails the reserved identity check, and calls `fail_leases(..., None, ...)`. L becomes unleased; W returns without another idle scheduling call.

The receipt is retained but no autonomous sampling request follows until unrelated later work arrives. `InputQueue::fail_runtime_lease` (`session/input_queue.rs:320–325`) sends a watch update; production subscribers are the running sleep/wait tools, not an idle scheduler. After U has finished there is no tool waiting to repair this. The producer's assertion that every interleaving converges via the winner's teardown scheduler is false for a winner that finishes before fail-back.

This is a static concurrency finding, not an observed executed failure. The hosted claim mutants prove refusal of wrong identity/task vacancy, but do not hold W between lease acquisition and attachment while U finishes. The compaction test stages an unleased notification behind a bare pin; it does not drive this taken-but-unattached race. Request a public-entry latch test named `exec_completion_lost_reservation_after_winner_idle_rewakes` that drives this ordering, asserts an autonomous sampling request without a new user turn, and kills a narrowing mutant that suppresses re-wake specifically when the winning turn already became idle. The repair must return leases and arrange a scheduler pass even when the winner already ran its last pass, while retaining identity/vacancy checks and retry bounds.

## Sweep and bounded free hunt

All 3/3 required surface rows have exactly one result below; 2 held within stated bounds, 1 broken by static attack. AC1's cleared-reservation mechanism and named mutant pass are reported, but its expanded lost-wake surface fails. AC2's history-is-not-ack behavior and two-lease fail-back are reported green; the literal pending-input-at-finish interleaving remains a disclosed execution gap rather than an impossibility established by this panel. AC3 compaction omission, AC4 bounded failure/suspension, AC5 transport submission acknowledgment, and AC6 dedup are supported by named hosted tests and source inspection. Guardian omission is a stated bound in the supplied surface table: request preparation only extends existing prompt input or errors (`guardian/request_budget.rs:67–185`); pending review finalization rejects non-single-UserInput (`guardian/input_budget.rs:81–98`); the guardian test drives preservation rather than omitted-then-later-sampled. This is not proof of the literal guardian-omission clause, and recording review must preserve that limitation.

Free hunt was bounded to trusted-lease membership/stale-token handling and integration/scope impact. Exact rendered-fragment equality and role checks avoid parsing forged marker text (`session/exec_completion_ack.rs:86–106`); token equality rejects stale fail/ack (`session/runtime_mailbox.rs:191–230`); transport acceptance is checked on the actual submitted prompt (`session/turn.rs:2676–2679`). No additional bypass was established. No wire API, CLI option, config type or rollout format changes were found in the diff. Model fragment definitions/caps are inherited, not enlarged here. The +2504/-44 CR combines stages and exceeds review-size guidance; D2 itself is reported +801/-17. Recommend retaining stage boundaries during integration; size is a note, not a second correctness finding.

## Logbook — panel-only record

2026-10-06: exact replay verified; hosted precheck reused, no builds. Newly identified R141-A-1: a taken-but-unattached lease can be returned after the winner's final scheduling pass, leaving pending work without an autonomous wake. Proposed deterministic attack remains unrun. No writes, verdict recording, accept/reject/status/handoff or notes were made on TASK-260929-csnn3a. This logbook entry travels only in this panel's task-scoped outcome; no control-root file was directly edited.

```verdict-findings
{
  "findings": [
    {
      "id": "R141-A-1",
      "row": "F1a cleared reservation",
      "invariant": "A reserved idle start backs off without losing its autonomous sampling wake when the reservation is replaced or busy.",
      "mechanism": "tasks/mod.rs:629-630 returns taken-but-unattached leases after back-off but schedules no wake. If the replacement task already finished and its scheduler skipped the still-leased entry, fail-back leaves the session idle with an unleased pending receipt and no future scheduler pass. Static ordering detailed above; not executed by this panel.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs (requested new test: exec_completion_lost_reservation_after_winner_idle_rewakes)",
          "command": "just test -p codex-core --test suite exec_completion_lost_reservation_after_winner_idle_rewakes (proposed; not run)",
          "expected_failure": "Pause W after leasing and before attachment; replace its reservation and finish U through its idle scheduler; resume W. Assert autonomous sampling without another user turn. Candidate is predicted to retain an unleased entry with no sampling request. Then require a narrowing mutant of the idle-after-winner recovery to fail this test."
        }
      ],
      "severity": "robustness",
      "repeat-of": null
    }
  ],
  "notes": [
    "Replay tree equals the expected candidate exactly; replay and diff-check command exits are 0.",
    "Hosted precheck 2 is accepted attached execution evidence on the exact tree: baseline four lanes success, eight named mutant kills; raw hosted exit codes unknown. No local builds or tests.",
    "Retain-only-task-present run ID conflicts between results and precheck table; use 37430576321 from precheck, reconcile 37430476321 in results.",
    "Guardian preservation is supported with source citations; literal guardian omission is not executed, per the supplied table's stated bound.",
    "F1b literal leftover-at-finish path remains an execution gap; its history-is-not-ack and two-lease retry behaviors are driven.",
    "CR spans 15 files, +2504/-44 including inherited D1; preserve staged integration boundaries.",
    "Only TASK-261006-t3wcgu receives board mutations and the verdict outcome."
  ],
  "surface_results": [
    {
      "row": "F1a cleared reservation",
      "result": "broken",
      "evidence": "R141-A-1 static ordering. Hosted retain_only_task_present (37430576321), reserved_claim_ignores_identity (37430532942), reserved_claim_ignores_task (37430554179) kill their named tests but do not attack winner-idle-before-fail-back ordering."
    },
    {
      "row": "F1b finishing task",
      "result": "held",
      "evidence": "Hosted baseline plus acknowledge_on_recording (37430446385) and fail_first_tracked_only (37430491098) killed by exec_completion_finishing_task_gets_sampling_wake. hook_runtime.rs:786 notes recording; tasks/mod.rs:810 fails unsubmitted before scheduling. Bound: literal leftover-at-finish interleaving is not forced by this test."
    },
    {
      "row": "compaction, guardian and transport",
      "result": "held",
      "evidence": "Hosted compact_acks_staged (37430468861), guardian_prep_drops_exec_fragments (37430511988), ack_skipped_when_websockets_enabled (37430424561) killed by the corresponding public-entry tests. Kept persistent_failures_suspend_visibly_without_spin asserts three attempts, warning and no duplicate history; source confirms exact prompt membership and transport acceptance. Guardian result uses the source-cited preservation bound, not literal omission coverage."
    }
  ],
  "free_hunt": {
    "scope": "Trusted fragment membership, stale receipt tokens, API/config/rollout compatibility and diff size; read-only static attacks, no builds.",
    "result": "No additional concrete bypass or regression established within this bounded hunt.",
    "unexecuted": "Requested winner-idle-before-fail-back public-entry latch test; no new attack was executed locally."
  }
}
```
