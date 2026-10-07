# Coverage map — TASK-260929-3f6hfg goal-background-wait-vertical-test

Surface rows from the brief's `surface-table.md`, in order. Every row
names attacking tests and at least one killed narrowing mutant
(hosted precheck 1, worktree tree
`c83869e576d1e024cfdbb5f63cfe8b83c6e969cb`, base run 37633617318 all
lanes green). Test paths are
`codex-rs/app-server/tests/suite/v2/goal_background_wait.rs`
(`suite::v2::goal_background_wait::`).

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| controlled-exit vertical | `notified_exec_exit_wakes_gated_goal_with_receipt_fragment` (AC1/AC2/AC3: pre-release count 2, post-release count 4 with `source="exec_completion"` + `receipt_id` + `exit_code: 0`, goal `Complete`) | `silence-ignores-armed` → `notified_exec_…` (`:357`, run 37633736582, 3/3 tries); `drop-wake` → `notified_exec_…` + `user_burst_…` (run 37633707303); `wake-without-fragment` → `notified_exec_…` (`:357`) + `user_burst_…` (`:458`) (run 37633768227, 3/3 tries each) | check-in timers/warning (AC1–AC3 hold seconds; core-level); restart/resume rearming (not in AC); in-turn arbitrary polling (§11 stated bound); Windows-host barrier run (AC7 targets hosted Linux lane) |
| negatives | `headless_host_refuses_notify_on_exit_and_promises_no_wake` (AC4: no schema advertisement, refusal text, ungated continuation); `unopted_server_process_does_not_gate_goal_continuation` (AC5: no ack, continuation while wedged); `user_burst_during_background_wait_admitted_without_loss_or_duplication` (AC6: 2 turns admitted, exact texts, wake follows) | `allow-notify-on-incapable-host` → `headless_host_…` (run 37633645894); `always-subscribe` → `unopted_server_…` (run 37633676266) | `thread/queue/*` API path for AC6 (AC allows "queued **or** burst"; burst driven; queue API is a separate experimental surface) |
| harness quality | all 4 tests: release-file barrier with sh/PowerShell variants, zero test-side sleeps (notification/RPC-round-trip/bounded-timeout waits only); `TestAppServer::builder` + `send_thread_start_request_with_auto_env`; `skip_if_remote!`/`skip_if_wine_exec!` with stated reasons | all 5 mutant patches above target production files only (`ext/extension-api/src/pending_work.rs`, `core/src/unified_exec/async_watcher.rs`, `core/src/hook_runtime.rs`, `core/src/tools/handlers/unified_exec/exec_command.rs` ×2) — no test-code mutants; each is narrowing (gate stays, admits exactly one reject-class member), not delete-only | none claimed: no silent skips (barrier skips are explicit macros with reasons; headless test runs on every lane) |

Survivors: 0 of 5. No row is uncovered; no silent waiver.
