# TASK-260929-3ld28o \u2014 state-change-observations: results

Revision 8 (review handoff on hosted precheck 7): V1 spawn
delivery-bound fix for merged-verdict-rev2 A-F1/D-F1. Worktree tree
`486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7` (base `07c018be`).
`git diff --name-only 568588ed 486ebfe5` prints exactly two paths
(`spawn.rs`, `multi_agents_tests.rs`); every other line is byte-identical
to the precheck-6 green tree `568588ed`. The two orchestrator test-only
edits from `b1-orch-compile-fix.md` (E0382 label fix,
`#![allow(clippy::expect_used)]` in
`ext/goal/tests/state_change_observations.rs`) remain in the tree.
Hosted precheck 7 is green on this exact tree. Review handoff is authorized by
`TASK-260929-3ld28o_handoff-note-7.md`; no repository file changed this run.

Successor-run fmt fix (test-only, whitespace): the rev6 tree's new
stub-`AgentControl` lines in `multi_agents_tests.rs` failed
`cargo fmt --check` (exit 1: three over-long `Box::pin(async { ... })`
one-liners plus one collapsible `record_usage` signature). rustfmt
expanded/collapsed those four spots only (+12/-3 within the file, no
token change); no mutant touches this file so `mutants.json` is
byte-identical and still 16/16 `git apply --check` clean.

Precheck history: precheck 6 (run 38047301443, tree `568588ed`) was
green with 15/15 kills and closed rev1 A-F1, A-F2, A-F3, F1, F2; it is
superseded by this rework. Precheck 4/5 are older history (see rev5).

## Finding responses (merged verdict rev2) \u2014 verified on hosted precheck 7

A-F1/D-F1 (same V1 spawn sibling, conservative missed reset) \u2014 FIXED in
production, killer test added, mutant attached. V1
`spawn_agent_internal` (`control/spawn.rs:849-870`) admits the initial
input, commits the reservation and disarms rollback, then samples
`get_status` into `LiveAgent.status` (`:890-894`) before returning Ok.
A child can error after admission, so an accepted result may carry
`AgentStatus::Errored`. `handle_spawn_agent` (`spawn.rs:150-152`)
copied that liveness into the completed item via
`collab_tool_call_status` (`multi_agents.rs:90-93` maps Errored to
Failed), while still returning a successful `SpawnAgentResult`. Goal
counting (`accounting.rs:296-306`) counts SpawnAgent only when
Completed, so an ACCEPTED spawn yielded 0 observations.

- Fix (core, `spawn.rs`, +9/-1, exactly as rev1 did for send_input):
  the emitted completed-item status is now bound to the spawn
  `result` at the committing path (Ok \u2192 Completed, Err \u2192 Failed);
  sampled child liveness stays in `agents_states` for display. The
  tool result itself still propagates unchanged. V2 spawn already
  uses a receipt-success Started activity and is left untouched.
- Regression test (core, real V1 `SpawnAgentHandler` + deterministic
  accepted-receipt fixture):
  `spawn_agent_accepted_with_errored_child_emits_completed_item`
  drives the handler with a stub `AgentControl` returning
  `Ok(LiveAgent)` with a real thread id and `Errored("boom")` status,
  asserting handler Ok with that agent id, a Completed emitted item,
  `agents_states` preserving `Errored`, and the receiver id. Control
  `spawn_agent_refused_emits_failed_item` (stub returns Err) asserts
  refusal plus a Failed item with empty receivers/states.
- Observation link (goal unit, existing):
  `spawn_agent_completed_sets_observation` proves Completed \u2192 1 and
  `spawn_rejections_and_non_spawn_tools_do_not_set` proves Failed/
  InProgress SpawnAgent \u2192 0. Core cannot depend on goal, so the proof
  is this two-link chain: accepted-with-errored \u2192 Completed item
  (core, new) \u2192 1 observation (goal, existing). Both links are
  executed, mutant-killed tests.
- Bound (honest): the stub pins the handler mapping deterministically
  at the `AgentControl` boundary; it does not measure the real async
  race frequency (child erroring between admission and sampling).
  The verdict allows this fixture for the mapping ("Drive the real V1
  SpawnAgentHandler with an AgentControl accepted receipt"); a
  real-child race-timing case is not claimed.
- Narrowing mutant `spawn_status_ignores_delivery_result` (core:
  status from sampled liveness again, ignoring the spawn result) is
  KILLED by the accepted-with-errored test in the core lane on hosted
  precheck 7 (run 38083359851). The refused control remains the negative case.

Rev1 findings remain closed (precheck 6 evidence, unchanged files):
send_input delivery-bound with Compact refusal test; real-path
code-mode exactly-once with double-emit kill; paused/blocked update
narrowing; external set/clear production-site kills; SendMessage/
FollowupTask split kill. See rev5 for the full text.

## Summary (unchanged architecture)

Per-goal-turn state-change observations for goal pacing. A transient
per-turn count records whether at least one STATE-CHANGING outcome was
observed. Four reset sources, each recorded at its committing handler or
event, never at ToolFinish success:

- applied file change (FileChange Completed item via `on_item_completed`),
- actual plan transition (`on_plan_committed` hook from the plan handler,
  steps differ from the last committed plan),
- committed goal mutation (goal tools after DB success, external set/clear
  after the committed check),
- accepted spawn/follow-up (CollabAgentToolCall Completed for
  spawn/send tools, SubAgentActivity Started/Interacted; V1 send_input
  and V1 spawn emission are now both delivery-bound).

Existing activity booleans and the three-fully-empty-continuations
blocker are untouched; observations are separate additive state. No
core->goal dependency. No pacing timer in this leaf (TASK-260929-309h9n).

## Changed files

Production (precheck-6 base + this rework fix):

- `codex-rs/core/src/tools/handlers/multi_agents/spawn.rs` \u2014
  delivery-bound completed-item status (rev2 A-F1/D-F1 fix, +9/-1).
- `codex-rs/core/src/tools/handlers/multi_agents/send_input.rs` \u2014
  delivery-bound completed-item status (rev1 A-F1 fix, +10/-1,
  unchanged here).
- `codex-rs/core/src/tools/handlers/plan.rs` \u2014 fire
  `on_plan_committed` after successful plan parse/publication.
- `codex-rs/core/src/tools/lifecycle.rs` \u2014 thin plan-commit fan-out.
- `codex-rs/ext/extension-api/src/contributors.rs`,
  `contributors/tool_lifecycle.rs`, `lib.rs` \u2014 new defaulted
  `on_plan_committed` hook (`PlanCommitInput` borrows existing
  stores/plan; existing contributors stay compatible).
- `codex-rs/ext/goal/src/accounting.rs` \u2014 per-turn observation counts
  + classifier (existing activity functions byte-identical).
- `codex-rs/ext/goal/src/extension.rs` \u2014 `on_item_completed` and
  `on_plan_committed` recording.
- `codex-rs/ext/goal/src/runtime.rs` \u2014 external set/clear recording
  after the committed check.
- `codex-rs/ext/goal/src/tool.rs` \u2014 create/update recording after DB
  success.

Tests (this rework adds only the two core spawn tests):

- `codex-rs/core/src/tools/handlers/multi_agents_tests.rs` \u2014 Compact
  refusal + accepted control (rev1) plus new stub-`AgentControl`
  accepted-with-errored and refused spawn emission tests (rev2).
- `codex-rs/core/tests/suite/code_mode.rs` \u2014 item recorder, real-path
  nested-patch exactly-once test + wrapper-only control.
- `codex-rs/core/tests/suite/tool_lifecycle.rs` \u2014 plan hook fires.
- `codex-rs/ext/goal/tests/goal_extension_backend.rs` + new
  `goal_extension_backend/state_change_observation_tests.rs` \u2014 backend
  observation tests (create/update/paused/blocked, external set/clear,
  plan, spawn/ToolFinish, fresh runtime).
- New `codex-rs/ext/goal/tests/state_change_observations.rs` \u2014 unit
  classifier tests for all sources, non-resets, AC3, AC4, blocker-first,
  transience.

Size note for reviewers: 17 files, 1828 insertions(+), 7 deletions(-)
(tracked `git diff --stat HEAD`: 15 files +1007/-7; the 2 new test
files add 821 lines). Production logic is ~300 lines (rev2 adds 9);
the rest is the AC8-mandated test + mutant coverage. This exceeds the
800-line guideline; the justification is the per-gate narrowing-mutant
coverage AC8 requires. The rev2 delta alone is 2 files, +333/-1
(+9/-0 of it the whitespace fmt fix).

## Coverage map (AC -> tests)

AC1 \u2014 per-turn observation, four commit-point sources:

- file change: `applied_file_change_sets_observation` (unit),
  `backend_file_change_completed_sets_observation` (backend),
  `code_mode_leaf_applied_patch_delivered_exactly_once` (core real path).
- plan transition: `first_plan_counts_as_transition`,
  `plan_status_change_counts_as_transition`,
  `plan_step_text_change_counts_as_transition` (unit),
  `backend_plan_transition_sets_and_identical_does_not` (backend),
  `plan_committed_hook_fires_for_successful_update_plan` (core).
- goal mutation: `goal_mutation_sets_observation`,
  `goal_mutation_for_unknown_turn_is_ignored` (unit),
  `backend_goal_create_and_update_set_but_failed_create_does_not`,
  `backend_goal_update_paused_and_blocked_set_observation`,
  `backend_external_goal_set_and_clear_record_observation` (backend).
- spawn/follow-up: `spawn_agent_completed_sets_observation`,
  `send_input_completed_sets_observation`,
  `send_message_and_followup_task_completed_set_observation`,
  `subagent_started_and_interacted_set_observation` (unit),
  `backend_spawn_followup_sets_but_tool_finish_success_does_not`
  (backend), `send_input_rejected_compaction_emits_failed_item`,
  `send_input_accepted_emits_completed_item`,
  `spawn_agent_accepted_with_errored_child_emits_completed_item`,
  `spawn_agent_refused_emits_failed_item` (core emission).

AC2 \u2014 non-resets, each with a named test:

- failed tool: `failed_tool_does_not_set_observation`,
  `failed_or_declined_file_change_does_not_set`,
  `spawn_rejections_and_non_spawn_tools_do_not_set`,
  `send_input_failed_or_in_progress_does_not_set`.
- identical plan: `identical_plan_resubmission_does_not_set`.
- shell success: `shell_success_does_not_set_observation`,
  `code_mode_leaf_wrapper_only_delivers_no_file_change`.
- wrapper success: `code_mode_leaf_counts_once_and_wrapper_adds_none`
  (wrapper-only half asserts 0; the `exec` ToolFinish feed adds none
  and the integration tests prove the wrapper emits no item at all).
- model progress claim: `model_text_claiming_progress_does_not_set`.

AC3 \u2014 code-mode counted once:
`code_mode_leaf_counts_once_and_wrapper_adds_none` (classifier: 1 for
leaf + `exec` ToolFinish success + a shell CommandExecution, 0 for
the same without the leaf) plus
`code_mode_leaf_applied_patch_delivered_exactly_once` (real-path
delivery: exactly one FileChange, zero CommandExecution, no item
with the wrapper's call id) and the wrapper-only control (exactly
one nested CommandExecution, no wrapper item).

AC4 \u2014 no model-writable bypass:
`no_model_writable_bypass_sets_observation` (identical plan with magic
text, magic tool name with success, magic message text; count stays 1
from the first plan only). The plan API takes `&[PlanItemArg]`, so the
free-text `explanation` cannot reach the comparator at all.

AC5 \u2014 existing behavior preserved: `record_tool_outcome`,
`record_item`, and `empty_response_goal` are byte-identical logic (new
fields only); pre-existing suites were green on precheck 6. New
`empty_blocker_still_fires_first_with_no_observation` and
`observation_does_not_disturb_empty_blocker` prove the blocker fires
on schedule with and without observations.

AC6 \u2014 transient: `observation_is_transient_per_turn`,
`fresh_state_carries_no_observation_or_plan_memory` (unit),
`backend_fresh_runtime_carries_no_observation` (backend). Counts live in
the in-memory turn map (removed by `finish_turn`); plan memory lives in
the in-memory thread state (fresh `default()` on resume). Nothing is
written to rollout, history, or the goal store.

AC7 \u2014 stated bound: arbitrary shell side effects are UNKNOWN. A
successful shell command (ps/tail or any other) never sets the
observation, so pacing may stay conservative (delay when only shell
successes are observed) and completion is never inferred from shell
output or exit status.

AC8 \u2014 mutants (16 attached in `TASK-260929-3ld28o_mutants.json`,
byte-identical to rev6; hosted precheck 7 on tree `486ebfe5` reports
16/16 killed, 0 survivors):

| Mutant | Narrows | Hosted killer (lane) |
|---|---|---|
| file_completed_requires_auto_approved | R1 record set | applied_file_change_sets_observation (small) |
| plan_transition_ignores_content | R2 record set | plan_status_change_counts_as_transition (small) |
| goal_update_complete_only_records | R3 record set | backend_goal_update_paused_and_blocked_set_observation (small) |
| external_goal_set_does_not_record | R3 record set | backend_external_goal_set_and_clear_record_observation (small) |
| external_goal_clear_does_not_record | R3 record set | backend_external_goal_set_and_clear_record_observation (small) |
| spawn_only_spawn_agent_counts | R4 record set | send_input_completed_sets_observation (small) |
| spawn_followup_message_tools_dropped | R4 record set | send_message_and_followup_task_completed_set_observation (small) |
| send_input_status_ignores_delivery_result | R4/N1 boundary | send_input_rejected_compaction_emits_failed_item (core) |
| spawn_status_ignores_delivery_result | R4/N1 boundary (NEW) | spawn_agent_accepted_with_errored_child_emits_completed_item (core) |
| file_failed_counts_as_applied | N1 ignore set | failed_or_declined_file_change_does_not_set (small) |
| identical_plan_always_counts | N2 ignore set | identical_plan_resubmission_does_not_set (small) |
| command_execution_counts_as_state_change | N3 ignore set | shell_success_does_not_set_observation (small) |
| code_mode_nested_file_change_emitted_twice | AC3 exactly-once | code_mode_leaf_applied_patch_delivered_exactly_once (core) |
| tool_finish_success_records_mutation | N4 ignore set | backend_spawn_followup_sets_but_tool_finish_success_does_not (small) |
| agent_message_counts_as_state_change | N5 ignore set | model_text_claiming_progress_does_not_set (small) |
| agent_message_state_keyword_counts | AC4 bypass | no_model_writable_bypass_sets_observation (small) |

The 15 old mutants were killed on precheck 6 (tree `568588ed`);
precheck 7 reran all 16 on the new tree and reports every named killer failing. The new mutant reverts
`spawn.rs` to the sampled-status proxy; under it the new
accepted-with-errored test must fail (Failed instead of Completed)
while the refused control stays green.

Killer tests vs the CI mutant filter
(`test(observation) | test(state_change) | test(plan) | test(spawn) |
test(code_mode_leaf) | test(empty_blocker) | test(goal_mutation) |
test(goal_update) | test(goal_create) | test(file_change) |
test(shell_success) | test(tool_lifecycle) | test(tool_finish) |
test(agent_message) | test(send_input) | test(model_text)`): all
match \u2014 both new tests contain `spawn` (`test(spawn)`). Nothing missed
by the filter.

## Design decisions and bounds

- Count (`u32`), not bool, so AC3's exactly-once is assertable;
  `has_observed_state_change` is count > 0 for pacing.
- V1 send_input and V1 spawn item statuses now both report delivery,
  matching each other and the V2 paths (SubAgentActivity emitted only
  after successful commit). Liveness remains available in
  `agents_states`.
- Plan comparison covers steps+status only; `explanation` is excluded by
  API shape (`&[PlanItemArg]`).
- Goal mutations counted: explicit create/update/external set-clear only.
  Automatic stops and usage-accounting writes are excluded.
- Spawn/follow-up counted: `SpawnAgent`/`SendInput`/`SendMessage`/
  `FollowupTask` Completed plus `Started`/`Interacted`. Resume, wait,
  close, list, interrupt, and child `Completed` are excluded per the AC
  wording.
- External mutations with no active turn have no turn to record to; the
  pacing leaf handles inter-turn goal changes via goal
  identity/revision invalidation (documented bound).
- Observation accumulates per turn regardless of mid-turn goal identity
  changes; the mutation that changes goals records its own observation.
- The spawn accepted-receipt test is a deterministic handler-mapping
  fixture, not a real-child race-timing reproduction; race frequency
  is unknown and unclaimed.

## Commands (exact, with exit codes)

Prior successor run (verified the parked rev6 tree, fixed its fmt,
no behavior change; retained historical command record):

- Temp-index tree recomputation on arrival \u2014 exit 0, matched the
  parked `094e5623b3af280e5379c32936353830e6949eaf` exactly
  (candidate intact, uncommitted, 17 changed paths).
- `cargo fmt -- --config imports_granularity=Item --check`
  (worktree `codex-rs/`, `PATH=$HOME/.cargo/bin:$PATH`) \u2014 exit 1:
  the rev6 stub lines in `multi_agents_tests.rs` were unformatted.
  Reported truthfully as failing; fixed, not waived.
- `rustfmt --edition 2024` on that one file (same engine/config as
  `cargo fmt`, zero blast radius) \u2014 exit 0; `git status` still 17
  paths; the change is +12/-3 whitespace-only in the stub.
- `cargo fmt -- --config imports_granularity=Item --check` re-run \u2014
  exit 0, zero non-warning output lines (nightly-only
  `imports_granularity` warnings, expected).
- `git diff --check` \u2014 exit 0 (no whitespace errors).
- 16/16 mutant `git apply --check` \u2014 exit 0 each, both before and
  after the fmt fix (no mutant touches the reformatted file).
- Temp-index tree after the fix:
  `486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7`.
- `git diff --name-only 568588ed 486ebfe5` \u2014 exactly
  `multi_agents/spawn.rs` and `multi_agents_tests.rs`, exit 0.
- `git diff --stat HEAD`: 15 tracked files +1007/-7; the 2 new test
  files add 821 lines (517 + 304) \u2014 17 files, +1828/-7 total.
- Rev6 commands (predecessor run, kept for the record):
  `cargo fmt` apply exit 0, `--check` reported exit 0 (not
  reproduced here \u2014 the tree it left behind failed `--check` with
  exit 1 as shown above), `git diff --check` exit 0, 16/16
  `git apply --check` exit 0.

Not run locally (Mac mini addendum R194/R223: no local Rust
builds/checks/clippy/tests; the mechanical guard refuses them):

- `just fix`, `just clippy`, `just test` (any crate), `cargo nextest`,
  `cargo build/check/clippy/test`.
- All Rust compilation, lint, test execution, and mutant kills for this
  tree run on hosted relux-ci as precheck 7. Nothing here is claimed
  green on local evidence.

## Current handoff verification and logbook

2026-10-11: hosted precheck 7 (`TASK-260929-3ld28o_hosted-precheck-7.md`,
ivanopcode/codex run 38083359851) reports lint, small, core and app-server
lanes SUCCESS on tree `486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7`.
All 16 supplied mutants are killed by the named tests in the table above;
0 survivors. These are hosted lane conclusions and supplied-mutant results.
Individual hosted process exit codes and mutant run ids are not present in
this precheck attachment and remain unknown here; expected-red mutant jobs
are failing evidence, never described as exit 0. No local Rust build, lint or
test was attempted, per the Mac mini addendum. Existing activity, blocker,
transience and API tests are included in the green hosted suites; the
16/16 ratio describes supplied mutants, not every possible surface mutation.

Commands run directly during this handoff session:

- `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` \u2014 exit 0;
  confirms the exact tree is covered by green hosted run 38083359851.
- `git diff --check` \u2014 exit 0.
- Temporary-index `git read-tree HEAD`, `git add -A`, `git write-tree` \u2014
  each exit 0; computed tree `486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7`.
- `git diff --name-only 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7` \u2014 exit 0, empty output.

No source, test or formatting changes this session. The earlier reported
`094e5623` was superseded by whitespace-only rustfmt reflow in the stub
AgentControl implementations; the hosted tree is `486ebfe5`, as recorded in
`TASK-260929-3ld28o_orch-tree-note-7.md`. Both original orchestrator test-only
fixes (E0382 status-label-before-move and crate-level expect_used allowance)
remain included. Review rev2 A-F1/D-F1 are answered by the delivery-bound
spawn fix, accepted-with-errored regression, refused-spawn control and killed
`spawn_status_ignores_delivery_result` mutant. Rev1 fixes remain covered by
the same green snapshot and their named killed mutants.

All 11 existing checklist items were already checked on arrival; their test,
lint and build citations are refreshed to precheck 7. No unchecked command
was marked passing. Results refreshed before developer handoff. The candidate
remains UNCOMMITTED. Temporary index files and the temporary evidence staging
directory used in this session were removed.

## Remaining bounds

- The deterministic accepted-spawn fixture proves handler mapping; a real-child
  admission/error race frequency is unknown.
- Fresh-runtime tests plus persistence inspection establish transience; a public
  JSON-RPC resume count assertion is not claimed.
- Arbitrary shell side effects remain UNKNOWN. Pacing may stay conservative;
  completion is never inferred from shell output or exit status.
- Change-size guidance is exceeded (17 paths, +1828/-7, roughly 300 production
  lines). The smallest staging option remains the defaulted plan hook and core
  fan-out/test followed by the consumer and remaining tests. No restructuring
  was authorized for this handoff.

rev4 = rev3 tree republished for lifecycle repair; evidence: TASK-260929-3ld28o_hosted-precheck-7.md, TASK-260929-3ld28o_review-verdict-rev3.md
