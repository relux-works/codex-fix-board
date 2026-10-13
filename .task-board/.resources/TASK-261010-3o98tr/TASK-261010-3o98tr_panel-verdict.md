# R141 DELTA panel — CR-TASK-261007-3v81ko-2 revision 2

accept

Replay check: PASS. Base `07c018be3507b8d4a5558a85a117b94ed2a23872` plus the attached revision-2 patch, applied through a temporary index, produced exactly `ca07d336e99eb0ddcb15a180bbaaaf2a45388835`. No nested worktree, product edits, builds, local Rust tests, commits, or recording-review operations were performed. Every source citation below refers to this candidate tree, also represented by hosted snapshot commit `98ae625bdd680caf632828105d807d8723e163e8`.

## Commands and exit codes

Commands executed by this panel, from the assigned Story worktree:

| Command | Observed exit / result |
|---|---|
| `task-board m 'set_status(TASK-261010-3o98tr, status=analysis)'` | 0; panel task only |
| `mkdir -p .temp` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o98tr-replay.idx" git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872` | 0 |
| `task-board resource get TASK-261007-3v81ko TASK-261007-3v81ko_change-request_rev2.patch --output .temp/TASK-261007-3v81ko_change-request_rev2.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o98tr-replay.idx" git apply --cached .temp/TASK-261007-3v81ko_change-request_rev2.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o98tr-replay.idx" git write-tree` | 0; exact expected candidate tree |
| `git diff --check 07c018be3507b8d4a5558a85a117b94ed2a23872 ca07d336e99eb0ddcb15a180bbaaaf2a45388835` | 0 |
| `git diff --stat`, `git diff --numstat`, and scoped `git diff`, with the same base/tree pair | Each 0; eight paths, 668 additions / 58 deletions |
| Candidate `git show` reads and scoped `git grep` searches for exits, parser calls, TempDir ownership, keep/forget, and signals | Each 0; source reads, not execution tests |
| Python source-excerpt and prior-verdict JSON-reading scripts | Each 0; all five prior findings read |
| Python base/candidate exit-site count | 0; `exec/src/lib.rs` has 13 `std::process::exit(1)` sites on the base and 0 on the candidate |
| `git status --short` | 0; clean before creating this outcome |
| `python3 .temp/validate-panel-verdict.py` | 0; exactly one JSON block, five unique surface results, all five prior finding IDs, one-word verdict, and replay/command evidence verified |
| `task-board q 'get(TASK-261007-3v81ko) { description scope ac notes }'` | 0 |
| `task-board q 'get(TASK-261007-3v81ko) { preconditionResources outcomeResources }'` | 0 |
| `task-board resource get` for `surface-table.md`, previous merged verdict, producer results/brief, revision-2 validation log, hosted-precheck-2 report, and mutants JSON, each to `.temp/` | Each 0; read-only downloads |
| `task-board q 'get(TASK-261010-3o98tr) { checklist }'` | 0 |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` (three checkpoints) | Each 0; no directives |
| `gh run view 38021154057 --repo ivanopcode/codex --json headSha,status,conclusion,jobs,url` and the compact `--jq` projection | Each 0; four snapshot lanes success; four mutant small lanes failure |
| `gh run view 38021154057 --repo ivanopcode/codex --job JOB --log > .temp/LOG` for jobs `114123649089`, `114122236757`, `114123649003`, `114123649027`, `114123649031`, `114123649084` | Each 0; logs retrieved without running the hosted commands locally |
| `gh api repos/ivanopcode/codex/git/commits/98ae625bdd680caf632828105d807d8723e163e8 --jq '{sha,tree:.tree.sha}'` | 0; tree equals candidate exactly |
| `gh api repos/ivanopcode/codex/compare/98ae625bdd680caf632828105d807d8723e163e8...MUTANT --jq '[.files[]\|{filename,patch}]'` for all four mutant commits below | Each 0; each hosted diff matches the corresponding attached one-site mutant |
| `rg`, `sed`, `head`, `tail`, `cat`, and Python inspection of downloaded inputs/logs | Successful reads/searches exited 0, except discovery failures listed below |

Non-gate discovery failures are not passes: the initial query using unknown field `resources` exited 1; a second query using unknown field `attachments` exited 1. `task-board resource list` exited 0 but displayed help rather than a resource list; it was replaced with the successful resource projection. The combined skill-reference read exited 1 because its reviewer-role path was missing, although the negative-evidence reference was readable. Four scoped role/AGENTS/logbook file searches exited 1 (no matches); the role was subsequently read successfully from `/Users/administrator/.roles/reviewer/role.md`. `command -v logbook` exited 1. These do not establish any validation failure or success. The task's explicit panel contract supplies the surface sweep and non-recording rules.

The artifact validation, attachment and researcher handoff are separate panel lifecycle operations; their actual results are recorded in this task's activity/run transcript. No future command is asserted green here.

## Hosted execution evidence accepted, not rerun locally

Primary source: [relux-ci run 38021154057](https://github.com/ivanopcode/codex/actions/runs/38021154057). Its overall conclusion is **failure**, as expected for a workflow containing killing mutant jobs. It is not an all-green workflow. Candidate jobs `lint`, `snapshot small`, `snapshot core`, and `snapshot app-server` are success (4/4); all four mutant small jobs fail with explicitly logged exit **100**. The workflow controller head `2543194083e87e51973c6d60dfa7b40f386fb9fa` is distinct from the tested snapshot: checkout logs for snapshot small and lint pin `98ae625bdd680caf632828105d807d8723e163e8`, whose GitHub Git API tree equals the replay tree.

The [snapshot small log](https://github.com/ivanopcode/codex/actions/runs/38021154057/job/114123649089) records this command, followed by 930 tests run, 930 passed, 1 skipped:

`INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-tools -p codex-goal-extension -p codex-extension-api -p codex-rollout-trace -p codex-queue-extension -p codex-exec -p codex-arg0 -p codex-cli "${filter[@]}"`

All ten `suite::tmpdir_cleanup` tests and both `codex-cli::exec_tmpdir_cleanup` tests have individual PASS records (12/12). The successful job supports exit 0 for this test step; no local invocation is claimed. Core/app-server job success was checked through GitHub job metadata and the attached report, rather than re-reading their full suite logs.

| Hosted mutant / pinned commit | Small job and real exit | Observed failure; expected-red rationale |
|---|---|---|
| `empty_stdin_error_prefix` / `52fe1d4fee603ef3f398b27a424b908895a75a1a` | [114123649003](https://github.com/ivanopcode/codex/actions/runs/38021154057/job/114123649003), 100 | `exec_empty_stdin_preserves_stderr`; full-stderr diff shows unwanted `Error: No prompt provided via stdin.` |
| `empty_stdin_process_exit` / `a9456ba7fa63604b839761274210fed019e43078` | [114123649027](https://github.com/ivanopcode/codex/actions/runs/38021154057/job/114123649027), 100 | Empty-stdin cleanup and stderr tests report actual `codex-arg0*` leftovers; early process exit skips the guard |
| `error_seen_process_exit` / `223b9af27ebfd1441101e459127ef42705fc33ee` | [114123649031](https://github.com/ivanopcode/codex/actions/runs/38021154057/job/114123649031), 100 | Server-error cleanup and stderr tests report actual `codex-arg0*` leftovers; post-session process exit skips the guard |
| `exec_parse_exit` / `13db913a20327e470c12a585c3268e30b4e0121b` | [114123649084](https://github.com/ivanopcode/codex/actions/runs/38021154057/job/114123649084), 100 | Help and invalid-argument tests report actual `codex-arg0*` leftovers; restored `TopCli::parse()` bypasses drop |

Each mutant suite ran 24 tests, with 907 filtered/skipped. Failures were the intended assertions, not compilation/setup failures. The precise coverage is 4/4 supplied mutants killed, two of the thirteen original library exit sites mutated, and one of two public parser dispatchers mutated. The multitool dispatcher has passing entry-point tests and equivalent source routing, but no separately executed narrowing mutant. No claim of universal mutation coverage is made.

The [lint log](https://github.com/ivanopcode/codex/actions/runs/38021154057/job/114122236757) records `just fmt-check` and scoped Clippy with `set -o pipefail`. The named Clippy package list excludes direct `-p codex-exec`, `-p codex-arg0`, and `-p codex-cli`; the green lane should not be described as an explicit Clippy run for all three changed crates. Compilation and behavior of those crates are exercised by snapshot small. No new local lint run was permitted by the brief.

## Previous findings: 5/5 checked

| Previous finding | Delta assessment / immutable source |
|---|---|
| A-F1 | Fixed. Both public dispatchers use `try_parse()`, print Clap's error, and return its code via `SilentExit`, instead of terminating inside the guarded future: `exec/src/main.rs:30-43`, `cli/src/main.rs:1036-1045`. All four parser entry-point tests pass; standalone parser mutant fails at leak assertions. |
| F1-clap-parser-exit-skips-arg0-guard | Fixed by the same A-F1 change; checked separately because the previous merged verdict retained it as a distinct finding. Help/error return through `arg0/src/lib.rs:281-285`; `--version` uses the same error-return arm but has no dedicated cleanup test. |
| A-F2 | Fixed. All thirteen former library exit sites retain their existing diagnostic or intentional silence and return `SilentExit::failure()`. `arg0/src/silent_exit.rs:55-68` suppresses only the marker and retains `Error: {err:?}` for ordinary anyhow errors. Whole-stderr tests for stdin/config/server pass, and the prefix mutant fails with the expected full-string difference. |
| A-F3 | Fixed within the stated scope. Both suites panic on root/entry enumeration failure. The home is a separate sibling of child TMPDIR, so the release guard's `starts_with(temp_root)` refusal does not apply to this fixture. Fresh home/root plus no alias-setup warning establishes setup occurred; missing roots fail closed. Both oracle attacks pass in snapshot small. Partial-entry fault injection and an actual release run remain unexecuted, rather than silently claimed covered. |
| A-F4 | Fixed by correcting the results' bound. The results now state only Ctrl-C routing is present and delivery is unverified; SIGTERM is unhandled and leaks on default termination; SIGKILL/abort do not run destructors. Source matches: `exec/src/lib.rs:1127-1133`, `app-server-client/src/lib.rs:355-358`, and the in-process runtime's startup/event loops. AC2 explicitly allows this bound. |

Sources read from the board: `surface-table.md`, `TASK-261007-3v81ko_review-verdict-rev1.md`, `TASK-261007-3v81ko_results.md`, `TASK-261007-3v81ko_hosted-precheck-2.md`, `TASK-261007-3v81ko_mutants.json`, and `TASK-261007-3v81ko_change-request_rev2-validation.log`. The latter records `mini-hosted-gate.sh` exit 0 and exact tree/run identity; it is not a full suite transcript. Producer brief/notes were context only. Candidate source can be resolved with `git show ca07d336e99eb0ddcb15a180bbaaaf2a45388835:<path>` or through the [immutable snapshot](https://github.com/ivanopcode/codex/tree/98ae625bdd680caf632828105d807d8723e163e8/codex-rs).

## Logbook entry — 2026-10-10

Decision: accept this DELTA panel within its documented evidence bounds. Exact replay matches; five previous findings are addressed; five surface rows were attacked; no new actionable defect was established. Evidence clarification: hosted run aggregate failure is expected from four mutant suites exiting 100, while all four candidate lanes pass. Direct changed-crate Clippy coverage is narrower than the successful lint job's name suggests. Original host-specific eight `.tmp*` directories per successful run remain unexplained; the demonstrated mechanism is destructor-skipping error/parser exits and the tested cleanup invariant. This entry travels in the task-scoped outcome because no `logbook` executable is available; nothing was written to the reviewed task or control-root files.

## Successor verification and handoff recovery — RUN-261010-e81fb2

The preceding review and its hosted-log inspection are preserved above as prior-run evidence. This successor did not rerun hosted tests or mutants. It independently replayed the patch, reread the current board inputs and candidate implementation/tests, rechecked the prior five finding IDs and all five surface rows, and refreshed GitHub run/tree metadata. The verdict remains accept with the same documented bounds.

| Successor command | Actual exit / result |
|---|---|
| `task-board m 'set_status(TASK-261010-3o98tr, status=analysis)'` | 0; own task only |
| `mkdir -p .temp` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o98tr-recovery-replay.idx" git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872` | 0 |
| `task-board resource get TASK-261007-3v81ko TASK-261007-3v81ko_change-request_rev2.patch --output .temp/TASK-261007-3v81ko_change-request_rev2.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o98tr-recovery-replay.idx" git apply --cached .temp/TASK-261007-3v81ko_change-request_rev2.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o98tr-recovery-replay.idx" git write-tree` | 0; ca07d336e99eb0ddcb15a180bbaaaf2a45388835 |
| `git diff --check 07c018be3507b8d4a5558a85a117b94ed2a23872 ca07d336e99eb0ddcb15a180bbaaaf2a45388835` | 0 |
| Scoped `git diff`, candidate `git show`, and residual-exit/signal `git grep` reads | Each 0; both dispatchers, marker propagation, all library conversions, guard lifetime and both fail-closed test oracles inspected |
| `task-board q` own task title/status/notes/checklist and resource projections; source description/scope/AC/notes and resource projections | Each corrected query 0 |
| `task-board resource get` fresh surface table, merged rev1 verdict, producer results, precheck-2 report, source rev2 validation log and own failed rev1 validation log | Each 0 |
| `gh run view 38021154057 --repo ivanopcode/codex --json headSha,status,conclusion,jobs,url --jq '{headSha,status,conclusion,url,jobs:[.jobs[]\|{name,conclusion,databaseId}]}'` | 0; four candidate lanes success, four mutant small lanes failure, aggregate failure |
| `gh api repos/ivanopcode/codex/git/commits/98ae625bdd680caf632828105d807d8723e163e8 --jq '{sha,tree:.tree.sha}'` | 0; exact candidate tree |
| Python current prior-verdict/results inspection | 0; five prior IDs confirmed and corrected signal bound reread |
| Python artifact relocation/recovery addendum script | 0; preserved outcome in ignored `.temp/`, removed only its untracked repository copy |
| `python3 .temp/validate-panel-verdict.py` | 0; one valid JSON block, one-word accept verdict, 5/5 distinct surface rows and 5/5 prior finding references |
| `git status --short` | 0; empty |
| `git diff --exit-code HEAD` | 0; empty tracked delta |
| `git ls-files --others --exclude-standard` | 0; no untracked repository files |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0; no directives |

Recovery anomaly and logbook addendum: the prior handoff's validation command `/Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` actually exited **1**. Its candidate tree `9c963a79d283306d9daec23dc649824118187715` included this research Markdown as a new repository file and had no recorded hosted run. That gate did not pass. The source CR's attached validation log separately records exit **0** for exact source tree `ca07d336...`; these are different candidates.

Resolution: preserve and update this task-scoped board outcome, move the local research copy into ignored `.temp/`, and hand off a research-only empty repository delta. This follows the project-management negative-evidence reference's C2 rule for outcome-backed research. No source validation exemption is fabricated, no hosted record is minted, and no product code or reviewed-task metadata is changed. Source review evidence remains anchored to the replay tree. Artifact validation/attachment/handoff results are recorded in this task's activity transcript; no future lifecycle command is asserted green here.

Successor discovery failures: two initial queries using `resources` each exited 1; a missing skill reviewer-role file read exited 1; a focused skill-reference search exited 1 (no matches). `task-board resource list` exited 0 but printed help. An attempted `rm -f` of the prior temporary index was rejected before execution (no process exit code); recovery used a separate index instead. None is presented as a passing gate. No cargo, just, build, test or fmt command was run in this successor.

```verdict-findings
{
  "findings": [],
  "notes": [
    "All five previous merged findings were checked individually and addressed; A-F1 and F1 share a parser mechanism but neither was omitted.",
    "Replay equals ca07d336e99eb0ddcb15a180bbaaaf2a45388835. Hosted snapshot commit 98ae625bdd680caf632828105d807d8723e163e8 resolves to that same tree via GitHub Git API; the workflow controller commit is not the tested candidate.",
    "Hosted candidate lanes 4/4 success; snapshot small 930/930 executed tests pass with 1 skipped; new tests 12/12 pass. Supplied narrowing mutants 4/4 killed, each small test step exit 100. Overall workflow failure is expected-red, not a passing aggregate.",
    "Mutation coverage is two of thirteen original library exit sites and one of two public parser dispatchers, plus an output-prefix mutant. No assertion of comprehensive per-site, per-platform, signal or detached-task coverage.",
    "Original eight-per-success-run .tmp* allocation source remains unreproduced and unidentified. Passing .tmp* scans protect the invariant, not an observed eight-to-zero transition.",
    "SIGINT delivery, release execution, Windows/macOS runtime results, partial-read fault injection and dedicated --version execution are unknown in this evidence. SIGTERM/SIGKILL/abort cleanup is explicitly bounded in the results.",
    "The hosted lint package list does not explicitly select the three changed crates for Clippy; snapshot small compiles/tests them. No local cargo/just/build/test commands ran.",
    "No mutation, accept/reject/withdraw, status or handoff was performed on TASK-261007-3v81ko. All panel outputs and lifecycle writes target TASK-261010-3o98tr only."
  ],
  "surface_results": [
    {
      "row": "tmpdir cleanup on every exit",
      "result": "held",
      "reason": "Attacked residual parser and error exits. Library process::exit(1) count is 13 on base, 0 on candidate; both dispatchers return from try_parse errors. Production route is run_main -> run_exec_session -> arg0 run_main_with_arg0_guard drop -> runtime teardown -> outer ExitCode. Hosted success/error/stdin/parser cleanup tests pass and one-site error/stdin/parser mutants fail with actual arg0 leftovers. Held for reviewed normal exit paths; original host-specific .tmp* root cause and exhaustive unrelated task ownership remain unknown."
    },
    {
      "row": "exit status and observable behavior",
      "result": "held",
      "reason": "Attacked marker propagation, lost diagnostics, extra Error prefixes and swallowed codes. All converted branches retain original printing/silence; marker survives direct ? propagation through both mains; mapper returns the stored code without extra output. Hosted tests assert 0/1/2 and whole stderr on three deterministic error classes; prefix mutant exits 100 at exact-string comparison. Other anyhow errors retain Debug rendering; helper/input refactors preserve successful values and error branches. No new await was added to these conversions."
    },
    {
      "row": "signal and abort bound",
      "result": "held",
      "reason": "Attacked the previous unsupported SIGTERM routing claim against the embedded runtime call chain. Corrected results explicitly state no SIGTERM handler on this exec path, destructor-skipping SIGTERM/SIGKILL/abort, and unverified OS delivery for source-present Ctrl-C routing. Held for the explicit bound permitted by AC2; 0 signal-injection tests, no signal cleanup attestation."
    },
    {
      "row": "persistent state unchanged",
      "result": "held",
      "reason": "Static deletion/path attack: no changes to persistent CODEX_HOME/sqlite/rollout storage or janitor policy; guard deletion remains confined to its existing CODEX_HOME/tmp/arg0/codex-arg0* TempDir. Only control-flow returns and public-main error mapping change. Held for storage location/deletion invariance; incidental flushing from orderly teardown is not claimed byte-identical."
    },
    {
      "row": "regression test and mutants",
      "result": "held",
      "reason": "Attacked vacuous setup, read failure mistaken for absence, wrong mutant identity and unrelated failure. Fresh sibling home plus root/warning precondition exercises setup; scanners panic on root and per-entry failure. Hosted 12/12 new tests pass, including two fail-closed oracle attacks. GitHub compare verifies all four hosted mutations are the attached one-site changes; logs show 4/4 kills at intended full-stderr or arg0-leak assertions, with exit 100. Measured coverage and unexecuted release/partial-read/platform cases are stated explicitly."
    }
  ],
  "free_hunt": [
    "Bounded pass after all five rows: both public dispatchers and their direct run_main propagation, arg0 guard lifetime, changed config/schema/stdin Result propagation, embedded signal chain, test oracle setup and immutable hosted mutant identities. No builds, code changes or first-finding early stop.",
    "Residual same-class search: remaining arg0 process exits are helper-dispatch branches before alias guard allocation; remaining cli exits belong to TUI/app-server/login subcommands and are not reachable from the Exec match arm. No residual in-process destructor-skipping exit was established in the examined exec route.",
    "Rework regression attack: load_output_schema(None) remains Ok(None); read/JSON failures remain printed error exits; optional empty stdin remains Ok(None); required/forced input never yields None, keeping resolve_prompt's unreachable arm unreachable. Resume/fork/review call sites propagate the new Result with ? rather than swallowing it.",
    "Test-evidence attack: verified snapshot-small/lint and all four mutant-small checkout identities and exact mutant diffs; confirmed expected-red exit 100 and intended leak/output assertions rather than compiler failure. Core/app-server evidence was read from job metadata and the attached report. Noted aggregate workflow failure and direct changed-crate Clippy bound.",
    "Remaining optional attacks, not claimed executed: a MultitoolCli::parse narrowing mutant killed by cli_exec_help_leaves_no_tmpdirs / cli_exec_invalid_args_leave_no_tmpdirs; a release-mode cleanup lane; directory-entry read fault injection; dedicated --version cleanup; OS signal delivery after observing a live guard. These do not establish defects in the reviewed fixes."
  ]
}
```
