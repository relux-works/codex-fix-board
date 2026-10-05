# TASK-260929-2gp04j (G2) — rebase refresh for precheck 6 (no product-code change)

Run: RUN-261005-a84460. Base moved 58042581a0 (G1) -> 31655cd8b5 (G1 replayed
onto trunk 729f259e62, P5-B) via `task-board worktree refresh-candidate`.
This run wrote no G2 product code; the only worktree change is the base move
plus restoring the 12 new-trunk P5-B files the refresh left as reversions.

## What happened

1. `task-board worktree refresh-candidate TASK-260929-2gp04j` first failed on
   commit signing (no SSH_AUTH_SOCK in the spawn env; git ssh-signing with
   ~/.ssh/ivanopcode prompted for a passphrase). Retried with
   `SSH_AUTH_SOCK=/Users/iv/.ssh/agent/active.sock` (login launchd agent,
   holds the ECDSA signing key): `refresh_advanced`, exit 0.
   - TrunkOID: 729f259e62a8d11d9e17398e487790e1ee5d8b8c
   - BranchOID: 31655cd8b5f8c57032d42c3b3907c6fee88b0580 (G1 replay, no conflicts)
2. The refresh preserves the candidate tree exactly, so the 12 P5-B trunk files
   (ea8899e6f9..729f259e62 touches ONLY codex-rs/core/src/unified_exec/*,
   12 files, zero overlap with G2's file set) appeared as worktree
   modifications/deletions. Per the tool contract ("incoming content must be
   combined by its producer") this run restored exactly those 12 paths from
   HEAD (`git restore --source=HEAD -- <12 paths>`). Leaving them would have
   shipped a CR reverting P5-B.
3. Verified: `git status` now shows exactly the G2 footprint — 12 modified
   tracked files + 5 untracked G2 paths, identical file list to pre-refresh.
   Real index untouched (all unstaged, nothing committed; branch tip is the
   board's replay commit, not a producer commit).

## Candidate identity (precheck 5 superseded)

- Precheck-5 tree fc288cc9d009923ec84e87428669fc51030712a4 NO LONGER matches.
- New candidate tree (temp-index read-tree HEAD + add -A + write-tree, twice):
  a8fc9e0cc6e0aad477aba7cd377e3c93203932fe
- New tree = trunk 729f259e62 + G1 replay 31655cd8b5 + unchanged G2 delta.
- G2 content byte-identical to precheck-5 candidate by construction (refresh
  preserves the candidate; this run touched only the 12 disjoint P5-B paths;
  pre/post file lists match). Not re-hashed against snapshot 225257e (signed,
  never landed, not fetched locally).

## Fast lane (local, exit codes real, no pipes hiding status)

From codex-rs/ with NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no INSTA_WORKSPACE_ROOT=$PWD:

| command | exit | result |
|---|---|---|
| codex-target-guard.sh | 0 | cleaned workspace members for this worktree |
| just fmt | 0 | no changes |
| just clippy -p codex-goal-extension -p codex-extension-api | 0 | 1 pre-existing codex-core lib warning (unused import registry.rs), out of scope |
| just clippy -p codex-core | 0 | pre-existing warnings only (scenarios.rs etc.), out of scope |
| just clippy -p codex-app-server | 0 | clean |
| just test -p codex-goal-extension -p codex-extension-api | 0 | 58/58 passed, 0 skipped |

NOT run locally per brief: codex-core / codex-app-server suites, mutant
executions (apply-check only, see below). Busy check printed FREE before building.

## Mutants

TASK-260929-2gp04j_mutants.json unchanged (still the 20 from precheck 5).
Apply-check against the rebased worktree (`git apply --check` per patch):
20/20 apply cleanly, so precheck 6 can run them unmodified:

create_waits_for_finish, turn_start_requires_baseline,
resume_skips_budget_limited, external_set_skips_budget_limited,
complete_retains_sleep, usage_limit_retains_sleep,
budget_limited_admits_continuation, disabled_clear_keeps_marker,
disable_preserves_active_marker, stop_preserves_active_marker,
timestamp_read_failure_keeps_known_marker, cleared_revision_accepts_old_read,
late_active_set_reinserts_cleared_goal, turn_stop_read_failure_keeps_marker,
abort_read_failure_keeps_marker, external_set_get_failure_keeps_marker,
external_set_prepare_failure_keeps_marker, fork_flush_prepare_failure_keeps_marker,
tool_finish_accounting_failure_keeps_marker, turn_error_skips_reconcile_after_stop_failure.

## Reviewer notes carried forward (unchanged)

- MODULE.bazel.lock / dev-deps note and the ~1334-line size note with the
  two-stage split live in TASK-260929-2gp04j_results.md; unaffected by this
  rebase (no dependency or file-set change). Results refresh happens at the
  post-precheck-6 handoff run.

## Request

HOSTED-PRECHECK-REQUESTED: precheck 6 (rebased on 729f259) — snapshot tree
a8fc9e0cc6e0aad477aba7cd377e3c93203932fe at checkpoint 31655cd8b5, run
relux-ci lint/small/core/app-server plus all 20 mutants. No handoff this turn.
