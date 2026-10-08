# DELTA panel — CR-TASK-260929-34a6ls-2 revision 2

changes_requested

## Replay and scope

Date: 2026-10-06. Reviewer task: TASK-261006-10jpkf, r141-panel-delta-task-260929-34a6ls-rev2.
Read-only candidate review, not a recording review. No mutation, note, acceptance,
rejection, status change, or handoff was made on TASK-260929-34a6ls.

Base: `4a27941d383ba8cdc2575bafdfeeef497b402a25`.
Temporary-index replay returned `ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe`, exactly
the expected candidate tree. The working-tree index was not used or changed.
All candidate citations below refer to that tree, not the worktree's base files.

Bounded research plan: decide whether revision 2 fixes the previous finding and
holds the three specified surfaces; frozen precondition is the supplied base,
patch and tree (no new grammar); time ceiling 60 minutes; one text outcome under
20 KiB; zero additional serial prerequisites; exit after replay, previous-finding
check, three-row sweep and bounded free hunt. No local cargo, just, build, test,
PR, branch or product-source write. Scratch files remain inside the assigned
worktree; resource attachment persists the outcome outside it through the board
CLI, without directly editing the control root.

## Commands and evidence honesty

Commands below ran directly, not through tee. Paths are relative to the assigned
project root unless otherwise stated. Resource reads and inspections are not
behavioral test execution.

| Command | Real exit | Result |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261006-10jpkf, status=analysis)'` | 0 | Assigned task started |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-10jpkf-replay.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Base loaded |
| `task-board resource get TASK-260929-34a6ls TASK-260929-34a6ls_change-request_rev2.patch --output .temp/TASK-260929-34a6ls_change-request_rev2.patch` | 0 | Supplied patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-10jpkf-replay.idx" git apply --cached .temp/TASK-260929-34a6ls_change-request_rev2.patch` | 0 | Patch replayed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-10jpkf-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git diff --check 4a27941d383ba8cdc2575bafdfeeef497b402a25 ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe` | 0 | Whitespace check only |
| `git show -s --format='%H %T' 292d295900ec86e6026e565983a79952f102f0b6` | 0 | Hosted snapshot commit maps to the exact candidate tree |
| `gh api repos/relux-works/codex/actions/runs/37399295391` | 0 | Successful snapshot run; workflow head is base, not snapshot |
| `gh api repos/relux-works/codex/actions/runs/37399295391/jobs` | 0 | core, lint, small, app-server all success |
| `gh api repos/relux-works/codex/actions/jobs/112062620620/logs` | 1 | Download refused terminal escape sequences; not missing evidence |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/112062620620/logs` | 0 | Actual hosted core log inspected |
| `gh api repos/relux-works/codex/actions/runs/37399313769/jobs` | 0 | ack-after-drain mutant: core failed, other lanes success |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/112062681244/logs` | 0 | Actual mutant core log inspected |
| `ruby .temp/TASK-261006-10jpkf/ack-placement.rb .temp/TASK-261006-10jpkf/turn.rs pre-drain` | 0 | `ack_before_drain=true` |
| `ruby .temp/TASK-261006-10jpkf/ack-placement.rb .temp/TASK-261006-10jpkf/turn.rs submission` | 1 | Expected-red static placement assertion: response cancellation, stream error and completed-budget error precede ack |
| `ruby .temp/TASK-261006-10jpkf/validate-outcome.rb .temp/TASK-261006-10jpkf/TASK-261006-10jpkf_panel-verdict.md` | 0 | Exactly one valid JSON block, three unique surface rows, required finding fields |

Static probe bootstrap initially exited 1 with `Missing source anchors`: it
searched for an untyped outcome declaration. Correcting the anchor to the actual
typed declaration produced the two recorded results above. This bootstrap failure
was not a product defect. An initial shell invocation containing `rm -f` was
refused before execution; no replay result was inferred from it. Scoped board
projection probes for `resources`, `artifacts` and `inputResources` were rejected;
the successful `outcomeResources` projection and exact resource downloads supplied
the evidence. These read failures were not treated as absence.

Read resources, each successfully downloaded (exit 0): `surface-table.md`,
`producer-brief.md`, `TASK-260929-34a6ls_review-verdict-rev1.md`,
`TASK-260929-34a6ls_results.md`, `TASK-260929-34a6ls_mutants.json`,
`TASK-260929-34a6ls_change-request_rev2-validation.log`, and the rev1 patch.
Candidate files were read with `git show <candidate-tree>:<path>` (exit 0).
An attempted `core/src/tool_metadata.rs` read failed (exit 128); the actual module
is `core/src/client_tool_metadata.rs`, read successfully. No finding depends on
the failed path. Other file searches, source projections and tooling checks were
orientation only, not gates.

### Reused hosted execution (not executed locally)

Run `37399295391`, core job `112062620620`: checkout log explicitly selects
`292d295900ec86e6026e565983a79952f102f0b6`, checks HEAD against WANT_SHA, and
the local object proves its tree equals the replay tree. Ubuntu 24.04.5,
Rust toolchain pinned by the workflow to 1.95.0. Core summary: 4982 passed,
11 skipped, 2 flaky. The named exec-completion and matcher tests below show PASS
lines, not merely an aggregate green badge. Core command uses the workflow's
existing exclusion expression; the skipped tests are not claimed covered.

Run `37399313769`, core job `112062681244`: checkout is the dedicated
`ack_after_tool_drain` mutant snapshot (`d05461e` in checkout log). Core summary:
4981 passed, 1 failed, 11 skipped; the sole failed test is
`completed_response_with_blocked_tool_acknowledges_before_interrupt`, including
retry failures. Hosted command exit is **100**, expected red. This is a successful
mutation kill, not a passing suite. The producer reports 9/9 kills overall; this
panel independently read the base core log and this one delta-mutant log, not
the other eight mutant logs. The other eight kills remain attributed to the
producer's results resource and are not presented as independently rerun proof.

## Previous finding and remaining defect

The original post-tool-drain window is repaired: candidate `turn.rs:3150`
acknowledges before `drain_in_flight` at `:3159`. The new integration test at
`core/tests/suite/exec_completion.rs:881` passes on the exact snapshot and fails
when the old placement is restored. That narrow repair is confirmed.

The same late-ack class survives **before the new hook**. In the Completed branch,
`turn.rs:2967` calls `record_token_usage_info`, and `:2975` breaks with its error.
`session/mod.rs:4805` propagates the real rollout-budget accounting result, via
`session/rollout_budget.rs:34`. The real integration test
`suite::rollout_budget::exhausted_budget_fails_current_and_later_turns`
(`core/tests/suite/rollout_budget.rs:280`) proves a successfully completed response
can yield SessionBudgetExceeded; it passes in the same hosted log. Thus a completed
request containing a trusted completion can skip `outcome.is_ok()` and leave its
already-sampled lease tracked. `tasks/mod.rs:739` then invokes `fail_unsubmitted`,
returning that lease to the retry path instead of acknowledging it. This defect
does not depend on interpreting an HTTP request merely sent as successfully
accepted: **response.completed has already arrived**.

There is also the broader accepted-but-not-completed window: `turn.rs:2632` can
break on cancellation, and `:2659` can break on a stream error after Created and
assistant output. No ack runs in the Created/output branches. A late transport
failure therefore still controls delivery accounting despite the model having
consumed the fragment. The existing failed-submission fixture emits invalid_prompt;
the aborted fixture delays the entire response before interrupt. Neither fixture
attacks a created/output-producing response interrupted later. Do not move ack
to reservation or history append; use actual successful transport acceptance and
the actual submitted membership, with no downstream budget/tool dependency.

No combined receipt+budget or post-output stream-error integration test was
executed by this panel. The blocking evidence is the pinned production control
flow and an independently verified existing budget error path, not a claim of
dynamic reproduction of the combined scenario.

## Logbook entry

2026-10-06 — delta review: exact replay and hosted snapshot identity verified;
previous tool-drain placement fixed and narrowing mutant genuinely killed;
completed-response budget error still bypasses acknowledgment. Recorded here as
the task-scoped outcome/logbook entry; no direct control-root logbook edit and
no write to the reviewed producer task.

```verdict-findings
{
  "findings": [
    {
      "id": "submission-ack-still-gated-by-response-outcome",
      "row": "acknowledgment point",
      "invariant": "A successfully submitted request containing a trusted completion acknowledges that lease independently of subsequent response-processing, budget-accounting, tool-drain, or cancellation errors.",
      "mechanism": "Candidate codex-rs/core/src/session/turn.rs:3150 still gates acknowledgment on outcome.is_ok(). ResponseEvent::Completed at :2936 runs token/budget accounting at :2967 and breaks Err at :2975 before reaching that hook. Real SessionBudgetExceeded is propagated through session/mod.rs:4805 and session/rollout_budget.rs:34; tasks/mod.rs:739 fails the still-tracked already-sampled lease. Additionally cancellation/stream errors at turn.rs:2632/:2659 after Created/output bypass the same hook. The old post-tool-drain window is fixed, but downstream response success still decides submission acknowledgment.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261006-10jpkf/ack-placement.rb",
          "command": "ruby .temp/TASK-261006-10jpkf/ack-placement.rb .temp/TASK-261006-10jpkf/turn.rs submission",
          "expected_failure": "Observed exit 1, expected-red static source-placement assertion: ack_before_response_loop=false; cancel_and_stream_error_before_ack=true; completed_budget_error_before_ack=true. Not a dynamic receipt reproduction. Probe source is included below for reproducibility."
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "PROPOSED, NOT RUN: cd codex-rs && just test -p codex-core --test all -E 'test(completed_response_budget_exhaustion_acknowledges_receipt)'",
          "expected_failure": "Add this test using build_with_auto_env and a real queued completion: complete the wake response with usage that exhausts the rollout budget; wait for SessionBudgetExceeded and TurnComplete; assert captured wake contains the trusted fragment and mailbox is (false,false). Candidate is expected to retain/requeue it because budget error bypasses ack. Test does not exist in the candidate and was not executed."
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "PROPOSED, NOT RUN: cd codex-rs && just test -p codex-core --test all -E 'test(accepted_response_stream_error_acknowledges_receipt)'",
          "expected_failure": "Add this test: after a real fragment-containing wake request emit response.created plus assistant output, then close/error the stream; bound retries and inspect receipt state. Candidate is expected to retain the already-sampled lease. Cover HTTP and WebSocket/fallback as applicable; no combined dynamic execution is claimed."
        }
      ],
      "severity": "regression",
      "repeat-of": "submission-ack-after-response"
    }
  ],
  "notes": [
    "Previous merged verdict contains one finding. Its specific tool-drain case is fixed: static pre-drain assertion exit 0, exact-tree hosted regression test PASS, delta narrowing mutant sole failing test with hosted exit 100.",
    "Acceptance criteria AC1 and AC2 are exercised for normally completed HTTP, WS and fallback requests. AC3-AC5 have real retry/abort/suspension public-entry tests. AC6 has one forged-input public-entry test plus four matcher unit tests. AC7 has capped unleased remainder tests, not a tracked receipt removed from the assembled prompt.",
    "Tracked-but-omitted membership attacks: 0 executed combined integration cases, 0 supplied ack-all-tracked narrowing mutants in rev2. Request tracked_receipt_omitted_from_submitted_prompt_stays_pending and an ack-all-tracked narrowing mutant if claiming this specific bound. Static exact membership filter holds; do not count the cap-doubled mutant as proof of post-tracking omission.",
    "The taskless abort path fail_leases(..., None, ...) suppresses a warning if suspension happens without a turn context. Public repeated-abort reachability is not established, so this is a retained suspicion rather than a second blocking finding.",
    "Total change size is 1238 insertions plus 27 deletions = 1265 changed lines, above 800-line guidance. Production acknowledgment module is 213 lines and sibling matcher tests 126; largest addition is 695 integration-test lines. Prefer a separate mailbox-attempt-accounting stage if splitting, preserving acknowledgment code with its behavioral integration tests. No behavioral severity assigned solely for size.",
    "Public hidden test_runtime_notification_state probe expands codex-core API by a test-only method. No external CLI/config/app-server wire shape changed by this candidate. Rollout stores fragment text, not lease metadata; resume does not rearm trusted lease ids.",
    "Review uses local pinned source and authenticated hosted job logs; no public web research or external facts required. Local build prohibition respected. Only the assigned review task receives this outcome and lifecycle writes."
  ],
  "surface_results": [
    {
      "row": "acknowledgment point",
      "result": "broken",
      "detail": "Prior post-tool-drain regression repaired and mutation-killed. Completed-response budget accounting still returns Err before outcome-gated ack; accepted-stream cancellation/error window also remains. Static expected-red exit 1, combined dynamic tests requested and unrun. Normal HTTP/WS/fallback hosted tests pass but do not cover those windows."
    },
    {
      "row": "membership authority",
      "result": "held",
      "detail": "Pinned exec_completion_ack.rs:80 rerenders from trusted leases, matches exact user InputText and filters tracked members at :123. Hosted forged_fragment_text_acknowledges_nothing, four matcher tests, capped batches and omitted_receipt_sampled_by_later_request pass. History repetition does not retrack acknowledged leases. Held within this measured bound; tracked-after-assembly omission remains 0 combined attacks, explicitly not established."
    },
    {
      "row": "failure, retry and suspension",
      "result": "held",
      "detail": "Hosted failed_submission_retries_once_without_second_history_append, aborted_submission_retries_and_samples_once and persistent_failures_suspend_visibly_without_spin pass on exact tree. Mailbox stale-fail and exhaustion units pass; source rejects stale tokens before increment and suspends at 3. Held for genuinely failed/preacceptance-aborted submissions, not the already-sampled downstream-error case assigned to acknowledgment point. Taskless warning reachability remains unestablished."
    }
  ],
  "free_hunt": [
    {
      "area": "Transport formatting and model-visible context",
      "result": "no additional established defect",
      "detail": "client_common.rs:60 normalizes images, client.rs:1010 strips ids/content-kind metadata, and client_tool_metadata.rs:12 only bounds optional tool metadata; these do not remove exec-completion InputText. WS incremental prior-response history differs from full prompt representation, but no omission defect is demonstrated. Existing completion fragment is a ContextualUserFragment in core/context, at most 768 bytes, batches capped at 8 (6144 bytes); this candidate introduces no new unbounded rendered fragment."
    },
    {
      "area": "Resume, retry and task cleanup",
      "result": "bounded observations retained",
      "detail": "Record path deduplicates exact trusted render against all raw history; turn abort takes unrecorded pending leases and recorded tracking is separately failed. No persisted token/lease authority added. Repeated taskless suspension warning remains unknown, not declared fixed or broken by proxy."
    }
  ]
}
```

## Reproducible static probe

Save the following as `.temp/TASK-261006-10jpkf/ack-placement.rb`. Materialize
`turn.rs` using `git show ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe:codex-rs/core/src/session/turn.rs`.
The script is a literal placement/control-flow anchor check, not a Rust test.

```ruby
source = File.read(ARGV.fetch(0))
sampling_start = source.index('async fn try_run_sampling_request(')
sampling = source[sampling_start..]
ack = sampling.index('exec_completion_ack::acknowledge_submitted(')
drain = sampling.index('drain_in_flight(')
outcome = sampling.index('let outcome: CodexResult<SamplingRequestResult> = loop')
raise 'Missing source anchors' unless ack && drain && outcome
if ARGV.fetch(1) == 'pre-drain'
  puts "ack_before_drain=#{ack < drain}"
  exit(ack < drain ? 0 : 1)
end
created = sampling.index('ResponseEvent::Created {')
cancel = sampling.index('if cancellation_token.is_cancelled()', outcome)
stream_error = sampling.index('Some(Err(err)) => break Err(err)', outcome)
budget_error = sampling.index('if let Err(err) = budget_result')
raise 'Missing rejection-path anchors' unless created && cancel && stream_error && budget_error
puts "ack_before_response_loop=#{ack < outcome}"
puts "cancel_and_stream_error_before_ack=#{cancel < ack && stream_error < ack}"
puts "completed_budget_error_before_ack=#{budget_error < ack}"
exit(ack < outcome ? 0 : 1)
```
