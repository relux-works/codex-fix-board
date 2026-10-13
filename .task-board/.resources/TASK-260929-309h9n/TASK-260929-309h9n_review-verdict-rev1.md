# Merged review verdict — TASK-260929-309h9n CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261011-3cyko9_panel-verdict.md` (changes_requested), `TASK-261011-3w3wcg_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A-F1",
      "row": "blocker order and waiting turns",
      "invariant": "AC5/AC8: preserve the three-fully-empty-continuations blocker FIRST and provide a narrowing mutant with a named direct killer for that ordering.",
      "mechanism": "The supplied pacing_blocker_order_swapped patch deletes the InactiveOrBudgetLimited branch from BackgroundWaitState::evaluate_locked (background_wait.rs:330-336). It never moves or narrows the empty-response blocker in GoalExtension::on_turn_stop (extension.rs:380-387) or its ordering relative to note_turn_completed (extension.rs:419-429). Hosted mutant-1 small fails only pacing_inactive_goal_never_paced, whose input is an inactive status and which never calls the blocker. The public empty-response suite disables pacing at thread_goal_empty_responses.rs:71. Thus the supplied mutant is killed, but does not establish the requested blocker-order property. Source ordering is currently correct; this is a missing adversarial proof, not an observed production failure. Request a focused narrowing mutant that defers EmptyResponse handling specifically for pacing-enabled automatic turns, and a production-path test asserting the third fully empty turn blocks before another pacing registration/turn is permitted.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/continuation_schedule.rs:664",
          "command": "gh run view 38160194813 --repo ivanopcode/codex --job 114533299061 --log",
          "expected_failure": "Observed hosted test-runner exit 100: only pacing_inactive_goal_never_paced fails. gh log retrieval itself exits 0. This reproduces the coverage mismatch, not an ordering regression.",
          "pinned_blobs": [
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/tests/continuation_schedule.rs (killer of the supplied mutant) blob 3ce4e86fbdbaaa175340f3578c05081edd01d02c",
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/src/extension.rs (on_turn_stop blocker then note_turn_completed) blob 91be5c24988ba959322c723efaf9fb0813d24dee",
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/src/background_wait.rs (evaluate_locked) blob 29863636c86496369bfc070e7723fad7af25275f",
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/core/tests/suite/goal_continuation_pacing.rs (requested new test goes here) blob b0e866324c9bd4dcb042bb4bd0fe3405f0ef1f0d"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_continuation_pacing.rs (requested addition: goal_pacing_empty_blocker_runs_before_rescheduling)",
          "command": "just test -p codex-core -E test(goal_pacing_empty_blocker_runs_before_rescheduling)",
          "expected_failure": "NOT RUN / proposed hosted attack: with pacing enabled and a narrow defer-empty-blocker mutant, require failure when the third fully empty automatic turn leaves the goal Active or arms a further continuation. Baseline must block at turn 3, with exactly three model requests and no later request.",
          "pinned_blobs": [
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/tests/continuation_schedule.rs (killer of the supplied mutant) blob 3ce4e86fbdbaaa175340f3578c05081edd01d02c",
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/src/extension.rs (on_turn_stop blocker then note_turn_completed) blob 91be5c24988ba959322c723efaf9fb0813d24dee",
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/src/background_wait.rs (evaluate_locked) blob 29863636c86496369bfc070e7723fad7af25275f",
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/core/tests/suite/goal_continuation_pacing.rs (requested new test goes here) blob b0e866324c9bd4dcb042bb4bd0fe3405f0ef1f0d"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261011-3cyko9"
      ]
    },
    {
      "id": "A-N1",
      "row": "one live timer",
      "invariant": "The pacing-disabled switch should be narrowly applied to suites that actually require consecutive automatic continuations; production event-wake interactions should remain observable.",
      "mechanism": "goal_background_wait.rs:189 applies CODEX_GOAL_PACING_DISABLED=1 in the common harness for all four tests. unopted_server_process_does_not_gate_goal_continuation and headless_host_refuses_notify_on_exit_and_promises_no_wake do require two consecutive goal continuations. notified_exec_exit_wakes_gated_goal_with_receipt_fragment instead starts once after goal set and then wakes with exec_completion; user_burst_during_background_wait_admitted_without_loss_or_duplication inserts two human turns and then an exec_completion wake. Those two tests need no back-to-back automatic goal continuation and could retain pacing. The switch is documented as never set in production and its production read accepts only exact value 1; the scope of this harness use is the advisory defect. Narrow the override to the two tests that need it, and retain a separate pacing-enabled wake-while-timer-armed attack for full interaction coverage.",
      "reproductions": [
        {
          "test_file": "codex-rs/app-server/tests/suite/v2/goal_background_wait.rs:172",
          "command": "git show 181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/app-server/tests/suite/v2/goal_background_wait.rs",
          "expected_failure": "Static inventory: the shared builder disables pacing for 4/4 tests, while only 2/4 require consecutive automatic goal turns. No production failure or newly executed test is claimed.",
          "pinned_blobs": [
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/app-server/tests/suite/v2/goal_background_wait.rs (shared harness sets the switch) blob bdfc43eea263162e177efbd18f65091b8be7b8a0"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261011-3cyko9"
      ]
    },
    {
      "id": "F1-blocker-mutant-proxy",
      "row": "blocker order and waiting turns",
      "invariant": "The three-fully-empty-continuations blocker runs FIRST and is unchanged; a nonempty waiting continuation is paced, not counted empty (AC5).",
      "mechanism": "Informational only: the supplied mutant pacing_blocker_order_swapped deletes the InactiveOrBudgetLimited early-return in BackgroundWaitState::evaluate_continuation, which is unreachable from the sole production caller (GoalRuntimeHandle::continue_if_idle passes GoalWaitStatus::Active unconditionally after its own Active-status gate, codex-rs/ext/goal/src/runtime.rs). Its only hosted killer is the direct unit test pacing_inactive_goal_never_paced (small lane), which calls evaluate_continuation with the inactive status explicitly. The production on_turn_stop order (stop_active_goal_for_turn EmptyResponse blocker before note_turn_completed, codex-rs/ext/goal/src/extension.rs) has no behavioral mutant because swapping those two calls is behavior-preserving: they read and write disjoint state (blocker reads accounting empties only; pacing records streak/predecessor only), so no killer could distinguish the orders. The substantive AC5 property is instead evidenced by (a) the on_turn_stop delta being a pure insertion after the unchanged blocker calls (verified by diff), (b) pacing_waiting_turn_is_paced_not_empty driving the REAL P4b-1 accounting classifier (empty_response_goal None, no observed state change, streak grows, paced wait armed), and (c) the pre-existing thread_goal_empty_responses 3-empty suite green (kill switch isolates blocker-unchanged). No actionable remedy exists; not verdict-blocking.",
      "reproductions": [
        {
          "test_file": "candidate codex-rs/ext/goal/src/runtime.rs + codex-rs/ext/goal/src/background_wait.rs + codex-rs/ext/goal/tests/continuation_schedule.rs (read-only git show of tree 181cc48fbd0b927f134ba39d268882a52551e776)",
          "command": "git show 181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/src/runtime.rs | sed -n '679,700p'; git grep -n 'InactiveOrBudgetLimited' 181cc48fbd0b927f134ba39d268882a52551e776 -- codex-rs/ext/goal/src/",
          "expected_failure": "No failure expected or observed: static witness confirms the mutant's deleted lines are unreachable from production (hardcoded Active at the only call site) while the row still holds via the cited unit, waiting-turn, and blocker-suite evidence plus hosted mutant kill.",
          "pinned_blobs": [
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/src/runtime.rs (continue_if_idle) blob 03da9c00eb413d5b7d7a33bf85d6f3131a9998d2",
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/src/background_wait.rs (evaluate_continuation) blob 29863636c86496369bfc070e7723fad7af25275f",
            "181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/tests/continuation_schedule.rs (pacing_inactive_goal_never_paced) blob 3ce4e86fbdbaaa175340f3578c05081edd01d02c"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261011-3w3wcg"
      ]
    }
  ],
  "notes": [
    "[TASK-261011-3cyko9] Sources are pinned to candidate 181cc48fbd0b927f134ba39d268882a52551e776 / hosted snapshot 2f00490d5f4f227486e92a0c523aa8d545fb24a5, not ambient worktree HEAD. No accept/reject/status/handoff/resource/note mutation was made on the source task.",
    "[TASK-261011-3cyko9] Entry-rule decision in b2-rework-brief-precheck3.md is honored: first after human turn / goal set / resume is immediate with revision-bearing ProceedNormal; later consecutive automatic continuations wait. This still invalidates old tickets through lifecycle hooks. It is an intentional exception to any reading that requires a delay before the first automatic continuation.",
    "[TASK-261011-3cyko9] Terminology discrepancy: AC1 and note_turn_completed docs define n as completed quiet continuations, but evaluate_pacing_locked feeds pacing_streak + 1 into pacing_delay. Thus after one completed quiet turn pacing_streak=1 but the next delay is 60 s, not pacing_delay(1)=30 s. Rework and both public tests expressly require that 60 s behavior. Reconcile AC/docs to upcoming continuation ordinal (or decide a different formula) before claiming the literal completed-count equation; this panel does not request reversing the explicit entry-rule rework.",
    "[TASK-261011-3cyko9] Kill-switch survey: app-server code_mode_host blocks test, thread_resume root/parent test, thread_goal_empty_responses parameterized test genuinely need consecutive automatic continuations. Of the shared goal_background_wait harness cases, only unopted and headless cases need it; two notification cases do not (A-N1). Core background_wait_inactive_on_unavailable_host_auto_continues uses runtime.disable_pacing because its two-goal-turn test explicitly expects immediate background-inactive behavior. New pacing suites do not set the switch. Exact string 1 is read in production code; documentation is a deployment convention, not compile-time exclusion or a security boundary.",
    "[TASK-261011-3cyko9] Candidate defines and hosted small runs 23 pacing tests, rather than the 22 claimed in results. This is an evidence inventory correction, not lost coverage.",
    "[TASK-261011-3cyko9] No independent Windows/foreign-exec suite, full workspace run, clock-discontinuity experiment, or additional proposed mutant was executed in this panel. Hosted snapshot tests are Linux evidence. Reported success steps have no printed numeric command exits; do not invent zero exit telemetry from an omitted log line.",
    "[TASK-261011-3cyko9] Architecture advisory: 923-line background_wait.rs now holds most stateful pacing evaluation/admission logic while the new 148-line module holds math/ticket. Consider an internal pacing state extraction preserving the one shared lock and slot. Cumulative CR includes the previously accepted observations stage; size numbers must not be misrepresented as only this scheduler leaf.",
    "[TASK-261011-3w3wcg] Orchestrator point 1 (kill switch): CODEX_GOAL_PACING_DISABLED is read at exactly one production site (extension.rs on_thread_start, gating only enable_pacing) and documented test-only in both the constant docs (continuation_schedule.rs: production never sets it) and every call-site comment. It is set by exactly 4 app-server suites via per-server-process with_env_overrides plus 1 core test via the typed disable_pacing() method; whole-tree grep confirms no other setters (no CI config, no nextest, no production). Every switched FILE drives back-to-back automatic continuations: thread_goal_empty_responses x3 empties, code_mode_host x3 failure turns, thread_resume root/parent lineage x2, goal_background_wait harness tests 3-4 x2 with empty snapshots, and the harness-level placement is justified because tests 1-2 in that file are behavior-neutral under the switch (non-empty snapshots take the background-gate path, user-turn predecessors take the entry-rule immediate path, so pacing would not engage for them either way). One caveat: the core headless test background_wait_inactive_on_unavailable_host_auto_continues drives a SINGLE continuation (asserts 1 request, awaits nothing after turn 1), so its disable_pacing() is vestigial under the entry rule (turn 1 is immediate either way) but harmless, documented, and green; removing it would be safe-or-better for teardown determinism. No production behavior depends on the switch.",
    "[TASK-261011-3w3wcg] Orchestrator point 2 (entry rule vs AC1 and ticket rows): the implemented n-convention matches the decided rule in b2-rework-brief-precheck3 section 3 exactly (floor 30s at streak 0, then doubling: wait = pacing_delay(streak+1), gaps 60/120/240s between consecutive quiet continuations, all >= 30s; no off-by-one; the surface table's attack family off-by-one-in-n was explicitly checked). Cap verified to u32::MAX, reset-to-floor verified with automatic predecessor still paced at 30s, all executed in hosted small/core/app-server lanes. Ticket rows hold under the entry rule: ProceedNormal records a ticket-free admission attempt that check_admission rechecks (generation + revision + empty snapshot); a fast human turn invalidates both an armed wait and an issued ticket (dedicated test covers both stages); all 8 invalidation causes cancel the armed timer, fire the hook, and fail the claim.",
    "[TASK-261011-3w3wcg] Orchestrator point 3 (blocker-order killer): the evaluation-side gate (inactive/budget-limited goals never pace) has a direct killer (pacing_inactive_goal_never_paced, sole killer of pacing_blocker_order_swapped in precheck 4). The on_turn_stop call order itself has no direct killer and cannot have one (behavior-preserving swap, disjoint state); see F1. The row holds via insertion-only diff, the real-classifier waiting-turn test, and the green pre-existing blocker suite.",
    "[TASK-261011-3w3wcg] Execution boundary: replay plus static attack only; no cargo/just/build/test commands run. Row results cite hosted relux-ci run 38160194813 on the EXACT candidate tree (snapshot of tree 181cc48fbd0b927f134ba39d268882a52551e776) as executed public-entry attacks: 4/4 lanes green and 6/6 mutants killed with the named killers. This panel independently re-verified replay (write-tree match), all 6 mutant patches git apply --check clean against the candidate tree, and every named killer's presence in the tree.",
    "[TASK-261011-3w3wcg] Accepted bounds (disclosed, not claimed): mutant-lane aggregate model-request totals are unknown (hosted summary gives lanes/killers, not totals); the results doc correctly scopes counts to passing-test assertions (app-server 4, core 1-then-2, units 0). No test drives 3 fully-empty continuations to stopped WITH pacing enabled (would need 60+120s real delays; safe by construction since pacing only delays and the blocker counts accounting empties independently). note_release has no production callers (covered method-level by the 8-cause invalidation test for future wiring)."
  ],
  "surface_results": [
    {
      "row": "spacing and streak math",
      "result": "held",
      "attack": "Attack first-entry pacing, overflow/cap, read-only success resetting the streak, and observed-change reset.",
      "evidence": "continuation_schedule.rs:61-69 uses saturating subtraction, bounded shift and capped checked multiplication; background_wait.rs:483 uses completed streak + 1 as the upcoming schedule index. Hosted small passes delay, reset, non-continuation and two-poll tests; missing-cap and reset mutants fail with exit 100. Hosted core confirms immediate first continuation then ~60 s. Held for the explicit precheck-3 rework timing rule; the completed-count/ordinal wording discrepancy is recorded in notes rather than silently treated as identical.",
      "reported_by": "TASK-261011-3cyko9"
    },
    {
      "row": "polls grow the streak end to end",
      "result": "held",
      "attack": "Try two consecutive get_goal polls with nonempty waiting text and no state-changing outcome; require actual requests and a larger second delay.",
      "evidence": "Hosted app-server goal_pacing_two_polls_first_immediate_second_60s passes in 69.259 s. Source asserts 2 then 4 requests, first delay <28 s, second >=58 s, and no third turn/extra request for 8 s. Core asserts 1 then 2 requests. Reset-on-non-change mutant kills pacing_two_polls_grow_streak and also fails the hosted core lane. Third-delay exact 120 s is unit-covered, not fully waited by the app-server test.",
      "reported_by": "TASK-261011-3cyko9"
    },
    {
      "row": "one live timer",
      "result": "held",
      "attack": "Try repeated evaluations, replacement, stale generation installs, turn-start invalidation and known pending work taking priority.",
      "evidence": "runtime.rs:606-639 calls the pre-existing CheckInTimer single slot, which aborts the old JoinHandle before replacement, detaches before callback, and rejects older-generation installs. Runtime construction installs its abort hook. Hosted core traverses actual timer/claim/start; hosted small passes replacement, event-wake, known-work and cancellation tests. Timer-not-cancelled mutant fails two named tests with exit 100. Event-wake pacing test directly calls note_turn_start; the real notification tests disable pacing, so a public combined wake-versus-armed-pacing-timer attack is not claimed; see A-N1.",
      "reported_by": "TASK-261011-3cyko9"
    },
    {
      "row": "ticket invalidation and admission",
      "result": "held",
      "attack": "Try changed revision, predecessor, generation, single-use reuse, fast intervening human turn, and read failure / mail between evaluation and publication.",
      "evidence": "background_wait.rs:569-665 consumes the attempt once under its lock and rejects changed generation, revision, goal, predecessor and nonempty snapshot. extension.rs:271 and :659 wire start/human input; runtime/tool hooks wire goal changes, clear, stop and resume. Existing Core goal_admission.rs:49-89, :93-110 and :145-183 enforce revision at early admission and locked publication; runtime holds goal permit across read/start. Hosted small passes stale/fast-human/claim tests; skip-revision mutant directly fails the named stale-revision test with exit 100. Fast-human and eight cancellation causes are helper-entry attacks; public fast-human replay not separately executed. note_release has no production caller in this or the base tree; receipt/mail transitions instead revise pending work and event turn start invalidates generation, so direct note_release test is not misrepresented as production dispatch proof.",
      "reported_by": "TASK-261011-3cyko9"
    },
    {
      "row": "blocker order and waiting turns",
      "result": "broken",
      "attack": "Trace the real turn-stop blocker ordering and attack whether its advertised mutant actually changes it.",
      "evidence": "extension.rs:380-387 invokes stop_active_goal_for_turn(EmptyResponse) before :419-429 records pacing. Waiting-turn test and public poll test hold nonempty waiting behavior. The supplied blocker-order patch attacks a different status gate, and its sole killer cannot exercise the empty blocker. Public empty-response suite runs with pacing disabled. A-F1 leaves AC8 ordering proof unsatisfied; no present ordering bug is claimed.",
      "reported_by": "TASK-261011-3cyko9"
    },
    {
      "row": "transient state",
      "result": "held",
      "attack": "Try persistence, resume with an accumulated streak/quota, and completion being mistaken for human input.",
      "evidence": "Pacing state lives only in WaitState; no rollout/config serialization change. note_resume clears streak, predecessor, ticket, deadlines and background quota; runtime.rs:582-602 reconciles the actual goal before resetting. Hosted small passes pacing_resume_restarts_at_floor_and_resets_quotas and the existing exhausted-allowance/late-completion test. Empty snapshot reassessment does not itself reset check_ins_used; restart reset is explicitly disclosed in results. An end-to-end pacing-enabled restart with a saved nonzero streak is not supplied.",
      "reported_by": "TASK-261011-3cyko9"
    },
    {
      "row": "no model-visible change",
      "result": "held",
      "attack": "Try new scheduler text, context fragments, history items or warning emission leaking into inference requests.",
      "evidence": "Candidate source diff adds no scheduling prompt/context/history construction. Runtime waits and returns before building the existing continuation steering item. Hosted app-server examines all 4 request bodies for pacing/PacingTicket/continuation_schedule/streak and exec_completion markers; hosted small confirms no warning during pacing wait/fire. Marker checks alone cannot prove arbitrary history equality; static diff supplies the complementary bounded check.",
      "reported_by": "TASK-261011-3cyko9"
    },
    {
      "row": "mutants and measurement",
      "result": "broken",
      "attack": "Replay every supplied mutant against the exact candidate; compare hosted commit trees, named failing tests, exit codes and asserted requests.",
      "evidence": "6/6 supplied patches replay exactly to the 6 hosted mutant trees; 6/6 hosted small runners exit 100 and the intended named tests fail. Snapshot small/core/app-server and lint are success. Semantically required mutant families covered: 4/5 (reset, cap, stale admission, cancellation); blocker ordering is not covered by the misnamed status-gate deletion. Entry-rule mutant is additional coverage. Requests measured: core 2, app-server 4, helper tests 0; total requests across mutant jobs unknown. A-F1.",
      "reported_by": "TASK-261011-3cyko9"
    },
    {
      "row": "placement and size",
      "result": "held",
      "attack": "Search for Core scheduling logic/dependencies, module size, and public surface beyond cross-crate needs.",
      "evidence": "New continuation_schedule.rs is 148 LoC with private module + explicit exports; wait-state integration stays in goal and shares its existing lock/timer rather than a second scheduler in Core. Core changes in the cumulative CR are thin observation hooks and tests inherited from the observation stage, not a Core pacing dependency. BackgroundWaitState is now 923 LoC (601 at CR base), tests file 849 LoC, and cumulative CR is +3706/-26, above repository guidance. This organization/size advisory needs review; held only for goal ownership and new-module <500 requirement, not a claim that all size guidance is satisfied.",
      "reported_by": "TASK-261011-3cyko9"
    }
  ],
  "free_hunt": [
    "[TASK-261011-3cyko9] {\"budget\": \"Four bounded additional attack families: switch scoping, streak index consistency, persistence/completion quota reset, and placement/public API inventory. Static only beyond reused hosted execution; no builds/tests/source mutations.\", \"results\": [{\"family\": \"switch-scoping\", \"result\": \"advisory A-N1; 2/4 common-harness tests need disablement, 2/4 do not.\"}, {\"family\": \"schedule-index\", \"result\": \"explicit rework behavior holds; completed-streak versus next-index discrepancy documented, no speculative change in product behavior requested.\"}, {\"family\": \"completion-and-resume\", \"result\": \"completion reassessment preserves background quota; resume resets transient quotas as disclosed; production dispatch of standalone note_release not established.\"}, {\"family\": \"placement-and-API\", \"result\": \"goal owns pacing, no Core dependency; module/total-size advisories documented, no additional runtime defect established.\"}]}",
    "[TASK-261011-3w3wcg] Bounded static hunt beyond the rows (no builds): (1) PacingTicket.streak/issued_at have no production readers, but streak divergence without invalidation is unreachable: every production streak change flows through note_turn_completed for a started turn, and every turn start bumps the generation, so the generation check implicitly covers streak freshness; NEW ticket per wait plus single-use consumption (outstanding handle + last-consumed id + attempt take) prevents cross-wait reuse. (2) CheckIn and pacing tickets share one next_ticket_id counter, keeping ids unique across both families. (3) Arithmetic is total: streak saturating_add, shift clamped to 31, u32 checked_mul with cap fallback plus .min(cap), deadline checked_add with Duration::MAX fallback, saturating_sub at read sites. (4) disable_pacing (test-only caller) clears slot/outstanding/attempt and fires the hook without a generation bump; stale timers fail the claim quietly. (5) The new ProceedWithoutGate arm removes the admission checker, restoring never-inserted equivalence for pacing-only headless hosts; gate-only flows still overwrite the checker on every Proceed arm. (6) Steering during a paced wait conservatively restarts the wait at the same streak (invalidation clears the anchor; streak kept because steering observes no state change itself). (7) Aborted turns correctly skip predecessor rebinding (only completed turns bind). (8) Named but not filed (out of scope, pre-existing code): a hypothetical mutant deleting the runtime Active pre-check has no killer in the tree, but it targets a pre-P4b line, not this CR. No blocking mechanism found outside the swept rows."
  ]
}
```


## Recording reviewer verification and logbook — 2026-10-12

TASK-260929-309h9n — continuation-schedule; CR-TASK-260929-309h9n-1 revision 1, candidate tree 181cc48fbd0b927f134ba39d268882a52551e776. Recording run RUN-261011-22df93.

Compared the complete attached panel A and panel B outcomes to this merged verdict. Findings preserved: 3/3 (A-F1, A-N1, F1-blocker-mutant-proxy); reproductions preserved: 4/4; notes preserved: 12/12; panel free-hunt records preserved: 2/2. Panel A's repeat-of null is normalized to "none", with unchanged meaning. Every surface row appears exactly once, in the prescribed order; results match the worst panel result. No finding is omitted and no new technical finding is added.

| Surface row | Merged result |
|---|---|
| spacing and streak math | held |
| polls grow the streak end to end | held |
| one live timer | held |
| ticket invalidation and admission | held |
| blocker order and waiting turns | broken |
| transient state | held |
| no model-visible change | held |
| mutants and measurement | broken |
| placement and size | held |

Recording verdict: changes_requested. Panel A requests changes; panel B accepts. A-F1 requires production-path proof that three fully empty automatic continuations block before pacing reschedules, and a corresponding narrowing mutant; the existing mutant attacks an inactive-status gate. A-N1 asks to narrow the shared background-wait test switch. The note from panel B is retained as informational. No production failure is inferred from the proof gap.

This run reread the three attached artifacts and validated their finding fields, reproduction fields, notes, free-hunt records, row uniqueness/order and worst-result merge. It did not rerun Rust tests, hosted CI, replay or mutants; execution evidence remains attributed to the panels and hosted precheck 4. No repository code, index, branch or temporary directory was changed or created. Board-resource reads, role/skill reads and scoped reject_cr schema read exited 0. An initial batched projection omitted semicolon separators and exited 1; the corrected read exited 0. A skill-relative reviewer-role path was missing; the role was read successfully from /Users/administrator/.roles/reviewer/role.md. command -v logbook exited 1, so this task-scoped outcome contains the logbook record. The run has no bound goal and no directives.

Route through reject_cr with this verdict as evidence; do not accept or mark done. Producer rework and another reviewer cycle are required.
