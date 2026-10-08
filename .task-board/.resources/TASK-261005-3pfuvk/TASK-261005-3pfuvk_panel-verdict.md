# TASK-261005-3pfuvk panel A verdict — CR-TASK-260929-1ma0pr-1 rev1

changes_requested

Replay: base `47f7a80476eb78f27f7ce97c8bf7eb9236c40b47` plus the attached revision-1 patch produced exactly `808000cbd14914847c7cd418f444dd9232281ddc` through a temporary index. The ordinary index/worktree was not changed. Snapshot `34cf97acbb80e9829c7b79669dad70e1cd0419c1` has the same tree. No build, cargo, just, commit, branch operation, source-task mutation or review recording was performed.

Recommendation: request the missing hosted queue persistence regression on this exact tree, then correct the result/coverage attestation. The existing implementation may be correct; this panel reproduced an evidence gap, not a product crash. A targeted follow-up is sufficient: from codex-rs on the exact snapshot, `just test -p codex-queue-extension --test queue_service -E 'test(forged_exec_completion_payload_is_skipped_without_panic)'`. This command was **requested, not run** by the panel. Do not change product code merely to repair this evidence.

Plan: one CR recommendation, frozen candidate above; one plain-text outcome; no new prerequisite; 35-minute ceiling including packaging, bounded free hunt up to 5 minutes. Exit criteria: replay match, three rows exactly once, reproduced findings and requested missing attacks recorded. Consuming reviewer: the orchestrator's recording reviewer. The run write-boundary rule takes precedence over the generic outside-worktree artifact wording; scratch output is in the assigned worktree and publication uses the resource CLI.

Evidence and command exits (panel execution)

- `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-3pfuvk-replay.idx" git read-tree 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47` — 0.
- `task-board resource get TASK-260929-1ma0pr TASK-260929-1ma0pr_change-request_rev1.patch --output .temp/TASK-260929-1ma0pr_change-request_rev1.patch` — 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-3pfuvk-replay.idx" git apply --cached .temp/TASK-260929-1ma0pr_change-request_rev1.patch` — 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-3pfuvk-replay.idx" git write-tree` — 0, exact expected tree above.
- `git diff --check 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47 808000cbd14914847c7cd418f444dd9232281ddc` — 0.
- `git rev-parse '34cf97ac^{tree}'` — 0, same tree.
- `gh run view 37302805027 --repo relux-works/codex --json jobs,headSha,url,workflowName > .temp/TASK-261005-3pfuvk/hosted-run.json` — 0.
- `gh run view 37302805027 --repo relux-works/codex --log > .temp/TASK-261005-3pfuvk/hosted-run.log` — 0, full completed four-lane log fetched. The workflow headSha is the base; actual checkout inputs and job records pin snapshot 34cf97ac, verified against its tree. No proxy reliance on headSha.
- `python3 .temp/TASK-261005-3pfuvk/audit_queue_coverage.py` — **1 (expected-red)**, the queue-coverage claim fails; not a passing gate.
- Tool readiness (`git --version`, `rg --version`, `gh --version`, `python3 --version`) and corrected resource/code reads — 0. `git status --short` — 0, no tracked changes.
- Failed discovery retained honestly: initial skill search — 2 (two optional directories absent); initial board projection — 1 (unknown resources field, corrected to named resource reads); two initial wrong `git show` persistence paths — 128 (corrected via ls-tree). The initial cleanup/read-tree command was rejected before execution for rm syntax, with no process exit; replay was then run without deletion. None is counted as passing evidence.

Accepted hosted execution (not rerun by panel)

Base [run 37302805027](https://github.com/relux-works/codex/actions/runs/37302805027) has success in all four lanes. Full log reports 4967 core tests passed, 1829 app-server tests passed and 242 small-crate tests passed; skip counts 11/2/0 respectively. Named core refusal, forged-history/resume, and nine-completion tests have PASS entries (log lines 15626–15627 and 17435–17438). Hosted job success is recorded, but no numeric process exit is independently exposed by gh JSON; this panel does not invent one.

Attached `TASK-260929-1ma0pr_hosted-precheck-2.md` reports m1–m10 killed on runs 37302828071, 37302850331, 37302873701, 37302897088, 37302920627, 37302942434, 37302964089, 37302986386, 37303009610, 37303033462. These are expected-red mutation results, not passing suites. Individual numeric exits were not present in that resource and were not independently collected. Precheck 1 is excluded because its base was red.

Surface coverage: 3/3 rows swept; 2 held, 1 broken on attestation. AC1/2/3/5 have named core driving/negative execution. AC4's core serde/resume portion executed; its specifically authored forged queue persistence regression was not selected in the claimed run (0/1). Compilation of codex-queue-extension as a dependency does not execute its integration test target.

Free hunt: inspected manual Serialize compatibility for all existing arms, public/internal TurnInput conversion, idle start and cancellation windows, and persistence boundaries. No additional reproduced blocking mechanism. Failure/acknowledgement recovery is explicitly story D scope. Historical request-size wording and the large replay delta are notes, not claimed proven defects. Empty free_hunt means no additional reproduced findings; it is not proof of absence.

Logbook-carrying anomaly: the results claim all required queue/core/app-server tests ran, while actual workflow selections omit the queue crate. Keep the compiled-versus-executed distinction in the orchestrator's record; this task-scoped resource carries that entry without editing the control-root LOGBOOK. Nothing was written or recorded on TASK-260929-1ma0pr.

Sources: the source task's `surface-table.md`, AC projection, `producer-brief.md`, `TASK-260929-1ma0pr_results.md`, `TASK-260929-1ma0pr_mutants.json`, and `TASK-260929-1ma0pr_hosted-precheck-2.md`; exact candidate git blobs; the full hosted job log linked above. Findings do not rely on external secondary sources.

Reproduction transcript

    queue package selected: False ; named test PASS record: False
    QueuePersistenceCoverageError: hosted run 37302805027 does not execute the claimed queue regression
    exit: 1

Reproduction source (save at the command's path after fetching the hosted log with the command above):

    import pathlib, re, subprocess, sys
    TREE = "808000cbd14914847c7cd418f444dd9232281ddc"
    name = "forged_exec_completion_payload_is_skipped_without_panic"
    workflow = subprocess.check_output(["git", "show", TREE + ":.github/workflows/relux-ci.yml"], text=True)
    test = subprocess.check_output(["git", "show", TREE + ":codex-rs/ext/queue/tests/queue_service.rs"], text=True)
    assert "async fn " + name in test
    log = pathlib.Path(".temp/TASK-261005-3pfuvk/hosted-run.log").read_text(encoding="utf-8-sig")
    assert "4967" in log and "1829" in log and "242" in log
    assert "34cf97acbb80e9829c7b79669dad70e1cd0419c1" in log
    lines = [line for line in log.splitlines() if "##[group]Run" in line and "just test" in line]
    print("Hosted test selections:")
    for line in lines: print(re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", line))
    print("Candidate test defined:", name)
    selected = any("-p codex-queue-extension" in line for line in lines)
    executed = any(name in line and "PASS" in line for line in log.splitlines())
    print("queue package selected:", selected, "; named test PASS record:", executed)
    if not selected or not executed:
        print("QueuePersistenceCoverageError: hosted run 37302805027 does not execute the claimed queue regression", file=sys.stderr)
        sys.exit(1)

```verdict-findings
{
  "findings": [
    {
      "id": "queue-test-coverage-attestation",
      "row": "internal TurnInput variant and persistence",
      "invariant": "Claimed executed AC4 forged-payload persistence coverage must identify a test actually selected and run on the exact candidate, rather than compiling a dependency or running another package.",
      "mechanism": "TASK-260929-1ma0pr_results.md AC4/surface map and \"Not run anywhere: nothing required remains unrun\" attribute queue_service.rs:1085 to base run 37302805027. The actual run selects core, app-server and four small crates; it never selects codex-queue-extension and contains no PASS entry for the named test. .github/workflows/relux-ci.yml package selections confirm the blind spot.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/queue/tests/queue_service.rs:1085 (coverage audit embedded below)",
          "command": "python3 .temp/TASK-261005-3pfuvk/audit_queue_coverage.py",
          "expected_failure": "Exit 1: QueuePersistenceCoverageError: hosted run 37302805027 does not execute the claimed queue regression. This is an evidence-attestation failure, not a reproduced failure in queue production code.",
          "pinned_blobs": [
            "git-blob:e79341df18d478c650667ab663cb1ae2c5fb7f44",
            "git-blob:5e076dc37d7ef62879cbf55c2256288be82de9dd",
            "sha256:ed599f0fde9ca3777407e0883470363c73537d7579396a57c8d1069a5d4cbc03",
            "sha256:e82d03c48a72f9886038e87d74261bb912efbbdcefba7a5a2caff56fed2a0f87"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Batch limit is enforced on newly leased fragments. The real suite expects cumulative history of 9 fragments on the second wake (exec_completion.rs:239), so the literal AC wording \"a request never carries more than 8 fragments\" should be clarified as incremental admission. This panel does not infer a total-history cap or require rewriting history.",
    "Sampling acknowledgement, failed/cancelled lease recovery and real process publication are deferred to story D/E by the attached brief; their current lack of production integration is not a defect of this leaf.",
    "Candidate diff against the supplied base is 2310 additions and 16 deletions across 18 files, larger than the producer estimate. It includes the runtime-mailbox foundation. Suggested coherent split, if needed: mailbox foundation; bounded fragment and serde; record/wake wiring with integration coverage. No arbitrary size-only blocking finding.",
    "Hosted mutation results are accepted from the attached hosted-precheck-2 resource (10 killed, 0 surviving). The panel independently fetched the full base-run record and verified selected tests and exact checkout. It did not fetch all mutant logs or execute Rust commands."
  ],
  "surface_results": [
    {
      "row": "exec-completion fragment",
      "result": "held",
      "detail": "Exact-tree base run 37302805027: forged recorded-history/resume public-entry attack passes; injection/classification/cap unit attacks and m1/m2/m3/m5 narrowing attacks are supported by attached precheck 2. Static trace record_pending_input -> ExecCompletionFragment -> record_conversation_items confirms wiring and 768-byte post-escape bound."
    },
    {
      "row": "batching and retention",
      "result": "held",
      "detail": "Base public-entry nine_pending_completions_sample_in_capped_batches_without_loss passes; lease FIFO cap and separate idle/in-turn predicates inspected. m4/m9/m10 killed per precheck 2; exactly-once nine-item rollout asserted. Held for incremental admission, not a cumulative-history bound."
    },
    {
      "row": "internal TurnInput variant and persistence",
      "result": "broken",
      "detail": "Serde refusal and rollout/resume attacks pass in hosted core lane; static public protocol/app-server paths remain separate and fail safely. Coverage-attestation attack reproduces the missing queue execution claimed as satisfied; queue behavioral result remains unknown. See queue-test-coverage-attestation."
    }
  ],
  "free_hunt": []
}
```
