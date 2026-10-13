# Orchestrator converge before rev6 (2026-10-13)

- Trunk moved `39c264c34` -> `99533cf03` (P3-1/P3-2 waiting guidance, continuation pacing, exec tmpdir cleanup, relux-ci).
- rev5 candidate tree `b91072a51501101110a4e13061a8c07a242aad6a` (backup ref `refs/tmp/g1-rev5-cand` in the control root).
- `git merge-tree` of rev5 onto the new trunk: two content conflicts (`core/tests/suite/mod.rs` adjacent `mod` lines,
  `ext/goal/src/runtime.rs` goal continuation start block); all other paths auto-merged.
- Route: both files were temporarily reset to the old base, `task-board worktree converge STORY-260929-wo5dnz` ran
  (rev5 -> stale, integration_base_moved), then both files were restored with the resolution:
  - `suite/mod.rs`: `mod goal_continuation_pacing;` followed by `mod goal_native_wait;`;
  - `runtime.rs`: G1's native-pending prelude unchanged; the evaluation gate became
    `wait_enabled || background_wait.is_pacing_enabled()`; the call stays `evaluate_continuation_with_native_pending`;
    the match arms are trunk's (`ProceedWithoutGate` removes the admission checker; Normal / Ticket / PacingTicket insert it).
- Verified: the resulting worktree tree `12315de7680d130b48fd7d371e39aa3ba7b559aa` differs from the precomputed 3-way
  merge-tree only in those two files; `cargo fmt --check` exits 0. No build or test ran on the mini.
- The resolution is mechanical. The rev6 producer must re-verify its semantics (`g1-rework-brief-rev6.md` §0).
