# TASK-260929-309h9n (P4b-2): orchestrator test compile fixes before precheck 3

Precheck 2 (run 38149210470, snapshot ac49dc10, tree e88ce693) passed the library build but stopped in the lint lane on two
test compile errors, so no other lane or mutant ran:
- `core/tests/suite/goal_continuation_pacing.rs:231:25` E0599: `Duration` has no `duration_since`.
  Fix: `second_deadline.saturating_sub(clock.now())` (same assertion: the n=2 deadline is exactly 60s past the frozen clock).
- `app-server/tests/suite/v2/goal_continuation_pacing.rs:194:21` E0283: type annotations needed for `read_notification`.
  Fix: `read_notification::<TurnStartedNotification>("turn/started")` (the assertion only checks that the timeout fires).
No behavior or assertion change. `cargo fmt -- --config imports_granularity=Item --check` exit 0. New tree 9751ddd89a50.
All 5 mutants still `git apply --check` clean. Unused-import scan of both new test files: clean.
