# Merged review verdict — TASK-260929-csyzcj CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261009-195ug2_panel-verdict.md` (changes_requested), `TASK-261009-12vy98_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "interrupted-fragment-outside-context",
      "row": "child state transitions",
      "invariant": "Repository model-visible-context rule 6: every newly injected fragment must be defined as a struct in core/context and implement ContextualUserFragment.",
      "mechanism": "codex-rs/core/src/session_prefix.rs:45-51 adds a raw format! renderer for the new INTERRUPTED fragment rather than a core/context struct/ContextualUserFragment implementation. core/src/agent/control/completion.rs:95-122 calls it and packages the resulting String into queue-only InterAgentCommunication. protocol/src/protocol.rs:883-906 copies plaintext content into AgentMessage model input; core/src/session/mod.rs:4001 records it. There is no intervening typed fragment conversion. Existing completion/message types under core/context implement the required trait; neither has an INTERRUPTED variant. This is a statically reproduced architecture/contract bypass, not a claim that an Interrupted runtime wake was executed or failed.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/session_prefix_tests.rs",
          "command": "git grep -n -F 'Agent interrupted. Its turn ended without a final answer' e8eef4f44743b4a6d256e610f91527e715ae042b -- codex-rs/core/src/context",
          "expected_failure": "Exit 1 (observed): no core/context definition of the new fragment. Paired candidate source read confirms the string exists in session_prefix.rs:50 and is called by completion.rs:99. This is a source-contract reproduction, not a Rust test.",
          "pinned_blobs": [
            "ccb9ac2e6397cf6a4ae8d4032380cd468fc00a53",
            "88c939fb107fccc3b6e93eb36e0be1560b3a3f99",
            "3a1b6ad7a7257c61f5355c260c3323b5b026c859"
          ]
        },
        {
          "test_file": "codex-rs/core/src/session_prefix_tests.rs",
          "command": "git grep -n -F 'format_inter_agent_interrupted_message' e8eef4f44743b4a6d256e610f91527e715ae042b -- codex-rs/core/src/context",
          "expected_failure": "Exit 1 (observed): no delegation from core/context. Source inspection reported raw_format_macro=true, contextual_fragment_delegation=false, context_definition_hits=[].",
          "pinned_blobs": [
            "ccb9ac2e6397cf6a4ae8d4032380cd468fc00a53",
            "88c939fb107fccc3b6e93eb36e0be1560b3a3f99",
            "3a1b6ad7a7257c61f5355c260c3323b5b026c859"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "requested_change": "Define the interrupted fragment under core/context with ContextualUserFragment and route production formatting through it. Add the mandatory real-interruption integration coverage on this leaf: registered parent gets exactly one queue-only notice/model request per Running -> Interrupted transition; ordinary parent remains quiet; no success claim and global is_final unchanged. Run a narrowing mutant on the production Interrupted delivery guard, not only on the string formatter.",
      "reported_by": [
        "TASK-261009-195ug2"
      ]
    }
  ],
  "notes": [
    "[TASK-261009-195ug2] {'id': 'interruption-routing-coverage-gap', 'text': 'AC7 production behavior remains unknown. Exact candidate grep for interrupt_agent|abort_all_tasks|TurnAbortReason|INTERRUPTED in goal_native_wait.rs exits 1. Only session_prefix_tests.rs:39 checks notice wording; producer results coverage map explicitly admits the real-abort once-per-transition gap. A passing formatter mutant is not proof of parent-marker eligibility, queue-only delivery or deduplication. Requested public-entry test/mutant is named in the finding; no runtime failure is inferred.'}",
    "[TASK-261009-195ug2] {'id': 'lifecycle-concurrency-unverified', 'text': 'Static interleaving worth targeting: pause continue_if_idle after inspecting Running, disable or stop the runtime, then release registration. runtime.rs:714-730 does not recheck lifecycle after the await; synchronous set_enabled(false)/stop already removed the marker. A second interleaving is old clear dropping its permit before asynchronous cleanup (runtime.rs:449-450), concurrent new active-goal registration, then old cleanup removing the new own marker. These were NOT executed; retain as suspicions. Request deterministic registration-vs-disable/stop and old-clear-vs-new-goal fixtures, not a separate research/harness leaf.'}",
    "[TASK-261009-195ug2] {'id': 'lifecycle-and-resume-evidence-bound', 'text': 'Producer reports 9/9 AC rows mapped but only 5/9 fully driven and 4/9 partial (AC5/7/8/9). Check-in units prove evaluation/ticket consumption, not live marker reinsert, exhausted retention and late queue-only model wake. restore_thread_runtime_after_resume against an injected in-memory marker is not full resume_thread_with_history with rendered SleepItem plus unloaded child. Add targeted native-child fake-time and full-resume cases or keep those behaviors explicitly unknown.'}",
    "[TASK-261009-195ug2] {'id': 'context-size-bound-unverified', 'text': 'The new formatter hard-codes a small payload but interpolates two AgentPaths without a local cap. AgentPath validators in the exact candidate protocol/src/agent_path.rs:125-180 constrain syntax, not length. Short-path approx_token_count unit coverage does not establish a hard item bound. No long-path public-entry reproduction ran, so >1k/P0 or >10k claims are not asserted; request boundary coverage if long task names are supported.'}",
    "[TASK-261009-195ug2] {'id': 'dependency-and-size-review', 'text': 'Diff is 1,665 insertions + 16 deletions over 26 files, exceeding repository 800-line guidance; 728 lines are one integration fixture file. Most growth is tests. Smallest plausible review stage separates typed owned-child inspection/atomic remove_if from goal wait wiring, subject to the orchestrator retaining coherent dependencies. Cargo.toml/Cargo.lock add the already-workspace codex-extension-items edge; MODULE.bazel.lock is unchanged. Whether bazel-lock-update ran or produced no drift is unknown from the attached gate summary; do not infer a Bazel failure.'}",
    "[TASK-261009-195ug2] {'id': 'reuse-and-no-source-writes', 'text': 'Hosted evidence is reused from task-scoped precheck 5 exactly bound to candidate tree, not rerun by this panel. No cargo, just, build, Rust suite, or mutant execution was performed. All source-task access was read-only; no accept/reject/status/handoff/resource write on TASK-260929-csyzcj.'}",
    "[TASK-261009-12vy98] note-finding PANELB-1: GoalRuntimeHandle::release_native_wait (codex-rs/ext/goal/src/runtime.rs, pub) has no production caller and no GoalService forwarding; the only invocation in the candidate tree is the suite test goal_wait_removed_on_clear_release_and_resume. The mechanism itself (check-in epoch reset plus conditional owned-id remove) is implemented and executed by that test, so no removal behavior is broken; the AC5 release trigger is reachable only by external holders of the runtime handle until a production caller wires it.",
    "[TASK-261009-12vy98] Producer-disclosed partial coverage accepted as stated residual risk: check-in reinsert with paused clock plus live child; exhausted-keep plus late wake with live child; disable/stop dedicated integration; real-abort once-per-transition; non-default inherited-settings assert; second-child-mid-turn full integration; full resume_thread_with_history with rendered SleepItem. Each invariant was additionally verified by code reading in this review.",
    "[TASK-261009-12vy98] PANELB-1 is advisory: release_native_wait is public, implemented, and tested; only production wiring is absent.",
    "[TASK-261009-12vy98] The AC1 suite-test doc comment claims inherited-settings coverage but asserts no settings; preservation was verified here by reading the shared wake path (queue-only mail selects no new task settings; turn built from thread defaults), not by that test.",
    "[TASK-261009-12vy98] Inspection errors fail open: a failed inspection leaves any pre-existing marker in place (late mail can still wake) and the error propagates to a warn log with retry at the next idle, which self-heals. This is the safe direction, not a finding.",
    "[TASK-261009-12vy98] No builds or tests were executed locally (forbidden: serialized shared build target); all execution evidence is hosted relux-ci on the exact candidate tree plus static attack.",
    "[TASK-261009-12vy98] Read-only on TASK-260929-csyzcj: only q and resource get were used there; no accept, reject, status, handoff, or other write."
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "Hosted candidate run 37855177143: goal_wait_registers_marker_and_wakes_on_child_completion drives set_thread_goal -> continue_if_idle -> native V2 child completion -> pending-work wake and asserts an outbound model request, silence before wake and removal on admitted turn start. Narrowing ignore_native_pending (37855194303) fails this public-entry test. One SleepItem is stored per TypeId, not per child.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md",
      "reported_by": "TASK-261009-195ug2"
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Hosted skip_failed_lookups mutant 37855265071 is killed by owned_children_inspection_propagates_failed_lookups (loaded, unknown Err, known Unloaded). Candidate OwnedChildInspection::is_pending_native_work admits only PendingInit/Running; runtime.rs:686-710 checks active goal and host capability before registration and propagates the entire read error. Bound: negative inspection coverage is through the narrow inspection API, not a full goal-start fixture with backend failure.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md",
      "reported_by": "TASK-261009-195ug2"
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Hosted insert_after_mail_check mutant 37855212822 is killed by goal_wait_latch_closes_completion_before_registration. Exact candidate test uses two real V2 children, holds registration before insert, confirms completion mail enqueued, releases once, forbids a second idle pass, and asserts mail-wake request plus absence of goal continuation. Every race-specific wait is bounded. Permit sharing at runtime.rs:736-742 closes the earlier recheck self-deadlock.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md",
      "reported_by": "TASK-261009-195ug2"
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "Hosted insert_clobbers_one_foreign (37855230691) and unconditional_remove (37855282786) fail goal_wait_preserves_foreign_sleep_across_register_and_turn_start as well as helper tests. Candidate ExtensionData::remove_if (state.rs:142-153) evaluates predicate/removes under the same mutex; registration/removal preserves a foreign clock-wait-1 marker across idle and turn start.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md",
      "reported_by": "TASK-261009-195ug2"
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "evidence": "Hosted goal_wait_removed_on_clear_release_and_resume drives public release_native_wait, GoalService::clear_thread_goal and restore_thread_runtime_after_resume. AC1/latch assert turn-start removal. Small native_pending_exhausts_checkins_then_waits_without_deadline demonstrates the 3-ticket bound. Held is limited to these attacks: native check-in removal/reinsert and exhausted-marker late wake, disable/stop interleaving, and full rollout resume are not established by the supplied integration fixtures.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md",
      "reported_by": "TASK-261009-195ug2"
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "Hosted goal_wait_registers_marker_and_wakes_on_child_completion asserts 500 ms no parent event after registration, no goal-wait: string in the wake body and no current_time. Static insertion only stores SleepItem; it calls no event/history/reminder API. Bound: CurrentTimeReminder is disabled in this fixture, so it cannot prove an enabled reminder schedule is unchanged.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md",
      "reported_by": "TASK-261009-195ug2"
    },
    {
      "row": "child state transitions",
      "result": "broken",
      "evidence": "The static model-context contract attack reproduced interrupted-fragment-outside-context (below). Hosted interrupted_claims_success mutant 37855247950 proves formatter wording only. Hosted two-child latch proves a second Running child remains pending, and existing pending_input::queue_only_agent_mail_wakes_sleeping_root_with_previous_turn_context pins a non-default cyber setting on the same wake scheduler. No supplied goal-wait integration test drives a real Interrupted transition or once-per-transition routing. That missing behavioral fixture is not reported as a reproduced runtime failure.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md",
      "reported_by": "TASK-261009-195ug2"
    }
  ],
  "free_hunt": [
    "[TASK-261009-195ug2] {\"budget_minutes\": 3, \"started_at_utc\": \"2026-10-08 23:39:59\", \"ended_at_utc\": \"2026-10-08 23:41:08\", \"examined\": [\"new model-visible interrupted fragment ownership/type\", \"registration versus synchronous disable/stop\", \"old clear versus new registration\", \"dependency lock and total diff size\", \"long canonical path bounds\"], \"findings\": [\"interrupted-fragment-outside-context\"], \"unexecuted_suspicions\": [\"lifecycle-concurrency-unverified\", \"context-size-bound-unverified\"]}",
    "[TASK-261009-12vy98] {\"probe\": \"permit-share deadlock-fix soundness (precheck-2 production bug)\", \"result\": \"no-finding\", \"evidence\": \"start_task awaits emit_turn_start_lifecycle BeforeTaskRegistration before spawning the task future, and goal on_turn_start consumes the shared GoalTurnStartPermit via remove, so the recheck-time permit share cannot self-deadlock and the lease drop is a no-op when consumed.\"}",
    "[TASK-261009-12vy98] {\"probe\": \"lost-wake interleave between insert/recheck and completion enqueue\", \"result\": \"no-finding\", \"evidence\": \"Two-flag argument over the marker slot and the mailbox queue: an enqueue that observes no marker must precede the insert, which precedes the recheck mail scan in program order, so the recheck observes the enqueued mail; an enqueue after the insert wakes via its own marker check. No lost-wake schedule exists.\"}",
    "[TASK-261009-12vy98] {\"probe\": \"goal-wait: namespace squatting by foreign SleepItem producers\", \"result\": \"no-finding\", \"evidence\": \"The only production SleepItem stored in extension data is the goal marker; the clock sleep tool renders history-only items keyed by call_id and never stores them. No foreign producer can mint a goal-wait: id in this tree.\"}",
    "[TASK-261009-12vy98] {\"probe\": \"side-effect scope of Interrupted reaching turn_finished\", \"result\": \"no-finding\", \"evidence\": \"turn_finished delegates solely to notify_parent_of_terminal_turn, whose Interrupted branch only sends the gated queue-only notice; ordinary parents (no owned marker) return before any send. No recording, metric, or scheduling side effect is added for Interrupted.\"}",
    "[TASK-261009-12vy98] {\"probe\": \"stale evaluate_continuation production callers missing native_pending\", \"result\": \"no-finding\", \"evidence\": \"All evaluate_continuation callers are tests; the sole production goal-continuation evaluation site (continue_if_idle) uses evaluate_continuation_with_native_pending. No Proceed-instead-of-Wait bypass path remains.\"}",
    "[TASK-261009-12vy98] {\"probe\": \"Cargo.lock delta review\", \"result\": \"no-finding\", \"evidence\": \"The lockfile delta is exactly one line: the new codex-extension-items dependency on the goal crate, matching its Cargo.toml change. No version drift.\"}"
  ]
}
```

## Recording reviewer confirmation

RUN-261009-2fe57d, 2026-10-09: read both authoritative panel outcomes and this merged verdict. Recording verdict: changes_requested, CR-TASK-260929-csyzcj-1 revision 1, candidate e8eef4f44743b4a6d256e610f91527e715ae042b.

Merge validation executed with Python (exit 0): **7/7 surface rows** appear exactly once in the specified order and preserve the worst panel result (**6 held / 1 broken**); **1/1 blocking findings** retain every original field and reproduction; **1/1 advisory findings** are explicitly preserved as the PANELB-1 note-finding, consistent with their nonblocking severity; **12/12 panel notes** and both panels' free-hunt records are preserved. PANELB-1 is carried in notes rather than the blocking findings array; its original structured reproduction remains in the linked panel B outcome. No new finding or technical re-review was performed.

Source outcomes: TASK-261009-195ug2_panel-verdict.md on TASK-261009-195ug2 and TASK-261009-12vy98_panel-verdict.md on TASK-261009-12vy98, fetched via task-board resource get (exit 0 each). Merged verdict fetch: exit 0. Goal query: exit 0, run is not goal-bound; directive query: exit 0, none recorded. Hosted precheck evidence is accepted from the panels as already-attached evidence; no build, test or mutant was rerun locally. Product code, branch and normal index were untouched.

Outcome-scoped logbook: Panel A requests changes while Panel B accepts; the merge correctly routes rework because child state transitions has the blocking interrupted-fragment-outside-context finding. Producer must use the required core/context typed fragment and add real-interruption integration coverage plus a narrowing production-delivery mutant. Advisory release wiring and all stated verification bounds travel with this verdict.
