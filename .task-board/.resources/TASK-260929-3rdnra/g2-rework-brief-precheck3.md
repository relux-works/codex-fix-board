# TASK-260929-3rdnra (G2): hosted precheck 3 is red on five core tests. Fix them, then request precheck 4

Hosted precheck 3 (ivanopcode/codex relux-ci run 38681700613, snapshot ci/TASK-260929-3rdnra/wip-3 @ 9ce52ab2834f) found lint,
small and app-server GREEN, and all 10 mutants killed. Those mutant results do not count because core is RED (R169). Five tests
failed all three tries. Job log: `impl/p4c/g2-precheck-3-core.log` (job 116249738221).

Note: after precheck 2 the orchestrator applied one test-only compile fix in `control_bridge_tests.rs` (`raw_items()` is an
iterator, so `.to_vec()` became `.cloned().collect::<Vec<_>>()` at the two assert sites). Keep that fix.

1. `agent::control::tests::bridge::native_runtime_fragment_records_idle_history_once_and_retains_wake`
   (control_bridge_tests.rs:194). Recording the fragment into idle history stamps the item: it gets `id: Some(msg_...)` and
   `internal_chat_message_metadata_passthrough { turn_id: Some("auto-compact-0"), create_time: Some(..) }`. The test expects
   the bare `ContextualUserFragment::into(fragment)` (`id: None`, `turn_id: None`).
   - First, check that the stamping is correct product behavior. It must match what the normal history-recording path does
     for any other item recorded while idle. In particular, is `turn_id = "auto-compact-0"` the right value for a fragment
     recorded outside any turn, or does it leak a stale or synthetic turn id? If it is wrong, fix the product code.
   - Then make the assertion compare what matters: exactly one new item; role, content and phase equal to the fragment; no
     duplicate after `maybe_start_turn_for_pending_work`. Compare the stamped item to itself on the second history read
     (record-once) instead of to the bare fragment. Do not weaken the record-once or no-duplicate checks.
2. `suite::pending_input::subagent_bridge::native_completion_mailbox_history_and_wake::{v1_registered_wait, v2_registered_wait,
   v1_without_wait}` (pending_input_subagent_bridge.rs:270), `assert_eq!(before_mail.requests().len(), usize::from(deferred_mail))`
   fails with left 1, right 0. This is a TEST bug. In `core/tests/common/responses.rs`, `base_mock()` puts the recording
   `ResponseMock` matcher BEFORE your custom matcher, so `requests()` records every `/responses` POST that wiremock evaluates
   against that mock, matched or not. Here that is the parent wake request, which reaches `before_mail` before `parent_wake`
   because of mount order. Fix the test so the count is the number of requests that actually matched. For example, mount
   `before_mail` only when `deferred_mail` (an `Option<ResponseMock>`), or filter `requests()` by the same predicate. Do not change
   `responses.rs`. Check every other `requests().len()` / `single_request()` in your new tests for the same trap, and fix the
   ones that are only right by luck of mount order.
3. `suite::goal_background_wait::scheduled_checkins_fire_through_production_runtime_under_paused_time` (EXISTING P4a test). Try 1
   timed out in `wait_for_event` (common/lib.rs:393). Tries 2 and 3 failed at goal_background_wait.rs:307 because
   `sink.warnings()` was empty where the test expects `CHECK_INS_STOPPED_WARNING`. On the G1 runs this test was flaky (2/3); now it
   fails 3/3. Find out whether your mailbox/bridge changes (for example extra mailbox work, or a changed idle/continue path on a goal
   thread) delay or suppress the third check-in, or the stopped warning, under paused time. If G2 causes it, fix the product code.
   If it is a pure harness race (the bounded `yield_now` loops), replace the loop with a deterministic wait on the real condition,
   with a timeout. Do not loosen any count assertion. Explain the root cause, with evidence, in the results file.

Keep every with-wait and without-wait case, and keep the 10 mutants killing. The upstream test
`subagent_notification_is_included_without_wait` must stay green and unchanged.

DISK IS BELOW THE LOCAL BUILD STOP LINE (about 37 GiB free, stop under 45 GiB). Run NO local cargo builds or tests this pass, only
`just fmt`. Hosted precheck is the gate, so type-check your code carefully by reading it: precheck 2 was lost to an iterator/slice
compile error. Update and re-attach the results and mutants files. Leave the candidate UNCOMMITTED and add the note
"HOSTED-PRECHECK-REQUESTED: precheck 4". Do NOT hand off. Follow R176 and R174.
