# TASK-261007-3v81ko results — fix-exec-tmpdir-cleanup (rev4 = landed tree)


## Rev4 = landed tree

Revision 4 is ready for review. The only change versus accepted revision 3 is
trunk's CI-only `.github/workflows/relux-ci.yml` patch: add `codex-arg0`
and `codex-cli` to the small snapshot and mutant lanes. No Rust code,
tests, persistent-state paths, or signal behavior changed.

The tracked recovery export was generated and attached as
`TASK-261007-3v81ko_landed-review-export.json`. Its `update_patch` touches
exactly one path, `.github/workflows/relux-ci.yml`. After
`worktree start-landed-rework` authorized rework, that exact patch was applied
without changes. The uncommitted worktree snapshot matches the signed landing:

- Previous candidate: `2f7ec5e30babb9dff4f00132ad9fd384663930b0`.
- Revision 4 snapshot / observed landing tree:
  `bde782b85ddbc8536536d0747b3917d0f24e1951`.
- Landing commit: `e0eff057620104a416080da616256ee7f32bda1b`.
- Export freshly verified signature status `G` and the exact current protected
  `relux/main` commit. PR #14 is merged at that same commit.

Hosted evidence accepted from prior execution (no local build/test rerun):
precheck 3 on the rev3 tree (run 38038510297: all four candidate lanes green,
5/5 narrowing mutants killed), plus exact-head landing relux-ci run
[38045370015](https://github.com/ivanopcode/codex/actions/runs/38045370015)
on `e0eff057`: lint, snapshot small, snapshot core, and snapshot app-server
all success. Both sets of job conclusions were read again with `gh run view`
(exit 0). Precheck 3's overall workflow conclusion is **failure**, expected:
its five small mutant jobs fail to demonstrate kills; the candidate jobs all
succeed. This is not represented as an overall passing workflow.

All 15 existing checklist items were left unchanged. The coverage map, mutant
kill table, and explicit signal/abort bounds below still apply: Ctrl-C routes
through graceful shutdown but OS delivery is untested; SIGTERM, SIGKILL, and
abort do not clean up and remain bounds. The original report's eight `.tmp*`
per successful run was not reproduced locally and is not claimed reproduced
by this recovery.

Commands run in this recovery (real exit codes):

- Required first `set_status(..., status=integrating)`: 0.
- `task-board worktree prepare-landed-review STORY-261007-1cpzdo --cr
  TASK-261007-3v81ko --revision 3 --landed-commit e0eff057620104a416080da616256ee7f32bda1b
  --json` (redirected to the specified export path): 0.
- Export update-patch path assertion: 0 (only relux-ci.yml).
- Export resource attachment: 0.
- `task-board worktree start-landed-rework STORY-261007-1cpzdo --cr
  TASK-261007-3v81ko --revision 3 --landed-commit e0eff057620104a416080da616256ee7f32bda1b
  --export /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/leak-landed-review.json`: 0.
  The transaction routed the task to `to-dev` for the new revision.
- Temp-index `git read-tree HEAD`, `git add -A`, and `git write-tree`:
  each 0 before applying (rev3 tree), after applying, and after rustfmt
  (both rev4 tree). No commits or branch changes.
- `git apply --check -` and `git apply -`, each using the export's exact
  update_patch on stdin: each 0.
- `git diff --name-only 2f7ec5e30babb9dff4f00132ad9fd384663930b0
  bde782b85ddbc8536536d0747b3917d0f24e1951`: 0; exactly relux-ci.yml.
- `git diff --check`: 0.
- Initial `cargo fmt -- --config imports_granularity=Item` and same with
  `--check`: each 127 (`cargo` absent from shell PATH). Corrected by using
  `/Users/administrator/.cargo/bin/cargo` for both commands: each 0, expected
  stable-channel imports_granularity warnings. Rust files remained byte-identical.
- `gh pr view 14 --repo ivanopcode/codex --json
  headRefOid,mergeCommit,statusCheckRollup,url,state`: 0 (merged exact commit).
- `gh run list --repo ivanopcode/codex --commit e0eff057620104a416080da616256ee7f32bda1b
  --json databaseId,workflowName,status,conclusion,headSha,url --limit 10`: 0,
  empty; workflow_dispatch records use the workflow ref as headSha, not the
  candidate being tested. Workflow-scoped listing (exit 0) found the landing run.
- `gh run view 38045370015 --repo ivanopcode/codex --json
  conclusion,displayTitle,jobs,url`: 0; all candidate lanes success.
- `gh run view 38038510297 --repo ivanopcode/codex --json
  conclusion,jobs,url`: 0; candidate lanes success, five expected-red small
  mutant jobs failure (5/5 killed per attached precheck record).
- `command -v logbook`: 1, executable unavailable. Recovery decision and
  validation anomaly are recorded here and in the task note instead.

No local Rust builds, clippy, or tests were run, per the Mac mini restriction.
Every temporary snapshot-index directory created by this run was deleted by
its context manager. Evidence files live under the existing task evidence
path outside the candidate worktree. No real CODEX_HOME was read/copied and
no installed codex binary was run. No complete/integrate/checkpoint command
was invoked. Handoff is the next board command after evidence and notes.

## Historical revision 3 handoff statement

CR rev3 is ready for review. Hosted precheck 3 (run 38038510297,
`TASK-261007-3v81ko_hosted-precheck-3.md`) ran the exact candidate tree
`2f7ec5e30babb9dff4f00132ad9fd384663930b0`: all four lanes green
(lint/small/core/app-server; small 932 passed, including both new
`/dev/full` stderr-failure tests), 14 new tests pass, 5/5 narrowing
mutants killed, 0 survivors. This run changed no file: the worktree tree
still equals `2f7ec5e3...` (temp-index check, exit 0; `git diff
--name-only` empty), so precheck 3 evidence applies verbatim. All 15
checklist items remain checked, citing that run.

## Summary of changes (rev1 + rev2 + rev3)

Rev1 removed 13 `process::exit(1)` calls from `codex-rs/exec/src/lib.rs` so
TempDir guards drop. Rev2 (review rev1 rework) kept the guard-dropping
mechanism with exact bytes (silent exits, clap `try_parse`) and hardened
the test oracles. Rev3 (review rev2 rework, one finding A2-F1) delegates
ordinary-error reporting back to std's `Termination` so a failing stderr
cannot panic:

- `codex-rs/arg0/src/silent_exit.rs`: replaced `exit_code_from_result(...
  ) -> ExitCode` with `exit_result_from_result(...) -> Result<ExitCode,
  anyhow::Error>`. Silent exits map to `Ok(code)` with no output; all
  other errors return `Err(err)` so std's `Termination` prints
  `Error: {Debug}` and returns `FAILURE`, ignoring write failures exactly
  like the base `fn main() -> anyhow::Result<()>`. Guards drop inside
  `arg0_dispatch_or_else` before this mapping runs.
- `codex-rs/arg0/src/lib.rs`: export rename only.
- `codex-rs/exec/src/main.rs` + `codex-rs/cli/src/main.rs`: outer `main`
  now returns `Result<ExitCode, anyhow::Error>` via the new helper. Inner
  `try_parse()` + `err.print()` + silent code unchanged.
- `codex-rs/exec/src/lib.rs`: untouched in rev3 (13 silent sites unchanged).
- Normal bytes/codes unchanged by construction:
  `Result<ExitCode, E: Debug>` `Termination` uses the same `Err` printing
  path as the base `Result<(), E: Debug>`; existing full-stderr tests pass
  unchanged (precheck 3 green).
- 2 new regression tests run a public binary on an ordinary-error path
  with stderr attached to `/dev/full`, asserting exit 1 (not panic 101)
  plus no leaks; both skip with a clear message where `/dev/full` is
  absent.

## Changed files

- `codex-rs/arg0/src/silent_exit.rs` (rev2 new; rev3: Termination delegation)
- `codex-rs/arg0/src/lib.rs` (export only)
- `codex-rs/exec/src/lib.rs` (13 sites: exact original `eprintln!` + silent return)
- `codex-rs/exec/src/main.rs` (`Result<ExitCode, anyhow::Error>` outer, `try_parse` + `err.print()` inner)
- `codex-rs/cli/src/main.rs` (same dispatcher fix for `MultitoolCli`)
- `codex-rs/exec/tests/suite/tmpdir_cleanup.rs` (rev2: 10 tests; rev3: +1 `/dev/full` test)
- `codex-rs/cli/tests/exec_tmpdir_cleanup.rs` (rev2 new, 2 tests; rev3: +1 `/dev/full` test)
- `codex-rs/exec/tests/suite/mod.rs` (rev1 registration, unchanged since)

## Coverage map (AC → driving test → refusal test)

| AC | Driving test | Refusal / mutant |
|---|---|---|
| AC1: N exec runs, isolated TMPDIR, 0 `.tmp*` | `exec_success_leaves_no_tmpdirs`, `exec_server_error_leaves_no_tmpdirs`, `exec_empty_stdin_leaves_no_tmpdirs` (empty `tmp_entries` + no `codex-arg0*` leak + setup proof). All pass in precheck 3. | `error_seen_process_exit` killed by `exec_server_error_leaves_no_tmpdirs`; `empty_stdin_process_exit` killed by `exec_empty_stdin_leaves_no_tmpdirs`. |
| AC2: success + error exits; signal/abort bound | Success leak test; error exits 1 (`server_error`, `empty_stdin`, `config_error` stderr tests); parser exits 0/2; stderr-failure exits 1 (not 101). Signal: stated bound below. | `exec_parse_exit` killed by `exec_help_leaves_no_tmpdirs` + `exec_invalid_args_leave_no_tmpdirs`; `empty_stdin_error_prefix` killed by `exec_empty_stdin_preserves_stderr`; `stderr_failure_eprintln` killed by both `/dev/full` tests. |
| AC3: regression fails pre-fix; narrowing mutants killed | Leak tests fail on pre-fix `process::exit` code; stderr tests fail on rev1 `bail!` code; `/dev/full` tests fail (exit 101) on rev2 `eprintln!` code. | 5/5 killed in precheck 3, 0 survivors (see table below). |
| AC4: CODEX_HOME persistent state unchanged | Only exit mechanics + tests change; no `find_codex_home`/sqlite/session/store path changes. Existing `prompt_stdin`/`server_error_exit`/`mcp_required_exit` substring assertions still pass (precheck 3 green). | — |
| AC5: hosted relux-ci green on exact candidate tree | Precheck 3 run 38038510297 on tree `2f7ec5e3...`: lint/small/core/app-server all success. | — |

Mutant kills (precheck 3, lanes small+core):

| mutant | killing tests |
|---|---|
| `empty_stdin_error_prefix` | `exec_empty_stdin_preserves_stderr` |
| `empty_stdin_process_exit` | `exec_empty_stdin_leaves_no_tmpdirs`, `exec_empty_stdin_preserves_stderr` |
| `error_seen_process_exit` | `exec_server_error_leaves_no_tmpdirs`, `exec_server_error_preserves_stderr` |
| `exec_parse_exit` | `exec_help_leaves_no_tmpdirs`, `exec_invalid_args_leave_no_tmpdirs` |
| `stderr_failure_eprintln` (new, rev3) | `exec_ordinary_error_stderr_failure_preserves_exit_code`, `cli_exec_stderr_failure_preserves_exit_code` |

## Review rev2 finding closed (A2-F1)

- A2-F1 (stderr write failure must not panic; row `exit status and
  observable behavior`, severity regression): rev2's `eprintln!` for
  ordinary errors panicked on a failing stderr (exit 101), while the base
  `anyhow::Result` `Termination` ignores write failures (exit 1). Rev3
  returns `Err(err)` from `main` so std prints it, after the TempDir
  guards have dropped. Public-binary regression tests:
  `exec_ordinary_error_stderr_failure_preserves_exit_code`
  (`codex-exec --worktree --ephemeral`, ordinary bail at
  `exec/src/lib.rs:303`) and
  `cli_exec_stderr_failure_preserves_exit_code`
  (`codex --remote ws://127.0.0.1:1 exec`, ordinary bail at
  `cli/src/main.rs:2158`), both with stderr on `/dev/full` (Linux CI;
  skip with a clear message where absent), both asserting exit 1 + no
  leaks. Narrowing mutant `stderr_failure_eprintln` (back to `eprintln!`,
  same normal bytes/code, panics on `/dev/full`) is killed by both tests.
  Panels B and the delta reviewer had already accepted rev2; this was the
  only remaining finding. Closed by precheck 3.

## Review rev1 findings closed (A-F1..A-F4 + F1, carried from rev2)

- A-F2 (stderr regression): silent-exit path restores exact bytes.
  Full-string `assert_eq` on whole stderr: empty-stdin
  (`"Reading prompt from stdin...\nNo prompt provided via stdin.\n"`),
  config error, server error (no extra `Error:` line). Mutant
  `empty_stdin_error_prefix` killed. Closed by precheck 2, still green in
  precheck 3 (tests pass unchanged).
- A-F1 + F1 (clap parser bypass): `try_parse` + `err.print()` + silent
  code in both dispatchers. Parser tests assert no leak AND unchanged
  output/exit code (exit 2 invalid args, exit 0 help; multitool pair in
  cli tests). Mutant `exec_parse_exit` killed. `--version` shares the
  help path but has no dedicated test; stated bound.
- A-F3 (oracle robustness): oracles panic on any read/entry error (2
  `should_panic` attack tests); sibling home outside TMPDIR; every test
  asserts setup-exercised (arg0 root is a dir + no alias warning) before
  claiming clean.
- A-F4 (signal bound): corrected below; no code change.

## AC2 signal/abort bound (explicit, truthful per A-F4)

- Ctrl-C (`SIGINT`): the exec path subscribes ONLY to
  `tokio::signal::ctrl_c` (`exec/src/lib.rs`, interrupt channel →
  turn/interrupt + graceful shutdown → returns through `main`, so guards
  drop). No test drives OS signal delivery (no signal-injection harness in
  the hosted lanes); delivery itself is unverified, the routing mechanism is
  present in source.
- `SIGTERM`: NOT handled on this exec path. The in-process app server
  (`InProcessAppServerClient::start` → `app-server in_process::start`)
  installs no SIGTERM subscription; the SIGTERM handler in
  `app-server/src/lib.rs` belongs to the separate transport-server runner.
  Default SIGTERM action terminates without running destructors, so TempDir
  guards leak. Stated bound, not fixed (AC2 permits a stated bound).
- `SIGKILL`/abort: terminate without destructors by construction; out of
  scope. Stated bound.

## Out-of-scope bounds (explicit)

- Non-exec `process::exit` sites in `cli/src/main.rs` (TUI fatal exit,
  app-server forced exit 0, login credential errors) are separate subcommand
  paths, not `codex exec`; left untouched.
- `--version` shares the fixed clap help path (code 0, stdout) but has no
  dedicated no-leak test; `--help` covers the mechanism.
- The multitool dispatcher has killer-capable tests but no dedicated mutant
  (the rework brief scoped one dispatcher mutant; the mechanism is shared).
- The issue's 8-per-run `.tmp*` on success was not reproduced with 0.159.0
  here; the fix removes the destructor-skipping mechanism for all held
  guards and the tests guard both `.tmp*` and arg0 invariants.
- `/dev/full` tests run on Linux CI; on Windows they skip with a clear message.

## Commands (exact, with exit codes)

This handoff run (no file changes; Mac mini: no cargo build/check/clippy/test):

- `task-board m 'set_status(TASK-261007-3v81ko, status=development)'` → exit 0.
- `git rev-parse HEAD` → `07c018be3507b8d4a5558a85a117b94ed2a23872`, exit 0.
- Temp-index `git read-tree HEAD && git add -A && git write-tree` → exit 0,
  tree `2f7ec5e30babb9dff4f00132ad9fd384663930b0` (equals precheck 3 snapshot).
- `git diff --name-only 2f7ec5e3... 2f7ec5e3...` → empty, exit 0.
- Rev3 authoring run (prior turn): `cargo fmt -- --config
  imports_granularity=Item` → exit 0; same with `--check` → exit 0;
  `git apply --check` on all 5 mutant patches → OK.
- Hosted precheck 3 run 38038510297: lint/small/core/app-server success;
  5/5 mutants killed (evidence: `TASK-261007-3v81ko_hosted-precheck-3.md`).

## Unverified

- OS-signal delivery to the exec binary is unverified (see bound above).
- No local compilation or test execution (Mac mini R194/R223); all Rust
  behavior evidence is hosted precheck 3 on the exact tree.
