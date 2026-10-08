# Panel B verdict — TASK-260929-2snjbb CR rev 3 (R141, non-recording)

Verdict: accept

## Replay tree check

Base 812b8037a8a62bac3ce80f7035c9d9142ffea75b + patch
TASK-260929-2snjbb_change-request_rev3.patch through a temporary index gives
write-tree 16a538869452dc36d083b8ab3c3e63a1e57c7285 — matches the expected
candidate tree exactly. No mismatch; review proceeded.

## Commands with exit codes

- task-board resource get (rev3 patch) — exit 0
- GIT_INDEX_FILE=... git read-tree 812b8037... — exit 0
- GIT_INDEX_FILE=... git apply --cached rev3 patch — exit 0
- GIT_INDEX_FILE=... git write-tree → 16a538869452dc36d083b8ab3c3e63a1e57c7285 — exit 0
- git archive 16a5388... (candidate files) + tar -x — exit 0
- python3 /tmp/TASK-261007-1c6vam-static-attack.py — exit 0, 13/13 probes passed
- git diff --stat 3e27108(rev2) 16a5388(rev3) — exit 0 (7 files, +559/-38)
- git grep/show reads on the candidate tree — exit 0 throughout
- No cargo, just, build or test executed (forbidden for this panel; shared
  target serialized). Execution evidence is the attached CR rev3 validation
  log (local fast lane) and hosted precheck 4 on the exact candidate tree.

## Row sweep summary

- gate scope and fairness: held. Scope gate is Automatic + goal only; re-read
  failure waits on both admission paths; inactive/disabled bypass. Hosted
  kills: overgate_non_goal_triggers (37550876321), treat_read_error_as_empty
  (37550965847), gate_only_queued_ignoring_armed (37550823483).
- check-in tickets and warning: held. Fired timers detach id-gated before the
  callback; stale installs rejected by generation guard; permit held only
  across the synchronous install; real-timer paused-time scheduled regression
  present. Hosted kills: keep_handle_in_slot_while_firing (37550841452),
  unconditional_slot_replace (37550984504), drop_timer_spawn (37550804014),
  reuse_ticket_id (37550931976), warning_repeats (37551004329),
  reset_epoch_on_turn_start (37550913595), drop_check_in_registration
  (37550786061). Ticket single-use, warning-once exact text, 30/60/120 cap 3
  all statically confirmed.
- admission recheck and invalidation: held. Late revision recheck immediately
  before start_task with clean abandon; core production-latch test arms
  between early admission and start. Hosted kills: no_late_recheck
  (37550859181), skip_revision_recheck (37550948899),
  preserve_ticket_across_invalidation (37550895448).

All five round-2 findings are confirmed fixed in source with killing
regressions; nothing carried forward. No new finding. See notes for retained
unexecuted bounds.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "execution-bound",
      "text": "Read-only replay plus static probes only. Ran no cargo, just, builds, Rust tests, or new hosted mutants. Hosted precheck 4 (snapshot c7652275, run 37550767559, four lanes success, 13/13 mutants killed, 0 survivors) is accepted as attached execution evidence on the exact replayed tree, not rerun or independently fetched. Local CR rev3 validation log (64 KiB truncated) shows fast-lane green: fmt-check exit 0, clippy, 267 small tests exit 0."
    },
    {
      "id": "round2-closure",
      "text": "All five round-2 findings verified fixed in the exact candidate: timer-aborts-own-admission and fired-timer-aborted-before-admission-reply by id-gated detach before on_fire (check_in_clock.rs fire path, probe P1); stale-timer-install-clobbers-current-registration by the generation guard plus permit-held synchronous install (probes P2, P7, P12); revision-recheck-before-await-window by the late recheck immediately before start_task with clean abandon (probes P3, P3b); scheduled-checkin-regression-not-exercised by the real-timer start_paused scheduled test driving claim→evaluate→admit→re-arm with time advance alone (probe P8). Each has a hosted killed narrowing mutant. No repeat-of carried forward."
    },
    {
      "id": "snapshot-coherence-bound",
      "text": "Retained unexecuted bound from rev1/rev2: try_read_snapshot reads the receipt store and mailbox under separate locks and loads revision last (pending_work.rs). A transition landing inside that read window could pair a pre-transition content view with a post-transition revision. No live reproduction exists and none was executed here; both admission checks would have to straddle transitions in the same direction for a wrong Allow. Not a finding."
    },
    {
      "id": "post-late-recheck-window",
      "text": "Unexecuted bound, not a finding: the late recheck sits at the last point before start_task exactly as rework-brief fix C scoped it, but start_task itself awaits (locks, plugin selection, lifecycle emit) without serializing against receipt transitions, which use their own mutex and atomic revision. A receipt arming inside start_task would not be caught; consequence is one goal turn starting despite just-armed work (the completion stays queued, no loss or starvation). Closing it needs shared commit locking beyond this leaf. Wanted test if pursued: latch inside start_task claim, arm a receipt, assert NotSubmitted; hosted lane required, not run."
    },
    {
      "id": "release-and-activation-bounds",
      "text": "note_release still has no production caller in the candidate (definition plus unit tests only); release controls arrive in stage 2e. Policy remains disabled by default; no missing-activation finding. State empty-reassessment tests plus core release/cancellation admission tests cover AC8 at this stage but do not prove a production late-completion or release event wakes the runtime."
    },
    {
      "id": "size-api-context",
      "text": "rev2→rev3 delta is exactly 7 files, +559/-38, all inside the E2 scheduler plus admission modules. No new model-visible fragment (admission checker is a sync Allow/Wait closure, no text injection). No wire, config, CLI, schema, or rollout change in rev3; no breaking change established. Full base replay includes checkpointed E1 prerequisites (28 files)."
    }
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Static scope gate Automatic+goal only (P5, P11); re-read failure waits on both paths (P3b); inactive/disabled bypass. Hosted exact-tree kills: overgate_non_goal_triggers 37550876321 by both core fairness tests, treat_read_error_as_empty 37550965847, gate_only_queued_ignoring_armed 37550823483. Local fast lane green."
    },
    {
      "row": "check-in tickets and warning",
      "result": "held",
      "evidence": "Id-gated detach before callback (P1); generation guard plus permit-held sync install (P2, P7, P12); real-timer start_paused scheduled regression (P8); ticket single-use (P4); warning-once exact text (P6, P9); 30/60/120 cap 3 (P10). Hosted kills: keep_handle_in_slot_while_firing 37550841452, unconditional_slot_replace 37550984504, drop_timer_spawn 37550804014, reuse_ticket_id 37550931976, warning_repeats 37551004329, reset_epoch_on_turn_start 37550913595, drop_check_in_registration 37550786061."
    },
    {
      "row": "admission recheck and invalidation",
      "result": "held",
      "evidence": "Late revision recheck immediately before start_task with clean abandon (P3); re-read failure safe (P3b); core production latch test receipt_armed_after_admission_blocks_automatic_start arms after early Allow. Hosted kills: no_late_recheck 37550859181, skip_revision_recheck 37550948899, preserve_ticket_across_invalidation 37550895448. All 8 invalidation events unit-covered incl. armed-cancel."
    }
  ],
  "free_hunt": [
    "Bounded static hunt after the surface sweep (no builds): timer abort/detach orderings, stale-install interleavings, snapshot coherence, post-late-recheck window inside start_task awaits, release callers, permit/delay separation, warning/count/epoch state machine, rev2→rev3 delta scope, context/wire/config surface. No additional blocking mechanism found. Residual items recorded as notes (snapshot-coherence-bound, post-late-recheck-window, release-and-activation-bounds), each with the wanted test named and none executed."
  ]
}
```
