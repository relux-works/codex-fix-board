# R141 panel A — CR-TASK-260929-2snjbb-4

changes_requested

Replay check: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` + rev4 patch produces exactly `c7180fab47012a651662cd207a48caafdf7b10db`; expected tree equals observed tree. All three replay commands exited 0.

Read-only panel: source task was never mutated. No builds or Rust tests ran here. The one blocking result below is an explicit static source-ordering witness; hosted test results are reused from the attached exact-tree precheck, not presented as local execution.

Research plan: recommend the current CR verdict for the recording reviewer; frozen candidate/base above; grammar not applicable. Bound 25 minutes review/packaging plus 5 minutes free hunt, one text outcome, no serial prerequisite. Exit is a 3/3 surface sweep and own-task researcher handoff. Consumer is the current recording-review slice; no new implementation/research scope.

| Command / inspection | Exit | Meaning |
|---|---:|---|
| `task-board m 'set_status(TASK-261007-1hgsgy, status=analysis)'` | 0 | Own task started |
| `command -v task-board`; `git --version`; `rg --version` readiness | 0 | Tools produced expected output; `.temp/TASK-261007-1hgsgy/tool-readiness-01.log` |
| Initial query with unsupported `resources` field | 1 | Read failure, corrected; no absence inferred |
| Initial combined skill read/search | 2 | Missing reviewer path / search directories, corrected |
| Scoped `get { description scope ac notes }`; `get { outcomeResources preconditionResources }`; own `get { checklist }` | 0 | Source AC/context/resource inventory and own checklist |
| `resource get` for patch, surface table, producer brief, results, coverage map, hosted-precheck-6, validation log, rev3 verdict, mutants | 0 each | Read-only materialization |
| `GIT_INDEX_FILE=... git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Temporary-index baseline |
| `GIT_INDEX_FILE=... git apply --cached .temp/TASK-260929-2snjbb_change-request_rev4.patch` | 0 | Patch replay |
| `GIT_INDEX_FILE=... git write-tree` | 0 | Exact expected candidate tree |
| `set -o pipefail; git archive <candidate> <selected paths> | tar -x -C .temp/TASK-261007-1hgsgy-cand` | 0 | Candidate source extraction only; no nested worktree |
| Scoped schema read and recovery schema read | 0 | Used only to repair unknown query field |
| Unsupported `task-board resource list` | 0 | Printed help, not counted as inventory |
| Corrected role/source/log reads (`cat`, `sed`, `rg`, `nl`, `git show`/diff/stat/rev-parse) | 0 | Pinned-source inspection; no executable Rust attack |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directive recorded |
| `python3 --version` | 0 | Python 3.14.7 readiness; local log |
| `python3 .temp/TASK-261007-1hgsgy/static_attack.py > .../admission-static-01.log` | **1** | **Expected-red static ordering witness**, not a passing gate or Rust race |
| `git diff --check` (standalone) | 0 | No tracked repository edits |


Attached execution source: `TASK-260929-2snjbb_hosted-precheck-6.md`, tree `c7180fab47012a651662cd207a48caafdf7b10db`, snapshot `6abf59d5`, base run `37569076583`. Reported 4/4 lanes success and 15/15 mutants killed, 0 survivors. Numeric hosted process exits are not supplied and are not invented. Local validation source: `TASK-260929-2snjbb_change-request_rev4-validation.log`; visible fast-lane exits are 0, with the stated transport/truncation boundary. Prior mechanism/disposition source: `TASK-260929-2snjbb_review-verdict-rev3.md`. Source citations below are at the replayed candidate tree, not live HEAD.

```verdict-findings
{
  "findings": [
    {
      "id": "revision-comparison-not-serialized-with-publication",
      "row": "admission recheck and invalidation",
      "invariant": "AC7: a receipt transition before the stated turn-publication linearization point must reject automatic goal admission; serialization or an authoritative changed-revision check must enforce the ordering.",
      "mechanism": "codex-rs/core/src/session/goal_admission.rs:131-137 holds Session.state, calls the final snapshot/revision check at :133, then writes last_started_turn_id at :137. The receipt Arm path in core/src/unified_exec/completion_receipt.rs:408,451,466 uses its own store mutex and atomic revision, never Session.state or active_turn. try_read_snapshot releases the receipt-store snapshot lock before returning and loads revision separately (core/src/session/pending_work.rs:51-64). Thus another OS thread can complete an Arm after the final comparison accepts R but before the documented publication write, and the caller still publishes true with no shared transition lock or subsequent comparison. Absence of await prevents cooperative task suspension, not concurrent OS-thread execution. This is a pinned-source legal-ordering witness, not an executed Rust race. The awaited-prefix defect from rev3 is fixed; this is the narrower nonserialized compare/write mechanism.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-1hgsgy/static_attack.py (full source embedded in this outcome)",
          "command": "python3 .temp/TASK-261007-1hgsgy/static_attack.py > .temp/TASK-261007-1hgsgy/admission-static-01.log",
          "expected_failure": "Observed exit 1, EXPECTED RED: source checks confirm distinct transition/publication locks and compare-before-write ordering; the embedded trace witnesses Arm completing in that interval. This command is a static ordering audit, not a Rust behavioral test. Requested hosted regression: receipt_armed_after_final_revision_read_before_publication_blocks_goal, using a two-OS-thread latch after the final snapshot revision read/comparison and before last_started_turn_id publication, then actual receipt-store Arm, and require GoalBackgroundWait with no published turn. Narrowing mutant: keep all early and late revision checks but release the shared transition/publication serialization before the publication write. Neither requested Rust test nor mutant was executed here.",
          "candidate_tree": "c7180fab47012a651662cd207a48caafdf7b10db",
          "pinned_blobs": [
            "git-blob:42eb6f6d767465e4d80a82102a3625173f722261",
            "git-blob:0423c6fbc105a1b61223e10422d92b7ae174a166",
            "git-blob:be9f60e63f1b4e36006fb3424ee09a2429f5325e"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Execution boundary: this panel reran temporary-index replay, source inspection, static ordering audit and artifact validation only. No cargo, just, compilation, Rust tests or new hosted mutant execution. Attached hosted-precheck-6.md is accepted as exact-tree execution evidence, not independently fetched or rerun; it reports conclusions and failed test names, not numeric process exit codes. No hosted exit codes are invented.",
    "Prior-round dispositions: the revision now carries the admitted revision into start_task and checks after the awaited prefix; receipt_armed_inside_start_task_blocks_automatic_start and move_final_check_before_awaits kill (37569183037) verify that repair. Persistent goal deltas are ignored before preparation; settings-preservation test plus apply_goal_settings_before_final_check kill (37569092438) verify the reported settings repair. The scheduler regression now uses a real installed GoalRuntimeHandle/live Core session and production timer, submission, automatic bookkeeping and warning; break_runtime_wait_arm_reentry kill (37569106946) attacks runtime wiring itself. These repairs are acknowledged; the new concurrency finding does not assert those hosted tests failed.",
    "Coverage: 3/3 surface rows swept, 2 held, 1 broken, 0 not-attacked. Attached exact-tree evidence reports 4/4 lanes success and 15/15 mutants killed, 0 survivors. None of the listed mutants/latches serializes or attacks the final synchronous compare-to-publication interval on another OS thread. Existing mutant kills are retained within their named bounds, not taken as proof of absence.",
    "Unexecuted snapshot-coherence bound: try_read_snapshot copies store and mailbox separately and loads revision last; a content view may therefore belong to an older revision. Wanted hosted attack: pending_snapshot_revision_matches_copied_contents with a real Arm between store copy and revision load. No new behavioral reproduction here; this separate concern is a note.",
    "Free-hunt storage observation: ext/goal/src/runtime.rs:74,135,170-177,736-737 adds a production Mutex<Vec<String>> and appends every admitted goal continuation without cap, drain or cfg gating, even while background waiting is disabled. Long-lived memory behavior was not executed. Prefer existing accounting observations or a bounded/test-scoped observer; wanted regression: production_goal_continuation_observation_is_bounded. This is a nonblocking note in this panel, not an alleged measured memory failure.",
    "Preparatory-stage bounds retained: note_release has no production caller yet; policy is intentionally disabled until activation. State release/reassessment and completion-after-cap tests are not proof that later external wake/control wiring is implemented. Wanted activation attacks: release_misarmed_subscription_wakes_runtime and completion_after_cap_wakes_runtime_without_human_input. No missing-default-activation finding added.",
    "Read-failure recovery bound: a fired timer consumes its registration before continue_if_idle; a subsequent contended snapshot read may return WaitOnReadFailure without scheduling another deadline. Safe no-continuation behavior is verified, recovery/liveness under this contention is unexecuted. Wanted test: scheduled_checkin_read_failure_rearms_after_contention. Nonblocking note.",
    "Context/API/scope: the contributor returns Vec::new and adds no model-visible fragment, history rewrite or prompt injection. New internal GoalBackgroundWait rejection has an app-server mapping. No new wire/config/CLI/rollout break established in bounded inspection. Full base replay is 36 files +4693/-54 and includes E1 prerequisite; rev3-to-rev4 is 16 files +813/-238. Reviewable corrective slice is actual shared admission/transition serialization plus its hosted regression, not another research chain.",
    "Inspection recoveries: unsupported resources field query exit 1; missing role reference and absent skill-search directories made the combined skill read/search command exit 2. Recovered by installed reviewer role path, resource get, and outcomeResources/preconditionResources projection. resource list is unsupported and printed help (exit 0), so it was not counted as a successful resource inventory. No failed/partial read was treated as absence.",
    "Local CR validation log: visible target guard exit 0, fmt-check exit 0, clippy exit 0 and small-crate 266/266 summary exit 0 with exact-command-shard 4/4 green. The task brief warns of the 64 KiB transport cap; unseen portions are not asserted to have run. Hosted precheck 6, not precheck 5, is authoritative.",
    "Logbook entry (task-scoped): rev4 fixes the awaited prefix but the claimed publication critical section does not include the receipt transition owner. Recorded as one bypass finding; held scope and scheduler rows preserved. No source task mutation, status, acceptance/rejection or handoff was performed. Outcome staging stays in the allowed run worktree; resource add performs the authorized managed storage write."
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Hosted precheck 6 base 37569076583: core/small/lint/app-server success on tree c7180fab47012a651662cd207a48caafdf7b10db. overgate_non_goal_triggers 37569198182 killed by core handle StartIfIdle fairness/non-goal tests; treat_read_error_as_empty 37569275012 killed by read_failure_never_treated_as_empty; gate_only_queued_ignoring_armed 37569152218 killed by the real-session scheduled suite and cap/firing tests. Static check_goal_admission restricts to Automatic + goal; other input/mail paths retain their existing checks. Held within these executed attacks, not a universal absence claim."
    },
    {
      "row": "check-in tickets and warning",
      "result": "held",
      "evidence": "Exact-tree hosted attacks: reuse_ticket_id 37569243904; warning_repeats 37569305975; reset_epoch_on_turn_start 37569228520; drop_check_in_registration 37569121979; drop_timer_spawn 37569137077; keep_handle_in_slot_while_firing 37569167785; unconditional_slot_replace 37569290755; break_runtime_wait_arm_reentry 37569106946. Named killing tests are in hosted-precheck-6.md. The actual suite goal_background_wait.rs now installs production runtime/Core, observes 3 real automatic turns at fake 30/60/120, and one production warning, and its runtime-only mutant is killed. Static timer detach and generation guards retain ownership repairs. No new scheduler failure reproduced."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "broken",
      "findings": [
        "revision-comparison-not-serialized-with-publication"
      ],
      "evidence": "Pinned-source static_attack.py expected-red exit 1 (embedded source/log) establishes nonserialized final comparison/publication ordering. Attached skip_revision_recheck 37569260011, preserve_ticket_across_invalidation 37569213125, move_final_check_before_awaits 37569183037, apply_goal_settings_before_final_check 37569092438 kills are acknowledged; they cover their earlier/lifecycle/effect windows rather than OS-thread Arm after the final revision read. Wait returns before timer delay with goal permit released; lifecycle invalidation/reset methods traced."
    }
  ],
  "free_hunt": [
    {
      "budget_minutes": 5,
      "method": "bounded static hunt after row sweep; no builds",
      "scope": [
        "snapshot coherence",
        "production observation growth",
        "read-failure timer recovery",
        "activation/release bounds",
        "context/API and delta size"
      ],
      "additional_blocking_findings": [],
      "result": "No additional reproduced blocking mechanism; observations and wanted tests retained as notes."
    }
  ]
}
```

Static reproduction source (self-contained, reads exact candidate Git blobs; no compilation):

```python
from pathlib import Path
import subprocess
import sys
TREE = 'c7180fab47012a651662cd207a48caafdf7b10db'
def source(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)
def body(text, marker):
    start = text.index('{', text.index(marker))
    depth = 1
    end = start + 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[start + 1:end - 1]
publish = body(source('codex-rs/core/src/session/goal_admission.rs'), 'pub(crate) async fn publish_goal_turn_if_revision_matches(')
arm = body(source('codex-rs/core/src/unified_exec/completion_receipt.rs'), 'pub(crate) fn resolve_initial_response(')
snapshot = body(source('codex-rs/core/src/session/pending_work.rs'), 'pub(crate) fn try_read_snapshot(')
assert publish.index('recheck_goal_admission_before_start') < publish.index('state.last_started_turn_id =')
assert 'self.state.lock().await' in publish
assert 'let mut state = self.lock_state()?' in arm
assert 'record.phase = ReceiptPhase::Armed' in arm
assert 'self.bump_revision()' in arm
assert 'active_turn' not in arm and 'session.state' not in arm
assert snapshot.index('.try_list_pending()') < snapshot.index('pending_work_revision()')
print('Pinned-source checks passed: comparison precedes publication; Arm owns independent store mutex; snapshot locks do not extend into publication.')
print('Static ordering witness (NOT an executed Rust race):')
print('A: hold active_turn + Session.state; final snapshot loads admitted revision R and comparison accepts.')
print('B: while A is preempted, resolve_initial_response(Arm) takes receipt-store mutex, publishes Armed, bumps R to R+1, and returns.')
print('A: resume; write last_started_turn_id and return true without a further shared receipt lock or revision comparison.')
print('At the specified publication-write linearization point, a completed pre-publication Arm is admitted. No .await is required for OS-thread preemption.')
print('EXPECTED RED: source-defined publication ordering invariant is not serialized with Arm. Exit 1; no Rust tests, builds, or live process race executed.')
sys.exit(1)
```

Observed `admission-static-01.log`, process exit **1** (expected red):

```text
Pinned-source checks passed: comparison precedes publication; Arm owns independent store mutex; snapshot locks do not extend into publication.
Static ordering witness (NOT an executed Rust race):
A: hold active_turn + Session.state; final snapshot loads admitted revision R and comparison accepts.
B: while A is preempted, resolve_initial_response(Arm) takes receipt-store mutex, publishes Armed, bumps R to R+1, and returns.
A: resume; write last_started_turn_id and return true without a further shared receipt lock or revision comparison.
At the specified publication-write linearization point, a completed pre-publication Arm is admitted. No .await is required for OS-thread preemption.
EXPECTED RED: source-defined publication ordering invariant is not serialized with Arm. Exit 1; no Rust tests, builds, or live process race executed.
```

Handoff conclusion: 3/3 rows reviewed; gate/fairness and ticket/warning rows held for named attacks; admission row broken by one static ordering mechanism. The requested new regression/mutant is **unrun**. Correct in the same E2 leaf using real shared ordering between receipt transitions and turn publication, then run the named regression and narrowing mutant through hosted CI. No accepted/done state or landing is claimed by this panel.

Artifact gate: `python3 .temp/TASK-261007-1hgsgy/validate_verdict.py` exited **0**. It checked one valid verdict-findings block, one verdict, all three unique surface rows, required typed finding/reproduction fields, string pinned-blob entries, exact replay tree, and no nonignored repository delta. Log: `.temp/TASK-261007-1hgsgy/verdict-validation-01.log`. Artifact authoring `python3 .../write_verdict.py` also exited 0. These are artifact/source checks, not product behavior tests.
