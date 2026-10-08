# R141 panel B — revision 6 verdict

accept

Replay base `0462dcc062b822bb8fff16cc31ce6eeab69823b9` plus `TASK-260929-u2i5rr_change-request_rev6.patch` produced `4a456609f6f928d331d327e167114e71abade872`, exactly the expected candidate tree. Review target: CR-TASK-260929-u2i5rr-6, not the current checkout. No product files changed.

## Plan and evidence boundary

Decision: recommend accept or changes_requested to the recording reviewer. Frozen precondition: supplied base, patch, candidate tree and single-row surface table; no new grammar. Budget: one static panel, 30 minutes, one outcome under 25 KiB, no archives or serial prerequisites. Exit: replay equality, one result per row, error-arm/test sweep, bounded free hunt, attach verdict and hand off own researcher task. Consuming slice: orchestrator merges panel verdicts for the existing B1 receipt leaf. No implementation, builds or external research required.

## Direct commands and actual exits

| Command / read | Exit | Observation |
| --- | ---: | --- |
| task-board m 'set_status(TASK-261002-rwld80, status=analysis)' | 0 | Own task only |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261002-rwld80-replay.idx" git read-tree 0462dcc062b822bb8fff16cc31ce6eeab69823b9 | 0 | Temporary index seeded |
| task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_change-request_rev6.patch --output .temp/TASK-260929-u2i5rr_change-request_rev6.patch | 0 | Read-only source materialization |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261002-rwld80-replay.idx" git apply --cached .temp/TASK-260929-u2i5rr_change-request_rev6.patch | 0 | Patch replay |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261002-rwld80-replay.idx" git write-tree | 0 | Exact expected tree printed |
| task-board q 'get(TASK-260929-u2i5rr) { description scope ac }' | 0 | AC/scope inspected |
| git show <candidate>:<each of the two receipt source files> | 0 | Exact candidate blobs materialized under task scratch |
| git diff --check <base> <candidate> | 0 | No whitespace errors |
| git diff --quiet 00518744e87f5bb1fa024ac3e2cdd903e6b0c5a8 <candidate> -- codex-rs/core/src/unified_exec/completion_receipt.rs codex-rs/core/src/unified_exec/mod.rs | 0 | Product/export unchanged versus rev5 |
| git grep -n -e CompletionReceiptStore -e SamplingLease -e ReceiptOwner <candidate> -- codex-rs ':!codex-rs/core/src/unified_exec/completion_receipt_tests.rs' | 0 | No integration callers outside module |
| python3 static name-set / sweep audit (inline, source and attached logs) | 0 | 24/24/24 exact names, 59 sweep entries, 6 bound-bearing entries |
| git status --short | 0 | Clean tracked/untracked status; scratch ignored |
| task-board q 'get(TASK-261002-rwld80) { checklist notes }' | 0 | Own checklist inspected |
| task-board spawn directives RUN-261002-161ed9 | 0 | No directives |

Tool readiness: command-v task-board/git/rg, git --version, rg --version and python3 --version each succeeded (0); scratch version logs under `.temp/TASK-261002-rwld80/`. Supporting reads of source/test ranges, surface-table, producer brief, results, previous verdict, local test log and hosted summary succeeded. No cargo/just commands run.

Recovery reads, not gates: initial query with unsupported `resources` field failed (1); scoped schema(operation=get) succeeded (0); `task-board resource list` displayed CLI help (0), not a resource inventory, so inventory came from a read-only directory listing. Missing agents/skills and .claude/skills paths produced rg diagnostics; the pipeline returned 0, not evidence those paths exist. Missing installed reviewer role read failed; later source-path ls also failed (1). Multi-command supporting read calls ending in unsuccessful role-file discovery returned 1 despite successful preceding reads. Resource-update attempt with unsupported --file failed (1); update --help succeeded (0), and the corrected SOURCE/--name form is used for attachment. None counted as green validation. The exact task brief supplies the review-round rules.

Packaging verification: inline Python parsed exactly one verdict-findings block, checked the exact four JSON keys, one surface result, empty findings and <25 KiB artifact bound; exit 0. Exact test definition line numbers were rechecked with rg (exit 0) and citations corrected before handoff.

## AC and error-arm fact check

All citations below refer to blobs at the candidate tree above, not worktree files.

| AC | Driving/refusal evidence in completion_receipt_tests.rs |
| --- | --- |
| 1 | happy path :70; second claim :110; all terminal late operations :1164 |
| 2 | forced early-inline/early-arm/arm-first orders :128; inline-before-exit :271; duplicate retained result :872; late active decision :979 |
| 3 | fail/requeue and stale acknowledge :299; stale fail :331; wrong phase/source :1042 |
| 4 | four unsampled cancellation states :363; terminal owner isolation :511; terminal late operations :1164 |
| 5 | 64 reserves / 65th refusal and replacement :453; bounded history :480; owner bytes :940,960 |
| 6 | source switching :730; claim race :771; wrong-source live token :1093 |

Checked the 59-entry producer sweep against every branch in completion_receipt.rs. The four same-lock defensive entries and two UUID-randomness entries have stated bounds; other entries name tests that actually reach the corresponding production method/arm. Active-phase errors, legitimate/foreign/unknown terminal paths, source/token mismatch, repeated cancellation and poison are distinguished. See JSON notes for the measured mapping ratio and its limits.

## Task-scoped logbook entry

2026-10-02: replay equality verified; rev6 closes the sole merged rev5 finding. Exact test-name sets matched candidate/producer/local PASS records. Recommendation accept with no new defect; retain explicit RNG/unreachable-arm and no-mutation-execution bounds. Installed role reference is missing; task brief and negative-evidence contract used without changing shared tooling. No mutation, status, handoff or verdict recorded on TASK-260929-u2i5rr. All board writes are confined to TASK-261002-rwld80 and its authorized lifecycle side effects.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Revision-5 finding resolve-initial-response-active-nonreserved-arm-unguarded is closed by completion_receipt_late_initial_response_refuses_each_active_nonreserved_state (tests:979-1039): Armed/Queued/Leased x Arm/InlineResult = 6/6 rejection cases, exact status preserved, original completion(Some(73)) acknowledged. M17 narrowing to late Armed admission would fail the Err assertion by static control-flow inspection; NOT executed.",
    "All 6/6 AC rows have driving/refusal assertions inspected. The producer sweep has 59 grouped entries: 53 wholly mapped to named driving tests, 6 carry explicit unreachable/unforced bounds (one also maps the fresh UUID path). This is a static mapping ratio, not measured branch coverage. Every Err-returning arm and state transition was cross-checked against source, including the bounds at implementation:214-219,252-255,283-290,360,368.",
    "Candidate test definitions, producer legend, and attached local PASS names are exact matching sets: 24/24/24. Reused TASK-260929-u2i5rr_rev6-local-test.log reports 24 passing, 4881 skipped. Its exit-0 attribution is in the producer results supplement; this panel did not run that command. Hosted TASK-260929-u2i5rr_hosted-ci-rev6.md identifies commit 67a4de28f8cf75651c465ab9ae35d7ab97d18863, exact tree 4a456609f6f928d331d327e167114e71abade872, run 36998390061 and success for small/core/lint/app-server. That summary has no per-test rows. No live provider query was performed.",
    "No Rust builds, tests, or mutants executed here: measured panel mutant executions 0. M17/M18 remain unexecuted, not killed. Static reasoning shows M18 admitting a matching-token wrong-source lease fails the mismatch test Err(StaleLease) assertions (tests:1093-1103).",
    "Inactive B1 scope: candidate git grep finds no non-test receipt-store caller outside this module. API methods are the real entry points for this leaf; launch-before-reserve ordering, actual prompt membership, mailbox/transport integration and caller cleanup belong to B2/later and are not certified. Liveness requires callers to resolve/cancel; no automatic expiry is promised.",
    "The installed project-management package omits .roles/reviewer/role.md referenced by its router. The read failed rather than indicating an empty contract. Used the explicit panel brief, full negative-evidence reference and research-workflow contract; no infrastructure edits or substitute workflow introduced.",
    "Full CR adds 1834 lines over base, dominated by 1298 test lines; revision 6 adds 301/deletes 1 test lines only. This exceeds repository size guidance, but the reviewed coherent inactive state machine and its adversarial tests have no newly separable runtime stage. Nonblocking maintenance note; no extra prerequisite. Implementation remains unchanged from revision 5."
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "held",
      "reason": "Statically attacked every supplied family: exit/decision orders, duplicate claims, lease retry/staleness, owner isolation, all unsampled cancellation states, 64/65 capacity, stdin/pushed competition, and poisoned locks. Swept 1/1 surface rows and mapped 6/6 AC rows. The revision-5 late-decision hole is covered by 6 exact-state refusals and preservation assertions. Held under the requested read-only static scope plus attached execution evidence; no measured mutant kills claimed.",
      "evidence": [
        "candidate:codex-rs/core/src/unified_exec/completion_receipt.rs:243-527",
        "candidate:codex-rs/core/src/unified_exec/completion_receipt_tests.rs:70-1298",
        "TASK-260929-u2i5rr_results.md:Exhaustive error/transition-arm sweep",
        "TASK-260929-u2i5rr_rev6-local-test.log",
        "TASK-260929-u2i5rr_hosted-ci-rev6.md"
      ]
    }
  ],
  "free_hunt": [
    {
      "attack": "Cloned lease reuse, fail/ack and cancel/ack ordering",
      "result": "held",
      "reason": "All entry points hold the same store Mutex throughout lookup and mutation; first successful retire removes active membership. Clone acknowledgments then see terminal error; stale failed tokens cannot requeue a new lease. No double claim or partial state update found (implementation:441-511)."
    },
    {
      "attack": "Reserved(Some) cancellation and duplicate publication",
      "result": "held",
      "reason": "Reserved with retained exit is still active; cancel retires regardless of active phase. publish_exit only fills an empty Reserved completion or transitions Armed; all other phases refuse (implementation:389-399,492-511). Reserved(Some) cancellation is statically inspected, not a separate executed case."
    },
    {
      "attack": "Slot accounting and terminal eviction",
      "result": "held",
      "reason": "reserve checks active.len >=64 under lock; all terminal outcomes pass through retire, remove active, and retain at most 64 terminal records. Capacity and 65 sequential retirement tests attack the two bounds (implementation:252-297; tests:452-521). Test loop constants are coupled to active capacity; coordinated future edits to both bounds are not covered."
    },
    {
      "attack": "Owner isolation and forged lease target/source",
      "result": "held",
      "reason": "Owner comparison precedes state inspection on active and terminal lookups. Tests vary thread/generation/call separately and forge from real leases; wrong phase, stale token and matching-token wrong source are refused without harming the real lease (tests:511-727,1042-1115)."
    },
    {
      "attack": "RNG, bounded ownership and poison",
      "result": "held",
      "reason": "IDs check both active and terminal sets before insertion; owner IDs are byte-bounded and Debug redacted. RNG collision/exhaustion unforced; lease-token UUID collision remains probabilistic, not exhaustive. All eight store methods acquire lock_state and return LockPoisoned after the induced panic (tests:1249-1298)."
    },
    {
      "attack": "External surfaces and context",
      "result": "held",
      "reason": "Only two new internal files and one module export differ. No app-server/CLI/config/rollout API or model-context injection added. The unwired API is explicitly permitted, so unit API tests meet this stage scope; no agent behavior change requiring an integration test."
    }
  ]
}
```
