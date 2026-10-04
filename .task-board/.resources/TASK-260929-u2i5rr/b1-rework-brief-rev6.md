# Rework brief — TASK-260929-u2i5rr (B1), CR revision 6: last uncovered arm + a full error-arm sweep

Round 3 merged to changes_requested (`TASK-260929-u2i5rr_review-verdict-rev5.md`). The delta panel confirmed that every
round-2 finding is fixed. Panel A found one more gap:
- resolve-initial-response-active-nonreserved-arm-unguarded: in `resolve_initial_response`, the arm
  `(phase, _) => return Err(InvalidTransition { actual: phase.status() })` is never driven. No test calls
  resolve_initial_response with the LEGITIMATE owner on an Armed, Queued or LeasedToSampling receipt. A mutant that
  accepts those phases would survive.

Do this:
1. Add a deterministic test. For each of Armed, Queued and LeasedToSampling, call resolve_initial_response with the
   legitimate owner and assert `Err(InvalidTransition { actual: <that status> })`, and assert the receipt's state is
   unchanged afterwards.
2. Sweep `completion_receipt.rs` to stop a round 4 that finds the next arm. List EVERY match arm or branch that returns
   an `Err(...)` or performs a state transition, together with the test that drives it, in a table in
   `TASK-260929-u2i5rr_results.md`. Add a test for any arm that has none. Do not change product code unless a test
   exposes a real defect, and say so if one does.
3. Keep the leaf to its 3 paths. Revert any `just fix` edit outside them.
4. Fast lane only: busy check, guard, `just fmt`, `just clippy -p codex-core`. No local codex-core tests; hosted CI
   runs them on the exact candidate after handoff. Then busy check and handoff.

## Note (operator, 10:0xZ): resume after HOLD-BUILD
RUN-261002-aab881 wrote the rev-6 tests and the error-arm sweep, then held on a genuine BUSY (the G2 producer was
building). The target is free now. Do NOT redo the work: confirm the worktree holds the 3 leaf paths with the new tests,
run the busy check (FREE), then the guard, `just fmt` and `just clippy -p codex-core`. Fix only compile or lint
problems, then busy check and hand off. Only a printed `BUSY ...` line means HOLD.
