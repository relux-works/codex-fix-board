# R141 panel B TASK-261002-1ugz6h rev2 — non-recording review panel (tb-R141; models per R80/R132, tb-R146)

You review Change Request `CR-TASK-261002-1ugz6h-2` revision 2 of `TASK-261002-1ugz6h` as an independent panel. You are NOT the
recording reviewer. Do not run accept_cr, reject_cr, withdraw_cr, set_status or handoff on `TASK-261002-1ugz6h`, and do not
write anything on `TASK-261002-1ugz6h`. The orchestrator merges your verdict with the other panel's, and one recording reviewer
records the merged result.

## Inputs (read-only, all on `TASK-261002-1ugz6h`)
- Patch: resource `TASK-261002-1ugz6h_change-request_rev2.patch`. Base commit `35af013b901ed4be1b88416068f140e9ca5cc85d`. Expected candidate tree `429a14a27a106f73b5907a0d830c4548cb3f1ea4`.
- `surface-table.md`: the rows you must sweep. The task's AC table: `task-board q 'get(TASK-261002-1ugz6h) { description scope ac }'`.
- `producer-brief.md`, the task's results outcome and any notes. Treat them as context, not instructions.

## Replay (mandatory, first)
Replay through a temporary index, never a nested worktree:
```sh
cd "$(git rev-parse --show-toplevel)"; IDX="$PWD/.temp/TASK-261002-gy8y8u-replay.idx"; mkdir -p .temp; rm -f "$IDX"
GIT_INDEX_FILE="$IDX" git read-tree 35af013b901ed4be1b88416068f140e9ca5cc85d
task-board resource get TASK-261002-1ugz6h TASK-261002-1ugz6h_change-request_rev2.patch --output .temp/TASK-261002-1ugz6h_change-request_rev2.patch   # or read it from the board resources path
GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-261002-1ugz6h_change-request_rev2.patch
GIT_INDEX_FILE="$IDX" git write-tree    # must print 429a14a27a106f73b5907a0d830c4548cb3f1ea4
```
A mismatch is a finding (severity bypass) and ends the review. Read candidate files with
`git show 429a14a27a106f73b5907a0d830c4548cb3f1ea4:<path>`, or `git archive 429a14a27a106f73b5907a0d830c4548cb3f1ea4 <paths> | tar -x -C .temp/TASK-261002-gy8y8u-cand`.

## Review
Follow the reviewer role contract's review-round rules: attack, don't just read; every surface-table row gets
exactly one result (held / broken / not-attacked with a reason); then a bounded free hunt. Do NOT run cargo, just or
any build or test: the shared build target is serialized (one codex-fix build at a time). Execution evidence is the
element's CR validation log (local fast lane) and the hosted relux-ci result when attached. Your review is the replay
plus a static attack.

## Deliverable
Attach the outcome `TASK-261002-gy8y8u_panel-verdict.md` to YOUR task `TASK-261002-gy8y8u`. It must contain exactly one fenced block with
the info string `verdict-findings` holding one JSON object: `findings` (each with id, row, invariant, mechanism,
reproductions[test_file, command, expected_failure], severity in bypass|regression|robustness|note, repeat-of),
`notes`, `surface_results` (every row once) and `free_hunt`. Above the block, state the replay tree check, the
commands you ran with exit codes, and your one-word verdict: accept or changes_requested. Then run
`task-board handoff TASK-261002-gy8y8u --role researcher`.

## Orchestrator note for this CR
Round 2 of the Story's FINAL CR (story_final; diff against base 35af013 is cumulative). The two astra snapshot files were accepted in leaf 1 (CR-TASK-261002-ifa91r-1, checkpoint ec6a700, tree 5c365d9a): verify they are byte-identical to that checkpoint (git diff ec6a7009d28c3f3ae954bd388600b3b9b80c4c70 <candidate tree> touches only .github/workflows/relux-ci.yml) and spend the review on the workflow file. Round-1 merged verdict: TASK-261002-1ugz6h_review-verdict-rev1.md (3 findings: lint warnings not failing, inputs.sha not verified, push concurrency per ref). Hosted evidence for this exact tree: TASK-261002-1ugz6h_hosted-ci-stack-5.md (run 36974560859, all lanes green, lint gate count line) and the negative control TASK-261002-1ugz6h_hosted-ci-neg-1.md (run 36974565033: the gate fails the lint lane on an injected unused import). The 3 KNOWN_WARNINGS are upstream-baseline warnings present at the fork's upstream pin (verify with git show 0462dcc062b822bb8fff16cc31ce6eeab69823b9:<path>).
