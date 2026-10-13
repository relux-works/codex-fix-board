# TASK-260929-csyzcj (G1): Mac mini addendum to g1-rework-brief-precheck2.md (it overrides that brief and producer-brief.md where they conflict)

The campaign moved from ivmbp to the Mac mini on 2026-10-08. This host differs from the briefs written for ivmbp:

## 0. Restore the candidate first
Your Story worktree is new and starts clean at `relux/main` 39c264c34e61b5171ae13b0f756746c24ea5f51a. The precheck-2
candidate survives as the local ref `refs/remotes/origin/ci/TASK-260929-csyzcj/wip-2` (3d1a0573; it is in the shared object
store, so no network is needed). From the worktree root:

```sh
git diff --quiet && git diff 39c264c34e61b5171ae13b0f756746c24ea5f51a refs/remotes/origin/ci/TASK-260929-csyzcj/wip-2 | git apply
git diff --stat | tail -1   # expect: 26 files changed, 1485 insertions(+), 16 deletions(-)
```

The guard `git diff --quiet &&` means the diff is applied only on a clean tree. If the tree is already dirty, the candidate is
already there: check the stat and do not apply twice. Leave everything UNCOMMITTED; never commit, branch, fetch or push.

## 1. No local Rust builds or tests on this host (R194, R223). rustfmt IS available
- Building and executing fresh test binaries here crashes syspolicyd (R194), so builds, clippy and tests run only on hosted relux-ci (R223).
  A mechanical guard enforces this: `cargo build/check/clippy/test` are refused with exit 2. Do not try them, and do not try to bypass the guard.
- ALLOWED, and REQUIRED before you request a precheck: format with rustfmt from `codex-rs/`:
  `cargo fmt -- --config imports_granularity=Item` then `cargo fmt -- --config imports_granularity=Item --check` (it must exit 0).
  It builds nothing and creates no target dir. The warning that imports_granularity is nightly-only is expected; ignore it.
  Report the `--check` exit code in your results.
- IGNORE every other local command in the briefs: codex-target-guard.sh, codex-fix-suite-busy.py, `just fix/clippy/test`, `cargo nextest`, and any
  "LOCAL VERIFICATION" paragraph. Re-read changed code for clippy issues by hand (redundant closures, uninlined format args, collapsible ifs).

## 2. What to deliver (unchanged in substance)
- Fix items 1 and 2 of g1-rework-brief-precheck2.md (the hanging latch test, with bounded latch waits that panic clearly, and
  the surviving mutant `insert_after_mail_check`, which must fail that test by an assertion, not a timeout).
- Update `TASK-260929-csyzcj_mutants.json`: every patch must apply to your FINAL worktree, with correct hunk headers, and
  name its intended killer test. Update `TASK-260929-csyzcj_results.md`: what changed, the AC coverage map, and a list
  of what only hosted CI has verified, which is everything compiled. Re-attach both as outcome resources (`resource update`).
- Add the task note `HOSTED-PRECHECK-REQUESTED: precheck 3` and end your turn. Do NOT hand off.
- Evidence is plain text only (R176). If you ever need an archive store, use
  `/Users/administrator/Developer/ReluxWorks/codex/.temp/evidence-store/TASK-260929-csyzcj/`, not the ivmbp `/Users/iv/...` path.
