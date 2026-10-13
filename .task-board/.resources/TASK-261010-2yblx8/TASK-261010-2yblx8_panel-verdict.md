# Panel B verdict — TASK-260929-3ld28o CR rev2 (R141, non-recording)

Verdict: accept

Scope: Change Request CR-TASK-260929-3ld28o-2 revision 2 of TASK-260929-3ld28o
(state-change-observations). Independent panel B review; NOT the recording
reviewer. No accept/reject/withdraw/status/handoff/resource/note write was
issued on TASK-260929-3ld28o (read-only review).

## Replay tree check (mandatory, first) — MATCH

Base commit 07c018be3507b8d4a5558a85a117b94ed2a23872 exists (commit).
Patch TASK-260929-3ld28o_change-request_rev2.patch applied through a temporary
index (never a nested worktree). write-tree printed
568588edd89a50d4f259f9e17eb902cd38ae9e8e — exactly the expected candidate tree.
Base-to-candidate diff lists exactly the 16 CR paths (10 production, 6 test).

## Commands run, with exit codes

- git cat-file -t 07c018be... -> commit — exit 0
- task-board resource get TASK-260929-3ld28o <rev2 patch> — exit 0 (69783 bytes)
- GIT_INDEX_FILE=temp.idx git read-tree <base> — exit 0
- GIT_INDEX_FILE=temp.idx git apply --cached <rev2 patch> — exit 0
- GIT_INDEX_FILE=temp.idx git write-tree -> 568588edd89a50d4f259f9e17eb902cd38ae9e8e — exit 0
- task-board resource get x13 (surface-table, producer-brief, final-plan,
  results, mutants, hosted-precheck-6, handoff-note-6, rev1 verdict,
  rev2 validation log, 2 rework briefs, precheck-4, mini addendum) — exit 0 each
- git archive <candidate> <10 production paths> | tar -x — exit 0
- git diff --name-only <base> <candidate> -> 16 paths — exit 0
- git apply --check for each of the 15 mutant patches against the full
  candidate tree — all clean, exit 0 each (15/15)
- git show / git grep reads on the candidate tree (all probes below) — exit 0
- No cargo, just, build or test command was run (forbidden by the panel
  brief; the shared build target is serialized). Execution evidence is the
  CR validation log plus hosted relux-ci precheck 6 on the exact tree.

## Row sweep summary

All 7 surface rows attacked statically and held; rev1 merged findings
A-F1, A-F2, A-F3, F1, F2 are closed by production fix or executed,
mutant-killed coverage on the exact candidate tree (precheck 6, run
38047301443: lint/core/app-server/small success, 15/15 mutants killed).
One note-severity carryover (B-N1, rev1 panel-B F3 class) is recorded as a
finding object below; it does not block acceptance.

```verdict-findings
{
  "findings": [
    {
      "id": "B-N1",
      "row": "non-resets",
      "invariant": "AC2/AC8: every ignored item class stays ignored; a regression that starts recording one is caught.",
      "mechanism": "Ignore-arm execution coverage beyond AC2's five named non-resets is partial: tests feed FileChange(non-completed), AgentMessage, CommandExecution, a CollabAgentToolCall subset, SubAgentActivity(non-started) and ToolFinish-success to the classifier, while McpToolCall, DynamicToolCall, FunctionCallOutput, Plan, Reasoning, WebSearch, ImageView, Extension, ImageGeneration, EnteredReviewMode, ExitedReviewMode, ContextCompaction, UserMessage and HookPrompt never reach record_state_change_for_item in tests, so a regression that starts recording one would go undetected by the suite. Mitigated structurally: the match in ext/goal/src/accounting.rs:289-335 lists every TurnItem variant explicitly with no wildcard arm, so adding a recording arm requires touching the classifier and a new variant forces compile-time handling (non-exhaustive match is a compile error; hosted lint/type-check is green on this exact tree). Same observation class as rev1 panel-B note F3; the rev1 merged verdict carried it as a note, not a finding object, so repeat-of is none.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/accounting.rs (record_state_change_for_item, static read)",
          "command": "static inspection only: git show 568588ed:accounting.rs plus git grep of classifier feeds in the three observation test files; no build or test executed (forbidden by panel brief)",
          "expected_failure": "No failure observed and none claimed as executed: the ignore arm enumerates every TurnItem variant with no wildcard, so uncovered arms are compile-time-guarded. NOT a test execution."
        }
      ],
      "severity": "note",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Scope: CR-TASK-260929-3ld28o-2 rev2, candidate tree 568588edd89a50d4f259f9e17eb902cd38ae9e8e, base 07c018be3507b8d4a5558a85a117b94ed2a23872. Independent non-recording panel B. No source-task mutation of any kind was issued.",
    "Replay exactness passed: temp-index read-tree/apply/write-tree all exit 0, write-tree matches the expected tree exactly.",
    "Method: replay plus static attack; no cargo/just/build/test executed per the panel brief. Executed-attack evidence is hosted relux-ci run 38047301443 (precheck 6: lint/core/app-server/small all success on the exact candidate tree, snapshot equals worktree tree 568588ed, plus 15 narrowing-mutant runs, 15/15 killed, 0 survivors) and the CR rev2 validation log (mini-hosted-gate exit 0, exact_command_shard 1/1, test_case_coverage unknown). Hosted lane conclusions are cited as lane conclusions; individual process exit codes inside CI are unknown here and no expected-red run is presented as exit 0.",
    "Rev1 closure, verified on this tree: A-F1 fixed in production (send_input.rs delivery-bound status) and killed by send_input_rejected_compaction_emits_failed_item in the core lane; A-F2 covered by real-path code-mode tests (functions.exec to nested apply_patch with a recording contributor) with the double-emit mutant killed in the core lane; A-F3 covered by backend paused/blocked dispatch tests killing goal_update_complete_only_records; F1 covered through production GoalService set/clear call sites with both deletion mutants killed; F2 covered by SendMessage/FollowupTask Completed feeds killing spawn_followup_message_tools_dropped. Rev1 note F4 (wrong killer attribution in the results table) is fixed in results rev5.",
    "AC7 bound present verbatim in results rev5: arbitrary shell side effects are UNKNOWN; pacing stays conservative and completion is never inferred from shell output or exit status.",
    "Record-site inventory (10 sites, all at committing handlers/events, none in on_tool_finish): accounting.rs classifier arms x3, extension.rs on_item_completed and on_plan_committed, runtime.rs external set/clear x2, tool.rs create/update x2. on_tool_finish calls only record_tool_outcome (activity booleans); on_item_completed fires only from emit_turn_item_completed (session/mod.rs), so started items never reach the classifier.",
    "Protocol facts re-verified on the candidate tree: StepStatus exactly 3 variants (plans_equal pairwise match exhaustive); PlanItemArg carries only step+status and record_plan_transition receives &[PlanItemArg], so explanation is structurally unreachable; CollabAgentTool 9 variants (4 counted); SubAgentActivityKind 4 variants (Started/Interacted counted; Interrupted/Completed excluded, matching the AC wording).",
    "Change size 16 files / +1495 / -6 exceeds the 800-line guideline; production logic is ~290 lines and the rest is the AC8-mandated test plus mutant coverage. Advisory only, not a finding.",
    "Documented bounds accepted without findings: automatic goal stops and usage-accounting writes are excluded from goal-mutation observations (matches the rev1 accepted interpretation of committed goal mutation); last_committed_plan is thread-global so a cross-goal identical plan is not a transition (matches AC1 'differs from the previous plan'); an interrupt side effect on a refused send records nothing (conservative miss; interrupt is not an AC1 reset source); net-zero-but-Completed patches count as applied (host exit-0 semantics).",
    "Precheck-5 falsification incorporated: the rev3 premise that the exec wrapper 'arrives as CommandExecution' was disproven by hosted execution and corrected in rev4; verified here that execute_handler.rs contains zero turn-item emissions and nested leaves receive broker-generated {exec}-<uuid> call ids (delegate.rs), so zero wrapper observations holds because there is no wrapper item to classify."
  ],
  "surface_results": [
    {
      "row": "reset sources at committing handlers",
      "result": "held",
      "reason": "All four sources audited at their committing points. File changes: emit_patch_end emits Completed iff the apply exit code is 0 (Failed on message failure, Declined on rejection), once per end-stage. Plan: notify_plan_committed fires after successful parse and event publication; parse errors and Plan-mode rejection return before it. Goal mutations: create/update record only after the store write commits (None and Err return before); external set records only when live state equals the set goal, external clear only when a goal was actually deleted (clear_thread_goal gates apply on cleared_goal.is_some()). Spawn/follow-up: V1 send_input status is now delivery-bound (A-F1 fix); V1 spawn failure maps to (None, NotFound) -> Failed with status taken from the spawn result itself (no liveness race); V2 message/spawn emit activity only after the send/spawn ? commit, and the V2 CollabAgentToolCall record is private analytics, so each accepted spawn counts exactly once. 8/8 R-source mutants killed on the exact tree (precheck 6)."
    },
    {
      "row": "non-resets",
      "result": "held",
      "reason": "All five AC2 classes are executed and mutant-killed on the exact tree: failed tools (incl. the new Failed/InProgress SendInput unit link chained to the real-refusal core test), identical plan resubmission, shell success, wrapper success (plus proof the wrapper emits no item at all), and model progress claims. The classifier ignores CommandExecution, AgentMessage and every non-recording variant explicitly; ToolFinish success never records (on_tool_finish untouched, kill by the real-on_tool_finish backend test). B-N1 records the residual partial ignore-arm execution coverage as a note."
    },
    {
      "row": "code-mode leaf accounting",
      "result": "held",
      "reason": "Real-path coverage through functions.exec with a recording contributor: nested apply_patch delivers exactly one Completed FileChange, zero CommandExecutions, and no item with the wrapper call id; the wrapper-only control delivers exactly one nested CommandExecution and no FileChange. The double-emit mutant is killed by the exactly-once test in the core lane; the CommandExecution-counts mutant (a nested/direct exec leaf, not the wrapper) is killed premise-independently. Classifier composition (1 FileChange -> 1, CommandExecution -> 0) is unit-proven with killed mutants. The transient count is unreadable at any black-box entry after finish_turn, so delivery-plus-classifier composition is the documented proof shape."
    },
    {
      "row": "no model-writable bypass",
      "result": "held",
      "reason": "All observation writers enumerated: host item classification over committed items, post-store-commit mutation calls taking only turn_id, and the plan comparator over step/status only. No tool argument, plan text field, or message content reaches a count: PlanItemArg is step+status (explanation structurally excluded), keyword text is ignored by the classifier, and goal-tool args are validated/deserialized without copying unknown fields into accounting. Both keyword/text mutants killed with the bypass unit test as a named killer."
    },
    {
      "row": "existing activity and blocker untouched",
      "result": "held",
      "reason": "accounting.rs base-to-candidate diff has zero deletions (purely additive); record_tool_outcome, record_item, empty_response_goal and finish_turn are byte-identical. The only deletions in the CR are the plan.rs call_id/args rewire, the on_item_completed reindent (record_item call preserved verbatim), and the intended A-F1 send_input status line. The new count is separate state unread by the blocker; on_turn_stop ordering unchanged. Hosted precheck reports pre-existing suites plus the two new empty-blocker tests green."
    },
    {
      "row": "transient state",
      "result": "held",
      "reason": "Counts live only in the in-memory per-turn map (GoalTurnAccounting derives no Serialize; no rollout/history/store type touched; no observation reference exists outside ext/goal). finish_turn removes the turn; thread start builds GoalAccountingState::default() fresh; the on_thread_resume handler contains zero accounting/observation references so resume cannot revive counts. Fresh-state unit tests and the fresh-runtime backend test are green on hosted. Plan memory (last_committed_plan) is intentionally thread-scoped, not an observation."
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "reason": "New surface is one defaulted on_plan_committed hook plus the PlanCommitInput struct borrowing existing stores/plan; existing contributors stay source-compatible (default no-op). Core adds only the thin notify_plan_committed fan-out called from exactly one site (plan.rs after commit); no core->goal dependency (goal types referenced nowhere outside ext/goal); no model-context fragment, rollout, or wire change. Turn-id wiring verified consistent (sub_id) across start_turn, on_item_completed, on_plan_committed, goal tools, and external set/clear."
    }
  ],
  "free_hunt": [
    "{\"bound\": \"After the seven-row sweep, 8 focused probes on commit binding, identity wiring, and emission cardinality. No builds, no source mutation.\", \"probes\": [{\"area\": \"turn-id consistency across all five record paths\", \"outcome\": \"held: start_turn (sub_id via on_turn_start), on_item_completed (turn_store.level_id, constructed from sub_id), on_plan_committed (turn.sub_id), goal tools (invocation.turn.sub_id via to_extension_call), external set/clear (current_turn_id) all share one id family.\"}, {\"area\": \"V1 spawn failure/acceptance binding\", \"outcome\": \"held: Err maps to (None, NotFound) -> Failed; Ok status comes from the spawn result itself, so no A-F1-class liveness race exists for spawn.\"}, {\"area\": \"V2 double-count shape\", \"outcome\": \"held: V2 spawn/message emit exactly one public SubAgentActivity after the ? commit; the CollabAgentToolCall record is private analytics; V1 spawn emits no activity item. Each accepted spawn counts exactly once.\"}, {\"area\": \"no-op external clear\", \"outcome\": \"held: apply_external_goal_clear runs only when delete_thread_goal returned Some, so a clear with no live goal records nothing.\"}, {\"area\": \"external set commit gate\", \"outcome\": \"held: records only after reconcile_live_activity returns a committed goal equal to the set goal.\"}, {\"area\": \"patch emission cardinality\", \"outcome\": \"held: one emit_patch_end per terminal stage; Completed requires exit code 0; remaining callers are test-only.\"}, {\"area\": \"code-mode wrapper representation\", \"outcome\": \"held: execute_handler.rs has zero turn-item emissions; nested call ids are broker-generated, never the wrapper call id.\"}, {\"area\": \"resume revival\", \"outcome\": \"held: on_thread_resume references no accounting state; observations cannot be revived on resume.\"}], \"result\": \"All 8 probes held; no additional behavioral defect. Residual reliance from rev1 (no black-box end-to-end count assertion) remains inherently unassertable since the transient count has no production reader in this leaf; the delivery-plus-classifier composition with killed mutants on both links is the documented proof.\"}"
  ]
}
```
