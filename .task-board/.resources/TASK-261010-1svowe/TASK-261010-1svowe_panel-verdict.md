# TASK-261010-1svowe — r141-panel-delta-task-261007-3v81ko-rev3

accept

CR-TASK-261007-3v81ko-3, revision 3. Independent non-recording DELTA panel.

Replay check: base `07c018be3507b8d4a5558a85a117b94ed2a23872` plus the attached revision-3 patch, through temporary index `.temp/TASK-261010-1svowe-replay.idx`, writes exactly `2f7ec5e30babb9dff4f00132ad9fd384663930b0`, the expected candidate. No nested worktree. The later write-tree check returns the same tree. Production files were read from this tree, not the Story checkout.

Prior finding A2-F1 is addressed; no new finding established. Surface sweep: 5/5 rows, exactly one result each. This is ready for review by the recording-review chain, not a source-task acceptance transaction.

Commands and observed exit codes (run by this panel)

| Command | Exit/result |
|---|---|
| `mkdir -p .temp` |  0 |
| `rm -f .temp/TASK-261010-1svowe-replay.idx` | Not executed: tool policy rejected rm -f; no process exit code |
| `python3 -c 'from pathlib import Path; Path(".temp/TASK-261010-1svowe-replay.idx").unlink(missing_ok=True)'` |  0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-1svowe-replay.idx" git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872` |  0 |
| `task-board resource get TASK-261007-3v81ko TASK-261007-3v81ko_change-request_rev3.patch --output .temp/TASK-261007-3v81ko_change-request_rev3.patch` |  0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-1svowe-replay.idx" git apply --cached .temp/TASK-261007-3v81ko_change-request_rev3.patch` |  0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-1svowe-replay.idx" git write-tree` |  0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-1svowe-replay.idx" git write-tree` (after all mutation checks) | 0; same expected tree |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-1svowe-replay.idx" git apply --cached --check .temp/TASK-261010-1svowe-<name>.patch`, separately for empty_stdin_error_prefix, empty_stdin_process_exit, error_seen_process_exit, exec_parse_exit, stderr_failure_eprintln | 0 for each, 5/5; no mutation applied |
| `gh run view 38038510297 --repo ivanopcode/codex --json jobs,headSha,conclusion,url` (redirected to local JSON) | 0 |
| `gh run view 38038510297 --repo ivanopcode/codex --log` (redirected to local log) | 0; retrieval only, not test execution |
| `gh api repos/ivanopcode/codex/git/commits/aadfcaa85ed05ac3b62581e25fb94ccad1e9971e --jq '{sha: .sha, tree: .tree.sha}'` | 0; exact candidate tree |
| `gh api repos/ivanopcode/codex/compare/aadfcaa85ed05ac3b62581e25fb94ccad1e9971e...<mutant_sha>` with structured projection | 0 for each of 5 SHAs below |
| `python3 .temp/TASK-261010-1svowe-review-evidence.py` | 0; validates snapshot, 4/4 lane conclusions, 14/14 added tests, 5/5 exact hosted mutant edits/expected-red gates and diagnostic/13-site static comparison |
| Candidate/base/rev2 `git show`, `git diff`, and scoped `git grep` reads described below | 0 for every source read/search used as evidence |
| Board resource get: surface-table.md, prior rev2 verdict, results, producer brief, hosted-precheck-3, mutants.json, rev3-validation.log | 0 each; downloads/read-only |
| Corrected scoped board queries (description/scope/ac/notes, preconditionResources/outcomeResources/review, panel checklist/status) | 0 each |
| Initial query requesting nonexistent field resources | 1; corrected via schema, not treated as absent evidence |
| Initial router reviewer-role cat | 1; missing path; sibling installed reviewer role cat returned 0 |
| Role-file rg searches in router skill roots | 1 (no matches); alternate package located via Path.glob, exit 0 |
| `command -v gh; command -v logbook` | 1 overall; gh found, logbook absent |
| `task-board resource list TASK-261007-3v81ko` | 0 but only prints help; not evidence of absent resources; corrected scoped query used |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0; no directives |
| `task-board m 'set_status(TASK-261010-1svowe, status=analysis)'` | 0; panel task only |
| `git status --short` before review | 0; empty |
| Inline `python3` verdict validator: parse the sole verdict-findings block; compare its rows to surface-table; require exactly one accept line and replay before JSON | 0; one valid JSON object, 5/5 exact rows, 17,219 bytes before this evidence line |
| `git status --short` after artifact verification | 0; empty; only ignored .temp artifacts were written |

No Cargo/just/build/test gate ran locally. Inline Python static comparisons and log extraction also exited 0; the retained review-evidence script reproduces their relevant assertions. The attempted doc.rust-lang.org versioned source read returned a web-tool accessibility error (no shell exit code); pinned upstream raw Rust source and installed 1.95.0 rust-src were read successfully.

Sources and accepted execution evidence

- Read-only board resources on source task: `surface-table.md`, `TASK-261007-3v81ko_review-verdict-rev2.md`, `TASK-261007-3v81ko_results.md`, `TASK-261007-3v81ko_mutants.json`, `TASK-261007-3v81ko_hosted-precheck-3.md`, and `TASK-261007-3v81ko_change-request_rev3-validation.log`.
- [Hosted run 38038510297](https://github.com/ivanopcode/codex/actions/runs/38038510297): lint and snapshot small/core/app-server all success. Snapshot-small job 114175186675, log lines 12417–12420, 12968–13073: all 14 added tests PASS; line 13274: 932 passed, 1 skipped. The workflow controller head is not the snapshot.
- [Snapshot Git commit API](https://api.github.com/repos/ivanopcode/codex/git/commits/aadfcaa85ed05ac3b62581e25fb94ccad1e9971e): tree equals replay. Snapshot checkout appears at log lines 115, 8423, 35175 and 45753.
- [Shared reporter](https://github.com/ivanopcode/codex/blob/aadfcaa85ed05ac3b62581e25fb94ccad1e9971e/codex-rs/arg0/src/silent_exit.rs#L63), [guard lifetime](https://github.com/ivanopcode/codex/blob/aadfcaa85ed05ac3b62581e25fb94ccad1e9971e/codex-rs/arg0/src/lib.rs#L281), [exec main](https://github.com/ivanopcode/codex/blob/aadfcaa85ed05ac3b62581e25fb94ccad1e9971e/codex-rs/exec/src/main.rs#L29), [CLI main](https://github.com/ivanopcode/codex/blob/aadfcaa85ed05ac3b62581e25fb94ccad1e9971e/codex-rs/cli/src/main.rs#L1015).
- [Pinned Rust 1.95 Result Termination](https://github.com/rust-lang/rust/blob/1.95.0/library/std/src/process.rs#L2495) and [write-failure handling](https://github.com/rust-lang/rust/blob/1.95.0/library/std/src/io/stdio.rs#L1123) confirm ordinary Err reporting ignores sink write failures; this also matches installed rust-src. Delegation uses the same Err arm for Result<(), Error> and Result<ExitCode, Error>.

Hosted expected-red mutant gates (execution reused from that exact run)

| # / mutant | Commit SHA | Observed gate exit | Intended failure |
|---|---|---|---|
| 1 empty_stdin_error_prefix | 8699e57b6ebd5fce62ebe03d1d8dd7bfbd2010a0 | 100 | Full-stderr comparison: unexpected Error: prefix; log 59239–59245 |
| 2 empty_stdin_process_exit | cb096e4de6b1bbce15c2252b499b12335908f5b2 | 100 | Empty-stdin cleanup sees leaked codex-arg0 directory; log 34960–34961 |
| 3 error_seen_process_exit | 90cacc3c8280ba8c0d41875e1f20e29fc676f030 | 100 | Server-error cleanup sees leaked codex-arg0 directory; log 21764–21765 |
| 4 exec_parse_exit | e33ce0914dc81c97db201292fa363836f431c7ab | 100 | Help and invalid-argument cleanup see leaked codex-arg0 directories; log 17445–17446 |
| 5 stderr_failure_eprintln | d977a72e12a087b65ca98b822b5ccae5250e26cc | 100 | Both real binaries return panic code 101 instead of 1 on /dev/full; log 45396–45402 and 45491–45497 |

Every mutant is intentionally failing, not passing. Each mutant small command is the hosted `INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-tools -p codex-goal-extension -p codex-extension-api -p codex-rollout-trace -p codex-queue-extension -p codex-exec -p codex-arg0 -p codex-cli "${filter[@]}"`; the filter is `test(tmpdir_cleanup) | test(tmpdir) | test(stderr) | test(exit_code) | test(silent_exit) | test(try_parse) | test(help) | test(stderr_failure) | test(dev_full) | test(no_panic)`. The unmutated small command has no filter and succeeds. Candidate core/app-server and lint conclusions are successful; hosted lint does not explicitly select arg0/exec/cli for Clippy, while snapshot small compiles/tests them. This panel neither reran nor upgraded that evidence into broader platform coverage.

Logbook entry — 2026-10-10

DELTA rev3: A2-F1 addressed at both public binaries; exact replay/snapshot tree match, 5/5 surface rows held and 5/5 mutants killed for their intended assertions. No new defect or stop-the-line boundary established. Preserve original success-incident and signal/platform bounds. No external logbook executable/tool was available; this entry persists with the panel outcome and is echoed in panel notes.

```verdict-findings
{
  "findings": [],
  "notes": [
    "DELTA order followed: previous merged rev2 finding A2-F1 checked first (1/1 addressed), same-class search next, rework regression sweep next, followed by a bounded free hunt. Rev1 closures A-F1/F1, A-F2, A-F3 and A-F4 were also rechecked for regression.",
    "A2-F1 closure: arg0/src/silent_exit.rs:63-76 returns an ordinary error unchanged. exec/src/main.rs:29-52 and cli/src/main.rs:1015-1023 return Result<ExitCode, anyhow::Error>, invoking the identical Rust 1.95 Result Termination Err arm used by the base. Guard drop at arg0/src/lib.rs:281-285 occurs before mapping/terminal reporting. Hosted snapshot passes both public /dev/full tests; exact stderr_failure_eprintln mutant fails both specifically with Some(101) versus expected Some(1).",
    "Evidence identity: CR replay and GitHub Git commit API both give candidate tree 2f7ec5e30babb9dff4f00132ad9fd384663930b0. Snapshot aadfcaa85ed05ac3b62581e25fb94ccad1e9971e is checked out by lint and all snapshot lanes; workflow head 2543194083e87e51973c6d60dfa7b40f386fb9fa is only the workflow controller. Compare API confirms all five hosted mutants are single-commit changes based on that snapshot with edit payloads equal to the attached mutants.",
    "Measured coverage: 5/5 surface rows swept once; 4/4 candidate lanes successful; snapshot small 932/932 executed tests pass, 1 skipped; 14/14 added tests pass (11 exec plus 3 CLI, including 2 oracle tests and 2 /dev/full tests); 5/5 supplied mutants killed. Leak mutations cover 2/13 former explicit exec library exit sites and 1/2 public parser dispatchers; the fifth mutant covers ordinary-error reporting at both public entry points. The two other mutants/checks are the output-prefix mutant and shared-reporter write-failure mutant, not additional leak-site proofs.",
    "Bounds: original macOS eight-per-success .tmp* allocation source remains unreproduced/unidentified; 0/5 mutants establish that original eight-to-zero transition. SIGINT OS delivery is unverified (0 signal-injection tests); SIGTERM/SIGKILL/abort skip destructors and are explicitly bounded in results. Dedicated --version, partial-read fault injection, release-mode and macOS/Windows runtime execution are unknown. /dev/full tests explicitly skip where absent. Linux hosted execution proves they did run there because the matching mutant fails the exit-code assertions.",
    "Normal diagnostics preserved: independently compared all exec library eprintln expressions between base and candidate, equal; 13/13 explicit exit sites now return SilentExit. Full-stderr hosted tests pass. Existing explicit diagnostic eprintln failures can still panic, as in the base; they are not the removed terminal ordinary-error regression. No new ordinary-error eprintln reporter remains.",
    "Hosted aggregate workflow conclusion is failure as expected from mutant gates; each small mutant gate exits 100, not 0. Candidate lane success is separately verified. CR rev3 validation log records mini-hosted-gate exit 0 and exact_command_shard 1/1; it does not independently prove test-case coverage. No cargo, just, build, or local Rust test command ran in this panel.",
    "Non-recording boundary: no writes of any kind to TASK-261007-3v81ko. Resource retrieval/query/GitHub reads only. Outcome, notes, checklist and handoff target TASK-261010-1svowe only.",
    "Logbook fallback: no logbook executable or callable logbook tool is available. The dated logbook entry above is preserved in this task-scoped outcome and panel task notes; no external logbook publication is claimed.",
    "Skill-reference anomaly: the assigned project-management router's .roles/reviewer/role.md is absent (cat exit 1). A sibling installed project-management package's reviewer role was read successfully, but it has no review-round section. The explicit panel brief supplies the governing attack/sweep/DELTA contract; no missing reference was treated as permission to narrow review."
  ],
  "surface_results": [
    {
      "row": "tmpdir cleanup on every exit",
      "result": "held",
      "reason": "Exact-tree hosted success, server-error, empty-stdin, config-error, parser and ordinary-error public-binary tests pass. Mutants 2, 3 and 4 fail on real leaked codex-arg0 directories. Static scan verifies 13/13 former exec library exits return instead of terminating, result propagation reaches both public mains, and arg0 drops its guard after main_fn returns and before mapping. Remaining arg0 exits precede guard allocation; remaining CLI exits are distinct TUI/app-server/login branches. Held within normal-return and successful-removal bounds, not as exhaustive transitive TempDir or original macOS-incident proof."
    },
    {
      "row": "exit status and observable behavior",
      "result": "held",
      "reason": "A2-F1 corrected through the original Rust Result Termination Err arm; both public /dev/full tests pass and mutant 5 is killed by exit 101 versus 1. Existing full-stderr tests and both parser code/stream tests pass; prefix mutant 1 fails specifically on an added Error: prefix. All original explicit diagnostic expressions are unchanged. Normal success and SilentExit mapping retain codes 0/1/2. No new output write, await, error conversion or ordering change is introduced in the rev3 production delta."
    },
    {
      "row": "signal and abort bound",
      "result": "held",
      "reason": "AC2 permits a stated bound. Results explicitly state Ctrl-C routing exists but OS delivery is unverified, SIGTERM is unhandled on the in-process exec route, and SIGKILL/abort cannot run destructors. Source shows only ctrl_c subscription at exec/src/lib.rs:1129; no rev3 signal change. No signal runtime coverage is claimed."
    },
    {
      "row": "persistent state unchanged",
      "result": "held",
      "reason": "Base-to-candidate diff changes exit mechanics and tests only; rev3 narrows to reporter/mains and two tests. No persistent path, database schema, store initialization or deletion algorithm changes. Guard ownership remains CODEX_HOME/tmp/arg0/codex-arg0*; writer locks remain CODEX_HOME/thread-writer-locks via rollout/src/writer_lock.rs:35-39. Fixture homes are test-only sibling directories. Held for location/deletion invariance; incidental flushes from newly allowed destructors are not claimed byte-identical."
    },
    {
      "row": "regression test and mutants",
      "result": "held",
      "reason": "14/14 new tests pass on snapshot small; 5/5 exact hosted edit payloads match submitted mutants and all apply-check against replayed candidate (exit 0). Expected-red gates exit 100; kills show Error: prefix, leaked arg0 dirs, and stderr failure exit 101 for their respective defects. Fail-closed root/entry reads and two oracle rejection tests remain; ordinary leak tests require setup root and warning-free stderr. New /dev/full tests cannot inspect stderr warnings but require a fresh arg0 root; hosted matching mutant deaths establish their terminal reporter path was exercised. Per-site/platform/stress bounds remain explicit."
    }
  ],
  "free_hunt": [
    "Budget: one bounded static pass over both dispatchers and shared reporter, result/guard lifetime, remaining exit reachability, sampled TempDir ownership and persistent state, prompt/schema error propagation, and test-oracle/mutant causality. No product code edits or local builds.",
    "Same-class attack: searched SilentExit/reporter references and all explicit exec/CLI/arg0 exits. Shared ordinary-error reporter no longer uses eprintln; all thirteen preprinted library failures remain base-identical; parser branches intentionally ignore err.print errors, matching clap exit semantics. No additional new write-failure mechanism established.",
    "Rework attack: traced SilentExit and ordinary errors through exec run_main tail, cli Exec/Review bare ?, worker join, arg0 guard drop and both public main Result types. No context/to_string conversion introduced; no error is mistaken for Ok. Success yields SUCCESS, silent code yields its code, ordinary Err delegates to standard Termination.",
    "Ownership/persistence attack: arg0 allocation and removal unchanged; sampled app-server-client/in_process TempDir homes are cfg(test), rollout writer locks remain persistent home-scoped. Broader dependency graph, detached task stress and original .tmp* source are unknown; this is a bounded source audit.",
    "Test attack: each hosted mutation changes only its named site from the exact snapshot; failure diagnostics show the intended leak/output/status assertion, not compilation failure. New stderr tests use real public binaries and /dev/full; Linux mutant fails at exit comparison, proving no skip. No further regression established in the examined scope."
  ]
}
```
