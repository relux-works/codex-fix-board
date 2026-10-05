# TASK-260929-2fa1hy: goal-activity-marker-and-sleep-gate

## Description
Scope clock.sleep to active goals without widening it to every session (final plan section 4; round-1 review finding F2). Add a documented capability marker type `GoalActivity` (goal identity/revision + state Active | BudgetLimited) in a new codex-rs/ext/extension-api/src/goal_activity.rs, exported from codex-extension-api (core already depends on it; no core->goal dependency). In core/src/tools/spec_plan.rs keep the SleepTool hard gate and AlwaysOn unchanged; under ModelDriven: when Feature::CurrentTimeReminder is enabled keep consulting current_time_reminder.sleep_tool only; otherwise register sleep when model_has_clock OR a GoalActivity marker is present in session.services.thread_extension_data. The goal extension publisher hooks are the sibling leaf G2; this leaf only adds the type, the gate and tests that insert/remove the marker directly.

## Scope
codex-rs/ext/extension-api (new goal_activity.rs + export) and codex-rs/core/src/tools/spec_plan.rs plus tests. No goal-extension changes (sibling leaf).

## Acceptance Criteria
| # | Requirement | Driving test (production entry) | Negative/refusal |
| - | ----------- | ------------------------------- | ---------------- |
| 1 | ModelDriven + reminder feature off + model without clock + GoalActivity(Active) in thread data => clock.sleep in the sampled request tools | core/tests/suite test (test_codex + mocked responses) asserting the request's tool list | same setup without the marker => clock.sleep absent |
| 2 | GoalActivity(BudgetLimited) also exposes sleep | same harness | marker removed mid-thread => absent on the next sampling request |
| 3 | features.sleep_tool disabled wins over the marker | same harness | marker present + feature disabled => absent |
| 4 | Reminder feature on: only current_time_reminder.sleep_tool decides (explicit precedence edge from round-2 note 2) | same harness | reminder on + sleep_tool=false + marker => absent (stated as intended) |
| 5 | AlwaysOn and model_has_clock behaviour unchanged | existing spec tests / current_time_reminder suite | no non-sleep tool set changes |
| 6 | GoalActivity type documented and exported from codex-extension-api | unit test constructing/inserting it via ExtensionData | none (static values not tested per AGENTS.md) |
