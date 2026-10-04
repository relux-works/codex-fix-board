# TASK-260929-4ut0up (B2) — receipt hooks in unified exec

Read `producer-brief.md` (precondition) first, including its "Hosted pre-handoff check" section, and `final-plan.md`
sections 5 and 5.1-5.4. The AC table and scope are on the task. Your Story worktree holds the accepted, checkpointed B1
leaf (`CompletionReceiptStore`); build on its API, and change it only where a hook needs a missing transition
(retirement, owner construction), keeping every B1 test green.

Local validation (fast lane): `just fmt`, `just fix -p codex-core` (revert any edit outside your scope), and
`just clippy -p codex-core`. Do NOT run codex-core tests locally. Write the AC's tests anyway, as sibling `*_tests.rs`
unit tests in unified_exec plus core suite tests where needed, and make them compile.

Before handoff: attach `TASK-260929-4ut0up_mutants.json`. It holds at least one narrowing mutant per AC row, each naming
the test that must kill it (for example: publish the exit on `exit_token.cancelled()` before the drain; drop the
retention cap; skip slot release on inline delivery; let a default launch reserve a receipt). Then follow the hosted
pre-handoff check: add the note `HOSTED-PRECHECK-REQUESTED`, attach your results, and end the turn without handing off.
