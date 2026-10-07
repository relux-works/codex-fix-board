# Surface table — TASK-260929-3f6hfg goal-background-wait-vertical-test

| Row | Invariant | Attack families |
|---|---|---|
| controlled-exit vertical | through real JSON-RPC and tool dispatch: goal created, barrier-controlled process launched with notify_on_exit, turn ended; zero continuation model requests while the process runs; after release, exactly one wake request carrying the exec-completion fragment for the right receipt, then goal progress; a stalled runtime fails the test | drop the wake; wake without the fragment; extra continuation requests while gated; wrong receipt; test that passes on a stalled runtime |
| negatives | on a headless or incapable host notify_on_exit is not advertised and no wake is promised; an unopted server process does not gate continuation; user input queued or burst during the wait is admitted immediately without loss or duplication | allow notify on an incapable host; always subscribe; gating on unopted processes; dropped or duplicated user input during the wait |
| harness quality | deterministic barriers or latches with no sleeps; runs on the hosted app-server lane using the repo's remote-test helpers; any platform skips explicit and justified; mutants target production behavior, not only the test | sleep-based timing; silent skips; mutants killed only by unrelated tests |

```surface-table
{"rows": ["controlled-exit vertical", "negatives", "harness quality"]}
```
