# R141 panel A — thread pending-work snapshot, revision 1

changes_requested

Read-only panel of CR-TASK-260929-36bvsc-1. No mutation, verdict recording, status change or handoff on TASK-260929-36bvsc. Only TASK-261006-1z552y receives this outcome. No repository source changes, builds, cargo or just execution.

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus the attached revision-1 patch produced exactly candidate tree `0edaf3a0edd354ef941f7e5d0f92bd0e44ed8f1d`. PASS, exact write-tree match.

## Command evidence (this panel)

| Command | Exit/result |
|---|---|
| `task-board m 'set_status(TASK-261006-1z552y, status=analysis)'` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-1z552y-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 |
| `task-board resource get TASK-260929-36bvsc TASK-260929-36bvsc_change-request_rev1.patch --output .temp/TASK-260929-36bvsc_change-request_rev1.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-1z552y-replay.idx" git apply --cached .temp/TASK-260929-36bvsc_change-request_rev1.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-1z552y-replay.idx" git write-tree` | 0; expected tree printed |
| `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b 0edaf3a0edd354ef941f7e5d0f92bd0e44ed8f1d` | 0 |
| Scoped board reads of description/scope/ac/notes and own checklist; resource get of surface-table.md, producer-brief.md, results.md, hosted-precheck-2.md | 0 |
| `git diff --stat BASE TREE`, `git diff BASE TREE -- <changed core files>`, `git status --short`, `git show TREE:<candidate source paths>` | 0; clean source checkout |
| Candidate call-site `git grep -n`, bounded `rg`, `sed`, `nl`, skill/help reads and own run directives | Read-only; successful reads 0; exceptions below |

Discovery exceptions: initial skill search included nonexistent agents/skills and .claude/skills, exit 2 (existing .codex skills returned); invalid board resources projection exit 1, repaired to scoped fields/resource-get; positional schema query exited 0 with error JSON, repaired to schema(operation="get"); missing installed skill-relative reviewer role read printed error (composite call 0), repaired by reading /Users/iv/.roles/reviewer/role.md; unknown logbook query exited 0 with error JSON, no logbook mutation attempted; justfile search included nonexistent codex-rs/justfile (rg error; enclosing read call 0), root justfile supplied recipe. The suggested initial `rm -f` replay setup was rejected before process creation, no exit code, and no deletion was necessary because the temporary index did not exist. No failed discovery is counted as a passing gate.

## Accepted attached evidence, not rerun

Source: TASK-260929-36bvsc_hosted-precheck-2.md and TASK-260929-36bvsc_results.md, retrieved through resource get. Exact tree is pinned in the hosted report. Base hosted run 37463583436 / snapshot 84aa9a3f reports lint, small, core and app-server success. Four mutant runs report killed, 0 survivors. These reports expose lane conclusions, not raw numeric process exits: numeric hosted exit codes are unknown here. Expected-red mutant lanes are FAIL, never relabeled passing. Precheck-1 mutant evidence is void because its base was red. No external GitHub re-fetch or local runtime reproduction performed.

Coverage: surface sweep 3/3 rows, exactly one result each. AC1 fails the static production acknowledgement trace; AC2 transition bumps have named executed tests; AC3 explicit errors plus killed error-to-empty mutant; AC4 store locking supports no-gap, but the claimed concurrent latch test is serialized; AC5 additive extension API, actual Session provider install and goal-side API test are present, with dependency direction unchanged. Goal consuming policy remains outside scope.

## Logbook entry (task-scoped, no control-root edit)

2026-10-06: Panel A found the exclusion fixture assumes both receipt and mailbox acknowledgement, while the candidate production acknowledgement path removes only the mailbox entry. New union snapshot therefore keeps sampled work pending. Request a real acceptance-path regression and a narrowing fixture matching production. Also recorded serialized atomicity test and noncoherent revision read as evidence bounds. Replayed exact tree; accepted attached hosted attacks without claiming local execution. Outcome ready for recording-reviewer synthesis; this panel records nothing on the reviewed leaf.

## Verdict findings

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
          "expected_failure": "Requested hosted attack, NOT executed here: narrow the existing fixture to match production by omitting its manual store lease/ack at lines 179-182. The existing snapshot.is_empty assertion at line 194 must fail because ack_id is still store-Queued. Then add an integration regression driving exec_completion_ack::acknowledge_submitted and reading via the real thread PendingWorkProvider; after accepted sampling, assert the receipt is absent. Static trace confirmed on exact candidate; no Rust runtime reproduction or exit code claimed."
        }
      ],
      "severity": "bypass",
      "repeat-of": "none"
    }
  ],
  "notes": [
    {
      "id": "snapshot-revision-not-coherent",
      "row": "revision and atomicity",
      "text": "pending_work.rs:40-51 releases the receipt-store lock, reads mailbox, then loads revision. Static schedule: read empty store at r; another thread reserves/arms a receipt (r+2); read empty mailbox; load r+2. Return empty at r+2 although the receipt is Armed. Subsequent nonempty snapshot can have the same revision. This is a hazard for revision-based waiting, but the explicit AC only demands transition bumps and Armed-to-Queued no-gap, not full snapshot linearizability. Request a barrier-driven provider test for this schedule and clarify/cohere revision semantics; no runtime reproduction executed, therefore nonblocking note."
    },
    {
      "id": "atomicity-test-is-serialized",
      "row": "revision and atomicity",
      "text": "pending_work_tests.rs:445 uses default current_thread Tokio runtime. After the start barrier, synchronous publish_exit and try_list_pending do not overlap; the mailbox lock normally completes immediately and cooperative yields still cannot interrupt synchronous publish_exit. The test also calls build_snapshot directly with revision 0, not try_read_snapshot/provider, and ignores writer result. The store read under one lock statically protects Armed-to-Queued, but AC4 asks for a latch-driven concurrent-reader test. Hosted queued-exclusion mutant proves queued membership, not concurrent atomicity. Request an actual cross-thread latch-controlled provider test with explicit handling of expected contention; current concurrent atomicity execution claim is unverified."
    },
    {
      "id": "change-size",
      "text": "git diff --stat: 1166 additions + 31 deletions, over the 800-line nonmechanical guideline. Smallest coherent stage: provider/API types plus goal-side tests (273 added lines), then core wiring/store/mailbox snapshot plus tests. Core implementation is tightly coupled through one revision; do not split state wiring across partially functional stages. This is a reviewability note, not a demonstrated behavior defect."
    },
    {
      "id": "runtime-bound",
      "text": "Local builds and tests forbidden by panel brief. Hosted evidence accepted only for the named executed attacks; no claim that proposed attacks ran. The producer exclusion fixture differs from the actual acknowledgement path, so hosted success does not refute the static finding."
    }
  ],
  "surface_results": [
    {
      "row": "snapshot contents",
      "result": "broken",
      "evidence": "Static production-call trace above confirms acknowledged work is reintroduced from store Queued. Hosted run 37463583436 and narrowing runs 37463702577 (suspended admitted) / 37463635217 (queued excluded) cover membership/dedup but mask production acknowledgement by manually retiring the B receipt. Runtime confirmation of the newly identified path requested, not executed."
    },
    {
      "row": "revision and atomicity",
      "result": "held",
      "evidence": "Held for executed transition-bump attack: exact-tree hosted base 37463583436 and suspend_skips_revision_bump mutant 37463660857 killed by revision_increases_on_suspend. Store mutations bump while holding state lock; union covers both Armed and Queued. Named fourteen revision tests exist. This result does not attest coherent revision snapshots or genuinely concurrent AC4 execution; both limits are notes above."
    },
    {
      "row": "read failure and API boundary",
      "result": "held",
      "evidence": "Exact-tree hosted base 37463583436; provider_missing_mapped_to_empty mutant 37463609295 killed in core/small by read_failure_returns_explicit_error_not_empty_snapshot and goal_read_failure_is_explicit_error_not_empty. Static try_read_snapshot propagates both lock failures; read_pending_work preserves ProviderMissing/provider errors. Session installs weak-session provider; no Cargo dependency changes/core-to-goal edge introduced. Production provider contention end-to-end is not directly exercised by the new component tests."
    }
  ],
  "free_hunt": {
    "budget_minutes": 5,
    "result": "No additional blocking mechanism identified. Checked weak-session lifetime (no strong cycle), dependency direction, externally serialized/config/rollout/CLI surfaces (unchanged), model-visible context (no new injected fragment), Bazel source-file collection versus new ordinary .rs modules (no include_str/data dependency), revision coherence, and change size. Revision coherence and size recorded as bounded notes."
  }
}
```
