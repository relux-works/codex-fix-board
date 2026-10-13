# Panel B verdict — TASK-260929-309h9n CR-TASK-260929-309h9n-3 rev3 (R141, non-recording)

Verdict: accept

Replay tree check: PASS. Base 67789e1ee29e766e446c7f33feb61561d51f94db + patch
TASK-260929-309h9n_change-request_rev3.patch through a temporary index writes tree
3c5cbffcc73270bec86364ab42550441c87f933c, exactly the expected candidate tree.

Commands run (all read-only; no cargo, just, build or test executed):
- GIT_INDEX_FILE=$IDX git read-tree 67789e1e... — exit 0
- GIT_INDEX_FILE=$IDX git apply --cached .temp/TASK-260929-309h9n_change-request_rev3.patch — exit 0
- GIT_INDEX_FILE=$IDX git write-tree — exit 0, printed 3c5cbffcc73270bec86364ab42550441c87f933c
- git grep -n CODEX_GOAL_PACING_DISABLED|pacing_disabled_by_env|PACING_DISABLED_ENV_VAR 3c5cbffc -- codex-rs — exit 1 (empty, expected: switch gone)
- git grep -n std::env|getenv|var( 3c5cbffc -- codex-rs/ext/goal/src/ — exit 1 (empty, expected)
- git grep -n disable_pacing 3c5cbffc -- codex-rs — exit 1 (empty, expected: method deleted)
- git grep -n -i pacing 3c5cbffc -- codex-rs/core/src/state* codex-rs/state* — exit 1 (empty, expected: nothing persisted)
- 7x GIT_INDEX_FILE=$CANDIDX git apply --cached --check mut-<name>.patch — exit 0 each (7/7 mutants apply to the candidate tree)
- killer-presence greps for 14 named killer tests — all present in tree 3c5cbffc
- git show / git diff inspections of extension.rs, background_wait.rs, continuation_schedule.rs, features/src/lib.rs, app-server/src/extensions.rs, config.schema.json — exit 0

No accept/reject/status/handoff write was made on TASK-260929-309h9n. This file is attached to TASK-261012-1tzry5 only.

```verdict-findings
{
  "findings": [
    {
      "id": "B3-N1",
      "row": "placement and size",
      "invariant": "An explicit production policy ships with accurate, code-local bounds; a stored config value must not silently diverge from effective behavior (follows the A2-F1 accurate-bounds ask).",
      "mechanism": "The goal_continuation_pacing flag is read once in GoalExtension::on_thread_start (extension.rs:126,190-194). on_thread_resume (extension.rs:199-217) does not re-read it, by design, and resume preserves the thread-start choice: note_resume clears streak/predecessor/deadlines/quotas but never touches pacing_enabled (background_wait.rs:762-777), so there is no silent resume-disable. on_config_changed (extension.rs:252-264) re-runs goal_config(new_config) and inserts the full new GoalExtensionConfig into thread_store, but applies only `enabled` to the runtime: the stored continuation_pacing diverges from the effective value after a mid-thread toggle. Benign today because the sole thread_store GoalExtensionConfig reader takes max_goal_token_budget only (extension.rs:707-710) and no production path re-reads continuation_pacing. The 'read at thread start only' bound is documented in TASK-260929-309h9n_results.md ('Production policy and bounds'), but the field's in-code doc (extension.rs:67-68) is one line with no thread-start-only note. The rework brief explicitly scoped out a mid-thread toggle ('do not add a new mid-thread toggle in this rework; say explicitly whether ... re-read it') and the producer disclosed the behavior, so this is a note, not a defect: suggest a one-line doc comment on the field.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/extension.rs:199-217,252-264; codex-rs/ext/goal/src/background_wait.rs:762-777",
          "command": "git show 3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/ext/goal/src/extension.rs | sed -n '199,217p;252,264p'; git show 3c5cbffcc73270bec86364ab42550441c87f933c:codex-rs/ext/goal/src/background_wait.rs | sed -n '762,777p'",
          "expected_failure": "No failure: static witness, command exit 0. Resume preserves pacing_enabled; config-update stores but does not apply continuation_pacing; no in-code thread-start-only doc on the field."
        },
        {
          "test_file": "codex-rs/ext/goal/src/extension.rs:707-710 (sole stored-config reader)",
          "command": "git grep -n 'get::<GoalExtensionConfig>' 3c5cbffcc73270bec86364ab42550441c87f933c -- codex-rs",
          "expected_failure": "No failure: static witness, command exit 0. Exactly one reader site, and it takes max_goal_token_budget only, so the stored-but-unapplied flag value is unread."
        }
      ],
      "severity": "note",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Provenance: replay plus static attack only. No cargo, just, build, or Rust test command was run (panel rule: shared build target serialized). Executed evidence is hosted relux-ci run 38232681612 on the EXACT candidate tree 3c5cbffc (precheck 9: lint/small/core/app-server 4/4 green, 7/7 mutants killed), accepted from TASK-260929-309h9n_hosted-precheck-9.md and the rev3 validation log (mini-hosted-gate exit 0).",
    "Rev2-to-rev3 production delta on scheduling files is purely subtractive plus the flag swap: continuation_schedule.rs loses only the env const/fn block; background_wait.rs loses only disable_pacing; extension.rs swaps the env read for the flag read plus the E0382 copy-before-move. All rev2 held-row mechanisms were re-verified present in 3c5cbffc, not assumed carried.",
    "Trunk content from the base refresh (P3-1: ContextContributor impl, waiting_capability_fragments, related imports in extension.rs) is NOT under review and was not swept as Story content.",
    "A2-F1 / B2-N2 / D-N2 closure: the ambient CODEX_GOAL_PACING_DISABLED switch, its public reader/exports, and disable_pacing are fully removed (whole-tree greps exit 1), replaced by Feature::GoalContinuationPacing (Stable, default on) mapped by the single production host. The explicit-policy remedy the rev2 panels asked for is implemented and disclosed.",
    "B2-N1 hardening verified: core goal_background_wait fixture sets continuation_pacing:false and asserts !is_pacing_enabled(); precheck 9 core lane green. The precheck-6 P4a first-try failure and precheck-8 unrelated retries remain disclosed history; precheck 9's report gives no retry details, so no first-try claim is made.",
    "Carried bounds (decided, not findings): AC1 completed-count n vs implemented upcoming-ordinal pacing_delay(streak+1) wording gap; unit inventory is now exactly 22 (23 minus the removed env test), matching results; per-mutant failing lanes reported small/core only (no per-mutant app-server execution evidenced either way); note_release still has no production caller; marker-scan (4-request body scan) is weaker than full history equality; aggregate mutant-run model-request totals unknown.",
    "Flag-mutant killer direction: pacing_feature_flag_ignored is killed through the public runtime entry by core background_wait_inactive_on_unavailable_host_auto_continues, which asserts !is_pacing_enabled() under a continuation_pacing:false fixture (fails under || true). The four app-server .disable_feature opt-out sites are additional policy coverage whose back-to-back timing passes in the green app-server lane.",
    "No write of any kind was made on TASK-260929-309h9n (no accept/reject/withdraw/status/handoff/note/resource)."
  ],
  "surface_results": [
    {
      "row": "spacing and streak math",
      "result": "held",
      "attack": "Off-by-one in n; overflow/missing cap; reset on non-state-change; reset sourced from tool success/plan/model text; second classifier diverging from P4b-1; entry-rule deletion.",
      "evidence": "pacing_delay is byte-identical in behavior to the rev2-held code (rev2->rev3 diff on continuation_schedule.rs deletes only the env block): shift min 31, checked_mul with cap fallback plus .min(cap). Entry rule intact (background_wait.rs:464). Hosted precheck 9 on exact tree: small lane green incl pacing_delay_n1_n2_n3_and_cap; pacing_missing_cap killed by it; pacing_streak_reset_on_non_state_change killed incl by pacing_two_polls_grow_streak; entry mutant killed by 19 tests incl the named killer. Streak reads only P4b-1 accounting (has_observed_state_change); no second classifier."
    },
    {
      "row": "polls grow the streak end to end",
      "result": "held",
      "attack": "Poll treated as activity; streak reset per turn; units-only test without request counts.",
      "evidence": "App-server goal_pacing_two_polls_first_immediate_second_60s passes in the green precheck-9 app-server lane on the exact tree (asserts 2 then 4 requests, first start <28s, second >=58s, no third turn). pacing_streak_reset_on_non_state_change is killed by small+core incl pacing_two_polls_grow_streak and both core pacing tests. Poll handling is untouched by the flag rework."
    },
    {
      "row": "one live timer",
      "result": "held",
      "attack": "Second independent timer; tokio::spawn(sleep) per continuation; replacement leaking the old task; wake leaving pacing armed; pacing overriding a governing subscribed deadline; P4a check-in interference.",
      "evidence": "continuation_schedule.rs (135 LoC) contains zero timer code (math plus ticket only). background_wait.rs rev2->rev3 delta is the disable_pacing deletion only; the shared CheckInTimer slot, replacement/abort, and invalidation-hook wiring are unchanged. Hosted: replacement/wake/cancel unit tests green; pacing_timer_not_cancelled_on_invalidation killed by pacing_event_wake_preempts_timer and pacing_invalidation_cancels_armed_timer; pacing-enabled public wake tests green. P4a suite decoupled via continuation_pacing:false fixture; precheck-9 core green (retry-history bound in notes)."
    },
    {
      "row": "ticket invalidation and admission",
      "result": "held",
      "attack": "Skipped revision/generation check; check-then-act outside the lock; fast human turn not invalidating; stale timer starting a turn; invalidation not cancelling the sleeper.",
      "evidence": "check_pacing_admission_locked (background_wait.rs:627-663) rechecks outstanding handle plus generation plus reuse guard, goal id (attempt and state), revision (attempt and ticket), predecessor, and empty snapshot, consuming exactly once under the state lock; unchanged from rev2-held code. Hosted: pacing_stale_ticket_admission_skip_revision killed by pacing_stale_ticket_rejected_on_revision_change; fast-human/reuse/claim tests green. note_human_input resets streak and clears the automatic-predecessor mark. note_release no-production-caller bound carried."
    },
    {
      "row": "blocker order and waiting turns",
      "result": "held",
      "attack": "Pacing before the blocker; blocker thresholds changed; waiting turn classified empty.",
      "evidence": "EmptyResponse blocker (extension.rs:387) still runs before pacing bookkeeping note_turn_completed (extension.rs:430); thresholds untouched. Hosted: core goal_pacing_empty_blocker_runs_before_rescheduling green (immediate, 60s, 120s, Blocked, 3 requests then silence); pacing_blocker_skipped_for_paced_turns killed by it. pacing_waiting_turn_is_paced_not_empty green in small."
    },
    {
      "row": "transient state",
      "result": "held",
      "attack": "Streak persisted to rollout; stale subscription restored; allowance reset on completion; undisclosed restart reset.",
      "evidence": "note_resume (background_wait.rs:762-777) clears streak/goal/predecessor/deadlines/check-in quota and invalidates tickets; pacing_enabled is preserved so resume restarts at the floor without silently disabling. No pacing symbols in state/rollout paths (grep exit 1). Hosted pacing_resume_restarts_at_floor_and_resets_quotas green. Completion-not-renewing-allowance and restart-resetting-quotas bounds disclosed in results; completion path untouched by rework."
    },
    {
      "row": "no model-visible change",
      "result": "held",
      "attack": "Injected pacing text; history items for timers; cache-busting context changes; new warnings.",
      "evidence": "Story scheduling additions to the turn path are bookkeeping-only (record_state_change_for_item, note_turn_completed after the blocker); continuation_schedule.rs adds no prompt/history/context writes. The ContextContributor/waiting_capability_fragments in extension.rs is P3-1 trunk content, out of scope. Hosted: small pacing_emits_no_warnings_or_prompt_text green; app-server 4-request body scan green in the exact-tree lane. Marker-scan bound carried."
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "attack": "Mutant not applying to the final tree; killer outside the hosted filter; requests not measured.",
      "evidence": "7/7 mutant patches verified git apply --cached --check clean (exit 0 each) against the candidate index. Precheck 9 on the exact tree: 7/7 killed, 0 survivors, every named killer verified present in tree 3c5cbffc. Request counts asserted by hosted tests: core 2 and 3, app-server 4, wake tests 4 and 6, units 0. Required five families plus entry rule plus flag policy all covered with named killers."
    },
    {
      "row": "placement and size",
      "result": "held",
      "attack": "A2-F1 re-check: ambient/env production switch remnants; flag spec shape; flag reachability on every host path; config.schema.json drift in either features map; scheduler logic in codex-core; module size; new public API beyond need.",
      "evidence": "Env triple grep across codex-rs exit 1; disable_pacing grep exit 1; no std::env in ext/goal/src. Feature::GoalContinuationPacing sits next to Goals (Stable, default_enabled true, key goal_continuation_pacing). Schema entries present in BOTH features maps, alphabetical (fast_mode < goal_continuation_pacing < goals), sibling-identical shape; hosted core lane (fixture check) green. Single production installer: app-server thread_extensions maps the flag; every other GoalExtensionConfig construction is a test fixture with an explicit true/false; CLI/TUI install no goal extension directly. continuation_schedule.rs 135 LoC (<500); background_wait.rs 908 (down from 923, extraction remains advisory only). core/src delta is observation fan-out hooks only (notify_plan_committed plus call_id/args threading), no scheduler logic, no core->goal dependency. E0382 fix shape verified (continuation_pacing copied before config moves into thread store). A2-F1/B2-N2/D-N2 closed; residual mid-thread-toggle bound is note B3-N1."
    }
  ],
  "free_hunt": [
    {
      "family": "ambient or env-based production switch remnants",
      "result": "None found. Whole-tree greps for the env name, reader, and const exit 1; no std::env use remains in ext/goal/src. The test hook is fully excised, not re-pointed."
    },
    {
      "family": "flag reachability on every host path",
      "result": "Complete. app-server/src/extensions.rs is the only production GoalExtensionConfig construction; core and ext/goal constructions are all test fixtures with explicit values. No host can construct the config without choosing pacing behavior (bool field, no Default bypass)."
    },
    {
      "family": "config.schema.json drift vs generated shape",
      "result": "No drift. Both features maps carry goal_continuation_pacing with the exact sibling shape and correct alphabetical placement; the hosted core lane validates the fixture and is green."
    },
    {
      "family": "mid-thread toggle silently ignored",
      "result": "Bounded as note B3-N1: resume preserves the thread-start choice (no silent disable); config-update stores-but-does-not-apply (benign, value unread); results.md documents read-at-thread-start-only; in-code field doc lacks the note."
    },
    {
      "family": "rev2->rev3 production delta beyond the brief",
      "result": "None. Scheduling-file delta is the env-block deletion, disable_pacing deletion, and flag swap plus E0382 fix. extension.rs additionally carries P3-1 trunk imports/impl (ContextContributor), which is out-of-scope trunk content, not Story behavior."
    }
  ]
}
```
