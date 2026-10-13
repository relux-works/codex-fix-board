# TASK-260929-309h9n (P4b-2): orchestrator nextest timeout override before precheck 4

The "+1 timed out" in precheck 3's app-server lane was this task's own end-to-end test
(`suite::v2::goal_continuation_pacing::goal_pacing_two_polls_grow_streak_with_30s_then_60s_delays`, TMT at 60.0 s, 3/3):
the default nextest profile terminates at 30 s x 2. The reworked test
(`goal_pacing_two_polls_first_immediate_second_60s`) waits a real 60 s n=2 delay plus an 8 s no-third-turn window through a live
app-server (~75 s by the producer's estimate), so it would time out again.
Fix: one exact-name override in `codex-rs/.config/nextest.toml`, in the style of the existing long end-to-end overrides:
`slow-timeout = { period = "1m", terminate-after = 2 }` (120 s) for that single test. No test or product change.
Producer rework tree plus this override: 181cc48fbd0b; fmt --check exit 0; all 6 board mutants `git apply --check` clean.
The autonomous successor RUN-261011-b45417 was cancelled before snapshotting (worktree verified unchanged by it).
