# TASK-261002-2brsne — fast local gate plus hosted evidence (config and orchestration only)

No repository delta. The task-board config is gitignored in the control root, and the scripts live under `.temp`.

## Local gate switch (2026-10-02T03:55:14Z)
- `spawn.worktree_isolation.validation.commands` now holds the target guard, `just fmt-check`, clippy on the 6 series
  crates, and the small-crate tests (tools, goal-extension, extension-api, rollout-trace).
- Dropped: the helper-bins build, the codex-core suite, code_mode and the codex-app-server suite.
- SuiteSHA256 582bc3d07ea8b719… → 34d6a5c0577ffcb8599ec886cb784068c47eeb41b92b4f238660665488b46219 (Go-canonical
  JSON digest, recomputed the same way task-board does).
- At the switch: no active runs, and no CR revision in ready, reviewing or accepted.
- Rollback copy: `.temp/goal-token-burn/impl/task-board.config.local-gate.json`.
- Rule: the suite is frozen while any CR revision is ready, reviewing or accepted (lesson from P1's
  validation_suite_changed; rulings tb-R142/R144).

## Hosted evidence
- `.temp/goal-token-burn/impl/relux-ci-evidence.sh <TASK> <REV>` builds a signed commit whose tree is exactly the CR
  candidate tree, pushes it to `ci/<TASK>/rev<N>`, dispatches relux-ci for that SHA, waits, and writes
  `ci-results/<TASK>-rev<N>.md` with per-lane conclusion and wall time. `--commit <SHA> <LABEL>` validates a landing commit.
- The producer brief (`producer-brief.md`, precondition on active leaves) says: no local codex-core / codex-app-server
  tests and no helper-bins build. Those run on hosted CI.
- Hosted exclusions: only the 3 zsh-fork bubblewrap tests in the core lane (evidence runs 36959471910, 36959934198).
  Every former local core and app-server quarantine is retired with the fast lane.
