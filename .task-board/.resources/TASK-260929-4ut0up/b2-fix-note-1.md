# TASK-260929-4ut0up (B2): make the process-spawning tests Linux-safe, then request precheck 2

Hosted precheck 1 (`TASK-260929-4ut0up_hosted-precheck-1.md`, precondition) ran your exact worktree tree on Linux. 4 new
`receipt_hooks` unit tests fail with `LandlockSandboxExecutableNotProvided`: default_launches_reserve_no_receipts,
opted_in_decision_before_exit_queues_exactly_one_completion, opted_in_exit_before_decision_returns_inline_and_frees_slot
and terminal_stdin_claim_consumes_the_single_claim_first. They spawn real processes through unified exec without the
Linux sandbox setup; macOS seatbelt hid this. As a result, 3 mutants (ac2-success-inline-weakened-to-arm,
ac5-stdin-claim-leases-without-acknowledge, ac7-default-launch-forced-opt-in) cannot be shown to be killed.

Fix: set up these tests the way the existing unified_exec / process_manager tests that spawn real processes do on Linux.
Find that existing helper or sandbox policy, either a test sandbox policy that needs no Landlock helper or the
codex-linux-sandbox executable resolved through the repo's test helpers, and reuse it; do not invent a new mechanism.
The tests must keep driving the production exec_command / write_stdin paths. Platform rules: tests must pass on Linux
and macOS; do not skip them on Linux.
Then use the fast lane only (`just fmt`, `just clippy -p codex-core`), refresh results and mutants (keep all 16), add
the note `HOSTED-PRECHECK-REQUESTED: precheck 2`, and end your turn without handing off.
