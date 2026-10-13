# R141 panel A — native subagent wait, revision 1

changes_requested

Replay matches: base `39c264c34e61b5171ae13b0f756746c24ea5f51a` plus the CR patch produced exactly `e8eef4f44743b4a6d256e610f91527e715ae042b` via an isolated temporary index. No worktree source file was used as candidate evidence and no normal index was changed.

One blocking static contract violation: the newly injected Interrupted fragment bypasses the required core/context struct and ContextualUserFragment implementation. Runtime delivery of real Interrupted notices remains unproven; it is not reported as an executed failure. Sweep: **7/7 rows**, **6 held / 1 broken / 0 omitted**. A held row means only the attacks named below held. Six supplied narrowing mutants were reported killed on the exact candidate; that is **6/6 supplied mutants**, not exhaustive AC coverage.

Review was read-only against CR-TASK-260929-csyzcj-1. Only this panel task receives the outcome/checklist/handoff. No source-task recording was performed.

## Execution record

Every replay command ran as a standalone process; no validation command was piped through tee. Literal shell paths use the Story worktree root.

| Command actually run | Exit | Observation |
|---|---:|---|
| `task-board m 'set_status(TASK-261009-195ug2, status=analysis)'` | 0 | Panel lifecycle only |
| `mkdir -p .temp` | 0 | Scratch directory |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261009-195ug2-replay.idx" git read-tree 39c264c34e61b5171ae13b0f756746c24ea5f51a` | 0 | Base loaded into isolated index |
| `task-board resource get TASK-260929-csyzcj TASK-260929-csyzcj_change-request_rev1.patch --output .temp/TASK-260929-csyzcj_change-request_rev1.patch` | 0 | Authoritative patch retrieved |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261009-195ug2-replay.idx" git apply --cached .temp/TASK-260929-csyzcj_change-request_rev1.patch` | 0 | Patch replayed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261009-195ug2-replay.idx" git write-tree` | 0 | Exactly e8eef4f44743b4a6d256e610f91527e715ae042b |
| `git diff --stat 39c264c34e61b5171ae13b0f756746c24ea5f51a e8eef4f44743b4a6d256e610f91527e715ae042b` and `git diff --numstat` for the same OIDs | 0 each | 26 paths; 1,665 additions / 16 deletions |
| `git archive --format=tar --output=.temp/TASK-261009-195ug2-candidate.tar e8eef4f44743b4a6d256e610f91527e715ae042b codex-rs/core/src codex-rs/core/tests/suite/goal_native_wait.rs codex-rs/ext/goal codex-rs/ext/extension-api codex-rs/ext/items codex-rs/core/BUILD.bazel codex-rs/ext/goal/BUILD.bazel MODULE.bazel.lock` | 0 | Exact blobs staged locally; archive NOT attached |
| `mkdir -p .temp/TASK-261009-195ug2-cand` then `tar -xf .temp/TASK-261009-195ug2-candidate.tar -C .temp/TASK-261009-195ug2-cand` | 0 each | Candidate source inspection only |
| `git grep -n -E 'interrupt_agent\|abort_all_tasks\|TurnAbortReason\|INTERRUPTED' e8eef4f44743b4a6d256e610f91527e715ae042b -- codex-rs/core/tests/suite/goal_native_wait.rs` | 1 | No hits: expected-red coverage search; no real interruption driven in this fixture |
| `git grep -n -F 'Agent interrupted. Its turn ended without a final answer' e8eef4f44743b4a6d256e610f91527e715ae042b -- codex-rs/core/src/context` | 1 | No hits: source-contract reproduction; new notice defined outside required module |
| `git grep -n -F 'format_inter_agent_interrupted_message' e8eef4f44743b4a6d256e610f91527e715ae042b -- codex-rs/core/src/context` | 1 | No hits: no contextual type delegation |
| Inline `python3` source inspection of the extracted formatter and core/context files | 0 | JSON output: raw_format_macro=true, contextual_fragment_delegation=false, context_definition_hits=[] |
| `git grep -n -E 'has_goal_wait_sleep\|try_register_goal_wait_sleep\|goal_wait_sleep_id\|goal-wait:' e8eef4f44743b4a6d256e610f91527e715ae042b -- 'codex-rs/**/tests/*.rs' 'codex-rs/**/*_tests.rs'` | 0 | Goal-owned marker test references found only in the two new native_wait fixtures |
| `git grep -n -E 'INTERRUPTED\|Agent interrupted\.' e8eef4f44743b4a6d256e610f91527e715ae042b -- 'codex-rs/**/tests/*.rs' 'codex-rs/**/*_tests.rs'` | 0 | New notice asserted by formatter unit; other hit is unrelated TurnAborted guidance |
| Targeted git grep of goal-wait in baseline subagent_notifications, agent_control_tests, goal_background_wait and goal_extension_backend fixtures | 1 | No matching native-marker coverage; bounded search, not universal absence proof |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives; run not goal-bound |
| `git status --short` before research artifact creation | 0 | Empty; no product edits |

The initial combined replay command containing `rm -f` was rejected by the tool before execution: **no process exit code exists**. Replay was retried with standalone commands and `read-tree` initialization; no removal command ran.

Source reads (`git show`, candidate `sed`/`cat`/`rg`) succeeded except the explicit recoverable discovery errors: missing installed reviewer-role path (`cat`, exit 1), unsupported `resources` projection (`task-board q`, exit 1), unknown `task-board role` (exit 1), and searches referencing missing `.roles`, runtime.rs test file, multi_agents_v2.rs fixture or context.rs path (exit 2). The shipped reviewer contract was subsequently found and read from `/Users/administrator/Developer/ReluxWorks/task-board/skill-project-management/.roles/reviewer/role.md` (exit 0). `task-board resource list` returned help (exit 0); it was not treated as an inventory. Inventory was obtained with preconditionResources/outcomeResources projection (exit 0). All eight requested resource downloads (patch, surface table, producer brief, results, precheck 5, CR validation log, plan, mutants) returned 0. No failed or missing read is reported as green or absence.

Artifact JSON/row validation (`python3`): **exit 0**, exactly one valid verdict-findings object, 7/7 rows exactly once, required finding/reproduction keys and one-word verdict. The source/evidence searches returning 1 above are reported as failing/no-match searches, not passing Rust tests. `git check-ignore` for the initial root research artifact returned 1 (unignored); the artifact was moved under ignored `.temp` so handoff carries board evidence without changing the repository tree.

## Reused execution evidence and sources

- [Surface table](board-resource://TASK-260929-csyzcj/precondition/surface-table.md): seven required rows.
- [Task AC/description](board-element://TASK-260929-csyzcj): read with `task-board q 'get(TASK-260929-csyzcj) { description scope ac notes }'` (exit 0).
- [Hosted precheck 5](board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md): exact candidate tree; snapshot fdaacee7, parent 39c264c3; candidate run [37855177143](https://github.com/relux-works/codex/actions/runs/37855177143), core/app-server/lint/small success. These are reused attached observations, not freshly queried GitHub facts. The summary does not provide individual command exit codes, so those codes are **unknown** here.
- [Mutant definitions](board-resource://TASK-260929-csyzcj/outcome/TASK-260929-csyzcj_mutants.json): six narrowing patches. Precheck 5 reports each mutant killed on all three tries: ignore_native_pending 37855194303; insert_after_mail_check 37855212822; insert_clobbers_one_foreign 37855230691; interrupted_claims_success 37855247950; skip_failed_lookups 37855265071; unconditional_remove 37855282786. Failing lanes are expected-red, not passing commands; per-process exit values are not provided in the summary and remain **unknown**.
- [CR validation log](board-resource://TASK-260929-csyzcj/outcome/TASK-260929-csyzcj_change-request_rev1-validation.log): only mini-hosted-gate.sh is recorded, `[exit 0]`, same candidate tree and hosted run. Measured shard coverage is 1 required / 1 green / 0 failed / 0 missing; test-case coverage explicitly unknown. It is not a local full Rust-suite log.
- [Producer results](board-resource://TASK-260929-csyzcj/outcome/TASK-260929-csyzcj_results.md): coverage map admits real-abort, native live check-in/exhaustion, full resume and second-child-mid-turn gaps. The 9/9 number means rows mapped; producer labels only 5/9 fully driven.
- [Accepted plan sections 6–7](board-resource://TASK-260929-csyzcj/precondition/final-plan.md) and supplied AGENTS.md: lifecycle, queue-only wake, source-bound and model-context requirements. Producer brief and historical notes were context only.

No local build/test or mutant run occurred; therefore no local runtime pass, failure or survivor is claimed. The commands above reproduce static source/evidence observations. Proposed follow-up Rust attacks in the JSON were **not run**.

## Outcome-scoped logbook

2026-10-09, panel A: replay identity holds. The new Interrupted content bypasses the mandated contextual type layer. Formatter mutant kills prove wording, not production routing/once-per-transition eligibility. Record missing native lifecycle fixtures and two lifecycle concurrency hypotheses explicitly rather than upgrading them to tested behavior. Recommendation: repair typed fragment ownership and add the real-interruption regression/narrowing attack within this leaf; retain the other gaps as stated bounds. No source-task status/acceptance/resource changed.

```verdict-findings
{
  "findings": [
    {
      "id": "interrupted-fragment-outside-context",
      "row": "child state transitions",
      "invariant": "Repository model-visible-context rule 6: every newly injected fragment must be defined as a struct in core/context and implement ContextualUserFragment.",
      "mechanism": "codex-rs/core/src/session_prefix.rs:45-51 adds a raw format! renderer for the new INTERRUPTED fragment rather than a core/context struct/ContextualUserFragment implementation. core/src/agent/control/completion.rs:95-122 calls it and packages the resulting String into queue-only InterAgentCommunication. protocol/src/protocol.rs:883-906 copies plaintext content into AgentMessage model input; core/src/session/mod.rs:4001 records it. There is no intervening typed fragment conversion. Existing completion/message types under core/context implement the required trait; neither has an INTERRUPTED variant. This is a statically reproduced architecture/contract bypass, not a claim that an Interrupted runtime wake was executed or failed.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/session_prefix_tests.rs",
          "command": "git grep -n -F 'Agent interrupted. Its turn ended without a final answer' e8eef4f44743b4a6d256e610f91527e715ae042b -- codex-rs/core/src/context",
          "expected_failure": "Exit 1 (observed): no core/context definition of the new fragment. Paired candidate source read confirms the string exists in session_prefix.rs:50 and is called by completion.rs:99. This is a source-contract reproduction, not a Rust test."
        },
        {
          "test_file": "codex-rs/core/src/session_prefix_tests.rs",
          "command": "git grep -n -F 'format_inter_agent_interrupted_message' e8eef4f44743b4a6d256e610f91527e715ae042b -- codex-rs/core/src/context",
          "expected_failure": "Exit 1 (observed): no delegation from core/context. Source inspection reported raw_format_macro=true, contextual_fragment_delegation=false, context_definition_hits=[]."
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "requested_change": "Define the interrupted fragment under core/context with ContextualUserFragment and route production formatting through it. Add the mandatory real-interruption integration coverage on this leaf: registered parent gets exactly one queue-only notice/model request per Running -> Interrupted transition; ordinary parent remains quiet; no success claim and global is_final unchanged. Run a narrowing mutant on the production Interrupted delivery guard, not only on the string formatter."
    }
  ],
  "notes": [
    {
      "id": "interruption-routing-coverage-gap",
      "text": "AC7 production behavior remains unknown. Exact candidate grep for interrupt_agent|abort_all_tasks|TurnAbortReason|INTERRUPTED in goal_native_wait.rs exits 1. Only session_prefix_tests.rs:39 checks notice wording; producer results coverage map explicitly admits the real-abort once-per-transition gap. A passing formatter mutant is not proof of parent-marker eligibility, queue-only delivery or deduplication. Requested public-entry test/mutant is named in the finding; no runtime failure is inferred."
    },
    {
      "id": "lifecycle-concurrency-unverified",
      "text": "Static interleaving worth targeting: pause continue_if_idle after inspecting Running, disable or stop the runtime, then release registration. runtime.rs:714-730 does not recheck lifecycle after the await; synchronous set_enabled(false)/stop already removed the marker. A second interleaving is old clear dropping its permit before asynchronous cleanup (runtime.rs:449-450), concurrent new active-goal registration, then old cleanup removing the new own marker. These were NOT executed; retain as suspicions. Request deterministic registration-vs-disable/stop and old-clear-vs-new-goal fixtures, not a separate research/harness leaf."
    },
    {
      "id": "lifecycle-and-resume-evidence-bound",
      "text": "Producer reports 9/9 AC rows mapped but only 5/9 fully driven and 4/9 partial (AC5/7/8/9). Check-in units prove evaluation/ticket consumption, not live marker reinsert, exhausted retention and late queue-only model wake. restore_thread_runtime_after_resume against an injected in-memory marker is not full resume_thread_with_history with rendered SleepItem plus unloaded child. Add targeted native-child fake-time and full-resume cases or keep those behaviors explicitly unknown."
    },
    {
      "id": "context-size-bound-unverified",
      "text": "The new formatter hard-codes a small payload but interpolates two AgentPaths without a local cap. AgentPath validators in the exact candidate protocol/src/agent_path.rs:125-180 constrain syntax, not length. Short-path approx_token_count unit coverage does not establish a hard item bound. No long-path public-entry reproduction ran, so >1k/P0 or >10k claims are not asserted; request boundary coverage if long task names are supported."
    },
    {
      "id": "dependency-and-size-review",
      "text": "Diff is 1,665 insertions + 16 deletions over 26 files, exceeding repository 800-line guidance; 728 lines are one integration fixture file. Most growth is tests. Smallest plausible review stage separates typed owned-child inspection/atomic remove_if from goal wait wiring, subject to the orchestrator retaining coherent dependencies. Cargo.toml/Cargo.lock add the already-workspace codex-extension-items edge; MODULE.bazel.lock is unchanged. Whether bazel-lock-update ran or produced no drift is unknown from the attached gate summary; do not infer a Bazel failure."
    },
    {
      "id": "reuse-and-no-source-writes",
      "text": "Hosted evidence is reused from task-scoped precheck 5 exactly bound to candidate tree, not rerun by this panel. No cargo, just, build, Rust suite, or mutant execution was performed. All source-task access was read-only; no accept/reject/status/handoff/resource write on TASK-260929-csyzcj."
    }
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "Hosted candidate run 37855177143: goal_wait_registers_marker_and_wakes_on_child_completion drives set_thread_goal -> continue_if_idle -> native V2 child completion -> pending-work wake and asserts an outbound model request, silence before wake and removal on admitted turn start. Narrowing ignore_native_pending (37855194303) fails this public-entry test. One SleepItem is stored per TypeId, not per child.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md"
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Hosted skip_failed_lookups mutant 37855265071 is killed by owned_children_inspection_propagates_failed_lookups (loaded, unknown Err, known Unloaded). Candidate OwnedChildInspection::is_pending_native_work admits only PendingInit/Running; runtime.rs:686-710 checks active goal and host capability before registration and propagates the entire read error. Bound: negative inspection coverage is through the narrow inspection API, not a full goal-start fixture with backend failure.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md"
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Hosted insert_after_mail_check mutant 37855212822 is killed by goal_wait_latch_closes_completion_before_registration. Exact candidate test uses two real V2 children, holds registration before insert, confirms completion mail enqueued, releases once, forbids a second idle pass, and asserts mail-wake request plus absence of goal continuation. Every race-specific wait is bounded. Permit sharing at runtime.rs:736-742 closes the earlier recheck self-deadlock.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md"
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "Hosted insert_clobbers_one_foreign (37855230691) and unconditional_remove (37855282786) fail goal_wait_preserves_foreign_sleep_across_register_and_turn_start as well as helper tests. Candidate ExtensionData::remove_if (state.rs:142-153) evaluates predicate/removes under the same mutex; registration/removal preserves a foreign clock-wait-1 marker across idle and turn start.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md"
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "evidence": "Hosted goal_wait_removed_on_clear_release_and_resume drives public release_native_wait, GoalService::clear_thread_goal and restore_thread_runtime_after_resume. AC1/latch assert turn-start removal. Small native_pending_exhausts_checkins_then_waits_without_deadline demonstrates the 3-ticket bound. Held is limited to these attacks: native check-in removal/reinsert and exhausted-marker late wake, disable/stop interleaving, and full rollout resume are not established by the supplied integration fixtures.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md"
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "Hosted goal_wait_registers_marker_and_wakes_on_child_completion asserts 500 ms no parent event after registration, no goal-wait: string in the wake body and no current_time. Static insertion only stores SleepItem; it calls no event/history/reminder API. Bound: CurrentTimeReminder is disabled in this fixture, so it cannot prove an enabled reminder schedule is unchanged.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md"
    },
    {
      "row": "child state transitions",
      "result": "broken",
      "evidence": "The static model-context contract attack reproduced interrupted-fragment-outside-context (below). Hosted interrupted_claims_success mutant 37855247950 proves formatter wording only. Hosted two-child latch proves a second Running child remains pending, and existing pending_input::queue_only_agent_mail_wakes_sleeping_root_with_previous_turn_context pins a non-default cyber setting on the same wake scheduler. No supplied goal-wait integration test drives a real Interrupted transition or once-per-transition routing. That missing behavioral fixture is not reported as a reproduced runtime failure.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-5.md"
    }
  ],
  "free_hunt": {
    "budget_minutes": 3,
    "started_at_utc": "2026-10-08 23:39:59",
    "ended_at_utc": "2026-10-08 23:41:08",
    "examined": [
      "new model-visible interrupted fragment ownership/type",
      "registration versus synchronous disable/stop",
      "old clear versus new registration",
      "dependency lock and total diff size",
      "long canonical path bounds"
    ],
    "findings": [
      "interrupted-fragment-outside-context"
    ],
    "unexecuted_suspicions": [
      "lifecycle-concurrency-unverified",
      "context-size-bound-unverified"
    ]
  }
}
```
