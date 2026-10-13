# TASK-260929-csyzcj (G1): precheck 17 failed one new test. Find the root cause, fix it, then request precheck 18

Ivan's direction stands (task notes, loop-detector rev5 bound answer): no revision cap, the code must be reliable.

## What the hosted runs showed

- Precheck 16 (run 38327475123, tree 8343519c) stopped at lint: `goal_native_wait.rs:1211` passed `&Arc<Config>` where
  the generic `ThreadStartInput<'_, C>` needs `&Config`. The orchestrator fixed that one line (`&*parent.config().await`);
  see `g1-orch-test-fix-17.md`. Keep that fix.
- Precheck 17 (run 38328884035, snapshot `ci/TASK-260929-csyzcj/wip-17` = 5adf190a, your rev6 tree plus that line):
  lint, small and app-server green; **all 15 mutants killed**; core failed on one test:
  - `suite::goal_native_wait::goal_wait_dense_paths_interrupted_item_bound` failed 3 of 3 tries at
    `goal_native_wait.rs:244` (`running_owned_child_id`): "timed out waiting for the native child to reach Running",
    after about 11 s each time. Which depth timed out is not logged.
  - `suite::goal_native_wait::goal_wait_latch_closes_completion_before_registration` was FLAKY (failed once, passed on
    retry 2): `goal_native_wait.rs:513`, "goal set hung after the registration gate was released". It passed cleanly in
    prechecks 14 and 15, so treat it as a possible regression from the trunk integration (pacing) or rev6, not as noise.
  - Unrelated flakies, ignore: `hooks::permission_request_hook_allows_exec_command_without_user_approval`,
    `realtime_conversation::conversation_second_start_replaces_runtime`.
  - The excerpt is in `g1-precheck-17-core-excerpt.txt`.

## Required

1. Find the ROOT CAUSE of the dense-test timeout by reading the code. Do not just raise the timeout. Candidates to check:
   - does a spawn at depth 1 or 2 actually happen (`agent_max_depth` in `fixture()`; the 128-byte task-name cap; the
     path-total cap on the new path);
   - do the per-level `mount_sse_once_match` matchers capture the right requests once the interrupted child becomes the next
     parent (an inherited or forked history containing an earlier level's prompt would make `!body_contains(prompt)` or
     `!has_function_call_output` reject or steal requests);
   - does `inspect_directly_owned_native_children` on an interrupted parent still list its new child.
   If the cause is a product defect (for example a valid dense depth-3 spawn is refused or never starts), fix the product
   and say so in the results. If it is the test, fix the test. Make the failure message name the depth and the observed
   child statuses, so a future failure is diagnosable from the log alone.
2. Explain the latch flake. If the trunk integration (pacing timers, `ProceedWithoutGate` removing the admission
   checker, `ProceedWithPacingTicket`) or rev6 introduced a real race, fix it and add or adjust a test. If you conclude
   it is a test-harness timing issue, prove it from the code and make the test deterministic. Do not add retries or longer
   sleeps.
3. Keep every accepted fix and all 15 mutants applying and killed by their named killers. Update the results
   (`TASK-260929-csyzcj_results.md`) with both root causes.

`mini-producer-addendum.md` applies: only `cargo fmt -- --config imports_granularity=Item` then `--check` (exit 0);
no other cargo or just; no CODEX_HOME copies; delete temp dirs. Leave everything UNCOMMITTED, report the final tree id
after fmt, add the note `HOSTED-PRECHECK-REQUESTED: precheck 18`, and end your turn without handing off.
