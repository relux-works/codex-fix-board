# R141 panel A — receipt state machine revision 6

accept

Replay: base `0462dcc062b822bb8fff16cc31ce6eeab69823b9` plus `TASK-260929-u2i5rr_change-request_rev6.patch` produces `4a456609f6f928d331d327e167114e71abade872`, exactly the expected candidate tree. All inspection refers to those blobs, not the Story worktree HEAD.

Commands run by this panel (actual observed exits):

| Command | Exit | Evidence/result |
| --- | ---: | --- |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-240men-replay.idx" git read-tree 0462dcc062b822bb8fff16cc31ce6eeab69823b9` | 0 | Temporary index initialized |
| `task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_change-request_rev6.patch --output .temp/TASK-260929-u2i5rr_change-request_rev6.patch` | 0 | Patch fetched read-only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-240men-replay.idx" git apply --cached .temp/TASK-260929-u2i5rr_change-request_rev6.patch` | 0 | Replay applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-240men-replay.idx" git write-tree` | 0 | Exact expected tree above |
| `git diff --check 0462dcc062b822bb8fff16cc31ce6eeab69823b9 4a456609f6f928d331d327e167114e71abade872` | 0 | Patch whitespace check |
| `git show <candidate>:codex-rs/core/src/unified_exec/completion_receipt{,_tests}.rs` (two calls) | 0 | Exact candidate blobs inspected |
| `git diff 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8 <candidate> --stat` | 0 | Tests-only rev6 delta |
| `git grep -n CompletionReceiptStore <candidate> -- ':!codex-rs/core/src/unified_exec/completion_receipt_tests.rs'` | 0 | Only declaration/implementation |
| `task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_rev6-local-test.log --output .temp/TASK-261002-240men/local-test.log` | 0 | Complete 24-PASS log read |
| `tar -xOf <rev6-hold-evidence.tar.gz> clippy-01.log` | 0 | Successful clippy completion, three baseline warnings |
| `tar -xOf <rev6-hold-evidence.tar.gz> fmt-final-03.log` | 0 | Empty fmt log; exit 0 attributed to producer results, not inferred from emptiness |

No cargo/just/build/test execution by this panel. Producer gate exits (fmt/clippy/filtered tests: 0) are reused and attributed to the attached results, not fresh panel observations. The local log contains every candidate test's PASS row. Historical narrowing mutant kills are not re-executed or recertified. Initial orientation had a failed resource-field query (exit 1) and a missing role-path read (cat exit 1); corrected by scoped schema and `~/.roles/reviewer/role.md`. Neither is a validation success.

Research bound: decision is this panel's accept/changes_requested recommendation for CR revision 6; frozen input is the pinned base/patch/tree; one outcome, no archive, no serial research prerequisite; 30-minute static sweep plus 5-minute free hunt ceiling. Consuming step is the orchestrator's merged review, not new implementation research.

Panel evidence cross-check: standalone Python verification, exit 0, checked 24/24 exact test names against PASS rows and both SHA-256 values against the producer identities. Standalone Python artifact validation exited 0: exactly one valid verdict-findings JSON block, required top-level keys, empty findings/free_hunt, exactly one surface result, and one-word accept verdict. This is a packaging check, not a Rust behavior test.

## Outcome-scoped logbook

The previous late-initial-response finding is addressed by direct legitimate-owner calls in all three nonreserved active phases and both decisions, with preserved completion assertions. Additional rev6 tests cover unknown handles, late terminal operations, mismatched leases and all poisoned-lock entries. No product defect reproduced. No mutations whatsoever were issued on TASK-260929-u2i5rr. Artifact staged in this run's `.temp/` to honor the explicit run-write boundary; board attachment creates the durable outcome outside the managed worktree via the CLI.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "static-panel-bound",
      "text": "Held is scoped to the expressly authorized static attack through the receipt API plus reused execution evidence. This panel executed no Rust tests, builds, or mutants. M17/M18 remain unexecuted; their expected failures were checked by control/data-flow inspection, not claimed as kills."
    },
    {
      "id": "coverage",
      "text": "6/6 AC rows map to driving/refusal assertions; 24/24 candidate test names are present in the attached local test log with PASS. The error-arm sweep names driving tests for reachable public branches. Its stated undriven bounds are active-phase ReceiptPhase::error arms, missing active under the same held lock in retire and resolve action application, UUID collision retry and four-attempt exhaustion. These bounds agree with the implementation."
    },
    {
      "id": "execution-evidence",
      "text": "Reused TASK-260929-u2i5rr_rev6-local-test.log: Nextest run 77e1c120-e842-4a00-a897-ed9d39bad235, 24 passed, 4881 skipped. Producer reports exit 0 and two runs; the fetched log proves one full 24-test run, not two independent logs. Reused TASK-260929-u2i5rr_hosted-ci-rev6.md reports tree 4a456609f6f928d331d327e167114e71abade872, commit 67a4de28f8cf75651c465ab9ae35d7ab97d18863, run 36998390061, four success lanes. No fresh provider query; the hosted summary contains job conclusions rather than per-test rows."
    },
    {
      "id": "inactive-api",
      "text": "git grep on the exact candidate finds no runtime CompletionReceiptStore caller outside its declaration/implementation. This is explicitly the inactive B1 stage. Tool launch, mailbox, model-context effects and actual transport acknowledgement are outside this leaf; reserve-before-launch is a caller obligation, not attested integration."
    },
    {
      "id": "size",
      "text": "Base-to-candidate delta is 1834 additions across exactly the three scoped paths; rev5-to-rev6 is 301 additions/1 deletion solely in tests. Product code is unchanged from rev5. This exceeds generic review-size guidance but retains a single coherent inactive state machine; nonblocking maintainability note."
    },
    {
      "id": "mutant-delta",
      "text": "M17 narrows the late-decision guard to admit Armed: tests.rs:1007-1074 asserts exact InvalidTransition for both decisions on Armed/Queued/Leased, then samples the original 73 result. M18 admits a forged source with valid token: tests.rs:1077-1161 calls fail and acknowledge with TerminalStdinOutput against a PushedCompletion lease, asserts StaleLease, and acknowledges the legitimate lease to the original result. Both recipes would contradict explicit assertions; neither was run here."
    },
    {
      "id": "free-hunt-bound",
      "text": "Bounded static free hunt after the persisted surface sweep checked cloned lease reuse; cancel versus acknowledge/fail serialization; cancellation of Reserved(Some); freed capacity for InlineResult/Sampled/Cancelled; terminal eviction and UUID collision guards; cross-store receipt isolation; byte-bounded owners and opaque Debug. All mutations share the same mutex and terminal lookup validates owner before phase disclosure. No additional defect found. No scheduler model checking or forced random collisions were performed."
    }
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "held",
      "reason": "Static attack of public receipt API sequences and candidate assertions: forced exit-before-inline, exit-before-arm and arm-before-exit; repeated decision on each active nonreserved state with both decisions; duplicate exits on Reserved(Some)/Queued/Leased; stale token and wrong-source failure/ack; all terminal outcomes and foreign thread/generation/call owners; cancellation from each unsampled state; 64/65 capacity and release; competing stdin/pushed leases; all eight poisoned-lock entries. One mutex serializes lookup and mutation; refusal branches preserve phase/result. No bypass reproduced within this static panel.",
      "evidence": [
        "completion_receipt.rs:268-530",
        "completion_receipt_tests.rs:70-1298",
        "TASK-260929-u2i5rr_results.md (Exhaustive error/transition-arm sweep)",
        "TASK-260929-u2i5rr_rev6-local-test.log",
        "TASK-260929-u2i5rr_hosted-ci-rev6.md"
      ]
    }
  ],
  "free_hunt": []
}
```
