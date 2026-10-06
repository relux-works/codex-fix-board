# Merged review verdict — TASK-260929-34a6ls CR revision 2 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261006-2udqqe_panel-verdict.md` (changes_requested), `TASK-261006-rn31c2_panel-verdict.md` (changes_requested), `TASK-261006-10jpkf_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
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
          "severity_scope": "static control flow, not behavioral execution",
          "pinned_blobs": [
            "git-blob:3dc0b7f1d9c7385ed549ada025254477c45f8928",
            "git-blob:aeead7d7d9c48741b375ec378ea550e1ba97f315"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "Requested hosted-only: cd codex-rs && just test -p codex-core --test all -E 'test(accepted_response_interrupted_does_not_requeue_completion) | test(completed_response_budget_failure_does_not_requeue_completion)'",
          "expected_failure": "Proposed tests do not yet exist and were NOT RUN: response.created plus visible assistant output then stream interruption should leave the sampled lease gone with no completion retry; response.completed that exhausts rollout budget should also leave it gone. Current source skips ack in both error paths. A narrowing mutant requiring completed response success should fail these tests.",
          "pinned_blobs": [
            "git-blob:3dc0b7f1d9c7385ed549ada025254477c45f8928",
            "git-blob:aeead7d7d9c48741b375ec378ea550e1ba97f315",
            "git-blob:180eb3b53317d5677758ee862b856250bb0a3fb4"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "submission-ack-after-response",
      "reported_by": [
        "TASK-261006-2udqqe"
      ]
    },
    {
      "id": "completed-budget-error-skips-ack",
      "row": "acknowledgment point",
      "invariant": "A successfully submitted prompt containing the trusted fragment acknowledges its lease even if later response bookkeeping terminates the turn.",
      "mechanism": "Candidate turn.rs:2966-2976 performs fallible budget accounting after observing response.completed, but turn.rs:3149 gates acknowledgment on outcome.is_ok(). LocalAgentControl::record_rollout_budget_usage at agent/control/budget.rs:13-14 returns SessionBudgetExceeded for normal exhaustion. The resulting Err skips acknowledgment; tasks/mod.rs:739 fails the tracked lease back to unleased. Static branch verified on the exact candidate; combined runtime scenario not run.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261006-rn31c2/static_attacks.py",
          "command": "python3 .temp/TASK-261006-rn31c2/static_attacks.py --require-completed-ack-before-budget-error",
          "expected_failure": "Executed: exit 1, AssertionError: response.completed can exit on SessionBudgetExceeded before acknowledgment. This is an expected-red static placement check, not a Rust runtime execution.",
          "pinned_blobs": [
            "git-blob:aeead7d7d9c48741b375ec378ea550e1ba97f315"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "cd codex-rs && just test -p codex-core --test all -E 'test(completed_response_exhausting_budget_acknowledges_completion)'",
          "expected_failure": "Requested fixture, absent and NOT run: stage a real runtime notification, complete its wake response with valid usage crossing a configured rollout budget, preserve SessionBudgetExceeded, assert the captured prompt contains the fragment and mailbox state is (false, false). Candidate instead retains an unleased sampled notification.",
          "pinned_blobs": [
            "git-blob:180eb3b53317d5677758ee862b856250bb0a3fb4"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "submission-ack-after-response",
      "reported_by": [
        "TASK-261006-rn31c2"
      ]
    },
    {
      "id": "submission-ack-still-gated-by-response-outcome",
      "row": "acknowledgment point",
      "invariant": "A successfully submitted request containing a trusted completion acknowledges that lease independently of subsequent response-processing, budget-accounting, tool-drain, or cancellation errors.",
      "mechanism": "Candidate codex-rs/core/src/session/turn.rs:3150 still gates acknowledgment on outcome.is_ok(). ResponseEvent::Completed at :2936 runs token/budget accounting at :2967 and breaks Err at :2975 before reaching that hook. Real SessionBudgetExceeded is propagated through session/mod.rs:4805 and session/rollout_budget.rs:34; tasks/mod.rs:739 fails the still-tracked already-sampled lease. Additionally cancellation/stream errors at turn.rs:2632/:2659 after Created/output bypass the same hook. The old post-tool-drain window is fixed, but downstream response success still decides submission acknowledgment.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261006-10jpkf/ack-placement.rb",
          "command": "ruby .temp/TASK-261006-10jpkf/ack-placement.rb .temp/TASK-261006-10jpkf/turn.rs submission",
          "expected_failure": "Observed exit 1, expected-red static source-placement assertion: ack_before_response_loop=false; cancel_and_stream_error_before_ack=true; completed_budget_error_before_ack=true. Not a dynamic receipt reproduction. Probe source is included below for reproducibility.",
          "pinned_blobs": [
            "git-blob:aeead7d7d9c48741b375ec378ea550e1ba97f315"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "PROPOSED, NOT RUN: cd codex-rs && just test -p codex-core --test all -E 'test(completed_response_budget_exhaustion_acknowledges_receipt)'",
          "expected_failure": "Add this test using build_with_auto_env and a real queued completion: complete the wake response with usage that exhausts the rollout budget; wait for SessionBudgetExceeded and TurnComplete; assert captured wake contains the trusted fragment and mailbox is (false,false). Candidate is expected to retain/requeue it because budget error bypasses ack. Test does not exist in the candidate and was not executed.",
          "pinned_blobs": [
            "git-blob:aeead7d7d9c48741b375ec378ea550e1ba97f315",
            "git-blob:180eb3b53317d5677758ee862b856250bb0a3fb4"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "PROPOSED, NOT RUN: cd codex-rs && just test -p codex-core --test all -E 'test(accepted_response_stream_error_acknowledges_receipt)'",
          "expected_failure": "Add this test: after a real fragment-containing wake request emit response.created plus assistant output, then close/error the stream; bound retries and inspect receipt state. Candidate is expected to retain the already-sampled lease. Cover HTTP and WebSocket/fallback as applicable; no combined dynamic execution is claimed.",
          "pinned_blobs": [
            "git-blob:aeead7d7d9c48741b375ec378ea550e1ba97f315",
            "git-blob:180eb3b53317d5677758ee862b856250bb0a3fb4"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "submission-ack-after-response",
      "reported_by": [
        "TASK-261006-10jpkf"
      ]
    }
  ],
  "notes": [
    "[TASK-261006-2udqqe] No local cargo/just/build/test command and no reviewed-task mutation. Only the panel task lifecycle/resources/checklist/handoff are written.",
    "[TASK-261006-2udqqe] All three supplied surface rows have exactly one result: 2 held within stated bounds, 1 broken. Held does not certify unexecuted attack families.",
    "[TASK-261006-2udqqe] Hosted base evidence independently checked: exact snapshot candidate tree, 12/12 exec-completion integration cases passed. Three narrowing executions independently inspected; all expected-red hosted exit 100. Other six mutant logs not independently inspected.",
    "[TASK-261006-2udqqe] Cap omission tests omit before leasing, not a tracked receipt subsequently removed from assembled input. Tracked-but-omitted acknowledgment refusal has 0 public-entry executions established by this review; producer discloses this bound.",
    "[TASK-261006-2udqqe] Marker-substring mutant terminal summary includes two additional batch/remainder failures omitted from producer's killer table; no inference of a surviving mutant or green failed gate.",
    "[TASK-261006-2udqqe] This panel follows the supplied non-recording scope; no GitHub review/acceptance or producer lifecycle action is performed.",
    "[TASK-261006-rn31c2] Exactly 3/3 required surface rows swept; one broken, two held within the stated execution bounds.",
    "[TASK-261006-rn31c2] Revision-2 tool-drain repair is verified by exact-tree hosted PASS and attached ack_after_tool_drain kill, but does not eliminate the completed-response budget-error branch.",
    "[TASK-261006-rn31c2] Hosted 9/9 mutant kill ratio is the attached precheck-4 claim, not coverage of every conceivable path; individual mutant logs were not reread here.",
    "[TASK-261006-rn31c2] Membership tracked-omission bound persists from rev1: cap fixtures omit receipts before leasing, not already-tracked receipts cut from the final prompt. Request tracked_receipt_omitted_from_submitted_prompt_stays_pending plus ack_all_tracked mutant; neither ran. Exact matcher statically filters correctly, so this is a coverage note, not a proven defect.",
    "[TASK-261006-rn31c2] Stream failure after response.created/output but before response.completed is outside the supplied positive-completion tests. Request response_created_then_stream_error_receipt_policy to pin the submission-versus-completion contract; no speculative duplicate-delivery result is asserted.",
    "[TASK-261006-rn31c2] No writes on TASK-260929-34a6ls. Logbook-relevant remaining budget-error branch is recorded in this task-scoped outcome instead of editing control-root LOGBOOK.md.",
    "[TASK-261006-10jpkf] Previous merged verdict contains one finding. Its specific tool-drain case is fixed: static pre-drain assertion exit 0, exact-tree hosted regression test PASS, delta narrowing mutant sole failing test with hosted exit 100.",
    "[TASK-261006-10jpkf] Acceptance criteria AC1 and AC2 are exercised for normally completed HTTP, WS and fallback requests. AC3-AC5 have real retry/abort/suspension public-entry tests. AC6 has one forged-input public-entry test plus four matcher unit tests. AC7 has capped unleased remainder tests, not a tracked receipt removed from the assembled prompt.",
    "[TASK-261006-10jpkf] Tracked-but-omitted membership attacks: 0 executed combined integration cases, 0 supplied ack-all-tracked narrowing mutants in rev2. Request tracked_receipt_omitted_from_submitted_prompt_stays_pending and an ack-all-tracked narrowing mutant if claiming this specific bound. Static exact membership filter holds; do not count the cap-doubled mutant as proof of post-tracking omission.",
    "[TASK-261006-10jpkf] The taskless abort path fail_leases(..., None, ...) suppresses a warning if suspension happens without a turn context. Public repeated-abort reachability is not established, so this is a retained suspicion rather than a second blocking finding.",
    "[TASK-261006-10jpkf] Total change size is 1238 insertions plus 27 deletions = 1265 changed lines, above 800-line guidance. Production acknowledgment module is 213 lines and sibling matcher tests 126; largest addition is 695 integration-test lines. Prefer a separate mailbox-attempt-accounting stage if splitting, preserving acknowledgment code with its behavioral integration tests. No behavioral severity assigned solely for size.",
    "[TASK-261006-10jpkf] Public hidden test_runtime_notification_state probe expands codex-core API by a test-only method. No external CLI/config/app-server wire shape changed by this candidate. Rollout stores fragment text, not lease metadata; resume does not rearm trusted lease ids.",
    "[TASK-261006-10jpkf] Review uses local pinned source and authenticated hosted job logs; no public web research or external facts required. Local build prohibition respected. Only the assigned review task receives this outcome and lifecycle writes."
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
  ],
  "free_hunt": [
    "{\"area\": \"post-completion quota accounting\", \"result\": \"broken\", \"finding\": \"submission-ack-after-response\", \"evidence\": \"turn.rs:2959-2976 and agent/control/budget.rs:12-14; folded into the same acknowledgment-class finding, not a duplicate\", \"reported_by\": \"TASK-261006-2udqqe\"}",
    "{\"area\": \"wire prompt transformations\", \"result\": \"held\", \"evidence\": \"client.rs:1010 strips ids/content kinds; client_tool_metadata.rs:12 sheds optional executed-tool metadata while preserving ordinary fragment content. No concrete content-removal bypass identified. WebSocket incremental history is not treated as duplicate delivery.\", \"reported_by\": \"TASK-261006-2udqqe\"}",
    "{\"area\": \"external compatibility and context bounds\", \"result\": \"held\", \"evidence\": \"No config/CLI/app-server/serialized rollout receipt schema change in the 11-path delta; existing bounded ExecCompletionFragment and 8-entry per-wake cap remain. No unbounded new model-context item identified.\", \"reported_by\": \"TASK-261006-2udqqe\"}",
    "{\"area\": \"size/API and taskless abort visibility\", \"result\": \"note\", \"evidence\": \"1238 insertions plus 27 deletions exceed 800-line guidance, though 871 added lines are tests; public doc-hidden test_runtime_notification_state expands core API. fail_leases with no TurnContext suppresses warning at exec_completion_ack.rs:188; a repeated public-entry taskless-abort reproduction was not established. These are not claimed reproduced runtime regressions.\", \"reported_by\": \"TASK-261006-2udqqe\"}",
    "{\"result\": \"note\", \"detail\": \"Change-size guidance remains exceeded: 1238 insertions + 27 deletions = 1265 changed lines across 11 files; 695 integration-test additions dominate. Smallest coherent split: mailbox fail/suspend accounting with its tests, then acknowledgment/abort/dedup wiring with corresponding integration tests. Do not separate behavioral tests from the implementation just to meet the numeric threshold.\", \"repeat-of\": \"change-size-over-review-guidance\", \"reported_by\": \"TASK-261006-rn31c2\"}",
    "{\"result\": \"held\", \"detail\": \"No changed external app-server schema, CLI flags, config type, dependency, or rollout wire shape. Runtime lease metadata remains turn-local and does not persist or rearm on resume; hosted resume-silence test PASS. Fragment size is unchanged, bounded by pre-existing renderer; no new unbounded model-visible item introduced. Test-only public probe expands crate surface but follows adjacent existing CodexThread test hooks.\", \"reported_by\": \"TASK-261006-rn31c2\"}",
    "{\"area\": \"Transport formatting and model-visible context\", \"result\": \"no additional established defect\", \"detail\": \"client_common.rs:60 normalizes images, client.rs:1010 strips ids/content-kind metadata, and client_tool_metadata.rs:12 only bounds optional tool metadata; these do not remove exec-completion InputText. WS incremental prior-response history differs from full prompt representation, but no omission defect is demonstrated. Existing completion fragment is a ContextualUserFragment in core/context, at most 768 bytes, batches capped at 8 (6144 bytes); this candidate introduces no new unbounded rendered fragment.\", \"reported_by\": \"TASK-261006-10jpkf\"}",
    "{\"area\": \"Resume, retry and task cleanup\", \"result\": \"bounded observations retained\", \"detail\": \"Record path deduplicates exact trusted render against all raw history; turn abort takes unrecorded pending leases and recorded tracking is separately failed. No persisted token/lease authority added. Repeated taskless suspension warning remains unknown, not declared fixed or broken by proxy.\", \"reported_by\": \"TASK-261006-10jpkf\"}"
  ]
}
```
