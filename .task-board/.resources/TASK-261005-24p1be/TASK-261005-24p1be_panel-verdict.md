# R141 panel A — CR-TASK-260929-2gp04j-4 revision 4

accept

Replay: PASS. Base `729f259e62a8d11d9e17398e487790e1ee5d8b8c` plus the resource patch gives `65ad71d230e7d7ac5923b8f88739a504b0fc1d08`, exactly the expected candidate tree. Only a temporary index was used; real index and repository sources were not edited. Nothing was written or recorded on TASK-260929-2gp04j. This is advisory panel evidence, not recording-review acceptance.

## Commands and real exit codes

Commands ran directly, without tee or test-output pipe chains. Paths below are relative to the assigned worktree unless absolute.

| Command | Exit | Result |
|---|---:|---|
| `task-board m 'set_status(TASK-261005-24p1be, status=analysis)'` | 0 | Panel lifecycle only |
| `git --version`, `rg --version` | 0 each | Readiness output in `.temp/TASK-261005-24p1be/readiness.log` |
| Initial `rg --files ... agents .claude .codex` | 2 | Missing search roots; existing `.codex` skills were found; not a validation pass |
| First `get` projection with `resources` | 1 | Unsupported field; corrected read succeeded |
| `get` projection with `artifacts` | 0 process, query error | Unsupported field; not a successful board read |
| `schema(get)` | 1 | Unsupported positional syntax; `schema(operation="get")` subsequently exit 0 |
| Initial proposed `rm -f`/read-tree shell call | not executed | Tool rejected rm syntax; unique index path used instead |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-24p1be/replay.idx" git read-tree 729f259e62a8d11d9e17398e487790e1ee5d8b8c` | 0 | Read exact base |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev4.patch --output .temp/TASK-260929-2gp04j_change-request_rev4.patch` | 0 | Read-only materialization |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-24p1be/replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev4.patch` | 0 | Replay succeeded |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-24p1be/replay.idx" git write-tree` | 0 | Exact candidate tree above |
| `task-board resource get TASK-260929-2gp04j <name> --output <local>` for surface-table.md, producer-brief.md, TASK-260929-2gp04j_results.md, TASK-260929-2gp04j_hosted-precheck-8.md, TASK-260929-2gp04j_mutants.json | 0 each | Sources inspected under `.temp/TASK-261005-24p1be/` |
| `git diff --stat BASE TREE`, candidate `git show`, caller `git grep`, successful task description/AC/checklist projections | 0 | Static inspection only |
| `git diff --check 729f259e62a8d11d9e17398e487790e1ee5d8b8c 65ad71d230e7d7ac5923b8f88739a504b0fc1d08` | 0 | Whitespace check |
| `python3 --version` | 0 | Readiness output in task scratch |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives; no active run goal |
| Python driver invoking `git apply --cached --check -` for each attached mutant, with replay index | 0 driver, 0 each of 25 git processes | Applicable only; no mutant execution claimed |
| `git status --short` | 0 | No tracked/untracked repository delta reported |

Individual applicability exits:

- `create_waits_for_finish`: 0
- `turn_start_requires_baseline`: 0
- `resume_skips_budget_limited`: 0
- `external_set_skips_budget_limited`: 0
- `complete_retains_sleep`: 0
- `usage_limit_retains_sleep`: 0
- `budget_limited_admits_continuation`: 0
- `disabled_clear_keeps_marker`: 0
- `disable_preserves_active_marker`: 0
- `stop_preserves_active_marker`: 0
- `timestamp_read_failure_keeps_known_marker`: 0
- `cleared_revision_accepts_old_read`: 0
- `late_active_set_reinserts_cleared_goal`: 0
- `turn_stop_read_failure_keeps_marker`: 0
- `abort_read_failure_keeps_marker`: 0
- `external_set_get_failure_keeps_marker`: 0
- `external_set_prepare_failure_keeps_marker`: 0
- `fork_flush_prepare_failure_keeps_marker`: 0
- `tool_finish_accounting_failure_keeps_marker`: 0
- `turn_error_skips_reconcile_after_stop_failure`: 0
- `guard_skips_revocation_on_store_error`: 0
- `set_status_update_bypasses_guard`: 0
- `set_objective_update_bypasses_guard`: 0
- `set_replace_bypasses_guard`: 0
- `clear_delete_bypasses_guard`: 0

Outcome generation: Python writer exit 0. Outcome validation: standalone Python JSON/fence/row/verdict/replay assertions exit 0. The checked object contains exactly one surface result and no blocking findings.

## Surface sweep and fact checks

The surface table has exactly one row, `goal activity publisher`. AC coverage is 8/8 by named driving tests, not a count inferred from suite success. Each row below cites the candidate test and the attached precheck-8 execution report. Core paths refer to `codex-rs/core/tests/suite/goal_activity_tests.rs`; small paths refer to `codex-rs/ext/goal/tests/goal_extension_backend/goal_activity_tests.rs`.

| AC | Driving attack and negative shape | Static production entry |
|---|---|---|
| 1 | core create success/refusal and complete/paused/blocked; create_waits_for_finish mutant killed | tool.rs:174–195 reconciles under the permit before returning the result |
| 2 | core missing baseline, Plan mode and cleared goal; turn_start_requires_baseline killed | extension.rs:248–273 reconciliation precedes both early returns |
| 3 | core external set/resume all six statuses; BudgetLimited omission mutants killed | api.rs set settlement, runtime.rs restore_after_resume/apply_external_goal_set |
| 4 | core budget exhaustion/no continuation; small automatic stops; retained Complete/UsageLimited and broadened continuation mutants killed | runtime.rs accounting settlement/stop/continue_if_idle; extension.rs finish hooks |
| 5 | core latch across clear, stale set effects, disabled clear; late-set and disabled-clear killed | api.rs unconditional clear_activity; delayed effects re-read committed state |
| 6 | small disable/stop/re-enable lifecycle plus core disable mid-turn; both retention mutants killed | runtime.rs set_enabled/stop invalidate publication and remove goal-owned options/lease |
| 7 | real malformed SQLite rows, post-write reads, returning-row decode, refused delete/insert, recovery; all five guard mutants and failure-site mutants killed | api.rs:205,231,265,343 call guard_live_store_result; extension error arms revoke; publisher stores Unknown and removes capability |
| 8 | app-server tests/suite/v2/goal_activity_tests.rs created/refused assert second request tools and goal result | public thread/start and turn/start, GoalToolExecutor execution |

The revision-4 guard remains present in the five new mutants; four pass no runtime at one write site and one weakens revocation on a store error. They test behavioral leakage rather than source tokens. The dedicated replace test starts with a present marker and removes the committed row behind it before refusing INSERT; this closes the earlier already-absent-marker false assurance. DELETE RETURNING failure asserts both Err and committed row count zero. The post-UPDATE test repairs the malformed timestamp before asserting the committed Complete state, so error is not incorrectly equated with unchanged state. Set-prepare test's exact +3 revision check distinguishes the prepare revocation from the later write guard.

Hosted evidence accepted: [snapshot run](https://github.com/relux-works/codex/actions/runs/37263271056), as reported by the board-attached precheck-8 outcome (all four lanes success). No hosted process exit code is invented. Mutant runs are expected red, not green validations. Their recorded killing tests establish the intended failures; the unrelated guardian test failure on run 37263407731 is not used as a kill. Locally rerun: replay, diff check and 25 applicability checks only.

## Bounded free hunt and outcome-scoped logbook

Budget: one panel decision, one text outcome (<32 KiB), no serial prerequisites or builds; static sweep plus a short free hunt within this run. Frozen grammar is not applicable. Consumer is the recording reviewer of this exact CR. No further research leaf is proposed.

Beyond the single surface row, checked production callers in app-server thread_goal_processor.rs (resume at 109, external effects at 243), lock acquisition order, shared automatic-start lease cleanup, revision invalidation across disable/clear/stop, API/schema/CLI/config/rollout compatibility, and model-context injection. No new context fragment or unbounded model-visible payload is introduced; router capability changes are the intended behavior. Existing goal response serialization and persisted goal shape are unchanged. No additional reproduced blocking mechanism was found. This is a bounded static result, not an exhaustive concurrency proof.

Logbook: rev-4's single settlement guard closes the prior read-failure-retains-capability class across all four service write sites. Hosted replace-path kill now has a dedicated precondition proving capability was present before failure. Cumulative size and unexecuted Bazel lock verification remain explicitly noted for upstream staging/landing. No control-root logbook file was edited; this paragraph travels with the panel outcome.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "execution-provenance",
      "text": "No cargo/just/build/test command was run by this panel. Execution evidence is the attached TASK-260929-2gp04j_hosted-precheck-8.md and results outcome, accepted under the panel brief. Hosted conclusions, not independently fetched raw logs or numeric process exit codes, are available here. Snapshot is reported success on lint/small/core/app-server; mutant runs are intentionally failing. The truncated local validation log is not used to infer success."
    },
    {
      "id": "upstream-staging",
      "text": "Cumulative story patch is +2761/-153 across 22 files, including G1. It exceeds change-size guidance. Keep the producer-agreed upstream staging: G1 typed marker/router first, then G2 publisher/hooks with their matching integration and failure tests; within G2, retain the guard and its four-site regressions together. This panel does not split the court-ordered rework."
    },
    {
      "id": "bazel-lock-bound",
      "text": "Cargo manifest/lock changes are test edges to existing workspace dependencies; MODULE.bazel.lock is unchanged. Producer cites the existing rev1/2 precedent and landing re-verification. No Bazel command was run here and Bazel lock freshness is unverified by this panel; hosted Cargo lanes alone do not establish it."
    },
    {
      "id": "held-bound",
      "text": "held means the named attacks did not reproduce on the supplied exact-tree hosted evidence. It is not proof against every possible race, status transition or store failure. Re-enable reconciles at the next legitimate lifecycle event; pure API get and continuation-deferral reads are outside the publisher transition scope."
    }
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "held",
      "coverage": {
        "surface_rows": "1/1",
        "ac_rows": "8/8",
        "narrowing_mutants": "25/25 hosted killed; 25/25 independently apply"
      },
      "attacks": [
        "core create_goal_changes_the_next_sampling_tools (complete/paused/blocked/refused); app-server v2_create_goal_exposes_sleep_only_after_committed_success (created/refused)",
        "core turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal; external_set_and_resume_reconcile_first_request (all six statuses)",
        "core accounting_budget_keeps_sleep_without_automatic_continuation; small automatic_stop_revokes_activity_for_error_and_usage_limit",
        "core clear_revokes_before_late_create_finish_and_stale_set_effects; disable_mid_turn_removes_sleep_from_next_request; small disable_and_stop_revoke_activity_and_pending_options",
        "small tool_finish_reconciles_committed_state_independently_of_tool_name; read_failure_revokes_activity_and_next_turn_recovers; turn stop/abort/error/tool-finish failure recovery tests",
        "core external_set_get_failure_revokes_activity_and_next_turn_recovers; external_set_prepare_failure_revokes_activity_and_next_turn_recovers; fork_flush_read_failure_revokes_activity_and_next_turn_recovers",
        "core external_set_post_write_read_failure_revokes_activity_and_next_turn_recovers; clear_returning_decode_failure_revokes_activity_and_next_turn_recovers; clear_prepare_failure_revokes_activity_and_next_turn_recovers; external_set_replace_failure_revokes_activity_and_next_turn_recovers",
        "publisher_refuses_stale_revision_and_recovers_unknown_state (supplemental unit check, not the sole public-entry evidence)"
      ],
      "evidence": [
        "TASK-260929-2gp04j_hosted-precheck-8.md: snapshot a37e2ebc, tree 65ad71d230e7d7ac5923b8f88739a504b0fc1d08, run 37263271056",
        "TASK-260929-2gp04j_results.md: precheck-8 addendum and AC map",
        "guard mutant 37263469809; status-update 37263544776; objective-update 37263517219; replace 37263531175; clear-delete 37263317078",
        "late-set 37263485560; disabled-clear 37263392780; baseline 37263619598; budget continuation 37263301509",
        "all 25 applicability checks: git apply --cached --check -, each exit 0"
      ]
    }
  ],
  "free_hunt": []
}
```
