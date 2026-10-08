# R141 panel A TASK-260929-u2i5rr rev4 — non-recording review panel (tb-R141; models per R80/R132, tb-R146)

You review Change Request `CR-TASK-260929-u2i5rr-4` revision 4 of `TASK-260929-u2i5rr` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-u2i5rr`, and do not
write anything on `TASK-260929-u2i5rr`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-260929-u2i5rr`)
- Patch: resource `TASK-260929-u2i5rr_change-request_rev4.patch`. Base commit `0462dcc062b822bb8fff16cc31ce6eeab69823b9`. Expected candidate tree `e9a8095f146dd156b09351cc2af473781aa37272`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-u2i5rr) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261002-3auvlm-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 0462dcc062b822bb8fff16cc31ce6eeab69823b9
task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_change-request_rev4.patch --output .temp/TASK-260929-u2i5rr_change-request_rev4.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-u2i5rr_change-request_rev4.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print e9a8095f146dd156b09351cc2af473781aa37272
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show e9a8095f146dd156b09351cc2af473781aa37272:<path>`, or `git archive e9a8095f146dd156b09351cc2af473781aa37272 <paths> | tar -x -C .temp/TASK-261002-3auvlm-cand`.

## Review
Follow the reviewer role contract's review-round rules: attack, don't just read; every surface-table row gets
exactly one result (held / broken / not-attacked with a reason); then a bounded free hunt. Do NOT run cargo, just or
any build or test: the shared build target is serialized (one codex-fix build at a time). Execution evidence is the
element's CR validation log (local fast lane) and the hosted relux-ci result when attached. Your review is the replay
plus a static attack.

## Deliverable
Attach the outcome `TASK-261002-3auvlm_panel-verdict.md` to YOUR task `TASK-261002-3auvlm`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Then run
`task-board handoff TASK-261002-3auvlm --role researcher`.

## Orchestrator note for this CR
Round 2 for B1 (task_delta leaf of STORY-260929-wg1ya0). Revisions 2 and 3 failed only the old local gate (app-server load flakes); revision 4 republishes the same code (candidate tree e9a8095f, identical to rev 2) under the fast local lane. Round-1 merged verdict: TASK-260929-u2i5rr_review-verdict-rev1.md (F1-F3: missing mutant-killing tests). The completion_receipt unit tests live in codex-core and run on hosted relux-ci, not locally: a dispatch on this exact candidate tree is in flight and will be attached as TASK-260929-u2i5rr_hosted-ci-rev4.md; the recording step waits for it. Review statically against the surface table and the AC, and check the tests named in TASK-260929-u2i5rr_results.md for F1-F3.
