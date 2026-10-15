# Panel B verdict — CR-TASK-260929-csyzcj-1 rev1 (R141, non-recording)

Task: TASK-261014-uvs95n reviewing TASK-260929-csyzcj. This panel is not the
recording reviewer: nothing was written on TASK-260929-csyzcj (only read-only
q queries and resource get calls there; no accept, reject, status, handoff,
note, checklist, or resource write).

Verdict: accept

## Replay tree check

Base commit 99533cf034007f30e2c49916bcba411d7ffa282d plus patch resource
TASK-260929-csyzcj_change-request_rev1.patch through a temporary index gives
write-tree 0b9a8f04e991fd685a0d43a0b3f8a4cc11ddf148, which matches the expected
candidate tree exactly. No nested worktree was created. Candidate files were
read via git show and git archive of that tree.

## Commands run by this panel, with exit codes

- task-board m 'set_status(TASK-261014-uvs95n, status=analysis)' — exit 0
- task-board q reads on TASK-260929-csyzcj (description/scope/ac, outcome and
  precondition resource lists, review) — exit 0 each, after two exploratory
  failures: q 'resources(...)' exit 1 (unknown operation) and
  get(...) { resources } exit 1 (unknown field); both corrected via schema()
  to the outcomeResources projection. Neither was a validation gate.
- task-board resource get (surface-table.md, producer-brief.md,
  TASK-260929-csyzcj_results.md, TASK-260929-csyzcj_mutants.json,
  TASK-260929-csyzcj_change-request_rev1.patch,
  TASK-260929-csyzcj_change-request_rev1-validation.log,
  TASK-260929-csyzcj_hosted-precheck-19.md, g1-handoff-note-19.md,
  TASK-260929-csyzcj_precheck19-mutant-evidence.json,
  TASK-260929-csyzcj_review-verdict-rev1.md for verdict-shape reference) —
  exit 0 each
- GIT_INDEX_FILE=replay.idx git read-tree <base> — exit 0
- GIT_INDEX_FILE=replay.idx git apply --cached <rev1 patch> — exit 0
- GIT_INDEX_FILE=replay.idx git write-tree — exit 0, printed
  0b9a8f04e991fd685a0d43a0b3f8a4cc11ddf148 (exact match)
- git archive 0b9a8f04... <changed paths> | tar -x (candidate extract) — exit 0
- Read-only git show / git grep / git diff-tree inspection — exit 0
- No cargo, just, build, test, or mutant execution was run locally: forbidden
  (serialized shared build target). Execution evidence is hosted relux-ci on
  the exact candidate tree (below) plus static attack.

## Execution evidence identity (exact tree)

Hosted precheck 19, snapshot b6f695ec (ci/TASK-260929-csyzcj/wip-19),
relux-ci run 38476605332 on tree
0b9a8f04e991fd685a0d43a0b3f8a4cc11ddf148: lint, snapshot small, snapshot core,
and snapshot app-server lanes all succeeded. 15 of 15 narrowing mutants were
killed, each with named failing tests and exit code 100 (expected-red mutant
lanes, verified in TASK-260929-csyzcj_precheck19-mutant-evidence.json).

The local rev1 validation log is truncated mid-file by task-board (64 KiB cap,
BUG-260917-38ob0v; the file carries a "... validation log truncated; 57529
bytes omitted ..." marker between the clippy output and the small-crate test
tail). Visible head: target guard exit 0, just fmt-check exit 0, clippy start.
Visible tail: 346 of 346 small-crate tests passed, exit 0. It is treated as
partial evidence; the hosted lint and small lanes ran the same commands on the
same tree.

## Sweep summary

7 of 7 surface rows held, 0 blocking findings, 10 notes. Every row has at
least one attack executed through a production entry point on the exact
candidate tree that did not reproduce, plus a static attack on the mechanism.
Residual bounds (release wiring, disable/stop, check-in reinsertion,
exhausted late wake, reminder-enabled schedule, second-child-mid-turn,
non-default inherited settings) are disclosed in notes with named wanted
tests; each is a composition of held paths, verified by code reading.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Prior rev1 blocking finding interrupted-fragment-outside-context is CLOSED in this tree: the INTERRUPTED notice is now typed InterAgentInterruptedMessage in codex-rs/core/src/context/inter_agent_interrupted_message.rs implementing ContextualUserFragment (content_kind multi_agent.inter_agent_interrupted_message, assistant role, sibling markers), rendered through .render() by session_prefix.rs, with real Op::Interrupt integration tests and a compile-time 838-byte whole-item bound. Verified by reading; not re-reported as a finding.",
    "release_native_wait advisory (same class as prior panel-B PANELB-1): GoalRuntimeHandle::release_native_wait (codex-rs/ext/goal/src/runtime.rs:178) has no production caller; the only invocation in the candidate tree is suite goal_wait_removed_on_clear_release_and_resume. Its callees match base behavior: BackgroundWaitState::note_release had zero production callers on the base tree too, so no production release event exists for any wait type. The mechanism (epoch reset plus conditional owned-id remove) is implemented and executed by that test. Wanted: wire a production release trigger or keep the API-level contract; not blocking.",
    "Old-clear-vs-new-goal marker-steal interleaving (unexecuted suspicion, same class as prior panel-A lifecycle-concurrency note): apply_external_goal_clear and the apply_external_goal_set terminal arms drop the goal permit before awaiting remove_native_wait_marker, and removal matches any goal-wait id by prefix rather than the cleared generation. A concurrent set that registers a new marker inside that microsecond get_thread await window could have it removed. Window verified tiny (in-memory lock), outcome self-heals at the next idle or check-in turn (mail drains then), and no deterministic reproduction exists without a new test hook, so this stays a note. Wanted test: gate remove_native_wait_marker between permit-drop and remove, set a new goal plus Running child, release, assert the new marker survives.",
    "Inspection errors fail open in the safe direction: continue_if_idle returns Err on inspection failure, leaving any pre-existing marker in place (late mail can still wake) and logging a warning, with retry at the next idle. Verified by reading runtime.rs:725-745. Not a finding.",
    "The per-child generic InspectionFailed arm in inspect_owned_child_ids is currently unreachable defensive code: ThreadManagerState::get_thread fails only with ThreadNotFound (in-memory map). Reachable error arms (UnknownChild, SessionUnavailable, open-children failure) all propagate as Err. The skip_failed_lookups mutant is killed via its first hunk. Not a finding.",
    "Legacy over-cap parents cannot mint new children: join_new bounds the resulting total length, so a resumed parent already past MAX_PATH_BYTES gets a clear tool error on spawn. Documented in agent_path.rs (identities are rejected, never silently truncated). No AC requires legacy-deep spawn; out of contract. Not a finding.",
    "Residual bounds accepted as stated risk (all disclosed in the producer results map, each a composition of held paths verified by reading): no dedicated disable/stop removal integration; no full live-child check-in remove-then-reinsert cycle; no exhausted-check-ins late-wake integration; no reminder-enabled schedule assertion; no dedicated second-child-mid-turn integration; no non-default inherited-settings assertion. Wanted tests: plant-then-disable/stop asserting removal; paused-clock check-in cycle asserting remove then reinsert with a live Running child; exhausted-wait late-completion wake; reminder-enabled insert asserting an unchanged schedule; mid-turn second spawn observed at next idle; wake-turn options equality with non-default parent options.",
    "Local rev1 validation log is truncated mid-file (see header); treated as partial per the reviewer contract, with hosted lint/small lanes on the same tree as substitute evidence. The 15 mutant kills and 4 green lanes are cited from hosted precheck 19 run 38476605332, not from the local log.",
    "Candidate size is 34 files, 3151 insertions, 22 deletions; growth is test-heavy (1468-line goal_native_wait.rs suite). No BUILD.bazel or MODULE.bazel.lock change is needed: ext/goal BUILD uses the codex_rust_crate macro with Cargo-derived deps, the only manifest edge is workspace-internal codex-extension-items, and no include_str-style reads were added.",
    "Read-only review of TASK-260929-csyzcj: this panel used only q queries and resource get there. No accept_cr, reject_cr, withdraw_cr, set_status, handoff, note, checklist, or resource write was issued on TASK-260929-csyzcj. No cargo/just/build/test ran locally."
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "Hosted run 38476605332 on tree 0b9a8f04: suite::goal_native_wait::goal_wait_registers_marker_and_wakes_on_child_completion drives real V2 spawn, set_thread_goal, production idle, marker insert, child sleep completion, and asserts a real outbound parent wake model request carrying completion text (not marker presence), pre-wake event silence, and marker absence after the admitted wake turn. Narrowing mutant ignore_native_pending killed by this test plus 6 others (exit 100). Static: insert_if single-slot storage makes double registration structural-impossible; enqueue-then-check vs insert-then-recheck closes wake-without-marker (completion notices are trigger_turn=false, so the marker is the only wake grant).",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-19.md",
      "reported_by": "TASK-261014-uvs95n"
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Hosted run 38476605332: agent::control::tests::owned_children_inspection_propagates_failed_lookups drives a real thread manager plus registry (loaded child inspects; unknown id returns UnknownChild, never skipped; removed-but-known child reports Unloaded) and kills narrowing mutant skip_failed_lookups (exit 100). suite ordinary-parent-quiet and pacing-without-gate tests assert no marker without a goal and without the background gate despite a Running child; pending_native_work_is_only_pending_init_and_running pins the predicate over every status. Static: every inspection error arm returns Err and continue_if_idle propagates with no marker; unknown identities error instead of reading as Running.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-19.md",
      "reported_by": "TASK-261014-uvs95n"
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Hosted run 38476605332: suite::goal_native_wait::goal_wait_latch_closes_completion_before_registration pauses registration between Running-observed and insert with the production gate, confirms completion mail enqueued via test_has_pending_mailbox_mail, releases, and asserts the post-insert recheck consumes the mail and starts a mail-wake turn (no steering text, no marked continuations, slow child still pending, every wait bounded 10-15s with latch-specific messages). It kills narrowing mutant insert_after_mail_check (exit 100). Static: insert-before-recheck plus enqueue-before-marker-check is a sound two-flag latch; the goal semaphore is held across the window and the recheck shares the permit with on_turn_start (no self-deadlock).",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-19.md",
      "reported_by": "TASK-261014-uvs95n"
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "Hosted run 38476605332: suite::goal_native_wait::goal_wait_preserves_foreign_sleep_across_register_and_turn_start plants clock-wait-1, drives production spawn plus idle plus wake turn, and asserts the foreign item byte-identical and the owned marker absent throughout; units register_never_clobbers_foreign_sleep, register_refreshes_stale_own_generation, and conditional_remove_only_removes_owned_id pin insert and remove. Narrowing mutants insert_clobbers_one_foreign and unconditional_remove killed (exit 100 each). Static: insert_if and remove_if predicate plus mutate atomically under the entries mutex; ownership is by goal-wait prefix; goal wait is the sole production SleepItem writer (clock/sleep stores no extension marker), so clobbering in either direction is covered.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-19.md",
      "reported_by": "TASK-261014-uvs95n"
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "evidence": "Hosted run 38476605332: latch and dense-path integrations assert owned-marker absence right after TurnStarted through the production on_turn_start path; goal_wait_removed_on_clear_release_and_resume drives GoalService::clear_thread_goal and GoalService::restore_thread_runtime_after_resume production paths to removal; native_wait check-in and exhaustion units pin Wait, ticket admission, and Wait-without-deadline; narrowing mutant owned_generation_seven_not_removed killed by the conditional-remove unit (exit 100). Static: audited every persisted-status writer (set/clear/status tool, stop_active_goal success, set_enabled(false), stop, resume, all continue_if_idle early returns) — all remove the owned id; remaining clear_active_goal sites are accounting-only in turn context where the marker is already absent. Resume removes unconditionally before the enabled check; fork and spawn seed fresh extension data so no marker is cloned.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-19.md",
      "reported_by": "TASK-261014-uvs95n"
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "Hosted run 38476605332: the registers-marker integration asserts 500ms of zero parent events after the insert and a wake body containing neither goal-wait: nor current_time; narrowing mutant single_child_registration_records_history (history injection on single-child registration) is killed by it (exit 100). Static: registration is a pure ExtensionData map write — no event emission, history write, or scheduler call exists on the insert path — and the goal scheduler owns timers and warnings separately. Reminder-enabled schedule has no dedicated assertion (disclosed bound); the passive-storage mechanism cannot alter it.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-19.md",
      "reported_by": "TASK-261014-uvs95n"
    },
    {
      "row": "child state transitions",
      "result": "held",
      "evidence": "Hosted run 38476605332: suite::goal_wait_registered_parent_gets_single_interrupted_notice drives real Op::Interrupt on a Running V2 child and asserts exactly one INTERRUPTED agent_message in one wake request (agent_message-scoped), no FINAL_ANSWER and no success claim, spawn-path envelope identities, and child status Interrupted; the ordinary-parent negative asserts no enqueued notice and no wake; the dense-path integration asserts exactly one notice and exactly 838 model-visible bytes on the real wake request. Narrowing mutants interrupted_claims_success, interrupted_notice_delivered_twice, interrupted_sender_path_uncapped, interrupted_body_path_cap_256, envelope_author_display_uncapped, spawn_task_name_length_unchecked, legacy_paths_rejected_by_shared_parser, and legacy_long_path_rejected_by_shared_parser all killed (exit 100). Static: is_final is byte-untouched and pinned non-final for Interrupted; completion.rs gates notices on the parent holding the owned marker and sends trigger_turn=false; turn_finished routes only the notification; the 838 bound (142 fixed plus 2x78 body plus 2x270 envelope) was recomputed independently and matches the compile-time assert.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-19.md",
      "reported_by": "TASK-261014-uvs95n"
    }
  ],
  "free_hunt": [
    "{\"probe\": \"permit-share soundness of the post-insert recheck block\", \"result\": \"no-finding\", \"evidence\": \"Only two GoalTurnStartPermit inserters exist (recheck block and goal-continuation path, sequential in continue_if_idle, each lease-guarded); on_turn_start consumes via remove; the lease Drop removes leftovers. Goal semaphore serializes concurrent continue_if_idle. No stale permit outlives the critical section.\"}",
    "{\"probe\": \"old-clear-vs-new-goal marker steal\", \"result\": \"suspicion-kept-as-note\", \"evidence\": \"Permit is dropped before the async remove and removal is prefix-wide, so a concurrent set racing the microsecond get_thread window could lose its marker; self-heals at next idle or check-in. No deterministic reproduction without a new hook; named wanted test in notes.\"}",
    "{\"probe\": \"fork, spawn, and resume marker revival\", \"result\": \"no-finding\", \"evidence\": \"fork_thread_with_source and subagent spawn seed fresh ExtensionDataInit (capability roots only); live ExtensionData is never cloned. restore_after_resume removes unconditionally before the enabled check. No history-to-extension SleepItem rehydration path exists.\"}",
    "{\"probe\": \"foreign-overwrites-goal direction\", \"result\": \"no-finding\", \"evidence\": \"clock/sleep handler emits only a TurnItem and never stores an extension SleepItem; goal wait is the sole production writer of extension SleepItems, and insert_if/remove_if ownership semantics are pinned by unit plus integration tests against narrowing mutants.\"}",
    "{\"probe\": \"interrupted 838-byte bound arithmetic\", \"result\": \"verified\", \"evidence\": \"Independently recomputed: fixed prose 37+9+96=142, marker 14 bytes, body 142+2x(64+14)=298, item 298+2x(256+14)=838 <= 1000. Matches the compile-time assert, the dense unit test (exactly 838 both fixtures), and the dense-path integration on the real wake request.\"}",
    "{\"probe\": \"turn_finished side effects for Interrupted\", \"result\": \"no-finding\", \"evidence\": \"LocalAgentControl::turn_finished delegates solely to notify_parent_of_terminal_turn; Interrupted returns early for ordinary parents (no mail, verified by the quiet test asserting empty mailbox plus 1s event silence) and sends trigger_turn=false for registered waits.\"}",
    "{\"probe\": \"double TurnAborted duplicate notice\", \"result\": \"no-finding\", \"evidence\": \"Interrupted arises only from TurnAborted(Interrupted|BudgetLimited); the registered-parent integration pins exactly one notice through the real Op::Interrupt path and the delivered-twice narrowing mutant is killed by occurrence-count assertions. No second emission path found in session/mod.rs routing.\"}",
    "{\"probe\": \"goal-status writer audit for stale markers\", \"result\": \"no-finding\", \"evidence\": \"All production writers (app-server set/clear via apply_runtime_effects, model update_goal tool in turn context, stop_active_goal success, set_enabled, stop, resume) either remove the owned id or run where the marker is already absent (turn-start removal). Tool handle_update needs no removal: any turn start removed the marker first and idle re-entry re-evaluates.\"}",
    "{\"probe\": \"Bazel and manifest drift\", \"result\": \"no-finding\", \"evidence\": \"34 files, 3151 insertions, 22 deletions, test-heavy. ext/goal BUILD.bazel uses the codex_rust_crate macro with Cargo-derived deps; the only manifest edge is workspace-internal codex-extension-items in Cargo.toml/Cargo.lock; no new external crate and no build-time file reads, so no MODULE.bazel.lock or BUILD edit is required.\"}"
  ]
}
```
