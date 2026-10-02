# TASK-261002-1ugz6h — rework for CR revision 2 (apply the reviewed fixes; one file)

Round 1 (merged R141 verdict `TASK-261002-1ugz6h_review-verdict-rev1.md`, changes_requested) found:
- F1 (robustness): the lint lane did not fail on plain clippy/rustc warnings.
- F2 (robustness): `inputs.sha` was free text; nothing proved the job tested exactly that commit.
- push-concurrency-cross-sha (regression): push runs were grouped by ref, so a later push cancelled an earlier SHA's run.

The orchestrator prepared the fixed file as signed commit ea8899e6f97aea64136159286840c28c955243e8 (branch relux/hosted-ci,
parent fc22281 = your Story checkpoint's tree). Its `.github/workflows/relux-ci.yml` fixes them as follows.
- F2: a "Verify the checked-out commit" step right after checkout requires a full 40-hex SHA (passed through env, never
  interpolated into the script) and `git rev-parse HEAD` equal to it.
- concurrency: the group is `relux-ci-${{ inputs.sha || github.sha }}`, one group per exact commit for dispatch and push alike.
- F1: the lint lane fails on any clippy or rustc warning except the 3 upstream-baseline warnings listed inline. All 3 exist
  at the fork's upstream pin and come from no series commit:
  - core/src/tools/registry.rs, unused ToolCallSource import;
  - core/tests/suite/openai_file_mcp.rs, unused body_json import;
  - core/tests/suite/scenarios.rs, unused ReasoningEffort import.
  A plain `-- -D warnings` failed on the first (hosted run 36969374494). Clippy runs with `--color never`, ANSI codes are
  stripped before parsing, and the step prints a count line. An earlier draft (commit c1ace00) silently matched nothing
  because of colored output; that is fixed here.

Your job:
1. In the Story worktree run `git fetch origin relux/hosted-ci`, then
   `git checkout ea8899e6f97aea64136159286840c28c955243e8 -- .github/workflows/relux-ci.yml`, then `git reset -q`.
   Leave the file UNCOMMITTED, check that `git status --short` shows only that file, and that its blob equals
   `git rev-parse ea8899e6f9:.github/workflows/relux-ci.yml`.
2. Map each round-1 finding to the exact lines that fix it, in `TASK-261002-1ugz6h_results.md` (refresh it and note rev 2).
   Run the YAML parse check, and `actionlint` if it is installed.
3. Record the hosted selftest of this exact tree, run 36974560859 (push of ea8899e to ci/relux-ci-selftest/stack-5):
   each lane's conclusion and wall time, plus the lint step's count line ("clippy warnings: N distinct, 3 of them upstream
   baseline"). Then record the negative control, run 36974565033: commit 694b0ed = ea8899e plus one unused import in
   codex-tools, pushed to ci/relux-ci-selftest/neg-1. Its lint lane must FAIL with "clippy warnings outside the upstream
   baseline" naming tools/src/lib.rs; its other lanes were cancelled on purpose.
4. Busy check, guard, `just fmt-check`, then `task-board handoff TASK-261002-1ugz6h --role developer`.
