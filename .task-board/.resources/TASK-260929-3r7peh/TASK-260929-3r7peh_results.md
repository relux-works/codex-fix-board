# TASK-260929-3r7peh results — notify-on-exit + exec-notification activation

## Summary

Activated completion notifications together with the P4a goal background-wait
policy (final plan 5.1, 5.3, 6 and 10 stage 2e), stacked on landed P4a at
`2f522b9dc9`. Capable hosts only:

- New `AsyncNotificationSupport` host marker in `codex-extension-api`
  (default `Unavailable`). Seeded for roots at the app-server `thread/start`
  boundary from the host session source (only `Cli`/`VSCode` enable) and in
  `ThreadManager::spawn_thread`, where children inherit the parent's stored
  value explicitly (fail closed when the parent is unknown) and parentless
  roots/resumes take the host decision. A child's own source is never
  consulted, so descendants of headless exec stay `Unavailable`.
- `exec_command` gains opt-in `notify_on_exit` (default false), exposed in the
  schema only on capable interactive hosts. Acceptance reserves one of 64
  receipt slots before launch and refuses when full, before execution. The
  yielded response acknowledges the armed subscription with the receipt handle.
- New `exec_notification` tool (`read`/`release`), advertised only on capable
  hosts. Read returns retained terminal output (default 2000 tokens, clamped
  below 10000 per response, truncation indicated, never waits). Release disarms
  without killing, frees the slot, and cancels a pending wake. Stale, foreign,
  and unknown receipts are rejected.
- The exit watcher and the raced-arm path enqueue the mailbox wake for live
  `Queued` receipts only (released/cancelled/inline receipts earn nothing),
  closing the stage-2b TODO that left real exits waiting pre-enqueue.
- Goal `on_thread_start` enables the background-wait policy where the marker
  is `Available`, so pending opted-in work gates automatic continuation while
  explicit user input stays admissible.
- Tool descriptions promise exactly: a wake only when `notify_on_exit` was
  accepted, release disarms without terminating. No promise on incapable
  hosts. No no-wait/end-turn paragraph (deferred to P4b, as instructed).

Out of scope (per brief): app-server vertical test (sibling
TASK-260929-3f6hfg, F2), P3 capability flags, P4b pacing, P4c subagent wait.

## Changed files

Production (logic ~450 lines):

- `codex-rs/ext/extension-api/src/async_notification.rs` (new):
  `AsyncNotificationSupport::{Available, Unavailable}`,
  `for_host_session_source`, `read_from`.
- `codex-rs/ext/extension-api/src/lib.rs`: module export.
- `codex-rs/app-server/src/request_processors/thread_processor.rs`: seed the
  host decision into `thread_extension_init` at `thread/start`.
- `codex-rs/core/src/thread_manager.rs`: `inherited_async_notification_support`
  + seeding in `spawn_thread` (explicit parent inheritance, host fallback).
- `codex-rs/core/src/tools/handlers/shell_spec.rs`: `notify_on_exit` schema
  property + capability descriptions, `create_exec_notification_tool`, read
  token constants.
- `codex-rs/core/src/tools/handlers/unified_exec.rs`: `ExecCommandArgs.notify_on_exit`.
- `codex-rs/core/src/tools/handlers/unified_exec/exec_command.rs`: refusal
  before execution (one-shot + incapable host), completion-mode selection,
  capacity error mapping.
- `codex-rs/core/src/tools/handlers/unified_exec/exec_notification.rs`
  (new): `read`/`release` dispatch, owner resolution, mailbox cancel on
  release, token-bounded rendering.
- `codex-rs/core/src/tools/handlers/unified_exec_tests.rs`,
  `.../mod.rs`, `.../spec_plan.rs`: exports, router context, conditional
  `exec_notification` registration.
- `codex-rs/core/src/tools/context.rs`: `ExecCommandToolOutput.completion_receipt`
  + header acknowledgment.
- `codex-rs/core/src/unified_exec/completion_receipt.rs`:
  `InitialResponseOutcome::Queued` carries `TerminalCompletion` (mailbox
  entries need exit details on the raced-arm path),
  `ReceiptId::from_model_handle`, owner accessors.
- `codex-rs/core/src/unified_exec/receipt_hooks.rs`:
  `notification_owner_for_receipt` (binding-only resolve, thread+generation
  verify), `enqueue_published_completion` (enqueue, single liveness recheck
  + ghost cleanup, wake; the pre-enqueue gate was removed as redundant in
  the precheck-3 rework — see below).
- `codex-rs/core/src/unified_exec/receipt_output.rs`: `retained_sizes` peek.
- `codex-rs/core/src/unified_exec/async_watcher.rs`: publish match — enqueue
  + wake only on `Queued`; retained exits only feed the arm/inline rendezvous.
- `codex-rs/core/src/unified_exec/process_manager.rs`: raced-arm enqueue,
  receipt handle in the yielded response; removed the now-unused
  `exec_command` wrapper (kept its tracing span on the surviving entry).
- `codex-rs/ext/goal/src/extension.rs`: enable `background_wait_state` where
  available at thread start.

Tests (~2450 lines; new files + extensions):

- `codex-rs/core/src/tools/handlers/shell_spec_tests.rs`,
  `spec_plan_tests.rs`, `unified_exec_tests.rs`,
  `unified_exec/exec_notification_tests.rs` (new),
  `unified_exec/receipt_hooks_tests.rs`,
  `completion_receipt_tests.rs`, `thread_manager_tests.rs`,
  `tools/context_tests.rs`, `unified_exec/mod_tests.rs` (literal updates).
- `codex-rs/core/tests/suite/exec_notification.rs` (new) + `mod.rs`.
- `codex-rs/core/tests/suite/goal_background_wait.rs` (fixture + 2 tests).
- `codex-rs/ext/goal/tests/goal_extension_backend/background_wait_activation_tests.rs`
  (new).

## Coverage map — 8 of 8 AC rows driven

Every row is driven through its production entry point by a named committed
test. Ratios count distinct rows, not tests.

| AC | Production call site | Driving test(s) | Refusal / negative test(s) |
|---|---|---|---|
| AC1 available schema + listing | `build_tool_router` → `add_shell_tools`; `create_exec_command_tool_with_environment_id` | `available_host_lists_exec_notification_and_notify_on_exit`; `exec_command_schema_gates_notify_on_exit_on_host_capability` | `unavailable_host_hides_exec_notification_and_notify_on_exit`; `notify_on_exit_refused_before_execution_on_unavailable_host` (handler, asserts 0 slots); `exec_notification_opt_in_refused_on_headless_exec` (suite, asserts refusal + schema omission in the sampled request); `async_notification_child_of_headless_parent_stays_unavailable` (descendant half) |
| AC2 default false, no receipt/slot/wake | `ExecCommandHandler::handle_call` → `exec_command_with_completion_mode(Default)` | `exec_command_args_default_notify_on_exit_to_false`; `default_launch_acknowledges_no_receipt`; `exec_notification_default_launch_arms_and_wakes_nothing` (suite: no armed line + no wake after exit) | narrowing mutant m1 (arm by default) must fail the lib parse test and the suite test |
| AC3 65th refused pre-execution; process cap unchanged | `exec_command_inner` reserve-before-spawn; handler `ReceiptCapacityExceeded` mapping | `sixty_fifth_opted_in_launch_refused_before_execution` (asserts empty process list + default launch still runs); `exec_notification_capacity_refuses_65th_and_default_still_runs` (suite) | mutant m6 (handler drops opt-in) must fail both suite legs |
| AC4 read retained output, bounds, never blocks; stale/foreign/unknown rejected | `ExecNotificationHandler::handle_call` → `notification_owner_for_receipt` → `read_retained_output` | `read_returns_retained_terminal_output`; `read_indicates_truncation_and_stays_under_token_bound` (<10K tokens asserted); `exec_notification_opt_in_arms_and_read_returns_terminal_output` (suite, incl. wake-fragment assertion) | `read_rejects_unknown_receipt`, `read_rejects_malformed_receipt_handle`, `read_rejects_foreign_receipt`, `read_rejects_stale_receipt_after_release`, `read_before_exit_is_rejected_without_waiting` (never blocks); `exec_notification_unknown_receipt_rejected` (suite); mutant m5 (skip owner verify) |
| AC5 release disarms w/o kill, frees slot, no later wake | `ExecNotificationHandler::handle_call` → `release_completion_receipt` + `cancel_runtime_notification`; watcher publish-fails on cancelled | `release_disarms_frees_slot_and_cancels_pending_wake` (slot 1→0, pending wake cancelled); `opted_in_launch_arms_and_release_silences_later_exit` (real spawn: terminate still finds it alive; no mailbox entry after the terminal event) | `release_rejects_unknown_receipt`; `enqueue_published_completion_skips_disarmed_receipt`; `enqueue_published_completion_drops_ghost_retention`; suite `exec_notification_release_disarms_without_killing` (alive poll + stale read + no wake); mutants m4 (release skips mailbox cancel), m9 (recheck skips retention drop) |
| AC6 descriptions match capability | `create_exec_command_tool_with_environment_id`, `create_exec_notification_tool` | `exec_command_schema_gates_notify_on_exit_on_host_capability` (Unavailable description byte-identical; Available states the promise; asserts no "end the turn"); `exec_notification_tool_matches_expected_spec` (disarm-without-kill; read/release enum; required fields) | same tests assert the negative half (no `notify_on_exit` mention when Unavailable) |
| AC7 policy gates goal, user input admitted | `GoalExtension::on_thread_start` → `BackgroundWaitState::enable`; `continue_if_idle` Wait arm | `background_wait_activation_gates_goal_but_admits_user_input` (suite: 0 requests on idle, then user turn admitted with 1 request); `background_wait_activates_only_on_available_hosts` (goal backend: Available/Unavailable/absent) | `background_wait_inactive_on_unavailable_host_auto_continues` (suite: ungated 1-request continuation); mutants m7 (never enable), m8 (always enable) |
| AC8 explicit inheritance; headless child Unavailable | `ThreadManager::spawn_thread` → `inherited_async_notification_support` | `async_notification_child_of_available_parent_inherits_available`; `async_notification_roots_follow_host_session_source` (Cli/VSCode→Available; Exec/Mcp/Custom/Unknown→Unavailable); `async_notification_explicit_init_overrides_host_source` | `async_notification_child_of_headless_parent_stays_unavailable` (Internal child source, "not Exec", stays Unavailable); narrowing mutant m2 (derive from own session source) |

Out-of-contract rows: none. Every AC row is covered above; silence claims
nothing beyond this table.

Brief-gap report (handoff precondition 1): the producer brief carries no
surface table (`references/attack-surface-catalog.md` rows are not attached
to this task), so there is no surface-table coverage map. The final plan's
§12 research rows are plan-validation artifacts, not a brief surface table;
the AC-row map above is the operative coverage evidence.

## Commands and exit codes

Fast lane (from `codex-rs/`; target guard first):

- `/Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-target-guard.sh` → exit 0
- `python3 .../codex-fix-suite-busy.py --any` → `FREE` (before first build and before this handoff note)
- `cargo check -p codex-extension-api` → exit 0
- `cargo check -p codex-core` / `--tests` → exit 0
- `cargo check -p codex-goal-extension -p codex-app-server` (+ `--tests`) → exit 0
- `just clippy -p codex-extension-api -p codex-goal-extension` → exit 0
- `just clippy -p codex-core -p codex-app-server` → exit 0
- `just fix -p codex-core -p codex-goal-extension -p codex-extension-api -p codex-app-server` → exit 0 (also removed 3 pre-existing unused imports in files outside this leaf; reverted to keep the diff scoped)
- `just fmt` + `cargo fmt --check` → exit 0
- `just test -p codex-goal-extension` → exit 0, 71/71 pass, incl. new `background_wait_activation::background_wait_activates_only_on_available_hosts`
- `just test -p codex-extension-api` → exit 0, 12/12 pass

Targeted local run (local-build-allowance; gates: disk 79 GiB free ≥50,
CPU 79% idle ≥25%, memory 92% free ≥30%; after trim: 82 GiB free):

- `cargo nextest run -p codex-core --lib -E '<33 new lib tests>'` → first
  attempt exit non-zero: 30 pass, 2 fail on MY test expectations
  (`read_retained_output` after release returns `Cancelled{Released}`, not
  `UnknownReceipt` — the store retains terminal entries; the tool still
  reports "unknown or expired" because binding resolution fails first).
  Fixed the two expectations (no product change), re-ran with
  `--no-fail-fast`: exit 0, **33/33 pass, 2806 skipped**.
- `rm -rf /Users/iv/Developer/IV/codex-target/debug` after the run.

Not run locally (by design; hosted precheck requested):

- `codex-core` integration suites (`core/tests/suite/exec_notification.rs`,
  `goal_background_wait.rs` incl. AC7 tests) — written, compile-checked via
  `cargo check --tests` + clippy `--tests`, awaiting hosted CI.
- Mutant kills (9 narrowing mutants in `TASK-260929-3r7peh_mutants.json`,
  each validated with `git apply --check`) — awaiting hosted CI.

## Mutants (hosted precheck)

9 narrowing mutants, each preserving a valid case and naming its killer(s).
No survivors expected; none observed locally (mutants are not executed
locally by policy).

| Mutant | Narrows the gate to | Named killing test(s) |
|---|---|---|
| m1_arm_by_default | absent field arms; explicit false still clean | `exec_command_args_default_notify_on_exit_to_false`; suite `exec_notification_default_launch_arms_and_wakes_nothing` |
| m2_derive_child_from_not_exec | capability from own session source | `async_notification_child_of_headless_parent_stays_unavailable`; `async_notification_roots_follow_host_session_source` (Mcp arm) |
| m3_accept_opt_in_on_unavailable_host | one-shot refusal kept; host refusal removed | `notify_on_exit_refused_before_execution_on_unavailable_host`; suite `exec_notification_opt_in_refused_on_headless_exec` |
| m4_release_skips_mailbox_cancel | store release kept; wake cancel removed | `release_disarms_frees_slot_and_cancels_pending_wake` |
| m5_read_skips_owner_verify | binding resolve kept; thread/generation check removed | `read_rejects_foreign_receipt`; `notification_owner_resolves_launch_owner_across_tool_calls` |
| m6_handler_drops_opt_in | refusals kept; accepted opt-in launches default | suite `exec_notification_opt_in_arms_and_read_returns_terminal_output`, `exec_notification_capacity_refuses_65th_and_default_still_runs` |
| m7_goal_never_enables | activation removed | `background_wait_activates_only_on_available_hosts`; suite `background_wait_activation_gates_goal_but_admits_user_input` |
| m8_goal_always_enables | enable unconditional | `background_wait_activates_only_on_available_hosts` (Unavailable arm); suite `background_wait_inactive_on_unavailable_host_auto_continues` |
| m9_recheck_skips_retention_drop | single recheck kept except its retention drop; mailbox cancel + early return kept | `enqueue_published_completion_drops_ghost_retention` (ghost retention survives); `enqueue_published_completion_skips_disarmed_receipt` still passes (nothing retained there — proves narrowness) |

## Stated bounds and findings

- Interrupt/terminate/shutdown cancel store receipts but do not cancel
  mailbox entries (pre-existing deferred behavior). Post-exit terminate is
  moot; the residual interrupt-after-enqueue window delivers an already-
  occurred exit, which is arguably correct. Only `release` (AC5) cancels the
  mailbox entry.
- The enqueue helper has a single post-enqueue liveness recheck and
  cleans up (ghost retention drop + mailbox cancel) on a raced release; the
  residual release-between-recheck-and-wake window is shared with the
  pre-existing wake race. The mailbox additionally dedupes by receipt id, so
  watcher+arm double-enqueue is structurally impossible. A pre-enqueue gate
  existed in the precheck-1/2 candidate and was removed as redundant (it
  added no atomicity across the enqueue await); see the precheck-3 rework
  section.
- Tool owner resolution uses bindings only: retention re-inserted by a
  release-vs-exit race can never resurrect a readable subscription
  (proven by `enqueue_published_completion_drops_ghost_retention`).
- MCP/Custom/Unknown hosts stay `Unavailable` (fail closed); revisit only
  if MCP host persistence is verified.
- Goal `background_wait` enables at thread start regardless of the goal
  `enabled` flag: dormant while disabled, already correct if enabled later.
- Diff size ~3000 lines (logic ~450, tests ~2550) exceeds the 800-line
  review guidance; the leaf is an atomic activation (schema + tool +
  delivery + policy must land together; sibling F2 stacks on it) and cannot
  be staged further without shipping a half-promise.
- `just fix` side effects (3 unrelated unused-import removals) were
  reverted; the candidate contains only this leaf. No commits on the Story
  branch; work is uncommitted in the worktree for handoff snapshot.

## Handoff state

Code + tests are written, fast-lane gates are green, and 33/33 new lib tests
plus the goal/extension-api suites pass locally. Suite tests and mutant kills
need hosted CI on the exact candidate tree: `HOSTED-PRECHECK-REQUESTED` (see
task note) with `TASK-260929-3r7peh_mutants.json` attached. Checklist items
for passing tests, killed mutants, and handoff stay unchecked until that
evidence lands.

## F1 rework — hosted precheck 1 failures fixed (precheck 2 requested)

Precheck 1 (run 37600975837) verdict: small + app-server GREEN; lint
(`just fmt-check`) red; 3 `codex-core` suite failures. All three are test
bugs; production is unchanged by this rework (release does not kill, the
wake carries the fragment, the gate does not touch user turns — each
proven below). Only two test files changed:
`core/tests/suite/goal_background_wait.rs`,
`core/tests/suite/exec_notification.rs`.

### F0 — fmt
- Ran `just fmt`; `just fmt-check` now exits 0. `just clippy -p
  codex-core` exits 0 with the same 3-warning baseline, all in files
  outside this leaf (`core/src/tools/registry.rs`,
  `core/tests/suite/openai_file_mcp.rs`,
  `core/tests/suite/scenarios.rs`) — zero new warnings.

### F1 — user input "not admitted" while gated (test mock-topology bug)
- Root cause: wiremock serves same-priority mocks in mount order
  (`wiremock-0.6.5/src/mock_set.rs`: stable sort by priority, first match
  wins; `mock.rs`: "first one mounted has precedence"). The gate-phase
  sequence (mounted first, still hungry with `up_to_n_times(1)`) stole the
  user-turn request, so `user_mock.requests()` stayed 0 while the turn
  completed normally via the first mock. Production never gated the turn:
  `check_goal_admission` (`core/src/session/goal_admission.rs:54`)
  bypasses every non-`Automatic`/`goal` start without consulting the
  policy.
- Fix (test-only): one sequence for the whole test. Gate phase still
  asserts 0 requests (now with spare capacity, so a spurious continuation
  would be recorded — a real silence proof); user phase asserts exactly 1
  request AND that its user `input_text` contains "continue please"
  (`message_input_texts("user")`), proving the admitted request is the
  user turn's, not a gated continuation's.

### F2 — wake request "missing" the completion fragment (assertion bug)
- Root cause: the test searched `body_json().to_string()` (re-serialized
  JSON, quotes escaped as `\"`) for the raw `source="exec_completion"`
  wrapper, which can never match. The wake fired and carried the fragment;
  only the needle was wrong. Sibling suite `exec_completion.rs` checks
  unescaped texts for the same constant.
- Fix (test-only, same strength): `requests[2]
  .body_contains_text(EXEC_COMPLETION_WRAPPER)` — the repo helper that
  JSON-escapes the needle before searching. The local run proves the
  production path end to end (receipt → mailbox → idle wake → fragment in
  the sampled request).

### F3 — release test poll saw an exited process (timing flake + stdin finding)
- Root cause: `sleep 5` can elapse before the poll turn on a loaded
  machine. Release itself never kills: `release_completion_receipt`
  (store cancel + binding/retention drop) and `cancel_runtime_notification`
  (mailbox only) touch no process state — verified by reading, and proven
  by the passing live-poll below.
- First fix attempt (`read -r line` stdin gate) failed locally: stdin is
  EOF at spawn, so `read` returns immediately and the process exits.
- Final fix (test-only): the process is file-gated
  (`while [ ! -f .exec-notif-stop-<pid> ]; do sleep 0.2; done; echo done`;
  relative path, so both turns share the session cwd on local and remote
  executors; no new platform assumption beyond the file's existing POSIX
  commands). New tail: poll proves live → stale read proves expired →
  a default one-shot turn lands the stop file → a blocking
  `write_stdin` observe turn returns the terminal output, asserting
  `exited` + `done` (the echo proves the exit went through the gate —
  a spontaneous death would print nothing). No event wait can be missed
  however the exit interleaves with the turns.

### Strengthened silence proofs (same files, no loosening)
- Exact-count asserts on an exhausted `mount_sse_sequence` cannot observe
  a post-exhaustion request (unmatched → 404, unrecorded — the
  `ResponseMock` recorder is a matcher evaluated only on match). Both
  no-wake asserts (default-launch AC2, release AC5) now mount a trailing
  bare `mount_sse_once` sentinel (no `.expect`, so leaving it unconsumed
  passes drop-verification; default expectation range is unbounded) and
  assert 0 requests on it after exit + settle + 500ms grace. Any wake turn
  is recorded on the sentinel. The F1 gate-phase assert needs no sentinel
  (spare capacity in the single sequence already records strays).

### Local verification (this rework)
- Gates before the run: disk 74 GiB free (≥50), CPU 63.98% idle (≥25%),
  memory 92% free (≥30%). After trim (`rm -rf
  .../codex-target/debug`): disk 74 GiB free, memory 92% free.
- `cargo nextest run -p codex-core --test all -E
  'test(goal_background_wait) or test(exec_notification)'` → exit 0,
  **9 run, 9 passed, 2256 skipped** (3 goal_background_wait + 6
  exec_notification; full log `/tmp/f1/suite-run2.log` on the build host).
  An intermediate run during the rework exited non-zero (8 passed, 1
  failed: the `read`-gate variant, failing as analyzed above — output
  showed `Process exited with code 0` with `done`, proving stdin EOF at
  spawn); the file-gate run is green with exit 0.
- Mutant patches: all 9 re-verified with `git apply --check` against the
  reworked tree (production files untouched, patches byte-identical) —
  9/9 apply. m1/m7 suite killers remain the fixed tests (m1: armed-line
  assert still fails first under arm-by-default; m7: gate-phase 0-request
  assert fails when the policy never enables).
- Candidate left UNCOMMITTED in the Story worktree for snapshot.
- Not run: hosted precheck 2 (requested below) — the authoritative
  evidence for suite-green-on-candidate plus all 9 mutant kills.

## F1 rework 2 — hosted precheck 2 survivor m9 closed (precheck 3 requested)

Precheck 2 verdict (`f1-p2.ok`): all four lanes GREEN, 8 of 9 mutants killed.
One survivor: `m9_enqueue_skips_live_check` (removed the first
`is_live_queued_receipt` gate in `enqueue_published_completion`).

### Why old m9 survived (brief option-b analysis is unsatisfiable)

The intended killer `enqueue_published_completion_skips_disarmed_receipt`
passed under the mutant because the mutant was final-state-identical to the
base: the kept recheck also drops retention and cancels the mailbox entry,
so a disarmed receipt ends with no entry, no retention, and no wake either
way. `enqueue_runtime_notification`/`cancel_runtime_notification` leave no
other trace (`activity_tx` is a last-value watch channel; mailbox `cancel`
touches entries only). No final-state assertion can distinguish "skip up
front" from "enqueue then clean up on recheck", so strengthening the test's
final-state asserts (brief option b, literally) cannot kill that mutant.
The first gate was a pure optimization/transient-avoidance with no
atomicity (a release can land between it and the enqueue across the await),
so per the brief I took option (a).

### Production change (one file, net -4 lines)

`codex-rs/core/src/unified_exec/receipt_hooks.rs`,
`enqueue_published_completion`: removed the redundant pre-enqueue live-gate;
the post-enqueue recheck (ghost retention drop + mailbox cancel + early
return before the wake) is now the single load-bearing guard, and the doc
comment says so. Callers are unaffected (the helper returns `()`; both
production callers invoke it one-shot on live-`Queued` receipts; a second
call for one receipt is unreachable because publish/arm-to-`Queued` succeeds
at most once per receipt id). A disarmed receipt now transiently occupies the
mailbox between the enqueue and the recheck's cleanup (across the recheck's
lock awaits); the same transient already existed whenever a release landed
between the old first check and the enqueue, so this adds no new hazard
class — and the recheck still removes the entry before any wake this call
would start. No surviving entry, retention, or wake: the brief's invariant
("no retained output survives a disarm or release") holds and is asserted by
the tests below. No test file changed: both direct-helper tests already
assert the operative final states.

### Replacement mutant m9_recheck_skips_retention_drop

Removes ONLY the `self.receipt_hooks.lock().await.retention.drop(receipt_id);`
line from the single recheck (mailbox cancel + early return kept). Narrowing:
admission is exactly the ghost-retention member — no entry or wake survives,
only leaked output. Expected killer:
`enqueue_published_completion_drops_ghost_retention` (its
`retention.lookup(...) == RetentionLookup::Absent` assert fails: the ghost
stays `Present`). Kill audit — every other call on the mutant path is
read-only w.r.t. retention (verified by reading):
`retention.retained_sizes` takes `&self`;
`RuntimeMailbox::enqueue`/`cancel` mutate mailbox entries only and receive no
retention handle; `is_live_queued_receipt` reads `receipt_store.status`; the
early return skips the wake. `enqueue_published_completion_skips_disarmed_receipt`
still passes under the mutant (release already dropped its retention; mailbox
cancelled; read yields `Cancelled{Released}`), proving narrowness. All 9
mutant patches re-verified `git apply --check` clean against this tree
(m1–m8 byte-identical; old m9 retired).

### Local verification (this rework)

- Suite-busy probe before the first build: `FREE`.
- Target guard: exit 0 (same checkout, cache kept).
- `just fmt`: exit 0; `git status` shows the same file set (no fmt side effects).
- `just clippy -p codex-core`: exit 0; the same 3-warning baseline, all in
  untouched files (`core/src/tools/registry.rs`, `openai_file_mcp.rs`,
  `scenarios.rs`) — zero new warnings.
- Allowance gates before the run: disk 74 GiB free (≥50), CPU 70.57% idle
  (≥25%), memory 92% free (≥30%).
- `cargo nextest run -p codex-core --lib -E
  'test(enqueue_published_completion_skips_disarmed_receipt) or
  test(enqueue_published_completion_drops_ghost_retention)'` → exit 0,
  **2 run, 2 passed, 2837 skipped**.
- After trim (`rm -rf .../codex-target/debug`): disk 76 GiB free, memory
  92% free.
- Candidate left UNCOMMITTED in the Story worktree (HEAD still `2f522b9`)
  for snapshot. Mutants are not executed locally by policy; precheck 3 is
  the authoritative evidence for the base plus all 9 kills.

## Handoff refresh — hosted precheck 3 GREEN, 9/9 mutants killed (CR rev 1)

This section refreshes the outcome for handoff. No worktree file was changed
for this refresh (tree still `dbd39ab8c59adabe27ebb25838003680214c8d14`,
HEAD still `2f522b9dc9`, candidate uncommitted; verified with a temp index:
`GIT_INDEX_FILE=$(mktemp) git read-tree HEAD && git add -A && git write-tree`
prints `dbd39ab8c59adabe27ebb25838003680214c8d14`, MATCH).

### Precheck 3 verdict (authoritative evidence)

Source: `TASK-260929-3r7peh_hosted-precheck-3.md` (precondition).
Snapshot commit `74434fa5`, run `37618361186`, tree
`dbd39ab8c59adabe27ebb25838003680214c8d14` (equals this worktree tree).

- Lanes: lint success, core success, app-server success, small success.
  All four green on the exact candidate tree.
- Mutants: 9 total, 9 killed, 0 survivors.

### Mutant evidence (Standing Order 7)

Each mutant narrows its gate (weakens to admit exactly one member of the
rejected class); delete-only shapes were not used. Killing tests are quoted
from the precheck-3 report; expected killers are from
`TASK-260929-3r7peh_mutants.json`.

| Mutant | What it narrows the gate to | Named test(s) that fail (precheck 3) | Survivor bound |
|---|---|---|---|
| m1_arm_by_default | absent `notify_on_exit` arms; explicit false still clean | `_disabled_expects`, `_enabled_expects`, `_escalated_expects` (lanes app-server, core, small; report-truncated names) — expected: `exec_command_args_default_notify_on_exit_to_false`, suite `exec_notification_default_launch_arms_and_wakes_nothing` | killed, no survivor |
| m2_derive_child_from_not_exec | capability from own session source instead of explicit inheritance | `async_notification_child_of_headless_parent_stays_unavailable`, `async_notification_roots_follow_host_session_source`, `encrypted_parent_reply_survives_incremental_guardian_reviews` (lanes lint, core) | killed, no survivor |
| m3_accept_opt_in_on_unavailable_host | one-shot refusal kept; host-capability refusal removed | `exec_notification_opt_in_refused_on_headless_exec`, `notify_on_exit_refused_before_execution_on_unavailable_host` (lanes lint, core) | killed, no survivor |
| m4_release_skips_mailbox_cancel | store release kept; pending-wake cancel removed | `release_disarms_frees_slot_and_cancels_pending_wake` (lane core) | killed, no survivor |
| m5_read_skips_owner_verify | binding resolve kept; thread/generation check removed | `notification_owner_resolves_launch_owner_across_tool_calls`, `read_rejects_foreign_receipt` (lane core) | killed, no survivor |
| m6_handler_drops_opt_in | refusals kept; accepted opt-in silently launches default | `exec_notification_capacity_refuses_65th_and_default_still_runs`, `exec_notification_opt_in_arms_and_read_returns_terminal_output`, `exec_notification_release_disarms_without_killing` (lane core) | killed, no survivor |
| m7_goal_never_enables | activation removed; policy only manually enabled | `background_wait_activates_only_on_available_hosts`, `background_wait_activation_gates_goal_but_admits_user_input`, `scheduled_checkins_fire_through_production_runtime_under_paused_time` (lanes small, lint, core) | killed, no survivor |
| m8_goal_always_enables | capability read kept; enable unconditional | `background_wait_activates_only_on_available_hosts`, `background_wait_inactive_on_unavailable_host_auto_continues`, `scheduled_checkins_fire_through_production_runtime_under_paused_time` (lanes small, core) | killed, no survivor |
| m9_recheck_skips_retention_drop | single recheck kept except its retention drop; cancel + early return kept, only ghost output leaks | `enqueue_published_completion_drops_ghost_retention` (lane core) | killed, no survivor |

Survivors: none. Every mutant has at least one named failing test.

### Surface-table coverage map (handoff precondition 1)

The handoff run carries `surface-table.md` (4 rows). Each row maps to the
committed tests that exercise it and to at least one narrowing mutant those
tests kill (kill evidence: precheck 3 above). No row is uncovered.

| Surface row | Tests that exercise it | Narrowing mutant(s) killed |
|---|---|---|
| host capability | `async_notification_child_of_headless_parent_stays_unavailable`, `async_notification_child_of_available_parent_inherits_available`, `async_notification_roots_follow_host_session_source`, `async_notification_explicit_init_overrides_host_source`, `available_host_lists_exec_notification_and_notify_on_exit`, `unavailable_host_hides_exec_notification_and_notify_on_exit`, `exec_command_schema_gates_notify_on_exit_on_host_capability`, `notify_on_exit_refused_before_execution_on_unavailable_host`, suite `exec_notification_opt_in_refused_on_headless_exec` | m2 (derive-from-not-Exec killed by the headless-child test), m3 (accept-opt-in-on-unavailable killed by both refusal tests) |
| opt-in and receipts | `exec_command_args_default_notify_on_exit_to_false`, `default_launch_acknowledges_no_receipt`, `sixty_fifth_opted_in_launch_refused_before_execution`, suite `exec_notification_default_launch_arms_and_wakes_nothing`, suite `exec_notification_capacity_refuses_65th_and_default_still_runs` | m1 (arm-by-default), m6 (handler-drops-opt-in killed by both suite legs) |
| exec_notification read and release | `read_returns_retained_terminal_output`, `read_indicates_truncation_and_stays_under_token_bound`, `read_rejects_unknown_receipt`, `read_rejects_malformed_receipt_handle`, `read_rejects_foreign_receipt`, `read_rejects_stale_receipt_after_release`, `read_before_exit_is_rejected_without_waiting`, `release_disarms_frees_slot_and_cancels_pending_wake`, `opted_in_launch_arms_and_release_silences_later_exit`, `release_rejects_unknown_receipt`, `enqueue_published_completion_skips_disarmed_receipt`, `enqueue_published_completion_drops_ghost_retention`, suite `exec_notification_opt_in_arms_and_read_returns_terminal_output`, suite `exec_notification_release_disarms_without_killing`, suite `exec_notification_unknown_receipt_rejected` | m4 (release-skips-mailbox-cancel), m5 (read-skips-owner-verify), m9 (recheck-skips-retention-drop) |
| activation | `background_wait_activates_only_on_available_hosts`, suite `background_wait_activation_gates_goal_but_admits_user_input`, suite `background_wait_inactive_on_unavailable_host_auto_continues` | m7 (goal-never-enables), m8 (goal-always-enables) |

Correction to the earlier "Brief-gap report" paragraph above: it was written
when the producer brief carried no surface table. The handoff run attaches
`surface-table.md`, so the map in this section is now the operative
surface-table evidence; all 4 rows are covered with killed mutants.

### Handoff preconditions

1. Coverage map: AC map above is 8 of 8 rows driven through production entry
   points; surface-table map in this section covers all 4 rows with killed
   mutants. No uncovered row.
2. Landing-gate properties green: precheck 3, all four lanes green on this
   exact tree (run 37618361186).
3. Reviewer tests kept: no reviewer tests were previously committed for this
   task (first CR rev); nothing removed or renamed.
4. Out-of-contract rows: none. Every AC row and every surface-table row is
   covered above; silence claims nothing beyond these tables.
5. Rework diff bounded: precheck-2 rework touched only the two suite test
   files named in the F1 brief (`core/tests/suite/goal_background_wait.rs`,
   `core/tests/suite/exec_notification.rs`); precheck-3 rework touched only
   `core/src/unified_exec/receipt_hooks.rs` (net -4 lines, brief option a).
   Both are inside the leaf scope; nothing outside it.

### Checklist citation (this handoff)

- Item 1 (AC table detailed before spawn): the task carries AC1–AC8; checked.
- Item 3 (tests written and passing): fast lane + targeted local runs above,
  plus precheck-3 all-green on this tree; checked.
- Item 5 (n of m AC rows driven): 8 of 8, production call sites in the AC
  map; checked.
- Item 6 (negative tests for gates): refusal tests in the AC map (AC1/AC4/AC5
  negatives), all green in precheck 3; checked.
- Item 7 (narrowing mutant per gate): 9/9 killed, table above; checked.
- Item 8 (source-text gate): not applicable — no gate in this leaf inspects
  source text (gates inspect host capability, opt-in args, receipt slots,
  receipt ownership/generation, and goal enablement); vacuously satisfied,
  checked.
- Item 12 (logbook when relevant): findings, bounds, and rework analyses are
  recorded in this outcome (Stated bounds, F1 rework, m9 analysis sections);
  no control-root edit per the run write boundary; checked.
- Items 2, 4, 9, 10, 11 were already checked and remain true (code written,
  candidate uncommitted, lint clean per precheck-3 lint lane, builds green,
  outcome attached).

### Commands for this handoff run (no worktree writes)

- Temp-index tree check (read-only): MATCH
  `dbd39ab8c59adabe27ebb25838003680214c8d14` (exit 0).
- `git status --porcelain=v1`: 31 entries (26 modified + 5 new), HEAD
  `2f522b9dc9` — candidate uncommitted for snapshot.
- `python3 .../codex-fix-suite-busy.py --any`: see handoff note (FREE
  required before handoff).
- No cargo/just/fmt/clippy/test command was run in this handoff run, by
  instruction (do NOT change any file); all build/test evidence is the
  fast-lane/local runs recorded above plus hosted precheck 3 on this exact
  tree.
