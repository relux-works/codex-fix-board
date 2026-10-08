# TASK-261005-1379z0 — panel A, CR-TASK-260929-1ma0pr-2

accept

## Scope and bounded review contract

Independent, non-recording revision-2 review. Decision: whether the supplied candidate satisfies this leaf's five AC clauses and three surface rows. Frozen inputs: base `47f7a80476eb78f27f7ce97c8bf7eb9236c40b47`, candidate tree `5b2ea16af484965b3dd34f6ca4198dd903732541`, supplied surface table, and final-plan.md sections 5.1–5.2. No new grammar or implementation is proposed. Budget: one inline panel, at most 45 minutes, zero serial research prerequisites, one text outcome under 24 KiB, no archives attached. Exit: exact replay, one result per row, bounded free hunt, evidence distinction, and researcher handoff on this task only.

No builds, cargo, just, local Rust tests, commits, branch changes, source edits, or mutations of TASK-260929-1ma0pr were performed. Candidate files were read from the candidate Git tree, not assumed from the worktree. Scratch inputs and logs are under `.temp/TASK-261005-1379z0/`; the attached outcome is the canonical persistent handoff. It is transferred outside the managed worktree by the board resource API, not by directly writing the control root.

## Replay and command exit codes

Replay uses a separate index and leaves the normal index/worktree untouched. All three replay commands were rerun separately with their actual exit codes captured:

| Command | Exit | Evidence |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261005-1379z0, status=analysis)'` | 0 | Only this panel task's lifecycle was started. |
| `task-board resource get TASK-260929-1ma0pr TASK-260929-1ma0pr_change-request_rev2.patch --output .temp/TASK-261005-1379z0/change-request.patch` | 0 | Read-only materialization of supplied CR. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-1379z0/replay-verified.idx" git read-tree 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47` | 0 | Exact base loaded. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-1379z0/replay-verified.idx" git apply --cached .temp/TASK-261005-1379z0/change-request.patch` | 0 | Patch applied to temporary index. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-1379z0/replay-verified.idx" git write-tree` | 0 | Printed `5b2ea16af484965b3dd34f6ca4198dd903732541`, exactly the expected candidate. |
| `git rev-parse a743b62596aa374bcc63075c982f2917f3feb673^{tree}` | 0 | Hosted checkout snapshot has the same candidate tree. |
| `git diff --check 47f7a804 5b2ea16a` | 0 | No whitespace errors in replayed delta. |
| `git archive 5b2ea16af484965b3dd34f6ca4198dd903732541 <selected paths> \| tar -x -C .temp/TASK-261005-1379z0/candidate` | 0 | `pipefail` enabled; read-only extraction for static inspection. |
| `gh run view 37349767142 -R relux-works/codex --json headSha,conclusion,jobs,url` | 0 | All four jobs success. |
| `gh run view 37349767142 -R relux-works/codex --log` | 0 | Independently fetched exact-checkout base execution evidence. |
| `gh run view 37317490875 -R relux-works/codex --log-failed` | 0 | Retrieved m4 failure log; this is retrieval success, not mutant-test success. |
| `gh run view 37317410177 -R relux-works/codex --log-failed` | 0 | Retrieved m10 failure log. |
| `gh run view 37317600437 -R relux-works/codex --log-failed` | 0 | Retrieved m8 failure log. |

Additional successful read-only resource retrievals (each exit 0): `surface-table.md`, `producer-brief.md`, `final-plan.md`, `TASK-260929-1ma0pr_results.md`, `TASK-260929-1ma0pr_mutants.json`, `TASK-260929-1ma0pr_hosted-precheck-3.md`, `TASK-260929-1ma0pr_change-request_rev2-validation.log`, and `TASK-260929-1ma0pr_review-verdict-rev1-recorded.md`. AC, resource-list, notes, panel-checklist and run-directive reads succeeded. Tool readiness was checked for task-board, git, rg, gh, python3 and apply_patch; outputs retained in task scratch.

Outcome structural gate: standalone `python3` here-doc using `json`, `pathlib`, `re` and `subprocess`, exit **0**. It asserted exactly one verdict-findings block, the four required JSON keys, no findings, exactly the three supplied surface names once in order, valid held results, exactly one standalone verdict `accept`, outcome below 24 KiB, replay-tree equal to snapshot-tree, all four hosted base jobs successful, and empty `git status --porcelain`. No Rust process was involved.

Read-only discovery failures were not gates or passing evidence: an initial board projection requested unsupported `resources` (exit 1, replaced by `outcomeResources preconditionResources` after schema inspection); the installed skill's referenced reviewer role file was absent (`cat`, exit 1); an initially guessed app-server file path did not exist (`rg`, exit 2, relocated to `src/request_processors/thread_queue_processor.rs`). Review follows the supplied explicit round contract and the installed context, breaking-change, testing and change-size skill bodies. No missing prerequisite was silently represented as read.

## Hosted evidence: executed elsewhere, not rerun locally

The base run API reports workflow head `c9bf761a4c3107479acf4fa6722d271866d0a941`. That is NOT the tested snapshot. Checkout and verification logs explicitly use `a743b62596aa374bcc63075c982f2917f3feb673` in all four lanes; local Git verifies that snapshot's tree equals the replayed candidate. Thus the tested-tree claim does not rely on the workflow head SHA.

Independently read base run 37349767142:

| Lane | Executed result | Bound |
| --- | --- | --- |
| core | 4967/4967 passed, 11 skipped; job success | Named tests below have individual PASS lines, not just suite summaries. |
| small | 260/260 passed, 0 skipped; job success | Includes the queue crate and forged-payload public-entry regression. |
| app-server | 1829/1829 passed, 2 skipped; job success | Supports exhaustive/public integration compatibility; skipped tests are not counted as executed. |
| lint | job success | The truncated local validation log is not used to infer its missing clippy tail. |

The base jobs report success; no explicit numeric shell exit is printed for their successful test steps in the inspected excerpts. The `gh` retrievals exited 0. These are distinct facts. No local test execution or local exit-0 Rust gate is claimed.

Primary log citations for run 37349767142, in `hosted-run.log`: checkout/verification core lines 38–157; core fragment attacks 4992–4999; serde/refusal/batching 5761–5781; public-entry history/resume/batching 7564–7567; two-entry wake 8654; core summary 9172; app-server summary 15332; queue-forgery PASS 19215; small summary 19416. Line numbers refer to the fetched log, not source code.

Hosted precheck 3 additionally attests base runs 37317650053 and 37352331583 (all four lanes success) and all 10/10 narrowing mutants killed, 0 survivors. Those extra base runs and seven remaining mutant logs are accepted from that attached resource, not independently fetched by this panel.

Independently fetched narrowing failure evidence:

| Mutant/run | Observed failure | Actual hosted exit |
| --- | --- | ---: |
| m4-batch-cap-9 / 37317490875 | Unit eight-plus-one gate fails and real wake/transport nine-item test times out waiting for the missing second wake, after all retries. | core `just test`: 100 |
| m10-follow-up-readmits-runtime / 37317410177 | In-turn predicate unit test fails; nine-item and two-item wake public-entry tests fail after all retries. | core `just test`: 100 |
| m8-record-persists-trigger-metadata / 37317600437 | Wake/rollout/resume invariant test fails after all retries. | core `just test`: 100; lint: 1 |

These are expected-red executions and remain failures, not passing suites. The fetched m4/m10/m8 logs contain explicit `Process completed with exit code` records. The seven other mutants' numeric command exits are unknown to this panel; their killed results and named tests are attributed only to hosted-precheck-3.md.

## Static attacks and bounded free hunt

1. **Fragment bound/injection/classification.** `core/src/context/exec_completion.rs:87` renders escaped data before truncation; `:126` subtracts actual wrapper overhead; `:167` escapes ampersands/angles and ASCII controls; `:183` preserves UTF-8 boundaries and reserves the truncation marker. Fixed numeric fields cannot inject separators. No command or raw output field exists in the completion snapshot. Production `hook_runtime.rs:777` uses this fragment and records contextual ResponseItems. Classification uses the pre-existing internal wrapper; host `exec.completion` annotation, not receipt-looking text, determines non-authorization. Existing user authorization classifier at `context/contextual_user_message.rs:58` preserves real user/legacy messages even when they quote the wrapper. Syntactic context matching itself is not an authenticity or receipt-ack gate.
2. **Batch/retention/spin.** `tasks/mod.rs:488` leases with the eight-fragment constant; `session/runtime_mailbox.rs:145` filters leased/suspended entries before FIFO `.take(limit)` and leaves the remainder in the mailbox. `session/input_queue.rs:578` sees only in-turn deliverable input/mail, not idle-only runtime entries. This blocks the capped-remainder spin without hiding runtime work from the separate idle pending/trigger predicates (`runtime_mailbox.rs:117`, `:127`). Hosted 9-item test asserts cumulative history 9 and rollout count 9. The unit gate independently pins first batch 8 and retained batch 1. Full ack/fail/cancel production wiring is not claimed by this staged leaf.
3. **Serialization/persistence/resume.** Internal `session/input_queue.rs:43` includes the skipped-deserialization variant and `:63` manually serializes existing arms but refuses every ExecCompletion, including empty vectors. RefusingEnvelope preserves the existing annotated-item refusal. Public `protocol::TurnInput` is not extended. `app-server/src/request_processors/thread_queue_processor.rs:336` rejects non-user queue items without panic. `ext/queue/src/service.rs:405` discards invalid/non-user payloads before dispatch; the new test at `ext/queue/tests/queue_service.rs:1085` exercises this real service with a forged persisted payload followed by a live user item, then checks the actual request. Recording remains ResponseItem-only; resume tests drive restart after real wake transport and after a forged ResponseItem admitted through start_turn_if_idle.

Bounded free hunt additionally examined test staging, public/internal API separation, serialization order/flattened fields, lease-token ownership, suspended/leased trigger states, abort/lease-drop exposure and changed-file size. No additional in-scope reproduced defect was found. Review did not extend into deferred real-process publication, transport acknowledgement, cancellation/retry integration or tool exposure (stories D/E/F). The public test admission helper is synthetic, though subsequent wake/record/transport/resume paths are real. Therefore this review is not an end-to-end real-process notification capability attestation.

## Logbook-carrying observations and review bounds

- The revision-1 `queue-test-coverage-attestation` failure is resolved on this candidate: run 37349767142's small lane executes `codex-queue-extension::queue_service::forged_exec_completion_payload_is_skipped_without_panic` and reports PASS, rather than merely containing the source test. Queue coverage is now established, not inferred from app-server success.
- Batch limits mean **newly delivered** fragments (8, 6144 UTF-8 bytes), not all accumulated request history. Accepted plan section 5.2 explicitly permits normal history repetition; the second wake request holds nine cumulative fragments. This panel does not attest a total-history/request cap of eight. This wording ambiguity was already recorded by the revision-1 review, not newly introduced by revision 2.
- Replay delta is 2344 insertions and 16 deletions across 18 paths, including mailbox foundation. This exceeds the 800-line review guidance. A future split can separate mailbox foundation, fragment/serde, and wake/record integration plus public-entry tests. It is a reviewability note, not an independently reproduced defect requiring rejection of this frozen rework.
- `ExecCompletionFragment` itself is 197 lines, below the leaf's 500-line module bound. No new individual model-context item exceeds the 768-byte bound; historical accumulation is not asserted bounded by this leaf.
- No control-root logbook file was edited. These task-scoped outcome observations carry the logbook handoff allowed by the run write boundary. No finding, verdict, note, checklist, status, accept/reject or handoff write was made on TASK-260929-1ma0pr.

Coverage: surface rows **3/3** held, AC clauses **5/5** addressed within staged scope, attached narrowing results **10/10** killed, independently fetched mutant failure logs **3/10**. Blind spots: seven mutant logs and two extra base runs rely on attached precheck evidence; deferred production publisher and sampling-ack lifecycle are outside this leaf; skipped hosted tests and platform execution beyond the cited hosted lanes are not attested.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Replay from base 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47 produces exactly candidate tree 5b2ea16af484965b3dd34f6ca4198dd903732541; read-tree, cached apply, and write-tree each exited 0.",
    "Independently verified hosted run 37349767142 checks out a743b62596aa374bcc63075c982f2917f3feb673, whose tree equals the candidate; workflow headSha c9bf761a4c3107479acf4fa6722d271866d0a941 is not used as the tested-tree pin.",
    "Prior queue-test-coverage-attestation is resolved: queue-selecting small lane reports PASS for forged_exec_completion_payload_is_skipped_without_panic at fetched base log line 19215. No assertion relies on the truncated local validation tail.",
    "Bound means newly delivered fragments <=8 and <=6144 bytes. Normal cumulative history repetition is explicitly allowed by final-plan.md section 5.2; this is not a total-request/history size attestation.",
    "All 10 narrowing mutant kills and the two additional green base runs are accepted from hosted-precheck-3.md. This panel independently fetched base run 37349767142 and m4/m10/m8 failure logs; their core test exits are 100, with m8 lint exit 1. No local builds or Rust tests ran.",
    "Delta is 2344 insertions and 16 deletions across 18 files, above size guidance; dependency-ordered foundation/fragment/integration split is a reviewability suggestion, not a reproduced in-scope defect.",
    "Real-process publication, sampling acknowledgement, cancellation/retry production integration and tool exposure remain staged to D/E/F. Tests use synthetic admission followed by real wake/record/transport/resume. Those deferred capabilities are not attested.",
    "Bounded free hunt swept API separation, serialization compatibility, staging races, lease-token isolation, suspended/leased trigger semantics and abort exposure; no additional in-scope defect found. Logbook observations travel in this task-scoped outcome, with no direct control-root edits and no writes on TASK-260929-1ma0pr."
  ],
  "surface_results": [
    {
      "row": "exec-completion fragment",
      "result": "held",
      "detail": "Post-escape wrapper-inclusive UTF-8 cap, field injection and host classification traced through hook_runtime::record_pending_input. Exact-tree base log lines 4992-4999 and 7564 verify adversarial fragment/classifier and forged-history/restart tests; attached m1/m2/m3/m5 narrowing kills corroborate the gates. No receipt privilege is derived from model-visible text."
    },
    {
      "row": "batching and retention",
      "result": "held",
      "detail": "Production idle starter leases at most eight FIFO non-suspended unleased entries, retains the remainder, and separates idle runtime triggers from in-turn pending input. Exact-tree base unit/public-entry PASS lines 5765,5779,7565,8654; independently fetched m4/m10 logs fail core tests with exit 100. Attached m9 proves suspended exclusion. Held for new admission, not cumulative request history; acknowledgement integration remains deferred."
    },
    {
      "row": "internal TurnInput variant and persistence",
      "result": "held",
      "detail": "Internal empty/populated serialization refusal and deserialization refusal, existing JSON encoding compatibility, ResponseItem-only record/restart, and public queue rejection all traced. Base PASS lines 5761,5763,5781,7564,7567 and queue-service PASS 19215 address the former execution gap. Attached m6/m7 and independently fetched m8 narrowing kills support refusal/compatibility/persistence sensitivity; m8 core exit 100 and lint exit 1 are failures, not passing gates."
    }
  ],
  "free_hunt": []
}
```
