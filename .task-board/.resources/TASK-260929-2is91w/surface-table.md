# Surface table — TASK-260929-2is91w waiting-capabilities-snapshot

| Row | Invariant | Attack families |
|---|---|---|
| flag derivation | sleep, stdin, native_wait (with its actual tool name), exec_notify (host AND opt-in AND stdin and receipt controls) and native_mail_wait (host AND installed policy) are derived exactly as AC1 states (AC1) | one AND-condition dropped; wrong tool name; native_wait V1/V2 mixed up |
| final-router derivation | flags come from the FINAL captured router after exclusions and name collisions; excluded, shadowed and deferred-not-callable tools are false until discovery (AC2) | derivation from the pre-exclusion list; deferred tool counted; nested-only (code-mode) tool counted as direct |
| subscriptions are not capabilities | acknowledged or pending subscriptions never flip a flag (AC3) | a receipt or ack treated as exec_notify |
| one snapshot, both paths | the same snapshot instance reaches both context paths and the goal contributor within one sampling step (AC4) | recomputed per path; divergence between paths |
| configuration coverage | remote catalog, hard/reminder off, headless/exec, code-mode and an excluded receipt tool behave per spec (AC5) | remote catalog ignored; headless host advertises notifications |
| bounded and transient | the snapshot is a small bounded struct, not persisted to history or rollout (AC6) | unbounded collections; persisted or rewritten history |
| API surface and placement | extension-api surface is minimal; no core->goal dependency; replaces the update_plan_enabled pass-through without behavior loss (scope) | core growth; broken contributor contract; a regression in the plan-enabled signal |

```surface-table
{"rows": ["flag derivation", "final-router derivation", "subscriptions are not capabilities", "one snapshot, both paths", "configuration coverage", "bounded and transient", "API surface and placement"]}
```
