# Merged review verdict — TASK-261007-3v81ko CR revision 2 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261010-2s8bqd_panel-verdict.md` (changes_requested), `TASK-261010-sg1s87_panel-verdict.md` (accept), `TASK-261010-3o98tr_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A2-F1",
      "row": "exit status and observable behavior",
      "invariant": "Ordinary errors must retain the previous failure exit status even when their terminal stderr write fails.",
      "mechanism": "Candidate codex-rs/arg0/src/silent_exit.rs:63 uses eprintln! for non-SilentExit errors. Both public mains now call this helper. Base mains returned anyhow::Result, whose Rust 1.95 Result Termination uses attempt_print_to_stderr and ignores write failures. eprintln! instead panics on failing stderr. Public codex-exec --worktree --ephemeral returns an ordinary anyhow error at exec/src/lib.rs:303 before any normal stderr output, exposing the new panic path with stderr attached to /dev/full. Static source proof; candidate runtime status is not measured. Delegate ordinary errors to the existing Termination implementation and request a public-binary regression test.",
      "reproductions": [
        {
          "test_file": "codex-rs/exec/tests/suite/tmpdir_cleanup.rs",
          "command": "env CODEX_HOME=\"$FIXTURE_HOME\" TMPDIR=\"$FIXTURE_TMP\" TEMP=\"$FIXTURE_TMP\" TMP=\"$FIXTURE_TMP\" RUST_LOG=off \"$CODEX_EXEC_BIN\" --worktree --ephemeral 2>/dev/full",
          "expected_failure": "Requested Linux hosted attack, NOT executed: use the exact candidate binary, fresh writable sibling home/temp directories, and assert exit 1 plus no leaked arg0 directories. The candidate reporter is inferred to panic on ENOSPC instead of returning 1; a new exec_ordinary_error_with_failing_stderr_preserves_exit_code test should fail that status assertion. The base Termination reporter ignores ENOSPC and returns failure.",
          "pinned_blobs": [
            "d41f27b7c675f822dad13e4b7bd760b9b78dfe27"
          ]
        },
        {
          "test_file": "codex-rs/cli/tests/exec_tmpdir_cleanup.rs",
          "command": "env CODEX_HOME=\"$FIXTURE_HOME\" TMPDIR=\"$FIXTURE_TMP\" TEMP=\"$FIXTURE_TMP\" TMP=\"$FIXTURE_TMP\" RUST_LOG=off \"$CODEX_BIN\" --remote ws://127.0.0.1:1 exec 2>/dev/full",
          "expected_failure": "Requested Linux hosted attack, NOT executed: the remote/exec incompatibility returns an ordinary anyhow error from cli/src/main.rs:2158 through cli_main and the shared reporter. A new cli_exec_ordinary_error_with_failing_stderr_preserves_exit_code test should require exit 1 and cleaned arg0 state; candidate reporting is inferred to panic on the failing stderr sink.",
          "pinned_blobs": [
            "34d60b881edc77a9beb7ea1a984b1a9e2a4691e2"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-2s8bqd"
      ]
    }
  ],
  "notes": [
    "[TASK-261010-2s8bqd] Replay and GitHub snapshot commit 98ae625bdd680caf632828105d807d8723e163e8 both identify tree ca07d336e99eb0ddcb15a180bbaaaf2a45388835. Review is source plus exact-tree hosted evidence, with no locally executed Rust gates.",
    "[TASK-261010-2s8bqd] Rev1 A-F1/F1 parser leaks, A-F2 normal stderr-prefix regression, A-F3 fail-open/vacuous oracles, and A-F4 false SIGTERM claim are addressed. A2-F1 is a newly introduced write-failure class, not a repeat of the previously corrected normal-output prefix defect.",
    "[TASK-261010-2s8bqd] Coverage: 5/5 surface rows swept; 12/12 new tests pass; 4/4 submitted mutants killed; 2/13 original explicit exec exit sites mutated plus 1/2 parser dispatchers mutated; 0/4 mutants prove the original eight-per-success .tmp* incident; 0 OS-signal delivery tests. Multitool parser has 2 passing public-entry tests but no dedicated mutant. These fractions are bounds, not universal exit-site or platform claims.",
    "[TASK-261010-2s8bqd] The hosted log's exit 100 is an expected failing gate on each mutant; gh retrieval exit 0 only proves successful evidence retrieval. Aggregate CI failure is expected from the mutant matrix, not a failure of the unmodified candidate lanes.",
    "[TASK-261010-2s8bqd] No logbook executable or board logbook operation was available. The dated logbook entry is preserved above in this panel outcome; no control-root file or source task was written.",
    "[TASK-261010-sg1s87] Non-recording panel: no accept_cr, reject_cr, withdraw_cr, set_status, handoff, resource mutation or notes write was performed on TASK-261007-3v81ko. All outcome and lifecycle writes target TASK-261010-sg1s87.",
    "[TASK-261010-sg1s87] Zero local builds or test executions (no cargo/just invocations). Execution evidence is hosted precheck 2 run 38021154057 on the exact candidate tree ca07d336 (lint/small/core/app-server success, 12 new tests pass, 4/4 mutants killed) plus the CR rev2 validation log (mini-hosted-gate exit 0).",
    "[TASK-261010-sg1s87] Rev1 closure verified in-tree: A-F1 fixed by try_parse plus err.print plus silent code in both dispatchers with 4 parser no-leak tests and exec_parse_exit killed; A-F2 fixed by the silent-exit path with 3 full-string stderr tests and empty_stdin_error_prefix killed; A-F3 fixed by fail-closed oracles with 2 should_panic attack tests, a sibling CODEX_HOME and a setup-exercised precondition; A-F4 fixed by the truthful signal bound in the results text; F1-clap is the same site as A-F1 and is fixed and tested with it.",
    "[TASK-261010-sg1s87] Clap equivalence verified against the pinned clap_builder 4.5.58 source (docs.rs): Error::exit() is exactly `let _ = self.print(); process::exit(self.exit_code())`, so the try_parse plus print plus silent-code replacement renders identical bytes, streams and codes (0 help, 2 parse error) including the broken-pipe swallow. Parser::parse() is try_parse() plus exit() on error, so the only behavioral delta is destructors running.",
    "[TASK-261010-sg1s87] Termination equivalence verified: exit_code_from_result maps Ok to SUCCESS, SilentExit to its code with no output, and every other error to `Error: {Debug}` plus FAILURE, byte-identical to the previous `fn main() -> anyhow::Result<()>` Termination. The sorted eprintln set in codex-rs/exec/src/lib.rs is identical between base and candidate (diff exit 0).",
    "[TASK-261010-sg1s87] SilentExit propagation verified end to end: all 13 converted sites plus both dispatcher arms return it directly, every intermediate step (resolve/load/bootstrap helpers, run_exec_session tail return, both mains) uses a bare `?` or tail return with no map_err/context/to_string conversion, and run_main_with_arg0_guard drops the guard before the result reaches exit_code_from_result.",
    "[TASK-261010-sg1s87] Improvement note, not a regression: the error_seen path now flushes buffered stdout where the old process::exit(1) silently dropped it; exit code and stderr are unchanged.",
    "[TASK-261010-sg1s87] Accepted stated bounds: --version shares the fixed clap help path (code 0, stdout) but has no dedicated test; the multitool dispatcher has killer-capable tests but no mutant (the rework brief scoped exactly one dispatcher mutant, and the mechanism is shared); the original 8-per-run success-path .tmp* leak was not reproduced, so the 10 isolated no-leak runs guard the invariant rather than proving an 8-to-0 transition; OS signal delivery is unverified and SIGTERM/SIGKILL/abort cleanup is explicitly out of scope.",
    "[TASK-261010-sg1s87] Surface sweep 5/5 with exactly one result per row. Hosted conclusions cite the exact-tree precheck (tree ca07d336), not a green-equivalent reuse. No claim of exhaustive transitive TempDir inventory beyond the exec-path production audit or of dynamic path coverage beyond the hosted lanes.",
    "[TASK-261010-3o98tr] All five previous merged findings were checked individually and addressed; A-F1 and F1 share a parser mechanism but neither was omitted.",
    "[TASK-261010-3o98tr] Replay equals ca07d336e99eb0ddcb15a180bbaaaf2a45388835. Hosted snapshot commit 98ae625bdd680caf632828105d807d8723e163e8 resolves to that same tree via GitHub Git API; the workflow controller commit is not the tested candidate.",
    "[TASK-261010-3o98tr] Hosted candidate lanes 4/4 success; snapshot small 930/930 executed tests pass with 1 skipped; new tests 12/12 pass. Supplied narrowing mutants 4/4 killed, each small test step exit 100. Overall workflow failure is expected-red, not a passing aggregate.",
    "[TASK-261010-3o98tr] Mutation coverage is two of thirteen original library exit sites and one of two public parser dispatchers, plus an output-prefix mutant. No assertion of comprehensive per-site, per-platform, signal or detached-task coverage.",
    "[TASK-261010-3o98tr] Original eight-per-success-run .tmp* allocation source remains unreproduced and unidentified. Passing .tmp* scans protect the invariant, not an observed eight-to-zero transition.",
    "[TASK-261010-3o98tr] SIGINT delivery, release execution, Windows/macOS runtime results, partial-read fault injection and dedicated --version execution are unknown in this evidence. SIGTERM/SIGKILL/abort cleanup is explicitly bounded in the results.",
    "[TASK-261010-3o98tr] The hosted lint package list does not explicitly select the three changed crates for Clippy; snapshot small compiles/tests them. No local cargo/just/build/test commands ran.",
    "[TASK-261010-3o98tr] No mutation, accept/reject/withdraw, status or handoff was performed on TASK-261007-3v81ko. All panel outputs and lifecycle writes target TASK-261010-3o98tr only."
  ],
  "surface_results": [
    {
      "row": "tmpdir cleanup on every exit",
      "result": "held",
      "reason": "Public-entry hosted success/server-error/empty-stdin and both binaries' parser tests pass; three one-site leak mutants fail specifically on leaked arg0 directories. Static attack traces all 13 converted explicit exits through ? to arg0/src/lib.rs:281-285, which drops the owner before returning. Both try_parse branches return instead of exiting. Residual arg0 helper exits precede guard allocation and residual CLI exits belong to other subcommands. Held within normal-exit, successful-removal and stated signal bounds; original macOS eight .tmp* incident remains unknown, not claimed reproduced.",
      "reported_by": "TASK-261010-2s8bqd"
    },
    {
      "row": "exit status and observable behavior",
      "result": "broken",
      "reason": "A2-F1: ordinary-error reporting introduces panic on failing stderr. Exact normal-stderr tests and parser status/stream tests pass, and the prefix mutant fails as intended, but none exercises terminal stderr I/O failure. The static Rust 1.95 implementation comparison establishes the changed failure mechanism; the named new public-entry attacks remain unexecuted.",
      "reported_by": "TASK-261010-2s8bqd"
    },
    {
      "row": "signal and abort bound",
      "result": "held",
      "reason": "Results explicitly say Ctrl-C routing exists but OS delivery is unverified; SIGTERM is unhandled and leaks; SIGKILL/abort skip destructors. Source confirms only tokio::signal::ctrl_c at exec/src/lib.rs:1129 and no SIGTERM subscription in in-process startup. AC2 permits an explicit bound; no signal coverage is claimed.",
      "reported_by": "TASK-261010-2s8bqd"
    },
    {
      "row": "persistent state unchanged",
      "result": "held",
      "reason": "Diff attack finds no persistent path, store initialization, schema or deletion changes. The existing arg0 guard owns only CODEX_HOME/tmp/arg0/codex-arg0*; rollout writer locks remain CODEX_HOME/thread-writer-locks (rollout/src/writer_lock.rs:35-39). Added test homes are sibling fixtures, not production relocation. Held for location/deletion invariance, not byte-identical incidental destructor flushing.",
      "reported_by": "TASK-261010-2s8bqd"
    },
    {
      "row": "regression test and mutants",
      "result": "held",
      "reason": "Snapshot-small log directly shows 12/12 new tests PASS. Mutant logs show relevant full-stderr diff or actual leaked codex-arg0 directories, with gate exit 100 on all four. Oracles now panic on root/entry read failure; setup requires an existing fresh arg0 root and no setup warning, with homes outside isolated TMPDIR. Two oracle attack tests pass. Coverage limitations and the unexecuted new stderr-write-failure attack are stated, not silently counted green.",
      "reported_by": "TASK-261010-2s8bqd"
    }
  ],
  "free_hunt": [
    "[TASK-261010-2s8bqd] Bounded hunt: inspected shared exit helper semantics, both CLI routes and remaining process exits; A2-F1 arose from comparing ordinary-error reporting with pinned Rust Termination, beyond the producer's normal-stderr tests.",
    "[TASK-261010-2s8bqd] Inspected arg0 guard lifetime/thread/runtime return order, keep/forget/static ownership candidates in exec, in-process server/client, core/state/MCP and rollout code. Matching temporary homes in sampled core/MCP/server sources are test-only. No additional production leak mechanism established; this scoped search is not a whole dependency graph proof.",
    "[TASK-261010-2s8bqd] Inspected output-schema absence/read/decode and prompt resolution changes: None maps to Ok(None); read/decode errors still refuse with original diagnostics and silent failure; resume/fork/review propagation uses ?. No new await or post-return cleanup loop added at converted sites. No additional regression established.",
    "[TASK-261010-2s8bqd] Inspected Bazel source/test discovery: defs.bzl globs src/**/*.rs and tests/*.rs/tests/**, so new Rust source and CLI integration tests are included without BUILD changes. No dependencies, generated schemas, protocol wire types or model-visible context changed.",
    "[TASK-261010-2s8bqd] Stopped after these bounded areas and all five rows. Original success-incident root cause, signal delivery, repeated-run stress and Windows/macOS candidate execution remain unknown; Linux hosted evidence was reused, not presented as cross-platform execution.",
    "[TASK-261010-sg1s87] {\"budget\": \"One bounded static pass over the candidate tree after the 5-row sweep: guard lifecycle, full-tree exit inventory with exec-path reachability, production TempDir inventory, persist primitives, clap and Termination equivalence against pinned sources, SilentExit propagation, and mutant semantics. No builds, no edits to product code.\", \"attacks\": [{\"surface\": \"Remaining process::exit reachability from codex-exec and codex exec\", \"result\": \"held\", \"evidence\": \"zero in exec/src; arg0 exits pre-guard (lib.rs:82-164); cli exits confined to TUI/app-server/login/cloud/debug_sandbox paths (main.rs:765,1290,1585,1597); exit_status only from debug_sandbox; stdio watchdog transport-server only\"}, {\"surface\": \"Production TempDir inventory on exec path\", \"result\": \"held\", \"evidence\": \"only the arg0 guard (lib.rs:383-384, prefix codex-arg0, dropped in run_main_with_arg0_guard); rollout temp files are auto-removed; keep/persist are deliberate staging/atomic writes; thread-writer-locks lives under the home, not in a TempDir\"}, {\"surface\": \"Clap try_parse replacement fidelity\", \"result\": \"held\", \"evidence\": \"pinned clap_builder 4.5.58 Error::exit is print plus exit_code; replacement calls the same functions; codes and streams asserted hosted on both dispatchers\"}, {\"surface\": \"SilentExit swallowing by intermediate error mapping\", \"result\": \"held\", \"evidence\": \"all call sites bare ? or tail returns; map_err sites in exec lib wrap unrelated errors (OSS setup, in-process client init); downcast_ref would traverse anyhow contexts in any case\"}, {\"surface\": \"Mutant genuineness (narrowing, killed for the right reason)\", \"result\": \"held\", \"evidence\": \"all 4 apply clean; each reverses one site; kills come from leak assertions and the full-string stderr assert, matching precheck 2 killer table\"}], \"remaining_bounds\": [\"Original success-path .tmp* allocation source unidentified (stated bound).\", \"Only Linux hosted debug entry-point evidence inspected; macOS/Windows execution unknown.\", \"No OS-signal injection was executed (stated bound).\", \"--version and config.toml-load-error bytes covered by shared-mechanism reasoning plus static byte identity, not dedicated full-string tests.\"]}",
    "[TASK-261010-3o98tr] Bounded pass after all five rows: both public dispatchers and their direct run_main propagation, arg0 guard lifetime, changed config/schema/stdin Result propagation, embedded signal chain, test oracle setup and immutable hosted mutant identities. No builds, code changes or first-finding early stop.",
    "[TASK-261010-3o98tr] Residual same-class search: remaining arg0 process exits are helper-dispatch branches before alias guard allocation; remaining cli exits belong to TUI/app-server/login subcommands and are not reachable from the Exec match arm. No residual in-process destructor-skipping exit was established in the examined exec route.",
    "[TASK-261010-3o98tr] Rework regression attack: load_output_schema(None) remains Ok(None); read/JSON failures remain printed error exits; optional empty stdin remains Ok(None); required/forced input never yields None, keeping resolve_prompt's unreachable arm unreachable. Resume/fork/review call sites propagate the new Result with ? rather than swallowing it.",
    "[TASK-261010-3o98tr] Test-evidence attack: verified snapshot-small/lint and all four mutant-small checkout identities and exact mutant diffs; confirmed expected-red exit 100 and intended leak/output assertions rather than compiler failure. Core/app-server evidence was read from job metadata and the attached report. Noted aggregate workflow failure and direct changed-crate Clippy bound.",
    "[TASK-261010-3o98tr] Remaining optional attacks, not claimed executed: a MultitoolCli::parse narrowing mutant killed by cli_exec_help_leaves_no_tmpdirs / cli_exec_invalid_args_leave_no_tmpdirs; a release-mode cleanup lane; directory-entry read fault injection; dedicated --version cleanup; OS signal delivery after observing a live guard. These do not establish defects in the reviewed fixes."
  ]
}
```
