# Surface table — TASK-260929-17t419 wire-integer-arguments-into-waiting-tools

| Row | Invariant | Attack families |
|---|---|---|
| error surface | Every waiting-tool call with a non-integral or wrong-typed number returns the existing structured argument-error output through the real handler; integral decimals are accepted; tool payloads outside the named fields (dynamic, MCP, extension, plan) are forwarded byte-for-byte unchanged | fractional values on each annotated field; string/boolean values; accepted 1000.0-style values on each field through the production entry point; dynamic tool payload containing 1.0; create_goal token_budget decimals; advertised schema drift beyond the named parameters; code-mode invocation path |

```surface-table
{"rows": ["error surface"]}
```
