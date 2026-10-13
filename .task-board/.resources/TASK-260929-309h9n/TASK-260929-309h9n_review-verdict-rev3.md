# Merged review verdict — TASK-260929-309h9n CR revision 3 (tb-R141 / R132 merge)

Verdict: **accept**

Panel outcomes: `TASK-261012-3f8dah_panel-verdict.md` (accept), `TASK-261012-1tzry5_panel-verdict.md` (accept), `TASK-261012-3laumx_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "B3-N1",
      "row": "placement and size",
      "invariant": "An explicit production policy ships with accurate, code-local bounds; a stored config value must not silently diverge from effective behavior (follows the A2-F1 accurate-bounds ask).",
      "mechanism": "The goal_continuation_pacing flag is read once in GoalExtension::on_thread_start (extension.rs:126,190-194). on_thread_resume (extension.rs:199-217) does not re-read it, by design, and resume preserves the thread-start choice: note_resume clears streak/predecessor/deadlines/quotas but never touches pacing_enabled (background_wait.rs:762-777), so there is no silent resume-disable. on_config_changed (extension.rs:252-264) re-runs goal_config(new_config) and inserts the full new GoalExtensionConfig into thread_store, but applies only `enabled` to the runtime: the stored continuation_pacing diverges from the effective value after a mid-thread toggle. Benign today because the sole thread_store GoalExtensionConfig reader takes max_goal_token_budget only (extension.rs:707-710) and no production path re-reads continuation_pacing. The 'read at thread start only' bound is documented in TASK-260929-309h9n_results.md ('Production policy and bounds'), but the field's in-code doc (extension.rs:67-68) is one line with no thread-start-only note. The rework brief explicitly scoped out a mid-thread toggle ('do not add a new mid-thread toggle in this rework; say explicitly whether ... re-read it') and the producer disclosed the behavior, so this is a note, not a defect: suggest a one-line doc comment on the field.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/extension.rs:199-217,252-264; codex-rs/ext/goal/src/background_wait.rs:762-777",
          "command": "git show 3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/ext/goal/src/extension.rs | sed -n '199,217p;252,264p'; git show 3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/ext/goal/src/background_wait.rs | sed -n '762,777p'",
          "expected_failure": "No failure: static witness, command exit 0. Resume preserves pacing_enabled; config-update stores but does not apply continuation_pacing; no in-code thread-start-only doc on the field.",
          "pinned_blobs": [
            "3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/ext/goal/src/background_wait.rs (candidate file) blob 185d2042b7d392d9794d9a25fd21ad76b5eacc56",
            "3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/ext/goal/src/extension.rs (candidate file) blob 070b4f4484aaa33b03ac6dd629b37b94367d5771"
          ]
        },
        {
          "test_file": "codex-rs/ext/goal/src/extension.rs:707-710 (sole stored-config reader)",
          "command": "git grep -n 'get::<GoalExtensionConfig>' 3c5cbffcc73270bec86364ab42550441c87f933c -- codex-rs",
          "expected_failure": "No failure: static witness, command exit 0. Exactly one reader site, and it takes max_goal_token_budget only, so the stored-but-unapplied flag value is unread.",
          "pinned_blobs": [
            "3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/ext/goal/src/extension.rs (candidate file) blob 070b4f4484aaa33b03ac6dd629b37b94367d5771"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-1tzry5"
      ]
    },
    {
      "id": "DELTA3-N1",
      "row": "one live timer",
      "invariant": "B2-N1 / D-N1: retain failed first attempts and bound attribution; aggregate green is not evidence of reliable first-try check-in behavior.",
      "mechanism": "Precheck 9 still retries scheduled_checkins_fire_through_production_runtime_under_paused_time: TRY 1 FAIL 10.515s, panic core/tests/common/lib.rs:393 timeout waiting for event; TRY 2 PASS 1.321s. The candidate fixture supplies continuation_pacing:false, so removal of pacing from this fixture did not eliminate the flake. It keeps a stalled Armed receipt throughout, and CheckInTimer is unchanged by the scheduler delta. The fixture advances paused time after TurnComplete/manual idle without awaiting the next arm; teardown synchronization remains a plausible lead, not a proven cause. The report claims only aggregate lane success and explicitly avoids a precheck-9 first-try claim. No deterministic production defect or new pacing regression established. Keep this as an informational reliability follow-up, not grounds to reject this delta.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs:115-119,199-320 at 3c5cbffcc73270bec86364ab42550441c87f933c",
          "command": "gh run view 38232681612 --repo ivanopcode/codex --job 114758681056 --log",
          "expected_failure": "Executed retrieval exit 0. Observed hosted TRY 1 FAIL (10.515s), TRY 2 PASS (1.321s); individual failed test process numeric exit is not printed, so unknown. Snapshot core aggregate success: 5131 passed, 2 flaky, 11 skipped. No local tests run.",
          "pinned_blobs": [
            "3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/core/tests/suite/goal_background_wait.rs (candidate file) blob bfc0f0923af4f108e593522fb61d12a58cfbbf35"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs::scheduled_checkins_fire_through_production_runtime_under_paused_time",
          "command": "HOSTED REQUEST, NOT RUN: just test -p codex-core -E 'test(scheduled_checkins_fire_through_production_runtime_under_paused_time)' with retries disabled and arm/teardown tracing; compare a fixture variant awaiting the fresh arm after each TurnComplete",
          "expected_failure": "No failure presumed; record per-attempt failure rate and identical 3-request/quota/warning assertions. Requested diagnostic exit unknown.",
          "pinned_blobs": [
            "3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/core/tests/suite/goal_background_wait.rs (candidate file) blob bfc0f0923af4f108e593522fb61d12a58cfbbf35"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "D-N1",
      "reported_by": [
        "TASK-261012-3laumx"
      ]
    }
  ],
  "notes": [
    "[TASK-261012-3f8dah] Independent non-recording panel A, CR-TASK-260929-309h9n-3 revision 3. accept is this panel opinion; only the recording reviewer may accept/reject the source CR. No mutation, note, attachment, status or handoff was performed on TASK-260929-309h9n.",
    "[TASK-261012-3f8dah] Exact replay and source identity: base 67789e1ee29e766e446c7f33feb61561d51f94db, candidate 3c5cbffcc73270bec86364ab42550441c87f933c. Upstream P3-1 content is excluded from the reviewed delta. No builds/tests/fmt or code edits by this panel.",
    "[TASK-261012-3f8dah] Accepted execution evidence is TASK-260929-309h9n_hosted-precheck-9.md and results, bound to this exact tree; 4/4 successful lanes and 7/7 mutant kills. Reported lane conclusions are not individual process exit codes. No invented mutant/test exit codes or first-try claim. Prior-tree prechecks 6/8 are context only, not validation of this tree.",
    "[TASK-261012-3f8dah] Flag policy is read at thread start only, is default on, and can be opted out via [features] goal_continuation_pacing=false. This is documented in the producer outcome. Current source field docs are shorter; they do not promise dynamic reconfiguration.",
    "[TASK-261012-3f8dah] P4a fixture decoupling is present (continuation_pacing=false). Historical precheck-6 check-in retry and precheck-8 unrelated retries remain disclosed; precheck 9 gives no retry detail, so reliability beyond that run remains unknown.",
    "[TASK-261012-3f8dah] No blocking findings. Local logbook executable is unavailable (exit 127), and no logbook connector is exposed. The task-scoped outcome contains the logbook entry and this panel task receives the same handoff note; no source-task write is used as a substitute.",
    "[TASK-261012-3f8dah] Installed project-management skill reviewer reference was absent at its referenced path (cat exit 1); a bundled role copy was readable but lacked a review-round contract. The explicit supplied panel contract governs: all 9 rows swept once, then bounded free hunt, with exact-tree hosted public-entry attacks accepted.",
    "[TASK-261012-3f8dah] Successor RUN-261012-a8e65c preserves predecessor sweep/free-hunt and hosted evidence; it directly reran temporary-index replay, whitespace/static schema/host/flag checks, and empty-delta mini-hosted-gate (exit 0). Prior handoff gate exit 1 is disclosed. Text report is persisted as a panel outcome; repository delta is empty. No original-task write or local build/test.",
    "[TASK-261012-3f8dah] free-hunt: After the 9-row sweep, bounded static hunt covered three additional paths: (1) committed plan/spawn/file observations versus model text and wrapper success; (2) unavailable notification host plus default pacing and pending-provider installation; (3) external integration surfaces and raw delivery status. No additional blocking mechanism identified.",
    "[TASK-261012-3f8dah] free-hunt: Observation path: PlanHandler publishes parsed args then notify_plan_committed; extension records actual step transitions, excluding explanation-only/identical plans. Applied FileChange requires Completed; accepted collab deliveries require Completed or Started/Interacted. V1 spawn/send changes distinguish accepted delivery from subsequent child liveness, keeping agents_states. Model text, ordinary exec/tool success, polling and wrapper success cannot reset the streak. Candidate tests state_change_observations and code_mode supply production-oriented evidence; no new local execution claimed.",
    "[TASK-261012-3f8dah] free-hunt: Host availability path: Core session.rs:1816-1831 publishes PendingWorkProvider unconditionally, independently of AsyncNotificationSupport. Thus pacing on an unavailable-notification host does not treat absence of the notification capability as absence/failure of the provider. Read failure remains WaitOnReadFailure/Wait, not empty. Only app-server production installs goal extension; standalone exec/tui have no alternate GoalExtensionConfig constructor in this tree. This is a bounded source inventory, not a claim about future external embedders.",
    "[TASK-261012-3f8dah] free-hunt: Integration surface path: feature is an additive config key in both maps; no new CLI parameter, app-server RPC shape or pacing rollout field. Collab raw item status semantics intentionally change from child liveness to delivery outcome; wire enum/shape and agents_states remain unchanged, with accepted/refused status tests. No extra external-schema change found. Inherited core publication locking is unchanged by this CR delta.",
    "[TASK-261012-3f8dah] free-hunt: Remaining limits: no local runtime/race/mutant execution; no fresh generated Rust schema run; exact-tree hosted report is summarized and does not expose individual process exits/retries. Held results apply to the named attacks and static paths, not exhaustive timing or platform coverage.",
    "[TASK-261012-1tzry5] Provenance: replay plus static attack only. No cargo, just, build, or Rust test command was run (panel rule: shared build target serialized). Executed evidence is hosted relux-ci run 38232681612 on the EXACT candidate tree 3c5cbffc (precheck 9: lint/small/core/app-server 4/4 green, 7/7 mutants killed), accepted from TASK-260929-309h9n_hosted-precheck-9.md and the rev3 validation log (mini-hosted-gate exit 0).",
    "[TASK-261012-1tzry5] Rev2-to-rev3 production delta on scheduling files is purely subtractive plus the flag swap: continuation_schedule.rs loses only the env const/fn block; background_wait.rs loses only disable_pacing; extension.rs swaps the env read for the flag read plus the E0382 copy-before-move. All rev2 held-row mechanisms were re-verified present in 3c5cbffc, not assumed carried.",
    "[TASK-261012-1tzry5] Trunk content from the base refresh (P3-1: ContextContributor impl, waiting_capability_fragments, related imports in extension.rs) is NOT under review and was not swept as Story content.",
    "[TASK-261012-1tzry5] A2-F1 / B2-N2 / D-N2 closure: the ambient CODEX_GOAL_PACING_DISABLED switch, its public reader/exports, and disable_pacing are fully removed (whole-tree greps exit 1), replaced by Feature::GoalContinuationPacing (Stable, default on) mapped by the single production host. The explicit-policy remedy the rev2 panels asked for is implemented and disclosed.",
    "[TASK-261012-1tzry5] B2-N1 hardening verified: core goal_background_wait fixture sets continuation_pacing:false and asserts !is_pacing_enabled(); precheck 9 core lane green. The precheck-6 P4a first-try failure and precheck-8 unrelated retries remain disclosed history; precheck 9's report gives no retry details, so no first-try claim is made.",
    "[TASK-261012-1tzry5] Carried bounds (decided, not findings): AC1 completed-count n vs implemented upcoming-ordinal pacing_delay(streak+1) wording gap; unit inventory is now exactly 22 (23 minus the removed env test), matching results; per-mutant failing lanes reported small/core only (no per-mutant app-server execution evidenced either way); note_release still has no production caller; marker-scan (4-request body scan) is weaker than full history equality; aggregate mutant-run model-request totals unknown.",
    "[TASK-261012-1tzry5] Flag-mutant killer direction: pacing_feature_flag_ignored is killed through the public runtime entry by core background_wait_inactive_on_unavailable_host_auto_continues, which asserts !is_pacing_enabled() under a continuation_pacing:false fixture (fails under || true). The four app-server .disable_feature opt-out sites are additional policy coverage whose back-to-back timing passes in the green app-server lane.",
    "[TASK-261012-1tzry5] No write of any kind was made on TASK-260929-309h9n (no accept/reject/withdraw/status/handoff/note/resource).",
    "[TASK-261012-1tzry5] free-hunt: {\"family\": \"ambient or env-based production switch remnants\", \"result\": \"None found. Whole-tree greps for the env name, reader, and const exit 1; no std::env use remains in ext/goal/src. The test hook is fully excised, not re-pointed.\"}",
    "[TASK-261012-1tzry5] free-hunt: {\"family\": \"flag reachability on every host path\", \"result\": \"Complete. app-server/src/extensions.rs is the only production GoalExtensionConfig construction; core and ext/goal constructions are all test fixtures with explicit values. No host can construct the config without choosing pacing behavior (bool field, no Default bypass).\"}",
    "[TASK-261012-1tzry5] free-hunt: {\"family\": \"config.schema.json drift vs generated shape\", \"result\": \"No drift. Both features maps carry goal_continuation_pacing with the exact sibling shape and correct alphabetical placement; the hosted core lane validates the fixture and is green.\"}",
    "[TASK-261012-1tzry5] free-hunt: {\"family\": \"mid-thread toggle silently ignored\", \"result\": \"Bounded as note B3-N1: resume preserves the thread-start choice (no silent disable); config-update stores-but-does-not-apply (benign, value unread); results.md documents read-at-thread-start-only; in-code field doc lacks the note.\"}",
    "[TASK-261012-1tzry5] free-hunt: {\"family\": \"rev2->rev3 production delta beyond the brief\", \"result\": \"None. Scheduling-file delta is the env-block deletion, disable_pacing deletion, and flag swap plus E0382 fix. extension.rs additionally carries P3-1 trunk imports/impl (ContextContributor), which is out-of-scope trunk content, not Story behavior.\"}",
    "[TASK-261012-3laumx] Non-recording DELTA review. Every finding in merged rev2 was examined before same-class and regression sweeps. No write of any kind was made to TASK-260929-309h9n; no accept_cr/reject_cr/withdraw_cr/status/handoff there.",
    "[TASK-261012-3laumx] A2-F1 fixed through its explicit-production-policy alternative: default-on Stable feature plus ordinary config opt-out, removed test-only env reader and ambient unit assumption. B2-N2 and D-N2 same switch/API concerns separately checked and resolved; not collapsed into the flake. B2-N1 fixture isolation implemented; D-N1 attribution remains unknown and is carried as DELTA3-N1. Rev1 direct blocker proof and narrow app-server opt-outs retained.",
    "[TASK-261012-3laumx] Policy bounds: [features] goal_continuation_pacing=false restores immediate consecutive automatic continuations. Read at runtime thread creation/on_thread_start; in-place config updates and on_thread_resume do not apply a new pacing value. A new resumed runtime may run on_thread_start with its loaded config before on_thread_resume. Results Production policy and bounds / Disclosed bounds state start-only, no mid-thread toggle. Feature API field docs could repeat that lifecycle for host implementers; this is a documentation recommendation, not an alleged unsupported toggle.",
    "[TASK-261012-3laumx] Scope pinned to base 67789e1e and candidate 3c5cbffc. Trunk P3-1 is excluded. Old-base rework diff af312067 -> eb655488 checked separately; import-only refresh preserved PlanCommitInput and PromptFragment and production flag mapping. No candidate code was edited.",
    "[TASK-261012-3laumx] Execution distinction: this panel executed temporary-index replay, static Git/JSON checks, mutation applicability/tree binding and hosted metadata/log retrieval. No cargo, just, build, Rust test, new hosted run or new mutation execution. Hosted evidence was accepted after independently verifying exact identities, not rerun locally.",
    "[TASK-261012-3laumx] Coverage 9/9 surface rows, one result each; 7/7 supplied mutation trees bound to executed red hosted lanes. Hosted snapshot core 5131 passed (2 flaky), 11 skipped; small 1489 passed, 1 skipped; app-server 1834 passed, 2 skipped. 22 pacing unit functions/pass records after removal of the ambient-env test (rev2 had 23). Snapshot core other retry: permission_request_hook_allows_exec_command_without_user_approval. No additional first-try reliability claim.",
    "[TASK-261012-3laumx] Blind spots retained: no dedicated public-entry quiet-timer wake/stale-ticket attack, full-history equality, Windows/foreign-exec replay, clock rollback experiment or public saved-streak restart in this panel. note_release has no production caller; receipt/mail revision checks provide indirect stale-admission refusal. Generator was inspected statically; just write-config-schema was not executed.",
    "[TASK-261012-3laumx] Available project-management SKILL.md was read; its referenced .roles/reviewer/role.md is absent from that installed package. Used the explicit panel/task review-round contract (sweep all rows, bounded free hunt, truthful evidence), without treating missing file as absent review obligations.",
    "[TASK-261012-3laumx] free-hunt: {\"family\": \"ambient switches / host coverage / schema\", \"result\": \"No surviving ambient pacing production input found. Required typed field forces literal callers to choose policy; the sole production mapper uses feature config. Profile/global schema exact additions match generator boolean branch. No missed host bypass established.\"}",
    "[TASK-261012-3laumx] free-hunt: {\"family\": \"mid-thread config / resume / API breakage\", \"result\": \"Start-only policy matches results disclosure. on_config_changed updates Goals enablement and stored config but leaves live pacing policy; no silent dynamic toggle promised. Added public GoalExtensionConfig field requires source caller adaptation; all in-tree constructors accounted for; no app-server wire/rollout/CLI-parameter breaking shape found.\"}",
    "[TASK-261012-3laumx] free-hunt: {\"family\": \"wall-clock / release / read failure\", \"result\": \"SystemCheckInClock wall-clock rollback may reject a single fired claim without rearming; timer code predates and is unchanged by this delta, so inherited unverified risk, not new proven regression. Requested future attack: pacing_clock_rollback_rearms_until_deadline through production timer/runtime. Read failures return WaitOnReadFailure/Wait, never empty fallback. No release caller claimed.\"}",
    "[TASK-261012-3laumx] free-hunt: {\"family\": \"P4a rework reliability / synchronized teardown\", \"result\": \"Exact snapshot repeats timeout with pacing off; DELTA3-N1 preserves the anomaly and unknown attribution. Desired hosted diagnostic is specified in reproductions. No new build run or speculative causal assertion.\"}"
  ],
  "surface_results": [
    {
      "row": "spacing and streak math",
      "result": "held",
      "evidence": "Attacked off-by-one, overflow, missing cap, and false resets. continuation_schedule.rs:49-56 saturates n-1, limits shift, checked-multiplies, and caps at 1800s; background_wait.rs:484-487 uses completed quiet streak + 1. Thus the first continuation after human/set/resume is immediate, a first quiet predecessor produces the next n=2 delay (60s), and observed change yields the 30s floor. This entry exception is documented in candidate module docs and producer results. Hosted pacing_delay_n1_n2_n3_and_cap, pacing_state_change_resets_streak_to_floor, pacing_two_polls_grow_streak; missing-cap and false-reset mutants killed. Core real runtime test goal_pacing_first_immediate_second_at_60s asserts two requests. Held for these bounds; arbitrary polling within one turn remains outside scope.",
      "reported_by": "TASK-261012-3f8dah"
    },
    {
      "row": "polls grow the streak end to end",
      "result": "held",
      "evidence": "Attacked the helper-only proof and treating get_goal success/waiting text as state change. Candidate app-server/tests/suite/v2/goal_continuation_pacing.rs:95-212 drives thread/start and thread/goal/set, then two real get_goal tool turns. It asserts two requests after turn 1, four after turn 2, first start <28s, second >=58s after prior completion, and no early third start in 8s. on_turn_stop reads the committed-observation count before finish_turn; ordinary tool success and agent text are excluded by accounting.rs:286-345. Exact-tree hosted app-server lane green; false-reset mutant killed in small/core. Request ratio is 4/4 scripted requests, two per poll turn.",
      "reported_by": "TASK-261012-3f8dah"
    },
    {
      "row": "one live timer",
      "result": "held",
      "evidence": "Attacked a second timer, replacement leakage, event pre-emption and overriding known-work deadlines. runtime.rs:604-639 and 722-731 arm only the existing CheckInTimer; check_in_clock.rs:127-169 aborts the prior slot and detaches the fired entry before callback. background_wait.rs:227-236 invokes the runtime abort hook on invalidation. Nonempty snapshots use the background gate before pacing; no pacing timer is added alongside it. Exact-tree hosted pacing_new_schedule_replaces_old_without_accumulation, pacing_event_wake_preempts_timer, pacing_invalidation_cancels_armed_timer and pacing_known_work_uses_background_wait_instead support the state machine; core pacing tests exercise the actual timer/runtime/start path; producer reports pacing-enabled app-server exec wake scenarios with 4 and 6 requests. Timer-not-cancelled mutant killed in small. Held for these paths, without a local concurrency stress execution.",
      "reported_by": "TASK-261012-3f8dah"
    },
    {
      "row": "ticket invalidation and admission",
      "result": "held",
      "evidence": "Attacked revision/generation/predecessor/reuse mismatches and the fast intervening human turn. PacingTicket binds goal, revision, predecessor, generation and cause; background_wait.rs:574-588 consumes the attempt under the state lock and refuses read failure/generation mismatch, then :632-663 checks outstanding identity, goal, revision, predecessor, nonempty pending state and reuse. Human, steering, goal mutation, clear/stop/resume invalidate; on_turn_start always invalidates. Production runtime publishes the shared admission checker before start_turn_if_idle; existing core goal_admission.rs consumes it and preserves a revision comparison at the publication linearization point. Those inherited core admission rules are inspected as dependencies, not reviewed as new trunk content. Hosted stale-revision mutant killed by pacing_stale_ticket_rejected_on_revision_change; fast-human, predecessor-change, reused-ticket and wrong-generation tests cover the additional shapes. Core/app-server verticals exercise successful ticket admission. Held for named attacks; no new generation-only public-entry mutant was executed by this panel.",
      "reported_by": "TASK-261012-3f8dah"
    },
    {
      "row": "blocker order and waiting turns",
      "result": "held",
      "evidence": "Attacked pacing that bypasses the empty blocker and conflating nonempty waiting text with emptiness. extension.rs:386-394 executes the existing EmptyResponse stop before accounting/pacing at :425-435; accounting.record_item treats nonblank assistant text as activity while observation classification excludes it. Exact-tree hosted core goal_pacing_empty_blocker_runs_before_rescheduling drives the production idle path with pacing on: 3 requests, persisted Blocked goal, no armed wait, still 3 requests after +241s. pacing_blocker_skipped_for_paced_turns was killed by that test. Small pacing_waiting_turn_is_paced_not_empty and the app-server waiting-message poll test cover the nonempty case. The blocker is tested directly, not inferred from a timing proxy.",
      "reported_by": "TASK-261012-3f8dah"
    },
    {
      "row": "transient state",
      "result": "held",
      "evidence": "Attacked rollout persistence, stale resume state and completion granting a fresh allowance. All added pacing fields are in in-memory WaitState; PacingTicket has no serialization implementation. restore_after_resume reconciles goal then calls note_resume; background_wait.rs:762-780 discards streak, predecessor, outstanding handle and deadline. First post-resume continuation is immediate, then quiet turns restart from the schedule floor. Existing background_wait completion evaluation clears deadlines without renewing check_ins_used; test completion_after_cap_wakes_without_counting_as_human_input (background_wait.rs:564-621) explicitly retains 3 consumed check-ins. Subscription/work completion is the completion meant here; explicit goal mutation has its separately defined reset. Hosted small pacing_resume_restarts_at_floor_and_resets_quotas and existing completion tests support these semantics. Producer results explicitly disclose restart resetting transient quotas and losing live observations; no stale subscription restoration is introduced.",
      "reported_by": "TASK-261012-3f8dah"
    },
    {
      "row": "no model-visible change",
      "result": "held",
      "evidence": "Attacked scheduling text injection, history items and context cache changes. All scheduling additions are host-only fields/timers; pacing Wait uses emit_warning=false, and no context/steering template or rollout shape changes appear in the delta. Existing continuation steering is unchanged. Candidate app-server poll vertical scans all 4 outbound request bodies for pacing/PacingTicket/continuation_schedule/streak and completion-fragment markers; hosted app-server lane green. Small pacing_emits_no_warnings_or_prompt_text covers warning-free schedule evaluation. Held for the scheduling leaf and named markers plus static full-delta context inspection; this is not a general claim of byte identity between all model requests.",
      "reported_by": "TASK-261012-3f8dah"
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "evidence": "Attacked patch drift, missing killers and counting unit tests as model requests. Original review run checked each of 7 patches with git apply --cached --check against the replayed candidate index: 7/7 exit 0, tree unchanged afterwards. Accepted exact-tree hosted precheck 9 reports 7/7 killed, 0 survivors, with named killers: pacing_two_polls_grow_streak (false reset); pacing_delay_n1_n2_n3_and_cap (cap); pacing_stale_ticket_rejected_on_revision_change (revision); pacing_invalidation_cancels_armed_timer (cancel); goal_pacing_empty_blocker_runs_before_rescheduling (blocker); pacing_first_continuation_after_human_turn_proceeds_immediately (entry); background_wait_inactive_on_unavailable_host_auto_continues (ignored config). The final killer is in the full goal_background_wait path selected by test(goal). Reported model requests: core quiet 2, core blocker 3 and silence, app-server polls 4 and silence, wake cases 4/6, goal units 0. Coverage ratio describes these seven submitted mutants, not all possible refusal clauses or races.",
      "reported_by": "TASK-261012-3f8dah"
    },
    {
      "row": "placement and size",
      "result": "held",
      "evidence": "Attacked leftover ambient policy, incomplete host mapping, schema drift and silently claimed mid-thread toggles. Dedicated continuation_schedule.rs is 135 lines. Scheduler stays in ext/goal and reuses the existing background-wait implementation; core production delta is thin committed-observation hooks and delivery-status fixes, with no core-to-goal production dependency. Candidate-wide grep locates exactly one production GoalExtensionConfig constructor (app-server/src/extensions.rs:84-90), which maps the Stable default-on Feature::GoalContinuationPacing. Seven other struct constructions are explicit test fixtures (pacing true in its core vertical; false in P4a/activity/backend fixtures). No old CODEX_GOAL_PACING_DISABLED/pacing_disabled_by_env/disable_pacing symbol remains (grep exit 1). Static schema diff finds only 2/2 boolean-key insertions, matching config::schema::features_schema generation for this registry entry. on_thread_start alone enables pacing; resume/config-update do not re-read it, and producer results Production policy and bounds/Disclosed bounds say so explicitly. Ignored-feature mutant is killed on exact tree. Prior ambient-switch mechanism A2-F1/B2-N2/D-N2 is closed; no new placement defect found. Full Rust schema regeneration was not run locally.",
      "reported_by": "TASK-261012-3f8dah"
    }
  ],
  "free_hunt": []
}
```
