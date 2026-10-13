# TASK-261007-3v81ko precheck 3 request — review rev2 rework (A2-F1)

## Final tree

- Tree: `2f7ec5e30babb9dff4f00132ad9fd384663930b0` (temp index: `git read-tree HEAD`, `git add -A`, `git write-tree`, exit 0)
- HEAD: `07c018be3507b8d4a5558a85a117b94ed2a23872` (same trunk as precheck 2, no moves)
- Status: UNCOMMITTED, no file changes after tree computation
- Note added: `HOSTED-PRECHECK-REQUESTED: precheck 3`

## What changed (A2-F1 fix)

Finding: `silent_exit.rs:63` used `eprintln!` for ordinary errors, which panics
on failing stderr, while base `fn main() -> anyhow::Result<()>` used
`Termination`, which ignores write failures.

Fix (delegate to `Termination`, guards-drop order preserved):

- `codex-rs/arg0/src/silent_exit.rs`: replaced `exit_code_from_result(...) ->
  ExitCode` with `exit_result_from_result(...) -> Result<ExitCode,
  anyhow::Error>`. Silent exits map to `Ok(code)` with no output; all other
  errors return `Err(err)` so std's `Termination` prints `Error: {Debug}` and
  returns `FAILURE`, ignoring write failures exactly like the base. Guards are
  dropped inside `arg0_dispatch_or_else` before this mapping runs.
- `codex-rs/arg0/src/lib.rs`: export rename only.
- `codex-rs/exec/src/main.rs`, `codex-rs/cli/src/main.rs`: outer `main` now
  returns `Result<ExitCode, anyhow::Error>` via the new helper. Inner
  `try_parse` + `err.print()` + silent code unchanged. `exec/src/lib.rs`
  untouched (13 silent sites unchanged).
- Normal bytes unchanged by construction: `Result<ExitCode, E: Debug>`
  `Termination` uses the same `Err` printing path as the base
  `Result<(), E: Debug>`. Existing full-stderr tests must still pass unchanged.

## New tests (2)

Both run a public binary on an ordinary-error path with stderr attached to
`/dev/full`, assert exit 1 (not panic 101) plus no leaks, and skip with a clear
message where `/dev/full` is absent (Windows). Both names contain
`stderr_failure` for the mutant filter.

- `codex-rs/exec/tests/suite/tmpdir_cleanup.rs::exec_ordinary_error_stderr_failure_preserves_exit_code`:
  `codex-exec --worktree --ephemeral` (ordinary bail at `exec/src/lib.rs:303`,
  before any other output). Uses `std::process::Command` with
  `stderr(Stdio::from(/dev/full))`. Setup proof via existing arg0 root
  (`is_dir`; the CODEX_HOME-under-TMPDIR refusal returns before creating it);
  warning-free check unavailable since stderr is discarded. Then empty
  `.tmp*` + no `codex-arg0*` leak asserts.
- `codex-rs/cli/tests/exec_tmpdir_cleanup.rs::cli_exec_stderr_failure_preserves_exit_code`:
  `codex --remote ws://127.0.0.1:1 exec` (ordinary bail at
  `cli/src/main.rs:2158` via `reject_remote_mode_for_subcommand`). Same
  `/dev/full` contract and arg0 leak asserts.

No other test files changed. Total new tests: 14 (12 from rev2 + 2 here).

## Mutants (5, all `git apply --check` clean on final tree)

Kept 4 from precheck 2 (3 lib.rs verbatim; `exec_parse_exit` rebased to the
new `fn main() -> Result<...>` signature); added 1 narrowing mutant for A2-F1.
See `TASK-261007-3v81ko_mutants.json` (updated).

| mutant | patch summary | expected killer test(s) |
|---|---|---|
| `error_seen_process_exit` | lib.rs error_seen back to `process::exit(1)` | `exec_server_error_leaves_no_tmpdirs`, `exec_server_error_preserves_stderr` |
| `empty_stdin_process_exit` | lib.rs empty stdin back to `process::exit(1)` | `exec_empty_stdin_leaves_no_tmpdirs`, `exec_empty_stdin_preserves_stderr` |
| `empty_stdin_error_prefix` | lib.rs empty stdin back to `bail!` (`Error:` prefix) | `exec_empty_stdin_preserves_stderr` |
| `exec_parse_exit` | exec main.rs back to `TopCli::parse()` (updated context) | `exec_help_leaves_no_tmpdirs`, `exec_invalid_args_leave_no_tmpdirs` |
| `stderr_failure_eprintln` (new) | silent_exit.rs ordinary branch back to `eprintln!` + `Ok(FAILURE)` (same normal bytes/code, panics on `/dev/full`) | `exec_ordinary_error_stderr_failure_preserves_exit_code`, `cli_exec_stderr_failure_preserves_exit_code` |

The new mutant preserves normal exit codes and stderr bytes; it is killed only
by the `/dev/full` exit-1 assertion (mutant exits 101). Killer-test filter:
existing `test(tmpdir_cleanup) | test(tmpdir) | test(stderr) | test(exit_code)`
plus `test(stderr_failure) | test(dev_full) | test(no_panic)` already covers
both new tests (both contain `stderr_failure`). No other pattern needed.

## Commands (exact, with exit codes)

Mac mini: no cargo build/check/clippy/test (R194/R223). `cargo` via
`$HOME/.cargo/bin` (PATH did not include it).

- `task-board m 'set_status(TASK-261007-3v81ko, status=development)'` → exit 0
- `cargo fmt -- --config imports_granularity=Item` (from `codex-rs/`) → exit 0
  (expected nightly-only `imports_granularity` warnings)
- `cargo fmt -- --config imports_granularity=Item --check` → exit 0 (same warnings)
- `git apply --check` on each of the 5 mutant patches → all exit 0
- `git read-tree HEAD; git add -A; git write-tree` → exit 0, tree `2f7ec5e3...`
- `grep exit_code_from_result` → no references remain; `exit_result_from_result`
  in arg0 lib + silent_exit + both mains only

## Precheck 3 ask

Run slim relux-ci on tree `2f7ec5e30babb9dff4f00132ad9fd384663930b0` (snapshot)
plus the 5-mutant matrix (lanes small+core, or as before). Expected: 4 lanes
green on snapshot (14 new tests pass, including 2 new `/dev/full` tests on
Linux); 5/5 mutants killed, 0 survivors. Then resume this task with
`TASK-261007-3v81ko_hosted-precheck-3.md` for checklist + handoff (CR rev3).
No handoff in this turn per rework brief.

## Unverified (hosted only)

- No local compilation or test execution (Mac mini). All Rust behavior evidence
  awaits hosted precheck 3 on the exact tree.
- `/dev/full` tests run on Linux CI; on Windows they skip with a clear message.
- OS-signal delivery still unverified; SIGTERM/SIGKILL/abort bound from rev2
  results unchanged.
