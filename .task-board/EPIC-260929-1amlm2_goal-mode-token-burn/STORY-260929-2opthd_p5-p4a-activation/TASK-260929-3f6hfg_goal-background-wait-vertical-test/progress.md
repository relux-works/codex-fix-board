## Status
done

## Review
required

## Task Class
code

## Estimate
estimated(fibonacci(8))

## Blocked By
- (none)

## Blocks
- TASK-260929-2is91w

## Checklist
- [x] AC table detailed before spawn
- [x] Code written per task description and AC
- [x] Relevant tests written for new or changed behavior and passing
- [x] In a managed Story worktree the candidate is left UNCOMMITTED in the worktree for the handoff to snapshot — never commit on the Story branch. A producer commit moves the branch tip off the recorded checkpoint and the handoff refuses with change_request_candidate_committed_past_checkpoint; repair with `git reset --soft <checkpoint_oid>` before completing again.
- [x] Every command, message, state, or refusal named in the AC is driven through the production entry point by a named committed test, or is declared a stated bound. Report coverage as a ratio — `n of m AC rows driven` — and name the production call site for each. Prose in place of the ratio is not evidence.
- [x] Gating, refusing, validating, authorizing, or attesting behavior covered by negative tests that fail when the gate admits what it must reject, with the production call site named
- [x] Every gate ships at least one NARROWING mutant — the gate stays present and is weakened to admit exactly one member of the class it must reject, and a named test must fail. A delete-only mutant proves only that the gate exists and is not accepted as evidence.
- [x] A gate that inspects source text is additionally attacked by a mutant that PRESERVES the searched-for token and changes behavior, and the mutant harness executes the behavioral suite, not only the static checker.
- [x] Lint clean
- [x] Relevant build/validation commands run after changes and build not broken
- [x] New outcome artifact attached on the board with a task-scoped name when the work produces notes, logs, screenshots, or other deliverables
- [x] Important findings, decisions, anomalies, or regressions recorded in logbook when relevant
- [x] Implementation matches AC
- [x] Solution fits project architecture
- [x] Tests green
- [x] Gate, refusal, validation, authorization, and attestation behavior attacked, not read — positive-path-only evidence is not accepted
- [x] If review does not accept the work — verdict evidence added and status routed by the explicit verdict branches

## Notes
Intra-story order: runs after sibling TASK-260929-3r7peh is accepted and checkpointed (blocked_by removed because a checkpointed sibling stays integrating until the Story lands, which would deadlock).
spawn agent resolution: Agent selection: muse via explicit_override
spawn queued: [implementer] developer (muse) (run=RUN-261007-08e3af, max_parallel=4)
spawn run started: [implementer] developer (muse) (run=RUN-261007-08e3af)
HOSTED-PRECHECK-REQUESTED: run relux-ci app-server lane on the candidate tree for v2::goal_background_wait (4 tests, expect all green on Linux lane), then apply each mutant in TASK-260929-3f6hfg_mutants.json and re-run the goal_background_wait filter, expecting the named killing test to FAIL per mutant (silence-ignores-armed, drop-wake, wake-without-fragment -> notified_exec_exit_wakes_gated_goal_with_receipt_fragment; allow-notify-on-incapable-host -> headless_host_refuses_notify_on_exit_and_promises_no_wake; always-subscribe -> unopted_server_process_does_not_gate_goal_continuation). Collateral failures in core suites on mutants are expected (noted per mutant); only the named kill matters. Fast lane already green locally: just fmt, just clippy -p codex-app-server (exit 0, --tests), just fix -p codex-app-server (exit 0). Code written, NOT handed off; checklist 3/5/6/7 left unchecked pending hosted evidence.
spawn run child final message (run=RUN-261007-08e3af, tools=150 patches=25 failed=2):
This pass ends with code written and a hosted precheck requested — not handed off (status stays `development`).

**What was produced**

- New `codex-rs/app-server/tests/suite/v2/goal_background_wait.rs` (4 tests, all AC rows 7/7 mapped to driving tests with production call sites) plus a 1-line `mod` registration. Left uncommitted; no production changes.
- Test 1 covers AC1/AC2/AC3: goal/set triggers the first turn, the scripted model launches a barrier-held process with `notify_on_exit`, silence is asserted via request counts after RPC round-trips, release produces exactly one fragment-bearing wake request (receipt handle cross-linked from the tool-result ack), and `update_goal` completes the goal. A stalled runtime fails at the wake wait.
- Test 2 (AC6): two user turns during the wait, each delivered exactly once, wake still follows. Test 3 (AC5): unopted server process doesn't gate. Test 4 (AC4): `--session-source exec` headless host refuses the opt-in, hides the schema, promises no wake, continues ungated. Barrier tests skip remote/Wine lanes with reasons; the headless test runs everywhere.
- `TASK-260929-3f6hfg_mutants.json`: 5 narrowing mutants (all `git apply --check` green), each with a named killing test; expected core-suite collateral documented per mutant.

**Verification (real exit codes)**

- `just fmt`, `just clippy -p codex-app-server` (exit 0, `--tests`), `just fix -p codex-app-server` (exit 0). One pre-existing `codex-core` warning left untouched.
- `just test -p codex-app-server` deliberately not run — the brief forbids local app-server suites, so execution and mutant kills ride the hosted precheck.

**Board state**

- Attached `TASK-260929-3f6hfg_results.md` and `TASK-260929-3f6hfg_mutants.json`; added the `HOSTED-PRECHECK-REQUESTED` note specifying the 4-test green run plus per-mutant kill expectations. Checklist items 3/5/6/7 left unchecked pending hosted evidence; all others checked.
agent completed: [implementer] developer (muse) (exit=0)
spawn run completed: muse (run=RUN-261007-08e3af, pid=47565, exit=0)
No Change Request revision was published for TASK-260929-3f6hfg (handoff_unsatisfied): the board is not at to-review
spawn autonomous recovery: run RUN-261007-08e3af queued successor RUN-261007-764d5a (attempt 1/1, model=muse-spark-1.3-contributor): producer run RUN-261007-08e3af remains unsatisfied: producer run RUN-261007-08e3af published no Change Request and reached no handoff branch while TASK-260929-3f6hfg is development: the board is not at to-review
spawn run started: [implementer] developer (muse) (run=RUN-261007-764d5a)
spawn run RUN-261007-764d5a cancelled by operator; operator action required; reason: no operator reason supplied
spawn agent resolution: Agent selection: muse via explicit_override
spawn queued: [implementer] developer (muse) (run=RUN-261007-c065ca, max_parallel=4)
spawn run started: [implementer] developer (muse) (run=RUN-261007-c065ca)
F2 handoff rev2: tree still c83869e576d1e024cfdbb5f63cfe8b83c6e969cb (temp-index check x2, exit 0); zero worktree changes. Precheck 1 base run 37633617318 all lanes green. 5/5 mutants killed, each by a vertical test: silence-ignores-armed -> notified_exec_exit_wakes_gated_goal_with_receipt_fragment (:357, run 37633736582, raw log verified); drop-wake -> notified_exec + user_burst (37633707303); wake-without-fragment -> notified_exec (:357) + user_burst (:458) (37633768227, raw log verified); allow-notify-on-incapable-host -> headless_host_refuses_notify_on_exit_and_promises_no_wake (37633645894); always-subscribe -> unopted_server_process_does_not_gate_goal_continuation (37633676266). 0 survivors. Results refreshed, coverage map attached.
spawn run child final message (run=RUN-261007-c065ca, tools=33 patches=2 failed=0):
Handed off to review.

TASK-260929-3f6hfg (goal-background-wait vertical test) is now `to-review` with 12/12 checklist items green. Worktree tree confirmed unchanged (`c83869e5…`, exit 0, zero file edits), candidate left uncommitted for snapshot. Hosted precheck 1 applied: base run 37633617318 all lanes green, 5/5 mutants killed with 0 survivors, and I verified from raw CI failed-logs that each mutant is killed by an app-server vertical test — including `silence-ignores-armed` and `wake-without-fragment`, whose summary rows truncate the killer list. Refreshed `TASK-260929-3f6hfg_results.md` and attached the new `TASK-260929-3f6hfg_coverage-map.md` (3/3 surface rows mapped to tests + killed mutants).
agent completed: [implementer] developer (muse) (exit=0)
spawn run completed: muse (run=RUN-261007-c065ca, pid=29137, exit=0)
spawn agent resolution: Agent selection: codex via explicit_override
spawn queued: [reviewer] reviewer (codex) (run=RUN-261007-554bf3, max_parallel=4)
spawn run started: [reviewer] reviewer (codex) (run=RUN-261007-554bf3)
agent completed: [reviewer] reviewer (codex) (exit=0)
spawn run completed: codex (run=RUN-261007-554bf3, pid=5963, exit=0)
spawn agent resolution: Agent selection: codex via explicit_override
spawn queued: [implementer] developer (codex) (run=RUN-261007-a970a6, max_parallel=4)
spawn run started: [implementer] developer (codex) (run=RUN-261007-a970a6)
agent completed: [implementer] developer (codex) (exit=0)
spawn run completed: codex (run=RUN-261007-a970a6, pid=935, exit=0)
spawn run RUN-261007-a970a6 failed; operator action required; failure: integration_binding_state_invalid: Change Request CR-TASK-260929-3f6hfg-1 revision 1 is integrated, want accepted or checkpointed

## Precondition Resources
- [final-plan.md](file://TASK-260929-3f6hfg/final-plan.md) — codex-fix preconditions
- [producer-brief.md](file://TASK-260929-3f6hfg/producer-brief.md) — codex-fix preconditions
- [local-build-allowance.md](file://TASK-260929-3f6hfg/local-build-allowance.md)
- [surface-table.md](file://TASK-260929-3f6hfg/surface-table.md)
- [TASK-260929-3f6hfg_hosted-precheck-1.md](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_hosted-precheck-1.md)
- [f2-handoff-note-1.md](file://TASK-260929-3f6hfg/f2-handoff-note-1.md)
- [recording-brief-rev1.md](file://TASK-260929-3f6hfg/recording-brief-rev1.md)
- [complete-note.md](file://TASK-260929-3f6hfg/complete-note.md)

## Outcome Resources
- [TASK-260929-3f6hfg_spawn-log_-implementer--developer--muse-_RUN-261007-08e3af.log](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_spawn-log_-implementer--developer--muse-_RUN-261007-08e3af.log) — System spawn log captured by task-board
- [TASK-260929-3f6hfg_results.md](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_results.md) — Vertical test results rev2: hosted precheck 1 applied, 5/5 mutants killed by vertical tests
- [TASK-260929-3f6hfg_mutants.json](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_mutants.json) — 5 narrowing mutant patches with named killing tests
- [TASK-260929-3f6hfg_spawn-log_-implementer--developer--muse-_RUN-261007-764d5a.log](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_spawn-log_-implementer--developer--muse-_RUN-261007-764d5a.log) — System spawn log captured by task-board
- [TASK-260929-3f6hfg_spawn-log_-implementer--developer--muse-_RUN-261007-c065ca.log](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_spawn-log_-implementer--developer--muse-_RUN-261007-c065ca.log) — System spawn log captured by task-board
- [TASK-260929-3f6hfg_coverage-map.md](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_coverage-map.md) — Surface-table coverage map: 3 rows to attacking tests and killed narrowing mutants
- [TASK-260929-3f6hfg_change-request_rev1.patch](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_change-request_rev1.patch) — Change Request CR-TASK-260929-3f6hfg-1 revision 1 candidate patch (repository_delta=present, 33 changed paths)
- [TASK-260929-3f6hfg_change-request_rev1-validation.log](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_change-request_rev1-validation.log) — Change Request CR-TASK-260929-3f6hfg-1 revision 1 bounded validation log
- [TASK-260929-3f6hfg_review-verdict-rev1.md](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_review-verdict-rev1.md) — Merged panel accept verdict with recording reviewer attestation; all 8 notes and 3 held rows preserved
- [TASK-260929-3f6hfg_spawn-log_-reviewer--reviewer--codex-_RUN-261007-554bf3.log](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_spawn-log_-reviewer--reviewer--codex-_RUN-261007-554bf3.log) — System spawn log captured by task-board
- [TASK-260929-3f6hfg_recording-review-rev1.md](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_recording-review-rev1.md) — Recording reviewer merge audit: both panels accept, 0 findings, 8/8 notes preserved, 3/3 held surface rows
- [TASK-260929-3f6hfg_review-verdict-recorded-rev1.md](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_review-verdict-recorded-rev1.md) — Recording-owned merged verdict: 3 held rows, no blocking/free-hunt findings; full panel notes and hunt narrative preserved
- [TASK-260929-3f6hfg_spawn-log_-implementer--developer--codex-_RUN-261007-a970a6.log](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_spawn-log_-implementer--developer--codex-_RUN-261007-a970a6.log) — System spawn log captured by task-board
- [TASK-260929-3f6hfg_complete-log.md](file://TASK-260929-3f6hfg/TASK-260929-3f6hfg_complete-log.md) — Landing checks and both completion transaction outputs with exit codes

## Created
2026-09-29T00:50:51Z

## Last Update
2026-10-07T15:52:16Z

## Assigned To
[implementer] developer (codex)
