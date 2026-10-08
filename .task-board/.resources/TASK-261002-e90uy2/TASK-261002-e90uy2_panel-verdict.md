# Panel B — revision 5 receipt-state-machine review

accept

Panel task: TASK-261002-e90uy2 — r141-panel-b-task-260929-u2i5rr-rev5.
Reviewed CR-TASK-260929-u2i5rr-5 without recording anything on its owning task.

Replay: base `0462dcc062b822bb8fff16cc31ce6eeab69823b9` plus the attached rev5 patch produced **exactly** `00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8` via `git write-tree`. No nested worktree, checkout, commit or source edit was used.

## Decision and bounds

The decision is whether rev5 addresses the round-2 findings and satisfies the inactive B1 state-machine contract. It does under the requested replay/static review. The existing 17 tests are retained and the three new tests plus deterministic source assertions cover all five prior finding classes. Scope is exactly the three authorized files; implementation bytes match rev4.

Review budget: 25 minutes total, up to 5 minutes for free hunt; one outcome document, no archive, no serial research prerequisite. Frozen input is the named candidate tree. Exit is this panel verdict; consumer is the orchestrator's merged recording review of B1, followed by existing B2 integration. No new implementation or research task is requested.

## Commands and real exits

Working directory was the assigned Story worktree. `IDX` below denotes `$PWD/.temp/TASK-261002-e90uy2-replay.idx`; no default index was modified. Each replay/gate command ran as a standalone process, without a pipeline.

| Command | Exit | Observed result |
|---|---:|---|
| `task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_change-request_rev5.patch --output .temp/TASK-260929-u2i5rr_change-request_rev5.patch` | 0 | Patch materialized |
| `GIT_INDEX_FILE="$IDX" git read-tree 0462dcc062b822bb8fff16cc31ce6eeab69823b9` | 0 | Base loaded |
| `GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-u2i5rr_change-request_rev5.patch` | 0 | Patch applied |
| `GIT_INDEX_FILE="$IDX" git write-tree` | 0 | Exact expected tree above |
| `python3 .temp/TASK-261002-e90uy2/audit.py` | 0 | Three-path scope; all three SHA-256 values equal validation manifest; implementation unchanged from rev4; 17/17 prior names preserved; 20/20 names match manifest |
| `git diff --check 0462dcc062b822bb8fff16cc31ce6eeab69823b9 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8` | 0 | No whitespace errors |
| `git diff e9a8095f146dd156b09351cc2af473781aa37272 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8 -- codex-rs/core/src/unified_exec/completion_receipt.rs codex-rs/core/src/unified_exec/completion_receipt_tests.rs` | 0 | Only 167 new test lines |
| `git grep -n 'CompletionReceiptStore' 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8 -- codex-rs ':!codex-rs/core/src/unified_exec/completion_receipt_tests.rs'` | 0 | Declaration/implementation only |

Additional read-only inspection used successful `git show`, `rg`, `sed`, `cat`, Python tarfile reads and task-specific board reads. No build or behavioral test ran here; there are no locally observed mutant exit codes. Producer manifest reports target guard, fmt, clippy and diff-check exits 0. Archive clippy tail reaches `Finished dev profile`, with three known restored upstream import warnings; those are not receipt defects. Attached hosted report supplies all four successful job conclusions for this exact tree.

Read/discovery anomalies, not gates: the initial query with unsupported `resources` field exited 1; it was replaced by supported task projections and direct read-only resource inspection. The first combined skill read exited 1 because the Claude skill path lacked `.roles/reviewer/role.md`; the installed `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md` was located and read successfully. `task-board resource list` printed help with exit 0 and was not treated as a resource inventory. No missing read was treated as absent evidence.

## Requested mutant assessment

All line citations below are candidate-tree lines in `codex-rs/core/src/unified_exec/`. These are **predicted failures by static inspection**, not measured kills. The execution command for each would be `just test -p codex-core -E 'test(completion_receipt)'`; it was intentionally not run.

| Mutant / refusal variant | Named test and decisive assertion | Static verdict |
|---|---|---|
| M12: remove terminal_error owner check | `terminal_history_refuses_foreign_owners_and_repeat_cancellation`, tests:511; foreign `lease_for_sampling`, resolve, publish, fail and ack must return ForeignOwner for all three terminal states | Fails: terminal phase error differs from ForeignOwner |
| M13: remove terminal status owner check | Same test, tests:562 | Fails: status exposes Ok(terminal status) instead of ForeignOwner |
| M14: map terminal cancel ForeignOwner to AlreadyTerminal | Same test, tests:566 | Fails: error equality distinguishes both variants |
| M15: delete oldest eviction | `terminal_history_evicts_only_the_oldest_after_64_outcomes`, tests:480 | Fails: first receipt remains Cancelled instead of UnknownReceipt |
| M15 narrowing: evict at 65 rather than 64 | Same test, tests:496-506 | Fails at oldest lookup after 65 retirements; early eviction also fails retained-entry loop |
| M12 generation-only exemption | Foreign owner helper tests:29 includes same thread/call and generation+1 | Fails for generation case on terminal operation errors |
| M13 generation-only exemption | Same helper and terminal status assertion | Fails for generation case on terminal status |
| M14 generation-only exemption | Same helper and terminal cancel assertion | Fails for generation case on cancel |
| Own terminal cancel returns Ok/raw error, or admits only Sampled | Same terminal-history test, tests:607-612 | Fails: all Sampled/InlineResult/Cancelled owner cancellations require AlreadyTerminal and preserved status |
| call-id `>` becomes `>=` | `owner_accepts_256_bytes_and_refuses_257`, tests:960 | Fails at 256-byte owner construction; 257-byte refusal remains explicit |
| M16: hard-code PushedCompletion in both lease and record | `terminal_stdin_and_pushed_sources_share_one_lease`, tests:730, assertions:748-763 | Fails deterministically at LeasedToSampling source, before ack; Sampled source also asserted. Happy-path tests:70 proves pushed attribution |

The previous five findings are closed at the requested static-assessment level: terminal-history-paths-untested, terminal-path-owner-gates-unguarded, terminal-history-bound-unguarded, owner-call-id-boundary-256 and sampling-source-attribution-nondeterministic.

## Surface sweep and free hunt

The supplied table has one row; **1/1 rows swept, 6/6 AC mappings inspected**. Surface result was persisted before the free hunt. The public entry point for this inactive leaf is the crate-visible receipt API; no tool/runtime integration is asserted.

AC1: happy path and second-claim refusal (tests:70,110). AC2: barriers force exit-first inline, exit-first arm and arm-first; duplicate reserved publication cannot overwrite retained completion (128,271,872). AC3: stale acknowledgment and stale fail cannot consume/requeue the newer claim (299,331). AC4: all four unsampled phases cancel with preserved reasons; terminal cancellation cannot rewrite outcomes (363,511). AC5: capacity refuses the next reservation and release admits another; terminal history and owner-byte bounds are tested (453,480,960). AC6: barrier race and deterministic lease handover enforce one consumed claim and correct source (730,771). Foreign active/terminal owner checks and poisoned-lock structured error are explicit (511,616,659,696,979).

Free hunt additionally traced cloned lease reuse, cancel/ack ordering, cancellation while Reserved already retains an exit, collision rejection against active and terminal IDs, eviction ordering, byte-length validation and mutex scope. Each transition holds the same mutex; no mutation can interleave between ownership lookup and retirement. No additional reproducible defect was identified. This is bounded static analysis, not exhaustive concurrency verification.

## Sources and outcome-scoped logbook

- Candidate blobs, pinned above: `completion_receipt.rs`, `completion_receipt_tests.rs`, `mod.rs`.
- Owning task's `description scope ac` projection: explicitly inactive B1; no watchers/mailbox yet.
- Attached `surface-table.md`, `final-plan.md` sections 5.1/5.4, `producer-brief.md`, `b1-rework-brief-rev5.md` and merged `TASK-260929-u2i5rr_review-verdict-rev4.md` define the scope and mutant set.
- `TASK-260929-u2i5rr_results.md` and `TASK-260929-u2i5rr_validation-rev5.tar.gz` manifest/logs: exact SHA-256 matches checked independently; historical mutant execution not reused as rev5 proof.
- `TASK-260929-u2i5rr_hosted-ci-rev5.md`: [relux-ci run 36987452652](https://github.com/relux-works/codex/actions/runs/36987452652), supplied exact-tree successful execution report.

Logbook: replay identity held; all requested mutant variants now meet concrete assertions by inspection; three unrelated import changes are absent; no product bytes changed since rev4. No file under the board control root was edited directly and no mutation targeted TASK-260929-u2i5rr. Evidence is attached only to this panel task. CI execution claims are attributed to supplied evidence, and static mutant predictions remain labeled.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "execution-bound",
      "text": "This panel performed replay, exact-blob inspection and static attacks only. No Rust build, test or mutant was executed. Held means held under the explicitly requested static panel with reused execution evidence, not an observed mutant kill. Current measured mutant executions: 0; statically mapped prior mutant/refusal variants: 11/11."
    },
    {
      "id": "hosted-evidence",
      "text": "Reused TASK-260929-u2i5rr_hosted-ci-rev5.md: commit 00726e16afb1f84c81717b3fe404c5965438b170, exact tree 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8, run 36987452652 reports success for lint, small, core and app-server. The panel brief reports 20 passing receipt tests; the attached summary itself contains job conclusions, not individual test rows. No fresh provider query was made. Historical mutant logs in the rev5 archive are not current mutant execution evidence."
    },
    {
      "id": "inactive-scope",
      "text": "The store has no non-test runtime caller; git grep finds only its declaration and implementation. This is expressly the inactive B1 scope. Reserve-before-launch, actual prompt membership, output retention, mailbox integration and transport acknowledgment remain B2/later obligations, not attested here."
    },
    {
      "id": "size",
      "text": "Candidate has 1534 added lines across exactly three allowed paths, including 998 test lines. This exceeds repository review-size guidance. Implementation is 532 physical lines before its test module, but under 500 nonblank/noncomment lines. Existing single coherent state-machine stage; nonblocking maintainability note, no new split prerequisite requested."
    },
    {
      "id": "free-hunt-bounds",
      "text": "Static free hunt checked cloned lease reuse, cancel/ack ordering, reserved-with-retained-exit cancellation, terminal eviction, UUID collision checks, byte-based owner bounds, lock scope and runtime callers. No additional defect found. UUID retry exhaustion is not injected, scheduler interleavings are not exhaustively modeled, and the test using MAX_COMPLETION_RECEIPTS as its loop bound would not detect coordinated changes to both active and terminal constants. These are stated bounds, not claims of absence."
    }
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "held",
      "reason": "All 6/6 AC rows have named receipt-API driving and refusal assertions in the exact candidate. Statically attacked early exit/arm ordering, duplicate publication, stale leases, cancellation, 64/65 capacity, foreign owners on active and terminal paths, shared-source claims and lock poisoning. New rev5 assertions defeat each requested mutant by direct control/data-flow inspection. Execution evidence is reused exact-tree hosted CI, not a new panel test run.",
      "evidence": [
        "completion_receipt_tests.rs:70-358",
        "completion_receipt_tests.rs:363-613",
        "completion_receipt_tests.rs:616-997",
        "TASK-260929-u2i5rr_hosted-ci-rev5.md"
      ]
    }
  ],
  "free_hunt": []
}
```
