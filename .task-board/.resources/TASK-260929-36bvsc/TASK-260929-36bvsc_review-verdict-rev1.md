# Merged review verdict — TASK-260929-36bvsc CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261006-1z552y_panel-verdict.md` (changes_requested), `TASK-261006-3gh4h9_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "sampled-receipt-remains-pending",
      "row": "snapshot contents",
      "invariant": "AC1: acknowledged/sampled completions must not be reported as pending work.",
      "mechanism": "codex-rs/core/src/session/pending_work.rs:71-80 unions store Queued/Leased without a mailbox entry. Production session/exec_completion_ack.rs:168-170 calls only InputQueue::acknowledge_runtime_lease (input_queue.rs:347-349), which removes the mailbox entry and bumps revision but never acknowledges the B receipt. CompletionReceiptStore therefore still returns the receipt as Queued. The test pending_work_tests.rs:179-182 manually leases and acknowledges the store, unlike production; its comment at :167 claiming production acknowledges both is false on this candidate. After actual mailbox acceptance the snapshot resurrects the sampled receipt as Queued indefinitely.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/session/pending_work_tests.rs",
          "command": "cd codex-rs && just test -p codex-core --lib -E 'test(snapshot_excludes_suspended_acknowledged_and_cancelled)'",
          "expected_failure": "Requested hosted attack, NOT executed here: narrow the existing fixture to match production by omitting its manual store lease/ack at lines 179-182. The existing snapshot.is_empty assertion at line 194 must fail because ack_id is still store-Queued. Then add an integration regression driving exec_completion_ack::acknowledge_submitted and reading via the real thread PendingWorkProvider; after accepted sampling, assert the receipt is absent. Static trace confirmed on exact candidate; no Rust runtime reproduction or exit code claimed.",
          "pinned_blobs": [
            "git-blob:d8177695f1d3e83b373f619e1f25b66b799a0ab1",
            "git-blob:f6faa89fb35efcff197e744fac78aee1a5bf4d6d",
            "git-blob:74d2e7752d8d1763744483d4007573af77824afc",
            "git-blob:31ac9c39b3b8454800f60643381776af9ba5b300"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261006-1z552y"
      ]
    },
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
          "evidence_kind": "static source-path assertion; not a runtime test",
          "pinned_blobs": [
            "git-blob:d8177695f1d3e83b373f619e1f25b66b799a0ab1",
            "git-blob:f6faa89fb35efcff197e744fac78aee1a5bf4d6d",
            "git-blob:74d2e7752d8d1763744483d4007573af77824afc",
            "git-blob:31ac9c39b3b8454800f60643381776af9ba5b300",
            "git-blob:c66b927f4c4dcbe433cd91883c4b0989da935c64"
          ]
        },
        {
          "test_file": "codex-rs/core/src/session/pending_work_tests.rs (requested new test production_acknowledgement_removes_pending_work)",
          "command": "just test -p codex-core production_acknowledgement_removes_pending_work",
          "expected_failure": "Through a real Session: reserve/arm/publish a receipt, enqueue and lease its runtime notification, record its fragment, drive acknowledge_submitted on server acceptance, read via the installed PendingWorkProvider; assert receipt absent. Candidate leaves it in queued. Test must not manually acknowledge the receipt store.",
          "executed": false,
          "pinned_blobs": [
            "git-blob:d8177695f1d3e83b373f619e1f25b66b799a0ab1",
            "git-blob:f6faa89fb35efcff197e744fac78aee1a5bf4d6d",
            "git-blob:74d2e7752d8d1763744483d4007573af77824afc",
            "git-blob:31ac9c39b3b8454800f60643381776af9ba5b300",
            "git-blob:c66b927f4c4dcbe433cd91883c4b0989da935c64"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261006-3gh4h9"
      ]
    }
  ],
  "notes": [
    "[TASK-261006-1z552y] {'id': 'snapshot-revision-not-coherent', 'row': 'revision and atomicity', 'text': 'pending_work.rs:40-51 releases the receipt-store lock, reads mailbox, then loads revision. Static schedule: read empty store at r; another thread reserves/arms a receipt (r+2); read empty mailbox; load r+2. Return empty at r+2 although the receipt is Armed. Subsequent nonempty snapshot can have the same revision. This is a hazard for revision-based waiting, but the explicit AC only demands transition bumps and Armed-to-Queued no-gap, not full snapshot linearizability. Request a barrier-driven provider test for this schedule and clarify/cohere revision semantics; no runtime reproduction executed, therefore nonblocking note.'}",
    "[TASK-261006-1z552y] {'id': 'atomicity-test-is-serialized', 'row': 'revision and atomicity', 'text': 'pending_work_tests.rs:445 uses default current_thread Tokio runtime. After the start barrier, synchronous publish_exit and try_list_pending do not overlap; the mailbox lock normally completes immediately and cooperative yields still cannot interrupt synchronous publish_exit. The test also calls build_snapshot directly with revision 0, not try_read_snapshot/provider, and ignores writer result. The store read under one lock statically protects Armed-to-Queued, but AC4 asks for a latch-driven concurrent-reader test. Hosted queued-exclusion mutant proves queued membership, not concurrent atomicity. Request an actual cross-thread latch-controlled provider test with explicit handling of expected contention; current concurrent atomicity execution claim is unverified.'}",
    "[TASK-261006-1z552y] {'id': 'change-size', 'text': 'git diff --stat: 1166 additions + 31 deletions, over the 800-line nonmechanical guideline. Smallest coherent stage: provider/API types plus goal-side tests (273 added lines), then core wiring/store/mailbox snapshot plus tests. Core implementation is tightly coupled through one revision; do not split state wiring across partially functional stages. This is a reviewability note, not a demonstrated behavior defect.'}",
    "[TASK-261006-1z552y] {'id': 'runtime-bound', 'text': 'Local builds and tests forbidden by panel brief. Hosted evidence accepted only for the named executed attacks; no claim that proposed attacks ran. The producer exclusion fixture differs from the actual acknowledgement path, so hosted success does not refute the static finding.'}",
    "[TASK-261006-3gh4h9] {'id': 'mixed-time-revision', 'text': 'pending_work.rs:41-54 reads receipt lists, mailbox entries and revision separately. A concurrent mutation may pair older contents with the newer revision. Not behaviorally reproduced; request a deterministic production-provider test snapshot_revision_matches_contents_during_mutation with latches between reads before making a stronger coherence claim.'}",
    "[TASK-261006-3gh4h9] {'id': 'atomicity-test-bound', 'text': 'armed_to_queued_is_atomic_for_concurrent_readers uses default tokio::test scheduling, synchronous store reads and an uncontended mailbox lock; it calls build_snapshot directly, not try_read_snapshot. Its start barrier does not force an interleaving inside the actual production read. Hosted mutant kill establishes queued-store inclusion, not complete concurrency coherence.'}",
    "[TASK-261006-3gh4h9] {'id': 'change-size', 'text': 'Diff: 1166 insertions, 31 deletions across 11 files, exceeding guidance. Snapshot API/provider plus its API tests can be one preparatory stage; shared revision and core snapshot wiring/tests form the dependent stage. Nonblocking review note, not an additional behavioral finding.'}"
  ],
  "surface_results": [
    {
      "row": "snapshot contents",
      "result": "broken",
      "evidence": "Static production-call trace above confirms acknowledged work is reintroduced from store Queued. Hosted run 37463583436 and narrowing runs 37463702577 (suspended admitted) / 37463635217 (queued excluded) cover membership/dedup but mask production acknowledgement by manually retiring the B receipt. Runtime confirmation of the newly identified path requested, not executed.",
      "reported_by": "TASK-261006-1z552y"
    },
    {
      "row": "revision and atomicity",
      "result": "held",
      "evidence": "Held for executed transition-bump attack: exact-tree hosted base 37463583436 and suspend_skips_revision_bump mutant 37463660857 killed by revision_increases_on_suspend. Store mutations bump while holding state lock; union covers both Armed and Queued. Named fourteen revision tests exist. This result does not attest coherent revision snapshots or genuinely concurrent AC4 execution; both limits are notes above.",
      "reported_by": "TASK-261006-1z552y"
    },
    {
      "row": "read failure and API boundary",
      "result": "held",
      "evidence": "Exact-tree hosted base 37463583436; provider_missing_mapped_to_empty mutant 37463609295 killed in core/small by read_failure_returns_explicit_error_not_empty_snapshot and goal_read_failure_is_explicit_error_not_empty. Static try_read_snapshot propagates both lock failures; read_pending_work preserves ProviderMissing/provider errors. Session installs weak-session provider; no Cargo dependency changes/core-to-goal edge introduced. Production provider contention end-to-end is not directly exercised by the new component tests.",
      "reported_by": "TASK-261006-1z552y"
    }
  ],
  "free_hunt": [
    "[TASK-261006-1z552y] {\"budget_minutes\": 5, \"result\": \"No additional blocking mechanism identified. Checked weak-session lifetime (no strong cycle), dependency direction, externally serialized/config/rollout/CLI surfaces (unchanged), model-visible context (no new injected fragment), Bazel source-file collection versus new ordinary .rs modules (no include_str/data dependency), revision coherence, and change size. Revision coherence and size recorded as bounded notes.\"}"
  ]
}
```
