# TASK-261007-3v81ko: review rev1 changes_requested. Fix A-F1..A-F4, then request precheck 2

The merged verdict is `TASK-261007-3v81ko_review-verdict-rev1.md` (precondition). Panel A (codex sol high) requested changes;
panel B (muse max) accepted, noting F1 too. Hosted precheck 1 was green and killed both mutants, so the core idea holds:
returning instead of `process::exit` lets the TempDir guards drop. `mini-producer-addendum.md` applies (cargo fmt allowed and
required; no other cargo). Your worktree base is now trunk 07c018be (CI-only commits on ivanopcode/codex); your files are unchanged.

1. A-F2, regression, MUST fix: user-visible stderr must not change. Today, returning `anyhow::Error` from `main` makes Rust's
   `Termination` print `Error: <Debug>`, so `No prompt provided via stdin.` became `Error: No prompt provided via stdin.`,
   config errors gained an `Error: ` prefix, and server failures print an extra `Error: exec turn failed` after
   print_final_output. Keep the exact previous stderr bytes and ordering and the same exit codes, while still letting the
   guards drop. One way: the inner function returns a typed exit outcome (an exit code, plus the message it already
   printed), the outer main prints nothing extra and maps it to `std::process::ExitCode` after all guards are dropped. Add
   tests that compare the FULL stderr (whole-string `assert_eq`, not substring) and the exit status for empty stdin, a config
   error and a server error.
2. A-F1: clap `parse()` exits the process on invalid args and on --help/--version AFTER `arg0_dispatch_or_else` has created the
   `CODEX_HOME/tmp/arg0/codex-arg0*` guard (exec/src/main.rs:30 TopCli::parse; cli/src/main.rs:1033 MultitoolCli::parse). Fix it
   with `try_parse()` and render clap's error yourself with the SAME output and exit code (`err.print()`, then return its
   exit code through the same ExitCode path), so the guard drops. Cover invalid args and --help with a no-leak test that
   also asserts the unchanged output and exit code. If one of these paths stays out of scope, state it as an explicit bound
   with the reason.
3. A-F3, test oracle: `tmpdir_cleanup.rs:10-13` and `:29-33` treat read_dir errors and partial reads as "clean". Make the
   oracle fail closed: a read error panics with a message. Also prove the protected resource EXISTED: the test must observe
   that arg0 setup actually created its guard dir during the run (for example, a temp dir listing taken while the child is
   alive, or a precondition that fails if the arg0 path was refused), so a skipped setup cannot pass vacuously. Fix the
   release-build vacuity: the fixture puts CODEX_HOME under the child's TMPDIR, which arg0/src/lib.rs:344-356 refuses. Use
   separate dirs so the arg0 path is exercised.
4. A-F4: correct the signal bound in the results. Only `tokio::signal::ctrl_c` is subscribed on this exec path
   (exec/src/lib.rs:1114-1120), and the in-process app server installs no SIGTERM handler. So state truthfully: Ctrl-C goes
   through graceful shutdown (say whether a test covers it); SIGTERM and SIGKILL/abort are NOT cleaned up and are a stated
   bound. Do not claim graceful SIGTERM.
5. Mutants: keep the 2 existing mutants and add narrowing mutants for item 1 (re-add the `Error:` prefix on one path) and item 2
   (go back to `parse()` at one dispatcher). Each needs a named killer test. All patches must apply to your final tree.
Run cargo fmt plus `--check` (exit 0), leave everything UNCOMMITTED, report the final tree id, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 2`, and end your turn without handing off. The CI test filter for mutants will be
`test(tmpdir_cleanup) | test(tmpdir) | test(stderr) | test(exit_code)`; tell me if your killer tests need another pattern.
