# R141 panel A TASK-260929-u2i5rr rev5 — non-recording review panel (tb-R141; models per R80/R132, tb-R146)

You review Change Request `CR-TASK-260929-u2i5rr-5` revision 5 of `TASK-260929-u2i5rr` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-260929-u2i5rr`, and do not
write anything on `TASK-260929-u2i5rr`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-260929-u2i5rr`)
- Patch: resource `TASK-260929-u2i5rr_change-request_rev5.patch`. Base commit `0462dcc062b822bb8fff16cc31ce6eeab69823b9`. Expected candidate tree `00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-260929-u2i5rr) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261002-2bf97a-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 0462dcc062b822bb8fff16cc31ce6eeab69823b9
task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_change-request_rev5.patch --output .temp/TASK-260929-u2i5rr_change-request_rev5.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-u2i5rr_change-request_rev5.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8:<path>`, or `git archive 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8 <paths> | tar -x -C .temp/TASK-261002-2bf97a-cand`.

## Review
Follow the reviewer role contract's review-round rules: attack, don't just read; every surface-table row gets
exactly one result (held / broken / not-attacked with a reason); then a bounded free hunt. Do NOT run cargo, just or
any build or test: the shared build target is serialized (one codex-fix build at a time). Execution evidence is the
element's CR validation log (local fast lane) and the hosted relux-ci result when attached. Your review is the replay
plus a static attack.

## Deliverable
Attach the outcome `TASK-261002-2bf97a_panel-verdict.md` to YOUR task `TASK-261002-2bf97a`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Then run
`task-board handoff TASK-261002-2bf97a --role researcher`.

## Orchestrator note for this CR
Round 3 for B1 (task_delta leaf of STORY-260929-wg1ya0). Round-2 merged verdict: TASK-260929-u2i5rr_review-verdict-rev4.md (5 test-coverage findings: terminal-history bound M15, terminal-path owner gates M12-M14, AlreadyTerminal, 256-byte call-id boundary, deterministic sampling-source attribution M16). Revision 5 adds tests for them and reverts 3 out-of-scope upstream lint edits (now 3 paths). Hosted evidence for this exact tree: TASK-260929-u2i5rr_hosted-ci-rev5.md (run 36987452652, all lanes green, 20 completion_receipt tests pass incl. owner_accepts_256_bytes_and_refuses_257, terminal_history_evicts_only_the_oldest_after_64_outcomes, terminal_history_refuses_foreign_owners_and_repeat_cancellation). Judge by reading whether each named mutant now fails a test; say so per mutant.
