# Merged review verdict — TASK-260929-csnn3a CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261006-t3wcgu_panel-verdict.md` (changes_requested), `TASK-261006-12rjcb_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

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
          "expected_failure": "Pause W after leasing and before attachment; replace its reservation and finish U through its idle scheduler; resume W. Assert autonomous sampling without another user turn. Candidate is predicted to retain an unleased entry with no sampling request. Then require a narrowing mutant of the idle-after-winner recovery to fail this test.",
          "pinned_blobs": [
            "git-blob:a4f2600724980b2d9896cbdf4ee7bcb3cef633c5",
            "git-blob:a67a7eaada7c5748f010d5feb235db7c668f962c"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261006-t3wcgu"
      ]
    }
  ],
  "notes": [
    "[TASK-261006-t3wcgu] Replay tree equals the expected candidate exactly; replay and diff-check command exits are 0.",
    "[TASK-261006-t3wcgu] Hosted precheck 2 is accepted attached execution evidence on the exact tree: baseline four lanes success, eight named mutant kills; raw hosted exit codes unknown. No local builds or tests.",
    "[TASK-261006-t3wcgu] Retain-only-task-present run ID conflicts between results and precheck table; use 37430576321 from precheck, reconcile 37430476321 in results.",
    "[TASK-261006-t3wcgu] Guardian preservation is supported with source citations; literal guardian omission is not executed, per the supplied table's stated bound.",
    "[TASK-261006-t3wcgu] F1b literal leftover-at-finish path remains an execution gap; its history-is-not-ack and two-lease retry behaviors are driven.",
    "[TASK-261006-t3wcgu] CR spans 15 files, +2504/-44 including inherited D1; preserve staged integration boundaries.",
    "[TASK-261006-t3wcgu] Only TASK-261006-t3wcgu receives board mutations and the verdict outcome.",
    "[TASK-261006-12rjcb] {'id': 'mid-start-claim-gap', 'severity': 'note', 'text': 'Unexecuted suspicion: tasks/mod.rs:364-390 releases active_turn after recording/draining, activates plugin selection, appends drained input to the old turn state, and awaits BeforeTaskRegistration lifecycle before checking the reservation again. A replacement during this interval can make the second check return false after session/lifecycle effects. Existing reserved_start tests replace/busy the reservation before start_task, so neither hosted claim mutant establishes this interval. Request a latch contributor at BeforeTaskRegistration, launch an exec wake through the real API, replace/interrupt while latched, then release and assert winner plugin state, balanced lifecycle callbacks, eventual mailbox sampling and no duplication. Suggested new core/tests/suite/exec_completion.rs test: exec_completion_reserved_start_replaced_between_claims; hosted command just test -p codex-core exec_completion_reserved_start_replaced_between_claims. Not run; no production finding inferred.'}",
    "[TASK-261006-12rjcb] {'id': 'mutant-final-newline', 'severity': 'note', 'text': 'Raw reserved_claim_ignores_task payload in TASK-260929-csnn3a_mutants.json has no final LF. On this host Git 2.54.0 git apply --cached --check exits 128, corrupt patch at line 11. Appending only LF in a scratch copy makes the same check exit 0. Raw applies are 7/8, normalized applies 8/8; apply checks do not execute mutants. Hosted precheck names a killing test and core failure for this mutant, but does not document its patch serialization. This portability defect is in auxiliary replay evidence; it does not contradict the hosted test verdict or alter CR candidate tree. Preserve final LF when materializing this mutant.'}",
    "[TASK-261006-12rjcb] {'id': 'hosted-run-id-correction', 'severity': 'note', 'text': 'Use precondition TASK-260929-csnn3a_hosted-precheck-2.md as authoritative: retain_only_task_present run is 37430576321; results.md section 1 incorrectly lists 37430476321. No source-task write was made.'}",
    "[TASK-261006-12rjcb] {'id': 'review-size', 'severity': 'note', 'text': 'Exact CR/base diff is 15 paths, +2504/-44, not the results leaf-relative 8 paths +801/-17. The CR includes D1 acknowledgment work and D2 race/test work. For upstream review, first land acknowledgment/tracking/retry changes and their integration tests, then TurnStartClaim and D2 regressions on that base. D2 alone is 818 changed lines by producer count; splitting claim fix and its tests from the remaining regression additions would reduce review size. No schema/config/CLI surface changes found.'}"
  ],
  "surface_results": [
    {
      "row": "F1a cleared reservation",
      "result": "broken",
      "evidence": "R141-A-1 static ordering. Hosted retain_only_task_present (37430576321), reserved_claim_ignores_identity (37430532942), reserved_claim_ignores_task (37430554179) kill their named tests but do not attack winner-idle-before-fail-back ordering.",
      "reported_by": "TASK-261006-t3wcgu"
    },
    {
      "row": "F1b finishing task",
      "result": "held",
      "evidence": "Hosted baseline plus acknowledge_on_recording (37430446385) and fail_first_tracked_only (37430491098) killed by exec_completion_finishing_task_gets_sampling_wake. hook_runtime.rs:786 notes recording; tasks/mod.rs:810 fails unsubmitted before scheduling. Bound: literal leftover-at-finish interleaving is not forced by this test.",
      "reported_by": "TASK-261006-t3wcgu"
    },
    {
      "row": "compaction, guardian and transport",
      "result": "held",
      "evidence": "Hosted compact_acks_staged (37430468861), guardian_prep_drops_exec_fragments (37430511988), ack_skipped_when_websockets_enabled (37430424561) killed by the corresponding public-entry tests. Kept persistent_failures_suspend_visibly_without_spin asserts three attempts, warning and no duplicate history; source confirms exact prompt membership and transport acceptance. Guardian result uses the source-cited preservation bound, not literal omission coverage.",
      "reported_by": "TASK-261006-t3wcgu"
    }
  ],
  "free_hunt": [
    "[TASK-261006-t3wcgu] {\"scope\": \"Trusted fragment membership, stale receipt tokens, API/config/rollout compatibility and diff size; read-only static attacks, no builds.\", \"result\": \"No additional concrete bypass or regression established within this bounded hunt.\", \"unexecuted\": \"Requested winner-idle-before-fail-back public-entry latch test; no new attack was executed locally.\"}"
  ]
}
```

## Recording confirmation

Both panel outcomes checked: 1/1 findings and 11/11 notes retained; 3/3 surface rows retained with worst-panel results. No new review or execution claim. repeat-of normalized from null to none. See TASK-260929-csnn3a_recording-confirmation-rev1.md.
