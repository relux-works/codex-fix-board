# TASK-260929-309h9n (P4b-2 continuation-schedule): producer note for precheck 1

Read in this order: `final-plan.md` (section 8 P4b, section 11 attack table rows p4b-pacing-scheduler), the AC on this task,
`producer-brief.md`, then `mini-producer-addendum.md`, which OVERRIDES producer-brief.md wherever they conflict
(no local cargo except `cargo fmt`, nothing committed, mutants as JSON).

## Base

Story worktree `/Users/administrator/Developer/ReluxWorks/codex/.temp/STORY-260929-35sarf/worktree` at checkpoint f369ef563
(tree 486ebfe5, P4b-1 state-change observations, accepted rev4). Build on it; do not modify P4b-1 behavior except where an AC
here needs a hook.

## Design constraints (decided by the orchestrator; do not redesign)

1. ONE timer per goal thread. `ext/goal/src/check_in_clock.rs` already has the injectable `CheckInClock` and the single-slot,
   generation-guarded `CheckInTimer`, and `ext/goal/src/background_wait.rs` already issues `CheckInTicket`s with the
   invalidation notes (`note_human_input`, `note_turn_start`, `note_steering`, `note_goal_mutation`, `note_clear`,
   `note_stop`, `note_release`, `note_resume`). The pacing delay MUST be scheduled through that same slot and ticket/claim
   machinery (extend it or factor a shared piece into `continuation_schedule.rs`); a second independent timer or a
   `tokio::spawn(sleep)` per continuation fails AC3. When both a subscribed-wait deadline and a pacing deadline apply, one
   timer holds the governing deadline; an event wake pre-empts it exactly like a background-wait wake does today.
2. The streak input is P4b-1's observation: a continuation turn with zero recorded state-changing outcomes (the
   accounting count for that turn) grows the streak; any observation resets it to the floor. Do not invent a second
   classifier; do not read tool success, plan text or model text.
3. Order in the continuation decision: the existing three-fully-empty-continuations blocker (`accounting.rs`) runs FIRST and
   is unchanged; then pacing. A nonempty "waiting" turn is paced, never counted as empty.
4. Admission at fire time rechecks the ticket (goal id + revision, predecessor turn, generation/cause) AND pending mail /
   predecessor state under the same lock that `check_admission` uses today; a stale ticket returns without starting a turn.
   A human turn that starts and ends before the deadline must still invalidate (turn-start note bumps the generation).
5. Transient only: no rollout/history/persisted field; resume restarts at the floor. Nothing model-visible (AC7).
6. Keep `continuation_schedule.rs` under 500 LoC excluding tests; tests in sibling `*_tests.rs` files and
   `ext/goal/tests/`; the app-server two-poll request-count test goes in the app-server suite next to the existing goal
   background-wait vertical test (commit 39c264c34 on trunk shows the shape).

## Tests and mutants

- Fake-time units for n=1,2,3, the 30 min cap, reset, one-live-timer replacement, event pre-emption, every invalidation cause,
  fast intervening human turn, blocker-first ordering, nonempty waiting paced, resume at floor, no model-visible change.
- App-server: two consecutive poll-only continuations -> assert the request count and that the second delay is the n=2 delay.
- Mutants (AC8), each `git apply --check`-clean against your FINAL tree and naming its killer test: streak reset on a
  non-state-change; missing cap; stale-ticket admission (skip revision or generation check); timer not cancelled on
  invalidation; blocker order swapped. Name test functions so a filter on `test(continuation_schedule) | test(pacing) |
  test(goal)` selects every killer; say in results which filter they need.
- Report model requests per scenario (AC8) in the results.

## Lint hygiene (recurring hosted failures on this campaign)

Redundant closures (use method paths), uninlined format args, collapsible ifs, needless borrows, `vec![` where an array works,
single-arm `match` (use `if let`/irrefutable `let`), `#[cfg(test)]` on anything production code calls, unused imports after
refactors, `/*param*/` comments on opaque positional literals. Exhaustive matches, no wildcard arms where avoidable.

## Finish

`cargo fmt -- --config imports_granularity=Item` then `--check` (exit 0). Leave everything UNCOMMITTED; report the tree id after
the last edit (temp index method from the addendum); attach `TASK-260929-309h9n_mutants.json`; add the note
`HOSTED-PRECHECK-REQUESTED: precheck 1`; delete any temp dir you made; end your turn without handing off.
