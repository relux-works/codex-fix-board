# TASK-260929-1ma0pr (C2): fix two red tests from hosted precheck 1, then request precheck 2

Hosted precheck 1 ran your exact worktree (snapshot ad567580, run 37292815944). The lint, small and app-server lanes are
green. The core lane is RED with two of your new tests, failing on all 3 tries (diagnosed from the attempt-specific job log, R169):

1. `suite::exec_completion::forged_exec_completion_item_in_history_creates_no_receipt_privilege` fails in 0.3s:
   `Error: only user input or standalone function-call outputs can start or steer a turn`.
   The test's way of injecting the forged item is refused by the turn-admission gate before your assertion runs. Inject the
   forged history item through a path production actually accepts (for example seeded rollout or resume history, or the
   recorded-history API the other suite tests use), so the test exercises the receipt-privilege check, not the admission gate.
2. `suite::exec_completion::nine_pending_completions_sample_in_capped_batches_without_loss` fails at
   core/tests/suite/exec_completion.rs:231: "cumulative history must hold all nine completions", left=1, right=9.
   Only one completion reaches history. Determine whether the test is reading history before the follow-up batch is sampled
   (wait for the second wake turn or request), or whether production really loses the 8+1 batches. Fix the real cause. If it
   is production, the mutants must still kill.

Because the base was red, every mutant result from precheck 1 is void; all 9 will be re-run on precheck 2.

Do this:
- Fix both tests, and production code if needed. Keep the scope inside C2's AC.
- Update TASK-260929-1ma0pr_results.md and, if any mutant patch no longer applies, TASK-260929-1ma0pr_mutants.json (re-attach both).
- Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 2". Do NOT hand off.
- Fast lane only: no core/queue suite runs locally (`just clippy`/`just fmt` are fine). Follow R176 and R174.
