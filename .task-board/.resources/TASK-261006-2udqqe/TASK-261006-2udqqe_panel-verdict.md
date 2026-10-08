# Panel A — CR-TASK-260929-34a6ls-2, revision 2

changes_requested

## Scope and replay

Read-only, non-recording panel for TASK-261006-2udqqe. No source edits, builds, tests, commits, branch changes, or writes to TASK-260929-34a6ls. All local scratch is inside the run worktree; the sole attached text outcome is copied into board-managed storage by the resource CLI. The run write boundary takes precedence over the generic request to create the input file outside the worktree.

Temporary-index replay of base `4a27941d383ba8cdc2575bafdfeeef497b402a25` plus `TASK-260929-34a6ls_change-request_rev2.patch` produced exactly `ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe`, the expected candidate tree. Candidate inspection uses that tree, not the Story checkout's current source. No nested worktree was made.

Bounded plan: decide whether this revision satisfies the three supplied surface rows; frozen precondition is the exact patch/base/tree triple above, not a new grammar; worker budget 60 minutes, one text outcome, no archives, zero additional research prerequisites; exit after replay, one result per row, bounded free hunt, and panel verdict. No unrelated implementation or workflow repair.

## Commands and actual exit codes

Commands below were executed by this panel unless explicitly marked hosted. Local build/test execution: **0 commands**.

| Command / operation | Exit | Evidence |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261006-2udqqe, status=analysis)'` | 0 | Panel lifecycle only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-2udqqe-replay.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Temporary index initialized |
| `task-board resource get TASK-260929-34a6ls TASK-260929-34a6ls_change-request_rev2.patch --output .temp/TASK-260929-34a6ls_change-request_rev2.patch` | 0 | Patch materialized read-only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-2udqqe-replay.idx" git apply --cached .temp/TASK-260929-34a6ls_change-request_rev2.patch` | 0 | Patch replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-2udqqe-replay.idx" git write-tree` | 0 | Exact expected tree above |
| `git rev-parse 292d2959^{tree}` | 0 | Hosted snapshot tree equals candidate |
| `git diff --check 4a27941d383ba8cdc2575bafdfeeef497b402a25 ebc9a73b3447d8f2bd27aacb9fdd375575ca0ebe` | 0 | Whitespace check only |
| `perl .temp/TASK-261006-2udqqe/submission-ack-static.pl .temp/TASK-261006-2udqqe-cand/codex-rs/core/src/session/turn.rs` | **1** | Expected-red source-order attack; NOT a passing gate or a dynamic reproduction |
| `python3 .temp/TASK-261006-2udqqe/validate-outcome.py` | 0 | One JSON object, one-word verdict, 3/3 unique surface rows, required finding/reproduction fields |
| `gh api repos/relux-works/codex/actions/runs/37399295391` and `/jobs` | 0 each | Provider run and job metadata |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/112062620620/logs` | 0 | Exact-snapshot core log |
| `gh api repos/relux-works/codex/actions/runs/{37399313769,37402888227,37399486308}/jobs` (three separate requests) | 0 each | Mutant job metadata |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/{112062681244,112073812151,112063238746}/logs` (three separate requests) | 0 each | Three mutant logs |

Successful supporting reads: resource downloads for `surface-table.md`, `producer-brief.md`, results, mutants, revision-1 verdict, revision-2 validation log all returned 0; compact AC/checklist/schema queries, Git source/stat/diff reads, source extraction and sanitized log inspection returned 0 at their shell-call boundary. These are reads, not behavioral gates. Readiness outputs are in `.temp/TASK-261006-2udqqe/{readiness,hosted-readiness,perl-readiness}.log`.

Exploratory failures are not hidden: queries using unsupported `resources` or `resource` projections returned 1; the attempted positional `schema(element)` returned a schema-error JSON envelope (shell exit 0); the wrong candidate path `core/src/client/tool_metadata.rs` returned Git exit 128 and was corrected to `core/src/client_tool_metadata.rs`; a raw hosted-log download without `--allow-escape-sequences` returned 1 and the explicit retry returned 0. The initial combined `rm -f`/read-tree invocation was rejected before process creation (no shell exit code), so read-tree was run separately without deletion. No failed read is treated as evidence of absence.

## Hosted execution actually reused

Provider metadata for run **37399295391** reports core, lint, small and app-server jobs `success`. Its workflow `head_sha` is the base, NOT the snapshot: the core log explicitly checks out `292d295900ec86e6026e565983a79952f102f0b6`; `git rev-parse 292d2959^{tree}` independently gives the exact candidate tree. Core job **112062620620** ran `INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-core -E 'not ( test(=suite::skill_approval::shell_zsh_fork_skill_scripts_ignore_declared_permissions) | test(=suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_guardian_reviews_persistent_terminal_in_current_turn) | test(=suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_parent_approval_preserves_denied_reads))'`: successful hosted step (exit 0), **4982 passed, 11 skipped**, including 12/12 `suite::exec_completion` cases. This is accepted hosted evidence, not locally rerun evidence; excluded/skipped tests are not counted as passing.

Independently downloaded mutant logs establish these expected-red executions (hosted step exit **100**, not 0):

| Run / core job | Snapshot checked out | Attack and observed failure |
| --- | --- | --- |
| 37399313769 / 112062681244 | `d05461ec3e7ee15fb25eedbe3b5d274705d2423e` | `ack_after_tool_drain`: `completed_response_with_blocked_tool_acknowledges_before_interrupt` fails; only that test remains failed in the terminal summary |
| 37402888227 / 112073812151 | `2fc7c9d6bdc4592ad9710de103f785a217fb2e64` | `marker_substring_membership`: forged handle, altered payload and forged-text integration fail; final summary ALSO fails both `nine_pending_completions_sample_in_capped_batches_without_loss` and `omitted_receipt_sampled_by_later_request` |
| 37399486308 / 112063238746 | `de75ab136c15eb3b1f1a9bc05dfc0091d6cbbda2` | `suspend_threshold_doubled`: both exhaustion and stale-fail unit tests fail |

Git diffs against snapshot 292d2959 show only the intended files change for these three runs: `turn.rs`, `exec_completion_ack.rs`, and `runtime_mailbox.rs`, respectively. Thus these are candidate-derived narrowing attacks, not arbitrary failures. The other six mutant executions are reported by the producer results; this panel has NOT independently downloaded their logs and does NOT present the aggregate 9/9 as independently measured.

Local CR validation resource records target guard, fmt-check, clippy and small-crate suite exit 0, with `coverage_unit=exact_command_shard required=4 green=4 failed=0 missing=0 test_case_coverage=unknown`. It is bounded/truncated and does not independently establish core behavior. The hosted core log supplies the relevant execution evidence.

## Finding and recommendation

Revision 2 genuinely repairs the completed-response/tool-drain interruption slice of `submission-ack-after-response`; the exact-tree regression test and narrowing mutant demonstrate that slice. It still uses `outcome.is_ok()` at `core/src/session/turn.rs:3150` as its sampling receipt, after the response loop. An accepted `ResponseEvent::Created` at :2673 only stores the response id. Subsequent stream error/EOF at :2659/:2660 or interrupt yields an error and skips acknowledgment even though the request already reached the model. A completed response can likewise hit the post-completion budget error at :2975 before acknowledgment. `agent/control/budget.rs:12` concretely returns `SessionBudgetExceeded` for exhausted budget; this is not an imaginary error branch. The abort/end paths then fail the still-tracked lease (:1052 in `tasks/mod.rs`; `exec_completion_ack.rs:145`), so an already sampled fragment is treated as unsampled and can be re-offered (ordinary stream failure/interruption) or retained/suspended (budget termination).

Move membership acknowledgment to a trustworthy transport-acceptance boundary independent of response completion, response processing and tool drain; do not solve this by acknowledging before transport acceptance. Request two public-entry regressions: accepted response.created/assistant-output followed by disconnect or interrupt, and response.completed whose usage exhausts the rollout budget. Assert prompt membership, mailbox acknowledgment, and no completion-specific retry wake. Existing delayed-HTTP abort test waits before the response body is available, so it does not exercise accepted-response interruption. These new dynamic attacks are **requested and unrun**, not claimed executed.

## Logbook entry (task-scoped; no control-root edit)

2026-10-06, TASK-261006-2udqqe: exact rev2 replay passed; completed-response/tool-drain regression is repaired, but acknowledgment still depends on response-success/budget handling rather than accepted submission. Repeated finding is routed in this outcome only, never written to the reviewed task. Producer's marker-substring mutant killer list omits two additional final failures present in the independently downloaded log; the mutant is killed nonetheless. Membership tracked-but-prompt-omitted execution remains unmeasured (cap remainder is unleased, a different case).

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
          "severity_scope": "static control flow, not behavioral execution"
        },
        {
          "test_file": "codex-rs/core/tests/suite/exec_completion.rs",
          "command": "Requested hosted-only: cd codex-rs && just test -p codex-core --test all -E 'test(accepted_response_interrupted_does_not_requeue_completion) | test(completed_response_budget_failure_does_not_requeue_completion)'",
          "expected_failure": "Proposed tests do not yet exist and were NOT RUN: response.created plus visible assistant output then stream interruption should leave the sampled lease gone with no completion retry; response.completed that exhausts rollout budget should also leave it gone. Current source skips ack in both error paths. A narrowing mutant requiring completed response success should fail these tests."
        }
      ],
      "severity": "regression",
      "repeat-of": "submission-ack-after-response"
    }
  ],
  "notes": [
    "No local cargo/just/build/test command and no reviewed-task mutation. Only the panel task lifecycle/resources/checklist/handoff are written.",
    "All three supplied surface rows have exactly one result: 2 held within stated bounds, 1 broken. Held does not certify unexecuted attack families.",
    "Hosted base evidence independently checked: exact snapshot candidate tree, 12/12 exec-completion integration cases passed. Three narrowing executions independently inspected; all expected-red hosted exit 100. Other six mutant logs not independently inspected.",
    "Cap omission tests omit before leasing, not a tracked receipt subsequently removed from assembled input. Tracked-but-omitted acknowledgment refusal has 0 public-entry executions established by this review; producer discloses this bound.",
    "Marker-substring mutant terminal summary includes two additional batch/remainder failures omitted from producer's killer table; no inference of a surviving mutant or green failed gate.",
    "This panel follows the supplied non-recording scope; no GitHub review/acceptance or producer lifecycle action is performed."
  ],
  "surface_results": [
    {
      "row": "acknowledgment point",
      "result": "broken",
      "reason": "Positive HTTP/WS/fallback and pre-drain acknowledgment attacks hold on exact hosted candidate; ack_after_tool_drain is killed. Post-accepted-response stream/budget error paths still skip outcome-Ok acknowledgment, repeating the submission-versus-response defect.",
      "evidence": ["candidate turn.rs:2659,2673,2975,3150", "hosted 37399295391 core exec_completion tests", "hosted 37399313769 narrowing attack exit 100", "panel static attack exit 1"],
      "findings": ["submission-ack-after-response"]
    },
    {
      "row": "membership authority",
      "result": "held",
      "reason": "Trusted leases select members by exact rerendered InputText and user role; mailbox acknowledgment also checks lease token. Forged handle/payload/role attacks and cap-remainder later delivery pass on exact candidate; marker-substring narrowing is killed. History repetitions have no remaining tracked lease after ack. Bound: tracked-but-removed-from-prompt branch has no executed public-entry attack, and cap remainder does not prove that branch.",
      "evidence": ["candidate exec_completion_ack.rs:65-136", "candidate runtime_mailbox.rs:187-199", "hosted 37399295391 matcher and forged/cap tests", "hosted 37402888227 narrowing attack exit 100"],
      "requested_attack": "Track a real recorded lease, remove only its fragment from the assembled prompt at a real supported omission boundary, submit that prompt and prove it is not acknowledged; later include it and prove one ack. Narrow filtering to acknowledge all tracked leases and require this test to fail."
    },
    {
      "row": "failure, retry and suspension",
      "result": "held",
      "reason": "For genuinely failed/unaccepted submissions, fail-unsubmitted and pending-input abort handling return current leases, exact history scan avoids second append, fail counts only a matching current token and suspends on attempt 3. Hosted retry/abort/exhaustion tests assert counts and silence; doubled-threshold narrowing fails. Already-accepted submission misclassification is assigned once to acknowledgment point, not duplicated here. Taskless-abort visible-warning reachability remains unproved.",
      "evidence": ["candidate hook_runtime.rs:778-806", "candidate runtime_mailbox.rs:207-233", "candidate tasks/mod.rs:563-599,641-665,738-739,1052", "hosted 37399295391 retry/abort/suspension tests", "hosted 37399486308 narrowing attack exit 100"]
    }
  ],
  "free_hunt": [
    {"area": "post-completion quota accounting", "result": "broken", "finding": "submission-ack-after-response", "evidence": "turn.rs:2959-2976 and agent/control/budget.rs:12-14; folded into the same acknowledgment-class finding, not a duplicate"},
    {"area": "wire prompt transformations", "result": "held", "evidence": "client.rs:1010 strips ids/content kinds; client_tool_metadata.rs:12 sheds optional executed-tool metadata while preserving ordinary fragment content. No concrete content-removal bypass identified. WebSocket incremental history is not treated as duplicate delivery."},
    {"area": "external compatibility and context bounds", "result": "held", "evidence": "No config/CLI/app-server/serialized rollout receipt schema change in the 11-path delta; existing bounded ExecCompletionFragment and 8-entry per-wake cap remain. No unbounded new model-context item identified."},
    {"area": "size/API and taskless abort visibility", "result": "note", "evidence": "1238 insertions plus 27 deletions exceed 800-line guidance, though 871 added lines are tests; public doc-hidden test_runtime_notification_state expands core API. fail_leases with no TurnContext suppresses warning at exec_completion_ack.rs:188; a repeated public-entry taskless-abort reproduction was not established. These are not claimed reproduced runtime regressions."}
  ]
}
```

## Static checker source

This is a source-order refusal probe, not an execution of Rust or a replacement for the requested hosted tests. Reads the extracted exact-tree `turn.rs`; exits 1 for the observed delayed/error-gated arrangement:

    use strict;
    use warnings;
    local $/;
    open my $source, '<', $ARGV[0] or die "open: $!";
    my $text = <$source>;
    my $start = index($text, 'async fn try_run_sampling_request(');
    die "sampling function absent\n" if $start < 0;
    my $body = substr($text, $start);
    my $created = index($body, 'ResponseEvent::Created { response_id }');
    my $completed = index($body, 'ResponseEvent::Completed {');
    my $ack = index($body, 'exec_completion_ack::acknowledge_submitted(');
    my $error = index($body, 'Some(Err(err)) => break Err(err)');
    my $budget = index($body, 'if let Err(err) = budget_result');
    my $gated = index($body, 'if outcome.is_ok()');
    die "required landmarks absent\n" if grep { $_ < 0 } ($created, $completed, $ack, $error, $budget, $gated);
    print "created=$created completed=$completed stream_error=$error budget_error=$budget outcome_gate=$gated acknowledgment=$ack\n";
    if ($created < $completed && $completed < $budget && $budget < $gated && $gated < $ack && $error < $ack) {
        print "FAIL: no acknowledgment at accepted-response creation; post-acceptance stream/budget errors bypass the outcome-Ok acknowledgment. Static placement proof only, not a runtime reproduction.\n";
        exit 1;
    }
    print "Source ordering differs; manually re-evaluate.\n";
    exit 0;
