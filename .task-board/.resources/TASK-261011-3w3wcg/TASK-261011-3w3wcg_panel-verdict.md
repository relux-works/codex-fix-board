# R141 panel B verdict — CR-TASK-260929-309h9n-1 revision 1

accept

Replay: base e0eff057620104a416080da616256ee7f32bda1b plus the attached rev1 patch produced exactly candidate tree 181cc48fbd0b927f134ba39d268882a52551e776 through a temporary index (git write-tree match). No worktree or real-index mutation; no source edits, builds, or tests run; no writes of any kind on TASK-260929-309h9n (read-only review; all panel writes target TASK-261011-3w3wcg).

Commands run directly (exit codes):

| Command | Exit | Evidence |
|---|---:|---|
| task-board m 'set_status(TASK-261011-3w3wcg, status=analysis)' | 0 | Own-task lifecycle only |
| task-board q reads (reviewed-task AC, progress) | 0 | Read-only inputs |
| GIT_INDEX_FILE=...replay.idx git read-tree e0eff057620104a416080da616256ee7f32bda1b | 0 | Replay base loaded |
| cp board patch to .temp/TASK-260929-309h9n_change-request_rev1.patch | 0 | Read-only patch retrieval |
| GIT_INDEX_FILE=...replay.idx git apply --cached (patch) | 0 | Patch replayed cleanly |
| GIT_INDEX_FILE=...replay.idx git write-tree | 0 | Printed exactly 181cc48fbd0b927f134ba39d268882a52551e776 |
| git archive 181cc48... (goal + pacing tests + nextest) piped to tar -x | 0 | Candidate extraction for static review |
| mutant apply-check driver: 6x git apply --cached --check vs candidate tree | 0 | All 6 mutants apply cleanly (each exit 0) |
| git show / git diff / git grep scoped reads | 0 | All cited code evidence |
| python3 prior-verdict schema probe (first attempt, own typo) | 1 | My probe typo (NameError), not an artifact gate; corrected rerun exited 0 |

This panel ran no cargo, just, builds, or Rust tests per the brief (shared build target is serialized). Executed-attack evidence is the CR validation log (mini-hosted-gate.sh exit 0 attesting tree 181cc48fbd0b927f134ba39d268882a52551e776 green on hosted relux-ci run 38160194813) and TASK-260929-309h9n_hosted-precheck-4.md (lint/small/core/app-server 4/4 green, 6/6 narrowing mutants killed on the exact candidate tree). Static replay and inspection above are this panel's own work.

```verdict-findings
{
  "findings": [
    {
      "id": "F1-blocker-mutant-proxy",
      "row": "blocker order and waiting turns",
      "invariant": "The three-fully-empty-continuations blocker runs FIRST and is unchanged; a nonempty waiting continuation is paced, not counted empty (AC5).",
      "mechanism": "Informational only: the supplied mutant pacing_blocker_order_swapped deletes the InactiveOrBudgetLimited early-return in BackgroundWaitState::evaluate_continuation, which is unreachable from the sole production caller (GoalRuntimeHandle::continue_if_idle passes GoalWaitStatus::Active unconditionally after its own Active-status gate, codex-rs/ext/goal/src/runtime.rs). Its only hosted killer is the direct unit test pacing_inactive_goal_never_paced (small lane), which calls evaluate_continuation with the inactive status explicitly. The production on_turn_stop order (stop_active_goal_for_turn EmptyResponse blocker before note_turn_completed, codex-rs/ext/goal/src/extension.rs) has no behavioral mutant because swapping those two calls is behavior-preserving: they read and write disjoint state (blocker reads accounting empties only; pacing records streak/predecessor only), so no killer could distinguish the orders. The substantive AC5 property is instead evidenced by (a) the on_turn_stop delta being a pure insertion after the unchanged blocker calls (verified by diff), (b) pacing_waiting_turn_is_paced_not_empty driving the REAL P4b-1 accounting classifier (empty_response_goal None, no observed state change, streak grows, paced wait armed), and (c) the pre-existing thread_goal_empty_responses 3-empty suite green (kill switch isolates blocker-unchanged). No actionable remedy exists; not verdict-blocking.",
      "reproductions": [
        {
          "test_file": "candidate codex-rs/ext/goal/src/runtime.rs + codex-rs/ext/goal/src/background_wait.rs + codex-rs/ext/goal/tests/continuation_schedule.rs (read-only git show of tree 181cc48fbd0b927f134ba39d268882a52551e776)",
          "command": "git show 181cc48fbd0b927f134ba39d268882a52551e776:codex-rs/ext/goal/src/runtime.rs | sed -n '679,700p'; git grep -n 'InactiveOrBudgetLimited' 181cc48fbd0b927f134ba39d268882a52551e776 -- codex-rs/ext/goal/src/",
          "expected_failure": "No failure expected or observed: static witness confirms the mutant's deleted lines are unreachable from production (hardcoded Active at the only call site) while the row still holds via the cited unit, waiting-turn, and blocker-suite evidence plus hosted mutant kill."
        }
      ],
      "severity": "note",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Orchestrator point 1 (kill switch): CODEX_GOAL_PACING_DISABLED is read at exactly one production site (extension.rs on_thread_start, gating only enable_pacing) and documented test-only in both the constant docs (continuation_schedule.rs: production never sets it) and every call-site comment. It is set by exactly 4 app-server suites via per-server-process with_env_overrides plus 1 core test via the typed disable_pacing() method; whole-tree grep confirms no other setters (no CI config, no nextest, no production). Every switched FILE drives back-to-back automatic continuations: thread_goal_empty_responses x3 empties, code_mode_host x3 failure turns, thread_resume root/parent lineage x2, goal_background_wait harness tests 3-4 x2 with empty snapshots, and the harness-level placement is justified because tests 1-2 in that file are behavior-neutral under the switch (non-empty snapshots take the background-gate path, user-turn predecessors take the entry-rule immediate path, so pacing would not engage for them either way). One caveat: the core headless test background_wait_inactive_on_unavailable_host_auto_continues drives a SINGLE continuation (asserts 1 request, awaits nothing after turn 1), so its disable_pacing() is vestigial under the entry rule (turn 1 is immediate either way) but harmless, documented, and green; removing it would be safe-or-better for teardown determinism. No production behavior depends on the switch.",
    "Orchestrator point 2 (entry rule vs AC1 and ticket rows): the implemented n-convention matches the decided rule in b2-rework-brief-precheck3 section 3 exactly (floor 30s at streak 0, then doubling: wait = pacing_delay(streak+1), gaps 60/120/240s between consecutive quiet continuations, all >= 30s; no off-by-one; the surface table's attack family off-by-one-in-n was explicitly checked). Cap verified to u32::MAX, reset-to-floor verified with automatic predecessor still paced at 30s, all executed in hosted small/core/app-server lanes. Ticket rows hold under the entry rule: ProceedNormal records a ticket-free admission attempt that check_admission rechecks (generation + revision + empty snapshot); a fast human turn invalidates both an armed wait and an issued ticket (dedicated test covers both stages); all 8 invalidation causes cancel the armed timer, fire the hook, and fail the claim.",
    "Orchestrator point 3 (blocker-order killer): the evaluation-side gate (inactive/budget-limited goals never pace) has a direct killer (pacing_inactive_goal_never_paced, sole killer of pacing_blocker_order_swapped in precheck 4). The on_turn_stop call order itself has no direct killer and cannot have one (behavior-preserving swap, disjoint state); see F1. The row holds via insertion-only diff, the real-classifier waiting-turn test, and the green pre-existing blocker suite.",
    "Execution boundary: replay plus static attack only; no cargo/just/build/test commands run. Row results cite hosted relux-ci run 38160194813 on the EXACT candidate tree (snapshot of tree 181cc48fbd0b927f134ba39d268882a52551e776) as executed public-entry attacks: 4/4 lanes green and 6/6 mutants killed with the named killers. This panel independently re-verified replay (write-tree match), all 6 mutant patches git apply --check clean against the candidate tree, and every named killer's presence in the tree.",
    "Accepted bounds (disclosed, not claimed): mutant-lane aggregate model-request totals are unknown (hosted summary gives lanes/killers, not totals); the results doc correctly scopes counts to passing-test assertions (app-server 4, core 1-then-2, units 0). No test drives 3 fully-empty continuations to stopped WITH pacing enabled (would need 60+120s real delays; safe by construction since pacing only delays and the blocker counts accounting empties independently). note_release has no production callers (covered method-level by the 8-cause invalidation test for future wiring)."
  ],
  "surface_results": [
    {
      "row": "spacing and streak math",
      "result": "held",
      "detail": "Held by executed attacks on the exact tree: pacing_delay unit test pins n=0..8,100,u32::MAX (30/30/60/120/240/480/960/cap); entry-rule n-convention verified against the decided brief (floor 30s at streak 0, wait=pacing_delay(streak+1)); hosted small lane green; pacing_missing_cap killed by the delay test; core and app-server integration tests executed real 60s n=2 waits (remaining in (45,60] paused; >=58s real)."
    },
    {
      "row": "polls grow the streak end to end",
      "result": "held",
      "detail": "Held by the app-server vertical test over real JSON-RPC with real get_goal poll turns: 4 requests total, first delay <28s, second >=58s (a poll-as-activity reset would floor the second wait at ~30s and fail); hosted app-server lane green; pacing_streak_reset_on_non_state_change killed by pacing_two_polls_grow_streak. Single P4b-1 observation input; no second classifier in the delta."
    },
    {
      "row": "one live timer",
      "result": "held",
      "detail": "Held structurally and by execution: zero new spawn/sleep sites in the goal delta; pacing reuses the single-slot CheckInTimer (abort-old plus newer-generation-wins); re-evaluation re-arms the same deadline (no accumulation) and invalidation starts a fresh episode; event wake and all 8 causes pre-empt via the shared hook with claim-fail proof; early/superseded/wrong-generation claims rejected; hosted small lane green."
    },
    {
      "row": "ticket invalidation and admission",
      "result": "held",
      "detail": "Held by execution: one test drives all 8 invalidation causes (turn start, steering, goal mutation, release, human input, clear, stop, resume), each cancelling the armed timer, firing the hook exactly once, and failing the claim; fast intervening human turn invalidates both the armed wait and the issued ticket; revision-change, predecessor-change, and reuse admissions all rejected; ticket binds goal/revision/predecessor/generation/streak (asserted field by field); entry-rule immediate path records an attempt rechecked at admission; pacing_stale_ticket_admission_skip_revision killed; hosted small+core green."
    },
    {
      "row": "blocker order and waiting turns",
      "result": "held",
      "detail": "Held: on_turn_stop delta is a pure insertion of note_turn_completed AFTER the unchanged blocker calls (verified by diff); waiting-turn test uses the real accounting classifier (nonempty waiting turn: empty None, zero state change, streak grows, paced wait armed); inactive/budget-limited goals never pace and going inactive cancels the armed registration; pre-existing 3-empty blocker suite green; pacing_blocker_order_swapped killed by its named unit killer. See note F1 for the mutant's proxy scope."
    },
    {
      "row": "transient state",
      "result": "held",
      "detail": "Held by execution: resume test resets streak, predecessor, outstanding ticket, armed deadline, and check_ins_used, proceeds immediately first, then paces n=2 from the floor; turn completion touches only pacing_* fields (allowance untouched); goal-status mutations keep the pre-existing epoch reset that AC4 requires as invalidation; restart-resets-quotas disclosed in results and logbook; nothing persisted (no rollout/history fields in the delta)."
    },
    {
      "row": "no model-visible change",
      "result": "held",
      "detail": "Held structurally and by execution: delta adds no prompt text, fragments, history, or context code (grep-verified); pacing waits emit no warnings (unit test across a full wait/fire/admit cycle); all 4 app-server request bodies scanned for pacing/PacingTicket/continuation_schedule/streak markers plus completion-fragment absence; hosted lanes green."
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "detail": "Held: all 6 mutants re-verified git apply --check clean against the exact candidate tree by this panel (each exit 0); all 6 killed on hosted precheck 4 with named killers re-verified present in the tree (streak-reset, missing-cap, stale-admission, uncancelled-timer, blocker-order, entry-rule); killer names all match the pacing/goal filter; request counts asserted in passing tests (app-server 4 incl. no-early-turn3 still-4, core 1-then-2, units 0); unknown mutant-lane aggregates disclosed, not claimed."
    },
    {
      "row": "placement and size",
      "result": "held",
      "detail": "Held: continuation_schedule.rs is new at 148 LoC; hooks are thin (accounting +5, extension +15, runtime +16, lib +7); background_wait growth is inside the mandatory shared WaitState lock (evaluation/admission atomicity) with module docs; zero codex-core or app-server production files touched; tests live in ext/goal/tests plus the core/app-server suites; public additions limited to the needed ticket/schedule API; no new core-to-goal edge."
    }
  ],
  "free_hunt": [
    "Bounded static hunt beyond the rows (no builds): (1) PacingTicket.streak/issued_at have no production readers, but streak divergence without invalidation is unreachable: every production streak change flows through note_turn_completed for a started turn, and every turn start bumps the generation, so the generation check implicitly covers streak freshness; NEW ticket per wait plus single-use consumption (outstanding handle + last-consumed id + attempt take) prevents cross-wait reuse. (2) CheckIn and pacing tickets share one next_ticket_id counter, keeping ids unique across both families. (3) Arithmetic is total: streak saturating_add, shift clamped to 31, u32 checked_mul with cap fallback plus .min(cap), deadline checked_add with Duration::MAX fallback, saturating_sub at read sites. (4) disable_pacing (test-only caller) clears slot/outstanding/attempt and fires the hook without a generation bump; stale timers fail the claim quietly. (5) The new ProceedWithoutGate arm removes the admission checker, restoring never-inserted equivalence for pacing-only headless hosts; gate-only flows still overwrite the checker on every Proceed arm. (6) Steering during a paced wait conservatively restarts the wait at the same streak (invalidation clears the anchor; streak kept because steering observes no state change itself). (7) Aborted turns correctly skip predecessor rebinding (only completed turns bind). (8) Named but not filed (out of scope, pre-existing code): a hypothetical mutant deleting the runtime Active pre-check has no killer in the tree, but it targets a pre-P4b line, not this CR. No blocking mechanism found outside the swept rows."
  ]
}
```
