# TASK-260929-3f6hfg results rev2 — goal-background-wait vertical test (hosted precheck 1 applied)

## Tree confirmation (this run, no code changes)

Worktree tree still equals `c83869e576d1e024cfdbb5f63cfe8b83c6e969cb`
(temp index: `git read-tree HEAD` + `git add -A` + `git write-tree`, twice,
exit 0). Zero worktree files changed in this run. Candidate remains
UNCOMMITTED (2 files) for the handoff snapshot:

- `codex-rs/app-server/tests/suite/v2/goal_background_wait.rs` (new, ~600 lines, 4 tests)
- `codex-rs/app-server/tests/suite/v2/mod.rs` (+1 line: `mod goal_background_wait;`)

No production changes. No `Cargo.toml`/`Cargo.lock`/schema/Bazel changes.

## Hosted evidence accepted (precheck 1, exact tree)

Base run 37633617318 (snapshot 542a2e5c): lanes
core/app-server/lint/small all `success` — the 4 vertical tests are green
on the hosted app-server lane.

Mutant runs: 5 total, 5 killed, 0 survivors. Vertical killer for each
mutant (precheck-1 table, plus raw failed-log pulls below for the two
mutants whose table row truncates the killer list to 4):

| Mutant | Run | App-server vertical test that fails | Failure site |
|---|---|---|---|
| `silence-ignores-armed` | 37633736582 | `suite::v2::goal_background_wait::notified_exec_exit_wakes_gated_goal_with_receipt_fragment` | `:357` `source="exec_completion"` assertion, TRY 1/2/3 FAIL (verified in job 112834407564/112834409439 failed logs) |
| `drop-wake` (AC3) | 37633707303 | `notified_exec_exit_wakes_gated_goal_with_receipt_fragment` and `user_burst_during_background_wait_admitted_without_loss_or_duplication` | wake `turn/started` wait times out (precheck table) |
| `wake-without-fragment` | 37633768227 | `notified_exec_exit_wakes_gated_goal_with_receipt_fragment` (`:357`) and `user_burst_during_background_wait_admitted_without_loss_or_duplication` (`:458` receipt assertion), all 3 tries each (verified in job 112834507515 failed log) | fragment assertions |
| `allow-notify-on-incapable-host` | 37633645894 | `headless_host_refuses_notify_on_exit_and_promises_no_wake` | refusal-text assertions (precheck table) |
| `always-subscribe` | 37633676266 | `unopted_server_process_does_not_gate_goal_continuation` | continuation wait / no-ack assertion (precheck table) |

Every mutant patch touches production behavior only
(`pending_work.rs`, `async_watcher.rs`, `hook_runtime.rs`,
`exec_command.rs` ×2); none touches test code. Survivor-bound
statement: no survivors, so no survival bound is owed. No test in this
leaf inspects source text — every gate is asserted behaviorally on
mock-server request bodies, notification order, and RPC state — so the
source-text mutant clause (checklist 8) is N/A.

## AC coverage map — 7 of 7 AC rows driven (hosted-green)

| AC | Driving test (committed, `v2::goal_background_wait::`) | Production call site |
|---|---|---|
| AC1 zero continuation before release | `notified_exec_exit_wakes_gated_goal_with_receipt_fragment` (mock count stays 2 after `turn/completed` + `thread/goal/get` round-trips) | `GoalRuntimeHandle::continue_if_idle` via `GoalExtension::on_thread_idle` (background-wait `Wait` on Armed receipt) |
| AC2 one wake with fragment + progress | same test (count 4, `source="exec_completion"` + `receipt_id: {ack-uuid}` + `exit_code: 0` in request 3, goal `Complete` via `thread/goal/get`) | exit watcher `publish_exit` → `enqueue_published_completion` → `TurnInput::ExecCompletion` → `ExecCompletionFragment`, then `update_goal` tool |
| AC3 stalled runtime fails | same test (wake `turn/started` wait times out; `drop-wake` mutant killed by it, run 37633707303) | same wake path as AC2 |
| AC4 headless/incapable host | `headless_host_refuses_notify_on_exit_and_promises_no_wake` (`--session-source exec`; schema lacks `notify_on_exit`, `exec_notification` absent, refusal text, prompt ungated continuation) | `AsyncNotificationSupport::for_host_session_source` seeding → `ExecCommandHandler` refusal + spec gating in `shell_spec` |
| AC5 unopted server not gated | `unopted_server_process_does_not_gate_goal_continuation` (no `receipt ID` ack, continuation arrives while child wedged, no fragment) | default `ExecCompletionMode::Default` (no receipt reserved) → empty `PendingWorkSnapshot` → `ProceedNormal` |
| AC6 burst admitted, no loss/dup | `user_burst_during_background_wait_admitted_without_loss_or_duplication` (2 user turns during wait, each exactly one request carrying its text, `thread/read` texts exactly `["wait-user-one", "wait-user-two"]`, wake still follows) | `turn/start` → `start_or_steer_turn` (user path bypasses the goal gate); `thread/read` items |
| AC7 hosted lane + explicit skips | all tests use `TestAppServer::builder` (auto env) + `send_thread_start_request_with_auto_env`; barrier tests `skip_if_remote!`/`skip_if_wine_exec!` with reasons; headless test runs on every lane; base run green on hosted Linux lane | — |

Negative/refusal rows: AC4 (refusal gate), AC5 (must-not-gate), AC6
(must-admit) are the negative tests; each fails if the gate
admits/rejects wrongly (refusal-text assertion, continuation-timeout,
turn/text-count assertions). All green on the base run, all attacked by
a narrowing mutant killed above.

## Commands (real exit codes)

This run (verification only, no builds per the F2 note):

| Command | Exit |
|---|---|
| `task-board m 'set_status(...)'` | 0 |
| tree check (temp index `read-tree`/`add -A`/`write-tree`, ×2) | 0 |
| `gh run view` + `--log-failed` pulls for runs 37633736582, 37633768227 (read-only) | 0 |

Accepted from the prior pass (unchanged tree, same candidate):

| Command | Exit |
|---|---|
| `codex-fix-suite-busy.py --any` (before build, FREE) | 0 |
| `codex-target-guard.sh` | 0 |
| `just fmt` (after edits) | 0 |
| `just clippy -p codex-app-server` (includes `--tests`) | 0 |
| `just fix -p codex-app-server` | 0 |
| `git apply --check` on each of the 5 mutant patches | 0 × 5 |

Hosted (authoritative for suites/mutants):
base run 37633617318 all lanes green; mutant runs 37633645894,
37633676266, 37633707303, 37633736582, 37633768227 all killed (0
survivors). `just test -p codex-app-server` was never run locally per
the brief; nothing is claimed from local execution of it.

## Out-of-contract rows (acceptance-clause basis)

- `thread/queue/*` API path for AC6: the AC allows "queued **or** burst";
  this leaf drives the burst shape (two `turn/start`s inside one wait).
  The experimental queue API is a separate surface.
- In-turn polling bounds (§11 of final-plan: arbitrary unregistered
  polling remains a stated bound) — inter-turn silence only, per the task.
- Check-in timers (30/60/120 min) and warning text — covered at core
  level (`core/tests/suite/goal_background_wait.rs`); the vertical test
  holds the wait for seconds, far below the first deadline.
- Restart/resume rearming — core-level per final-plan §5.3; not in this
  leaf's AC.
- Windows-host execution of the PowerShell barrier is written but will
  only be proven if relux-ci runs a Windows app-server lane; Linux hosted
  lane is the AC7 target.

## Surface table → coverage map

The brief carries the 3-row surface table; the filled map is
`TASK-260929-3f6hfg_coverage-map.md` (attached beside this note): every
row maps to attacking tests and at least one killed narrowing mutant.
No production defect was exposed (base green, mutants behave as
predicted); nothing outside F's scope was touched.

## Logbook notes (carried forward; no control-root edit)

- `ResponseMock`/`mount_sse_sequence` record only `/responses` POSTs, so
  request counts are exact; bodies beyond the scripted sequence panic the
  responder (fail-closed).
- Harness must own the wiremock `MockServer` and must not be
  destructured by value (drops TempDir guards).
- `goal/set` triggering the first turn dictates goal-first script
  ordering; a manual `turn/start` first would race the set-triggered
  continuation.
- `TestAppServer::builder().with_args(&["--session-source", "exec"])`
  gives a headless host through the production binary (AC4 without any
  test-only seam).
- Precheck killer tables truncate to 4 tests per mutant; for
  `silence-ignores-armed` and `wake-without-fragment` the vertical
  killers were confirmed in the raw `--log-failed` output (this run).

## Status

Candidate unchanged and hosted-green with 5/5 mutants killed by the
vertical tests. Checklist items 3/5/6/7 checked citing precheck 1.
Ready for review.
