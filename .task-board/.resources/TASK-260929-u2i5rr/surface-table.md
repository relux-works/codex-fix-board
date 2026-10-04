# Surface table — TASK-260929-u2i5rr receipt-state-machine

| Row | Invariant | Attack families |
|---|---|---|
| concurrency state machine | every reserved receipt ends in exactly one terminal outcome (InlineResult, Sampled once, or Cancelled with reason); no lost exit, no duplicate claim, no slot leak; capacity 64 enforced before launch | exit before/after the initial-response decision (both orders forced with barriers); lease failure and stale lease tokens; cancel from each state; double sample; stdin claim vs pushed claim race; 64/65 capacity and slot release; generation mismatch (receipt from another thread/generation); panics or poisoned locks surfacing as structured errors |

```surface-table
{"rows": ["concurrency state machine"]}
```
