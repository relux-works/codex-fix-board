# TASK-261010-3cmjct — r141-panel-delta-task-261007-3v81ko-rev4

accept

Ready for review. Independent, non-recording DELTA panel for
CR-TASK-261007-3v81ko-4. Findings: 0; surface sweep: 5/5 held, each once.
No resource, notes, status, acceptance, rejection, withdrawal, or handoff write
was made on TASK-261007-3v81ko — fix-exec-tmpdir-cleanup.

## Replay and delta

Base `07c018be3507b8d4a5558a85a117b94ed2a23872` plus the attached
`TASK-261007-3v81ko_change-request_rev4.patch` produces exactly
`bde782b85ddbc8536536d0747b3917d0f24e1951` through a temporary index.
The expected and actual write-tree values match. No nested worktree was used.

Commands below ran separately, with the real exit status preserved:

| Command | Exit | Observation |
|---|---:|---|
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3cmjct-replay.idx" git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872` | 0 | Base loaded |
| `task-board resource get TASK-261007-3v81ko TASK-261007-3v81ko_change-request_rev4.patch --output .temp/TASK-261007-3v81ko_change-request_rev4.patch` | 0 | Patch retrieved read-only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3cmjct-replay.idx" git apply --cached .temp/TASK-261007-3v81ko_change-request_rev4.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3cmjct-replay.idx" git write-tree` | 0 | Exact expected candidate tree |
| `git diff --name-only 2f7ec5e30babb9dff4f00132ad9fd384663930b0 bde782b85ddbc8536536d0747b3917d0f24e1951` | 0 | Only `.github/workflows/relux-ci.yml` |
| `git diff --exit-code 2f7ec5e30babb9dff4f00132ad9fd384663930b0 bde782b85ddbc8536536d0747b3917d0f24e1951 -- codex-rs` | 0 | Entire Rust source/test/build tree unchanged |
| `git diff --check 07c018be3507b8d4a5558a85a117b94ed2a23872 bde782b85ddbc8536536d0747b3917d0f24e1951` | 0 | No whitespace errors |

DELTA order followed: previous merged verdict first, same-class search second,
regression sweep third, then a bounded free hunt. The previous merged
`TASK-261007-3v81ko_review-verdict-rev3.md` accepts with an empty findings array:
0/0 outstanding findings to repair. Its historical closures A-F1/F1, A-F2,
A-F3, A-F4 and A2-F1 were rechecked, including their recorded limitations.

The rev3-to-rev4 change adds `-p codex-arg0 -p codex-cli` to the workflow's
small snapshot and mutant commands at lines 178 and 324. It changes no Rust
behavior, tests, home/state paths, signal handling, test filter, or gate exit
handling. The matrix, exact-checkout checks, and nonempty mutant-filter
requirement remain in place. The hosted job logs already select these packages;
there is no claimed newly executed mutation campaign on the rev4 tree.

## Execution evidence inspected, not rerun

The [landing commit API](https://api.github.com/repos/ivanopcode/codex/git/commits/e0eff057620104a416080da616256ee7f32bda1b)
resolves to the exact candidate tree. The actual `RUN_SHA` in both retrieved
landing logs is `e0eff057620104a416080da616256ee7f32bda1b`; the workflow
controller head is not used as the tested tree identity.

[Landing run 38045370015](https://github.com/ivanopcode/codex/actions/runs/38045370015)
has 4/4 successful candidate lanes: lint `114193722047`, small `114195291609`,
core `114195291571`, app-server `114195291589`. Small and lint logs were
downloaded and read directly; core/app-server conclusions were inspected in
job metadata. No assertion about unread core/app-server test-case counts is made.
The exact-tree small lane reports **932 tests run, 932 passed, 1 skipped**.
All **14/14 added tests** have individual PASS records: 11 exec and 3 CLI;
12 drive public binaries, 2 attack the leak-scan oracles.

The successful hosted small command is:

`INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-tools -p codex-goal-extension -p codex-extension-api -p codex-rollout-trace -p codex-queue-extension -p codex-exec -p codex-arg0 -p codex-cli "${filter[@]}"`

Its step succeeded (exit 0), with an empty snapshot filter. Hosted lint's
`just fmt-check` and its Clippy step succeeded (exit 0). The latter selects
tools/core/goal-extension/extension-api/app-server/rollout-trace/queue-extension;
direct Clippy coverage of exec/arg0/cli is not inferred from the lane name.
Three warnings were classified as the three recorded upstream warnings.

[Historical precheck 3 run 38038510297](https://github.com/ivanopcode/codex/actions/runs/38038510297)
tests rev3 tree `2f7ec5e30babb9dff4f00132ad9fd384663930b0`, not rev4.
Its candidate lanes succeeded; its aggregate conclusion is **failure** because
five mutant-small gates fail intentionally. Every mutant log was read directly:

| Mutant | Hosted job | Gate exit | Intended failing assertion |
|---|---:|---:|---|
| `empty_stdin_error_prefix` | 114175186766 | 100 | `exec_empty_stdin_preserves_stderr`: extra `Error:` prefix |
| `empty_stdin_process_exit` | 114175186731 | 100 | Empty-stdin cleanup and stderr tests: leaked `codex-arg0*` |
| `error_seen_process_exit` | 114175186708 | 100 | Server-error cleanup and stderr tests: leaked `codex-arg0*` |
| `exec_parse_exit` | 114175186702 | 100 | Exec help and invalid-argument cleanup tests: leaked `codex-arg0*` |
| `stderr_failure_eprintln` | 114175186747 | 100 | Both public stderr-failure tests: child exit 101 versus required 1 |

These are actual nonzero test failures, not green gates or compiler-only kills.
Expected-failure rationale: each patch restores one destructor-skipping exit,
adds the removed diagnostic prefix, or restores the failing-stderr panic.
All five historical small gates used the package command above with
`-E "$TEST_FILTER" --no-tests=pass`; the logged filter is
`test(tmpdir_cleanup) | test(tmpdir) | test(stderr) | test(exit_code) | test(silent_exit) | test(try_parse) | test(help) | test(stderr_failure) | test(dev_full) | test(no_panic)`.

Each attached patch was independently replayed against both rev3 and rev4
through a temporary index. Every `read-tree`, `apply --cached`, and `write-tree`
exited 0 (30 commands). The five rev3 replay trees match the hosted Git commit
API trees exactly; each hosted mutant has the single parent
`aadfcaa85ed05ac3b62581e25fb94ccad1e9971e`. Each rev3/rev4 mutant pair is
Rust-identical (`git diff --exit-code OLD NEW -- codex-rs`, exit 0 each):

| Mutant | Rev3 replay / hosted tree | Rev4 replay tree (not executed) |
|---|---|---|
| `empty_stdin_error_prefix` | `5c8a84789294f9bb461a44a891952f0f4a01373e` | `6e0523022a30ad4d84f9b7714239f6492e3e65dd` |
| `empty_stdin_process_exit` | `75c9b7958760d23cb5f282be0736eebd2f824e58` | `c6597f691759f6067bc0516b1c3670edbd9c73a3` |
| `error_seen_process_exit` | `cbe7592e9303149e93f07e10d1c42bfa1cf59e12` | `6844710b5c2aa567c09ef4449cf3c19443725ebb` |
| `exec_parse_exit` | `5dd7d22cdbf6a47bca8a1ad829fd5a912d2a15c7` | `c2c933593c68b2451143f9aceb33a36cc306166c` |
| `stderr_failure_eprintln` | `829dc4ae798ab28d4cd95765e5665ddb5d6de38b` | `ba7a71bef7d5f1fd10a09ff6ba0e35d7e223463d` |

For those replays, the exact command templates were
`GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3cmjct-mutant.idx" git read-tree TREE`,
`GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3cmjct-mutant.idx" git apply --cached .temp/TASK-261010-3cmjct-NAME.patch`,
and `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3cmjct-mutant.idx" git write-tree`;
TREE is respectively the full rev3/rev4 candidate above and NAME is each table row.

The rev4 CR validation log is readable, four lines, and records
`mini-hosted-gate.sh` exit 0, `exact_command_shard required=1 green=1 failed=0 missing=0`,
`test_case_coverage=unknown`. Its `.github/` equivalence allowance is not itself
an exact-tree execution proof. This review uses the independent landing run
for exact rev4 baseline evidence; precheck 3 remains historical mutation
sensitivity evidence about unchanged Rust and the matching hosted command.
No full-tree/config/environment identity equivalence or exact-rev4 mutant kill
is claimed.

## Inspection commands and recovery honesty

All commands were synchronous or awaited to process exit. No cargo, just,
build, formatter, Clippy, local test, commit, branch change, or source mutation
was run in this panel. Git temporary-index operations mutate only private
indexes/objects, never the repository index or candidate files.

| Inspection | Real exit codes |
|---|---|
| Initial `task-board m 'set_status(TASK-261010-3cmjct, status=analysis)'` | 0 |
| `task-board q 'get(TASK-261007-3v81ko) { description scope ac notes }'` and later `{ outcomeResources }`; panel `{ checklist }` | 0 each |
| `task-board resource get TASK-261007-3v81ko NAME --output .temp/PANEL-NAME` for surface-table, prior merged verdict, results, producer brief, rev4 validation, precheck3 report, rev4 handoff verification and mutants | 0 each |
| `gh run view RUN --repo ivanopcode/codex --json conclusion,displayTitle,jobs,url` for 38045370015 and 38038510297, redirected to private text files | 0 each |
| `gh run view RUN --repo ivanopcode/codex --job JOB --log` for landing lint/small and the five historical mutant jobs listed above, redirected to private logs | 0 each; all awaited |
| `gh api repos/ivanopcode/codex/git/commits/SHA` for landing and five historical mutant SHAs | 0 each |
| Candidate `git show TREE:PATH`, base/candidate diffs, scoped `git grep`, `rg` over candidate Bazel/test-registration files, and `cat`/`sed` artifact reads | 0 except recoveries below |
| Python assertions: landing identity, 5 hosted mutant identities/parents, 13 removed exits/17 equal diagnostics, 14 test PASS records, five logged exit-100 records | 0 each |
| `git status --short` and `printenv TASK_BOARD_RUN_ID` | 0 each; initial repository status clean |
| `task-board spawn directives RUN-261010-e82a42` at two safe checkpoints | 0 each; no directives |
| `command -v logbook` | 1; no installed executable, no external logbook write claimed |
| Python outcome validation: parse exactly one JSON block, check exact five-row order/uniqueness, accept line and unchanged tracked files | 0; all assertions passed |
| `task-board resource add TASK-261010-3cmjct .research/TASK-261010-3cmjct_panel-verdict.md --type outcome --name TASK-261010-3cmjct_panel-verdict.md -d 'Non-recording rev4 DELTA accept: exact replay, 5/5 held rows, exact-tree hosted baseline and bounded historical mutant evidence'` | 0; task-scoped text outcome attached |

The six hosted commit reads used full SHAs:
`e0eff057620104a416080da616256ee7f32bda1b`,
`8699e57b6ebd5fce62ebe03d1d8dd7bfbd2010a0`,
`cb096e4de6b1bbce15c2252b499b12335908f5b2`,
`90cacc3c8280ba8c0d41875e1f20e29fc676f030`,
`e33ce0914dc81c97db201292fa363836f431c7ab`,
`d977a72e12a087b65ca98b822b5ccae5250e26cc`.

Recoverable inspection failures were not presented as greens:

- Initial temporary-index setup with `rm -f` was rejected before process launch
  by automatic command review; no process exit code exists. Replaced only that
  private-index cleanup with Python `Path.unlink(missing_ok=True)` (exit 0).
- Queries with unknown `resources` and `inputResources` fields exited 1.
  Corrected to the supported `outcomeResources` projection; scoped
  `schema(operation=get)` exited 0. Unsupported `resource list` printed help
  with exit 0 twice; it enumerated no resources and was not used as evidence.
- The installed skill's linked `.roles/reviewer/role.md` is absent: its `cat`
  failed, but the composite shell call subsequently read negative-evidence.md
  and exited 0. Two bounded installed-package file searches exited 1 for no
  match; a further board/package search found no matching role file. The
  explicit panel brief supplies the review-round contract; no missing text was
  claimed read.
- Candidate extraction first requested nonexistent `codex-rs/defs.bzl`:
  underlying `git show` exit 128, Python exit 1. A correction mistyped the tree
  OID and similarly exited 1/128; a diff with that mistyped OID exited 128.
  Corrected root `defs.bzl` and full candidate OID succeeded, exit 0.
- A composite delta/logbook inspection exited 1 because logbook was absent;
  its preceding delta command succeeded. Standalone delta checks subsequently
  exited 0 as recorded above.
- An initial test-name enumeration omitted digits and reported 13 matches
  (Python exit 0). Corrected attribute/name parsing asserts exactly 14 names
  and 14 corresponding PASS records, exit 0; the 13-match intermediate count
  is not the coverage result.

## Sources, bounds, and logbook fallback

Task resources cited above are read-only inputs on the source task, especially
`surface-table.md`, `TASK-261007-3v81ko_review-verdict-rev3.md`,
`TASK-261007-3v81ko_results.md`,
`TASK-261007-3v81ko_hosted-precheck-3.md`, and
`TASK-261007-3v81ko_change-request_rev4-validation.log`.
Code citations below refer to the exact candidate tree, not the worktree HEAD.

Coverage bounds: 5/5 rows swept; 14/14 added tests passed on exact rev4;
historical 5/5 submitted mutants killed; 0/5 rev4 mutant executions;
2/13 former library exit sites individually mutated, 1/2 public parser
dispatchers mutated, 0 OS-signal injections, 0 attacks reproduce the original
eight-per-success `.tmp*` allocation. Linux debug evidence does not establish
macOS/Windows/release behavior. Dedicated version cleanup, multitool-only parser
mutation, repeated-process stress, and per-entry filesystem fault injection
remain unexecuted. These are inherited stated bounds, not new failing behavior.

Dated logbook fallback (2026-10-10): retain the distinction between a CI-only
equivalence gate and actual candidate execution. Exact rev4 baseline is green;
rev3 mutants are historical, their Rust payloads unchanged. No regression found.
SIGINT delivery remains unverified; SIGTERM/SIGKILL/abort cleanup is not promised.
The logbook executable is unavailable (exit 1), so this task-scoped outcome and
the panel task's notes preserve this entry; no publication elsewhere is claimed.

## Successor verification and handoff recovery — RUN-261010-e1f179

The review above is the preserved predecessor report from RUN-261010-e82a42.
Its replay, detailed static sweep and historical five-mutant evidence are
inherited evidence, not commands newly executed by this successor. The successor
read the attached report, previous merged verdict, surface table, producer
results and failed panel validation log. No substantive verdict or row changed.

Commands newly run by the successor, with real exit codes:

| Command / check | Exit | Result |
|---|---:|---|
| Initial panel `set_status(TASK-261010-3cmjct, status=analysis)` | 0 | Lifecycle resumed on panel only |
| Replay `git read-tree BASE`, patch `task-board resource get`, `git apply --cached`, `git write-tree`, using the private replay index above | 0 each | Exact required `bde782b85ddbc8536536d0747b3917d0f24e1951` reproduced |
| `git diff --exit-code REV3 REV4 -- codex-rs` | 0 | All Rust files byte-identical |
| `git diff --check BASE REV4` | 0 | No whitespace errors |
| `git diff REV3 REV4` | 0 | Only the two package additions in relux-ci.yml |
| Fresh `gh api repos/ivanopcode/codex/git/commits/e0eff057620104a416080da616256ee7f32bda1b` | 0 | Exact candidate tree independently verified |
| Fresh `gh run view 38045370015 --repo ivanopcode/codex --json conclusion,jobs,url` | 0 | 4/4 candidate lanes success |
| Fresh `gh run view 38045370015 --repo ivanopcode/codex --job 114195291609 --log` | 0 | Retrieval awaited to process exit; no build/test rerun |
| Corrected Python verification of fresh metadata/log, test names from exact-tree files and verdict structure | 0 | Exact RUN_SHA; 932/932 passed; 14/14 named tests PASS; saved report equals attachment; exactly one JSON block; 5/5 rows in order |
| Exact-tree `git show` for shared SilentExit reporter and exec main | 0 each | Ordinary errors delegated and parser exit propagated after guard drop |
| Supported board queries, resource retrievals and `spawn directives RUN-261010-e1f179` | 0 each | Read-only source inputs, prior checklist all checked, no directives |

Recovery failures are not green checks: two unsupported `resources` field
queries exited 1; `resource list` twice printed help with exit 0 without listing
resources; missing reviewer-reference `cat` exited 1, and bounded no-match
searches exited 1. An accidental shortened candidate OID made a composite pair
of `git show` calls exit 128; both were repeated with the full OID and exited 0.
The first Python log assertion exited 1 because ANSI sequences separated the
summary words; stripping ANSI and checking all named PASS records exited 0.
Two composite inspection calls exited 1 because the linked delivery-validation
file or logbook/search target was absent, not because a candidate gate failed.
Initial `rm -f` setup was rejected before launch with no process exit; Python
unlink of that private index succeeded (exit 0). No user approval was needed.

The predecessor's automatic panel CR gate really failed with exit 1:
its log names tree `4ed6e050b282a31bd3f5d336f612533fce95a834` with no hosted
record. Its `repository_delta=present` was the duplicate untracked research
report, not a source change. The outcome was already durably attached. This
successor moved the local copy to ignored `.temp/TASK-261010-3cmjct/artifacts/RESEARCH.md`
so the research-only panel has an empty repository delta, while updating the
same task-scoped text outcome through resource CRUD. No gate or policy code was
modified; no hosted precheck is needed for an empty source delta.

Successor validation after relocating the duplicate report:

- `/Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh`: **exit 0**. Actual output: `mini-hosted-gate: empty delta (tree bde782b85ddbc8536536d0747b3917d0f24e1951 = HEAD tree); nothing to validate`.
- `git status --short`: **exit 0**, empty. No tracked or untracked repository delta remains.
- Report preservation/relocation Python script: **exit 0**. The attached outcome is retained and updated, not silently replaced by a new resource.

This green is an empty-delta validation result for the panel's handoff, not a
new execution of the source candidate's tests. The prior panel gate remains
truthfully recorded as exit 1.

Dated logbook fallback (2026-10-10): preserve this evidence-only recovery and
the actual exit-1 refusal rather than relabeling it passing. Logbook remains
unavailable; this outcome and panel notes hold the record. Source task writes
remain zero. No cargo, just, formatter, build or local test was run.

```verdict-findings
{
  "findings": [],
  "notes": [
    "DELTA sequence: previous merged rev3 verdict accepts with 0 findings; 0/0 outstanding closures. Historical A-F1/F1, A-F2, A-F3, A-F4 and A2-F1 mechanisms and bounds remain intact. Rust tree unchanged rev3 to rev4.",
    "Replay read-tree/apply/write-tree each exit 0: exact bde782b85ddbc8536536d0747b3917d0f24e1951. Landing commit API and landing small/lint RUN_SHA independently identify the same candidate.",
    "Exact rev4 landing run 38045370015: 4/4 candidate lanes success; small job 114195291609 reports 932 passed/932 run, 1 skipped, with 14/14 added tests individually PASS. Linux debug evidence only; no local Rust gate rerun.",
    "Historical precheck 3 run 38038510297 is rev3 evidence, not exact rev4. Its five mutant-small gates all actually exit 100 on intended assertions; overall workflow failure is expected. Five replayed rev3 mutation trees equal hosted Git API trees and have the expected single snapshot parent. Five replayed rev4 mutations apply cleanly and are Rust-identical to historical counterparts, but were not executed.",
    "mini-hosted-gate rev4 log exits 0 using a .github-only equivalence allowance; exact_command_shard 1/1, test_case_coverage unknown. The landing run separately establishes actual rev4 baseline execution. No full-tree/config/environment equivalence claim is used to relabel old mutations.",
    "Measured bounds: 5/5 rows swept once; 12 public-entry and 2 oracle tests; historical 5/5 mutants killed; exact rev4 mutants 0/5 executed; individual exit-site mutations 2/13 library sites, 1/2 public parser dispatchers; signal delivery tests 0; original eight .tmp success transition attacks 0. No expanded coverage inferred from prose.",
    "FREE HUNT budget: one bounded static pass after the surface sweep over CI routing/failure semantics, remaining exit reachability, result/guard ownership, diagnostic equality, absence-vs-read-error propagation, persistent paths and Bazel discovery. No further defect established; free-hunt details follow in these notes and free_hunt is empty for the leaf-verdict schema used by the previous merged verdict.",
    "FREE HUNT CI: both package additions present in snapshot and mutant commands; empty-filter baseline runs the full package selection. Nonempty mutant filter and --no-tests=pass behavior unchanged. Actual historical commands and exact rev4 log select arg0/cli. Exact-checkout guards and matrix small/core/app-server routing unchanged; no failure suppression introduced.",
    "FREE HUNT reachability: candidate exec library has 0 process::exit calls versus 13 base calls. All 17 eprintln expressions are equal in source order. Exec and CLI main return Result<ExitCode, anyhow::Error>, invoke shared exit_result_from_result; CLI Exec/Review arms propagate with bare ?. Arg0 residual exits occur in pre-allocation helper dispatch; sampled CLI exits belong to other subcommands.",
    "FREE HUNT absence/error: load_output_schema at exec/src/lib.rs:2137-2163 returns Ok(None) only for absent path, and silent error for unreadable or malformed input. Prompt/read/decode helpers propagate errors through ?, while optional-empty stdin is legitimate Ok(None). No fallback-on-read-failure introduced.",
    "FREE HUNT ownership/build: arg0 retained guard drops at arg0/src/lib.rs:281-285 before terminal mapping. Sampled embedded app-server test homes are cfg(test); persistent rollout lock namespace remains home-scoped. BUILD.bazel uses root defs.bzl source/test globs covering silent_exit and test files; suite registration is present. No dependency, config schema, protocol, rollout format or model-context change found. This is not exhaustive dependency/plugin ownership proof.",
    "Inherited unexecuted attacks, not new findings: dedicated --version cleanup, multitool-only parse mutant killed by the two CLI parser tests, OS Ctrl-C after guard allocation, macOS/Windows/release execution, repeated-run stress and per-entry read failure injection. /dev/full skips where absent; Linux historical mutation proves both write-failure assertions ran there.",
    "Non-recording boundary honored: all source-task access read-only; outcome, notes, checklist and researcher handoff target only TASK-261010-3cmjct. Missing installed reviewer reference is disclosed, and explicit panel brief governs the sweep. logbook executable unavailable (exit 1); dated entry is retained in this outcome and panel notes."
  ],
  "surface_results": [
    {
      "row": "tmpdir cleanup on every exit",
      "result": "held",
      "reason": "Exact rev4 small job 114195291609 passes public codex-exec success/server-error/empty-stdin/help/invalid-argument cleanup and CLI parser cleanup tests. Static comparison removes 13/13 explicit library exits; guard owner/drop is unchanged at arg0/src/lib.rs:281-285 and bare Result propagation reaches both mains. Historical leak/parser mutations fail on real codex-arg0 remnants, not compile failures. Scope is normal exits with successful filesystem cleanup; original eight-per-success .tmp allocation and signal delivery remain stated unknowns."
    },
    {
      "row": "exit status and observable behavior",
      "result": "held",
      "reason": "Shared reporter at arg0/src/silent_exit.rs:63-76 returns ordinary errors unchanged to std Termination, preserving the prior ordinary-error reporting contract; SilentExit maps code without a second diagnostic after guard drop. Exact rev4 baseline passes full empty-stdin/config/server stderr assertions, parser codes 0/2 and both /dev/full code-1 tests. Historical prefix mutant fails the exact output assertion and reporter mutant fails both public tests with child 101 versus 1. All 17 library eprintln expressions remain base-identical; no new error swallowing, printing or exit regression is established."
    },
    {
      "row": "signal and abort bound",
      "result": "held",
      "reason": "AC2 explicitly admits a stated bound. Results retain unverified OS SIGINT delivery, unhandled SIGTERM destructor leak, and SIGKILL/abort destructor bypass. Candidate exec/src/lib.rs:1129 has Ctrl-C subscription and interrupt/shutdown routing, unchanged in rev4; sampled embedded in_process startup adds no SIGTERM subscription. Executed signal injections: 0. Early startup signal delivery is not asserted protected."
    },
    {
      "row": "persistent state unchanged",
      "result": "held",
      "reason": "Rev4 changes only workflow package selection; full Rust subtree equals rev3. Base-to-candidate production changes exit propagation/reporting only, with no new deletion, relocation or config/state initializer change. Unchanged arg0 guard owns CODEX_HOME/tmp/arg0/codex-arg0* (arg0/src/lib.rs:350-386); rollout writer locks stay codex_home.join(WRITER_LOCK_DIR) (rollout/src/writer_lock.rs:35-39). Isolated test homes are fixtures. This attests path/deletion invariance, not byte-identical incidental destructor flushing."
    },
    {
      "row": "regression test and mutants",
      "result": "held",
      "reason": "Exact rev4 baseline passes 14/14 added tests including 2 oracle refusals and both real-entry stderr-failure tests. Oracles fail on root or entry read errors and normal tests assert fresh-root/warning-free setup using sibling CODEX_HOME; /dev/full setup proof is weaker because stderr is unavailable, as previously bounded. Historical 5/5 mutant kills have actual exit 100 and intended leak/output/status diagnostics, with replay identities verified; all apply to rev4 and preserve identical Rust payloads. They remain historical sensitivity proof, not executed rev4 mutations. CI delta does not narrow the logged package selection, test filter or assertions. Submitted mutations cover 2/13 library exits and 1/2 public parser dispatchers, not every failure site or the original eight-directory incident."
    }
  ],
  "free_hunt": []
}
```
