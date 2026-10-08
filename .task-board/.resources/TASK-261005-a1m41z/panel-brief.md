# R141 panel A TASK-260929-1rcgsj rev1 — non-recording review panel (tb-R141; same-provider review, operator rule tb-R147)

You review Change Request `CR-TASK-260929-1rcgsj-1` revision 1 of `TASK-260929-1rcgsj` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-1rcgsj`, and do not
write anything on `TASK-260929-1rcgsj`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-260929-1rcgsj`)
- Patch: resource `TASK-260929-1rcgsj_change-request_rev1.patch`. Base commit `47f7a80476eb78f27f7ce97c8bf7eb9236c40b47`. Expected candidate tree `37fad741767c46d11094adb9be747d5aae83c145`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-1rcgsj) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261005-a1m41z-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47
task-board resource get TASK-260929-1rcgsj TASK-260929-1rcgsj_change-request_rev1.patch --output .temp/TASK-260929-1rcgsj_change-request_rev1.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-1rcgsj_change-request_rev1.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print 37fad741767c46d11094adb9be747d5aae83c145
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show 37fad741767c46d11094adb9be747d5aae83c145:<path>`, or `git archive 37fad741767c46d11094adb9be747d5aae83c145 <paths> | tar -x -C .temp/TASK-261005-a1m41z-cand`.

## Review
Follow the reviewer role contract's review-round rules: attack, don't just read; every surface-table row gets
exactly one result (held / broken / not-attacked with a reason); then a bounded free hunt. Do NOT run cargo, just or
any build or test: the shared build target is serialized (one codex-fix build at a time). Execution evidence is the
element's CR validation log (local fast lane) and the hosted relux-ci results when attached. Hosted runs on the EXACT
candidate tree (snapshot plus narrowing-mutant runs) ARE executed public-entry attacks for this review: cite them to
mark a row held or broken. If you need an attack that was not run, name the test or mutant you want; do not mark a row
not-attacked only because local builds are forbidden. The local validation log is truncated by task-board (64 KiB cap,
BUG-260917-38ob0v); the hosted lint and small lanes run the same commands on the same tree. Your review is the replay
plus a static attack.

## Deliverable
Attach the outcome `TASK-261005-a1m41z_panel-verdict.md` to YOUR task `TASK-261005-a1m41z`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Attach only that text file:
no archives or binary files (tb-R176). Do not stop at the first finding; sweep every surface row (tb-R170). Then run
`task-board handoff TASK-261005-a1m41z --role researcher`.
