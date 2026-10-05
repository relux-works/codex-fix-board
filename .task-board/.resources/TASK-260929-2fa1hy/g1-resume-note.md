# Resume note for TASK-260929-2fa1hy — build, check and hand off (code already written)

Your earlier run wrote the code and parked with HOLD-BUILD because another codex-fix build held the shared target.
Since then the board's local gate became the FAST lane: target guard, fmt-check, clippy on the series crates and
small-crate tests. GitHub-hosted CI (`relux-ci`) runs the codex-core and codex-app-server suites, including your
`core/tests/suite` tests, on the exact candidate tree after you hand off. Read the updated `producer-brief.md`
(precondition) first.

1. Run `python3 /Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-fix-suite-busy.py --any`. On BUSY,
   follow the brief's HOLD-BUILD rule.
2. From your worktree, run the guard, then from `codex-rs/`: `just fmt`, `just fix -p codex-core -p codex-extension-api`,
   `just clippy -p codex-core -p codex-extension-api` and `just test -p codex-extension-api`. Do NOT run
   `just test -p codex-core` locally; the AC's core suite tests run on hosted CI.
3. Make sure every AC row has its driving and refusal test written and compiling. Record in
   `TASK-260929-2fa1hy_results.md` which of them only hosted CI runs.
4. Run the busy check again, then `task-board handoff TASK-260929-2fa1hy --role developer`.
