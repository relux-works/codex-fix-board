# R141 DELTA panel verdict — goal-background-wait-policy revision 3

changes_requested

Panel task: TASK-261007-3nfu39 — r141-panel-delta-task-260929-2snjbb-rev3.
Read-only target: CR-TASK-260929-2snjbb-3. No recording-review mutation or any other write was made on TASK-260929-2snjbb.

Replay check: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus attached revision-3 patch produced exactly candidate tree `16a538869452dc36d083b8ab3c3e63a1e57c7285`. All candidate claims below use `git show <candidate-tree>:<path>`, not the worktree HEAD. No nested worktree, branch operation or build was used.

| Executed command / check | Real exit | Result |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261007-3nfu39, status=analysis)'` | 0 | Panel lifecycle only |
| Readiness: `command -v task-board git rg python3`; `task-board --help`; `git --version`; `rg --version`; `python3 --version` | 0 | Log `.temp/TASK-261007-3nfu39/readiness-01.log` |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3nfu39-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Temporary index initialized |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev3.patch --output .temp/TASK-260929-2snjbb_change-request_rev3.patch` | 0 | Read-only producer resource download |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3nfu39-replay.idx" git apply --cached .temp/TASK-260929-2snjbb_change-request_rev3.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3nfu39-replay.idx" git write-tree` | 0 | Exact expected tree above |
| `task-board resource get TASK-260929-2snjbb surface-table.md --output .temp/TASK-261007-3nfu39/surface-table.md` | 0 | 3 surface rows |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_review-verdict-rev2.md --output .temp/TASK-261007-3nfu39/previous-verdict.md` | 0 | 5 prior findings |
| `python3 .temp/TASK-261007-3nfu39/static_attack.py fixed-ownership` | 0 | Source fixes verified; no runtime attestation |
| `python3 .temp/TASK-261007-3nfu39/static_attack.py scheduled-test` | 1 | Expected-red: runtime regression still bypassed by a test helper |
| `python3 .temp/TASK-261007-3nfu39/static_attack.py post-late-check` | 1 | Expected-red: awaited start window remains after comparison |
| `python3 .temp/TASK-261007-3nfu39/static_attack.py rejected-settings` | 1 | Expected-red: persistent settings commit precedes refusal |
| `git diff --check` | 0 | No tracked delta from this panel |
| `python3 .temp/TASK-261007-3nfu39/validate_verdict.py` | 0 | Exactly one valid findings JSON block, exact 3-row coverage, valid findings, source/log inclusion and <64 KiB text outcome |

Each static witness ran as a standalone Python process, redirected directly to its numbered log (no `tee` or status-hiding gate pipeline). Red witnesses are failing, never presented as green tests. Format validation exit is included only after its successful execution before attachment.

Routine resource/source reads and narrow successful board queries exited 0. Operational diagnostic failures, not gates: initial role-file read through `.claude` skill path exited 1 (resolved by reading installed `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md`, exit 0); unsupported resource/attachment projection queries and an invalid scoped schema request exited 1 (recovered with explicit resource names and bounded resource-directory listing); absent skill directories inventory exited 2. Candidate extraction outer Python exited 0 but optional missing `ext/goal/src/controller.rs` git show exited 128; no controller claim relied on it. Guessed `session/token_usage.rs` and `session/turn_input_settings.rs` git shows exited 128; subsequent empty-file rg exited 1; symbols resolved in session/mod.rs and turn_input.rs. These absent paths/read errors are not treated as successful evidence. Spawn directives read at safe checkpoints exited 0 and had none.

## Prior round, key aspects and recommendation

| Previous finding | Disposition on revision 3 |
| --- | --- |
| timer-aborts-own-admission | Source mechanism fixed: identity detach before callback; component negative test reported killed mutant |
| fired-timer-aborted-before-admission-reply | Same ownership mechanism fixed; full automatic bookkeeping covered by outstanding scheduled-regression request |
| stale-timer-install-clobbers-current-registration | Source mechanism fixed: generation guard and permit-held install |
| revision-recheck-before-await-window | Partial fix; residual window inside awaited start_task repeats the class |
| scheduled-checkin-regression-not-exercised | Repeats: real timer now tested, production runtime still replaced by test-only re-entry |

5/5 prior findings checked; 3/3 surface rows swept; one held and two broken. Recommend same-leaf rework for a commit-time admission check, rejection without publishing persistent settings, and a real GoalRuntimeHandle scheduled regression with a runtime-only mutant. No new serial research leaf is required.

## Sources and evidence bounds

Read-only board inputs: `surface-table.md`, `producer-brief.md`, `e2-rework-brief-rev3.md`, `TASK-260929-2snjbb_review-verdict-rev2.md`, `TASK-260929-2snjbb_results.md`, `TASK-260929-2snjbb_coverage-map.md`, `TASK-260929-2snjbb_mutants.json`, and `TASK-260929-2snjbb_hosted-precheck-4.md`. Code citations in findings are exact candidate path:line references, with Git blob pins printed by the probes below. Attached hosted summary is accepted execution evidence per panel brief, not independently rerun. It reports lane statuses and test names, not numeric process exits. No external publication or repository acceptance is attested.

## Logbook (task-scoped outcome, no control-root edit)

2026-10-07: Exact revision-3 replay confirmed. Timer ownership/stale-install fixes acknowledged. Two rev2 mechanisms remain: simulation instead of real runtime scheduler regression and awaited admission-to-start window. Free hunt found persistent-settings side effects before late rejection. All source witnesses are explicitly static; new runtime regressions and mutants are requested, not claimed executed. Producer task untouched; evidence attached only to this panel task before researcher handoff.

```verdict-findings
{
  "findings": [
    {
      "id": "revision-recheck-before-await-window",
      "row": "admission recheck and invalidation",
      "invariant": "AC7 rejects a receipt transition anywhere between continuation check and turn start, using serialization or a revision recheck at commit.",
      "mechanism": "codex-rs/core/src/session/turn_input.rs:529-543 places the new late comparison before calling the awaited start_task. core/src/tasks/mod.rs:353-388 still awaits timing, total_token_usage, active/state locks, input draining and before-registration lifecycle; there is no subsequent goal revision comparison. Session::total_token_usage (core/src/session/mod.rs:1460) waits on Session.state; receipt reserve/Arm (completion_receipt.rs:367-467) uses an independent store mutex and bumps revision. Legal source-established interleaving: late check accepts revision R, start_task parks awaiting Session.state, another thread reserves and Arms at R+2, then start_task resumes and records/registers the automatic goal. The new latch at turn_input_tests.rs:1500-1534 Arms while apply_started is blocked, so it covers the earlier preparation interval, not this residual interval.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3nfu39/static_attack.py (full source below)",
          "command": "python3 .temp/TASK-261007-3nfu39/static_attack.py post-late-check",
          "expected_failure": "Observed exit 1: static source ordering/independent-lock witness; no Rust race executed. Requested regression: receipt_armed_inside_start_task_blocks_automatic_start, latch total_token_usage/state acquisition after the final comparison and before record_started_turn, reserve+Arm via production store, then expect GoalBackgroundWait with no registered task/reservation. Narrowing mutant: move the commit comparison back before the awaited start_task interval, preserving the preparation check."
        }
      ],
      "severity": "bypass",
      "repeat-of": "rev2: revision-recheck-before-await-window"
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
          "expected_failure": "Observed exit 1: static commit-before-refusal witness. Requested regression: late_goal_rejection_leaves_thread_settings_unchanged, extend the existing public handle latch with a deliberately different initial effort and a deep before/after ThreadSettingsSnapshot equality plus no ThreadSettingsApplied notification. Narrowing mutant: keep revision refusal but allow the rejected preparation to publish settings before the refusal. No new Rust assertion was executed."
        }
      ],
      "severity": "bypass",
      "repeat-of": "none"
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
          "expected_failure": "Observed exit 1: static exact-source coverage witness; not an executed production scheduler failure. Requested regression: scheduled_checkins_fire_via_runtime_under_paused_time with enabled real GoalRuntimeHandle/backend, real Armed receipt, one real idle trigger, fake-time-only 30/60/120 starts, automatic bookkeeping, one warning event, active/wakeable state and late completion wake. Narrowing mutant: keep CheckInTimer and BackgroundWaitState intact but suppress runtime.rs Wait-arm spawn_check_in_timer or its continue_if_idle callback; this exact production regression must fail."
        }
      ],
      "severity": "regression",
      "repeat-of": "rev2: scheduled-checkin-regression-not-exercised"
    }
  ],
  "notes": [
    {
      "id": "prior-round-dispositions",
      "text": "5/5 prior finding records assessed: timer-aborts-own-admission and fired-timer-aborted-before-admission-reply share the corrected detach-before-callback mechanism (source probe 0; component kill 37550841452); stale-timer-install-clobbers-current-registration has generation guard plus permit-held install (source probe 0; kill 37550984504). Revision-recheck-before-await-window is partially repaired with a later preparation check but residual awaited start window persists. Scheduled-checkin-regression-not-exercised persists as test-owned async re-entry. No remaining self-abort failure asserted; end-to-end accounting coverage remains bounded by the scheduled finding."
    },
    {
      "id": "execution-provenance",
      "text": "This panel ran only exact-tree replay, source reads and Python static witnesses; no cargo, just, builds, Rust tests or hosted mutants. Reused TASK-260929-2snjbb_hosted-precheck-4.md tree 16a538869452dc36d083b8ab3c3e63a1e57c7285, snapshot c7652275, base 37550767559, 13/13 reported mutant kills and four lane success statuses. Hosted summary has no numeric process exit codes, so none are invented. Truncated local CR validation log is not relied upon for unseen commands. drop_timer_spawn is component-wide deletion, unconditional_slot_replace deletes a generation check, no_late_recheck deletes the late block: the report label all narrowing/no delete-only overstates those classes; kills still count for their stated component bounds."
    },
    {
      "id": "retained-bounds",
      "text": "Snapshot lists and revision are sampled separately (pending_work.rs:51-64); no newly executed coherence failure. note_release has no production caller in this preparatory stage; external release/completion activation is deferred as acknowledged previously. Policy intentionally disabled by default; no missing-default-activation finding. Stage 2e deferral does not satisfy the explicit rev2 same-leaf scheduler regression request."
    },
    {
      "id": "context-api-size",
      "text": "Goal TurnInputContributor returns empty Vec (extension.rs:608-614), so no new model-visible fragment or history rewrite is injected. Internal NotSubmittedReason::GoalBackgroundWait has an app-server handling arm; no additional wire/config/CLI/rollout break found in bounded inspection. Rejected-settings finding addresses an existing public Core submission contract. Rev2-to-rev3 delta: 7 files, +559/-38; full replay vs base: 28 files, +4104/-40 including E1 prerequisite. Keep corrective stage on commit-time admission and the real runtime regression; do not add a research prerequisite or widen product scope."
    }
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Reused exact-tree hosted precheck 4 base run 37550767559, four successful lanes. Core public handle/start-if-idle attacks goal_background_wait_blocks_goal_but_admits_user_and_followup and goal_background_wait_ignores_non_goal_triggers kill overgate_non_goal_triggers (37550876321). Read-error mutant 37550965847 and Armed-only mutant 37550823483 killed. Static core guard restricts Automatic+goal. Held only for these named attacks; complete runtime composition is not inferred."
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "scheduled-checkin-regression-not-exercised"
      ],
      "evidence": "scheduled-test source witness exit 1. Ownership fix source probe exit 0; hosted keep_handle_in_slot_while_firing 37550841452 and unconditional_slot_replace 37550984504 kill component regressions. Reuse-ticket 37550931976, epoch 37550913595, warning 37551004329 and drop_timer_spawn 37550804014 killed. These do not drive production runtime continuation/accounting."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "broken",
      "findings": [
        "revision-recheck-before-await-window",
        "rejected-goal-start-commits-settings"
      ],
      "evidence": "post-late-check and rejected-settings static witnesses exit 1. Hosted no_late_recheck 37550859181 validates the preparation-window latch; skip_revision_recheck 37550948899 and preserve_ticket_across_invalidation 37550895448 killed. No attached attack arms inside start_task after the final comparison or checks settings after the late refusal."
    }
  ],
  "free_hunt": {
    "budget_minutes": 5,
    "method": "bounded static delta/call-site/effect-order review after all 3 surface rows were recorded in the row journal",
    "scope": [
      "new late-refusal side effects",
      "timer ownership/generation/permit",
      "snapshot revision coherence",
      "release/resume/disable callers",
      "API/context exposure",
      "actual review delta size"
    ],
    "additional_findings": [
      "rejected-goal-start-commits-settings"
    ],
    "result": "One new effect-order regression; no further blocking mechanisms. Existing snapshot/control-activation bounds remain notes."
  }
}
```

## Executable static witnesses

```python
import json
import subprocess
import sys

TREE = "16a538869452dc36d083b8ab3c3e63a1e57c7285"

def source(path):
    result = subprocess.run(["git", "show", TREE + ":" + path], capture_output=True, text=True)
    if result.returncode:
        print(result.stderr)
        sys.exit(2)
    blob = subprocess.check_output(["git", "rev-parse", TREE + ":" + path], text=True).strip()
    print("PIN", path, blob)
    return result.stdout

mode = sys.argv[1]
if mode == "fixed-ownership":
    timer = source("codex-rs/ext/goal/src/check_in_clock.rs")
    runtime = source("codex-rs/ext/goal/src/runtime.rs")
    fire = timer[timer.index("let handle = tokio::spawn"):timer.index("slot.entry = Some(TimerEntry")]
    assert fire.index("entry.id == id") < fire.index("slot.entry.take()") < fire.index("on_fire().await")
    spawn = timer[timer.index("pub fn spawn<F>"):]
    assert spawn.index("existing.generation > generation") < spawn.index("if let Some(old) = slot.entry.take()")
    wait = runtime[runtime.index("BackgroundWaitEvaluation::Wait {"):runtime.index("BackgroundWaitEvaluation::WaitOnReadFailure")]
    assert "self.spawn_check_in_timer(deadline, armed_generation)" in wait
    assert "drop(goal_state_permit)" not in wait
    print("PASS: identity detach before callback; stale generation rejected before cancellation; runtime Wait installs while holding permit. Static source verification only.")
    sys.exit(0)
if mode == "scheduled-test":
    test = source("codex-rs/ext/goal/tests/background_wait.rs")
    helper = test[test.index("fn spawn_check_in_reentry("):test.index("async fn wait_for_check_ins")]
    driver = test[test.index("async fn scheduled_checkins_fire_via_runtime_under_paused_time()") :]
    assert "spawn_check_in_reentry(" in driver
    assert "timer.spawn(" in helper
    for token in ["claim_due_deadline", "evaluate_continuation", "check_admission", "note_turn_start"]:
        assert token in helper
    for token in ["GoalRuntimeHandle", "continue_if_idle(", "start_turn_if_idle(", "mark_goal_continuation", "set_invalidation_hook", "background_wait_warning"]:
        assert token not in helper + driver
    print("FAIL: scheduled regression exercises a test-owned timer/state callback; production GoalRuntimeHandle, Core starts, automatic accounting, abort hook and warning emitter are absent. A runtime-only Wait-arm/continuation mutant is outside this test. Static coverage witness only; no runtime failure claimed.")
    sys.exit(1)
if mode == "post-late-check":
    turn = source("codex-rs/core/src/session/turn_input.rs")
    goal = source("codex-rs/core/src/session/goal_admission.rs")
    tasks = source("codex-rs/core/src/tasks/mod.rs")
    session = source("codex-rs/core/src/session/mod.rs")
    receipts = source("codex-rs/core/src/unified_exec/completion_receipt.rs")
    test = source("codex-rs/core/src/session/turn_input_tests.rs")
    last = turn[turn.index("// Late revision recheck:"):turn.index("async fn steer(")]
    assert last.index("recheck_goal_admission_before_start") < last.index(".start_task(")
    start = tasks[tasks.index("pub(crate) async fn start_task<"):tasks.index("let handle = tokio::spawn(", tasks.index("pub(crate) async fn start_task<"))]
    assert start.index("self.total_token_usage().await") < start.index("self.record_started_turn")
    assert "goal_admission" not in start and "pending_work_revision" not in start
    usage = session[session.index("pub(crate) async fn total_token_usage"):]
    assert "self.state.lock().await" in usage[:600]
    arm = receipts[receipts.index("pub(crate) fn resolve_initial_response("):receipts.index("/// Publishes a fully finalized exit")]
    assert "self.lock_state()?" in arm and "self.bump_revision()" in arm
    assert "active_turn" not in arm and "goal_state" not in arm
    late_test = test[test.index("async fn receipt_armed_after_admission_blocks_automatic_start()") :]
    assert late_test.index("arm_session_receipt(") < late_test.index("drop(persistence_guard)")
    print("FAIL: last comparison precedes awaited total_token_usage (Session.state lock), record_started_turn and lifecycle awaits; no receipt revision recheck exists in start_task before registration. Legal static schedule: check R; park at state lock in total_token_usage; reserve+Arm on independent receipt mutex bumps to R+2; release state lock; record/start still proceeds. Existing latch arms before apply_started returns, hence before last comparison. Not an executed Rust race.")
    sys.exit(1)
if mode == "rejected-settings":
    turn = source("codex-rs/core/src/session/turn_input.rs")
    context = source("codex-rs/core/src/session/turn_context.rs")
    session = source("codex-rs/core/src/session/mod.rs")
    protocol = source("codex-rs/protocol/src/turn_input.rs")
    tests = source("codex-rs/core/src/session/turn_input_tests.rs")
    path = turn[turn.index("let goal_admitted_revision ="):turn.index("async fn steer(")]
    assert path.index(".apply_started(") < path.index("recheck_goal_admission_before_start")
    reject = path[path.index("recheck_goal_admission_before_start"):path.index(".start_task(")]
    assert "TurnInputSubmission::NotSubmitted" in reject
    assert "update_settings" not in reject and "rollback" not in reject
    apply = turn[turn.index("async fn apply_started("):turn.index("async fn apply_steered(")]
    assert "new_turn_with_sub_id_if(" in apply and "thread_settings::emit_applied" in apply
    assert "self.update_settings_if(updates, should_start).await" in context
    assert "state.session_configuration = updated;" in session
    assert "Core rejected the input without applying settings or start options." in protocol
    test = tests[tests.index("async fn receipt_armed_after_admission_blocks_automatic_start()") :]
    assert "effort: Some(Some(ReasoningEffort::High))" in test
    assert "thread_settings_snapshot" not in test
    print("FAIL: apply_started commits settings via new_turn_with_sub_id_if -> update_settings_if and emits ThreadSettingsApplied before the new late rejection. Rejection only clears reservation/rechecks pending work; it does not undo committed config or notification. Existing hosted latch with effort override demonstrates this path is reachable but does not assert before/after settings. Static effect-order witness; no new Rust execution.")
    sys.exit(1)
raise SystemExit(2)
```

### fixed-ownership — recorded output

```text
PIN codex-rs/ext/goal/src/check_in_clock.rs 73de2bfd4375d64dca2cb9639ecad07b23896e15
PIN codex-rs/ext/goal/src/runtime.rs 66e6ca9c6135251c558298b1b57810f09e96c87a
PASS: identity detach before callback; stale generation rejected before cancellation; runtime Wait installs while holding permit. Static source verification only.
```

### scheduled-test — recorded output

```text
PIN codex-rs/ext/goal/tests/background_wait.rs 22417586602b881c3821e3e1277ed418705e6db0
FAIL: scheduled regression exercises a test-owned timer/state callback; production GoalRuntimeHandle, Core starts, automatic accounting, abort hook and warning emitter are absent. A runtime-only Wait-arm/continuation mutant is outside this test. Static coverage witness only; no runtime failure claimed.
```

### post-late-check — recorded output

```text
PIN codex-rs/core/src/session/turn_input.rs 481ebc9deee74a3b8d84a65977096c92d4cd7cc4
PIN codex-rs/core/src/session/goal_admission.rs f93063fd3ce2c7e5b3d25618ad21a29ac9b7f3bd
PIN codex-rs/core/src/tasks/mod.rs 2a4707c2de74d96c1113beedf6972355b56db946
PIN codex-rs/core/src/session/mod.rs 8414dcfa10c4733b08f8cf7e55fbce6b5c2d700d
PIN codex-rs/core/src/unified_exec/completion_receipt.rs be9f60e63f1b4e36006fb3424ee09a2429f5325e
PIN codex-rs/core/src/session/turn_input_tests.rs a9615ea903b0584007ebf83dbf3f642452f553da
FAIL: last comparison precedes awaited total_token_usage (Session.state lock), record_started_turn and lifecycle awaits; no receipt revision recheck exists in start_task before registration. Legal static schedule: check R; park at state lock in total_token_usage; reserve+Arm on independent receipt mutex bumps to R+2; release state lock; record/start still proceeds. Existing latch arms before apply_started returns, hence before last comparison. Not an executed Rust race.
```

### rejected-settings — recorded output

```text
PIN codex-rs/core/src/session/turn_input.rs 481ebc9deee74a3b8d84a65977096c92d4cd7cc4
PIN codex-rs/core/src/session/turn_context.rs 0d7b59d77ea6089bf4c157176a923a8069c1da62
PIN codex-rs/core/src/session/mod.rs 8414dcfa10c4733b08f8cf7e55fbce6b5c2d700d
PIN codex-rs/protocol/src/turn_input.rs c07f06c4056e2487457b56570de797a0adf81d8c
PIN codex-rs/core/src/session/turn_input_tests.rs a9615ea903b0584007ebf83dbf3f642452f553da
FAIL: apply_started commits settings via new_turn_with_sub_id_if -> update_settings_if and emits ThreadSettingsApplied before the new late rejection. Rejection only clears reservation/rechecks pending work; it does not undo committed config or notification. Existing hosted latch with effort override demonstrates this path is reachable but does not assert before/after settings. Static effect-order witness; no new Rust execution.
```

## Verdict format verification

```text
PASS: 1 verdict-findings JSON; 3/3 unique surface rows; 3 findings with full fields; one-word verdict; executable source/logs embedded; 26750 bytes
```

The byte count above is the pre-append outcome; this verification section is also below the same 64 KiB ceiling.

```python
import json
import pathlib
import re

root = pathlib.Path(".temp/TASK-261007-3nfu39")
p = root / "TASK-261007-3nfu39_panel-verdict.md"
s = p.read_text()
blocks = re.findall(r"^```verdict-findings\n(.*?)^```", s, flags=re.M | re.S)
assert len(blocks) == 1, len(blocks)
x = json.loads(blocks[0])
assert set(x) == {"findings", "notes", "surface_results", "free_hunt"}
surface = root.joinpath("surface-table.md").read_text()
expected = json.loads(re.search(r"```surface-table\n(.*?)\n```", surface, re.S).group(1))["rows"]
actual = [r["row"] for r in x["surface_results"]]
assert actual == expected and len(actual) == len(set(actual))
assert all(r["result"] in {"held", "broken", "not-attacked"} for r in x["surface_results"])
ids = set()
for f in x["findings"]:
    assert {"id", "row", "invariant", "mechanism", "reproductions", "severity", "repeat-of"}.issubset(f)
    assert f["row"] in expected and f["severity"] in {"bypass", "regression", "robustness", "note"}
    assert f["repeat-of"] and f["id"] not in ids
    ids.add(f["id"])
    for r in f["reproductions"]:
        assert {"test_file", "command", "expected_failure"}.issubset(r)
for r in x["surface_results"]:
    assert set(r.get("findings", [])).issubset(ids)
    assert r["result"] != "broken" or r.get("findings")
assert s[:s.index("```verdict-findings")].splitlines().count("changes_requested") == 1
assert len(p.read_bytes()) < 65536
assert root.joinpath("static_attack.py").read_text() in s
for mode in ["fixed-ownership", "scheduled-test", "post-late-check", "rejected-settings"]:
    assert root.joinpath(mode + "-01.log").read_text() in s
print("PASS: 1 verdict-findings JSON; 3/3 unique surface rows; 3 findings with full fields; one-word verdict; executable source/logs embedded;", len(p.read_bytes()), "bytes")
```
