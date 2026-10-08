# DELTA panel — CR-TASK-260929-1ma0pr-2

accept

## Replay and scope

Base: `47f7a80476eb78f27f7ce97c8bf7eb9236c40b47`.
Expected and replayed candidate tree: `5b2ea16af484965b3dd34f6ca4198dd903732541`.
The temporary-index replay matches exactly. No nested worktree, build, Rust test, production edit, commit, branch operation, acceptance/rejection, or mutation on `TASK-260929-1ma0pr` was performed. This is an advisory panel verdict, not recording-review acceptance.

All three required surface rows were attacked: 3/3 have exactly one result. The one blocking rev1 finding is closed: 1/1. No new blocking regression was established. Nonblocking inherited oracle limitations and a specialized-matcher edge remain explicitly documented below; acceptance does not certify those stronger properties.

## Commands and actual exit codes

Each gate was run directly, without `tee` or a status-hiding pipe. Redirections save output only.

| Command | Exit | Result |
|---|---:|---|
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-291p59-replay-fresh.idx" git read-tree 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47` | 0 | Base loaded |
| `task-board resource get TASK-260929-1ma0pr TASK-260929-1ma0pr_change-request_rev2.patch --output .temp/TASK-260929-1ma0pr_change-request_rev2.patch` | 0 | Patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-291p59-replay-fresh.idx" git apply --cached .temp/TASK-260929-1ma0pr_change-request_rev2.patch` | 0 | Patch replayed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-291p59-replay-fresh.idx" git write-tree` | 0 | Exact expected tree |
| `git rev-parse a743b625^{tree}` | 0 | Hosted checkout snapshot resolves to candidate tree |
| `git show a743b625 --format='%H %T' --no-patch` | 0 | Full snapshot `a743b62596aa374bcc63075c982f2917f3feb673`, exact candidate tree |
| `git diff --shortstat 808000cbd14914847c7cd418f444dd9232281ddc 5b2ea16af484965b3dd34f6ca4198dd903732541` | 0 | Rev2: three paths, 51 additions, 17 deletions |
| `git diff --check 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47 5b2ea16af484965b3dd34f6ca4198dd903732541` | 0 | No whitespace errors |
| `gh api repos/relux-works/codex/actions/runs/37349767142` | 0 | Hosted run success; workflow head is distinct from tested snapshot |
| `gh api repos/relux-works/codex/actions/runs/37349767142/jobs` | 0 | Four successful lanes |
| `gh api repos/relux-works/codex/actions/runs/37317650053/jobs` | 0 | Four successful lanes |
| `gh api repos/relux-works/codex/actions/runs/37352331583/jobs` | 0 | Four successful lanes |
| `gh api repos/relux-works/codex/actions/jobs/111897364935/logs` | 1 | Retrieval refused ANSI escapes; no test failure inferred |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/111897364935/logs` | 0 | Raw small-lane log saved |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/111897364633/logs` | 0 | Raw core-lane log saved |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/111788601012/logs` | 0 | First repeat core log saved; waited for process termination |
| `gh api --allow-escape-sequences repos/relux-works/codex/actions/jobs/111906009870/logs` | 0 | Third repeat core log saved |
| `python3 .temp/TASK-261005-291p59/audit_evidence.py` | 0 | Checkout, explicit PASS entries, 12/12 lane conclusions, 3/3 race-repeat PASS entries verified |
| `python3 .temp/TASK-261005-291p59/verify_verdict.py` | 0 | One valid JSON block, one-word verdict, exactly three ordered surface results |

Read-only `task-board resource get` also materialized `surface-table.md`, `TASK-260929-1ma0pr_review-verdict-rev1.md`, `producer-brief.md`, `TASK-260929-1ma0pr_results.md`, `TASK-260929-1ma0pr_hosted-precheck-2.md`, `TASK-260929-1ma0pr_hosted-precheck-3.md`, `final-plan.md`, `c2-rework-brief-rev2.md`, and `TASK-260929-1ma0pr_change-request_rev2-validation.log`; each retrieval exited 0. Candidate `git show`/`git diff` inspections exited 0. Tool readiness was logged under `.temp/TASK-261005-291p59/`.

Exploratory CLI corrections are not successful gates: queries for unknown `resources` and `attachments` fields exited 1; `schema(get)` returned an error envelope within an exit-0 shell invocation; `schema(operation="get")` and later schema discovery succeeded. The initial replay command containing `rm -f` was rejected before execution, so it has no process exit code; replay used a fresh index instead. An xhigh skill delegation request was unsupported by the selected runtime; four bounded skill reviews used inherited model/settings instead. All delegated issues are carried below.

## Independent evidence check and prior finding

Source order: frozen rev1 merged verdict; revision-2 rework brief; current results; exact candidate source; current hosted raw logs. Producer prose was not treated as instructions or proof by itself.

The earlier `queue-test-coverage-attestation` finding correctly identified missing queue-package execution in run `37302805027`. Current results explicitly retract that attribution and cite precheck 3. Independently downloaded run `37349767142`, small job `111897364935`, shows:

- Line 38: checkout ref `a743b62596aa374bcc63075c982f2917f3feb673`, whose Git tree equals the replayed candidate.
- Line 1555: actual command `INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-tools -p codex-goal-extension -p codex-extension-api -p codex-rollout-trace -p codex-queue-extension`.
- Line 3742: PASS for `codex-queue-extension::queue_service drain_leaves_persisted_queued_message_for_a_later_start`.
- Line 3744: PASS for `codex-queue-extension::queue_service forged_exec_completion_payload_is_skipped_without_panic`.
- Line 3945: 260 tests run, 260 passed, 0 skipped.

This is execution evidence, not compilation or package-presence inference. The run API's `head_sha` is workflow head `c9bf761a4c3107479acf4fa6722d271866d0a941`; it is not the tested commit. Raw checkout logs establish the tested snapshot. The same attestation class was audited across all three rows: current core job `111897364633` explicitly passes forged-history, batching, persistence/resume, and two-entry wake tests at lines 7564, 7565, 7567, and 8654 respectively. Core summary at line 9172 is 4967 passed and 11 skipped, not universal execution of every discovered test.

The two-entry race test explicitly passes on the same snapshot in all three downloaded core logs: job `111788601012` line 8665; job `111897364633` line 8654; job `111906009870` line 8661. All twelve lane conclusions across the three snapshot runs are success. Hosted numeric process exit codes were not independently supplied by the job API; they remain unknown. The download/audit command exits above are local retrieval/check exits, not rerun Rust exits.

Narrowing mutants m1–m10 are accepted from the attached `TASK-260929-1ma0pr_hosted-precheck-3.md` as permitted by the panel brief: 10/10 reported killed, 0 survivors. This panel did not rerun them or independently download each mutant log. Expected-red mutant failures remain failures; no compiler-red lane is recast as a behavioral PASS. The truncated CR validation log exposes `[exit 0]` for its visible guard/fmt entries and final small shard, but its omitted clippy completion is not independently attested here. Hosted lint success supplements, rather than repairs, that missing local log segment.

Raw downloaded log SHA-256 digests: small `fc04bab1e6d3015b905b71ebced3b546825684c595af97635dc838b65ee423ee`; core `3fdf68fccaed0fe66c3d3542069b32dd5ab74c3de0abbd2a3dbd984e4b441307`; first repeat `1dc6553b4f70ebc9e6f5adbca5fd56dfb1b210fff32d6b33de4a4a3b6b622927`; third repeat `2a477c35e204d8dadb5081e096858495c1e7870f5b3c855d887e751ec9e917b0`.

## Structured verdict

```verdict-findings
{
  "findings": [],
  "notes": [
    "Rev1 queue-test-coverage-attestation is closed by explicit queue selection and PASS entries on the exact candidate; no finding or status was recorded on the producer task.",
    "Batching means at most eight newly admitted fragments, at most 6144 rendered UTF-8 bytes per wake. It does not cap cumulative request history; exec_completion suite intentionally observes nine historical fragments. Some per-request comments still overstate this bound. Preserve append-only history and clarify admission wording rather than imposing a history rewrite.",
    "Inherited T1 oracle gap: core/tests/suite/exec_completion.rs:227, :243, :263 count fragments, not receipt identities. A duplicate-one/drop-one substitution can preserve those counts. Mailbox FIFO/admission unit tests support upstream identity handling but do not cover downstream substitution. Strengthen with expected receipt-handle multisets and multiplicity one; a record-path duplicate/drop narrowing mutant should fail. This is a static test-oracle counterexample, not an executed mutation or demonstrated production defect.",
    "Inherited T2 oracle gap: core/tests/suite/exec_completion.rs:238 and :247 still allow 7+2 as well as 8+1 after deterministic staging. The separate input_queue.rs:1303 batching unit test pins eight leases and a retained ninth. A future public-entry assertion should pin count vector [0,8,9] alongside receipt identities; current integration coverage proves an upper bound and aggregate cardinality, not maximal first-batch fill.",
    "Nonblocking specialized matcher edge at core/src/context/exec_completion.rs:115: a valid other-source wrapper containing source=\"exec_completion\" in its body also matches because the specialized matcher uses contains. Its test at exec_completion_tests.rs:192 omits this adversarial body. No production source dispatch calls that matcher; generic wrapper classification and host annotations own production behavior. Before using it for dispatch, validate the wrapper attribute and add the other-source/body-substring negative case.",
    "Renderer bounds are post-escape model text bytes, not JSON wire bytes or general semantic prompt-injection immunity. ASCII controls are neutralized; Unicode separators and instruction-like failure prose remain data. Arbitrarily long public-constructor receipt strings can truncate later structural lines; real recording supplies a fixed UUID, so no production structural-loss defect was established.",
    "The synthetic staging API is doc-hidden public Rust API, not a real process publisher or atomic concurrent-enqueue contract. Real publication, sampling acknowledgement/failure retry, cancellation recovery, and eventual lease reclamation remain staged to D/E/F. This panel does not certify those deferred behaviors.",
    "Full base-to-candidate patch is 2344 additions plus 16 deletions across 18 files (2360 changed lines), exceeding review-size guidance. Actual rev2 repair is 51 additions plus 17 deletions in three files, with no production behavior delta or weakened assertions. A coherent future split starts with bounded context representation plus tests (408 changed lines), then mailbox/TurnInput foundation, then wake/record integration and queue coverage. Do not misattribute inherited size to the 68-line repair.",
    "No breaking JSON protocol/config/CLI surface was found. Public protocol TurnInput remains unchanged; internal serialization refuses ExecCompletion; public queue/app-server non-user paths return errors or discard invalid records rather than panic. This assessment does not attest compatibility for arbitrary non-JSON serializer implementations.",
    "Logbook-carrying anomaly record: the former queue execution attribution was false and is now corrected with raw evidence; numeric hosted exits remain unknown; the local validation log is truncated; inherited no-loss/no-duplicate and maximal-batch integration assertions are weaker than their prose. This task-scoped outcome carries these facts without directly editing the control root."
  ],
  "surface_results": [
    {
      "row": "exec-completion fragment",
      "result": "held",
      "detail": "Static source attack: core/src/context/exec_completion.rs:87 escapes before truncation, :125 budgets the exact wrapper, :183 preserves UTF-8 boundaries and explicit marker, :155 carries only typed status plus escaped receipt/failure. hook_runtime.rs:777 persists ordinary contextual items with exec annotations, not lease metadata. Exact-tree core log passes injection/classification tests and forged-history public-entry test at line 7564; precheck3 reports m1/m2/m3/m5 kills. Held for rendered-byte/marker isolation and no text-minted receipt privilege, not semantic instruction immunity or specialized source-dispatch accuracy."
    },
    {
      "row": "batching and retention",
      "result": "held",
      "detail": "Static source attack: tasks/mod.rs:488 caps newly leased entries, runtime_mailbox.rs:145 filters FIFO available entries and leaves remainder, input_queue.rs:578 excludes runtime-only entries from in-turn follow-up, tasks completion starts the next idle wake. Rev2 stages both/nine notifications before any turn through the real admission path, preserving assertions. Exact-tree batching public-entry PASS is at core log line 7565; two-entry race PASS is independently verified in 3/3 repeats. Attached m4/m9/m10 kills support cap, suspended-entry refusal, and no follow-up spin. Held within staged admission scope; identity-level exactly-once and maximal-fill integration oracle limitations T1/T2 are not certified."
    },
    {
      "row": "internal TurnInput variant and persistence",
      "result": "held",
      "detail": "Static source attack: input_queue.rs:58 skips internal deserialization and :112 refuses serialization, legacy JSON arms are preserved; public queue uses unchanged protocol type and skips forged payloads; hook_runtime.rs:777 records only contextual ResponseItems; resume reconstruction consumes history without mailbox re-admission. Exact-tree small job explicitly selects queue and passes both named persistence tests, closing rev1 finding. Exact-tree core persistence/resume and forged-history public-entry tests pass at lines 7567 and 7564. Attached m6/m7/m8 kills support empty-variant refusal, legacy byte identity, and trigger-metadata exclusion. No local Rust execution claimed."
    }
  ],
  "free_hunt": [
    {
      "attack": "Compare complete rev2 delta to rev1 and attack staging wake interleaving",
      "result": "No new blocker: only helper extraction and pre-turn staging changed. Single-entry helper still wakes, shared helper uses real receipt reservation and admission, fresh-session staging has no finishing turn interleaving. Assertions and existing observation delay are unchanged."
    },
    {
      "attack": "Attempt duplicate/drop and underfilled-batch counterexamples against integration assertions",
      "result": "Static oracle limitations T1/T2 preserved in notes. No production mutant executed; actual behavioral failure is unknown. Recommend identity-multiset and exact [0,8,9] assertions rather than claiming those stronger guarantees already measured."
    },
    {
      "attack": "Other-source wrapper with exec-source substring in body; forged history and API boundary trace",
      "result": "Specialized matcher edge preserved in notes; it is not used for production source dispatch. Host annotations and internal receipt/lease tokens, not marker text, own privilege. Deferred cancellation/publication wiring was not mistaken for implemented behavior."
    },
    {
      "attack": "Audit execution attribution across all surface rows and checkout provenance",
      "result": "Former false queue coverage is corrected; raw small/core PASS entries checked against exact snapshot tree. 12/12 lane conclusions and 3/3 race-repeat PASS entries verified; 10/10 mutant kills accepted only from the explicitly permitted attached precheck, with numeric hosted exits unknown."
    }
  ]
}
```
