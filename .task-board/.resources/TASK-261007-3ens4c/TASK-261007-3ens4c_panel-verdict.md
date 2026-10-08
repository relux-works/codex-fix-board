# TASK-261007-3ens4c — R141 panel A, CR revision 3

changes_requested

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus the attached rev3 patch produced **exactly** candidate tree `16a538869452dc36d083b8ab3c3e63a1e57c7285`. Replay used a temporary index, not the live index or a nested worktree. Sources below are read from that tree, not current HEAD.

This is a non-recording panel. All board mutations in this run target TASK-261007-3ens4c; none target TASK-260929-2snjbb. No accept/reject/status/handoff write on the reviewed task. No source change, commit or build. The outcome is prepared outside the managed worktree at `/tmp/TASK-261007-3ens4c-artifacts/TASK-261007-3ens4c_panel-verdict.md`, per the assignment; scratch and replay files are inside the run worktree's ignored `.temp/`.

## Commands actually rerun and observed exit codes

| Command | Exit | Meaning |
|---|---:|---|
| `task-board m 'set_status(TASK-261007-3ens4c, status=analysis)'` | 0 | Own panel lifecycle only |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev3.patch --output .temp/TASK-260929-2snjbb_change-request_rev3.patch` | 0 | Read-only patch retrieval |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3ens4c-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Seed temporary index |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3ens4c-replay.idx" git apply --cached .temp/TASK-260929-2snjbb_change-request_rev3.patch` | 0 | Replay patch |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3ens4c-replay.idx" git write-tree` | 0 | Printed exact expected tree |
| `git archive --format=tar --output=.temp/TASK-261007-3ens4c/candidate.tar 16a538869452dc36d083b8ab3c3e63a1e57c7285 codex-rs/core/src/session codex-rs/core/src/tasks codex-rs/core/src/unified_exec codex-rs/ext/goal codex-rs/ext/extension-api codex-rs/protocol/src/turn_input.rs codex-rs/core/src/agent/control codex-rs/app-server/src/request_processors/turn_processor.rs` | 0 | Local pinned source export; archive is scratch only, not attached |
| `tar -xf .temp/TASK-261007-3ens4c/candidate.tar -C .temp/TASK-261007-3ens4c/candidate` | 0 | Read-only source inspection copy |
| `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b 16a538869452dc36d083b8ab3c3e63a1e57c7285` | 0 | Patch whitespace check only |
| `python3 .temp/TASK-261007-3ens4c/static_attack.py scheduler > .temp/TASK-261007-3ens4c/scheduler-01.log 2>&1` | 1 | Expected-red static coverage witness; real failure, no Rust execution |
| `python3 .temp/TASK-261007-3ens4c/static_attack.py admission > .temp/TASK-261007-3ens4c/admission-01.log 2>&1` (first script version) | 1 | Audit-fixture error: wrong field-name assertion; excluded from finding evidence |
| `python3 .temp/TASK-261007-3ens4c/static_attack.py admission > .temp/TASK-261007-3ens4c/admission-02.log 2>&1` (corrected source below) | 1 | Expected-red static post-check ordering witness; no live race claimed |
| `git status --short` | 0 | No tracked/untracked repository delta reported; scratch ignored |

All audits were standalone processes with direct file redirection, no tee or pipe chain. Tool readiness was recorded in `.temp/TASK-261007-3ens4c/readiness-01.log` and `readiness-02.log` (task-board and git available, git version output, Python 3 version output; commands exited 0). Reads of the task AC, resources, candidate blobs, role contract and previous verdict exited 0 after the explicitly listed inspection recovery in notes. No local Rust suite, new mutant execution or hosted command exit code is claimed.

## Accepted attached execution evidence and references

Read-only resources on TASK-260929-2snjbb under `/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-2snjbb/`:

- `surface-table.md`: normative three review rows; task AC retrieved with `task-board q 'get(TASK-260929-2snjbb) { description scope ac notes }'` (exit 0).
- `TASK-260929-2snjbb_hosted-precheck-4.md`: exact candidate tree above, snapshot c7652275, run 37550767559; 4/4 lanes success and 13/13 killed mutants. Summary carries conclusions, not numeric command exit codes. Accepted as attached public-entry attack evidence under the panel brief.
- `TASK-260929-2snjbb_mutants.json`: inspected actual patch targets. `drop_timer_spawn` deletes timer helper behavior; it does not narrow the production runtime adapter. `no_late_recheck` deletes the comparison before the callee, covering the earlier preparation latch only.
- `TASK-260929-2snjbb_review-verdict-rev2.md`, `e2-rework-brief-rev3.md`, `TASK-260929-2snjbb_results.md`, `TASK-260929-2snjbb_coverage-map.md`: previous mechanisms, explicit requested real-runtime regression and producer claims. Context is not treated as independent behavioral proof.
- Candidate file references in the findings resolve as `git show 16a538869452dc36d083b8ab3c3e63a1e57c7285:<path>`; blob pins are included per reproduction.

No web sources are needed for these repository/source/evidence claims. The four green lanes and 13 kills are accepted attached results, not rerun by this panel. All new blocking evidence here is explicitly static.

## Bounded plan and task-scoped logbook

Decision: accept rev3 for merged recording versus return E2 for focused rework. Frozen precondition: the replay base/tree/patch tuple above (grammar not applicable). Ceiling: 40 minutes including packaging, plus a five-minute free-hunt ceiling within it. Artifact budget: one plain-text verdict, no attached archive. Serial research prerequisites: zero. Exit: three row results, one valid findings packet, attach evidence, researcher handoff. Consumer: recording reviewer, then E2 commit serialization and production scheduled-runtime test; no separate research leaf.

Logbook, 2026-10-07: exact replay passed. Three old ownership symptoms have source fixes with matching hosted helper attacks. Two prior classes persist: callee awaits after the last revision check, and the scheduled test still substitutes its own adapter. Requested rework stays in E2 with named deterministic regressions and production-route narrowing mutants. Inspection/audit fixture errors were recovered and excluded from passing evidence. No observation or mutation was recorded on the reviewed task. Sweep progress was saved under `.temp/TASK-261007-3ens4c/sweep.md` after each row.

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
      "repeat-of": "CR-TASK-260929-2snjbb-2 / revision-recheck-before-await-window"
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
      "repeat-of": "CR-TASK-260929-2snjbb-2 / scheduled-checkin-regression-not-exercised"
    }
  ],
  "notes": [
    {
      "id": "execution-bound",
      "text": "Read-only review: no repository source edits, commits, cargo/just/builds, local Rust tests or new hosted mutants. Only temporary-index replay, pinned-source audits and artifact validation were rerun here. The hosted precheck-4 summary is accepted as attached evidence, not independently fetched; it reports job conclusions and named failed tests, not numeric underlying command exit codes. None are invented. The truncated CR validation log is not counted as proof of unseen commands."
    },
    {
      "id": "ownership-fixes-acknowledged",
      "text": "Rev2 timer-aborts-own-admission and fired-timer-aborted-before-admission-reply share the fired-slot ownership cause: CheckInTimer now takes its own entry by id before on_fire().await. Stale-timer-install-clobbers-current-registration is addressed by a generation guard and permit-held coherent armed_deadline install. Hosted precheck-4 lists keep_handle_in_slot_while_firing 37550841452 killed by fired_timer_continuation_survives_turn_start_invalidation, and unconditional_slot_replace 37550984504 killed by stale_install_never_replaces_newer_generation_timer. These helper-level fixes are acknowledged, without inferring mark_goal_continuation always executes from the helper test."
    },
    {
      "id": "coverage-ratios",
      "text": "Surface sweep 3/3: 1 held, 2 broken, 0 not-attacked. Attached hosted evidence: 4/4 lanes success; 13/13 mutants killed, 0 survivors. Of the 1 newly named full scheduled-runtime regression, 0/1 reaches GoalRuntimeHandle/Core registration; it does cover the real timer/state. The new core latch covers the 1 preparation window, not the 1 additional callee-await window identified in the source audit. AC4/5 full runtime composition and AC7 actual commit ordering remain bounded; a claimed 10/10 driving-test map is not equivalent to full-contract coverage."
    },
    {
      "id": "future-activation-and-read-failure-bounds",
      "text": "Policy is intentionally disabled until the later activation slice. note_release has no production caller in this preparatory candidate; controls/late-completion wake wiring are deferred and not a new blocking finding here. A failed timer-fired snapshot read may consume the deadline before WaitOnReadFailure returns without rearming (runtime.rs:579/682; background_wait.rs:321/386); recovery behavior was not executed, so it is an unresolved nonblocking contention note. Snapshot contents/revision are copied across independent locks (pending_work.rs:51-65); coherence remains an unexecuted bound, not an extra finding."
    },
    {
      "id": "scope-context-api-size",
      "text": "No new model-visible fragment: GoalExtension contributor returns Vec::new; prompt/template text is unchanged in this CR. NotSubmittedReason::GoalBackgroundWait has a matching exhaustive app-server branch; no new wire/config/CLI/rollout break established. Replay vs CR base includes checkpointed E1: 28 files, +4104/-40. Actual rev2-to-rev3 delta is 7 files, +559/-38. Smallest next corrective slice is actual commit serialization and the production scheduled-runtime regression in E2; no new research prerequisite or generalized harness leaf is required."
    },
    {
      "id": "inspection-recovery",
      "text": "Two compact board queries initially used unsupported resources field and exited 1; recovered using documented resource paths and scoped get/schema calls. A reviewer role reference through the lazy skill symlink was absent (cat exit 1); the installed /Users/iv/.agents/skills/project-management/.roles/reviewer/role.md was read instead. These are read/fixture failures, never green gates. Corrected admission audit exit 1 is deliberately expected-red and distinct from its first fixture-error exit 1."
    }
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Exact-tree hosted precheck 4 base run 37550767559 reports core/small/lint/app-server success. overgate_non_goal_triggers 37550876321 killed by goal_background_wait_blocks_goal_but_admits_user_and_followup (core turn_input_tests.rs:1247 drives handle StartIfIdle) and goal_background_wait_ignores_non_goal_triggers (:1375). Armed-only mutant 37550823483 and read-error mutant 37550965847 also killed in the attached report. Static predicate restricts the gate to Automatic + goal; all other kinds/triggers bypass. Held only for these named attacks."
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "scheduled-checkin-regression-not-exercised"
      ],
      "evidence": "scheduler audit exit 1 proves the new paused-time regression still substitutes a local adapter for GoalRuntimeHandle. Hosted cap/epoch/single-use/warning/timer-helper attacks are acknowledged: reuse_ticket_id 37550931976, warning_repeats 37551004329, reset_epoch_on_turn_start 37550913595, drop_timer_spawn 37550804014. Their kills cannot establish the bypassed production runtime route."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "broken",
      "findings": [
        "revision-recheck-before-await-window"
      ],
      "evidence": "Corrected admission audit exit 1 establishes the remaining callee-await window after the late comparison. Hosted no_late_recheck 37550859181 kills receipt_armed_after_admission_blocks_automatic_start, whose persistence-lock latch is before this final comparison. skip_revision_recheck 37550948899 and preserve_ticket_across_invalidation 37550895448 kills are acknowledged; they do not exercise the remaining commit race."
    }
  ],
  "free_hunt": {
    "budget_minutes": 5,
    "method": "Bounded static hunt after all rows, no builds",
    "scope": [
      "rev2-to-rev3 timer ownership and lock ordering",
      "read-failure/deadline recovery",
      "disabled/resume/release lifecycle",
      "model context, API and change size"
    ],
    "additional_blocking_findings": [],
    "result": "No additional confirmed mechanism; contention/coherence/activation limits retained as notes. No live behavioral race or runtime mutant claimed."
  }
}
```

## Reproducible static audit source

Save as `.temp/TASK-261007-3ens4c/static_attack.py` from the repository root. Both corrected audit modes intentionally exit 1 on this candidate. These are source/coverage audits, not tests of Tokio runtime behavior.

```python
"""Expected-red source audits of the pinned candidate; never Rust execution."""
import subprocess
import sys

TREE = '16a538869452dc36d083b8ab3c3e63a1e57c7285'


def source(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)


def line(text, fragment):
    return text[:text.index(fragment)].count('\n') + 1


mode = sys.argv[1]
if mode == 'scheduler':
    path = 'codex-rs/ext/goal/tests/background_wait.rs'
    text = source(path)
    test = text[text.index('async fn scheduled_checkins_fire_via_runtime_under_paused_time()'):]
    helper = text[text.index('fn spawn_check_in_reentry('):text.index('async fn wait_for_check_ins(')]
    assert 'spawn_check_in_reentry(' in test
    assert 'state_cb.evaluate_continuation(' in helper
    assert 'state_cb.check_admission(' in helper
    assert 'state_cb.note_turn_start();' in helper
    # The regression must reach the actual GoalRuntimeHandle and Core submission.
    actual_runtime = any(token in test + helper for token in (
        'GoalRuntimeHandle', 'runtime.continue_if_idle(', '.start_turn_if_idle(',
        'GoalExtension', 'mark_goal_continuation(',
    ))
    print(f'{TREE}:{path}:{line(text, "async fn scheduled_checkins_fire_via_runtime_under_paused_time()")}: test calls test-local spawn_check_in_reentry')
    print(f'{path}:{line(text, "fn spawn_check_in_reentry(")}: helper directly evaluates, admits, invalidates, and recursively schedules the state')
    print('actual GoalRuntimeHandle/Core submission in test/helper:', actual_runtime)
    assert actual_runtime, 'EXPECTED RED: production-runtime check-in regression is still replaced by a test-local adapter'
elif mode == 'admission':
    path = 'codex-rs/core/src/session/turn_input.rs'
    text = source(path)
    marker = 'super::goal_admission::recheck_goal_admission_before_start(session, goal_admitted_revision)'
    late = text.index(marker)
    call = text.index('.start_task(', late)
    assert 'goal_admitted_revision' not in text[call:text.index('Ok(TurnInputSubmission::Started', call)]
    tasks_path = 'codex-rs/core/src/tasks/mod.rs'
    tasks = source(tasks_path)
    entry = tasks.index('pub(crate) async fn start_task<T: SessionTask>')
    commit = tasks.index('self.record_started_turn(&turn_context.sub_id).await;', entry)
    window = tasks[entry:commit]
    assert '.mark_turn_started(started_at)\n            .await' in window
    assert 'self.total_token_usage().await' in window
    assert 'self.active_turn.lock().await' in window
    checks_in_window = 'recheck_goal_admission' in window or 'admitted_revision' in window
    print(f'{TREE}:{path}:{line(text, marker)}: revision check occurs before start_task; no admitted revision passed to callee')
    print(f'{tasks_path}:{line(tasks, "pub(crate) async fn start_task<T: SessionTask>")}: callee awaits timing, token usage and active_turn before recording turn start')
    print(f'{tasks_path}:{line(tasks, "self.record_started_turn(&turn_context.sub_id).await;")}: commit reachable with no goal revision comparison in callee prefix:', not checks_in_window)
    receipts = source('codex-rs/core/src/unified_exec/completion_receipt.rs')
    assert 'fn bump_revision(&self)' in receipts
    assert 'self.revision.fetch_add(1, Ordering::SeqCst);' in receipts
    assert 'let mut state = self.lock_state()?;' in receipts
    print('Source-established schedule: late check at revision r; timing/state lock yields; independent receipt Arm bumps to r+1; resume start_task and record the turn without rechecking.')
    assert checks_in_window, 'EXPECTED RED: receipt transition can still land after the last check and before turn start'
else:
    raise ValueError(mode)
```

## Observed audit logs

### scheduler-01.log

```text
16a538869452dc36d083b8ab3c3e63a1e57c7285:codex-rs/ext/goal/tests/background_wait.rs:1230: test calls test-local spawn_check_in_reentry
codex-rs/ext/goal/tests/background_wait.rs:1142: helper directly evaluates, admits, invalidates, and recursively schedules the state
actual GoalRuntimeHandle/Core submission in test/helper: False
Traceback (most recent call last):
  File "/Users/iv/Developer/IV/codex/.temp/STORY-261007-2s5pfk/worktree/.temp/TASK-261007-3ens4c/static_attack.py", line 34, in <module>
    assert actual_runtime, 'EXPECTED RED: production-runtime check-in regression is still replaced by a test-local adapter'
           ^^^^^^^^^^^^^^
AssertionError: EXPECTED RED: production-runtime check-in regression is still replaced by a test-local adapter
```

### admission-01.log

```text
16a538869452dc36d083b8ab3c3e63a1e57c7285:codex-rs/core/src/session/turn_input.rs:530: revision check occurs before start_task; no admitted revision passed to callee
codex-rs/core/src/tasks/mod.rs:337: callee awaits timing, token usage and active_turn before recording turn start
codex-rs/core/src/tasks/mod.rs:370: commit reachable with no goal revision comparison in callee prefix: True
Traceback (most recent call last):
  File "/Users/iv/Developer/IV/codex/.temp/STORY-261007-2s5pfk/worktree/.temp/TASK-261007-3ens4c/static_attack.py", line 55, in <module>
    assert 'pending_work_revision' in receipts
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

### admission-02.log

```text
16a538869452dc36d083b8ab3c3e63a1e57c7285:codex-rs/core/src/session/turn_input.rs:530: revision check occurs before start_task; no admitted revision passed to callee
codex-rs/core/src/tasks/mod.rs:337: callee awaits timing, token usage and active_turn before recording turn start
codex-rs/core/src/tasks/mod.rs:370: commit reachable with no goal revision comparison in callee prefix: True
Source-established schedule: late check at revision r; timing/state lock yields; independent receipt Arm bumps to r+1; resume start_task and record the turn without rechecking.
Traceback (most recent call last):
  File "/Users/iv/Developer/IV/codex/.temp/STORY-261007-2s5pfk/worktree/.temp/TASK-261007-3ens4c/static_attack.py", line 59, in <module>
    assert checks_in_window, 'EXPECTED RED: receipt transition can still land after the last check and before turn start'
           ^^^^^^^^^^^^^^^^
AssertionError: EXPECTED RED: receipt transition can still land after the last check and before turn start
```

## Outcome structure validation

`python3 .temp/TASK-261007-3ens4c/package_verdict.py` exited 0. `python3 .temp/TASK-261007-3ens4c/validate_verdict.py > .temp/TASK-261007-3ens4c/verdict-validation-01.log 2>&1` exited **0**. Observed output: exactly one valid findings JSON block, 3/3 unique rows derived independently from surface-table.md, two pinned findings, one-word verdict and replay recorded. This validates packaging, not the Rust implementation.
