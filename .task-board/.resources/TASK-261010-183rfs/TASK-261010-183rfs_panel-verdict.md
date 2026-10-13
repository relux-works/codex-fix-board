# Panel B verdict — CR-TASK-261007-3v81ko-1 rev1

Panel task: TASK-261010-183rfs (R141 panel B, non-recording review of TASK-261007-3v81ko rev 1).
One-word verdict: accept

## Replay tree check: MATCH

Base 07c018be3507b8d4a5558a85a117b94ed2a23872 plus resource
TASK-261007-3v81ko_change-request_rev1.patch through a temporary index writes tree
e5b504a6db93a1a72cb79cbac37030ad13a26db1, exactly the expected candidate tree.
Changed paths: 3 (codex-rs/exec/src/lib.rs, codex-rs/exec/tests/suite/mod.rs,
codex-rs/exec/tests/suite/tmpdir_cleanup.rs).

## Commands run, with exit codes

Replay (temporary index .temp/TASK-261010-183rfs-replay.idx, never a nested worktree):
- GIT_INDEX_FILE=$IDX git read-tree 07c018be... -> exit 0
- task-board resource get TASK-261007-3v81ko TASK-261007-3v81ko_change-request_rev1.patch -> exit 0
- GIT_INDEX_FILE=$IDX git apply --cached (patch) -> exit 0
- GIT_INDEX_FILE=$IDX git write-tree -> exit 0, printed e5b504a6db93a1a72cb79cbac37030ad13a26db1 (MATCH)

Candidate extraction and static sweep (all read-only against the e5b504a6 tree):
- git archive e5b504a6 (3 paths) | tar -x -> exit 0
- git grep process::exit on BASE codex-rs/exec/src/lib.rs -> exit 0, 13 matches (all converted by the CR)
- git grep process::exit on CANDIDATE codex-rs/exec/src -> exit 1, no matches (expected: all removed)
- git grep or_exit leftovers on candidate exec/src -> exit 1, no matches (expected: rename complete)
- git grep into_path / .keep() / persist / forget( on candidate exec+arg0 src -> only unrelated hits
  (PathBuf::into_path_buf, persisted session-files flag, test names); no TempDir leak primitive -> n/a
- git grep TempDir/tempfile on candidate exec/src (non-test) + arg0 -> only production TempDir is the
  arg0 session guard (codex-rs/arg0/src/lib.rs), held by Arg0PathEntryGuard and dropped after main_fn
  returns, including on Err (run_main_with_arg0_guard) -> n/a
- git grep process::exit across all production codex-rs -> remaining sites are other binaries and
  helper-process dispatch (cli, login, doctor, app-server, bwrap, apply-patch standalone, arg0 helper
  branches that run before any guard exists); none reachable in-process from codex-exec run_main,
  except clap CLI-parser exits (finding F1) -> n/a
- Converted-function call-site audit (load_bootstrap_config x4, resolve_prompt, resolve_root_prompt,
  load_output_schema, read_prompt_from_stdin): every site propagates with ? or tail-returns Result;
  no swallowed errors -> n/a
- Existing exit-assertion audit (server_error_exit, prompt_stdin, output_schema, mcp_required_exit):
  .code(1)/.success() plus contains() substring matchers, compatible with anyhow main rendering -> n/a
- Interrupt/shutdown audit (candidate lib.rs:1114-1230,1308-1326): tokio ctrl_c -> interrupt channel ->
  turn/interrupt -> graceful shutdown -> return through main; error_seen bail preserves exit 1 -> n/a
- Mutant patch checks against the candidate lib.rs blob cdaa155c (matches CR index line and handoff notes):
  git apply --check error_seen_process_exit.patch -> exit 0
  git apply --check empty_stdin_process_exit.patch -> exit 0
- Green-equivalence re-verification: git diff 73c75aed e5b504a6 --stat and git diff 39c264c 07c018be
  --stat -> exit 0 each, both CI-only (.github/dependabot.yaml, .github/workflows/relux-ci.yml);
  cmp of the two full diffs -> exit 0, DIFFS IDENTICAL (hosted run 38009138137 evidence transfers exactly)
- task-board q get (description/scope/ac/notes/resources) and 12x task-board resource get -> exit 0 each
- which logbook -> exit 1 (no logbook CLI on this host; findings live in this outcome plus board note)

Not run: cargo, just, or any build/test (forbidden by the panel brief; shared build target is
serialized). No writes of any kind were made on TASK-261007-3v81ko (only query and resource-get reads).

## Row sweep summary (key aspects)

- tmpdir cleanup on every exit: HELD. 13/13 destructor-skipping exits removed from exec/src;
  zero into_path/keep/forget; guard-drop ordering verified in code; hosted 3/3 isolated-TMPDIR
  leak tests pass (success, server-error, empty-stdin). Residual: F1 (robustness) — clap CLI-parser
  exits (--help/--version exit 0, bad flags exit 2) still skip the arg0 guard drop; pre-existing,
  narrow, janitor self-healed; wanted-test named, not run.
- exit status and observable behavior: HELD. anyhow main preserves exit 1 on all 13 converted paths;
  hosted code/substring assertions pass (433/433 codex-exec incl. pre-existing exit tests). stderr
  gains standard "Error: " rendering and the error_seen path gains one line (note N1); messages kept
  as substrings; no new awaits, no swallowed errors, flush/hang analysis clean.
- signal and abort bound: HELD as stated-bound per the row clause. Results state SIGKILL/abort out of
  scope and SIGTERM/SIGINT delivery unverified; the graceful-shutdown mechanism cited (ctrl_c ->
  turn/interrupt -> return through main) exists in code at the cited lines.
- persistent state unchanged: HELD. Patch changes exit mechanics only; no home/session/sqlite path
  changes; new tests use an isolated home under TMPDIR.
- regression test and mutants: HELD. Hosted 2/2 narrowing mutants killed by the named tests; kill
  attribution is the leak assertions (mutants restore exact pre-fix snippets, so exit-code assertions
  still pass on them); both mutant patches verified to apply cleanly to the candidate tree; child
  genuinely uses the isolated TMPDIR (TMPDIR/TEMP/TMP plus CODEX_HOME/CODEX_SQLITE_HOME env).

Accepted producer bound (verified as honestly stated, twice, in the results outcome): the reporter's
8-per-run success-path .tmp* leak was not reproduced in the producer environment (0 .tmp* on success
and error with 0.159.0, mock and real API), so the .tmp* assertions guard the invariant going forward
rather than demonstrating an 8-to-0 transition; the demonstrated leak fixed is the error-path arg0-dir
leak (verified on 0.159.0: failed runs leaked one codex-arg0* dir, success runs none). See notes N2/N3.

```verdict-findings
{
  "findings": [
    {
      "id": "F1-clap-parser-exit-skips-arg0-guard",
      "row": "tmpdir cleanup on every exit",
      "invariant": "every TempDir created on the codex exec path is dropped or removed on success, error and empty-stdin exits",
      "mechanism": "codex-rs/exec/src/main.rs runs TopCli::parse() (clap derive) inside main_fn, which executes AFTER arg0_dispatch() creates the Arg0PathEntryGuard TempDir (codex-rs/arg0/src/lib.rs: run_main_with_arg0_guard holds the guard across the whole main_fn future). clap parse() calls process::exit on CLI parse errors (code 2) and on --help/--version (code 0), so those CLI-parser exits terminate the process with the guard alive and leak one codex-arg0* dir per invocation under CODEX_HOME/tmp/arg0. Pre-existing: main.rs is untouched by this CR. Blast radius is narrow (CLI-parser exits only, not session exits) and startup janitor_cleanup removes the stale dir on the next run. Fixing it here would mean restructuring the shared arg0 dispatch used by every binary or changing clap exit code 2, both out of proportion for this CR.",
      "reproductions": [
        {
          "test_file": "codex-rs/exec/tests/suite/tmpdir_cleanup.rs (wanted test: exec_help_leaves_no_arg0_dirs)",
          "command": "run codex-exec --help with isolated CODEX_HOME and TMPDIR (same IsolatedExec harness), then assert leaked_arg0_dirs(home) is empty",
          "expected_failure": "wanted test fails: one leaked codex-arg0* dir present after --help exits 0; same shape for an invalid flag exiting 2"
        }
      ],
      "severity": "robustness",
      "repeat-of": null
    }
  ],
  "notes": [
    "N1 stderr rendering under anyhow main: the 13 converted paths now surface as 'Error: <original message>' (anyhow Debug via fn main() -> anyhow::Result<()>) instead of the bare eprintln line, and the error_seen path gains one stderr line where the old code exited silently. Exit codes are exact (1) and original messages are preserved as substrings; pre-existing code/substring assertions (prompt_stdin, server_error_exit, mcp_required_exit, output_schema) all pass on hosted run 38009138137. Standard codebase rendering, disclosed via substring assertions; no action.",
    "N2 non-reproduction bound accepted: results state twice that the issue's 8-per-run success-path .tmp* leak was not reproduced with 0.159.0 in the producer environment (0 .tmp* on success and error, mock and real API). The success-path .tmp* mechanism is therefore still unidentified, and the hosted .tmp* assertions guard the invariant rather than proving an 8-to-0 transition. The CR's demonstrated fix is the error-path arg0 leak (verified pre-fix behavior: failed runs leaked one codex-arg0* dir). This residual unknown is about the original issue's environment, not a defect in the CR, which strictly reduces leak surface (13 destructor-skipping exits removed, zero added) on every converted path.",
    "N3 mutant lane filter: hosted precheck ran mutants with test filter 'test(tmpdir_cleanup) | test(tmpdir)', so the claim that pre-existing exit-code tests still pass on the mutants is by-construction (mutants restore the exact pre-fix snippets those tests passed on) rather than executed. Airtight for process::exit(1) restorations; no action.",
    "N4 remaining process::exit audit: every other production process::exit in codex-rs belongs to a different binary (cli/login/doctor/app-server/bwrap/apply-patch standalone) or to arg0 helper-process dispatch branches that run before any TempDir guard exists. None is reachable in-process from codex-exec run_main except the clap parser exits in F1.",
    "N5 resolve_prompt unreachable! verified safe: read_prompt_from_stdin returns Ok(None) only for StdinPromptBehavior::OptionalAppend; the RequiredIfPiped/Forced arms used by resolve_prompt bail on every empty path, so the else-unreachable arm is genuinely unreachable."
  ],
  "surface_results": [
    {
      "row": "tmpdir cleanup on every exit",
      "result": "held",
      "evidence": "base exec/src/lib.rs had exactly 13 process::exit (git grep exit 0); candidate exec/src has zero (grep exit 1, no matches); zero TempDir into_path/keep/forget; arg0 guard provably dropped on every converted Err path (run_main_with_arg0_guard drops after main_fn returns); hosted run 38009138137: 3/3 isolated-TMPDIR tests pass (success, server-error, empty-stdin), 0 .tmp* and 0 arg0 leaks; 2/2 narrowing mutants killed, proving the tests detect the mechanism. Residual F1 (robustness) attached."
    },
    {
      "row": "exit status and observable behavior",
      "result": "held",
      "evidence": "anyhow main maps every converted Err to exit 1, matching all 13 old exit(1) sites; hosted 433/433 codex-exec incl. pre-existing .code(1)/.success/contains assertions; every converted call site propagates with ? (none swallowed); no new awaits (no new hangs); stdout flushing is a superset of old behavior (destructors now run). stderr rendering delta recorded as note N1."
    },
    {
      "row": "signal and abort bound",
      "result": "held",
      "evidence": "results outcome states the explicit bound (SIGKILL/abort out of scope by construction; SIGTERM/SIGINT delivery unverified), satisfying the row's covered-or-stated clause; cited mechanism grounded in candidate code (ctrl_c -> interrupt channel -> turn/interrupt -> graceful shutdown -> return through main, lib.rs:1114-1230,1308-1326)."
    },
    {
      "row": "persistent state unchanged",
      "result": "held",
      "evidence": "CR touches only exit mechanics (13 exit sites -> Result returns, 4+3+4+2 call-site updates) plus new tests; no changes to find_codex_home, sqlite_home, session/store paths; new tests run against an isolated home/ dir under TMPDIR; pre-existing message/exit assertions pass on hosted."
    },
    {
      "row": "regression test and mutants",
      "result": "held",
      "evidence": "hosted 2/2 mutants killed by the named tests (error_seen by exec_server_error_leaves_no_tmpdirs, empty_stdin by exec_empty_stdin_leaves_no_tmpdirs); kills attribute to leak assertions since exit-code assertions pass on mutants by construction; both mutant patches verified git apply --check clean (exit 0) against candidate blob cdaa155c; child uses isolated TMPDIR via TMPDIR/TEMP/TMP/CODEX_HOME/CODEX_SQLITE_HOME env; tmp_entries scans tempfile's .tmp prefix and arg0 root matches code (tmp/arg0, codex-arg0 prefix)."
    }
  ],
  "free_hunt": [
    {
      "area": "CLI-parser exits (TopCli::parse in exec/src/main.rs)",
      "outcome": "finding F1 (robustness): --help/--version/bad-flag exits skip the arg0 guard drop; pre-existing, narrow, janitor-healed; wanted test named, not run (no builds per brief)"
    },
    {
      "area": "success-path .tmp* root cause from the issue report",
      "outcome": "no finding in the CR: mechanism unidentified and unreproduced in the producer environment (stated bound, accepted as note N2); CR removes the proven error-path mechanism and guards the .tmp* invariant on all three exit classes"
    },
    {
      "area": "TempDir owned by detached task or static; keep/forget/persist primitives",
      "outcome": "no finding: no such site on the codex-exec path; only production TempDir is the arg0 guard with verified drop ordering"
    },
    {
      "area": "early return paths without a dedicated test (config/schema/login/git-check sites)",
      "outcome": "no finding: all 13 sites share the single verified mechanism (Err return -> guard drop in run_main_with_arg0_guard); tested at both ends (pre-network stdin error, post-session error_seen) plus mutants; per-site tests would add no signal"
    },
    {
      "area": "load_output_schema None-path and resolve_* refactors",
      "outcome": "no finding: None -> Ok(None) preserved; unreachable! arm verified genuinely unreachable (note N5)"
    },
    {
      "area": "buffered-output flush and hang regressions",
      "outcome": "no finding: new paths run strictly more destructors (superset flush); no new await points introduced"
    }
  ]
}
```
