# TASK-260929-34a6ls (D1): rev 2 has one red test on hosted precheck 3. Fix it, then request precheck 4

Hosted precheck 3 (run 37393084857, core job 112042526597) ran your exact worktree. Lint, small and app-server are GREEN.
Core is RED on your new test, on all 3 tries (R169, attempt-specific log):

- `suite::exec_completion::completed_response_with_blocked_tool_acknowledges_before_interrupt` panics in the wiremock
  verification: "Mock #1. Expected range of matching incoming requests: == 3. Number of matched incoming requests: 2".

Work out which side is wrong. If the correct behavior after interrupting a completed sampled request is that the receipt
is acknowledged and NOT re-sampled, then a third /v1/responses request may legitimately never happen. In that case fix the
mock expectation, and assert the real invariant directly: acknowledged exactly once, never requeued, never re-sampled.
If a third request IS required (for example, the turn that follows the interrupt), make the test drive it deterministically.
Never loosen the check that the receipt is not sampled twice.
All 9 mutant results from precheck 3 are void because the base was red. They will be re-run.

LOCAL VERIFICATION ALLOWED THIS TIME (one targeted run only, approved by tb-arbiter): right before building, check `df -g /`
AND CPU idle (`top -l 2 -n 0 | grep 'CPU usage' | tail -1`). Only if at least 50 GiB is free AND CPU idle is at least 25% (R112), you may run ONLY `cd codex-rs && cargo nextest run -p codex-core --test all -E 'test(exec_completion)'`
(or the repo's `just test -p codex-core -- exec_completion` equivalent). Run nothing else heavy, and never two builds at once.
Afterwards, trim with `rm -rf /Users/iv/Developer/IV/codex-target/debug`. Record free disk BEFORE and AFTER the build, plus the CPU-idle reading, in the results. RAM is tight: run nothing in parallel with the build. If either gate fails, skip it and rely on the hosted run.

Then update TASK-260929-34a6ls_results.md and the mutants file (re-attach both). Leave the candidate UNCOMMITTED and add the
note "HOSTED-PRECHECK-REQUESTED: precheck 4". Do NOT hand off. Follow R176 and R174.
