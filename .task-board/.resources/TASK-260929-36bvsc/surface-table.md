# Surface table — TASK-260929-36bvsc thread-pending-work-snapshot

| Row | Invariant | Attack families |
|---|---|---|
| snapshot contents | the snapshot reports exactly the Armed receipts plus the unsampled, non-suspended Queued/Leased runtime entries, each receipt once; never live servers, acknowledged, cancelled or suspended entries; not derived from list_processes | double counting across the B store and the mailbox; suspended admitted; queued excluded; server processes leaking in; acknowledged or cancelled still reported |
| revision and atomicity | the work revision strictly increases on every arm, queue, lease, fail-back, acknowledge, cancel, suspend and release transition; Armed->Queued is atomic for concurrent readers (never in neither set, never in both) | a transition that skips the bump; a concurrent reader during Armed->Queued; revision reuse after release; ordering under contention |
| read failure and API boundary | a failed or contended read returns an explicit error, never an empty snapshot, including through the goal-side API; ext/goal reads it through the extension API with no core->goal dependency | provider missing mapped to empty; contended store mapped to empty; goal adapter swallowing the error; dependency direction |

```surface-table
{"rows": ["snapshot contents", "revision and atomicity", "read failure and API boundary"]}
```
