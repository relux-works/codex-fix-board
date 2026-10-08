# R141 delta panel — CR-TASK-260929-2snjbb-4 rev4

changes_requested

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` + `TASK-260929-2snjbb_change-request_rev4.patch` produced `c7180fab47012a651662cd207a48caafdf7b10db` via temporary index; **exact expected candidate tree match**. A second write-tree returned the same tree. Repository tracked diff is empty. Nothing was recorded on the reviewed task: all task-board mutations target this panel task only.

Review plan: decide whether rev4 closes the rev3 merged findings; pinned precondition is the replayed CR tree (no external grammar). Single panel, no serial prerequisite, bounded to 45 minutes including packaging and 5 minutes of free hunt. Artifact budget is one plain-text outcome with embedded reproduction source/logs. Consumer is the orchestrator's merged verdict and same-leaf E2 correction; no additional research leaf.

Previous findings: five entries, three unique classes. Scheduler composition and persistent-settings rejection are addressed; revision-check/publication atomicity still fails the stated ordering contract. See the structured finding for the remaining mechanism and requested production regression.

## Commands and observed exit codes

| Command actually run here | Exit | Interpretation |
|---|---:|---|
| `task-board m 'set_status(TASK-261007-2j7e5c, status=analysis)'` | 0 | Panel lifecycle only |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev4.patch --output .temp/TASK-260929-2snjbb_change-request_rev4.patch` | 0 | Read-only input |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2j7e5c-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Replay base |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2j7e5c-replay.idx" git apply --cached .temp/TASK-260929-2snjbb_change-request_rev4.patch` | 0 | Replay patch |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2j7e5c-replay.idx" git write-tree` (twice) | 0 each | Exact `c7180fab47012a651662cd207a48caafdf7b10db` |
| `task-board resource get` for surface-table, rev3 verdict, producer brief, results, coverage-map, mutants and hosted-precheck-6, each to task-scoped `.temp/` | 0 each | Inputs read successfully |
| `task-board q 'get(TASK-260929-2snjbb) { description ac }'` | 0 | Task normative AC |
| `task-board q 'get(TASK-260929-2snjbb) { description scope ac resources notes }'` | 1 | Unsupported resources field, read failure recovered; not an absent-resource claim |
| `cat .../project-management/references/research-workflow.md .../project-management/.roles/reviewer/role.md` (lazy skill path) | 1 | Missing role reference, installed role path read successfully afterward (0) |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directive; run not goal-bound |
| `set -o pipefail; git archive TREE <candidate paths> | tar -x -C .temp/TASK-261007-2j7e5c-cand` | 0 | Bounded extraction; audited bytes verified again against pinned git show |
| `python3 .temp/TASK-261007-2j7e5c/static_attack.py scope` | 0 | Static predicate/error audit; hosted public-entry execution reused |
| `python3 .temp/TASK-261007-2j7e5c/static_attack.py scheduler` | 0 | Static real-runtime composition audit; hosted mutant execution reused |
| `python3 .temp/TASK-261007-2j7e5c/static_attack.py publication` | **1** | **Expected failing source lock/order witness**, not an executed Rust race |
| `python3 .temp/TASK-261007-2j7e5c/static_attack.py free-hunt` | 0 | Source audit of production test-observation retention; nonblocking note |
| `git diff --exit-code` | 0 | Tracked worktree unchanged |
| `git diff --check` | 0 | No whitespace delta |

Each static audit ran as a standalone process with stdout/stderr redirected to the corresponding `scope-01.log`, `scheduler-01.log`, `publication-01.log`, `free-hunt-01.log`; redirection preserves the process's actual exit code. No Rust validation was run. Hosted job conclusions and mutant kills are reused evidence, **not invented numeric command exits**. The artifact-format check and board attachment/handoff have their own tool-reported exit codes after this document is written.

## Sources and result journal

Normative read-only inputs are board resources on the reviewed task: `surface-table.md`, `TASK-260929-2snjbb_review-verdict-rev3.md`, `e2-rework-brief-rev4.md`, `producer-brief.md`, `TASK-260929-2snjbb_results.md`, `TASK-260929-2snjbb_coverage-map.md`, `TASK-260929-2snjbb_mutants.json`, `TASK-260929-2snjbb_hosted-precheck-6.md`. Candidate citations below mean `git show c7180fab47012a651662cd207a48caafdf7b10db:<path>`, not the worktree's HEAD. The hosted report explicitly binds snapshot `6abf59d5`, base run `37569076583`, all four lanes and 15/15 kills to this tree. No direct GitHub re-fetch or unseen local-validation tail is claimed.

Rows were appended before advancing to the next row:

- gate scope and fairness: held; static scope audit exit 0; hosted precheck 6 public-entry fairness tests and overgate_non_goal_triggers kill reused (37569198182). Read failure/Armed attacks also reused. Bound: policy default-disabled and release/completion activation deferred.
- check-in tickets and warning: held; scheduler static composition audit exit 0; real suite test in hosted precheck 6 plus runtime-only break_runtime_wait_arm_reentry kill reused (37569106946). Prior simulated-runtime finding fixed. Timer/ticket/epoch/warning kills reused; full future activation not inferred.
- admission recheck and invalidation: broken; publication static independent-lock witness exit 1 expected-red, not a Rust race execution. revision-recheck-before-await-window repeats as cross-thread final-check-to-publication window. Hosted residual-before-comparison latch and settings/invalidation kills acknowledged.

```verdict-findings
{
  "findings": [
    {
      "id": "revision-recheck-before-await-window",
      "row": "admission recheck and invalidation",
      "invariant": "AC7 and rev4 rework item 1: Arm before the last_started_turn_id publication must reject the automatic goal start; the final revision comparison and publication must be serialized against receipt transitions.",
      "mechanism": "codex-rs/core/src/session/goal_admission.rs:131-137 holds Session.state and compares via recheck_goal_admission_before_start at :133, then writes last_started_turn_id at :137. The caller holds active_turn (core/src/tasks/mod.rs:374-407), but neither lock excludes Arm: completion_receipt.rs:402 acquires only CompletionReceiptStore.state, updates the phase at :450 and bumps the shared atomic revision at :466. pending_work.rs:51-64 copies lists under short-lived store/mailbox guards then loads a revision; those guards are already gone when the helper returns at goal_admission.rs:104. Legal cross-thread schedule with a pre-reserved receipt: A finishes the final comparison at R; B acquires the independent receipt mutex, Arms and bumps R+1; A resumes and writes last_started_turn_id. There is no further comparison or common transition guard. No await closes cooperative task yielding only, not OS preemption or simultaneous worker threads. Thus Arm precedes the explicitly documented publication point but the automatic turn still publishes. The new residual test pauses before publish_goal_turn_if_revision_matches, so it cannot expose the interval after that helper comparison. This is an exact-source independent-lock/order witness, not a claimed executed Rust race.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-2j7e5c/static_attack.py (full source embedded below)",
          "command": "python3 .temp/TASK-261007-2j7e5c/static_attack.py publication",
          "expected_failure": "Observed exit 1, expected-red: publication-01.log verifies pinned bytes, owned snapshot copies, an independent receipt mutex/SeqCst bump, and a separate Session write without shared transition exclusion. No fixture assertion failed and no Rust behavior was executed. Add receipt_armed_between_final_compare_and_publication_blocks_automatic_start: real handle StartIfIdle, multi-thread/OS-thread receipt Arm placed after the final comparison but before the publication write, require GoalBackgroundWait and no published turn/reservation/effects. Retain the existing before-comparison and post-publication controls. Serialize comparison plus publication with every E1 revision transition (or use one genuinely atomic admission/transition protocol), rather than adding another late read. Narrowing mutant: remove that shared exclusion while retaining the final equality comparison; the new test must fail. This requested test/mutant was not run here.",
          "candidate_tree": "c7180fab47012a651662cd207a48caafdf7b10db",
          "pinned_blobs": [
            "git-blob:42eb6f6d767465e4d80a82102a3625173f722261",
            "git-blob:0423c6fbc105a1b61223e10422d92b7ae174a166",
            "git-blob:be9f60e63f1b4e36006fb3424ee09a2429f5325e",
            "git-blob:f6faa89fb35efcff197e744fac78aee1a5bf4d6d",
            "git-blob:c1e893c8f3968d07fdcb9a2bc7c8ccffe88d07bc"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "CR-TASK-260929-2snjbb-3 / revision-recheck-before-await-window"
    }
  ],
  "notes": [
    {
      "id": "prior-finding-disposition",
      "text": "All five previous merged entries were checked: the two revision-recheck-before-await-window entries remain the one finding above (callee-await interval closed, independent-thread compare/publication interval remains); the two scheduled-checkin-regression-not-exercised entries are fixed by the real core suite fixture plus the runtime-only mutant; rejected-goal-start-commits-settings is fixed for persistent deltas by clearing the gated goal delta and the settings/notification-equality test. Existing hosted effect-free test is acknowledged, not rerun."
    },
    {
      "id": "execution-bound",
      "text": "No cargo, just, build, Rust test, new hosted run or mutant execution. Reused attached TASK-260929-2snjbb_hosted-precheck-6.md, bound to exact replay tree and snapshot 6abf59d5. It reports four job conclusions success and fifteen killed mutants with named tests; it does not provide underlying numeric command exit codes, which remain unknown. Producer results/coverage are cross-checked against candidate sources. Truncated CR validation is not counted as proof of unseen commands; precheck 5 is explicitly excluded because its base was red."
    },
    {
      "id": "coverage-ratios",
      "text": "Surface sweep 3/3: 2 held, 1 broken, 0 not-attacked. Attached hosted evidence 4/4 base lanes success, 15/15 mutants killed, 0 survivors. Prior findings: 5/5 entries inspected, 3/3 unique classes inspected; 2 classes fixed, 1 remains. Of the extra interval between final comparison and publication identified here, 0/1 executed Rust regressions cover it; hosted move_final_check_before_awaits tests the earlier prefix, not shared cross-thread exclusion."
    },
    {
      "id": "production-test-observation-retention",
      "text": "Nonblocking fix-induced note: ext/goal/src/runtime.rs:74,135,170-176,736-737 allocates a test_marked_continuations Mutex<Vec<String>> in every production runtime and appends on every successful goal continuation, even when background waiting is disabled. No cap, draining or reset reference exists; the source audit observes uncapped retention, not a measured memory failure/OOM. Prefer opt-in test observation or bounded accounting evidence instead of always-on historical test storage."
    },
    {
      "id": "activation-and-contention-bounds",
      "text": "Background wait remains intentionally default-disabled until stage 2e. note_release has no production caller in this preparatory candidate; full release/completion activation is not inferred from helper tests. A timer claim is consumed before a failed snapshot read; automatic retry after that contention remains unexecuted and nonblocking, as noted in rev3. The independent store/mailbox snapshot coherence bound is retained separately; no new claim of a reproduced incoherent snapshot."
    },
    {
      "id": "context-api-size",
      "text": "No new model-visible fragment or history rewrite established: goal context contributor returns Vec::new; API/config/CLI/rollout schemas are unchanged by the rev3-to-rev4 delta. Existing GoalBackgroundWait protocol reason has an exhaustive app-server arm. Actual rev3-to-rev4 delta: 16 paths, +813/-238 (includes removal of 182 lines of simulated scheduler test); CR base replay includes E1: 36 paths, +4693/-54. For the next correction keep the smallest coherent slice: shared admission/receipt-transition synchronization, its multi-thread public-entry regression and narrowing mutant. Do not add a serial research prerequisite."
    },
    {
      "id": "inspection-recovery",
      "text": "Initial get query using unsupported resources field exited 1; recovered by compact get description/scope/ac/notes and task-scoped resource gets. cat through the lazy skill path to reviewer role exited 1; installed /Users/iv/.agents/skills/project-management/.roles/reviewer/role.md read successfully. resource list printed usage (exit 0), so it was not evidence of an empty resource set; scoped resource paths recovered discovery. A skill-inventory rg had absent directories (head pipeline status 0); it was not a gate. Initial archive extraction was an unchecked pipeline; it was repeated with pipefail, exit 0, and every audited file was byte-compared to git show TREE:path."
    }
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Hosted exact-tree precheck 6 (base 37569076583), public handle StartIfIdle fairness tests and overgate_non_goal_triggers run 37569198182; read-error mutant 37569275012 and Armed-only mutant 37569152218 killed. Static scope audit exit 0 confirms Automatic+goal-only predicate, disabled/inactive bypass and fail-closed errors. Held for these named attacks, not proof of absence."
    },
    {
      "row": "check-in tickets and warning",
      "result": "held",
      "evidence": "Real production suite scheduled_checkins_fire_through_production_runtime_under_paused_time constructs live session, enables policy, Arms a real receipt, advances paused clock, observes three Core turns marked automatic and exact one warning. Hosted runtime-only break_runtime_wait_arm_reentry run 37569106946 is killed by that test. Static scheduler audit exit 0 confirms installation/Wait-arm/claim/re-entry/accounting, and deletion of the local simulated adapter. Hosted ticket/cap/epoch/warning/ownership/generation kills acknowledged."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "broken",
      "findings": [
        "revision-recheck-before-await-window"
      ],
      "evidence": "Pinned independent-lock/publication audit exit 1 expected-red proves a permitted source interleaving after final revision equality and before publication. Existing hosted 37569183037 covers Arm before the comparison, and 37569092438 covers rejected persistent-settings effects; invalidation mutant 37569213125 and revision mutant 37569260011 kills are acknowledged. They do not exercise the identified OS-thread interval."
    }
  ],
  "free_hunt": [
    {
      "budget_minutes": 5,
      "method": "Bounded static fix-induced/call-site hunt after all three rows were recorded in row-journal.txt; no builds",
      "scope": [
        "comparison/transition lock ownership",
        "rejected-settings effect ordering",
        "real scheduler composition and permit/timer ownership",
        "new production test-observation storage",
        "release/resume/disable callers",
        "context/API/change-size surfaces"
      ],
      "additional_blocking_findings": [],
      "result": "No extra blocking mechanism beyond the repeated publication race. Unbounded test-observation retention, contention recovery, snapshot coherence and preparatory activation limits recorded as nonblocking notes; no live memory/race experiment claimed."
    }
  ]
}
```

## Reproducible pinned-source audit

Re-extract the candidate paths with the pipefail archive command above, then save this exact source as `.temp/TASK-261007-2j7e5c/static_attack.py`. It verifies candidate bytes against the tree before checking structure. It is a static witness, not a substitute Rust runtime fixture.

```python
from pathlib import Path
import hashlib
import subprocess
import sys

TREE = 'c7180fab47012a651662cd207a48caafdf7b10db'
ROOT = Path('.temp/TASK-261007-2j7e5c-cand')

def read(path):
    data = (ROOT / path).read_bytes()
    pinned = subprocess.run(['git', 'show', f'{TREE}:{path}'], capture_output=True, check=True).stdout
    assert data == pinned, f'fixture differs from pinned candidate: {path}'
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    print(f'PIN {path} git-blob:{digest}')
    return data.decode()

def section(source, first, next_marker):
    start = source.index(first)
    return source[start:source.index(next_marker, start + len(first))]

mode = sys.argv[1]
g = read('codex-rs/core/src/session/goal_admission.rs')
w = read('codex-rs/ext/goal/src/background_wait.rs')
r = read('codex-rs/ext/goal/src/runtime.rs')
if mode == 'scope':
    assert 'kind != TurnStartKind::Automatic || turn_trigger != Some("goal")' in g
    assert 'enabled: false,' in w
    assert 'if !state.enabled || status == GoalWaitStatus::InactiveOrBudgetLimited' in w
    assert 'Err(error) => {\n                return BackgroundWaitEvaluation::WaitOnReadFailure { error };' in w
    assert 'Err(_) => return GoalAdmissionDecision::Wait' in w
    assert 'if goal.status != codex_state::ThreadGoalStatus::Active' in r
    print('PASS static predicate/error audit; public-entry attacks reused from hosted precheck 6, not executed here')
elif mode == 'scheduler':
    s = read('codex-rs/core/tests/suite/goal_background_wait.rs')
    t = read('codex-rs/ext/goal/tests/background_wait.rs')
    assert 'spawn_check_in_reentry' not in t
    for token in ['install_with_backend_and_clock', 'runtime.background_wait_state().enable()',
                  'test_arm_exec_receipt_for_background_wait', 'tokio::time::advance',
                  'test_marked_goal_continuations', 'vec![CHECK_INS_STOPPED_WARNING.to_string()]',
                  'assert_eq!(mock.requests().len(), 3)']:
        assert token in s, token
    timer = section(r, 'fn spawn_check_in_timer', 'pub(crate) async fn continue_if_idle')
    assert 'state.claim_due_deadline' in timer and 'runtime.continue_if_idle().await' in timer
    assert 'self.spawn_check_in_timer(deadline, armed_generation)' in r
    assert '.start_turn_if_idle(' in r and '.mark_goal_continuation(turn_id.clone())' in r
    print('PASS real production scheduler composition present; hosted runtime-only mutant kill reused')
elif mode == 'publication':
    p = read('codex-rs/core/src/session/pending_work.rs')
    c = read('codex-rs/core/src/unified_exec/completion_receipt.rs')
    q = read('codex-rs/core/src/session/input_queue.rs')
    task = read('codex-rs/core/src/tasks/mod.rs')
    publish = g[g.index('pub(crate) async fn publish_goal_turn_if_revision_matches'):]
    snapshot = section(p, 'pub(crate) fn try_read_snapshot', '/// Builds a snapshot')
    lists = section(c, 'pub(crate) fn try_list_pending', '/// Reserves capacity')
    arm = section(c, 'pub(crate) fn resolve_initial_response', '/// Publishes a fully finalized exit')
    assert 'let mut state = self.state.lock().await' in publish
    assert publish.index('recheck_goal_admission_before_start') < publish.index('state.last_started_turn_id =')
    assert 'receipt_store' not in publish and 'MutexGuard' not in snapshot
    assert 'Result<PendingReceiptLists, ReceiptError>' in lists and 'Ok(lists)' in lists
    assert 'let mut state = self.lock_state()?' in arm and 'self.bump_revision();' in arm
    assert 'active_turn' not in arm and 'session' not in arm
    assert 'self.revision.fetch_add(1, Ordering::SeqCst)' in c
    assert 'self.pending_work_revision.load(Ordering::SeqCst)' in q
    assert '.publish_goal_turn_if_revision_matches(' in task
    print('EXPECTED RED static lock/order witness, NOT an executed Rust race:')
    print('A holds Session active/state; final snapshot owns copied lists, releases receipt/mailbox guards, loads revision R.')
    print('After equality returns but before last_started_turn_id write, B can lock receipt store, Arm reserved receipt and bump R+1; B needs neither A lock.')
    print('A then writes last_started_turn_id with no further comparison. SeqCst orders atomics but does not atomically couple that load to the separate state write.')
    print('No await prevents cooperative Tokio yielding; it does not prevent OS preemption/concurrent worker execution. Hosted pre-check latch is before this comparison.')
    sys.exit(1)
elif mode == 'free-hunt':
    assert 'test_marked_continuations: std::sync::Mutex<Vec<String>>' in r
    assert 'test_marked_continuations: std::sync::Mutex::new(Vec::new())' in r
    assert 'marked.push(turn_id)' in r
    assert len([line for line in r.splitlines() if 'test_marked_continuations' in line]) == 4
    print('NOTE source-proven retention: unconditional production continuation success appends to an uncapped test-observation Vec; no removal/reset reference in runtime.rs. No memory/OOM execution claimed.')
else:
    raise SystemExit(f'unknown mode {mode}')
```

## Captured audit outputs

`scope-01.log`

```text
PIN codex-rs/core/src/session/goal_admission.rs git-blob:42eb6f6d767465e4d80a82102a3625173f722261
PIN codex-rs/ext/goal/src/background_wait.rs git-blob:8647c6005bf6131884dc395aa59914d1be4a2182
PIN codex-rs/ext/goal/src/runtime.rs git-blob:ba8e5bff095a15da01bbb502c1d6325f40f943db
PASS static predicate/error audit; public-entry attacks reused from hosted precheck 6, not executed here
```

`scheduler-01.log`

```text
PIN codex-rs/core/src/session/goal_admission.rs git-blob:42eb6f6d767465e4d80a82102a3625173f722261
PIN codex-rs/ext/goal/src/background_wait.rs git-blob:8647c6005bf6131884dc395aa59914d1be4a2182
PIN codex-rs/ext/goal/src/runtime.rs git-blob:ba8e5bff095a15da01bbb502c1d6325f40f943db
PIN codex-rs/core/tests/suite/goal_background_wait.rs git-blob:325d3622e196d6084b181b37e0693b350469d4ca
PIN codex-rs/ext/goal/tests/background_wait.rs git-blob:50f05eb92a6394a3d3c5101cb711de20801436a2
PASS real production scheduler composition present; hosted runtime-only mutant kill reused
```

`publication-01.log`

```text
PIN codex-rs/core/src/session/goal_admission.rs git-blob:42eb6f6d767465e4d80a82102a3625173f722261
PIN codex-rs/ext/goal/src/background_wait.rs git-blob:8647c6005bf6131884dc395aa59914d1be4a2182
PIN codex-rs/ext/goal/src/runtime.rs git-blob:ba8e5bff095a15da01bbb502c1d6325f40f943db
PIN codex-rs/core/src/session/pending_work.rs git-blob:0423c6fbc105a1b61223e10422d92b7ae174a166
PIN codex-rs/core/src/unified_exec/completion_receipt.rs git-blob:be9f60e63f1b4e36006fb3424ee09a2429f5325e
PIN codex-rs/core/src/session/input_queue.rs git-blob:f6faa89fb35efcff197e744fac78aee1a5bf4d6d
PIN codex-rs/core/src/tasks/mod.rs git-blob:c1e893c8f3968d07fdcb9a2bc7c8ccffe88d07bc
EXPECTED RED static lock/order witness, NOT an executed Rust race:
A holds Session active/state; final snapshot owns copied lists, releases receipt/mailbox guards, loads revision R.
After equality returns but before last_started_turn_id write, B can lock receipt store, Arm reserved receipt and bump R+1; B needs neither A lock.
A then writes last_started_turn_id with no further comparison. SeqCst orders atomics but does not atomically couple that load to the separate state write.
No await prevents cooperative Tokio yielding; it does not prevent OS preemption/concurrent worker execution. Hosted pre-check latch is before this comparison.
```

`free-hunt-01.log`

```text
PIN codex-rs/core/src/session/goal_admission.rs git-blob:42eb6f6d767465e4d80a82102a3625173f722261
PIN codex-rs/ext/goal/src/background_wait.rs git-blob:8647c6005bf6131884dc395aa59914d1be4a2182
PIN codex-rs/ext/goal/src/runtime.rs git-blob:ba8e5bff095a15da01bbb502c1d6325f40f943db
NOTE source-proven retention: unconditional production continuation success appends to an uncapped test-observation Vec; no removal/reset reference in runtime.rs. No memory/OOM execution claimed.
```

## Task-scoped logbook entry

Rev4 source witness repeats the revision-check/publication race through independent OS-thread transitions despite moving the comparison inside start_task. The rework brief's no-await criterion is insufficient without common transition exclusion. This outcome records the finding, addressed classes and evidence bounds; no reviewed-task or control-root logbook write was made. Route the smallest same-leaf synchronization fix with a deterministic multi-thread regression and narrowing mutant.

Artifact validation: `python3 .temp/TASK-261007-2j7e5c/validate_verdict.py` exited **0**. Checked exactly one parseable verdict-findings JSON block, required finding/reproduction fields, all 3/3 surface rows exactly once, the one-word verdict, pinned replay tree and embedded audit evidence. No code/test gate was marked passing on this format check.
