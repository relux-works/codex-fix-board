# Republish note for TASK-260929-u2i5rr — revision 3 (routine, no code change expected)

Revision 2 (your F1-F3 tests) passed every gate command except two app-server websocket signal tests that are
timing-sensitive under host load (FLAKY in an earlier unrelated run, 27 flaky tests in this one; this leaf does not
touch app-server). They are now quarantined with evidence (known-baseline-failures.md). Keep the code as it is.
Run the guard, re-run `just test -p codex-core -E 'test(completion_receipt)'` once, refresh
`TASK-260929-u2i5rr_results.md` (list the F1-F3 tests and the mutants they kill), run the `--any` busy check, and
hand off. Do not edit README.md or anything outside the leaf scope.
