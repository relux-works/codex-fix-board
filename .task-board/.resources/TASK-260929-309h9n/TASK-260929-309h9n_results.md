# TASK-260929-309h9n — continuation-schedule: precheck 9 review handoff

## Current provenance and exact-tree evidence

Protected base: 67789e1ee29e766e446c7f33feb61561d51f94db (P3-1 landed).
Signed Story checkpoint: 4649d6571e09fb755c8f204931a6020a40605951.
Uncommitted candidate tree: 3c5cbffcc73270bec86364ab42550441c87f933c.
The mini-hosted-gate returned exit 0 for this exact tree and hosted run 38232681612.
No source, test or config file changed during this handoff.

Accepted hosted evidence: TASK-260929-309h9n_hosted-precheck-9.md,
[relux-ci run 38232681612](https://github.com/ivanopcode/codex/actions/runs/38232681612),
ref relux/ci-next. Lint, small, core and app-server: 4/4 success.
Mutants: 7/7 killed, 0 survivors. Precheck 9 supersedes precheck 8 for this refreshed tree.
The hosted report supplies lane conclusions, not individual test-process exit codes;
no unreported process exit codes are invented.

The scoped supported refresh preserved product content from old candidate
eb655488b22ff6bb17a3a3a6250fd60e3a202209 / checkpoint ba7249177b414c71ac277ae41fa3dc5dc5b1f16b.
Exactly one checkpoint-replay import conflict in codex-rs/ext/goal/src/extension.rs was resolved:
keep PlanCommitInput then PromptFragment. Authorized replacement p4b/b2-replay-extension.rs,
SHA-256 cefdd1fd6376d19b3240a30fd52cb70777201e1949f62ba26c4863b94799cf27.
The supplied replacement was verified byte-for-byte against only that resolved hunk.
Supported refresh returned refresh_advanced with no candidate-delta conflict;
the resulting tree matches the orchestrator's prediction.
TASK-260929-309h9n_refresh-logbook-9.md retains all recovery command exits and resolution details.
TASK-260929-309h9n_successor-logbook-9.md retains the earlier expected gate refusal before
precheck 9 was recorded. That pending-evidence boundary is now closed.

## Implementation retained

The new ext/goal/src/continuation_schedule.rs owns pacing math and ticket types.
BackgroundWaitState integrates pacing into the existing single CheckInTimer slot, lock,
generation, invalidation and admission machinery; no second timer or detached sleep is added.
GoalRuntimeHandle::continue_if_idle evaluates pacing through that slot.
GoalExtension::on_turn_stop preserves the existing empty-response blocker before bookkeeping.
P4b-1 committed observations determine the streak; poll counts and model text do not reset it.
Core production scheduling/context is unchanged; core and app-server suites drive the real runtime.
The dedicated module is under 500 LoC. No prompt, history or rollout scheduling field is added.

## Summary

Rework per `b2-rework-brief-review2.md` closes review rev2 `A2-F1` (row `placement and size`):
the ambient `CODEX_GOAL_PACING_DISABLED` kill switch is gone, replaced by an explicit production
policy — `Feature::GoalContinuationPacing` (`goal_continuation_pacing`, `Stable`, default on) —
mapped by the host into `GoalExtensionConfig::continuation_pacing` and read once at thread start.
Every other rev2 row is held unchanged (spacing/streak, polls, timer, ticket, blocker, transient,
no model-visible change). The P4a `goal_background_wait` core fixture now sets `false`, decoupling
that suite from pacing (B2-N1 hardening); its explicit `disable_pacing()` call is removed and the
method itself is deleted (no remaining caller). No production scheduling behavior changes except
the opt-out mechanism.

## Changed files (review rev2 rework; plus orchestrator fix 8)

- `codex-rs/features/src/lib.rs`: `GoalContinuationPacing` variant + spec next to `Goals`.
- `codex-rs/core/config.schema.json`: `goal_continuation_pacing` boolean in both features maps,
  alphabetically before `goals` (hand-edited to generated shape; hosted core lane checks fixture).
- `codex-rs/ext/goal/src/extension.rs`: `continuation_pacing: bool` on `GoalExtensionConfig`;
  `on_thread_start` enables pacing only when set.
- `codex-rs/app-server/src/extensions.rs`: maps `Feature::GoalContinuationPacing`.
- `codex-rs/ext/goal/src/continuation_schedule.rs`, `lib.rs`: env const/fn and exports removed.
- `codex-rs/ext/goal/src/background_wait.rs`: `disable_pacing()` deleted.
- `codex-rs/ext/goal/tests/continuation_schedule.rs`: env import + `pacing_disabled_by_default_with_env_kill_switch` removed.
- Core fixtures: `goal_continuation_pacing.rs` sets `true`; `goal_background_wait.rs` and
  `goal_activity_tests.rs` set `false`. P4a test asserts `!is_pacing_enabled()` via fixture config
  instead of calling `disable_pacing()`. No test in `goal_background_wait.rs` needs pacing `true`.
- Ext/goal harnesses (`goal_extension_backend.rs` x3, `background_wait_activation_tests.rs`): `false`.
- App-server: `goal_background_wait.rs` harness, `code_mode_host.rs`, `thread_goal_empty_responses.rs`,
  `thread_resume.rs` use `.disable_feature(Feature::GoalContinuationPacing)`; `with_env_overrides` removed.

## Production policy and bounds (A2-F1 accurate bounds)

- Pacing is on by default (`default_enabled: true`, host maps at thread extensions install).
- `[features] goal_continuation_pacing = false` restores immediate back-to-back automatic continuations.
- The flag is read once at thread start (`GoalExtension::on_thread_start`). `on_thread_resume` does
  not re-read it (resume only reconciles goal state and discards transient waits via `note_resume`).
  The config-update path (`ConfigContributor::on_config_changed`, `extension.rs:~253`) does not re-read
  it either (it only updates `enabled`); no mid-thread toggle was added in this rework.
- After the change, `git grep -n CODEX_GOAL_PACING_DISABLED -- codex-rs` is empty (exit 1).

## AC coverage map (hosted precheck 9: 4/4 lanes green; 7/7 mutants killed)

| AC | Requirement | Driving test | Refusal / negative test |
|----|-------------|--------------|-------------------------|
| AC1 | Entry rule + spacing/delays | `goal_pacing_first_immediate_second_at_60s` + `pacing_delay_n1_n2_n3_and_cap` | `pacing_first_continuation_paced_after_human_turn`, `pacing_missing_cap` |
| AC2 | Two polls grow streak end to end | app-server `goal_pacing_two_polls_first_immediate_second_60s` | `pacing_streak_reset_on_non_state_change` |
| AC3 | One live timer, event pre-emption | `pacing_new_schedule_replaces_old_without_accumulation`, `pacing_event_wake_preempts_timer`, `pacing_invalidation_cancels_armed_timer` + pacing-enabled wake tests | `pacing_timer_not_cancelled_on_invalidation` |
| AC4 | Ticket binding/invalidation/admission | `pacing_ticket_binds_goal_revision_predecessor_generation`, `pacing_stale_ticket_rejected_on_revision_change`, `pacing_fast_intervening_human_turn_invalidates` | `pacing_stale_ticket_admission_skip_revision` |
| AC5 | Blocker FIRST, waiting paced | `goal_pacing_empty_blocker_runs_before_rescheduling` | `pacing_blocker_skipped_for_paced_turns` |
| AC6 | Transient only, resume at floor | `pacing_resume_restarts_at_floor_and_resets_quotas` | (disclosed bound: restart resets quotas) |
| AC7 | No model-visible change | `pacing_emits_no_warnings_or_prompt_text` + app-server body scan | — |
| AC8 | Mutants + request counts | 7 mutants (6 existing + flag); counts below | — |

Killer mapping (7 mutants):

- `pacing_streak_reset_on_non_state_change` -> `pacing_two_polls_grow_streak` (+ core pacing tests)
- `pacing_missing_cap` -> `pacing_delay_n1_n2_n3_and_cap`
- `pacing_stale_ticket_admission_skip_revision` -> `pacing_stale_ticket_rejected_on_revision_change`
- `pacing_timer_not_cancelled_on_invalidation` -> `pacing_invalidation_cancels_armed_timer`
- `pacing_blocker_skipped_for_paced_turns` -> `goal_pacing_empty_blocker_runs_before_rescheduling`
- `pacing_first_continuation_paced_after_human_turn` -> `pacing_first_continuation_after_human_turn_proceeds_immediately`
- `pacing_feature_flag_ignored` -> observed hosted killer
  `suite::goal_background_wait::background_wait_inactive_on_unavailable_host_auto_continues`
  (core lane). The app-server opt-out cases are additional policy coverage; they are not
  reported as observed mutant killers in precheck 9.

Hosted filter: `test(pacing) | test(continuation_schedule) | test(goal)`.
The observed flag killer is selected by its full `goal_background_wait` test path.
All seven mutants were killed in hosted precheck 9; none survived. Exact lane failures and
all observed killer names are in `TASK-260929-309h9n_hosted-precheck-9.md`.

## Model requests per scenario (asserted by green hosted precheck 9)

| Scenario | Requests | Source |
|----------|----------|--------|
| Core paused-time two quiet turns | 2 (1 per turn) | `goal_pacing_first_immediate_second_at_60s` |
| Core blocker proof: 3 empty turns, then silence | 3 (still 3 after +241 s) | `goal_pacing_empty_blocker_runs_before_rescheduling` |
| App-server two poll turns | 4 (2 per turn) + no early third in 8 s | `goal_pacing_two_polls_first_immediate_second_60s` |
| App-server background-wait wake tests (pacing-enabled) | 4 and 6 | `notified_exec_exit_...`, `user_burst_...` |
| All `ext/goal` pacing unit tests | 0 | fake time, no model |

## Feature-flag inventory (env var gone)

- `v2/goal_background_wait.rs` harness (`pacing_disabled` param, `/*pacing_disabled*/` callsites kept):
  only `unopted_server_process_does_not_gate_goal_continuation` and
  `headless_host_refuses_notify_on_exit_and_promises_no_wake` pass `true` -> `.disable_feature(...)`.
  Doc now says users opt out via `[features] goal_continuation_pacing = false`.
- `v2/thread_goal_empty_responses.rs`: `.disable_feature(...)` (three back-to-back empties).
- `v2/code_mode_host.rs::app_server_blocks_goal_after_repeated_code_mode_host_failures`: same (three back-to-back).
- `v2/thread_resume.rs::thread_goal_keeps_original_root_until_external_objective_edit`: same (two chained).
- Core `goal_background_wait.rs` fixture: `continuation_pacing: false` (decouples P4a suite; B2-N1).
- Core `goal_activity_tests.rs` fixture: `false` (preserves timing; only idle emit is BudgetLimited, never paced).
- Core `goal_continuation_pacing.rs` fixture: `true` (pacing suite).
- Ext/goal harnesses: `false` (no pacing coverage there).
- New suites (core/app-server pacing, goal units): pacing active, no switch.

## Personally run verification — this handoff

Every gate was run directly without a pipe or tee.

| Command | Actual exit | Result |
| --- | --- | --- |
| bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh | 0 | Exact tree 3c5cbffc matches green hosted run 38232681612 |
| /Users/administrator/.cargo/bin/cargo fmt -- --config imports_granularity=Item --check (from codex-rs) | 0 | Expected stable-channel imports_granularity warnings; no file changes |
| git diff --check | 0 | Clean |
| git diff --cached --check | 0 | Clean |
| git rev-parse HEAD | 0 | Checkpoint 4649d6571e09fb755c8f204931a6020a40605951 |
| git merge-base --is-ancestor 67789e1ee29e766e446c7f33feb61561d51f94db HEAD | 0 | Required base ancestry |
| git grep -n CODEX_GOAL_PACING_DISABLED -- codex-rs | 1 | Expected empty result; removed env switch absent |
| Python patch-check runner (resource read plus seven git apply --check - child processes) | 0 | 7/7 patches clean, none applied |

Each git apply --check exited 0 individually:
pacing_streak_reset_on_non_state_change, pacing_missing_cap,
pacing_stale_ticket_admission_skip_revision, pacing_timer_not_cancelled_on_invalidation,
pacing_blocker_skipped_for_paced_turns, pacing_first_continuation_paced_after_human_turn,
pacing_feature_flag_ignored. Patch applicability is distinct from hosted mutant execution.

No local build, check, clippy or tests were run: the Mac mini addendum prohibits them.
Hosted compilation, lint, small tests, core/app-server integration tests and mutant kills
are accepted from precheck 9, not claimed as personally rerun.
This handoff made zero model requests; scenario counts above are asserted by the hosted tests.
No code change after the gate verification, no commit, branch switch or manual recovery.

## Review findings and retained fixes

- A2-F1, B2-N2, D-N2: the ambient env opt-out and exported test-only reader are removed.
  The explicit Stable feature is default on; the bounds and opt-out inventory above describe the shipped policy.
  The flag-ignored narrowing mutant is killed by the public core runtime entry test named above.
- B2-N1: the P4a core fixture is configured with pacing off. Its
  `scheduled_checkins_fire_through_production_runtime_under_paused_time` passed on the first
  try in precheck 8; this hardens the fixture without claiming a proven cause for its earlier retry.
- D-N1: precheck 6's check-in test failed try 1 then passed try 2; that retry is retained
  in the record. No unsupported claim of reliable first-try behavior or unrelatedness is made.
- Review rev1's blocker proof remains the production-path core test
  `goal_pacing_empty_blocker_runs_before_rescheduling`, with the actual blocker-skipping
  mutant killed. Core pacing synchronization fixes remain unchanged.
- Orchestrator compile fixes 2 and 3 remain: `Duration::checked_mul` multiplier uses u32;
  test deadline math uses `saturating_sub`; notification read supplies `TurnStartedNotification`.
- Orchestrator logic fix 4 remains: first goal binding retains the recorded streak;
  only replacement of an already bound goal resets it.
- Orchestrator CI fix 4 remains: the exact app-server pacing test has a 120 s nextest timeout
  because it measures a real 60 s delay.
- Orchestrator lint fix 8 remains: `continuation_pacing` is copied before `config` is moved
  into the thread store. Precheck 7 genuinely failed E0382 before tests/mutants; precheck 8 validates the fix.
- Precheck 8 core had two retries: `hooks::permission_request_hook_allows_exec_command_without_user_approval`
  and `realtime_conversation::conversation_second_start_replaces_runtime`; both passed on retry.
  These are recorded as retries, not first-try passes.

## Checklist evidence and handoff logbook

Validation items 3/4/5/10 cite exact-tree precheck 9 (4/4 successful lanes, 7/7 killed mutants).
Items 1/2/8/9 retain pre-spawn surface-table.md and the AC map.
Items 6/7 cite this refreshed outcome and TASK-260929-309h9n_handoff-logbook-9.md.
Item 11 retains recorded changes_requested verdicts and reject routing.
The rev2 findings are answered above; this developer handoff does not record review acceptance.

## Disclosed bounds

- First continuation after human input, goal set/mutation or resume proceeds immediately.
  Pacing applies after an automatic goal predecessor; observed change resets to the 30 s floor.
- Pacing is default on. [features] goal_continuation_pacing = false restores immediate
  back-to-back automatic continuations.
- Feature policy is read at thread start only; resume and config-update do not re-read it.
- Resume clears transient waits/streaks; restart resets transient quotas and loses live observation.
  Completion does not renew the human-input allowance.
- Arbitrary polling within a turn remains unpaced (plan section 11).
- Historical precheck-6 P4a retry and precheck-8 unrelated retries remain disclosed above.
  Precheck 9's report gives no retry details; no additional first-try claim is made.
- No temporary directory/file was created manually this turn. The gate removes its temporary index
  via its EXIT trap. No CODEX_HOME copy, no installed codex reproduction, no background process remains.
