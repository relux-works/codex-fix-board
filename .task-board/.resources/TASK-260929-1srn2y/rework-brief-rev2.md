# Rework brief — Change Request revision 2 of TASK-260929-1srn2y

You are the researcher producing revision 2. Revision 1 (your gpt-6-astra review) went through review round 1
(claude-fable-5-1, max; run `RUN-260928-a4ac16`) and came back `changes_requested` with two blocking findings and
ten notes. The orchestrator re-verified both blocking findings at the pinned commit.

## Inputs

| Resource | Role |
|---|---|
| `TASK-260929-1srn2y_review-verdict-rev1.md` (outcome on this task) | Round-1 verdict: findings F1/F2, notes N1-N10, adjudication table, section 8 "Corrections the next revision must make". Your prompt also carries its findings array. |
| `TASK-260929-1srn2y_goal-token-burn-astra-review.md` | Your revision-1 document. |
| `research-rev3.md` | Primary plan with section 5 (merge of revision 1) and section 6 (round-1 outcome). |
| `brief.md`, `article.md`, `tekacs-*`, `surface-table.md` | Original brief, source article, fork patch/analysis, and the surface table round 2 will be swept against. |

## Deliverable

ONE self-contained consolidated document: the **final patch series** that the implementation leaf will consume
without needing the earlier documents. Attach it as a new outcome:
`task-board resource add TASK-260929-1srn2y <file> --type outcome --name TASK-260929-1srn2y_goal-token-burn-final-plan.md`

It must contain:

1. **Findings resolution table**: F1, F2, N1-N10 -> how each is resolved (with the section of this document), or
   explicitly rejected with pinned evidence. Held rows from round 1 are not re-litigated without new evidence.
2. **F1 resolution (P5 delivery).** Acceptance means "included in a sampling request". Deliver completions
   through the existing trigger-turn mailbox so `maybe_start_turn_for_pending_work` owns the idle wake and
   `has_trigger_turn_mailbox_items` gives completions priority over goal continuation. Decide, with evidence,
   between a new mailbox/`TurnInput` variant and a runtime-authored `InterAgentCommunication` with
   `trigger_turn = true` (note: that type carries agent author/recipient paths and inter-agent semantics; check
   rollout truncation, `thread_rollout_truncation.rs` trigger-turn boundaries, resume, and UI/event effects).
   Drop the proposed `session/async_input.rs` inbox unless you show the mailbox cannot satisfy an invariant.
   Add the two F1 paths (reservation dropped by `clear_reserved_idle_turn`; injection into a finishing task) to
   the race table, each with a test. Keep the receipt state machine, fragment bound, and headless gating.
   Re-estimate the stage sizes.
3. **F2 resolution (P2 sleep exposure).** Replace "Feature::Goals enabled" with a goal-active marker in
   thread extension data: where the type lives (no `codex-core` -> goal-crate dependency; `codex-extension-api`
   or core), exactly which goal-extension hooks insert and remove it (create success, turn start with an
   active/budget-limited goal, resume; complete, blocked, paused, cleared, thread stop), explicit precedence
   against `current_time_reminder.sleep_tool` and `features.sleep_tool.enabled = false`, and the required
   negative test (non-goal session, non-clock model: no sleep) and positive test (sampling step after
   `create_goal`: sleep present).
4. **Notes that change the design:** N1 (P4b low activity = absence of state-changing outcomes, not tool
   count; measure request counts), N2 (P4c via the existing durable-sleep `SleepItem` marker: verify every side
   effect of inserting it, e.g. UI items, current-time reminders, wake semantics for queue-only mail, and who
   removes it), N4 (model-facing release of a mis-armed subscription; user-visible "automatic check-ins stopped"),
   N5 (`create_goal.token_budget` in P1 or a stated gap), N6 (exact capability flags into the continuation
   template, like `update_plan_enabled`), N3/N8/N9/N10 as applicable.
5. **Final series table**: order, principal files, tests (unit + `core/tests/suite` + `app-server/tests/suite`),
   size, risk. Each stage within the `AGENTS.md` 800-line rule (prefer < 500 for logic). Say where
   `AGENTS.md` "resist adding code to codex-core" pushes code elsewhere.
6. The exact P3 replacement text for `continuation.md`, conditional on the capability flags.

## Rules

- Evidence: pinned upstream `33a0f766a647208b471cfbcad889c67fd324ee04`; read pinned blobs (`git show 33a0f766a6:<path>`);
  cite `path:line`; mark anything unverified.
- Read-only: no tracked-file edits, commits, pushes or PRs. Builds optional and bounded (targeted
  `cargo check -p` or one filtered test only to settle a decisive point).
- Budget: this is a republish; the leaf's 90-minute research budget continues (about 31 minutes were used by
  revision 1), so you have about 55 minutes including packaging. One outcome document, under 45 KB.
- No new research leaf. Anything still open becomes a stated bound for the implementation leaf.
- English.
