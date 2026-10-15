# Surface table — TASK-260929-3rdnra v1-subagent-notification-bridge

| Row | Invariant | Attack families |
|---|---|---|
| V1 delivery channel | a V1 child completion reaches the parent only as queue-only runtime-mailbox data built from the same bounded SubagentNotification fragment; no direct transcript injection remains (AC1) | direct inject restored on some path; fragment sent twice (mailbox plus inject); trigger_turn set on the queued item; a different, unbounded fragment on the new path |
| wake permission | a V1 parent with a registered goal-owned wait (G1 SleepItem) is woken by a real model request; a parent without one makes no request of its own, and the data reaches its next turn instead of being dropped; V2 results never wake an ordinary parent (AC2, AC7) | wake without a registered wait; drop for parents without a wait; data visible only after an extra unwanted request; counts asserted against the wrong mock (capture-order trap) |
| identity and paths | no fabricated AgentPath appears in the V1 fragment, events or history; V1 identifies the child by thread id only (AC3) | `/root/...` path synthesized for V1; path leaked through an event; V2 path formatting changed |
| status matrix and bounds | completed, error, closed and interrupted each produce the correct bounded fragment for V1 and V2; payloads stay bounded and valid JSON under escaped, unicode and oversized inputs (AC4) | status mapped to the wrong text; interrupted claims success; unbounded error text; truncation that splits UTF-8 or breaks JSON |
| mid-turn and idle history | a second child finishing mid-turn is delivered exactly once; idle recording writes the fragment to history once with correct stamping (id, turn id, create time) and never re-appends it when the queued mail is drained or a turn starts (AC5, AC6) | lost mid-turn delivery; duplicate on drain; re-append on turn start; a stale or synthetic turn_id stamped on an idle record |
| transcript change and regressions | the before/after parent history change for V1 is asserted; existing upstream tests (subagent_notification_is_included_without_wait, pending_input, G1 native wait, P4a scheduled check-ins) stay green and unweakened (AC6, AC7) | upstream assertion weakened; transcript asserted by presence only; P4a timing test made non-deterministic or its counts loosened |

```surface-table
{"rows": ["V1 delivery channel", "wake permission", "identity and paths", "status matrix and bounds", "mid-turn and idle history", "transcript change and regressions"]}
```
