# R141 panel B TASK-261002-ifa91r rev1 — non-recording review panel (tb-R141; models per R80/R132, tb-R146)

You review Change Request `CR-TASK-261002-ifa91r-1` revision 1 of `TASK-261002-ifa91r` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-261002-ifa91r`, and do not
write anything on `TASK-261002-ifa91r`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-261002-ifa91r`)
- Patch: resource `TASK-261002-ifa91r_change-request_rev1.patch`. Base commit `35af013b901ed4be1b88416068f140e9ca5cc85d`. Expected candidate tree `5c365d9a68ea6d2cee0488eb58a37a539ce354d4`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-261002-ifa91r) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261002-3ksr2m-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 35af013b901ed4be1b88416068f140e9ca5cc85d
task-board resource get TASK-261002-ifa91r TASK-261002-ifa91r_change-request_rev1.patch --output .temp/TASK-261002-ifa91r_change-request_rev1.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-261002-ifa91r_change-request_rev1.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print 5c365d9a68ea6d2cee0488eb58a37a539ce354d4
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:<path>`, or `git archive 5c365d9a68ea6d2cee0488eb58a37a539ce354d4 <paths> | tar -x -C .temp/TASK-261002-3ksr2m-cand`.

## Review
Follow the reviewer role contract's review-round rules: attack, don't just read; every surface-table row gets
exactly one result (held / broken / not-attacked with a reason); then a bounded free hunt. Do NOT run cargo, just or
any build or test: the shared build target is serialized (one codex-fix build at a time). Execution evidence is the
element's CR validation log (local fast lane) and the hosted relux-ci result when attached. Your review is the replay
plus a static attack.

## Deliverable
Attach the outcome `TASK-261002-3ksr2m_panel-verdict.md` to YOUR task `TASK-261002-3ksr2m`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Then run
`task-board handoff TASK-261002-3ksr2m --role researcher`.
