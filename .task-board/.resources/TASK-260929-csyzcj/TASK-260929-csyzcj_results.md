# TASK-260929-csyzcj results — G1 rework for precheck 2 (test-only fix)

## Summary

Precheck 1 was RED on the two central suite tests: with a supposedly Running
native child, the goal-owned `SleepItem` was absent after idle, and the idle
path never reached the registration gate. I traced the production path
`GoalExtension::on_thread_idle` → `GoalRuntimeHandle::continue_if_idle` →
`CodexThread::inspect_directly_owned_native_children` → `insert_if` →
`recheck_pending_work_for_goal_wait` and found the production wiring correct;
the defect was in the suite setup, which never created a Running V2 child, so
inspection correctly returned no pending work. This pass fixes only
`codex-rs/core/tests/suite/goal_native_wait.rs` (no production change):

1. Fixture enables `Feature::MultiAgentV2` (+ explicit `Collab`) and sets
   `sleep_tool_mode = AlwaysOn`. Default config is V1-only
   (`MultiAgentV2` defaults off), so the plain `spawn_agent` call never
   dispatched; with `ModelDriven` + reminder disabled + a clock-less test
   model, the child's `clock.sleep` was never registered either.
2. `spawn_call` now uses the V2 wire format
   `ev_function_call_with_namespace(..., "collaboration", "spawn_agent", ...)`
   with `fork_turns: "none"` (was plain `spawn_agent`, which matches neither
   V1's `multi_agent_v1/*` nor V2's `collaboration/*`).
3. `sleep_call` now uses `ev_function_call_with_namespace(..., "clock",
   "sleep", ...)` (was plain `"clock.sleep"`, which never dispatches to the
   namespaced `clock/sleep` handler, so the child completed instantly instead
   of staying Running on a 2 s sleep).
4. Matchers use structured `has_function_call_output(call_id)` instead of
   `body.contains("spawn_agent")` / `body.contains("clock.sleep")`: the tools
   list always contains tool names (so `!contains("spawn_agent")` never
   matched), and namespaced calls contain no `"clock.sleep"` substring. Child
   initial-step matchers additionally exclude the parent prompt, because the
   parent's post-spawn request contains the spawn args (`"do slow work"`) in
   its history and would otherwise steal the child's mock.
5. The goal is set after the parent's `TurnComplete` instead of before the
   user turn. An external set on idle work-less state starts a spurious goal
   continuation that would consume scripted mocks; setting it after the spawn
   still drives production `continue_if_idle` (via the set itself plus the
   explicit idle emit). The latch test now drives `set_goal` through the
   registration gate (same production pause point, before insert).

Test assertions are unchanged (marker presence, wake request contents,
silence, foreign preservation); only the setup now actually establishes the
precondition. This is a fix, not a weakening.

Status: code fixed, fast-lane green locally, core integration + mutants
require hosted precheck 2. This turn ends with HOSTED-PRECHECK-REQUESTED (no
handoff).

## Changed files (this pass)

- `codex-rs/core/tests/suite/goal_native_wait.rs` — fixture flags, namespaced
  mock calls, structured matchers, set-after-spawn ordering (only file
  changed; all production files byte-identical to the precheck-1 tree).

Carried over unchanged from the previous pass (precheck-1 GREEN lanes):
production lease, inspection, scheduler reuse, removal, V2 Interrupted gating,
plus small-crate unit tests. See prior results for that inventory.

## Coverage map — 9 of 9 AC rows driven (assertions unchanged)

Production call sites (unchanged): `GoalRuntimeHandle::continue_if_idle`
(`runtime.rs`), `CodexThread::inspect_directly_owned_native_children` +
`recheck_pending_work_for_goal_wait` (`codex_thread.rs`),
`LocalAgentRuntime::inspect_owned_child_ids` (`runtime_context.rs`),
`try_register_goal_wait_sleep` / `remove_goal_wait_sleep` (`native_wait.rs`),
`BackgroundWaitState::evaluate_continuation_with_native_pending`
(`background_wait.rs`), `GoalExtension::on_turn_start` (`extension.rs`),
`notify_parent_of_terminal_turn` (`completion.rs`).

| AC | Driving test (production call site) | Refusal / narrowing test |
|---|---|---|
| AC1 marker + queue-only wake with model request | `goal_native_wait::goal_wait_registers_marker_and_wakes_on_child_completion` via `set_goal` → `continue_if_idle` → `inspect…` → `try_register` → `recheck` → explicit idle → V2 mail → scheduler wake; asserts wake request contains `worker completed`, marker removed on turn start | Silence before wake asserted (500 ms no-event after insert, request counts); no-marker negative covered by AC2 tests |
| AC2 no marker for non-goal/unloaded/unknown/failed; errors propagate | `owned_children_inspection_propagates_failed_lookups` (control unit) via `inspect_owned_child_ids`: loaded → Loaded, removed (known) → Unloaded, unknown id → `UnknownChild` Err; non-goal path returns before inspection in `continue_if_idle` | Same test asserts `expect_err` for unknown (mutant M1 skips → `Ok`, fails) |
| AC3 latch (insert before mail check + recheck) | `goal_native_wait::goal_wait_latch_closes_completion_before_registration` via `set_goal` → `continue_if_idle` paused at `TestNativeWaitRegistrationGate`: child finishes in window, release → wake request | Mutant M2 (recheck before insert) misses wake → `parent_wake` 0, fails |
| AC4 foreign preserved (insert + conditional remove) | Goal unit `register_never_clobbers_foreign_sleep` + `conditional_remove_only_removes_owned_id` via lease helpers; integration `goal_wait_preserves_foreign_sleep_across_register_and_turn_start` via `set_goal` + `continue_if_idle` + `on_turn_start` with foreign present | Mutants M3 (unconditional remove deletes foreign) and M4 (insert admits `clock-wait-1`) fail preservation asserts |
| AC5 removal / check-in reinsert / exhausted keep + late wake | Removal on turn start (AC1 asserts `!has_goal_wait_sleep` after wake start); clear/release/resume-removal via `goal_wait_removed_on_clear_release_and_resume` (`GoalService::clear_thread_goal` → `apply_external_goal_clear`, `release_native_wait`, `restore_thread_runtime_after_resume`); check-in evaluation with native via goal unit `empty_exec_with_native_pending_waits_and_uses_checkins` + `native_pending_exhausts_checkins…` (Wait → ticket ×3 → Wait None + warning) | Mutant M6 (ignore `native_pending`) returns ProceedNormal for empty+pending → fails Wait assert. GAPS (unchanged): full integration of check-in reinsert with paused clock + live child; exhausted-keep + late-completion wake with live child; disable/stop dedicated integration (share `remove_goal_wait_sleep`, unit-covered) |
| AC6 no UI / history / reminder from storing marker | AC1 asserts 500 ms silence after insert (no parent events), wake body has no `goal-wait:` (no history item) and no `current_time` (reminder disabled, unchanged) | Design: `ExtensionData::insert` emits nothing, schedules nothing; no dedicated refusal mutant (absence asserted, not a gate) |
| AC7 Interrupted once per transition, queue-only, `is_final` unchanged | Unit `interrupted_notice_is_queue_only_without_claiming_success` (message `INTERRUPTED`, no `FINAL_ANSWER`/`completed`/`success`, < token cap) + `interrupted_stays_non_final` (`is_final(Interrupted)==false`) via `session_prefix` / `status` | Mutant M5 (Interrupted claims `FINAL_ANSWER`+success) fails message asserts. GAP (unchanged): integration with real abort (once-per-transition mail when marker present, quiet otherwise) |
| AC8 reused / error / second-child per state; inherited settings preserved | Unit `pending_native_work_is_only_pending_init_and_running` (reused uses current status; Completed/Errored/Shutdown/NotFound/Interrupted do not permit registration) via `OwnedChildInspection::is_pending_native_work`; AC1 wake uses scheduler path that preserves inherited settings (same `maybe_start_turn_for_pending_work` as pending-input) | GAPS (unchanged): explicit inherited-settings assert with non-default parent settings; second-child-mid-turn integration |
| AC9 resume never revives | `goal_wait_removed_on_clear_release_and_resume` via `GoalService::restore_thread_runtime_after_resume` → `restore_after_resume` (removes marker; never inserts; unloaded child yields no marker at next idle) | GAP (unchanged): full `resume_thread_with_history` with rendered `SleepItem` in history + unloaded child → assert no marker after resume idle |

Ratio: 9 of 9 AC rows driven (4 fully: AC1/2/3/4; 5 partially: AC5/6/7/8/9 as above).
Negative shapes: forged/unknown child (UnknownChild Err, not empty); absent
evidence (Unloaded/empty → no marker, no wait); check present but uncalled
(inspection before registration; recheck after insert); bypass (foreign
marker wake still works without clobber); capability (persistent host only).

## Out of contract

- V1 notification bridge (task: “Out of scope: the V1 notification bridge
  (sibling TASK-260929-3rdnra, G2)”). V1 completions still use
  `inject_fragment_without_turn` (not mailbox), so they do not wake via
  durable sleep until the sibling lands. This leaf covers V2 queue-only
  (already mailbox) + lease + V2 `Interrupted` gating. Silence does not claim
  V1 coverage.

## Mutants (narrowing; precheck-1 kills void, re-run in precheck 2)

Unchanged from the previous pass; all 6 patches verified to apply to the
current tree via `git apply --check` (production files untouched this pass).

| Mutant | What it narrows the gate to | Named test that must fail |
|---|---|---|
| `skip_failed_lookups` (runtime_context: unknown/inspection failures `continue` instead of `Err`) | Error propagation → silent skip (list_agents shape); admits unknown as empty | `agent::control::tests::owned_children_inspection_propagates_failed_lookups` (`expect_err` → gets `Ok`) |
| `insert_after_mail_check` (runtime: `recheck` before `try_register`, no post-insert recheck) | Latch → completion-before-registration loss | `goal_native_wait::goal_wait_latch_closes_completion_before_registration` (`parent_wake` 0, times out) |
| `unconditional_remove` (native_wait: `remove` instead of `remove_if` owned-only) | Conditional remove → deletes foreign | `native_wait::conditional_remove_only_removes_owned_id` (foreign preserved assert fails); also `goal_wait_preserves_foreign_sleep…` |
| `insert_clobbers_one_foreign` (native_wait: predicate also admits `clock-wait-1`) | Never-clobber → admits exactly one foreign | `native_wait::register_never_clobbers_foreign_sleep` (returns true + foreign gone, fails) |
| `interrupted_claims_success` (session_prefix: `INTERRUPTED` → `FINAL_ANSWER` + “completed successfully”) | No-success-claim → claims success | `session_prefix_tests::interrupted_notice_is_queue_only_without_claiming_success` (no-FINAL_ANSWER/completed/success asserts fail) |
| `ignore_native_pending` (background_wait: `is_empty() && !native_pending` → `is_empty()`) | Native-gated wait → proceeds despite Running child | `native_wait::empty_exec_with_native_pending_waits_and_uses_checkins` (expects Wait, gets ProceedNormal) |

No survivors claimed; all kills pending hosted precheck 2. A mutant with no
named failing test would be reported as survivor — none here.

## Commands (real exit codes; no pipes on gates)

- `python3 …/codex-fix-suite-busy.py --any` → `FREE`, exit 0 (before first
  build; re-checked before clippy runs).
- `/Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-target-guard.sh`
  → same checkout, cache kept, exit 0.
- `cd codex-rs && just fmt` → exit 0 (after edits; re-ran after matcher fix).
- `cd codex-rs && just clippy -p codex-core` (stdout+stderr redirected to a
  file, exit read directly, no pipe) → exit 0, `Finished dev profile`.
  6 warning lines, all pre-existing in unrelated files
  (`tools/registry.rs` ToolCallSource import, `openai_file_mcp.rs`,
  `scenarios.rs`); zero warnings mention `goal_native_wait`.
- `git apply --check` for each of the 6 mutant diffs → all apply, exit 0.
- Local `cargo nextest run -p codex-core --test all -E 'test(goal_native_wait)'`:
  NOT RUN as evidence. First attempt launched while edits were still landing
  (stale tree) and its tail was truncated in delivery, so its result is
  UNKNOWN (reported as unrun, not as a pass). Re-check before the evidence
  run showed disk 48 GiB < 50 GiB gate → skipped per the rework brief, then
  trimmed. Hosted precheck 2 is the authoritative run.
- NOT RUN locally (per brief; hosted only): `just test -p codex-core`,
  `just test -p codex-app-server`, full `just test`, background builds.
- Small-crate suites not re-run this pass (no small-crate file changed; small
  lane was GREEN in precheck 1 on the same small-crate tree).

## Machine readings (local-build-allowance)

- Before evidence-run decision: disk 48 GiB free (`df -g /`), CPU 57.76%
  idle, memory free 92%. Disk gate (≥50 GiB) FAILED → local run skipped.
- After `rm -rf /Users/iv/Developer/IV/codex-target/debug`: disk 51 GiB free.
- Earlier (before first build): disk 54 GiB, CPU 51.49% idle, memory 92%.

## Unverified / next pass

- Hosted precheck 2 must run: `suite::goal_native_wait::*` (4 tests),
  `owned_children_tests`, `status_tests`,
  `session_prefix_tests::interrupted_notice…`,
  `control_tests::owned_children_inspection_propagates_failed_lookups`, plus
  all 6 mutants (each must fail its named test; precheck-1 kills are void).
- Gaps carried over (see coverage map): AC5 check-in-reinsert /
  exhausted-keep + late wake with live child + paused clock, disable/stop
  dedicated integration; AC7 real-abort once-per-transition integration;
  AC8 inherited-settings assert + second-child-mid-turn; AC9 full
  `resume_thread_with_history` with rendered `SleepItem`.

## Checklist mapping

- Code written per description + AC: yes — test-only fix this pass (V2 scope;
  V1 out per task). Production from previous pass unchanged.
- Tests written + passing: 4 integration tests fixed to establish a real
  Running V2 child; compile green (clippy exit 0), execution pending hosted
  precheck 2. Small-crate 13 passed in precheck 1 (same tree).
- Build not broken: clippy exit 0 for codex-core; fmt exit 0.
- Outcome attached: this file + `TASK-260929-csyzcj_mutants.json` (6 narrowing
  diffs, unchanged, re-attached).
- Logbook: not updated (no anomaly/regression beyond the diagnosed fixture
  defect, recorded here).
