# R141 panel A — CR-TASK-260929-34a6ls-1 revision 1

changes_requested

## Scope and replay

Non-recording, read-only source review. Nothing was written to TASK-260929-34a6ls; no source files were edited, no branch operations performed, and no build or Rust test executed. Only TASK-261006-iufewn receives this outcome and handoff. Scratch and the upload source remain inside the run worktree, following the explicit run write boundary; the attached resource is the durable handoff.

Decision: whether this exact CR implements sampling acknowledgment, not response-completion acknowledgment. Frozen precondition: base `4a27941d383ba8cdc2575bafdfeeef497b402a25`, candidate tree `8e03a0e18d68ac6891de673dd8d55bf0dce5c30e`, and the three supplied surface rows. Budget: one bounded static sweep plus a short free hunt, one text outcome, no serial prerequisite or new implementation.

Temporary-index replay produced **exactly** `8e03a0e18d68ac6891de673dd8d55bf0dce5c30e`. `git read-tree`, `git apply --cached`, and `git write-tree` each exited **0**. Review reads use the candidate tree, not the worktree HEAD.

## Commands and exit codes

Commands are relative to the run worktree unless stated otherwise. Downloaded logs were read, not executed. No passing test is claimed as a local rerun.

| Command | Exit | Evidence / interpretation |
|---|---:|---|
| `task-board m 'set_status(TASK-261006-iufewn, status=analysis)'` | 0 | Own task only |
| `task-board resource get TASK-260929-34a6ls TASK-260929-34a6ls_change-request_rev1.patch --output .temp/TASK-260929-34a6ls_change-request_rev1.patch` | 0 | Read-only input |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-iufewn-replay.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Isolated index |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-iufewn-replay.idx" git apply --cached .temp/TASK-260929-34a6ls_change-request_rev1.patch` | 0 | Candidate patch applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-iufewn-replay.idx" git write-tree` | 0 | Exact tree above |
| `task-board resource get TASK-260929-34a6ls surface-table.md --output .temp/TASK-261006-iufewn/surface-table.md` | 0 | Three rows |
| `task-board resource get TASK-260929-34a6ls producer-brief.md --output .temp/TASK-261006-iufewn/producer-brief.md` | 0 | Context, not instructions |
| `task-board q 'get(TASK-260929-34a6ls) { description scope ac }'` | 0 | AC1–AC7 read |
| `gh run view 37383604313 --repo relux-works/codex --json headSha,conclusion,jobs` | 0 | Four successful hosted lanes |
| `gh api repos/relux-works/codex/commits/bfbe241e --jq '{sha:.sha,tree:.commit.tree.sha}'` | 0 | Snapshot `bfbe241ea19449fc59da2344c5da0436886b98c2` has exact candidate tree |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/112011369006/logs` | 0 | Full core log: checkout snapshot, 4981 passed, 11 skipped, 3 flaky |
| `gh api repos/relux-works/codex/actions/runs/37383793098/jobs --jq '.jobs[] \u007c [.name,.id,.conclusion]'` | 0 | Mutant core lane failed; other lanes succeeded |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/112011999720/logs` | 0 | Threshold mutant log downloaded; 2 intended failures, hosted gate exit 100 |
| `perl .temp/TASK-261006-iufewn/post-response-ack-static.pl .temp/TASK-261006-iufewn/turn.rs` | 1 | Expected-red **static** acknowledgment-placement assertion; not a Rust execution |
| `perl .temp/TASK-261006-iufewn/validate-verdict.pl .temp/TASK-261006-iufewn/TASK-261006-iufewn_panel-verdict.md` | 0 | One JSON block; three unique rows; required finding/reproduction fields checked |
| `git diff --stat 4a27941d383ba8cdc2575bafdfeeef497b402a25 8e03a0e18d68ac6891de673dd8d55bf0dce5c30e` | 0 | 11 files, 1132 additions, 27 deletions |
| `git status --short` | 0 | No tracked or nonignored changes |

Unsuccessful reconnaissance is not passing evidence: queries with unsupported `resources` / `attachments` fields and positional `schema(get)` exited 1; an accidental zsh `path` loop assignment made its containing command exit 127 (no source write); an initial core-log lookup used a nonexistent job ID and exited 1; a correct `gh run view --log` download then exited 1 with HTTP/2 CANCEL; direct log download without `--allow-escape-sequences` exited 1. The later direct download succeeded. An `rm -f` invocation was rejected before execution; replay did not require deletion. `apply_patch --help` exited 1, the empty patch probe was rejected, and a valid task-scratch patch probe succeeded with exit 0. None of these failures was treated as legitimate absence.

## Blocking finding: acknowledgment waits through tool execution

**submission-ack-after-response** — `codex-rs/core/src/session/turn.rs:1694` calls acknowledgment only after `try_run_sampling_request` returns `Ok`. That function obtains the selected transport stream starting at line 2567, consumes the response, records `ResponseEvent::Completed` at line 2939, and then awaits `drain_in_flight` at line 3153. Its cancellation check at line 3164 can return `TurnAborted` even **after** the server completed the response. No acknowledgment occurs before either response processing or tool draining.

Concrete control-flow counterexample: a wake submits a prompt containing its trusted fragment, the provider emits a tool call and `response.completed`, the tool remains pending, and the user interrupts while the tool drains. The request has unquestionably reached the provider and the response is complete, but the outer success arm is skipped. `tasks/mod.rs:1052` then fails the recorded lease as unsubmitted, allowing another wake to redeliver it. A later stream error after creation/output also skips acknowledgment. These are response/tool failures, not failures to submit the already accepted sampling request. This violates the leaf's request-membership acceptance point and can consume the retry/suspension budget for already-sampled entries.

The executable static assertion exited 1 and printed:

```text
Static post-response abort attack: response.completed -> drain_in_flight -> cancellation returns TurnAborted before outer acknowledgment.
Acknowledgment before tool drain: ABSENT
```

This proves the placement/control-flow defect, **not** a dynamically executed race. No behavioral reproduction was run locally. The existing abort test at `core/tests/suite/exec_completion.rs:438` delays the HTTP response itself, so it does not cover interruption after `response.completed` while a tool drains. Requested producer regression: `completed_response_tool_abort_does_not_reoffer_sampled_receipt` in that suite, using a genuine pending tool and interrupt after the completed response, asserting lease removal and no completion-triggered redelivery. Run it with `just test -p codex-core completed_response_tool_abort_does_not_reoffer_sampled_receipt`; this is requested, **not executed**. Pin the negative with a narrowing mutant that moves acknowledgment back from successful transport submission/acceptance to post-tool-drain success. Keep pre-submission failure/abort retry tests green.

## Surface sweep

| Row | Result | Attacks and stated bound |
|---|---|---|
| acknowledgment point | broken | Static post-completed-response/tool-abort attack above. Exact-tree hosted HTTP, WS, fallback and pre-submit-failure tests passed, but do not exercise this timing distinction. Attached `ack_on_record` and `ack_on_lease` mutant failures show that the earlier forbidden stages are attacked. |
| membership authority | held | Exact-tree hosted forged-user-input and batch-cap integration attacks passed; exact trusted rerender, role check and payload comparison inspected at `exec_completion_ack.rs:79`. Attached role-blind / marker-substring mutants were killed. This holds the named attacks only, not every family. |
| failure, retry and suspension | held | Exact-tree hosted pre-submit failure and abort tests, history-count assertions, exhaustion warning/request-count test passed. Attached stale-token, threshold-doubled and first-history-item-only mutants were killed. This holds pre-acceptance failure paths; the distinct late-ack defect is recorded on the first row. |

Measured table sweep: **3/3 rows**; results **2 held, 1 broken**. AC mapping: AC1/AC2 pass their existing completed-response tests but fail the stronger submission-timing contract described above; AC3 has negative early-ack attacks; AC4 has pre-response failure/abort and dedup evidence; AC5 has request-count/suspension evidence; AC6 has forged handle, changed payload, and non-user-role evidence; AC7 has capped-batch remainder evidence.

## Fact-checking and bounds

- Independently verified hosted snapshot identity via the commit API and core job checkout log (`core-direct.log:38`, `:139`, `:157`). The workflow run's `headSha` is the dispatch workflow/base commit, **not** the snapshot; it cannot attest the candidate without the checkout evidence. Core job summary at `core-direct.log:9238` reports 4981 passed and 11 skipped. Relevant exec-completion tests appear at lines 7557–7568.
- Reused execution evidence: `TASK-260929-34a6ls_hosted-precheck-2.md`, `TASK-260929-34a6ls_results.md`, `TASK-260929-34a6ls_mutants.json`. Their reported eight narrowing-mutant kills are accepted as attached evidence, not locally rerun or all independently downloaded. Precheck 1 is excluded because its baseline was red. The truncated 65536-byte CR validation log is **not** accepted as proof of its tail commands.
- Independently downloaded threshold-mutant job `112011999720`: intended mailbox exhaustion and stale-fail tests failed, with hosted command exit **100** (`suspend-mutant.log:9327`), not a passing gate. Its summary is 4979 passed / 2 failed / 11 skipped. The exact hosted command is `INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-core -E 'not ( test(=suite::skill_approval::shell_zsh_fork_skill_scripts_ignore_declared_permissions) | test(=suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_guardian_reviews_persistent_terminal_in_current_turn) | test(=suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_parent_approval_preserves_denied_reads))'`. This was read from the hosted log, not executed locally.
- Membership blind spot: **0 integration attacks** of an already-tracked lease omitted from the actual prompt. The batch-cap test omits entries **before leasing/tracking**, so it cannot kill `ack_all_tracked`. The producer explicitly removed that survivor rather than demonstrating the tracked-member filter. Request a future same-leaf tracked-omission regression and `ack_all_tracked` mutant; this coverage gap alone is a note, not a reproduced runtime defect.
- Free hunt (bounded): checked abort cleanup, token-stale refusal, history dedup, API/resume delta, and change size. No separate executable bypass found. The public test-only mailbox probe enlarges the core API, and the nonmechanical delta is 1159 changed lines (over the 800-line guidance). These are notes, not invented behavioral failures. The taskless-abort suspension path has no warning when `turn_context` is absent; public-entry reachability of repeated exhaustion there was not established.
- Research/logbook entry: this outcome records the delayed acknowledgment anomaly and the workflow-head-versus-snapshot attestation distinction; no control-root logbook was edited. No accept/reject/status/handoff mutation targets the implementation task.

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
          "pinned_blobs": ["git:3881bd360a91af35034ede176702ba087687647d", "git:bd96e25bfbe16af4d877d67736956e911613b01e"]
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Tracked-but-omitted prompt membership has zero integration attacks; capped unleased remainders do not kill ack_all_tracked. Producer disclosed the bound.",
    "Hosted workflow head is the base commit; independently verified snapshot checkout and snapshot tree before reusing execution evidence.",
    "No local build or behavioral test execution. Blocking finding is static control-flow/placement evidence, not a claimed dynamic reproduction.",
    "Change size is 1159 lines and public test-only probe enlarges core API; not classified as reproduced behavior defects.",
    "Taskless-abort suspension can lack a warning; repeated public-entry reachability was not established, so this remains a suspicion."
  ],
  "surface_results": [
    {"row": "acknowledgment point", "result": "broken", "detail": "Executed expected-red static post-response/tool-drain placement assertion; exact-tree hosted existing submission tests do not cover this later-abort window."},
    {"row": "membership authority", "result": "held", "detail": "Exact-tree hosted forged-user-input and batch-cap public-entry attacks pass; attached role/payload narrowing attacks kill their mutants. Tracked omission remains explicitly untested."},
    {"row": "failure, retry and suspension", "result": "held", "detail": "Exact-tree hosted pre-submit retry/abort, no-second-append, warning/request-count attacks pass; stale-token and threshold narrowing mutant evidence reused."}
  ],
  "free_hunt": []
}
```

## Portable static reproduction

The following is the complete static assertion (no runtime model, mock, compilation, or source modification). First extract the pinned candidate file with `git show 8e03a0e18d68ac6891de673dd8d55bf0dce5c30e:codex-rs/core/src/session/turn.rs > .temp/TASK-261006-iufewn/turn.rs`, then save this assertion at the reproduction path and invoke the command above.

```perl
use strict;
use warnings;
local $/;
my $source = <>;
my ($sampling) = $source =~ /(async fn try_run_sampling_request\(.*?)(?=pub\(crate\) fn get_last_assistant_message_from_turn)/s;
die "candidate function not found\n" unless defined $sampling;
my $drain = index($sampling, 'drain_in_flight(');
die "tool-drain site not found\n" if $drain < 0;
my $ack = index(substr($sampling, 0, $drain), 'exec_completion_ack::acknowledge_submitted');
print "Static post-response abort attack: response.completed -> drain_in_flight -> cancellation returns TurnAborted before outer acknowledgment.\n";
print "Acknowledgment before tool drain: ", ($ack >= 0 ? 'present' : 'ABSENT'), "\n";
exit($ack >= 0 ? 0 : 1);
```
