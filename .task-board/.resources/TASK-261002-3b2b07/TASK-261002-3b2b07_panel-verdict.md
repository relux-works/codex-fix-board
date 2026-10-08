# R141 DELTA panel — CR-TASK-260929-2gp04j-2, revision 2

changes_requested

Replay: base `ea8899e6f97aea64136159286840c28c955243e8` plus the attached revision-2 patch produced exactly `d401bcff58f9724a36966053dde5386be1af7882`. This is the expected candidate tree. No source files or branch state were changed.

## Commands and exit codes

Each validation below ran as a standalone process without pipes or tee.

| Command | Exit | Result |
|---|---:|---|
| `task-board m 'set_status(TASK-261002-3b2b07, status=analysis)'` | 0 | Panel lifecycle only |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev2.patch --output .temp/TASK-260929-2gp04j_change-request_rev2.patch` | 0 | Read-only input materialization |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3b2b07-replay.idx" git read-tree ea8899e6f97aea64136159286840c28c955243e8` | 0 | Temporary index initialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3b2b07-replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev2.patch` | 0 | Patch replayed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3b2b07-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git diff --exit-code 58042581a0b507ae62e7b1d8381c429baea1f689 d401bcff58f9724a36966053dde5386be1af7882 -- codex-rs/core/src/tools/spec_plan.rs codex-rs/core/tests/suite/current_time_reminder.rs codex-rs/ext/extension-api` | 0 | G1 unchanged (rerun standalone) |
| `git diff --check ea8899e6f97aea64136159286840c28c955243e8 d401bcff58f9724a36966053dde5386be1af7882` | 0 | Whitespace check |
| `python3 .temp/TASK-261002-3b2b07/TASK-261002-3b2b07_static-witness.py` | 1 | Expected-red, failing static witness: read-error paths bypass revocation. **Not a passing runtime gate.** |

Input reads (`surface-table.md`, `producer-brief.md`, merged rev1 verdict, results, hosted precheck 3), candidate `git show` reads, scoped checklist query and directive check exited 0. Initial compound skill-read/query command exited 1: linked reviewer-role file missing and `resources` was an invalid query field; recovered using compact valid projections and resource get. `task-board resource list` exited 0 but displayed help; it supplied no resource inventory. Tool readiness (git, rg, task-board, Python) exited 0; logs are in `.temp/TASK-261002-3b2b07/`. No builds, Rust tests, or mutants were executed by this panel.

Artifact structure validation: standalone `python3` JSON/schema assertion process exited 0; exactly one `verdict-findings` block, 1/1 unique surface rows, required finding/reproduction fields, and one-word verdict verified.

## Review and evidence bounds

Decision: whether rev2 repairs the merged round-1 finding across the publisher surface. Frozen precondition: CR base/tree and the single supplied surface row; grammar not applicable. Budget: one 45-minute static review, one verdict and one small witness, no prerequisite research leaves. Exit: exact replay, previous-finding assessment, one result per surface row and bounded free hunt. Consumer: orchestrator's merged verdict, followed by producer rework if requested.

The four repaired exits now publish Unknown/removal before returning. The malformed-row stop/abort tests and the two added narrowing mutants target that repair. Attached hosted evidence reports 15/15 kills, which this panel accepts as prior execution evidence for its stated tests only. It does not prove the uncovered external-set/fork paths.

Static counterexample: retain a published marker from a healthy Active goal, then make the goal row unreadable (the existing `updated_at_ms = 9223372036854775807` fixture). A live `GoalService::set_thread_goal` prepares accounting, reports the failed read, then its own read returns an error before publication. A fork flush propagates the failed accounting read directly. Both leave the previous marker until a later reconciling lifecycle event. These are real public service entries; app-server calls them from `thread_goal_processor.rs:121` and `:176`. The app-server set wrapper also has an earlier goal-service read, so this panel does not claim the persistent malformed-row scenario passes through that wrapper to set itself. The uncovered service paths remain within G2's runtime contract. The transient tool-finish window is a third same-class exit; it is statically evident but not dynamically reproduced.

Recommended rework: route read-error exits consistently through the sole publisher (including service/prepare callers) and add real-entry negative tests plus narrowing mutants for these paths. Preserve failure as Unknown rather than treating it as absence. No compensating policy change is needed.

## Task-scoped logbook

2026-10-02: Replay exact; G1 unchanged. Round-1 named paths repaired, same read-error class still exists outside those four exits. Producer's external-set persistent-failure reconciliation claim is contradicted by early `?` exits. Expected-red witness exit 1 attached; runtime reproduction not run. No write to the reviewed task. Upstream staging, dev-cycle and lock notes retained as nonblocking context.

## Sources

All code references resolve against candidate tree `d401bcff58f9724a36966053dde5386be1af7882` via `git show TREE:path`: `codex-rs/ext/goal/src/{activity,api,extension,runtime,tool}.rs`, `codex-rs/ext/goal/tests/goal_extension_backend/goal_activity_tests.rs`, `codex-rs/core/tests/suite/goal_activity_tests.rs`, `codex-rs/app-server/tests/suite/v2/goal_activity_tests.rs`, and `codex-rs/app-server/src/request_processors/thread_goal_processor.rs`. Board inputs: `surface-table.md`, `TASK-260929-2gp04j_review-verdict-rev1.md`, `TASK-260929-2gp04j_results.md`, `TASK-260929-2gp04j_hosted-precheck-3.md`. Hosted run referenced by the attached evidence: https://github.com/relux-works/codex/actions/runs/37014493254 (not independently queried).

```verdict-findings
{
  "findings": [
    {
      "id": "external-accounting-read-failure-retains-capability",
      "row": "goal activity publisher",
      "invariant": "Every goal-store read failure must revoke GoalActivity, record reconciliation Unknown, report the error, and allow the next legitimate lifecycle event to retry.",
      "mechanism": "The original four turn-stop/abort exits now revoke, but the same class remains in GoalService::set_thread_goal (api.rs:188-202,244-248): prepare_external_goal_mutation_locked errors only warn, then get_thread_goal propagates a persistent read failure with ? before reconcile_live_activity at :283. A previously published Active/BudgetLimited marker survives. GoalService::flush_thread_goal_progress_for_fork (:114-129) directly propagates the same preparation/accounting read error without reconciliation. runtime.rs:671-673 and :735-737 call current_goal_status_for_metrics; :790-797 propagates get_thread_goal failure before publication at :687/:751. The on_tool_finish accounting Err branch (extension.rs:555-560) also returns without revocation after its earlier reconcile, leaving a transient-failure window.",
      "reproductions": [
        {
          "test_file": "TASK-261002-3b2b07_static-witness.py",
          "command": "python3 .temp/TASK-261002-3b2b07/TASK-261002-3b2b07_static-witness.py",
          "expected_failure": "Exit 1 (observed): pinned-source control-flow witness verifies set/fork goal-read error propagation before Unknown/removal, plus the tool-finish post-reconcile accounting error exit. Static witness only; no dynamic Rust reproduction was run. Suggested production regression: publish Active on a registered live runtime, start a turn and record a token delta, corrupt updated_at_ms using the existing read-failure fixture, call GoalService::set_thread_goal or flush_thread_goal_progress_for_fork, then assert GoalActivity None and recovery on the next turn start; current control flow retains Some."
        }
      ],
      "severity": "robustness",
      "repeat-of": "accounting-read-failure-retains-capability"
    }
  ],
  "notes": [
    "The previous merged finding is repaired at the specifically named turn-stop/abort exits: all four call revoke_activity_on_read_failure; publisher error branch sets Unknown, increments revision, removes GoalActivity, and reports the error. New stop/abort tests use a real malformed GoalStore row and assert removal/recovery. Same-class coverage is still incomplete (F1).",
    "Hosted execution is reused attached evidence, not independently rerun or remotely re-attested: TASK-260929-2gp04j_hosted-precheck-3.md identifies tree d401bcff58f9724a36966053dde5386be1af7882, snapshot 10bc26b11571a85b738ba8a84569fc33f56ffc1f, run 37014493254 green lint/small/core/app-server, and 15/15 intended mutant kills. These kills do not cover external set/fork persistent read failures or the tool-finish transient window.",
    "G1 paths are byte-identical to checkpoint 58042581a0b507ae62e7b1d8381c429baea1f689. Replay and static checks were run here; no cargo/just/build/test or mutant execution was run.",
    "Producer results claim external set preparation failures subsequently reconcile on persistent failure. The early get_thread_goal ? paths contradict that claim. The stated tool-finish transient bound is explicit but does not satisfy the unconditional read-failure invariant.",
    "Nonblocking round-1 context retained: G2 is 1526 changed lines (1450 insertions / 76 deletions); stage upstream delivery. Core->goal test-only dev edge is not a normal-library cycle. Bazel lock no-delta refresh is producer evidence, not independently verified by this panel.",
    "No mutations, resources, status changes, accept/reject or handoff were made on TASK-260929-2gp04j. Only this panel task receives outcome resources and lifecycle writes.",
    "Installed project-management reviewer-role reference was missing. Explicit panel review-round instructions were followed; no source workflow was modified."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "1/1 surface rows statically attacked, including create success/refusal, baseline/Plan early exits, all six resume/set statuses, update/stop/budget transitions, disabled clear and late callbacks, disable/stop/re-enable, read failures, revision/order guards, and app-server next-request integration. Named round-1 stop/abort paths repaired; persistent external set/fork read-failure paths and transient tool-finish accounting exit retain the same class (F1). Runtime interleaving coverage is bounded to attached tests; no dynamic attack performed here."
    }
  ],
  "free_hunt": [
    "Bounded static hunt: checked G1 identity, single production publisher, revision invalidation and permit ownership; no additional rework-induced regression established. Arbitrary thread-wide turn-start-lease interleavings remain dynamically unverified, as already noted in round 1.",
    "Checked test-only dependency edge, Bazel source module listing, core/app-server production-entry tests, and whitespace; size/dependency/lock notes remain nonblocking."
  ]
}
```
