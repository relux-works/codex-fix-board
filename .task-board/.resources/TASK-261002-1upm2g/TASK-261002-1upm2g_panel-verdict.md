# TASK-261002-1upm2g — R141 panel A, revision 2

changes_requested

Replay: base `ea8899e6f97aea64136159286840c28c955243e8` + resource `TASK-260929-2gp04j_change-request_rev2.patch` through a temporary index produced **exactly** `d401bcff58f9724a36966053dde5386be1af7882`. Expected tree matched. Review is static; no Rust build/test/mutant execution was performed here.

## Decision and bounds

This panel informs the recording review of CR-TASK-260929-2gp04j-2. Frozen input is the exact candidate tree and one-row surface table; no grammar work applies. Budget: one bounded static sweep plus caller/free hunt, at most 60 minutes, one verdict and one small witness, no archives and no serial prerequisite. Exit: replay recorded, every row assigned once, finding and evidence attached. Consumer: recording reviewer and owning G2 rework leaf. No delivery or acceptance on the reviewed task is authorized for this panel.

The stop/abort repairs are supported by exact-candidate hosted evidence. The same read-error class remains on fork-flush and tool-finish accounting paths. Recommendation: changes requested for AC 7; the source witness is a failing static check, not runtime proof.

## Commands and actual exit codes

Each gate below ran as a standalone process, without a pipe or tee. The index variable was `$PWD/.temp/TASK-261002-1upm2g-replay.idx`.

| Command | Exit | Result |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261002-1upm2g, status=analysis)'` | 0 | Panel lifecycle only |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev2.patch --output .temp/TASK-260929-2gp04j_change-request_rev2.patch` | 0 | Read-only patch download |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-1upm2g-replay.idx" git read-tree ea8899e6f97aea64136159286840c28c955243e8` | 0 | Base loaded |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-1upm2g-replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev2.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-1upm2g-replay.idx" git write-tree` | 0 | Exact expected candidate tree |
| `git diff --exit-code 58042581a0b507ae62e7b1d8381c429baea1f689 d401bcff58f9724a36966053dde5386be1af7882 -- codex-rs/core/src/tools/spec_plan.rs codex-rs/ext/extension-api codex-rs/core/tests/suite/current_time_reminder.rs` | 0 | G1 unchanged |
| `git diff --check ea8899e6f97aea64136159286840c28c955243e8 d401bcff58f9724a36966053dde5386be1af7882` | 0 | No patch whitespace errors |
| `gh api repos/relux-works/codex/actions/runs/37014493254 --jq '{id,conclusion,status,head_sha,html_url}'` | 0 | Hosted baseline success |
| `gh api repos/relux-works/codex/actions/runs/37014493254/jobs --jq '.jobs[] | {name,conclusion}'` | 0 | core/app-server/lint/small all success |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/110861926465/logs > .temp/TASK-261002-1upm2g/hosted-small.log` | 0 | Pinned snapshot checkout and PASS for two new regressions |
| `python3 .temp/TASK-261002-1upm2g/TASK-261002-1upm2g_static-witness.py` | **1** | Expected-red static error-path witness: uncaught read errors bypass publication |

Readiness: task-board status command 0, git 2.54.0, rg readiness 0, Python 3.14.7 and gh 2.97.0 readiness 0; logs stored in panel `.temp/`. Inspection commands (git show/diff/grep, compact board reads, source/resource reads) succeeded after bounded syntax/path recovery. Initial board query including unsupported `resources` returned 1; initial reviewer-role path read failed (file not installed under skill symlink, combined read/query call 1); role read recovered from `/Users/iv/.curator/sources/project-management/.roles/reviewer/role.md`. The first `gh api .../logs` returned 1 because gh refused terminal escapes; explicit allowed-output download returned 0. These are operational read failures, not green gates or product defects.

## Attack sweep (one surface row, all its families)

| Family / AC | Static attack and evidence | Result |
| --- | --- | --- |
| Create success/refusal, AC 1 | Tool holds mutation permit and reconciles before returning; core tests assert second sampling request gains sleep only for success. Forged-name finish test reconciles committed DB state. | held |
| Turn-start early returns, AC 2 | Reconcile precedes missing-baseline and Plan returns; missing-baseline/Plan/no-goal tests inspect resulting requests. | held |
| Resume/external set, AC 3 | Active/BudgetLimited publish, four other statuses remove; six-case core test separately removes marker before runtime effects/resume to force each path. | held |
| Update/automatic stop/budget, AC 4 | Tool update post-outcome reconciliation; stop mutation reconciliation; BudgetLimited marker retained without new automatic turn. Read-error bypass is separately AC 7. | held |
| Disabled clear and stale callbacks, AC 5 | Clear publisher is unconditional; delayed effects re-read committed state, guarded publication invalidates old reads; core latch test and stale revision test cover refusal. | held |
| Stop/disable/re-enable, AC 6 | Synchronous removal plus accounting/options/lease cleanup; re-enable invalidates rather than reuses marker and reconciles on next event. Hook tests drive production config contributor directly. | held within stated dynamic-config bound |
| Read failure/recovery, AC 7 | Reconcile failures remove/Unknown; four new stop/abort calls repair original paths. Fork flush and later tool-finish accounting read failures bypass publisher. | **broken** |
| App-server sampling, AC 8 | v2 created/refused cases inspect all three requests: `[false, success, false]`, plus create result status. | held |
| Duplicate/out-of-order publisher events | Duplicate committed snapshot keeps revision; clear, failure, disable/re-enable, stop invalidate stale reads. | held statically and by reused publisher test evidence |

These family rows are supporting detail; the JSON assigns exactly one result to the single authoritative surface-table row.

## Sources and evidence provenance

All implementation citations refer to immutable tree `d401bcff58f9724a36966053dde5386be1af7882`, read with `git show TREE:path`. Source blobs are pinned in the finding. Primary board sources (read only): `surface-table.md`, task AC projection, `producer-brief.md`, `TASK-260929-2gp04j_results.md`, `TASK-260929-2gp04j_review-verdict-rev1.md`, and `TASK-260929-2gp04j_hosted-precheck-3.md`. [Hosted baseline](https://github.com/relux-works/codex/actions/runs/37014493254) was independently queried; exact snapshot checkout was checked in the small-lane log. Snapshot `10bc26b11571a85b738ba8a84569fc33f56ffc1f^{tree}` equals replay candidate. Fifteen mutant kills are accepted from the attached precheck evidence; no panel runtime execution claimed.

## Outcome-scoped logbook

- Replay exact; no reviewed-task mutations or source changes.
- Round-1 error class persists outside the four newly repaired callback exits. Fork flush gives a persistent-failure control-flow witness; tool-finish gives a transient-after-success witness. Repeated finding is explicitly linked to revision 1.
- Hosted baseline is green and candidate-pinned; its green status and 15 selected mutant kills do not establish the absent error-path coverage.

```verdict-findings
{
  "findings": [
    {
      "id": "accounting-read-failure-retains-capability",
      "row": "goal activity publisher",
      "invariant": "Every goal-store read failure removes GoalActivity, records reconciliation Unknown, reports the error, and retries at the next legitimate lifecycle event (AC 7). A failed read is not an absence or continued proof of Active state.",
      "mechanism": "The rev-2 fix covers four turn-stop/abort exits, but runtime.rs:671-673 and :735-737 still propagate current_goal_status_for_metrics read failures before publication; :790-796 performs the actual fallible get_thread_goal. Production app-server fork at thread_processor.rs:5246-5252 calls thread_goal_processor.rs:116-123 -> GoalService::flush_thread_goal_progress_for_fork (api.rs:114-130) -> prepare_external_goal_mutation_locked (runtime.rs:254-283) -> accounting. That error propagates to the fork response without any reconciliation/removal of the source thread marker. With an already Active marker and unaccounted token/time delta, a persistent malformed-row failure is sufficient. Separately, on_tool_finish first reconciles at extension.rs:501-513, but its later accounting Err arm at :555-559 only warns/returns, bypassing :562-573. A read failure after the first successful read leaves the Known marker intact. Earlier success does not certify a later failed read.",
      "reproductions": [
        {
          "test_file": "TASK-261002-1upm2g_static-witness.py",
          "command": "python3 .temp/TASK-261002-1upm2g/TASK-261002-1upm2g_static-witness.py",
          "expected_failure": "Exit 1 (observed): expected-red immutable-source control-flow witness verifies both uncaught error chains. Static only, not a dynamic Rust reproduction. Runtime scenario for fork: seed Active, start a default turn, record nonzero usage, corrupt updated_at_ms as in the existing real-GoalStore tests, invoke flush_thread_goal_progress_for_fork, assert Err plus GoalActivity None; source instead propagates Err and leaves Some. Runtime scenario for tool finish needs a bounded fault/latch between its successful leading reconcile and metrics read; not executed by this no-build panel.",
          "pinned_blobs": [
            "git-blob:87849af544305d6d8897a382e62a746d9f6d4e8e",
            "git-blob:153d947f523890868dac9554c9a84393800f4869",
            "git-blob:a4512db548378bcdf499cd47eca670d366a8f9a3"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "CR-TASK-260929-2gp04j-1/accounting-read-failure-retains-capability"
    }
  ],
  "notes": [
    "Exact replay tree d401bcff58f9724a36966053dde5386be1af7882. No source edits, builds, tests, commits, branch changes, or mutations on TASK-260929-2gp04j.",
    "G1 paths byte-identical to checkpoint 58042581a0b507ae62e7b1d8381c429baea1f689: spec_plan.rs, ext/extension-api subtree, current_time_reminder.rs. Standalone diff --exit-code returned 0.",
    "Round-1 stop/abort finding repaired at the four inspected error exits; the attached 15/15 mutant kill evidence covers those fixes but has no fork-flush or after-leading-reconcile tool-finish read-failure mutant. Persistent-read-only coverage cannot establish AC 7 for all error exits.",
    "Hosted baseline independently checked through gh API: all four lanes success. Run metadata head_sha is dispatch base ea8899e6, not candidate; fetched small job log pins checkout 10bc26b11571a85b738ba8a84569fc33f56ffc1f, whose local tree equals candidate, and explicitly shows PASS for both new stop/abort tests. All 15 mutant kills are reused attached precheck-3 evidence, not rerun or independently audited run-by-run by this panel.",
    "Producer results explicitly exclude the on_tool_finish error interval as transient and untested. AC 7 has no persistent-only exception; inability to test without fault injection does not make a fallible read infallible.",
    "Nonblocking retained review notes: G2 delta 1526 changed lines and cumulative CR 1821 changed lines exceed size guidance; upstream staging remains required per orchestrator. Core dev-dependency on goal creates a test-only package cycle, not a production library cycle. No Bazel execution or independent lock regeneration here; earlier producer lock evidence reused.",
    "Recommendation: ensure accounting read-error propagation reaches the existing sole publisher for every caller, including fork-flush and tool-finish. Add named regressions through those production entries with recovery assertions and narrowing mutants; do not add a persistent-only exception or source-text gate. Recording reviewer/orchestrator owns rework routing, including repeat-of handling."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "1/1 surface-table rows swept; all listed transition/attack families inspected. Create, turn-start early returns, six-status resume/set, update/stop/budget, disabled clear/late callback, disable/re-enable/stop, duplicate/stale publisher revisions and v2 sampling flows have supporting source/test evidence. Read-error accounting paths remain broken under the same prior finding class; see finding accounting-read-failure-retains-capability."
    }
  ],
  "free_hunt": [
    {
      "topic": "Fork progress flush error propagation",
      "result": "broken",
      "detail": "Bounded caller search found a production fork entry with no preceding reconcile and no revocation on propagated accounting read error; included in the single finding, not duplicated."
    },
    {
      "topic": "Permit lease and lifecycle races",
      "result": "not-attacked",
      "detail": "Reviewed lease ownership/drop and revision invalidation statically; user-turn overtaking and disable/re-enable interleavings were not dynamically scheduled in this no-build panel. No additional defect claimed."
    },
    {
      "topic": "Dependency/API/context scope",
      "result": "held",
      "detail": "G1 unchanged, no new wire/config/CLI types or model-context fragment; inspected dev dependencies and Bazel source glob wiring. This is a static scope result, not an independent Bazel validation."
    }
  ]
}
```

Artifact verification: inline Python JSON/schema/cardinality check exited **0**: exactly 1 verdict-findings block, 1/1 surface rows, valid required finding/reproduction fields, one-word verdict, and snapshot tree equal to candidate. No runtime behavior inferred from this format check.
