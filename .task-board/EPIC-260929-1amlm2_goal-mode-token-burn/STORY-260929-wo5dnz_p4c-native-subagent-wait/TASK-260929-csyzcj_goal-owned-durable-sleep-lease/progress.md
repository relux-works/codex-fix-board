## Status
to-dev

## Review
required

## Task Class
code

## Estimate
estimated(fibonacci(13))

## Blocked By
- TASK-260929-2snjbb

## Blocks
- (none)

## Checklist
- [ ] AC table detailed before spawn
- [ ] Code written per task description and AC
- [ ] Relevant tests written for new or changed behavior and passing
- [ ] In a managed Story worktree the candidate is left UNCOMMITTED in the worktree for the handoff to snapshot — never commit on the Story branch. A producer commit moves the branch tip off the recorded checkpoint and the handoff refuses with change_request_candidate_committed_past_checkpoint; repair with `git reset --soft <checkpoint_oid>` before completing again.
- [ ] Every command, message, state, or refusal named in the AC is driven through the production entry point by a named committed test, or is declared a stated bound. Report coverage as a ratio — `n of m AC rows driven` — and name the production call site for each. Prose in place of the ratio is not evidence.
- [ ] Gating, refusing, validating, authorizing, or attesting behavior covered by negative tests that fail when the gate admits what it must reject, with the production call site named
- [ ] Every gate ships at least one NARROWING mutant — the gate stays present and is weakened to admit exactly one member of the class it must reject, and a named test must fail. A delete-only mutant proves only that the gate exists and is not accepted as evidence.
- [ ] A gate that inspects source text is additionally attacked by a mutant that PRESERVES the searched-for token and changes behavior, and the mutant harness executes the behavioral suite, not only the static checker.
- [ ] Lint clean
- [ ] Relevant build/validation commands run after changes and build not broken
- [ ] New outcome artifact attached on the board with a task-scoped name when the work produces notes, logs, screenshots, or other deliverables
- [ ] Important findings, decisions, anomalies, or regressions recorded in logbook when relevant

## Notes
spawn agent resolution: Agent selection: muse via explicit_override
spawn queued: [implementer] developer (muse) (run=RUN-261007-da6cd2, max_parallel=4)
spawn run started: [implementer] developer (muse) (run=RUN-261007-da6cd2)
HOSTED-PRECHECK-REQUESTED: codex-core lane (lib unit: owned_children_tests, status_tests, session_prefix_tests::interrupted_notice, control_tests::owned_children_inspection_propagates_failed_lookups; integration suite::goal_native_wait 4 tests) + small lane (codex-extension-api state, codex-goal-extension native_wait) on candidate tree, plus each of the 6 mutants in TASK-260929-csyzcj_mutants.json (skip_failed_lookups, insert_after_mail_check, unconditional_remove, insert_clobbers_one_foreign, interrupted_claims_success, ignore_native_pending) with its named killing test. Code written, fast-lane green locally (fmt/clippy/small tests exit 0); core/app-server suites not run locally per brief. Work left UNCOMMITTED in Story worktree; no handoff this turn.
spawn run child final message (run=RUN-261007-da6cd2, tools=271 patches=59 failed=1):
Hosted precheck requested for TASK-260929-csyzcj (not handed off — awaiting hosted results).

What was delivered this pass: goal-owned durable-sleep lease (`goal-wait:<generation>` via `insert_if` before mail check + scheduler recheck), narrow owned-children inspection (`Loaded`/`Unloaded`/error, propagates), P4a check-in reuse for native pending, conditional removal on turn start/clear/disable/stop/release/resume, and V2 `Interrupted` queue-only notices without changing `is_final`. V1 bridge stays out of scope per task (sibling G2).

Evidence attached: `TASK-260929-csyzcj_results.md` (coverage map 9/9 rows, 4 fully + 5 partially with named gaps, commands with exit codes) and `TASK-260929-csyzcj_mutants.json` (6 narrowing mutants with named killing tests). Fast-lane green locally: `just fmt` exit 0, `just clippy` for all touched crates exit 0, small tests 13 passed exit 0 (`codex-extension-api` state 7, `codex-goal-extension` native_wait 6). Core integration/unit compile (clippy) but run hosted only per brief. Work left uncommitted on `task-board/story/STORY-260929-wo5dnz` for snapshot; no handoff run.
agent completed: [implementer] developer (muse) (exit=0)
spawn run completed: muse (run=RUN-261007-da6cd2, pid=68940, exit=0)
No Change Request revision was published for TASK-260929-csyzcj (handoff_unsatisfied): the board is not at to-review
spawn autonomous recovery: run RUN-261007-da6cd2 queued successor RUN-261007-e1bbd0 (attempt 1/1, model=muse-spark-1.3-contributor): producer run RUN-261007-da6cd2 remains unsatisfied: producer run RUN-261007-da6cd2 published no Change Request and reached no handoff branch while TASK-260929-csyzcj is development: the board is not at to-review
spawn run started: [implementer] developer (muse) (run=RUN-261007-e1bbd0)
spawn run RUN-261007-e1bbd0 cancelled by operator; operator action required; reason: no operator reason supplied
spawn agent resolution: Agent selection: muse via explicit_override
spawn queued: [implementer] developer (muse) (run=RUN-261007-5cb4d2, max_parallel=4)
spawn run started: [implementer] developer (muse) (run=RUN-261007-5cb4d2)
HOSTED-PRECHECK-REQUESTED: precheck 2
spawn run child final message (run=RUN-261007-5cb4d2, tools=125 patches=12 failed=0):
Hosted precheck requested for TASK-260929-csyzcj (not handed off — awaiting hosted results).

Top finding: production wiring was correct; the suite never created a Running V2 child. Default config is V1-only, and the mocks used plain `spawn_agent` / `"clock.sleep"` wire formats that never dispatch (V2 needs `collaboration/spawn_agent`, sleep needs `clock/sleep`), so inspection correctly found no pending work. Fixed test-only in `goal_native_wait.rs`: enable `MultiAgentV2` + `AlwaysOn` sleep, namespaced mock calls, structured `function_call_output` matchers (old substring matchers could never match), and set-goal-after-spawn ordering (avoids a spurious pre-work continuation). Assertions unchanged.

Evidence: `just fmt` exit 0, `just clippy -p codex-core` exit 0 with zero warnings in the fixed file, all 6 mutant patches verified to apply. Local nextest skipped per disk gate (48 GiB < 50 GiB at decision time); first attempt was stale/truncated and is reported as unrun. Results + mutants re-attached, note `HOSTED-PRECHECK-REQUESTED: precheck 2` added, tree left uncommitted on checkpoint `39c264c`, disk trimmed back to 52 GiB.
agent completed: [implementer] developer (muse) (exit=0)
spawn run completed: muse (run=RUN-261007-5cb4d2, pid=17453, exit=0)
No Change Request revision was published for TASK-260929-csyzcj (handoff_unsatisfied): the board is not at to-review
spawn autonomous recovery: run RUN-261007-5cb4d2 queued successor RUN-261007-ffe38d (attempt 1/1, model=muse-spark-1.3-contributor): producer run RUN-261007-5cb4d2 remains unsatisfied: producer run RUN-261007-5cb4d2 published no Change Request and reached no handoff branch while TASK-260929-csyzcj is development: the board is not at to-review
spawn run started: [implementer] developer (muse) (run=RUN-261007-ffe38d)
spawn run RUN-261007-ffe38d cancelled by operator; operator action required; reason: no operator reason supplied

## Precondition Resources
- [final-plan.md](file://TASK-260929-csyzcj/final-plan.md) — codex-fix preconditions
- [producer-brief.md](file://TASK-260929-csyzcj/producer-brief.md) — codex-fix preconditions
- [local-build-allowance.md](file://TASK-260929-csyzcj/local-build-allowance.md)
- [g1-rework-brief-precheck1.md](file://TASK-260929-csyzcj/g1-rework-brief-precheck1.md)
- [g1-rework-brief-precheck2.md](file://TASK-260929-csyzcj/g1-rework-brief-precheck2.md)

## Outcome Resources
- [TASK-260929-csyzcj_spawn-log_-implementer--developer--muse-_RUN-261007-da6cd2.log](file://TASK-260929-csyzcj/TASK-260929-csyzcj_spawn-log_-implementer--developer--muse-_RUN-261007-da6cd2.log) — System spawn log captured by task-board
- [TASK-260929-csyzcj_results.md](file://TASK-260929-csyzcj/TASK-260929-csyzcj_results.md) — G1 rework results for precheck 2: test-only fixture fix, coverage map, gates
- [TASK-260929-csyzcj_mutants.json](file://TASK-260929-csyzcj/TASK-260929-csyzcj_mutants.json) — 6 narrowing mutant diffs with named killing tests (unchanged, re-attached for precheck 2)
- [TASK-260929-csyzcj_spawn-log_-implementer--developer--muse-_RUN-261007-e1bbd0.log](file://TASK-260929-csyzcj/TASK-260929-csyzcj_spawn-log_-implementer--developer--muse-_RUN-261007-e1bbd0.log) — System spawn log captured by task-board
- [TASK-260929-csyzcj_spawn-log_-implementer--developer--muse-_RUN-261007-5cb4d2.log](file://TASK-260929-csyzcj/TASK-260929-csyzcj_spawn-log_-implementer--developer--muse-_RUN-261007-5cb4d2.log) — System spawn log captured by task-board
- [TASK-260929-csyzcj_spawn-log_-implementer--developer--muse-_RUN-261007-ffe38d.log](file://TASK-260929-csyzcj/TASK-260929-csyzcj_spawn-log_-implementer--developer--muse-_RUN-261007-ffe38d.log) — System spawn log captured by task-board

## Created
2026-09-29T00:50:59Z

## Last Update
2026-10-07T21:22:42Z

## Assigned To
[implementer] developer (muse)
