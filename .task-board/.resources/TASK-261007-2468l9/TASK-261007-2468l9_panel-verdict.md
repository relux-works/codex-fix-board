# R141 panel A — notify-on-exit and exec-notification activation, revision 1

accept

Panel task: TASK-261007-2468l9 — r141-panel-a-task-260929-3r7peh-rev1.
Read-only subject: CR-TASK-260929-3r7peh-1, revision 1. This is an independent, non-recording recommendation, not CR acceptance.

Replay: base `2f522b9dc9d639fe5195d93d61431a0caff662d5` plus the attached revision-1 patch yielded `dbd39ab8c59adabe27ebb25838003680214c8d14`, exactly the expected candidate tree. The hosted snapshot commit `74434fa5` independently resolves locally to that same tree. Candidate inspection used pinned `git show` blobs; the run branch was not changed.

## Review bounds and key aspects

Decision: supply the orchestrator's panel recommendation for this exact candidate. Frozen precondition: revision-1 patch/base/candidate tree above; grammar freezing is not applicable. Worker budget: 40 minutes including evidence packaging; free hunt bounded to 5 minutes after the ordered four-row sweep. Artifact budget: one text outcome, below 32 KiB, no archive. Serial prerequisites: zero. Exit: replay identity, one result per surface row, verdict JSON validated and outcome attached. Consumer: the recording reviewer merges panel recommendations before the notification-activation implementation can be accepted. No new implementation or research prerequisite is created.

Coverage: **4/4 surface rows held under the named attacks**, **8/8 AC rows mapped to named tests** in the producer results, **9/9 mutant patches independently apply-check clean**. Hosted precheck 3 reports **9/9 killed, 0 survivors**. This is measured coverage of named attacks, not proof of absence. The full suite was not rerun by this panel. The local CR validation log explicitly records four green command shards, but its 64 KiB board cap prevents treating it as a complete raw hosted test log.

Static review traced root/child capability seeding, schema/handler refusal, opt-in selection, reservation-before-spawn, receipt owner and generation checks, release/cancel, retained output bounds, both exit enqueue callers, goal lifecycle activation and the user-input admission fast path. The background fragment implementation is unchanged and bounded to 768 bytes each, eight fragments per request; the new failure-detail input is capped before enqueue. No config, CLI flag, app-server wire payload, dependency or rollout format changes were found in the patch. `completion_receipt` is an added internal output field and model-facing acknowledgement text.

The bounded free hunt found no reproduced blocking mechanism. Two watcher/retention ordering suspicions and the incomplete m1 killer names are recorded explicitly as notes, with concrete hosted test requests. Neither suspicion is claimed to have executed. The large diff is also noted with a possible staged boundary.

## Commands personally run and real exit codes

Every replay and validation command ran as a standalone process, without `tee`. No cargo, just, build or product test was run.

| Command | Exit | Observed result |
|---|---:|---|
| `task-board m 'set_status(TASK-261007-2468l9, status=analysis)'` | 0 | Panel task entered analysis |
| Readiness: `command -v task-board`, `git --version`, `rg --version`, `task-board --version`; `python3 --version` | 0 | Output stored in run-local `.temp/TASK-261007-2468l9/readiness.log` |
| `task-board resource get TASK-260929-3r7peh TASK-260929-3r7peh_change-request_rev1.patch --output .temp/TASK-260929-3r7peh_change-request_rev1.patch` | 0 | Patch materialized read-only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2468l9-replay.idx" git read-tree 2f522b9dc9d639fe5195d93d61431a0caff662d5` | 0 | Temporary index initialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2468l9-replay.idx" git apply --cached .temp/TASK-260929-3r7peh_change-request_rev1.patch` | 0 | Revision-1 patch replayed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2468l9-replay.idx" git write-tree` | 0 | Exact candidate tree, MATCH |
| `git rev-parse '74434fa5^{tree}'` | 0 | Hosted snapshot has the same candidate tree |
| `git diff --check 2f522b9dc9d639fe5195d93d61431a0caff662d5 dbd39ab8c59adabe27ebb25838003680214c8d14` | 0 | Patch whitespace check green |
| `git rev-list --count HEAD..main`; `git rev-parse HEAD` | 0 | Count 0 against local main; HEAD is the pinned base. No fresh-trunk or build claim is based on this check |
| Candidate file materialization/static reads (`git show`, `sed`, `rg`), review-state writes | 0 | Candidate blobs inspected; temporary artifacts only |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` (safe checkpoints) | 0 | No directives; run not goal-bound |

Each command below used `GIT_INDEX_FILE="$PWD/.temp/TASK-261007-2468l9-replay.idx" git apply --cached --check .temp/TASK-261007-2468l9/mutants/<name>.patch` against the replayed candidate index:

| Mutant | Apply-check exit |
|---|---:|
| `m1_arm_by_default` | 0 |
| `m2_derive_child_from_not_exec` | 0 |
| `m3_accept_opt_in_on_unavailable_host` | 0 |
| `m4_release_skips_mailbox_cancel` | 0 |
| `m5_read_skips_owner_verify` | 0 |
| `m6_handler_drops_opt_in` | 0 |
| `m7_goal_never_enables` | 0 |
| `m8_goal_always_enables` | 0 |
| `m9_recheck_skips_retention_drop` | 0 |

Read/discovery failures (not gates and not presented as passing): the initial `rg --files agents/skills .claude/skills .codex/skills -g SKILL.md` exited 2 because the first two directories do not exist; the combined inspection call also exited 2. An initial board projection containing `resources` exited 1 (unknown field); corrected to `description scope ac notes`, exit 0. The first reviewer-contract path read exited 1 (missing file); the installed `.agents` reviewer contract was located and read, exit 0. Candidate materialization attempted `core/src/session/runtime_notifications.rs`: its individual `git show` exited 128 (path absent); the actual `runtime_mailbox.rs` and `input_queue.rs` were subsequently inspected successfully. `task-board resource list` exited 0 but printed help, so no resource-list claim was inferred. Some large display outputs were truncated; the decisive sections were then read narrowly. No failed or partial read was treated as absence evidence.

Hosted evidence is **accepted from attachments, not personally rerun**. Precheck 3 reports the base run's lint/core/app-server/small conclusions as `success`; mutant runs report failing lanes and named killers. It does not supply numeric process exit codes, which remain unknown here. The CR validation log explicitly records `[exit 0]` for the visible fast-lane command shards; those are producer executions. Their codes are not panel executions.

Outcome validation: `python3 .temp/TASK-261007-2468l9/validate-verdict.py` verifies one verdict-findings JSON block, exact unique surface-row coverage, findings fields/severities, one-word verdict and the artifact budget. Observed exit **0**: one JSON block, one accept verdict, all 4 rows once, no blocking findings, 14994-byte initial draft and below-32-KiB attached text. The same validator is rerun on this updated text before attachment.

## Sources and review logbook

- [surface-table.md](/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-3r7peh/surface-table.md) — read-only source.
- [producer-brief.md](/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-3r7peh/producer-brief.md) — read-only source.
- [TASK-260929-3r7peh_results.md](/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-3r7peh/TASK-260929-3r7peh_results.md) — read-only source.
- [TASK-260929-3r7peh_hosted-precheck-3.md](/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-3r7peh/TASK-260929-3r7peh_hosted-precheck-3.md) — read-only source.
- [TASK-260929-3r7peh_mutants.json](/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-3r7peh/TASK-260929-3r7peh_mutants.json) — read-only source.
- [TASK-260929-3r7peh_change-request_rev1-validation.log](/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-3r7peh/TASK-260929-3r7peh_change-request_rev1-validation.log) — read-only source.
- [TASK-260929-3r7peh_change-request_rev1.patch](/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-3r7peh/TASK-260929-3r7peh_change-request_rev1.patch) — read-only source.

Source claims were cross-checked against the exact candidate paths named in the JSON below, using `git show dbd39ab8c59adabe27ebb25838003680214c8d14:<path>` with the `codex-rs/` prefix. Surface row citations abbreviate `core/src/` or `ext/` paths. Hosted run IDs come directly from the precheck resource, not inferred from unrelated runs.

Logbook entry: replay and snapshot identities match; surface sweep reached 4/4; source task was read only. The former m9 pre-enqueue mutant survivor was replaced before this CR; present m9 checks only retention-drop cleanup. The late watcher-insertion and sampled-before-recheck schedules remain unmeasured suspicions. m1's truncated killer names are an evidence bound. These observations travel in this task-scoped outcome; no control-root LOGBOOK.md was edited.

No accept/reject/withdraw/status/handoff, notes, checklist or resource mutation was made on TASK-260929-3r7peh. The only board writes belong to this panel task. No repository source changes, commits, branch switches or nested worktrees were made. This text is staged in ignored run-local scratch; its attached outcome is stored outside the worktree solely by the allowed resource CLI.

The result is ready for review. Verdict JSON follows; free_hunt lists reproduced findings beyond the table, hence is empty. Unconfirmed observations are notes.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "retained-exit-arm-order-unconfirmed",
      "row": "exec_notification read and release",
      "severity": "note",
      "mechanism": "async_watcher.rs:211-232 publishes the store exit before await-locking and inserting output. process_manager.rs:818-833 assumes retention already exists when Arm observes Queued. The Retained publication branch never calls enqueue itself.",
      "observation": "Static candidate schedule to investigate: cache Alive; watcher publishes Retained then waits for output-buffer lock; launch arms and enqueues with Absent retention, returns its receipt; release removes binding/retention; watcher inserts pending output with queue_wake=false. No deterministic public-entry reproduction was run or attached, so late ghost retention and incorrect wake metadata remain unknown, not established defects. Existing m9 kills enqueue-helper cleanup with retention already inserted; it does not measure this insertion-after-cleanup ordering.",
      "requested_attack": "Add a deterministic watcher/arm barrier test, named exec_notification_exit_before_arm_retention_release_race, driving exec_command -> exec_notification release with the real exit watcher paused after publish_exit and before insert_pending. Assert no retained bytes, no mailbox item, and slot freed after resuming watcher. Run via just test -p codex-core on a hosted exact-candidate snapshot.",
      "repeat-of": "none"
    },
    {
      "id": "sampled-before-enqueue-recheck-unconfirmed",
      "row": "exec_notification read and release",
      "severity": "note",
      "mechanism": "receipt_hooks.rs:380-391 cleans retention for every status other than Queued, including Sampled; enqueue_runtime_notification publishes mailbox activity before this recheck.",
      "observation": "Investigate an independent wake or stdin claim sampling between mailbox enqueue and the status recheck. Cleanup might discard still-readable sampled output. Neither a forced interleaving nor a failing public-entry read exists in the attached evidence; classification is suspicion only.",
      "requested_attack": "Hosted deterministic public tool test exec_notification_sampled_before_enqueue_recheck_keeps_output: pause enqueue helper after mailbox admission, sample/claim via real wake or write_stdin, resume recheck, then exec_notification read must retain terminal output.",
      "repeat-of": "none"
    },
    {
      "id": "m1-killer-identity-bound",
      "severity": "note",
      "observation": "Precheck 3 reports m1 killed but lists only _disabled_expects, _enabled_expects, _escalated_expects suffixes. Do not assert the expected parser/no-wake tests were the observed killers. Base all-green plus the m6 named public-entry kills support the opt-in row; recover full m1 test names if stronger mutation attribution is wanted."
    },
    {
      "id": "large-review-unit",
      "severity": "note",
      "observation": "Exact diff is 31 files, 3188 insertions and 37 deletions. It exceeds the repository 800-line guidance. A possible preparatory stage is the dormant AsyncNotificationSupport type plus explicit ThreadManager inheritance tests, followed by tool/delivery activation and then goal-policy activation, retaining end-to-end coverage for the activated stage. Current behavior reviewed as one candidate; no size-only blocking finding."
    }
  ],
  "surface_results": [
    {
      "row": "host capability",
      "result": "held",
      "evidence": "Hosted base 37618361186; m2 37618411404 and m3 37618436832. ThreadManager::start_thread/spawn_internal_session inheritance negatives and exec_command public handler refusal. Static trace: thread_manager.rs:2190-2209, spec_plan.rs:1119-1132, exec_command.rs:260-279. Bounds: trusted ExtensionDataInit may override the source; no untrusted marker setter found."
    },
    {
      "row": "opt-in and receipts",
      "result": "held",
      "evidence": "Hosted base 37618361186 runs default no-wake and 65th-pre-execution-refusal integration attacks; m6 37618514232 killed by capacity and opt-in suites. m1 37618386393 killed, but report exposes only suffixes, so exact expected m1 killer identity is not inferred. Static trace: notify_on_exit serde(default), handler selects NotifyOnExit only on true, process_manager.rs:544-579 reserves before open_session_with_sandbox; stdin never reserves; process cap code unchanged."
    },
    {
      "row": "exec_notification read and release",
      "result": "held",
      "evidence": "Hosted base 37618361186: read output/wake fragment, unknown receipt and file-gated release/no-later-wake public tool suites. Hosted m4 37618462152, m5 37618487494, m9 37618590261 kill mailbox-cancel, owner-verify and ghost-retention weakening. Static: exec_notification.rs:98-153; receipt_hooks.rs:273-296,312-391. Clamp is 9000 body tokens plus bounded header; UUID is parsed and trim-normalized; stale release removes binding; release touches no process kill path. Bounds: m9 invokes enqueue helper directly, not a deterministic watcher/arm race."
    },
    {
      "row": "activation",
      "result": "held",
      "evidence": "Hosted base 37618361186: background_wait_activation_gates_goal_but_admits_user_input, background_wait_inactive_on_unavailable_host_auto_continues and receipt-to-mailbox-to-fragment suite. m7 37618540192 and m8 37618565570 fail named integration tests. Static: goal extension on_thread_start activates from marker; goal_admission.rs:54 bypasses non-Automatic/non-goal starts. Bounds: user admission is driven; follow-up admission is supported by unchanged shared fast path, not a new separately measured test."
    }
  ],
  "free_hunt": []
}
```
