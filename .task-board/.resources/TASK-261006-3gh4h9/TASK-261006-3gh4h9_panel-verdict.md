# Panel B — CR-TASK-260929-36bvsc-1 revision 1

changes_requested

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus attached rev1 patch produced exactly `0edaf3a0edd354ef941f7e5d0f92bd0e44ed8f1d`. Temporary index only; no checkout, builds, tests, commits, or source edits. No mutation on TASK-260929-36bvsc.

Review bounds: decision is panel acceptance of this CR, grammar precondition not applicable (no new wire grammar), one text outcome, no serial research prerequisites, at most 30 minutes static review plus 5 minutes free hunt. Consuming slice is the existing snapshot API, followed by the separately scoped E2 waiting policy. Authoritative evidence is candidate blobs, the source task AC/surface table, and attached hosted precheck 2; no internet sources needed.

## Command evidence

Direct replay commands, each exit 0:

- `task-board resource get TASK-260929-36bvsc TASK-260929-36bvsc_change-request_rev1.patch --output .temp/TASK-260929-36bvsc_change-request_rev1.patch`
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-3gh4h9-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b`
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-3gh4h9-replay.idx" git apply --cached .temp/TASK-260929-36bvsc_change-request_rev1.patch`
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-3gh4h9-replay.idx" git write-tree` → expected tree above.

Readiness: git 2.54.0, rg 15.2.0, Python 3.14.7 available; task-board help exit 0 (saved tool-readiness.log). Initial skill-search aggregate exit 2 because some searched directories were absent; recovered using explicit skill paths. Initial board projections containing `resources` were rejected, and positional scoped schema query was rejected; these are discovery failures, not gates. Corrected AC/notes/checklist reads succeeded. Candidate `git show`, `git diff`, and caller searches succeeded (exit 0). No passing runtime result is claimed from these reads.

Static acknowledgement attack: standalone `python3 -` exit **1**, expected red. It reads the exact candidate blobs with `git show`, checks the production path and queued-union branch, then asserts receipt-store acknowledgement wiring is present. Output: `Exact candidate static trace: acknowledge_submitted -> mailbox-only acknowledge; snapshot still unions store Queued.` Assertion: `production sampling acceptance never retires the queued receipt-store claim`. This is an executed source-path assertion, NOT a Rust behavioral execution. The source trace supports the finding; the requested real-entry regression below remains unrun locally due to the explicit no-build rule.

Exact static attack script (run through python3 stdin):

    import subprocess
    T='0edaf3a0edd354ef941f7e5d0f92bd0e44ed8f1d'
    def blob(p): return subprocess.check_output(['git','show',f'{T}:{p}'],text=True)
    a=blob('codex-rs/core/src/session/exec_completion_ack.rs')
    q=blob('codex-rs/core/src/session/input_queue.rs')
    p=blob('codex-rs/core/src/session/pending_work.rs')
    f=a.split('pub(crate) async fn acknowledge_submitted(',1)[1].split('\npub(crate)',1)[0]
    g=q.split('pub(crate) async fn acknowledge_runtime_lease(',1)[1].split('\n    }',1)[0]
    assert 'acknowledge_runtime_lease(lease)' in f
    assert 'runtime_notifications.lock().await.acknowledge(lease)' in g
    assert 'for receipt_id in store_lists.queued' in p
    print('Exact candidate static trace: acknowledge_submitted -> mailbox-only acknowledge; snapshot still unions store Queued.')
    assert 'acknowledge_pushed_completion' in f or 'acknowledge_sampled' in f, 'production sampling acceptance never retires the queued receipt-store claim'

Reused execution evidence, not rerun by this panel: `TASK-260929-36bvsc_hosted-precheck-2.md` pins tree above and snapshot 84aa9a3f; run 37463583436 reports app-server/lint/core/small success. Mutant runs 37463609295, 37463635217, 37463660857, 37463702577 report intended test failures, 4/4 killed. The summary does not supply numeric process exit codes for hosted mutants; they are failing outcomes, not passes. Truncated local validation is not relied upon. Precheck 1 mutant evidence is void because its baseline was red.

Artifact structure verification: standalone Python JSON/row/field validation exit 0; exactly one verdict-findings block and 3/3 unique surface rows.

## Ordered sweep and bounded free hunt

1. **snapshot contents — broken.** Static production acknowledgement trace below contradicts the exclusion invariant. Hosted exclusion mutants are useful but the test manually updates both stores; it does not refute this defect.
2. **revision and atomicity — held within named attacks.** Hosted revision tests and suspend_skips_revision_bump (37463660857), plus store_queued_excluded_from_snapshot (37463635217), exercise the declared transitions and no-gap union. Broader coherence remains a note.
3. **read failure and API boundary — held within named attacks.** Hosted provider_missing_mapped_to_empty (37463609295) is killed by core and goal read-error tests. Nonblocking read errors propagate; session.rs:1819 installs the provider with weak ownership. No new core→goal dependency.

Free hunt examined production callers, terminal-stdin/release divergence, separately sampled revision, test scheduling, external API compatibility and change size. No additional reproduced runtime finding. No local runtime tests were run or promised. AC1 fails the static production path; AC2/AC4 retain cited hosted evidence with the concurrency bound below; AC3 and AC5 retain cited hosted/API evidence. E2 policy remains out of scope.

Logbook entry (task-scoped; no control-root edit): production sampling acceptance only removes the mailbox entry, while the new snapshot also considers receipt-store Queued pending. Existing exclusion test manually retires both stores. Request a real session acknowledgement regression on the same leaf, not another research harness. No accept/reject/status/handoff operation was made on the source task.

```verdict-findings
{
  "findings": [
    {
      "id": "acknowledged-store-claim-still-pending",
      "row": "snapshot contents",
      "invariant": "Acknowledged completions must not remain in pending-work snapshots (AC1).",
      "mechanism": "codex-rs/core/src/session/exec_completion_ack.rs:169 calls InputQueue::acknowledge_runtime_lease (input_queue.rs:347), which only removes RuntimeMailbox entries (runtime_mailbox.rs:239-250). No production caller of UnifiedExecProcessManager::acknowledge_pushed_completion exists. The receipt remains Queued in the receipt store, and pending_work.rs:74-78 reinserts it even after mailbox acknowledgement. pending_work_tests.rs:170-182 manually acknowledges both stores and masks the production divergence.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/session/exec_completion_ack.rs + input_queue.rs + pending_work.rs (exact candidate static trace)",
          "command": "python3 - < static attack script printed above",
          "expected_failure": "AssertionError: production sampling acceptance never retires the queued receipt-store claim",
          "exit_code": 1,
          "evidence_kind": "static source-path assertion; not a runtime test"
        },
        {
          "test_file": "codex-rs/core/src/session/pending_work_tests.rs (requested new test production_acknowledgement_removes_pending_work)",
          "command": "just test -p codex-core production_acknowledgement_removes_pending_work",
          "expected_failure": "Through a real Session: reserve/arm/publish a receipt, enqueue and lease its runtime notification, record its fragment, drive acknowledge_submitted on server acceptance, read via the installed PendingWorkProvider; assert receipt absent. Candidate leaves it in queued. Test must not manually acknowledge the receipt store.",
          "executed": false
        }
      ],
      "severity": "bypass",
      "repeat-of": "none"
    }
  ],
  "notes": [
    {
      "id": "mixed-time-revision",
      "text": "pending_work.rs:41-54 reads receipt lists, mailbox entries and revision separately. A concurrent mutation may pair older contents with the newer revision. Not behaviorally reproduced; request a deterministic production-provider test snapshot_revision_matches_contents_during_mutation with latches between reads before making a stronger coherence claim."
    },
    {
      "id": "atomicity-test-bound",
      "text": "armed_to_queued_is_atomic_for_concurrent_readers uses default tokio::test scheduling, synchronous store reads and an uncontended mailbox lock; it calls build_snapshot directly, not try_read_snapshot. Its start barrier does not force an interleaving inside the actual production read. Hosted mutant kill establishes queued-store inclusion, not complete concurrency coherence."
    },
    {
      "id": "change-size",
      "text": "Diff: 1166 insertions, 31 deletions across 11 files, exceeding guidance. Snapshot API/provider plus its API tests can be one preparatory stage; shared revision and core snapshot wiring/tests form the dependent stage. Nonblocking review note, not an additional behavioral finding."
    }
  ],
  "surface_results": [
    {
      "row": "snapshot contents",
      "result": "broken",
      "finding_ids": [
        "acknowledged-store-claim-still-pending"
      ],
      "evidence": "Exact candidate static acknowledgement trace, exit 1; hosted suspension/queued mutants do not exercise production acceptance wiring."
    },
    {
      "row": "revision and atomicity",
      "result": "held",
      "evidence": "Hosted 37463583436 revision and atomicity tests; 37463660857 suspend mutant and 37463635217 queued-union mutant killed. Scope limited to those attacks."
    },
    {
      "row": "read failure and API boundary",
      "result": "held",
      "evidence": "Hosted 37463609295 provider-missing mutant killed in core and goal; installed provider and error propagation statically traced."
    }
  ],
  "free_hunt": []
}
```
