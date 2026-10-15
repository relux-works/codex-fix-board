# R141 panel A — V1 subagent notification bridge, revision 1

accept

Non-recording panel for CR-TASK-260929-3rdnra-1. No mutation, review disposition, status, note, or handoff was written to TASK-260929-3rdnra. This recommendation is for the recording reviewer, not CR acceptance or landing.

## Replay and evidence identity

Base: `8a9cf9c2af0e815cb25893a1fbb21524dc0f3147`.
Expected and replayed candidate tree: `c57fb1b76d54fff5816a1a264a76d497bb80b50d`.
Independent `git rev-parse f1dd5d5a4d34^{tree}` returned that same tree. The attached hosted precheck 4 names this snapshot and relux-ci run [38690480458](https://github.com/ivanopcode/codex/actions/runs/38690480458). This panel reuses its reported successful lint/small/core/app-server lanes and 10/10 named behavioral mutant kills. It did not rerun those lanes or retrieve raw hosted logs. Numeric hosted process exit codes are not supplied and remain unknown; job success and expected-red mutant failures are not relabeled as locally executed gates.

## Commands and real exits

Commands ran in the assigned Story worktree. `IDX` below abbreviates `$PWD/.temp/TASK-261015-k2z98t-replay.idx`.

| Command | Exit | Observed result |
|---|---:|---|
| `task-board m 'set_status(TASK-261015-k2z98t, status=analysis)'` | 0 | Own task started |
| `git --version`; `task-board --version` | 0 | Readiness output persisted in task scratch |
| `GIT_INDEX_FILE="$IDX" git read-tree 8a9cf9c2af0e815cb25893a1fbb21524dc0f3147` | 0 | Temporary index initialized |
| `task-board resource get TASK-260929-3rdnra TASK-260929-3rdnra_change-request_rev1.patch --output .temp/TASK-260929-3rdnra_change-request_rev1.patch` | 0 | Patch materialized |
| `GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-260929-3rdnra_change-request_rev1.patch` | 0 | Exact base replay succeeded |
| `GIT_INDEX_FILE="$IDX" git write-tree` | 0 | Exact candidate tree above |
| `git rev-parse f1dd5d5a4d34^{tree}` | 0 | Exact hosted snapshot tree confirmed |
| `git diff --check 8a9cf9c2af0e815cb25893a1fbb21524dc0f3147 c57fb1b76d54fff5816a1a264a76d497bb80b50d` | 0 | No whitespace errors |
| `git diff --stat 8a9cf9c2af0e815cb25893a1fbb21524dc0f3147 c57fb1b76d54fff5816a1a264a76d497bb80b50d` | 0 | 12 files; 866 insertions, 70 deletions |
| `git diff --name-only 8a9cf9c c57fb1b -- codex-rs/core/tests/suite/goal_native_wait.rs codex-rs/core/src/session/inject.rs codex-rs/core/src/session/turn_context.rs` | 0 | These dependencies unchanged |
| `git status --short`; `git rev-list --count HEAD..main` | 0 | Clean tracked checkout; count 0. Evidence is pinned to candidate, not worktree HEAD |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives; run not goal-bound |
| `python3 --version` | 0 | Artifact-checker runtime readiness |

No cargo, just, build, product test, formatter, or local mutant execution was run. Source inspection used candidate `git show` and base-to-candidate `git diff` (exit 0). Unchanged supporting recording-context code was also read from the checkout after checking its candidate delta was empty.

Exploratory failures, not passing validation: `get(...){... resources ...}` exited 1 (unknown projection); `schema(type=task)` exited 1 (unsupported schema scope). Recovery used the scoped `schema(operation=get)` (0), supported projections (0), and read-only resource paths. A combined skill read exited 1 because the `.claude` reviewer-role file was absent; the current `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md` was then read successfully. `task-board resource list` returned help with exit 0 and was not treated as a resource listing. Searches mentioning absent skill directories and the obsolete `core/src/codex.rs` path emitted errors; their enclosing pipelines/command groups returned 0, which is not evidence those paths were searched. Subsequent reads used resolved existing paths.

## Review scope and sources

Decision: recommend acceptance or rework of this exact revision. Frozen precondition: the base, patch and candidate tree above; no new grammar. Budget: one bounded panel pass, at most 45 minutes and one text outcome, no serial research prerequisite. Exit: all six surface rows and bounded free hunt assessed. Consumer: the orchestrator's merged panel verdict and recording reviewer, not a new implementation leaf.

Source resources, read-only under `.task-board/.resources/TASK-260929-3rdnra/`: `surface-table.md`, `producer-brief.md`, `TASK-260929-3rdnra_hosted-precheck-4.md`, `TASK-260929-3rdnra_handoff-precheck4.md`, `TASK-260929-3rdnra_results.md`, `g2-handoff-note-4.md`; AC1–AC7 read through `get(TASK-260929-3rdnra) { description scope ac notes }` (0). The truncated historical local validation log is not used to certify a passing command; hosted evidence is the authorized substitute in this panel brief.

The exact diff retains the upstream no-wait integration test and G1 native-wait file. The P4a change waits for actual deadline registration and sink notification; exact 30/60/120-minute deadlines, three check-ins, one warning, and no fourth armed deadline remain asserted. This is synchronization repair, not relaxed request counts. New HTTP assertions count server captures filtered by thread, avoiding the documented matcher capture-order trap.

Coverage: 6/6 surface rows attacked by the supplied exact-tree hosted executions and checked statically here; 7/7 AC rows have named coverage. Held means the cited attacks did not reproduce on the candidate, not proof against every schedule or input.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "context-token-manual-review",
      "text": "P0 context-review flag: the new V1 scalar cap is not a tokenizer-specific <=1000-token guarantee. Manual review here checked the ContextualUserFragment implementation and worst-case JSON expansion: (384 status + 64 reference) * 6 bytes plus fixed envelope/suffix remains below 3 KiB and therefore below the 10K-token ceiling for byte-based tokenization. Escaped adversarial content can exceed 1K tokens; the recording reviewer must retain this flag rather than treating a byte test as a 1K-token proof. Candidate context/subagent_notification.rs:13-68 and control_bridge_tests.rs:164-179. No exact tokenizer measurement was run."
    },
    {
      "id": "v2-bounds-scope",
      "text": "AC4 wording should not be read as a newly established global cap for successful V2 output. Unchanged session_prefix.rs:20-48 copies Completed(Some(message)); its error path is truncated. Hosted matrix covers correct V2 routing/status, while adversarial JSON bounds tests exercise V1 only. Under AC7's unchanged-V2 requirement this is a pre-existing scope limit, not a reproduced regression of this revision."
    },
    {
      "id": "size-and-staging",
      "text": "936 changed lines exceed the 800-line guidance. 674 lines are the two new bridge test files. The smallest plausible preparatory split is the independent 89-line P4a synchronization repair, followed by bridge production plus required tests; the latter still exceeds 800 lines. Do not split runtime mailbox recording from its wake/once-only regressions. The producer explicitly documented this exception; it is nonblocking for this panel."
    },
    {
      "id": "evidence-bounds",
      "text": "Hosted evidence is reused, not rerun; numeric mutant exit codes and platform/foreign-exec details are absent. Tests directly install a goal SleepItem for bridge wake cases; unchanged G1 tests cover real registration. The status matrix drives production watcher/router methods but does not exercise an entire shutdown lifecycle. No new guarantee for reused V1 child turns or restart-restored wake authority is established."
    }
  ],
  "surface_results": [
    {
      "row": "V1 delivery channel",
      "result": "held",
      "evidence": "Hosted precheck 4: v1_direct_inject and v1_duplicate_fragment fail named V1 matrix/idle-history tests. Static trace: control.rs:531 -> CodexThread::queue_runtime_fragment -> InputQueue::enqueue_runtime_fragment. Runtime payload cannot set trigger_turn; active reservation prevents idle history recording. No direct watcher injection remains."
    },
    {
      "row": "wake permission",
      "result": "held",
      "evidence": "Hosted native_completion_mailbox_history_and_wake V1/V2 registered and ordinary cases, native_interrupted_wait_wakes_once registered/unregistered cases, and upstream no-wait test pass. v1_ordinary_wake, v1_drop_without_wait, v1_interrupt_without_goal, v2_result_wakes_ordinary are killed. Static scheduler checks existing wake authority; ordinary runtime mail is recorded without scheduling. Request counts are exact server captures filtered by thread."
    },
    {
      "row": "identity and paths",
      "result": "held",
      "evidence": "Hosted v1_fabricated_path killed by V1 status cases and v1_registered_wait. Matrix compares the complete expected UUID fragment and asserts no InterAgentCommunication op. Spawn and resume install this watcher only outside V2; V2 terminal routing retains real AgentPath. The legacy JSON key agent_path is retained, but its V1 value is the child thread ID."
    },
    {
      "row": "status matrix and bounds",
      "result": "held",
      "evidence": "Hosted eight native_status_mailbox_fragment cases and three native_v1_fragment_bounds_payload cases pass; v1_unbounded_error killed by error_escaped/error_unicode. Candidate chars().take preserves UTF-8, serde emits valid JSON, Completed/Errored classification is retained, Interrupted does not become success. V2 successful-output bound is limited as explicitly noted; no global V2 bound is inferred."
    },
    {
      "row": "mid-turn and idle history",
      "result": "held",
      "evidence": "Hosted native_second_child_finishes_mid_turn_once::{v1,v2} and native_runtime_fragment_records_idle_history_once_and_retains_wake pass. v1_drop_midturn, v1_duplicate_fragment, v1_idle_fragment_reappended killed. InputQueue transitions RuntimeFragment to RecordedRuntimeFragment under its lock, retains pending presence for late registration, and drains the recorded marker without a second append. Session holds active_turn across idle recording, excluding concurrent turn admission. Test preserves the exact stamped record on reread."
    },
    {
      "row": "transcript change and regressions",
      "result": "held",
      "evidence": "Hosted core/app-server baseline green, including upstream pending_input, no-wait, G1 and scheduled-checkin tests. V1 before/after asserts unchanged history prefix plus exactly one addition, then exactly one final notification. v1_drop_without_wait and v1_idle_fragment_reappended killed. Static P4a diff retains exact deadlines/counts and strengthens lifecycle synchronization; no upstream no-wait or G1 test modification."
    }
  ],
  "free_hunt": []
}
```

## Bounded free hunt and outcome logbook

After the six-row sweep, inspected spawn/resume watcher registration for a second V2 Interrupted route, idle-recording lock order and fresh context provenance, retained marker retirement, and public-surface changes. Both spawn and resume gate the watcher with `multi_agent_version != V2`; no double V2 interruption route was found. The recording context uses the unchanged `new_default_turn_for(InjectItems)` and fresh `next_internal_sub_id`, not a reused previous turn. Live mailbox markers are not serialized into a new API/config schema; no CLI/dependency/schema change appears in the diff. Cancellation between claiming and recording a fragment was considered but not executed and is not asserted safe for all schedules. No additional reproduced finding was established; no new local runtime attack is claimed.

This outcome is the task-scoped logbook: exact replay and hosted identity match; oversized change exception and token/bounds limits recorded; unsupported exploratory reads corrected without treating failed reads as absence. Product files, real Git index, branch and reviewed task were not modified. Scratch lives inside the assigned worktree to obey the later explicit run-write boundary; the persistent copy is attached through resource CRUD only. Panel recommendation is ready for review.

Artifact validation: `python3` JSON/shape checker exited 0; exactly one verdict block and six unique ordered rows. Its in-memory duplicate-block negative control was rejected by the intended assertion. No product tests were run.
