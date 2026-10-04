# TASK-260929-u2i5rr — revision-5 coverage map


**6 of 6 AC rows have driving and refusal tests through the production receipt API. Execution on this revised test tree: 0 of 6 AC rows driven in this local run.** The latest brief explicitly delegates core test execution to hosted relux-ci after handoff; Clippy type-checking is not reported as test execution. The inactive module has no exec/tool call sites yet, as required by this leaf.

| AC | Driving test | Refusal test | Production entry points |
|---|---|---|---|
| 1 | `completion_receipt_happy_path_samples_exactly_once` | `completion_receipt_rejects_a_second_claim_after_sampling` | reserve:274 → resolve_initial_response:302 → publish_exit:375 → lease_for_sampling:404 → acknowledge_sampled:464 |
| 2 | `completion_receipt_exit_and_initial_response_are_linearized_in_both_orders` (barriers force exit-first inline, exit-first arm, and arm-first) | `completion_receipt_inline_decision_waits_for_finalized_exit`; inline leasing refusal in the order test; `completion_receipt_duplicate_exit_while_reserved_preserves_first_completion` | publish_exit:375, resolve_initial_response:302, lease_for_sampling:404 |
| 3 | `completion_receipt_failed_lease_requeues_same_receipt_and_rejects_stale_token` | `completion_receipt_stale_failed_lease_cannot_requeue_a_new_lease` | fail_sampling:441, lease_for_sampling:404, acknowledge_sampled:464 |
| 4 | `completion_receipt_cancellation_is_terminal_from_each_unsampled_state` | Cancelled leasing/acknowledgment refusal within that test; new terminal repeat-cancellation table | cancel:492, status:515, lease_for_sampling:404, acknowledge_sampled:464, reserve:274 |
| 5 | `completion_receipt_capacity_refuses_the_65th_and_reuses_a_freed_slot`; new terminal-history eviction and call-id boundary tests | Structured CapacityExceeded at reservation 65; UnknownReceipt for evicted terminal id; InvalidOwner at 257 bytes | reserve:274, cancel:492, status:515, ReceiptOwner::new:34 |
| 6 | `completion_receipt_terminal_stdin_and_pushed_claim_race_consumes_once`; `completion_receipt_terminal_stdin_and_pushed_sources_share_one_lease`; happy path for deterministic pushed attribution | AlreadyLeased/AlreadyConsumed assertions in both shared-claim tests | lease_for_sampling:404, fail_sampling:441, acknowledge_sampled:464, status:515 |

Surface-table map, using the supplied single row:

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| concurrency state machine | All 20 named completion_receipt tests; specifically the three new regression tests and the strengthened deterministic stdin test above | Current-tree mutant execution is unverified under the fast-lane prohibition. Historical rev2 evidence records M1/M2/M4/M5/M6/M7/M9/M10/M11 failures; tests changed, so that is not reused as a current-tree gate pass. New and narrowing mutant recipes are mapped below for execution by hosted validation/review | none within the receipt-state-machine surface; exec launch, watchers, mailbox, transport, model wake, and host integration are outside this leaf per Description “Not wired to tools or the mailbox yet” and Scope “no watcher/process-manager hooks” |


Mutant recipes and expected failing tests are in TASK-260929-u2i5rr_results.md. No current-tree behavioral mutant execution is claimed: local core tests are forbidden by the latest fast-lane brief. Historical observed kills do not validate this changed test tree.
