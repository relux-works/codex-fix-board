# R141 panel B revision 2 — ready for review

changes_requested

Read-only independent panel for CR-TASK-260929-2snjbb-2. No mutation was made on TASK-260929-2snjbb. No builds, Cargo/Just commands, local Rust tests, commits, branch changes, or hosted jobs were launched.

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus the attached rev2 patch produces tree `3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214`, exactly the expected candidate. The review uses that tree rather than the worktree HEAD. Worktree HEAD equals the stated base; `git rev-list --count HEAD..main` reports 0. No tracked repository changes were made.

Commands actually run (exit codes are literal):

| Command / inspection | Exit | Result |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261007-uct3ql, status=analysis)'` | 0 | Own panel lifecycle only |
| Tool readiness: `command -v task-board git rg python3`, `git --version`, `rg --version`, `task-board --help` | 0 | Logs under `.temp/TASK-261007-uct3ql/` |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-uct3ql-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Temporary index |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev2.patch --output .temp/TASK-260929-2snjbb_change-request_rev2.patch` | 0 | Read-only source retrieval |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-uct3ql-replay.idx" git apply --cached .temp/TASK-260929-2snjbb_change-request_rev2.patch` | 0 | Patch replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-uct3ql-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b 3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214` | 0 | Whitespace check only |
| `python3 .temp/TASK-261007-uct3ql/static_attack.py epoch` | 0 | Source fix/wiring check; no behavioral proof |
| `python3 .temp/TASK-261007-uct3ql/static_attack.py scheduled-test` | 1 | Expected-red: required scheduled regression uses manual helper calls |
| `task-board q 'get(TASK-260929-2snjbb) { description scope ac }'` | 0 | All ACs inspected |
| Board surface/brief/results/coverage/precheck3/rev1 verdict resource reads; candidate `git show`, diff, archive/inspection and source searches | 0 | Cited below; archive extraction only, no binary attachment |
| Own task checklist read and `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives; no active run goal |
| `git status --short`, `git rev-parse HEAD`, `git rev-list --count HEAD..main` | 0 | Clean tracked worktree; pinned base; count 0 |

Read/discovery failures, not validation successes: initial `rg --files agents/skills .claude/skills .codex/skills ...` exited 2 because two directories are absent; initial `get(...){description scope ac resources notes}` exited 1 (unsupported resources field); `schema(get)` exited 1 (unsupported positional syntax), corrected `schema(operation="get")` exited 0; first reviewer-role cat at the curator skill path exited 1 (missing path), corrected read at `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md` exited 0; guessed `git show ...:codex-rs/core/src/session/extension_lifecycle.rs` failed (path absent) and the combined discovery command exited 1. No failed read was treated as absence of behavior. A global `rg --files` discovery with no matching output exited 1 and was replaced by explicit symlink inspection.

Decision: request the missing real scheduled runtime regression and a runtime-spawn narrowing mutant in the same leaf. Existing state-machine tests and hosted mutant kills remain useful. This panel does not demand a new research chain or claim a reproduced scheduler malfunction.

AC sweep: AC1–AC3 held for the named hosted scope/read-failure/state attacks; AC4–AC5 lack real timer/continuation regression proof; AC6 empty-state late-completion reassessment is tested, actual runtime wake is bounded; AC7 sequential revision attack held, latch/post-check window is unexecuted; AC8 core cancellation/release admission held, external release wiring is deferred; AC9 state invalidation/resume attacks held, real timer cancellation is unexecuted; AC10 source confirms permit drop before spawn and synchronous state evaluation, no dynamic semaphore test claimed.

Research bounds: one decision (whether this panel recommends accepting rev2); no new grammar; 30-minute ceiling, one text outcome, no serial research prerequisite, five-minute maximum free hunt. Consuming action is same-leaf rework of the scheduler regression, followed by the recording reviewer. The replay, three-row sweep and recommendation satisfy this panel's exit criteria.

Sources: authoritative board resources under `.task-board/.resources/TASK-260929-2snjbb/`: `surface-table.md`, `producer-brief.md`, `e2-rework-brief-rev2.md`, `TASK-260929-2snjbb_results.md`, `TASK-260929-2snjbb_coverage-map.md`, `TASK-260929-2snjbb_hosted-precheck-3.md`, `TASK-260929-2snjbb_recorded-review-verdict-rev1.md`; exact candidate paths/lines in the structured findings. Sources were supplied locally; no external web claims are made.

Logbook entry (task-scoped outcome, no control-root edit): rev2 replay matched exactly; the epoch and timer wiring corrections are present; the named scheduler regression still manually simulates state transitions. Preserve hosted 9/9 kills without attributing them to execution of the real scheduler. Request a same-leaf fake-clock runtime test and a spawn-path narrowing mutant. Do not mutate or route the reviewed source task from this panel.

```verdict-findings
{
  "findings": [
    {
      "id": "scheduled-checkin-regression-not-exercised",
      "row": "check-in tickets and warning",
      "invariant": "AC4-AC5 and Evidence That Counts: scheduled check-ins must be exercised through the real timer/continuation entry point, with fake time alone driving 30/60/120 minutes and the warning; a manually called helper does not establish runtime behavior.",
      "mechanism": "codex-rs/ext/goal/tests/background_wait.rs:884-971 is a synchronous #[test]. At :906 it calls require_claimed_ticket, whose definition at :69-90 manually calls claim_due_deadline, evaluate_continuation and check_admission. It manually calls note_turn_start and require_wait too. No CheckInClock, CheckInTimer or GoalRuntimeHandle is instantiated. Thus the newly added runtime.rs:568-580 callback and check_in_clock.rs:78-88 scheduler are outside this regression. The drop_check_in_registration mutant attacks state registration, not timer spawning or runtime re-entry. The required rework regression remains a simulation, while results/coverage claim actual scheduled firing. This is an observed coverage/attestation defect, not an assertion that the production scheduler has been executed and failed.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-uct3ql/static_attack.py (source embedded below)",
          "command": "python3 .temp/TASK-261007-uct3ql/static_attack.py scheduled-test",
          "expected_failure": "Observed exit 1: the exact candidate test uses synchronous manual state calls and does not exercise an injected clock, timer, or runtime continuation. Static pinned-source coverage reproduction only; no Rust test or runtime mutant was executed.",
          "candidate_tree": "3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214"
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "requested_regression": "Replace or supplement stalled_subscription_fires_scheduled_checkins with an enabled runtime fixture and injectable manual clock: initiate one real idle evaluation with an unchanged Armed receipt, advance fake time without manual evaluate/claim/admit calls, observe actual starts at 30/60/120, then exactly one warning and an active/wakeable goal. Retain the current state tests.",
      "requested_narrowing_mutant": "Keep BackgroundWaitState deadline registration intact but suppress the runtime Wait-arm spawn_check_in_timer call, or allow only its first spawn. The real scheduled regression must fail. NOT RUN in this panel; requires the serialized hosted lane. No new research leaf is needed."
    }
  ],
  "notes": [
    {
      "id": "epoch-and-wiring-fix-present",
      "text": "The prior turn-start-resets-check-in-origin/checkin-epoch-reset-on-turn-start mechanism is corrected: background_wait.rs:480-484 only invalidates tickets and preserves epoch/count. Runtime :662-665 drops the goal permit before spawning the timer. Static epoch probe exited 0. The prior discarded-deadline implementation is replaced by a real spawn call. These source fixes are acknowledged; the finding concerns the required regression evidence, not a claim that either original source defect is unchanged."
    },
    {
      "id": "timer-self-cancellation-followup",
      "text": "Unexecuted concern, not a blocking finding: CheckInTimer keeps the fired callback task in its abort slot. A runtime callback awaits start_turn_if_idle; on_turn_start calls note_turn_start, whose installed hook aborts that slot. A real scheduled runtime test should verify turn-start cancellation does not cancel the awaiting continuation before mark_goal_continuation or strand lifecycle/accounting work. The direct state test cannot exercise this interaction. No behavioral failure was reproduced."
    },
    {
      "id": "snapshot-and-post-check-window",
      "text": "Retained unexecuted bound from rev1: pending_work.rs:51-64 takes receipt/mailbox snapshots separately and loads revision last; turn_input.rs:459-484 rechecks before asynchronous settings preparation and later task start. Existing tests exercise a transition before handle with a test-double checker, not a latch through the real BackgroundWaitState and admission/start window. Request a barrier-based test if this race is investigated; no failing behavior established by this panel."
    },
    {
      "id": "release-and-late-completion-bound",
      "text": "note_release still has no production caller in this preparatory stage. State tests show empty-snapshot reassessment and reset; core public handle tests show release/cancellation opens admission. They do not prove a production late-completion or release event wakes the runtime. Activation/control wiring is deferred to stage 2e and is not a new blocking finding here."
    },
    {
      "id": "evidence-provenance",
      "text": "Reused only attached precheck 3, which names the exact replayed tree and snapshot ce274182. Base run 37539907712 records success in app-server/small/lint/core; nine mutant runs record kills. Those hosted results are accepted as attached execution evidence, not rerun locally or independently fetched from GitHub. The truncated local CR log is not counted as proof of an unseen command. Attached producer reports local just fmt exit 1 (environmental stable/nightly setting mismatch); it is not presented as green."
    }
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Attached exact-tree base 37539907712 and core public handle/start_if_idle tests goal_background_wait_blocks_goal_but_admits_user_and_followup and goal_background_wait_ignores_non_goal_triggers. overgate_non_goal_triggers run 37539976644 kills both. treat_read_error_as_empty run 37540085008 and gate_only_queued_ignoring_armed run 37539955446 are killed. Static goal_admission.rs:30 restricts the check to Automatic plus goal; failures remain explicit. Held only for these attacks, not every possible fairness ordering."
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "scheduled-checkin-regression-not-exercised"
      ],
      "evidence": "Pinned-source coverage probe expected-red exit 1. Hosted state-path mutants reuse_ticket_id 37540043763, warning_repeats 37540106313, reset_epoch_on_turn_start 37540019902 and drop_check_in_registration 37539932669 were killed. The epoch correction is present, but none of these named tests executes the actual scheduled runtime path. This result identifies missing mandatory runtime regression evidence, not a reproduced runtime malfunction."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "held",
      "evidence": "Attached exact-tree base core public handle tests goal_background_wait_revision_recheck_catches_transition and goal_background_wait_allows_when_empty_and_after_release. skip_revision_recheck run 37540065393 and preserve_ticket_across_invalidation run 37539997698 are killed in the goal state tests. Static invalidation hooks reset registrations and runtime drops the semaphore before scheduling. Held for the named executed attacks, with real checker race/release/cancellation limits recorded separately."
    }
  ],
  "free_hunt": {
    "budget_minutes": 5,
    "method": "Bounded static hunt after surface sweep; no builds or additional runtime executions.",
    "scope": [
      "timer callback/abort ownership",
      "snapshot coherence and post-check awaits",
      "release callers",
      "protocol/app-server/context surface"
    ],
    "additional_blocking_findings": [],
    "notes": [
      "timer-self-cancellation-followup",
      "snapshot-and-post-check-window",
      "release-and-late-completion-bound"
    ],
    "result": "No additional reproduced blocking mechanism. New NotSubmittedReason has an exhaustive app-server handling arm; no serialized API/config/rollout break established. TurnInputContributor returns an empty context-fragment vector."
  }
}
```

## Executed static probe source

```python
import subprocess
import sys

TREE = '3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214'
def source(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)

mode = sys.argv[1]
state = source('codex-rs/ext/goal/src/background_wait.rs')
runtime = source('codex-rs/ext/goal/src/runtime.rs')
tests = source('codex-rs/ext/goal/tests/background_wait.rs')
if mode == 'epoch':
    hook = state.split('pub fn note_turn_start(&self)', 1)[1].split('pub fn note_steering', 1)[0]
    assert 'invalidate_tickets()' in hook
    assert 'wait_started_at =' not in hook
    assert 'check_ins_used =' not in hook
    assert 'check_ins_keep_epoch_across_admitted_turns' in tests
    assert 'self.spawn_check_in_timer(deadline, generation)' in runtime
    print('PASS: turn-start preserves epoch/count; runtime consumes the deadline via timer spawn. Static source check only.')
elif mode == 'scheduled-test':
    test = tests.split('fn stalled_subscription_fires_scheduled_checkins()', 1)[1].split('#[test]', 1)[0]
    helper = tests.split('fn require_claimed_ticket(', 1)[1].split('#[test]', 1)[0]
    assert 'require_claimed_ticket(&state, deadline, deadline)' in test
    assert 'state.claim_due_deadline(' in helper
    assert 'state.evaluate_continuation(' in helper
    assert 'state.check_admission(' in helper
    assert 'state.evaluate_continuation(' in test
    assert 'CheckInTimer' not in tests and 'CheckInClock' not in tests
    assert 'GoalRuntimeHandle' not in tests
    backend = source('codex-rs/ext/goal/tests/goal_extension_backend.rs')
    assert 'background_wait_state' not in backend
    print('FAIL: claimed scheduled regression is a synchronous manual state-machine simulation; no injected clock, real timer, runtime continuation, or time-only wake. A runtime spawn-removal mutant is not exercised by this test.')
    sys.exit(1)
else:
    raise ValueError(mode)

```

Artifact verification: `python3 .temp/TASK-261007-uct3ql/validate_verdict.py` exited 0: exactly one valid verdict-findings JSON block, 3/3 unique surface rows, required finding/reproduction fields, one-word verdict, and text size below 64 KiB. Outcome written outside the managed worktree under `/tmp/TASK-261007-uct3ql/` as requested; control-root persistence occurs only through resource CRUD.
