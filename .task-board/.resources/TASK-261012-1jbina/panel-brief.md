# R141 panel B TASK-260929-1w5ivu rev3 — non-recording review panel (tb-R141; same-provider review, operator rule tb-R147)

You review Change Request `CR-TASK-260929-1w5ivu-3` revision 3 of `TASK-260929-1w5ivu` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-1w5ivu`, and do not
write anything on `TASK-260929-1w5ivu`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-260929-1w5ivu`)
- Patch: resource `TASK-260929-1w5ivu_change-request_rev3.patch`. Base commit `7e4289e21fab653fea8c0089a7ffd790145e5686`. Expected candidate tree `0909471501a910f604164a2bba7b586e2ebf9ba8`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-1w5ivu) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261012-1jbina-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 7e4289e21fab653fea8c0089a7ffd790145e5686
task-board resource get TASK-260929-1w5ivu TASK-260929-1w5ivu_change-request_rev3.patch --output .temp/TASK-260929-1w5ivu_change-request_rev3.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-1w5ivu_change-request_rev3.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print 0909471501a910f604164a2bba7b586e2ebf9ba8
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show 0909471501a910f604164a2bba7b586e2ebf9ba8:<path>`, or `git archive 0909471501a910f604164a2bba7b586e2ebf9ba8 <paths> | tar -x -C .temp/TASK-261012-1jbina-cand`.

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
Attach the outcome `TASK-261012-1jbina_panel-verdict.md` to YOUR task `TASK-261012-1jbina`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Attach only that text file:
no archives or binary files (tb-R176). Do not stop at the first finding; sweep every surface row (tb-R170). Then run
`task-board handoff TASK-261012-1jbina --role researcher`.

## Orchestrator note for this CR
Revision 3 differs from revision 2 (tree 78633964) by exactly one line: codex-rs/ext/goal/BUILD.bazel adds "src/waiting_world_state.rs" to integration_compile_data_extra, fixing review-2 finding A2-F1 (the #[path]-included source was missing from Bazel integration compile data). Orchestrator note TASK-260929-1w5ivu_orch-bazel-fix-6.md (precondition) explains the fix and the same-class sweep. The results text also corrects A2-N1 (the snapshot is at most 512 B only for ASCII names, about 602 B worst case; fragment bounds unaffected). Verify the one-line delta against rev2 (git diff 786339645058198ba030dffbba8ed1cfbf1e36a9 0909471501a910f604164a2bba7b586e2ebf9ba8), re-check A2-F1 and any other #[path] or include_str!/include_bytes! input of the whole delta against BUILD.bazel compile data, and confirm nothing else changed. Rev2 panels B and delta accepted every other row; hosted precheck 6 (TASK-260929-1w5ivu_hosted-precheck-6.md, run 38286079342) ran on the exact tree 09094715: all lanes green, 8/8 mutants killed.
