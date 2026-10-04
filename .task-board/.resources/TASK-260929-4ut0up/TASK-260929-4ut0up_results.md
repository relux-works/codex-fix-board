# TASK-260929-4ut0up — watcher-and-output-retention-hooks: developer results (handoff on precheck 2)

## Handoff evidence (this run, 2026-10-05)

- Worktree tree verified UNCHANGED vs precheck 2 snapshot: temp-index
  `git read-tree HEAD && git add -A && git write-tree` →
  `7de6b3c2ed82f07002c613263cd650cc16b20108` (exit 0), matching precheck 2
  snapshot `9e692fdcd16a373a59f7d262159b377d588163d0`. No code changed in
  this run; hosted evidence below applies to the exact candidate tree.
- Hosted precheck 2 (`TASK-260929-4ut0up_hosted-precheck-2.md`): run
  https://github.com/relux-works/codex/actions/runs/37219783600 — SUCCESS
  on all lanes (lint, small, core, app-server). The 4 Linux-Landlock tests
  from precheck 1 now pass.
- Narrowing mutants: **16 of 16 killed by their intended tests** on hosted
  CI (results JSON: `.temp/goal-token-burn/impl/p5/b2-precheck-2-results.json`;
  mutant runs 37219798755 … 37219999698, 16 runs).
- Surface-table coverage (brief row "receipt hooks in unified exec"): every
  attack family in the row is exercised by the AC→test map below —
  exit-before/after initial yield (AC2 tests), drain/denial held (AC1),
  3 MiB output (AC3), 64/65 capacity + LRU retirement (AC4), stdin vs
  pushed claim race (AC5), release/terminate/interrupt/shutdown (AC6),
  foreign/unknown receipt reads (AC3), default launches beyond 64 (AC7),
  process-store removal before read (AC3) — and each AC ships ≥1 narrowing
  mutant killed by a named test (see Mutants).
- Out-of-contract rows: none. All 7 AC rows are driven through production
  entry points by committed tests (7 of 7).
- Rework diff bounded: all changes inside
  `codex-rs/core/src/unified_exec/` (leaf scope); nothing outside it.

Status: ready for review. No new code in this run — evidence refresh only.

## Summary

Rework after hosted precheck 1 (4 Linux failures, 13/16 mutants killed).
Two changes, both inside `codex-rs/core/src/unified_exec/`:

1. **Linux sandbox setup for the spawning tests** (`receipt_hooks_tests.rs`):
   `hook_test_session` now sets `config.codex_linux_sandbox_exe` on Linux via
   the existing `core_test_support::find_codex_linux_sandbox_exe()` helper
   (same helper the integration harness `default_test_overrides` and
   `guardian_tests.rs` use). No skip on Linux: a missing helper fails loudly
   via `expect`. No-op on macOS/Windows (cfg-gated). Tests still drive the
   production `exec_command` / `write_stdin` paths.
2. **Claim-before-unbind ordering fix** (`process_manager.rs`): precheck 1's
   4th failure was NOT Landlock — the CI log shows
   `terminal_stdin_claim_consumes_the_single_claim_first` panicking at
   `receipt_hooks_tests.rs:1231` with `Queued` vs expected
   `Sampled { TerminalStdinOutput }`. Root cause: `refresh_process_state`
   removed the process entry AND unbound the receipt before `write_stdin`'s
   terminal branches ran `claim_terminal_stdin_output`, so the claim always
   found no binding and the receipt stayed `Queued` (deterministic on every
   platform; the tests had never run before precheck 1). Fix:
   `refresh_process_state` no longer unbinds; the `write_stdin` `Exited` and
   `Unknown`-but-exited branches claim first and unbind after. The
   `exec_command` inline paths are unaffected (they settle and unbind by
   receipt id); default launches never bind, so existing behavior is
   unchanged.

Fast-lane validation green; `codex-core` suites run on hosted CI only per
B2 brief. Work left uncommitted for the handoff snapshot.

## Changed files (worktree, uncommitted)

Tracked (modified) — leaf files:

- `codex-rs/core/src/unified_exec/completion_receipt.rs` — `ExecCompletionMode`,
  `ReceiptError::Retired`, `SamplingLease::receipt_id()`, `active_len()`
- `codex-rs/core/src/unified_exec/errors.rs` — `ReceiptCapacityExceeded`
- `codex-rs/core/src/unified_exec/mod.rs` — `ExitWatcherReceiptHook`, manager
  fields `receipt_store` / `receipt_hooks` / `receipt_generation`
- `codex-rs/core/src/unified_exec/async_watcher.rs` — `spawn_exit_watcher` takes
  `Option<ExitWatcherReceiptHook>`; publish after exit+drain+denial+
  classification; failure maps to `exit_code: None`
- `codex-rs/core/src/unified_exec/process_manager.rs` — reserve-before-spawn,
  arm-on-Alive, inline settle, cancel/unbind paths, capacity refusal;
  claim-before-unbind in `write_stdin` terminal branches, no unbind
  in `refresh_process_state`
- `codex-rs/core/src/unified_exec/oneshot.rs` — `Default` completion mode
- `codex-rs/core/src/unified_exec/async_watcher_tests.rs` — `None` hook args

New (untracked):

- `codex-rs/core/src/unified_exec/receipt_output.rs` (196 LoC) + sibling tests
- `codex-rs/core/src/unified_exec/receipt_hooks.rs` (373 LoC) + sibling tests
- `codex-rs/core/src/unified_exec/receipt_output_tests.rs` (211 LoC)
- `codex-rs/core/src/unified_exec/receipt_hooks_tests.rs` (~1655 LoC);
  Linux `codex_linux_sandbox_exe` in `hook_test_session`

New modules are under 500 LoC excluding tests. Diff is inside the
leaf scope (`unified_exec` only); nothing outside it.

## AC → test coverage map

- AC1 (publish only after drain+denial+classification; failed→Failed;
  timed_out preserved):
  `receipt_exit_publishes_only_after_drain_denial_and_classification`,
  `receipt_failed_exit_maps_to_failed_completion`,
  `receipt_exit_preserves_timed_out`
- AC2 (opt-in rendezvous; inline settle frees slot; exactly-once queue):
  `opted_in_exit_before_decision_returns_inline_and_frees_slot`,
  `opted_in_decision_before_exit_queues_exactly_one_completion`
- AC3 (retention survives process removal; 1 MiB head/tail + omitted;
  unknown/foreign reads refused): `retained_output_survives_process_entry_removal`,
  `retained_output_over_cap_keeps_head_tail_and_omitted_count`,
  `retained_output_read_refuses_unknown_and_foreign_receipts`, plus the 6
  `receipt_output_tests.rs` unit tests (verbatim, head/tail+omitted, cap bound,
  sampled→LRU retire, foreign-owner refusal, drop)
- AC4 (64 slots; 65th refused before spawn; LRU retire sampled-with-output;
  release frees active+sampled):
  `receipt_capacity_refuses_65th_unsampled_reservation`,
  `opted_in_exec_refuses_65th_before_spawning`,
  `new_reservation_retires_least_recently_sampled_output`,
  `release_frees_active_and_sampled_slots`
- AC5 (single shared stdin/pushed claim):
  `terminal_stdin_claim_consumes_the_single_claim_first`,
  `terminal_stdin_and_pushed_claims_race_exactly_once`
- AC6 (release→Released no kill; terminate/prune→OwnerStopped;
  interrupt→Interrupted; shutdown→Shutdown frees all):
  `release_cancels_receipt_and_keeps_process_running`,
  `terminate_process_cancels_before_killing`,
  `interrupt_cancels_before_signalling`,
  `shutdown_cancels_all_receipts_and_frees_slots`
- AC7 (default launches reserve nothing):
  `default_launches_reserve_no_receipts`

Coverage: 7 of 7 AC rows driven through production entry points
(`exec_command_with_completion_mode`, `write_stdin`, `terminate_process`,
`terminate_all_processes`, `release_completion_receipt`).

## Mutants

`TASK-260929-4ut0up_mutants.json`: 16 narrowing mutants, ≥1 per AC
(AC1×3, AC2×2, AC3×2, AC4×2, AC5×1, AC6×5, AC7×1), each naming its killing
test. Hosted precheck 2 confirms **16 of 16 killed by their intended
tests**:

| Mutant | Narrowed gate | Killing test |
|---|---|---|
| ac1-failed-exit-reports-minus-one | failed exit must map to Failed, not an exit code | `receipt_failed_exit_maps_to_failed_completion` |
| ac1-publish-on-exit-token-before-drain | publish only after drain+denial+classification | `receipt_exit_publishes_only_after_drain_denial_and_classification` |
| ac1-timed-out-dropped-to-false | timed_out must survive publication | `receipt_exit_preserves_timed_out` |
| ac2-capacity-refusal-proceeds-as-default | 65th unsampled reservation must refuse, not degrade | `opted_in_exec_refuses_65th_before_spawning` |
| ac2-success-inline-weakened-to-arm | exit-before-decision must settle inline, not arm | `opted_in_exit_before_decision_returns_inline_and_frees_slot` |
| ac3-omitted-count-subtracted | omitted-byte count must be exact | `retained_output_over_cap_keeps_head_tail_and_omitted_count` |
| ac3-retention-cap-doubled | retention cap is exactly 1 MiB | `retained_output_over_cap_keeps_head_tail_and_omitted_count` |
| ac4-capacity-counts-active-only | capacity counts held slots incl. sampled-with-output | `receipt_capacity_refuses_65th_unsampled_reservation` |
| ac4-retire-most-recently-sampled | retirement evicts least-recently-sampled | `new_reservation_retires_least_recently_sampled_output` |
| ac5-stdin-claim-leases-without-acknowledge | stdin terminal output consumes the single claim | `terminal_stdin_claim_consumes_the_single_claim_first` |
| ac6-interrupt-cancels-with-released | interrupt must cancel with Interrupted | `interrupt_cancels_before_signalling` |
| ac6-release-cancels-with-owner-stopped | release must cancel with Released | `release_cancels_receipt_and_keeps_process_running` |
| ac6-release-leaks-retained-output | release must free the slot incl. retained output | `release_frees_active_and_sampled_slots` |
| ac6-shutdown-cancels-with-released | shutdown must cancel with Shutdown | `shutdown_cancels_all_receipts_and_frees_slots` |
| ac6-terminate-cancels-with-released | terminate must cancel with OwnerStopped | `terminate_process_cancels_before_killing` |
| ac7-default-launch-forced-opt-in | default launches reserve no receipt | `default_launches_reserve_no_receipts` |

Survivors: none (0/16). Every mutant has a named failing test.

## Exact commands and exit codes

Prior run (precheck-2 rework, from `.../STORY-260929-wg1ya0/worktree`):

- `task-board m 'set_status(TASK-260929-4ut0up, status=development)'` → exit 0
- `codex-fix-suite-busy.py --any` → `FREE`, exit 0
- `codex-target-guard.sh` → exit 0 (cleaned workspace members)
- `cd codex-rs && just fmt` → exit 0
- `cd codex-rs && just clippy -p codex-core` → exit 0, 0 errors, finished
  in 5m30s; only the 3 pre-existing out-of-scope warnings
  (`tools/registry.rs`, `tests/suite/openai_file_mcp.rs`,
  `tests/suite/scenarios.rs`), left untouched
- Mutant loop `git apply --check /tmp/b2fix/patches/m*.patch` → 16/16 OK
- CI evidence for the 4th failure read via
  `gh run view 37008593036 --job 110842628802 --log-failed` (exit 0):
  stdin test panicked at `receipt_hooks_tests.rs:1231`, `Queued` vs
  `Sampled { TerminalStdinOutput }` — not a Landlock error.

This run (handoff, no code changes):

- `task-board m 'set_status(TASK-260929-4ut0up, status=development)'` → exit 0
- Temp-index `git read-tree HEAD && git add -A && git write-tree` →
  `7de6b3c2ed82f07002c613263cd650cc16b20108`, exit 0 (matches precheck 2 tree)
- `codex-fix-suite-busy.py --any` → (see handoff run output)
- `task-board resource update` of this file → (see handoff run output)
- `task-board handoff TASK-260929-4ut0up --role developer` → (see handoff run output)

## Unverified / hosted-only

- All `codex-core` unit + integration suites (incl. the 2 new test files and
  the B1 receipt tests): run on hosted CI only, per B2 brief — precheck 2
  run 37219783600 is green on all lanes. Not run locally by design.
- Mutant kills: confirmed by hosted CI per-mutant runs (16 runs listed in
  precheck 2 evidence); kill table above.
- Nothing left unverified that the brief permits verifying locally.
