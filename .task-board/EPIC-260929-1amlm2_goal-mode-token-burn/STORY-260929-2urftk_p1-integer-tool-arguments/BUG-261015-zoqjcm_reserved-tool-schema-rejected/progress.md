## Status
backlog

## Review
required

## Task Class
code

## Estimate
estimated(fibonacci(3))

## Blocked By
- (none)

## Blocks
- (none)

## Checklist
- [ ] AC1: advertised schemas of wait_agent v1/v2, exec_command, write_stdin, clock.sleep, create_goal byte-identical to upstream 0462dcc; git diff 0462dcc -- '*.snap' is empty
- [ ] AC2: P1 integral-decimal parsing and its tests unchanged and green
- [ ] AC3: wire-contract pin test for each P1-touched tool's advertised parameters, with negative integer check
- [ ] Hosted relux-ci lint, small, core, app-server green on the exact candidate tree
- [ ] All mutants in BUG-261015-zoqjcm_mutants.json killed by hosted CI
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
LIVE-EVIDENCE 2026-10-15T19:40Z: codex-base (upstream 0462dcc release build, run 38773745523) exec -m gpt-6-astra -> base-ok (15495 tokens). codex-relux (e063784, run 38763975745) same prompt -> 400 collaboration.wait_agent is reserved and must match the configured schema. Diagnosis confirmed. All 17 snap diffs vs upstream are hash= lines only.
spawn agent resolution: Agent selection: codex via explicit_override
spawn queued: [implementer] developer (codex) (run=RUN-261015-a5e236, max_parallel=4)
spawn run started: [implementer] developer (codex) (run=RUN-261015-a5e236)

## Precondition Resources
- [producer-brief.md](file://BUG-261015-zoqjcm/producer-brief.md)
- [zoqjcm-producer-brief.md](file://BUG-261015-zoqjcm/zoqjcm-producer-brief.md)
- [final-plan.md](file://BUG-261015-zoqjcm/final-plan.md)
- [surface-table.md](file://BUG-261015-zoqjcm/surface-table.md)

## Outcome Resources
- [BUG-261015-zoqjcm_spawn-log_-implementer--developer--codex-_RUN-261015-a5e236.log](file://BUG-261015-zoqjcm/BUG-261015-zoqjcm_spawn-log_-implementer--developer--codex-_RUN-261015-a5e236.log) — System spawn log captured by task-board

## Created
2026-10-15T17:05:57Z

## Last Update
2026-10-15T19:33:24Z

## Assigned To
[implementer] developer (codex)
