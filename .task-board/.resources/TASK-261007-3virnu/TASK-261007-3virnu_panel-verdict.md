# R141 panel A — CR-TASK-260929-2snjbb-2 revision 2

changes_requested

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus supplied patch produced exactly `3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214`. Temporary index only; no branch/commit/worktree mutation or writes to TASK-260929-2snjbb.

Bounded plan: decision is whether rev2 satisfies its three surface rows; frozen precondition is the exact patch/base/tree and surface-table; 60-minute ceiling, one plain-text outcome (under 64 KiB), no serial research prerequisite. Consuming slice is orchestrator recording review/rework of this CR. Exit is full row sweep, source-cited verdict and attached outcome. Sources: task AC, surface-table.md, producer-brief.md, results.md, coverage-map.md, hosted-precheck-3.md and review-verdict-rev1.md on the reviewed task, plus exact candidate Git blobs. Logbook record is task-scoped below; no direct control-root edits.

Commands and exit codes (this panel):
- `task-board m 'set_status(TASK-261007-3virnu, status=analysis)'`: 0.
- `git --version`, `rg --version`, `python3 --version`: 0; readiness verified. Missing agents/skills and .claude/skills reported by discovery; .codex/skills used.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3virnu/replay-v2.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b`: 0.
- `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev2.patch --output .temp/TASK-260929-2snjbb_change-request_rev2.patch`: 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3virnu/replay-v2.idx" git apply --cached .temp/TASK-260929-2snjbb_change-request_rev2.patch`: 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3virnu/replay-v2.idx" git write-tree`: 0; exact expected tree.
- Resource retrieval for surface-table, producer-brief, results, coverage-map, hosted-precheck-3 and review-verdict-rev1: each 0.
- Candidate `git show`, diff/stat and numbered source reads: 0. Archive extraction ran as a pipe without pipefail, so its composite exit 0 is NOT used as replay/gate evidence; replay and Git source inspection above are authoritative.
- `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b 3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214`: 0.
- `python3 .temp/TASK-261007-3virnu/static_attack.py timer`: **1**, expected red: cancellable firing task reaches its own abort hook before task registration.
- `python3 .temp/TASK-261007-3virnu/static_attack.py race`: **1**, expected red: final checker precedes awaited setup, no commit recheck.
- These two commands inspect source, not execute Rust behavior. Requested runtime tests have NOT RUN; no numeric exit is assigned to them.
- Initial query with unsupported `resources` field: 1. `schema(get)` invalid positional query: 1. Scoped corrected reads: 0. Initial `rm -f` index setup rejected before execution (no process exit code); fresh index used. `task-board logbook --help`: 1, unavailable command; unknown logbook mutation probes also failed. Findings are preserved as a task-scoped logbook entry in this outcome and task notes instead.
- No cargo/just/build/test command run. Hosted report: base 37539907712 four lanes success; 9/9 mutants killed, 0 survivors, accepted as attached evidence only. No invented hosted command exit codes.

Coverage: exactly 3/3 rows swept (1 held, 2 broken), 0 not-attacked. This measures row sweep only, not all AC compositions.

```verdict-findings
{
  "findings": [
    {
      "id": "timer-aborts-own-admission",
      "row": "check-in tickets and warning",
      "invariant": "AC4/AC5 scheduled check-ins must reach task registration and subsequent warning; timer invalidation must not cancel an already firing admission.",
      "mechanism": "codex-rs/ext/goal/src/check_in_clock.rs:85-89 keeps the firing JoinHandle in slot while on_fire is awaited. runtime.rs:577 awaits continue_if_idle inside that same timer task. GoalExtension::on_turn_start (extension.rs:248) calls note_turn_start, which fires abort_hook (background_wait.rs:198-204; check_in_clock.rs:50-52). The extension does not override turn_start_phase; contributors.rs:219-220 defaults to BeforeTaskRegistration. Core tasks/mod.rs:383-389 awaits that hook inline before tokio::spawn at line 422. Thus the continuation aborts its own task before registration; if reconcile_activity or later setup yields Pending, cancellation drops start_task with an ownerless reservation and no registered sampling task. Ticket was already consumed. This is a source-established cancellation path, not a claimed executed Tokio failure. Detach the fired timer from the cancellable sleeping slot before invoking the continuation, using identity-safe ownership.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3virnu/static_attack.py (source included below)",
          "command": "python3 .temp/TASK-261007-3virnu/static_attack.py timer",
          "expected_failure": "Actual exit 1, expected-red static source witness. No Rust execution. Request runtime fake-clock test with a deliberately pending turn-start reconciliation; assert all three check-ins register tasks and no bare reservation remains. Add a narrowing mutant retaining the fired handle through its callback."
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    },
    {
      "id": "revision-recheck-before-await-window",
      "row": "admission recheck and invalidation",
      "invariant": "AC7 catches receipt transitions between continuation check and turn start, by serialization or revision rejection.",
      "mechanism": "core/src/session/turn_input.rs:459-464 performs the sole goal admission check, then awaits PreparedTurnInputSettings::prepare (469), apply_started (479), context input processing, and start_task (530). ReceiptStore transitions use their own mutex and atomic revision (core/src/unified_exec/completion_receipt.rs:320,337-338), not the goal semaphore or reservation lock. Schedule a reserve/arm after the last check while preparation is pending: admission observed empty at revision R, receipt moves to Armed at R+1, then the automatic goal still starts without another revision comparison. Existing goal_background_wait_revision_recheck_catches_transition (turn_input_tests.rs:1419) arms before calling handle and installs an inline checker, so it does not exercise this interval.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3virnu/static_attack.py (source included below)",
          "command": "python3 .temp/TASK-261007-3virnu/static_attack.py race",
          "expected_failure": "Actual exit 1, expected-red static ordering witness; no live race executed. Request a barrier in preparation after the real goal checker, arm a receipt through the production store, resume and assert NotSubmitted rather than Started. Serialize transitions with commit or revalidate coherently at commit; narrowing mutant skips only that final recheck."
        }
      ],
      "severity": "bypass",
      "repeat-of": "rev1 note post-recheck-race-unexecuted / snapshot-coherence-followup"
    }
  ],
  "notes": [
    {
      "id": "execution-bound",
      "text": "Read-only replay and static attacks only. No builds, cargo, just, new Rust tests or executed runtime mutants. Hosted evidence is accepted from the attached precheck-3 report, not independently rerun or queried. Report supplies lane success and killed outcomes, not numeric command exit codes; these are not invented."
    },
    {
      "id": "rework-and-coverage",
      "text": "Rev1 epoch reset removed; actual production timer spawning is now present. Nevertheless stalled_subscription_fires_scheduled_checkins at tests/background_wait.rs:884 is a synchronous state model invoking require_claimed_ticket/note_turn_start/require_wait manually; it neither instantiates CheckInTimer nor calls continue_if_idle. Reported 9/9 mutant kills cover state/helper and Core entry attacks, not end-to-end scheduled launches. drop_check_in_registration is listed killed by three state tests in the hosted report; the producer also claims stalled test, which the supplied kill table does not establish."
    },
    {
      "id": "release-and-snapshot-bounds",
      "text": "note_release has no production caller in the candidate scope, only definition/tests; external control activation belongs to the subsequent slice. State empty reassessment tests do not prove a real late completion/release wake. Snapshot contents and revision are copied separately in pending_work.rs:51-65; coherent sampling needs a transition-during-read barrier test. No additional reproduced live failure claimed."
    },
    {
      "id": "size-api-context",
      "text": "Full replay includes checkpointed E1 prerequisites: 28 files, 3583 insertions/40 deletions. Producer states E2 rev2 delta is 7 goal files +567/-26. Smallest corrective slice is timer ownership and admission commit race with real vertical regressions, not a generalized research chain. No new model context fragment is injected (contributor returns empty Vec), nor established breaking wire/config/rollout change. New internal NotSubmittedReason has exhaustive app-server handling."
    }
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Attached exact-tree precheck-3 base 37539907712 reports four lanes success. Core public-entry fairness tests listed in coverage map; overgate_non_goal_triggers 37539976644 killed by both; Armed-only 37539955446 and read-error 37540085008 killed. Static goal_admission gate restricts Automatic + goal. Held for these attacks, not a claim of complete runtime composition."
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "timer-aborts-own-admission"
      ],
      "evidence": "Static timer witness exit 1. State-model hosted reuse_ticket_id 37540043763, warning_repeats 37540106313, reset_epoch_on_turn_start 37540019902, drop_check_in_registration 37539932669 killed. They do not exercise the timer-task cancellation path."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "broken",
      "findings": [
        "revision-recheck-before-await-window"
      ],
      "evidence": "Static ordering witness exit 1. Hosted skip_revision_recheck 37540065393 and preserve_ticket_across_invalidation 37539997698 killed. Existing core transition is sequential before handle, not AC7 latch after the last checker."
    }
  ],
  "free_hunt": {
    "budget_minutes": 5,
    "scope": "Timer ownership/cancellation, receipt snapshot coherence, lifecycle release/resume/disable, API/context and change size.",
    "result": "All three rows swept. Two static mechanisms elevated; snapshot coherence and external release/late wake remain bounded notes. No live behavioral reproduction claimed."
  }
}
```

## Task-scoped logbook — 2026-10-07

CR rev2 replay matches. Epoch and timer registration rework is present. New cancellation path aborts the firing timer during its own pre-registration lifecycle; AC7 still has an unprotected post-check await interval. Route these mechanisms to focused rework and real fake-clock/latch regressions. No recording verdict or status mutation made on the reviewed task.

## Static probe source

    from pathlib import Path
    import sys
    
    root = Path(__file__).parent
    cand = root / 'candidate/codex-rs'
    def read(p):
        return (cand / p).read_text()
    
    mode = sys.argv[1]
    if mode == 'timer':
        timer = read('ext/goal/src/check_in_clock.rs')
        runtime = read('ext/goal/src/runtime.rs')
        extension = read('ext/goal/src/extension.rs')
        contributors = read('ext/extension-api/src/contributors.rs')
        tasks = (root / 'tasks.rs').read_text()
        assert 'on_fire().await;' in timer
        assert '= Some(handle);' in timer
        assert 'handle.abort();' in timer
        assert 'background_wait.set_invalidation_hook(check_in_timer.abort_hook())' in runtime
        assert 'runtime.continue_if_idle().await' in runtime
        hook = extension[extension.index('fn on_turn_start'):extension.index('fn on_turn_stop')]
        assert 'note_turn_start();' in hook
        assert 'reconcile_activity(input.thread_store, &permit)' in hook
        assert 'fn turn_start_phase' not in extension
        assert 'TurnStartPhase::BeforeTaskRegistration' in contributors
        start = tasks[tasks.index('pub(crate) async fn start_task'):]
        assert start.index('emit_turn_start_lifecycle(') < start.index('tokio::spawn(')
        print('STATIC WITNESS: firing handle remains cancellable during its own inline BeforeTaskRegistration hook; pending await can cancel continuation before task registration.')
        sys.exit(1)
    elif mode == 'race':
        source = read('core/src/session/turn_input.rs')
        start = source[source.index('async fn start_if_idle('):source.index('async fn steer(')]
        assert start.count('check_goal_admission(') == 1
        check = start.index('check_goal_admission(')
        prepare = start.index('PreparedTurnInputSettings::prepare(')
        launch = start.index('.start_task(')
        assert check < prepare < launch
        assert '.await' in start[prepare:launch]
        assert 'receipt_store' not in start
        print('STATIC WITNESS: sole revision check precedes awaited preparation and task start; receipt store transitions are not serialized with that interval.')
        sys.exit(1)
    else:
        raise ValueError(mode)

Artifact verification: standalone Python JSON/schema/unique-row/size check exited 0; exactly one block, 3/3 rows, 2 findings, under 64 KiB.
