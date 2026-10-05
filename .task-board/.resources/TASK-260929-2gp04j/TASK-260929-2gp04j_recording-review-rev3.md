# TASK-260929-2gp04j — goal-activity-publisher-hooks: recording review rev3

Verdict: changes_requested. Recording-only verification; no fresh code review, source changes, builds, or test reruns.

Run: RUN-261005-115389. spawn goal returned none (run not goal-bound).

Candidate: a8fc9e0cc6e0aad477aba7cd377e3c93203932fe; CR revision 3.

| Panel | Verdict | Finding records retained | Surface result | Notes retained |
| --- | --- | ---: | --- | ---: |
| TASK-261005-2x4cdu | changes_requested | 1 of 1 | goal activity publisher: broken | 6 of 6 |
| TASK-261005-my1dv8 | changes_requested | 2 of 2 | goal activity publisher: broken | 7 of 7 |
| TASK-261005-19i1t5 | changes_requested | 1 of 1 | goal activity publisher: broken | 7 of 7 |

Merge completeness: 4 of 4 panel finding records, 1 of 1 distinct surface rows, 20 of 20 notes, and all panel free-hunt entries retained. No findings were added, dropped, reclassified or independently re-attested by this recording run. The merged artifact preserves panel records separately; overlapping clear witnesses are not four independently established mechanisms.

Evidence boundary: panel attacks are explicitly static control-flow plus SQLite witnesses. Requested Rust regressions are unexecuted/unwritten; hosted results are reused panel inputs. This run checks faithful aggregation only, as mandated by recording-brief-rev3.md.

Canonical rejection evidence: TASK-260929-2gp04j_review-verdict-rev3.md. SHA256: ea5f0073c2291fb265d850e4b8e8f808634f46e04872c5a05a4d39f95f833c89.

Outcome-scoped logbook: all three panel verdicts request rework. Preserve clear preparation/delete-return decoding and external set post-write-read failures in the producer rework scope. Failed API returns must not be taken as proof that SQL rolled back.

Commands: initial reviewing mutation (exit 0); task-board readiness/help (exit 0); resource get for merged verdict and three panels (exit 0 each); spawn goal (exit 0, none); scoped reject_cr schema (exit 0); merge JSON field/note/surface/free-hunt verification (exit 0). Optional skill-location ls reported missing .claude path; the existing .codex skill was read. No validation result relies on that diagnostic.

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
          "expected_failure": "Exit 1 observed (expected red). Pinned-source control-flow witness plus SQLite autocommit corroboration; NOT a Rust runtime test. It verifies DELETE returning conversion and UPDATE follow-up reads escape before publication.",
          "pinned_blobs": [
            "codex-rs/ext/goal/src/api.rs 2d9780400b43ad12dfeb4ea5e207ce966a249f7a",
            "codex-rs/ext/goal/src/runtime.rs 2ca2a4f6db68a03380c279a223b02b0b0b9b1237",
            "codex-rs/state/src/runtime/goals.rs ed616e16b7c81d06bcf02302912e16f71ad936f3",
            "codex-rs/state/src/model/thread_goal.rs 12d2a78dac8990be14e2718d4427726c783916bc"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_activity_tests.rs (requested new regression: clear_returning_decode_failure_revokes_activity)",
          "command": "just test -p codex-core clear_returning_decode_failure_revokes_activity",
          "expected_failure": "NOT RUN / not yet authored. Reuse fixture/start_live_turn in Plan mode: seed Active, reconcile marker, corrupt updated_at_ms to i64::MAX, call service.clear_thread_goal, assert Err AND database get returns None AND marker None. Current candidate should fail marker assertion. Then turn-start recovers absence. Add a narrowing mutant preserving successful-clear removal while skipping error-path revocation.",
          "pinned_blobs": [
            "codex-rs/ext/goal/src/api.rs 2d9780400b43ad12dfeb4ea5e207ce966a249f7a",
            "codex-rs/ext/goal/src/runtime.rs 2ca2a4f6db68a03380c279a223b02b0b0b9b1237",
            "codex-rs/state/src/runtime/goals.rs ed616e16b7c81d06bcf02302912e16f71ad936f3",
            "codex-rs/state/src/model/thread_goal.rs 12d2a78dac8990be14e2718d4427726c783916bc"
          ]
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
          "expected_failure": "Exit 1 observed (expected red). Pinned-source control-flow witness plus SQLite autocommit corroboration; NOT a Rust runtime test. It verifies DELETE returning conversion and UPDATE follow-up reads escape before publication.",
          "pinned_blobs": [
            "codex-rs/ext/goal/src/api.rs 2d9780400b43ad12dfeb4ea5e207ce966a249f7a",
            "codex-rs/ext/goal/src/runtime.rs 2ca2a4f6db68a03380c279a223b02b0b0b9b1237",
            "codex-rs/state/src/runtime/goals.rs ed616e16b7c81d06bcf02302912e16f71ad936f3",
            "codex-rs/state/src/model/thread_goal.rs 12d2a78dac8990be14e2718d4427726c783916bc"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_activity_tests.rs (requested new regression: external_set_post_write_read_failure_revokes_activity)",
          "command": "just test -p codex-core external_set_post_write_read_failure_revokes_activity",
          "expected_failure": "NOT RUN / not yet authored. Reuse fixture/start_live_turn in Plan mode, seed/reconcile Active, install AFTER UPDATE trigger corrupting updated_at_ms, set status Complete through GoalService. Assert Err and marker None; current candidate should fail marker assertion. Drop trigger, repair timestamp, verify committed Complete and next lifecycle keeps marker absent. Exercise objective and status-only branches; narrowing mutant skips post-write-read error revocation while preserving pre-read revocation.",
          "pinned_blobs": [
            "codex-rs/ext/goal/src/api.rs 2d9780400b43ad12dfeb4ea5e207ce966a249f7a",
            "codex-rs/ext/goal/src/runtime.rs 2ca2a4f6db68a03380c279a223b02b0b0b9b1237",
            "codex-rs/state/src/runtime/goals.rs ed616e16b7c81d06bcf02302912e16f71ad936f3",
            "codex-rs/state/src/model/thread_goal.rs 12d2a78dac8990be14e2718d4427726c783916bc"
          ]
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
          "expected_failure": "Observed exit 1, expected-red static control-flow witness plus real SQLite execution of the pinned DELETE RETURNING SQL. SQLite confirms row count 0 before fallible caller decoding. This is NOT execution of the Rust production entry point.",
          "pinned_blobs": [
            "codex-rs/ext/goal/src/api.rs 2d9780400b43ad12dfeb4ea5e207ce966a249f7a",
            "codex-rs/ext/goal/src/runtime.rs 2ca2a4f6db68a03380c279a223b02b0b0b9b1237",
            "codex-rs/state/src/runtime/goals.rs ed616e16b7c81d06bcf02302912e16f71ad936f3",
            "codex-rs/state/src/model/thread_goal.rs 12d2a78dac8990be14e2718d4427726c783916bc"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_activity_tests.rs (requested new regression)",
          "command": "just test -p codex-core goal_activity::clear_decode_failure_revokes_activity_and_next_turn_recovers",
          "expected_failure": "NOT RUN and test not yet authored. Adapt external_set_get_failure fixture: publish Active, start a Plan turn, set updated_at_ms=i64::MAX, call service.clear_thread_goal, expect Err but GoalActivity None and raw SQL row count 0; next turn must remain absent. Current source retains Some. Also add pending-usage preparation failure plus a DELETE-refusal trigger variant; require Unknown/removal before returning. Add a narrowing mutant omitting clear-error revocation.",
          "pinned_blobs": [
            "codex-rs/ext/goal/src/api.rs 2d9780400b43ad12dfeb4ea5e207ce966a249f7a",
            "codex-rs/ext/goal/src/runtime.rs 2ca2a4f6db68a03380c279a223b02b0b0b9b1237",
            "codex-rs/state/src/runtime/goals.rs ed616e16b7c81d06bcf02302912e16f71ad936f3",
            "codex-rs/state/src/model/thread_goal.rs 12d2a78dac8990be14e2718d4427726c783916bc"
          ]
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
    "Recording receipt only; authoritative verdict remains TASK-260929-2gp04j_review-verdict-rev3.md"
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "1/1 rows swept, 8/8 AC families inspected. Hosted snapshot plus narrowing-mutant attacks support create/refusal, early-return turn start, six-status resume/set, terminal update/automatic stop/budget, disabled clear/stale callbacks, disable/re-enable/stop, read-failure/recovery, and v2 next-request tools. Static + SQL clear-error witness exposes an uncovered AC5/AC7 failure; this broken result is explicitly not a locally executed Rust public-entry reproduction.",
      "reported_by": "TASK-261005-2x4cdu"
    }
  ]
}
```

## Recording-route diagnostics

Canonical evidence was refused twice (exit 1): pre-existing artifact has no digest in launch manifest, even after recording attestation. New recording evidence was refused (exit 1): several panel reproduction objects lack pinned_blobs. Those objects now carry the exact API/runtime/state/model blob digests already supplied by panel A and corroborated in panel B notes for the same candidate tree. This adds evidence metadata only; no finding or reproduction is newly asserted or executed.
