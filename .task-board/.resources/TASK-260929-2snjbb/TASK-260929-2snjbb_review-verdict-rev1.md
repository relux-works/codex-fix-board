# Merged review verdict — TASK-260929-2snjbb CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261007-2w3nzy_panel-verdict.md` (changes_requested), `TASK-261007-2dp0i6_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "turn-start-resets-check-in-origin",
      "row": "check-in tickets and warning",
      "invariant": "AC4: check-ins at absolute 30, 60, 120 minutes from wait start, reassessed after each check-in.",
      "mechanism": "codex-rs/ext/goal/src/background_wait.rs:374-378 clears wait_started_at on every turn start; codex-rs/ext/goal/src/extension.rs:246 invokes it in production. evaluate_continuation:273-279 then inserts the new now and adds CHECK_IN_DELAYS[check_ins_used]. After first check-in at 30m, next idle at 31m gives deadline 91m instead of 60m. The hosted timing test omits note_turn_start between admissions.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-2w3nzy/static_attack.py (full source below)",
          "command": "python3 .temp/TASK-261007-2w3nzy/static_attack.py deadline",
          "expected_failure": "exit 1: absolute-deadline invariant violated by production turn-start hook; pinned-source trace, not Rust behavioral execution.",
          "pinned_blobs": [
            "git-blob:1b30543f5ed04b033d1e3ed1f9204712b26e78b4",
            "git-blob:c7dd35775084584a517125cf06eb7a7e6df3f8e2"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261007-2w3nzy"
      ]
    },
    {
      "id": "check-in-deadline-discarded",
      "row": "check-in tickets and warning",
      "invariant": "AC4 fallback check-ins actually fire; plan stage 2d includes scheduler foundation.",
      "mechanism": "codex-rs/ext/goal/src/runtime.rs:608-624 destructures next_check_in, logs it, drops the permit and returns. No registration, timer, or future continuation is scheduled from the deadline. With enabled policy and an unchanged Armed receipt, passage of time alone has no callback to reevaluate. The timing tests supply now and call evaluate_continuation manually. Activation remains intentionally deferred to stage 2e; that does not supply the missing stage-2d scheduler foundation.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-2w3nzy/static_attack.py (full source below)",
          "command": "python3 .temp/TASK-261007-2w3nzy/static_attack.py timer",
          "expected_failure": "exit 1: deadline is destructured, logged and discarded; no timer is armed. Static wiring reproduction only, not a live fake-clock test.",
          "pinned_blobs": [
            "git-blob:213f0af935347b2bfe9281265940c7b3e8fa670e"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261007-2w3nzy"
      ]
    },
    {
      "id": "checkin-epoch-reset-on-turn-start",
      "row": "check-in tickets and warning",
      "invariant": "AC4: check-ins at absolute 30, 60 and 120 minutes from the wait start; turn start invalidates tickets without renewing that human-input epoch.",
      "mechanism": "codex-rs/ext/goal/src/background_wait.rs:372 clears wait_started_at on every note_turn_start while retaining check_ins_used. The production hook at ext/goal/src/extension.rs:246 invokes it for the admitted check-in. evaluate_continuation at background_wait.rs:273-278 then adds the next absolute offset to a newly created epoch. With persistent pending work and effectively immediate check-in turns, the returned deadlines become 30/90/210 minutes rather than 30/60/120. The existing firing test never calls note_turn_start between check-ins.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/background_wait.rs (requested new test check_ins_keep_epoch_across_admitted_turns)",
          "command": "just test -p codex-goal-extension --test background_wait check_ins_keep_epoch_across_admitted_turns",
          "expected_failure": "NOT RUN: test does not yet exist and builds are forbidden. Start pending at minute 0; evaluate/admit at 30; invoke the real turn-start hook or note_turn_start, then evaluate pending again at 30 and 60. Assert next_check_in is minute 60 and second ticket is due at 60. Candidate returns deadline 90 and Wait at 60. Add narrowing mutant that resets the epoch only on goal-triggered turn start. Static source witness inspection ran, exit 0; this is not an executed Rust reproduction.",
          "pinned_blobs": [
            "git-blob:1b30543f5ed04b033d1e3ed1f9204712b26e78b4",
            "git-blob:c7dd35775084584a517125cf06eb7a7e6df3f8e2",
            "git-blob:0e78416e3af158256e7c028684dbf53b5418e767"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261007-2dp0i6"
      ]
    },
    {
      "id": "checkin-deadline-discarded",
      "row": "check-in tickets and warning",
      "invariant": "AC4-AC5: fallback check-ins actually fire and the warning follows the third check-in without requiring another human message or work event.",
      "mechanism": "codex-rs/ext/goal/src/runtime.rs:608-623 destructures next_check_in, logs it, drops the goal permit and returns. It registers no timer or wake. The candidate-wide reference sweep finds no production consumer of this deadline other than that log. GoalExtension::on_thread_idle at extension.rs:191-203 invokes continuation once; there is no goal-owned scheduled re-entry. A stalled Armed subscription with no subsequent events therefore never reaches the first fallback check-in or warning. Disabled-by-default activation is intentional; the missing scheduler foundation is separate from enabling it.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/background_wait.rs (requested runtime test stalled_subscription_fires_scheduled_checkins)",
          "command": "just test -p codex-goal-extension --test background_wait stalled_subscription_fires_scheduled_checkins",
          "expected_failure": "NOT RUN: test does not yet exist and builds are forbidden. Enable the preparatory policy through a runtime fixture; use the real idle contributor with a persistent Armed receipt and a paused clock, no more idle callbacks/messages/exits. Advance to 30/60/120 minutes and assert one real admitted check-in each, then exactly one warning while the goal stays active. Candidate schedules no callback and produces zero check-ins. A narrowing mutant scheduling only the first deadline must fail the later checks. Static candidate-wide caller inspection and Wait-arm witness ran, exit 0; no runtime test is claimed.",
          "pinned_blobs": [
            "git-blob:c7dd35775084584a517125cf06eb7a7e6df3f8e2",
            "git-blob:213f0af935347b2bfe9281265940c7b3e8fa670e",
            "git-blob:0e78416e3af158256e7c028684dbf53b5418e767"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261007-2dp0i6"
      ]
    }
  ],
  "notes": [
    "[TASK-261007-2w3nzy] {'id': 'post-recheck-race-unexecuted', 'text': 'core/src/session/turn_input.rs:459 checks once, before awaited settings preparation and start_task. Receipt transitions use their own store lock/revision. Existing latch-named test arms before handle(), not after the last check. A post-recheck transition looks unprotected; runtime reproduction unknown. Request a latch after check_goal_admission, arm a receipt, resume settings and assert no Started. Not promoted to a finding without execution.'}",
    "[TASK-261007-2w3nzy] {'id': 'release-hook-not-wired', 'text': 'git grep over exact candidate found note_release only as a definition and direct goal test calls; no production caller. Stage 2e adds release controls, so track this wiring there; no claim that release invalidation has already run through production.'}",
    "[TASK-261007-2w3nzy] {'id': 'coverage-bound', 'text': 'Hosted base and mutant evidence reused, not rerun. 3/3 rows have named executed attacks, 7/7 reported mutants killed. These ratios do not establish all production lifecycle compositions. 10/10 AC rows have named tests in the producer map; AC4 composition is contradicted by the static trace.'}",
    "[TASK-261007-2w3nzy] {'id': 'scope-size', 'text': 'Replay patch spans 26 files including prerequisite E1 snapshot code; producer E2 map reports 721 logic lines plus tests. Smallest rework is timer foundation and turn-start deadline preservation with composed tests; do not create a separate generalized research prerequisite.'}",
    "[TASK-261007-2dp0i6] {'id': 'execution-bound', 'text': 'This panel performed replay and static attacks only, as explicitly required. No cargo, just, build, Rust test, or new mutant was executed. New reproduction names are requested tests, not passing or failing executed tests. Existing hosted evidence is reused only for its named attacks.'}",
    "[TASK-261007-2dp0i6] {'id': 'snapshot-coherence-followup', 'text': 'Static free-hunt concern, not a reproduced blocking finding: core/src/session/pending_work.rs:51-64 copies the receipt lists and mailbox under separate locks, then samples the revision last. A receipt can become Armed after the list copy but before revision load, making old contents carry a newer revision. Also the admission recheck precedes async preparation and start_task. Request a barrier-based production test with a transition inside the snapshot read and another after the checker but before start_task. The existing goal_background_wait_revision_recheck_catches_transition performs sequential reserve/arm then handle, with an inline test-double checker; it is not a latch test of the real goal checker.'}",
    "[TASK-261007-2dp0i6] {'id': 'release-and-late-wake-bound', 'text': 'Candidate-wide note_release references are its definition and helper tests. Real subscription activation/control wiring belongs to stage 2e, so missing external activation alone is not a finding here. AC6/AC8 helpers prove empty-state reassessment, not a scheduled late completion/release wake. Preserve these limits in the coverage claim and add the real vertical tests in activation.'}",
    "[TASK-261007-2dp0i6] {'id': 'size-and-context', 'text': 'Combined base-to-candidate diff is 3041 insertions and 39 deletions across 26 files, including the already-checkpointed E1 work; producer describes only the E2 delta. No new model-visible fragment is injected (TurnInputContributor returns an empty vector). The new NotSubmittedReason is not serialized; inspected app-server match is exhaustive. No breaking wire/config/rollout change was established.'}"
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Exact-tree precheck 2 base run 37530053147; core public handle/start_if_idle tests goal_background_wait_blocks_goal_but_admits_user_and_followup and goal_background_wait_ignores_non_goal_triggers. Mutant overgate_non_goal_triggers run 37530108526 fails both; Armed run 37530082819 and read-error run 37530215463 also killed. Held only for these attacks.",
      "reported_by": "TASK-261007-2w3nzy"
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "turn-start-resets-check-in-origin",
        "check-in-deadline-discarded"
      ],
      "evidence": "Pinned-source probes both expected red exit 1. Hosted ticket/warning mutants 37530162208 and 37530240516 killed; manual state evaluations omit production turn start / timer callback.",
      "reported_by": "TASK-261007-2w3nzy"
    },
    {
      "row": "admission recheck and invalidation",
      "result": "held",
      "evidence": "Exact-tree base core tests revision_recheck_catches_transition and allows_when_empty_and_after_release; hosted skip_revision_recheck 37530189584 and preserve_ticket_across_invalidation 37530135461 killed. Bounds: post-check race and production release hook not executed, see notes.",
      "reported_by": "TASK-261007-2w3nzy"
    }
  ],
  "free_hunt": [
    "[TASK-261007-2w3nzy] {\"budget_minutes\": 5, \"result\": \"No additional reproduced blocking mechanism. Examined disable/resume, release callers, post-admission await window, wire enum addition and scope size; unresolved execution gaps remain notes.\"}",
    "[TASK-261007-2dp0i6] {\"budget_minutes\": 5, \"scope\": \"Snapshot coherence, post-check admission window, external API/context exposure, release callers, combined diff size. Static only; no new build or execution.\", \"blocking_findings\": [], \"notes\": [\"snapshot-coherence-followup\", \"release-and-late-wake-bound\", \"size-and-context\"]}"
  ]
}
```

## Recording reviewer confirmation — RUN-261006-7c6927

Read both complete panel outcome resources and compared their structured verdicts with this merged artifact. All 4/4 panel finding records (two mechanisms under panel-specific class names), 8/8 notes, and 3/3 surface rows are retained. Both panels report held / broken / held in the supplied row order; both request changes. The merge preserves each finding's invariant, mechanism, reproduction, severity, and repeat-of unchanged, with pinned blob metadata added. No panel finding or surface result was dropped. R132 preserves the distinct class names.

Recording scope only: no fresh code review, builds, tests, new findings, or repository changes. Existing panels' static-versus-behavioral execution bounds remain unchanged. The run is not goal-bound (`task-board spawn goal` returned Active Goal: none).

Logbook: recorded the existing changes_requested round for CR revision 1, candidate tree ffa1c230e68efdb2a7de81099ce670927c825c02. Rework is preserving the human-input check-in epoch across admitted turns and registering a real cancellable scheduled re-entry. This records revision 1 only, not any later candidate or the attached revision-2 producer brief.

Verification: Python structured merge comparison exited 0; both panel records' required fields and reproductions match the merged entries, all panel notes are retained, and both panels' three row results match. Task-board readiness and resource retrieval succeeded. An initial compact query used an unsupported resources field and failed; no absence was inferred.
