# TASK-261011-16oznh — R141 DELTA panel, CR revision 3

accept

Replay check: **exact match**. Temporary-index replay of
`TASK-260929-3ld28o_change-request_rev3.patch` on base
`07c018be3507b8d4a5558a85a117b94ed2a23872` produced
`486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7`, exactly the expected candidate.
No nested worktree, build, Rust command, source edit or source-task write.
All seven surface rows have exactly one result: **7/7 held**.
Prior merged findings **2/2 addressed**; no new blocking findings.

Commands run directly in this panel (replay/gates are standalone processes):

| Command | Actual exit / evidence |
|---|---|
| `task-board m 'set_status(TASK-261011-16oznh, status=analysis)'` | 0; panel task only |
| `mkdir -p .temp` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-16oznh-replay.idx" git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872` | 0 |
| `task-board resource get TASK-260929-3ld28o TASK-260929-3ld28o_change-request_rev3.patch --output .temp/TASK-260929-3ld28o_change-request_rev3.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-16oznh-replay.idx" git apply --cached .temp/TASK-260929-3ld28o_change-request_rev3.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-16oznh-replay.idx" git write-tree` | 0; exact candidate tree above |
| `task-board q 'get(TASK-260929-3ld28o) { description scope ac }'` | 0 |
| `task-board resource get TASK-260929-3ld28o <resource> --output <scratch-file>` for surface-table, prior merged verdict, producer brief, results, hosted precheck 7, mutants and rev3 validation | Each 0; read-only |
| `git diff --stat 07c018be3507b8d4a5558a85a117b94ed2a23872 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7` | 0; 17 paths +1828/-7 |
| `git diff 568588edd89a50d4f259f9e17eb902cd38ae9e8e 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7` | 0; spawn.rs and multi_agents_tests.rs only |
| `git diff --check 07c018be3507b8d4a5558a85a117b94ed2a23872 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7` | 0 |
| `gh run view 38083359851 --repo ivanopcode/codex --json status,conclusion,headSha,jobs,url` and compact projection | Each 0; overall conclusion failure, four snapshot/lint lanes success |
| `gh api repos/ivanopcode/codex/git/commits/eb345af5e4085cf3120a250904ef85389037a8e3` with projection | 0; exact candidate tree and base parent |
| `gh run view 38083359851 --repo ivanopcode/codex --job <id> --log` | Each 0 for plan 114304659447, lint 114304675139, snapshot small 114306081168, core 114306081213, app-server 114306081245, and every failing mutant job below |
| `python3` standalone source equality/inventory audit | 0; every inspected `git show` 0; four methods identical, test-fed variants 5/19 |
| `python3` standalone hosted-mutant identity audit | 0; each of 16 `gh api .../git/commits/<sha>` 0; each per-mutant standalone `git read-tree <candidate>`, `git apply --cached <patch>` and `git write-tree` 0; matches 16/16 |
| `python3` standalone hosted-killer log audit | 0; metadata/log fetches 0; 16/16 relevant killers fail, runner exits each 100 |
| `task-board spawn directives RUN-261011-19a823` | 0; no directives |
| `python3 .temp/16oznh-validate-verdict.py` | 0; one valid findings block, seven unique expected rows, required keys and verdict checked |

Exploratory command failures were not gates and were not represented as passes:
initial `get(...){... resources ...}` exited 1 (unknown field), repaired using
`preconditionResources outcomeResources` (exit 0); skill-relative reviewer-role
`cat` exited 1 (missing), recovered via `~/.roles/reviewer/role.md` (exit 0);
file-discovery `rg` searches with no matches exited 1. Candidate materialization
initially probed four nonexistent paths with `git show` exit 128; correct V2
message/spawn and `core/src/tools/code_mode/execute_handler.rs` were then read
with exit 0. The initial combined mkdir/remove/read-tree request was refused
before process creation because it contained `rm -f` (no process exit code);
the safer separate mkdir/read-tree replay above succeeded without removal.
No review conclusion relies on a failed or unreadable input.

Evidence sources: all source paths below are pinned to candidate tree above,
not ambient worktree HEAD. Board sources (read-only): `surface-table.md`,
`TASK-260929-3ld28o_review-verdict-rev2.md`,
`TASK-260929-3ld28o_results.md` revision 8,
`TASK-260929-3ld28o_hosted-precheck-7.md`,
`TASK-260929-3ld28o_mutants.json`, and
`TASK-260929-3ld28o_change-request_rev3-validation.log`.
Hosted evidence: [relux-ci run 38083359851](https://github.com/ivanopcode/codex/actions/runs/38083359851)
and [exact snapshot Git commit](https://github.com/ivanopcode/codex/commit/eb345af5e4085cf3120a250904ef85389037a8e3).
The panel reran replay, source audits, hosted identity checks and artifact
validation itself; it **reused** hosted suites and mutants, without executing
Rust checks locally. CR local command shard is 1/1 green; test-case coverage
is unknown. Hosted snapshot/lint numeric exits are not explicitly printed;
job/step conclusions are success. Every expected-red mutant exit below is
observed as 100, never represented as passing.

Hosted mutation evidence, independently matched to attached patches:

| # | Mutant / hosted commit | Named failing tests | Failing job | Gate exit | Tree match |
|---|---|---|---|---|---|
| 1 | `agent_message_counts_as_state_change` / `02206238a095454833328b631b9ccfe9afec035d` | `model_text_claiming_progress_does_not_set`, `no_model_writable_bypass_sets_observation` | [mutant-1 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306081223) | 100 (expected failure) | `f2340ad27876664e9de2da33a0a4bfe31c924ebe` exact |
| 2 | `agent_message_state_keyword_counts` / `3dccd02ca7a01837918b88971043a68cc1ce8964` | `model_text_claiming_progress_does_not_set`, `no_model_writable_bypass_sets_observation` | [mutant-2 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306081165) | 100 (expected failure) | `18f4c1f5dfd70dcf46d374192e35774d3165b684` exact |
| 3 | `code_mode_nested_file_change_emitted_twice` / `144e577d088821fe443cb994d400e0e472bf6f75` | `suite::code_mode::code_mode_leaf_applied_patch_delivered_exactly_once` | [mutant-3 core](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306081252) | 100 (expected failure) | `2e496bbb3303674d08395e54d1a3b9ead182b4ea` exact |
| 4 | `command_execution_counts_as_state_change` / `88f939d2676b0823c1bc46ef694de963fbfc41f2` | `code_mode_leaf_counts_once_and_wrapper_adds_none`, `shell_success_does_not_set_observation` | [mutant-4 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306081169) | 100 (expected failure) | `afe487fd638a7a8517bab7aa16bd7cea1c1682ad` exact |
| 5 | `external_goal_clear_does_not_record` / `4c8c89adf02f6cbb16987db00d2630bd6e41d7cb` | `state_change_observation::backend_external_goal_set_and_clear_record_observation` | [mutant-5 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306081187) | 100 (expected failure) | `d256d2e2925fd872a848db3dfb59deff9fc18f55` exact |
| 6 | `external_goal_set_does_not_record` / `0d34bdf5b776859d5bea68c7bc203d6c403db325` | `state_change_observation::backend_external_goal_set_and_clear_record_observation` | [mutant-6 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306081196) | 100 (expected failure) | `047797960a7328bb513cf9a13198a9416bf3f165` exact |
| 7 | `file_completed_requires_auto_approved` / `a9717fc656dd042058814cb6046c0ef8ac31d88c` | `applied_file_change_sets_observation`, `code_mode_leaf_counts_once_and_wrapper_adds_none`, `state_change_observation::backend_file_change_completed_sets_observation`, `state_change_observation::backend_fresh_runtime_carries_no_observation` | [mutant-7 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306082231) | 100 (expected failure) | `3bc2020bdd27716f053972696659400e19737cf4` exact |
| 8 | `file_failed_counts_as_applied` / `96eeec548ef40b91a155a3e7b3f733ceea5a8807` | `failed_or_declined_file_change_does_not_set`, `state_change_observation::backend_file_change_completed_sets_observation` | [mutant-8 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306082209) | 100 (expected failure) | `dba722312a027a6d7425aafb9c7e4cda4b1227e1` exact |
| 9 | `goal_update_complete_only_records` / `dba10726635cb732700d1c3288e453478e1db1f5` | `state_change_observation::backend_goal_update_paused_and_blocked_set_observation` | [mutant-9 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306082267) | 100 (expected failure) | `54a129bdcb152c9cc679694d3200669d015f9000` exact |
| 10 | `identical_plan_always_counts` / `cf3e7bc446dd57646987eb74d8c7b7a5a6f2d157` | `identical_plan_resubmission_does_not_set`, `no_model_writable_bypass_sets_observation`, `state_change_observation::backend_plan_transition_sets_and_identical_does_not` | [mutant-10 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306082322) | 100 (expected failure) | `afebd870f6cf3ea6df14503ea5267b9ed1665f31` exact |
| 11 | `plan_transition_ignores_content` / `bceadc587cda06b36edb71257f6c26e3c8734512` | `plan_status_change_counts_as_transition`, `plan_step_text_change_counts_as_transition`, `state_change_observation::backend_plan_transition_sets_and_identical_does_not` | [mutant-11 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306082436) | 100 (expected failure) | `bad6d3bd250afceb5ea11efd6ce0a518842e0a87` exact |
| 12 | `send_input_status_ignores_delivery_result` / `910966b8f30b1ca4a0e86c7666b8528953d5a754` | `suite::scenarios::guardian_agent_messages::encrypted_parent_reply_survives_incremental_guardian_reviews`, `tools::handlers::multi_agents::tests::send_input_rejected_compaction_emits_failed_item` | [mutant-12 core](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306083100) | 100 (expected failure) | `83132cec18bea06a58a04b6607e5ca320df338bd` exact |
| 13 | `spawn_followup_message_tools_dropped` / `ba4fa2d79ab75f1143d160c1be6cc5ddbc5ddae9` | `send_message_and_followup_task_completed_set_observation` | [mutant-13 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306083320) | 100 (expected failure) | `ca057805aa94cc8992877bdf28c2d76797716dbe` exact |
| 14 | `spawn_only_spawn_agent_counts` / `f744d81992699732142076b726c90c6f10dc3063` | `send_input_completed_sets_observation`, `send_message_and_followup_task_completed_set_observation` | [mutant-14 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306083188) | 100 (expected failure) | `f72369189054bd22732030df4543aef2ddc30394` exact |
| 15 | `spawn_status_ignores_delivery_result` / `01f0eb5cc5d87fc2e7575e38b5425a069012eaaa` | `tools::handlers::multi_agents::tests::spawn_agent_accepted_with_errored_child_emits_completed_item` | [mutant-15 core](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306083295) | 100 (expected failure) | `e5924ad6cf8bf60ac15c87c9414cd5670222ee8d` exact |
| 16 | `tool_finish_success_records_mutation` / `edef3c5090146f38bba9e1636e9678a36869885e` | `state_change_observation::backend_spawn_followup_sets_but_tool_finish_success_does_not` | [mutant-16 small](https://github.com/ivanopcode/codex/actions/runs/38083359851/job/114306083436) | 100 (expected failure) | `2b1e53a0d7130fb533a01e63f7a97369b31cc059` exact |

Logbook, 2026-10-11 (task-scoped): replay exact; rev2 A-F1/D-F1 closed by
receipt-based V1 spawn mapping and the exact-tree accepted-errored killer.
All supplied hosted mutants independently identified and replay-matched,
16/16 killed. Previous partial-ignore coverage and change-size advisories
retained with explicit bounds. Mutant-12 has an additional guardian-message
failure, while its intended refusal killer also fails; no unsupported causality
claim. Overall hosted run is expected-red despite green snapshot lanes.
No mutations were recorded on the source task. Research verdict is ready for review.

Successor recovery, RUN-261011-0d3111 (2026-10-11):

The command table above describes the predecessor panel run
RUN-261011-19a823. This successor reused its saved static sweep and hosted
execution evidence; it did not re-execute those suites or the 16 mutants.
It independently reran the mandatory candidate replay and checks below.
The candidate, attached corpus and hosted run identities remain unchanged.

| Successor command / check | Actual exit / evidence |
|---|---|
| `task-board m 'set_status(TASK-261011-16oznh, status=analysis)'` | 0 |
| `git rev-parse --show-toplevel`, `mkdir -p .temp` | 0 each |
| `python3 -c 'from pathlib import Path; Path(".temp/TASK-261011-16oznh-replay.idx").unlink(missing_ok=True)'` | 0; removed only the scratch index |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-16oznh-replay.idx" git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872` | 0 |
| `task-board resource get TASK-260929-3ld28o TASK-260929-3ld28o_change-request_rev3.patch --output .temp/TASK-260929-3ld28o_change-request_rev3.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-16oznh-replay.idx" git apply --cached .temp/TASK-260929-3ld28o_change-request_rev3.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-16oznh-replay.idx" git write-tree` | 0; exact tree 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7 |
| Source/panel `task-board q ...` projections using `preconditionResources outcomeResources`, and source AC query | 0 each |
| Resource reads for panel rev1 validation and source rev2 recording refusal | 0 each |
| `git diff --check 07c018be3507b8d4a5558a85a117b94ed2a23872 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7` | 0; standalone rerun |
| `gh api repos/ivanopcode/codex/git/commits/eb345af5e4085cf3120a250904ef85389037a8e3 --jq '{tree: .tree.sha, parents: [.parents[].sha]}'` | 0; exact candidate and base parent |
| `gh run view 38083359851 --repo ivanopcode/codex --json status,conclusion,jobs` with compact lane projection | 0; four snapshot/lint lanes success; overall expected-red failure |
| Standalone `python3` source-method/evidence audit | 0; `git show` base/candidate exit 0 each; 4/4 original methods identical; 16/16 saved mutant identity records and exit-100 logs rechecked |
| `python3 .temp/16oznh-validate-verdict.py` | 0; successor artifact validation, seven rows and advisory finding schema |
| `task-board spawn directives RUN-261011-0d3111` | 0; none |
| `git status --porcelain=v1 --untracked-files=all`, `git check-ignore .temp/TASK-261011-16oznh/artifacts/RESEARCH.md` | 0 each; clean source worktree and ignored research storage |
| Panel-only `task-board resource update ...`, `set_notes(...)` and `resource get ...` | 0 each; updated verdict attached and fetched |
| Standalone `python3` attached-outcome byte-equality, verdict-schema and clean-worktree check | 0; exact attached bytes, one valid block, all seven rows once, zero source changes |

Successor exploratory failures: two unsupported `resources` projections
exited 1; missing skill-relative reviewer-role read exited 1; search with
absent `artifacts` path exited 2. Each was recovered by valid projections,
`~/.roles/reviewer/role.md`, or existing artifact reads. `rm -f` scratch-index
removal was rejected before process creation, so it has no exit code; the
Python unlink above succeeded. No failed exploratory read supported a verdict.

Logbook, successor recovery: the predecessor's own research handoff validation
failed with **exit 1**, because its untracked `.research` verdict was captured
as a source delta whose tree had no hosted green record. This is the panel's
handoff failure, not a failure of the reviewed source candidate. The verdict
is retained as an outcome resource and the local research copy is relocated
under ignored `.temp/TASK-261011-16oznh/artifacts/RESEARCH.md`, leaving no
repository delta. The project-management CR runbook's research-only path
skips source validation for an empty delta and still publishes for review.
No gate configuration, source, branch, index or authority was changed.
No build was run. B-N1 is retained as structured nonblocking D-N1, following
`TASK-260929-3ld28o_recording-review-refusal-rev2.md`; the two blocking prior
findings remain addressed. Source task remains read-only.

```verdict-findings
{
  "findings": [
    {
      "id": "D-N1",
      "row": "non-resets",
      "invariant": "AC2/AC8: ignored item classes must remain ignored; execution coverage should expose a regression that starts recording one.",
      "mechanism": "Retained rev2 B-N1 advisory. Classifier-focused tests directly construct 5/19 TurnItem families. Fourteen other ignored families (UserMessage, FunctionCallOutput, HookPrompt, Plan, Reasoning, DynamicToolCall, WebSearch, ImageView, Extension, ImageGeneration, EnteredReviewMode, ExitedReviewMode, McpToolCall, ContextCompaction) lack distinct executed ignore-arm feeds. Production explicitly enumerates every variant without a wildcard, and the five AC2 categories have hosted killers. Exhaustiveness prevents omission of a new variant but cannot prevent recording an existing ignored variant. No executed surviving mutant or observed product failure is claimed.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/accounting.rs:289-335 and classifier-focused observation test files (static inventory)",
          "command": "Static inspection on 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7: git show <candidate>:codex-rs/ext/goal/src/accounting.rs; compare TurnItem inventory and test feeds using the saved source audit. No Rust test executed locally.",
          "expected_failure": "Unknown/unexecuted: to measure the gap, feed each remaining ignored family at the goal callback and narrow the ignore match to record that family; require the corresponding new negative test to fail. Existing suite survival is not asserted."
        }
      ],
      "severity": "note",
      "repeat-of": "rev2/B-N1"
    }
  ],
  "notes": [
    "Scope: independent non-recording DELTA panel on CR-TASK-260929-3ld28o-3, candidate 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7, base 07c018be3507b8d4a5558a85a117b94ed2a23872. All board writes are restricted to TASK-261011-16oznh. No accept_cr, reject_cr, withdraw_cr, set_status, handoff, resource, checklist or notes mutation was issued on TASK-260929-3ld28o.",
    "Prior merged verdict rev2 contains exactly two findings (A-F1 and D-F1), both describing the same V1 accepted-spawn/liveness mechanism. Audited 2/2; production fix and deterministic handler-boundary tests address both correctly. The new test pins mapping rather than measuring async real-child race incidence, which remains unknown. Rework changes exactly two files relative to rev2; no unrelated accounting logic changed.",
    "Prior B-N1 advisory retained. Source-derived TurnItem inventory is 19 variants; classifier-focused tests directly construct 5/19 (FileChange, CollabAgentToolCall, SubAgentActivity, CommandExecution, AgentMessage). Additional un-fed ignore families: UserMessage, FunctionCallOutput, HookPrompt, Plan, Reasoning, DynamicToolCall, WebSearch, ImageView, Extension, ImageGeneration, EnteredReviewMode, ExitedReviewMode, McpToolCall, ContextCompaction. Exhaustive production match prevents implicit fallthrough but does not constitute executed negative coverage for those 14. No executed survivor is claimed; the five AC2 non-reset categories are covered.",
    "Hosted exactness independently verified, rather than inferred from workflow headSha. Plan and snapshot checkout name eb345af5e4085cf3120a250904ef85389037a8e3; GitHub git-commit API returns exactly candidate tree 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7 with parent base 07c018be3507b8d4a5558a85a117b94ed2a23872. Workflow headSha e0eff057620104a416080da616256ee7f32bda1b identifies the workflow definition and is not the test-input tree.",
    "Executed attack evidence reused from run 38083359851. Lint and snapshot small/core/app-server jobs succeed. Small: 948/948 passed, 1 skipped; core: 5081/5081 passed, 11 skipped, 3 flaky tests recovered by retries; app-server: 1833/1833 passed, 2 skipped. Overall workflow conclusion is failure because expected-red mutant lanes fail. Numeric snapshot/lint process exit codes are not explicitly printed in these logs; successful job/step conclusions are reported as such, not invented local exits.",
    "All 16 attached mutant patches replay to their respective hosted commit trees (16/16), all 16 hosted commits have the exact snapshot as parent, and all 16 fail a named relevant killer with runner exit 100 (16/16 killed, 0/16 survivors). This ratio applies to the supplied mutant corpus, not all possible paths or mutations. Mutant-12 also hit an unrelated guardian-message scenario failure; the named send_input refusal killer fails independently, so its kill does not depend on that extra failure.",
    "CR rev3 validation log records mini-hosted-gate.sh exit 0, coverage_unit=exact_command_shard required=1 green=1 failed=0 missing=0; test_case_coverage=unknown. Accepted as attached evidence; not rerun locally. No cargo, just, build, lint, formatting or Rust test command was run by this panel.",
    "AC7 stated bound verified in results revision 8: arbitrary shell side effects are UNKNOWN; pacing may stay conservative and completion is never inferred from shell output or exit status. Automatic goal stops and usage-accounting writes remain excluded as previously reviewed. Plan memory is thread-global, so identical plans across goals are not a transition. These are maintained documented bounds, not new regressions.",
    "Large-diff advisory retained: 17 paths +1828/-7 exceeds 800-line guidance, mainly test scaffolding/coverage; roughly 300 production lines. Split suggestion is the defaulted plan hook + thin core dispatch/test, then goal consumer and remaining tests. No code restructuring was performed in this read-only panel.",
    "Successor recovery RUN-261011-0d3111: retain the B-N1 advisory as structured D-N1 (severity note, repeat-of rev2/B-N1) because the rev2 recording-review refusal explicitly identified loss of this object during merging. This is advisory evidence preservation, not a new blocking implementation defect. Verdict remains accept; all seven rows remain held."
  ],
  "surface_results": [
    {
      "row": "reset sources at committing handlers",
      "result": "held",
      "reason": "Four reset-source families swept. accounting.rs:289-335 records only Completed FileChange, Completed spawn/send collaboration items, and Started/Interacted subagent activities; extension.rs:344 invokes it only on item completion (session/mod.rs:2623-2641). PlanHandler publishes then calls notify_plan_committed; extension.rs:526 compares steps/status, not explanation. Goal create/update record after successful DB results (tool.rs:250,321); external set/clear follow committed-state reconciliation (runtime.rs:394,445), with read failure propagated. Rev2 A-F1/D-F1 are fixed by result.is_ok() in V1 spawn.rs:181-185, with liveness retained separately. Snapshot core passes accepted-errored and refused-spawn tests; mutant-15 core exit 100 kills the accepted-errored boundary. V1 send_input uses the same receipt rule, and mutant-12 core kills Compact refusal. V2 spawn/message emit Started/Interacted after successful receipts, without consulting liveness for observations. File, plan, goal-update, external-set/clear and message narrowing attacks all have named kills in the exact-tree hosted run. Observation proof composes real handler emission with executed goal classifier/callback tests; no real-child race-frequency measurement is claimed."
    },
    {
      "row": "non-resets",
      "result": "held",
      "reason": "All five AC2 categories have named executed tests: failed_tool_does_not_set_observation/failed_or_declined_file_change_does_not_set, identical_plan_resubmission_does_not_set, shell_success_does_not_set_observation, code_mode_leaf_counts_once_and_wrapper_adds_none plus the real wrapper-only control, and model_text_claiming_progress_does_not_set. Hosted mutants 1,4,8,10,12,16 fail with exit 100. ToolFinish success changes only old activity state, not observation; CommandExecution and AgentMessage are ignored; identical plan compares step/status. Failed/refused spawn and send map to Failed and do not increment. Bound: the classifier-focused tests directly feed 5/19 TurnItem families; the other 14 ignored families are statically handled by the exhaustive match, without a distinct executed ignore-arm test for each."
    },
    {
      "row": "code-mode leaf accounting",
      "result": "held",
      "reason": "Two real public-entry scenarios pass in snapshot core: functions.exec -> nested apply_patch writes the file and delivers exactly one Completed FileChange, no CommandExecution and no wrapper-call-id item; wrapper-only exec -> nested read-only exec_command delivers zero FileChange, exactly one nested CommandExecution and no wrapper item. core/tests/suite/code_mode.rs:6850 onward uses a registered turn contributor and the real broker path. Mutant-3 core duplicates the completed leaf emission and fails code_mode_leaf_applied_patch_delivered_exactly_once (exit 100). Goal classifier/callback tests compose Completed leaf -> one count, command/ToolFinish -> zero. core/src/tools/code_mode/execute_handler.rs emits no turn item of its own. The two-link delivery/classification proof is explicit; no single end-to-end public count assertion is claimed."
    },
    {
      "row": "no model-writable bypass",
      "result": "held",
      "reason": "Writers are private host accounting methods reached by committed items, post-store goal calls, and the plan hook. Runtime exposes read-only count/boolean accessors. No tool schema, response, history item or model-controlled force/count field was added. record_plan_transition takes &[PlanItemArg], excluding explanation. no_model_writable_bypass_sets_observation feeds magic plan/message/tool text and preserves only the legitimate first-plan count; text and keyword mutants 1/2 both fail with exit 100. Source inspection verifies content does not set the count except as a legitimate changed plan or committed action."
    },
    {
      "row": "existing activity and blocker untouched",
      "result": "held",
      "reason": "Independent source equality audit verifies record_tool_outcome, record_item, empty_response_goal and finish_turn are 4/4 byte-identical to base; command exit 0. The separate count is never consumed by the existing blocker, and on_turn_stop ordering is unchanged. Hosted small passes empty_blocker_still_fires_first_with_no_observation and observation_does_not_disturb_empty_blocker: the third empty continuation triggers with or without an observation. Existing core and goal suites pass on this exact snapshot; no pacing timer is introduced in this leaf."
    },
    {
      "row": "transient state",
      "result": "held",
      "reason": "Count is a private u32 in in-memory GoalTurnAccounting, initializes to zero and disappears when finish_turn removes the turn; plan memory is private in-memory GoalAccountingInner. Neither type is serialized. Thread start initializes default accounting in fresh ExtensionData; resume restores persisted goals without importing observation fields. observation_is_transient_per_turn, fresh_state_carries_no_observation_or_plan_memory and backend_fresh_runtime_carries_no_observation pass in hosted small. The backend fresh runtime shares the same DB and still reports zero. Bound: this is fresh-runtime execution plus persistence/resume source inspection, not a public JSON-RPC resume-count assertion."
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "reason": "New defaulted ToolLifecycleContributor::on_plan_committed preserves existing implementations; PlanCommitInput borrows existing stores/plan and adds no model-visible context. The core handler and fan-out remain thin; goal accounting owns classification. The real plan_committed_hook_fires_for_successful_update_plan passes in snapshot core, and extension-api/small plus hosted lint are green. No new crate dependency, configuration, schema, CLI flag, rollout field or core->goal dependency was added. V1 collaboration completion status deliberately becomes receipt-based while agents_states retains presentation liveness. The existing V2 analytics proxy is not emitted as a turn item and is not an observation bypass. Size advisory: full CR is 17 paths +1828/-7; rev3 delta is only spawn.rs and multi_agents_tests.rs (+333/-1). Defaulted plan hook, core fan-out and its integration test remain the smallest coherent staging option."
    }
  ],
  "free_hunt": {
    "bound": "After auditing prior findings, swept every surface row, then inspected sibling V1/V2 acceptance mappings, item-start/completion delivery, private observation writer/readers, goal reconcile failures, wire/persistence surfaces and change-size/test identity. Static attack plus exact-tree hosted evidence; no builds.",
    "attacks": [
      {
        "target": "Acceptance versus child liveness siblings",
        "result": "held",
        "reason": "V1 spawn/send are result-bound. Remaining collab_tool_call_status users are V1 resume/close (excluded from observation) and V2 spawn analytics; V2 observation comes from receipt-success Started, not the analytics item. V2 messages use a common receipt-success Interacted path. No additional liveness-proxy observation defect found."
      },
      {
        "target": "Started/completed double counting and code-mode wrapper",
        "result": "held",
        "reason": "Goal writes only at on_item_completed. emit_sub_agent_activity starts then completes one item; only completion is classified. Real nested-patch duplicate-emission mutant is killed. Wrapper emits no turn item."
      },
      {
        "target": "Failed reads versus legitimate goal absence",
        "result": "held",
        "reason": "External set/clear reconcile_live_activity returns Result and is awaited with ?, before the committed/absence decision. Error cannot flow into the committed.is_none() fallback. The changes preserve the pre-existing reconciliation failure behavior."
      },
      {
        "target": "Observation persistence, context exposure and caller inventory",
        "result": "held",
        "reason": "No new serialization, rollout/history/context fragment, dependency or schema surface; private writers are confined to goal source and host callbacks. Runtime count accessors are read-only for the next pacing leaf. Original activity methods are byte-identical."
      },
      {
        "target": "Residual test-coverage and size advisories",
        "result": "held",
        "reason": "5/19 directly fed TurnItem families and oversized total diff remain stated advisories. They are not presented as universal coverage or newly executed defects."
      }
    ],
    "new_blocking_findings": 0,
    "unexecuted_requested_attacks": []
  }
}
```
