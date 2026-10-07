# Merged review verdict — TASK-260929-2snjbb CR revision 3 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261007-3ens4c_panel-verdict.md` (changes_requested), `TASK-261007-1c6vam_panel-verdict.md` (accept), `TASK-261007-3nfu39_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "revision-recheck-before-await-window",
      "row": "admission recheck and invalidation",
      "invariant": "AC7: catch a receipt transition between the continuation check and actual turn start, by serialization or rejecting a changed revision.",
      "mechanism": "codex-rs/core/src/session/turn_input.rs:530 compares the revision, then calls start_task at :538 without carrying that revision. In core/src/tasks/mod.rs:350-370, start_task still awaits mark_turn_started, total_token_usage and active_turn.lock before record_started_turn. total_token_usage (core/src/session/mod.rs:1460-1462) acquires the independent async session-state mutex. Receipt Arm uses its own store mutex (unified_exec/completion_receipt.rs:320) and bumps its atomic revision at :466; neither the goal permit nor the active-turn reservation serializes this transition. A permissible schedule is: the late check accepts r; a callee lock suspends; reserve/Arm publishes r+1; the callee resumes and records/starts the automatic goal with no further check. Rev3 closes the preparation window but leaves the same check-before-await mechanism inside its callee. This is a pinned-source ordering witness, not a claimed executed Rust race.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3ens4c/static_attack.py (full corrected source embedded below)",
          "command": "python3 .temp/TASK-261007-3ens4c/static_attack.py admission",
          "expected_failure": "Observed exit 1 in admission-02.log: EXPECTED RED, callee prefix has awaits and no admitted revision/check. First admission-01 attempt exited 1 on a wrong field-name audit assertion and is excluded as reproduction. No Rust behavior executed. Add a deterministic test holding a callee timing/state lock after the late check, Arm via the real receipt store, release the latch and require GoalBackgroundWait with no committed/ownerless turn. Carry revision to the actual commit and serialize against receipt transitions; use a narrowing mutant that checks only the pre-callee window.",
          "candidate_tree": "16a538869452dc36d083b8ab3c3e63a1e57c7285",
          "pinned_blobs": [
            "git-blob:481ebc9deee74a3b8d84a65977096c92d4cd7cc4",
            "git-blob:f93063fd3ce2c7e5b3d25618ad21a29ac9b7f3bd",
            "git-blob:2a4707c2de74d96c1113beedf6972355b56db946",
            "git-blob:8414dcfa10c4733b08f8cf7e55fbce6b5c2d700d",
            "git-blob:be9f60e63f1b4e36006fb3424ee09a2429f5325e"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "CR-TASK-260929-2snjbb-2 / revision-recheck-before-await-window",
      "reported_by": [
        "TASK-261007-3ens4c"
      ]
    },
    {
      "id": "scheduled-checkin-regression-not-exercised",
      "row": "check-in tickets and warning",
      "invariant": "AC4/AC5 and the rev3 rework brief D: fake time alone must drive scheduled check-ins through the real GoalRuntimeHandle/Core admission and automatic-turn accounting, with a production-entry narrowing mutant.",
      "mechanism": "codex-rs/ext/goal/tests/background_wait.rs:1230 now uses paused Tokio time and a real CheckInTimer, but calls spawn_check_in_reentry at :1142. That test-local adapter directly calls claim_due_deadline, evaluate_continuation, check_admission and note_turn_start, then recursively schedules itself. It never constructs GoalRuntimeHandle, calls continue_if_idle/start_turn_if_idle, receives a Core Started result, marks a turn automatic or emits the production warning. The real adapter at ext/goal/src/runtime.rs:572-588 is therefore still bypassed. The hosted drop_timer_spawn mutant modifies CheckInTimer::spawn, not the production Wait-arm/re-entry route, so its kill cannot detect a runtime-only wiring failure. This is the repeated observed integration-coverage defect; it does not assert that a live runtime check-in was executed and failed.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3ens4c/static_attack.py (full corrected source embedded below)",
          "command": "python3 .temp/TASK-261007-3ens4c/static_attack.py scheduler",
          "expected_failure": "Observed exit 1 in scheduler-01.log: EXPECTED RED, actual GoalRuntimeHandle/Core submission in the named test and adapter is False. Add/supplement an enabled GoalRuntimeHandle + live thread fixture under an injected paused clock; advance time alone and observe real registered turns at 30/60/120, automatic accounting and one warning. Narrow only runtime Wait-arm spawning or runtime callback re-entry while retaining the timer/state; require that production fixture to fail. That requested mutant was NOT executed here.",
          "candidate_tree": "16a538869452dc36d083b8ab3c3e63a1e57c7285",
          "pinned_blobs": [
            "git-blob:22417586602b881c3821e3e1277ed418705e6db0",
            "git-blob:66e6ca9c6135251c558298b1b57810f09e96c87a",
            "git-blob:73de2bfd4375d64dca2cb9639ecad07b23896e15"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "CR-TASK-260929-2snjbb-2 / scheduled-checkin-regression-not-exercised",
      "reported_by": [
        "TASK-261007-3ens4c"
      ]
    },
    {
      "id": "revision-recheck-before-await-window",
      "row": "admission recheck and invalidation",
      "invariant": "AC7 rejects a receipt transition anywhere between continuation check and turn start, using serialization or a revision recheck at commit.",
      "mechanism": "codex-rs/core/src/session/turn_input.rs:529-543 places the new late comparison before calling the awaited start_task. core/src/tasks/mod.rs:353-388 still awaits timing, total_token_usage, active/state locks, input draining and before-registration lifecycle; there is no subsequent goal revision comparison. Session::total_token_usage (core/src/session/mod.rs:1460) waits on Session.state; receipt reserve/Arm (completion_receipt.rs:367-467) uses an independent store mutex and bumps revision. Legal source-established interleaving: late check accepts revision R, start_task parks awaiting Session.state, another thread reserves and Arms at R+2, then start_task resumes and records/registers the automatic goal. The new latch at turn_input_tests.rs:1500-1534 Arms while apply_started is blocked, so it covers the earlier preparation interval, not this residual interval.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3nfu39/static_attack.py (full source below)",
          "command": "python3 .temp/TASK-261007-3nfu39/static_attack.py post-late-check",
          "expected_failure": "Observed exit 1: static source ordering/independent-lock witness; no Rust race executed. Requested regression: receipt_armed_inside_start_task_blocks_automatic_start, latch total_token_usage/state acquisition after the final comparison and before record_started_turn, reserve+Arm via production store, then expect GoalBackgroundWait with no registered task/reservation. Narrowing mutant: move the commit comparison back before the awaited start_task interval, preserving the preparation check.",
          "pinned_blobs": [
            "git-blob:8414dcfa10c4733b08f8cf7e55fbce6b5c2d700d",
            "git-blob:481ebc9deee74a3b8d84a65977096c92d4cd7cc4",
            "git-blob:2a4707c2de74d96c1113beedf6972355b56db946"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "rev2: revision-recheck-before-await-window",
      "reported_by": [
        "TASK-261007-3nfu39"
      ]
    },
    {
      "id": "rejected-goal-start-commits-settings",
      "row": "admission recheck and invalidation",
      "invariant": "A StartIfIdleSubmission::NotSubmitted must leave persistent settings and start options unapplied (codex-rs/protocol/src/turn_input.rs); rework must preserve the existing admission contract.",
      "mechanism": "codex-rs/core/src/session/turn_input.rs:475-477 runs apply_started before the new late rejection at :529-534. apply_started at :159-179 commits through new_turn_with_sub_id_if and emits ThreadSettingsApplied. turn_context.rs:1074 calls update_settings_if, whose session/mod.rs:1908 assigns state.session_configuration. On revision mismatch the new rejection only clears the reserved turn and tries pending work; it does not undo configuration or notification. The new hosted latch itself submits effort=High (:1505-1507), Arms during preparation and gets NotSubmitted, but never compares thread settings. A different valid initial effort therefore changes despite rejected automatic input. This is a source-established effect-order regression, not a claim of newly executed before/after assertions.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3nfu39/static_attack.py (full source below)",
          "command": "python3 .temp/TASK-261007-3nfu39/static_attack.py rejected-settings",
          "expected_failure": "Observed exit 1: static commit-before-refusal witness. Requested regression: late_goal_rejection_leaves_thread_settings_unchanged, extend the existing public handle latch with a deliberately different initial effort and a deep before/after ThreadSettingsSnapshot equality plus no ThreadSettingsApplied notification. Narrowing mutant: keep revision refusal but allow the rejected preparation to publish settings before the refusal. No new Rust assertion was executed.",
          "pinned_blobs": [
            "git-blob:8414dcfa10c4733b08f8cf7e55fbce6b5c2d700d",
            "git-blob:481ebc9deee74a3b8d84a65977096c92d4cd7cc4"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261007-3nfu39"
      ]
    },
    {
      "id": "scheduled-checkin-regression-not-exercised",
      "row": "check-in tickets and warning",
      "invariant": "AC4-AC5 and the rev2 required regression drive the real timer/GoalRuntimeHandle continuation/Core admission/accounting under fake time, and kill a production-runtime-only scheduler mutant.",
      "mechanism": "codex-rs/ext/goal/tests/background_wait.rs:1230-1297 now uses real CheckInTimer and paused time, but delegates to test-only spawn_check_in_reentry (:1142-1207). That helper manually evaluates/checks admission, calls note_turn_start, and recursively rearms a timer; it never calls GoalRuntimeHandle::continue_if_idle, Core start_turn_if_idle, automatic bookkeeping or the warning emitter, and does not install the runtime abort hook. Runtime production composition is at runtime.rs:572-587, :671-717. The hosted drop_timer_spawn patch removes CheckInTimer::spawn itself, not the runtime Wait-arm call or runtime continuation, so its kill establishes timer component coverage only. The prior simulated-regression mechanism persists, moved into an asynchronous test helper. Producer results explicitly defer full continuation/automatic marking to stage 2e despite the same-leaf rework brief requiring it.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3nfu39/static_attack.py (full source below)",
          "command": "python3 .temp/TASK-261007-3nfu39/static_attack.py scheduled-test",
          "expected_failure": "Observed exit 1: static exact-source coverage witness; not an executed production scheduler failure. Requested regression: scheduled_checkins_fire_via_runtime_under_paused_time with enabled real GoalRuntimeHandle/backend, real Armed receipt, one real idle trigger, fake-time-only 30/60/120 starts, automatic bookkeeping, one warning event, active/wakeable state and late completion wake. Narrowing mutant: keep CheckInTimer and BackgroundWaitState intact but suppress runtime.rs Wait-arm spawn_check_in_timer or its continue_if_idle callback; this exact production regression must fail.",
          "pinned_blobs": [
            "git-blob:66e6ca9c6135251c558298b1b57810f09e96c87a",
            "git-blob:22417586602b881c3821e3e1277ed418705e6db0"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "rev2: scheduled-checkin-regression-not-exercised",
      "reported_by": [
        "TASK-261007-3nfu39"
      ]
    }
  ],
  "notes": [
    "[TASK-261007-3ens4c] {'id': 'execution-bound', 'text': 'Read-only review: no repository source edits, commits, cargo/just/builds, local Rust tests or new hosted mutants. Only temporary-index replay, pinned-source audits and artifact validation were rerun here. The hosted precheck-4 summary is accepted as attached evidence, not independently fetched; it reports job conclusions and named failed tests, not numeric underlying command exit codes. None are invented. The truncated CR validation log is not counted as proof of unseen commands.'}",
    "[TASK-261007-3ens4c] {'id': 'ownership-fixes-acknowledged', 'text': 'Rev2 timer-aborts-own-admission and fired-timer-aborted-before-admission-reply share the fired-slot ownership cause: CheckInTimer now takes its own entry by id before on_fire().await. Stale-timer-install-clobbers-current-registration is addressed by a generation guard and permit-held coherent armed_deadline install. Hosted precheck-4 lists keep_handle_in_slot_while_firing 37550841452 killed by fired_timer_continuation_survives_turn_start_invalidation, and unconditional_slot_replace 37550984504 killed by stale_install_never_replaces_newer_generation_timer. These helper-level fixes are acknowledged, without inferring mark_goal_continuation always executes from the helper test.'}",
    "[TASK-261007-3ens4c] {'id': 'coverage-ratios', 'text': 'Surface sweep 3/3: 1 held, 2 broken, 0 not-attacked. Attached hosted evidence: 4/4 lanes success; 13/13 mutants killed, 0 survivors. Of the 1 newly named full scheduled-runtime regression, 0/1 reaches GoalRuntimeHandle/Core registration; it does cover the real timer/state. The new core latch covers the 1 preparation window, not the 1 additional callee-await window identified in the source audit. AC4/5 full runtime composition and AC7 actual commit ordering remain bounded; a claimed 10/10 driving-test map is not equivalent to full-contract coverage.'}",
    "[TASK-261007-3ens4c] {'id': 'future-activation-and-read-failure-bounds', 'text': 'Policy is intentionally disabled until the later activation slice. note_release has no production caller in this preparatory candidate; controls/late-completion wake wiring are deferred and not a new blocking finding here. A failed timer-fired snapshot read may consume the deadline before WaitOnReadFailure returns without rearming (runtime.rs:579/682; background_wait.rs:321/386); recovery behavior was not executed, so it is an unresolved nonblocking contention note. Snapshot contents/revision are copied across independent locks (pending_work.rs:51-65); coherence remains an unexecuted bound, not an extra finding.'}",
    "[TASK-261007-3ens4c] {'id': 'scope-context-api-size', 'text': 'No new model-visible fragment: GoalExtension contributor returns Vec::new; prompt/template text is unchanged in this CR. NotSubmittedReason::GoalBackgroundWait has a matching exhaustive app-server branch; no new wire/config/CLI/rollout break established. Replay vs CR base includes checkpointed E1: 28 files, +4104/-40. Actual rev2-to-rev3 delta is 7 files, +559/-38. Smallest next corrective slice is actual commit serialization and the production scheduled-runtime regression in E2; no new research prerequisite or generalized harness leaf is required.'}",
    "[TASK-261007-3ens4c] {'id': 'inspection-recovery', 'text': 'Two compact board queries initially used unsupported resources field and exited 1; recovered using documented resource paths and scoped get/schema calls. A reviewer role reference through the lazy skill symlink was absent (cat exit 1); the installed /Users/iv/.agents/skills/project-management/.roles/reviewer/role.md was read instead. These are read/fixture failures, never green gates. Corrected admission audit exit 1 is deliberately expected-red and distinct from its first fixture-error exit 1.'}",
    "[TASK-261007-1c6vam] {'id': 'execution-bound', 'text': 'Read-only replay plus static probes only. Ran no cargo, just, builds, Rust tests, or new hosted mutants. Hosted precheck 4 (snapshot c7652275, run 37550767559, four lanes success, 13/13 mutants killed, 0 survivors) is accepted as attached execution evidence on the exact replayed tree, not rerun or independently fetched. Local CR rev3 validation log (64 KiB truncated) shows fast-lane green: fmt-check exit 0, clippy, 267 small tests exit 0.'}",
    "[TASK-261007-1c6vam] {'id': 'round2-closure', 'text': 'All five round-2 findings verified fixed in the exact candidate: timer-aborts-own-admission and fired-timer-aborted-before-admission-reply by id-gated detach before on_fire (check_in_clock.rs fire path, probe P1); stale-timer-install-clobbers-current-registration by the generation guard plus permit-held synchronous install (probes P2, P7, P12); revision-recheck-before-await-window by the late recheck immediately before start_task with clean abandon (probes P3, P3b); scheduled-checkin-regression-not-exercised by the real-timer start_paused scheduled test driving claim→evaluate→admit→re-arm with time advance alone (probe P8). Each has a hosted killed narrowing mutant. No repeat-of carried forward.'}",
    "[TASK-261007-1c6vam] {'id': 'snapshot-coherence-bound', 'text': 'Retained unexecuted bound from rev1/rev2: try_read_snapshot reads the receipt store and mailbox under separate locks and loads revision last (pending_work.rs). A transition landing inside that read window could pair a pre-transition content view with a post-transition revision. No live reproduction exists and none was executed here; both admission checks would have to straddle transitions in the same direction for a wrong Allow. Not a finding.'}",
    "[TASK-261007-1c6vam] {'id': 'post-late-recheck-window', 'text': 'Unexecuted bound, not a finding: the late recheck sits at the last point before start_task exactly as rework-brief fix C scoped it, but start_task itself awaits (locks, plugin selection, lifecycle emit) without serializing against receipt transitions, which use their own mutex and atomic revision. A receipt arming inside start_task would not be caught; consequence is one goal turn starting despite just-armed work (the completion stays queued, no loss or starvation). Closing it needs shared commit locking beyond this leaf. Wanted test if pursued: latch inside start_task claim, arm a receipt, assert NotSubmitted; hosted lane required, not run.'}",
    "[TASK-261007-1c6vam] {'id': 'release-and-activation-bounds', 'text': 'note_release still has no production caller in the candidate (definition plus unit tests only); release controls arrive in stage 2e. Policy remains disabled by default; no missing-activation finding. State empty-reassessment tests plus core release/cancellation admission tests cover AC8 at this stage but do not prove a production late-completion or release event wakes the runtime.'}",
    "[TASK-261007-1c6vam] {'id': 'size-api-context', 'text': 'rev2→rev3 delta is exactly 7 files, +559/-38, all inside the E2 scheduler plus admission modules. No new model-visible fragment (admission checker is a sync Allow/Wait closure, no text injection). No wire, config, CLI, schema, or rollout change in rev3; no breaking change established. Full base replay includes checkpointed E1 prerequisites (28 files).'}",
    "[TASK-261007-3nfu39] {'id': 'prior-round-dispositions', 'text': '5/5 prior finding records assessed: timer-aborts-own-admission and fired-timer-aborted-before-admission-reply share the corrected detach-before-callback mechanism (source probe 0; component kill 37550841452); stale-timer-install-clobbers-current-registration has generation guard plus permit-held install (source probe 0; kill 37550984504). Revision-recheck-before-await-window is partially repaired with a later preparation check but residual awaited start window persists. Scheduled-checkin-regression-not-exercised persists as test-owned async re-entry. No remaining self-abort failure asserted; end-to-end accounting coverage remains bounded by the scheduled finding.'}",
    "[TASK-261007-3nfu39] {'id': 'execution-provenance', 'text': 'This panel ran only exact-tree replay, source reads and Python static witnesses; no cargo, just, builds, Rust tests or hosted mutants. Reused TASK-260929-2snjbb_hosted-precheck-4.md tree 16a538869452dc36d083b8ab3c3e63a1e57c7285, snapshot c7652275, base 37550767559, 13/13 reported mutant kills and four lane success statuses. Hosted summary has no numeric process exit codes, so none are invented. Truncated local CR validation log is not relied upon for unseen commands. drop_timer_spawn is component-wide deletion, unconditional_slot_replace deletes a generation check, no_late_recheck deletes the late block: the report label all narrowing/no delete-only overstates those classes; kills still count for their stated component bounds.'}",
    "[TASK-261007-3nfu39] {'id': 'retained-bounds', 'text': 'Snapshot lists and revision are sampled separately (pending_work.rs:51-64); no newly executed coherence failure. note_release has no production caller in this preparatory stage; external release/completion activation is deferred as acknowledged previously. Policy intentionally disabled by default; no missing-default-activation finding. Stage 2e deferral does not satisfy the explicit rev2 same-leaf scheduler regression request.'}",
    "[TASK-261007-3nfu39] {'id': 'context-api-size', 'text': 'Goal TurnInputContributor returns empty Vec (extension.rs:608-614), so no new model-visible fragment or history rewrite is injected. Internal NotSubmittedReason::GoalBackgroundWait has an app-server handling arm; no additional wire/config/CLI/rollout break found in bounded inspection. Rejected-settings finding addresses an existing public Core submission contract. Rev2-to-rev3 delta: 7 files, +559/-38; full replay vs base: 28 files, +4104/-40 including E1 prerequisite. Keep corrective stage on commit-time admission and the real runtime regression; do not add a research prerequisite or widen product scope.'}"
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Exact-tree hosted precheck 4 base run 37550767559 reports core/small/lint/app-server success. overgate_non_goal_triggers 37550876321 killed by goal_background_wait_blocks_goal_but_admits_user_and_followup (core turn_input_tests.rs:1247 drives handle StartIfIdle) and goal_background_wait_ignores_non_goal_triggers (:1375). Armed-only mutant 37550823483 and read-error mutant 37550965847 also killed in the attached report. Static predicate restricts the gate to Automatic + goal; all other kinds/triggers bypass. Held only for these named attacks.",
      "reported_by": "TASK-261007-3ens4c"
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "scheduled-checkin-regression-not-exercised"
      ],
      "evidence": "scheduler audit exit 1 proves the new paused-time regression still substitutes a local adapter for GoalRuntimeHandle. Hosted cap/epoch/single-use/warning/timer-helper attacks are acknowledged: reuse_ticket_id 37550931976, warning_repeats 37551004329, reset_epoch_on_turn_start 37550913595, drop_timer_spawn 37550804014. Their kills cannot establish the bypassed production runtime route.",
      "reported_by": "TASK-261007-3ens4c"
    },
    {
      "row": "admission recheck and invalidation",
      "result": "broken",
      "findings": [
        "revision-recheck-before-await-window"
      ],
      "evidence": "Corrected admission audit exit 1 establishes the remaining callee-await window after the late comparison. Hosted no_late_recheck 37550859181 kills receipt_armed_after_admission_blocks_automatic_start, whose persistence-lock latch is before this final comparison. skip_revision_recheck 37550948899 and preserve_ticket_across_invalidation 37550895448 kills are acknowledged; they do not exercise the remaining commit race.",
      "reported_by": "TASK-261007-3ens4c"
    }
  ],
  "free_hunt": [
    "[TASK-261007-3ens4c] {\"budget_minutes\": 5, \"method\": \"Bounded static hunt after all rows, no builds\", \"scope\": [\"rev2-to-rev3 timer ownership and lock ordering\", \"read-failure/deadline recovery\", \"disabled/resume/release lifecycle\", \"model context, API and change size\"], \"additional_blocking_findings\": [], \"result\": \"No additional confirmed mechanism; contention/coherence/activation limits retained as notes. No live behavioral race or runtime mutant claimed.\"}",
    "[TASK-261007-1c6vam] Bounded static hunt after the surface sweep (no builds): timer abort/detach orderings, stale-install interleavings, snapshot coherence, post-late-recheck window inside start_task awaits, release callers, permit/delay separation, warning/count/epoch state machine, rev2→rev3 delta scope, context/wire/config surface. No additional blocking mechanism found. Residual items recorded as notes (snapshot-coherence-bound, post-late-recheck-window, release-and-activation-bounds), each with the wanted test named and none executed.",
    "[TASK-261007-3nfu39] {\"budget_minutes\": 5, \"method\": \"bounded static delta/call-site/effect-order review after all 3 surface rows were recorded in the row journal\", \"scope\": [\"new late-refusal side effects\", \"timer ownership/generation/permit\", \"snapshot revision coherence\", \"release/resume/disable callers\", \"API/context exposure\", \"actual review delta size\"], \"additional_findings\": [\"rejected-goal-start-commits-settings\"], \"result\": \"One new effect-order regression; no further blocking mechanisms. Existing snapshot/control-activation bounds remain notes.\"}"
  ]
}
```
