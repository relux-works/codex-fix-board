# R141 panel B TASK-260929-309h9n rev3 — non-recording review panel (tb-R141; same-provider review, operator rule tb-R147)

You review Change Request `CR-TASK-260929-309h9n-3` revision 3 of `TASK-260929-309h9n` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-309h9n`, and do not
write anything on `TASK-260929-309h9n`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-260929-309h9n`)
- Patch: resource `TASK-260929-309h9n_change-request_rev3.patch`. Base commit `67789e1ee29e766e446c7f33feb61561d51f94db`. Expected candidate tree `3c5cbffcc73270bec86364ab42550441c87f933c`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-309h9n) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261012-1tzry5-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 67789e1ee29e766e446c7f33feb61561d51f94db
task-board resource get TASK-260929-309h9n TASK-260929-309h9n_change-request_rev3.patch --output .temp/TASK-260929-309h9n_change-request_rev3.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-309h9n_change-request_rev3.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print 3c5cbffcc73270bec86364ab42550441c87f933c
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show 3c5cbffcc73270bec86364ab42550441c87f933c:<path>`, or `git archive 3c5cbffcc73270bec86364ab42550441c87f933c <paths> | tar -x -C .temp/TASK-261012-1tzry5-cand`.

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
Attach the outcome `TASK-261012-1tzry5_panel-verdict.md` to YOUR task `TASK-261012-1tzry5`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Attach only that text file:
no archives or binary files (tb-R176). Do not stop at the first finding; sweep every surface row (tb-R170). Then run
`task-board handoff TASK-261012-1tzry5 --role researcher`.

## Orchestrator note for this CR
Rev3 = rev2 rework plus a base refresh. (1) Rework on the old base: git diff af312067fcd2392b78deb95d3f71925e739622b7 eb655488b22ff6bb17a3a3a6250fd60e3a202209 (rev2 tree -> precheck-8 tree). It replaces the CODEX_GOAL_PACING_DISABLED env kill switch (A2-F1/B2-N2/D-N2) with Feature::GoalContinuationPacing (key goal_continuation_pacing, Stable, default on), mapped by app-server/src/extensions.rs into GoalExtensionConfig.continuation_pacing and read in on_thread_start only. It decouples the P4a goal_background_wait core fixture from pacing (B2-N1), and it keeps the orchestrator mechanical fix TASK-260929-309h9n_orch-lint-fix-8.md (E0382). (2) Base refresh: trunk moved to 67789e1e when P3-1 landed (PR #15); refresh-candidate replayed the P4b-1 checkpoint as 4649d6571 with one import-only conflict in ext/goal/src/extension.rs (PlanCommitInput + PromptFragment kept, p4b/b2-replay-extension.rs). Trunk content (P3-1) is NOT under review; review only the Story delta against base 67789e1e. Judge the feature flag under the placement-and-size row (A2-F1 was raised there) and also look for: an ambient or env-based production switch left anywhere, the flag not reaching the extension on every host path (app-server vs other hosts constructing GoalExtensionConfig), config.schema.json drift against the generated shape (both features maps), and a mid-thread toggle that resume or config-update would silently ignore (it is documented as read at thread start only; check that the docs say so). Hosted evidence: precheck 9 run 38232681612 on exactly tree 3c5cbffc, all four lanes green, 7/7 mutants killed (TASK-260929-309h9n_hosted-precheck-9.md). The mini runs no local cargo builds or tests: do not run cargo test/build/check/clippy; cargo fmt --check is allowed.
