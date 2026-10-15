# Merged review verdict — TASK-260929-3rdnra CR revision 1 (tb-R141 / R132 merge)

Verdict: **accept**

Panel outcomes: `TASK-261015-k2z98t_panel-verdict.md` (accept), `TASK-261015-9ql09b_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [],
  "notes": [
    "[TASK-261015-k2z98t] {'id': 'context-token-manual-review', 'text': 'P0 context-review flag: the new V1 scalar cap is not a tokenizer-specific <=1000-token guarantee. Manual review here checked the ContextualUserFragment implementation and worst-case JSON expansion: (384 status + 64 reference) * 6 bytes plus fixed envelope/suffix remains below 3 KiB and therefore below the 10K-token ceiling for byte-based tokenization. Escaped adversarial content can exceed 1K tokens; the recording reviewer must retain this flag rather than treating a byte test as a 1K-token proof. Candidate context/subagent_notification.rs:13-68 and control_bridge_tests.rs:164-179. No exact tokenizer measurement was run.'}",
    "[TASK-261015-k2z98t] {'id': 'v2-bounds-scope', 'text': \"AC4 wording should not be read as a newly established global cap for successful V2 output. Unchanged session_prefix.rs:20-48 copies Completed(Some(message)); its error path is truncated. Hosted matrix covers correct V2 routing/status, while adversarial JSON bounds tests exercise V1 only. Under AC7's unchanged-V2 requirement this is a pre-existing scope limit, not a reproduced regression of this revision.\"}",
    "[TASK-261015-k2z98t] {'id': 'size-and-staging', 'text': '936 changed lines exceed the 800-line guidance. 674 lines are the two new bridge test files. The smallest plausible preparatory split is the independent 89-line P4a synchronization repair, followed by bridge production plus required tests; the latter still exceeds 800 lines. Do not split runtime mailbox recording from its wake/once-only regressions. The producer explicitly documented this exception; it is nonblocking for this panel.'}",
    "[TASK-261015-k2z98t] {'id': 'evidence-bounds', 'text': 'Hosted evidence is reused, not rerun; numeric mutant exit codes and platform/foreign-exec details are absent. Tests directly install a goal SleepItem for bridge wake cases; unchanged G1 tests cover real registration. The status matrix drives production watcher/router methods but does not exercise an entire shutdown lifecycle. No new guarantee for reused V1 child turns or restart-restored wake authority is established.'}",
    "[TASK-261015-9ql09b] P0 manual context-review flag: the 384-scalar cap permits escape-heavy serialized items above 1,000 tokens; <3 KiB is a byte bound, not a tokenizer bound. The existing SubagentNotification type is reused and tightened, not a new unbounded context type. Recording reviewer should explicitly acknowledge manual context review; no tokenizer execution or measured token count is claimed.",
    "[TASK-261015-9ql09b] Hosted execution is reused exclusively from TASK-260929-3rdnra_hosted-precheck-4.md: tree c57fb1b76d54fff5816a1a264a76d497bb80b50d, snapshot f1dd5d5a4d34, run 38690480458. It supplies success conclusions and named behavioral mutant failures, but no numeric process exits. Those exits remain unknown, not zero or invented 100.",
    "[TASK-261015-9ql09b] Idle-history unit assertion snapshots the newly stamped object and checks persistence; it does not independently assert a specific turn-id spelling or timestamp. Static trace shows the unchanged new_inject_items_context -> new_default_turn_for -> next_internal_sub_id path, matching existing idle injection. Optional future narrowing attack: corrupt only stamp provenance and assert expected metadata independently; not a reproduced defect.",
    "[TASK-261015-9ql09b] Bounds: V1 retains existing first-final-status watcher lifetime; repeated reused-child turns, all scheduler interleavings, Windows/foreign-exec runs, cancellation during idle recording, and tokenizer-specific caps were not proven. Error/closed status matrix drives production watcher/router rather than full V2 shutdown. No unsupported guarantee inferred.",
    "[TASK-261015-9ql09b] No writes, status, acceptance, rejection, or handoff were made on TASK-260929-3rdnra. This is a non-recording panel recommendation, not CR acceptance."
  ],
  "surface_results": [
    {
      "row": "V1 delivery channel",
      "result": "held",
      "evidence": "Hosted precheck 4: v1_direct_inject and v1_duplicate_fragment fail named V1 matrix/idle-history tests. Static trace: control.rs:531 -> CodexThread::queue_runtime_fragment -> InputQueue::enqueue_runtime_fragment. Runtime payload cannot set trigger_turn; active reservation prevents idle history recording. No direct watcher injection remains.",
      "reported_by": "TASK-261015-k2z98t"
    },
    {
      "row": "wake permission",
      "result": "held",
      "evidence": "Hosted native_completion_mailbox_history_and_wake V1/V2 registered and ordinary cases, native_interrupted_wait_wakes_once registered/unregistered cases, and upstream no-wait test pass. v1_ordinary_wake, v1_drop_without_wait, v1_interrupt_without_goal, v2_result_wakes_ordinary are killed. Static scheduler checks existing wake authority; ordinary runtime mail is recorded without scheduling. Request counts are exact server captures filtered by thread.",
      "reported_by": "TASK-261015-k2z98t"
    },
    {
      "row": "identity and paths",
      "result": "held",
      "evidence": "Hosted v1_fabricated_path killed by V1 status cases and v1_registered_wait. Matrix compares the complete expected UUID fragment and asserts no InterAgentCommunication op. Spawn and resume install this watcher only outside V2; V2 terminal routing retains real AgentPath. The legacy JSON key agent_path is retained, but its V1 value is the child thread ID.",
      "reported_by": "TASK-261015-k2z98t"
    },
    {
      "row": "status matrix and bounds",
      "result": "held",
      "evidence": "Hosted eight native_status_mailbox_fragment cases and three native_v1_fragment_bounds_payload cases pass; v1_unbounded_error killed by error_escaped/error_unicode. Candidate chars().take preserves UTF-8, serde emits valid JSON, Completed/Errored classification is retained, Interrupted does not become success. V2 successful-output bound is limited as explicitly noted; no global V2 bound is inferred.",
      "reported_by": "TASK-261015-k2z98t"
    },
    {
      "row": "mid-turn and idle history",
      "result": "held",
      "evidence": "Hosted native_second_child_finishes_mid_turn_once::{v1,v2} and native_runtime_fragment_records_idle_history_once_and_retains_wake pass. v1_drop_midturn, v1_duplicate_fragment, v1_idle_fragment_reappended killed. InputQueue transitions RuntimeFragment to RecordedRuntimeFragment under its lock, retains pending presence for late registration, and drains the recorded marker without a second append. Session holds active_turn across idle recording, excluding concurrent turn admission. Test preserves the exact stamped record on reread.",
      "reported_by": "TASK-261015-k2z98t"
    },
    {
      "row": "transcript change and regressions",
      "result": "held",
      "evidence": "Hosted core/app-server baseline green, including upstream pending_input, no-wait, G1 and scheduled-checkin tests. V1 before/after asserts unchanged history prefix plus exactly one addition, then exactly one final notification. v1_drop_without_wait and v1_idle_fragment_reappended killed. Static P4a diff retains exact deadlines/counts and strengthens lifecycle synchronization; no upstream no-wait or G1 test modification.",
      "reported_by": "TASK-261015-k2z98t"
    }
  ],
  "free_hunt": []
}
```
