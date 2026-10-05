# TASK-260929-1rcgsj: input-queue-runtime-leases

## Description
Internal runtime-notification mailbox entries for exec completions (final plan 5.2; verdict rev3 note 1; stage 2b, leaf 1 of STORY p5-runtime-mailbox). InputQueue gains a runtime-notification entry kind carrying a B receipt reference. It is a named internal variant, never a fake InterAgentCommunication. Runtime entries are NOT removed by drain: they stay logically leased until the receipt is acknowledged as sampled or is cancelled. A failed sampling attempt returns the entry unleased, so it is retried later without a duplicate. Trigger-mail queries (has_trigger_turn_mailbox_items and drain's trigger selection) include unsampled, non-suspended runtime entries, so they keep priority over goal continuation. Suspended entries (retry exhausted) are excluded, so they never block start_if_idle or suppress idle contributors (note 1). Idle wake belongs to maybe_start_turn_for_pending_work: a pending runtime entry is pending work with trigger exec_completion. It preserves the thread's execution settings, invents no initiating agent and resets no human quota. Inter-agent mail semantics stay unchanged. Out of scope: the context fragment and TurnInput variant (C2), sampling acknowledgement wiring (story D), tool exposure (story F).

## Scope
codex-rs/core/src/session/input_queue.rs (or a new small sibling module for runtime entries), the trigger query in core/src/session/turn_input.rs, and the trigger/settings selection in core/src/tasks/mod.rs maybe_start_turn_for_pending_work, plus tests. No protocol or app-server changes.

## Acceptance Criteria
| # | Requirement | Driving test (production entry) | Negative/refusal |
| - | ----------- | ------------------------------- | ---------------- |
| 1 | A runtime entry survives drain as leased: drain hands it to the turn, a second drain does not re-offer it while leased, acknowledgement removes it, and a failed sampling returns it unleased exactly once | InputQueue unit tests through the public crate API | double acknowledgement is refused or a no-op; a failed-then-retried entry is never delivered twice |
| 2 | An unsampled, non-suspended runtime entry counts as trigger mail and suppresses automatic goal continuation | turn_input admission test with an active goal and a pending runtime entry | a SUSPENDED entry does not count: continuation and start_if_idle proceed (note 1) |
| 3 | With no active turn, one pending runtime entry starts exactly one turn via maybe_start_turn_for_pending_work, with trigger exec_completion and the thread's current execution settings | core suite test with mocked responses asserting one sampling request | two runtime entries still start one wake turn; no InterAgent author appears; the human quota is not reset |
| 4 | Inter-agent mail behaviour is unchanged (defer/accept delivery, trigger_turn selection, drain order) | existing input_queue and mailbox tests unchanged | non-trigger inter-agent mail still never starts a turn on its own |
| 5 | Cancelling the receipt removes the runtime entry whether leased or not; a cancelled entry is never re-offered or sampled | unit tests per lease state | a lease token for a cancelled entry cannot acknowledge |

