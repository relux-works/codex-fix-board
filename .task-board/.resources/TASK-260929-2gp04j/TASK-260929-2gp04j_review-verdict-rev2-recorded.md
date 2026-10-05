# Merged review verdict — TASK-260929-2gp04j CR revision 2 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261002-1upm2g_panel-verdict.md` (changes_requested), `TASK-261002-1abmbj_panel-verdict.md` (changes_requested), `TASK-261002-3b2b07_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

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
      "repeat-of": "CR-TASK-260929-2gp04j-1/accounting-read-failure-retains-capability",
      "reported_by": [
        "TASK-261002-1upm2g"
      ]
    },
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
      "repeat-of": "CR-TASK-260929-2gp04j-1:accounting-read-failure-retains-capability",
      "reported_by": [
        "TASK-261002-1abmbj"
      ]
    },
    {
      "id": "external-accounting-read-failure-retains-capability",
      "row": "goal activity publisher",
      "invariant": "Every goal-store read failure must revoke GoalActivity, record reconciliation Unknown, report the error, and allow the next legitimate lifecycle event to retry.",
      "mechanism": "The original four turn-stop/abort exits now revoke, but the same class remains in GoalService::set_thread_goal (api.rs:188-202,244-248): prepare_external_goal_mutation_locked errors only warn, then get_thread_goal propagates a persistent read failure with ? before reconcile_live_activity at :283. A previously published Active/BudgetLimited marker survives. GoalService::flush_thread_goal_progress_for_fork (:114-129) directly propagates the same preparation/accounting read error without reconciliation. runtime.rs:671-673 and :735-737 call current_goal_status_for_metrics; :790-797 propagates get_thread_goal failure before publication at :687/:751. The on_tool_finish accounting Err branch (extension.rs:555-560) also returns without revocation after its earlier reconcile, leaving a transient-failure window.",
      "reproductions": [
        {
          "test_file": "TASK-261002-3b2b07_static-witness.py",
          "command": "python3 .temp/TASK-261002-3b2b07/TASK-261002-3b2b07_static-witness.py",
          "expected_failure": "Exit 1 (observed): pinned-source control-flow witness verifies set/fork goal-read error propagation before Unknown/removal, plus the tool-finish post-reconcile accounting error exit. Static witness only; no dynamic Rust reproduction was run. Suggested production regression: publish Active on a registered live runtime, start a turn and record a token delta, corrupt updated_at_ms using the existing read-failure fixture, call GoalService::set_thread_goal or flush_thread_goal_progress_for_fork, then assert GoalActivity None and recovery on the next turn start; current control flow retains Some.",
          "pinned_blobs": [
            "git-blob:a4512db548378bcdf499cd47eca670d366a8f9a3",
            "git-blob:87849af544305d6d8897a382e62a746d9f6d4e8e",
            "git-blob:153d947f523890868dac9554c9a84393800f4869"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "accounting-read-failure-retains-capability",
      "reported_by": [
        "TASK-261002-3b2b07"
      ]
    }
  ],
  "notes": [
    "[TASK-261002-1upm2g] Exact replay tree d401bcff58f9724a36966053dde5386be1af7882. No source edits, builds, tests, commits, branch changes, or mutations on TASK-260929-2gp04j.",
    "[TASK-261002-1upm2g] G1 paths byte-identical to checkpoint 58042581a0b507ae62e7b1d8381c429baea1f689: spec_plan.rs, ext/extension-api subtree, current_time_reminder.rs. Standalone diff --exit-code returned 0.",
    "[TASK-261002-1upm2g] Round-1 stop/abort finding repaired at the four inspected error exits; the attached 15/15 mutant kill evidence covers those fixes but has no fork-flush or after-leading-reconcile tool-finish read-failure mutant. Persistent-read-only coverage cannot establish AC 7 for all error exits.",
    "[TASK-261002-1upm2g] Hosted baseline independently checked through gh API: all four lanes success. Run metadata head_sha is dispatch base ea8899e6, not candidate; fetched small job log pins checkout 10bc26b11571a85b738ba8a84569fc33f56ffc1f, whose local tree equals candidate, and explicitly shows PASS for both new stop/abort tests. All 15 mutant kills are reused attached precheck-3 evidence, not rerun or independently audited run-by-run by this panel.",
    "[TASK-261002-1upm2g] Producer results explicitly exclude the on_tool_finish error interval as transient and untested. AC 7 has no persistent-only exception; inability to test without fault injection does not make a fallible read infallible.",
    "[TASK-261002-1upm2g] Nonblocking retained review notes: G2 delta 1526 changed lines and cumulative CR 1821 changed lines exceed size guidance; upstream staging remains required per orchestrator. Core dev-dependency on goal creates a test-only package cycle, not a production library cycle. No Bazel execution or independent lock regeneration here; earlier producer lock evidence reused.",
    "[TASK-261002-1upm2g] Recommendation: ensure accounting read-error propagation reaches the existing sole publisher for every caller, including fork-flush and tool-finish. Add named regressions through those production entries with recovery assertions and narrowing mutants; do not add a persistent-only exception or source-text gate. Recording reviewer/orchestrator owns rework routing, including repeat-of handling.",
    "[TASK-261002-1abmbj] No builds/tests run. Hosted precheck-3 outcome reports all four lanes green on run 37014493254 and 15/15 intended narrowing-mutant kills; these are reused attached evidence, not independently executed here. Snapshot commit 10bc26b tree was independently resolved and matches candidate d401bcff exactly.",
    "[TASK-261002-1abmbj] Producer results map 8/8 AC rows to tests. Those tests and 15 mutants do not establish coverage of external-set error exits or the tool-finish second-read window. The stated untestable transient bound is not a contractual exclusion from AC7; external-set is a persistent-failure witness and avoids that bound.",
    "[TASK-261002-1abmbj] G1 spec_plan, extension-api subtree and current_time_reminder tests are unchanged against checkpoint 58042581 (diff exit 0). All G2 changed source files and test entry points inspected; exactly one surface-table row exists.",
    "[TASK-261002-1abmbj] Keep nonblocking round-1 context: oversized diff requires upstream staging by orchestrator; core test-only dev-dependency cycle is not a production library cycle; Bazel activity.rs compile data is declared. Lock refresh/no-delta is producer evidence, not Bazel verification by this panel.",
    "[TASK-261002-1abmbj] Automatic-start shared permit lease has no turn identity. Overtaking turn or disable/re-enable races were inspected but not dynamically reproduced; no additional blocking finding claimed.",
    "[TASK-261002-3b2b07] The previous merged finding is repaired at the specifically named turn-stop/abort exits: all four call revoke_activity_on_read_failure; publisher error branch sets Unknown, increments revision, removes GoalActivity, and reports the error. New stop/abort tests use a real malformed GoalStore row and assert removal/recovery. Same-class coverage is still incomplete (F1).",
    "[TASK-261002-3b2b07] Hosted execution is reused attached evidence, not independently rerun or remotely re-attested: TASK-260929-2gp04j_hosted-precheck-3.md identifies tree d401bcff58f9724a36966053dde5386be1af7882, snapshot 10bc26b11571a85b738ba8a84569fc33f56ffc1f, run 37014493254 green lint/small/core/app-server, and 15/15 intended mutant kills. These kills do not cover external set/fork persistent read failures or the tool-finish transient window.",
    "[TASK-261002-3b2b07] G1 paths are byte-identical to checkpoint 58042581a0b507ae62e7b1d8381c429baea1f689. Replay and static checks were run here; no cargo/just/build/test or mutant execution was run.",
    "[TASK-261002-3b2b07] Producer results claim external set preparation failures subsequently reconcile on persistent failure. The early get_thread_goal ? paths contradict that claim. The stated tool-finish transient bound is explicit but does not satisfy the unconditional read-failure invariant.",
    "[TASK-261002-3b2b07] Nonblocking round-1 context retained: G2 is 1526 changed lines (1450 insertions / 76 deletions); stage upstream delivery. Core->goal test-only dev edge is not a normal-library cycle. Bazel lock no-delta refresh is producer evidence, not independently verified by this panel.",
    "[TASK-261002-3b2b07] No mutations, resources, status changes, accept/reject or handoff were made on TASK-260929-2gp04j. Only this panel task receives outcome resources and lifecycle writes.",
    "[TASK-261002-3b2b07] Installed project-management reviewer-role reference was missing. Explicit panel review-round instructions were followed; no source workflow was modified."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "1/1 surface-table rows swept; all listed transition/attack families inspected. Create, turn-start early returns, six-status resume/set, update/stop/budget, disabled clear/late callback, disable/re-enable/stop, duplicate/stale publisher revisions and v2 sampling flows have supporting source/test evidence. Read-error accounting paths remain broken under the same prior finding class; see finding accounting-read-failure-retains-capability.",
      "reported_by": "TASK-261002-1upm2g"
    }
  ],
  "free_hunt": [
    "{\"topic\": \"Fork progress flush error propagation\", \"result\": \"broken\", \"detail\": \"Bounded caller search found a production fork entry with no preceding reconcile and no revocation on propagated accounting read error; included in the single finding, not duplicated.\", \"reported_by\": \"TASK-261002-1upm2g\"}",
    "{\"topic\": \"Permit lease and lifecycle races\", \"result\": \"not-attacked\", \"detail\": \"Reviewed lease ownership/drop and revision invalidation statically; user-turn overtaking and disable/re-enable interleavings were not dynamically scheduled in this no-build panel. No additional defect claimed.\", \"reported_by\": \"TASK-261002-1upm2g\"}",
    "{\"topic\": \"Dependency/API/context scope\", \"result\": \"held\", \"detail\": \"G1 unchanged, no new wire/config/CLI types or model-context fragment; inspected dev dependencies and Bazel source glob wiring. This is a static scope result, not an independent Bazel validation.\", \"reported_by\": \"TASK-261002-1upm2g\"}",
    "{\"area\": \"G1 identity, package dependencies and build-data declarations, shared permit lease\", \"result\": \"No additional blocking reproduction. G1 identity and diff checks green; no Bazel execution or dynamic concurrency proof.\", \"reported_by\": \"TASK-261002-1abmbj\"}",
    "[TASK-261002-3b2b07] Bounded static hunt: checked G1 identity, single production publisher, revision invalidation and permit ownership; no additional rework-induced regression established. Arbitrary thread-wide turn-start-lease interleavings remain dynamically unverified, as already noted in round 1.",
    "[TASK-261002-3b2b07] Checked test-only dependency edge, Bazel source module listing, core/app-server production-entry tests, and whitespace; size/dependency/lock notes remain nonblocking."
  ]
}
```

## Recording reviewer attestation — RUN-261002-a1da59

Read all three named panel outcomes. All three verdicts are changes_requested. Verified that 3/3 panel finding records and every panel note are preserved verbatim; 1/1 unique surface rows remains broken, the worst panel result. No fresh code review, builds, runtime tests or findings were added. Panel evidence remains explicitly static, with hosted evidence reused only within its stated bounds. Normalized free_hunt object entries to JSON strings solely to satisfy the installed verdict schema, preserving all content. The supplied union retains overlapping panel records rather than inventing or silently dropping findings. The prior read-failure class repeats; rework must add named production-entry regressions and narrowing mutants for external set, fork flush, and tool-finish accounting.

Initial dry-run rejected pre-existing evidence without reviewer ownership. This attestation updates the resource through the board CLI. Full merge check and outcome-scoped logbook: TASK-260929-2gp04j_recording-review-rev2.md.

Recording schema repair: the third panel omitted pinned_blobs. Added exact candidate api/runtime/extension blob IDs resolved by git rev-parse, which match the other panels. No reproduction claim or finding changed. Board refused original resource ownership after update; recording uses this newly created reviewer-owned resource.
