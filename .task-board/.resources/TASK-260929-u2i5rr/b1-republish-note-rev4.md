# Republish note for TASK-260929-u2i5rr — revision 4 (routine, no code change expected)

Revision 3 passed every local gate command except the codex-app-server suite: timing-sensitive tests flaked under
host load, and this leaf does not touch app-server. Since then the board's local gate became the FAST lane: target
guard, fmt-check, clippy on the series crates and small-crate tests. GitHub-hosted CI (`relux-ci`) runs the codex-core
and codex-app-server suites, your completion_receipt unit tests included, on the exact candidate tree after you
hand off. Read the updated `producer-brief.md` (precondition) first. Keep the code as it is.

1. Run `python3 /Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-fix-suite-busy.py --any`. On BUSY,
   follow the brief's HOLD-BUILD rule.
2. From your worktree, run the guard, then from `codex-rs/`: `just fmt` and `just clippy -p codex-core`. Clippy runs
   with `--tests`, so it type-checks your tests. Do NOT run `just test -p codex-core` locally.
3. Refresh `TASK-260929-u2i5rr_results.md`: list the F1-F3 tests and the mutants they kill, and state that the
   codex-core unit tests run on hosted CI after handoff.
4. Run the busy check again, then `task-board handoff TASK-260929-u2i5rr --role developer`.
Do not edit README.md or anything outside the leaf scope.

## Note (operator, 2026-10-02 07:3xZ): re-handoff after a false BUSY
RUN-261002-226bc7 checked the candidate (guard, fmt and clippy green, byte-identical to the rev 2 patch) and then held
its handoff, because the busy check returned BUSY for a read-only R141 review panel. That was a false positive: the check
now ignores reviewer and researcher runs. Do NOT redo the work. Confirm the worktree still holds the same 6 paths, re-run
the busy check (it should say FREE), and hand off. If it still says BUSY for a developer run or a validation phase, follow
the HOLD-BUILD rule.

## Note (operator, 07:5xZ): the busy check is authoritative; do not second-guess it
RUN-261002-58276d got `FREE` from codex-fix-suite-busy.py both times, then held anyway after its own `spawn status` look
at a live developer run. That run was an integration/complete run, which never builds; the script excludes those on
purpose, together with read-only reviewer and researcher runs. Rule for this run: when the script prints FREE, hand off
right away. Do not inspect `spawn list` or `spawn status` to override it. Only a printed `BUSY ...` line triggers HOLD-BUILD.
