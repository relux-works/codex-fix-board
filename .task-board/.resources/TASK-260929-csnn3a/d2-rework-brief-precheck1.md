# TASK-260929-csnn3a (D2): fix two red tests from hosted precheck 1, then request precheck 2

Hosted precheck 1 (run 37420955553, core job 112129966169) ran your exact worktree on bc00d9b. Lint, small and app-server
are GREEN. Core is RED on two of your new tests, failing all 3 tries (R169, attempt-specific log):

1. `exec_completion_compaction_omission_keeps_receipt_pending` panics at core/tests/suite/exec_completion.rs:1731:
   "second request must be the compaction summarization". The test assumes the second /v1/responses request is the
   compaction summary, but on this base it is not. That could be remote compaction v2 (x-codex-beta-features:
   remote_compaction_v2 is on by default in the suite), different request ordering, or no compaction being triggered at all.
   Drive compaction deterministically: explicitly configure the compaction mode the test asserts, or match the request by
   content, not by position. Then assert that the receipt stays pending and is sampled by a later request.
2. `exec_completion_survives_cleared_idle_reservation` (F1a) panics in core/tests/common/lib.rs:393: "timeout waiting for
   event: Elapsed(())". The event it waits for never arrives. Either the test never reaches the cleared-reservation state,
   or production drops the retained mail. That is exactly the F1a bug class, so find out which. If production loses it,
   fix production (inside D's scope); the retain_only_task_present mutant must still be killed.

AC3 (guardian omission): your stated-bound argument (results §3, "structural impossibility") is acceptable ONLY if it is
backed by a code citation at this base showing the guardian path cannot omit a recorded fragment, plus the preservation
test passing. The panels will judge it. Do not drop the guardian preservation test.

All mutant results from precheck 1 are void because the base was red. They will all be re-run.

LOCAL VERIFICATION ALLOWED (one targeted run, same gates as D1): right before building, check `df -g /` (>= 50 GiB),
CPU idle (>= 25%, via `top -l 2 -n 0 | grep 'CPU usage' | tail -1`) and `memory_pressure | tail -1` (free >= 30%). Do not
start if any gate fails, and kill cargo if memory free falls under 30% during the build. Run ONLY
`cd codex-rs && RUST_MIN_STACK=33554432 cargo nextest run -p codex-core --test all -E 'test(exec_completion)'`.
Then `rm -rf /Users/iv/Developer/IV/codex-target/debug`. Record disk before and after, CPU and memory in the results.
Nothing in parallel.

Update the results and mutants files (re-attach both). Leave the candidate UNCOMMITTED and add the note
"HOSTED-PRECHECK-REQUESTED: precheck 2". Do NOT hand off. Follow R176 and R174.
