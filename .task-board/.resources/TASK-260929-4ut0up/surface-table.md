# Surface table — TASK-260929-4ut0up watcher-and-output-retention-hooks

| Row | Invariant | Attack families |
|---|---|---|
| receipt hooks in unified exec | an opted-in process yields exactly one terminal outcome per receipt (inline result, one queued completion, or a cancellation with reason) published only after exit, output drain, denial settling and final classification; retained output is bounded (1 MiB head/tail with truncation indicated) and readable only by its owner; slots are freed exactly on inline delivery, release, owner stop/shutdown or retirement of sampled output; default (non-opted-in) launches are byte-for-byte unchanged | exit before/after the initial yield (both orders forced); drain/denial monitor held while exit is observed; 3 MiB output; 64/65 capacity with mixed states and LRU retirement; stdin claim vs pushed claim race; release vs terminate vs interrupt vs shutdown; foreign/unknown receipt reads; default launches beyond 64 processes; process-store removal before the read |

```surface-table
{"rows": ["receipt hooks in unified exec"]}
```
