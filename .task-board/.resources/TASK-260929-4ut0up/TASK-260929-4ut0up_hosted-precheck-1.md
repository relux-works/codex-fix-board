# Hosted pre-handoff evidence: TASK-260929-4ut0up (B2 watcher-and-output-retention-hooks), precheck 1

## Snapshot of the exact pre-handoff worktree
- commit `1381a8e20edfb60c75ecdd70f7eab26615f16e8d` (signed, never landed), tree `ebf602f732c49b175f70c16a16f04c5d033b1258`
- run https://github.com/relux-works/codex/actions/runs/37008593036: lint, small and app-server **success**; core **FAILURE**
- core: 4903 run, 4899 passed, **4 failed** (deterministic 3/3). Each failed with
  `Failed to create unified exec process: LandlockSandboxExecutableNotProvided`:
  - unified_exec::receipt_hooks::tests::default_launches_reserve_no_receipts
  - unified_exec::receipt_hooks::tests::opted_in_decision_before_exit_queues_exactly_one_completion
  - unified_exec::receipt_hooks::tests::opted_in_exit_before_decision_returns_inline_and_frees_slot
  - unified_exec::receipt_hooks::tests::terminal_stdin_claim_consumes_the_single_claim_first
  These tests spawn real processes through unified exec without the Linux sandbox setup (Landlock needs the
  codex-linux-sandbox executable, or a test sandbox policy that does not require it). macOS (seatbelt) hides this.

## Narrowing mutants (16; failures of the 4 tests above are ignored as platform failures)
- **Killed by the intended test (13):** ac1-failed-exit-reports-minus-one, ac1-publish-on-exit-token-before-drain,
  ac1-timed-out-dropped-to-false, ac2-capacity-refusal-proceeds-as-default, ac3-omitted-count-subtracted,
  ac3-retention-cap-doubled, ac4-capacity-counts-active-only, ac4-retire-most-recently-sampled,
  ac6-interrupt-cancels-with-released, ac6-release-cancels-with-owner-stopped, ac6-release-leaks-retained-output,
  ac6-shutdown-cancels-with-released, ac6-terminate-cancels-with-released.
- **Not demonstrated (3)**, because the intended killing test is one of the 4 platform failures:
  ac2-success-inline-weakened-to-arm, ac5-stdin-claim-leases-without-acknowledge, ac7-default-launch-forced-opt-in.
