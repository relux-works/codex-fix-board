# Merged review verdict — TASK-260929-3r7peh CR revision 1 (tb-R141 / R132 merge)

Verdict: **accept**

Panel outcomes: `TASK-261007-2468l9_panel-verdict.md` (accept), `TASK-261007-j2lf0k_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [],
  "notes": [
    "[TASK-261007-2468l9] {'id': 'retained-exit-arm-order-unconfirmed', 'row': 'exec_notification read and release', 'severity': 'note', 'mechanism': 'async_watcher.rs:211-232 publishes the store exit before await-locking and inserting output. process_manager.rs:818-833 assumes retention already exists when Arm observes Queued. The Retained publication branch never calls enqueue itself.', 'observation': 'Static candidate schedule to investigate: cache Alive; watcher publishes Retained then waits for output-buffer lock; launch arms and enqueues with Absent retention, returns its receipt; release removes binding/retention; watcher inserts pending output with queue_wake=false. No deterministic public-entry reproduction was run or attached, so late ghost retention and incorrect wake metadata remain unknown, not established defects. Existing m9 kills enqueue-helper cleanup with retention already inserted; it does not measure this insertion-after-cleanup ordering.', 'requested_attack': 'Add a deterministic watcher/arm barrier test, named exec_notification_exit_before_arm_retention_release_race, driving exec_command -> exec_notification release with the real exit watcher paused after publish_exit and before insert_pending. Assert no retained bytes, no mailbox item, and slot freed after resuming watcher. Run via just test -p codex-core on a hosted exact-candidate snapshot.', 'repeat-of': 'none'}",
    "[TASK-261007-2468l9] {'id': 'sampled-before-enqueue-recheck-unconfirmed', 'row': 'exec_notification read and release', 'severity': 'note', 'mechanism': 'receipt_hooks.rs:380-391 cleans retention for every status other than Queued, including Sampled; enqueue_runtime_notification publishes mailbox activity before this recheck.', 'observation': 'Investigate an independent wake or stdin claim sampling between mailbox enqueue and the status recheck. Cleanup might discard still-readable sampled output. Neither a forced interleaving nor a failing public-entry read exists in the attached evidence; classification is suspicion only.', 'requested_attack': 'Hosted deterministic public tool test exec_notification_sampled_before_enqueue_recheck_keeps_output: pause enqueue helper after mailbox admission, sample/claim via real wake or write_stdin, resume recheck, then exec_notification read must retain terminal output.', 'repeat-of': 'none'}",
    "[TASK-261007-2468l9] {'id': 'm1-killer-identity-bound', 'severity': 'note', 'observation': 'Precheck 3 reports m1 killed but lists only _disabled_expects, _enabled_expects, _escalated_expects suffixes. Do not assert the expected parser/no-wake tests were the observed killers. Base all-green plus the m6 named public-entry kills support the opt-in row; recover full m1 test names if stronger mutation attribution is wanted.'}",
    "[TASK-261007-2468l9] {'id': 'large-review-unit', 'severity': 'note', 'observation': 'Exact diff is 31 files, 3188 insertions and 37 deletions. It exceeds the repository 800-line guidance. A possible preparatory stage is the dormant AsyncNotificationSupport type plus explicit ThreadManager inheritance tests, followed by tool/delivery activation and then goal-policy activation, retaining end-to-end coverage for the activated stage. Current behavior reviewed as one candidate; no size-only blocking finding.'}",
    "[TASK-261007-j2lf0k] Residual release-between-recheck-and-wake window in enqueue_published_completion is shared with the pre-existing wake race (producer-stated bound). Worst case is a spurious idle turn with no fragment, not a missed or ghost wake: release still cancels the mailbox entry, and the mailbox dedupes by receipt id. No CR-introduced hazard.",
    "[TASK-261007-j2lf0k] Interrupt/terminate/shutdown cancel store receipts but not mailbox entries; only release cancels the mailbox entry. Pre-existing deferred behavior, producer-stated; post-exit terminate is moot and the interrupt-after-enqueue window delivers an already-occurred exit.",
    "[TASK-261007-j2lf0k] Goal background_wait enables at thread start regardless of the goal enabled flag; dormant while disabled, already correct if enabled later. Producer-stated, no hazard.",
    "[TASK-261007-j2lf0k] MCP/Custom/Unknown hosts stay Unavailable (fail closed) until persistence is verified. Intended, covered by async_notification_roots_follow_host_session_source.",
    "[TASK-261007-j2lf0k] Candidate diff is 31 files, ~3188 insertions / 37 deletions, exceeding the 800-line guidance; the leaf is an atomic activation (schema + tool + delivery + policy must land together; sibling F2 stacks on it) and cannot be staged without shipping a half-promise. Accepted as justified."
  ],
  "surface_results": [
    {
      "row": "host capability",
      "result": "held",
      "evidence": "Hosted base 37618361186; m2 37618411404 and m3 37618436832. ThreadManager::start_thread/spawn_internal_session inheritance negatives and exec_command public handler refusal. Static trace: thread_manager.rs:2190-2209, spec_plan.rs:1119-1132, exec_command.rs:260-279. Bounds: trusted ExtensionDataInit may override the source; no untrusted marker setter found.",
      "reported_by": "TASK-261007-2468l9"
    },
    {
      "row": "opt-in and receipts",
      "result": "held",
      "evidence": "Hosted base 37618361186 runs default no-wake and 65th-pre-execution-refusal integration attacks; m6 37618514232 killed by capacity and opt-in suites. m1 37618386393 killed, but report exposes only suffixes, so exact expected m1 killer identity is not inferred. Static trace: notify_on_exit serde(default), handler selects NotifyOnExit only on true, process_manager.rs:544-579 reserves before open_session_with_sandbox; stdin never reserves; process cap code unchanged.",
      "reported_by": "TASK-261007-2468l9"
    },
    {
      "row": "exec_notification read and release",
      "result": "held",
      "evidence": "Hosted base 37618361186: read output/wake fragment, unknown receipt and file-gated release/no-later-wake public tool suites. Hosted m4 37618462152, m5 37618487494, m9 37618590261 kill mailbox-cancel, owner-verify and ghost-retention weakening. Static: exec_notification.rs:98-153; receipt_hooks.rs:273-296,312-391. Clamp is 9000 body tokens plus bounded header; UUID is parsed and trim-normalized; stale release removes binding; release touches no process kill path. Bounds: m9 invokes enqueue helper directly, not a deterministic watcher/arm race.",
      "reported_by": "TASK-261007-2468l9"
    },
    {
      "row": "activation",
      "result": "held",
      "evidence": "Hosted base 37618361186: background_wait_activation_gates_goal_but_admits_user_input, background_wait_inactive_on_unavailable_host_auto_continues and receipt-to-mailbox-to-fragment suite. m7 37618540192 and m8 37618565570 fail named integration tests. Static: goal extension on_thread_start activates from marker; goal_admission.rs:54 bypasses non-Automatic/non-goal starts. Bounds: user admission is driven; follow-up admission is supported by unchanged shared fast path, not a new separately measured test.",
      "reported_by": "TASK-261007-2468l9"
    }
  ],
  "free_hunt": [
    "[TASK-261007-j2lf0k] {\"id\": \"FH1\", \"area\": \"to-completion path drops completion_mode (handler computes NotifyOnExit but Some(timeout) branch calls exec_command_to_completion which hardcodes Default)\", \"result\": \"not a bug: unreachable with notify_on_exit=true because OneShot lifetime is refused pre-execution before that branch (exec_command.rs:262 vs :338-340). Layered defense holds.\"}",
    "[TASK-261007-j2lf0k] {\"id\": \"FH2\", \"area\": \"release racing the single post-enqueue recheck (release lands after recheck passes, before maybe_start_turn_for_pending_work)\", \"result\": \"benign residual shared with the pre-existing wake race; at most a spurious idle turn, no ghost wake or leaked retention. Recorded as a note, not a finding.\"}",
    "[TASK-261007-j2lf0k] {\"id\": \"FH3\", \"area\": \"capacity accounting with retire_least_recently_sampled (used = active + sampled; retire path could admit a 65th reservation)\", \"result\": \"correct: retirement frees a real sampled slot, so admission after retire is capacity-consistent; with 64 active + 0 sampled the 65th is refused, as the lib test proves.\"}",
    "[TASK-261007-j2lf0k] {\"id\": \"FH4\", \"area\": \"model-supplied receipt handle parsing (whitespace, non-UUID, foreign UUID)\", \"result\": \"from_model_handle trims and returns None for non-UUID (rejected as unknown); parsed ids are lookup keys only with ownership verified separately. Covered by malformed/unknown/foreign tests.\"}",
    "[TASK-261007-j2lf0k] {\"id\": \"FH5\", \"area\": \"mailbox double-enqueue (watcher + raced arm both calling enqueue_published_completion)\", \"result\": \"structurally impossible: publish/arm-to-Queued succeeds at most once per receipt id (Queued carries the TerminalCompletion through the rendezvous), and the mailbox dedupes by receipt id.\"}"
  ]
}
```

## Recording reviewer attestation — CR revision 1

The recording reviewer read both panel outcomes and this merged verdict. Both panels explicitly accept the exact candidate tree `dbd39ab8c59adabe27ebb25838003680214c8d14`. A personally executed JSON comparison passed: 4/4 ordered surface rows held in each panel and the merge, zero panel findings, all 9 notes preserved and all 5 nonblocking free-hunt investigations preserved. No fresh product review or test was run, per recording-brief-rev1.md. The two retention-order suspicions remain unconfirmed notes. The m1 killer-identity bound remains explicit.

The new task-scoped outcome `TASK-260929-3r7peh_recording-review-rev1.md` contains the recording check evidence and logbook entry. Acceptance is recommended from the complete panel merge, with no added findings. The first accept_cr attempt was refused with `change_request_evidence_missing` because this merged resource predated the run and the run manifest had no digest. This update adds the recording reviewer's own judgement without changing panel results.
