# TASK-260929-2snjbb (E2): CR revision 4. Linearization point, rejection without effects, real runtime integration test

Review round 3 (`TASK-260929-2snjbb_review-verdict-rev3.md`, outcome; tb-R209 panels: codex sol high + muse max + delta) is
**changes_requested**. Gate scope held. Panel B accepted; panel A and delta report two repeated classes, plus one new finding.
"Check later" does not converge: any comparison followed by an await before the turn is published stays racy, because
receipt Arm uses its own mutex. Implement the following design EXACTLY.

1. LINEARIZATION POINT (findings revision-recheck-before-await-window, repeat).
   Carry the admitted work revision INTO start_task as a parameter for automatic goal continuation. Do the FINAL comparison
   inside start_task, under the same lock/critical section that publishes the started turn (immediately before
   record_started_turn), with NO await between the comparison and the publication. That publication is the linearization
   point. An Arm that happens before it is caught and rejects the automatic start. An Arm after it is, by definition, work
   arriving after the turn started, which is legitimate (the turn is running and the receipt is delivered later).
   Document this rule in a code comment at the comparison. The earlier comparisons may stay as fast-path rejections, but
   only the linearization-point check is authoritative. If start_task's existing locks make a single critical section
   impossible, stop and explain the constraint precisely in the results instead of adding another early check.
2. REJECTION WITHOUT EFFECTS (finding rejected-goal-start-commits-settings).
   A rejected automatic goal start must leave no observable effect: no settings commit, no ThreadSettingsApplied
   notification, no ownerless reservation, and the ticket handled per AC4. Either automatic goal continuation carries no
   settings delta (assert it and test it), or defer apply_started's commit and notification until after the
   linearization-point check. Test: an automatic start rejected at the linearization point leaves thread settings and
   emitted notifications byte-identical to before (narrowing mutant: apply settings before the final check).
3. REAL RUNTIME INTEGRATION TEST (finding scheduled-checkin-regression-not-exercised, repeat).
   Delete the test-local spawn_check_in_reentry helper. Add a suite test (core/tests/suite or the goal extension's
   integration tests) that builds a REAL session with the goal extension and the background-wait policy ENABLED through test
   config. Activation stays off by default; enabling it in a test is in scope for stage 2d. With an unchanged Armed
   receipt and paused tokio time, advancing time alone makes the production CheckInTimer -> GoalRuntimeHandle re-entry
   (runtime.rs Wait arm, continue_if_idle -> Core start_turn_if_idle) start a real turn that is marked automatic. After the
   third check-in, the production warning is emitted once. Narrowing mutant: break the runtime Wait-arm re-entry (not
   CheckInTimer::spawn); it must be killed by this test. Do not claim deferral to stage 2e.
4. Race test for item 1: drive an Arm in the residual interval inside start_task (a latch on the token-usage or state-lock
   await), and assert the automatic start is rejected. A second case arms just after publication and asserts the turn runs
   and the receipt stays pending. Mutant: move the final comparison before the awaits.
Keep all other E2, E1 and D tests green. Generate mutant patches with `git diff`. Update and re-attach the results and
mutants files. Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 5". Do NOT hand off.
local-build-allowance.md applies under all its gates (narrow filters). Follow R176 and R174.
