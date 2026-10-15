# TASK-260929-csyzcj (G1): precheck 18 has one remaining red test. Fix the fixture, then request precheck 19

Hosted precheck 18 (ivanopcode/codex run 38365654460) ran tree a318e169 (snapshot ci/TASK-260929-csyzcj/wip-18 dec9f630).
5159 of 5160 core tests pass, and lint, small and app-server are GREEN. One test is red, failing 3/3 (R169, job 115196317030):

- `suite::goal_native_wait::goal_wait_dense_paths_interrupted_item_bound` at core/tests/suite/goal_native_wait.rs:1183:
  "depth 0: the parent model must expose native V2 spawning".
  The precheck-17 fix (fixture model gpt-5.5 -> gpt-6-sol) was not enough: the parent model the test configures still
  does not advertise native V2 spawn. Find which model or catalog metadata enables V2 spawning in the test harness. Look
  at how the passing goal_native_wait tests and the existing V2 spawn suite tests (spawn / agent tests) configure their
  model or feature flag, and use exactly that. Do NOT weaken the assertion: the test must really drive the dense
  interrupted-item path through a V2-spawning parent, and the item bound (<= 1000 B, worst case 838 B) must still be asserted.
Also seen, not a blocker: `goal_background_wait::scheduled_checkins_fire_through_production_runtime_under_paused_time`
was FLAKY 2/3 on this run. If you can see a deterministic cause while you are in the scheduler tests, note it in the
results. Do not change it in this leaf unless it is trivially a test-harness race.

No local cargo on the mini rule does not apply on ivmbp, but keep the standing ivmbp build gates (local-build-allowance.md):
one narrow run `-p codex-core --test all -E 'test(goal_native_wait)'`, df >= 50 GiB, CPU idle >= 25%, memory free >= 30%,
trim afterwards. Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 19". Do NOT hand off.
Follow R176 and R174.
