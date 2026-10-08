# Panel B — goal background wait policy, CR revision 1

changes_requested

Review of CR-TASK-260929-2snjbb-1, non-recording panel. The source task was read only; no notes, status, accept/reject, or handoff writes were made there.

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus the attached revision-1 patch produces `ffa1c230e68efdb2a7de81099ce670927c825c02`, exactly the expected candidate tree. Only a temporary index was used; the real index/branch were not changed. All candidate code inspection is bound to this tree, not the Story checkout HEAD.

Research contract: decision is whether this exact CR meets its three surfaces and ten ACs; frozen precondition is its base/patch/tree tuple, not a new grammar; maximum review budget 30 minutes plus a 5-minute free hunt; artifact budget one text outcome, no archives; no serial prerequisite; exit is one verdict with every row represented. Consumer is the orchestrator's merged R141 verdict and the next E2 implementation revision. This outcome also carries the task-scoped logbook observations: the missing deadline consumer and lifecycle epoch reset, and limits of the producer's claimed 10/10 coverage.

Commands and exit codes (this panel):

| Command | Exit | Result |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261007-2dp0i6, status=analysis)'` | 0 | Own task only |
| `git --version`, `rg --version`, `task-board --help`, `python3 --version` | 0 | Tool readiness; scratch logs under `.temp/TASK-261007-2dp0i6/` |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2dp0i6-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Temporary index initialized |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev1.patch --output .temp/TASK-260929-2snjbb_change-request_rev1.patch` | 0 | Patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2dp0i6-replay.idx" git apply --cached .temp/TASK-260929-2snjbb_change-request_rev1.patch` | 0 | Patch replayed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2dp0i6-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b ffa1c230e68efdb2a7de81099ce670927c825c02` | 0 | Whitespace check only |
| `git grep -n 'next_check_in\|CHECK_IN_DELAYS\|note_release' ffa1c230e68efdb2a7de81099ce670927c825c02 -- codex-rs` | 0 | Deadline consumers and release callers enumerated |
| `git grep -n 'tokio::time\|sleep_until\|next_check_in\|CHECK_IN_DELAYS' ffa1c230e68efdb2a7de81099ce670927c825c02 -- codex-rs/ext/goal/src` | 0 | No goal timer registration; returned deadline only logged |
| `python3` inline exact-candidate source-witness inspection | 0 | Confirmed reset/return code shapes, not production execution; transcript below |
| `git status --short`, candidate `git show`/`git diff`/`git grep`, scoped successful board reads/resource get | 0 | Read-only inspection; working tree clean |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives |

Failed discovery commands were not validation: projections containing `resources` and `attachments`, and positional `schema(get)`, each exited 1; corrected to scoped `description scope ac`, `notes`, and `schema(operation="get")`. The attempted `resource list` returned help (0), not a resource inventory; inventory was subsequently read from the existing resource directory. One skill path was absent; its canonical installed reviewer body was found and read. None of these failures was treated as absent evidence or a green gate.

Static witness output (exit 0):

> Exact candidate source witnesses confirmed. This is static inspection, not Rust execution. Wait arm consumes next_check_in only in destructuring and debug logging; returns with no scheduled wake. Turn-start hook clears wait_started_at but preserves check_ins_used. Source trace: first check-in at t=30 consumes count 1; turn-start clears epoch; next idle at t=30 sets epoch 30; next deadline = 30+60 = 90, not 60. Next immediate check-in yields t=90+120=210, not 120.

The witness script read extracted candidate blobs, checked the exact `note_turn_start` assignment, production lifecycle call, deadline addition, and Wait branch's two deadline references (binding plus log) and return. It is an aid to static review, not a model offered as an execution test. The reported 30/90/210 trace is conditional on externally invoked reevaluations and immediate check-in turns; absent external callbacks the discarded-deadline defect prevents even that trace.

Execution evidence accepted from the source task, not rerun: `TASK-260929-2snjbb_hosted-precheck-2.md`, `TASK-260929-2snjbb_coverage-map.md`, `TASK-260929-2snjbb_results.md`, and the task notes bind snapshot `3ea2ac72`/run `37530053147` to the exact candidate tree. The four hosted lanes are recorded success; seven narrowing mutants are recorded killed, zero survivors. Hosted raw process exit codes are not supplied in the compact precheck, so no numeric hosted exit code is invented. Precheck-1 results are explicitly void. The review accepts the brief's authorization to reuse these hosted public-entry attacks. This is no attestation that every runtime behavior was exercised.

Artifact validation: standalone Python JSON/structure check exited 0: exactly one `verdict-findings` block, unique 3/3 row results, and every required finding/reproduction field present.

Coverage: 3/3 surface rows have exactly one disposition (held, broken, held). Rows 1 and 3 each have an accepted hosted core-entry attack; row 2 has static counterexamples and only helper-level hosted execution for its timer behavior. The producer's 10/10 named-AC map is not 10/10 composed-runtime coverage. New tests and narrowing mutants requested below were NOT executed and have unknown exits.

References: `surface-table.md`, source-task AC projection, `producer-brief.md`, `final-plan.md` sections 6 and staging (2d scheduler foundation; 2e paired activation), and the three evidence resources above, all read from source-task resources. Code references resolve against `ffa1c230e68efdb2a7de81099ce670927c825c02:<path>`. No external factual claims or source-task mutations are needed.

```verdict-findings
{
  "findings": [
    {
      "id": "checkin-epoch-reset-on-turn-start",
      "row": "check-in tickets and warning",
      "invariant": "AC4: check-ins at absolute 30, 60 and 120 minutes from the wait start; turn start invalidates tickets without renewing that human-input epoch.",
      "mechanism": "codex-rs/ext/goal/src/background_wait.rs:372 clears wait_started_at on every note_turn_start while retaining check_ins_used. The production hook at ext/goal/src/extension.rs:246 invokes it for the admitted check-in. evaluate_continuation at background_wait.rs:273-278 then adds the next absolute offset to a newly created epoch. With persistent pending work and effectively immediate check-in turns, the returned deadlines become 30/90/210 minutes rather than 30/60/120. The existing firing test never calls note_turn_start between check-ins.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/background_wait.rs (requested new test check_ins_keep_epoch_across_admitted_turns)",
          "command": "just test -p codex-goal-extension --test background_wait check_ins_keep_epoch_across_admitted_turns",
          "expected_failure": "NOT RUN: test does not yet exist and builds are forbidden. Start pending at minute 0; evaluate/admit at 30; invoke the real turn-start hook or note_turn_start, then evaluate pending again at 30 and 60. Assert next_check_in is minute 60 and second ticket is due at 60. Candidate returns deadline 90 and Wait at 60. Add narrowing mutant that resets the epoch only on goal-triggered turn start. Static source witness inspection ran, exit 0; this is not an executed Rust reproduction."
        }
      ],
      "severity": "bypass",
      "repeat-of": "none"
    },
    {
      "id": "checkin-deadline-discarded",
      "row": "check-in tickets and warning",
      "invariant": "AC4-AC5: fallback check-ins actually fire and the warning follows the third check-in without requiring another human message or work event.",
      "mechanism": "codex-rs/ext/goal/src/runtime.rs:608-623 destructures next_check_in, logs it, drops the goal permit and returns. It registers no timer or wake. The candidate-wide reference sweep finds no production consumer of this deadline other than that log. GoalExtension::on_thread_idle at extension.rs:191-203 invokes continuation once; there is no goal-owned scheduled re-entry. A stalled Armed subscription with no subsequent events therefore never reaches the first fallback check-in or warning. Disabled-by-default activation is intentional; the missing scheduler foundation is separate from enabling it.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/background_wait.rs (requested runtime test stalled_subscription_fires_scheduled_checkins)",
          "command": "just test -p codex-goal-extension --test background_wait stalled_subscription_fires_scheduled_checkins",
          "expected_failure": "NOT RUN: test does not yet exist and builds are forbidden. Enable the preparatory policy through a runtime fixture; use the real idle contributor with a persistent Armed receipt and a paused clock, no more idle callbacks/messages/exits. Advance to 30/60/120 minutes and assert one real admitted check-in each, then exactly one warning while the goal stays active. Candidate schedules no callback and produces zero check-ins. A narrowing mutant scheduling only the first deadline must fail the later checks. Static candidate-wide caller inspection and Wait-arm witness ran, exit 0; no runtime test is claimed."
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    }
  ],
  "notes": [
    {
      "id": "execution-bound",
      "text": "This panel performed replay and static attacks only, as explicitly required. No cargo, just, build, Rust test, or new mutant was executed. New reproduction names are requested tests, not passing or failing executed tests. Existing hosted evidence is reused only for its named attacks."
    },
    {
      "id": "snapshot-coherence-followup",
      "text": "Static free-hunt concern, not a reproduced blocking finding: core/src/session/pending_work.rs:51-64 copies the receipt lists and mailbox under separate locks, then samples the revision last. A receipt can become Armed after the list copy but before revision load, making old contents carry a newer revision. Also the admission recheck precedes async preparation and start_task. Request a barrier-based production test with a transition inside the snapshot read and another after the checker but before start_task. The existing goal_background_wait_revision_recheck_catches_transition performs sequential reserve/arm then handle, with an inline test-double checker; it is not a latch test of the real goal checker."
    },
    {
      "id": "release-and-late-wake-bound",
      "text": "Candidate-wide note_release references are its definition and helper tests. Real subscription activation/control wiring belongs to stage 2e, so missing external activation alone is not a finding here. AC6/AC8 helpers prove empty-state reassessment, not a scheduled late completion/release wake. Preserve these limits in the coverage claim and add the real vertical tests in activation."
    },
    {
      "id": "size-and-context",
      "text": "Combined base-to-candidate diff is 3041 insertions and 39 deletions across 26 files, including the already-checkpointed E1 work; producer describes only the E2 delta. No new model-visible fragment is injected (TurnInputContributor returns an empty vector). The new NotSubmittedReason is not serialized; inspected app-server match is exhaustive. No breaking wire/config/rollout change was established."
    }
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Reused hosted exact-tree run 37530053147 and narrowing-mutant run 37530108526: goal_background_wait_blocks_goal_but_admits_user_and_followup and goal_background_wait_ignores_non_goal_triggers exercise core handle/start_if_idle. The overgate_non_goal_triggers mutant is reported killed. Scope filter at goal_admission.rs:30 bypasses non-Automatic/non-goal callers. Held is limited to these named attacks, not every AC1-AC3 shape. Error and inactive helper results are supplementary."
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "checkin-epoch-reset-on-turn-start",
        "checkin-deadline-discarded"
      ],
      "evidence": "Static source counterexamples against the replayed candidate. Hosted helper tests and killed reuse_ticket_id/warning_repeats mutants do not drive timer scheduling or the admitted-turn lifecycle. Source-witness command exit 0 confirms both code shapes; requested Rust regressions were not run."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "held",
      "evidence": "Reused hosted exact-tree run 37530053147: goal_background_wait_revision_recheck_catches_transition and goal_background_wait_allows_when_empty_and_after_release enter core handle/start_if_idle with real receipt transitions and the test-double admission checker. Hosted 37530189584 and 37530135461 kill skip_revision_recheck and preserve_ticket_across_invalidation in helper tests. Static Wait and read-failure paths explicitly drop the goal semaphore. Held is limited to the named sequential transition/release attacks; no claim of a latch attack or composed runtime-ticket proof."
    }
  ],
  "free_hunt": {
    "budget_minutes": 5,
    "scope": "Snapshot coherence, post-check admission window, external API/context exposure, release callers, combined diff size. Static only; no new build or execution.",
    "blocking_findings": [],
    "notes": [
      "snapshot-coherence-followup",
      "release-and-late-wake-bound",
      "size-and-context"
    ]
  }
}
```
