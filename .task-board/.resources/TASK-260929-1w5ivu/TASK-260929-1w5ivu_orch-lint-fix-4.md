# TASK-260929-1w5ivu: orchestrator lint fix before precheck 4

Precheck 3 (run 38255143212, tree b6d57f59) failed in lint before any test ran:
`core/tests/suite/waiting_guidance.rs:213: error[E0063]: missing field continuation_pacing in initializer of
GoalExtensionConfig`. This is base drift: the field arrived with P4b (relux/main 7e4289e2) after this delta was written, and
the producer could not compile on the mini.

Fix (mechanical, test fixture only): the suite's goal-config closure now maps
`continuation_pacing: c.features.enabled(Feature::GoalContinuationPacing)`, exactly as production does in
`app-server/src/extensions.rs:84-90`. No assertion changed. `cargo fmt --check` exit 0, `git diff --check` clean, all 8
mutants still `git apply --check` clean. New candidate tree `bae5da77b475230605658a56ae797322809bdb5b`.

Pacing stays on by default here, as in production. The waiting-guidance tests end with the goal completed or with a dead
manager, so no automatic continuation fires and pacing cannot change their exact request counts.
