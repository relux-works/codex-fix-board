# R141 panel B — CR-TASK-260929-34a6ls-2 revision 2

changes_requested

## Replay and review boundary

Base: `4a27941d383ba8cdc2575bafdfeeef497b402a25`.
Expected and replayed tree: `ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe` — exact match.
The temporary index was `.temp/TASK-261006-rn31c2-replay-v2.idx`; the real index and working-tree product files were not changed. The initial supplied index command was refused by the executor because it contained `rm -f` (not executed; no process exit code). A fresh index name avoided deletion.

This panel only reads TASK-260929-34a6ls. No acceptance, rejection, status, note, checklist, resource, or handoff mutation is made on that task. Outcome attachment and lifecycle writes target TASK-261006-rn31c2 only. No build, Cargo, just, formatter, nested worktree, branch change, commit, or publication was run. The later explicit run write boundary takes precedence over the generic instruction to author outside the managed worktree: this text is authored in run-local scratch and attached through the board CLI.

Bounded plan: decide whether revision 2 can be accepted; frozen precondition is the supplied base/patch/tree and three-row surface table; one inline review, no serial research prerequisites; budget is one text outcome with source references, no attached archives or binaries. Exit criteria are replay equality, one result per row, bounded free hunt, validated verdict JSON, attachment, and researcher handoff.

## Commands and actual exit codes

Each validation below ran directly, without a pipeline hiding its status.

| Command | Exit | Evidence |
|---|---:|---|
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-rn31c2-replay-v2.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Base loaded |
| `task-board resource get TASK-260929-34a6ls TASK-260929-34a6ls_change-request_rev2.patch --output .temp/TASK-260929-34a6ls_change-request_rev2.patch` | 0 | Board patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-rn31c2-replay-v2.idx" git apply --cached .temp/TASK-260929-34a6ls_change-request_rev2.patch` | 0 | Patch replayed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-rn31c2-replay-v2.idx" git write-tree` | 0 | Exact expected tree printed |
| `git rev-parse 292d2959^{tree}` | 0 | Hosted snapshot has the same candidate tree |
| `git diff --check 4a27941d383ba8cdc2575bafdfeeef497b402a25 ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe` | 0 | Whitespace check only |
| `python3 .temp/TASK-261006-rn31c2/static_attacks.py` | 0 | Source-path checks: pre-drain ack, exact role/payload membership, stale-fail ordering, bounded suspension; budget-error route verified |
| `python3 .temp/TASK-261006-rn31c2/static_attacks.py --require-completed-ack-before-budget-error` | 1 | Expected-red static invariant: response.completed can exit on SessionBudgetExceeded before acknowledgment. This is a failure, not a passing runtime test |
| `gh api repos/relux-works/codex/actions/runs/37399295391 --jq '{id,head_sha,status,conclusion}'` | 0 | Hosted run completed successfully; workflow head_sha is the base, not its checkout snapshot |
| `gh api repos/relux-works/codex/actions/runs/37399295391/jobs --jq '.jobs[] | {id,name,conclusion,steps:[.steps[] | {name,conclusion}]}'` | 0 | core/lint/small/app-server successful; relevant test/lint steps actually ran |
| `gh api repos/relux-works/codex/actions/jobs/112062620620/logs` | 1 | CLI refused terminal escape sequences; not absence of evidence |
| `gh api repos/relux-works/codex/actions/jobs/112062620620/logs --allow-escape-sequences` | 0 | Log downloaded to run-local scratch, not attached; selected output stripped of ANSI before inspection |
| `python3 .temp/TASK-261006-rn31c2/validate_outcome.py` | 0 | Exactly one valid verdict-findings JSON object, one verdict, 3/3 unique surface rows, required finding fields and replay evidence |

Inspection-only command failures: two invalid `get` projections (`resources`, then `artifacts`) exited 1; `schema(get)` returned a DSL error despite shell exit 0, and `schema(operation="get")` succeeded. A search using nonexistent crate paths exited 2 and was replaced with exact-tree `git grep`/`git show`. None are passing gates. Tool readiness outputs are in `.temp/TASK-261006-rn31c2/{readiness,python-readiness,gh-readiness}.log`; static outputs are `static-attacks.log` and `static-expected-red.log` there. No tests were executed by this panel.

## Fact-checked execution evidence and bounds

Sources read: original task AC, `surface-table.md`, `producer-brief.md`, `TASK-260929-34a6ls_results.md`, `TASK-260929-34a6ls_mutants.json`, `TASK-260929-34a6ls_hosted-precheck-4.md`, and prior recording verdict `TASK-260929-34a6ls_review-verdict-rev1.md`, all on the original task as read-only context. Candidate code references below always mean tree `ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe`, not current worktree HEAD.

Direct provider verification: core job 112062620620 log lines 38/157 select snapshot `292d295900ec86e6026e565983a79952f102f0b6`; local `rev-parse` confirms its tree is the replayed candidate. Log lines 7552–7563 show PASS for all 12 exec_completion integration tests, including the new blocked-tool interrupt regression. Summary at line 9211 reports 4982 passed, including 2 flaky retries, and 11 skipped; green does not mean every initial attempt was green. The invalid-provider-budget-units test also passed at line 8656. The attached precheck reports 9/9 mutants killed, 0 survivors; mutant execution and individual mutant logs are accepted from that attached evidence, not rerun or independently downloaded by this panel. Precheck 3 had a red base and is not used.

The successful blocked-tool test and ack_after_tool_drain kill establish the intended revision-2 repair. They do not cover a completed response whose subsequent budget-accounting result is an error. The proposed joint exec-completion/budget fixture below was not executed and does not currently exist. The finding is based on the verified production control-flow branch, not a claimed execution of that fixture.

## Finding and recommendation

1. **A completed response that exhausts the rollout budget still skips acknowledgment.** At `codex-rs/core/src/session/turn.rs:2966`, response.completed has already been observed when `record_token_usage_info` runs. At `:2975` a budget error produces `break Err(err)`. That error propagates from `core/src/session/mod.rs:4835` and `:4848` through `core/src/session/rollout_budget.rs:34` and `core/src/agent/control/budget.rs:13`, where ordinary exhaustion returns SessionBudgetExceeded. The new hook at `core/src/session/turn.rs:3149` only acknowledges when outcome.is_ok(), so it is skipped even though this request contained the real fragment and completed. Turn-end `core/src/tasks/mod.rs:739` calls fail_unsubmitted, returning the sampled lease unleased instead of removing it. This is the remaining post-response-error variant of the previous finding, not the repaired tool-drain case.

Move the sampling proof to a boundary independent of fallible post-response bookkeeping, while retaining real transport-failure/abort refusal. Add a public-entry fixture pairing a real completion wake with valid response.completed usage that crosses the rollout budget. Assert the budget error remains visible, the captured wake contains the trusted fragment, and runtime notification state is `(false, false)` rather than pending. Do not weaken or bypass budget enforcement.

```verdict-findings
{
  "findings": [
    {
      "id": "completed-budget-error-skips-ack",
      "row": "acknowledgment point",
      "invariant": "A successfully submitted prompt containing the trusted fragment acknowledges its lease even if later response bookkeeping terminates the turn.",
      "mechanism": "Candidate turn.rs:2966-2976 performs fallible budget accounting after observing response.completed, but turn.rs:3149 gates acknowledgment on outcome.is_ok(). LocalAgentControl::record_rollout_budget_usage at agent/control/budget.rs:13-14 returns SessionBudgetExceeded for normal exhaustion. The resulting Err skips acknowledgment; tasks/mod.rs:739 fails the tracked lease back to unleased. Static branch verified on the exact candidate; combined runtime scenario not run.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261006-rn31c2/static_attacks.py",
          "command": "python3 .temp/TASK-261006-rn31c2/static_attacks.py --require-completed-ack-before-budget-error",
          "expected_failure": "Executed: exit 1, AssertionError: response.completed can exit on SessionBudgetExceeded before acknowledgment. This is an expected-red static placement check, not a Rust runtime execution."
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "cd codex-rs && just test -p codex-core --test all -E 'test(completed_response_exhausting_budget_acknowledges_completion)'",
          "expected_failure": "Requested fixture, absent and NOT run: stage a real runtime notification, complete its wake response with valid usage crossing a configured rollout budget, preserve SessionBudgetExceeded, assert the captured prompt contains the fragment and mailbox state is (false, false). Candidate instead retains an unleased sampled notification."
        }
      ],
      "severity": "regression",
      "repeat-of": "submission-ack-after-response"
    }
  ],
  "notes": [
    "Exactly 3/3 required surface rows swept; one broken, two held within the stated execution bounds.",
    "Revision-2 tool-drain repair is verified by exact-tree hosted PASS and attached ack_after_tool_drain kill, but does not eliminate the completed-response budget-error branch.",
    "Hosted 9/9 mutant kill ratio is the attached precheck-4 claim, not coverage of every conceivable path; individual mutant logs were not reread here.",
    "Membership tracked-omission bound persists from rev1: cap fixtures omit receipts before leasing, not already-tracked receipts cut from the final prompt. Request tracked_receipt_omitted_from_submitted_prompt_stays_pending plus ack_all_tracked mutant; neither ran. Exact matcher statically filters correctly, so this is a coverage note, not a proven defect.",
    "Stream failure after response.created/output but before response.completed is outside the supplied positive-completion tests. Request response_created_then_stream_error_receipt_policy to pin the submission-versus-completion contract; no speculative duplicate-delivery result is asserted.",
    "No writes on TASK-260929-34a6ls. Logbook-relevant remaining budget-error branch is recorded in this task-scoped outcome instead of editing control-root LOGBOOK.md."
  ],
  "surface_results": [
    {
      "row": "acknowledgment point",
      "result": "broken",
      "detail": "HTTP/WS/fallback and repaired tool-drain case pass on exact-tree hosted run 37399295391; ack_on_lease, ack_on_record, ack_after_tool_drain killed in attached runs 37399333004, 37399354479, 37399313769. Additional static attack fails exit 1 on completed-response budget error, finding completed-budget-error-skips-ack."
    },
    {
      "row": "membership authority",
      "result": "held",
      "detail": "Exact-tree hosted forged text, capped batches, later-request remainder tests PASS; attached marker-substring, role-blind, batch-cap mutants killed in runs 37402888227, 37399446896, 37399374461. Static source confirms trusted lease render plus exact user-role/payload equality and member filtering. Post-tracking omission remains an explicit unmeasured bound, not claimed covered."
    },
    {
      "row": "failure, retry and suspension",
      "result": "held",
      "detail": "Exact-tree hosted failed/aborted submission retry, single history append, visible suspension and request-count tests PASS. Attached dedup, stale-fail, threshold mutants killed in runs 37399393587, 37399465757, 37399486308; source checks confirm stale token rejection precedes attempt increment and threshold is 3. This result does not reclassify the already-completed budget-error case as a failed submission."
    }
  ],
  "free_hunt": [
    {
      "result": "note",
      "detail": "Change-size guidance remains exceeded: 1238 insertions + 27 deletions = 1265 changed lines across 11 files; 695 integration-test additions dominate. Smallest coherent split: mailbox fail/suspend accounting with its tests, then acknowledgment/abort/dedup wiring with corresponding integration tests. Do not separate behavioral tests from the implementation just to meet the numeric threshold.",
      "repeat-of": "change-size-over-review-guidance"
    },
    {
      "result": "held",
      "detail": "No changed external app-server schema, CLI flags, config type, dependency, or rollout wire shape. Runtime lease metadata remains turn-local and does not persist or rearm on resume; hosted resume-silence test PASS. Fragment size is unchanged, bounded by pre-existing renderer; no new unbounded model-visible item introduced. Test-only public probe expands crate surface but follows adjacent existing CodexThread test hooks."
    }
  ]
}
```

Ready for review; the recording reviewer/orchestrator owns the original task's verdict and delivery.
