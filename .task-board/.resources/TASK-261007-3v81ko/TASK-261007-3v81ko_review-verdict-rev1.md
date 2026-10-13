# Merged review verdict — TASK-261007-3v81ko CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261010-gjhb8b_panel-verdict.md` (changes_requested), `TASK-261010-183rfs_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A-F1",
      "row": "tmpdir cleanup on every exit",
      "invariant": "Every normal exec exit must return through the owner of its TempDir guard, including errors at the public entry point.",
      "mechanism": "Residual, pre-existing bypass inside the stated every-exit scope: arg0_dispatch_or_else creates the CODEX_HOME/tmp/arg0/codex-arg0* guard before calling main_fn. codex-exec then calls TopCli::parse (exec/src/main.rs:30); codex exec calls MultitoolCli::parse (cli/src/main.rs:1033). Clap 4.5.58 parse exits on invalid arguments/help rather than returning, so run_main_with_arg0_guard never reaches its drop. The patch changes only exec/src/lib.rs and leaves both dispatchers untouched. Invalid arguments therefore still skip destruction when alias setup succeeds. This is static call-chain proof, not a runtime reproduction in this panel.",
      "reproductions": [
        {
          "test_file": "codex-rs/exec/tests/suite/tmpdir_cleanup.rs (requested new exec_parse_error_leaves_no_tmpdirs test)",
          "command": "INSTA_WORKSPACE_ROOT=\"$PWD\" just test -p codex-exec -E 'test(exec_parse_error_leaves_no_tmpdirs)'",
          "expected_failure": "After adding the named test, invoke the real codex-exec binary with --definitely-invalid-option and an isolated CODEX_HOME whose alias setup is verified. Clap exits 2 and leaves codex-arg0* behind. Also exercise --help (exit 0). Not executed here.",
          "pinned_blobs": [
            "e5b504a6db93a1a72cb79cbac37030ad13a26db1:codex-rs/exec/tests/suite/tmpdir_cleanup.rs (requested new exec_parse_error_leaves_no_tmpdirs test)"
          ]
        },
        {
          "test_file": "codex-rs/cli/tests/exec_tmpdir_cleanup.rs (requested new exec_parse_error_leaves_no_tmpdirs test)",
          "command": "INSTA_WORKSPACE_ROOT=\"$PWD\" just test -p codex-cli -E 'test(exec_parse_error_leaves_no_tmpdirs)'",
          "expected_failure": "After adding the named test, invoke codex exec --definitely-invalid-option, verify alias setup happened, then assert no arg0 session dir remains. Current dispatcher exits before dropping it. Not executed here.",
          "pinned_blobs": [
            "e5b504a6db93a1a72cb79cbac37030ad13a26db1:codex-rs/cli/tests/exec_tmpdir_cleanup.rs (requested new exec_parse_error_leaves_no_tmpdirs test)"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-gjhb8b"
      ]
    },
    {
      "id": "A-F2",
      "row": "exit status and observable behavior",
      "invariant": "Cleanup is the only observable change; stderr bytes and ordering remain stable.",
      "mechanism": "exec/src/lib.rs:2249 changes the empty-stdin branch from eprintln plus exit(1) to an anyhow error. Both public mains return anyhow::Result; Rust Termination prints Error: followed by Debug output when the error reaches main. The final diagnostic consequently changes from No prompt provided via stdin. to Error: No prompt provided via stdin. Likewise configuration errors acquire Error: Error loading config.toml..., and lib.rs:1313 emits an additional Error: exec turn failed after print_final_output for server failures. Anyhow can also emit a backtrace when enabled. Existing tests use substring matches or only status 1, so the hosted green does not preserve the surface-table output invariant. Exit 1 is still preserved on the tested error paths.",
      "reproductions": [
        {
          "test_file": "codex-rs/exec/tests/suite/prompt_stdin.rs (requested new exec_empty_stdin_preserves_stderr test)",
          "command": "INSTA_WORKSPACE_ROOT=\"$PWD\" just test -p codex-exec -E 'test(exec_empty_stdin_preserves_stderr)'",
          "expected_failure": "After adding the test, capture deterministic stderr for a real binary with empty piped stdin and compare the terminal diagnostic line with the base bytes. Candidate has an added Error: prefix. Disable ambient backtraces for the basic comparison; separately exercise enabled backtraces. Not executed here.",
          "pinned_blobs": [
            "e5b504a6db93a1a72cb79cbac37030ad13a26db1:codex-rs/exec/tests/suite/prompt_stdin.rs (requested new exec_empty_stdin_preserves_stderr test)"
          ]
        },
        {
          "test_file": "codex-rs/exec/tests/suite/server_error_exit.rs (requested exact-output assertion)",
          "command": "INSTA_WORKSPACE_ROOT=\"$PWD\" just test -p codex-exec -E 'test(exits_non_zero_when_server_reports_error)'",
          "expected_failure": "With a new assertion excluding an extra terminal diagnostic, the existing mock response.failed entry-point test fails because candidate adds Error: exec turn failed after final output. Current unchanged test passes because it checks only code(1). Requested assertion not executed here.",
          "pinned_blobs": [
            "e5b504a6db93a1a72cb79cbac37030ad13a26db1:codex-rs/exec/tests/suite/server_error_exit.rs (requested exact-output assertion)"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-gjhb8b"
      ]
    },
    {
      "id": "A-F3",
      "row": "regression test and mutants",
      "invariant": "The cleanup oracle may attest absence only after a successful, complete directory read; the protected resource must actually have existed.",
      "mechanism": "New tmpdir_cleanup.rs:10-13 and :29-33 convert every read_dir error to an empty Vec and flatten away per-entry read failures. assert_no_leaks then interprets these as clean. ENOTDIR, permission/I/O faults and partial reads are not evidence of absence. In addition the tests never establish that arg0 setup succeeded: production explicitly permits setup failure and proceeds with no guard. In release builds the fixture places CODEX_HOME under the child TMPDIR, which arg0/src/lib.rs:344-356 explicitly refuses, making its arg0 check vacuous there. Hosted debug mutants do kill real leaks; this finding concerns the untested oracle fail-open states, not a claim that those observed kills were false.",
      "reproductions": [
        {
          "test_file": "codex-rs/exec/tests/suite/tmpdir_cleanup.rs (requested leak_scan_rejects_unreadable_root oracle attack)",
          "command": "INSTA_WORKSPACE_ROOT=\"$PWD\" just test -p codex-exec -E 'test(leak_scan_rejects_unreadable_root)'",
          "expected_failure": "After adding the test, place a regular file at an expected scan-directory path; require a scan failure instead of an empty result. Current helper maps ENOTDIR to empty. Add partial-read fault coverage where the harness supports it. Not executed here.",
          "pinned_blobs": [
            "e5b504a6db93a1a72cb79cbac37030ad13a26db1:codex-rs/exec/tests/suite/tmpdir_cleanup.rs (requested leak_scan_rejects_unreadable_root oracle attack)"
          ]
        },
        {
          "test_file": "codex-rs/exec/tests/suite/tmpdir_cleanup.rs (requested arg0_setup_is_exercised assertion)",
          "command": "INSTA_WORKSPACE_ROOT=\"$PWD\" just test -p codex-exec --release -E 'test(tmpdir_cleanup)'",
          "expected_failure": "With an assertion that the child created the arg0 root and no alias-setup warning occurred, current release fixture fails: home is beneath temp_dir so production refuses alias setup. Move home outside the isolated system temp root while retaining the scan and verify setup before claiming arg0 coverage. Requested assertion/release run not executed here.",
          "pinned_blobs": [
            "e5b504a6db93a1a72cb79cbac37030ad13a26db1:codex-rs/exec/tests/suite/tmpdir_cleanup.rs (requested arg0_setup_is_exercised assertion)"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-gjhb8b"
      ]
    },
    {
      "id": "A-F4",
      "row": "signal and abort bound",
      "invariant": "The published signal bound must distinguish verified graceful paths, unverified delivery and unsupported termination paths.",
      "mechanism": "The results resource states Ctrl-C / SIGTERM go through existing turn/interrupt + graceful shutdown, then labels signal delivery unverified. Candidate exec/src/lib.rs:1114-1120 subscribes only to tokio::signal::ctrl_c. Its InProcessAppServerClient::start calls app-server in_process::start (app-server-client/src/lib.rs:355-359), whose runtime installs no SIGTERM subscription; the SIGTERM handler in app-server/src/lib.rs belongs to the separate transport-server runner. Thus the positive SIGTERM graceful-routing claim is unsupported by this exec path. SIGKILL/abort limitation is accurately stated. Correction can be a truthful SIGTERM bound; implementing a new signal mechanism is not required by AC2 if it is explicitly bounded.",
      "reproductions": [
        {
          "test_file": "TASK-261007-3v81ko_results.md (signal-bound claim) and codex-rs/exec/tests/suite/tmpdir_cleanup.rs (optional requested signal test)",
          "command": "INSTA_WORKSPACE_ROOT=\"$PWD\" just test -p codex-exec -E 'test(exec_sigterm_cleanup)'",
          "expected_failure": "If coverage is claimed, add the named Unix public-entry test: wait for a verified live arg0 directory during a deliberately blocked turn, deliver SIGTERM, wait for process termination, and require cleanup. Static call-chain predicts termination without the exec Ctrl-C interrupt path. Runtime outcome remains unverified here. Alternatively correct the results to say SIGTERM cleanup is unsupported/unverified without asserting graceful routing.",
          "pinned_blobs": [
            "e5b504a6db93a1a72cb79cbac37030ad13a26db1:TASK-261007-3v81ko_results.md (signal-bound claim) and codex-rs/exec/tests/suite/tmpdir_cleanup.rs (optional requested signal test)"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-gjhb8b"
      ]
    },
    {
      "id": "F1-clap-parser-exit-skips-arg0-guard",
      "row": "tmpdir cleanup on every exit",
      "invariant": "every TempDir created on the codex exec path is dropped or removed on success, error and empty-stdin exits",
      "mechanism": "codex-rs/exec/src/main.rs runs TopCli::parse() (clap derive) inside main_fn, which executes AFTER arg0_dispatch() creates the Arg0PathEntryGuard TempDir (codex-rs/arg0/src/lib.rs: run_main_with_arg0_guard holds the guard across the whole main_fn future). clap parse() calls process::exit on CLI parse errors (code 2) and on --help/--version (code 0), so those CLI-parser exits terminate the process with the guard alive and leak one codex-arg0* dir per invocation under CODEX_HOME/tmp/arg0. Pre-existing: main.rs is untouched by this CR. Blast radius is narrow (CLI-parser exits only, not session exits) and startup janitor_cleanup removes the stale dir on the next run. Fixing it here would mean restructuring the shared arg0 dispatch used by every binary or changing clap exit code 2, both out of proportion for this CR.",
      "reproductions": [
        {
          "test_file": "codex-rs/exec/tests/suite/tmpdir_cleanup.rs (wanted test: exec_help_leaves_no_arg0_dirs)",
          "command": "run codex-exec --help with isolated CODEX_HOME and TMPDIR (same IsolatedExec harness), then assert leaked_arg0_dirs(home) is empty",
          "expected_failure": "wanted test fails: one leaked codex-arg0* dir present after --help exits 0; same shape for an invalid flag exiting 2",
          "pinned_blobs": [
            "e5b504a6db93a1a72cb79cbac37030ad13a26db1:codex-rs/exec/tests/suite/tmpdir_cleanup.rs (wanted test: exec_help_leaves_no_arg0_dirs)"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261010-183rfs"
      ]
    }
  ],
  "notes": [
    "[TASK-261010-gjhb8b] No accept_cr, reject_cr, withdraw_cr, set_status, handoff, resource mutation or notes write was performed on TASK-261007-3v81ko. This is the non-recording panel; all outcome/lifecycle writes target TASK-261010-gjhb8b.",
    "[TASK-261010-gjhb8b] All finding reproduction commands are REQUESTED future attacks, not commands executed in this panel. Proposed test names must be added before running their filters; current tests without the requested assertions do not demonstrate those failures. Local cargo/just/build/runtime test execution count is zero.",
    "[TASK-261010-gjhb8b] Surface sweep 5/5, exactly one result per row; static mechanisms verified 6/6. No claim of exhaustive transitive TempDir inventory or dynamic path coverage.",
    "[TASK-261010-gjhb8b] Hosted snapshot tree is 73c75aedfa7434b0d04cd54c83b062532d9d24dd at bd805b90, not the replay tree. No exact-e5b504a6 execution is attached. Operator resource leak-handoff-note-2 authorizes green-equivalent reuse; independently verified all codex-rs and .github/actions bytes match and total delta equals exactly trunk 39c264c..07c018be. Hosted conclusions are evidence about those identical code/test inputs, not an invented exact-tree run.",
    "[TASK-261010-gjhb8b] Run 38009138137 aggregate conclusion is failure, EXPECTED because mutant-1 small and mutant-2 small each exit 100. Snapshot lint/small/core/app-server jobs are success. The CR validation log is 466 bytes and records mini-hosted-gate exit 0 with required=1 green=1 and test_case_coverage=unknown; it is not a local full-suite log.",
    "[TASK-261010-gjhb8b] Producer reports original .tmp* success/error leak was not reproduced. Hosted failures show CODEX_HOME/tmp/arg0/codex-arg0* leaks, not .tmp* leaks. AC1 original eight-directory symptom and repeated N-run workload remain unknown; the tests make one invocation per isolated fixture (three cases total). Do not claim the incident root cause or original symptom is fixed from this proxy.",
    "[TASK-261010-gjhb8b] AC assessment: AC1 only narrower three-fixture no-leak observations available; AC2 success/server-error/empty-stdin supported but parser gap and signal-bound correction needed; AC3 two named site mutants killed; AC4 held statically; AC5 snapshot four lanes green under explicit green-equivalent authorization, aggregate expected-red, no exact candidate-tree run.",
    "[TASK-261010-183rfs] N1 stderr rendering under anyhow main: the 13 converted paths now surface as 'Error: <original message>' (anyhow Debug via fn main() -> anyhow::Result<()>) instead of the bare eprintln line, and the error_seen path gains one stderr line where the old code exited silently. Exit codes are exact (1) and original messages are preserved as substrings; pre-existing code/substring assertions (prompt_stdin, server_error_exit, mcp_required_exit, output_schema) all pass on hosted run 38009138137. Standard codebase rendering, disclosed via substring assertions; no action.",
    "[TASK-261010-183rfs] N2 non-reproduction bound accepted: results state twice that the issue's 8-per-run success-path .tmp* leak was not reproduced with 0.159.0 in the producer environment (0 .tmp* on success and error, mock and real API). The success-path .tmp* mechanism is therefore still unidentified, and the hosted .tmp* assertions guard the invariant rather than proving an 8-to-0 transition. The CR's demonstrated fix is the error-path arg0 leak (verified pre-fix behavior: failed runs leaked one codex-arg0* dir). This residual unknown is about the original issue's environment, not a defect in the CR, which strictly reduces leak surface (13 destructor-skipping exits removed, zero added) on every converted path.",
    "[TASK-261010-183rfs] N3 mutant lane filter: hosted precheck ran mutants with test filter 'test(tmpdir_cleanup) | test(tmpdir)', so the claim that pre-existing exit-code tests still pass on the mutants is by-construction (mutants restore the exact pre-fix snippets those tests passed on) rather than executed. Airtight for process::exit(1) restorations; no action.",
    "[TASK-261010-183rfs] N4 remaining process::exit audit: every other production process::exit in codex-rs belongs to a different binary (cli/login/doctor/app-server/bwrap/apply-patch standalone) or to arg0 helper-process dispatch branches that run before any TempDir guard exists. None is reachable in-process from codex-exec run_main except the clap parser exits in F1.",
    "[TASK-261010-183rfs] N5 resolve_prompt unreachable! verified safe: read_prompt_from_stdin returns Ok(None) only for StdinPromptBehavior::OptionalAppend; the RequiredIfPiped/Forced arms used by resolve_prompt bail on every empty path, so the else-unreachable arm is genuinely unreachable."
  ],
  "surface_results": [
    {
      "row": "tmpdir cleanup on every exit",
      "result": "broken",
      "reason": "A-F1: both parser entry points still bypass the guard; the three hosted cases establish a narrower bound, not every exit. Original eight .tmp* dirs per successful run remain unreproduced.",
      "reported_by": "TASK-261010-gjhb8b"
    },
    {
      "row": "exit status and observable behavior",
      "result": "broken",
      "reason": "A-F2: error propagation preserves tested status 1 but changes stderr and adds a terminal diagnostic; static source plus documented Termination/anyhow behavior.",
      "reported_by": "TASK-261010-gjhb8b"
    },
    {
      "row": "signal and abort bound",
      "result": "broken",
      "reason": "A-F4: SIGKILL/abort and unverified delivery are stated, but SIGTERM graceful routing is positively claimed without a handler on the exec path.",
      "reported_by": "TASK-261010-gjhb8b"
    },
    {
      "row": "persistent state unchanged",
      "result": "held",
      "reason": "Static diff attack: only error-return mechanics and tests change. No CODEX_HOME/sqlite/rollout allocation or deletion path changes. arg0 guard already owns only CODEX_HOME/tmp/arg0/codex-arg0*, not persistent state. Held for location/deletion invariance, not bit-identical incidental flushing at process exit.",
      "reported_by": "TASK-261010-gjhb8b"
    },
    {
      "row": "regression test and mutants",
      "result": "broken",
      "reason": "Hosted evidence establishes 2/2 one-site mutants killed specifically by real arg0 leak assertions; A-F3 nevertheless exposes fail-open scan results and unverified setup/release coverage in the newly added oracle. Coverage is 2/13 removed exit sites mutated, 0/2 mutants proving the originally reported .tmp* leak, 0 signal-injection tests.",
      "reported_by": "TASK-261010-gjhb8b"
    }
  ],
  "free_hunt": [
    "[TASK-261010-gjhb8b] {\"budget\": \"One bounded pass over public dispatchers/arg0 lifetime, changed Result propagation and the in-process signal call chain after sweeping five rows; stop after source verification and hosted-log cross-checks. No builds or edits to product code.\", \"attacks\": [{\"surface\": \"Public parser exit before run_main\", \"result\": \"broken\", \"finding\": \"A-F1\", \"evidence\": \"exec/src/main.rs:30; cli/src/main.rs:1033; arg0/src/lib.rs:232,276-280; Clap 4.5.58 Parser docs\"}, {\"surface\": \"Release test fixture prevents alias setup\", \"result\": \"broken\", \"finding\": \"A-F3\", \"evidence\": \"tmpdir_cleanup.rs:51-54,75-77; arg0/src/lib.rs:344-356\"}, {\"surface\": \"False transfer of transport-server SIGTERM support into embedded exec runtime\", \"result\": \"broken\", \"finding\": \"A-F4\", \"evidence\": \"exec/src/lib.rs:974,1116; app-server-client/src/lib.rs:355-359; app-server/src/in_process.rs event loops; separate app-server/src/lib.rs:216-227\"}], \"remaining_bounds\": [\"Original host-reported .tmp* allocation source not identified; no root-cause proof.\", \"Only Linux hosted debug entry-point evidence inspected; macOS/Windows execution unknown.\", \"No fault-injected directory enumeration or OS-signal injection was executed.\", \"No claim of comprehensive coverage for all thirteen return conversions, remote execution, resume/fork or detached-task TempDir ownership.\"]}",
    "[TASK-261010-183rfs] {\"area\": \"CLI-parser exits (TopCli::parse in exec/src/main.rs)\", \"outcome\": \"finding F1 (robustness): --help/--version/bad-flag exits skip the arg0 guard drop; pre-existing, narrow, janitor-healed; wanted test named, not run (no builds per brief)\"}",
    "[TASK-261010-183rfs] {\"area\": \"success-path .tmp* root cause from the issue report\", \"outcome\": \"no finding in the CR: mechanism unidentified and unreproduced in the producer environment (stated bound, accepted as note N2); CR removes the proven error-path mechanism and guards the .tmp* invariant on all three exit classes\"}",
    "[TASK-261010-183rfs] {\"area\": \"TempDir owned by detached task or static; keep/forget/persist primitives\", \"outcome\": \"no finding: no such site on the codex-exec path; only production TempDir is the arg0 guard with verified drop ordering\"}",
    "[TASK-261010-183rfs] {\"area\": \"early return paths without a dedicated test (config/schema/login/git-check sites)\", \"outcome\": \"no finding: all 13 sites share the single verified mechanism (Err return -> guard drop in run_main_with_arg0_guard); tested at both ends (pre-network stdin error, post-session error_seen) plus mutants; per-site tests would add no signal\"}",
    "[TASK-261010-183rfs] {\"area\": \"load_output_schema None-path and resolve_* refactors\", \"outcome\": \"no finding: None -> Ok(None) preserved; unreachable! arm verified genuinely unreachable (note N5)\"}",
    "[TASK-261010-183rfs] {\"area\": \"buffered-output flush and hang regressions\", \"outcome\": \"no finding: new paths run strictly more destructors (superset flush); no new await points introduced\"}"
  ]
}
```
