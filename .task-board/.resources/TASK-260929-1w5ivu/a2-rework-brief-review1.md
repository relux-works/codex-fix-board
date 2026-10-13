# TASK-260929-1w5ivu (P3-2): review rev1 changes_requested. Move the waiting guidance into a goal-owned World State section, then request precheck 3

The verdict is `TASK-260929-1w5ivu_review-verdict-rev1.md`. Panel B accepted. Panel A requested changes on two rows; both
findings are real and share one cause: the fragment rides the per-turn `contribute_turn_context` path, which has no
baseline.
- **F1 (`request agreement`).** After the goal stops, `contribute_turn_context` returns nothing, so the turn-2 fragment
  stays in append-only history with its positive `clock.sleep` sentence and is never corrected. In
  `waiting_guidance_goal_stop_adds_no_new_fragment`, `requests[4]` (the first request of turn 3) has no `clock.sleep`
  but keeps the old claim. That is a turn-start mismatch, outside the bound the orchestrator accepted.
- **F2 (`incremental, no churn`).** Every new turn changes `TurnContextItem.turn_id`, so
  `record_context_updates_and_set_reference_context_item` (`core/src/session/mod.rs:4748-4753`) calls
  `build_turn_context_contribution_items` again. The goal contributor re-appends an identical fragment on every
  active-goal turn: about 1.2 KB per turn of pure churn, in a token-burn series.

## The fix: World State, the codex channel for change-diffed context

Core already has the mechanism AC5 and plan §9 ("appended by normal context diffs only on change") describe:
`ContextContributor::contribute_world_state` (`ext/extension-api/src/contributors.rs:135`) returning
`WorldStateSectionContribution`s (`ext/extension-api/src/contributors/world_state.rs`).
- The harness persists each section's snapshot and calls `render_diff(previous)` only when it differs.
- It re-checks retained fragments after compaction.
- It runs on EVERY sampling step: `record_step_world_state_if_changed` (`core/src/session/turn.rs:509`,
  `core/src/session/mod.rs:3701`), plus turn start (`mod.rs:4720`).
- So it also closes the two mid-turn windows that the orchestrator accepted as a bound. That decision is superseded:
  the target is now agreement on every request.

Use `ext/git-attribution/src/world_state.rs` as the template. It is a developer-role section with an enabled fragment,
an explicit "disabled" retraction on the true→false transition, and `with_retained_fragment_matcher`. Mirror its
`(current, PreviousWorldStateSection)` match exhaustively, and justify each arm for the waiting case (especially
`Unknown`).

### 1. Thin plumbing (orchestrator-authorized minimal core touch; AC9 exception)

- Add `pub waiting_capabilities: &'a WaitingCapabilities` (doc line: the same snapshot as this step's
  `TurnContextContributionInput`) to `WorldStateContributionInput`.
- Pass `&step_context.waiting_capabilities` at its single construction site (`core/src/session/world_state.rs:298`).
- Fix every other construction that `git grep -n "WorldStateContributionInput {"` finds. Nothing else in codex-core
  changes.

### 2. Goal section (`ext/goal`, new module, e.g. `src/waiting_world_state.rs`)

- **Section id** e.g. `goal_waiting_guidance`, with its own start/end markers and role `developer`.
- **Snapshot** (bounded): while GoalActivity is present (the same Active + BudgetLimited gate as today), a small JSON
  object of the five flags plus the capped native wait name. When the goal is not active, `false`/`null`.
  - Keep a zero footprint for threads that never had an active goal: if the goal is inactive AND
    `input.previous_world_state` has no entry for this id, contribute no section at all.
  - State the resulting rollout effect in the results.
- **Rendering**:
  - On activation, or on any change of the flags or name: render the full fragment through the existing
    `waiting_capability_fragments` renderer (same sentences, order and cap; AC2/AC4 unchanged).
  - Unchanged snapshot: `None`.
  - Active→inactive: render one short, static retraction, for example "Waiting guidance given earlier in this thread no
    longer applies; the goal is not active." Keep it bounded and pinned byte-exact in `ext/goal/tests`.
  - Inactive with an absent or inactive previous: `None`.
  - The AC3 "nothing for inactive goals" rule is amended to allow exactly this one transition retraction.
- **Compaction**: add `with_retained_fragment_matcher` for the active fragment, so a fragment compacted out of history is
  re-rendered exactly once.
- **Remove the fragment from `contribute_turn_context`.** The continuation template change (AC1) stays as it is. There
  must be no double emission.

### 3. Tests (core suite; exact request counts as before)

- Flip the bound pins in `waiting_guidance_tool_created_goal_reacts_at_next_turn`:
  - `requests[1]` (right after `create_goal`) now carries the fragment, agreeing with `clock.sleep`;
  - the request after mid-turn completion carries the retraction;
  - assert agreement (`SLEEP_MARKER` count in the latest guidance == tool present) on EVERY request.
  - Drop the "KNOWN BOUND" comments.
- F1: in the goal-stop test, assert that the first request after the stop carries the retraction exactly once, and that
  no later request adds anything.
- F2: two (or three) consecutive unchanged active-goal TURNS carry exactly one fragment in total; a flag change across
  turns adds exactly one more.
- Compaction: if the suite has a compaction helper (see the existing compact suites), assert that after compaction the
  current fragment is present exactly once. If no helper makes this proportionate, say why and cover the
  retained-matcher arm with a unit test instead.
- Keep every other AC6 case (code-mode-only, remote catalog, excluded receipt, headless, post-create, non-goal).
  - "Matches the same request's tools" now means the most recent guidance or retraction in that request's history.

### 4. Mutants (update `TASK-260929-1w5ivu_mutants.json`)

- Keep the AC8 six where they still apply; rewrite any whose target moved.
- Add `waiting_world_state_always_renders`: `render_diff` ignores `previous` and always renders. F2's test must kill it.
- Add `waiting_world_state_no_retraction`: the active→inactive arm returns `None`. F1's test must kill it.
- Every killer must be selected by `test(waiting) | test(guidance) | test(continuation) | test(goal)`.

## Keep

- AC1, AC2, AC4, AC7 and AC10 unchanged.
- Report the size again; production grows by the section module, so keep it tight. Remove the turn-context path code you
  no longer need.
- `mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item`, then `--check` exit 0; no other
  cargo; no CODEX_HOME copies; delete temp dirs.
- Leave everything UNCOMMITTED, report the final tree id after fmt, add the note `HOSTED-PRECHECK-REQUESTED: precheck 3`,
  and end your turn without handing off.

Base note: P4b landed (relux/main 7e4289e2, PR #16) and the orchestrator converged this Story onto it. The workspace HEAD is
`7e4289e21fab653fea8c0089a7ffd790145e5686`, and your starting candidate is tree `9ff1a412eb6cf6a74f0ebf44ae92631ccc01b882`:
the rev1 delta re-applied by a 3-way merge, with one import-only conflict in `ext/goal/src/extension.rs` (GoalActivity and
PlanCommitInput both kept). Verify both before editing.
- The new trunk includes P4b continuation pacing: `continuation_schedule.rs`, the `goal_continuation_pacing` feature
  and `PlanCommitInput`. Do not change P4b code.
- Precheck 3 must also keep the P4b suites green. Their killers are selected by `test(goal)`.
