# Rework note for TASK-260929-u2i5rr — revision 2 (answers review findings F1-F3)

The reviewer found no behavioural defect; every attack held. The blocking findings are unguarded gates: narrowing
mutants survive the 13-test suite. Keep the implementation unless a new test proves a defect, and add named tests
that fail against each mutant:
- F1 `owner-gate-unguarded-on-lease-and-resolve`: a foreign owner (other thread, other runtime generation, other
  call) must be refused with ForeignOwner on `lease_for_sampling` and on `resolve_initial_response`. Where
  reachable, also cover fail_sampling and acknowledge with a lease built for another owner. Kills M1 and M2.
- F2 `stale-lease-fail-unguarded`: after a requeue and a re-lease, the stale first lease calling `fail_sampling`
  must return StaleLease and must not requeue the live lease. Kills M4.
- F3 `duplicate-exit-while-reserved-unguarded`: a second `publish_exit` while the receipt is still Reserved (before
  the initial-response decision) must be refused (InvalidTransition). The retained first completion stays intact.
  Kills M7.
Attach `TASK-260929-u2i5rr_results.md` with the list of new tests and, for each, the mutant it kills. Run the mutant
by applying the reviewer's one-line edit to a scratch copy outside the worktree, never to your candidate, and
report the real exit codes. Then run the tb-R58 suite check and hand off (or hold).
