# R141 panel B — V1 subagent notification bridge, revision 1

accept

Replay: `8a9cf9c2af0e815cb25893a1fbb21524dc0f3147` plus the attached CR patch produced exactly `c57fb1b76d54fff5816a1a264a76d497bb80b50d`. The real Git index and candidate files were not changed. No local build, Rust test, formatter, or mutant was run.

## Review plan and result

Decision: recommend acceptance or rework of CR-TASK-260929-3rdnra-1 to the recording reviewer. Frozen precondition: supplied base, patch, candidate tree and six-row surface table; grammar freeze is inapplicable. Budget: one bounded static panel pass (30 minutes maximum, including packaging), free hunt up to 5 minutes, one text outcome below 20 KiB, no serial prerequisite. Exit: exact replay plus all six surfaces classified and one verdict. Consumer: recording reviewer for this bridge implementation, not a new research leaf.

Coverage: 6/6 surface rows attacked using supplied exact-tree hosted public-entry evidence and independently inspected candidate code/assertions; 6 held, 0 broken, 0 not-attacked. Seven AC rows map to those surfaces. Ten hosted narrowing mutants were reported killed, zero survivors. These are reused execution results, not locally rerun results. Held means the named attacks did not reproduce a defect, not exhaustive correctness.

Bounded free hunt inspected spawn/resume watcher selection, active-turn/queue lock ordering, late-wait retained mailbox presence, unchanged idle stamp provenance, scalar/JSON limits and P4a timing-test changes. No additional reproduced blocking mechanism; remaining proof limits appear in notes.

## Commands and real exits

All replay gates were separate standalone processes (no pipelines):

| Command | Exit / result |
|---|---|
| `task-board m 'set_status(TASK-261015-9ql09b, status=analysis)'` | 0 |
| `git --version`; `task-board --version` | readiness output persisted in `.temp/TASK-261015-9ql09b/readiness.log`; successful setup shell 0 |
| `task-board resource get TASK-260929-3rdnra TASK-260929-3rdnra_change-request_rev1.patch --output .temp/TASK-261015-9ql09b/change.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261015-9ql09b/replay.idx" git read-tree 8a9cf9c2af0e815cb25893a1fbb21524dc0f3147` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261015-9ql09b/replay.idx" git apply --cached .temp/TASK-261015-9ql09b/change.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261015-9ql09b/replay.idx" git write-tree` | 0; exact expected tree above |
| `git diff --check 8a9cf9c2af0e815cb25893a1fbb21524dc0f3147 c57fb1b76d54fff5816a1a264a76d497bb80b50d` | 0 |
| `git diff --quiet BASE TREE -- codex-rs/core/src/session/inject.rs codex-rs/core/src/session/turn_context.rs codex-rs/core/src/agent/control/spawn.rs codex-rs/core/tests/suite/goal_native_wait.rs` (BASE/TREE as above) | 0; unchanged source provenance and G1 tests |
| Candidate `git show TREE:<path>` and `git diff BASE TREE` inspections | 0; 12 paths, 866 additions / 70 deletions |
| Hosted relux-ci lint/small/core/app-server, run 38690480458 | success per supplied resource; numeric process exits not supplied |
| Hosted ten mutant executions | expected-red behavioral failures per supplied resource; numeric exits not supplied; never represented as passing processes |
| Local builds/tests/mutants | NOT RUN, per panel constraint |

Exploratory read failures: initial `get(...){... resources ...}` query exited 1 (unknown field); corrected projection used description/scope/ac/notes. Installed reviewer-role file read exited 1 (missing file); read authoritative source role file successfully instead. `resource list` is unsupported and only printed help; resource paths were enumerated read-only with rg. One rg invocation included absent `session/history.rs` and reported an error; no absence conclusion was drawn. A broad read-only role-path search ended 0. These are discovery failures, not passed validation. No remote CI log was fetched independently; the prompt explicitly authorizes the attached precheck as execution evidence.

Artifact structural validation: Python JSON parse, exactly one fenced verdict block, exact six-row order/uniqueness, accepted verdict consistency, and <20 KiB ceiling all passed (exit 0). This checks document structure only, not product behavior.

## Sources and outcome-scoped logbook

- Board resource `TASK-260929-3rdnra/surface-table.md`: six invariants and attack families.
- Board task AC projection: AC1 queue-only delivery; AC2 wake permission; AC3 identity; AC4 status/bounds; AC5 mid-turn; AC6 transcript; AC7 V2 regression.
- Board resources `TASK-260929-3rdnra_hosted-precheck-4.md`, `TASK-260929-3rdnra_mutants.json`, `TASK-260929-3rdnra_handoff-precheck4.md`, `TASK-260929-3rdnra_results.md`: execution provenance, mutant definitions, prior failures, candidate scope and declared limits. [Hosted run](https://github.com/ivanopcode/codex/actions/runs/38690480458).
- Candidate blobs: `codex-rs/core/src/{agent/control.rs,agent/control/completion.rs,agent/control_bridge_tests.rs,codex_thread.rs,context/subagent_notification.rs,session/input_queue.rs,tasks/mailbox.rs,tasks/mod.rs}` and `codex-rs/core/tests/suite/{pending_input_subagent_bridge.rs,goal_background_wait.rs}`. All inspected against the exact tree with git show/diff, not assumed from current checkout.
- 2026-10-15 panel log: exact replay succeeded; supplied hosted evidence reused with numeric-exit uncertainty retained; six surfaces swept; static free hunt found no new blocker. P0 context-size/manual-review flag and stamp-test limitation are preserved explicitly. Artifact is task-scoped scratch plus board outcome; no tracked source or control-root logbook edit. All mutation targets are this panel task only.

```verdict-findings
{
  "findings": [],
  "notes": [
    "P0 manual context-review flag: the 384-scalar cap permits escape-heavy serialized items above 1,000 tokens; <3 KiB is a byte bound, not a tokenizer bound. The existing SubagentNotification type is reused and tightened, not a new unbounded context type. Recording reviewer should explicitly acknowledge manual context review; no tokenizer execution or measured token count is claimed.",
    "Hosted execution is reused exclusively from TASK-260929-3rdnra_hosted-precheck-4.md: tree c57fb1b76d54fff5816a1a264a76d497bb80b50d, snapshot f1dd5d5a4d34, run 38690480458. It supplies success conclusions and named behavioral mutant failures, but no numeric process exits. Those exits remain unknown, not zero or invented 100.",
    "Idle-history unit assertion snapshots the newly stamped object and checks persistence; it does not independently assert a specific turn-id spelling or timestamp. Static trace shows the unchanged new_inject_items_context -> new_default_turn_for -> next_internal_sub_id path, matching existing idle injection. Optional future narrowing attack: corrupt only stamp provenance and assert expected metadata independently; not a reproduced defect.",
    "Bounds: V1 retains existing first-final-status watcher lifetime; repeated reused-child turns, all scheduler interleavings, Windows/foreign-exec runs, cancellation during idle recording, and tokenizer-specific caps were not proven. Error/closed status matrix drives production watcher/router rather than full V2 shutdown. No unsupported guarantee inferred.",
    "No writes, status, acceptance, rejection, or handoff were made on TASK-260929-3rdnra. This is a non-recording panel recommendation, not CR acceptance."
  ],
  "surface_results": [
    {
      "row": "V1 delivery channel",
      "result": "held",
      "evidence": "control.rs:441-533 calls queue_runtime_fragment; codex_thread.rs:1227 enqueues before scheduling, and RuntimeFragment never triggers a turn. Hosted native_status_mailbox_fragment::v1_completed plus v1_direct_inject and v1_duplicate_fragment kills attack direct injection and duplication. Idle persistence is scheduler-owned, not a watcher bypass."
    },
    {
      "row": "wake permission",
      "result": "held",
      "evidence": "tasks/mod.rs:556-566 requires trigger mail or durable sleep. input_queue.rs:199 excludes runtime payloads from triggers; completion.rs:151 checks goal ownership for Interrupted. Hosted native_completion_mailbox_history_and_wake both versions and native_interrupted_wait_wakes_once registered/unregistered assert exact per-thread server request counts. v1_ordinary_wake, v1_drop_without_wait, v1_interrupt_without_goal and v2_result_wakes_ordinary were killed. Goal registration is supplied by G1; unchanged G1 tests are included in hosted core."
    },
    {
      "row": "identity and paths",
      "result": "held",
      "evidence": "Fresh/resumed production spawn call sites exclude V2 watchers; V1 passes existing child identity, with no new AgentPath construction or InterAgentCommunication. Hosted V1 status matrix and v1_registered_wait reject fabricated /root paths; v1_fabricated_path killed. V2 router/path formatting unchanged."
    },
    {
      "row": "status matrix and bounds",
      "result": "held",
      "evidence": "Hosted eight native_status_mailbox_fragment cases drive watcher/router, covering completed/error/shutdown/interrupted for both versions. V1 caps reference at 64 scalars and status text at 384, preserves variant, truncates at scalar boundaries, and serializes with serde_json. Hosted escaped/Unicode bound cases pass and v1_unbounded_error is killed. V2 output formatting remains unchanged; no new universal V2 output-size guarantee is claimed."
    },
    {
      "row": "mid-turn and idle history",
      "result": "held",
      "evidence": "Hosted native_second_child_finishes_mid_turn_once::{v1,v2} drives real spawn, sleeping children, parent wake and second arrival, asserting exactly one occurrence per result. v1_drop_midturn and v1_duplicate_fragment killed. Idle recording holds active_turn across claim and recording; RecordedRuntimeFragment retains wake presence but drains to no item. Hosted idle-history regression and v1_idle_fragment_reappended kill establish record-once behavior. Stamp semantic correctness is statically traced to unchanged recording context, with the assertion limitation noted below."
    },
    {
      "row": "transcript change and regressions",
      "result": "held",
      "evidence": "Hosted v1_without_wait checks unchanged history prefix and exactly one added notice before explicit input, then one notification in subsequent history/request. Upstream no-wait and G1 files remain unchanged; hosted core includes them. P4a rework awaits real deadline registration and sink notification, retaining exact 30/60/120-minute deadlines, three continuations/requests, one warning and no further deadline. No weakened count or removal of production callback found. v1_drop_without_wait and v1_idle_fragment_reappended are killed."
    }
  ],
  "free_hunt": []
}
```
