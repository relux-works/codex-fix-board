# R141 panel A verdict — TASK-260929-u2i5rr CR-TASK-260929-u2i5rr-4 rev4 (non-recording)

Verdict: **accept**

## Replay tree check
Base `0462dcc062b822bb8fff16cc31ce6eeab69823b9` + patch `TASK-260929-u2i5rr_change-request_rev4.patch` through a temporary index
(`.temp/TASK-261002-3auvlm-replay.idx`, no nested worktree):
`git write-tree` printed `e9a8095f146dd156b09351cc2af473781aa37272` = expected candidate tree. MATCH.

## Commands run (all exit 0)
| Command | Exit |
| --- | ---: |
| `GIT_INDEX_FILE=$IDX git read-tree 0462dcc062…` | 0 |
| `task-board resource get TASK-260929-u2i5rr …_change-request_rev4.patch --output …` | 0 |
| `GIT_INDEX_FILE=$IDX git apply --cached …rev4.patch` | 0 |
| `GIT_INDEX_FILE=$IDX git write-tree` -> e9a8095f… | 0 |
| `git archive e9a8095f… codex-rs/core/src/unified_exec …registry.rs` / `git show e9a8095f…:…tests.rs` (read candidate) | 0 |
| `git grep` unused-import checks on the candidate tree (ToolCallSource, body_json(, ReasoningEffort) | 0 |

No cargo / just / build / test was run (per brief). Nothing was written on TASK-260929-u2i5rr (reads only: resource get, q get).
Hosted `relux-ci` result (`TASK-260929-u2i5rr_hosted-ci-rev4.md`) was NOT yet attached when I looked ("resource not found"); execution evidence for
the 17 completion_receipt tests is therefore still pending. The recording step must wait for it, as the orchestrator already planned.

## Round-1 findings F1-F3: statically re-checked against the named tests
Each of the four tests listed in the results note exists in the candidate and fails against the corresponding narrowing mutant by construction (read, not executed):
- F1/M1 `lease_for_sampling` owner gate: `completion_receipt_foreign_owner_is_refused_on_resolve_and_lease` leases a Queued receipt with 3 foreign owners (thread, generation, call) and expects `ForeignOwner`; without the gate the first foreign lease succeeds -> assert fails.
- F1/M2 `resolve_initial_response` owner gate: same test, Reserved receipt, foreign `Arm` expects `ForeignOwner`; without the gate it returns `Armed`.
- F1/M10, M11 `fail_sampling` / `acknowledge_sampled` owner gate: `completion_receipt_foreign_lease_is_refused_on_fail_and_acknowledge` forges a lease with a foreign owner (token and source unchanged) so only the owner gate can refuse.
- F2/M4 stale fail token: `completion_receipt_stale_failed_lease_cannot_requeue_a_new_lease` calls `fail_sampling(first_lease)` after a re-lease, expects `StaleLease`, live lease intact, second lease still acks.
- F3/M7 duplicate exit while Reserved: `completion_receipt_duplicate_exit_while_reserved_preserves_first_completion` expects `InvalidTransition{Reserved}` and that the FIRST completion is what InlineResult and Queued later yield (both branches).
All 13 round-1 tests remain; suite is 17 `#[test]`s (counted). Code is byte-identical to the rev2 tree per the results note, and the replay confirms rev4's tree is the expected one.

## AC coverage (static): 6 of 6 rows have a driving test and a refusal test
1 happy path / second claim -> AlreadyConsumed; 2 both orders forced with barriers / InlineResult lease -> InvalidTransition{InlineResult}; 3 lease failure requeue / stale ack and stale fail; 4 cancel from Reserved, Armed, Queued, Leased; 5 capacity 64/65 + slot reuse; 6 stdin vs pushed share one lease and a 3-party barrier race.
One mutex guards all state, so every operation is linearizable; no lock-ordering or deadlock surface exists (single lock, no callbacks under lock).

```verdict-findings
{
  "findings": [
    {
      "id": "terminal-history-paths-untested",
      "row": "concurrency state machine",
      "invariant": "Terminal history is bounded (64), and a foreign owner learns nothing about a retired receipt; cancel on an already-terminal receipt is refused (AlreadyTerminal).",
      "mechanism": "completion_receipt.rs `retire` evicts via `pop_front` at MAX_TERMINAL_RECEIPTS; `terminal_error` and the terminal arm of `status` return ForeignOwner for a foreign owner; `cancel` maps any terminal outcome except Unknown/Foreign to AlreadyTerminal. The test file has zero occurrences of AlreadyTerminal, UnknownReceipt, MAX_TERMINAL_RECEIPTS, and every ForeignOwner assertion targets an ACTIVE receipt (Reserved/Queued/Leased). Static analysis only: narrowing mutants (drop the pop_front eviction; drop the owner comparison in terminal_error/status terminal arm; make cancel on a terminal receipt return Ok or the raw terminal error) are predicted to survive the 17-test suite. Not executed (no builds allowed in this panel).",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/unified_exec/completion_receipt_tests.rs",
          "command": "static: grep -nE 'AlreadyTerminal|UnknownReceipt|MAX_TERMINAL' completion_receipt_tests.rs (0 hits); grep -n ForeignOwner shows only active-receipt cases",
          "expected_failure": "a test retiring 65 receipts must see the oldest return UnknownReceipt; a foreign owner on a Sampled/Cancelled receipt must get ForeignOwner; cancel after Sampled/Cancelled must return AlreadyTerminal. Mutants of these three gates are predicted to survive today."
        }
      ],
      "severity": "robustness",
      "repeat-of": "none"
    },
    {
      "id": "owner-call-id-boundary-256",
      "row": "concurrency state machine",
      "invariant": "ReceiptOwner accepts call ids of 1..=256 bytes and refuses empty or >256.",
      "mechanism": "`call_id.len() > MAX_CALL_ID_BYTES`: the test checks only empty and 257 bytes. A narrowing mutant (`>=`, rejecting a valid 256-byte id) is predicted to survive. Static analysis only, not executed.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/unified_exec/completion_receipt_tests.rs",
          "command": "static: completion_receipt_owner_requires_a_bounded_call_id asserts only \"\" and 257 bytes",
          "expected_failure": "a 256-byte call id must be accepted; the `>=` mutant is predicted to survive."
        }
      ],
      "severity": "robustness",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Replay: write-tree equals expected candidate tree e9a8095f146dd156b09351cc2af473781aa37272.",
    "Hosted relux-ci result for rev4 was not attached when reviewed; no local execution evidence for the 17 completion_receipt tests exists in this panel. The orchestrator's recording step should wait for TASK-260929-u2i5rr_hosted-ci-rev4.md as planned.",
    "Scope: the patch has 3 import-only deletions outside the task's stated scope (tools/registry.rs ToolCallSource, tests/suite/openai_file_mcp.rs body_json matcher, tests/suite/scenarios.rs ReasoningEffort). I verified on the candidate tree that each removed import has no remaining use (registry_tests.rs uses `use super::*` but never names ToolCallSource; body_json( is not called, only set_body_json; ReasoningEffort not referenced). They are unused at base 0462dcc062 too, so the deletions are behavior-neutral; they are presumably there to keep the clippy -D warnings lane green. Recording reviewer may want them split out or acknowledged as out-of-scope.",
    "Size: 1367 insertions (535 impl incl. test-mod hook + 831 tests). Non-test impl is 466 non-blank non-comment lines (<500). Total exceeds the AGENTS.md 800-line guidance but is test-dominated and a single coherent stage; no split needed.",
    "Bounds already stated by the producer and acceptable for a stage-2a leaf: Reserved slots have no timeout (caller contract for B2); evicted terminal ids report UnknownReceipt (still a refusal); `#![allow(dead_code)]` covers the intentionally unwired API.",
    "Cloneable SamplingLease: clones share the token, so double use is refused by the token/consumed checks (stale or AlreadyConsumed); not a bypass.",
    "The `source` equality in fail_sampling/acknowledge_sampled is redundant given the token (equivalent-mutant candidate); not counted."
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "held",
      "detail": "Exactly-one-terminal outcome, no lost/duplicated exit, no slot leak, capacity 64 before launch, owner gates on all 7 entry points (status/publish/resolve/lease/fail/ack/cancel), stale tokens, duplicate exit on Reserved and on Queued, InlineResult never leased, cancel from Reserved/Armed/Queued/Leased, stdin-vs-pushed single claim, poisoned lock -> LockPoisoned all held statically and are guarded by named tests that would fail against narrowing mutants (F1-F3 re-checked). Two robustness test gaps are reported above; no behavioral defect found."
    }
  ],
  "free_hunt": [
    "Single Mutex linearizes every operation; checked for lock held across callbacks or re-entrancy: none.",
    "resolve_initial_response two-phase (match then mutate) runs under the same guard, so no TOCTOU between decision and write; the `None` fallbacks after get_mut are unreachable.",
    "Exit-after-cancel (watcher race): publish_exit on a retired receipt returns the terminal error (Cancelled{reason}), never resurrects the receipt; behavior correct, untested (covered by finding terminal-history-paths-untested).",
    "UUID id reuse after terminal eviction is only guarded for retained entries; negligible with v4 randomness, and owner gates still apply.",
    "Cancel while Leased followed by in-flight ack returns Cancelled, so a cancelled receipt cannot be consumed (tested).",
    "Registry/test import deletions checked for hidden uses via git grep on the candidate tree: none."
  ]
}
```
