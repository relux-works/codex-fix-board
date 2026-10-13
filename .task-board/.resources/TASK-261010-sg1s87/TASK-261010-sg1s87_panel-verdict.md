# Panel B verdict — TASK-261007-3v81ko CR rev2 (R141 non-recording panel, tb-R141/tb-R147)

Verdict: accept

## Replay tree check (mandatory, first)

Base 07c018be3507b8d4a5558a85a117b94ed2a23872 plus
TASK-261007-3v81ko_change-request_rev2.patch, applied through a temporary
index (never a nested worktree), gives tree
ca07d336e99eb0ddcb15a180bbaaaf2a45388835 — exactly the expected candidate
tree. Match: yes. No replay mismatch, so the review proceeded.

## Commands run (with exit codes)

- git rev-parse --show-toplevel → exit 0
- GIT_INDEX_FILE=$IDX git read-tree 07c018be... → exit 0
- task-board resource get TASK-261007-3v81ko
  TASK-261007-3v81ko_change-request_rev2.patch → ok, file materialized
- GIT_INDEX_FILE=$IDX git apply --cached (patch) → exit 0
- GIT_INDEX_FILE=$IDX git write-tree → ca07d336..., exit 0, matches expected
- git archive ca07d336... (arg0, exec, cli, login, utils/cli) | tar -x → exit 0
- git grep / git show reads on base and candidate trees → exit 0
- 4 mutant patches extracted from TASK-261007-3v81ko_mutants.json,
  git apply --check against candidate files → all 4 clean, exit 0
- diff of sorted eprintln sets, base vs candidate codex-rs/exec/src/lib.rs →
  identical, exit 0
- cargo / just / build / test invocations: 0 (forbidden by the panel brief;
  execution evidence is hosted precheck 2 run 38021154057 on the exact tree
  plus the CR validation log with mini-hosted-gate exit 0)
- Two self-inflicted shell issues, both superseded and not evidence: one
  process-substitution one-liner failed with exit 2 under /bin/sh (rerun with
  temp files, exit 0); one filesystem-wide find for clap sources was
  terminated before producing output (replaced by direct registry and
  docs.rs reads of the pinned version).

## Row sweep summary

5/5 surface rows swept with exactly one result each: all held, 0 findings.
Every rev1 finding (A-F1..A-F4 plus F1-clap, same site as A-F1) is addressed
in this tree and killed or textually closed by hosted precheck 2 evidence on
the exact candidate tree. Stated bounds (--version untested, cli dispatcher
unmutated, original 8-per-run .tmp* unreproduced, signal delivery unverified
with SIGTERM/SIGKILL/abort explicitly out of scope) are accepted as notes.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Non-recording panel: no accept_cr, reject_cr, withdraw_cr, set_status, handoff, resource mutation or notes write was performed on TASK-261007-3v81ko. All outcome and lifecycle writes target TASK-261010-sg1s87.",
    "Zero local builds or test executions (no cargo/just invocations). Execution evidence is hosted precheck 2 run 38021154057 on the exact candidate tree ca07d336 (lint/small/core/app-server success, 12 new tests pass, 4/4 mutants killed) plus the CR rev2 validation log (mini-hosted-gate exit 0).",
    "Rev1 closure verified in-tree: A-F1 fixed by try_parse plus err.print plus silent code in both dispatchers with 4 parser no-leak tests and exec_parse_exit killed; A-F2 fixed by the silent-exit path with 3 full-string stderr tests and empty_stdin_error_prefix killed; A-F3 fixed by fail-closed oracles with 2 should_panic attack tests, a sibling CODEX_HOME and a setup-exercised precondition; A-F4 fixed by the truthful signal bound in the results text; F1-clap is the same site as A-F1 and is fixed and tested with it.",
    "Clap equivalence verified against the pinned clap_builder 4.5.58 source (docs.rs): Error::exit() is exactly `let _ = self.print(); process::exit(self.exit_code())`, so the try_parse plus print plus silent-code replacement renders identical bytes, streams and codes (0 help, 2 parse error) including the broken-pipe swallow. Parser::parse() is try_parse() plus exit() on error, so the only behavioral delta is destructors running.",
    "Termination equivalence verified: exit_code_from_result maps Ok to SUCCESS, SilentExit to its code with no output, and every other error to `Error: {Debug}` plus FAILURE, byte-identical to the previous `fn main() -> anyhow::Result<()>` Termination. The sorted eprintln set in codex-rs/exec/src/lib.rs is identical between base and candidate (diff exit 0).",
    "SilentExit propagation verified end to end: all 13 converted sites plus both dispatcher arms return it directly, every intermediate step (resolve/load/bootstrap helpers, run_exec_session tail return, both mains) uses a bare `?` or tail return with no map_err/context/to_string conversion, and run_main_with_arg0_guard drops the guard before the result reaches exit_code_from_result.",
    "Improvement note, not a regression: the error_seen path now flushes buffered stdout where the old process::exit(1) silently dropped it; exit code and stderr are unchanged.",
    "Accepted stated bounds: --version shares the fixed clap help path (code 0, stdout) but has no dedicated test; the multitool dispatcher has killer-capable tests but no mutant (the rework brief scoped exactly one dispatcher mutant, and the mechanism is shared); the original 8-per-run success-path .tmp* leak was not reproduced, so the 10 isolated no-leak runs guard the invariant rather than proving an 8-to-0 transition; OS signal delivery is unverified and SIGTERM/SIGKILL/abort cleanup is explicitly out of scope.",
    "Surface sweep 5/5 with exactly one result per row. Hosted conclusions cite the exact-tree precheck (tree ca07d336), not a green-equivalent reuse. No claim of exhaustive transitive TempDir inventory beyond the exec-path production audit or of dynamic path coverage beyond the hosted lanes."
  ],
  "surface_results": [
    {
      "row": "tmpdir cleanup on every exit",
      "result": "held",
      "reason": "13/13 destructor-skipping exits removed from the exec path and zero remain: full-tree audit shows the other process::exit sites are pre-guard arg0 helper branches or separate subcommands/binaries (TUI, app-server, login, cloud, debug_sandbox, doctor, stdio watchdog, sandbox helpers), none reachable in-process from codex-exec or codex exec. The only production TempDir on the exec path is the arg0 guard with verified drop-before-map ordering; keep/persist sites are deliberate plugin-staging and atomic-write persists. Hosted exact-tree evidence: 10 isolated no-leak runs (success, server error, empty stdin, 3 full-stderr, clap exits 0/2 on both dispatchers) plus 3 leak-class mutants killed."
    },
    {
      "row": "exit status and observable behavior",
      "result": "held",
      "reason": "Exact bytes by construction plus executed proof: identical eprintln set base vs candidate, same clap print() rendering with asserted streams and codes (0/1/2), Termination-identical non-silent mapping, and SilentExit propagation with no intermediate conversion. Hosted exact-tree evidence: 3 full-string stderr assert_eq tests, help/invalid-args stream and code assertions on both dispatchers, 1 stderr-class mutant killed, and the pre-existing substring suites green."
    },
    {
      "row": "signal and abort bound",
      "result": "held",
      "reason": "Results state a truthful explicit bound, which AC2 permits: Ctrl-C is routed through the existing tokio ctrl_c interrupt channel with delivery unverified (no signal-injection harness), SIGTERM has no handler on this exec path and is stated as not cleaned up, SIGKILL/abort are out of scope by construction. Signal code is untouched by this CR (patch file list), and the ctrl_c subscription is present at candidate exec/src/lib.rs:1127-1133."
    },
    {
      "row": "persistent state unchanged",
      "result": "held",
      "reason": "Static diff attack: the patch changes only exit mechanics (silent returns, ExitCode mapping, try_parse dispatchers) and tests. No find_codex_home, sqlite, session, store or rollout path logic changes; the arg0 guard still owns only CODEX_HOME/tmp/arg0/codex-arg0*. Held for location and deletion invariance."
    },
    {
      "row": "regression test and mutants",
      "result": "held",
      "reason": "12/12 new tests pass hosted on the exact tree, driving the real binaries with isolated TMPDIR and sibling CODEX_HOME. All 4 narrowing mutants apply clean to the candidate tree (verified git apply --check) and are killed on it by tests asserting the exact reverted property (leak assertions for the 3 exit restorations, full-string stderr for the Error-prefix mutant). Oracles fail closed (2 should_panic attacks pass hosted) and the setup-exercised precondition is non-vacuous (fresh fixture per test, warning string matches production)."
    }
  ],
  "free_hunt": [
    "{\"budget\": \"One bounded static pass over the candidate tree after the 5-row sweep: guard lifecycle, full-tree exit inventory with exec-path reachability, production TempDir inventory, persist primitives, clap and Termination equivalence against pinned sources, SilentExit propagation, and mutant semantics. No builds, no edits to product code.\", \"attacks\": [{\"surface\": \"Remaining process::exit reachability from codex-exec and codex exec\", \"result\": \"held\", \"evidence\": \"zero in exec/src; arg0 exits pre-guard (lib.rs:82-164); cli exits confined to TUI/app-server/login/cloud/debug_sandbox paths (main.rs:765,1290,1585,1597); exit_status only from debug_sandbox; stdio watchdog transport-server only\"}, {\"surface\": \"Production TempDir inventory on exec path\", \"result\": \"held\", \"evidence\": \"only the arg0 guard (lib.rs:383-384, prefix codex-arg0, dropped in run_main_with_arg0_guard); rollout temp files are auto-removed; keep/persist are deliberate staging/atomic writes; thread-writer-locks lives under the home, not in a TempDir\"}, {\"surface\": \"Clap try_parse replacement fidelity\", \"result\": \"held\", \"evidence\": \"pinned clap_builder 4.5.58 Error::exit is print plus exit_code; replacement calls the same functions; codes and streams asserted hosted on both dispatchers\"}, {\"surface\": \"SilentExit swallowing by intermediate error mapping\", \"result\": \"held\", \"evidence\": \"all call sites bare ? or tail returns; map_err sites in exec lib wrap unrelated errors (OSS setup, in-process client init); downcast_ref would traverse anyhow contexts in any case\"}, {\"surface\": \"Mutant genuineness (narrowing, killed for the right reason)\", \"result\": \"held\", \"evidence\": \"all 4 apply clean; each reverses one site; kills come from leak assertions and the full-string stderr assert, matching precheck 2 killer table\"}], \"remaining_bounds\": [\"Original success-path .tmp* allocation source unidentified (stated bound).\", \"Only Linux hosted debug entry-point evidence inspected; macOS/Windows execution unknown.\", \"No OS-signal injection was executed (stated bound).\", \"--version and config.toml-load-error bytes covered by shared-mechanism reasoning plus static byte identity, not dedicated full-string tests.\"]}"
  ]
}
```

