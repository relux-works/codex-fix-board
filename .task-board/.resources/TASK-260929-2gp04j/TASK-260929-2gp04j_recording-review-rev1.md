# Recording review confirmation — TASK-260929-2gp04j goal-activity-publisher-hooks, revision 1

Recording verdict: changes_requested. The named merged verdict resource remains authoritative for reject_cr.

Read both panel outcomes and the merged outcome. Automated merge comparison passed (merge-check-01.log, exit 0): 1/1 blocking findings preserved field-for-field, 11/11 structured notes preserved with panel attribution, 1/1 surface rows preserved with the worst result broken, and empty free-hunt lists retained. Panel A recommends changes_requested; panel B recommends accept. The union therefore requires rework.

The finding remains explicitly bounded to panel A's immutable-source control-flow witness, not a dynamic Rust reproduction. No builds, tests, mutants or new source review were run by this recording reviewer. No code modified. The run is not goal-bound (spawn goal returned none).

Outcome-scoped logbook: 2026-10-02 — merged verdict verified complete; route revision 1 to rework using the attached merged verdict. Require the named accounting/abort read-failure lifecycle regression and narrowing mutant requested by panel A; no additional findings introduced.

## Preserved merged verdict

# Merged review verdict — TASK-260929-2gp04j CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261002-36s1fj_panel-verdict.md` (changes_requested), `TASK-261002-3k97mc_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "accounting-read-failure-retains-capability",
      "row": "goal activity publisher",
      "invariant": "A goal-store read failure removes GoalActivity, records reconciliation Unknown, and is retried by the next legitimate lifecycle event.",
      "mechanism": "codex-rs/ext/goal/src/runtime.rs:660-676 propagates the metrics goal read error before publication; current_goal_status_for_metrics at :783-785 propagates get_thread_goal errors, and ext/goal/src/extension.rs:405-417 logs/returns on abort without revoking the previously Known marker.",
      "reproductions": [
        {
          "test_file": "TASK-261002-36s1fj_static-witness.py",
          "command": "python3 .temp/TASK-261002-36s1fj/TASK-261002-36s1fj_static-witness.py",
          "expected_failure": "Exit 1: immutable-source control-flow witness finds an actual get_thread_goal error propagation path from on_turn_abort that bypasses the sole publisher's Unknown/removal branch. Static witness only; dynamic Rust regression not run because builds/tests are prohibited for this panel.",
          "pinned_blobs": [
            "git-blob:625003a79fbdd9bb54f9287d1b800e2162636097",
            "git-blob:b3070a3a4ad155a6a0525980adec4042648c91f5"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261002-36s1fj"
      ]
    }
  ],
  "notes": [
    "[TASK-261002-36s1fj] No builds/tests or mutant executions were rerun by this panel; expected-red static witness exit 1 is not presented as a passing runtime gate.",
    "[TASK-261002-36s1fj] Hosted baseline success was independently checked; 13/13 mutant kills are reused attached evidence and do not cover accounting/abort read-failure narrowing.",
    "[TASK-261002-36s1fj] G2 is 1385 changed lines; inactive ~225-line foundation is the smallest proposed coherent stage, but the remaining ~1160-line stage still exceeds the 800-line guidance.",
    "[TASK-261002-36s1fj] The test-only core->goal->core graph is not a production dependency cycle. Lock refresh was required and producer evidence says it ran with no lock delta; no Bazel build was executed here.",
    "[TASK-261002-36s1fj] Re-enable and mid-turn disable coverage exercises production extension hooks directly; no production session path dynamically flips Goals via refresh_runtime_config today.",
    "[TASK-261002-3k97mc] {'id': 'oversize-delivery-staging', 'severity': 'note', 'text': 'Cumulative CR is 1680 changed lines; G2 is 1385. Proposed ~225-line first stage leaves ~1160 lines. Keep G1 separate and stage hook groups with their tests for upstream delivery.'}",
    "[TASK-261002-3k97mc] {'id': 'dev-cycle-target-bound', 'severity': 'note', 'text': 'Core dev-dep on goal and goal normal-dep on core forms a package-level dev cycle, not a normal core-library cycle. Exact-tree hosted compilation passed.'}",
    "[TASK-261002-3k97mc] {'id': 'bazel-lock-evidence-bound', 'severity': 'note', 'text': 'Producer reports just bazel-lock-update exit 0 with no delta. Panel did not run Bazel; Cargo-only hosted success cannot prove Bazel lock freshness.'}",
    "[TASK-261002-3k97mc] {'id': 'accounting-read-error-window', 'severity': 'note', 'text': 'runtime.rs:775 may return a read failure before publisher reconciliation in progress-accounting paths. Not reproduced through a permitted public-entry test; investigate transient failure after the preceding successful reconcile.'}",
    "[TASK-261002-3k97mc] {'id': 'unbound-turn-start-lease', 'severity': 'note', 'text': 'runtime.rs:570 and extension.rs:254 share a thread-wide permit lease without submission identity. Overtaking user turn and disable/re-enable interleavings were not dynamically attacked here.'}",
    "[TASK-261002-3k97mc] {'id': 'execution-provenance', 'severity': 'note', 'text': 'Panel independently ran replay and static checks only; public-entry executions and mutation failures are reused hosted evidence. Workflow dispatch head is not the tested checkout; logs pin checkout 016a4248 and tree 4d289590.'}"
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "All seven transition families inspected; accounting goal-read errors bypass Unknown/removal on abort and turn-stop error exits (F1).",
      "reported_by": "TASK-261002-36s1fj"
    }
  ],
  "free_hunt": []
}
```
