# TASK-260929-36bvsc: thread-pending-work-snapshot

## Description
Thread-level pending-work snapshot for the goal waiting policy (final plan section 6 'Expose a minimal typed snapshot'; stage 2d, leaf 1 of STORY p4a-goal-background-wait; stacked on landed P5-2c, relux/main 812b8037). Add a minimal typed, read-only snapshot of the thread's pending exec-completion work: Armed receipts (B state machine), unsampled Queued/Leased runtime-mailbox entries (C1 leases, not suspended), and a monotonically increasing work revision that changes on every reservation or receipt transition (arm, queue, lease, fail-back, acknowledge, cancel, suspend, release). Expose it through the extension-facing API (codex-extension-api or thread extension data) so ext/goal can read it at goal continuation without a core->goal dependency. Do NOT use list_processes: it is live-only and includes servers. A failed read is an explicit error variant, never an empty snapshot. Armed->Queued is observed atomically (never a moment where a receipt is in neither set). Suspended (retry-exhausted) entries are excluded from pending work. Out of scope: the policy that consumes it (TASK-260929-2snjbb, E2).

## Scope
(define task scope)

## Acceptance Criteria
AC1 The snapshot reports Armed receipts plus unsampled, non-suspended Queued/Leased entries, and nothing else (no live servers, no acknowledged or suspended entries). AC2 The revision strictly increases on each arm, queue, lease, fail-back, acknowledge, cancel, suspend and release transition. A named test drives each one. AC3 A read failure returns an explicit error, distinct from an empty snapshot. A narrowing mutant mapping error to empty must fail a named test. AC4 Armed->Queued is atomic with respect to the snapshot: a concurrent reader never sees the receipt in neither set (latch-driven test). AC5 ext/goal can call it through the extension API with no new core->goal dependency (compile-level evidence plus a goal-side unit test using it).
