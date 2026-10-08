# TASK-261005-my1dv8 panel B — CR-TASK-260929-2gp04j-3

changes_requested

Replay: base `729f259e62a8d11d9e17398e487790e1ee5d8b8c` plus rev3 patch through a temporary index produced `a8fc9e0cc6e0aad477aba7cd377e3c93203932fe`, exactly the expected candidate tree.

Commands run by this panel (real exits):

| Command | Exit | Evidence |
|---|---:|---|
| `task-board m 'set_status(TASK-261005-my1dv8, status=analysis)'` | 0 | own task only |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev3.patch --output .temp/TASK-260929-2gp04j_change-request_rev3.patch` | 0 | read-only resource |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-my1dv8-replay.idx" git read-tree 729f259e62a8d11d9e17398e487790e1ee5d8b8c` | 0 | replay base |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-my1dv8-replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev3.patch` | 0 | replay patch |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-my1dv8-replay.idx" git write-tree` | 0 | exact candidate match |
| `git rev-parse '622007038bd2422ab19b446331ad21733f93e693^{tree}'` | 0 | hosted snapshot tree equals candidate |
| `git diff --check 729f259e62a8d11d9e17398e487790e1ee5d8b8c a8fc9e0cc6e0aad477aba7cd377e3c93203932fe` | 0 | patch whitespace check only |
| `gh api repos/relux-works/codex/actions/runs/37247519316/jobs --jq '.jobs[] | {id,name,conclusion}'` | 0 | all four hosted lanes success |
| `gh api repos/relux-works/codex/actions/jobs/111568238431/logs` | 1 | refused terminal escapes; no evidence inferred from this failure |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/111568238431/logs` and equivalent job `111568238578` | 0 each | small/core logs in panel scratch; exact checkout and PASS names verified |
| `python3 .temp/TASK-261005-my1dv8/static-witness.py` | 1 | EXPECTED RED: two pinned-source bypasses; SQLite corroboration only, no Rust execution |
| `git status --short` | 0 | empty tracked/untracked source delta (scratch ignored) |

Outcome-format validation: standalone Python JSON/fence/row/required-field check exited 0; exactly one valid block, 1/1 row once, two findings, one-word verdict, under the 30KiB artifact bound.

No builds or Rust tests run. No accept/reject/status/handoff or other write on the reviewed task. Early diagnostic query with unsupported `resources` field exited 1 and was repaired with a compact `description scope ac` read. Missing reviewer-role path and obsolete app-server path probes were diagnostic failures, repaired by reading the source skill and relocated request processor; no validation claim relies on them.

Sources: candidate blobs above; `surface-table.md`, `producer-brief.md`, prior rev2 verdict and `TASK-260929-2gp04j_results.md` on the reviewed task; [exact-tree hosted run](https://github.com/relux-works/codex/actions/runs/37247519316). All 20 mutant run IDs remain in the cited precheck-6 result table (37247532651–37247852091). Outcome is non-recording and ready for review aggregation.

```verdict-findings
{
  "findings": [
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
      "repeat-of": "CR-TASK-260929-2gp04j-2/accounting-read-failure-retains-capability"
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
      "repeat-of": "CR-TASK-260929-2gp04j-2/accounting-read-failure-retains-capability"
    }
  ],
  "notes": [
    "Exact replay matched a8fc9e0cc6e0aad477aba7cd377e3c93203932fe. No builds, Rust tests, source changes, commits, branch operations, or mutations on TASK-260929-2gp04j. All board writes target this panel task only.",
    "Pinned candidate API blob 2d9780400b43ad12dfeb4ea5e207ce966a249f7a; state goals blob ed616e16b7c81d06bcf02302912e16f71ad936f3. Existing timestamp fixture and state/model/thread_goal.rs TryFrom prove i64::MAX is a real decoding failure. SQLite witness corroborates statement commitment, not the full Rust behavior.",
    "Hosted snapshot 622007038bd2422ab19b446331ad21733f93e693 resolves locally to the exact replay tree. Run 37247519316 jobs independently read through gh API: lint/small/core/app-server all success. Downloaded small/core logs independently pin checkout and passing named tests. 20/20 narrowing kills are accepted from TASK-260929-2gp04j_results.md precheck-6 table and hosted-precheck-6.md, not rerun or independently audited per mutant by this panel.",
    "AC 8/8 has named production-entry driving/refusal tests in the producer map. That is mapping coverage, not exhaustive failure-path proof. The new set/prepare/fork/tool-finish tests repair the specific prior findings; they do not cover internal post-write reads or DELETE RETURNING decode failure.",
    "Logbook (task-scoped outcome, no control-root file edit): rev3 read-site sweep misclassifies fallible read-modify-return methods as pure writes; an error does not establish mutation rollback. Recommendation: account for GoalStore internals, route every service mutation error through sole-publisher revoke/reconcile, add the two named production regressions and narrowing mutants. This is ordinary rework, not an external blocker.",
    "Nonblocking carried context: cumulative CR is 2207 additions / 98 deletions (includes G1); upstream staging remains orchestrator-owned. No Bazel build/lock regeneration attested here. Test-only sqlx edge and same dependency pin remain producer evidence.",
    "Budget: one non-recording review decision, frozen candidate tree; grammar not applicable. Bounded 30-minute static sweep/free hunt, one text outcome under 30KiB, zero serial prerequisites. Exit is a swept verdict; consuming slice is recording-review aggregation and targeted G2 rework."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "reason": "Swept all attack families. Hosted exact-tree evidence holds normal create/refusal, early-return turn start, all resume/set statuses, terminal update/stop/accounting, disabled clear, disable/stop/re-enable, stale revision/callback and app-server next-request behavior. Static attacks identify two unhandled read failures after committed service mutations (findings above).",
      "attacks": [
        "create: create_goal_changes_the_next_sampling_tools and app-server v2_create_goal_exposes_sleep_only_after_committed_success; create_waits_for_finish mutant killed",
        "turn-start missing baseline/Plan and stale absent marker: turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal; turn_start_requires_baseline killed",
        "resume/external set: external_set_and_resume_reconcile_first_request all six statuses; external_set_skips_budget_limited and resume_skips_budget_limited killed",
        "terminal updates/automatic stop/accounting: complete/paused/blocked tests, accounting_budget_keeps_sleep_without_automatic_continuation, automatic_stop_revokes_activity_for_error_and_usage_limit; complete/usage-limit/budget-limited mutants killed",
        "clear/feature-off/stale effects: clear_revokes_before_late_create_finish_and_stale_set_effects; disabled_clear/late_active_set/cleared_revision mutants killed; newly attacked returned-row failure is broken",
        "disable/stop/re-enable and wait/timer options: disable_and_stop_revoke_activity_and_pending_options, disable_mid_turn_removes_sleep_from_next_request; disable/stop mutants killed",
        "read failures: kept read/stop/abort tests and new set-get/set-prepare/fork-flush/tool-finish/turn-error regressions; corresponding mutants killed. Internal set post-write read and clear return decoding remain broken",
        "duplicate/out-of-order: publisher_refuses_stale_revision_and_recovers_unknown_state checks duplicate revision stability, clear/disable invalidation and stale-read rejection; stale callback effects re-read under permit",
        "one writer: candidate static search confines GoalActivity insertion/removal to activity.rs; core consumes presence at spec_plan.rs:148"
      ]
    }
  ],
  "free_hunt": {
    "scope": "Bounded inspection of GoalStore mutation internals, feature teardown, permit ownership/reconciliation, sole-writer search, production service callers and spec-plan consumer.",
    "result": "Two same-class error-publication gaps reported above; no additional blocking issue established. No first-hit stop: all one surface row and all its attack families swept.",
    "bounds": "Static panel; no local cargo/just/build/test. Requested new Rust attacks are unexecuted. Full JSON-RPC fault-injection, Bazel and overlapping automatic/manual-turn lease races remain unmeasured, not claimed green."
  }
}
```
