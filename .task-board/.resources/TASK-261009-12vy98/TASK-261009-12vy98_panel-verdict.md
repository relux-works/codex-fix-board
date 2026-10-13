# Panel B verdict — R141 TASK-260929-csyzcj rev1 (CR-TASK-260929-csyzcj-1)

Verdict: accept

Replay tree check: PASS. Base 39c264c34e61b5171ae13b0f756746c24ea5f51a + CR patch
TASK-260929-csyzcj_change-request_rev1.patch via a temporary index yields
e8eef4f44743b4a6d256e610f91527e715ae042b, exactly the expected candidate tree.

Commands run (all read-only; exit codes real):
- GIT_INDEX_FILE=$IDX git read-tree 39c264c3... -> exit 0
- task-board resource get TASK-260929-csyzcj <10 inputs + patch> -> exit 0 each
- GIT_INDEX_FILE=$IDX git apply --cached <patch> -> exit 0
- GIT_INDEX_FILE=$IDX git write-tree -> e8eef4f44743b4a6d256e610f91527e715ae042b, exit 0
- git archive e8eef4f4... | tar -x -C .temp/TASK-261009-12vy98-cand -> exit 0
- git diff-tree --name-status base..candidate (26 paths) -> exit 0
- git diff base..candidate (per-file review) + scoped grep/sed reads -> exit 0
- No cargo/just/build/test executed locally (forbidden: serialized shared build
  target). Execution evidence cited from hosted relux-ci runs on the exact
  candidate tree: candidate 37855177143 (lint/small/core/app-server green),
  mutants 37855194303-37855282786 (6/6 killed, 0 survivors).
- Nothing written on TASK-260929-csyzcj (only q + resource get there).

```verdict-findings
{
  "findings": [
    {
      "id": "PANELB-1",
      "row": "marker lifecycle",
      "invariant": "AC5: the owned marker is removed on admitted turn start, goal inactive/clear/disable, thread stop, or explicit wait release.",
      "mechanism": "GoalRuntimeHandle::release_native_wait (codex-rs/ext/goal/src/runtime.rs, pub) has no production caller and no GoalService forwarding; the only invocation in the candidate tree is the suite test goal_wait_removed_on_clear_release_and_resume. The mechanism itself (check-in epoch reset plus conditional owned-id remove) is implemented and executed by that test, so no removal behavior is broken; the AC5 release trigger is reachable only by external holders of the runtime handle until a production caller wires it.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/runtime.rs",
          "command": "grep -rn release_native_wait <candidate-tree>/codex-rs --include=*.rs",
          "expected_failure": "exactly two hits: the definition (ext/goal/src/runtime.rs) and the suite-test call (core/tests/suite/goal_native_wait.rs); zero production call sites"
        }
      ],
      "severity": "note",
      "repeat-of": null
    }
  ],
  "notes": [
    "Producer-disclosed partial coverage accepted as stated residual risk: check-in reinsert with paused clock plus live child; exhausted-keep plus late wake with live child; disable/stop dedicated integration; real-abort once-per-transition; non-default inherited-settings assert; second-child-mid-turn full integration; full resume_thread_with_history with rendered SleepItem. Each invariant was additionally verified by code reading in this review.",
    "PANELB-1 is advisory: release_native_wait is public, implemented, and tested; only production wiring is absent.",
    "The AC1 suite-test doc comment claims inherited-settings coverage but asserts no settings; preservation was verified here by reading the shared wake path (queue-only mail selects no new task settings; turn built from thread defaults), not by that test.",
    "Inspection errors fail open: a failed inspection leaves any pre-existing marker in place (late mail can still wake) and the error propagates to a warn log with retry at the next idle, which self-heals. This is the safe direction, not a finding.",
    "No builds or tests were executed locally (forbidden: serialized shared build target); all execution evidence is hosted relux-ci on the exact candidate tree plus static attack.",
    "Read-only on TASK-260929-csyzcj: only q and resource get were used there; no accept, reject, status, handoff, or other write."
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "AC1 integration goal_wait_registers_marker_and_wakes_on_child_completion asserts a real wake model request (wake mock len 1, body carries the completion text) plus marker removal at turn start and 500ms pre-wake silence; the single typed SleepItem slot makes double registration impossible; queue-only mail cannot wake without a stored SleepItem (scheduler gate in tasks/mod.rs plus handlers.rs check). Hosted candidate run 37855177143 green; ignore_native_pending mutant killed by this test (run 37855194303)."
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Non-goal and inactive threads return before inspection and remove any stale marker (runtime.rs early returns); unloaded or empty ownership yields no marker (live edges only; TOCTOU unloads report Unloaded); unknown ids and backend failures return OwnedChildrenReadError, never an empty list (runtime_context.rs), and continue_if_idle propagates as Err. Narrowing mutant skip_failed_lookups killed by owned_children_inspection_propagates_failed_lookups (run 37855265071)."
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Insert precedes the mail recheck in program order (runtime.rs); the recheck shares the held goal permit so the synchronous wake-turn start cannot self-deadlock (verified: start_task awaits BeforeTaskRegistration and goal on_turn_start consumes the shared permit). The two-child latch test bounds every wait (10-15s) and asserts a mail-wake turn and request with no steering text and no marked continuations. Narrowing mutant insert_after_mail_check killed by the latch assertion (run 37855212822). Interleave analysis shows no lost-wake schedule between insert/recheck and the enqueue marker check."
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "insert_if admits only absent-or-own ids and remove_if removes only own ids, both atomic under the ExtensionData lock; the suite foreign test preserves clock-wait-1 across register plus turn start while the foreign marker still permits the wake (intended); unit tests register_never_clobbers_foreign_sleep and conditional_remove_only_removes_owned_id. Narrowing mutants insert_clobbers_one_foreign (run 37855230691) and unconditional_remove (run 37855282786) killed. No other production code stores SleepItems (clock sleep renders history-only items), so the goal-wait: namespace has no squatter."
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "evidence": "Removal on admitted turn start (goal on_turn_start), disable/stop/clear paths (runtime.rs), the release API, and resume restore; Wait and exhausted arms leave the marker untouched so late completions still wake; AC1 and latch assert removal at wake start; clear/release/resume asserted by goal_wait_removed_on_clear_release_and_resume. Residual: release_native_wait has no production caller yet (PANELB-1, note); check-in reinsert with a live child and exhausted-keep late wake rest on construction plus unit tests (producer-disclosed gaps)."
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "ExtensionData insert is a plain map operation (no events, scheduling, history, or reminder changes); AC1 asserts 500ms of no-event silence after the insert and a wake body without goal-wait: and without current_time; the latch test asserts a wake body without goal-wait:. No refusal mutant exists because silence is asserted absence, not a gate (disclosed)."
    },
    {
      "row": "child state transitions",
      "result": "held",
      "evidence": "is_final is untouched (status.rs diff is tests only); Interrupted now reaches turn_finished, which is solely notify_parent_of_terminal_turn (no other side effects); the notice is queue-only (trigger_turn false), gated on the parent holding a goal-owned marker, formatted INTERRUPTED with no FINAL_ANSWER/completed/success wording and under the token cap (unit tests). Narrowing mutant interrupted_claims_success killed (run 37855247950). The shared wake path preserves thread execution settings for queue-only mail. Residual: no real-abort once-per-transition integration and no non-default-settings assert (producer-disclosed gaps); duplicate notices would require duplicate TurnAborted events from the core event stream."
    }
  ],
  "free_hunt": [
    {
      "probe": "permit-share deadlock-fix soundness (precheck-2 production bug)",
      "result": "no-finding",
      "evidence": "start_task awaits emit_turn_start_lifecycle BeforeTaskRegistration before spawning the task future, and goal on_turn_start consumes the shared GoalTurnStartPermit via remove, so the recheck-time permit share cannot self-deadlock and the lease drop is a no-op when consumed."
    },
    {
      "probe": "lost-wake interleave between insert/recheck and completion enqueue",
      "result": "no-finding",
      "evidence": "Two-flag argument over the marker slot and the mailbox queue: an enqueue that observes no marker must precede the insert, which precedes the recheck mail scan in program order, so the recheck observes the enqueued mail; an enqueue after the insert wakes via its own marker check. No lost-wake schedule exists."
    },
    {
      "probe": "goal-wait: namespace squatting by foreign SleepItem producers",
      "result": "no-finding",
      "evidence": "The only production SleepItem stored in extension data is the goal marker; the clock sleep tool renders history-only items keyed by call_id and never stores them. No foreign producer can mint a goal-wait: id in this tree."
    },
    {
      "probe": "side-effect scope of Interrupted reaching turn_finished",
      "result": "no-finding",
      "evidence": "turn_finished delegates solely to notify_parent_of_terminal_turn, whose Interrupted branch only sends the gated queue-only notice; ordinary parents (no owned marker) return before any send. No recording, metric, or scheduling side effect is added for Interrupted."
    },
    {
      "probe": "stale evaluate_continuation production callers missing native_pending",
      "result": "no-finding",
      "evidence": "All evaluate_continuation callers are tests; the sole production goal-continuation evaluation site (continue_if_idle) uses evaluate_continuation_with_native_pending. No Proceed-instead-of-Wait bypass path remains."
    },
    {
      "probe": "Cargo.lock delta review",
      "result": "no-finding",
      "evidence": "The lockfile delta is exactly one line: the new codex-extension-items dependency on the goal crate, matching its Cargo.toml change. No version drift."
    }
  ]
}
```
