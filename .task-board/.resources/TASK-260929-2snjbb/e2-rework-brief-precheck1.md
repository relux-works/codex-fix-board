# TASK-260929-2snjbb (E2): fix the red revision-recheck test from hosted precheck 1, then request precheck 2

Hosted precheck 1 (snapshot run 37490126742, core job 112360376104) ran your exact worktree on e26d221. Lint, small and
app-server are GREEN. Core is RED on your unit test, failing all 3 tries (R169):

- `session::turn_input::tests::goal_background_wait_revision_recheck_catches_transition` at
  core/src/session/turn_input_tests.rs:1431: `assert_ne!` failed with left: 0, right: 0.
  The two revisions the test compares are both 0, so the transition the test performs does not move the E1 work revision
  in this setup. Either the test's "transition" does not go through a path that bumps the revision (for example, it
  mutates state directly or uses a test double whose revision stays at 0), or the admission contributor reads a different
  revision source from the one the transition bumps. If it is the second case, that is a real AC7 defect: the
  gate-to-start race would go unnoticed. Fix production so the contributor rechecks the same revision that E1's
  transitions bump. Otherwise drive a real E1 transition (arm, queue, lease, acknowledge) in the test. Do not weaken the
  assertion.

Mutant notes: each of the 7 mutants also has other killing tests, but all results are void because the base was red.
The orchestrator now applies mutant patches with `git apply --recount`. Six of your 7 patches had wrong hunk line counts:
regenerate them with `git diff` against the candidate so they apply cleanly as written.

local-build-allowance.md applies under all its gates (narrow filter: `-p codex-core --lib -E 'test(goal_background_wait) or
test(turn_input)'`). Update the results and mutants files (re-attach both). Leave the candidate UNCOMMITTED and add the note
"HOSTED-PRECHECK-REQUESTED: precheck 2". Do NOT hand off. Follow R176 and R174.
