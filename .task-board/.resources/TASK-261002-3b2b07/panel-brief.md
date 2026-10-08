# R141 panel DELTA TASK-260929-2gp04j rev2 — non-recording review panel (tb-R141; same-provider review, operator rule tb-R147)

You review Change Request `CR-TASK-260929-2gp04j-2` revision 2 of `TASK-260929-2gp04j` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-2gp04j`, and do not
write anything on `TASK-260929-2gp04j`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

This is the DELTA panel (round 2+). Check, in order: (1) every finding of the previous round's merged verdict (`TASK-260929-2gp04j_review-verdict-rev<prev>.md` on TASK-260929-2gp04j) is fixed correctly; (2) whether the same class of problem appears anywhere else in the code; (3) whether the rework broke anything.

## Inputs (read-only, all on `TASK-260929-2gp04j`)
- Patch: resource `TASK-260929-2gp04j_change-request_rev2.patch`. Base commit `ea8899e6f97aea64136159286840c28c955243e8`. Expected candidate tree `d401bcff58f9724a36966053dde5386be1af7882`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-2gp04j) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261002-3b2b07-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree ea8899e6f97aea64136159286840c28c955243e8
task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev2.patch --output .temp/TASK-260929-2gp04j_change-request_rev2.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev2.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print d401bcff58f9724a36966053dde5386be1af7882
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show d401bcff58f9724a36966053dde5386be1af7882:<path>`, or `git archive d401bcff58f9724a36966053dde5386be1af7882 <paths> | tar -x -C .temp/TASK-261002-3b2b07-cand`.

## Review
Follow the reviewer role contract's review-round rules: attack, don't just read; every surface-table row gets
exactly one result (held / broken / not-attacked with a reason); then a bounded free hunt. Do NOT run cargo, just or
any build or test: the shared build target is serialized (one codex-fix build at a time). Execution evidence is the
element's CR validation log (local fast lane) and the hosted relux-ci result when attached. Your review is the replay
plus a static attack.

## Deliverable
Attach the outcome `TASK-261002-3b2b07_panel-verdict.md` to YOUR task `TASK-261002-3b2b07`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Then run
`task-board handoff TASK-261002-3b2b07 --role researcher`.

## Orchestrator note for this CR
Round 2 of the story-final CR of STORY-260929-bohnqb (P2). Round-1 merged verdict: TASK-260929-2gp04j_review-verdict-rev1.md (one finding: a goal-store read failure on the progress-accounting / turn-stop / abort paths left a stale GoalActivity marker). Leaf 1 (G1) is checkpointed at 58042581; verify G1 paths are unchanged versus it and focus on G2. The candidate tree d401bcff is byte-identical to the hosted precheck-3 snapshot, so TASK-260929-2gp04j_hosted-precheck-3.md is exact-candidate evidence: run 37014493254 green on all lanes and 15/15 narrowing mutants killed by their intended tests, including turn_stop_read_failure_keeps_marker and abort_read_failure_keeps_marker for the round-1 finding. Non-blocking context already noted in round 1: size ~1400 lines (upstream PR will be staged), test-only dev-dependency cycle, bazel lock refreshed without delta.
