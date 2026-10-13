# TASK-260929-csyzcj (G1): hosted precheck 7 is RED on one assertion, and one test is flaky. Fix both, then request precheck 8

CI moved to ivanopcode/codex (slim relux-ci: one run per precheck). Precheck 7 is run 38004388813, snapshot wip-7 466a1c23
(= your tree b714b408). The interrupt-test timing fix WORKS: lint, small and app-server are GREEN, and core has 5084 of 5085
passing. Every one of the 7 mutants failed, but a red snapshot voids them, and `interrupted_notice_delivered_twice` was killed
ONLY by the test that also fails on the snapshot. `mini-producer-addendum.md` applies (cargo fmt allowed and required; no other cargo).

1. `goal_wait_registered_parent_gets_single_interrupted_notice` FAILS 3/3 at `core/tests/suite/goal_native_wait.rs:885`:
   `assert!(!wake_body.contains("FINAL_ANSWER"))`. The wake request DID contain exactly one INTERRUPTED notice, so the
   earlier assertions pass. Most likely cause, which you must confirm from the code: `wake_body` is the WHOLE request JSON,
   and the multi-agent instructions (`prompts/src/model_messages/multi_agent.rs`, and possibly the model instructions)
   mention `FINAL_ANSWER` as a message type in every request. So the assertion is too broad. Fix it so it still proves
   what AC7 needs: no `Message Type: FINAL_ANSWER` notice for THIS child's interrupted transition. For example, assert on
   the inter-agent message items of the request (the input item carrying the INTERRUPTED notice, and that no input item is a
   FINAL_ANSWER completion message from this child), not on the serialized body. The same applies to the
   `"completed successfully"` check. If instead you find that a real completion message IS delivered alongside, that is a
   production bug: fix it in production and say so.
2. FLAKY: `goal_wait_latch_closes_completion_before_registration` failed on try 1 and passed on try 2. This is the race test
   for AC3, and it must be deterministic. Find the nondeterminism (the order of mock requests, an unbounded race between the
   fast child's completion and the gate, or a timing-based wait) and remove it. Do not add retries or sleeps to paper over it.
3. Keep `interrupted_notice_delivered_twice` killed by an ASSERTION on a passing candidate. After item 1, the test must still
   count exactly one INTERRUPTED notice for the transition. All 7 mutant patches must apply to your final tree.
4. Mutant test filter used by CI (tell me if a killer test falls outside it):
   `test(goal_native_wait) | test(native_wait) | test(owned_children) | test(interrupted) | test(native_pending) | test(foreign_sleep) | test(conditional_remove)`.
Run `cargo fmt` plus `--check` (exit 0), leave everything UNCOMMITTED, report the final tree id, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 8`, and end your turn without handing off.
