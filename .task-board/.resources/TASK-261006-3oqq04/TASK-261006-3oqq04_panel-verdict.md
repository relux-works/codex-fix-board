# R141 panel B — pending-work snapshot, revision 2

accept

Read-only panel recommendation for CR-TASK-260929-36bvsc-2. This is not a recording acceptance. No writes made to TASK-260929-36bvsc.

Replay: base `812b8037a8a62bac3ce80f7035c9d9142ffea75b` plus the attached revision-2 patch produced `cf567d98480d05428ed9dea58f66306dbf030ff6`, exactly the expected candidate tree. No nested worktree, checkout mutation, commits, builds, cargo or just commands.

## Commands and exit codes

Executed here as standalone processes:

| Command | Exit | Evidence |
|---|---:|---|
| `task-board resource get TASK-260929-36bvsc TASK-260929-36bvsc_change-request_rev2.patch --output .temp/TASK-260929-36bvsc_change-request_rev2.patch` | 0 | Source patch materialized read-only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-3oqq04-replay.idx" git read-tree 812b8037a8a62bac3ce80f7035c9d9142ffea75b` | 0 | Fresh task-specific index |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-3oqq04-replay.idx" git apply --cached .temp/TASK-260929-36bvsc_change-request_rev2.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-3oqq04-replay.idx" git write-tree` | 0 | Exact tree above |
| `git diff --check 812b8037a8a62bac3ce80f7035c9d9142ffea75b cf567d98480d05428ed9dea58f66306dbf030ff6` | 0 | No whitespace errors |
| `python3 -` (inline static call-chain assertions in transcript) | 0 | Mailbox acknowledgment guard, lease_pushed_completion and acknowledge_pushed_completion all present in candidate blob; static check only |
| `python3 -` (second/third row append, each standalone) | 0 / 0 | Three-row sweep persisted in task scratch |
| `python3 -` (outcome contract validation) | 0 | One JSON block; exact 3 unique rows; accept with empty findings; clean tracked worktree |

Inspection commands `git show`, `git diff --stat/--numstat`, task AC/checklist projections, and resource text reads succeeded. Initial discovery `rg --files agents/skills .claude/skills .codex/skills ...` exited 2 because the first two paths do not exist; the installed .codex skills were read. Initial task projection requesting unsupported `resources` exited 1; corrected compact projection succeeded. Missing reviewer-role paths emitted errors in compound inspection calls; the actual installed role at `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md` was subsequently found and read. These are discovery failures, not passing validation gates. Python readiness was checked before static assertions.

Accepted attached execution evidence, not rerun here: hosted precheck 3 pins this exact tree and snapshot `9ac368c5`; base run 37473988733 reports success in core/app-server/lint/small lanes. Five narrowing mutants report 5/5 kills and zero survivors; named tests/run IDs are in the row results. Hosted summary does not include numeric individual command exit codes, so none are invented. Local CR validation log is supplementary: head records target guard and fmt-check exits 0; tail records 244/244 small tests and exit 0 plus exact-command-shard 4/4 green. Its task-board truncation bound means it is not used to independently attest every middle command. No CI run was launched by this panel.

## Sources and decision

Candidate paths below refer to `git show cf567d98480d05428ed9dea58f66306dbf030ff6:<path>`, never ambient checkout contents. Board read-only sources: `surface-table.md`, `producer-brief.md`, `TASK-260929-36bvsc_results.md`, `TASK-260929-36bvsc_hosted-precheck-3.md`, `TASK-260929-36bvsc_change-request_rev2-validation.log`, and the rev1 review outcome under `.resources/TASK-260929-36bvsc/` in the authoritative board. Sources are pinned internal evidence; no internet facts required.

Sweep: 3/3 rows, one result per row; 0 blocking findings. The rev1 acknowledgment defect is fixed on the executed acceptance path. AC1/AC2/AC3/AC5 have named hosted evidence; AC4 has static single-lock protection and a killed queued-inclusion mutant, with concurrency execution limits stated below. Acceptance is bounded to those attacks, not proof of absence.

Task-specific logbook entry: exact replay succeeded; five attached narrowing-mutant kills accepted; revision coherence, concurrent-provider testing, alternate retirement integration and oversized diff remain notes. Nothing is recorded on the source task. Artifact budget: one plain-text outcome; no archives. Decision: panel recommendation only, consumed by the recording reviewer. Frozen input: exact base/patch/tree; no prerequisites added. Review/free hunt bounded to this round and five minutes of free hunt.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "snapshot-revision-not-coherent",
      "row": "revision and atomicity",
      "text": "codex-rs/core/src/session/pending_work.rs:49-63 reads store, then mailbox, then revision without a version retry. Static schedule: copy empty store, concurrent reserve+arm, copy empty mailbox, load new revision; returned empty and later nonempty contents can share a revision. This repeats the rev1 nonblocking note. AC2 requires transition bumps, not full linearizability. Request a latch-controlled production-provider snapshot_revision_matches_contents_during_mutation test before relying on revision equality as content equality. Not executed here; not a blocking finding."
    },
    {
      "id": "atomicity-test-bound",
      "row": "revision and atomicity",
      "text": "codex-rs/core/src/session/pending_work_tests.rs:517-604 uses default current-thread tokio::test; start Barrier does not force overlap inside synchronous store operations. Readers call build_snapshot directly with revision 0, and writer publish result is ignored. Hosted store_queued_excluded_from_snapshot kill establishes queued inclusion, not concurrent provider execution. Static same-lock phase move protects Armed->Queued, but AC4 latch-driven execution remains bounded. Request a multi-thread latch-controlled read_pending_work test handling legitimate contention explicitly."
    },
    {
      "id": "alternate-retirement-bound",
      "row": "snapshot contents",
      "text": "Free hunt checked receipt_hooks.rs:209-269 cancellation/release and :327-345 terminal-stdin retirement. These retire B without cancelling mailbox entries; build_snapshot can still union mailbox entries after B retirement. Current production enqueue is not wired to real exits (codex_thread.rs:535-581 is a test helper; stage 2e is pending), so no live public-entry reproduction was established. Treat this as an integration boundary to test when watcher wiring lands, not a demonstrated regression of this leaf."
    },
    {
      "id": "change-size",
      "text": "Exact diff is 1288 insertions plus 34 deletions over 12 files, exceeding the 800-line nonmechanical guideline. Smallest coherent staging option: extension API/provider types plus goal-side API tests (273 added lines), then dependent shared revision/core snapshot wiring and tests. Keep shared store/mailbox revision wiring in one coherent stage. Nonblocking reviewability note."
    },
    {
      "id": "provider-installation-test-bound",
      "row": "read failure and API boundary",
      "text": "production_acknowledgement_removes_pending_work uses a real Session fixture and actual acknowledge_submitted/read_pending_work, but manually installs its provider (pending_work_tests.rs:192-214); it does not exercise Session startup installation at session.rs:1817-1829. Static startup wiring is present. Production provider contention and startup installation are not independently attested by this test."
    }
  ],
  "surface_results": [
    {
      "row": "snapshot contents",
      "result": "held",
      "evidence": "Exact-tree hosted precheck 3 base run 37473988733; production_ack_skips_store_retirement killed by production_acknowledgement_removes_pending_work (37474019570); suspended_queued_admitted killed by snapshot_excludes_suspended_and_cancelled (37474137228); store_queued_excluded_from_snapshot killed by membership tests (37474077806). Static manager lease+ack follows successful mailbox retirement. Rev1 sampled-receipt-remains-pending mechanism repaired on the tested acceptance path. No process liveness enumeration. Held means these attacks only."
    },
    {
      "row": "revision and atomicity",
      "result": "held",
      "evidence": "Exact-tree hosted base 37473988733 exercises 14 revision_increases_on_* tests (all eight requested transition classes); suspend_skips_revision_bump killed by revision_increases_on_suspend (37474108222). store_queued_excluded_from_snapshot killed by armed_to_queued_is_atomic_for_concurrent_readers and membership test (37474077806). Same receipt-store lock covers Armed->Queued; dedup map prevents both sets. This is not an attestation of genuinely concurrent provider atomicity or revision/content coherence; notes state those bounds."
    },
    {
      "row": "read failure and API boundary",
      "result": "held",
      "evidence": "Exact-tree hosted base 37473988733; provider_missing_mapped_to_empty killed by goal_read_failure_is_explicit_error_not_empty and read_failure_returns_explicit_error_not_empty_snapshot (37474048117). Source try_read_snapshot maps both lock errors to explicit error variants; read_pending_work preserves ProviderMissing/provider errors. Goal API test imports extension-api; no dependency manifest changes and no new core->goal edge. Component contention tests exist; provider contention end-to-end remains a note."
    }
  ],
  "free_hunt": {
    "budget_minutes": 5,
    "result": "No additional blocking reproduction established. Checked alternate cancellation/stdin paths, weak-session ownership, extension installation, CLI/config/app-server/rollout serialized surfaces, model-visible fragments, Bazel data dependencies, and change size. No new injected context fragment or external wire schema. Integration and evidence bounds recorded as notes; no new builds/tests run."
  }
}
```
