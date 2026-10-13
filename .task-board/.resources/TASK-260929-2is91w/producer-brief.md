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
- Local validation is the FAST lane only (from `codex-rs/`): `just fmt` after edits, `just fix -p <crate>` and
  `just clippy -p <crate>` for every crate you touched (clippy runs with `--tests`, so it type-checks new test code
  in `codex-core` / `codex-app-server` without linking test binaries), and `just test -p <crate>` for the small
  crates only: `codex-tools`, `codex-goal-extension`, `codex-extension-api`, `codex-rollout-trace`.
- Do NOT run `just test -p codex-core` or `just test -p codex-app-server` locally, and do not build the integration
  helper binaries. Those suites run on GitHub-hosted CI (`relux-ci`, lanes lint / small / core / app-server)
  against the exact Change Request candidate tree after you hand off; the orchestrator routes any real failure back
  to you with the CI job log as a rework. Write the integration tests the AC requires anyway, make them compile
  (clippy), and state in your results which tests only hosted CI has run.
- Never run the full `just test`. Do not leave background builds running. A build may wait on the shared cargo
  lock while another build finishes; that is expected.
- Run each gate command directly (no `tee`, no pipes that hide the exit code) and report real exit codes.

## Handoff
- Attach a task-scoped outcome `<TASK-ID>_results.md`: summary, changed files, every AC row mapped to its
  driving test and refusal test (coverage map), exact commands with exit codes, and anything unverified.
- Then run `task-board handoff <TASK-ID> --role developer`. The board's local landing gate (target guard,
  fmt-check, clippy, small-crate tests) runs automatically at Change Request publication; hosted CI then runs the
  heavy codex-core / codex-app-server suites on the exact candidate tree.

## One build at a time: pipeline without building (rulings tb-R58, tb-R64, keeper recommendation 2026-10-01)
Only one codex-fix build/suite may use the shared cargo target at a time. Before your FIRST cargo/just command,
and again right before `task-board handoff`, run once:
`python3 /Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-fix-suite-busy.py --any`
- `FREE` -> build/test (guard first) and hand off as usual.
- `BUSY ...` -> do NOT run cargo/just and do NOT poll or wait. You may read code and write your change without
  compiling. When your edits are done, attach `<TASK-ID>_results.md` (what you changed, what still needs a build),
  add a task note `HOLD-BUILD: another codex-fix run is building (<runs>) — code written, not yet built`, and end
  your turn. The orchestrator resumes you for build, test and handoff once the target is free.

## Hosted pre-handoff check (when your checklist needs codex-core/app-server results or mutants)
The board refuses handoff while the checklist items for passing tests and killed mutants are unchecked, and you may not
run codex-core/app-server suites locally. When your AC needs them:
1. Write the code and tests, make the fast-lane checks pass, and attach `<TASK-ID>_mutants.json`: a list of
   `{"name", "patch"}`, where each patch is a unified diff against your worktree that narrows one gate and names the test
   expected to kill it in your results.
2. Add a task note `HOSTED-PRECHECK-REQUESTED: <what to run>` and end your turn WITHOUT handing off. Do not mark
   unexecuted items green.
3. The orchestrator snapshots your exact worktree tree into a signed commit and runs relux-ci on it and on each mutant.
   You are then resumed with `<TASK-ID>_hosted-precheck-<n>.md`, which lists the run ids, test results and killed
   mutants. Check the items citing that evidence, without changing code, and hand off. A code change after the snapshot
   invalidates the evidence and needs a new precheck.

## Evidence format (collective rule tb-R176)
Attach only plain-text evidence to the board: markdown, `.log` and `.json`. Never attach archives or other binary files
(`.zip`, `.tar.gz`, `.gz`, images). If you need an archive, write it under
`/Users/iv/Developer/IV/codex/.temp/evidence-store/<TASK-ID>/` and attach a short text resource with its path, sha256 and
size. Never use the lite context profile (tb-R174).
