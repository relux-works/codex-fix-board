# TASK-260929-csyzcj (G1): the goal-wait marker never registers in production. Fix it, then request precheck 2

Hosted precheck 1 (see g1-p1.ok; core job in run of the wip-1 snapshot) ran your exact worktree on 39c264c. Lint, small and
app-server are GREEN. Core is RED on your two central suite tests, failing all 3 tries (R169):

1. `suite::goal_native_wait::goal_wait_registers_marker_and_wakes_on_child_completion` at goal_native_wait.rs:259:
   `assertion failed: has_goal_wait_sleep(test.codex.thread_extension_data())`. With a Running native child, the goal-owned
   SleepItem is NOT present after the parent goes idle.
2. `suite::goal_native_wait::goal_wait_latch_closes_completion_before_registration` at goal_native_wait.rs:379:
   "idle should pause at the registration gate". The idle path never reaches your registration gate either.
Both point to the same defect: the registration hook is not wired into the production idle path in this configuration. It
may be the wrong hook (for example, called only from a path the test never takes), a gate on host capability or policy
activation that is false here, an inspection that returns no owned children for natively spawned agents, or registration
happening on a different thread's extension data. Trace from the goal extension's on_thread_idle (or whatever P4a/F
activation calls) to the insert_if, and fix the real wiring. Do not weaken the tests. Every mutant "kill" from precheck 1
leaned on these two red tests, so all 6 are void and will be re-run.

LOCAL VERIFICATION (local-build-allowance.md, all gates; NOTE disk is tight, about 58 GiB free, so check df right before
and skip the local run if under 50 GiB): `cd codex-rs && RUST_MIN_STACK=33554432 cargo nextest run -p codex-core --test all -E
'test(goal_native_wait)'`, then trim and record readings. Update and re-attach the results and mutants files. Leave the
candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 2". Do NOT hand off. Follow R176 and R174.
