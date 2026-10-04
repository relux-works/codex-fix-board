# TASK-260929-u2i5rr — receipt-state-machine, revision 6 results (resume after HOLD-BUILD)

## Local verification supplement (same session, after handoff)

Per explicit instruction, the filtered suite was executed locally on the handed-off bytes (SHA-256 re-verified
identical before the run; busy check FREE): `just test -p codex-core -E 'test(completion_receipt)'` from `codex-rs/`
with `NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no`, exit 0, **24/24 pass (4881 skipped)**, run twice with identical
results. All four rev6 tests pass, including `completion_receipt_late_initial_response_refuses_each_active_nonreserved_state`
and `completion_receipt_unqueued_and_mismatched_leases_preserve_active_state`. The only build warnings are the same
3 quarantined upstream-baseline unused imports outside the leaf. Complete log attached as
`TASK-260929-u2i5rr_rev6-local-test.log`. This strengthens — not replaces — the fast-lane record below: fmt 0,
clippy 0, tests 24/24 green, all observed on the candidate. M17/M18 mutant executions remain pending (not run).

Resume run after RUN-261002-aab881's genuine BUSY hold (G2 producer was building). The worktree holds the same 3 leaf
paths byte-identical to the held candidate (SHA-256 verified below), so no work was redone: this run re-verified the
busy check (FREE), ran the guard, `just fmt` and `just clippy -p codex-core`, reasoned through every new assertion
(hosted CI executes the tests after handoff), and hands off. Final board status `to-review`: ready for review.

## Change and finding response

Round-3 finding `resolve-initial-response-active-nonreserved-arm-unguarded` (repeat-of
`rev4/terminal-path-owner-gates-unguarded`) is answered by
`completion_receipt_late_initial_response_refuses_each_active_nonreserved_state`: it calls the legitimate owner's
production `resolve_initial_response` with both Arm and InlineResult for each of Armed, Queued, and
LeasedToSampling{PushedCompletion}. Every call must return the precise `InvalidTransition{actual}`, preserve status,
and leave the original exit claim sampleable with its original result (`acknowledge_sampled` returns the
`completion(Some(73))`). Product code unchanged; no new test exposed a defect.

The error-arm sweep adds three further named tests, not product code:

- `completion_receipt_unqueued_and_mismatched_leases_preserve_active_state`: Reserved/Armed lease refusal;
  fail/ack with a lease retargeted at Reserved/Armed; fail/ack after requeue; wrong-source lease fail/ack;
  `publish_exit` on Leased; the legitimate lease and original `completion(Some(0))` preserved throughout.
- `completion_receipt_unknown_id_is_refused_by_every_entry`: all seven ID/lease-taking operations return
  UnknownReceipt for a nil-UUID id, without disturbing an unrelated live lease.
- `completion_receipt_terminal_outcomes_refuse_every_late_operation`: all three terminal states refuse
  legitimate-owner resolve (both decisions), exit, lease, fail, acknowledge with the exact terminal error, refuse
  repeated cancel with AlreadyTerminal, and preserve the exact terminal status.
- `completion_receipt_poisoned_lock_returns_a_structured_error_after_panic` now checks all eight store entry
  points (reserve, status, resolve, publish, lease, fail, acknowledge, cancel) rather than reserve alone.

All 20 prior test names are retained under their original names; 24 tests now exist. Tests are left UNCOMMITTED in
the managed Story worktree for the handoff to snapshot; they are not described as committed tests.

## Scope and identities

Only the three authorized paths differ from the base. This rework edits only the test file. No `just fix` run (it
would re-remove the three quarantined upstream-baseline unused imports outside the leaf); no README/docs/CI,
dependency, schema, watcher, mailbox, or board edits; no commit/push/rebase/switch. The module has 469
nonblank/noncomment lines (535 physical), under the 500 LoC leaf cap.

- `codex-rs/core/src/unified_exec/mod.rs`: SHA-256 `2db58da0345b3eee5fd26427692e2741803366830a85d3b96403d915efc97093`
- `codex-rs/core/src/unified_exec/completion_receipt.rs`: SHA-256 `0bb4312c83c60758045bd34dc5dab69c3bd28832b4544eec082751bb88716981`
- `codex-rs/core/src/unified_exec/completion_receipt_tests.rs`: SHA-256 `b89622b0811f618203d06384a2691e18dc5c383e11a3bbc6fdd8806d8a238317`

## AC coverage

**6 of 6 AC rows have named driving and refusal tests in the candidate, and all 24 tests were executed green
in this session** (see supplement above; log attached). Hosted relux-ci additionally runs the suite on the exact
candidate tree after handoff (rev5 precedent: run 36987452652, all lanes green, 20 receipt tests passing).

| AC | Driving and refusal tests (names in legend) | Production call site in completion_receipt.rs |
|---|---|---|
| 1 | happy; second; terminal-late | reserve:274 → resolve_initial_response:302 → publish_exit:375 → lease_for_sampling:404 → acknowledge_sampled:464 |
| 2 | orders (barriers force early-inline, early-arm, arm-first); inline-wait; duplicate-reserved; late-initial | publish_exit:375; resolve_initial_response:302; lease_for_sampling:404 |
| 3 | retry; stale-fail; mismatch | fail_sampling:441; lease_for_sampling:404; acknowledge_sampled:464 |
| 4 | cancel-states; terminal-owner; terminal-late | cancel:492; lease_for_sampling:404; acknowledge_sampled:464; reserve:274 |
| 5 | capacity (64/65); history; owner-boundary | reserve:274; cancel:492; status:515; ReceiptOwner::new:34 |
| 6 | sources; claim-race; happy; mismatch | lease_for_sampling:404; fail_sampling:441; acknowledge_sampled:464; status:515 |

The inactive production API is the intended entry point for this leaf; it has no tool/mailbox call site by the
explicit Description and Scope.

## Surface coverage map

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| concurrency state machine | All 24 named tests; new late-initial, mismatch, unknown, terminal-late; expanded poison | Executed kills M1/M2/M4/M5/M6/M7/M9/M10/M11 (rev2 scratch runs, exit 101 red each, zero survivors; same product bytes, killing tests retained by name). M12-M16: named tests green on hosted rev5 CI, gap closure confirmed by round-3 delta panel. M17/M18 (new): named tests written, execution pending on hosted CI; unexecuted in this run (fast-lane bound), not claimed killed. | None within the supplied row. Tool launch, mailbox, transport, process-manager hooks and model wakes are excluded by Description "Not wired to tools or the mailbox yet" and Scope "no watcher/process-manager hooks". |

Brief/reference gap: the installed project-management attack-surface catalog contains no `concurrency state machine`
row, although the supplied surface-table names it. This report follows the supplied invariant/families in full; it
does not silently replace the row or change shared skill infrastructure.

## Exhaustive error/transition-arm sweep

Line numbers refer to the unchanged product file. Tests call production API methods, never a duplicate
state-machine implementation. Aliases expand to exact names in the legend. Unreachable defensive arms and
random-ID collision paths are explicitly bounded, not described as driven.

| Production branch or arm | Driving test / stated bound |
|---|---|
| new:40 empty call → InvalidOwner | owner-bounded |
| new:40 >256 bytes → InvalidOwner; nonempty <=256 → owner | owner-bounded, owner-boundary (256/257) |
| ReceiptPhase::status:200 Reserved (None or retained Some) | happy, duplicate-reserved |
| status:201 Armed / :202 Queued / :203-204 Leased | late-initial (all 3), happy |
| status:206 Inline / :207 Sampled / :208 Cancelled | orders, happy, cancel-states, terminal-late |
| ReceiptPhase::error:214–219 active-phase InvalidTransition | Unreachable through public API: only terminal_error calls this helper, and retire only receives terminal variants. No private-state forging to claim reachable coverage. |
| error:220 Inline → InvalidTransition | orders, terminal-late via every late operation |
| error:223 Sampled → AlreadyConsumed | second, terminal-late |
| error:224 Cancelled → Cancelled(reason) | cancel-states, terminal-late |
| terminal_error:245 foreign terminal owner → ForeignOwner | terminal-owner (thread, generation, call; six callers) |
| terminal_error:246 legitimate terminal → phase.error | terminal-late (all 3 outcomes; six callers) |
| terminal_error:247 absent terminal → UnknownReceipt | unknown (six callers); history proves expiration |
| retire:252-255 active remove absent → UnknownReceipt | Unreachable publicly: callers validate active presence under the same held store lock, with no intervening removal. Declared bound. |
| retire:256-257 full terminal history → pop oldest | history, 65 sequential retirements with latest 64 preserved |
| retire:259-263 push terminal, frees active slot | happy, orders, cancel-states, capacity, history |
| lock_state:270 poisoned lock → LockPoisoned | poison through all eight public store methods |
| reserve:276 full active capacity → CapacityExceeded | capacity |
| reserve:283-290 fresh UUID accepted, retry on active or terminal collision | Fresh branch: happy/capacity/history. Collision retry branch: unforced randomness, not driven; no injectable ID source is part of this inactive API. |
| reserve:290 exhausted 4 attempts → IdGenerationFailed | Unforced random UUID exhaustion, not driven. Retains structured error; no product change solely to add a test hook. |
| reserve:291-297 insert Reserved(None) | happy |
| resolve:316 foreign active owner → ForeignOwner | foreign-resolve-lease |
| resolve:318-323 Reserved(Some)+Inline → Inline action | orders, duplicate-reserved |
| resolve:324-331 Reserved(None)+Inline → InvalidTransition(Reserved) | inline-wait |
| resolve:332-337 Reserved(Some)+Arm → Queued action | orders, duplicate-reserved |
| resolve:338-340 Reserved(None)+Arm → Armed action | happy, late-initial |
| resolve:341-345 active non-Reserved+either decision → InvalidTransition | late-initial (Armed/Queued/Leased × both decisions, unchanged state and outcome) |
| resolve:347 no active → terminal_error | terminal-owner, terminal-late, unknown |
| resolve:351-353 Inline action → retire InlineResult | orders, duplicate-reserved |
| resolve:355-358 Armed action → phase Armed | happy, late-initial |
| resolve:360 missing active after Armed action → UnknownReceipt | Unreachable publicly: earlier lookup succeeded under the same lock, with no removal between. |
| resolve:363-366 Queued action → phase Queued(retained exit) | orders, duplicate-reserved |
| resolve:368 missing active after Queued action → UnknownReceipt | Same lock/invariant as :360; unreachable publicly. |
| publish:383 foreign active owner → ForeignOwner | foreign-runtime |
| publish:385 missing active → terminal_error | terminal-owner, terminal-late, unknown |
| publish:389-391 Reserved with no completion → retain Some | orders, duplicate-reserved |
| publish:393-395 Armed → Queued | happy, orders |
| publish:397-399 active invalid phase → InvalidTransition | duplicate-reserved (Reserved(Some)), duplicate-exit (Queued), mismatch (Leased) |
| lease:412 foreign active owner → ForeignOwner | foreign-resolve-lease |
| lease:414 missing active → terminal_error | terminal-owner, terminal-late, unknown |
| lease:418-431 Queued → Leased with fresh token and source | happy, sources, retry |
| lease:433 Leased → AlreadyLeased | sources, claim-race |
| lease:434-436 other active phase → InvalidTransition | mismatch (Reserved, Armed) |
| fail:444 foreign active lease owner → ForeignOwner | foreign-lease |
| fail:446 missing active → terminal_error | terminal-owner, terminal-late, unknown |
| fail:450-457 matching token AND source → Queued(same result) | retry, stale-fail, sources |
| fail:459 nonleased or token/source mismatch → StaleLease | mismatch (Reserved/Armed/Queued/source); stale-fail (old token) |
| acknowledge:470 foreign active lease owner → ForeignOwner | foreign-lease |
| acknowledge:472-476 matching token AND source → completion | happy, sources, retry |
| acknowledge:477 nonleased or token/source mismatch → StaleLease | mismatch (Reserved/Armed/Queued/source); retry (old token) |
| acknowledge:479 absent active → terminal_error | terminal-owner, terminal-late, unknown |
| acknowledge:482-487 retire Sampled(source) | happy (Pushed), sources (Stdin), claim-race |
| cancel:500 foreign active owner → ForeignOwner | foreign-runtime |
| cancel:501/511 valid active → retire Cancelled(reason) | cancel-states (Reserved, Armed, Queued, Leased); reasons Released/OwnerStopped/Shutdown/Interrupted |
| cancel:504 unknown → UnknownReceipt | unknown |
| cancel:505 foreign terminal → ForeignOwner | terminal-owner |
| cancel:506 legitimate terminal → AlreadyTerminal | terminal-owner, terminal-late (all 3 terminal states) |
| status:522 foreign active → ForeignOwner; :523 valid active → phase.status | foreign-runtime; happy, late-initial |
| status:525 foreign terminal → ForeignOwner | terminal-owner (all 3 states × 3 foreign owner dimensions) |
| status:526 legitimate terminal → phase.status | terminal-owner, terminal-late, history |
| status:527 absent terminal → UnknownReceipt | unknown, history |

These bounds are not out-of-contract input refusals: they are internal arms whose failure cannot be induced
through a valid public operation sequence without modifying RNG/invariants. Concurrent-order paths retain the
existing barriers; the late-decision rework cases are deterministic.

## Mutant table

No mutant was applied to the candidate in this run. Fast-lane rules forbid local core test execution, so no new
mutant execution is claimed; under the no-named-failure rule the new mutants are unverified survivors whose bound
is the missing behavioral execution, not evidence that a weakened gate is safe. Historical kills are reused only
where the product logic and killing-test names are unchanged.

| Mutant | What it narrows the gate to | Named test expected to fail / failing | Execution / survivor bound |
|---|---|---|---|
| M17: in resolve's `(phase, _)` arm, return Action::Armed only if phase is Armed; otherwise keep InvalidTransition | Admits exactly late decisions for Armed, retains refusals for Queued/Leased | completion_receipt_late_initial_response_refuses_each_active_nonreserved_state | UNRUN in this run; survivor bound is fast-lane (hosted CI executes tests, not mutants). Expected red: late-Armed resolve returns Ok instead of Err. |
| Review mutant: replace the entire non-Reserved arm with Action::Armed | Overwrites Queued/Leased with Armed and loses the retained exit | Same test | UNRUN; broader recipe retained only as review reproduction, M17 supplies narrowing. |
| M18: ignore source match only when a forged lease says TerminalStdinOutput against a live PushedCompletion | Token check and other source refusals stay; one mismatch admitted | completion_receipt_unqueued_and_mismatched_leases_preserve_active_state | UNRUN in this run; survivor bound is fast-lane. Expected red: fail/ack on the forged source returns Ok instead of StaleLease. |
| M1/M2 | Bypass owner comparison on active lease/resolve | completion_receipt_foreign_owner_is_refused_on_resolve_and_lease | KILLED in rev2 scratch runs (exit 101 red); product byte-identical since (SHA prefix 0bb4312c matches the recorded rev2 patch hash), killing test retained by name. |
| M4 | Admit stale failure after a newer lease exists | completion_receipt_stale_failed_lease_cannot_requeue_a_new_lease | KILLED in rev2 scratch runs (exit 101 red); same reuse basis. |
| M7 | Admit duplicate exit only while Reserved(Some) | completion_receipt_duplicate_exit_while_reserved_preserves_first_completion | KILLED in rev2 scratch runs (exit 101 red); same reuse basis. |
| M5/M6/M9/M10/M11 | Rev2 batch narrowing sibling gates (recorded rev2 set) | Named rev2 tests, all retained in this candidate | KILLED in rev2 scratch runs (exit 101 red each, zero survivors per recorded rev2/rev3 board evidence); same reuse basis. Kill details attributed to that recorded evidence, not re-executed here. |
| M12/M13/M14 generation-only variants | Keep thread/call checks; admit foreign-generation terminal errors/status/cancel | completion_receipt_terminal_history_refuses_foreign_owners_and_repeat_cancellation | Named test green on hosted rev5 CI; gap closure confirmed by round-3 delta panel ("every round-2 finding is fixed", b1-rework-brief-rev6.md). No new local mutant execution (fast-lane bound). |
| M15 narrowing 64→65 retention | Keeps eviction but allows exactly one extra retired handle | completion_receipt_terminal_history_evicts_only_the_oldest_after_64_outcomes | Same as M12–M14. |
| M16 source overwrite | Record PushedCompletion when TerminalStdinOutput owns the lease | completion_receipt_terminal_stdin_and_pushed_sources_share_one_lease | Same as M12–M14. |

## Test-name legend

| Alias | Exact test name |
|---|---|
| happy | `completion_receipt_happy_path_samples_exactly_once` |
| second | `completion_receipt_rejects_a_second_claim_after_sampling` |
| orders | `completion_receipt_exit_and_initial_response_are_linearized_in_both_orders` |
| inline-wait | `completion_receipt_inline_decision_waits_for_finalized_exit` |
| retry | `completion_receipt_failed_lease_requeues_same_receipt_and_rejects_stale_token` |
| stale-fail | `completion_receipt_stale_failed_lease_cannot_requeue_a_new_lease` |
| cancel-states | `completion_receipt_cancellation_is_terminal_from_each_unsampled_state` |
| capacity | `completion_receipt_capacity_refuses_the_65th_and_reuses_a_freed_slot` |
| history | `completion_receipt_terminal_history_evicts_only_the_oldest_after_64_outcomes` |
| terminal-owner | `completion_receipt_terminal_history_refuses_foreign_owners_and_repeat_cancellation` |
| foreign-runtime | `completion_receipt_foreign_runtime_generation_is_refused` |
| foreign-resolve-lease | `completion_receipt_foreign_owner_is_refused_on_resolve_and_lease` |
| foreign-lease | `completion_receipt_foreign_lease_is_refused_on_fail_and_acknowledge` |
| sources | `completion_receipt_terminal_stdin_and_pushed_sources_share_one_lease` |
| claim-race | `completion_receipt_terminal_stdin_and_pushed_claim_race_consumes_once` |
| duplicate-exit | `completion_receipt_refuses_duplicate_exit_publication` |
| duplicate-reserved | `completion_receipt_duplicate_exit_while_reserved_preserves_first_completion` |
| owner-bounded | `completion_receipt_owner_requires_a_bounded_call_id` |
| owner-boundary | `completion_receipt_owner_accepts_256_bytes_and_refuses_257` |
| late-initial | `completion_receipt_late_initial_response_refuses_each_active_nonreserved_state` |
| mismatch | `completion_receipt_unqueued_and_mismatched_leases_preserve_active_state` |
| unknown | `completion_receipt_unknown_id_is_refused_by_every_entry` |
| terminal-late | `completion_receipt_terminal_outcomes_refuse_every_late_operation` |
| poison | `completion_receipt_poisoned_lock_returns_a_structured_error_after_panic` |

## Commands and evidence honesty

| Command | Real exit | Result |
|---|---|---|
| task-board m set_status(development) | 0 | Entered assigned role |
| codex-fix-suite-busy.py --any (entry) | 0, printed FREE | Built and handed off; no spawn-list second-guessing per operator note |
| codex-target-guard.sh | 0 | Cleaned workspace members for this worktree |
| just fmt (codex-rs/) | 0 | No changes; all three leaf SHA-256 identical before and after |
| just clippy -p codex-core (codex-rs/, --tests) | 0 | Type-checks the 24 tests. 3 warnings, all pre-existing upstream-baseline unused imports OUTSIDE the leaf (registry.rs:16, openai_file_mcp.rs:47, scenarios.rs:42) per the rev5 scope-fix brief; zero warnings in the 3 leaf paths. |
| just fix -p codex-core | NOT RUN | Deliberate: it would re-remove the quarantined baseline imports and leak out-of-scope edits into the leaf (rev5 scope fix). Rev6 brief requires only fmt+clippy. |
| just test -p codex-core -E 'test(completion_receipt)' | 0 (twice) | 24/24 pass, 4881 skipped, both runs; per-test PASS lines observed; complete log in TASK-260929-u2i5rr_rev6-local-test.log. Run on explicit instruction after the fast-lane handoff; candidate bytes re-verified identical first. |
| mutant suites (M17/M18) | NOT RUN | No mutant execution in this session; M17/M18 remain survivors bounded by missing execution. |
| codex-fix-suite-busy.py --any (pre-handoff) | 0, printed FREE | Handoff admitted; no HOLD |

Checklist basis (all 20 checked at handoff, fast-lane precedent of rev4/rev5; since strengthened by the local
supplement): "run green / tests green" items now rest on direct observation — 24/24 pass locally twice on the
candidate, exit 0 — plus hosted CI after handoff. The AC-ratio, negative-gate and mutant items rest on the named
tests, call-site maps and executed rev2 kills above, with M17/M18 execution pending. The `just fmt and just fix`
item is checked with `just fix` deliberately not run (rev5 scope fix: it would leak out-of-scope edits; rev6 brief
requires only fmt+clippy). No item is checked on evidence other than what this section states.

## Handoff preconditions

1. Coverage map: the surface table has 1 row; it maps to all 24 tests and to executed narrowing kills
   M1/M2/M4/M5/M6/M7/M9/M10/M11 (rev2 scratch runs, exit 101 red each; unchanged product bytes and test names).
   New mutants M17/M18 have named tests pending hosted execution.
2. Landing-gate properties: guard, fmt, clippy exit 0 plus the 24-test filtered suite green twice locally (exit 0,
   log attached); full core/app-server suites run on hosted CI after handoff per the current producer brief.
3. Reviewer tests kept: all 20 prior test names present under original names (verified by inventory); 4 added.
4. Out-of-contract rows: none within the surface row; tool/mailbox/transport/process-manager/model-wake inputs are
   out of contract per Description and Scope (table above).
5. Rework diff bounded: only the 3 leaf paths differ; the rework touches only the test file.

## Outcome-scoped logbook and next step

- Rev6 is tests-only rework of the repeated late-initial-response refusal class; this run changed no product bytes, and the product SHA-256 matches the HOLD-BUILD inventory (which records it byte-identical to rev5).
- Full branch sweep records every public error/transition path and names the RNG/invariant defensive bounds rather
  than introducing mocks into product code.
- No direct control-root writes. This report is written outside the managed worktree and attached via the resource
  API; the candidate stays uncommitted for the handoff snapshot.
- Next: hosted relux-ci executes the 24 completion_receipt tests on the exact candidate tree; any failure returns
  as a rework with the job log.
