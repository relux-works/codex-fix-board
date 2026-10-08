# TASK-261007-3qu2ce — R141 panel A, goal-background-wait-policy rev5

accept

Read-only, non-recording review of CR-TASK-260929-2snjbb-5. This verdict is a panel recommendation for the recording reviewer. No accept/reject/withdraw/status/handoff/resource/note mutation was made on TASK-260929-2snjbb. No repository source changed, and this run did not commit, switch, rebase, merge, push or build.

## Replay and directly run commands

Base: `812b8037a8a62bac3ce80f7035c9d9142ffea75b`.
Expected and replayed candidate tree: `13972f7d936f6280c9b0cae88749c6f5c1a56a9a` — exact equality.
`IDX=$PWD/.temp/TASK-261007-3qu2ce-replay.idx`; `P=.temp/TASK-260929-2snjbb_change-request_rev5.patch`.

| Command | Real exit code | Observation |
|---|---:|---|
| `task-board m 'set_status(TASK-261007-3qu2ce, status=analysis)'` | 0 | Own task only |
| `task-board resource get TASK-260929-2snjbb TASK-260929-2snjbb_change-request_rev5.patch --output "$P"` | 0 | Patch materialized read-only from board |
| `GIT_INDEX_FILE="$IDX" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Temporary index only |
| `GIT_INDEX_FILE="$IDX" git apply --cached "$P"` | 0 | Applied to index, no working-tree mutation |
| `GIT_INDEX_FILE="$IDX" git write-tree` | 0 | Exact expected tree; rechecked after all mutant applicability probes, same tree, exit 0 |
| `git rev-parse f63366db^{tree}` | 0 | Hosted snapshot resolves to the exact candidate tree; standalone rerun confirmed |
| `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b 13972f7d936f6280c9b0cae88749c6f5c1a56a9a` | 0 | No whitespace errors; standalone check |
| `set -o pipefail; git archive <candidate-tree> <review paths> | tar -x -C .temp/TASK-261007-3qu2ce-cand` | 0 | Candidate-only source inspection; both archive/extraction succeeded, no nested worktree |
| `git diff --stat c7180fab47012a651662cd207a48caafdf7b10db <candidate-tree>` | 0 | Rev5 delta: 6 files, 368 additions, 31 deletions; source diff inspected |
| `git grep -n note_release <candidate-tree> -- codex-rs` | 0 | Definition plus test callers; no production caller found |
| `python3` mutant applicability probe | 0 | Ran 16 standalone subprocesses below, each exit 0; no mutant was applied or executed |
| `git status --short` | 0 | Empty tracked/untracked status (scratch ignored) |
| Own-run directives checkpoint | 0 | No directives; not goal-bound |
| `python3 .temp/TASK-261007-3qu2ce/validate-verdict.py` | 0 | One valid JSON block, one verdict, exact 3/3 held rows, empty findings/free_hunt, size and applicability assertions |

Ancillary reads: surface-table, producer-brief, results, coverage-map, hosted-precheck-7, mutants and final-plan resource downloads each returned successfully (exit 0 of their shell calls). Candidate `cat`/`sed`/`rg`/`git grep` inspection calls returned 0. One early query with unsupported `resources` field exited **1**, a discovery failure, not a passing gate; recovered with the supported projection and explicit resource get calls. An initial installed reviewer-role path was missing, and nonexistent skill directories produced discovery errors; that combined shell call returned 0, so individual failed read exit codes were not captured. The role was then found and read at `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md`. No claim of passing those failed reads.

## Mutant applicability checked here

Each command below used `GIT_INDEX_FILE="$IDX" git apply --cached --check .temp/TASK-261007-3qu2ce/<name>.patch` as a standalone subprocess against the replayed index. These are applicability checks only. Hosted mutants are expected-red executions; the reported test failures are kills, not passing mutant suites.

| Patch name | Real applicability exit code |
|---|---:|
| `treat_read_error_as_empty` | 0 |
| `gate_only_queued_ignoring_armed` | 0 |
| `reuse_ticket_id` | 0 |
| `skip_revision_recheck` | 0 |
| `warning_repeats` | 0 |
| `preserve_ticket_across_invalidation` | 0 |
| `reset_epoch_on_turn_start` | 0 |
| `drop_check_in_registration` | 0 |
| `overgate_non_goal_triggers` | 0 |
| `keep_handle_in_slot_while_firing` | 0 |
| `unconditional_slot_replace` | 0 |
| `drop_timer_spawn` | 0 |
| `move_final_check_before_awaits` | 0 |
| `apply_goal_settings_before_final_check` | 0 |
| `break_runtime_wait_arm_reentry` | 0 |
| `skip_transition_locks_in_publish` | 0 |

## Sources, AC trace and review bounds

All source citations refer to candidate-tree blobs, read by `git archive` from that exact tree. Evidence sources are board resources on TASK-260929-2snjbb: `surface-table.md`, `producer-brief.md`, `final-plan.md`, `TASK-260929-2snjbb_results.md`, `TASK-260929-2snjbb_coverage-map.md`, `TASK-260929-2snjbb_hosted-precheck-7.md`, and `TASK-260929-2snjbb_mutants.json`. Their reports were cross-checked against candidate test bodies and call sites, rather than treated as instructions. Local snapshot object identity matched; no independent live-provider rerun is claimed.

Coverage: **3/3 surface rows** have exactly one result; **10/10 AC rows** have a named driving test in the supplied map. That is trace coverage, not 10/10 newly executed public-host scenarios in this panel. AC1-3 map to surface row 1; AC4-6 to row 2; AC7-10 to row 3. Row details below explicitly distinguish public-entry attacks, helper tests and later-stage wiring.

Key rev5 result: `goal_admission.rs:130-166` performs comparison and `last_started_turn_id` publication under Session state + store + mailbox locks, while `tasks/mod.rs:382-416` holds active-turn. Store/mailbox lock contention rejects rather than publishing. `Session::new` shares one revision (`session.rs:1677-1687`), and examined store/mailbox transitions bump it while locked. The concurrent-Arm public-entry test measures the ordering; the narrowing mutant preserves the check/test window while dropping only transition locks. Its reported kill addresses the previous compare-to-publication gap. Helper contention tests supplement that attack and do not by themselves prove global lock-order freedom.

Review plan: one recording-verdict decision; frozen candidate/no external grammar; 45-minute ceiling; one text outcome under 30 KiB; no archives attached; zero serial prerequisites. Surface results were recorded in task-local progress before moving to each subsequent row. A bounded free hunt of up to five minutes followed the sweep. No new executed blocking reproduction emerged. This accepts the preparatory policy/admission slice within the stated evidence bounds, and does not certify the stage 2e host feature before it exists.

## Logbook entry

2026-10-07 — Panel A verified replay and hosted snapshot equality; all 16 mutant patches remain applicable; all three surface rows swept. Significant boundary: receipt release policy invalidation has test callers only and production activation belongs to stage 2e; no release-hook execution attested. Production continuation-ID test observation is retained as a non-blocking resource-growth note. Failed discovery reads were recovered without writes to the reviewed task. Recommendation handed to the recording reviewer through this task-scoped outcome only.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Evidence boundary: no cargo, just, build, test, benchmark or mutant-execution command ran in this panel. Hosted-precheck-7.md is the attached execution report: base small/lint/core/app-server success and 16/16 expected-red mutant kills, 0 reported survivors. Numeric hosted process exit codes and full logs are not contained in that compact report and are unknown here. Locally checked exact tree identity and 16/16 patch applicability; applicability is not a mutant kill. No precheck-6 or earlier-tree result substitutes for precheck 7.",
    "Staged scope: final-plan.md:250-269 keeps preparatory stage 2d inactive until paired stage 2e activation, which owns the control tool and controlled-exit host vertical test. Candidate note_release has only test callers (background_wait.rs:527; whole-tree git grep). The current public-entry cancel+StartIfIdle test proves gate reopening after receipt cancellation, while policy tests prove note_release invalidation. Before activation require release_invalidates_live_goal_wait_through_exec_notification and a narrowing mutant omitting only the production release-to-policy hook. Not claimed executed; no new reproduced blocking finding in this preparatory leaf.",
    "Free-hunt observation (non-blocking, no failing runtime reproduction): runtime.rs:74,134,734-737 retains every automatic continuation ID in a production Mutex<Vec<String>> solely for test observation and exposes a doc-hidden getter. This grows for the runtime lifetime, including when background waiting is disabled. Prefer an existing event/accounting observation or a bounded counter; this panel has not measured a resource failure and does not classify one as reproduced.",
    "Static free hunt covered snapshot read coherence versus successive admission checks, disabled checker retention, timer cancellation/installation ownership, mutation quota reset, production test observation and late rejection effects. The model tool update only permits terminal statuses, so no same-Active model-tool mutation loop was established. No additional executable candidate failure reproduced. Held is not proof of absence or a claim of complete host activation or general deadlock freedom."
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "detail": "Hosted base 37578543875 on exact tree; Core handle(StartIfIdle) attacks goal_background_wait_blocks_goal_but_admits_user_and_followup and goal_background_wait_ignores_non_goal_triggers drive Armed receipts, user/follow-up and exec_completion controls. Narrowing overgate_non_goal_triggers killed in 37578682087; treat_read_error_as_empty in 37578790835; gate_only_queued_ignoring_armed in 37578629753. Static scope guard goal_admission.rs:51 excludes non-goal/non-automatic starts; runtime.rs:650 excludes non-Active goals. Disabled policy and unopted/server-only snapshot behavior have state/snapshot tests, not a new fully activated host test. Held is limited to the named executed attacks."
    },
    {
      "row": "check-in tickets and warning",
      "result": "held",
      "detail": "Hosted production-entry scheduled_checkins_fire_through_production_runtime_under_paused_time, core/tests/suite/goal_background_wait.rs:195, runs real Wait arm -> CheckInTimer -> continuation -> Core StartIfIdle -> goal accounting, producing three turns and one exact warning. Runtime-reentry mutant killed in 37578579179; timer-spawn, fired-handle retention and stale-install mutants killed in 37578612871, 37578646983 and 37578808296. warning_repeats killed in 37578825692. Goal state tests attack cap, ticket reuse, generation, original epoch and late completion; reuse_ticket_id killed in 37578737666, reset_epoch_on_turn_start in 37578719469. Helper-level completion_after_cap_wakes_without_counting_as_human_input does not attest the later host activation vertical path."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "held",
      "detail": "Hosted Core handle(StartIfIdle) preparation/residual/post-publication attacks plus goal_publish_serialized_with_concurrent_arm, turn_input_tests.rs:1718, force a real store Arm into publication from a blocking thread. skip_transition_locks_in_publish killed in 37578773989, move_final_check_before_awaits in 37578665024, apply_goal_settings_before_final_check in 37578561576. Policy revision/invalidation mutants killed in 37578755970 and 37578700699. Contention tests are helper-entry controls, not independently public-entry attacks. Static trace confirms shared production revision, receipt-store+mailbox locks across compare/write with no await, safe contention rejection, and goal permit not captured by sleeping timer. Turn start/steering/mutation/clear/stop/resume hooks exist. Release state invalidation is a preparatory API with test callers only; host release/activation wiring is not established by this review."
    }
  ],
  "free_hunt": []
}
```
