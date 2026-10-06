# TASK-260929-csnn3a (D2 CR rev2) results — f1-regressions-and-failure-paths

Handoff on hosted precheck 3. Worktree `task-board/story/STORY-260929-3bvsxx`
on `bc00d9b301`, candidate UNCOMMITTED: 9 files, +1024/-17, temp-index tree
`f0cf63cd9fc511340d23e680f43e846403157f62` verified unchanged this run
(exit 0, §8). No file changed this run. Rev2 delta over the precheck-2 tree
(`3e3f7357`): 4 files, +223/-0, all inside D's scope.

## 1. R141-A-1 answer (row "F1a cleared reservation")

Review round 1 (`TASK-260929-csnn3a_review-verdict-rev1.md`,
changes_requested) held F1b and compaction/guardian/transport, and broke F1a
with one finding, R141-A-1 (severity robustness, repeat-of none): after a
reserved-start back-off, taken-but-unattached leases were failed back with no
wake, so a winner that already finished could leave an idle session with an
unleased pending receipt and no future scheduler pass.

Production fix (`codex-rs/core/src/tasks/mod.rs`, back-off branch of
`maybe_start_turn_for_pending_work_with_sub_id`): after `fail_leases`
(:642), when leases were taken, run one
`maybe_start_turn_for_pending_work` pass (:643-652). No double-wake: a live
winner holds an active turn so the pass returns early and its own teardown
wakes later. No spin: suspended entries no longer count as pending so the
pass returns at the idle gate. Leaseless back-offs skip the pass. Kept from
rev1: `TurnStartClaim` reserve/back-off in `start_task` (:279-310, :342),
which claims only the waker's own reservation and fails taken-but-unattached
leases back instead of stranding them.

Regression test `exec_completion_lost_reservation_after_winner_idle_rewakes`
(public entry, latches, no sleeps): a `TestWakeLeaseGate` pauses wake W after
leasing and before attaching; winner user turn U starts, finishes, and its
teardown scheduler pass — latched via the gate — skips the still-leased entry
(`(false, true)` asserted before and after); after disarm and release, W backs
off, fails back, and re-wakes. Asserted: 2 requests (winner 0 frags, re-wake 1
frag), history 1, mailbox `(false, false)`, silence after settle.

Narrowing mutant `backoff_skips_post_failback_rewake` (fail-back kept,
re-wake block removed): killed by the new test only, hosted run 37441638357
(core lane fails, §2). Kept: `reserved_start_*` unit tests and all D1/D2
suite tests under original names (§7).

Rework diff bounded: rev2 touches 4 files, all inside the brief's D scope
(sampling acknowledgment / F1 races): `tasks/mod.rs` (+35, fix),
`codex_thread.rs` (+91, test-only gate hooks, no-ops unless armed), `lib.rs`
(+2, re-export), `core/tests/suite/exec_completion.rs` (+95, new test).
Nothing outside D's scope.

## 2. Hosted precheck 3 verdict on this exact tree

Snapshot commit 53c4e843, run 37441567186: lanes
`{'small': 'success', 'app-server': 'success', 'core': 'success', 'lint':
'success'}`. All green. Precheck 1 had a red base so its mutant results are
void; precheck 3 re-ran everything on tree `f0cf63cd`.

Mutants: 9 total, 9 killed, 0 survivors.

| Mutant | Run | What it narrows the gate to | Named test(s) that fail |
|---|---|---|---|
| `retain_only_task_present` | 37441786360 | inject admits task-present input only | `exec_completion_survives_cleared_idle_reservation` |
| `acknowledge_on_recording` | 37441615109 | recording into history counts as sampling | `exec_completion_finishing_task_gets_sampling_wake`, `aborted_submission_retries_and_samples_once`, `exec_completion_sampling_ack` |
| `fail_first_tracked_only` | 37441688497 | fail-back covers exactly one tracked lease | `exec_completion_finishing_task_gets_sampling_wake` |
| `compact_acks_staged` | 37441663087 | compact acknowledges staged leases | `exec_completion_compaction_omission_keeps_receipt_pending` |
| `guardian_prep_drops_exec_fragments` | 37441714373 | guardian prompt prep drops exec fragments | `exec_completion_guardian_prompt_preserves_receipt` |
| `ack_skipped_when_websockets_enabled` | 37441591474 | ack follows transport config, not submission proof | `exec_completion_sampling_ack`, `http_fallback_submission_acknowledges`, `websocket_submission_acknowledges` |
| `reserved_claim_ignores_identity` | 37441739252 | Reserved claim checks vacancy, not turn identity | `tasks::tests::reserved_start_backs_off_when_turn_replaced` |
| `reserved_claim_ignores_task` | 37441762646 | Reserved claim checks identity, not vacancy | `tasks::tests::reserved_start_backs_off_when_turn_busy` |
| `backoff_skips_post_failback_rewake` | 37441638357 | back-off fails leases back but schedules no wake | `exec_completion_lost_reservation_after_winner_idle_rewakes` (only) |

Every mutant preserves the gate and weakens exactly one class member; no
delete-only mutant; no survivors so no survival bounds to state.

## 3. AC coverage map (6 of 6 AC rows driven)

Every row driven through the production entry point (`test_codex` +
`Op`/public `CodexThread` API + mock sampling requests).

| AC | Driving test(s) | Production call site(s) | Refusal / narrowing mutant (killing test) |
|---|---|---|---|
| AC1 F1a passes; fails under retain-only-task-present | `exec_completion_survives_cleared_idle_reservation`; `exec_completion_lost_reservation_after_winner_idle_rewakes` | `CodexThread::inject_if_running` → `Session::inject_if_running` (`inject.rs:17`); drop mirrors `clear_reserved_idle_turn` (`turn_input.rs:615`); wake `maybe_start_turn_for_pending_work` (`tasks/mod.rs:496`) → `acknowledge_submitted` (`turn.rs`); back-off re-wake (`tasks/mod.rs:643-652`) | `retain_only_task_present` → F1a test (37441786360); `backoff_skips_post_failback_rewake` → new test only (37441638357) |
| AC2 F1b passes; fails under acknowledge-on-recording | `exec_completion_finishing_task_gets_sampling_wake` | `record_pending_input` → `note_recorded` (`hook_runtime.rs`); `fail_unsubmitted` (`tasks/mod.rs`); retry `maybe_start_turn_for_pending_work`; `acknowledge_submitted` (`turn.rs`) | `acknowledge_on_recording`, `fail_first_tracked_only` → this test (37441615109, 37441688497) |
| AC3 compaction omission → pending → later sampled | `exec_completion_compaction_omission_keeps_receipt_pending` | `compact` (`handlers.rs`); local `run_compact_task` (`compact.rs`); wake path as AC1 | `compact_acks_staged` → no post-compact wake (37441663087) |
| AC3 guardian omission → pending → later sampled | `exec_completion_guardian_prompt_preserves_receipt` + stated bound with base citations (§5.1) | `prepare_prompt` (`guardian/request_budget.rs:67`); `finalize_guardian_input` (`guardian/input_budget.rs`, via `guardian/mod.rs:14`); review scoping (`review_session.rs`) | `guardian_prep_drops_exec_fragments` → wake never samples (37441714373) |
| AC4 transport failure → pending; bounded retries; visible suspension | `exec_completion_sampling_ack`; kept `persistent_failures_suspend_visibly_without_spin` | `fail_leases` (`exec_completion_ack.rs`); suspend `RuntimeMailbox::fail` + warning | `ack_skipped_when_websockets_enabled` → retry never acks (37441591474) |
| AC5 fallback acks only the submitting transport | `exec_completion_sampling_ack` (426 handshake asserted) | WS→HTTP fallback on 426 (`client.rs`); `acknowledge_submitted` (`exec_completion_ack.rs`) | Same `ack_skipped_when_websockets_enabled` (37441591474) |
| AC6 no history duplicates across retries | history-count asserts in all suite tests + `items_contain_lease` skip (`hook_runtime.rs`) | record dedup path | `fail_first_tracked_only` + `acknowledge_on_recording` |

## 4. Surface-table coverage map (3 of 3 rows)

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| F1a cleared reservation | `exec_completion_survives_cleared_idle_reservation`; `exec_completion_lost_reservation_after_winner_idle_rewakes`; `tasks::tests::reserved_start_*` (4) | `retain_only_task_present`; `reserved_claim_ignores_identity`; `reserved_claim_ignores_task`; `backoff_skips_post_failback_rewake` → new test only | reservation-scoped injected input dropped with the reservation → AC1 names only retained runtime mail (pre-existing `clear_reserved_idle_turn`, outside D scope) |
| F1b finishing task | `exec_completion_finishing_task_gets_sampling_wake` | `acknowledge_on_recording`; `fail_first_tracked_only` → this test | F1b literal leftover → AC2's named behavior fully driven; leftover needs a transient pre-loop error and is unreachable deterministically (stated bound) |
| compaction, guardian and transport | `exec_completion_compaction_omission_keeps_receipt_pending`; `exec_completion_guardian_prompt_preserves_receipt`; `exec_completion_sampling_ack` | `compact_acks_staged`; `guardian_prep_drops_exec_fragments`; `ack_skipped_when_websockets_enabled` | guardian-omission letter → AC3 stated bound with base citations (§5.1); exit-before-arm, stdin, capacity, burst, owner/host → task-brief out-of-scope (story E/F) |

## 5. Stated bounds (not silence)

1. AC3-guardian letter ("omitted, later sampled") is structurally impossible
   at this base: guardian prompt prep only extends the prompt
   (`guardian/request_budget.rs:67` `prepare_prompt`), finalize rejects
   non-UserInput turns (`guardian/input_budget.rs` `finalize`, re-exported at
   `guardian/mod.rs:14`), and review context is session-scoped
   (`review_session.rs`). Covered by the preservation test (which the
   `guardian_prep_drops_exec_fragments` mutant kills, 37441714373) plus this
   bound. The panels accepted this shape in round 1.
2. F1b literal leftover-at-finish interleaving needs a transient pre-loop
   error and is unreachable deterministically; history-is-not-ack and
   two-lease retry are driven.
3. Reservation-scoped injected input dropped with the reservation is outside
   AC1 (only retained runtime mail is named).
4. Inter-agent mail drained by a losing wake is not failed back
   (pre-existing; only exec leases fail back). Outside D scope.
5. Checklist item 8 (token-preserving source-text mutant) is vacuous: no gate
   in the production diff inspects source text (only gate is
   `TurnStartClaim` identity/vacancy checks; prompt-membership ack is D1 scope
   with kept marker/role mutants).
6. The new mutant kill is liveness-based (missing wake → event timeout); the
   pass path is fast and latch-driven.

## 6. Out-of-contract rows

None inside the brief beyond §4's map column. Exit-before-arm, stdin,
capacity, burst and owner/host races are excluded per the task description
(story E/F). D1's committed tests kept untouched and green (full lanes in
precheck 3, §2). Reviewer tests kept under original names (§7).

## 7. Reviewer tests kept

Every previously committed reviewer test is present under its original name
and green in precheck 3's core lane: kept D1 suite tests including
`aborted_submission_retries_and_samples_once`,
`http_fallback_submission_acknowledges`,
`websocket_submission_acknowledges`,
`persistent_failures_suspend_visibly_without_spin`, and the
`reserved_start_*` unit tests; D2 suite tests added in rev1 kept untouched.
No test was renamed, deleted, or narrowed.

## 8. Validation (this run)

- Temp-index tree: `f0cf63cd9fc511340d23e680f43e846403157f62` (exit 0;
  `git read-tree HEAD`, `git add -A`, `git write-tree` on a temp index).
  `git diff --stat`: 9 files, +1024/-17. No file changed.
- Busy check `codex-fix-suite-busy.py --any` and `task-board handoff` run
  after this attachment per d2-handoff-note-3; outcomes recorded in the board
  note, not replayed here.
- NOT run locally this run: no builds, no `just`/`cargo` commands (handoff
  note forbids file changes); full core/app-server lanes and all 9 mutant
  kills come from hosted precheck 3 on this exact tree per the
  producer-brief ban (snapshot 53c4e843, run 37441567186). No R205 load
  generators; no attached busy workers.
