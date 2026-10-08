# R141 panel B — CR-TASK-260929-1ma0pr-2

accept

## Replay and scope

Base: `47f7a80476eb78f27f7ce97c8bf7eb9236c40b47`.
Expected and replayed candidate tree: `5b2ea16af484965b3dd34f6ca4198dd903732541`.
The patch was replayed using a separate Git index, not the working index or a nested worktree. The write-tree value matches exactly. Candidate source was read using `git show <candidate-tree>:<path>`; this review does not rely on the Story checkout's HEAD being current trunk.

Read-only, non-recording review. No cargo, just, build, test, commit, branch switch, or source edit was performed. No mutation, resource attachment, status, accept/reject, or handoff was made on TASK-260929-1ma0pr. All outcome and lifecycle writes belong to TASK-261005-cd2m0l. Artifact staging stays inside the run worktree to honor the explicit run-write boundary; the board receives only this text outcome through its CLI.

## Commands and exit codes

These replay/gate commands ran as standalone commands, without tee or status-masking pipelines:

| Command | Exit | Result |
|---|---:|---|
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-cd2m0l-replay.idx" git read-tree 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47` | 0 | Base index loaded |
| `task-board resource get TASK-260929-1ma0pr TASK-260929-1ma0pr_change-request_rev2.patch --output .temp/TASK-260929-1ma0pr_change-request_rev2.patch` | 0 | Supplied CR patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-cd2m0l-replay.idx" git apply --cached .temp/TASK-260929-1ma0pr_change-request_rev2.patch` | 0 | Patch applied to base |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-cd2m0l-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git diff --check` | 0 | Review introduced no tracked delta |
| `python3 .temp/TASK-261005-cd2m0l/verify-verdict.py` | 0 | Single JSON block; exact three surface rows; exact-tree hosted checkout, queue attacks and ten mutant test failures verified |

Readiness: `git --version`, `task-board --version`, `gh --version`, `python3 --version` succeeded (0). Task-specific resource retrieval succeeded (0) for surface-table, producer brief, results, precheck 3, rev2 validation log, recorded rev1 verdict, and mutants. GitHub API reads succeeded (0) for snapshot commit identity, the three base-run conclusions, base-run jobs, and ten mutant job inventories. Downloads of the core/small base logs and ten mutant core logs with `gh api .../logs --allow-escape-sequences` each exited 0. No hosted test was rerun by this panel.

Exploratory failures are not passing gates: unsupported board projections (`resources`, `attachments`) exited 1; `schema(get)` returned a typed argument error; nonexistent remote `relux` and the old app-server path lookup failed and were corrected to origin and `request_processors/thread_queue_processor.rs`. The initial replay shell request containing `rm -f` was rejected before execution; all four actual replay steps above subsequently ran independently. Initial plain gh log downloads refused terminal escape sequences; their per-command exit statuses were masked by subsequent reads, so they are unknown, not successes. The successful explicit retry logs are the evidence used here.

## Evidence identity and coverage

Bounded decision: advise the recording reviewer whether rev2 is acceptable. Frozen precondition is the supplied base/patch/tree triple; no new grammar is designed. Scope is three surface rows plus one static free hunt, no serial prerequisites or new research leaves. Artifact budget is one text verdict; no archive. Exit criterion is replay identity plus one evidenced result for each row and a machine-readable verdict.

Source resources on the reviewed task (read-only): `surface-table.md`, `TASK-260929-1ma0pr_results.md`, `TASK-260929-1ma0pr_hosted-precheck-3.md`, `TASK-260929-1ma0pr_mutants.json`, and `TASK-260929-1ma0pr_review-verdict-rev1-recorded.md`.

Direct provider checks supplement those resources:

- Snapshot `a743b62596aa374bcc63075c982f2917f3feb673` has tree `5b2ea16af484965b3dd34f6ca4198dd903732541` per GitHub commit metadata.
- Runs 37317650053, 37349767142 and 37352331583 report success. Run 37349767142 has four successful lanes. Its workflow head is `c9bf761a4c3107479acf4fa6722d271866d0a941`, NOT the tested snapshot: core job 111897364633 and small job 111897364935 explicitly check out and verify the full a743b625 snapshot SHA. This distinction was checked rather than inferring tree identity from the workflow head.
- Core job's raw log reports 4967 passed, 11 skipped. The task-specific fragment, serde, batching, wake, forged-history and resume tests all have individual PASS records. The lane excludes three named unrelated zsh-fork tests; this review makes no claim about those or all-platform coverage.
- Small job's raw log includes PASS for `codex-queue-extension::queue_service::forged_exec_completion_payload_is_skipped_without_panic` and `drain_leaves_persisted_queued_message_for_a_later_start`. The actual lane command includes `-p codex-queue-extension`, fixing the prior review's queue-test-coverage-attestation finding. This is executed queue evidence, not a proxy from core tests or a crate omitted by the command.
- Mutant coverage is 10/10 executed and killed, 0 survivors, from precheck 3. This panel independently queried all ten job inventories and read their core failure logs. Failed mutant gates remain failing: logs show nextest test failures and a nonzero process exit; they are evidence that a narrowed gate is detected, not a claim of ten passing suites.
- Full raw logs are retained under `.temp/TASK-261005-cd2m0l/` in this run; attached precheck 3 and the provider run/job IDs provide persistent source references. The CR validation log is truncated and is NOT used to attest any omitted local clippy exit.

Hosted core command (not rerun locally): `INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-core -E 'not ( test(=suite::skill_approval::shell_zsh_fork_skill_scripts_ignore_declared_permissions) | test(=suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_guardian_reviews_persistent_terminal_in_current_turn) | test(=suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_parent_approval_preserves_denied_reads))'`. It passed on the base snapshot (provider step success), but its numerical process exit is not explicitly printed in the successful log. The small command is `INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-tools -p codex-goal-extension -p codex-extension-api -p codex-rollout-trace -p codex-queue-extension`; it also reports provider success. No numeric success exit is invented from missing log text.

The same core command on each narrowing mutant reports **exit 100**, expected failure because its named refusal/bound assertion is violated. Each has a final TRY 3 FAIL record, not merely an unrelated flaky failure:

| Mutant | Run | Core job | Exit | Killing test (short name) |
|---|---:|---:|---:|---|
| m1 fragment cap 769 | 37317381008 | 111787440305 | 100 | nine_pending_completions_batch_eight_and_retain_one |
| m2 drop greater-than escaping | 37317438139 | 111787633193 | 100 | fragment_escapes_marker_injection_and_newlines |
| m3 reject exec source | 37317464801 | 111787730258 | 100 | fragment_is_classified_as_internal_context_not_user_text |
| m4 batch cap 9 | 37317490875 | 111787823355 | 100 | nine_pending_completions_batch_eight_and_retain_one |
| m5 user-prefixed kind | 37317518170 | 111787915999 | 100 | fragment_renders_all_fields_inside_the_internal_context_wrapper |
| m6 serialize empty internal variant | 37317545621 | 111788007114 | 100 | exec_completion_variant_refuses_serialization |
| m7 always emit user acceptance order | 37317574233 | 111788100212 | 100 | user_input_variant_serializes_byte_identically |
| m8 persist trigger metadata | 37317600437 | 111788192378 | 100 | wake_turn_persists_only_contextual_response_items_and_resume_stays_silent |
| m9 admit suspended trigger | 37317628533 | 111788285480 | 100 | runtime_suspended_entries_are_excluded_from_trigger_and_lease |
| m10 readmit idle runtime in follow-up | 37317410177 | 111787532677 | 100 | in_turn_follow_up_ignores_idle_only_runtime_entries |

## Surface sweep

| Surface | Result | Attack and production trace |
|---|---|---|
| exec-completion fragment | held | Hosted injection/classifier/long-id/multibyte tests and forged recorded-history/resume attack pass on the exact tree. `hook_runtime.rs:777` records `ExecCompletionFragment` through `record_conversation_items`; `exec_completion.rs:129` subtracts wrapper overhead before post-escape UTF-8 truncation, preserving the closing wrapper. m1/m2/m3/m5 narrow size, escaping, source classification and kind, and are killed. |
| batching and retention | held | Hosted nine-completion wake test traverses idle wake, recording and response requests; FIFO unit test asserts 8+1 and <=6144 newly rendered bytes. `tasks/mod.rs:488` admits at most 8 leases; `input_queue.rs:578` excludes idle-only runtime remainder from in-turn follow-up, preventing empty-resample spin. m4/m9/m10 narrow batch admission, suspension and follow-up, and are killed. |
| internal TurnInput variant and persistence | held | Empty and populated internal variants refuse serialization and forged deserialization; shadow-enum/literal checks preserve existing serialization. Hosted queue forged-payload test enters durable queue service and dispatches the live item behind the forgery. Hosted wake rollout/resume test persists contextual ResponseItems and resumes silently. m6/m7/m8 narrow empty serialization, user byte identity and metadata persistence, and are killed. |

Held means the cited attacks did not reproduce, not proof of absence. Surface coverage is 3/3; AC coverage is 5/5 within the staged semantics below. No row is inferred held merely because builds are forbidden locally.

## Bounds and logbook-carrying observations

1. Rev1's attestation finding is resolved for rev2: the actual small lane selects the queue crate and names both queue tests as passing. The historical rev1 verdict is not rewritten.
2. The bound is 8 NEW fragments per admission, not a total bound over cumulative request history. The second wake's request contains 9 historical fragments intentionally, while adding only the retained remainder. The accepted plan and prior recorded review allow history repetition. Literal total-request <=8/6144 wording needs clarification; this review does not attest that stronger incompatible property.
3. Receipt publication by real processes, sampling acknowledgement/fail/retry integration and tool exposure remain deferred to D/E/F. Current integration tests use the test admission hook, then real idle wake/record/request/rollout/resume entries. They do not prove real-process publication or failure/abort lease recovery. Snapshot failure text is caller-supplied classification data, not a validation that arbitrary future publishers omit raw output.
4. Static free hunt checked app-server/public-enum separation, annotated-item serialization refusal, hook bypass for internal completions, lease token matching, pending versus trigger predicates, and truncation framing. No reproduced additional defect. Suspected lease loss on aborted/failed sampling remains unverified and belongs to deferred acknowledgement wiring; no executed abort-recovery attack is claimed.
5. The supplied replay is 2344 insertions and 16 deletions across 18 paths, including mailbox foundation. It exceeds change-size guidance. A coherent split is mailbox foundation, then fragment/serde, then wake/record plus integration coverage. This is a reviewability note, not a reproduced behavioral failure.
6. Public protocol TurnInput and app-server schemas are unchanged. At this base, persistence uses `codex_protocol::turn_input::TurnInput`, distinct from internal core TurnInput. `ext/queue/src/service.rs:425` discards invalid persisted payloads and continues; `app-server/src/request_processors/thread_queue_processor.rs:336` returns a structured error for non-user queue items. No config, CLI or dependency delta was found.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Rev1 queue-test-coverage-attestation is resolved on rev2: exact snapshot small job 111897364935 selects codex-queue-extension and records both forged-payload and later-start queue tests PASS. This observation is carried for the logbook only; nothing was written on the reviewed task.",
    "Batch cap is incremental admission, not cumulative history. The nine-completion suite intentionally observes nine historical fragments in the second wake request. No total-request cap is attested.",
    "Real process publication, sampling acknowledgement, fail/cancel/retry integration and tool exposure remain staged to D/E/F. Abort-recovery behavior is unverified, not proved by helper mailbox tests.",
    "Full supplied delta is 2344 insertions and 16 deletions across 18 paths. Suggested reviewable stages: mailbox foundation, fragment/serde, wake/record integration. Size alone is not a blocking behavior finding.",
    "Hosted evidence is Linux, with eleven skipped core tests and three named zsh-fork exclusions. No local build/test or all-platform claim. Truncated local validation cannot prove omitted exits.",
    "Free hunt inspected serializer wrappers, public API separation, hook bypass, lease tokens, UTF-8/entity truncation and idle/in-turn predicates; no additional failing reproduction. Future failure-field publishers must preserve the no-command/no-output contract."
  ],
  "surface_results": [
    {
      "row": "exec-completion fragment",
      "result": "held",
      "detail": "Exact-tree core job 111897364633 records injection/classification/cap and forged-history-resume attacks PASS; static post-escape wrapper budget inspected; m1/m2/m3/m5 killed."
    },
    {
      "row": "batching and retention",
      "result": "held",
      "detail": "Exact-tree nine-completion public-entry wake/request/rollout attack and 8+1 FIFO byte-cap test PASS; m4/m9/m10 killed. Bound applies to new admission; ack/fail production wiring is deferred."
    },
    {
      "row": "internal TurnInput variant and persistence",
      "result": "held",
      "detail": "Exact-tree serde-refusal/identity and rollout/resume attacks PASS; exact-tree small job 111897364935 executes forged durable-queue dispatch attack PASS; m6/m7/m8 killed."
    }
  ],
  "free_hunt": []
}
```
