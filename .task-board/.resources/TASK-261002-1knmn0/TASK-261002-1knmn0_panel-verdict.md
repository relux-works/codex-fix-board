# Panel verdict — TASK-260929-u2i5rr CR-5 rev5 (R141 DELTA, non-recording)

Verdict: **accept**

## Replay tree check
- Base `0462dcc062b822bb8fff16cc31ce6eeab69823b9`, patch `TASK-260929-u2i5rr_change-request_rev5.patch` (3 paths: completion_receipt.rs, completion_receipt_tests.rs, unified_exec/mod.rs).
- `GIT_INDEX_FILE=<tmp idx> git read-tree <base>` exit 0; `task-board resource get ... --output` exit 0; `git apply --cached` exit 0; `git write-tree` exit 0 printing `00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8` = expected candidate tree. MATCH.
- `git diff base..candidate --stat -- codex-rs/core/src/tools codex-rs/core/tests` is empty: the three out-of-scope lint-import edits are gone. The only change outside the two receipt files is the one-line `pub(crate) mod completion_receipt;` in mod.rs.
- Production code is unchanged against rev4 by line anchors (:245, :256, :421-430, :505, :525 are in place). Rev5 is test-only plus the scope revert.

## Commands run (no cargo/just/build/test, per brief)
| Command | Exit |
| --- | ---: |
| git read-tree (temp index) | 0 |
| task-board resource get (patch, verdict-rev4, hosted-ci-rev5, surface-table) | 0 |
| git apply --cached | 0 |
| git write-tree | 0 |
| git show <tree>:... (candidate impl + tests, read in full) | 0 |
| git diff base..tree --stat (scope check) | 0 |

Execution evidence is not mine: hosted relux-ci run 36987452652 on this exact tree (`00518744...`) is attached as TASK-260929-u2i5rr_hosted-ci-rev5.md with all four jobs (small, lint, app-server, core) green. That artifact records job conclusions only; it does not list per-test names, so the brief's "20 tests pass" is not independently visible there. I counted 20 `completion_receipt_*` test fns in the candidate file, matching the brief's count.

## Round-2 finding fix check (each named mutant judged by reading)
| Finding / mutant | Killing test | Result |
| --- | --- | --- |
| terminal-history-bound-unguarded, M15 (delete pop_front eviction) | `..._terminal_history_evicts_only_the_oldest_after_64_outcomes` retires 65 receipts one at a time; asserts status(first)==UnknownReceipt, status of all 64 others==Cancelled. Also kills: eviction `==`->`>` (65th push keeps receipt 0), pop_back instead of pop_front, constant 65 or 63 (63 evicts receipts[1] too). | killed |
| terminal-path-owner-gates, M12 (drop :245 owner compare in terminal_error) | `..._terminal_history_refuses_foreign_owners_and_repeat_cancellation`: for Sampled, InlineResult and Cancelled receipts x 3 foreign owners (thread, runtime-generation, call-id) it calls lease, resolve, publish_exit, and forged-lease fail_sampling/acknowledge_sampled. Without :245 these return AlreadyConsumed / InvalidTransition / Cancelled, not ForeignOwner. Narrowing the compare to a single field is also caught, since each owner differs in exactly one field. | killed |
| M13 (drop :525 owner compare in status terminal branch) | same test, `store.status(receipt_id, foreign_owner)` expects Err(ForeignOwner); mutant returns Ok(status). | killed |
| M14 (drop :505 ForeignOwner passthrough in cancel) | same test, foreign `cancel` on a terminal receipt expects ForeignOwner; mutant yields AlreadyTerminal. | killed |
| AlreadyTerminal | same test, owner `cancel` after Sampled/Inline/Cancelled expects AlreadyTerminal; mutants returning Ok or the raw terminal error fail. Legit owner status after each foreign probe is re-asserted (no state corruption, no leak of outcome). | killed |
| owner-call-id-boundary-256 | `..._owner_accepts_256_bytes_and_refuses_257`: 256 bytes must construct and reserve; 257 refused. `>`->`>=` mutant fails the expect. | killed |
| sampling-source-attribution-nondeterministic, M16 | `..._terminal_stdin_and_pushed_sources_share_one_lease` now deterministically asserts LeasedToSampling{TerminalStdinOutput} and Sampled{TerminalStdinOutput} after a stdin-sourced lease+ack. Replacing the stored source in the phase, in the SamplingLease, or in the Sampled retire record with PushedCompletion fails (status mismatch, or StaleLease on ack via the source equality). | killed |

## Same-class sweep
Terminal-path gates now have a call-site-by-call-site foreign test (status, cancel, lease, resolve, publish_exit, fail, ack), and active-path gates are covered by the pre-existing rev2 tests. Remaining unguarded mutants are not owner/bound gates and are recorded as notes, not findings (see `notes`).

## Rework regression check
Impl untouched, so no behavior regression is possible from product code. The new tests are single-threaded and deterministic. The existing thread tests keep a barrier handshake with no deadlock path (the race test's lose-then-ack ordering is forced by `both_leases_attempted`). The tests access `SamplingLease` private fields as a child module, so no visibility changes were needed. Hosted lint (clippy) is green on this tree.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Replay: write-tree equals expected candidate tree 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8 (exit 0 at every step).",
    "Scope: the three out-of-scope upstream lint edits are reverted; candidate touches exactly completion_receipt.rs, completion_receipt_tests.rs and one export line in unified_exec/mod.rs. The prior-round scope notes are resolved.",
    "Hosted evidence (run 36987452652, tree 00518744) shows four green jobs; the artifact lists job conclusions only, not per-test names, so the 20-test and named-test claims rest on my static count of 20 completion_receipt_* fns, not on a visible test list.",
    "Residual unguarded mutant (non-gate, robustness-level, not reported as finding): cancel() on an evicted/unknown id maps UnknownReceipt through the :504 arm; deleting it would yield AlreadyTerminal and no test calls cancel/lease/resolve/publish on an evicted id (UnknownReceipt is asserted only via status, once). Same for terminal_error's None => UnknownReceipt arm on the non-status paths. Refusal still happens either way; only the error variant differs.",
    "Residual: IdGenerationFailed and the id-collision check in reserve() have no test; unreachable without an injection seam (v4 UUID), so it is an accepted bound.",
    "Residual (equivalent-mutant candidate): the `*source == lease.source` check in fail_sampling/acknowledge_sampled is redundant given the token; no test forges a lease with matching token and different source. Not counted.",
    "Stated bounds carried from earlier rounds: Reserved slots have no timeout (caller contract for sibling B2); evicted terminal ids report UnknownReceipt; module is unwired (#![allow(dead_code)]) by design for stage 2a; barrier tests prove ordering semantics under one mutex, not true interleaving, which is sufficient with a single lock.",
    "Size: 535 impl lines (466 non-blank non-comment, under 500) and about 998 lines of tests; test-dominated and a single coherent stage."
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "held",
      "detail": "Every attack family has a test: both exit/decision orders under barriers, lease failure and stale tokens (both fail and ack), cancel from each of Reserved/Armed/Queued/Leased, double sample, stdin vs pushed race and deterministic source attribution, 64/65 capacity and slot release, owner mismatch on thread, generation and call id on active AND terminal paths, bounded terminal history with eviction, poisoned lock. All five named round-2 mutants (M12-M16) plus AlreadyTerminal and the 256-byte boundary are killed by reading."
    }
  ],
  "free_hunt": [
    "Checked that the foreign-owner test builds its forged leases from a real lease clone with receipt_id and owner overwritten, so fail_sampling/acknowledge_sampled reach terminal_error with a foreign owner for each terminal kind (not just the active path).",
    "Checked the eviction test against the capacity bound: it reserves and cancels sequentially so active never exceeds 1, and it uses MAX_COMPLETION_RECEIPTS+1 = 65 outcomes while the code bound is the separate MAX_TERMINAL_RECEIPTS (both 64); changing the code constant in either direction is caught, but a future divergence of the two constants would make the test's 65 count stale, which is a maintenance note only.",
    "Checked mutants on retire(): active.remove then push_back; dropping the remove would leak slots and be caught by the capacity and cancel-frees-slot tests; swapping the retired phase kind is caught by the per-kind status assertions in the terminal test.",
    "Checked terminal-lookup order: terminal() scans newest-first; no duplicate ids are possible (reserve checks both active and terminal), so rev and find order is equivalent.",
    "Checked that the new test never relies on timing or thread scheduling; the only threaded tests use barriers with a forced order.",
    "Checked reserve() slot accounting after Inline/Sampled/Cancelled: all three go through retire(), the single path that removes from active."
  ]
}
```
