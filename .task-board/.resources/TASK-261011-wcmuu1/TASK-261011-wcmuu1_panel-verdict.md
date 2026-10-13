# Panel verdict — R141 panel B on TASK-260929-3ld28o CR rev3 (CR-TASK-260929-3ld28o-3)

Panel task: TASK-261011-wcmuu1 (independent, non-recording). No accept/reject/status/handoff
write of any kind was issued on TASK-260929-3ld28o; all board mutations belong to TASK-261011-wcmuu1.

Scope: Change Request CR-TASK-260929-3ld28o-3 revision 3.
Base 07c018be3507b8d4a5558a85a117b94ed2a23872.
Expected candidate tree 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7.

Verdict: accept

## Replay tree check (mandatory, first)

Replayed through a temporary index, never a nested worktree. One early attempt used a
mistyped base OID (my own typo, read-tree exit 128, apply exit 1, discarded); the corrected
run below is the gate:

- git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872 with GIT_INDEX_FILE=.temp/TASK-261011-wcmuu1-replay.idx — exit 0
- git apply --cached .temp/panel/TASK-260929-3ld28o_change-request_rev3.patch — exit 0
- git write-tree — exit 0, printed 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7, exactly the expected candidate tree

Candidate files were read with git show / git archive on that tree only.

## Other commands run (real exit codes)

- git diff --name-only 568588edd89a50d4f259f9e17eb902cd38ae9e8e 486ebfe5 — exit 0; exactly two paths (multi_agents/spawn.rs, multi_agents_tests.rs). Every other line is byte-identical to the precheck-6 green tree.
- 16/16 mutant patches git apply --check --cached against the candidate tree — exit 0 each.
- 16/16 temp-index mutant replays match the hosted mutant commit trees byte-for-byte by tree OID (all 16 hosted mutant commits are children of snapshot eb345af5).
- gh api snapshot commit eb345af5e4085cf3120a250904ef85389037a8e3 — exit 0; tree is exactly 486ebfe5, parent is the CR base. Hosted lanes ran on the exact candidate tree.
- gh api run 38083359851 jobs — exit 0; plan/lint/snapshot-small/snapshot-core/snapshot-app-server success; each mutant has exactly one failing lane (13 small, 3 core), matching the precheck-7 table; overall run conclusion is failure because the 16 expected-red mutant lanes fail.
- gh run view logs (mutant-15 core, mutant-3 core, snapshot core) — exit 0; kill attributions confirmed in raw logs (see notes).
- No cargo, just, build, or test command was run by this panel (forbidden by the brief). Execution evidence is hosted relux-ci run 38083359851 plus the CR rev3 validation log (mini-hosted-gate.sh exit 0, exact_command_shard 1/1, test_case_coverage unknown).

## Row sweep summary

All 7 surface rows swept, exactly one result each: 7 held, 0 broken, 0 not-attacked.
One structured finding at severity note (B-N1, row non-resets, repeat of rev2/B-N1):
ignore-arm execution coverage beyond the five named AC2 non-resets stays partial and stays
structurally mitigated by the exhaustive classifier match. It is advisory, not blocking,
and is preserved as a finding object per the rev1/rev2 recording-refusal guidance.
Rev2 blocking findings A-F1/D-F1 are fixed in production, regression-tested, and
mutant-killed on this exact tree (details in surface_results row 1 and notes).

```verdict-findings
{
  "findings": [
    {
      "id": "B-N1",
      "row": "non-resets",
      "invariant": "AC2/AC8: every ignored item class stays ignored; a regression that starts recording one is caught.",
      "mechanism": "Ignore-arm execution coverage beyond AC2's five named non-resets is partial: tests feed FileChange(non-completed), AgentMessage, CommandExecution, a CollabAgentToolCall subset, SubAgentActivity(non-started) and ToolFinish-success to the classifier, while McpToolCall, DynamicToolCall, FunctionCallOutput, Plan, Reasoning, WebSearch, ImageView, Extension, ImageGeneration, EnteredReviewMode, ExitedReviewMode, ContextCompaction, UserMessage and HookPrompt never reach record_state_change_for_item in tests, so a regression that starts recording one would go undetected by the suite. Mitigated structurally: the match in ext/goal/src/accounting.rs:290-334 lists every TurnItem variant explicitly with no wildcard arm, so adding a recording arm requires touching the classifier and a new variant forces compile-time handling (non-exhaustive match is a compile error; hosted lint/type-check is green on this exact tree). Classifier file is byte-identical to the rev2 green tree, so this condition is unchanged from rev2 panel-B B-N1.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/accounting.rs (record_state_change_for_item, static read)",
          "command": "static inspection only: git show 486ebfe5:accounting.rs plus git grep of classifier feeds in the observation test files; no build or test executed (forbidden by panel brief)",
          "expected_failure": "No failure observed and none claimed as executed: the ignore arm enumerates every TurnItem variant with no wildcard, so uncovered arms are compile-time-guarded. NOT a test execution."
        }
      ],
      "severity": "note",
      "repeat-of": "rev2/B-N1"
    }
  ],
  "notes": [
    "[TASK-261011-wcmuu1] Independent non-recording panel B on CR-TASK-260929-3ld28o-3 rev3. Base/patch replay tree exactly equals expected candidate 486ebfe5. No local cargo/just/build/test ran; production behavior evidence is static plus hosted logs unless stated.",
    "[TASK-261011-wcmuu1] Hosted identity independently verified via GitHub API: snapshot commit eb345af5e4085cf3120a250904ef85389037a8e3 has tree exactly 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7 with parent 07c018be (the CR base). Run 38083359851: plan/lint/snapshot-small/snapshot-core/snapshot-app-server success; overall conclusion failure because 16 expected-red mutant lanes fail. Snapshot core: 5081/5081 passed, 11 skipped, 3 flaky retried to green.",
    "[TASK-261011-wcmuu1] Mutant evidence independently verified: all 16 hosted mutant commits are children of the snapshot commit, and local temp-index replay of each attached mutant patch reproduces the hosted mutant tree OID exactly (16/16). Failing-lane pattern matches the precheck-7 table exactly (13 small, 3 core). Raw logs confirm: mutant-15 core (spawn_status tree e5924ad6) fails spawn_agent_accepted_with_errored_child_emits_completed_item 3/3 tries at multi_agents_tests.rs:3170 (the Completed assertion) while spawn_agent_refused_emits_failed_item and send_input_rejected_compaction_emits_failed_item PASS under it; mutant-3 core (code_mode tree 2e496bbb) fails code_mode_leaf_applied_patch_delivered_exactly_once; both new spawn tests PASS on snapshot core. Numeric exit codes of CI steps other than these log-confirmed kills are unknown here; no expected-red run is presented as exit 0.",
    "[TASK-261011-wcmuu1] Rev2 A-F1/D-F1 closure, verified on this tree: spawn.rs:178-192 binds the V1 completed-item status to result.is_ok() (delivery), mirroring send_input.rs:114-125; sampled liveness stays in agents_states for display (spawn.rs:175-177); the emission precedes result propagation so the refused path emits exactly one Failed item. The new accepted-with-errored test drives the real SpawnAgentHandler with an AgentControl accepted receipt (Ok LiveAgent, real thread id, Errored status) as the rev2 verdict allowed; the stub shape matches spawn_agent_internal (commit, disarm, then get_status sampled into LiveAgent). Observation link Completed->1 / Failed->0 is the unchanged executed classifier (accounting.rs:296-306). The deterministic fixture pins handler mapping; real-child race frequency remains unknown and unclaimed, as the results file honestly states.",
    "[TASK-261011-wcmuu1] AC7 bound present in results: arbitrary shell side effects are UNKNOWN; pacing may stay conservative and completion is never inferred from shell output or exit status.",
    "[TASK-261011-wcmuu1] Record-site inventory re-verified: exactly 2 state-change record calls in extension.rs (:344 on_item_completed, :526 on_plan_committed); on_tool_finish records only activity/progress state; on_item_completed has exactly one production caller (session/mod.rs:2631, inside emit_turn_item_completed); runtime/tool record sites unchanged from rev2 green tree. Rev2-to-rev3 delta is exactly 2 files (+333/-1), so all other CR files are byte-identical to the precheck-6 green tree.",
    "[TASK-261011-wcmuu1] Presentation consequence of the mandated fix (advisory, not a finding): an accepted spawn with an already-errored child now emits Completed instead of Failed. TUI renders a terminal cell either way; analytics maps Completed to tool-success instead of tool-error, consistent with the tool call having succeeded and with the rev1 send_input precedent; exec output is a passthrough; V2 event mappings are untouched. agents_states retains Errored for display in all these paths.",
    "[TASK-261011-wcmuu1] Change size 17 paths +1828/-7 exceeds the 800-line guideline; production logic is roughly 300 added lines and the rest is the AC8-mandated test plus mutant coverage. Smallest first stage remains the defaulted plan-commit hook, core fan-out, and plan test. Advisory only, not a finding. No model-visible context, wire schema, config, or dependency change."
  ],
  "surface_results": [
    {
      "row": "reset sources at committing handlers",
      "result": "held",
      "reason": "Rev2 A-F1/D-F1 fixed and executed on this exact tree: V1 spawn completion is bound to result.is_ok() (spawn.rs:178-192), mirroring the rev1 send_input fix; liveness stays in agents_states; refused path emits exactly one Failed item before result propagation. New accepted-with-errored test (real handler, AgentControl accepted receipt) passes on snapshot core and deterministically kills spawn_status_ignores_delivery_result (3/3 log-confirmed fails at the Completed assertion) while the refused control stays green. Classifier counts SpawnAgent only when Completed. Other three sources byte-identical to rev2 green tree; V2 receipt-success paths untouched. No remaining acceptance-proxy found."
    },
    {
      "row": "non-resets",
      "result": "held",
      "reason": "5/5 named AC2 non-reset categories have named tests, all present in the candidate and green on snapshot small; the five ignore-set mutants (failed patch, identical plan, command execution, ToolFinish success, agent text) are killed in the small lane. Static: classifier ignores CommandExecution/AgentMessage; on_tool_finish never records state changes; identical plans compare steps/status only; refused spawn emits Failed, which the classifier excludes. Residual partial ignore-arm execution coverage is retained as structured note finding B-N1."
    },
    {
      "row": "code-mode leaf accounting",
      "result": "held",
      "reason": "Real-path nested-patch exactly-once test plus wrapper-only control green on snapshot core; double-emit mutant killed in core (log-confirmed: exactly-once test fails under mutant-3). Classifier gives 1 for leaf FileChange Completed plus exec ToolFinish plus shell item, 0 without the leaf. Wrapper emits no turn item (execute_handler has zero emissions; nested call ids are broker-generated). Files byte-identical to rev2 green tree."
    },
    {
      "row": "no model-writable bypass",
      "result": "held",
      "reason": "Observation writers are host-completed classification, post-store goal mutation calls, and the plan-commit callback; SpawnAgentArgs and other tool args carry no count/force field. Plan comparator takes &[PlanItemArg] (step+status only, plan_tool.rs:17-20), so explanation is structurally unreachable. Bypass tests green on snapshot small; keyword mutant killed. The V1 spawn defect class is closed by a host delivery binding, not a model-settable value."
    },
    {
      "row": "existing activity and blocker untouched",
      "result": "held",
      "reason": "record_tool_outcome, record_item, empty_response_goal, finish_turn are 4/4 byte-identical base-to-candidate (verified by extraction). Observation state is separate and never read by the blocker. Empty-blocker tests (fires first with and without a separately recorded observation) green on snapshot small alongside the existing suites."
    },
    {
      "row": "transient state",
      "result": "held",
      "reason": "Counts live in the in-memory turn map removed by finish_turn; plan memory is in-memory thread state. on_thread_resume reconciles and restores only idle/active markers and metrics (runtime.rs:585-603); no observation counts cross resume. Unit plus backend fresh-runtime transience tests green on snapshot small. No rollout/history/protocol write carries the field."
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "reason": "Defaulted on_plan_committed hook keeps existing contributors compatible; PlanCommitInput borrows stores/plan. Core adds a thin handler call, contributor fan-out, and the two delivery-status bindings; classification stays in the goal extension. No core-to-goal dependency, no new wire schema, config, dependency, or persisted field. Lint plus extension-api suites green on the exact tree."
    }
  ],
  "free_hunt": [
    "[TASK-261011-wcmuu1] {\"attack\": \"V1 spawn emission cardinality on every path\", \"result\": \"held\", \"evidence\": \"One emit_turn_item_started plus exactly one emit_turn_item_completed per handler invocation past the depth check; the completed emission precedes result propagation so Err emits Failed; depth-limit refusal returns before any emission (conservative, correct: a refused spawn is no observation). Telemetry failure record is counter-only, not a turn item.\"}",
    "[TASK-261011-wcmuu1] {\"attack\": \"Consumers of the changed SpawnAgent item status\", \"result\": \"held\", \"evidence\": \"TUI renders terminal cells for Completed and Failed alike; analytics success/error mapping change is consistent with the tool call having succeeded (same class as the rev1 send_input fix); exec mapping is a passthrough; app-server SpawnBegin/InteractionEnd mappings are V2-event paths, untouched. agents_states preserves Errored for display everywhere.\"}",
    "[TASK-261011-wcmuu1] {\"attack\": \"Dead code or lint risk from dropping collab_tool_call_status use\", \"result\": \"held\", \"evidence\": \"spawn.rs imports via use super::* (glob), so no unused-import lint; the status variable is still consumed by agents_states construction. Hosted lint lane is green on this exact tree.\"}",
    "[TASK-261011-wcmuu1] {\"attack\": \"New mutant narrows instead of deleting\", \"result\": \"held\", \"evidence\": \"spawn_status_ignores_delivery_result reverts exactly the 9-line delivery-binding hunk to the sampled-status proxy. Under it the accepted-with-errored test fails (Failed instead of Completed) while the refused control stays green (log-confirmed), so the mutant narrows the accepted/refused boundary rather than deleting the gate.\"}",
    "[TASK-261011-wcmuu1] {\"attack\": \"Rev1 closures still hold on this tree\", \"result\": \"held\", \"evidence\": \"send_input delivery binding intact (file rev2-identical); code-mode real-path, paused/blocked dispatch, external set/clear production-site, and message-variant kills all re-executed on precheck 7 with the same named killers. Rev2-to-rev3 delta touches only spawn.rs plus its tests.\"}",
    "[TASK-261011-wcmuu1] {\"attack\": \"Turn-id consistency across record paths\", \"result\": \"held\", \"evidence\": \"Rev2-verified single id family across start_turn, on_item_completed, on_plan_committed, goal tools, and external set/clear is unchanged (those files are rev2-identical); spawn.rs touches no turn ids.\"}",
    "[TASK-261011-wcmuu1] {\"attack\": \"Evidence identity confusion (workflow head vs snapshot, mutant mismatch)\", \"result\": \"held\", \"evidence\": \"Snapshot commit tree independently equals candidate; all 16 mutant commits are snapshot children whose trees equal local replay of the attached patches; failing lanes and log-confirmed killers match the precheck table. Workflow head_sha is the definition commit, not test input, and was not used as evidence.\"}"
  ]
}
```
