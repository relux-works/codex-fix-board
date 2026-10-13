# TASK-260929-309h9n (P4b-2): orchestrator logic fix after precheck 3

Precheck 3 (run 38150062342) small lane: 4 unit tests in `ext/goal/tests/continuation_schedule.rs` failed with every pacing
deadline one doubling short (6030s vs 6060s, 11030s vs 11060s, 18030s vs 18060s, 18890s vs 18980s).
Cause: `BackgroundWaitState::evaluate_pacing_locked` treated the FIRST goal binding (`pacing_goal_id == None`) as a goal switch
and reset `pacing_streak`, `pacing_predecessor` and the rest, discarding what `note_turn_completed` recorded before the first
evaluation. Fix in `ext/goal/src/background_wait.rs`: when the bound goal differs, reset only if a goal was already bound
(`pacing_goal_id.is_some()`), then bind. Goal mutation, clear, stop and resume keep their explicit resets.
fmt --check exit 0; tree 2eff387ce234; all 5 mutants still `git apply --check` clean.
Core and app-server lane failures are NOT addressed here; see `b2-rework-brief-precheck3.md`.
