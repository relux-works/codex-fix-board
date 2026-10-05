# TASK-260929-2gp04j (G2) — goal-activity publisher hooks

Read `producer-brief.md` (precondition) first, including its "Hosted pre-handoff check" section, and `final-plan.md`
section 4 (transition table). The AC table and scope are on the task. Your Story worktree already holds the accepted and
checkpointed G1 leaf: the GoalActivity type in codex-extension-api and the spec_plan sleep gate. Build on it; do not
change G1's gate.

Local validation (fast lane): `just test -p codex-goal-extension -p codex-extension-api` and clippy for the crates you
touch. Do NOT run codex-core or codex-app-server tests locally. Write the AC's core suite tests and the app-server test
anyway, and make them compile.

Before handoff: attach `TASK-260929-2gp04j_mutants.json`. It holds at least one narrowing mutant per publisher hook
family: create, turn start, resume/external set, update/stop/limit, clear, stop/disable, read failure and stale
callback. Each mutant names the test that must kill it. Then follow the hosted pre-handoff check: add the note
`HOSTED-PRECHECK-REQUESTED`, attach your results, and end the turn without handing off. You will be resumed with the
hosted evidence.
