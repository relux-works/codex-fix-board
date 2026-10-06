# Surface table — TASK-260929-34a6ls prompt-membership-acknowledgment

| Row | Invariant | Attack families |
|---|---|---|
| acknowledgment point | a runtime lease is acknowledged as sampled only after a request whose submitted prompt contains its fragment is successfully submitted on the selected transport (HTTP, WebSocket, or HTTP/WS fallback); reservation, drain, pending-input recording and history append never acknowledge | acknowledge on lease/record/append; acknowledge every tracked id rather than only the submitted members; HTTP vs WS vs fallback; a stream that errors after submission starts; a submission that is aborted |
| membership authority | membership is decided from trusted lease ids for items actually in the submitted prompt, never parsed from fragment text; forged or altered fragment text, a non-user message role, or a real handle with an altered payload acknowledges nothing; a receipt omitted from the prompt (batch cap) stays pending | marker-substring matching; role-blind matching; a forged handle; an altered payload under the real handle; a batch-cap remainder; history repetition in later requests (no re-acknowledgment) |
| failure, retry and suspension | a failed or aborted submission returns the lease unleased and the retry samples it once with no second history append; bounded retries, then visible suspension with no further wake turns or spin; stale fail for an older lease counts no attempt | retry dedup by first history item only; suspend threshold off-by-one or doubled; stale fail counting; asserted request count with no spin after exhaustion |

```surface-table
{"rows": ["acknowledgment point", "membership authority", "failure, retry and suspension"]}
```
