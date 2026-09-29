# Review brief — round 2 (Change Request revision 3) of TASK-260929-1srn2y

You are the reviewer for revision 3. The producer briefs (`brief.md`, `rework-brief-rev2.md`) are context, not
your instructions. Your instructions are this brief, `surface-table.md` (unchanged from round 1), and the reviewer
role contract. The round-1 verdict is `TASK-260929-1srn2y_review-verdict-rev1.md`; your prompt carries its
findings array.

## What is under review

The candidate is `TASK-260929-1srn2y_goal-token-burn-final-plan.md` — the consolidated final patch series that
the implementation leaf will consume. It was produced as CR revision 2; revision 2 went `stale` only because the
Story workspace base lagged trunk (44 upstream paths were counted as delta). The orchestrator ran `worktree converge`,
and revision 3 republishes the same document unchanged (SHA-256
`e25bfd07e8e2559570b67e37d98653c3537a1cac34039ffee938796bd6e0f4a0`, see `TASK-260929-1srn2y_republish-rev3-note.md`)
with `repository_delta=empty`. "Delta since revision 1" below means the content delta between the revision-1 outcome
and this final plan. It must stand alone.

Order of work (per the reviewer contract):

1. Attack the delta since revision 1 FIRST: the F1 resolution (P5 delivery on the trigger-turn mailbox,
   acceptance = included in a sampling request, both F1 paths in the race table) and the F2 resolution (P2
   goal-active marker, hooks, precedence, tests). Fix-induced defects live there. For each round-1 finding decide
   resolved / not resolved, with a reproduction if not resolved (`repeat-of: rev1/<id>`).
2. Check the findings-resolution table covers F1, F2 and N1-N10, and that each claimed resolution exists in the
   document and holds at the pin.
3. Sweep all 8 surface-table rows; every row gets exactly one result.
4. Free hunt beyond the table.

## Evidence, budget, deliverable

- Pinned upstream `33a0f766a647208b471cfbcad889c67fd324ee04`; read pinned blobs (`git show 33a0f766a6:<path>`);
  cite `path:line`; mark anything unverified. Read-only; builds optional and bounded.
- `review_budget_minutes`: 45 for steps 1-3; free hunt: 10 minutes.
- Verdict artifact: attach as `TASK-260929-1srn2y_review-verdict-rev3.md` (task-scoped outcome), with the same
  structure as round 1 and the machine-readable `verdict-findings` block rules below:
  `findings`, `notes`, `surface_results` (all 8 rows), `free_hunt`. A finding that repeats a round-1 mechanism
  uses `repeat-of: rev1/<id>`; new mechanisms use `none`.
- Routing: every row `held` and an empty free hunt -> `accept_cr(TASK-260929-1srn2y, revision=3, evidence=TASK-260929-1srn2y_review-verdict-rev3.md)`.
  Otherwise route the element to `analysis` with the verdict attached. Do not leave it in `reviewing`. English.

### Machine-readable verdict block (required, exactly one)

The verdict file must contain exactly one fenced block with the info string `verdict-findings` holding one JSON
object. It is validated by `accept_cr` / the rejection route; a near-miss fence or malformed JSON is refused.

```text
```verdict-findings
{
  "findings": [
    {
      "id": "p5-admission-loss",
      "row": "p5-completion-delivery",
      "invariant": "<row invariant that did not hold>",
      "mechanism": "<path:line at 33a0f766a6, or a one-sentence design statement>",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/codex_thread.rs",
          "command": "git show 33a0f766a6:codex-rs/core/src/codex_thread.rs | sed -n '374,395p'",
          "expected_failure": "<what the output shows that breaks the plan>",
          "pinned_blobs": ["<git rev-parse 33a0f766a6:codex-rs/core/src/codex_thread.rs>"]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none"
    }
  ],
  "notes": ["<non-blocking suspicion>"],
  "surface_results": [
    {"row": "p5-completion-delivery", "result": "broken"},
    {"row": "p4a-goal-gating", "result": "held"},
    {"row": "p4b-pacing-scheduler", "result": "not-attacked", "detail": "budget"}
  ],
  "free_hunt": []
}
```
```

Field mapping for this research leaf: `test_file` is the cited source file (or a probe script you wrote under a
gitignored path); `command` is the exact read-only command; `expected_failure` states what the output
demonstrates; `pinned_blobs` is the non-empty list of git blob OIDs (`git rev-parse 33a0f766a6:<path>`) of every
file the reproduction reads. `id` is a whitespace-free slug. `severity` is one of `bypass`, `regression`,
`robustness`, `note`; in plan terms: `bypass` = the planned patch would leave a token-burn mechanism in place or
accept a state it must refuse; `regression` = the plan would break existing Codex behaviour; `robustness` = an
unhandled failure path in the design. `surface_results` lists all 8 rows from `surface-table.md`, each once.
