# R141 panel A TASK-260929-2gp04j rev3 — non-recording review panel (tb-R141; same-provider review, operator rule tb-R147)

You review Change Request `CR-TASK-260929-2gp04j-3` revision 3 of `TASK-260929-2gp04j` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-2gp04j`, and do not
write anything on `TASK-260929-2gp04j`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-260929-2gp04j`)
- Patch: resource `TASK-260929-2gp04j_change-request_rev3.patch`. Base commit `729f259e62a8d11d9e17398e487790e1ee5d8b8c`. Expected candidate tree `a8fc9e0cc6e0aad477aba7cd377e3c93203932fe`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-2gp04j) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261005-2x4cdu-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 729f259e62a8d11d9e17398e487790e1ee5d8b8c
task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev3.patch --output .temp/TASK-260929-2gp04j_change-request_rev3.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev3.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print a8fc9e0cc6e0aad477aba7cd377e3c93203932fe
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show a8fc9e0cc6e0aad477aba7cd377e3c93203932fe:<path>`, or `git archive a8fc9e0cc6e0aad477aba7cd377e3c93203932fe <paths> | tar -x -C .temp/TASK-261005-2x4cdu-cand`.

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
Attach the outcome `TASK-261005-2x4cdu_panel-verdict.md` to YOUR task `TASK-261005-2x4cdu`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Attach only that text file:
no archives or binary files (tb-R176). Do not stop at the first finding; sweep every surface row (tb-R170). Then run
`task-board handoff TASK-261005-2x4cdu --role researcher`.

## Orchestrator note for this CR
Round 3 of the story-final CR of STORY-260929-bohnqb (P2). Round-2 verdict TASK-260929-2gp04j_review-verdict-rev2.md (read-failure class in set_thread_goal / metrics paths). Rev 3 adds a sweep table of every goal-state read and revokes on each failure; the Story was rebased onto trunk 729f259. Exact-tree hosted evidence: TASK-260929-2gp04j_hosted-precheck-6.md (tree a8fc9e0c, all lanes green, 20/20 mutants killed) - cite it as executed attacks.
