# Merged review verdict — TASK-260929-u2i5rr CR revision 4 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261002-3auvlm_panel-verdict.md` (changes_requested), `TASK-261002-3d4gn2_panel-verdict.md` (accept), `TASK-261002-3ptwun_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

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
      "repeat-of": "none",
      "reported_by": [
        "TASK-261002-3auvlm"
      ]
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
      "repeat-of": "none",
      "reported_by": [
        "TASK-261002-3auvlm"
      ]
    },
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
      "repeat-of": "owner-gate-unguarded-on-lease-and-resolve (rev1 F1), sibling path",
      "reported_by": [
        "TASK-261002-3ptwun"
      ]
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
      "repeat-of": "none",
      "reported_by": [
        "TASK-261002-3ptwun"
      ]
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
      "repeat-of": "none",
      "reported_by": [
        "TASK-261002-3ptwun"
      ]
    }
  ],
  "notes": [
    "[TASK-261002-3auvlm] Replay: write-tree equals expected candidate tree e9a8095f146dd156b09351cc2af473781aa37272.",
    "[TASK-261002-3auvlm] Hosted relux-ci result for rev4 was not attached when reviewed; no local execution evidence for the 17 completion_receipt tests exists in this panel. The orchestrator's recording step should wait for TASK-260929-u2i5rr_hosted-ci-rev4.md as planned.",
    "[TASK-261002-3auvlm] Scope: the patch has 3 import-only deletions outside the task's stated scope (tools/registry.rs ToolCallSource, tests/suite/openai_file_mcp.rs body_json matcher, tests/suite/scenarios.rs ReasoningEffort). I verified on the candidate tree that each removed import has no remaining use (registry_tests.rs uses `use super::*` but never names ToolCallSource; body_json( is not called, only set_body_json; ReasoningEffort not referenced). They are unused at base 0462dcc062 too, so the deletions are behavior-neutral; they are presumably there to keep the clippy -D warnings lane green. Recording reviewer may want them split out or acknowledged as out-of-scope.",
    "[TASK-261002-3auvlm] Size: 1367 insertions (535 impl incl. test-mod hook + 831 tests). Non-test impl is 466 non-blank non-comment lines (<500). Total exceeds the AGENTS.md 800-line guidance but is test-dominated and a single coherent stage; no split needed.",
    "[TASK-261002-3auvlm] Bounds already stated by the producer and acceptable for a stage-2a leaf: Reserved slots have no timeout (caller contract for B2); evicted terminal ids report UnknownReceipt (still a refusal); `#![allow(dead_code)]` covers the intentionally unwired API.",
    "[TASK-261002-3auvlm] Cloneable SamplingLease: clones share the token, so double use is refused by the token/consumed checks (stale or AlreadyConsumed); not a bypass.",
    "[TASK-261002-3auvlm] The `source` equality in fail_sampling/acknowledge_sampled is redundant given the token (equivalent-mutant candidate); not counted.",
    "[TASK-261002-3d4gn2] {'id': 'execution-bound', 'text': 'Panel B ran replay and static checks only, as explicitly required. Reused executed attacks are identified below; no cargo, just, build, test, or mutant was executed in this panel. The hosted-ci-rev4 artifact was absent at the successful directory inspection. Current hosted execution remains unknown and is a required recording-reviewer gate, not a passing result inferred from local lint.'}",
    "[TASK-261002-3d4gn2] {'id': 'inactive-api-bound', 'text': 'The candidate exports the module but has no runtime callers outside its tests. This is explicitly required by the B1 description; launch-before-reserve, process watchers, mailbox delivery and sampling integration belong to B2/later leaves. Public entry point here means the crate-visible CompletionReceiptStore API.'}",
    "[TASK-261002-3d4gn2] {'id': 'retention-bound', 'text': 'Terminal history evicts its oldest entry at 64; old handles return UnknownReceipt. Reserved slots require caller cancellation if no decision arrives. Neither bounded history nor caller-driven cleanup proves eventual completion for an abandoned reservation.'}",
    "[TASK-261002-3d4gn2] {'id': 'scope-and-size', 'text': 'The six-path patch includes three unused-import removals outside the declared three-path scope; no remaining exact identifier use exists in any affected file. The overall diff is 1367 insertions and 3 deletions, above repository review-size guidance. Implementation is 532 physical lines before cfg(test), or 466 nonblank/noncomment lines; producer reports 468 using a different count. These are scope/maintainability notes, not reproduced behavior defects.'}",
    "[TASK-261002-3ptwun] Replay: write-tree equals e9a8095f146dd156b09351cc2af473781aa37272 (exit 0 at every step).",
    "[TASK-261002-3ptwun] Hosted relux-ci result TASK-260929-u2i5rr_hosted-ci-rev4.md was NOT attached when this review ran (resource not found). The completion_receipt unit tests run only on that lane; this review gives no execution evidence for them. The recording step should wait for it, as the orchestrator note says. Rev3 last ran the 17-test suite green locally per the results note (not re-verified here).",
    "[TASK-261002-3ptwun] Scope: the patch edits three files outside the task Scope (registry.rs, openai_file_mcp.rs, scenarios.rs: one unused-import removal each). They are compile-safe by grep, and they are the three entries in relux-ci.yml KNOWN_WARNINGS, which become stale but harmless entries. This is a small scope overrun against 'completion_receipt.rs + tests + module export only'; accept or move it to a separate change at the recorder's discretion. It risks trivial merge conflicts with upstream for these three lines.",
    "[TASK-261002-3ptwun] cancel() on an already-terminal receipt returns AlreadyTerminal; no test pins that (cancel after Sampled/Cancelled/InlineResult). A silent Ok would not corrupt state because the receipt is no longer in `active`, so this is a note, not a finding. Could be added to the terminal-path test above.",
    "[TASK-261002-3ptwun] ReceiptOwner::new boundary: only '' and 257 bytes are tested; a 256-byte id (accepted) is not, so a `>`->`>=` mutation on MAX_CALL_ID_BYTES survives. Low value; add one positive 256-byte case if the new test file is touched anyway.",
    "[TASK-261002-3ptwun] Barrier-forced 'both orders' tests are sequentially ordered around one mutex, so they prove ordering semantics but not interleaving; with a single lock held across each transition that is sufficient for this stage.",
    "[TASK-261002-3ptwun] Stated bounds carried from rev1: terminal history capped at 64 (evicted id -> UnknownReceipt); Reserved slots have no timeout, so a caller that never decides holds a slot until cancel (caller contract for sibling B2); module is not wired to launch/watcher/mailbox.",
    "[TASK-261002-3ptwun] argument-comment-lint: `uncommented_anonymous_literal_argument` is allow-by-default and not part of relux-ci, so literal arguments such as receipt_owner(1) are not a finding."
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "broken",
      "detail": "Behavior held under every static attack and rev1 F1-F3 are fixed with killing tests; broken only in the test-guard sense: owner gates on the terminal-history path (terminal_error :245, status :525, cancel :505), the terminal-history bound (:256) and stdin source attribution (:421-430) are unguarded by any test. Findings: terminal-path-owner-gates-unguarded, terminal-history-bound-unguarded, sampling-source-attribution-nondeterministic.",
      "reported_by": "TASK-261002-3ptwun"
    }
  ],
  "free_hunt": [
    "[TASK-261002-3auvlm] Single Mutex linearizes every operation; checked for lock held across callbacks or re-entrancy: none.",
    "[TASK-261002-3auvlm] resolve_initial_response two-phase (match then mutate) runs under the same guard, so no TOCTOU between decision and write; the `None` fallbacks after get_mut are unreachable.",
    "[TASK-261002-3auvlm] Exit-after-cancel (watcher race): publish_exit on a retired receipt returns the terminal error (Cancelled{reason}), never resurrects the receipt; behavior correct, untested (covered by finding terminal-history-paths-untested).",
    "[TASK-261002-3auvlm] UUID id reuse after terminal eviction is only guarded for retained entries; negligible with v4 randomness, and owner gates still apply.",
    "[TASK-261002-3auvlm] Cancel while Leased followed by in-flight ack returns Cancelled, so a cancelled receipt cannot be consumed (tested).",
    "[TASK-261002-3auvlm] Registry/test import deletions checked for hidden uses via git grep on the candidate tree: none.",
    "[TASK-261002-3ptwun] Checked all state transitions for check-then-act gaps: each public method takes the single lock once and mutates inside it; none releases between read and write.",
    "[TASK-261002-3ptwun] Checked slot accounting: active.len() counts Reserved/Armed/Queued/Leased only; retire() removes from active for Sampled, InlineResult and Cancelled, so every terminal outcome frees a slot, and the reserve ID-uniqueness loop checks both active and terminal.",
    "[TASK-261002-3ptwun] Checked lease forging: SamplingLease has private fields and a fresh v4 UUID token per lease; the only way to forge one is inside the module's own tests.",
    "[TASK-261002-3ptwun] Checked error mapping for lease/ack/fail on terminal receipts: Sampled -> AlreadyConsumed, Cancelled -> Cancelled{reason}, InlineResult -> InvalidTransition; consistent with the tests that exist.",
    "[TASK-261002-3ptwun] Checked Reserved-with-retained-exit then Cancel: the retained completion is dropped with the cancellation by design (explicit terminal reason), not lost silently.",
    "[TASK-261002-3ptwun] Checked that removing the three unused imports cannot break compilation of registry_tests.rs (`use super::*` but only a fully qualified ToolCallSource path), openai_file_mcp.rs or scenarios.rs by grep on the candidate and base blobs.",
    "[TASK-261002-3ptwun] Checked Cargo lints: expect_used/unwrap_used are denied in the workspace but clippy.toml sets allow-expect-in-tests/allow-unwrap-in-tests, so the test file's `.expect(...)` calls are fine; production code in the module uses no unwrap/expect."
  ]
}
```


## Recording reviewer confirmation (RUN-261002-154951)

Merge check: every finding from panels 3auvlm (2) and 3ptwun (3) is present in the merged findings array (5 findings, unioned by distinct mechanism); panel 3d4gn2 (accept) raised no findings; the single surface row `concurrency state machine` is carried with its worst panel result (`broken`); all panel notes and free-hunt entries are retained. Merge accepted as correct. No findings added by this run. Verdict: changes_requested.
