# Panel verdict — R141 panel B, TASK-260929-2snjbb CR rev5 (non-recording)

Verdict: accept

This is the independent panel verdict of Change Request CR-TASK-260929-2snjbb-5
(revision 5) of TASK-260929-2snjbb. This panel is NOT the recording reviewer:
no accept, reject, status, or handoff write was made on TASK-260929-2snjbb,
and nothing was recorded there. No cargo, just, build, or test command was run
(brief forbids local builds; the shared target is serialized). Execution
evidence is the element CR validation log plus the attached hosted precheck 7
results on the exact candidate tree, cited below as executed public-entry
attacks. Hosted run ids are taken from the attached precondition
TASK-260929-2snjbb_hosted-precheck-7.md and accepted as exact-tree evidence;
they were not independently re-fetched, and no hosted numeric exit codes are
invented (the precheck reports lane conclusions and named killing tests).

## Replay tree check

PASS. Base 812b8037a8a62bac3ce80f7035c9d9142ffea75b plus resource
TASK-260929-2snjbb_change-request_rev5.patch through a temporary index yields
tree 13972f7d936f6280c9b0cae88749c6f5c1a56a9a, which equals the expected
candidate tree exactly. Candidate files were read via git show / git archive
of that tree; byte comparison of the archived admission files against git show
output was used where extraction was involved.

## Commands with real exit codes (this panel run)

- task-board m set_status(TASK-261007-276t8v, status=analysis) : exit 0
- task-board q get(TASK-260929-2snjbb) projections (description/scope/ac, outcomeResources, preconditionResources) : exit 0
- task-board resource get of 11 inputs (rev5 patch, surface-table.md, producer-brief.md, results.md, coverage-map.md, mutants.json, hosted-precheck-7.md, handoff-note-7.md, rework-brief-rev5.md, rev5-validation.log, verdict-rev4.md) : exit 0 each
- GIT_INDEX_FILE=temp.idx git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b : exit 0
- GIT_INDEX_FILE=temp.idx git apply --cached rev5.patch : exit 0
- GIT_INDEX_FILE=temp.idx git write-tree : printed 13972f7d936f6280c9b0cae88749c6f5c1a56a9a, exit 0
- git archive 13972f7d... of 10 admission/scheduler paths | tar -x : exit 0
- git diff c7180fab... 13972f7d... --stat and path diffs (rev4 to rev5) : exit 0
- git show / git grep reads against tree 13972f7d... (about 15 read-only inspections: locks, bumps, gates, tests, warning text, intervals) : exit 0 each
- git status --porcelain (worktree clean; scratch lives under excluded .temp/) : exit 0
- cargo / just / rustc / nextest : NOT RUN (forbidden by the panel brief)

## Row sweep summary (all 3 surface rows swept, worst-first)

Row 1 gate scope and fairness: HELD. check_goal_admission gates only
Automatic+goal (goal_admission.rs:54); every other kind/trigger returns
admitted_revision None and publishes without inner locks, so user, follow-up,
inter-agent, and trigger mail stay immediately admissible. Disabled policy and
InactiveOrBudgetLimited status return ProceedWithoutGate (background_wait.rs).
Read failure returns Wait / WaitOnReadFailure, never empty. Hosted precheck 7
on the exact tree kills overgate_non_goal_triggers (run 37578682087, both core
fairness tests), treat_read_error_as_empty (37578790835), and
gate_only_queued_ignoring_armed (37578629753). Row code is byte-identical to
rev4, which every panel held.

Row 2 check-in tickets and warning: HELD. Intervals are absolute 30/60/120 min
(CHECK_IN_DELAYS), cap 3 (MAX_CHECK_INS_PER_HUMAN_INPUT), ticket ids increment
and are consumed exactly once via outstanding+generation+last_consumed_ticket_id
under one mutex; revision must still match, so a ticket bypasses only the work
gate. Warning text is the exact AC5 string, latched by warning_emitted.
note_turn_start invalidates without moving wait_started_at (epoch anchored at
human input). Hosted precheck 7 kills all 8 row mutants (reuse_ticket_id
37578737666, warning_repeats 37578825692, reset_epoch_on_turn_start
37578719469, drop_check_in_registration 37578596335, drop_timer_spawn
37578612871, keep_handle_in_slot_while_firing 37578646983,
unconditional_slot_replace 37578808296, break_runtime_wait_arm_reentry
37578579179), including through the real-runtime suite test
scheduled_checkins_fire_through_production_runtime_under_paused_time. Row code
is byte-identical to rev4, which every panel held.

Row 3 admission recheck and invalidation: HELD. The rev4 mechanism
(revision-comparison-not-serialized-with-publication and its
revision-recheck-before-await-window repeat: cross-thread Arm between the
final comparison and the publication write) is FIXED. Rev5 compares the
admitted revision and writes last_started_turn_id while holding one shared
serialization (active_turn held by the start_task caller, Session.state, the
receipt-store std lock, the runtime-mailbox try_lock; no await between compare
and write). Static audit: every store transition bumps the shared revision
while holding lock_state; every mailbox transition bumps while holding the
mailbox mutex (methods take &mut self, reachable only through the mutex); the
revision Arc is the single one Session::new shares between InputQueue and the
receipt store; the publish closure acquires no outer lock (atomic load,
try_lock, gate flags, write to the already-held state guard), and store/mailbox
methods acquire no session lock, so the documented order
active_turn, Session.state, store, mailbox has no inversion path; inner
try_lock contention or poisoning rejects safe (never empty, never blocks),
pinned by two 5-second contention tests. Revision-only publish is sound:
content and revision are both checked at evaluate/check time, revision is
loaded last in try_read_snapshot so any transition during a read surfaces as a
revision mismatch at the next comparison, and no content mutation exists
without a bump. Hosted precheck 7 kills skip_transition_locks_in_publish
(37578773989, by the multi-thread race test order assertion plus both
contention tests), move_final_check_before_awaits (37578665024, by the race,
residual, and settings tests), skip_revision_recheck (37578755970),
preserve_ticket_across_invalidation (37578700699), and
apply_goal_settings_before_final_check (37578561576). Tickets invalidate on
all six triggers plus resume; the goal semaphore is never held across a delay
(sync lock-brief evaluation, spawn never awaits).

Prior-round disposition: the merged rev4 verdict carried 2 findings of 1
mechanism (cross-thread compare/publication race). That mechanism is closed by
the serialized publish plus the multi-thread regression
goal_publish_serialized_with_concurrent_arm and its narrowing mutant
skip_transition_locks_in_publish. No repeat-of is carried forward because no
blocking finding remains. The rev4 scheduler and settings repairs are retained
(code unchanged; their mutants re-killed on precheck 7).

Free hunt (bounded, about 15 minutes, static only, after the sweep): rev4 to
rev5 delta scope (6 files, +368/-31, admission/publication path plus tests
only); test-gate production footprint (TestGoalPublishGate inert without an
installed gate; one extension-data lookup; bounded sleeps test-only);
double-spend across concurrent starts (attempt take + outstanding/consumed
checks under one mutex); revision wrap (impractical u64); poison handling
(reject safe); effect-free rejection (no settings commit, no notification, no
reservation leak); model-visible context (none added); wire/config/CLI/rollout
surface (no change in the rev4 to rev5 delta); change size (full base replay
is 36 files +5030/-54 including E1 prerequisites; the corrective slice is the
6-file serialization). No additional blocking mechanism found. Residual items
are notes with wanted tests named where one exists; none was executed here.

```verdict-findings
{
  "findings": [],
  "notes": [
    "execution-bound: read-only review. Ran temporary-index replay, git show/archive/diff/grep reads, board get/resource-get reads, and worktree-cleanliness check only. Ran no cargo, just, build, Rust test, or new hosted mutant. Hosted precheck 7 on the exact tree (snapshot f63366db, run 37578543875, small/lint/core/app-server green, 16/16 narrowing mutants killed, 0 survivors) is accepted as attached public-entry attack evidence; its table reports lane conclusions and named killing tests, not numeric process exit codes, so none are invented. The 64 KiB-truncated local CR rev5 validation log is relied upon only for its visible head (target guard exit 0, fmt-check exit 0) and tail (small-crate 266/266 pass, exact-command-shard 4/4 green); unseen middle commands are not asserted.",
    "prior-round-disposition: merged rev4 verdict (changes_requested) carried 2 findings of 1 mechanism (cross-thread Arm between final revision comparison and last_started_turn_id publication). Rev5 closes it with the serialized compare-and-publish under the shared store+mailbox lock set, the multi-thread regression goal_publish_serialized_with_concurrent_arm, and the narrowing mutant skip_transition_locks_in_publish (killed, run 37578773989). The rev4 scheduler (real-runtime suite) and effect-free-rejection repairs are retained byte-identical and their mutants re-killed on precheck 7. No repeat-of carried forward; no blocking finding remains.",
    "coverage: surface sweep 3/3 (3 held, 0 broken, 0 not-attacked). Attached exact-tree evidence: 4/4 base lanes green, 16/16 mutants killed, 0 survivors, every row covered by at least one narrowing mutant kill. Rev4-to-rev5 delta is 6 files +368/-31 confined to the admission/publication path and tests; ext/goal, turn_input.rs, pending_work.rs, and the suite test are byte-identical to rev4.",
    "lock-order-audit: publish holds active_turn (caller) -> Session.state -> receipt-store (std try_lock) -> runtime-mailbox (tokio try_lock), no await inside. All store bumps run under lock_state; all mailbox bumps run under the mailbox mutex (&mut self reachable only through it); the revision Arc is the single Session-shared counter; the publish closure acquires no outer lock and store/mailbox methods acquire no session lock, so no inversion path exists. Contention/poison rejects safe via try_lock, pinned by goal_publish_rejects_safe_when_store_contended and goal_publish_rejects_safe_when_mailbox_contended (5 s no-deadlock bounds).",
    "snapshot-coherence-bound (safe by construction, not a finding): try_read_snapshot copies store and mailbox under separate short locks and loads revision last, so a transition during a read pairs stale content with a NEW revision, which mismatches at the next comparison and rejects. Content+revision are both enforced at evaluate/check time and revision again at the serialized publish; no content mutation exists without a bump. Wanted test if pursued: pending_snapshot_revision_matches_copied_contents; not executed here.",
    "release-and-read-failure-bounds (retained preparatory notes, not findings): note_release still has no production caller in this stage-2d candidate (definition plus unit tests only); full release/completion wake wiring arrives in stage 2e, and AC8 is covered at this stage by the release unit test plus core empty/release admission tests. A timer-fired snapshot read failure consumes the fired deadline and returns WaitOnReadFailure without re-arming; recovery waits for the next event, which matches the stated safe behavior (never treat failure as empty). Wanted tests: release_misarmed_subscription_wakes_runtime, scheduled_checkin_read_failure_rearms_after_contention; not executed here.",
    "production-observation-note (nonblocking, fix-induced retention): ext/goal/src/runtime.rs keeps a Mutex<Vec<String>> of admitted goal continuations appended on every success, also while waiting is disabled, with no cap or drain observed. No memory failure was measured or executed. Wanted regression: production_goal_continuation_observation_is_bounded; prefer existing accounting observations or a bounded/test-scoped observer.",
    "mutant-class-note (not a finding): drop_timer_spawn replaces the whole spawn body (component-wide) rather than narrowing one rejection class, so the producer all-narrowing label overstates that one entry as it did in rev3/rev4. The narrowing bound it gestures at is established by the truly narrowing keep_handle_in_slot_while_firing (37578646983), unconditional_slot_replace (37578808296), and break_runtime_wait_arm_reentry (37578579179), each killed by its paired regression. All 16 kills count for their stated component bounds; 0 survivors, so no survival bounds are owed.",
    "context-api-size: no new model-visible fragment (goal admission contributor is an internal checker; no history rewrite observed). No protocol/wire change in the rev4-to-rev5 delta; no config, CLI, schema, or rollout change observed in bounded inspection; no breaking change established. Full base-to-candidate replay is 36 files (+5030/-54) including checkpointed E1 prerequisites; the reviewable corrective slice is the 6-file serialization plus its tests.",
    "logbook (task-scoped): rev5 closes the rev4 cross-thread compare/publication race with a shared store+mailbox serialization, a multi-thread race regression, and a narrowing mutant, all observed green/killed on hosted precheck 7. No source-task mutation, status change, acceptance/rejection, or handoff was performed on TASK-260929-2snjbb. Outcome staging stayed in the allowed run worktree plus /tmp; the board write is this resource add only."
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Static: check_goal_admission (goal_admission.rs:54) gates only Automatic+goal; all other kinds/triggers return admitted_revision None and publish without inner locks. Disabled/inactive-or-budget-limited returns ProceedWithoutGate; read failure returns Wait/WaitOnReadFailure, never empty. Exact-tree hosted attacks on 13972f7d (precheck 7, run 37578543875 base green): overgate_non_goal_triggers 37578682087 killed by goal_background_wait_blocks_goal_but_admits_user_and_followup + goal_background_wait_ignores_non_goal_triggers; treat_read_error_as_empty 37578790835 killed by read_failure_never_treated_as_empty; gate_only_queued_ignoring_armed 37578629753 killed by cap/firing/epoch tests. Row code byte-identical to rev4 (all panels held). Held within these executed attacks, not a universal absence claim."
    },
    {
      "row": "check-in tickets and warning",
      "result": "held",
      "evidence": "Static: CHECK_IN_DELAYS 30/60/120 min absolute, MAX_CHECK_INS_PER_HUMAN_INPUT 3, ticket ids increment and consume exactly once (outstanding+generation+last_consumed under one mutex) with revision still enforced, so each ticket bypasses only the work gate; warning is the exact AC5 string latched by warning_emitted; note_turn_start invalidates without moving wait_started_at (epoch anchored at human input). Exact-tree hosted attacks: reuse_ticket_id 37578737666, warning_repeats 37578825692, reset_epoch_on_turn_start 37578719469, drop_check_in_registration 37578596335, drop_timer_spawn 37578612871, keep_handle_in_slot_while_firing 37578646983, unconditional_slot_replace 37578808296, break_runtime_wait_arm_reentry 37578579179, all killed, incl. through scheduled_checkins_fire_through_production_runtime_under_paused_time (real session + production timer/runtime/Core, 3 automatic turns + exact warning once). Row code byte-identical to rev4 (all panels held)."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "held",
      "evidence": "Static: publish_goal_turn_if_revision_matches (goal_admission.rs:131-167) compares the admitted revision and writes last_started_turn_id under active_turn + Session.state + receipt-store + mailbox with no await between; every revision bump runs under the store or mailbox lock on the single Session-shared counter; try_lock contention/poison rejects safe; lock-order audit finds no inversion path (store/mailbox are leaves). Regression: goal_publish_serialized_with_concurrent_arm forces a real OS-thread Arm into the compare-to-publish window and requires publication to win the shared sequence (Started, receipt pending); goal_publish_rejects_safe_when_store_contended + goal_publish_rejects_safe_when_mailbox_contended bound fail-safe. Exact-tree hosted kills: skip_transition_locks_in_publish 37578773989 (race order + both contention tests), move_final_check_before_awaits 37578665024 (race + residual + settings), skip_revision_recheck 37578755970, preserve_ticket_across_invalidation 37578700699, apply_goal_settings_before_final_check 37578561576. Residual (receipt_armed_inside_start_task), post-publish control, settings-equality, invalidation (6 triggers + resume), and no-semaphore-across-delay tests all green on base run 37578543875. The rev4 compare/publication race mechanism is closed; held within these executed attacks."
    }
  ],
  "free_hunt": [
    "Bounded static free hunt after all 3 rows were recorded held (no builds; about 15 minutes): rev4-to-rev5 delta scope and confinement; test-gate production footprint (TestGoalPublishGate inert without install; bounded test-only waits); concurrent-start double-spend (attempt take + outstanding/consumed checks under one mutex); revision wrap/poison (impractical / reject-safe); effect-free rejection ordering; snapshot coherence safety argument; release/resume/disable lifecycle callers; warning/count/epoch state machine; model-visible context and protocol/wire/config/CLI/rollout surface; producer all-narrowing label accuracy. No additional blocking mechanism found. Residual items recorded as notes (snapshot-coherence-bound, release-and-read-failure-bounds, production-observation-note, mutant-class-note), each with the wanted test named where one exists and none executed."
  ]
}
```
