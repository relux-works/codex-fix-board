# R141 panel DELTA TASK-260929-2is91w rev5 — non-recording review panel (tb-R141; same-provider review, operator rule tb-R147)

You review Change Request `CR-TASK-260929-2is91w-5` revision 5 of `TASK-260929-2is91w` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-2is91w`, and do not
write anything on `TASK-260929-2is91w`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

This is the DELTA panel (round 2+). Check, in order: (1) every finding of the previous round's merged verdict (`TASK-260929-2is91w_review-verdict-rev<prev>.md` on TASK-260929-2is91w) is fixed correctly; (2) whether the same class of problem appears anywhere else in the code; (3) whether the rework broke anything.

## Inputs (read-only, all on `TASK-260929-2is91w`)
- Patch: resource `TASK-260929-2is91w_change-request_rev5.patch`. Base commit `e0eff057620104a416080da616256ee7f32bda1b`. Expected candidate tree `afb8c830d764ba489a9f2f922c0babdf1dbe036e`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-2is91w) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261012-1xa3sr-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree e0eff057620104a416080da616256ee7f32bda1b
task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev5.patch --output .temp/TASK-260929-2is91w_change-request_rev5.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-2is91w_change-request_rev5.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print afb8c830d764ba489a9f2f922c0babdf1dbe036e
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show afb8c830d764ba489a9f2f922c0babdf1dbe036e:<path>`, or `git archive afb8c830d764ba489a9f2f922c0babdf1dbe036e <paths> | tar -x -C .temp/TASK-261012-1xa3sr-cand`.

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
Attach the outcome `TASK-261012-1xa3sr_panel-verdict.md` to YOUR task `TASK-261012-1xa3sr`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Attach only that text file:
no archives or binary files (tb-R176). Do not stop at the first finding; sweep every surface row (tb-R170). Then run
`task-board handoff TASK-261012-1xa3sr --role researcher`.

## Orchestrator note for this CR
Loop-detector S1 (revisions=5 > 3) answered with fan-out: this round reviews the FULL surface table, every row attacked afresh, not only the delta. Rev4 was accepted by all panels but unrecordable because row `configuration coverage` (AC5) was not-attacked for the remote catalog leg. Rev5 adds integration test remote_catalog_replacement_changes_waiting_snapshot (core/tests/suite/search_tool.rs): two List cases (remote-only path) and two Hide cases (same-slug merge in models-manager/src/manager.rs apply_remote_models, with merge-proof assertions). Mutant snapshot_ignores_remote_catalog_replacement is killed in precheck 14 (run 38191980780); it SURVIVED precheck 12 when only the remote-only path was driven. Attack this row directly and mark it held or broken; every row must end held or broken, never not-attacked. Precheck 14 core first failed suite::scenarios::guardian_agent_messages::encrypted_parent_reply_survives_incremental_guardian_reviews (3x 10s timeout); a rerun of that job on the same snapshot passed (1.6s), and the test also flaked on this base in precheck 11; the CR touches no guardian code. Confirm or refute that attribution. Put any free-hunt coverage in notes; free_hunt must hold only real findings.
