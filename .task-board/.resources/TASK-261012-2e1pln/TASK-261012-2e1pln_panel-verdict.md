# Panel B verdict — TASK-260929-309h9n CR-TASK-260929-309h9n-2 revision 2 (R141, non-recording)

Verdict: **accept**

## Replay tree check

Replayed the CR patch on base `e0eff057620104a416080da616256ee7f32bda1b` through a
temporary index (no nested worktree). `git write-tree` printed
`af312067fcd2392b78deb95d3f71925e739622b7`, exactly the expected candidate tree.
No mismatch; review proceeded to the full surface sweep. Candidate files were read via
`git show af312067...:<path>` and a `git archive` extract; no builds or tests were run
(forbidden by the brief; shared build target is serialized).

## Commands run with exit codes

- `task-board m 'set_status(TASK-261012-2e1pln, status=analysis)'` — exit 0 (own-task lifecycle)
- `GIT_INDEX_FILE="$IDX" git read-tree e0eff057...` — exit 0
- `task-board resource get TASK-260929-309h9n TASK-260929-309h9n_change-request_rev2.patch` — exit 0
- `GIT_INDEX_FILE="$IDX" git apply --cached <patch>` — exit 0
- `GIT_INDEX_FILE="$IDX" git write-tree` — exit 0, printed `af312067...` (match)
- `git archive af312067... <6 src paths> | tar -x` — exit 0
- `git archive af312067... <2 test paths> | tar -x` — exit 0
- Mutant `git apply --cached --check` against the candidate index, all 6 mutants — exit 0 each
- Read-only `git show` / `git grep` / `git diff` for the static attack — exit 0
- No `cargo`, `just`, build, or test command was run (brief forbids them)
- No `accept_cr` / `reject_cr` / `set_status` / `handoff` / note / resource write on
  `TASK-260929-309h9n` was made; all board reads there were `q` and `resource get`.

Correction note: a first mutant-check attempt ran `git apply --check` (5x exit 1, 1x exit 0)
against the story worktree instead of the candidate index due to a scoping error on my
side; it was rerun correctly with `--cached` against the candidate index (6x exit 0).
The recorded result is the corrected one.

```verdict-findings
{
  "findings": [
    {
      "id": "B2-N1",
      "row": "one live timer",
      "invariant": "Orchestrator Q1 / AC3: pacing shares the single check-in timer slot without perturbing the P4a check-in flow; the precheck-6 flake of suite::goal_background_wait::scheduled_checkins_fire_through_production_runtime_under_paused_time (TRY 1 FAIL after 10.5 s, TRY 2 PASS) must be attributed or bounded before accept.",
      "mechanism": "Static attack over the exact candidate tree found no causal mechanism. (a) Pacing arms pending_deadline only for empty snapshots: evaluate_locked routes non-empty snapshots to the unchanged check-in path whenever the gate is enabled (background_wait.rs). The P4a test holds a stalled Armed receipt for its whole run, so every evaluation takes the check-in path; pacing evaluation never runs there. (b) The only pacing code executing in that flow is enable-once at thread start plus one brief non-awaiting Mutex section in note_turn_completed at turn stop: no await, no I/O, cannot stall 10 s. (c) CheckInTimer spawn/claim for the gate path is unchanged from base except claim's '!enabled' becoming '!enabled && !pacing_enabled', a no-op when enabled=true as the test asserts. check_in_clock.rs is byte-identical to base. (d) The ProceedWithoutGate checker-removal is unreachable in that test (status hardcoded Active at the only call site; gate enabled). (e) The 10.5 s signature matches exactly one 10 s 'timeout waiting for event' (wait_for_event_with_timeout floors every poll at 10 s, core/tests/common/lib.rs) plus setup: a real-time scheduling stall, and the retry passed on the identical tree; first-try green in prechecks 4 and 5 and in P3-1 precheck 12. Informational only: no defect established. Residual unknown: the exact awaited event/assertion (no CI log access from this panel). Suggested non-blocking hardening: call disable_pacing() in the P4a fixture to decouple the suites, or capture the failing assertion on the next flake.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs: scheduled_checkins_fire_through_production_runtime_under_paused_time (read-only git show of tree af312067fcd2392b78deb95d3f71925e739622b7)",
          "command": "git show af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/core/tests/suite/goal_background_wait.rs | sed -n '199,320p'; git diff e0eff057620104a416080da616256ee7f32bda1b af312067fcd2392b78deb95d3f71925e739622b7 -- codex-rs/ext/goal/src/check_in_clock.rs",
          "expected_failure": "No failure expected or observed: static witness that pacing cannot engage in the P4a flow (snapshots always non-empty; timer file unchanged) and the hosted TRY 1 fail / TRY 2 pass on the identical tree is an unattributed CI scheduling stall, not a CR regression."
        }
      ],
      "severity": "note",
      "repeat-of": "none"
    },
    {
      "id": "B2-N2",
      "row": "one live timer",
      "invariant": "Orchestrator Q2: CODEX_GOAL_PACING_DISABLED must be an acceptable production surface, not a test-only hook forbidden by AGENTS.md (avoid test-only functions in the implementation; avoid mutating process env in tests).",
      "mechanism": "Judged acceptable; no change requested. (a) Production reads the switch at exactly one site, once per thread start (extension.rs on_thread_start), exact-'1' match, gating only enable_pacing. Whole-tree grep on the candidate: 4 app-server suites set it via per-server-process with_env_overrides (no process-env mutation anywhere), 1 core test uses the typed disable_pacing() method; no CI, nextest, or production setters. (b) disable_pacing() is the AGENTS.md-compliant alternative to env mutation in-process (a parallel test binary must not mutate shared process env); it is also a coherent runtime API symmetric with enable_pacing that clears the slot/outstanding/attempt and fires the hook, not a stub. (c) Fail-open direction is cost-only (pre-pacing timing, more model requests), no privilege; docs state production never sets it. (d) A-N1 closure verified in-tree: start_goal_harness takes pacing_disabled with /*pacing_disabled*/ callsites; only unopted_server_process_does_not_gate_goal_continuation and headless_host_refuses_notify_on_exit_and_promises_no_wake pass true, while notified_exec_exit_wakes_gated_goal_with_receipt_fragment and user_burst_during_background_wait_admitted_without_loss_or_duplication run pacing-enabled and pass hosted (4 and 6 requests). Optional long-term direction (config flag instead of env) is out of scope for this CR.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/extension.rs:186-187, codex-rs/app-server/tests/suite/v2/goal_background_wait.rs:177-200,306,433,540,609 (read-only git show/grep of tree af312067fcd2392b78deb95d3f71925e739622b7)",
          "command": "git grep -n 'PACING_DISABLED_ENV_VAR\\|pacing_disabled_by_env\\|CODEX_GOAL_PACING_DISABLED\\|disable_pacing\\|enable_pacing' af312067fcd2392b78deb95d3f71925e739622b7 -- codex-rs",
          "expected_failure": "No failure expected or observed: static inventory confirms one production read site, per-process-only test setters, no process-env mutation, and the narrowed harness."
        }
      ],
      "severity": "note",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Sources pinned to candidate af312067fcd2392b78deb95d3f71925e739622b7, not ambient worktree HEAD. No accept/reject/status/handoff/resource/note mutation was made on TASK-260929-309h9n.",
    "Execution boundary: replay plus static attack only; no cargo/just/build/test commands run. Row results cite hosted relux-ci run 38188455502 (precheck 6) on the EXACT candidate tree as executed public-entry attacks: lint/small/core/app-server 4/4 green, 6/6 mutants killed with named killers. This panel independently re-verified replay (write-tree match), all 6 mutant patches git apply --cached --check clean against the candidate index, and every named killer's presence in the tree.",
    "Production is identical between rev1 (181cc48f) and rev2 (af312067): the inter-revision delta is 2 test files only (goal_background_wait.rs harness param, goal_continuation_pacing.rs rework). A-F1 and A-N1 closures are test-only as claimed; all rev1 held-row evidence carries forward subject to re-verification, which this panel performed.",
    "Terminology carried from rev1 (decided, not a finding): AC1's completed-count n vs the implemented upcoming-ordinal wait pacing_delay(streak+1) (gaps 60/120/240 s between consecutive quiet continuations, all >= 30 s). This matches the explicit entry-rule rework decision in b2-rework-brief-precheck3; no behavior change requested.",
    "Evidence inventory correction carried from rev1: the candidate defines 23 pacing unit tests (23 #[test] fns in ext/goal/tests/continuation_schedule.rs), not the 22 claimed in results. Coverage is not lost.",
    "Mutant-lane bound: precheck 6 reports per-mutant failing lanes as small/core only; per-mutant app-server execution is not evidenced either way. No row depends on it: every mutant has a named small/core killer. Mutant-lane aggregate model-request totals remain unknown; counts are scoped to passing-test assertions (core 2 and 3, app-server 4, wake tests 4 and 6, units 0).",
    "note_release has no production caller in this or the base tree (pre-existing). Release still invalidates stale pacing tickets indirectly: every receipt-store/mailbox transition bumps the pending-work revision, which admission rechecks; the next idle evaluation re-arms from the new revision. Not misrepresented as direct dispatch proof.",
    "Wake-vs-armed-pacing-timer bound: the armed-timer preemption unit test drives note_turn_start directly; production wiring (on_turn_start invalidates before the enabled check, for every turn start) plus the two pacing-enabled hosted wake tests cover the interaction. No dedicated public-entry test lands a wake while a pacing timer is provably armed.",
    "Size advisory carried: background_wait.rs is 923 LoC; cumulative CR is +3900/-34 across 31 paths (tests-heavy coherent scheduler slice, disclosed in results). Held only for goal ownership, new-module <500, and no core scheduler growth.",
    "P4a flake residual: exact awaited event unknown without CI log access; attribution rests on the static no-mechanism trace plus identical-tree green retry."
  ],
  "surface_results": [
    {
      "row": "spacing and streak math",
      "result": "held",
      "attack": "Attack entry-rule bypass, overflow/missing cap, reset on non-state-change, reset-source divergence from P4b-1, and the n-convention.",
      "evidence": "pacing_delay is total: saturating_sub, shift clamped to 31, u32 checked_mul with cap fallback plus .min(cap) (continuation_schedule.rs:62-69); n=0/1 floor 30 s, n=2 60 s, cap 30 min verified by hosted pacing_delay_n1_n2_n3_and_cap killing pacing_missing_cap. note_turn_completed is the sole production streak writer (background_wait.rs:792-809) and consumes only the P4b-1 has_observed_state_change classifier: no second classifier; pacing_streak_reset_on_non_state_change killed in small+core. Entry rule (first continuation immediate, then paced) proven end to end by hosted core goal_pacing_first_immediate_second_at_60s (turn 1 < 28 s, n=2 deadline in (45,60] s, 2 requests) and the entry-deletion mutant killed by 19 tests. n-convention matches the decided rework rule (see notes)."
    },
    {
      "row": "polls grow the streak end to end",
      "result": "held",
      "attack": "Drive two consecutive read-only get_goal polls with nonempty waiting text through a real server; require request growth and the n=2 second delay.",
      "evidence": "Hosted app-server goal_pacing_two_polls_first_immediate_second_60s passes: first poll < 28 s, second >= 58 s, 2 then 4 requests with the tool result attached, no third turn/request in the 8 s n=3 window, goal stays Active. Unit pacing_two_polls_grow_streak kills the reset-on-non-change mutant. Bound: per-mutant app-server execution not evidenced (see notes); small/core killers suffice."
    },
    {
      "row": "one live timer",
      "result": "held",
      "attack": "Attack second timers, detached sleeps, replacement leaks, stale-generation installs, wake-without-preemption, pacing overriding governing deadlines, and the P4a shared-slot flake.",
      "evidence": "Exactly one slot: pacing arms the shared pending_deadline and CheckInTimer (file byte-identical to base), whose spawn aborts the old handle before replacement and rejects older-generation installs; timers detach before claiming and quiet-exit when superseded/invalidated/disabled/early (runtime.rs:616-641, background_wait.rs:529-548). Hosted small passes replacement, event-wake, known-work, and cancellation tests; pacing_timer_not_cancelled_on_invalidation killed by the two named tests. Non-empty snapshots always take the gate path, so pacing never overrides a governing subscribed deadline (unit pacing_known_work_uses_background_wait_instead). Both app-server wake tests run pacing-enabled and pass hosted. P4a flake attacked with no mechanism found (B2-N1); kill-switch surface judged acceptable (B2-N2)."
    },
    {
      "row": "ticket invalidation and admission",
      "result": "held",
      "attack": "Attack skipped revision/generation checks, check-then-act outside the lock, fast human turns, stale-timer turn starts, and each invalidation cause.",
      "evidence": "Ticket binds goal id + revision, predecessor turn, and generation/cause (continuation_schedule.rs:80-89). All causes wired: any turn start invalidates before the enabled check (extension.rs:271, covers fast human turns), human input (TurnInputContributor), goal set/mutate/clear, terminal completion (via note_goal_mutation), stop, resume, steering; release covered via revision bump (see notes). check_admission consumes the attempt once under the state lock and rechecks generation, revision (attempt AND ticket), goal identity, predecessor, outstanding handle, single-use id, and empty snapshot (background_wait.rs:569-665). Hosted small passes bind/stale-predecessor/stale-revision/reuse/claim/fast-human tests; pacing_stale_ticket_admission_skip_revision killed by exactly pacing_stale_ticket_rejected_on_revision_change."
    },
    {
      "row": "blocker order and waiting turns",
      "result": "held",
      "attack": "Attack blocker-after-pacing, blocker threshold changes, and waiting turns misclassified as empty. Re-verify the A-F1 closure behaviorally.",
      "evidence": "A-F1 closed: hosted core goal_pacing_empty_blocker_runs_before_rescheduling (pacing ENABLED) drives 3 fully empty continuations (immediate, n=2 60 s, n=3 120 s under paused time) to terminal Blocked, asserts no armed wait after the blocking turn via ThreadIdle::wait ordering, advances past n=4 (241 s) with no TurnStarted in 250 ms and requests stopped at 3; it is the sole killer of pacing_blocker_skipped_for_paced_turns in the core lane. on_turn_stop delta is a pure insertion after the unchanged EmptyResponse/ExecutionUnavailable blocker calls (extension.rs:379-387 blocker, :423-429 pacing record). Waiting turns: unit pacing_waiting_turn_is_paced_not_empty drives the real P4b-1 classifier (empty_response_goal None, streak grows, wait armed), and the app-server polls carry waiting text and are paced, not counted empty."
    },
    {
      "row": "transient state",
      "result": "held",
      "attack": "Attack persisted streaks/subscriptions, resume restoring stale state, and completion resetting the human-input allowance.",
      "evidence": "Zero pacing references under codex-rs/core/src/session and codex-rs/state: timers/streaks/counters live only in WaitState. note_resume clears streak, goal, predecessor, deadlines, tickets, and quotas (background_wait.rs:762-775); restore_after_resume reconciles the live goal first, then resets (runtime.rs). Empty-snapshot reassessment (completion path) never touches check_ins_used. Hosted small passes pacing_resume_restarts_at_floor_and_resets_quotas; restart-resets-quotas and resume-immediate-first are disclosed bounds in results."
    },
    {
      "row": "no model-visible change",
      "result": "held",
      "attack": "Attack injected pacing text, history/context items for timers, and warning emission into inference requests.",
      "evidence": "Zero diff in steering.rs/events.rs; runtime waits-and-returns before building the existing continuation steering item. Hosted app-server scans all 4 two-poll request bodies for pacing/PacingTicket/continuation_schedule/streak/exec_completion markers (absent); hosted small pacing_emits_no_warnings_or_prompt_text passes. Bound: marker scans plus the bounded static diff jointly evidence the row; markers alone are not full history equality."
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "attack": "Replay every supplied mutant against the exact candidate; check named killers exist and AC8 families are covered; verify request counts are asserted, not prose.",
      "evidence": "6/6 mutant patches git apply --cached --check clean against the candidate index (exit 0 each, verified by this panel); 6/6 killed hosted with named killers (reset: two-polls/core tests; cap: delay test; stale: revision test; timer: wake+cancellation tests; blocker: new core blocker test; entry: 19 tests incl. the immediate-first test). All five AC8 families covered plus the entry rule. Requests asserted per scenario: core 2 then blocker 3-and-silence, app-server 4, wake tests 4/6, units 0. Bounds: 23-vs-22 count nit and unknown mutant-lane totals (see notes); no independent mutants for transient/model-visible/placement rows, disclosed in results."
    },
    {
      "row": "placement and size",
      "result": "held",
      "attack": "Attack scheduler logic in codex-core, core->goal dependencies, module size, and public surface beyond need.",
      "evidence": "Scheduler leaf is new private module continuation_schedule.rs (148 LoC) with explicit re-exports; stateful evaluation stays in ext/goal sharing the existing lock/slot. No codex-core production growth from this leaf (core production deltas in the cumulative diff belong to the P4b-1 observation stage); rev1->rev2 delta is 2 test files only. Tests live in ext/goal/tests and core/app-server suites. New public API is the minimal cross-crate surface (delay consts/fn, ticket, enable/disable, streak/predecessor/deadline readers). Advisory: 923-LoC background_wait.rs and cumulative size exceed guidance (see notes)."
    }
  ],
  "free_hunt": [
    "ProceedWithoutGate checker-removal equivalence (bounded static proof): in base, evaluation ran only when the gate was enabled, so base ProceedWithoutGate was unreachable in production (status hardcoded Active) and the blind checker insert only affected unit tests. In the candidate it is reachable exactly when pacing-but-not-gate is enabled with a non-empty snapshot (pacing-only headless hosts): removing the checker restores base never-inserted equivalence so Core (goal_admission.rs: 'no checker => gate inactive => proceed') admits without consulting a stale attempt. Evaluation-to-publish holds the goal permit, so no interleaving turn start can observe the transient. No defect; the change is strictly safer than base.",
    "Ticket/counter/arithmetic hygiene (bounded static sweep): PacingTicket.streak/issued_at have no production readers, but divergence without invalidation is unreachable (every production streak change flows through note_turn_completed for a started turn; every turn start bumps the generation, which admission checks). CheckIn and pacing tickets share one next_ticket_id counter, keeping ids unique across families. Arithmetic is total (saturating_add streak, shift min 31, checked_mul with cap fallback plus .min(cap), checked_add deadline with Duration::MAX fallback, saturating_sub reads). disable_pacing clears slot/outstanding/attempt and fires the hook without a generation bump; any in-flight timer then fails its claim quietly and any published checker finds no attempt and Waits. No defect.",
    "Lifecycle-edge sweep (bounded static): steering invalidates (generation bump, abort) while conservatively keeping the streak since steering itself observes no state change; aborted turns skip predecessor rebinding (only completed turns bind via on_turn_stop); human turns bind predecessor with is_continuation=false so the next continuation is immediate via both note_human_input and the turn-stop record; goal completion funnels through note_goal_mutation after the terminal status write. Release relies on the revision bump rather than note_release (see notes). No defect outside the swept rows."
  ]
}
```
