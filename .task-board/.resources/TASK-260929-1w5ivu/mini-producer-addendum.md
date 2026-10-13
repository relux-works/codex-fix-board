# Mac mini addendum for codex-fix producers (overrides producer-brief.md wherever they conflict)

The campaign runs on the Mac mini. This host differs from the ivmbp briefs:

1. No local Rust builds, checks, clippy or tests (R194, R223). Building and executing fresh binaries here crashes syspolicyd.
   A mechanical guard refuses `cargo build/check/clippy/test/nextest`; do not try them and never try to bypass it.
   IGNORE every local build or test step in producer-brief.md: codex-target-guard.sh, codex-fix-suite-busy.py,
   `just fix/clippy/test`, `cargo nextest`, and the busy check. All of that runs on hosted relux-ci.
2. rustfmt IS allowed and REQUIRED. From `codex-rs/`: `cargo fmt -- --config imports_granularity=Item`, then
   `cargo fmt -- --config imports_granularity=Item --check`, which must exit 0. Report that exit code in your results.
   It builds nothing. The nightly-only warning about imports_granularity is expected.
3. Because nothing compiles locally, be rigorous by reading: check types, imports, visibility, trait bounds and call
   sites by hand, and re-read for clippy issues (redundant closures, uninlined format args, collapsible ifs, needless
   borrows). Write the integration tests the AC requires anyway, and list in your results which tests only hosted CI will run.
4. Mutants: attach `<TASK-ID>_mutants.json` as a list of `{"name", "patch"}`. Each patch is a unified diff against your
   FINAL worktree, `git apply --check`-clean, and narrows exactly one gate. Name its killer test in your results.
5. Do not commit. Leave the candidate UNCOMMITTED, report the tree id computed AFTER your last edit (temp index:
   `git read-tree HEAD`, `git add -A`, `git write-tree`), add the note `HOSTED-PRECHECK-REQUESTED: precheck 1`, and end
   your turn without handing off.
6. Evidence is plain text only (R176). Paths: use `/Users/administrator/Developer/ReluxWorks/codex/...`, never `/Users/iv/...`.
7. Never copy a real CODEX_HOME (~/.codex: sessions, auth, sqlite) into a repro or test dir, and never run the installed `codex`
   binary for reproductions on this host. If you create any temporary directory yourself, delete it before you end your turn
   and say so in your results. (2026-10-09: a producer's repro left 16 GiB in $TMPDIR.)
