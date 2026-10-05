# Surface table — TASK-260929-1rcgsj input-queue-runtime-leases

| Row | Invariant | Attack families |
|---|---|---|
| runtime mailbox lease lifecycle | a runtime-notification entry (named internal variant carrying a receipt reference, never a fake InterAgentCommunication) survives drain as LEASED until its receipt is acknowledged as sampled or cancelled; a failed sampling attempt returns it unleased exactly once and it is retried without duplicate delivery; duplicate enqueue of one receipt never yields two deliveries; cancel removes leased and unleased entries; stale ack/fail for an older lease is refused | drain then ack; drain then fail then re-drain; stale ack/fail after re-lease; duplicate enqueue; cancel while leased vs unleased; interleaving with inter-agent mail (its semantics unchanged); ordering/priority among mixed entries |
| trigger and suspension semantics | has_trigger_turn_mailbox_items and drain's trigger selection count unsampled, non-suspended runtime entries (so they take priority over goal continuation); suspended (retry-exhausted) entries are excluded from trigger, lease and pending-work and never block start_if_idle or suppress idle contributors; suspension of a leased entry stops it suppressing | suspended-only queue; suspended while leased; mixed suspended + live; goal continuation suppressed only by live runtime entries; turn_input admission with goal active vs suspended entries |
| idle wake | maybe_start_turn_for_pending_work treats a pending runtime entry as pending work with trigger exec_completion: exactly one turn for one or many entries, preserved thread execution settings, no invented initiating agent/parent/user input, no human quota reset; a queue with no runtime entries never wakes | one entry; two entries -> one turn; queue-only/inter-agent-only never wakes; busy thread (no wake while a turn runs); settings preservation (model/cwd/approval); no human input fabricated in history |

```surface-table
{"rows": ["runtime mailbox lease lifecycle", "trigger and suspension semantics", "idle wake"]}
```
