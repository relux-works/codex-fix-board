# Merged review verdict — TASK-260929-34a6ls CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261006-iufewn_panel-verdict.md` (changes_requested), `TASK-261006-1xq7fq_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "submission-ack-after-response",
      "row": "acknowledgment point",
      "invariant": "A successfully submitted sampling request containing the trusted fragment acknowledges its lease without waiting for response completion or downstream tool completion.",
      "mechanism": "codex-rs/core/src/session/turn.rs:1694 acknowledges only after try_run_sampling_request succeeds; response completion at :2939 is followed by tool draining at :3153 and cancellation at :3164, so an already completed request can return TurnAborted and tasks/mod.rs:1052 requeues its sampled lease.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261006-iufewn/post-response-ack-static.pl",
          "command": "perl .temp/TASK-261006-iufewn/post-response-ack-static.pl .temp/TASK-261006-iufewn/turn.rs",
          "expected_failure": "Exit 1: acknowledgment before tool drain is ABSENT. Static source-placement reproduction only; post-response tool-abort integration execution remains requested and unrun.",
          "pinned_blobs": [
            "git:3881bd360a91af35034ede176702ba087687647d",
            "git:bd96e25bfbe16af4d877d67736956e911613b01e"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261006-iufewn"
      ]
    }
  ],
  "notes": [
    "[TASK-261006-iufewn] Tracked-but-omitted prompt membership has zero integration attacks; capped unleased remainders do not kill ack_all_tracked. Producer disclosed the bound.",
    "[TASK-261006-iufewn] Hosted workflow head is the base commit; independently verified snapshot checkout and snapshot tree before reusing execution evidence.",
    "[TASK-261006-iufewn] No local build or behavioral test execution. Blocking finding is static control-flow/placement evidence, not a claimed dynamic reproduction.",
    "[TASK-261006-iufewn] Change size is 1159 lines and public test-only probe enlarges core API; not classified as reproduced behavior defects.",
    "[TASK-261006-iufewn] Taskless-abort suspension can lack a warning; repeated public-entry reachability was not established, so this remains a suspicion.",
    "[TASK-261006-1xq7fq] {'id': 'ack-delayed-through-tool-drain', 'row': 'acknowledgment point', 'severity': 'note', 'mechanism': 'codex-rs/core/src/session/turn.rs:1698 acknowledges only after try_run_sampling_request returns Ok. That callee obtains the transport stream at 2567, consumes ResponseEvent::Completed at 2939, then drains in-flight tool futures at 3153 and checks cancellation at 3164 before returning. Even a completed sampling response can therefore remain unacknowledged while a tool waits; an interrupt there returns TurnAborted, and codex-rs/core/src/tasks/mod.rs:1052 calls fail_unsubmitted. A post-created stream error similarly returns before the acknowledgment hook. The source ordering is verified; an execution demonstrating its receipt/wake consequences is not available in the supplied attacks.', 'requested_attack': {'test_file': 'codex-rs/core/tests/suite/exec_completion.rs', 'test_name': 'completed_response_with_blocked_tool_acknowledges_before_interrupt', 'command': \"cd codex-rs && just test -p codex-core --test all -E 'test(completed_response_with_blocked_tool_acknowledges_before_interrupt)'\", 'scenario': 'Enqueue a real completion, submit its wake prompt, emit a function call and response.completed, keep the tool awaiting approval, inspect notification state before interrupt, then interrupt and assert no completion retry wake. Assert the captured request contains the trusted fragment.', 'expected_failure': 'Candidate is expected to retain the leased notification until tool drain and to re-offer it on interrupt, contrary to acknowledgment at successful submission. This proposed test does not exist yet and was NOT run. Also request a response.created/output-then-stream-error variant to clarify submission versus response-completion semantics.'}, 'repeat-of': 'none'}",
    "[TASK-261006-1xq7fq] {'id': 'tracked-omission-not-executed', 'row': 'membership authority', 'severity': 'note', 'mechanism': 'The supplied batch-cap test omits the ninth receipt before leasing/recording, not a receipt already tracked by PendingExecCompletionAcks but removed from the assembled prompt. The replaced ack_all_tracked mutant could survive that test. Exact matcher code filters members correctly on static inspection, but its integration-level tracked-omission refusal is not measured by the current 8/8 kill ratio.', 'requested_attack': {'test_file': 'codex-rs/core/tests/suite/exec_completion.rs', 'test_name': 'tracked_receipt_omitted_from_submitted_prompt_stays_pending', 'command': \"cd codex-rs && just test -p codex-core --test all -E 'test(tracked_receipt_omitted_from_submitted_prompt_stays_pending)'\", 'scenario': 'Use a real final-prompt omission path after tracking, assert the exact submitted request lacks that receipt, assert the lease is not acknowledged, then include it on a later request. Narrow acknowledge_submitted to acknowledge every tracked id and require this public-entry test to fail.', 'expected_failure': 'The ack-all-tracked mutant should clear the omitted real lease; the exact candidate should retain it. Neither this proposed fixture nor mutant was run in this panel; compaction/guardian behavior is a stated producer bound, not silently covered.'}, 'repeat-of': 'none'}",
    "[TASK-261006-1xq7fq] {'id': 'change-size-over-review-guidance', 'severity': 'note', 'mechanism': 'git diff --stat reports 1,132 insertions and 27 deletions across 11 paths: 1,159 changed lines, above the 800-line nonmechanical guidance. The new 212-line acknowledgment module and 126-line sibling tests are small individually; 596 integration-test additions are the largest component. A coherent split could first land mailbox attempt/suspension accounting with its existing and new mailbox tests, then land turn-level acknowledgment, abort/dedup wiring, and the transport integration tests together. Do not split acknowledgment production changes away from their behavioral tests merely to hit the numeric threshold.', 'repeat-of': 'none'}"
  ],
  "surface_results": [
    {
      "row": "acknowledgment point",
      "result": "broken",
      "detail": "Executed expected-red static post-response/tool-drain placement assertion; exact-tree hosted existing submission tests do not cover this later-abort window.",
      "reported_by": "TASK-261006-iufewn"
    },
    {
      "row": "membership authority",
      "result": "held",
      "detail": "Exact-tree hosted forged-user-input and batch-cap public-entry attacks pass; attached role/payload narrowing attacks kill their mutants. Tracked omission remains explicitly untested.",
      "reported_by": "TASK-261006-iufewn"
    },
    {
      "row": "failure, retry and suspension",
      "result": "held",
      "detail": "Exact-tree hosted pre-submit retry/abort, no-second-append, warning/request-count attacks pass; stale-token and threshold narrowing mutant evidence reused.",
      "reported_by": "TASK-261006-iufewn"
    }
  ],
  "free_hunt": []
}
```
