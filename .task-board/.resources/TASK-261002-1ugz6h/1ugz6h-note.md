# TASK-261002-1ugz6h — add the fork-only relux-ci workflow (one new file)

The orchestrator already prepared the exact file. It is in signed commit
7ae33a059056dad776bd0b81fb2b4883615b9b5a (branch relux/hosted-ci in relux-works/codex, parent fc22281 = the
snapshot fix that is your previous leaf's checkpoint). The only file is `.github/workflows/relux-ci.yml`. It is
fork-only: it never goes upstream. This leaf lands it on relux/main through the normal CR flow.

Your job:
1. In your Story worktree run `git fetch origin relux/hosted-ci`, then
   `git checkout 7ae33a059056dad776bd0b81fb2b4883615b9b5a -- .github/workflows/relux-ci.yml`, then `git reset -q`.
   Leave the file UNCOMMITTED. Confirm `git status --short` shows only that one new file, and that
   `git hash-object .github/workflows/relux-ci.yml` equals `git rev-parse 7ae33a0590:.github/workflows/relux-ci.yml`.
2. Check the workflow statically:
   `python3 -c "import yaml;yaml.safe_load(open('.github/workflows/relux-ci.yml'))"`, and `actionlint` on the file if
   it is installed (say so if it is not).
3. Confirm the hosted selftest of this exact tree: run 36963367409 (push of 7ae33a0 to ci/relux-ci-selftest/stack-2).
   Record each lane's conclusion and wall time from `gh run view 36963367409 --repo relux-works/codex --json jobs`.
   If it is still running, record that and wait for it to finish; never claim a result you have not seen.
4. Run the busy check (`codex-fix-suite-busy.py --any`), the guard and `just fmt-check` (from `codex-rs/`).
5. Attach `TASK-261002-1ugz6h_results.md`, then `task-board handoff TASK-261002-1ugz6h --role developer`.
