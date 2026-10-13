# Merged review verdict — TASK-260929-309h9n CR revision 2 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261012-18lf7s_panel-verdict.md` (changes_requested), `TASK-261012-2e1pln_panel-verdict.md` (accept), `TASK-261012-2x08jb_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A2-F1",
      "row": "placement and size",
      "invariant": "AGENTS.md: avoid test-only functions in the main implementation and avoid proliferating test-only public API; pacing is mandatory for consecutive automatic continuations unless an explicitly supported production policy says otherwise.",
      "mechanism": "continuation_schedule.rs:42-52 declares the switch Test-only and adds public pacing_disabled_by_env(), which directly reads ambient CODEX_GOAL_PACING_DISABLED. lib.rs:36,39 exports both the constant and accessor. The unconditionally compiled production GoalExtension::on_thread_start (extension.rs:184-188) skips enable_pacing when the value is exactly 1. Therefore a released app-server/CLI process inherits a real opt-out, not a test-confined injection; the claims production never sets this and pacing is always active there describe a convention, not enforced behavior. The hosted public-entry unopted-server case supplies the switch via per-child environment, launches the production app-server and runs two automatic continuations / four requests in 2.206s. It establishes that the opt-out changes production scheduling. The rework brief explicitly retained this switch; that is acknowledged context, but the panel is asked to assess its fit against AGENTS.md rather than treat the producer brief as authority. Remove the production test-only accessor/exports and adapt legacy timing through existing clock/dependency injection or pacing-aware waits. If an operational opt-out is intended, define and test it as an explicit production policy with accurate bounds rather than claim it is test-only. Per-child with_env_overrides does not mutate the test runner process; there is no set_var/remove_var violation alleged.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/continuation_schedule.rs:42; codex-rs/ext/goal/src/extension.rs:184; codex-rs/ext/goal/src/lib.rs:36",
          "command": "git grep -n -E 'CODEX_GOAL_PACING_DISABLED|pacing_disabled_by_env|PACING_DISABLED_ENV_VAR' af312067fcd2392b78deb95d3f71925e739622b7 -- codex-rs",
          "expected_failure": "Executed static witness, command exit 0: production accessor and activation branch are unconditionally compiled and public exports exist. The policy mismatch is the finding; no failing Rust test is claimed.",
          "pinned_blobs": [
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/ext/goal/src/continuation_schedule.rs (candidate file) blob 5c9843a6d0b5a935fe6b836cc8f0288bbab91a38",
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/ext/goal/src/extension.rs (candidate file) blob 91be5c24988ba959322c723efaf9fb0813d24dee",
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/ext/goal/src/lib.rs (candidate file) blob 7ac2b6235335aa8c799fc509db9bb59b177c6291"
          ]
        },
        {
          "test_file": "codex-rs/app-server/tests/suite/v2/goal_background_wait.rs:177,196,507,540",
          "command": "gh run view 38188455502 --repo ivanopcode/codex --job 114617661332 --log",
          "expected_failure": "Retrieval executed with exit 0. Existing unopted_server_process_does_not_gate_goal_continuation PASSES in 2.206s with the per-child switch, asserts two automatic turns and four requests under 30s read timeouts, exercising the released app-server path without a pacing delay. This is executed evidence of the override, not a newly failing test.",
          "pinned_blobs": [
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/app-server/tests/suite/v2/goal_background_wait.rs (candidate file) blob dd31a31a57509e43e8902df821131c1a6398930c"
          ]
        },
        {
          "test_file": "codex-rs/app-server/tests/suite/v2/goal_continuation_pacing.rs:139 (proposed inherited-environment attack)",
          "command": "CODEX_GOAL_PACING_DISABLED=1 just test -p codex-app-server -E 'test(goal_pacing_two_polls_first_immediate_second_60s)'",
          "expected_failure": "NOT RUN / requested hosted attack. On the candidate, inherited override should make the second_delay >=58s assertion fail. After removing production test plumbing, baseline mandatory spacing should pass even if this obsolete test variable is inherited. Numeric exit is unknown; no execution claimed.",
          "pinned_blobs": [
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/app-server/tests/suite/v2/goal_continuation_pacing.rs (candidate file) blob b9f480e79ea12bea4ab4cd2a893c3c7978f1c468"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-18lf7s"
      ]
    },
    {
      "id": "B2-N1",
      "row": "one live timer",
      "invariant": "Orchestrator Q1 / AC3: pacing shares the single check-in timer slot without perturbing the P4a check-in flow; the precheck-6 flake of suite::goal_background_wait::scheduled_checkins_fire_through_production_runtime_under_paused_time (TRY 1 FAIL after 10.5 s, TRY 2 PASS) must be attributed or bounded before accept.",
      "mechanism": "Static attack over the exact candidate tree found no causal mechanism. (a) Pacing arms pending_deadline only for empty snapshots: evaluate_locked routes non-empty snapshots to the unchanged check-in path whenever the gate is enabled (background_wait.rs). The P4a test holds a stalled Armed receipt for its whole run, so every evaluation takes the check-in path; pacing evaluation never runs there. (b) The only pacing code executing in that flow is enable-once at thread start plus one brief non-awaiting Mutex section in note_turn_completed at turn stop: no await, no I/O, cannot stall 10 s. (c) CheckInTimer spawn/claim for the gate path is unchanged from base except claim's '!enabled' becoming '!enabled && !pacing_enabled', a no-op when enabled=true as the test asserts. check_in_clock.rs is byte-identical to base. (d) The ProceedWithoutGate checker-removal is unreachable in that test (status hardcoded Active at the only call site; gate enabled). (e) The 10.5 s signature matches exactly one 10 s 'timeout waiting for event' (wait_for_event_with_timeout floors every poll at 10 s, core/tests/common/lib.rs) plus setup: a real-time scheduling stall, and the retry passed on the identical tree; first-try green in prechecks 4 and 5 and in P3-1 precheck 12. Informational only: no defect established. Residual unknown: the exact awaited event/assertion (no CI log access from this panel). Suggested non-blocking hardening: call disable_pacing() in the P4a fixture to decouple the suites, or capture the failing assertion on the next flake.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs: scheduled_checkins_fire_through_production_runtime_under_paused_time (read-only git show of tree af312067fcd2392b78deb95d3f71925e739622b7)",
          "command": "git show af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/core/tests/suite/goal_background_wait.rs | sed -n '199,320p'; git diff e0eff057620104a416080da616256ee7f32bda1b af312067fcd2392b78deb95d3f71925e739622b7 -- codex-rs/ext/goal/src/check_in_clock.rs",
          "expected_failure": "No failure expected or observed: static witness that pacing cannot engage in the P4a flow (snapshots always non-empty; timer file unchanged) and the hosted TRY 1 fail / TRY 2 pass on the identical tree is an unattributed CI scheduling stall, not a CR regression.",
          "pinned_blobs": [
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/core/tests/suite/goal_background_wait.rs (candidate file) blob 7f88964f6722ab9b1b78c837f90ab543b449d42b",
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/ext/goal/src/check_in_clock.rs (candidate file) blob 73de2bfd4375d64dca2cb9639ecad07b23896e15"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-2e1pln"
      ]
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
          "expected_failure": "No failure expected or observed: static inventory confirms one production read site, per-process-only test setters, no process-env mutation, and the narrowed harness.",
          "pinned_blobs": [
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/app-server/tests/suite/v2/goal_background_wait.rs (candidate file) blob dd31a31a57509e43e8902df821131c1a6398930c",
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/ext/goal/src/extension.rs (candidate file) blob 91be5c24988ba959322c723efaf9fb0813d24dee"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-2e1pln"
      ]
    },
    {
      "id": "D-N1",
      "row": "one live timer",
      "invariant": "An executed public-entry check-in attack must not be described as reliably green when it retries; diagnose its relation to pacing without inventing a cause.",
      "mechanism": "The exact snapshot check-in test times out waiting for an event on TRY 1 (10.516s), then passes TRY 2 (1.222s). Its real Armed receipt is never completed or released, so every evaluation takes the nonempty-snapshot background-wait branch; it cannot enter evaluate_pacing_locked or install a pacing deadline. CheckInTimer, that test, and the goal production code are identical to rev1. However, TurnComplete precedes active-turn cleanup/idle and this P4a test still manually emits idle and advances time without waiting for a fresh arm. That pre-existing race is a plausible diagnostic lead, not an established root cause. Pacing adds turn-stop bookkeeping compared with the original pre-pacing base and may alter timing; direct slot interference is statically excluded for this fixture, timing-induced exposure is unknown. Recommend a focused hosted synchronized run with teardown/arm tracing before classifying the flake as unrelated.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs:199-320",
          "command": "gh run view 38188455502 --repo ivanopcode/codex --job 114617661821 --log",
          "expected_failure": "Observed TRY 1 FAIL at core/tests/common/lib.rs:393, timeout waiting for event; TRY 2 PASS. Log retrieval exits 0; successful hosted step has no printed numeric exit. No deterministic local reproduction or root-cause assertion.",
          "pinned_blobs": [
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/core/tests/suite/goal_background_wait.rs (candidate file) blob 7f88964f6722ab9b1b78c837f90ab543b449d42b"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs::scheduled_checkins_fire_through_production_runtime_under_paused_time",
          "command": "HOSTED PROPOSAL: just test -p codex-core -E 'test(scheduled_checkins_fire_through_production_runtime_under_paused_time)' with arm/idle tracing and teardown synchronization, compared with the unsynchronized exact candidate",
          "expected_failure": "Not run in this panel. Require explicit per-phase arm/generation observations and repeated results; distinguish teardown race from an unexpected pending snapshot becoming empty. No failure is presumed.",
          "pinned_blobs": [
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/core/tests/suite/goal_background_wait.rs (candidate file) blob 7f88964f6722ab9b1b78c837f90ab543b449d42b"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-2x08jb"
      ]
    },
    {
      "id": "D-N2",
      "row": "placement and size",
      "invariant": "AGENTS.md prefers avoiding test-only implementation helpers and ambient test inputs; crate API should remain small.",
      "mechanism": "pacing_disabled_by_env and its exported environment-name constant exist solely for test compatibility according to their own docs. The reader runs in normal on_thread_start, so a real production process with CODEX_GOAL_PACING_DISABLED=1 also disables pacing. It is therefore a shipped opt-out, not a test-isolated hook, and 'pacing always active in production' is not enforced. No test here mutates the parent process environment; app-server overrides are child-process inputs. The entry-rule rework decision explicitly retained this switch for legacy tests, and rev2 narrows its scope as requested. This panel accepts that recorded compatibility exception for this delta; it does not declare the hook an ideal API or a blanket exception to AGENTS. Prefer typed dependency/config injection and reduce the exported testing API, or explicitly describe the production opt-out. The unit assertion that ambient env is not disabled remains an avoidable test determinism issue.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/continuation_schedule.rs:42-53; codex-rs/ext/goal/src/extension.rs:184-188; codex-rs/ext/goal/tests/continuation_schedule.rs:841-849",
          "command": "git grep -n 'CODEX_GOAL_PACING_DISABLED\\|pacing_disabled_by_env\\|PACING_DISABLED_ENV_VAR\\|disable_pacing()' af312067fcd2392b78deb95d3f71925e739622b7 -- codex-rs",
          "expected_failure": "Static inventory command exits 0. The exact string 1 bypasses enable_pacing at normal thread start; the ambient-env assertion can fail under that setting. No process environment mutation, production launch, or new runtime failure was executed.",
          "pinned_blobs": [
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/ext/goal/src/continuation_schedule.rs (candidate file) blob 5c9843a6d0b5a935fe6b836cc8f0288bbab91a38",
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/ext/goal/src/extension.rs (candidate file) blob 91be5c24988ba959322c723efaf9fb0813d24dee",
            "af312067fcd2392b78deb95d3f71925e739622b7:codex-rs/ext/goal/tests/continuation_schedule.rs (candidate file) blob 3ce4e86fbdbaaa175340f3578c05081edd01d02c"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-2x08jb"
      ]
    }
  ],
  "notes": [
    "[TASK-261012-18lf7s] N1 — P4a flake: independently retrieved core job 114617661821: scheduled_checkins_fire_through_production_runtime_under_paused_time TRY 1 FAIL at 10.516s; panic core/tests/common/lib.rs:393 timeout waiting for event; TRY 2 PASS 1.222s. The log does not identify which of the three TurnComplete waits timed out or print the test process numeric exit. Do not invent one. Candidate core aggregate is success, 5083 passed (1 flaky), 11 skipped. Failed first attempt remains a failure.",
    "[TASK-261012-18lf7s] N1 mechanism assessment: the fixture arms one stalled receipt BEFORE setting the goal and never completes/releases it in this test. Every continuation snapshot stays nonempty, so background_wait.rs:356-370 never enters evaluate_pacing_locked; the unchanged known-work branch retains absolute 30/60/120min slots. CheckInTimer code is byte-identical to CR base. No pacing overwrite/cancellation of that slot was established for this scenario. Additional on_turn_stop bookkeeping changes scheduling/interleavings, so a timing-sensitive pre-existing test may be exposed by this CR without a production timer defect.",
    "[TASK-261012-18lf7s] N1 plausible interleaving: tasks/mod.rs:1037 sends TurnComplete before :1040-1057 clears active_turn and emits idle. The P4a test at :274-291 immediately pauses, calls emit_thread_idle_lifecycle_if_idle (which can no-op while active), advances another 30/60min and resumes without awaiting the actual idle rearm. The new pacing tests explicitly fixed this pattern using pause then await_pacing_armed and ThreadIdle::wait. Static trace supports the synchronization explanation; it does not prove this was the hosted failure. Requested diagnostic: hosted repeated exact-tree just test -p codex-core -E test(scheduled_checkins_fire_through_production_runtime_under_paused_time) with NEXTEST_RETRIES=0, then a narrow test-only variant waiting for the expected check-in slot after each TurnComplete before advance; require the same 3 requests/quota/warning and compare reproduction rates. Do not add a pacing env override to conceal the failure. No local execution of this diagnostic.",
    "[TASK-261012-18lf7s] N2 — Entry/math wording: completed streak=1 feeds pacing_delay(2)=60s; after reset completed streak=0 feeds pacing_delay(1)=30s. AC1 describes n as completed quiet continuations, which literally would yield 30s after one. The precheck3 decision and both public/core tests explicitly require immediate first then 60s/120s. Held for that decided behavior, with the completed-count versus upcoming-index documentation discrepancy retained; no request to undo the authorized entry rule.",
    "[TASK-261012-18lf7s] N3 — Prior review closure: A-F1 and F1-blocker-mutant-proxy are closed by direct pacing-enabled third-empty test and narrowing mutant, not by the inactive-status proxy. A-N1 is closed: goal_background_wait harness disables pacing only for unopted/headless tests; notified-exit and user-burst tests keep it enabled. A2-F1 is a separate production API/policy mechanism, not a repeat of A-N1 harness breadth.",
    "[TASK-261012-18lf7s] N4 — API/size bound: no new CLI flag, app-server JSON schema, config or rollout serialization found. The environment opt-out is a new production input in the cumulative scheduler stage, even though unchanged in rev2. background_wait.rs is 923 lines; most stateful pacing is there, not in the 148-line math/ticket module. Consider internal pacing-state extraction retaining the shared lock. Cumulative CR sizing includes accepted sibling observations; the rev2 production diff is empty.",
    "[TASK-261012-18lf7s] N5 — Execution provenance: this panel ran replay, Git/JSON inspection, six mutant apply/check/tree comparisons and hosted metadata/log reads. It ran no cargo, just, build, Rust tests or new mutants. Reused execution is exact-tree hosted run 38188455502, snapshot commit a921adbbdf13ac8327478dc15274dc160e5bedad, tree af312067fcd2392b78deb95d3f71925e739622b7. Dispatcher head 9f8fdf9a has a different tree and is not the tested snapshot. Workflow overall conclusion failure is expected because mutant jobs are red; only snapshot lanes are 4/4 success.",
    "[TASK-261012-18lf7s] N6 — Blind spots: timer/cancellation and fast-human helpers do not launch public event dispatch. The two pacing-enabled notification tests exercise subscribed background waits, not an already armed quiet pacing wait. note_release has no production caller. Context marker scans are not entire-history equality. No independent Windows/foreign-exec, full workspace rerun, public saved-streak restart, clock-jump diagnostic or new inherited-env attack executed. Coverage is nine rows swept once, six supplied mutations matched and killed, five required mutation families covered; no claim of exhaustive scheduling-state coverage.",
    "[TASK-261012-18lf7s] free-hunt: {\"family\": \"production env override / ambient tests\", \"result\": \"A2-F1; no parent-process environment mutation found. The unit pacing_disabled_by_default_with_env_kill_switch asserts ambient env is unset, so it is also sensitive to inherited deployment state; this is part of the same mechanism, not a second finding.\"}",
    "[TASK-261012-18lf7s] free-hunt: {\"family\": \"wall-clock discontinuity\", \"result\": \"SystemCheckInClock uses wall-clock now with a Tokio duration sleep; if wall time steps backward while sleeping, claim_due_deadline can reject the single fire and leave a registration without a live task. Code predates this CR and no discontinuity experiment executed, so it is an unverified inherited robustness risk, not a new proven regression. Named desired attack: pacing_clock_rollback_rearms_until_deadline through production timer/runtime with an injected clock jump.\"}",
    "[TASK-261012-18lf7s] free-hunt: {\"family\": \"read failure / quota / persistence\", \"result\": \"Read errors return WaitOnReadFailure and admission Wait, never empty fallback. Empty-snapshot completion does not reset check_ins_used. Restart quota reset is disclosed. No persisted pacing state or new observation classifier found.\"}",
    "[TASK-261012-18lf7s] free-hunt: {\"family\": \"publication race / ticket cause / ownership\", \"result\": \"Generation plus turn-start invalidation covers changes to streak/automatic predecessor; stale attempts are consumed under the state lock and revision rechecked at publication. No new gate bypass established. Existing timer holds only weak runtime and releases the permit before sleeping. Cross-crate public env accessor is unnecessary for internal start wiring (A2-F1).\"}",
    "[TASK-261012-2e1pln] Sources pinned to candidate af312067fcd2392b78deb95d3f71925e739622b7, not ambient worktree HEAD. No accept/reject/status/handoff/resource/note mutation was made on TASK-260929-309h9n.",
    "[TASK-261012-2e1pln] Execution boundary: replay plus static attack only; no cargo/just/build/test commands run. Row results cite hosted relux-ci run 38188455502 (precheck 6) on the EXACT candidate tree as executed public-entry attacks: lint/small/core/app-server 4/4 green, 6/6 mutants killed with named killers. This panel independently re-verified replay (write-tree match), all 6 mutant patches git apply --cached --check clean against the candidate index, and every named killer's presence in the tree.",
    "[TASK-261012-2e1pln] Production is identical between rev1 (181cc48f) and rev2 (af312067): the inter-revision delta is 2 test files only (goal_background_wait.rs harness param, goal_continuation_pacing.rs rework). A-F1 and A-N1 closures are test-only as claimed; all rev1 held-row evidence carries forward subject to re-verification, which this panel performed.",
    "[TASK-261012-2e1pln] Terminology carried from rev1 (decided, not a finding): AC1's completed-count n vs the implemented upcoming-ordinal wait pacing_delay(streak+1) (gaps 60/120/240 s between consecutive quiet continuations, all >= 30 s). This matches the explicit entry-rule rework decision in b2-rework-brief-precheck3; no behavior change requested.",
    "[TASK-261012-2e1pln] Evidence inventory correction carried from rev1: the candidate defines 23 pacing unit tests (23 #[test] fns in ext/goal/tests/continuation_schedule.rs), not the 22 claimed in results. Coverage is not lost.",
    "[TASK-261012-2e1pln] Mutant-lane bound: precheck 6 reports per-mutant failing lanes as small/core only; per-mutant app-server execution is not evidenced either way. No row depends on it: every mutant has a named small/core killer. Mutant-lane aggregate model-request totals remain unknown; counts are scoped to passing-test assertions (core 2 and 3, app-server 4, wake tests 4 and 6, units 0).",
    "[TASK-261012-2e1pln] note_release has no production caller in this or the base tree (pre-existing). Release still invalidates stale pacing tickets indirectly: every receipt-store/mailbox transition bumps the pending-work revision, which admission rechecks; the next idle evaluation re-arms from the new revision. Not misrepresented as direct dispatch proof.",
    "[TASK-261012-2e1pln] Wake-vs-armed-pacing-timer bound: the armed-timer preemption unit test drives note_turn_start directly; production wiring (on_turn_start invalidates before the enabled check, for every turn start) plus the two pacing-enabled hosted wake tests cover the interaction. No dedicated public-entry test lands a wake while a pacing timer is provably armed.",
    "[TASK-261012-2e1pln] Size advisory carried: background_wait.rs is 923 LoC; cumulative CR is +3900/-34 across 31 paths (tests-heavy coherent scheduler slice, disclosed in results). Held only for goal ownership, new-module <500, and no core scheduler growth.",
    "[TASK-261012-2e1pln] P4a flake residual: exact awaited event unknown without CI log access; attribution rests on the static no-mechanism trace plus identical-tree green retry.",
    "[TASK-261012-2e1pln] free-hunt: ProceedWithoutGate checker-removal equivalence (bounded static proof): in base, evaluation ran only when the gate was enabled, so base ProceedWithoutGate was unreachable in production (status hardcoded Active) and the blind checker insert only affected unit tests. In the candidate it is reachable exactly when pacing-but-not-gate is enabled with a non-empty snapshot (pacing-only headless hosts): removing the checker restores base never-inserted equivalence so Core (goal_admission.rs: 'no checker => gate inactive => proceed') admits without consulting a stale attempt. Evaluation-to-publish holds the goal permit, so no interleaving turn start can observe the transient. No defect; the change is strictly safer than base.",
    "[TASK-261012-2e1pln] free-hunt: Ticket/counter/arithmetic hygiene (bounded static sweep): PacingTicket.streak/issued_at have no production readers, but divergence without invalidation is unreachable (every production streak change flows through note_turn_completed for a started turn; every turn start bumps the generation, which admission checks). CheckIn and pacing tickets share one next_ticket_id counter, keeping ids unique across families. Arithmetic is total (saturating_add streak, shift min 31, checked_mul with cap fallback plus .min(cap), checked_add deadline with Duration::MAX fallback, saturating_sub reads). disable_pacing clears slot/outstanding/attempt and fires the hook without a generation bump; any in-flight timer then fails its claim quietly and any published checker finds no attempt and Waits. No defect.",
    "[TASK-261012-2e1pln] free-hunt: Lifecycle-edge sweep (bounded static): steering invalidates (generation bump, abort) while conservatively keeping the streak since steering itself observes no state change; aborted turns skip predecessor rebinding (only completed turns bind via on_turn_stop); human turns bind predecessor with is_continuation=false so the next continuation is immediate via both note_human_input and the turn-stop record; goal completion funnels through note_goal_mutation after the terminal status write. Release relies on the revision bump rather than note_release (see notes). No defect outside the swept rows.",
    "[TASK-261012-2x08jb] Previous merged findings reviewed 3/3: A-F1 closed by direct blocker test and selective mutant; A-N1 closed by per-caller switch scope; F1-blocker-mutant-proxy superseded. Their source and exact hosted evidence were inspected independently.",
    "[TASK-261012-2x08jb] The explicit entry-rule decision in b2-rework-brief-precheck3.md is honored: first after human/goal mutation/resume is immediate; consecutive quiet turns subsequently wait 60s,120s,... capped at 1800s. The public tests require that behavior. The stale documentation calling n the completed streak while runtime passes completed streak+1 is unchanged advisory debt; do not infer a requested reversal of the approved rule.",
    "[TASK-261012-2x08jb] Sources: source-task surface-table.md, TASK-260929-309h9n_review-verdict-rev1.md, producer-brief.md, b2-rework-brief-precheck3.md, TASK-260929-309h9n_results.md, TASK-260929-309h9n_mutants.json, TASK-260929-309h9n_change-request_rev2-validation.log and TASK-260929-309h9n_hosted-precheck-6.md, plus candidate git objects and independently fetched hosted logs.",
    "[TASK-261012-2x08jb] Request counts asserted by hosted public-entry tests: core quiet turns=2; core blocker=3, still 3 after +241s; app-server two polls=4; pacing-enabled notified-exit=4, user-burst=6. Goal helper/unit tests issue 0 requests. Mutant-job aggregate model request count is unknown, not reconstructed from baseline assertions.",
    "[TASK-261012-2x08jb] Pacing unit inventory is 23, not the results' 22. Hosted snapshot jobs run full selected package lanes; the pacing/goal filter applies to mutant jobs, not snapshot lanes.",
    "[TASK-261012-2x08jb] Cumulative CR against its supplied base is 31 files, +3900/-34, including the inherited observations stage. Results' 17-file scheduler slice is not the cumulative CR. New continuation_schedule.rs is 148 lines, while background_wait.rs is 923; the size/extraction advisory from rev1 remains. Revision delta adds tests only and does not worsen production module size.",
    "[TASK-261012-2x08jb] No cargo, just, build, local Rust test, full workspace, Windows or foreign-exec execution occurred. Hosted results are Linux evidence. Static source reasoning supplements executed hosted attacks; it does not become a newly executed public test.",
    "[TASK-261012-2x08jb] note_release has no production caller in this candidate (also noted in rev1). Normal receipt changes are rechecked via pending-work revision and event turn-start invalidation; direct note_release unit coverage is not claimed as production-dispatch proof.",
    "[TASK-261012-2x08jb] Logbook command unavailable (exit 1); the task-scoped outcome embeds the important anomaly, decisions and bounds below. No write was made on TASK-260929-309h9n.",
    "[TASK-261012-2x08jb] free-hunt: {\"budget\": \"Four bounded static families beyond the required sweep; reuse exact hosted execution, no new builds.\", \"results\": [{\"family\": \"precheck-6 check-in flake\", \"result\": \"D-N1 advisory; direct pacing-slot overwrite excluded by permanently nonempty receipt branch, exact cause/timing contribution unknown. Proposed hosted arm/teardown trace named.\"}, {\"family\": \"test-only production env reader\", \"result\": \"D-N2 advisory; exported helper is compatibility-only by intent but live in release code. Parent environment is not mutated by tests; ambient assertion remains fragile.\"}, {\"family\": \"rework teardown safety\", \"result\": \"Core tests now use production sole armer and bounded pause/yield observation. Blocked tail uses registered ThreadIdle. Both exact candidate tests pass first try and blocker mutant fails the intended status assertion. No production rework to regress.\"}, {\"family\": \"evidence identity and scope\", \"result\": \"Independently matched snapshot 1/1 and mutant trees 6/6; workflow FAILURE expected from mutant jobs; package green counts and one flaky test read from real logs. Corrected 23-vs-22 unit count and cumulative-versus-scheduler-only diff claims.\"}]}"
  ],
  "surface_results": [
    {
      "row": "spacing and streak math",
      "result": "held",
      "attack": "Attack off-by-one, saturation/cap, classifier divergence and reset on read-only success.",
      "evidence": "Default pacing: continuation_schedule.rs:61-69 bounds the shift and caps checked multiplication; background_wait.rs:483-484 schedules pacing_delay(completed_streak+1). Hosted small executes 23 pacing tests (not the 22 in the producer inventory); missing-cap and reset-on-non-change mutants fail with exit 100. Core immediate-first/60s-second and app-server 69.314s two-poll test pass. Held against the explicit entry/index decision in b2-rework-brief-precheck3.md; the literal AC completed-count formula still needs wording reconciliation (N2). The production opt-out is separately broken in placement and size (A2-F1).",
      "reported_by": "TASK-261012-18lf7s"
    },
    {
      "row": "polls grow the streak end to end",
      "result": "held",
      "attack": "Drive thread/start and thread/goal/set, two get_goal polls, nonempty waiting text and actual inference requests.",
      "evidence": "Hosted snapshot app-server job 114617661332 passes goal_pacing_two_polls_first_immediate_second_60s in 69.314s. Candidate test asserts 2 then 4 requests, first start <28s, second >=58s and no third request/turn in 8s. Core job 114617661821 passes the 2-request vertical. Mutant reset-on-non-change is killed by both core pacing tests (job 114617661353, exit 100), and the hosted small summary names pacing_two_polls_grow_streak. Third 120s delay is exercised through the core blocker test, not a full third public poll turn.",
      "reported_by": "TASK-261012-18lf7s"
    },
    {
      "row": "one live timer",
      "result": "held",
      "attack": "Try duplicate evaluations, replacement, stale installs, notification wake, invalidation and pending subscribed-work priority; inspect the reported P4a retry.",
      "evidence": "runtime.rs:116-117 installs the existing CheckInTimer abort hook; :616-639 uses its sole slot; check_in_clock.rs replaces/aborts the prior JoinHandle and detaches before callback. No second pacing sleep/task implementation exists. Known nonempty work takes background_wait.rs:382-424 rather than evaluate_pacing_locked. Small replacement/known-work/wake/cancel tests pass; uncancelled-hook mutant job 114617661382 exits 100 on pacing_event_wake_preempts_timer and pacing_invalidation_cancels_armed_timer. Pacing-enabled public notified-exit and user-burst cases pass (2.086s and 3.221s). These public cases arm the background check-in deadline, not a quiet pacing deadline; a public wake during an already armed quiet pacing wait is not independently executed. P4a retry diagnosis and requested discrimination are N1, not concealed by the green retry.",
      "reported_by": "TASK-261012-18lf7s"
    },
    {
      "row": "ticket invalidation and admission",
      "result": "held",
      "attack": "Try changed revision, generation, predecessor/goal, replayed tickets, fast intervening input and fresh pending mail/read failure.",
      "evidence": "background_wait.rs:229-236 invalidates generation, attempt, ticket and deadline and fires the abort hook. :569-665 consumes the attempt once under its mutex and checks generation/revision/goal/predecessor/empty snapshot. extension.rs:271 invokes turn-start invalidation; :655-660 handles human input; runtime/tool handle goal mutation, clear, stop and resume. Core goal_admission.rs rechecks pending revision at admission and at publication under the receipt/mail locks; runtime holds its goal permit through read/start. Hosted stale-revision mutant job 114617661351 exits 100 on pacing_stale_ticket_rejected_on_revision_change. Fast-human/reuse/claim tests pass in small. Eight invalidation causes are helper-entry evidence; note_release still has no production caller and is not presented as a wired release-dispatch proof. No new stale-admission mechanism established.",
      "reported_by": "TASK-261012-18lf7s"
    },
    {
      "row": "blocker order and waiting turns",
      "result": "held",
      "attack": "Narrow the actual EmptyResponse blocker for pacing-enabled automatic turns; require third-empty blockage and silence beyond the next deadline.",
      "evidence": "extension.rs:380-387 still handles EmptyResponse before :423-429 records pacing. New core goal_pacing_empty_blocker_runs_before_rescheduling passes in 0.945s on snapshot job 114617661821 with pacing enabled: immediate first, 60s second, 120s third, Blocked, no armed deadline, exactly 3 requests and still 3 after +241s. Narrowing mutant pacing_blocker_skipped_for_paced_turns replays to a1dba7bb and fails this direct killer on every hosted attempt (job 114617661324, exit 100). Waiting-turn unit exercises real accounting and app-server poll messages are nonempty. Previous A-F1 and F1-blocker-mutant-proxy proof gap is closed.",
      "reported_by": "TASK-261012-18lf7s"
    },
    {
      "row": "transient state",
      "result": "held",
      "attack": "Try serialization of streak/timers, resume after accumulated quiet turns, completion refreshing quotas and undisclosed restart reset.",
      "evidence": "All new pacing state is private in-memory WaitState, without rollout/config/schema serialization. note_resume (:762-774) clears predecessor/streak/tickets/deadline/check-in quota; restore_after_resume reconciles goal then resets state. Hosted small pacing_resume_restarts_at_floor_and_resets_quotas passes; existing exhausted-allowance/late-completion coverage and static empty-snapshot branch preserve check_ins_used on completion. Restart allowance reset and immediate first post-resume continuation are disclosed. No separate public restart with saved nonzero pacing streak or persistence-narrowing mutant supplied; no stronger claim made.",
      "reported_by": "TASK-261012-18lf7s"
    },
    {
      "row": "no model-visible change",
      "result": "held",
      "attack": "Search scheduling paths for new prompt/history/context fragments or warnings and inspect all four public poll requests.",
      "evidence": "Pacing changes policy state, runtime scheduling and tracing only. Wait returns before existing continuation_steering_item construction; no scheduling fragments or history rewrite added. Hosted app-server test checks all four requests for pacing/PacingTicket/continuation_schedule/streak and unwanted exec_completion markers; hosted small no-warning test passes. Marker absence alone is weaker than arbitrary history equality; source diff supplies the complementary bounded inspection. No new context item/schema surface introduced.",
      "reported_by": "TASK-261012-18lf7s"
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "attack": "Apply every supplied mutant to the exact candidate through a temporary index, compare hosted commit trees, then check intended killer and real runner exits.",
      "evidence": "6/6 apply checks exit 0; all six computed mutant trees exactly match GitHub git/commits tree values. Required five families now covered 5/5 (reset, cap, stale revision, cancellation, direct blocker), plus entry-rule mutant. Each selected hosted killer lane exits 100, expected-red; none is reported passing. Model requests are assertions in snapshot tests: core pacing 2; core empty blocker 3; app-server polls 4; public wake cases 4/6; helper tests 0. Aggregate mutant-run model-request total remains unknown. Hosted snapshot jobs are green; overall workflow is failure because negative mutant jobs are intentionally red.",
      "reported_by": "TASK-261012-18lf7s"
    },
    {
      "row": "placement and size",
      "result": "broken",
      "attack": "Inspect ownership, public API, production test-only plumbing, new-module size and cumulative-versus-revision diff.",
      "evidence": "New continuation_schedule.rs is private with explicit exports and 148 lines; scheduling remains in goal, with no new core pacing dependency. A2-F1: exported pacing_disabled_by_env and PACING_DISABLED_ENV_VAR are a test-only ambient override in the production start path. Documentation does not restrict deployment consumption. background_wait.rs grows from 601 to 923 lines and carries most stateful scheduling; extraction remains an organization advisory. CR base-to-candidate is cumulative 31 paths, +3900/-34 including accepted observation work; rev1-to-rev2 is only 2 test paths, +214/-28, zero production change. This panel does not misattribute inherited core hooks to rev2.",
      "reported_by": "TASK-261012-18lf7s"
    }
  ],
  "free_hunt": []
}
```
