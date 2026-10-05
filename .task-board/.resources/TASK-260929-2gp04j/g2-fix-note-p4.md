# TASK-260929-2gp04j (G2): one surviving mutant after precheck 4

Precheck 4 (`.temp/goal-token-burn/impl/p2/g2-precheck-4-results.json`): the snapshot is green on all lanes and 19 of 20 mutants are killed. The rev-3 read-failure sweep is confirmed by the new tests.
The survivor is **turn_start_requires_baseline**: with the mutant applied, no test failed. In prechecks 1-3 it was killed by `turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal`, so the rev-3 changes weakened that test or that path.
Restore a test that fails when turn start skips reconciliation for baseline-less turns, without weakening any other test. Keep all 20 mutants, using the fast lane only. Then add the note `HOSTED-PRECHECK-REQUESTED: precheck 5` and end your turn without handing off.
