# TASK-261007-3v81ko review verdict, CR revision 4 (landed-tree rework)

Verdict: **accept**

Panel outcomes: `TASK-261010-3cmjct_panel-verdict.md` (delta, codex gpt-6.1-sol high: accept, 0 findings).

Merge note (orchestrator): CR rev4 is the landed-tree rework produced by `worktree prepare-landed-review` / `start-landed-rework`. Its only
difference from rev3, which panels A, B and delta plus the recording reviewer accepted, is the CI-only `.github/workflows/relux-ci.yml` hunk
from trunk 25431940. The update patch in the export is restricted to that file. A full A+B round is not repeated for a CI-only delta;
the delta reviewer verified exactly that difference. The rev3 review remains history; this verdict authorizes only the rev4 tree
bde782b85ddbc8536536d0747b3917d0f24e1951.

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
