# TASK-260929-csyzcj (G1): hosted precheck 6 is RED. Your two new interrupt tests fail on the candidate, and lint fmt fails. Fix both, then request precheck 7

Precheck 6: snapshot wip-6 7c2072c8 (tree 3c919459 = your worktree), run 37869022037. small and app-server are GREEN.
A red snapshot voids every mutant result. Note also that every mutant "killed" only the two new tests, which fail anyway.
The typed fragment itself is fine: `interrupted_fragment_renders_exact_notice_body` passes. `g1-rework-mini-addendum.md` still applies.

1. core: both new tests fail deterministically on all 3 tries, and both fail at the SAME kind of assertion:
   - `goal_wait_registered_parent_gets_single_interrupted_notice` panics at `goal_native_wait.rs:834`:
     `assert_eq!(child_sleep.requests().len(), 1)` got **0**.
   - `goal_wait_ordinary_parent_stays_quiet_on_child_interrupt` panics at `goal_native_wait.rs:973`:
     `assert_eq!(child_sleep.requests().len(), 1)` got **0**.
   The child's sleep request has not reached the mock when you assert, or the mock matcher never matches the child's
   real request. Find out which by reading the existing passing tests in this file, which wait for their children
   correctly. Then (a) wait deterministically, with a bounded timeout and a clear panic, until the child's request has
   arrived and the child is actually Running before you interrupt it, and (b) make sure each mock matches exactly one
   real request. Do not delete these assertions. They prove that the interrupt hits a Running child, which is the whole
   point of the test.
2. lint, `just fmt-check`, at `goal_native_wait.rs:844` and `:954`. This time you OVER-broke a call that fits on one line.
   rustfmt wants exactly this, in both places:
   ```rust
       wait_for_event(&child, |event| matches!(event, EventMsg::TurnAborted(_))).await;
   ```
   The rule: rustfmt keeps a call on ONE line if it fits within 100 columns (counting indentation), and only breaks it
   when it doesn't fit. Check every call you added or changed against that rule in both directions.
   Clippy did not run again, because fmt failed first, so re-read your new code for clippy issues as well.
3. After the fix, the interrupt tests must still kill `interrupted_notice_delivered_twice` and `interrupted_claims_success`
   with an assertion. Make sure all 7 mutant patches apply to your FINAL tree, re-attach the mutants and results files,
   and report the final tree id computed AFTER your last edit (last time you reported bcf50ef6, but the real final tree was
   3c919459).
Leave everything UNCOMMITTED, add the note `HOSTED-PRECHECK-REQUESTED: precheck 7`, and end your turn without handing off.
