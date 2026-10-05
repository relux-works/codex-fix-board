# Surface table — TASK-260929-2fa1hy goal-activity-marker-and-sleep-gate

| Row | Invariant | Attack families |
|---|---|---|
| capability gate | clock.sleep is registered for a ModelDriven session exactly when (reminder feature off AND (model_has_clock OR a GoalActivity marker is present)) or (reminder feature on AND current_time_reminder.sleep_tool); features.sleep_tool disabled always wins; AlwaysOn unchanged | marker absent/present/removed between sampling steps; BudgetLimited vs Active; reminder feature explicit on with sleep_tool false or absent; hard disable; AlwaysOn; model catalog with and without clock; code-mode exposure (sleep stays DirectModelOnly); marker type spoofed by an unrelated ExtensionData entry |

```surface-table
{"rows": ["capability gate"]}
```
