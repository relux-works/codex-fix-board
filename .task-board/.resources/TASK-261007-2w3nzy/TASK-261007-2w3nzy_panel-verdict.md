# R141 panel A — goal-background-wait-policy rev1

changes_requested

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` + CR patch through temporary index produced exactly `ffa1c230e68efdb2a7de81099ce670927c825c02` (expected candidate tree). Read-only review; no builds, cargo, just, commits, branch changes, or writes on TASK-260929-2snjbb.

## Command evidence

Commands actually run by this panel (standalone replay and probe processes):

| Command | Exit | Result |
| --- | ---: | --- |
| `task-board m set_status` on panel task | 0 | analysis |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev1.patch --output .temp/TASK-260929-2snjbb_change-request_rev1.patch` | 0 | patch read |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2w3nzy-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | base index loaded |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2w3nzy-replay.idx" git apply --cached .temp/TASK-260929-2snjbb_change-request_rev1.patch` | 0 | replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2w3nzy-replay.idx" git write-tree` | 0 | exact expected tree |
| `python3 .temp/TASK-261007-2w3nzy/static_attack.py deadline` | 1 | expected-red source trace; deadline origin reset |
| `python3 .temp/TASK-261007-2w3nzy/static_attack.py timer` | 1 | expected-red source wiring check; deadline discarded |
| `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b ffa1c230e68efdb2a7de81099ce670927c825c02` | 0 | whitespace check only |

Read-only retrieval of surface-table, producer-brief, results, coverage-map, hosted-precheck-2, mutants and final-plan: each `task-board resource get` exit 0. Candidate `git show` reads and production caller `git grep`: exit 0. Board scoped AC/resource/checklist reads: exit 0 after correcting invalid `resources` projection (initial query errors were nonzero; combined command exit 1). Initial skill inventory reported two absent directories; no workflow depended on them. Reviewer role reference at curator path was missing (cat exit 1), then successfully read from installed `.agents/skills` (exit 0). Python/git/rg/task-board readiness succeeded; no Rust tool used.

Hosted evidence was accepted from attached `TASK-260929-2snjbb_hosted-precheck-2.md`, not rerun or independently queried on GitHub. It pins this exact tree to snapshot 3ea2ac72 and base run 37530053147; small/lint/app-server/core report success. Seven mutant runs report expected failures, 7 killed / 7, 0 survivors. Numeric process exit codes are not provided by that hosted summary; do not infer them from lane conclusions. Precheck 1 is void. Local CR validation is bounded/truncated and is not relied on for absent tail commands.

## Recommendation and logbook entry

Request localized E2 rework: preserve the wait-episode origin across check-in turn starts and provide the cancellable timer foundation demanded by plan stage 2d. Add composed fake-time tests that run turn-start hooks between admissions and drive actual timer callbacks without human/mail stimuli. Suggested tests: `check_in_turn_start_preserves_absolute_deadlines`, `pending_work_timer_wakes_idle_goal`; run through the repository's `just test -p codex-goal-extension` lane on hosted exact-tree evidence. No Rust behavioral reproduction of these new cases was run by this panel. Source probes below confirm concrete wiring, not runtime execution or a generic source-text gate.

Logbook: hosted timing tests pass while production turn-start resets their time origin; their direct policy calls omit that composition. The runtime returns a deadline to debug logging only. Leave activation off pending the intended paired stage 2e; lack of enable callers is intentional, not itself a defect. Post-admission races and release wiring need named production tests in owning rework/activation, not another research chain. All producer-task accesses were reads.

Sources: all code citations refer to the exact candidate tree above; plan §6 and stage 2d table (lines 165–177, 258), surface-table.md, results AC map, hosted-precheck-2.md and coverage-map.md were retrieved from producer resources. The configured review is a static panel with externally attached execution evidence.

```verdict-findings
{
  "findings": [
    {
      "id": "turn-start-resets-check-in-origin",
      "row": "check-in tickets and warning",
      "invariant": "AC4: check-ins at absolute 30, 60, 120 minutes from wait start, reassessed after each check-in.",
      "mechanism": "codex-rs/ext/goal/src/background_wait.rs:374-378 clears wait_started_at on every turn start; codex-rs/ext/goal/src/extension.rs:246 invokes it in production. evaluate_continuation:273-279 then inserts the new now and adds CHECK_IN_DELAYS[check_ins_used]. After first check-in at 30m, next idle at 31m gives deadline 91m instead of 60m. The hosted timing test omits note_turn_start between admissions.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-2w3nzy/static_attack.py (full source below)",
          "command": "python3 .temp/TASK-261007-2w3nzy/static_attack.py deadline",
          "expected_failure": "exit 1: absolute-deadline invariant violated by production turn-start hook; pinned-source trace, not Rust behavioral execution."
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    },
    {
      "id": "check-in-deadline-discarded",
      "row": "check-in tickets and warning",
      "invariant": "AC4 fallback check-ins actually fire; plan stage 2d includes scheduler foundation.",
      "mechanism": "codex-rs/ext/goal/src/runtime.rs:608-624 destructures next_check_in, logs it, drops the permit and returns. No registration, timer, or future continuation is scheduled from the deadline. With enabled policy and an unchanged Armed receipt, passage of time alone has no callback to reevaluate. The timing tests supply now and call evaluate_continuation manually. Activation remains intentionally deferred to stage 2e; that does not supply the missing stage-2d scheduler foundation.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-2w3nzy/static_attack.py (full source below)",
          "command": "python3 .temp/TASK-261007-2w3nzy/static_attack.py timer",
          "expected_failure": "exit 1: deadline is destructured, logged and discarded; no timer is armed. Static wiring reproduction only, not a live fake-clock test."
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    }
  ],
  "notes": [
    {
      "id": "post-recheck-race-unexecuted",
      "text": "core/src/session/turn_input.rs:459 checks once, before awaited settings preparation and start_task. Receipt transitions use their own store lock/revision. Existing latch-named test arms before handle(), not after the last check. A post-recheck transition looks unprotected; runtime reproduction unknown. Request a latch after check_goal_admission, arm a receipt, resume settings and assert no Started. Not promoted to a finding without execution."
    },
    {
      "id": "release-hook-not-wired",
      "text": "git grep over exact candidate found note_release only as a definition and direct goal test calls; no production caller. Stage 2e adds release controls, so track this wiring there; no claim that release invalidation has already run through production."
    },
    {
      "id": "coverage-bound",
      "text": "Hosted base and mutant evidence reused, not rerun. 3/3 rows have named executed attacks, 7/7 reported mutants killed. These ratios do not establish all production lifecycle compositions. 10/10 AC rows have named tests in the producer map; AC4 composition is contradicted by the static trace."
    },
    {
      "id": "scope-size",
      "text": "Replay patch spans 26 files including prerequisite E1 snapshot code; producer E2 map reports 721 logic lines plus tests. Smallest rework is timer foundation and turn-start deadline preservation with composed tests; do not create a separate generalized research prerequisite."
    }
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Exact-tree precheck 2 base run 37530053147; core public handle/start_if_idle tests goal_background_wait_blocks_goal_but_admits_user_and_followup and goal_background_wait_ignores_non_goal_triggers. Mutant overgate_non_goal_triggers run 37530108526 fails both; Armed run 37530082819 and read-error run 37530215463 also killed. Held only for these attacks."
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "turn-start-resets-check-in-origin",
        "check-in-deadline-discarded"
      ],
      "evidence": "Pinned-source probes both expected red exit 1. Hosted ticket/warning mutants 37530162208 and 37530240516 killed; manual state evaluations omit production turn start / timer callback."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "held",
      "evidence": "Exact-tree base core tests revision_recheck_catches_transition and allows_when_empty_and_after_release; hosted skip_revision_recheck 37530189584 and preserve_ticket_across_invalidation 37530135461 killed. Bounds: post-check race and production release hook not executed, see notes."
    }
  ],
  "free_hunt": {
    "budget_minutes": 5,
    "result": "No additional reproduced blocking mechanism. Examined disable/resume, release callers, post-admission await window, wire enum addition and scope size; unresolved execution gaps remain notes."
  }
}
```

## Replayable static probes

Save the following in `.temp/TASK-261007-2w3nzy/static_attack.py` and run the two commands above. This reads pinned Git blobs, does not compile or execute Rust.

```python
import re
import subprocess
import sys
TREE = 'ffa1c230e68efdb2a7de81099ce670927c825c02'
def blob(path):
    return subprocess.check_output(['git', 'show', TREE + ':' + path], text=True)
policy = blob('codex-rs/ext/goal/src/background_wait.rs')
runtime = blob('codex-rs/ext/goal/src/runtime.rs')
extension = blob('codex-rs/ext/goal/src/extension.rs')
if sys.argv[1] == 'deadline':
    hook = policy.split('pub fn note_turn_start(&self)', 1)[1].split('\n    }', 1)[0]
    assert 'background_wait_state().note_turn_start()' in extension
    assert 'wait_started_at.get_or_insert(now)' in policy
    assert 'CHECK_IN_DELAYS' in policy and 'Duration::from_secs(60 * 60)' in policy
    print('Pinned production on_turn_start resets the origin used for the next absolute deadline.', flush=True)
    print('Trace: wait begins t=0; first admission t=30; turn-start clears origin; idle reassessment t=31 inserts 31; second deadline is 31+60=91, required absolute deadline is 60.', flush=True)
    assert 'state.wait_started_at = None;' not in hook, 'absolute-deadline invariant violated by production turn-start hook'
elif sys.argv[1] == 'timer':
    branch = runtime.split('BackgroundWaitEvaluation::Wait {', 1)[1].split('BackgroundWaitEvaluation::WaitOnReadFailure', 1)[0]
    print('Pinned runtime Wait branch:\nBackgroundWaitEvaluation::Wait {' + branch, flush=True)
    references = [line for line in branch.splitlines() if 'next_check_in' in line]
    print('Deadline uses: ' + repr(references), flush=True)
    assert any('next_check_in' in line and '?next_check_in' not in line and 'next_check_in,' not in line for line in branch.splitlines()), 'deadline is destructured, logged and discarded; no timer is armed'
else:
    raise ValueError(sys.argv[1])
```

## Probe outputs (real exit 1 for each)

```text
Pinned production on_turn_start resets the origin used for the next absolute deadline.
Trace: wait begins t=0; first admission t=30; turn-start clears origin; idle reassessment t=31 inserts 31; second deadline is 31+60=91, required absolute deadline is 60.
Traceback (most recent call last):
  File "/Users/iv/Developer/IV/codex/.temp/STORY-261007-hcov7u/worktree/.temp/TASK-261007-2w3nzy/static_attack.py", line 17, in <module>
    assert 'state.wait_started_at = None;' not in hook, 'absolute-deadline invariant violated by production turn-start hook'
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: absolute-deadline invariant violated by production turn-start hook
Pinned runtime Wait branch:
BackgroundWaitEvaluation::Wait {
                    next_check_in,
                    emit_warning,
                } => {
                    if emit_warning {
                        self.inner.event_emitter.background_wait_warning(
                            self.thread_id().to_string(),
                            crate::background_wait::CHECK_INS_STOPPED_WARNING.to_string(),
                        );
                    }
                    tracing::debug!(
                        ?next_check_in,
                        "goal continuation waiting for subscribed work"
                    );
                    drop(goal_state_permit);
                    return Ok(());
                }
                
Deadline uses: ['                    next_check_in,', '                        ?next_check_in,']
Traceback (most recent call last):
  File "/Users/iv/Developer/IV/codex/.temp/STORY-261007-hcov7u/worktree/.temp/TASK-261007-2w3nzy/static_attack.py", line 23, in <module>
    assert any('next_check_in' in line and '?next_check_in' not in line and 'next_check_in,' not in line for line in branch.splitlines()), 'deadline is destructured, logged and discarded; no timer is armed'
           ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: deadline is destructured, logged and discarded; no timer is armed
```

Artifact format verification: Python JSON parse and assertions returned exit 0: exactly one verdict-findings block, exactly three distinct ordered surface rows, valid finding fields/severities, one-word verdict, size below 40 KiB. Sole attached outcome carries the logbook entry and full static probe source/outputs. Prepared under the run worktree write boundary; resource add materializes the outside-worktree board artifact through authorized CLI, without direct control-root edits.
