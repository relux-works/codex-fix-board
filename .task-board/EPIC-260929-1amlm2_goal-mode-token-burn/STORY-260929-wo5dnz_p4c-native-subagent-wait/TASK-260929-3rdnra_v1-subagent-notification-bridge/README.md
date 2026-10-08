# TASK-260929-3rdnra: v1-subagent-notification-bridge

## Description
V1 subagent notification bridge (final plan section 7 'Bridge V1'; leaf 2 of STORY p4c-native-subagent-wait; verdict rev3 note 7: the V1 transcript change needs a test). Intra-story order: runs after sibling TASK-260929-csyzcj (G1) is accepted and checkpointed. core/src/agent/control.rs (re-locate ~:510-518) currently injects SubagentNotification directly for V1, bypassing the wake path. Instead, send the same bounded notification fragment as queue-only runtime-mailbox data. Fabricate no AgentPath. The goal-owned SleepItem (G1) supplies wake permission; ordinary parents without a registered wait stay quiet (no wake). Cover the completed, error, closed and interrupted child statuses, plus another child finishing mid-turn, for BOTH V1 and V2. The V1 transcript change must be asserted by a test (what the parent's history now contains versus before).

## Scope
(define task scope)

## Acceptance Criteria
AC1 For V1, a child's completion reaches the parent as queue-only runtime-mailbox data, with no direct transcript injection (narrowing mutant: restore the direct inject). AC2 A V1 parent with a registered goal wait is woken. A V1 parent without one is not woken (asserted request counts). AC3 No fabricated AgentPath appears in the fragment or the events. AC4 Completed, error, closed and interrupted statuses each produce the bounded fragment correctly for V1 and V2 (parameterized). AC5 A second child finishing mid-turn is delivered once, without loss or duplication. AC6 The V1 transcript change is asserted (a before/after history test). AC7 V2 behavior is unchanged (existing pending_input tests extended for both versions).
