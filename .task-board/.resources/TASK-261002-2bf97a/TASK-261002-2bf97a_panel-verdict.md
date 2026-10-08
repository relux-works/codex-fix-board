# Panel A verdict — TASK-260929-u2i5rr CR-TASK-260929-u2i5rr-5 rev5 (non-recording)

Verdict: changes_requested

## Replay
- Base `0462dcc062b822bb8fff16cc31ce6eeab69823b9`, temporary index `.temp/TASK-261002-2bf97a-replay.idx`.
- `git read-tree` exit 0; `task-board resource get ... rev5.patch` exit 0; `git apply --cached` exit 0; `git write-tree` exit 0 printing `00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8`, equal to the expected candidate tree. Match.
- Patch touches exactly 3 paths: `completion_receipt.rs`, `completion_receipt_tests.rs`, `unified_exec/mod.rs` (one added line `pub(crate) mod completion_receipt;`). The 3 out-of-scope lint edits are gone.
- Hosted evidence read: `TASK-260929-u2i5rr_hosted-ci-rev5.md` (tree 00518744..., run 36987452652, conclusion success; small/lint/app-server/core all success). I ran no cargo/just/build/test.

## Commands run (all exit 0)
task-board set_status on my own task; git read-tree; task-board resource get (patch, surface-table.md, verdict4, hosted-ci-rev5); git apply --cached; git write-tree; git show of the candidate files; static reading and grep of the candidate tests.

## Rev4 mutants, judged by reading (static; not executed)
| Mutant | Fails a test now? | By |
| --- | --- | --- |
| M15 delete the `pop_front` eviction (also: `==`->`>`, const 63/128, `pop_back`) | yes | `terminal_history_evicts_only_the_oldest_after_64_outcomes`: status(receipts[0]) must be UnknownReceipt and receipts[1..] must stay Cancelled |
| M12 drop owner gate in `terminal_error` | yes | `terminal_history_refuses_foreign_owners_and_repeat_cancellation`: foreign resolve/publish/lease/fail/ack on Sampled, InlineResult and Cancelled receipts must be ForeignOwner (forged lease with real receipt_id and foreign owner covers fail/ack) |
| M13 drop owner gate in terminal branch of `status` | yes | same test, `status(receipt, foreign)` |
| M14 drop `ForeignOwner` passthrough in `cancel` | yes | same test, foreign cancel must be ForeignOwner, not AlreadyTerminal |
| AlreadyTerminal (cancel on terminal by owner returns Ok or raw error) | yes | same test, owner cancel on all 3 terminal kinds must be AlreadyTerminal, status unchanged |
| 256-byte boundary (`>` -> `>=`, `>` -> `> 257`, drop `is_empty`) | yes | `owner_accepts_256_bytes_and_refuses_257` plus the empty-id test |
| M16 lease records PushedCompletion regardless of `source` | yes, deterministically | `terminal_stdin_and_pushed_sources_share_one_lease` now asserts `LeasedToSampling{TerminalStdinOutput}` and `Sampled{TerminalStdinOutput}`; a one-sided source mutation also trips the `source == lease.source` check in acknowledge |

All five rev4 findings are closed on the static read, and the hosted lane ran the 20 tests green.

## New finding (one)
`resolve_initial_response` has a catch-all arm `(phase, _) => InvalidTransition` for active receipts that are not Reserved. No test calls it with the legitimate owner on an Armed, Queued or LeasedToSampling receipt. I checked every call site: lines 59, 83, 152, 191, 220, 279, 293, 390, 401, 531, 678, 891 and 919 are all on Reserved receipts, and lines 578 and 669 use foreign owners. A mutant `(phase, _) => Action::Armed` (or `Action::Queued`) compiles, keeps all 20 tests green by reading, and a second `Arm` on a Queued receipt would overwrite `Queued(completion)` with `Armed`. That loses the finalized exit, which is the core invariant of AC2. The same untested-gate class applies to `Arm` or `InlineResult` after Armed. The fix is one small test.

```verdict-findings
{
  "findings": [
    {
      "id": "resolve-initial-response-active-nonreserved-arm-unguarded",
      "row": "concurrency state machine",
      "invariant": "A second or late initial-response decision on an active receipt that is no longer Reserved is refused with InvalidTransition and never overwrites Queued/Leased/Armed state, so a retained or queued exit is never lost.",
      "mechanism": "completion_receipt.rs resolve_initial_response, arm `(phase, _) => return Err(InvalidTransition{actual: phase.status()})`. No test calls resolve_initial_response with the legitimate owner on an Armed, Queued or LeasedToSampling receipt (all owner-matching call sites are on Reserved receipts; the terminal cases go through terminal_error, not this arm). A mutant that turns this arm into `Action::Armed` or `Action::Queued(..)` overwrites Queued(completion) with Armed, silently losing the exit. Static analysis only; not executed.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/unified_exec/completion_receipt_tests.rs",
          "command": "Mutant (static, not run): in resolve_initial_response replace the `(phase, _) => { return Err(...) }` arm body with `Action::Armed`. Then `just test -p codex-core -E 'test(completion_receipt)'`.",
          "expected_failure": "Add a test: after `queued_receipt`, `resolve_initial_response(id, &owner, Arm)` and `(.., InlineResult)` must return Err(InvalidTransition{actual: Queued}); after an Arm, a second Arm and an InlineResult must return Err(InvalidTransition{actual: Armed}); after a lease the same calls return Err(InvalidTransition{actual: LeasedToSampling{..}}); status is unchanged and the lease still acknowledges the original completion. The mutant turns it red; today it survives by reading."
        }
      ],
      "severity": "robustness",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Hosted relux-ci for the exact rev5 tree is attached and green (run 36987452652); local execution was not re-run in this panel.",
    "Smaller untested arms, not counted as findings: cancel/publish_exit/lease on an evicted id return UnknownReceipt via the same `terminal_error` None arm, but only `status` asserts UnknownReceipt; a mutant mapping `cancel`'s UnknownReceipt arm to AlreadyTerminal survives by reading. publish_exit on a LeasedToSampling receipt (the `phase =>` arm) is untested but shares the arm with the Queued case that is tested.",
    "The sampling race test is ordered by barriers around one mutex, so it proves linearization semantics, not interleaving; sufficient for a single-lock stage-2a leaf.",
    "Reserved slots have no timeout (caller contract for B2); `#![allow(dead_code)]` covers the intentionally unwired API; terminal history is bounded at 64 and evicted ids report UnknownReceipt."
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "held except the one finding above: replay exact; capacity 64/65 and slot release, both exit/decision orders, stale lease and lease failure, cancel from each unsampled state, double sample, stdin vs pushed race, generation/thread/call mismatch on active and terminal receipts, terminal history bound, poisoned lock and the call-id bound all have tests that fail under the narrowing mutants I checked; the one gap is the non-Reserved arm of resolve_initial_response"
    }
  ],
  "free_hunt": [
    "Slot accounting: retire removes from `active`, so Sampled/InlineResult/Cancelled free the slot; reserve checks `active.len() >= 64`; terminal entries do not consume capacity. Held.",
    "ReceiptId collision: reserve checks active and terminal before insert. Held; IdGenerationFailed is not reachable by test.",
    "Lease token is a fresh Uuid per lease; clone sharing is refused by token/consumed checks; the redundant `source` equality is an equivalent-mutant candidate.",
    "publish_exit after InlineResult or Cancelled returns a structured error rather than silently dropping; the caller owns the consequence in B2."
  ]
}
```
