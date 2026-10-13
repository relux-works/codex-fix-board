# Surface table — TASK-260929-csyzcj goal-owned-durable-sleep-lease

| Row | Invariant | Attack families |
|---|---|---|
| registration and wake | a goal parent with a Running native child registers exactly one owned marker at idle, and the child's queue-only completion wakes the parent with a real model request (AC1) | marker present but no wake; wake without marker; double registration; wake asserted by marker presence instead of request |
| eligibility and inspection errors | no marker for non-goal threads, unloaded or unknown children, or failed inspection; inspection errors propagate and never read as "no children" or "not pending" (AC2) | skipped failed lookups; error mapped to empty; non-goal thread registering; unknown child treated as Running |
| completion-before-registration race | a child finishing between the idle inspection and the marker insert still wakes the parent; the mail recheck happens after the insert under the same serialization (AC3) | insert after the mail check; recheck before insert; a lost wake when the completion lands in the window; tests that hang instead of failing |
| foreign sleep ownership | insert_if never clobbers a foreign SleepItem; the conditional remove removes only the owned id (AC4) | clobbering one foreign item; unconditional remove; id reuse; foreign marker lost across register and turn start |
| marker lifecycle | removal on admitted turn start, goal clear/disable, thread stop and release; on a check-in it is removed, then reinserted at idle while still waiting; kept after the check-ins are exhausted, so a late completion still wakes; resume does not revive it (AC5, AC9) | marker surviving turn start; stale marker after goal clear; reinsertion missing after a check-in; marker dropped after exhausted check-ins; revived on resume |
| side-effect silence | storing the marker emits no sleep UI events, no history item and no reminder change (AC6) | a UI event emitted on insert; a history item written; reminder schedule altered |
| child state transitions | an Interrupted child yields exactly one queue-only notice per transition, global is_final unchanged, and the notice never claims success; reused, error and second-child-mid-turn cases behave per state; inherited turn settings are preserved on wake (AC7, AC8) | interrupted claims success; duplicate notices; is_final flipped; a second child mid-turn lost; settings reset on wake |

```surface-table
{"rows": ["registration and wake", "eligibility and inspection errors", "completion-before-registration race", "foreign sleep ownership", "marker lifecycle", "side-effect silence", "child state transitions"]}
```
