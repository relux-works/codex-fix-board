# Recording audit and merge refusal — prompt-membership-acknowledgment, CR revision 2

Changes requested; supplied merged artifact refused for duplicate mechanisms.

Candidate: `ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe`. Checked 3/3 panel finding payloads, 19/19 notes, and 3/3 surface rows. No repository code changes.

```verdict-findings
{
  "verdict": "changes_requested",
  "recording_disposition": "merged artifact refused; correction required before named reject route",
  "findings": [
    {
      "id": "submission-ack-after-response",
      "row": "acknowledgment point",
      "invariant": "A successfully accepted sampling request containing the trusted fragment acknowledges its lease without requiring response completion or downstream response processing success.",
      "mechanism": "codex-rs/core/src/session/turn.rs:2673 handles accepted response creation without acknowledgment. The sole ack at :3150-3151 is gated by outcome.is_ok() after the response loop. Stream error/EOF at :2659-2663 or cancellation after acceptance skips it; even response.completed can encounter record_token_usage_info's budget failure at :2975-2976 before it. codex-rs/core/src/agent/control/budget.rs:12-14 returns SessionBudgetExceeded on exhaustion. tasks/mod.rs:1052 and exec_completion_ack.rs:145 fail the still-tracked sampled lease. Rev2 fixes interruption during tool drain only, not this earlier post-acceptance window.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261006-2udqqe/submission-ack-static.pl",
          "command": "perl .temp/TASK-261006-2udqqe/submission-ack-static.pl .temp/TASK-261006-2udqqe-cand/codex-rs/core/src/session/turn.rs",
          "expected_failure": "Observed exit 1, expected-red static source-placement proof: created=6225 completed=18910 stream_error=5801 budget_error=20515 outcome_gate=27864 acknowledgment=27893. No runtime consequence was executed locally. Checker source is included below.",
          "severity_scope": "static control flow, not behavioral execution"
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "Requested hosted-only: cd codex-rs && just test -p codex-core --test all -E 'test(accepted_response_interrupted_does_not_requeue_completion) | test(completed_response_budget_failure_does_not_requeue_completion)'",
          "expected_failure": "Proposed tests do not yet exist and were NOT RUN: response.created plus visible assistant output then stream interruption should leave the sampled lease gone with no completion retry; response.completed that exhausts rollout budget should also leave it gone. Current source skips ack in both error paths. A narrowing mutant requiring completed response success should fail these tests."
        },
        {
          "test_file": ".temp/TASK-261006-rn31c2/static_attacks.py",
          "command": "python3 .temp/TASK-261006-rn31c2/static_attacks.py --require-completed-ack-before-budget-error",
          "expected_failure": "Executed: exit 1, AssertionError: response.completed can exit on SessionBudgetExceeded before acknowledgment. This is an expected-red static placement check, not a Rust runtime execution."
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "cd codex-rs && just test -p codex-core --test all -E 'test(completed_response_exhausting_budget_acknowledges_completion)'",
          "expected_failure": "Requested fixture, absent and NOT run: stage a real runtime notification, complete its wake response with valid usage crossing a configured rollout budget, preserve SessionBudgetExceeded, assert the captured prompt contains the fragment and mailbox state is (false, false). Candidate instead retains an unleased sampled notification."
        },
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
      "repeat-of": "submission-ack-after-response",
      "reported_by": [
        "TASK-261006-2udqqe",
        "TASK-261006-rn31c2",
        "TASK-261006-10jpkf"
      ]
    }
  ],
  "notes": [
    "Recording-only audit: no new candidate finding, code review, build, or attack was performed. All panel finding payloads and 19 notes are preserved. All panels request changes.",
    "The supplied merge contains three entries for the same mechanism at turn.rs:3149-3151: acknowledgment gated by outcome.is_ok(). Budget failure, stream error and cancellation are symptoms of this same gate. Missing: mechanism deduplication under the existing submission-ack-after-response id, retaining all seven reproduction entries and all panel provenance.",
    "Do not record the supplied three-entry artifact through reject_cr. Orchestrator must correct the merged resource and reroute recording review. This is recoverable artifact rework, not an external blocker.",
    "Panel reproductions are static placement checks; proposed combined runtime tests remain unrun. This audit does not promote them to executed behavioral evidence."
  ],
  "surface_results": [
    {
      "row": "acknowledgment point",
      "result": "broken",
      "reason": "Positive HTTP/WS/fallback and pre-drain acknowledgment attacks hold on exact hosted candidate; ack_after_tool_drain is killed. Post-accepted-response stream/budget error paths still skip outcome-Ok acknowledgment, repeating the submission-versus-response defect.",
      "evidence": [
        "candidate turn.rs:2659,2673,2975,3150",
        "hosted 37399295391 core exec_completion tests",
        "hosted 37399313769 narrowing attack exit 100",
        "panel static attack exit 1"
      ],
      "findings": [
        "submission-ack-after-response"
      ],
      "reported_by": "TASK-261006-2udqqe"
    },
    {
      "row": "membership authority",
      "result": "held",
      "reason": "Trusted leases select members by exact rerendered InputText and user role; mailbox acknowledgment also checks lease token. Forged handle/payload/role attacks and cap-remainder later delivery pass on exact candidate; marker-substring narrowing is killed. History repetitions have no remaining tracked lease after ack. Bound: tracked-but-removed-from-prompt branch has no executed public-entry attack, and cap remainder does not prove that branch.",
      "evidence": [
        "candidate exec_completion_ack.rs:65-136",
        "candidate runtime_mailbox.rs:187-199",
        "hosted 37399295391 matcher and forged/cap tests",
        "hosted 37402888227 narrowing attack exit 100"
      ],
      "requested_attack": "Track a real recorded lease, remove only its fragment from the assembled prompt at a real supported omission boundary, submit that prompt and prove it is not acknowledged; later include it and prove one ack. Narrow filtering to acknowledge all tracked leases and require this test to fail.",
      "reported_by": "TASK-261006-2udqqe"
    },
    {
      "row": "failure, retry and suspension",
      "result": "held",
      "reason": "For genuinely failed/unaccepted submissions, fail-unsubmitted and pending-input abort handling return current leases, exact history scan avoids second append, fail counts only a matching current token and suspends on attempt 3. Hosted retry/abort/exhaustion tests assert counts and silence; doubled-threshold narrowing fails. Already-accepted submission misclassification is assigned once to acknowledgment point, not duplicated here. Taskless-abort visible-warning reachability remains unproved.",
      "evidence": [
        "candidate hook_runtime.rs:778-806",
        "candidate runtime_mailbox.rs:207-233",
        "candidate tasks/mod.rs:563-599,641-665,738-739,1052",
        "hosted 37399295391 retry/abort/suspension tests",
        "hosted 37399486308 narrowing attack exit 100"
      ],
      "reported_by": "TASK-261006-2udqqe"
    }
  ]
}
```

Logbook: 2026-10-06 — recording audit preserves panel evidence and refuses duplicate class recording; task returned for merged-artifact correction.
