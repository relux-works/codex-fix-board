# Surface table — TASK-260929-309h9n continuation-schedule

| Row | Invariant | Attack families |
|---|---|---|
| spacing and streak math | automatic continuations are >= 30 s apart; streak n gives min(30 s * 2^(n-1), 30 min); any observed state change (P4b-1 observation) resets to the floor (AC1) | off-by-one in n; overflow or missing cap; reset on a non-state-change; reset read from tool success, plan text or model text; a second classifier diverging from P4b-1 |
| polls grow the streak end to end | two consecutive read-only poll continuations grow the streak and the second delay is the n=2 delay, measured by app-server request counts (AC2) | poll treated as activity; streak reset per turn; test asserting only units, not requests |
| one live timer | exactly one timer per goal thread, shared with the background-wait check-in slot; a new schedule replaces the old; no detached sleeps; an event wake (mail, child completion, subscribed exec notification) pre-empts the timer (AC3) | a second independent timer; tokio::spawn(sleep) per continuation; replacement that leaks the old task; wake that leaves the pacing timer armed; pacing overriding a governing subscribed deadline |
| ticket invalidation and admission | the ticket binds goal id + revision, predecessor turn and generation/cause; human input, steering, goal change/clear, stop, completion/release and any new turn invalidate it, including a human turn that starts and ends before the deadline; admission rechecks ticket + predecessor + pending mail under the admission lock (AC4) | skipped revision or generation check; check-then-act outside the lock; fast human turn not invalidating; stale timer starting a turn; invalidation not cancelling the sleeping timer |
| blocker order and waiting turns | the three-fully-empty-continuations blocker runs first and is unchanged; a nonempty waiting continuation is paced, not counted empty (AC5) | pacing before the blocker; blocker thresholds changed; waiting turn classified empty |
| transient state | timers, streaks and counters are not persisted; resume reconciles and restarts at the floor; completion does not reset the human-input allowance; restart resetting quotas is disclosed (AC6) | streak persisted to rollout; stale subscription restored; allowance reset on completion; undisclosed bound |
| no model-visible change | no prompt text, history or context change from scheduling (AC7) | injected pacing text; history items for timers; cache-busting context changes |
| mutants and measurement | narrowing mutants for reset-on-non-change, missing cap, stale admission, uncancelled timer and blocker order each have a named killer; model requests per scenario reported (AC8) | mutant not applying to the final tree; killer outside the hosted filter; requests not measured |
| placement and size | logic in `ext/goal/src/continuation_schedule.rs` (< 500 LoC excl. tests); no core growth beyond thin hooks; no core->goal dependency; tests in sibling `*_tests.rs` / suites (scope) | scheduler logic in codex-core; large edits to runtime.rs/extension.rs; new public API beyond need |

```surface-table
{"rows": ["spacing and streak math", "polls grow the streak end to end", "one live timer", "ticket invalidation and admission", "blocker order and waiting turns", "transient state", "no model-visible change", "mutants and measurement", "placement and size"]}
```
