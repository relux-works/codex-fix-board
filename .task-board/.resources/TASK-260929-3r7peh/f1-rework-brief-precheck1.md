# TASK-260929-3r7peh (F1): three real suite failures and fmt from hosted precheck 1. Fix them, then request precheck 2

Hosted precheck 1 (run 37600975837) ran your exact worktree on 2f522b9. small and app-server are GREEN. Red (R169):

0. LINT: `just fmt-check` fails. Run `just fmt` (and clippy, keeping zero new warnings over the 3-warning baseline).
1. `suite::goal_background_wait::background_wait_activation_gates_goal_but_admits_user_input` at goal_background_wait.rs:397:
   "user input should be admitted while gated", left=0, right=1. While the activated policy gates goal continuation, a user
   message was NOT admitted. That is a fairness violation (P4a AC1, F1 AC7): user/follow-up input must never be held. Find
   whether activation gates too broadly (for example, at the admission contributor for all inputs instead of only automatic
   goal continuation), or whether the test sends input in a way production never admits. Fix production if it gates user input.
2. `suite::exec_notification::exec_notification_opt_in_arms_and_read_returns_terminal_output` at exec_notification.rs:175:
   "wake request should carry the completion fragment". After the opted-in process exits, the wake request does not contain
   the exec-completion fragment, so the end-to-end path (receipt -> mailbox -> idle wake -> fragment in the request) is
   broken in the activated configuration. Trace it: is the receipt armed, the mailbox entry enqueued, the wake started, and
   the fragment recorded? Fix the broken link; do not loosen the assertion.
3. `suite::exec_notification::exec_notification_release_disarms_without_killing` at exec_notification.rs:537:
   "live session should still answer after release", but the output shows "Process exited with code 0". Either release
   kills or retires the process (a real AC5 defect), or the test's command naturally exits too early (use a process that
   stays alive until the test tells it to stop). Prove the process survives release, and that a later exit yields no wake.
Mutant results are void because the base was red. Several mutants were only "killed" by these red tests; they will be re-run.

LOCAL VERIFICATION (local-build-allowance.md, all gates): this time run the failing suite tests locally before requesting
the precheck: `cd codex-rs && RUST_MIN_STACK=33554432 cargo nextest run -p codex-core --test all -E 'test(goal_background_wait) or
test(exec_notification)'`. Run it sequentially, trim afterwards, and record readings. Update and re-attach the results and mutants
files (patches via `git diff`). Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 2". Do NOT
hand off. Follow R176 and R174.
