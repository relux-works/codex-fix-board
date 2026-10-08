# TASK-261005-2x4cdu panel A — CR-TASK-260929-2gp04j-3

changes_requested

Replay base `729f259e62a8d11d9e17398e487790e1ee5d8b8c` produced exactly `a8fc9e0cc6e0aad477aba7cd377e3c93203932fe` (expected candidate tree).

## Commands and real exit codes

| Command run by this panel | Exit | Evidence |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261005-2x4cdu, status=analysis)'` | 0 | Own-task lifecycle only |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev3.patch --output .temp/TASK-260929-2gp04j_change-request_rev3.patch` | 0 | Read-only input |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2x4cdu-replay.idx" git read-tree 729f259e62a8d11d9e17398e487790e1ee5d8b8c` | 0 | Temporary index |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2x4cdu-replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev3.patch` | 0 | Patch replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2x4cdu-replay.idx" git write-tree` | 0 | Exact tree above |
| `git show -s --format='%H %T' 622007038bd2422ab19b446331ad21733f93e693` | 0 | Exact hosted snapshot tree identity |
| `python3 .temp/TASK-261005-2x4cdu/TASK-261005-2x4cdu_static-witness.py > .temp/TASK-261005-2x4cdu/static-witness-01.log` | **1** | Expected-red static + SQL witness; failure is not a passing gate |
| `git diff --check 729f259e62a8d11d9e17398e487790e1ee5d8b8c a8fc9e0cc6e0aad477aba7cd377e3c93203932fe` | 0 | Standalone whitespace check |

Tool readiness (`python3 --version`, `git --version`, `rg --version`) exited 0; scratch log is `.temp/TASK-261005-2x4cdu/tool-readiness-01.log`. Routine source/resource reads ran successfully. An exploratory board projection used unsupported `resources`, and an exploratory `git show` used a nonexistent path; neither supplied validation evidence. Corrected task-specific reads and the actual state `runtime/goals.rs` were used thereafter.

## Evidence boundary and coverage

This is replay plus static review. No Rust tests, local builds or hosted reruns were executed here. Reused execution source: `TASK-260929-2gp04j_hosted-precheck-6.md`, snapshot [hosted run 37247519316](https://github.com/relux-works/codex/actions/runs/37247519316), and referenced `g2-precheck-6-results.json`. Snapshot tree matches independently. Existing hosted attacks hold within their tested bounds; none addresses clear's error-before-publication path. Every surface row has exactly one result below.

Task-specific research contract: decision is this CR's panel verdict; frozen input is the replay identity; 45-minute review and 5-minute free-hunt ceiling, one text outcome, no serial prerequisites. Consuming slice is the recording reviewer of existing G2 implementation. No production edits requested or made in this panel.

## Outcome-scoped logbook

2026-10-05: rev3 covers previously named set/fork/tool-finish read failures, but clear still has a warning-only accounting error and an early delete error. The producer's assumption “delete failure implies unchanged committed state” is false for post-DELETE row decoding. Reuse the existing malformed-row fixture; add clear-specific regression and narrowing mutant to the owning implementation. Nothing was recorded on TASK-260929-2gp04j.

```verdict-findings
{
  "findings": [
    {
      "id": "clear-error-retains-capability",
      "row": "goal activity publisher",
      "invariant": "A goal-state read failure revokes GoalActivity and records Unknown; committed clear removes the marker unconditionally. Failed reads never authorize capability.",
      "mechanism": "codex-rs/ext/goal/src/api.rs:314-325: clear preparation/accounting errors only warn, and delete_thread_goal errors propagate before clear_activity at :330. runtime.rs:684-686 propagates a metrics goal-read error before publication. state/src/runtime/goals.rs:472-496 performs DELETE RETURNING outside a transaction and then fallibly decodes the returned row. An invalid updated_at_ms can therefore cause clear to report Err after the goal was deleted, while the previously published marker survives. Alternatively a persistent read/database failure makes both preparation and delete fail without removing the marker. These are two witnesses of the same missing clear-error revocation.",
      "reproductions": [
        {
          "test_file": "TASK-261005-2x4cdu_static-witness.py (full source below)",
          "command": "python3 .temp/TASK-261005-2x4cdu/TASK-261005-2x4cdu_static-witness.py",
          "expected_failure": "Observed exit 1. Pinned-source control-flow witness verifies both clear error exits before publisher revocation; exact candidate DELETE RETURNING executed in isolated SQLite proves malformed row removal precedes returned-row decoding. STATIC + SQL witness, not a Rust runtime or public-entry execution. Output reproduced below.",
          "pinned_blobs": [
            "codex-rs/ext/goal/src/api.rs 2d9780400b43ad12dfeb4ea5e207ce966a249f7a",
            "codex-rs/ext/goal/src/runtime.rs 2ca2a4f6db68a03380c279a223b02b0b0b9b1237",
            "codex-rs/state/src/runtime/goals.rs ed616e16b7c81d06bcf02302912e16f71ad936f3",
            "codex-rs/state/src/model/thread_goal.rs 12d2a78dac8990be14e2718d4427726c783916bc"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "CR-TASK-260929-2gp04j-2:external-accounting-read-failure-retains-capability"
    }
  ],
  "notes": [
    "Exact replay passed; snapshot commit 622007038bd2422ab19b446331ad21733f93e693 independently resolves to candidate tree a8fc9e0cc6e0aad477aba7cd377e3c93203932fe. No builds, cargo, just, branch changes, commits, or original-task mutations.",
    "Hosted precheck-6 is reused attached evidence: all four snapshot lanes success and 20/20 narrowing mutants reported killed. Local results JSON names failing goal tests for each mutant, although its killed booleans are false; failures/meaningful test names support the attached human summary. Individual hosted process exit codes were not supplied or independently fetched; no numeric exit code is inferred from a job conclusion.",
    "Producer read-site sweep row 7 claims a delete failure leaves committed state and marker accurate. DELETE RETURNING followed by fallible row decoding disproves that premise; read-site row 15 has the same gap. These rows are producer context, not additional surface-table rows.",
    "Request core regression clear_read_failure_revokes_activity_and_next_turn_recovers: use fixture/start_live_turn/record_live_usage, publish Active then corrupt updated_at_ms as existing external_set_get_failure test does; invoke GoalService::clear_thread_goal, assert Err and GoalActivity None. Reconcile next turn and assert marker absent when deletion committed. Add persistent read+delete failure case (rename goal table during live accounting), restore table and assert next-turn recovery with higher revision. Add narrowing mutant skipping revocation only for clear preparation/delete errors. These are requested, not executed tests.",
    "Revision-3 set/fork/tool-finish repair paths are present and match their named hosted kills. The remaining clear path repeats the prior all-read-failures class; request focused rework on the existing implementation, no new research leaf.",
    "Nonblocking size note: cumulative base-to-candidate change is 2207 insertions / 98 deletions across 22 files, including G1 prerequisite surfaces; stage upstream delivery. No new wire/config/CLI shape or history fragment observed; typed capability changes tool selection only. Bazel/dependency regeneration and target-platform runtime testing were not rerun by this panel."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "1/1 rows swept, 8/8 AC families inspected. Hosted snapshot plus narrowing-mutant attacks support create/refusal, early-return turn start, six-status resume/set, terminal update/automatic stop/budget, disabled clear/stale callbacks, disable/re-enable/stop, read-failure/recovery, and v2 next-request tools. Static + SQL clear-error witness exposes an uncovered AC5/AC7 failure; this broken result is explicitly not a locally executed Rust public-entry reproduction."
    }
  ],
  "free_hunt": [
    "Bounded static hunt of committed-delete versus returned-row decoding identified the second clear-error witness, merged in clear-error-retains-capability.",
    "Single publisher, revision invalidation, permit lease ownership, dependency/build wiring, external API and model-context scope inspected. No additional reproduced mechanism; arbitrary concurrency schedules and Bazel execution remain unverified."
  ]
}
```

## Witness output

    STATIC WITNESS: clear preparation read error only warns; delete error exits before publisher revocation.
    SQL WITNESS: exact candidate DELETE RETURNING removes malformed row before fallible Rust timestamp decoding.
    Expected red: rev3 retains prior GoalActivity on both clear error exits. No Rust/public-entry runtime test executed.

## Reproducible pinned-source witness

    import re
    import sqlite3
    import subprocess
    import sys
    TREE = 'a8fc9e0cc6e0aad477aba7cd377e3c93203932fe'
    def blob(path):
        return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)
    api = blob('codex-rs/ext/goal/src/api.rs')
    clear = api.split('pub async fn clear_thread_goal(', 1)[1].split('async fn read_thread_goal_for_set(', 1)[0]
    prepare = clear.split('let Err(err) = runtime.prepare_external_goal_mutation_locked(permit).await', 1)[1].split('let cleared_goal', 1)[0]
    assert 'tracing::warn!' in prepare
    assert 'revoke_' not in prepare and 'reconcile_' not in prepare
    assert clear.index('})?;') < clear.index('runtime.clear_activity(permit).await')
    runtime = blob('codex-rs/ext/goal/src/runtime.rs')
    account = runtime.split('async fn account_active_goal_progress_locked(', 1)[1].split('async fn account_idle_goal_progress(', 1)[0]
    assert account.index('current_goal_status_for_metrics(') < account.index('.await?;') < account.index('self.reconcile_live_activity(permit).await?;')
    goals = blob('codex-rs/state/src/runtime/goals.rs')
    delete = goals.split('pub async fn delete_thread_goal(', 1)[1].split('pub async fn account_thread_goal_usage(', 1)[0]
    assert 'row.map(|row| thread_goal_from_row(&row)).transpose()' in delete
    assert '.fetch_optional(self.pool.as_ref())' in delete
    assert 'transaction' not in delete
    sql = re.search('r#"(.*?)"#', delete, re.S).group(1)
    model = blob('codex-rs/state/src/model/thread_goal.rs')
    assert 'updated_at: epoch_millis_to_datetime(row.updated_at_ms)?' in model
    with sqlite3.connect(':memory:', isolation_level=None) as db:
        db.execute('CREATE TABLE thread_goals (thread_id TEXT, goal_id TEXT, objective TEXT, status TEXT, token_budget INTEGER, tokens_used INTEGER, time_used_seconds INTEGER, created_at_ms INTEGER, updated_at_ms INTEGER)')
        db.execute("INSERT INTO thread_goals VALUES ('t','g','work','active',NULL,0,0,0,9223372036854775807)")
        returned = db.execute(sql, ('t',)).fetchall()
        assert returned[0][-1] == 9223372036854775807
        assert db.execute('SELECT COUNT(*) FROM thread_goals').fetchone()[0] == 0
    print('STATIC WITNESS: clear preparation read error only warns; delete error exits before publisher revocation.')
    print('SQL WITNESS: exact candidate DELETE RETURNING removes malformed row before fallible Rust timestamp decoding.')
    print('Expected red: rev3 retains prior GoalActivity on both clear error exits. No Rust/public-entry runtime test executed.')
    sys.exit(1)

Artifact validation (standalone Python JSON/required-field/unique-row check): exit 0. Output: PASS: one verdict-findings block; valid required fields; 1/1 unique surface rows; changes_requested verdict.
