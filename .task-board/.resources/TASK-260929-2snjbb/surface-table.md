# Surface table — TASK-260929-2snjbb goal-background-wait-policy

| Row | Invariant | Attack families |
|---|---|---|
| gate scope and fairness | only automatic goal continuation is gated by known pending exec work; user and follow-up input, inter-agent mail and trigger mail are admitted immediately; inactive or budget-limited goals and unopted or server-only processes never engage the gate; a failed snapshot read is never treated as no pending work | over-gating non-goal triggers or user input; read error mapped to empty; Armed ignored (only Queued gated); budget-limited or inactive goal gated; global idle suppression |
| check-in tickets and warning | fallback check-ins at 30, 60 and 120 minutes (fake time), at most three per human input; each ticket bypasses only the work gate, exactly once, and no status, Plan, shutdown, capacity, input or newer-turn check; after the third, the exact warning is emitted once and the goal stays active and wakeable; human input renews, a completion pre-empts timers without counting as human input | ticket id reuse; repeated bypass; wrong intervals or cap; warning repeats or wrong text; goal marked paused, blocked or complete; a late completion counted as human input |
| admission recheck and invalidation | the new automatic-admission contributor rechecks the E1 revision so a receipt transition between the continuation check and turn start is caught; tickets are invalidated on steering, turn start, goal mutation, clear, stop and release; resume discards stale waits; release of a mis-armed subscription lets paced continuation proceed without a kill; the goal semaphore is never held across a delay | skipped revision recheck; ticket preserved across invalidation; a different revision source; semaphore held during delay; stale wait surviving resume |

```surface-table
{"rows": ["gate scope and fairness", "check-in tickets and warning", "admission recheck and invalidation"]}
```
