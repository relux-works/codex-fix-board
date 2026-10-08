# R141 DELTA panel verdict — TASK-260929-u2i5rr, CR-TASK-260929-u2i5rr-4 rev4 (non-recording)

Reviewer task: TASK-261002-3ptwun. Nothing was written on TASK-260929-u2i5rr (no accept/reject/withdraw/set_status/handoff; only `resource get` and `q get` reads).

Verdict: **changes_requested**

The one-word verdict is driven by a single class repeat (see finding `terminal-path-owner-gates-unguarded`): the F1 class (owner gate with no narrowing-mutant-killing test) still exists on the terminal-history path. F1-F3 themselves are fixed. The candidate source was not reproduced broken. The fix is one small test. The recording reviewer may downgrade this to accept-with-note if the repair is judged not worth another round.

## Replay tree check
- `git read-tree 0462dcc062b822bb8fff16cc31ce6eeab69823b9` into a temporary index: exit 0.
- `task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_change-request_rev4.patch --output .temp/...`: exit 0.
- `git apply --cached` of the patch onto that index: exit 0.
- `git write-tree`: exit 0, printed `e9a8095f146dd156b09351cc2af473781aa37272` = expected candidate tree. **MATCH** (no bypass finding).
- The patch touches 6 paths: `completion_receipt.rs` (+535), `completion_receipt_tests.rs` (+831), `unified_exec/mod.rs` (+1, `pub(crate) mod completion_receipt;`), and three one-line unused-import removals (`tools/registry.rs`, `tests/suite/openai_file_mcp.rs`, `tests/suite/scenarios.rs`).

## Other commands run (all read-only; no cargo/just/build/test)
| Command | Exit |
|---|---|
| `task-board m 'set_status(TASK-261002-3ptwun, status=analysis)'` (own task) | 0 |
| `task-board resource get TASK-260929-u2i5rr {surface-table.md, producer-brief.md, review-verdict-rev1.md, results.md}` | 0 each |
| `task-board q 'get(TASK-260929-u2i5rr) { description scope ac }'` | 0 |
| `git show e9a8095f…:<path>` for `completion_receipt.rs`, `completion_receipt_tests.rs`, `mod.rs`, `registry.rs`, `registry_tests.rs`, `openai_file_mcp.rs`, `scenarios.rs`; `git grep` for the removed imports | 0 (two early `git show` calls with a zsh `$C:co` expansion typo failed with exit 128 and were rerun correctly) |
| `task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_hosted-ci-rev4.md` | "resource not found": the hosted relux-ci result is **not attached yet**. Not claimed as evidence either way. |

Not executed: any mutant. All mutant kill/survive statements below are static reasoning from the source and test text, not executed runs. Each is a one-token edit with a single call path, so the reasoning is unambiguous, but it is labelled "static".

## Part 1 — previous round (rev1 merged verdict) F1-F3: all fixed
| Rev1 finding | Fix in rev4 candidate | Static check |
|---|---|---|
| F1 owner gate unguarded on `lease_for_sampling` / `resolve_initial_response` (M1/M2) | `completion_receipt_foreign_owner_is_refused_on_resolve_and_lease` drives foreign thread, foreign generation and foreign call owners (`foreign_receipt_owners`) on both entry points, then confirms the legitimate owner still arms/queues | M1 (drop owner arm at `lease_for_sampling`:412) would return `Ok(lease)` where `Err(ForeignOwner)` is asserted: killed. M2 (drop at `resolve_initial_response`:316) would return `Armed`: killed. |
| F1 (cont.) foreign lease on `fail_sampling` / `acknowledge_sampled` (M10/M11) | `completion_receipt_foreign_lease_is_refused_on_fail_and_acknowledge` mutates the private `lease.owner` for each foreign owner | M10 (drop owner arm :444) would requeue `Ok(())`: killed. M11 (:470) would sample: killed. |
| F2 stale first lease calling `fail_sampling` after re-lease (M4) | `completion_receipt_stale_failed_lease_cannot_requeue_a_new_lease` | Dropping `*token == lease.token` at :454 with same source would requeue the live lease, returning `Ok(())` where `StaleLease` is asserted: killed. Live second lease is then acknowledged, proving it was left intact. |
| F3 duplicate `publish_exit` while Reserved (M7) | `completion_receipt_duplicate_exit_while_reserved_preserves_first_completion` covers both the later-InlineResult and later-Arm/Queued consumers and asserts the FIRST completion is yielded | Dropping `if stored.is_none()` at :389 would overwrite and return `RetainedUntilDecision`: killed. |

Rev1 M5 (ack token) and M9 (capacity `>=`) remain killed by the unchanged tests. M10/M11 source-comparison-only variants (`*source == lease.source`) are equivalent mutants (the UUID token already binds); not counted.

## Part 2 — same class elsewhere
Owner/ForeignOwner gates are checked on three more sites that no test reaches, because every `ForeignOwner` assertion in the suite (test lines 505, 509, 513, 534, 553, 573, 580) is made against a receipt that is still in `active`. Bounds/gates in the same family that are also unguarded are listed in the findings. See `terminal-path-owner-gates-unguarded`, `terminal-history-bound-unguarded`, `sampling-source-attribution-nondeterministic`.

## Part 3 — did the rework break anything
No. The rework changed tests only (candidate tree identical to rev2); the source blobs are byte-identical per the results note and the tree hash matches. The three unrelated unused-import removals compile-check by grep: `ToolCallSource` has no remaining unqualified use in `registry.rs` and `registry_tests.rs` uses only the fully qualified path (line 839); `body_json` and `ReasoningEffort` have no use besides their import lines in the base. Scope note below.

## Surface table (one result per row)
| Row | Result |
|---|---|
| concurrency state machine | **broken (test-guard only)**: behavioral attacks held; rev1 F1-F3 fixed; the F1 class still repeats on the terminal-history owner gates (finding 1), plus two lower-severity guard gaps (findings 2-3). |

Attacks that held (static, source + tests): exit before/after decision with both orders forced; duplicate publish on Reserved/Queued; lease while leased; stdin vs pushed claim race (loser can only see AlreadyLeased because the second barrier holds the winner's ack until both attempts are made); stale-token ack and fail after requeue; cancel from Reserved/Armed/Queued/Leased; cancelled receipt cannot lease/ack; 64/65 capacity and slot reuse; foreign thread/generation/call on active receipts for all seven entry points; poisoned lock -> `LockPoisoned` (single `lock_state` choke point); all state transitions happen inside one lock scope, so no check-then-act gap between the decision read and the mutation in `resolve_initial_response`, `lease_for_sampling` or `acknowledge_sampled`.

```verdict-findings
{
  "findings": [
    {
      "id": "terminal-path-owner-gates-unguarded",
      "row": "concurrency state machine",
      "invariant": "A receipt is visible and usable only to its owning thread/runtime generation/call on EVERY path, including after it reaches a terminal state and sits in the bounded terminal history (AC: ids tied to owner).",
      "mechanism": "Three ForeignOwner gates sit on the terminal-history path: StoreState::terminal_error `Some(receipt) if receipt.owner != *owner => ForeignOwner` (completion_receipt.rs:245, used by publish_exit, lease_for_sampling, resolve_initial_response, fail_sampling, acknowledge_sampled), CompletionReceiptStore::cancel `ReceiptError::ForeignOwner => Err(ForeignOwner)` passthrough (:505), and CompletionReceiptStore::status terminal branch `Some(record) if record.owner != *owner => Err(ForeignOwner)` (:525). No test creates a terminal receipt (Sampled, InlineResult, Cancelled) and then calls any API with a foreign owner or foreign lease; every ForeignOwner assertion targets an active receipt. Narrowing mutants that drop :245 or :525 would let a foreign owner read a terminal receipt's outcome (Cancelled reason, Sampled source) or get a real error instead of ForeignOwner, and mutant :505 would make a foreign cancel on a terminal receipt return AlreadyTerminal; the whole suite stays green. Same class as rev1 F1, on the sibling path. Static analysis only; mutants not executed.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/unified_exec/completion_receipt_tests.rs",
          "command": "Mutant M12 (static, not run): in completion_receipt.rs delete the line `Some(receipt) if receipt.owner != *owner => ReceiptError::ForeignOwner,` in StoreState::terminal_error. Mutant M13: delete `Some(record) if record.owner != *owner => Err(ReceiptError::ForeignOwner),` in the terminal branch of status(). Mutant M14: delete the `ReceiptError::ForeignOwner => Err(ReceiptError::ForeignOwner),` arm in cancel(). Then `just test -p codex-core -E 'test(completion_receipt)'`.",
          "expected_failure": "A new test is needed: for each state Sampled, InlineResult and Cancelled, retire a receipt, then call status, cancel, lease_for_sampling and a lease cloned with a foreign `owner` field on fail_sampling/acknowledge_sampled using each foreign_receipt_owners(n) owner; each must return Err(ForeignOwner) and the legitimate owner must still see the true terminal status. With that test M12/M13/M14 each turn it red; today 17 of 17 pass under all three (by reading)."
        }
      ],
      "severity": "robustness",
      "repeat-of": "owner-gate-unguarded-on-lease-and-resolve (rev1 F1), sibling path"
    },
    {
      "id": "terminal-history-bound-unguarded",
      "row": "concurrency state machine",
      "invariant": "The retained terminal history is bounded at 64 entries; the oldest entry is evicted and then reports UnknownReceipt (documented bound, AC5 'bounded'; AGENTS 'no unbounded items').",
      "mechanism": "StoreState::retire `if self.terminal.len() == MAX_TERMINAL_RECEIPTS { self.terminal.pop_front(); }` (:256). No test retires more than 64 receipts, so deleting the eviction (unbounded VecDeque growth, linear scan in terminal()) or changing the constant leaves the suite green. The documented UnknownReceipt-after-eviction behavior is likewise asserted nowhere. Static analysis only.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/unified_exec/completion_receipt_tests.rs",
          "command": "Mutant M15 (static, not run): delete the `if self.terminal.len() == MAX_TERMINAL_RECEIPTS { self.terminal.pop_front(); }` block in retire(). Then `just test -p codex-core -E 'test(completion_receipt)'`.",
          "expected_failure": "A new test that cancels MAX_COMPLETION_RECEIPTS + 1 receipts one at a time (slots are freed each time) must see status(first) == Err(UnknownReceipt) while status(last) == Ok(Cancelled). M15 turns it red; today all tests pass under M15 (by reading)."
        }
      ],
      "severity": "robustness",
      "repeat-of": "none"
    },
    {
      "id": "sampling-source-attribution-nondeterministic",
      "row": "concurrency state machine",
      "invariant": "The lease and the Sampled record carry the source that actually won the shared claim (PushedCompletion vs TerminalStdinOutput), so downstream code knows which path consumed the completion (AC6 'whichever is sampled first consumes it').",
      "mechanism": "The only test asserting a TerminalStdinOutput-derived status is the thread race test, which compares Sampled{source: winner} against whichever side won, so a mutant that records PushedCompletion regardless of the `source` argument in lease_for_sampling (:421-430) is caught only on the interleavings where stdin wins. The deterministic test `..._sources_share_one_lease` acknowledges a stdin lease but never asserts status Sampled{TerminalStdinOutput} or LeasedToSampling{TerminalStdinOutput}. Static analysis only.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/unified_exec/completion_receipt_tests.rs",
          "command": "Mutant M16 (static, not run): in lease_for_sampling replace both `source` values stored in LeasedToSampling and SamplingLease with `SamplingSource::PushedCompletion`. Then `just test -p codex-core -E 'test(completion_receipt)'`.",
          "expected_failure": "In `completion_receipt_terminal_stdin_and_pushed_sources_share_one_lease` add status(...) == LeasedToSampling{source: TerminalStdinOutput} after the stdin lease and == Sampled{source: TerminalStdinOutput} after the ack. M16 then fails deterministically; today it fails only when stdin wins the thread race."
        }
      ],
      "severity": "robustness",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Replay: write-tree equals e9a8095f146dd156b09351cc2af473781aa37272 (exit 0 at every step).",
    "Hosted relux-ci result TASK-260929-u2i5rr_hosted-ci-rev4.md was NOT attached when this review ran (resource not found). The completion_receipt unit tests run only on that lane; this review gives no execution evidence for them. The recording step should wait for it, as the orchestrator note says. Rev3 last ran the 17-test suite green locally per the results note (not re-verified here).",
    "Scope: the patch edits three files outside the task Scope (registry.rs, openai_file_mcp.rs, scenarios.rs: one unused-import removal each). They are compile-safe by grep, and they are the three entries in relux-ci.yml KNOWN_WARNINGS, which become stale but harmless entries. This is a small scope overrun against 'completion_receipt.rs + tests + module export only'; accept or move it to a separate change at the recorder's discretion. It risks trivial merge conflicts with upstream for these three lines.",
    "cancel() on an already-terminal receipt returns AlreadyTerminal; no test pins that (cancel after Sampled/Cancelled/InlineResult). A silent Ok would not corrupt state because the receipt is no longer in `active`, so this is a note, not a finding. Could be added to the terminal-path test above.",
    "ReceiptOwner::new boundary: only '' and 257 bytes are tested; a 256-byte id (accepted) is not, so a `>`->`>=` mutation on MAX_CALL_ID_BYTES survives. Low value; add one positive 256-byte case if the new test file is touched anyway.",
    "Barrier-forced 'both orders' tests are sequentially ordered around one mutex, so they prove ordering semantics but not interleaving; with a single lock held across each transition that is sufficient for this stage.",
    "Stated bounds carried from rev1: terminal history capped at 64 (evicted id -> UnknownReceipt); Reserved slots have no timeout, so a caller that never decides holds a slot until cancel (caller contract for sibling B2); module is not wired to launch/watcher/mailbox.",
    "argument-comment-lint: `uncommented_anonymous_literal_argument` is allow-by-default and not part of relux-ci, so literal arguments such as receipt_owner(1) are not a finding."
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "broken",
      "detail": "Behavior held under every static attack and rev1 F1-F3 are fixed with killing tests; broken only in the test-guard sense: owner gates on the terminal-history path (terminal_error :245, status :525, cancel :505), the terminal-history bound (:256) and stdin source attribution (:421-430) are unguarded by any test. Findings: terminal-path-owner-gates-unguarded, terminal-history-bound-unguarded, sampling-source-attribution-nondeterministic."
    }
  ],
  "free_hunt": [
    "Checked all state transitions for check-then-act gaps: each public method takes the single lock once and mutates inside it; none releases between read and write.",
    "Checked slot accounting: active.len() counts Reserved/Armed/Queued/Leased only; retire() removes from active for Sampled, InlineResult and Cancelled, so every terminal outcome frees a slot, and the reserve ID-uniqueness loop checks both active and terminal.",
    "Checked lease forging: SamplingLease has private fields and a fresh v4 UUID token per lease; the only way to forge one is inside the module's own tests.",
    "Checked error mapping for lease/ack/fail on terminal receipts: Sampled -> AlreadyConsumed, Cancelled -> Cancelled{reason}, InlineResult -> InvalidTransition; consistent with the tests that exist.",
    "Checked Reserved-with-retained-exit then Cancel: the retained completion is dropped with the cancellation by design (explicit terminal reason), not lost silently.",
    "Checked that removing the three unused imports cannot break compilation of registry_tests.rs (`use super::*` but only a fully qualified ToolCallSource path), openai_file_mcp.rs or scenarios.rs by grep on the candidate and base blobs.",
    "Checked Cargo lints: expect_used/unwrap_used are denied in the workspace but clippy.toml sets allow-expect-in-tests/allow-unwrap-in-tests, so the test file's `.expect(...)` calls are fine; production code in the module uses no unwrap/expect."
  ]
}
```

## Commands to hand over for repair (non-binding suggestion)
One additional test file section only: terminal-state foreign-owner test (finding 1), a 65-retire eviction test (finding 2), two status assertions in the stdin-share test (finding 3). No source change is implied by any finding.
