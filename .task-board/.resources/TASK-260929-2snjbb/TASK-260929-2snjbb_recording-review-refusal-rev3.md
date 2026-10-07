# TASK-260929-2snjbb — goal-background-wait-policy: recording review refusal

CR revision 3; candidate tree `16a538869452dc36d083b8ab3c3e63a1e57c7285`.

Recording decision: REFUSE the supplied merge. Panel disposition remains changes_requested. Route the element to to-dev for merge correction and the existing panel-requested rework; no acceptance, no code modification, and no fresh production review.

Compared all three named panel outcomes with `TASK-260929-2snjbb_review-verdict-rev3.md`. Panel A and delta request changes; panel B accepts. The merge retains all five original finding records and all 16 panel notes, with no original finding/reproduction field removed or changed (delta reproduction blob pins were added). All 3/3 surface row names and worst results survive: held, broken, broken.

Corrections required before the named canonical verdict can be stamped:

- Collapse the two reports of `revision-recheck-before-await-window` into one mechanism with both reproductions and panel attribution. Both describe the remaining awaited start_task interval after the late comparison.
- Collapse the two reports of `scheduled-checkin-regression-not-exercised` into one mechanism with both reproductions and panel attribution. Both describe test-local re-entry replacing GoalRuntimeHandle/Core integration.
- The admission recheck and invalidation row must link `rejected-goal-start-commits-settings` in addition to `revision-recheck-before-await-window`. The delta panel row includes both; the merged row includes only the latter. The finding itself is present in the array, so this is a lost row linkage, not a lost finding record.
- Order the consolidated blocking findings bypass first. The supplied list puts a regression before later bypass records.

Expected corrected set: three mechanisms, not five. Expected row finding links: gate scope and fairness [] (held); check-in tickets and warning [scheduled-checkin-regression-not-exercised] (broken); admission recheck and invalidation [revision-recheck-before-await-window, rejected-goal-start-commits-settings] (broken). Retain every original reproduction, evidence bound, repeat-of and panel disagreement; do not add findings.

## Verification and task-scoped logbook

2026-10-07: first lifecycle mutation, all four resource retrievals, run-goal query and compact status query exited 0. Run is not goal-bound; directives were empty. Artifact comparison executed with Python 3; detailed data is attached separately as merge-audit JSON. Initial combined display was truncated; subsequent local JSON extraction and per-field comparison recovered complete records. Truncated display was not treated as complete evidence.

No cargo/just/builds, new attacks, hosted fetch, source edits, commits or branch operations. The supplied panel static witnesses and hosted reports remain panel evidence only; this recording run reran none of them. Per the explicit recording-brief exception, reject_cr was not invoked against the incorrect canonical merge and accept_cr was not invoked. This is a recording refusal, not an external blocker.

## Exact inherited payload (reference only, not a replacement verdict)

The following JSON is the refused canonical payload, retained without changing its findings or surface results. Its duplicate mechanisms and missing row linkage are the discrepancies above.

```json
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
          "pinned_blobs": {
            "codex-rs/core/src/session/turn_input.rs": "481ebc9deee74a3b8d84a65977096c92d4cd7cc4",
            "codex-rs/core/src/session/goal_admission.rs": "f93063fd3ce2c7e5b3d25618ad21a29ac9b7f3bd",
            "codex-rs/core/src/tasks/mod.rs": "2a4707c2de74d96c1113beedf6972355b56db946",
            "codex-rs/core/src/session/mod.rs": "8414dcfa10c4733b08f8cf7e55fbce6b5c2d700d",
            "codex-rs/core/src/unified_exec/completion_receipt.rs": "be9f60e63f1b4e36006fb3424ee09a2429f5325e"
          }
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
          "pinned_blobs": {
            "codex-rs/ext/goal/tests/background_wait.rs": "22417586602b881c3821e3e1277ed418705e6db0",
            "codex-rs/ext/goal/src/runtime.rs": "66e6ca9c6135251c558298b1b57810f09e96c87a",
            "codex-rs/ext/goal/src/check_in_clock.rs": "73de2bfd4375d64dca2cb9639ecad07b23896e15"
          }
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
    "Recording refusal: the supplied canonical merged verdict was not stamped. All findings below are inherited verbatim from that resource; no new production findings. Duplicate entries are retained here solely to show the exact merge defect."
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
  "free_hunt": []
}
```
