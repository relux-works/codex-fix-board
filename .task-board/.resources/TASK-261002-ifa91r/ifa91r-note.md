# TASK-261002-ifa91r — apply the P1 astra snapshot refresh (mechanical, no other change)

The orchestrator already prepared the exact change as signed commit
fc22281fe0ec781670b8520ffe2761673515cad0, branch relux/p1-astra-snapshots in relux-works/codex. Its parent is your
trunk, relux/main 35af013. It updates 12 hash lines in two snapshot files and nothing else:
- codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_kickoff_remote_compaction_windows.snap
- codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_plugin_refresh.snap

Why: P1 (35af013) changed the clock and collaboration tool-schema fingerprints, but these two snapshots were in the
local quarantine (a host global-skills leak), so they went stale. GitHub-hosted CI runs 36959471910 and 36959934198
fail both tests 3/3 with exactly these 6 hash lines per file (insta diff in the core job log).

Your job:
1. In your Story worktree run `git fetch origin relux/p1-astra-snapshots`, then
   `git cherry-pick --no-commit fc22281fe0ec781670b8520ffe2761673515cad0`, then `git reset -q` (unstage; leave the
   change UNCOMMITTED). Confirm `git diff --stat` shows exactly those 2 files, 12 insertions and 12 deletions.
2. Check each changed line against the insta diff in the hosted log: run
   `gh run view 36959934198 --repo relux-works/codex --log-failed`, or read the copy at
   `/Users/iv/Developer/IV/codex/.temp/relux-ci/selftest-core-02.log` and search for "Snapshot file:".
3. Run the busy check (`codex-fix-suite-busy.py --any`), the guard, and from `codex-rs/` `just fmt-check`. These
   are snapshot files, so no other local build is needed. Do NOT run codex-core tests locally: the hosted core lane
   runs both astra tests on this exact tree.
4. Attach `TASK-261002-ifa91r_results.md` (diff stat, line check, commands with exit codes), then
   `task-board handoff TASK-261002-ifa91r --role developer`.

## Note (operator, tb-R122 short lane)
Your change is already in the Story worktree from RUN-261002-bf3102. That run handed off and was validation-queued
at shared-queue position 8, then was cancelled only to move its suite into the R122 short lane. Do NOT redo the work.
Verify the candidate is intact: `git diff --stat` shows exactly the 2 snapshot files with 12+/12-, and every line
still matches fc22281. Re-run the busy check, the guard and `just fmt-check`, refresh the results outcome if anything
changed (note this re-handoff), and hand off again.
