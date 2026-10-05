# Hosted pre-handoff evidence: TASK-260929-2fa1hy (G1 goal-activity-marker-and-sleep-gate), precheck 1

Orchestrator-run under the codex-fix hosted-CI model. The fast local lane forbids local codex-core suites, so the
producer's current-candidate core execution and narrowing-mutant replay ran on GitHub-hosted relux-ci.

## Snapshot of the exact pre-handoff worktree
- commit `dc09022358edd7d4f59c13c8f282b5b9df2cd1e5` (signed, never landed), tree `403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd` = Story workspace
  STORY-260929-bohnqb (base ea8899e plus the 5 uncommitted G1 paths) at 08:13Z
- run https://github.com/relux-works/codex/actions/runs/36983853906: **success**, all lanes (lint, small, core, app-server)
- core: 4860 run, 4860 passed (2 flaky passed on retry), 11 skipped. All 6 G1 request tests PASS:
  - goal_activity_controls_model_driven_sleep_on_each_sampling_request::{direct_tools, code_mode}
  - disabled_sleep_tool_feature_wins_over_goal_activity
  - current_time_reminder_sleep_setting_overrides_goal_activity::{explicit_true, explicit_false, missing_config}

## Narrowing mutants (patches from TASK-260929-2fa1hy_mutants.json, each applied on the snapshot tree)
| mutant | commit | run | core lane | killing test(s) |
| --- | --- | --- | --- | --- |
| hard_disable_bypass | 859b052 | 36983895784 | failure (1 failed) | disabled_sleep_tool_feature_wins_over_goal_activity |
| reminder_false_bypass | c53f17d | 36983937144 | failure (1 failed) | current_time_reminder_sleep_setting_overrides_goal_activity::explicit_false |
| no_marker_admitted | 1eb8590 | 36983916432 | failure (27 failed) | goal_activity_controls_model_driven_sleep_on_each_sampling_request (+ spec_plan/code_mode tests); lint also fails (unused field) |

All three mutants are killed by their named tests on hosted runners.
