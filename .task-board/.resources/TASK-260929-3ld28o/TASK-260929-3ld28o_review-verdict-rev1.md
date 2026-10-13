# Merged review verdict — TASK-260929-3ld28o CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261010-3pnf38_panel-verdict.md` (changes_requested), `TASK-261010-15htrb_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A-F1",
      "row": "reset sources at committing handlers",
      "invariant": "AC1/AC2: only accepted follow-ups reset; failed tools and rejected sends do not.",
      "mechanism": "Static production counterexample: V1 send_input.rs:95-131 captures a failed send, then emits a Completed CollabAgentToolCall from get_status rather than the send result, and only afterwards propagates result?. multi_agents.rs:86-94 treats Running (and other non-error statuses) as Completed. AgentControl::send_input maps NotSubmitted to InvalidRequest (control.rs:130-156) without removing a live child for this error (316-329). A child with a Compact task refuses steering (turn_input.rs:718-722,372) while its status can remain Running. GoalExtension::on_item_completed (extension.rs:342-344) calls accounting.rs:295-304, which counts this rejected send. The existing event status was formerly presentation; this change promotes it to acceptance evidence. The symmetric race can miss an accepted send if the child subsequently becomes Errored. Bind the observation to the delivery result at its committing path, preserving rejection and accepted-send semantics.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/tools/handlers/multi_agents_tests.rs (requested send_input_rejected_compaction_does_not_observe_state_change)",
          "command": "Requested hosted: just test -p codex-core -E 'test(send_input_rejected_compaction_does_not_observe_state_change)'",
          "expected_failure": "NOT RUN here. Reuse the non-regular-task fixture in core/src/session/turn_input_tests.rs:954; activate a parent goal, keep a child in Compact with Running status, call the real V1 SendInputHandler, and assert refusal plus unchanged parent observation (0). Static trace predicts an observation of 1 on this candidate. Include a successful-send control and an error-status-after-acceptance case.",
          "pinned_blobs": [
            "f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0:codex-rs/core/src/tools/handlers/multi_agents_tests.rs (requested send_input_rejected_compaction_does_not_observe_state_change)"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-3pnf38"
      ]
    },
    {
      "id": "A-F2",
      "row": "code-mode leaf accounting",
      "invariant": "AC3 and AC8: one actual nested applied change counts exactly once, wrapper-only success counts zero, demonstrated at the public exec entry with a narrowing mutant.",
      "mechanism": "state_change_observations.rs:338-361 directly calls accounting methods on a locally included accounting.rs (:12); it never executes functions.exec, CodeModeExecuteHandler, submit_nested_tool (core/src/tools/code_mode/mod.rs:335-412), or the production lifecycle. Its wrapper fixture is a ps CommandExecution item. The mutant tool_finish_success_records_mutation changes extension.rs, a module this test does not include, so it cannot be killed by this test. Hosted precheck 4 correctly names backend_spawn_followup_sets_but_tool_finish_success_does_not as its killer, which also injects callbacks and does not assert a real nested leaf+wrapper count. Therefore 0/1 required public code-mode accounting scenarios are executed by the submitted observation tests; the unit classifier count is useful but does not discharge AC3. Add actual exec->nested apply_patch coverage, assert before finish_turn clears counts, and kill a mutant that records wrapper success only for CodeMode or double-emits nested leaf completion.",
      "reproductions": [
        {
          "test_file": "codex-rs/app-server/tests/suite/goal_state_change_observations.rs (requested new integration case code_mode_applied_leaf_counts_once)",
          "command": "Requested hosted: just test -p codex-app-server -E 'test(code_mode_applied_leaf_counts_once)'",
          "expected_failure": "NOT RUN or implemented here. Drive JSON-RPC/model functions.exec with one successful tools.apply_patch and assert real file contents plus observation count 1 before turn stop; run wrapper-only control with count 0. Under a CodeMode-only extra wrapper-observation mutant the new test must fail with count 2/1. Existing classifier-only test cannot establish these runtime assertions.",
          "pinned_blobs": [
            "f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0:codex-rs/app-server/tests/suite/goal_state_change_observations.rs (requested new integration case code_mode_applied_leaf_counts_once)"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-3pnf38"
      ]
    },
    {
      "id": "A-F3",
      "row": "reset sources at committing handlers",
      "invariant": "AC8: each reset source has a narrowing mutant with a named killer; deletion-only proof is insufficient.",
      "mechanism": "The supplied goal_update_does_not_record mutant removes the entire update-goal recording call (tool.rs:319-320). It preserves create, but is deletion-only within the update gate. The sole backend observation assertion for update dispatch uses status complete (state_change_observation_tests.rs:132-169). It does not cover the other permitted committed update statuses paused and blocked (tool.rs:280-290), or external set/clear observation counts (runtime.rs:388-395,439-446). A mutant recording updates only when args.status == Complete narrows accepted update classes without changing this named killer. No executed result for such a mutant is attached. Replace/supplement the deletion mutant with complete-only recording and tests through actual update dispatch for paused and blocked; include explicit external-set/clear observation checks if those are claimed covered.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/goal_extension_backend/state_change_observation_tests.rs (requested backend_goal_paused_and_blocked_mutations_set_observation)",
          "command": "Requested hosted: just test -p codex-goal-extension --test goal_extension_backend -E 'test(backend_goal_paused_and_blocked_mutations_set_observation)'",
          "expected_failure": "NOT RUN or implemented here. Start independent goal turns, dispatch update_goal with paused and blocked, require one committed observation each. Under a mutant wrapping tool.rs:319-320 in args.status == ThreadGoalStatus::Complete, both should fail with 0. Survival of this proposed mutant has not been measured; only the coverage mismatch is statically established.",
          "pinned_blobs": [
            "f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0:codex-rs/ext/goal/tests/goal_extension_backend/state_change_observation_tests.rs (requested backend_goal_paused_and_blocked_mutations_set_observation)"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-3pnf38"
      ]
    },
    {
      "id": "F1",
      "row": "reset sources at committing handlers",
      "invariant": "Every committed goal mutation (create/update/external set-clear) records exactly one observation at its committing handler after the store commit (AC1/R3).",
      "mechanism": "The two external-mutation record sites (runtime.rs apply_external_goal_set and apply_external_goal_clear) are correct on inspection (record only after the committed-state check, only when a turn exists) but no test drives them through the production call site: unit tests call record_goal_mutation directly and backend tests exercise only create/update tools (verified: no test references apply_external_goal_*). A mutant deleting either record call survives the full suite. Failure mode is a missed observation (conservative pacing delay), never a false reset.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/goal_extension_backend/state_change_observation_tests.rs",
          "command": "hosted relux-ci lane small on the exact candidate tree plus a narrowing mutant deleting the record_goal_mutation call in apply_external_goal_set",
          "expected_failure": "SURVIVES with current tests (suite stays green); wanted test backend_external_goal_set_and_clear_record would fail under the mutant (expected count >= 1, observed 0)",
          "pinned_blobs": [
            "1f9930e8f9dc12b40f2a4806bca2e40b01020697"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-15htrb"
      ]
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
          "expected_failure": "SURVIVES with current tests (suite stays green); wanted cases send_message/followup_task Completed asserting count 1 would fail under the mutant",
          "pinned_blobs": [
            "c3a913fd826f1b16002dcd98056de46be6989594"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-15htrb"
      ]
    }
  ],
  "notes": [
    "[TASK-261010-3pnf38] Scope: CR-TASK-260929-3ld28o-1 revision 1, independent non-recording panel A. No source-task accept/reject/withdraw/status/handoff/resource/note mutation was issued.",
    "[TASK-261010-3pnf38] Replay exactness passed. All source citations refer to candidate tree f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0. Direct runtime attacks were prohibited; static counterexample A-F1 is not reported as an executed Rust reproduction.",
    "[TASK-261010-3pnf38] Hosted evidence source: TASK-260929-3ld28o_hosted-precheck-4.md, run 38013874463. Reports lint/core/app-server/small success and 10/10 mutant kills, but contains lane conclusions rather than individual process exit codes or mutant run IDs. Those codes are unknown here; no expected-red run is represented as exit 0.",
    "[TASK-261010-3pnf38] Hosted checked tree is 3dbcad941982fa04b3bdc899e697cfc4295154e8, not the candidate. git diff confirms identical codex-rs bytes and exactly two CI-only changed paths. The CR validation log runs mini-hosted-gate.sh (reported exit 0, exact_command_shard 1/1, test_case_coverage unknown) and explicitly accepts rebased-equivalent evidence. This proves the source equivalence checked here, not an executed exact-tree hosted run or unchanged workflow/config/environment identity. Do not label this exact-candidate execution. Request targeted follow-up attacks on the frozen revision, not an indiscriminate full replay.",
    "[TASK-261010-3pnf38] AC7 is explicitly satisfied by results.md: arbitrary shell side effects are UNKNOWN; shell success is not observed progress or completion.",
    "[TASK-261010-3pnf38] Existing classifier tests and recorded hosted mutant kills are retained as helper/callback evidence. Production source checks are distinguished from public-entry executed attacks. No row is not-attacked merely because builds are prohibited.",
    "[TASK-261010-3pnf38] Diff +1061/-5 across 13 files exceeds the 800-line guideline: production +275/-5, tests +786. Smallest independent stage is the defaulted extension-api hook plus thin core plan dispatch and its core test (135 added lines, 2 removed); the consumer/tests can follow. Within the consumer stage, remove redundant callback-fixture boilerplate while retaining actual entry attacks. Size is advisory rather than a separate runtime finding.",
    "[TASK-261010-15htrb] note-finding F3: Ignore-arm coverage beyond AC2's five named non-resets is partial: only FileChange(non-completed), AgentMessage, CommandExecution, a CollabAgentToolCall subset and SubAgentActivity(non-started) are fed to record_state_change_for_item in tests. McpToolCall, DynamicToolCall, FunctionCallOutput, Plan, Reasoning, WebSearch, ImageView, Extension, ImageGeneration, Entered/ExitedReviewMode, ContextCompaction, UserMessage and HookPrompt never reach the classifier in tests, so a regression adding one as recording would go undetected. Mitigated: the match is exhaustive with no wildcard arm, so future TurnItem variants force compile-time handling.",
    "[TASK-261010-15htrb] note-finding F4: The results-file AC8 table names code_mode_leaf_counts_once_and_wrapper_adds_none as the killer of tool_finish_success_records_mutation, but that mutant hooks extension on_tool_finish, which the unit test never calls (it calls accounting record_tool_outcome directly), so the unit test cannot kill it. Hosted precheck-4 evidence correctly attributes the kill to backend_spawn_followup_sets_but_tool_finish_success_does_not, which drives the real on_tool_finish with Completed{success:true} through the registry. Doc-only: the mutant IS killed and AC3's double-count mutant (command_execution_counts_as_state_change) IS killed by the AC3 unit test.",
    "[TASK-261010-15htrb] Replay: temp-index write-tree f861a84e0df895b20ebc42b02a0cdaa5e3cad7b0 matches the expected candidate tree exactly (read-tree/apply/write-tree all exit 0).",
    "[TASK-261010-15htrb] Method: static attack only; no cargo/just/build/test executed per the panel brief. Executed-attack evidence is hosted relux-ci run 38013874463 (lint/core/app-server/small all success on the exact candidate tree incl. snapshot plus 10 narrowing-mutant runs) and the CR validation log (exit 0).",
    "[TASK-261010-15htrb] Record-site inventory (9 sites, all at committing handlers/events, none in on_tool_finish): accounting.rs classifier arms x3, extension.rs on_item_completed and on_plan_committed, runtime.rs external set/clear x2, tool.rs create/update x2.",
    "[TASK-261010-15htrb] accounting.rs diff is purely additive (0 deletions across the file); record_tool_outcome/record_item/empty_response_goal are byte-identical. Total CR deletions (5 lines) are the plan.rs call_id/args.clone rewire and the on_item_completed reindent.",
    "[TASK-261010-15htrb] Protocol facts verified on the candidate tree: StepStatus has exactly 3 variants (plans_equal pairwise match is exhaustive); PlanItemArg carries only step+status (explanation structurally unreachable); CollabAgentTool has 9 variants (4 counted); PatchApplyStatus has 3 variants + None, all covered by tests; SubAgentActivityKind has 4 variants, all covered by tests.",
    "[TASK-261010-15htrb] AC7 bound present verbatim in the results file (arbitrary shell side effects UNKNOWN; pacing conservative; completion never inferred from shell output).",
    "[TASK-261010-15htrb] Change size 13 files / 1061 insertions / 5 deletions noted; production logic ~283 lines, remainder tests."
  ],
  "surface_results": [
    {
      "row": "reset sources at committing handlers",
      "result": "broken",
      "reason": "A-F1 proves the acceptance-proxy defect by a static production trace; A-F3 identifies the missing narrowing-class evidence. Audited all four sources: file events core/tools/events.rs:622-644 after apply result; plan handler:95-105 and lifecycle:165-183; goal tool:246-250/317-320 and external runtime:388-395/439-446; V1 send and V2 spawn/message commit paths. V2 emits one public SubAgentActivity after receipt and private analytics, so no V2 double count was found. Hosted callback tests do not attack V1 delivery refusal.",
      "reported_by": "TASK-261010-3pnf38"
    },
    {
      "row": "non-resets",
      "result": "broken",
      "reason": "A-F1: a failed real V1 send can count despite record_tool_outcome refusing to count ToolFinish. Other classes statically held: exhaustive classifier ignores CommandExecution and AgentMessage; plan comparison ignores explanation and detects identical steps/status. Hosted precheck reports kills for failed-patch/identical-plan/command/message/ToolFinish mutants, limited to their actual helper/callback driving tests. Named rejects constructed as Failed do not test production generating Completed for a refusal.",
      "reported_by": "TASK-261010-3pnf38"
    },
    {
      "row": "code-mode leaf accounting",
      "result": "broken",
      "reason": "A-F2: classifier exactly-once is tested, public functions.exec composition is not. 0/1 required nested-leaf public-entry count scenarios in the observation tests; generic backend ToolFinish mutant kill cannot replace that attack. Production submit_nested_tool was traced; no actual double count is claimed reproduced.",
      "reported_by": "TASK-261010-3pnf38"
    },
    {
      "row": "no model-writable bypass",
      "result": "held",
      "reason": "Static attack: searched observation writers; only host item classification, post-store mutation calls and the committed plan callback write counts. No newly added request/protocol field carries a count, and keyword text is ignored. Plan step/status changes are legitimate transitions; explanation cannot reach the comparator. Existing permissive goal argument deserialization does not copy unknown fields into accounting. Hosted keyword/text mutant kills support the classifier bound; V1 host acceptance proxy defect is already recorded under A-F1, not a direct writable-count field.",
      "reported_by": "TASK-261010-3pnf38"
    },
    {
      "row": "existing activity and blocker untouched",
      "result": "held",
      "reason": "Static equality check proves 4/4 existing functions byte-identical: record_tool_outcome, record_item, empty_response_goal, finish_turn. New count is separate and unread by the blocker. Existing on_turn_stop blocker ordering is unchanged. Hosted precheck reports old suites plus the two new empty-blocker tests green; no local runtime assertion is claimed.",
      "reported_by": "TASK-261010-3pnf38"
    },
    {
      "row": "transient state",
      "result": "held",
      "reason": "Static persistence/turn-boundary attack: count exists only in GoalTurnAccounting, defaults to zero, finish_turn removes the turn, and no rollout/history/store type is changed. Thread startup builds accounting in a fresh ExtensionData; resume reconciles goal DB state without loading observations. Hosted fresh-state/fresh-runtime and finish-turn tests support those memory boundaries. The fresh-runtime test creates a harness rather than exercising actual resume; a full resume count assertion is not claimed.",
      "reported_by": "TASK-261010-3pnf38"
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "reason": "Static compatibility attack: new PlanCommitInput borrows existing stores/plan; default on_plan_committed keeps existing contributors compatible. Core adds thin fan-out after successful plan parsing/publication, with no core->goal dependency or model-context/rollout wire change. The real core plan dispatch test records callback arguments; goal plan comparison is separately callback-tested. Additional plan clone/memory exists but no new model-context fragment is injected.",
      "reported_by": "TASK-261010-3pnf38"
    }
  ],
  "free_hunt": [
    "[TASK-261010-3pnf38] {\"bound\": \"After seven-row sweep, four focused targets: event-identity/double publication, goal identity/external mutation attribution, persistence and plan memory, validation identity/change-size. No builds, source mutations or unbounded search.\", \"result\": \"V1 result/status mismatch yielded A-F1; goal-status mutant class coverage yielded A-F3. V2 analytics is private and activity emitted once, so speculative V2 double counting was rejected. Per-turn memory is removed and no serialized count was found. Hosted config identity and oversized diff remain explicitly bounded notes.\", \"requested_attacks\": [\"Real V1 send_input refusal during child compaction with parent goal accounting; successful-send control.\", \"Actual functions.exec nested apply_patch plus wrapper-only count assertions and CodeMode-only wrapper/double-event mutant.\", \"Complete-only update-goal observation mutant killed by paused and blocked dispatch tests; external set/clear observation counts.\"]}",
    "[TASK-261010-15htrb] {\"summary\": \"Bounded free hunt completed: 8 probes, all held, no additional behavioral defects. One residual reliance named with a wanted attack.\", \"probes\": [{\"area\": \"plan-hook failure ordering\", \"outcome\": \"held: parse errors and Plan-mode rejection return before send_event/notify; an abort after a committed publish still correctly records (the plan WAS committed).\"}, {\"area\": \"plan-hook retry double-fire\", \"outcome\": \"held: a retried identical update_plan self-corrects via the comparator (second submit returns false, no count).\"}, {\"area\": \"first-plan-counts vs AC1 parenthetical\", \"outcome\": \"held: counting the first committed plan as a transition-from-nothing is documented in results, asserted by unit+backend tests, and green on hosted lanes; accepted, no finding.\"}, {\"area\": \"StepStatus exhaustiveness in plans_equal\", \"outcome\": \"held: StepStatus has exactly Pending/InProgress/Completed on the candidate tree, so the explicit-pair matches! is exhaustive and cross-status pairs correctly report transitions.\"}, {\"area\": \"overflow and concurrency of counts\", \"outcome\": \"held: saturating_add on u32; all record paths take &self through a poison-tolerant Mutex.\"}, {\"area\": \"empty-but-Completed FileChange edge\", \"outcome\": \"held: counts as applied; harmless (conservative-toward-progress direction on a host-committed item); no finding.\"}, {\"area\": \"SendInput non-Completed statuses\", \"outcome\": \"held: the status==Completed gate is one shared expression for all four counted tools and the SpawnAgent Failed/InProgress matrix proves the gate; accepted without a dedicated SendInput-Failed case.\"}, {\"area\": \"AC3 end-to-end leaf routing (wanted attack, not run)\", \"outcome\": \"residual reliance: the classifier half of exactly-once is executed and mutant-proven, but no core/code-mode test proves a real nested leaf's FileChange is delivered exactly once to the owning turn's on_item_completed. Wanted: a core suite test dispatching a real code-mode leaf that applies a file change and asserting the parent turn observes exactly 1 (and 0 for a failing leaf). Not marked not-attacked: hosted mutant runs on the exact candidate tree ARE executed attacks on the classifier.\"}]}"
  ]
}
```
