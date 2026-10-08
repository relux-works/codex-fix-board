# R141 panel B — TASK-261002-1abmbj: rev2 goal activity publisher review

changes_requested

Replay tree check: **MATCH**. Base `ea8899e6f97aea64136159286840c28c955243e8` plus resource `TASK-260929-2gp04j_change-request_rev2.patch`, replayed through a temporary index, gives exactly `d401bcff58f9724a36966053dde5386be1af7882`. Hosted snapshot `10bc26b11571a85b738ba8a84569fc33f56ffc1f^{tree}` independently resolves to that same tree.

## Scope and bounded plan

Decision: recommend accept or changes_requested for CR-TASK-260929-2gp04j-2; the recording reviewer consumes this outcome. Frozen input: named CR patch/base/tree and the one-row surface table; no new grammar. Budget: 30 minutes for sweep/packaging, 3 minutes bounded free hunt; one document plus small witness/logs, no archive, no serial research prerequisite. Exit: exact-tree replay, each surface row once, one verdict JSON block attached. Implementation consumer: existing G2 rework leaf, not a new research task. No repository edits, builds, tests, commits, branch operations, or writes on TASK-260929-2gp04j.

## Commands and real exit codes

| Command | Exit | Evidence / meaning |
|---|---:|---|
| `task-board m 'set_status(TASK-261002-1abmbj, status=analysis)'` | 0 | Own-task lifecycle only |
| `git --version`; `command -v task-board`; `command -v rg`; `python3 --version` | 0 | Tool readiness: Git 2.54.0, Python 3.14.7, CLIs available |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev2.patch --output .temp/TASK-260929-2gp04j_change-request_rev2.patch` | 0 | Read-only input retrieval |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-1abmbj-replay.idx" git read-tree ea8899e6f97aea64136159286840c28c955243e8` | 0 | Temporary index initialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-1abmbj-replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev2.patch` | 0 | Patch applies |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-1abmbj-replay.idx" git write-tree` | 0 | Expected candidate tree printed |
| `git diff --exit-code 58042581 d401bcff58f9724a36966053dde5386be1af7882 -- codex-rs/core/src/tools/spec_plan.rs codex-rs/ext/extension-api codex-rs/core/tests/suite/current_time_reminder.rs` | 0 | G1 unchanged; g1-identity-01.log empty by design |
| `git diff --check ea8899e6f97aea64136159286840c28c955243e8 d401bcff58f9724a36966053dde5386be1af7882` | 0 | diff-check-01.log empty by design |
| `git rev-parse 10bc26b11571a85b738ba8a84569fc33f56ffc1f^{tree}` | 0 | Hosted snapshot identity matches |
| `python3 .temp/TASK-261002-1abmbj/TASK-261002-1abmbj_static-witness.py` | **1** | Expected red, structural AC7 failure; not a passing test or runtime reproduction |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives |
| `git status --short` | 0 | Empty tracked/untracked repository delta; scratch is ignored |

Routine candidate `git show`, `git diff`, `git grep`, source `cat`/`sed`, task AC/checklist reads and resource-path inventory succeeded (exit 0). Initial discovery errors: unsupported query field `resources` exit 1 (recovered with resource CLI); absent role file under skill `.roles` exit 1 (loaded actual `/Users/iv/.roles/reviewer/role.md`); skills inventory over absent `agents/skills` and `.claude/skills` exit 2 (used existing `.codex/skills`). Role-path search with no match exited 1; no review assumption depends on it. These are not validation passes.

## Key finding and repair recommendation

Round-1 revocation is fixed for turn-stop and abort, but the read-failure class remains on external set and tool-finish accounting. For external set, start with a live committed Active goal and a published marker, corrupt `updated_at_ms` as the existing regression tests do, then call production `GoalService::set_thread_goal` with a valid objective update. Preparation either has no snapshot or propagates a read error to a warn-only handler; the direct goal read then errors via `?` before reconciliation. Nothing publishes Unknown/removal. This is a static path derivation, not a dynamically run scenario.

Route these read failures through the sole publisher. Add a named regression through external set and a narrowing mutant that retains the marker on that error path; cover the tool-finish second-read failure with targeted fault injection if necessary. Do not create another research leaf. Keep the existing 15 mutants and the two repaired tests.

## Outcome-scoped logbook

2026-10-02: replay matched; G1 preserved; static attack found the same read-failure revocation class still present outside the newly covered stop/abort exits. Producer's asserted external-set audit is contradicted by `api.rs` early `?` returns. Hosted green evidence remains valid for its exact tested candidate and measured 15/15 mutants; it does not prove untested read-error paths. Recorded solely on this panel task, with no source-task mutation.

## References and evidence limits

- Source task read-only resources: `surface-table.md`, `producer-brief.md`, `g2-rework-brief-rev2.md`, `TASK-260929-2gp04j_results.md`, `TASK-260929-2gp04j_review-verdict-rev1.md`, `TASK-260929-2gp04j_hosted-precheck-3.md`.
- Immutable candidate paths: `codex-rs/ext/goal/src/{activity,api,extension,runtime,tool}.rs`; tests in `ext/goal/tests`, `core/tests/suite/goal_activity_tests.rs`, `app-server/tests/suite/v2/goal_activity_tests.rs`.
- Production external callers: `codex-rs/app-server/src/request_processors/thread_goal_processor.rs:176` (set) and `:121` (fork flush).
- Reused hosted execution: https://github.com/relux-works/codex/actions/runs/37014493254 . This panel checked tree identity and read the attached outcome; it did not fetch hosted job logs or independently rerun suites/mutants.
- Static witness is intentionally bounded source analysis pinned to three blobs, not a parser, runtime emulator, or replacement for Rust regression tests.

```verdict-findings
{
  "findings": [
    {
      "id": "accounting-read-failure-retains-capability",
      "row": "goal activity publisher",
      "invariant": "AC7 and rev2 rework step 1 require every goal-state read failure on accounting/metrics paths to revoke GoalActivity through the sole publisher, record Unknown, report the error, and recover at the next lifecycle event.",
      "mechanism": "Remaining error propagation bypasses publication. GoalService::set_thread_goal at codex-rs/ext/goal/src/api.rs:188-202 and :243-251 warns on preparation/accounting error, then returns via ? on either get_thread_goal error before reconcile_live_activity at :283. A previously Known Active/BudgetLimited marker therefore survives a persistent malformed-row read failure. prepare_external_goal_mutation_locked calls accounting without error publication (runtime.rs:253-283). The same class remains on on_tool_finish at extension.rs:555-559 when current_goal_status_for_metrics (runtime.rs:796-804) fails after the leading successful reconcile. The latter needs a failure between reads; the former does not. The new four revoke calls cover stop/abort only.",
      "reproductions": [
        {
          "test_file": "TASK-261002-1abmbj_static-witness.py",
          "command": "python3 .temp/TASK-261002-1abmbj/TASK-261002-1abmbj_static-witness.py",
          "expected_failure": "Exit 1 (observed): pinned immutable-source control-flow witness identifies external-set goal-read ? exits and tool-finish accounting warn/return before sole-publisher error publication. Static evidence only; no Rust build, runtime fault injection or dynamic reproducer executed. Output attached as TASK-261002-1abmbj_static-witness-01.log.",
          "pinned_blobs": [
            "git-blob:a4512db548378bcdf499cd47eca670d366a8f9a3",
            "git-blob:87849af544305d6d8897a382e62a746d9f6d4e8e",
            "git-blob:153d947f523890868dac9554c9a84393800f4869"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "CR-TASK-260929-2gp04j-1:accounting-read-failure-retains-capability"
    }
  ],
  "notes": [
    "No builds/tests run. Hosted precheck-3 outcome reports all four lanes green on run 37014493254 and 15/15 intended narrowing-mutant kills; these are reused attached evidence, not independently executed here. Snapshot commit 10bc26b tree was independently resolved and matches candidate d401bcff exactly.",
    "Producer results map 8/8 AC rows to tests. Those tests and 15 mutants do not establish coverage of external-set error exits or the tool-finish second-read window. The stated untestable transient bound is not a contractual exclusion from AC7; external-set is a persistent-failure witness and avoids that bound.",
    "G1 spec_plan, extension-api subtree and current_time_reminder tests are unchanged against checkpoint 58042581 (diff exit 0). All G2 changed source files and test entry points inspected; exactly one surface-table row exists.",
    "Keep nonblocking round-1 context: oversized diff requires upstream staging by orchestrator; core test-only dev-dependency cycle is not a production library cycle; Bazel activity.rs compile data is declared. Lock refresh/no-delta is producer evidence, not Bazel verification by this panel.",
    "Automatic-start shared permit lease has no turn identity. Overtaking turn or disable/re-enable races were inspected but not dynamically reproduced; no additional blocking finding claimed."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "Swept all listed families statically: create success/refusal, pre-baseline/Plan start, resume/external set per status, updates/automatic stop/accounting, disabled clear/stale callback, disable/stop/re-enable, read failure/recovery, duplicate/out-of-order publication and app-server next request. Static immutable-source failure witness confirms remaining read-error exits (finding accounting-read-failure-retains-capability). Hosted dynamic family evidence reused; no new public-entry runtime attack run here."
    }
  ],
  "free_hunt": [
    {
      "area": "G1 identity, package dependencies and build-data declarations, shared permit lease",
      "result": "No additional blocking reproduction. G1 identity and diff checks green; no Bazel execution or dynamic concurrency proof."
    }
  ]
}
```
