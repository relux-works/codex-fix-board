# Merged review verdict — TASK-260929-2gp04j CR revision 3 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261005-2x4cdu_panel-verdict.md` (changes_requested), `TASK-261005-my1dv8_panel-verdict.md` (changes_requested), `TASK-261005-19i1t5_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

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
      "repeat-of": "CR-TASK-260929-2gp04j-2:external-accounting-read-failure-retains-capability",
      "reported_by": [
        "TASK-261005-2x4cdu"
      ]
    },
    {
      "id": "clear-returning-decode-retains-capability",
      "row": "goal activity publisher",
      "invariant": "AC5: committed clear removes the marker unconditionally. AC7: failed goal-state reads revoke the marker and record Unknown.",
      "mechanism": "codex-rs/ext/goal/src/api.rs:319-330 propagates delete_thread_goal Err at line 325 before clear_activity. The candidate codex-rs/state/src/runtime/goals.rs:472-496 executes DELETE ... RETURNING outside a transaction, then decodes the returned goal with thread_goal_from_row. A malformed updated_at_ms (the existing read-failure fixture) makes decoding fail AFTER the deletion commits. In Plan mode preparation short-circuits accounting, so a previously published Active marker survives this error although the committed goal is now absent. In Default mode a failing preparation only warns (api.rs:314-316); that arm also does not revoke. The sweep table rows 7 and 15 incorrectly infer that an Err means no committed clear occurred. Production caller: app-server/src/request_processors/thread_goal_processor.rs:289-294, GoalService::clear_thread_goal; report is specifically about the service entry, not an executed full JSON-RPC reproduction.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261005-my1dv8/static-witness.py",
          "command": "python3 .temp/TASK-261005-my1dv8/static-witness.py",
          "expected_failure": "Exit 1 observed (expected red). Pinned-source control-flow witness plus SQLite autocommit corroboration; NOT a Rust runtime test. It verifies DELETE returning conversion and UPDATE follow-up reads escape before publication."
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_activity_tests.rs (requested new regression: clear_returning_decode_failure_revokes_activity)",
          "command": "just test -p codex-core clear_returning_decode_failure_revokes_activity",
          "expected_failure": "NOT RUN / not yet authored. Reuse fixture/start_live_turn in Plan mode: seed Active, reconcile marker, corrupt updated_at_ms to i64::MAX, call service.clear_thread_goal, assert Err AND database get returns None AND marker None. Current candidate should fail marker assertion. Then turn-start recovers absence. Add a narrowing mutant preserving successful-clear removal while skipping error-path revocation."
        }
      ],
      "severity": "robustness",
      "repeat-of": "CR-TASK-260929-2gp04j-2/accounting-read-failure-retains-capability",
      "reported_by": [
        "TASK-261005-my1dv8"
      ]
    },
    {
      "id": "set-post-write-read-failure-retains-capability",
      "row": "goal activity publisher",
      "invariant": "AC3/4/7: external committed status changes reconcile the marker; every failed goal-state read removes it and records Unknown.",
      "mechanism": "codex-rs/ext/goal/src/api.rs:205-219 and :252-266 propagate update_thread_goal errors before reconcile_live_activity at :279. The candidate state/src/runtime/goals.rs:271-417 is not a pure write: it commits UPDATE, then calls get_thread_goal at :417 (and has a read-only branch at :400). A deterministic AFTER UPDATE trigger setting updated_at_ms=i64::MAX makes the pre-set read succeed, commits status Complete, then makes the follow-up read fail. With an already Active marker and Plan-mode accounting bypass, neither the new read_thread_goal_for_set wrapper nor the prepare-error revoke runs; the old marker remains after the goal has become Complete. Sweep row 14 inaccurately asserts committed state is unchanged on these errors. Production caller: app-server/src/request_processors/thread_goal_processor.rs:174-196 -> GoalService::set_thread_goal.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261005-my1dv8/static-witness.py",
          "command": "python3 .temp/TASK-261005-my1dv8/static-witness.py",
          "expected_failure": "Exit 1 observed (expected red). Pinned-source control-flow witness plus SQLite autocommit corroboration; NOT a Rust runtime test. It verifies DELETE returning conversion and UPDATE follow-up reads escape before publication."
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_activity_tests.rs (requested new regression: external_set_post_write_read_failure_revokes_activity)",
          "command": "just test -p codex-core external_set_post_write_read_failure_revokes_activity",
          "expected_failure": "NOT RUN / not yet authored. Reuse fixture/start_live_turn in Plan mode, seed/reconcile Active, install AFTER UPDATE trigger corrupting updated_at_ms, set status Complete through GoalService. Assert Err and marker None; current candidate should fail marker assertion. Drop trigger, repair timestamp, verify committed Complete and next lifecycle keeps marker absent. Exercise objective and status-only branches; narrowing mutant skips post-write-read error revocation while preserving pre-read revocation."
        }
      ],
      "severity": "robustness",
      "repeat-of": "CR-TASK-260929-2gp04j-2/accounting-read-failure-retains-capability",
      "reported_by": [
        "TASK-261005-my1dv8"
      ]
    },
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
      "repeat-of": "CR-TASK-260929-2gp04j-2/accounting-read-failure-retains-capability",
      "reported_by": [
        "TASK-261005-19i1t5"
      ]
    }
  ],
  "notes": [
    "[TASK-261005-2x4cdu] Exact replay passed; snapshot commit 622007038bd2422ab19b446331ad21733f93e693 independently resolves to candidate tree a8fc9e0cc6e0aad477aba7cd377e3c93203932fe. No builds, cargo, just, branch changes, commits, or original-task mutations.",
    "[TASK-261005-2x4cdu] Hosted precheck-6 is reused attached evidence: all four snapshot lanes success and 20/20 narrowing mutants reported killed. Local results JSON names failing goal tests for each mutant, although its killed booleans are false; failures/meaningful test names support the attached human summary. Individual hosted process exit codes were not supplied or independently fetched; no numeric exit code is inferred from a job conclusion.",
    "[TASK-261005-2x4cdu] Producer read-site sweep row 7 claims a delete failure leaves committed state and marker accurate. DELETE RETURNING followed by fallible row decoding disproves that premise; read-site row 15 has the same gap. These rows are producer context, not additional surface-table rows.",
    "[TASK-261005-2x4cdu] Request core regression clear_read_failure_revokes_activity_and_next_turn_recovers: use fixture/start_live_turn/record_live_usage, publish Active then corrupt updated_at_ms as existing external_set_get_failure test does; invoke GoalService::clear_thread_goal, assert Err and GoalActivity None. Reconcile next turn and assert marker absent when deletion committed. Add persistent read+delete failure case (rename goal table during live accounting), restore table and assert next-turn recovery with higher revision. Add narrowing mutant skipping revocation only for clear preparation/delete errors. These are requested, not executed tests.",
    "[TASK-261005-2x4cdu] Revision-3 set/fork/tool-finish repair paths are present and match their named hosted kills. The remaining clear path repeats the prior all-read-failures class; request focused rework on the existing implementation, no new research leaf.",
    "[TASK-261005-2x4cdu] Nonblocking size note: cumulative base-to-candidate change is 2207 insertions / 98 deletions across 22 files, including G1 prerequisite surfaces; stage upstream delivery. No new wire/config/CLI shape or history fragment observed; typed capability changes tool selection only. Bazel/dependency regeneration and target-platform runtime testing were not rerun by this panel.",
    "[TASK-261005-my1dv8] Exact replay matched a8fc9e0cc6e0aad477aba7cd377e3c93203932fe. No builds, Rust tests, source changes, commits, branch operations, or mutations on TASK-260929-2gp04j. All board writes target this panel task only.",
    "[TASK-261005-my1dv8] Pinned candidate API blob 2d9780400b43ad12dfeb4ea5e207ce966a249f7a; state goals blob ed616e16b7c81d06bcf02302912e16f71ad936f3. Existing timestamp fixture and state/model/thread_goal.rs TryFrom prove i64::MAX is a real decoding failure. SQLite witness corroborates statement commitment, not the full Rust behavior.",
    "[TASK-261005-my1dv8] Hosted snapshot 622007038bd2422ab19b446331ad21733f93e693 resolves locally to the exact replay tree. Run 37247519316 jobs independently read through gh API: lint/small/core/app-server all success. Downloaded small/core logs independently pin checkout and passing named tests. 20/20 narrowing kills are accepted from TASK-260929-2gp04j_results.md precheck-6 table and hosted-precheck-6.md, not rerun or independently audited per mutant by this panel.",
    "[TASK-261005-my1dv8] AC 8/8 has named production-entry driving/refusal tests in the producer map. That is mapping coverage, not exhaustive failure-path proof. The new set/prepare/fork/tool-finish tests repair the specific prior findings; they do not cover internal post-write reads or DELETE RETURNING decode failure.",
    "[TASK-261005-my1dv8] Logbook (task-scoped outcome, no control-root file edit): rev3 read-site sweep misclassifies fallible read-modify-return methods as pure writes; an error does not establish mutation rollback. Recommendation: account for GoalStore internals, route every service mutation error through sole-publisher revoke/reconcile, add the two named production regressions and narrowing mutants. This is ordinary rework, not an external blocker.",
    "[TASK-261005-my1dv8] Nonblocking carried context: cumulative CR is 2207 additions / 98 deletions (includes G1); upstream staging remains orchestrator-owned. No Bazel build/lock regeneration attested here. Test-only sqlx edge and same dependency pin remain producer evidence.",
    "[TASK-261005-my1dv8] Budget: one non-recording review decision, frozen candidate tree; grammar not applicable. Bounded 30-minute static sweep/free hunt, one text outcome under 30KiB, zero serial prerequisites. Exit is a swept verdict; consuming slice is recording-review aggregation and targeted G2 rework.",
    "[TASK-261005-19i1t5] Replay exact: base 729f259e62a8d11d9e17398e487790e1ee5d8b8c -> a8fc9e0cc6e0aad477aba7cd377e3c93203932fe. Snapshot 622007038bd2422ab19b446331ad21733f93e693 resolves to that same tree.",
    "[TASK-261005-19i1t5] All three round-2 finding records describe one class. Their named set-get branches, set preparation, fork preparation and tool-finish accounting error arm now revoke through the sole publisher. New tests cover both set branches, fork malformed reads, and tool-finish write-only fault after successful reconciliation. Exact repaired sites held; the class remains open in clear (F1).",
    "[TASK-261005-19i1t5] Hosted execution reused, not rerun or independently audited via GitHub: TASK-260929-2gp04j_hosted-precheck-6.md reports snapshot run 37247519316 success on all lanes and 20/20 narrowing mutants killed. These are executed attacks for the covered cases under the brief. No clear malformed-returned-row or clear-preparation refusal mutant exists among those 20; baseline green cannot prove this omitted error path.",
    "[TASK-261005-19i1t5] Tool-finish regression injects a write failure rather than a transient metrics read failure. The same Err arm unconditionally revokes for either source of error, verified statically; no separate dynamic transient-read execution claimed.",
    "[TASK-261005-19i1t5] No cargo, just, build, Rust test, branch mutation, commit or publication run here. Source task was read only; no notes/resources/status/accept/reject/handoff write on TASK-260929-2gp04j.",
    "[TASK-261005-19i1t5] Nonblocking inherited size note: cumulative CR 2305 changed lines (2207 additions/98 deletions) includes G1 and test-heavy rework; upstream staging remains orchestrator-owned. New sqlx edge is test-only; no independent Bazel execution or lock regeneration performed.",
    "[TASK-261005-19i1t5] Producer exclusion of pure API reads and deferral flags is a declared bound, not proof that every read failure revokes. F1 needs no expansion into those surfaces: clear is an explicitly required lifecycle mutation."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "1/1 rows swept, 8/8 AC families inspected. Hosted snapshot plus narrowing-mutant attacks support create/refusal, early-return turn start, six-status resume/set, terminal update/automatic stop/budget, disabled clear/stale callbacks, disable/re-enable/stop, read-failure/recovery, and v2 next-request tools. Static + SQL clear-error witness exposes an uncovered AC5/AC7 failure; this broken result is explicitly not a locally executed Rust public-entry reproduction.",
      "reported_by": "TASK-261005-2x4cdu"
    }
  ],
  "free_hunt": [
    "[TASK-261005-2x4cdu] Bounded static hunt of committed-delete versus returned-row decoding identified the second clear-error witness, merged in clear-error-retains-capability.",
    "[TASK-261005-2x4cdu] Single publisher, revision invalidation, permit lease ownership, dependency/build wiring, external API and model-context scope inspected. No additional reproduced mechanism; arbitrary concurrency schedules and Bazel execution remain unverified.",
    {
      "scope": "Bounded inspection of GoalStore mutation internals, feature teardown, permit ownership/reconciliation, sole-writer search, production service callers and spec-plan consumer.",
      "result": "Two same-class error-publication gaps reported above; no additional blocking issue established. No first-hit stop: all one surface row and all its attack families swept.",
      "bounds": "Static panel; no local cargo/just/build/test. Requested new Rust attacks are unexecuted. Full JSON-RPC fault-injection, Bazel and overlapping automatic/manual-turn lease races remain unmeasured, not claimed green.",
      "reported_by": "TASK-261005-my1dv8"
    },
    "[TASK-261005-19i1t5] Clear DELETE RETURNING decoding: broken; extended the same-class sweep into the GoalStore and found that fallible post-mutation decoding invalidates the producer assumption that a deletion Err preserves committed state. Included only once as F1.",
    "[TASK-261005-19i1t5] Publisher ownership and ordering: held statically; all production insert/remove GoalActivity calls in ext/goal are confined to activity.rs. Permit serializes mutations and revisions invalidate lifecycle changes. Arbitrary overtaking-turn/disable-re-enable schedules were not dynamically executed, so no universal concurrency proof claimed.",
    "[TASK-261005-19i1t5] API/context/dependency scope: no rework-added wire/config/CLI payload or model-context fragment found. Bazel declares activity.rs for integration compile data. Test-only dependency edges do not introduce a production library cycle. No additional blocking rework regression established."
  ]
}
```

## Recording reviewer attestation — RUN-261005-115389

The assigned recording reviewer read all three panel outcomes and verified exact retention of all 4 finding records (including every field and reproduction), 20 notes, all free-hunt entries, and the single distinct surface row (broken). All three panels request changes. No fresh review, finding, source modification, Rust test or hosted rerun was performed. Overlapping clear records remain panel records, not four independent mechanisms. The verdict remains changes_requested.

Completeness evidence: TASK-260929-2gp04j_recording-review-rev3.md, attached by this run. Initial reject_cr refused because the pre-existing merged resource had no launch-manifest digest; this attestation makes the evidence reviewer-authored without altering panel findings.
