# R141 panel A TASK-261007-3v81ko rev1 — non-recording review panel (tb-R141; same-provider review, operator rule tb-R147)

You review Change Request `CR-TASK-261007-3v81ko-1` revision 1 of `TASK-261007-3v81ko` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-261007-3v81ko`, and do not
write anything on `TASK-261007-3v81ko`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-261007-3v81ko`)
- Patch: resource `TASK-261007-3v81ko_change-request_rev1.patch`. Base commit `07c018be3507b8d4a5558a85a117b94ed2a23872`. Expected candidate tree `e5b504a6db93a1a72cb79cbac37030ad13a26db1`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-261007-3v81ko) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261010-gjhb8b-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 07c018be3507b8d4a5558a85a117b94ed2a23872
task-board resource get TASK-261007-3v81ko TASK-261007-3v81ko_change-request_rev1.patch --output .temp/TASK-261007-3v81ko_change-request_rev1.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-261007-3v81ko_change-request_rev1.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print e5b504a6db93a1a72cb79cbac37030ad13a26db1
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show e5b504a6db93a1a72cb79cbac37030ad13a26db1:<path>`, or `git archive e5b504a6db93a1a72cb79cbac37030ad13a26db1 <paths> | tar -x -C .temp/TASK-261010-gjhb8b-cand`.

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
Attach the outcome `TASK-261010-gjhb8b_panel-verdict.md` to YOUR task `TASK-261010-gjhb8b`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Attach only that text file:
no archives or binary files (tb-R176). Do not stop at the first finding; sweep every surface row (tb-R170). Then run
`task-board handoff TASK-261010-gjhb8b --role researcher`.
