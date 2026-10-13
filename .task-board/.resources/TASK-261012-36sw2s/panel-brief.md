# R141 panel B TASK-260929-1w5ivu rev1 — non-recording review panel (tb-R141; same-provider review, operator rule tb-R147)

You review Change Request `CR-TASK-260929-1w5ivu-1` revision 1 of `TASK-260929-1w5ivu` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-1w5ivu`, and do not
write anything on `TASK-260929-1w5ivu`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-260929-1w5ivu`)
- Patch: resource `TASK-260929-1w5ivu_change-request_rev1.patch`. Base commit `67789e1ee29e766e446c7f33feb61561d51f94db`. Expected candidate tree `3685fd24cebba08c08ef741f928c58610983abf9`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-1w5ivu) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261012-36sw2s-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 67789e1ee29e766e446c7f33feb61561d51f94db
task-board resource get TASK-260929-1w5ivu TASK-260929-1w5ivu_change-request_rev1.patch --output .temp/TASK-260929-1w5ivu_change-request_rev1.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-1w5ivu_change-request_rev1.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print 3685fd24cebba08c08ef741f928c58610983abf9
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show 3685fd24cebba08c08ef741f928c58610983abf9:<path>`, or `git archive 3685fd24cebba08c08ef741f928c58610983abf9 <paths> | tar -x -C .temp/TASK-261012-36sw2s-cand`.

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
Attach the outcome `TASK-261012-36sw2s_panel-verdict.md` to YOUR task `TASK-261012-36sw2s`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Attach only that text file:
no archives or binary files (tb-R176). Do not stop at the first finding; sweep every surface row (tb-R170). Then run
`task-board handoff TASK-261012-36sw2s --role researcher`.

## Orchestrator note for this CR
Rev1 of P3-2, the second leaf of STORY-260929-40trfs; P3-1 (the WaitingCapabilities snapshot) is already on trunk 67789e1e and is NOT under review. Review only the Story delta against base 67789e1e. Orchestrator decision recorded in the task notes: the turn-boundary bound is the accepted P3-2 contract. Contributions emit once per turn while routers rebuild per sampling step, so a goal created mid-turn leaves one follow-up request with clock.sleep and no fragment yet, and a goal completed mid-turn leaves one follow-up request whose fragment still names clock.sleep. Both windows are pinned in waiting_guidance_tool_created_goal_reacts_at_next_turn; per-step re-emission is a separate follow-up (a core change). Treat these two windows as disclosed bounds, not defects, but DO flag any third window, any claim mismatch at a turn-start request, or a bound the code comments misdescribe. Also disclosed: 1376 changed lines vs the 600 target (production about 90 lines; the rest is tests); native mail wait and the positive exec sentence are covered by unit tests only; the no-wait/end-turn paragraph is deferred until P4b pacing is active; BudgetLimited is gated in, following P2 GoalActivity scope. The §9 core goal-less exec paragraph is out of scope by orchestrator decision (it would change model-visible context for every session). Hosted evidence: precheck 2 run 38239371527 on exactly tree 3685fd24, all four lanes green, 7/7 mutants killed (TASK-260929-1w5ivu_hosted-precheck-2.md); precheck 1 failures and fixes are in a2-rework-brief-precheck1.md and the results fix map. The mini runs no local cargo builds or tests: do not run cargo test/build/check/clippy; cargo fmt --check is allowed.
