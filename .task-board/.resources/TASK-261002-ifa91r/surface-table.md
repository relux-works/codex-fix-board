# Surface table — TASK-261002-ifa91r p1-astra-snapshot-refresh

| Row | Invariant | Attack families |
|---|---|---|
| snapshot fidelity | the candidate changes exactly the 12 hash lines the hosted insta diff reports (6 per file) in the two astra scenario snapshots, to exactly the hosted "new results" values; no other file or line changes; afterwards no stale clock/collaboration fingerprint remains anywhere in codex-rs | line-by-line comparison against the hosted core job log (runs 36959471910 / 36959934198); `git grep` for the old hashes f402e8c5e9b5e317, fd994b11525da73c, 32be5470c6e39932, 4327e247f74ba810; consistency with the 8 astra snapshots P1 already refreshed (same new namespace hashes); whitespace/trailing-newline drift; header lines untouched |

```surface-table
{"rows": ["snapshot fidelity"]}
```
