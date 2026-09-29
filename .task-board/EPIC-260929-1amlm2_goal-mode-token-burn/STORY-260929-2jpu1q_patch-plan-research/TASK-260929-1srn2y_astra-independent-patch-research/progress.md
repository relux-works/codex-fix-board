## Status
done

## Review
none

## Task Class
research

## Estimate
notEstimated

## Blocked By
- (none)

## Blocks
- (none)

## Checklist
- [x] Own article-coverage table built before reading research.md: every mechanism and proposed fix mapped to upstream state at 33a0f766a6 with path:line evidence (Q1)
- [x] Per-patch verdict for P1-P6 (agree/modify/reject) with reasons and corrected designs where disagreeing
- [x] Questions Q2-Q10 from brief.md answered with evidence or marked unresolved with the cheapest resolution path during implementation
- [x] Final recommended patch series table: order, files, tests (unit + core/tests/suite), rough size, risk
- [x] No tracked repository file modified, no commit, no push; budget 90 minutes respected
- [x] Outcome attached as TASK-260929-1srn2y_goal-token-burn-astra-review.md (type outcome)
- [x] Findings written to file
- [x] Key aspects highlighted
- [x] Fact-checking performed — claims verified, sources cited
- [x] Findings linked on the board as a new task-scoped outcome resource
- [x] All questions from task description answered
- [x] Important findings, decisions, anomalies, or regressions recorded in logbook when relevant
- [x] Implementation matches AC
- [x] Solution fits project architecture
- [x] Tests green
- [x] Gate, refusal, validation, authorization, and attestation behavior attacked, not read — positive-path-only evidence is not accepted
- [x] If review does not accept the work — verdict evidence added and status routed by the explicit verdict branches
- [x] Rev2: findings resolution table covers F1, F2 and N1-N10 (resolved with section reference, or rejected with pinned evidence)
- [x] Rev2: P5 delivery redesigned on the trigger-turn mailbox with acceptance = included in a sampling request; both F1 paths in the race table with tests
- [x] Rev2: P2 uses a goal-active marker in thread extension data with explicit insert/remove hooks, precedence vs sleep switches, negative and positive tests
- [x] Rev2: consolidated final plan attached as TASK-260929-1srn2y_goal-token-burn-final-plan.md (type outcome), self-contained, under 45 KB

## Notes
spawn agent resolution: Agent selection: codex via explicit_override
spawn queued: [analyst] researcher (codex) (run=RUN-260928-c2e691, max_parallel=4)
spawn run started: [analyst] researcher (codex) (run=RUN-260928-c2e691)
Independent article/code coverage table persisted in the task scratch outcome before P1-P6 comparison. Key findings: worktree HEAD 88e9a8329d differs from pinned 33a0f766a6 (reading pinned blobs); native child completion uses trigger_turn=false; empty-turn guard predates the article and excludes text-only waiting. Bounded research continues; no source edits/builds/commits.
Research handoff evidence: TASK-260929-1srn2y_goal-token-burn-astra-review.md attached as outcome (39769 bytes). Q1-Q10 answered; P1-P5 modified, P6 deferred; recommended staged implementation starts P1 then P5+P4a. Logbook is included in section 6 of the outcome, per the run write boundary. Key findings: native completion is normally queue-only; global idle suppression would starve queued user input; headless exec exits at turn completion; cached input is excluded from current goal budget; global Value normalization changes passthrough semantics. Coverage table was saved before deliberate plan comparison, but literal blind exposure was impossible because research.md was inlined in the assignment. Static-only verification: git diff --exit-code=0, git diff --check=0, artifact verifier=0 (111 citation ranges in 61 pinned files; structure/ranges, not runtime proof). No builds/tests, tracked edits, commits or pushes. HEAD remains 88e9a8329d17bd141e4f3f0e7c78d07a7baa8b23; claims use pinned 33a0f766a6. Elapsed approximately 30 minutes of 90. Remaining implementation bounds are explicitly listed; no additional research leaf requested.
agent completed: [analyst] researcher (codex) (exit=0)
spawn run completed: codex (run=RUN-260928-c2e691, pid=71620, exit=0)
Orchestrator evidence check (review=none): outcome TASK-260929-1srn2y_goal-token-burn-astra-review.md (39769 bytes) read in full; checklist 12/12. Spot-verified 9 load-bearing claims at 33a0f766a6: current_turn_trigger getter exists (core/src/turn_metadata.rs:355); remote catalog replaces bundled models (models-manager/src/manager.rs:572-603); native child completion uses trigger_turn=false (core/src/agent/control/completion.rs:96-106); queue extension dispatches queued user input from on_thread_idle (ext/queue/src/service.rs:549-565); headless exec initiates shutdown on TurnCompleted (exec/src/event_processor_with_human_output.rs:309-339); goal budget excludes cached input (ext/goal/src/accounting.rs:527-531); max_goal_token_budget lives under [goals] (config/src/config_toml.rs:482,723); dynamic tools parse arguments into Value via parse_arguments (core/src/tools/handlers/dynamic.rs:138); JsonSchema::integer exists (tools/src/json_schema/types.rs:128). All confirmed. Accepted on evidence. Board element left at to-review: set_status(done) is refused while a CR exists, and the only sanctioned close (accept_cr + worktree integrate) would add commits to the upstream openai/codex checkout and publish board state, which is out of scope for this local, git-excluded board.
spawn agent resolution: Agent selection: claude via explicit_override
spawn queued: [reviewer] reviewer (claude) (run=RUN-260928-a6e86b, max_parallel=4)
spawn run RUN-260928-a6e86b failed; operator action required; failure: queued spawn preparation failed: composing review-round brief: loading the surface table for the review-round brief: surface table "surface-table.md" carries no ```surface-table block: a present table with no row set is malformed, not an absent table
spawn agent resolution: Agent selection: claude via explicit_override
spawn queued: [reviewer] reviewer (claude) (run=RUN-260928-a4ac16, max_parallel=4)
spawn run started: [reviewer] reviewer (claude) (run=RUN-260928-a4ac16)
Reviewer RUN-260928-a4ac16 verdict on CR rev 1: changes_requested. Empty repository delta is correct for this research leaf; rework is to the document. Blocking: F1 p5-acceptance-without-wake (robustness): plan defines completion ownership as turn acceptance, but at 33a0f766a6 inject_if_running accepts into a bare reservation that clear_reserved_idle_turn drops (inject.rs:21-37, turn_input.rs:615-624) and late input into a finishing task is recorded to history without a wake (tasks/mod.rs:668-697, 884, 451-457); fix by defining acceptance as sampled and delivering via the trigger-turn mailbox. F2 p2-goals-feature-overrides-sleep-config (regression): Feature::Goals is Stable/default-true (features/src/lib.rs:1702-1706) so the rev2 P2 rule exposes clock.sleep in every session and overrides current_time_reminder.sleep_tool=false (config/mod.rs:1311-1316, spec_plan.rs:1237-1244); the first-turn-gap justification fails because tools are rebuilt per sampling step (turn.rs:424-470) and spec_plan reads thread_extension_data (spec_plan.rs:137,341-343); fix with a goal-active marker. Rows: 6 held, 2 broken (p5-completion-delivery, p2-p3-capability-consistency). 10 notes incl. P4b two-poll blind spot, durable-sleep primitive for P4c, goal token_budget float gap. Evidence: TASK-260929-1srn2y_review-verdict-rev1.md. Routing to analysis.
agent completed: [reviewer] reviewer (claude) (exit=0)
spawn run completed: claude (run=RUN-260928-a4ac16, pid=54506, exit=0)
loop-detector rev1: S2/S3/S5 not evaluable — runtime-recorded verdict carries no stamped findings array
Orchestrator check of reviewer verdict RUN-260928-a4ac16 (changes_requested, TASK-260929-1srn2y_review-verdict-rev1.md): both blocking findings reproduced at 33a0f766a6. F1: inject_if_running accepts into any active_turn without the task.is_none() refusal that inject_hook_context_if_running applies (core/src/session/inject.rs:17-60); clear_reserved_idle_turn drops such a reservation (core/src/session/turn_input.rs:615-623); task end records unsampled pending input via run_hooks_and_record_inputs (core/src/tasks/mod.rs:670-695) and maybe_start_turn_for_pending_work wakes only for trigger_turn mail or a durable SleepItem (core/src/tasks/mod.rs:422-458, 883-885). F2: CurrentTimeReminderConfig.sleep_tool is a documented switch defaulting to false (core/src/config/mod.rs:1311-1325); spec planning reads thread_extension_data (core/src/tools/spec_plan.rs:135-139, 338-343); step context is captured per sampling request (core/src/session/turn.rs:424-470). Rework scope for revision 2: fold verdict section 8 corrections (P2 goal-active marker, P5 mailbox delivery with acceptance = sampled, P4c durable-sleep marker, P4b outcome-based classifier, P1 token_budget, P3 exact capability flags) into the final patch series.
spawn agent resolution: Agent selection: codex via explicit_override
spawn queued: [analyst] researcher (codex) (run=RUN-260928-91c9cd, max_parallel=4)
spawn run started: [analyst] researcher (codex) (run=RUN-260928-91c9cd)
Rev2 research started 2026-09-28 23:40 UTC; continuing the original 90-minute budget (about 31 minutes used previously, about 55 available). Scope: one self-contained outcome under 45 KB, no source edits or builds. Reproduced F1 and F2 at pinned 33a0f766a6; choosing internal runtime-completion mailbox variant with sampling acknowledgment, goal-active extension-data marker, and explicit durable-sleep ownership. Worktree HEAD bfdb1571780b326ce978696de12b1d81b5e978f2 differs from the pin. Research-only negative evidence will be labeled as source traces/document validation, never production-test proof.
Revision 2 outcome attached: TASK-260929-1srn2y_goal-token-burn-final-plan.md, 44720 bytes, SHA256 e25bfd07e8e2559570b67e37d98653c3537a1cac34039ffee938796bd6e0f4a0. F1/F2 and N1-N10 resolved or explicitly adjudicated; P5 uses retained mailbox leases until sampling, P2 uses goal-active thread data with config precedence, and V1 native completion needs a mailbox bridge. Q1-Q10, patch sequence, race tests, article coverage and outcome-scoped logbook are self-contained. Validation: research_checks.py exit 0, 186 checks / 117 citation ranges / 17 pinned anchors (research-check-16.log). Eleven narrowed plan-rule mutants exited 1 as expected (logs 04-14); both F1 regressions are isolated in 13/14. Coverage 8/8 research surfaces, 0/8 production behaviors executed. No Rust build/test claimed. git diff --exit-code, git diff --cached --exit-code and git diff --check all exit 0; status empty. Checklist 13-15 apply to research AC/design and the executed research verifier, not implementation or unrun Rust tests. All logs are in the run worktree .temp/goal-token-burn-rev2; no control-root files edited. About 37 minutes this run plus 31 previously, below the 90-minute budget.
agent completed: [analyst] researcher (codex) (exit=0)
spawn run completed: codex (run=RUN-260928-91c9cd, pid=17214, exit=0)
spawn agent resolution: Agent selection: codex via explicit_override
spawn queued: [analyst] researcher (codex) (run=RUN-260929-2e6ed6, max_parallel=4)
spawn run started: [analyst] researcher (codex) (run=RUN-260929-2e6ed6)
agent completed: [analyst] researcher (codex) (exit=0)
spawn run completed: codex (run=RUN-260929-2e6ed6, pid=36085, exit=0)
spawn agent resolution: Agent selection: claude via explicit_override
spawn queued: [reviewer] reviewer (claude) (run=RUN-260929-e591f8, max_parallel=4)
spawn run started: [reviewer] reviewer (claude) (run=RUN-260929-e591f8)
Review round 2 (CR rev 3, RUN-260929-e591f8, claude-fable-5-1): ACCEPTED. F1 resolved: acceptance = included in a sampling request, delivery via the existing trigger-turn mailbox with leased runtime entries; both F1 paths (cleared idle reservation, finishing task) in the race table with named tests, verified against input_queue.rs:142-228, tasks/mod.rs:437-534/668-697/884, turn_input.rs:395-478/615-623 at 33a0f766a6. F2 resolved: goal-active marker in extension-api thread data, every insert/remove hook resolves to the cited goal-extension lines, precedence keeps features.sleep_tool and current_time_reminder.sleep_tool authoritative (CurrentTimeReminder is off by default; its sleep_tool=true auto-default applies only at ReasoningEffort::Persistent), negative+positive request-level tests named. N1-N10 all resolved or rejected with pinned evidence. 8/8 surface rows held; 0 findings; 9 non-blocking notes (suspended-receipt vs trigger gate, explicit-reminder precedence edge, write_stdin session_id i32 wording, public TurnInput touch points, admission hook is new code, dead code in inactive stages, V1 bridge visibility, receipt slot exhaustion after 64 unreleased sampled receipts, 2 turns per completion in goal mode). Empty repository delta is correct for this read-only research leaf. Evidence: TASK-260929-1srn2y_review-verdict-rev3.md.
agent completed: [reviewer] reviewer (claude) (exit=0)
spawn run completed: claude (run=RUN-260929-e591f8, pid=70607, exit=0)

External integration evidence: Read-only research leaf; deliverable is the board outcome TASK-260929-1srn2y_goal-token-burn-final-plan.md (SHA-256 e25bfd07e8e2559570b67e37d98653c3537a1cac34039ffee938796bd6e0f4a0, 44720 bytes), accepted by reviewer RUN-260929-e591f8 (claude-fable-5-1 max) with verdict TASK-260929-1srn2y_review-verdict-rev3.md: 8/8 surface rows held, 0 findings, 9 implementation notes. Nothing lands in this repository by design: the control root is an upstream openai/codex clone and the plan is consumed by a separate implementation Story.

## Precondition Resources
- [brief.md](file://TASK-260929-1srn2y/brief.md) — Research brief: decision, budgets, questions Q1-Q10, constraints, outcome structure
- [article.md](file://TASK-260929-1srn2y/article.md) — Source article text (relux.works codex-goal-token-burn), fetched 2026-09-29
- [tekacs-9ffcf8d.trimmed.patch](file://TASK-260929-1srn2y/tekacs-9ffcf8d.trimmed.patch) — tekacs/codex 9ffcf8d background exec completion wake patch (models.json hunk summarized)
- [tekacs-fork-analysis.md](file://TASK-260929-1srn2y/tekacs-fork-analysis.md) — Prior verdict: fork does not fix the goal continuation spin
- [research.md](file://TASK-260929-1srn2y/research.md) — Primary session patch plan P1-P6 to challenge
- [research-rev2.md](file://TASK-260929-1srn2y/research-rev2.md) — Primary plan rev 2 after merging the astra review (section 5)
- [surface-table.md](file://TASK-260929-1srn2y/surface-table.md)
- [review-brief.md](file://TASK-260929-1srn2y/review-brief.md)
- [rework-brief-rev2.md](file://TASK-260929-1srn2y/rework-brief-rev2.md) — Rework brief for CR revision 2: resolve F1/F2 + notes into one final patch plan
- [research-rev3.md](file://TASK-260929-1srn2y/research-rev3.md) — Primary plan with section 6: review round 1 outcome
- [republish-brief-rev3.md](file://TASK-260929-1srn2y/republish-brief-rev3.md) — Mechanical republish of the unchanged rev-2 final plan as CR rev 3 after workspace base converge

## Outcome Resources
- [TASK-260929-1srn2y_spawn-log_-analyst--researcher--codex-_RUN-260928-c2e691.log](file://TASK-260929-1srn2y/TASK-260929-1srn2y_spawn-log_-analyst--researcher--codex-_RUN-260928-c2e691.log) — System spawn log captured by task-board
- [TASK-260929-1srn2y_goal-token-burn-astra-review.md](file://TASK-260929-1srn2y/TASK-260929-1srn2y_goal-token-burn-astra-review.md) — Independent pinned-source review: Q1-Q10, P1-P6 verdicts, revised patch order, race matrix and implementation bounds; 39769 bytes.
- [TASK-260929-1srn2y_change-request_rev1.patch](file://TASK-260929-1srn2y/TASK-260929-1srn2y_change-request_rev1.patch) — Change Request CR-TASK-260929-1srn2y-1 revision 1 candidate patch (repository_delta=empty, 0 changed paths)
- [TASK-260929-1srn2y_spawn-log_-reviewer--reviewer--claude-_RUN-260928-a6e86b.log](file://TASK-260929-1srn2y/TASK-260929-1srn2y_spawn-log_-reviewer--reviewer--claude-_RUN-260928-a6e86b.log) — System spawn log captured by task-board
- [TASK-260929-1srn2y_spawn-log_-reviewer--reviewer--claude-_RUN-260928-a4ac16.log](file://TASK-260929-1srn2y/TASK-260929-1srn2y_spawn-log_-reviewer--reviewer--claude-_RUN-260928-a4ac16.log) — System spawn log captured by task-board
- [TASK-260929-1srn2y_review-verdict-rev1.md](file://TASK-260929-1srn2y/TASK-260929-1srn2y_review-verdict-rev1.md) — Reviewer verdict for CR-TASK-260929-1srn2y-1 rev 1: changes_requested (F1 p5-acceptance-without-wake robustness, F2 p2-goals-feature-overrides-sleep-config regression), 8-row surface table, adjudication and per-patch corrections
- [TASK-260929-1srn2y_spawn-log_-analyst--researcher--codex-_RUN-260928-91c9cd.log](file://TASK-260929-1srn2y/TASK-260929-1srn2y_spawn-log_-analyst--researcher--codex-_RUN-260928-91c9cd.log) — System spawn log captured by task-board
- [TASK-260929-1srn2y_goal-token-burn-final-plan.md](file://TASK-260929-1srn2y/TASK-260929-1srn2y_goal-token-burn-final-plan.md) — Consolidated revision 2: F1/F2 and N1-N10 resolution, sampled mailbox delivery, goal-active sleep marker, patch stages and negative evidence. 44720 bytes; research only.
- [TASK-260929-1srn2y_change-request_rev2.patch](file://TASK-260929-1srn2y/TASK-260929-1srn2y_change-request_rev2.patch) — Change Request CR-TASK-260929-1srn2y-2 revision 2 candidate patch (repository_delta=present, 45 changed paths)
- [TASK-260929-1srn2y_spawn-log_-analyst--researcher--codex-_RUN-260929-2e6ed6.log](file://TASK-260929-1srn2y/TASK-260929-1srn2y_spawn-log_-analyst--researcher--codex-_RUN-260929-2e6ed6.log) — System spawn log captured by task-board
- [TASK-260929-1srn2y_republish-rev3-note.md](file://TASK-260929-1srn2y/TASK-260929-1srn2y_republish-rev3-note.md) — Revision 3 republish note for unchanged final plan
- [TASK-260929-1srn2y_change-request_rev3.patch](file://TASK-260929-1srn2y/TASK-260929-1srn2y_change-request_rev3.patch) — Change Request CR-TASK-260929-1srn2y-3 revision 3 candidate patch (repository_delta=empty, 0 changed paths)
- [TASK-260929-1srn2y_spawn-log_-reviewer--reviewer--claude-_RUN-260929-e591f8.log](file://TASK-260929-1srn2y/TASK-260929-1srn2y_spawn-log_-reviewer--reviewer--claude-_RUN-260929-e591f8.log) — System spawn log captured by task-board
- [TASK-260929-1srn2y_review-verdict-rev3.md](file://TASK-260929-1srn2y/TASK-260929-1srn2y_review-verdict-rev3.md) — Review round 2 verdict for CR revision 3 (final plan): accepted; F1/F2 resolved at the pin, 8/8 rows held, 0 findings, 9 notes, verdict-findings block

## Created
2026-09-28T22:16:21Z

## Last Update
2026-09-29T00:39:00Z

## Assigned To
[reviewer] reviewer (claude)
