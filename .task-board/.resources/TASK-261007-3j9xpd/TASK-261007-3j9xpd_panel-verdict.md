# DELTA panel verdict — CR-TASK-260929-2snjbb-2 revision 2

changes_requested

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus attached rev2 patch produced **exactly** candidate tree `3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214` through a temporary index. No worktree/index mutation outside the task scratch index; no source edits, builds or underlying-task writes.

Commands run directly (exit codes):

| Command | Exit | Evidence |
|---|---:|---|
| `task-board m 'set_status(TASK-261007-3j9xpd, status=analysis)'` | 0 | Own-task lifecycle only |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev2.patch --output .temp/TASK-261007-3j9xpd/rev2.patch` | 0 | Read-only patch retrieval |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3j9xpd/replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Replay base |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3j9xpd/replay.idx" git apply --cached .temp/TASK-261007-3j9xpd/rev2.patch` | 0 | Patch replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3j9xpd/replay.idx" git write-tree` | 0 | Exact expected tree printed |
| `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b 3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214` | 0 | Patch whitespace |
| `python3 .temp/TASK-261007-3j9xpd/static_attack.py fixed` | 0 | Old epoch defect and absent timer wiring corrected; static only |
| `python3 .temp/TASK-261007-3j9xpd/static_attack.py timer-ownership` | 1 | Expected-red source witness: fired callback still owned by abortable slot |
| `python3 .temp/TASK-261007-3j9xpd/static_attack.py stale-install` | 1 | Expected-red source interleaving: stale install cancels live timer |

Artifact validation: `python3 .temp/TASK-261007-3j9xpd/validate_verdict.py` exited 0 (one JSON object/block, required fields and reproductions, 3/3 unique surface rows, pinned sources and verdict). Packaging script exited 0.

Expected-red probes **failed**, as intended; neither is a passing Rust test or an executed Tokio concurrency reproduction. Source-bound call-chain assertions succeeded before each diagnostic. Full replay/static-probe source below permits reproduction without builds.

Read-only inputs retrieved with `task-board resource get` (each exit 0): `surface-table.md`, `producer-brief.md`, `TASK-260929-2snjbb_review-verdict-rev1.md`, `TASK-260929-2snjbb_results.md`, `TASK-260929-2snjbb_hosted-precheck-3.md`, `TASK-260929-2snjbb_coverage-map.md`, `TASK-260929-2snjbb_mutants.json`. Candidate `git archive` and extraction exited 0. `git show`, `git ls-tree`, scoped diffs and source reads supplied the cited code. No source evidence depends on the current checkout tree.

Read diagnostics, not gates: first query with unsupported `resources` field exited 1 and was repaired with `description scope ac notes`; a search across absent skill directories exited 2. The bundled reviewer role link was absent (read failed); assignment panel contract supplies the review-round rules. Unsupported positional schema and logbook mutation lookups returned JSON errors despite process exit 0; no successful mutation or absence was inferred from these. Logbook is carried below as own-task outcome evidence under the run write-boundary contract.

Plan: unblock the recording reviewer’s rev2 decision, not implementation; frozen input is CR rev2 base/tree/patch; grammar not applicable beyond the required verdict JSON schema. Worker ceiling 30 minutes; one text outcome, no archives attached; zero new serial prerequisites. Exit: replay plus 4/4 previous finding records, 3/3 surface results, bounded hunt and persisted verdict. Consumer: recording reviewer/orchestrator; rework goes into this existing goal leaf.

## Logbook entry — 2026-10-07

DELTA review replay matches rev2 tree. Both earlier defect mechanisms have code corrections, but the new production scheduler has two cancellation/installation ownership regressions. Existing hosted evidence reports 9/9 mutant kills yet its scheduler-labelled tests only exercise state methods. Request focused fake-clock runtime latch tests and production timer ownership fixes in the same leaf. No board mutation, note, handoff, accept or reject was made on TASK-260929-2snjbb. This logbook entry travels in this task-scoped outcome rather than editing control-root LOGBOOK.md.

```verdict-findings
{
  "findings": [
    {
      "id": "fired-timer-aborted-before-admission-reply",
      "row": "check-in tickets and warning",
      "invariant": "Scheduled check-ins must preserve the existing automatic-turn admission/accounting lifecycle; invalidating a consumed ticket must not cancel the admitted continuation before its Started reply is accounted.",
      "mechanism": "codex-rs/ext/goal/src/check_in_clock.rs:84-88 keeps the timer JoinHandle in the cancellable slot throughout on_fire().await. runtime.rs:574-582 runs continue_if_idle inside that same task. Its start_turn_if_idle awaits the Core reply (runtime.rs:688-700; core/src/session/mod.rs:1023), while the before-registration on_turn_start hook (extension.rs:248) invalidates state and aborts that slot (background_wait.rs:193-204; check_in_clock.rs:48-50). If cancellation is processed while the session callback awaits reconciliation, Core continues its already-queued turn, but the timer waiter drops before mark_goal_continuation at runtime.rs:700. The turn is not marked automatic for accounting.rs:219-228, so the existing empty-response guard can miss it. This is a new scheduler ownership regression, not proof that every check-in is lost.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3j9xpd/static_attack.py (full source in this outcome)",
          "command": "python3 .temp/TASK-261007-3j9xpd/static_attack.py timer-ownership",
          "expected_failure": "Executed exit 1: exact-source ownership/call-chain witness finds the fired task still cancellable while awaiting Core reply. Static only, not Rust/Tokio execution. Requested production regression: inject fake clock into GoalRuntimeHandle, latch the before-registration reconciliation after note_turn_start, process cancellation, finish Core start, and assert automatic-goal bookkeeping is recorded. Existing stalled_subscription_fires_scheduled_checkins never creates CheckInTimer.",
          "pinned_blobs": [
            "git-blob:38e3444d2446f7710aa98231c61284ac13429e1a",
            "git-blob:92f3f4c4f9f21461fbb229930470308b08f6b84f",
            "git-blob:8647c6005bf6131884dc395aa59914d1be4a2182",
            "git-blob:1272dcfbf6129a715e5053f5c79aff1f8b8339ea",
            "git-blob:8414dcfa10c4733b08f8cf7e55fbce6b5c2d700d",
            "git-blob:94c47023ead7ab1100ade55d75bb26f30d3c0c05",
            "git-blob:2a4707c2de74d96c1113beedf6972355b56db946",
            "git-blob:bb2b162ce0aee7bfee48f253708828508c5df858"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    },
    {
      "id": "stale-timer-install-clobbers-current-registration",
      "row": "admission recheck and invalidation",
      "invariant": "AC4/AC9: invalidated or superseded waits cannot replace the live generation timer and prevent its fallback check-in.",
      "mechanism": "codex-rs/ext/goal/src/runtime.rs:656-659 captures generation, drops the goal permit, then installs a timer without validating the registration atomically with installation. check_in_clock.rs:82-88 unconditionally cancels the current slot. On a multithread executor A can be preempted after dropping the permit; invalidation increments generation, and B can evaluate/register/spawn the new generation deadline. A resumes and cancels B to install the old generation timer. At fire, background_wait.rs:380-395 rejects A against B’s newer registration; no timer is left for B, so a stalled subscription does not check in until another event arrives. Generation checks reject the stale callback but do not protect the current timer from stale installation.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3j9xpd/static_attack.py (full source in this outcome)",
          "command": "python3 .temp/TASK-261007-3j9xpd/static_attack.py stale-install",
          "expected_failure": "Executed exit 1: source-pinned legal interleaving leaves registration=(1800,g1), slot=(1800,g0); g0 claim is false and g1 has no timer. Static interleaving witness, not Rust execution. Requested runtime latch after permit drop/before install: invalidate, install g1 through a second continuation, resume g0 install, advance fake clock, and assert g1 still fires. No existing hosted mutant exercises timer installation ordering.",
          "pinned_blobs": [
            "git-blob:38e3444d2446f7710aa98231c61284ac13429e1a",
            "git-blob:92f3f4c4f9f21461fbb229930470308b08f6b84f",
            "git-blob:8647c6005bf6131884dc395aa59914d1be4a2182"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Prior round 4/4 finding records checked: both epoch-reset IDs are fixed by note_turn_start retaining wait_started_at, confirmed by static fixed probe exit 0 and hosted reset_epoch_on_turn_start 37540019902. Both discarded-deadline IDs have production timer/claim/re-entry wiring now, confirmed by fixed probe; runtime ownership and concurrent installation are newly broken, not the old missing-registration mechanism. No repeat-of class carried forward.",
    "Execution boundary: this panel ran no cargo, just, builds, Rust tests, or new hosted mutants. Reused attached TASK-260929-2snjbb_hosted-precheck-3.md: exact tree 3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214, snapshot ce274182, base run 37539907712 reports small/lint/core/app-server success and 9/9 killed mutants, 0 survivors. Provider job exit codes are not present in that summary; they are not fabricated here.",
    "Coverage: 3/3 surface rows swept, 9/9 reported narrowing mutants killed; 0 tests in ext/goal/tests construct CheckInTimer or inject CheckInClock. stalled_subscription_fires_scheduled_checkins and invalidation_cancels_armed_check_in drive state/helper calls and a counter hook, not production timer/idle re-entry. drop_check_in_registration narrows state registration, not runtime spawning. Request real timer lifecycle/ordering regressions in this implementation leaf, not another research prerequisite.",
    "Existing bounds retained: snapshot coherence across independent locks and post-Core-recheck async start window have no new runtime reproduction; do not infer they are safe from the sequential test-double latch-named test. note_release still has no production caller; external activation/release controls are stage 2e. Policy remains intentionally disabled by default; no missing-activation finding.",
    "No new model-visible fragment: contributor returns an empty vector. No new breaking app-server wire/config/CLI/rollout change established. Rework is 7 files +567/-26 (285 logic plus 282 tests); base replay includes checkpointed E1 (+3583/-40 total) and is not the isolated E2 review size.",
    "Tokio cancellation fact checked against official JoinHandle::abort documentation: https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html#method.abort. Abort targets the task attached to the handle; it is not limited to its initial sleep. Cancellation timing is schedule-dependent, hence the requested latch tests and explicit static-only witness limit."
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "detail": "Held against named hosted attacks on exact rev2 tree: core handle/start_if_idle fairness tests; overgate_non_goal_triggers 37539976644, treat_read_error_as_empty 37540085008, gate_only_queued_ignoring_armed 37539955446 killed. Static scope guard remains Automatic + goal only; read errors return Wait. Does not certify every concurrent composition."
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "detail": "Prior epoch/registration defects fixed. New fired-timer-aborted-before-admission-reply regression; static witness exit 1. Reused ticket/warning/epoch mutant kills 37540043763, 37540106313, 37540019902, registration mutant 37539932669 do not execute the abortable timer."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "broken",
      "detail": "New stale-timer-install-clobbers-current-registration regression; static witness exit 1. Reused skip_revision_recheck 37540065393 and preserve_ticket_across_invalidation 37539997698 killed; synchronous state invalidation and permit-before-sleep checks hold only within their named bounds."
    }
  ],
  "free_hunt": [
    "Bounded free hunt (5-minute ceiling): inspected runtime cancellation/registration ordering, timer ownership, semaphore drop, lifecycle callers, snapshot/recheck windows, context/wire exposure and delta size. Two scheduler regressions recorded in existing rows; no additional blocking mechanism. Existing snapshot/race/release limits remain notes."
  ]
}
```

## Source-pinned static witnesses

Save as `.temp/TASK-261007-3j9xpd/static_attack.py` and run the commands above from a repository containing the candidate objects. These inspect exact blobs and trace legal operations, rather than executing Rust.

```python
import subprocess
import sys

TREE = '3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214'

def source(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)

def section(text, first, last):
    return text.split(first, 1)[1].split(last, 1)[0]

wait = source('codex-rs/ext/goal/src/background_wait.rs')
timer = source('codex-rs/ext/goal/src/check_in_clock.rs')
runtime = source('codex-rs/ext/goal/src/runtime.rs')
extension = source('codex-rs/ext/goal/src/extension.rs')
if sys.argv[1] == 'fixed':
    turn_start = section(wait, 'pub fn note_turn_start', '/// Invalidates tickets on steering.')
    assert 'invalidate_tickets()' in turn_start
    assert 'wait_started_at = None' not in turn_start
    assert 'drop(goal_state_permit);\n                    if let Some(deadline)' in runtime
    assert 'self.spawn_check_in_timer(deadline, generation)' in runtime
    assert 'state.claim_due_deadline(deadline, generation, clock.now())' in runtime
    assert 'runtime.continue_if_idle().await' in runtime
    assert 'clock.sleep_until(deadline).await;' in timer
    print('PASS: epoch preserved; Wait drops permit before timer; callback claims then re-enters. Static wiring only.')
    sys.exit(0)
if sys.argv[1] == 'stale-install':
    assert 'let generation = self.inner.background_wait.generation();\n                    drop(goal_state_permit);' in runtime
    assert 'self.spawn_check_in_timer(deadline, generation);' in runtime
    install = section(timer, 'pub fn spawn<F>', '/// Aborts the pending timer')
    assert 'self.cancel();' in install
    assert '*self.slot.lock().unwrap_or_else(PoisonError::into_inner) = Some(handle);' in install
    claim = section(wait, 'pub fn claim_due_deadline', '/// Installs the hook')
    assert 'armed.generation != generation' in claim
    # Legal multithread interleaving of the separately locked operations above.
    # A evaluated Wait(g0), captured g0 and dropped its permit, then was preempted.
    registration = (1800, 0)
    generation_a = registration[1]
    # Steering/turn-start invalidation, then a newer idle B arms/spawns g1.
    registration = (1800, 1)
    slot = registration
    # A resumes. Unconditional spawn cancels B and installs stale g0.
    slot = (1800, generation_a)
    accepted = slot == registration
    assert not accepted
    print('FAIL: legal source interleaving leaves registration=(1800,g1), timer-slot=(1800,g0); stale A replaces/cancels current B, then claim rejects g0. No timer remains for g1. Static interleaving witness only, not a Tokio execution.')
    sys.exit(1)
assert sys.argv[1] == 'timer-ownership'
callback = section(timer, 'let handle = tokio::spawn(async move {', '});')
assert callback.strip() == 'clock.sleep_until(deadline).await;\n            on_fire().await;'
assert '*self.slot.lock().unwrap_or_else(PoisonError::into_inner) = Some(handle);' in timer
assert 'handle.abort();' in timer
assert 'move || abort_timer_slot(&slot)' in timer
assert 'background_wait.set_invalidation_hook(check_in_timer.abort_hook());' in runtime
assert 'runtime.background_wait_state().note_turn_start();' in extension
invalidate = section(wait, 'fn invalidate_tickets(&mut self)', 'fn fire_invalidation_hook')
assert 'self.fire_invalidation_hook();' in invalidate
assert 'self.inner.accounting_state.mark_goal_continuation(turn_id);' in runtime
core = source('codex-rs/core/src/session/mod.rs')
handlers = source('codex-rs/core/src/session/handlers.rs')
tasks = source('codex-rs/core/src/tasks/mod.rs')
api = source('codex-rs/ext/extension-api/src/contributors.rs')
assert 'reply_rx.await.unwrap_or(Err(CodexErr::InternalAgentDied))' in core
assert handlers.index('let result = turn_input::handle(&sess, *request, mode, sub.id.clone()).await;') < handlers.index('let _ = reply.send(result);')
assert 'codex_extension_api::TurnStartPhase::BeforeTaskRegistration' in tasks
assert 'TurnStartPhase::BeforeTaskRegistration' in section(api, 'fn turn_start_phase', '///')
print('FAIL: fired timer retains its own JoinHandle throughout on_fire().await; before-registration turn-start hook aborts that handle while continuation awaits Core reply. No slot retirement separates pending sleep from admitted callback. A schedule cancelling the reply waiter skips mark_goal_continuation. Static source witness; no Tokio/Rust execution.')
sys.exit(1)
```
