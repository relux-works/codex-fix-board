# TASK-260929-36bvsc (E1): fix the red snapshot test from hosted precheck 1, then request precheck 2

Hosted precheck 1 (run 37458451362, core job 112251734577) ran your exact worktree. Lint, small and app-server are GREEN.
Core is RED on your unit test, failing all 3 tries (R169):

- `session::pending_work::tests::snapshot_reports_armed_queued_and_leased_only` at core/src/session/pending_work_tests.rs:106:
  `left == right` failed, left=2, right=1. The snapshot reports two entries where the test expects one.

Work out which side is wrong. Is one receipt counted in two sets (for example, Armed in the B store AND Queued in the
runtime mailbox during or after the Armed->Queued transition)? That would be a real AC1/AC4 defect: fix production so each
receipt appears exactly once. Or does the test's expectation miss a legitimately pending entry? Fix the test then, and say
why in the results. All 4 mutant results are void because the base was red; they will be re-run.

Your local-build allowance (`local-build-allowance.md`) still applies under all its gates: one narrow run of the
pending_work tests (`-p codex-core --lib -E 'test(pending_work)'`), then trim and record readings.
Update the results and mutants files (re-attach both). Leave the candidate UNCOMMITTED and add the note
"HOSTED-PRECHECK-REQUESTED: precheck 2". Do NOT hand off. Follow R176 and R174.
