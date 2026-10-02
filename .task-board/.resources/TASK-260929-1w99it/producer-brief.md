# Producer brief — goal token-burn series (applies to every code leaf)

## Where you work
- Your cwd is a task-board Story worktree of `relux-works/codex`, forked from `relux/main`
  (a pinned upstream `openai/codex` commit). Write only inside this worktree.
- Do NOT commit, push, rebase, merge, switch branches or open PRs. The orchestrator lands accepted work.
- The accepted plan is `final-plan.md` (precondition resource). Its `path:line` citations refer to upstream
  `33a0f766a6`; your base is newer. Re-locate every cited symbol in your worktree before editing, and check
  `git log 33a0f766a6..HEAD -- <files you touch>` for upstream changes since the plan was written.

## Repository rules
- Follow `AGENTS.md` at the repo root (codex-rs section): inline `format!` args, collapsible `if`, method
  references over closures, no bool/ambiguous `Option` positional params (or `/*param*/` comments), exhaustive
  `match`, new test modules in sibling `*_tests.rs` files via `#[path = ...]`, `pretty_assertions::assert_eq`,
  whole-object comparisons, no tests for statically defined values, integration tests under `core/tests/suite`
  with `test_codex` / `core_test_support::responses` for agent-visible behaviour.
- Resist adding code to `codex-core`; keep new modules small (< 500 LoC).
- Do not touch `Cargo.lock`, `MODULE.bazel.lock` or generated schema files unless the leaf truly needs a new
  dependency or schema change; if so run `just bazel-lock-update` / `just write-config-schema` and say why.

## Build and test on this shared machine (mandatory)
- Always export this environment for every cargo/just command (copy it verbatim):
  ```sh
  export CARGO_TARGET_DIR=/Users/iv/Developer/IV/codex-target CARGO_BUILD_JOBS=4 CARGO_INCREMENTAL=0 \
    RUSTY_V8_ARCHIVE=/Users/iv/Developer/IV/codex-cache/rusty_v8/librusty_v8_ptrcomp_sandbox_release_aarch64-apple-darwin.a.gz \
    RUSTY_V8_SRC_BINDING_PATH=/Users/iv/Developer/IV/codex-cache/rusty_v8/src_binding_ptrcomp_sandbox_release_aarch64-apple-darwin.rs \
    NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no
  ```
  Never set a private target dir, never use `--all-features`, never enable incremental builds (disk is tight).
  `INSTA_UPDATE=no` stops insta from writing `*.snap.new` files into the worktree (they would pollute the
  Change Request); accept intentional snapshot changes explicitly with `cargo insta accept -p <crate>` only
  when the leaf changes a snapshot on purpose.
- `codex-core` and `codex-app-server` integration tests spawn helper binaries from other packages. Build them
  once before running those tests (from `codex-rs/`):
  `cargo build -p codex-rmcp-client --bin test_stdio_server --bin test_streamable_http_server -p codex-shell-escalation --bin codex-execve-wrapper -p codex-app-server --bin codex-app-server --bin codex-app-server-test-notify-capture --bin exec-server -p codex-code-mode-host --bin codex-code-mode-host -p codex-cli --bin codex -p codex-exec --bin codex-exec`
  Missing-binary failures (`could not locate binary`, `failed to spawn code-mode host`) mean this step was
  skipped; they are environmental, never a reason to change product code.
- Run from `codex-rs/`: `just test -p <crate>` (nextest; filters like `-E 'test(name)'` pass through),
  `just fmt` after edits, `just fix -p <crate>` before handoff. Never run the full `just test`.
- One heavy build/test at a time; do not leave background builds running. A build may wait on the shared cargo
  lock while another build finishes; that is expected.
- Run each gate command directly (no `tee`, no pipes that hide the exit code) and report real exit codes.

## Handoff
- Attach a task-scoped outcome `<TASK-ID>_results.md`: summary, changed files, every AC row mapped to its
  driving test and refusal test (coverage map), exact commands with exit codes, and anything unverified.
- Then run `task-board handoff <TASK-ID> --role developer`. The board's landing-gate suite (fmt-check, clippy,
  scoped crate tests) runs automatically at Change Request publication and takes a while.
