# TASK-261005-19i1t5 — DELTA panel, CR-TASK-260929-2gp04j-3

changes_requested

Replay tree: **MATCH** — `a8fc9e0cc6e0aad477aba7cd377e3c93203932fe` from base `729f259e62a8d11d9e17398e487790e1ee5d8b8c`.

Read-only static panel. Decision: whether revision 3 closes the previous read-failure class without regressions. Frozen input: exact patch/base/tree above; grammar not applicable. Budget: one bounded panel sweep and free hunt, one text outcome, no serial research prerequisite. Consuming slice: orchestrator/recording reviewer merges panel verdicts for this CR. Exit criteria: replay identity, prior findings assessed, every surface row assigned once, concrete verdict attached. No production changes.

## Commands and exit codes

All replay and verification processes were run directly, without tee or backgrounding.

| Command | Exit | Evidence |
|---|---:|---|
| `task-board m 'set_status(TASK-261005-19i1t5, status=analysis)'` | 0 | Own task only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-19i1t5-replay.idx" git read-tree 729f259e62a8d11d9e17398e487790e1ee5d8b8c` | 0 | Temporary index |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev3.patch --output .temp/TASK-260929-2gp04j_change-request_rev3.patch` | 0 | Read-only source resource |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-19i1t5-replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev3.patch` | 0 | Replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-19i1t5-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git rev-parse '622007038bd2422ab19b446331ad21733f93e693^{tree}'` | 0 | Exact hosted snapshot tree |
| `git diff --check 729f259e62a8d11d9e17398e487790e1ee5d8b8c a8fc9e0cc6e0aad477aba7cd377e3c93203932fe` | 0 | Whitespace check |
| `python3 .temp/TASK-261005-19i1t5/static-clear-witness.py` | **1** | Expected-red: missing clear failure revocation; SQLite row deleted before caller decoding. Not a passing gate or Rust test |
| Resource reads for previous verdict, surface, hosted precheck 6, producer brief, results and mutants | 0 each | Stored in task-local `.temp/` |
| Scoped AC/checklist queries, source `git show`/`git grep`, snapshot materialization Python, status/diff inspection | 0 | Immutable candidate and bounded source inspection |

Diagnostic failures: initial skill discovery shell exited 2 because optional directories were absent; unsupported board projections `resources` and `artifacts` exited 1; `schema(get)` returned a DSL error (CLI exit 0), repaired with `schema(operation=get)` (0). `resource list` printed help (0); unused projection `inputs outcomes` was rejected (1). An initial replay invocation containing `rm -f` was rejected by command policy before execution (no process exit code); direct read-tree safely initialized the unused index. A local rg probe used the old app-server path and printed missing-file error; immutable `git grep` located `request_processors/thread_goal_processor.rs`. These are diagnostics, never passing gates. Tool-readiness outputs are under `.temp/TASK-261005-19i1t5/`.

No builds/tests were run. Hosted baseline and 20/20 mutant kills are accepted attached evidence, not independently rerun. Snapshot identity was independently checked here.

## Key finding and recommendation

The named round-2 exits are repaired, but clear is still an uncaught member of the same class. Revoke via the publisher on clear preparation and deletion/decode failure; distinguish a failed API return from whether SQL already committed. Add the concrete production-entry regression and narrowing mutant specified below. Green hosted lanes do not cover this error shape.

```verdict-findings
{
  "findings": [
    {
      "id": "clear-read-failure-retains-capability",
      "row": "goal activity publisher",
      "invariant": "AC7: a failed goal-state read revokes GoalActivity and records Unknown; a committed clear leaves no marker, including when decoding the deleted row fails.",
      "mechanism": "codex-rs/ext/goal/src/api.rs:311-326: clear preparation errors only warn; delete_thread_goal errors escape via ? before clear_activity at :331. codex-rs/state/src/runtime/goals.rs:472-496 executes autocommit DELETE RETURNING, then fallible thread_goal_from_row; model/thread_goal.rs:114 decodes updated_at_ms. Publish Active, use a Plan turn to avoid preparation accounting, corrupt updated_at_ms to i64::MAX, then call GoalService::clear_thread_goal: deletion removes the row, timestamp decoding returns Err, and no revocation executes. Marker remains Some although committed state is None. With Default-mode pending usage, the earlier metrics read also fails without revocation; a refused DELETE would leave Known after that read failure. Producer sweep rows 7 and 15 incorrectly assume every deletion Err means no committed deletion.",
      "reproductions": [
        {
          "test_file": "static-clear-witness.py (embedded below)",
          "command": "python3 .temp/TASK-261005-19i1t5/static-clear-witness.py",
          "expected_failure": "Observed exit 1, expected-red static control-flow witness plus real SQLite execution of the pinned DELETE RETURNING SQL. SQLite confirms row count 0 before fallible caller decoding. This is NOT execution of the Rust production entry point."
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_activity_tests.rs (requested new regression)",
          "command": "just test -p codex-core goal_activity::clear_decode_failure_revokes_activity_and_next_turn_recovers",
          "expected_failure": "NOT RUN and test not yet authored. Adapt external_set_get_failure fixture: publish Active, start a Plan turn, set updated_at_ms=i64::MAX, call service.clear_thread_goal, expect Err but GoalActivity None and raw SQL row count 0; next turn must remain absent. Current source retains Some. Also add pending-usage preparation failure plus a DELETE-refusal trigger variant; require Unknown/removal before returning. Add a narrowing mutant omitting clear-error revocation."
        }
      ],
      "severity": "robustness",
      "repeat-of": "CR-TASK-260929-2gp04j-2/accounting-read-failure-retains-capability"
    }
  ],
  "notes": [
    "Replay exact: base 729f259e62a8d11d9e17398e487790e1ee5d8b8c -> a8fc9e0cc6e0aad477aba7cd377e3c93203932fe. Snapshot 622007038bd2422ab19b446331ad21733f93e693 resolves to that same tree.",
    "All three round-2 finding records describe one class. Their named set-get branches, set preparation, fork preparation and tool-finish accounting error arm now revoke through the sole publisher. New tests cover both set branches, fork malformed reads, and tool-finish write-only fault after successful reconciliation. Exact repaired sites held; the class remains open in clear (F1).",
    "Hosted execution reused, not rerun or independently audited via GitHub: TASK-260929-2gp04j_hosted-precheck-6.md reports snapshot run 37247519316 success on all lanes and 20/20 narrowing mutants killed. These are executed attacks for the covered cases under the brief. No clear malformed-returned-row or clear-preparation refusal mutant exists among those 20; baseline green cannot prove this omitted error path.",
    "Tool-finish regression injects a write failure rather than a transient metrics read failure. The same Err arm unconditionally revokes for either source of error, verified statically; no separate dynamic transient-read execution claimed.",
    "No cargo, just, build, Rust test, branch mutation, commit or publication run here. Source task was read only; no notes/resources/status/accept/reject/handoff write on TASK-260929-2gp04j.",
    "Nonblocking inherited size note: cumulative CR 2305 changed lines (2207 additions/98 deletions) includes G1 and test-heavy rework; upstream staging remains orchestrator-owned. New sqlx edge is test-only; no independent Bazel execution or lock regeneration performed.",
    "Producer exclusion of pure API reads and deferral flags is a declared bound, not proof that every read failure revokes. F1 needs no expansion into those surfaces: clear is an explicitly required lifecycle mutation."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "1/1 rows swept. Create success/refusal, early-return turn-start, six-status resume/set, complete/paused/blocked updates, automatic stops and BudgetLimited, disabled clear/late callback, stop/disable/re-enable, malformed reads/recovery, revision ordering and app-server create-to-next-request inspected with mapped tests and 20 hosted narrowing attacks. Named rev-2 repairs held. Clear preparation/deletion error family is broken (F1); no matching hosted attack exists."
    }
  ],
  "free_hunt": [
    "Clear DELETE RETURNING decoding: broken; extended the same-class sweep into the GoalStore and found that fallible post-mutation decoding invalidates the producer assumption that a deletion Err preserves committed state. Included only once as F1.",
    "Publisher ownership and ordering: held statically; all production insert/remove GoalActivity calls in ext/goal are confined to activity.rs. Permit serializes mutations and revisions invalidate lifecycle changes. Arbitrary overtaking-turn/disable-re-enable schedules were not dynamically executed, so no universal concurrency proof claimed.",
    "API/context/dependency scope: no rework-added wire/config/CLI payload or model-context fragment found. Bazel declares activity.rs for integration compile data. Test-only dependency edges do not introduce a production library cycle. No additional blocking rework regression established."
  ]
}
```

## Outcome-scoped logbook

Same-class sweep found a false assumption in producer read-site rows 7/15: `delete_thread_goal` can commit deletion then fail decoding `RETURNING`. No control-root logbook file was edited. This outcome records the anomaly for the recording reviewer; only this panel task receives the resource and handoff.

## References

All code citations are pinned to candidate tree `a8fc9e0cc6e0aad477aba7cd377e3c93203932fe`, retrievable with `git show TREE:path`.

- `codex-rs/ext/goal/src/api.rs:311-331` — clear warning/early-return before revocation.
- `codex-rs/state/src/runtime/goals.rs:472-496` — DELETE RETURNING, then fallible decode.
- `codex-rs/state/src/model/thread_goal.rs:101-114` — timestamp conversion.
- `codex-rs/ext/goal/src/activity.rs:76-86` — sole publisher Unknown/removal/error reporting.
- `TASK-260929-2gp04j_review-verdict-rev2.md`, `surface-table.md`, `TASK-260929-2gp04j_results.md`, `TASK-260929-2gp04j_mutants.json` — read-only source-task resources.
- `TASK-260929-2gp04j_hosted-precheck-6.md` — exact-tree reused execution evidence; [snapshot run](https://github.com/relux-works/codex/actions/runs/37247519316).

## Reproducible static witness (not a Rust runtime test)

```python
import subprocess, sqlite3, sys
TREE = "a8fc9e0cc6e0aad477aba7cd377e3c93203932fe"
def source(path):
    return subprocess.check_output(["git", "show", TREE + ":" + path], text=True)
api = source("codex-rs/ext/goal/src/api.rs")
clear = api.split("pub async fn clear_thread_goal(", 1)[1].split("async fn read_thread_goal_for_set(", 1)[0]
prepare = clear.split("let cleared_goal", 1)[0]
assert "failed to prepare external goal mutation" in prepare
assert "revoke" not in prepare
assert ")?;" in clear.split(".delete_thread_goal(thread_id)", 1)[1].split("runtime.clear_activity", 1)[0]
goals = source("codex-rs/state/src/runtime/goals.rs")
delete = goals.split("pub async fn delete_thread_goal(", 1)[1].split("pub async fn account_thread_goal_usage(", 1)[0]
assert "DELETE FROM thread_goals" in delete and "RETURNING" in delete
assert "row.map(|row| thread_goal_from_row(&row)).transpose()" in delete
assert ".begin(" not in delete and "transaction" not in delete
# Exercise only the SQLite statement semantics, NOT the Rust entry point.
sql = delete.split('r#"', 1)[1].split('"#', 1)[0]
db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE thread_goals(thread_id TEXT, goal_id TEXT, objective TEXT, status TEXT, token_budget INTEGER, tokens_used INTEGER, time_used_seconds INTEGER, created_at_ms INTEGER, updated_at_ms INTEGER)")
db.execute("INSERT INTO thread_goals VALUES ('thread', 'goal', 'work', 'active', NULL, 0, 0, 0, 9223372036854775807)")
returned = db.execute(sql, ('thread',)).fetchall()
assert returned[0][-1] == 9223372036854775807
assert db.execute("SELECT COUNT(*) FROM thread_goals").fetchone()[0] == 0
print("EXPECTED RED: clear preparation does not revoke; delete decoding error escapes before clear_activity.")
print("SQLite DELETE RETURNING removed the malformed row before caller decoding; Rust entry-point test NOT RUN.")
sys.exit(1)
```

Packaging check: standalone Python JSON/row/identity validation exited 0 before attachment.
