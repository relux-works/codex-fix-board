# Loop-detector response: bound proposal (rev5, signal S4)

Producer spawn is REFUSED with `loop_bound_pending` until a human answers. Do not rework around this demand: the loop needs a bound, not another revision.

## Evidence

- Implementation size grew 1042 -> 1372 (>20%) in the step rev4 -> rev5 with the recorded acceptance text unchanged: thrash, not shaping.

## Bound proposal (references/planning-workflow.md, "Bounded leaves")

A leaf is boundable when its acceptance criteria are decidable by a finite test. Pick ONE and record it in the answer:

1. **State the accepted subset.** Name the inputs the leaf accepts — drawn from the real corpus, not from taste — so the finding's input classifies as in or out. Refusing an out-of-subset input is then valid; accepting it, or crashing on it, still blocks.
2. **Revision budget plus a named reference implementation.** Carry a `revision_budget` beside `task_class`, and the reference accepted values must equal, so the loop ends by count with an oracle deciding each round.
3. **Split by surface.** One leaf per catalog surface, each with its rows, coverage-map obligation and revision budget.

## How to answer

Append the answer line to the element notes — this is an explicit operator act, and only an explicit line clears the refusal:

```
task-board m 'set_notes(TASK-260929-csyzcj, text="loop-detector rev5: bound-answer decision=<your decision>")'
```

The gate admits the next producer run only when that line names THIS revision with a non-empty decision. An empty answer answers nothing; an answer naming an older bound clears nothing.
