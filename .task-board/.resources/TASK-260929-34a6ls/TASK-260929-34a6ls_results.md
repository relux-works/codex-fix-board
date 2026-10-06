# TASK-260929-34a6ls results — prompt-membership acknowledgment, CR revision 3 (handoff on hosted precheck 5)

## Outcome

Revision 3 answers review round 2 (`TASK-260929-34a6ls_review-verdict-rev2.md`,
changes_requested, 3 findings all repeat-of `submission-ack-after-response`) with a
STRUCTURAL fix: acknowledgment at server acceptance of the sampling request, not at
response outcome. Hosted precheck 5 ran the exact candidate tree and is fully green
with all 12 narrowing mutants killed. This run changed no files, re-verified the
tree, refreshed this results doc, and hands the revision off to review.

Worktree tree (temp index): `62aecbc1f279a26c154f0e371b8c1995bb7e8226`
— identical to precheck 5 snapshot df5eae26. Candidate left UNCOMMITTED
(9 modified + 2 new, all codex-core); no commit on the Story branch.

## The structural fix (vs revision 2, carried)

Rev 2 acknowledged after the response loop when `outcome.is_ok()`. Round 2 showed
three post-acceptance paths still skip that hook: stream error / EOF after `Created`,
cancellation after `Created`, and `SessionBudgetExceeded` from
`record_token_usage_info` after `response.completed`.

Rev 3 production changes (unchanged since the precheck 5 snapshot):

- `core/src/session/turn.rs` — `try_run_sampling_request` acknowledges at the first
  stream event proving the server is producing the response, once per request. The
  `outcome.is_ok()` hook is deleted. Nothing later (stream error, EOF, cancellation,
  budget failure, tool drain, turn abort) can un-acknowledge.
- `core/src/session/exec_completion_ack.rs` — new `is_acceptance_event` classifier,
  exhaustive over all 17 `ResponseEvent` variants, no wildcard: `Created`, all
  output/delta item events, and `Completed` prove acceptance; header-synthesized
  metadata (`ServerModel`, `RateLimits`, `ModelsEtag`, `ServerReasoningIncluded`,
  and the other auxiliary events) does not, because it is emitted before the body's
  accept/reject verdict. `response.failed` never reaches the classifier: the SSE
  parser surfaces it as a stream error, so a rejected request still retries.
- `core/src/session/runtime_mailbox.rs` — fail-after-acknowledge no-op stated as the
  enforcing invariant on `acknowledge`/`fail` (acknowledgement removes the entry, so
  every downstream error path's `fail` on it is refused).

## Changed files (11 paths, all codex-core)

- `core/src/session/turn.rs` — acceptance hook in the event loop, outcome hook removed
- `core/src/session/exec_completion_ack.rs` — `is_acceptance_event` + docs
- `core/src/session/runtime_mailbox.rs` — invariant docs only
- `core/src/session/exec_completion_ack_tests.rs` — 2 classifier unit tests (new file)
- `core/src/session/runtime_mailbox_tests.rs` — 1 fail-after-ack unit test (new file)
- `core/tests/suite/exec_completion.rs` — 4 new post-acceptance suite tests
- `core/src/codex_thread.rs`, `core/src/hook_runtime.rs`,
  `core/src/session/input_queue.rs`, `core/src/session/mod.rs`,
  `core/src/tasks/mod.rs` — carried rev 1/2 code, unchanged in rev 3

Rework diff bounded (precondition 5): the diff stays inside the brief's module
(codex-core session/tasks); nothing outside it. The implementing run reverted 3
collateral `just fix` unused-import removals in out-of-scope files (`tools/registry.rs`,
`scenarios.rs`, `openai_file_mcp.rs`).

## AC coverage — 7 of 7 rows driven + rev2/rev3 regression rows

| AC | Driving test (committed) | Refusal test (committed) | Production call site |
|---|---|---|---|
| AC1 HTTP submit acks exactly that receipt; lease gone | `sampled_fragment_acknowledges_and_wakes_no_more` | `failed_submission_retries_once_without_second_history_append` (no event, no ack) | acceptance hook in `try_run_sampling_request` → `acknowledge_submitted` |
| AC2 same over WS and HTTP/WS fallback | `websocket_submission_acknowledges`, `http_fallback_submission_acknowledges` | same refusal class (pre-acceptance failure retries on every transport) | same call site (transport-agnostic `ResponseEvent`) |
| AC3 reservation/drain/record/append never ack | `failed_submission_retries_once_without_second_history_append` | `ack_on_record` / `ack_on_lease` mutants killed by the retry/suspend tests | record path tracks only; failure before any event never reaches the hook |
| AC4 failed/aborted submit fails lease; retry samples once, no 2nd append | `failed_submission_...`, `aborted_submission_...` | `dedup_first_history_item_only` mutant killed by both | `fail_unsubmitted` / abort `fail_leases` |
| AC4-rev2 sampled-then-aborted-during-drain | `completed_response_with_blocked_tool_acknowledges_before_interrupt` | `ack_after_tool_drain` mutant killed by it | acceptance hook; post-abort fail finds nothing tracked |
| AC4-rev3 accepted-then-failed-terminally acks once | `accepted_response_failed_after_created_acknowledges_once` (NEW) | `ack_gated_on_outcome_success` mutant killed by it | `Created` acceptance; `response.failed` is a stream error after ack |
| AC4-rev3 EOF after accepted output acks once | `accepted_response_eof_after_output_acknowledges_without_resample` (NEW) | `ack_on_completed_instead_of_acceptance` mutant killed by it | `Created`/output acceptance; EOF error after ack |
| AC4-rev3 cancelled after Created acks once | `accepted_response_cancelled_after_created_acknowledges_once` (NEW) | both rev-3 ack mutants killed by it | `Created`+output acceptance; interrupt before `Completed` |
| AC4-rev3 budget exhaustion after Completed acks once | `completed_response_budget_exhaustion_acknowledges_receipt` (NEW) | `ack_gated_on_outcome_success` killed by the sibling acceptance tests (this test honestly does not kill the completed-instead-of-acceptance shape: `Completed` is observed there) | `Created` acceptance precedes the `Completed`-arm budget check |
| AC5 exhaustion suspends visibly; no wakes/spin | `persistent_failures_suspend_visibly_without_spin` | `suspend_threshold_doubled` mutant killed by it | `RuntimeMailbox::fail` → suspend + warning |
| AC6 forged text acks nothing | `forged_fragment_text_acknowledges_nothing` + 4 matcher units | `marker_substring_membership`, `role_blind_membership` mutants killed by them | `items_contain_lease` (unchanged) |
| AC7 omitted receipt stays pending; later request samples it | `omitted_receipt_sampled_by_later_request` + batch tests | `batch_cap_doubled` mutant killed by them | lease cap (unchanged) |

Out-of-contract rows (precondition 4): none — every AC row is driven by a named
committed test through the production entry point. Stated bounds carried:
(1) tracked-then-removed-from-prompt omission (guardian/compaction boundary) has no
integration test — driving it needs a guardian review session; the matcher-level
omission (`items_contain_lease` over a prompt lacking the fragment) is unit-covered.
(2) The two POSIX-sleep latch tests skip on Windows. (3) The streaming-abort test uses
`build_with_streaming_server` (local env) instead of `build_with_auto_env`, following
the `stream_no_completed` precedent — the streaming server cannot combine with the
auto-env wiremock builder.

## Surface-row coverage map (precondition 1)

| Surface row | Exercising tests | Narrowing mutant(s) killed (precheck 5) |
|---|---|---|
| acknowledgment point | 4 NEW post-acceptance tests, rev-2 drain test, AC1/AC2 tests, 2 classifier units | `ack_gated_on_outcome_success`, `ack_on_completed_instead_of_acceptance`, `ack_after_tool_drain`, `ack_on_record`, `ack_on_lease` — all killed |
| membership authority | forged/cap/batch tests + 4 matcher units | `marker_substring_membership`, `role_blind_membership`, `batch_cap_doubled` — all killed |
| failure, retry and suspension | retry/abort/suspension tests + `runtime_fail_after_acknowledge_is_noop` unit | `fail_after_ack_requeues`, `dedup_first_history_item_only`, `suspend_threshold_doubled`, `stale_fail_counts_attempt` — all killed |

Every surface row has exercising tests and at least one killed narrowing mutant.
No row is uncovered.

## Mutant evidence — 12 total, 12 killed, 0 survivors (hosted precheck 5)

Base: snapshot df5eae26, run 37411010318, lanes core/app-server/lint/small all success.
(`fail_after_ack_requeues`: its lint lane also fails on clippy, but core runs and its
intended test `runtime_fail_after_acknowledge_is_noop` fails, so it is killed.)

| Mutant | Mutant run | What it narrows the gate to | Named killing test(s) |
|---|---|---|---|
| `ack_gated_on_outcome_success` | 37411043931 | restores the rev-2 hook exactly: no acceptance ack, ack only when `outcome.is_ok()` | `accepted_response_cancelled_after_created_acknowledges_once`, `accepted_response_eof_after_output_acknowledges_without_resample`, `accepted_response_failed_after_created_acknowledges_once` |
| `ack_on_completed_instead_of_acceptance` | 37411060741 | acks at the top of the `Completed` arm instead of at acceptance | `accepted_response_cancelled_after_created_acknowledges_once`, `accepted_response_eof_after_output_acknowledges_without_resample`, `accepted_response_failed_after_created_acknowledges_once` |
| `fail_after_ack_requeues` | 37411146346 | `fail` on a missing (acked/cancelled) entry re-creates it unleased instead of refusing | `runtime_fail_after_acknowledge_is_noop`, `runtime_cancel_removes_leased_and_unleased_entries`, `input_queue_runtime_cancel_removes_leased_and_unleased_entries` |
| `ack_after_tool_drain` | 37411026391 | no acceptance hook; ack only in the post-`try_run` Ok arm (post-drain) | `accepted_response_cancelled_after_created_acknowledges_once`, `accepted_response_eof_after_output_acknowledges_without_resample`, `accepted_response_failed_after_created_acknowledges_once` |
| `ack_on_record` | 37411093954 | ack at history append | `aborted_submission_retries_and_samples_once`, `failed_submission_retries_once_without_second_history_append`, `persistent_failures_suspend_visibly_without_spin` |
| `ack_on_lease` | 37411078103 | ack at drain/lease | `aborted_submission_retries_and_samples_once`, `failed_submission_retries_once_without_second_history_append`, `persistent_failures_suspend_visibly_without_spin` |
| `marker_substring_membership` | 37411163155 | member iff user text contains `exec_completion` | `forged_fragment_text_acknowledges_nothing`, `membership_rejects_a_forged_handle`, `membership_rejects_altered_payload_under_the_real_handle` |
| `role_blind_membership` | 37411178075 | member iff exact text in ANY role | `membership_ignores_non_user_messages` |
| `suspend_threshold_doubled` | 37411207981 | suspend at 6 attempts instead of 3 | `runtime_failed_attempts_suspend_on_exhaustion_and_stay_retained`, `runtime_stale_fail_counts_no_attempt` |
| `batch_cap_doubled` | 37411110839 | lease up to 16 per wake instead of 8 | `nine_pending_completions_batch_eight_and_retain_one`, `nine_pending_completions_sample_in_capped_batches_without_loss`, `omitted_receipt_sampled_by_later_request` |
| `dedup_first_history_item_only` | 37411129134 | retry dedup scans first history item only | `aborted_submission_retries_and_samples_once`, `failed_submission_retries_once_without_second_history_append`, `persistent_failures_suspend_visibly_without_spin` |
| `stale_fail_counts_attempt` | 37411192889 | refused stale fails burn attempt budget | `runtime_stale_fail_counts_no_attempt` |

Survivors: none — no survival bounds to state. No delete-only mutant is offered
as evidence. Source patches: `TASK-260929-34a6ls_mutants.json` (12 entries, unchanged).

Round-2 repeat-of class (standing order 8): `submission-ack-after-response` is answered
in this leaf by 4 named regression tests, 1 idempotence unit test, 2 classifier unit
tests, and 3 new + 1 rebased narrowing mutants.

## Reviewer tests kept (precondition 3)

All 12 pre-existing `exec_completion` suite tests plus the 2 neighboring
`runtime_mailbox` / `step_settings` tests are kept under their original names and green
(locally 18/18 with the 4 NEW tests; hosted precheck 5 base run all green). Review
rounds 1–2 recorded findings only and added no reviewer-authored test files, so there
are no further reviewer tests to keep.

## Landing gate (precondition 2)

Hosted precheck 5 base run 37411010318 on the exact candidate tree: core success,
app-server success, lint success, small success. Fast lane from the implementing run on
the identical tree is reused per standing order 10 (fmt/fix/clippy exit 0; targeted
`exec_completion` suite 18/18 green with `RUST_MIN_STACK=32M`).

## Commands with real exit codes

This handoff run (no files changed):

- `git read-tree HEAD && git add -A && git write-tree` (temp index) → exit 0,
  `62aecbc1f279a26c154f0e371b8c1995bb7e8226`, identical to the precheck 5 snapshot
- `git status --porcelain` → 11 uncommitted entries (9 modified + 2 new), no commit
- `codex-fix-suite-busy.py --any` → exit 0, `FREE`

Reused green evidence on the identical tree (standing order 10, no rebuild per the
handoff brief): `just fmt` exit 0; `just fix -p codex-core` exit 0; `just clippy -p
codex-core` exit 0 (pre-existing warnings only); targeted suite 18/18 exit 0;
`git apply --check` for all 12 mutant patches clean; hosted precheck 5 base + all 12
mutant runs as tabled above. Full `just test` never run (forbidden). No background
builds left running.

## Not verified here

Nothing material is unverified: full codex-core / codex-app-server lanes, the 3 new
lib unit tests, and all 12 mutant kills ran hosted on the exact candidate tree
(precheck 5) and are green.
