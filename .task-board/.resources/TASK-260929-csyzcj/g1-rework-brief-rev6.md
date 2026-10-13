# TASK-260929-csyzcj (G1): rev6 rework. Re-verify the trunk integration, close the interrupted-item bound, then request precheck 16

Ivan's direction (2026-10-13, recorded in the task notes as the loop-detector rev5 bound answer): there is no revision
cap and the code must be reliable. Correctness beats speed: read before you change, and prove every claim.

## 0. What changed under you: the Story moved onto the new trunk

Trunk advanced from `39c264c34` to `99533cf03`. The new trunk adds:
- goal continuation pacing (`7e4289e21`): `BackgroundWaitState::is_pacing_enabled`,
  `BackgroundWaitEvaluation::ProceedWithPacingTicket`, and `ProceedWithoutGate` now REMOVES the published admission checker;
- per-step waiting capabilities and the goal waiting-guidance World State section (`67789e1ee`, `99533cf03`);
- exec tmpdir cleanup (`e0eff0576`).

The orchestrator converged your rev5 delta onto it with `task-board worktree converge` (rev5 is now stale with
`integration_base_moved`). Everything auto-merged except two hunks, which the orchestrator resolved mechanically
(see `g1-orch-converge-16.md`):
- `core/tests/suite/mod.rs`: kept both `mod goal_continuation_pacing;` and `mod goal_native_wait;`;
- `ext/goal/src/runtime.rs` (goal continuation start): kept your native-pending prelude unchanged, then
  `if wait_enabled || self.inner.background_wait.is_pacing_enabled()` and
  `evaluate_continuation_with_native_pending(.., native_pending, now)` with TRUNK's arms
  (`ProceedWithoutGate` removes `GoalBackgroundWaitAdmission`; `ProceedNormal | ProceedWithTicket | ProceedWithPacingTicket` insert it).

Required before the bound fix:
1. Review that resolution and every auto-merged intersecting path against trunk semantics: `core/src/session/mod.rs`,
   `core/src/tools/handlers/multi_agents_tests.rs`, `ext/goal/src/background_wait.rs` (`evaluate_locked` now carries both
   `native_pending` and pacing), `ext/goal/src/extension.rs`, `ext/goal/src/lib.rs`, `ext/goal/src/runtime.rs`.
   In particular decide, with a test where it matters, how native pending work interacts with pacing:
   native-pending with the background gate disabled but pacing enabled, native-pending with an empty exec snapshot under
   pacing, and the durable-sleep marker with a pacing wait. If the mechanical resolution is wrong, fix it.
2. Make sure your own World State / waiting-guidance interaction is right: the native wait tool now appears in the
   goal's waiting guidance (P3-2); nothing in G1 may contradict it.
3. Rebase every mutant in your mutants JSON onto the new tree (each must still apply and still be killed by its named,
   filter-selected test).

## 1. The rev5 finding (unchanged)

Do everything in `g1-rework-brief-review5.md` (P0 `interrupted-item-token-threshold-unreviewed`): whole model-visible
interrupted item <= 1000 bytes by construction, the item-bound const with a compile-time assert, the unit and
`goal_wait_dense_paths_interrupted_item_bound` integration tests, the body-cap mutant, corrected results.
Keep every earlier accepted fix exactly as it is.

## 2. Rules

`mini-producer-addendum.md` applies: only `cargo fmt -- --config imports_granularity=Item` then `--check` (exit 0);
no other cargo or just; no CODEX_HOME copies; delete temp dirs. Hosted CI is the only test gate.
Update `TASK-260929-csyzcj_results.md` (add a "trunk integration" section that names what you checked and how).
Leave everything UNCOMMITTED, report the final tree id after fmt, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 16`, and end your turn without handing off.
