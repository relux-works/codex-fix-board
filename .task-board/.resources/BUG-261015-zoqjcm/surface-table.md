# Surface table — BUG-261015-zoqjcm reserved-tool-schema-rejected

| Row | Invariant | Attack families |
|---|---|---|
| advertised wire schema | every parameter P1 touched (wait_agent v1/v2 timeout_ms; exec_command yield_time_ms, max_output_tokens; write_stdin session_id, yield_time_ms, max_output_tokens; clock.sleep duration_ms; create_goal token_budget) is advertised byte-identically to upstream 0462dcc: type, description, required, additionalProperties (AC1) | one parameter left as integer; description or required list drifted while fixing types; a tool missed (v2, goal extension); upstream compared against the wrong base |
| snapshots | `git diff 0462dcc -- '*.snap'` is empty; no snapshot refreshed to hide a remaining schema drift (AC1) | a hash line refreshed instead of restored; a snapshot outside the 17 changed; insta .snap.new left behind |
| tolerant parsing kept | the P1 deserializers and their consumers are unchanged; 60000.0 and 6e4 still accepted, fractions, overflow, sign errors and wrong types still refused (AC2) | deserialize_with dropped together with the schema revert; parsing tests weakened or deleted; guardian or rollout-trace reader reverted |
| regression pin | a wire-contract test pins each tool's full advertised parameters to literal upstream JSON and fails on a type flip or description change; it is a real comparison, not a self-comparison (AC3) | pin generated from the code under test; partial-field comparison that misses a type flip; pin only for some tools; negative integer check missing |
| scope and later patches | no change to P4a/P4c/P5 behaviour, exec_notification or parsing; any other drift of an upstream tool schema introduced by later patches is reported, not silently kept or reverted | P5 notify_on_exit removed without a decision; unrelated refactors; README/docs/CI edits |

```surface-table
{"rows": ["advertised wire schema", "snapshots", "tolerant parsing kept", "regression pin", "scope and later patches"]}
```
