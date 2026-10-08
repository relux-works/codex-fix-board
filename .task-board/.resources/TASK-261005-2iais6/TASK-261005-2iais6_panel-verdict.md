# R141 panel B — CR-TASK-260929-2gp04j-4

accept

Replay tree: `65ad71d230e7d7ac5923b8f88739a504b0fc1d08` — exact match to the brief and hosted precheck 8. Base: `729f259e62a8d11d9e17398e487790e1ee5d8b8c`. Replay used a temporary index; the real index and tracked tree were unchanged. No writes or verdict/status/handoff mutations were made on TASK-260929-2gp04j.

## Commands and real exit codes

All replay and validation steps below ran sequentially as standalone processes. Paths are relative to the assigned worktree unless absolute.

| Command | Exit | Result |
|---|---:|---|
| `task-board m 'set_status(TASK-261005-2iais6, status=analysis)'` | 0 | Panel lifecycle only |
| `command -v task-board git rg`; `git --version`; `rg --version` | 0 | Readiness output in `.temp/TASK-261005-2iais6/tool-readiness-01.log` |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev4.patch --output .temp/TASK-261005-2iais6/rev4.patch` | 0 | Patch read only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2iais6/replay.idx" git read-tree 729f259e62a8d11d9e17398e487790e1ee5d8b8c` | 0 | Base index |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2iais6/replay.idx" git apply --cached .temp/TASK-261005-2iais6/rev4.patch` | 0 | Replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2iais6/replay.idx" git write-tree` | 0 | Printed expected tree exactly |
| `git diff --check 729f259e62a8d11d9e17398e487790e1ee5d8b8c 65ad71d230e7d7ac5923b8f88739a504b0fc1d08` | 0 | No whitespace errors |
| `git diff --stat BASE TREE`; scoped `git diff BASE TREE -- <reviewed paths>`; `git show TREE:<path>` | 0 each | Candidate, not checkout, reviewed |
| `git status --short` (before and after static review) | 0 each | Empty tracked/untracked status |
| `task-board q 'get(TASK-260929-2gp04j) { description scope ac notes }'` | 0 | Read-only contract/context |
| `task-board q 'get(TASK-261005-2iais6) { ac checklist }'` | 0 | Panel requirements |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives; run not goal-bound |
| `python3 --version` | 0 | Readiness log `.temp/TASK-261005-2iais6/python-readiness-01.log` |
| Python JSON read of attached mutants; `cat`/`sed`/`rg` candidate and attachment reads | 0 each | 25 mutants, four guard-site narrowings checked |

Non-gate discovery failures were corrected: initial skill-path search exited 2 because `agents/` and `.claude/` are absent; query with unsupported `resources` field exited 1; positional `schema(get)` exited 1. Corrected scoped reads succeeded. No failed command is reported as a passing gate. Candidate extraction was a read-only archive pipeline, not a validation gate; its process result was 0, but per-stage statuses were not captured and it is not execution evidence. Candidate identity comes from the standalone index replay and `git show` reads.

Artifact creation via the task-scoped Python writer exited 0. The standalone Python verdict checker (one fence, JSON parse, exact required keys, one unique surface row, valid result, one verdict, empty blocking/free-hunt arrays) exited 0 before attachment.

## Contract sweep and fact checks

| AC | Production path and inspected named attack |
|---|---|
| 1 | `tool.rs:174-196` takes the state permit and re-reads before returning; core `create_goal_changes_the_next_sampling_tools` includes refused create. |
| 2 | `extension.rs:248-287` reconciles before missing baseline/Plan exits; `turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal`. |
| 3 | `runtime.rs:518-537` resume and `api.rs:291-298` successful set reconcile; `external_set_and_resume_reconcile_first_request` covers all six statuses. |
| 4 | Post-tool reconcile, stop and accounting reconciles; `accounting_budget_keeps_sleep_without_automatic_continuation`, `automatic_stop_revokes_activity_for_error_and_usage_limit`, create/update terminal cases. |
| 5 | `api.rs:342-360` guarded delete then unconditional clear, `activity.rs:117-122` revision bump; latched `clear_revokes_before_late_create_finish_and_stale_set_effects` drives disabled clear and stale effects. |
| 6 | `runtime.rs:124-142` disable/stop clears accounting and pending start options/permit; lifecycle `disable_and_stop_revoke_activity_and_pending_options`, core disable-mid-turn. |
| 7 | `activity.rs:79-86` removes and records Unknown; service guards `api.rs:205,233,264,342,389-407` protect all four writes. Real SQL malformed rows/triggers exercise failure before write, after committed update, after committed delete decode, and failed replacement with a still-published marker. Named recovery tests and site mutants are in precheck 8. |
| 8 | App-server test `v2_create_goal_exposes_sleep_only_after_committed_success` drives JSON-RPC thread/turn start and asserts the three request tool lists `[false, success, false]`. |

The source sweep found production GoalActivity writes only in `ext/goal/src/activity.rs`. Tool-name success is not publication authority. Service outcomes re-read committed state under the shared permit before applying delayed runtime effects. The disabled-clear test injects a stale marker deliberately, proving clear independently of disable. The new replace-path test starts with a published marker and removes the DB row behind the publisher before refusing INSERT; unlike the previous marker-already-absent phase, it can kill the replacement-site bypass.

Sources: read-only attachments under `/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-2gp04j/`: `surface-table.md`, `producer-brief.md`, `TASK-260929-2gp04j_results.md` (rev4/precheck8 addenda), `TASK-260929-2gp04j_hosted-precheck-8.md`, and `TASK-260929-2gp04j_mutants.json`. Candidate sources were pinned to the full replay tree above. No prior precheck's different tree was used to attest this revision.

## Bounded free hunt and outcome-scoped logbook

After the one-row sweep, inspected permit sharing at automatic turn start, revision invalidation, late external set/clear effects, fallible goal-state callers, wire/config/history impact, dev-dependency/Bazel wiring, and size. No additional reproduced blocking mechanism. Pure API get and continuation-deferral flag reads do not themselves mutate or authorize GoalActivity; no absence was inferred from their errors. No new context fragments, RPC shapes, CLI arguments, config schema, or rollout serialization are introduced by these hooks. Additional simultaneous config-toggle/automatic-start interleavings are not independently executed here; this is a verification bound, not a reproduced defect.

Logbook: exact-tree binding held; the formerly surviving replace-path bypass now has a sensitive live-marker regression and a reported hosted kill. Producer mutant classification and cumulative size were corrected as nonblocking notes. This panel has only its own task-scoped resource/lifecycle writes. Recommendation: accept the reviewed candidate subject to the recording reviewer's merge of panel verdicts; this panel records no decision on the producer task.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "mutant-classification",
      "text": "The producer says every mutant narrows a gate. guard_skips_revocation_on_store_error actually removes the error-arm revocation; treat it as a deletion control. The four independent *_bypasses_guard mutants keep the guard and pass None at one service write site each, providing the required site-specific narrowing evidence. This does not invalidate the 25 reported kills."
    },
    {
      "id": "size-and-delivery-bound",
      "text": "Full base-to-candidate diff is +2761/-153 across 22 files, including the previously accepted G1 marker/router slice. It exceeds normal review-size guidance. Keep the documented upstream staging: G1 marker/router and its tests first; G2 publisher/runtime/service hooks and integration attacks second. Further separate service-error settlement and its tests if needed; do not split producer state in this read-only panel."
    },
    {
      "id": "verification-bound",
      "text": "No local builds, tests, hosted-status retrieval or mutants were executed by this panel. Executed public-entry attacks are accepted from the attached exact-tree hosted precheck-8, per the panel brief. That attachment reports lane conclusions and intended test failures, not standalone process exit codes; unknown hosted exit codes are not synthesized. Bazel/other-OS execution is not independently established here."
    },
    {
      "id": "dependency-process",
      "text": "Candidate includes existing sqlx dev dependency edges and core->goal-extension dev dependency; MODULE.bazel.lock is unchanged. Producer documents the prior accepted Bazel-irrelevant precedent. No new dependency change in rev4 itself. This panel ran no regeneration/build, so it does not independently certify Bazel lock regeneration."
    }
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "held",
      "invariant": "Committed Active/BudgetLimited has the current marker; terminal/cleared/disabled/stopped/unknown state does not authorize sleep; delayed callbacks cannot restore stale goal authority.",
      "attacks": [
        "Exact-tree hosted snapshot 37263271056: core create_goal_changes_the_next_sampling_tools (success, refused, complete, paused, blocked); app-server v2_create_goal_exposes_sleep_only_after_committed_success (created/refused).",
        "Snapshot: turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal; external_set_and_resume_reconcile_first_request across all six statuses; accounting_budget_keeps_sleep_without_automatic_continuation.",
        "Snapshot: clear_revokes_before_late_create_finish_and_stale_set_effects; disable_mid_turn_removes_sleep_from_next_request; extension lifecycle disable_and_stop_revoke_activity_and_pending_options; forged-success tool_finish_reconciles_committed_state_independently_of_tool_name.",
        "Snapshot: read-failure/recovery tests at turn-start, turn-stop, abort, turn-error, tool-finish, external get/prepare/fork; new post-write/decode/refused-delete/replace failure attacks drive GoalService entries against a live thread and real SQLite faults.",
        "Narrowing mutant runs 37263517219, 37263531175, 37263544776, 37263317078 respectively bypass objective-update, replace, status-update and clear-delete guards; all killed by their named production-entry tests. Remaining attached status/lifecycle mutants cover BudgetLimited, clear revision, disable/stop and early return boundaries."
      ],
      "evidence": [
        "TASK-260929-2gp04j_hosted-precheck-8.md",
        "TASK-260929-2gp04j_mutants.json",
        "TASK-260929-2gp04j_results.md"
      ],
      "coverage": {
        "surface_rows": "1/1",
        "ac_rows": "8/8",
        "reported_mutant_kills": "25/25"
      },
      "bound": "Held is limited to the named executed attacks plus this static sweep; it is not proof of universal absence."
    }
  ],
  "free_hunt": []
}
```
