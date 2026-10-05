# Surface table — TASK-260929-2gp04j goal-activity-publisher-hooks

| Row | Invariant | Attack families |
|---|---|---|
| goal activity publisher | the GoalActivity marker in thread extension data always reflects COMMITTED goal state: present (Active or BudgetLimited, correct identity/revision) exactly when the committed goal is Active or BudgetLimited, absent otherwise; one publisher is the only writer; a stale callback never reinserts a cleared or older goal; a read failure removes the marker and the next lifecycle event reconciles | create success vs failure; turn start through the missing-token-baseline and Plan-mode early returns; resume and external set per status; update_goal / automatic stop / accounting limit; clear with feature enablement off; thread stop, feature disable and re-enable; injected goal-store read failure; revision race (late create/update callback after clear); duplicate or out-of-order lifecycle events; end-to-end app-server create -> next request |

```surface-table
{"rows": ["goal activity publisher"]}
```
