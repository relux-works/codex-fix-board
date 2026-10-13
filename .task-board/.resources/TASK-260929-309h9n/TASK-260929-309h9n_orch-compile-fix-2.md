# TASK-260929-309h9n (P4b-2): orchestrator compile fix before precheck 2

Precheck 1 (run 38148309948, snapshot 3f8d4168, tree 8062d43c) stopped in the lint lane on one compile error, so no other lane
or mutant ran: `ext/goal/src/continuation_schedule.rs:62:22: error[E0308]: mismatched types: expected u32, found u64`.
`Duration::checked_mul` takes a `u32`; `pacing_delay` built the multiplier as `1u64 << shift`.

Fix (mechanical, no behavior change): `let multiplier = 1u32 << shift;` (shift is already clamped to <= 31, so it fits).
`cargo fmt -- --config imports_granularity=Item --check` exit 0. New tree e88ce693a4f2. All 5 mutants of the board's
`TASK-260929-309h9n_mutants.json` still `git apply --check` clean (reused as precheck 2 mutants).
The orchestrator also read the rest of the source diff for further compile errors hidden behind this one
(enum match exhaustiveness in runtime.rs, `ArmedDeadline` fields, `has_observed_state_change`, `ExtensionData::remove`): none found.
