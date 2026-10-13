# Surface table — TASK-260929-3ld28o state-change-observations

| Row | Invariant | Attack families |
|---|---|---|
| reset sources at committing handlers | only an applied file change, an actual plan transition, a committed goal mutation and an accepted spawn/follow-up set the observation, each recorded at its committing handler or event, never at ToolFinish success (AC1) | recording at ToolFinish; a failed or declined patch counted as applied; a goal create that failed counted; a spawn rejection counted; send_input counted when not accepted |
| non-resets | failed tools, identical plan resubmissions, read-only and arbitrary shell success, code-mode wrapper success and model text claiming progress never set it (AC2) | identical plan counted as a transition; shell success counted; a keyword in model text counted; a command execution item counted |
| code-mode leaf accounting | a nested leaf with an applied change yields exactly one observation; the wrapper adds none (AC3) | double counting; the wrapper counted; a leaf missed |
| no model-writable bypass | no tool argument, plan text or message content can set the observation (AC4) | a plan field or message content that sets it; a goal tool argument that sets it |
| existing activity and blocker untouched | existing activity booleans and the three-fully-empty-continuations blocker behave exactly as before; the blocker still fires first (AC5) | the blocker order changed; activity booleans altered; the observation feeding the blocker |
| transient state | the observation is per goal turn, not persisted to rollout or history; resume and fresh runtime carry none (AC6) | persisted observation; carried across turns; revived on resume |
| API surface and placement | new extension-api surface (tool lifecycle contributor / plan-committed hook) is minimal and bounded; core changes are thin hooks only; no core->goal dependency (scope) | core growth beyond hooks; an unbounded or model-visible field; a broken extension-api contract for existing contributors |

```surface-table
{"rows": ["reset sources at committing handlers", "non-resets", "code-mode leaf accounting", "no model-writable bypass", "existing activity and blocker untouched", "transient state", "API surface and placement"]}
```
