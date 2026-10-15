# TASK-260929-3rdnra (G2): two bridge regressions on hosted precheck 1. Fix them, then request precheck 2

Hosted precheck 1 (ivanopcode/codex relux-ci run 38501625154, snapshot ci/TASK-260929-3rdnra/wip-1) found lint, small and
app-server GREEN and 8/8 mutants killed. Core is RED, with 3 tests failing all 3 tries (R169):

1. `suite::subagent_notifications::subagent_notification_is_included_without_wait` (EXISTING upstream test):
   "timed out waiting for parent rollout to include subagent notification". REGRESSION: with your bridge, a V1 parent
   that has NO registered goal wait never receives the child's notification in its history. AC2 says such a parent is
   not WOKEN. It does not say the notification is dropped. The queue-only runtime-mailbox data must still be delivered
   into the parent's next turn (or wherever the pre-change behavior put it), without starting a turn on its own. Restore
   that delivery. Do not change this upstream test.
2. `suite::pending_input::subagent_bridge::native_completion_mailbox_history_and_wake::v1_without_wait` and
   `::v2_without_wait` (your new tests) at pending_input.rs:446: the turn fails with
   "unexpected status 404 Not Found ... /v1/responses". The mock server received a model request it had no mock for,
   so a parent WITHOUT a registered wait issued an extra request (an unwanted wake), or the test under-mocks a request
   that is legitimate after the fix for item 1. Decide which one it is. A parent without a wait must make no request of
   its own; when it next runs a turn, the notification is in that request's input.
Keep every with-wait case and the mutants green. Add or adjust a narrowing mutant: "bridge drops queue-only data for
parents without a registered wait". The upstream test above must kill it.

DISK IS BELOW THE LOCAL BUILD STOP LINE (about 36 GiB free, stop under 45 GiB): run NO local cargo builds or tests this pass;
`just fmt` only. Hosted precheck is the gate. Update and re-attach the results and mutants files. Leave the candidate UNCOMMITTED
and add the note "HOSTED-PRECHECK-REQUESTED: precheck 2". Do NOT hand off. Follow R176 and R174.
