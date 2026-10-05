# Surface table — TASK-260929-1ma0pr exec-completion-fragment-and-turninput

| Row | Invariant | Attack families |
|---|---|---|
| exec-completion fragment | the whole escaped fragment is <= 768 UTF-8 bytes and carries only receipt/process ids and exit/failure/timeout/retention state (no command, no raw output); it uses the recognized internal-context wrapper and classifier; its text is data, so injected markers, newlines or closing tags cannot break out, acknowledge receipts or authorize actions; a forged exec-completion item in history creates no receipt privilege | boundary sizes (767/768/769 bytes, multibyte UTF-8); marker/tag injection in every field; newline injection; classifier treating it as user text; a forged item seeded through rollout/resume history |
| batching and retention | at most 8 fragments go into one request (<= 6144 bytes), and the remainder stays leased/retained and is sampled by a later wake with no loss and no duplicate; an in-turn follow-up does not count idle-only runtime entries (has_pending_input), so no re-sample spin | 9 pending -> 8+1; exactly 8; cap off-by-one; remainder lost vs duplicated; spin on capped remainder; interaction with C1 leases (ack/fail) and suspended entries |
| internal TurnInput variant and persistence | the internal exec-completion TurnInput variant refuses public serialization; the user-input variant serializes byte-identically to before; the exhaustive app-server TurnInput uses (request_processors.rs, thread_queue_processor.rs persistence) handle the variant; persisted history keeps only the contextual ResponseItems with no trigger metadata, so resume never rearms or wakes from text | serialize the internal variant (empty or non-empty); byte-identity of the existing variant; app-server queue persistence round trip; resume after a wake turn stays silent; trigger metadata leaking into the rollout |

```surface-table
{"rows": ["exec-completion fragment", "batching and retention", "internal TurnInput variant and persistence"]}
```
