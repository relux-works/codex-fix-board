# TASK-261005-23qv3d panel verdict — CR-TASK-260929-4ut0up-1 revision 1

accept

Replay: base `ea8899e6f97aea64136159286840c28c955243e8` plus the exact attached patch produced `7de6b3c2ed82f07002c613263cd650cc16b20108`; expected and actual trees are identical. Snapshot `9e692fdcd16a373a59f7d262159b377d588163d0^{tree}` independently resolves to the same tree. Working-tree HEAD was not used as candidate evidence.

## Plan and evidence boundary

Decision: provide the orchestrator a non-recording panel verdict for B2. Frozen input: CR revision 1, base and candidate trees above; no grammar change. Budget: one inline static sweep plus a bounded free hunt, one text outcome, zero serial prerequisites. Consumer: recording reviewer for this CR. Exit: replay checked, every surface row classified once, notes and execution bounds attached. No source edits, build/test execution, commits, or recording writes on TASK-260929-4ut0up. The panel is a researcher handoff, not acceptance of the source task.

## Commands run by this panel and real exits

Each replay/check command ran directly, without tee or a pipe masking status:

| Command | Exit | Observation |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261005-23qv3d, status=analysis)'` | 0 | Only panel lifecycle changed. |
| `command -v task-board git rg python3`; `git --version`; `rg --version`; `python3 --version` | 0 | Readiness outputs saved under `.temp/TASK-261005-23qv3d/tool-readiness.log`. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-23qv3d-replay-1.idx" git read-tree ea8899e6f97aea64136159286840c28c955243e8` | 0 | Separate index; normal index untouched. |
| `task-board resource get TASK-260929-4ut0up TASK-260929-4ut0up_change-request_rev1.patch --output .temp/TASK-260929-4ut0up_change-request_rev1.patch` | 0 | Read-only source-task resource fetch. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-23qv3d-replay-1.idx" git apply --cached .temp/TASK-260929-4ut0up_change-request_rev1.patch` | 0 | Replay applied. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-23qv3d-replay-1.idx" git write-tree` | 0 | Exact expected candidate tree. |
| `git diff --check ea8899e6f97aea64136159286840c28c955243e8 7de6b3c2ed82f07002c613263cd650cc16b20108` | 0 | No diff whitespace errors. |
| `git rev-parse '9e692fdcd16a373a59f7d262159b377d588163d0^{tree}'` | 0 | Matches replay tree. |
| Candidate export via Python calling `git diff --name-only BASE TREE` and `git show TREE:PATH` | 0 | 12 exact candidate blobs exported into task scratch. |
| Python JSON audit of `b2-precheck-2-results.json` | 0 | Asserted 4 successful snapshot lanes, 16 killed mutants, each with a named failing test. This audits prior evidence; it does not rerun CI. |
| `task-board q 'get(TASK-260929-4ut0up) { description scope ac }'` | 0 | Scoped source-task read only. |
| Candidate/resource reads via `cat`, `sed`, `nl`, `git show`, `git diff --stat` | 0 | Source citations below refer to candidate blobs, not mutable HEAD. |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives recorded. |

Exploratory failures, not passing gates: skill search including absent `agents/skills` and `.claude/skills` exited 2; unsupported `get { resources }` query exited 1; `schema(get)` positional syntax exited 1, corrected `schema(operation="get")` exited 0; a file search with no matching paths exited 1. `task-board resource list` printed help with exit 0 and provided no inventory; resources were discovered by read-only file enumeration instead. The initial `rm -f` index-reset call was rejected before process creation (no exit code); replay used a fresh index filename without deletion. No failing command was credited as validation success.

## Surface sweep and AC evidence

Surface table has exactly one row: **receipt hooks in unified exec**. Result: **held**, bounded to the previously executed attacks. Coverage: 1/1 surface rows, 7/7 AC rows with named tests, 16/16 narrowing mutants killed. No local cargo, just, builds or tests were run. Hosted results were accepted from attached precheck-2 evidence on the exact replay tree, and its referenced JSON was inspected. A killed mutant is an expected failing mutant run, not a green gate; raw hosted command exit codes were not attached and are not invented here.

| AC | Candidate tests in `receipt_hooks_tests.rs` | Attack coverage |
| --- | --- | --- |
| 1 | `receipt_exit_publishes_only_after_drain_denial_and_classification`, `receipt_failed_exit_maps_to_failed_completion`, `receipt_exit_preserves_timed_out` | Drain/monitor held; failed exit; timed_out. Three killed narrowing mutants. |
| 2 | `opted_in_exit_before_decision_returns_inline_and_frees_slot`, `opted_in_decision_before_exit_queues_exactly_one_completion` | Real opted-in launch, inline slot freeing and later exactly-once claim. Timing coverage bound noted in JSON. |
| 3 | `retained_output_survives_process_entry_removal`, `retained_output_over_cap_keeps_head_tail_and_omitted_count`, `retained_output_read_refuses_unknown_and_foreign_receipts` | Removal before read; 3 MiB transcript/head+tail cap; ownership refusal. Cap and omitted-count mutants killed. |
| 4 | `receipt_capacity_refuses_65th_unsampled_reservation`, `opted_in_exec_refuses_65th_before_spawning`, `new_reservation_retires_least_recently_sampled_output`, `release_frees_active_and_sampled_slots` | 64/65 refusal before real spawn; mixed-state capacity/LRU retirement. Active-only and reverse-LRU mutants killed. |
| 5 | `terminal_stdin_claim_consumes_the_single_claim_first`, `terminal_stdin_and_pushed_claims_race_exactly_once` | Real write_stdin against already-Queued receipt; shared lease/acknowledge. Missing-ack mutant killed. Before-publication order is a note below. |
| 6 | `release_cancels_receipt_and_keeps_process_running`, `terminate_process_cancels_before_killing`, `interrupt_cancels_before_signalling`, `shutdown_cancels_all_receipts_and_frees_slots` | Release/terminate/non-TTY interrupt/shutdown APIs with driver/backend latches. Five cancellation/retention mutants killed. |
| 7 | `default_launches_reserve_no_receipts` plus existing hosted suites | More than 64 default launches and live default launch. Forced-opt-in mutant killed; tool schemas/default launch selection unchanged. |

## Free hunt and logbook entry

2026-10-05 — Static review of watcher publication, stdin lock ordering, release/sampling capacity transfer and long-lived retired metadata. No additional executed reproduction and no blocking free-hunt finding. Observations are preserved as notes, with requested production-path tests. External integration surfaces, dependencies, configuration, rollouts and model context are unchanged by this CR; no new model-visible context fragment. The base-to-candidate diff contains checkpointed B1 as well as B2 (4,592 insertions); do not label all of it new B2 logic. New B2 modules `receipt_hooks.rs` and `receipt_output.rs` are 373 and 196 lines; implementation/tests remain in unified_exec. Size is a reviewability note, not a runtime reproduction.

FINDING: Exact replay and hosted snapshot trees match. DECISION: retain unexecuted static interleavings as notes under reviewer rule “A suspicion with no failing reproduction is a note”; request tests in the same leaf rather than a new research chain. SCOPE: only TASK-261005-23qv3d receives outcome/lifecycle writes; no direct control-root logbook edit.

## Artifact verification

Panel JSON/row/verdict validation via standalone Python exited 0; `git status --short` exited 0 with empty output. Candidate lock/test citation check via `rg -n` exited 0. No tracked or untracked repository changes. Artifact packaging and the same JSON validation are performed before attachment.

## Sources

- Source-task resources: `surface-table.md`, `producer-brief.md`, `b2-brief.md`, `final-plan.md` §5, `TASK-260929-4ut0up_results.md`, `TASK-260929-4ut0up_hosted-precheck-2.md`, `TASK-260929-4ut0up_change-request_rev1.patch`.
- Hosted snapshot run cited by attached evidence: https://github.com/relux-works/codex/actions/runs/37219783600; 16 mutant run IDs in precheck-2. This panel did not independently query GitHub.
- Referenced machine evidence read locally: `/Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/p5/b2-precheck-2-results.json`.
- All code citations use candidate tree `7de6b3c2ed82f07002c613263cd650cc16b20108`; candidate exports under `.temp/TASK-261005-23qv3d/candidate/`.
- Reviewer round contract: `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md`; research plan contract: `references/research-workflow.md`. Panel-specific no-build and non-recording instructions override recording-review lifecycle.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "stdin-before-exit-publication",
      "row": "receipt hooks in unified exec",
      "severity": "note",
      "repeat-of": "none",
      "invariant": "AC5: terminal stdin and pushed completion share one claim.",
      "mechanism": "codex-rs/core/src/unified_exec/process_manager.rs:1043 acquires the interaction lock throughout write_stdin; async_watcher.rs:191 needs the same lock before publishing. If a live-process poll starts before exit and observes exit while holding that lock, receipt_hooks.rs:332-337 cannot lease an Armed receipt; process_manager.rs:1228-1229 then unbinds and returns terminal output. Once the lock drops the watcher can queue a pushed claim. The existing claim tests wait for Queued before starting stdin (receipt_hooks_tests.rs:1236 and 1296), excluding this order.",
      "requested_attack": {
        "test_file": "codex-rs/core/src/unified_exec/receipt_hooks_tests.rs",
        "test_name": "terminal_stdin_started_before_exit_consumes_single_claim",
        "command": "cd codex-rs && just test -p codex-core terminal_stdin_started_before_exit_consumes_single_claim",
        "expected_failure": "Force write_stdin to hold interaction_lock before backend exit; after terminal stdin returns and watcher settles, assert a pushed lease is AlreadyConsumed. Static prediction: it instead succeeds from Queued. Add this test and a narrowing mutant in the same implementation leaf."
      },
      "execution": "Not executed or added: no builds/tests permitted. Source interleaving only; not counted as a reproduced blocking finding."
    },
    {
      "id": "publication-retention-split",
      "row": "receipt hooks in unified exec",
      "severity": "note",
      "repeat-of": "none",
      "invariant": "AC3/4/6: output retention, combined capacity and release agree with receipt lifecycle.",
      "mechanism": "codex-rs/core/src/unified_exec/async_watcher.rs:209-226 publishes first, then awaits output_buffer and hooks before insert_pending. Release, shutdown and acknowledge use hooks to mutate lifecycle+retention. An acknowledgement can retire the active receipt and move_to_sampled before output exists (receipt_hooks.rs:313-318), then watcher inserts pending output into an already Sampled receipt. Capacity counts active_len+sampled_count (receipt_hooks.rs:152), omitting it. Release/shutdown can similarly clear state between publication and insertion, allowing output to reappear after cancellation. These are one synchronization mechanism, not separate findings.",
      "requested_attack": {
        "test_file": "codex-rs/core/src/unified_exec/receipt_hooks_tests.rs",
        "test_name": "watcher_publication_and_retention_are_atomic_with_sampling_and_release",
        "command": "cd codex-rs && just test -p codex-core watcher_publication_and_retention_are_atomic_with_sampling_and_release",
        "expected_failure": "Hold output_buffer across watcher publication, observe Queued, then acknowledge a pushed lease or release/shutdown before unlocking output_buffer. After watcher insertion, assert Sampled output still holds one capacity slot, or cancelled/released output is absent. Static prediction: sampled output holds zero counted slots, or released output becomes readable. Drive spawn_exit_watcher and real manager APIs; do not test a substitute state machine."
      },
      "execution": "Not executed or added; source interleaving only, not a reproduced blocking finding."
    },
    {
      "id": "retired-metadata-growth",
      "row": "receipt hooks in unified exec",
      "severity": "note",
      "repeat-of": "none",
      "invariant": "Bounded runtime metadata under long-running receipt turnover (free hunt).",
      "mechanism": "codex-rs/core/src/unified_exec/receipt_output.rs:129 retains an owner marker for every retired receipt without a cap. receipt_hooks.rs:161 also preserves old bindings until release/shutdown. Repeated sampling and LRU retirement can accumulate metadata beyond the 64 output slots; CompletionReceiptStore terminal history is separately bounded. AC explicitly bounds output bytes and slots, but does not define retired-marker expiry, so this is also a contract-boundary note.",
      "requested_attack": {
        "test_file": "codex-rs/core/src/unified_exec/receipt_hooks_tests.rs",
        "test_name": "retired_receipt_metadata_is_bounded_across_turnover",
        "command": "cd codex-rs && just test -p codex-core retired_receipt_metadata_is_bounded_across_turnover",
        "expected_failure": "Specify an expiry bound first, then reserve/finish/sample/retire many more than 64 receipts without explicit release and assert retired markers and detached bindings stay within that bound."
      },
      "execution": "Not executed; no metadata cap asserted by the current AC. Nonblocking note."
    },
    {
      "id": "race-coverage-bound",
      "severity": "note",
      "repeat-of": "none",
      "mechanism": "The two initial-response tests use echo with 30s yield and sleep 2 with 250ms yield (receipt_hooks_tests.rs:763-844), rather than barrier-forcing both boundary orders requested in AC2. Hosted execution proves these two orders in those scenarios, not exhaustive boundary-race coverage. Several watcher/capacity tests directly install driver processes or reserve receipts; do not repeat the producer claim that every AC test launches through exec_command."
    }
  ],
  "surface_results": [
    {
      "row": "receipt hooks in unified exec",
      "result": "held",
      "evidence": "TASK-260929-4ut0up_hosted-precheck-2.md: exact tree 7de6b3c2ed82f07002c613263cd650cc16b20108, snapshot run 37219783600, 4/4 lanes success. Referenced b2-precheck-2-results.json inspected: 16/16 mutants killed with named failures. All listed attack families have named tests; see AC coverage below. Held is bounded to executed attacks; newly proposed interleavings are notes, not reproduced failures.",
      "coverage": "1/1 surface rows; 7/7 AC rows have named tests; 16/16 narrowing mutants killed."
    }
  ],
  "free_hunt": []
}
```
