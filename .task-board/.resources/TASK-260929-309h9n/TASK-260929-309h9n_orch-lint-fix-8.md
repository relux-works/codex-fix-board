# TASK-260929-309h9n: orchestrator compile fix before precheck 8

Precheck 7 (run 38216547888, tree 6dddbb09) failed in the lint lane before tests or mutants ran:
`ext/goal/src/extension.rs:188:16: error[E0382]: use of moved value: config`. In `on_thread_start`, `config` is moved into
`input.thread_store.insert(config)` (line 129), and the rework then read `config.continuation_pacing` at line 188.

Fix (mechanical, no behavior change): read `let continuation_pacing = config.continuation_pacing;` next to the existing
`let enabled = config.enabled;` before the move, and test `if continuation_pacing {` at the pacing site. fmt --check exit 0.
New tree eb655488b22ff6bb17a3a3a6250fd60e3a202209.

Mutant `pacing_feature_flag_ignored` was re-expressed for the new line as `if continuation_pacing || true {` (same semantics:
pacing is enabled regardless of the feature flag; the local stays used, so there is no unused-variable warning). All 7
mutants `git apply --check` clean (`b2-mutants-8.json`, which is now the board `TASK-260929-309h9n_mutants.json`).
