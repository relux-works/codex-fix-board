# Surface table — TASK-260929-csnn3a f1-regressions-and-failure-paths

| Row | Invariant | Attack families |
|---|---|---|
| F1a cleared reservation | when inject_if_running accepts a bare ActiveTurn and a settings failure drops the reservation, the retained runtime mail is still eventually sampled exactly once; a reserved idle start backs off (no lost, duplicate or stolen wake) when the turn was replaced or is busy | retain only task-present input; reserved claim ignoring turn identity or task presence; cleared reservation with no follow-up wake; double sampling after recovery |
| F1b finishing task | pending input recorded into history by a finishing task is not acknowledgment: the mailbox scheduler still produces a sampling request containing it, and only that request's acceptance acknowledges it | acknowledge on recording; fail only the first tracked lease; finishing-task race with the scheduler; history append without a sampling wake |
| compaction, guardian and transport | compaction or guardian omission leaves the receipt pending, and it is sampled by a later request; the guardian path preserves recorded fragments (a stated bound only with a code citation); transport failure keeps it pending with bounded retries, then visible suspension; HTTP/WS fallback acknowledges only the transport that submitted it; no history duplicates across retries | compaction acknowledging staged receipts; guardian prep dropping exec fragments; acknowledgment skipped when websockets are enabled; HTTP fallback; retry duplication |

```surface-table
{"rows": ["F1a cleared reservation", "F1b finishing task", "compaction, guardian and transport"]}
```
