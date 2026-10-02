# Producer brief — goal token-burn series (applies to every code leaf)

## Where you work
- Your cwd is a task-board Story worktree of `relux-works/codex`, forked from `relux/main`
  (a pinned upstream `openai/codex` commit). Write only inside this worktree.
- Do NOT commit, push, rebase, merge, switch branches or open PRs. The orchestrator lands accepted work.
- The accepted plan is `final-plan.md` (precondition resource). Its `path:line` citations refer to upstream
  `33a0f766a6`; your base is newer. Re-locate every cited symbol in your worktree before editing, and check
  `git log 33a0f766a6..HEAD -- <files you touch>` for upstream changes since the plan was written.

## Repository rules
- This is an upstream repository destined for discrete PRs: do NOT edit `README.md`, `docs/`, CI files or anything
  outside your leaf scope, even if your own global instructions ask you to maintain a README tools section.
- Follow `AGENTS.md` at the repo root (codex-rs section): inline `format!` args, collapsible `if`, method
  references over closures, no bool/ambiguous `Option` positional params (or `/*param*/` comments), exhaustive
  `match`, new test modules in sibling `*_tests.rs` files via `#[path = ...]`, `pretty_assertions::assert_eq`,
  whole-object comparisons, no tests for statically defined values, integration tests under `core/tests/suite`
  with `test_codex` / `core_test_support::responses` for agent-visible behaviour.
- Resist adding code to `codex-core`; keep new modules small (< 500 LoC).
- Do not touch `Cargo.lock`, `MODULE.bazel.lock` or generated schema files unless the leaf truly needs a new
  dependency or schema change; if so run `just bazel-lock-update` / `just write-config-schema` and say why.

## Build and test on this shared machine (mandatory)
- FIRST, before any cargo/just build or test in your worktree, run
  `/Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-target-guard.sh` (from your worktree). The cargo target
  is shared by several checkouts; cargo can silently reuse another checkout's artifacts for the same package, which
  produces phantom compile errors and false test results. The guard cleans workspace-member artifacts when the
  building checkout changed (external dependencies stay cached). Re-run it if you suspect stale artifacts.
- Build settings come from `/Users/iv/Developer/IV/codex/.temp/.cargo/config.toml`, which cargo reads automatically
  for every Story worktree under `.temp/`: shared target dir, `jobs = 4`, `incremental = false`, and the rusty_v8
  archive/binding paths. Do NOT set `CARGO_TARGET_DIR`, `CARGO_BUILD_JOBS`, `CARGO_INCREMENTAL` or `RUSTY_V8_*`
  yourself (an inline copy of these was once swallowed into CARGO_TARGET_DIR and wrote an 18 GB stray target).
- For tests, export only these, from `codex-rs/` of YOUR worktree:
  ```sh
  export NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no INSTA_WORKSPACE_ROOT="$PWD"
  ```
  `INSTA_UPDATE=no` stops insta from writing `*.snap.new` files into the worktree; accept intentional snapshot
  changes explicitly (`INSTA_UPDATE=always` scoped to the affected tests, or `cargo insta accept -p <crate>`).
  `INSTA_WORKSPACE_ROOT` must point at your worktree's `codex-rs`, otherwise insta may resolve the control root.
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

## Parallel stories: hold your handoff while another codex-fix suite runs (ruling tb-R58)
Only one codex-fix Change Request suite may run at a time. Right before `task-board handoff`, run once:
`python3 /Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-fix-suite-busy.py`
- `FREE` -> hand off as usual.
- `BUSY ...` -> do NOT hand off and do NOT poll or wait. Attach your `<TASK-ID>_results.md`, add a task note
  `HOLD: codex-fix suite busy (<runs>) — ready for handoff`, and end your turn. The orchestrator republishes
  your work when the running suite ends; nothing you wrote is lost.
