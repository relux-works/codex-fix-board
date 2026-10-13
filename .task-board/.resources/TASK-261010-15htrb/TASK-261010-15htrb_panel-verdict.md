# Panel B verdict — R141 TASK-260929-3ld28o rev1 (CR-TASK-260929-3ld28o-1)

Reviewer: TASK-261010-15htrb (non-recording panel; tb-R209 pair codex sol high + muse max).
Scope: read-only review of CR-TASK-260929-3ld28o-1 rev1. No builds run (brief forbids
cargo/just; shared target serialized). No write of any kind was made on TASK-260929-3ld28o.

## Replay tree check: MATCH

Base 07c018be3507b8d4a5558a85a117b94ed2a23872 + patch
TASK-260929-3ld28o_change-request_rev1.patch through a temporary index yields write-tree
f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0, exactly the expected candidate tree.

## Commands run (with exit codes)

- GIT_INDEX_FILE=$IDX git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872 -> exit 0
- GIT_INDEX_FILE=$IDX git apply --cached .temp/TASK-260929-3ld28o_change-request_rev1.patch -> exit 0
- GIT_INDEX_FILE=$IDX git write-tree -> exit 0, printed f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0
- task-board resource get TASK-260929-3ld28o <11 resources> --output .temp/<name> -> exit 0 (all)
- git archive f861a84... <13 candidate paths> | tar -x -C .temp/TASK-261010-15htrb-cand -> exit 0
- git diff 07c018be... f861a84... --stat and per-file diffs; git show/git grep reads on the
  candidate tree (record-site inventory, enum definitions, harness, restore_after_resume) -> exit 0
- cargo/just/build/test: NOT run (forbidden by the panel brief; execution evidence is the
  CR validation log plus hosted relux-ci run 38013874463 cited below)

## Verdict

accept

## Summary

All 7 surface rows held. The four reset sources record only at committing handlers/events
(9 record sites inventoried, none in on_tool_finish); all five AC2 non-resets have named
tests with hosted-killed narrowing mutants; code-mode exactly-once, no-model-bypass,
blocker preservation, transience, and API minimality all verified against the candidate
tree. Hosted evidence: relux-ci run 38013874463 (lanes lint/core/app-server/small all
success) plus 10/10 narrowing mutants killed on the exact candidate tree; CR validation
log exit 0. Two robustness findings (untested record arms with conservative-miss failure
mode) and two notes (partial ignore-arm coverage; one killer misattribution in the
results file) do not block landing.

```verdict-findings
{
  "findings": [
    {
      "id": "F1",
      "row": "reset sources at committing handlers",
      "invariant": "Every committed goal mutation (create/update/external set-clear) records exactly one observation at its committing handler after the store commit (AC1/R3).",
      "mechanism": "The two external-mutation record sites (runtime.rs apply_external_goal_set and apply_external_goal_clear) are correct on inspection (record only after the committed-state check, only when a turn exists) but no test drives them through the production call site: unit tests call record_goal_mutation directly and backend tests exercise only create/update tools (verified: no test references apply_external_goal_*). A mutant deleting either record call survives the full suite. Failure mode is a missed observation (conservative pacing delay), never a false reset.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/goal_extension_backend/state_change_observation_tests.rs",
          "command": "hosted relux-ci lane small on the exact candidate tree plus a narrowing mutant deleting the record_goal_mutation call in apply_external_goal_set",
          "expected_failure": "SURVIVES with current tests (suite stays green); wanted test backend_external_goal_set_and_clear_record would fail under the mutant (expected count >= 1, observed 0)"
        }
      ],
      "severity": "robustness",
      "repeat-of": null
    },
    {
      "id": "F2",
      "row": "reset sources at committing handlers",
      "invariant": "Accepted spawn/follow-up records exactly one observation per committing event: SpawnAgent/SendInput/SendMessage/FollowupTask Completed plus SubAgentActivity Started/Interacted (AC1/R4).",
      "mechanism": "The classifier arms for CollabAgentTool::SendMessage and FollowupTask Completed are never fed in any test (verified: no state-change test file references either variant; CollabAgentTool has 9 variants, tests drive SpawnAgent/SendInput plus exclusions). The existing spawn_only_spawn_agent_counts mutant bundles their removal with SendInput, so its kill by send_input_completed_sets_observation proves only SendInput coverage; a mutant dropping exactly SendMessage|FollowupTask survives. Failure mode is a missed observation (conservative), never a false reset.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/state_change_observations.rs",
          "command": "hosted relux-ci lane small on the exact candidate tree plus a narrowing mutant removing SendMessage|FollowupTask from the CollabAgentTool match in record_state_change_for_item",
          "expected_failure": "SURVIVES with current tests (suite stays green); wanted cases send_message/followup_task Completed asserting count 1 would fail under the mutant"
        }
      ],
      "severity": "robustness",
      "repeat-of": null
    },
    {
      "id": "F3",
      "row": "non-resets",
      "invariant": "Every non-state-changing item kind is ignored by the classifier (AC2).",
      "mechanism": "Ignore-arm coverage beyond AC2's five named non-resets is partial: only FileChange(non-completed), AgentMessage, CommandExecution, a CollabAgentToolCall subset and SubAgentActivity(non-started) are fed to record_state_change_for_item in tests. McpToolCall, DynamicToolCall, FunctionCallOutput, Plan, Reasoning, WebSearch, ImageView, Extension, ImageGeneration, Entered/ExitedReviewMode, ContextCompaction, UserMessage and HookPrompt never reach the classifier in tests, so a regression adding one as recording would go undetected. Mitigated: the match is exhaustive with no wildcard arm, so future TurnItem variants force compile-time handling.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/state_change_observations.rs",
          "command": "hosted relux-ci lane small on the exact candidate tree plus a widening mutant adding TurnItem::McpToolCall as a recording arm",
          "expected_failure": "SURVIVES with current tests (suite stays green); wanted ignore-arm sweep test feeding every non-recording variant would fail under the mutant"
        }
      ],
      "severity": "note",
      "repeat-of": null
    },
    {
      "id": "F4",
      "row": "code-mode leaf accounting",
      "invariant": "AC8 killer attribution in the results file is accurate.",
      "mechanism": "The results-file AC8 table names code_mode_leaf_counts_once_and_wrapper_adds_none as the killer of tool_finish_success_records_mutation, but that mutant hooks extension on_tool_finish, which the unit test never calls (it calls accounting record_tool_outcome directly), so the unit test cannot kill it. Hosted precheck-4 evidence correctly attributes the kill to backend_spawn_followup_sets_but_tool_finish_success_does_not, which drives the real on_tool_finish with Completed{success:true} through the registry. Doc-only: the mutant IS killed and AC3's double-count mutant (command_execution_counts_as_state_change) IS killed by the AC3 unit test.",
      "reproductions": [
        {
          "test_file": "TASK-260929-3ld28o_results.md (AC8 table) vs TASK-260929-3ld28o_hosted-precheck-4.md (killer map)",
          "command": "compare the AC8 table row for tool_finish_success_records_mutation against the hosted killer map",
          "expected_failure": "attribution mismatch found (unit test named in table, backend test actual in hosted evidence)"
        }
      ],
      "severity": "note",
      "repeat-of": null
    }
  ],
  "notes": [
    "Replay: temp-index write-tree f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0 matches the expected candidate tree exactly (read-tree/apply/write-tree all exit 0).",
    "Method: static attack only; no cargo/just/build/test executed per the panel brief. Executed-attack evidence is hosted relux-ci run 38013874463 (lint/core/app-server/small all success on the exact candidate tree incl. snapshot plus 10 narrowing-mutant runs) and the CR validation log (exit 0).",
    "Record-site inventory (9 sites, all at committing handlers/events, none in on_tool_finish): accounting.rs classifier arms x3, extension.rs on_item_completed and on_plan_committed, runtime.rs external set/clear x2, tool.rs create/update x2.",
    "accounting.rs diff is purely additive (0 deletions across the file); record_tool_outcome/record_item/empty_response_goal are byte-identical. Total CR deletions (5 lines) are the plan.rs call_id/args.clone rewire and the on_item_completed reindent.",
    "Protocol facts verified on the candidate tree: StepStatus has exactly 3 variants (plans_equal pairwise match is exhaustive); PlanItemArg carries only step+status (explanation structurally unreachable); CollabAgentTool has 9 variants (4 counted); PatchApplyStatus has 3 variants + None, all covered by tests; SubAgentActivityKind has 4 variants, all covered by tests.",
    "AC7 bound present verbatim in the results file (arbitrary shell side effects UNKNOWN; pacing conservative; completion never inferred from shell output).",
    "Change size 13 files / 1061 insertions / 5 deletions noted; production logic ~283 lines, remainder tests."
  ],
  "surface_results": [
    {
      "row": "reset sources at committing handlers",
      "result": "held",
      "reason": "All 9 record sites sit at committing handlers/events: tool.rs create/update record after DB success (verified post-? placement; failed create returns early, backend duplicate-create test holds count at 1); runtime.rs external set/clear record only after the committed-state check; extension on_item_completed classifies only Completed/Started/Interacted committing items; plan.rs notifies after PlanUpdate publication with parse-error and Plan-mode early returns before it; on_tool_finish records nothing (killed mutant tool_finish_success_records_mutation proves it). Hosted R1-R4 mutants all killed. Residual untested arms recorded as F1/F2 (robustness, conservative-miss mode)."
    },
    {
      "row": "non-resets",
      "result": "held",
      "reason": "Each AC2 non-reset has a named test: failed_tool_does_not_set_observation covers all 6 ToolCallOutcome variants through record_tool_outcome; failed_or_declined covers None/Failed/Declined FileChange; identical_plan_resubmission; shell_success (ToolFinish success + CommandExecution item); wrapper-only half of the AC3 test; model_text with 3 progress-claim texts. Hosted N1-N5 mutants all killed on lane small. Untested ignore-arm variants beyond AC2 recorded as F3 (note)."
    },
    {
      "row": "code-mode leaf accounting",
      "result": "held",
      "reason": "Classifier counts one FileChange Completed as 1 and ignores the wrapper CommandExecution and ToolFinish success (unit test asserts 1 for leaf+wrapper, 0 for wrapper-only). The double-count/wrapper mutant command_execution_counts_as_state_change is killed by this exact test on the hosted lane. Killer-attribution doc slip recorded as F4 (note). Exactly-once additionally relies on host routing of the leaf FileChange to the owning turn (see free_hunt)."
    },
    {
      "row": "no model-writable bypass",
      "result": "held",
      "reason": "No free-text path reaches any record method: the plan comparator takes &[PlanItemArg] (step+status only; explanation unreachable by API shape, verified against the protocol type); the classifier reads only host-set enums (PatchApplyStatus/tool/status/kind); turn_ids come from host stores/invocations. Magic-text plan/tool/message bypass test holds count at 1 and the agent_message_state_keyword_counts mutant is killed on the hosted lane."
    },
    {
      "row": "existing activity and blocker untouched",
      "result": "held",
      "reason": "Zero deletions in accounting.rs: record_tool_outcome/record_item/empty_response_goal byte-identical; on_tool_finish body unchanged (only on_item_completed gained one classifier line plus the new on_plan_committed method). Two new tests prove the three-empty blocker fires on schedule with and without observations; pre-existing suites green on hosted lint/core/app-server/small lanes (run 38013874463)."
    },
    {
      "row": "transient state",
      "result": "held",
      "reason": "Counts live in the per-turn map removed by finish_turn; plan memory is in-memory default() state; no state_change keys in rollout/history paths; restore_after_resume touches only active-goal markers. Proven by observation_is_transient_per_turn, fresh_state_carries_no_observation_or_plan_memory and backend_fresh_runtime_carries_no_observation, all green on the hosted lane."
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "reason": "New extension-api surface is one struct (PlanCommitInput) + one defaulted trait method (on_plan_committed) + re-exports; core adds only the thin notify_plan_committed fan-out and one call site after PlanUpdate publication; no core->goal edge (core touches extension-api only). The defaulted method cannot break existing contributors. Bounded: last_committed_plan is replaced per commit, never appended; no new model-visible field or tool."
    }
  ],
  "free_hunt": {
    "summary": "Bounded free hunt completed: 8 probes, all held, no additional behavioral defects. One residual reliance named with a wanted attack.",
    "probes": [
      {
        "area": "plan-hook failure ordering",
        "outcome": "held: parse errors and Plan-mode rejection return before send_event/notify; an abort after a committed publish still correctly records (the plan WAS committed)."
      },
      {
        "area": "plan-hook retry double-fire",
        "outcome": "held: a retried identical update_plan self-corrects via the comparator (second submit returns false, no count)."
      },
      {
        "area": "first-plan-counts vs AC1 parenthetical",
        "outcome": "held: counting the first committed plan as a transition-from-nothing is documented in results, asserted by unit+backend tests, and green on hosted lanes; accepted, no finding."
      },
      {
        "area": "StepStatus exhaustiveness in plans_equal",
        "outcome": "held: StepStatus has exactly Pending/InProgress/Completed on the candidate tree, so the explicit-pair matches! is exhaustive and cross-status pairs correctly report transitions."
      },
      {
        "area": "overflow and concurrency of counts",
        "outcome": "held: saturating_add on u32; all record paths take &self through a poison-tolerant Mutex."
      },
      {
        "area": "empty-but-Completed FileChange edge",
        "outcome": "held: counts as applied; harmless (conservative-toward-progress direction on a host-committed item); no finding."
      },
      {
        "area": "SendInput non-Completed statuses",
        "outcome": "held: the status==Completed gate is one shared expression for all four counted tools and the SpawnAgent Failed/InProgress matrix proves the gate; accepted without a dedicated SendInput-Failed case."
      },
      {
        "area": "AC3 end-to-end leaf routing (wanted attack, not run)",
        "outcome": "residual reliance: the classifier half of exactly-once is executed and mutant-proven, but no core/code-mode test proves a real nested leaf's FileChange is delivered exactly once to the owning turn's on_item_completed. Wanted: a core suite test dispatching a real code-mode leaf that applies a file change and asserting the parent turn observes exactly 1 (and 0 for a failing leaf). Not marked not-attacked: hosted mutant runs on the exact candidate tree ARE executed attacks on the classifier."
      }
    ]
  }
}
```
