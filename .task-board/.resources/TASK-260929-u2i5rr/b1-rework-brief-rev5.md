# Rework brief — TASK-260929-u2i5rr (B1 receipt-state-machine), CR revision 5: close the round-2 test gaps

The round-2 R141 review of revision 4 merged to changes_requested. Panels: A = sonnet, B = astra, plus the delta panel.
The merged verdict is `TASK-260929-u2i5rr_review-verdict-rev4.md`, and it has 5 robustness findings. All of them are
missing mutant-killing tests; none reports a product-code bug. Add tests in `completion_receipt_tests.rs` that kill each
named mutant. Change product code only if a new test exposes a real defect, and if it does, say so explicitly.

1. terminal-history-bound-unguarded (M15). Cancel MAX_COMPLETION_RECEIPTS + 1 receipts one at a time (each slot freed in
   turn). `status(first)` must be `Err(UnknownReceipt)`, and `status(last)` must be `Ok(Cancelled{..})`. Deleting the
   `pop_front` eviction in `StoreState::retire` must turn the test red.
2. terminal-path-owner-gates-unguarded (M12/M13/M14). Drive one receipt into each terminal state: Sampled, InlineResult
   and Cancelled. On each, call `status`, `cancel` and `lease_for_sampling` with a foreign owner, and call
   `fail_sampling` / `acknowledge_sampled` with a lease carrying a foreign owner (use the existing foreign-owner helpers).
   Each call must return `Err(ForeignOwner)`, and the legitimate owner must still see the true terminal status. Dropping
   the owner check in `terminal_error` (:245) or in the terminal arm of `status` (:525), or turning the `cancel`
   ForeignOwner passthrough (:505) into AlreadyTerminal, must each turn a test red.
3. terminal-history-paths-untested. `cancel` on a Sampled, InlineResult or Cancelled receipt by its own owner must return
   `Err(AlreadyTerminal)`. This overlaps with 1 and 2; one table-driven test may cover all three, as long as each mutant
   is killed.
4. owner-call-id-boundary-256. `ReceiptOwner::new` with a 256-byte call id is accepted, and with 257 bytes it is refused
   (`InvalidOwner`). The `>=` mutant must fail.
5. sampling-source-attribution-nondeterministic (M16). In
   `completion_receipt_terminal_stdin_and_pushed_sources_share_one_lease`, assert `status == LeasedToSampling{source:
   TerminalStdinOutput}` after the stdin lease and `Sampled{source: TerminalStdinOutput}` after the acknowledgement, and
   do the same for PushedCompletion in a deterministic test. A mutant that records PushedCompletion regardless of
   `source` must fail deterministically, not only when stdin wins a thread race.

Build and test rules (fast lane, see `producer-brief.md`): run the busy check, then the guard, then `just fmt` and
`just clippy -p codex-core`. Clippy type-checks the tests. Do NOT run codex-core tests locally: hosted relux-ci runs them
on the exact candidate tree after handoff, and any failure comes back to you with the job log. Because of that, reason
through every assertion carefully before you hand off. In `TASK-260929-u2i5rr_results.md`, list each new test, the
finding and mutant it kills, and the production line it guards. Then busy check and handoff. Do not edit README.md or
anything outside the leaf scope.

## Scope fix (orchestrator finding, not from the panels)
The revision-4 candidate also changes `core/src/tools/registry.rs`, `core/tests/suite/openai_file_mcp.rs` and
`core/tests/suite/scenarios.rs`. Each change only removes an unused import. These are upstream-baseline warnings, not
part of this leaf, and `just fix` removed them as a side effect. They would leak into B's upstream PR. Restore all three
files to the base (`git checkout -- <path>`) so the leaf touches only `unified_exec/mod.rs`, `completion_receipt.rs` and
`completion_receipt_tests.rs`. When you run `just fix -p codex-core`, revert any edit it makes outside those three paths
before handoff.
