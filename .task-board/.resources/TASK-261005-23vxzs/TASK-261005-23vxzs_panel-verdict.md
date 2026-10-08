# TASK-261005-23vxzs — DELTA panel verdict for CR-TASK-260929-2gp04j-4

accept

Replay tree check: **exact match**, `65ad71d230e7d7ac5923b8f88739a504b0fc1d08`, from base `729f259e62a8d11d9e17398e487790e1ee5d8b8c`. Hosted snapshot `a37e2ebc` independently resolves to this tree.

Scope: non-recording DELTA review. Read previous merged rev3 verdict, checked all four finding records, swept the single supplied surface row and all eight AC families, then performed a bounded same-class/regression hunt. No build/test or write on TASK-260929-2gp04j. Frozen tree; no additional prerequisite required.

## Commands run and actual exit codes

All validation commands ran directly; no tee or hidden pipe status. Scratch files are under `.temp/TASK-261005-23vxzs/`; the replay index is `.temp/TASK-261005-23vxzs-replay.idx`.

| Command | Exit | Evidence |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261005-23vxzs, status=analysis)'` | 0 | Panel lifecycle only |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev4.patch --output .temp/TASK-260929-2gp04j_change-request_rev4.patch` | 0 | Patch retrieved read only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-23vxzs-replay.idx" git read-tree 729f259e62a8d11d9e17398e487790e1ee5d8b8c` | 0 | Base loaded |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-23vxzs-replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev4.patch` | 0 | Replay applied in temporary index only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-23vxzs-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git rev-parse 'a37e2ebc^{tree}'` | 0 | Exact hosted snapshot identity |
| `git diff --check 729f259e62a8d11d9e17398e487790e1ee5d8b8c 65ad71d230e7d7ac5923b8f88739a504b0fc1d08` | 0 | No whitespace errors |
| `python3 .temp/TASK-261005-23vxzs/audit.py` | 0 | 25/25 distinct hosted/attached mutant names agree; all 25 `git apply --cached --check` subprocesses exit 0; no mutant applied/executed |
| `git grep -n -e 'insert(GoalActivity' -e 'remove::<GoalActivity>' 65ad71d230e7d7ac5923b8f88739a504b0fc1d08 -- codex-rs/ext/goal` | 0 | All seven production writes confined to activity.rs |
| `git diff --stat` / `--numstat` between rev3 and rev4 trees | 0 | Two files, 562 additions / 63 deletions |
| `git show <candidate>:<path>` pinned file reads/export (nine files) | 0 each | Candidate sources/tests/store internals inspected |
| `task-board resource get` for surface-table.md, previous rev3 verdict, producer-brief.md, results, hosted-precheck-8.md, mutants.json | 0 each | Source citations below |
| `task-board q 'get(TASK-260929-2gp04j) { description scope ac }'` | 0 | 8 AC rows read |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives |
| `git status --short` | 0 | No tracked/untracked repository delta |
| `python3` artifact JSON/structure validation (inline) | 0 | Exactly one verdict-findings block, accept verdict and 1/1 unique surface row; initial file 15451 bytes |
| `task-board resource add TASK-261005-23vxzs /tmp/TASK-261005-23vxzs_panel-verdict.md --type outcome --name TASK-261005-23vxzs_panel-verdict.md` (with description) | 0 | Outcome attached only to panel task |

Tool readiness: `git --version`, `rg --version`, `task-board --help`, `python3 --version` all returned expected output (0); readiness log is task-local. Initial combined skill inventory ended **2** because absent search directories were included; it still listed the available .codex skills. This was not a validation pass. An initial query requesting unsupported `resources` returned a semantic parse error, and `schema(get)` reported unsupported positional arguments (CLI process 0); corrected scoped AC query and `schema(operation="get")` succeeded. Neither failed read was treated as absence or green evidence.

Reused hosted commands: lint/small/core/app-server suites and 25 mutants were **not run by this panel**. Their process exit codes are **unknown here**; attached precheck-8 reports four success conclusions for snapshot run [37263271056](https://github.com/relux-works/codex/actions/runs/37263271056) and named failures for all 25 mutant runs. No exit code is inferred from a job conclusion.

## Sources and previous-round disposition

Read-only board resources on TASK-260929-2gp04j: `surface-table.md`, `producer-brief.md`, `TASK-260929-2gp04j_review-verdict-rev3.md`, `TASK-260929-2gp04j_results.md` (latest precheck-8 addendum supersedes earlier pending evidence), `TASK-260929-2gp04j_hosted-precheck-8.md`, `TASK-260929-2gp04j_mutants.json`. Source citations below are paths/lines in the exact candidate tree, read via git show rather than the stale worktree.

| Prior record | Result | Verified mechanism / execution evidence |
| --- | --- | --- |
| clear-error-retains-capability | addressed | Guarded delete settles both prepare failure + delete refusal and returned-row decode failure. Hosted run 37263317078 kills clear-site bypass. |
| clear-returning-decode-retains-capability | addressed | Regression :1051 asserts Err, no marker, zero SQL rows, next-turn absence and recovery. Same clear-site narrowing kill. |
| set-post-write-read-failure-retains-capability | addressed | Three service write sites guarded; post-write phases A/B and dedicated replace precondition. Runs 37263517219 / 37263544776 / 37263531175 kill individual site bypasses. |
| clear-read-failure-retains-capability | addressed | Refused deletion revokes conservatively; preparation error cannot escape before guarded settlement. Test :1129 and clear-site narrowing kill. |

## AC-family attack map (8/8 inspected)

These are dimensions within the one surface row, not extra surface_results rows. Hosted precheck-8 supplies execution on the exact tree; local work supplies static inspection.

| AC | Production entry and negative attack | Exact-tree evidence |
| --- | --- | --- |
| 1 | GoalToolExecutor::handle publishes before returning create; failed arguments still reconcile committed absence | create_goal_changes_the_next_sampling_tools created/refused; create_waits_for_finish killed 37263362618 |
| 2 | GoalExtension::on_turn_start reconciliation precedes baseline/Plan returns; cleared state removes stale capability | turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal; turn_start_requires_baseline killed 37263619598 |
| 3 | GoalService::set_thread_goal and restore_after_resume reconcile all six statuses | external_set_and_resume_reconcile_first_request; budget-limited set/resume narrowings killed 37263439586 / 37263501158 |
| 4 | Update/stop/accounting mutations reconcile; BudgetLimited keeps marker without automatic continuation | create_goal_changes_the_next_sampling_tools terminal statuses; automatic_stop_revokes_activity_for_error_and_usage_limit; accounting_budget_keeps_sleep_without_automatic_continuation; kills 37263346161 / 37263653941 / 37263301509 |
| 5 | Clear revokes unconditionally, including disabled clear; delayed create/set callbacks cannot replay authority | clear_revokes_before_late_create_finish_and_stale_set_effects; disabled_clear / late_active_set / cleared_revision kills 37263392780 / 37263485560 / 37263331927; new decode/refusal regressions and clear bypass kill 37263317078 |
| 6 | Feature disable/stop removes marker + pending state; enable reconciles committed state | disable_and_stop_revoke_activity_and_pending_options and disable_mid_turn_removes_sleep_from_next_request; disable/stop narrowings killed 37263377567 / 37263560187 |
| 7 | Publisher records Unknown/revokes on error; service guard now includes post-write/decode errors; next lifecycle recovers | read_failure, turn_stop/abort/error, tool_finish, set_get/prepare/post_write/replace, fork_flush, clear_decode/prepare regressions; individual narrowing kills listed in hosted table, all 25 named patches verified applicable |
| 8 | App-server v2 turn/start drives real create/refusal -> next /responses tools | v2_create_goal_exposes_sleep_only_after_committed_success created/refused, passing attached snapshot app-server lane |

## Outcome-scoped logbook

Rev3's rollback assumption was the defect: a read-modify-return method can report Err after commitment. Rev4's guard repairs that class across all four service write sites. The prior replace-path mutant survivor was a test-precondition gap: the original phase C started with no marker, so skipping revocation was invisible. The dedicated test :1194 explicitly establishes a stale published marker before failing insertion, and precheck-8 records its kill. No new regression or anomaly requiring original-task mutation was established. Evidence discrepancy: the brief guard-gut row lists three tests while results prose says five; this review relies on listed failures and the four independent site kills. Inherited size/Bazel and concurrency bounds remain explicit below.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Replay exact: base 729f259e62a8d11d9e17398e487790e1ee5d8b8c -> candidate 65ad71d230e7d7ac5923b8f88739a504b0fc1d08. Independently resolved hosted snapshot a37e2ebc^{tree} to the same tree. Source TASK-260929-2gp04j was read only: no accept/reject/withdraw/status/notes/resource/handoff write.",
    "Previous finding clear-error-retains-capability: addressed. api.rs:342-356 wraps delete_thread_goal result before ?; api.rs:394-405 revokes the live marker on any Err. Clear preparation warns at :338 but is followed without an intervening error exit by guarded delete, so either deletion success clears at :361 or error revokes. clear_prepare_failure and clear_returning_decode_failure exercise both outcomes; hosted clear_delete_bypasses_guard run 37263317078 kills both.",
    "Previous finding clear-returning-decode-retains-capability: addressed. StateRuntime still commits DELETE RETURNING before fallible decoding (state/src/runtime/goals.rs:472-496); the service guard correctly covers that fact instead of inferring rollback from Err. core/tests/suite/goal_activity_tests.rs:1051-1126 asserts Err, marker None, raw row count 0, continued absence and later Active recovery with higher revision. The exact-tree hosted snapshot reports this regression passing.",
    "Previous finding set-post-write-read-failure-retains-capability: addressed. The objective-update, replace, and status-update store calls are guarded at api.rs:205,233,264. StateRuntime update still reads after UPDATE at state/src/runtime/goals.rs:417, but all its Err outcomes now revoke. core/tests/suite/goal_activity_tests.rs:848-1048 phases A/B corrupt post-write timestamp, assert Err+marker absence and verify committed Complete after repair. Hosted narrowing kills: objective 37263517219, status 37263544776. Replace has its own stale-marker precondition and failure/recovery test at :1194-1282, killed by set_replace_bypasses_guard run 37263531175.",
    "Previous finding clear-read-failure-retains-capability: addressed by the same guarded delete. core/tests/suite/goal_activity_tests.rs:1129-1191 combines preparation write failure with DELETE refusal, asserts Err+marker None, then recovers the same Active goal with higher revision after removing the triggers. A persistent metrics read failure also reaches this guarded delete settlement; this latter specific fault is a static control-flow conclusion, not a separately executed Rust attack by this panel.",
    "Hosted evidence reused under the panel brief, not rerun: TASK-260929-2gp04j_hosted-precheck-8.md and the latest precheck-8 addendum in TASK-260929-2gp04j_results.md report snapshot run 37263271056 lint/small/core/app-server success and 25/25 mutant kills. Independent local checks establish exact tree identity, 25/25 mutant-name correspondence and 25/25 patch applicability. No live GitHub read or individual hosted logs fetched by this panel; numeric hosted process exit codes were not supplied, so they are UNKNOWN here. Job success is not represented as an independently observed shell exit 0.",
    "The guard_skips_revocation_on_store_error patch removes the error-arm revoke and is a supplementary delete-style control. The four *_bypasses_guard patches preserve the guard while withholding runtime for exactly one site: these are the narrowing evidence for site coverage. The brief hosted table lists three named guard-gut failures; results addendum says five. Acceptance relies on the three listed failures plus four individually named site kills, not on assuming the unlisted two guard-gut failures.",
    "Execution bounds: no cargo, just, builds, local Rust tests, mutant execution, branch operations, commits, publication or source changes. AC mapping 8/8 and surface sweep 1/1 are measured mapping/sweep counts, not exhaustive schedule/fault coverage. Arbitrary cancellation/concurrency schedules, pure read-only API failures, continuation-deferral flags, Bazel execution and foreign-OS execution were not dynamically established here.",
    "Rework size independently measured: revision 3 candidate -> revision 4 is 562 insertions/63 deletions in api.rs and one core integration-test file (625 changed lines; production delta 120/62). Full base -> candidate is 2761/153 across 22 files, including G1 prerequisites. This retains the upstream staging note: land typed capability/consumer prerequisite separately, then publisher/lifecycle/tests; integration/staging is orchestrator-owned. No rev4 wire/config/CLI/history-fragment or dependency change found."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "held",
      "detail": "1/1 supplied surface rows swept, 8/8 AC families inspected. All four prior finding records addressed; clear and three set store sites have concrete regression preconditions plus individually killed narrowing mutants on the exact candidate tree. Static same-class sweep through tool dispatch, metrics/accounting callers, lifecycle mutation errors and GoalStore post-write reads found no additional blocking escape. This held result uses attached hosted public-entry execution plus pinned static inspection, not locally executed Rust tests."
    }
  ],
  "free_hunt": [
    "Bounded same-class hunt: inspected GoalStore update/delete internals and caller settlement, all API store writes, unconditional post-tool reconciliation (tool.rs:175-195), accounting and stop error handlers (extension.rs:345,356,370,416,449-454,556), and fork preparation revoke (api.rs:125-134). Unlike revision 3, store Err no longer implies rollback; no new unguarded service write was found.",
    "Publisher ownership: git grep finds seven insert/remove calls, all confined to activity.rs. Publication revisions reject stale lifecycle reads; clear invalidates unconditionally, disable/stop revoke and remove goal-owned pending options/permits. Delayed API runtime effects re-read committed state and compare it before acting. These checks plus stale-revision and late-callback hosted kills support the stated row; no universal interleaving proof claimed.",
    "Rework regression hunt: guard awaits revocation while the existing goal-state permit is held; the revoke path resolves the live thread and publishes Err without reacquiring the semaphore, so no newly introduced self-deadlock was found. Success values and existing reconcile/clear paths are preserved. Failure propagates the original GoalServiceError after conservative removal; no public API payload changed.",
    "Context/API/build surfaces: candidate spec_plan consumes bounded typed GoalActivity to choose sleep; no new context fragment or history rewrite. Rev4 modifies only service error settlement and integration tests. Existing test-only sqlx edges and Bazel/dependency regeneration are inherited evidence, not independently validated. No additional blocking mechanism established within this bounded read-only review."
  ]
}
```
