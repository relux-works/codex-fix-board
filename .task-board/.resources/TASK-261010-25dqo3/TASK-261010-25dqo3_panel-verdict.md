# TASK-261010-25dqo3 — R141 panel A, CR-TASK-260929-csyzcj-3 revision 3

changes_requested

Replay: base `39c264c34e61b5171ae13b0f756746c24ea5f51a` plus the attached rev3 patch gives exactly candidate tree `9ccda9214ac5b9f0ddb5533b77418d0f2045d74b`. Temporary-index write-tree returned that OID twice, exit 0 both times. No nested worktree was used.

Key result: the 682-byte interruption **body** cap is correct, but the complete model input still includes unbounded `author`/`recipient`. This is a P0 repeat of the complete-item bound defect. Lifecycle concurrency stays advisory because the public app-server goal RPCs are serialized per thread and no reachable runtime reproduction was executed.

Commands and observed exits (panel execution, not producer execution):

| Command/process | Exit | Evidence |
|---|---:|---|
| `task-board m 'set_status(TASK-261010-25dqo3, status=analysis)'` | 0 | Own panel task only. |
| Initial replay setup containing `rm -f` | no process exit | Tool policy refused process creation; none of that shell call ran. Replaced safely below. |
| `python3 -c 'from pathlib import Path; p=Path(".temp/TASK-261010-25dqo3-replay.idx"); p.parent.mkdir(exist_ok=True); p.unlink(missing_ok=True)'` | 0 | Temporary index setup only. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-25dqo3-replay.idx" git read-tree 39c264c34e61b5171ae13b0f756746c24ea5f51a` | 0 | Replay base. |
| `task-board resource get TASK-260929-csyzcj TASK-260929-csyzcj_change-request_rev3.patch --output .temp/TASK-260929-csyzcj_change-request_rev3.patch` | 0 | Read-only patch download. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-25dqo3-replay.idx" git apply --cached .temp/TASK-260929-csyzcj_change-request_rev3.patch` | 0 | Patch application to temporary index. |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-25dqo3-replay.idx" git write-tree` (twice) | 0 each | Exact candidate both times. |
| `git diff --check 39c264c34e61b5171ae13b0f756746c24ea5f51a 9ccda9214ac5b9f0ddb5533b77418d0f2045d74b` (standalone gate) | 0 | Whitespace gate; no build. |
| `python3 .temp/TASK-261010-25dqo3-envelope-assay.py` (standalone attack) | **1** | **Expected-red/failing**: whole item exceeds the bound even though body assertions pass. Not a passing test. |
| `python3 .temp/TASK-261010-25dqo3-validate-verdict.py` (standalone artifact gate) | 0 | One valid findings block, one-word verdict, seven exact rows, replay identity, complete embedded assay. |
| `git status --porcelain=v1` (standalone) | 0 | Empty; no tracked repository edits. |
| `task-board spawn directives RUN-261010-8264cd` (twice) | 0 each | No directives; run not goal-bound. |

Read-only evidence commands: successful `task-board q get` projections for description/scope/AC, own checklist, and preconditionResources/outcomeResources exited 0. Resource downloads for surface-table.md, producer-brief.md, results, precheck-10, rev3-validation, final-plan.md and rev2 verdict exited 0. Candidate `git diff --stat`, diff subsets, `git show 9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:<existing path>`, `git grep`, `git ls-tree`, and bounded reads/searches of their local copies succeeded in the calls cited below. The three source reads inside the assay individually exited 0. Source citations below always refer to this candidate, not the worktree's base files.

Exploration/recovery failures, none represented as green validation:
- Two initial board queries with the unknown `resources` projection: exit 1 each; repaired to preconditionResources/outcomeResources. Scoped `schema(operation=get)`: exit 0.
- Skill-relative reviewer-role `cat`: exit 1 (file absent); the installed `/Users/administrator/.roles/reviewer/role.md` read exited 0. project-management SKILL.md, querying, roles, and negative-evidence reads succeeded.
- Two skill-reference `rg --files` probes had no matches, exit 1; an optional role-directory search including absent paths exited 2.
- `task-board resource list TASK-260929-csyzcj`: exit 0, but prints help rather than resources; resource projection supplied the actual list.
- Candidate `git show ...:codex-rs/core/src/session/turn_start/scheduler.rs` lookup: shell exit 128 (path absent); actual scheduler is core/src/tasks/mod.rs.
- Candidate control/registry.rs lookup: shell exit 128 (path absent); registry/edge behavior read from control/runtime_context.rs.
- Compound app-server codex_message_processor.rs lookup plus subsequent rg: overall shell exit 1 (path absent); repaired to message_processor.rs, successful read.
- `git rev-parse 'refs/heads/TASK-260929-csyzcj/wip-10^{tree}'`: exit 128 (ref unavailable); hosted identity is reused from attached evidence only.

Accepted execution evidence: [hosted precheck 10](board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md) reports run [38053090893](https://github.com/ivanopcode/codex/actions/runs/38053090893), exact candidate tree, all four lanes successful, 8/8 narrowing mutants killed. No individual hosted process exits are inferred from these statuses. [Rev3 validation](board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_change-request_rev3-validation.log) records mini-hosted-gate.sh **[exit 0]**, one exact-command shard green, test-case coverage unknown. This panel reran only replay, static reads/assay and whitespace/artifact checks. It ran no cargo/just/build/test/hosted workflow.

```verdict-findings
{
  "findings": [
    {
      "id": "interrupted-agent-message-envelope-unbounded",
      "row": "child state transitions",
      "invariant": "AGENTS.md model-visible-context rules 3–5: every newly injected item has a hard size cap; no item exceeds 10K tokens; any new item able to cross 1K tokens requires P0/manual review. Rev2 requested a bound on the complete item, including model-visible envelope fields.",
      "mechanism": "The fragment caps both textual path interpolations, but the production delivery creates InterAgentCommunication with the full child/parent AgentPaths (core/src/agent/control/completion.rs:117–123). protocol/src/protocol.rs:883–920 creates ResponseItem::AgentMessage with author=self.author.to_string() and recipient=self.recipient.to_string(), independently of the bounded content. These are model-visible fields: core/src/context_manager/history.rs:1081–1102 explicitly includes author+recipient bytes in its model-visible item estimator. protocol/src/models.rs:1037–1047 serializes both Strings. History truncates FunctionCallOutput/CustomToolCallOutput only (history.rs:542–555); Prompt::get_formatted_input_for_request clones AgentMessage unchanged (client_common.rs:60–69,92–95), and client.rs:895 passes that input to ResponsesApiRequest. V2 spawn's task_name is an unrestricted String (multi_agents_v2/spawn.rs:263–272), passed to thread_spawn_source at :148–154, then AgentPath::join (multi_agents_common.rs:140–148); agent_path.rs:125–180 validates syntax without a length cap. Thus the new interruption item is still unbounded even though body() is bounded. With recipient=/root and a syntax-valid sender /root/ plus 4,000 or 80,000 lowercase characters, the pinned formatter yields a 417-byte body (<=682), while the entire item's repo-model-visible estimate is 4,428/80,428 bytes, or 1,107/20,107 tokens. This is a source-contract witness, not a Rust execution, actual tokenizer measurement, or observed long-name model request.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261010-25dqo3-envelope-assay.py",
          "command": "python3 .temp/TASK-261010-25dqo3-envelope-assay.py",
          "exit_code": 1,
          "expected_failure": "Observed expected-red exit 1 at the <=10,000 estimated-token assertion. All three pinned git-show subprocesses exited 0; capped body assertions passed, but full AgentMessage author+recipient+content exceeded the limit. The complete assay is embedded below.",
          "executed": true
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_native_wait.rs (requested: goal_wait_interrupted_notice_bounds_full_agent_message)",
          "command": "Hosted only: just test -p codex-core",
          "expected_failure": "Not added or executed by this panel. Drive collaboration/spawn_agent with a long valid task_name, a registered goal wait, and child Op::Interrupt; assert the full outbound agent_message bound including author/recipient, not just content text. Current candidate should violate that bound while its body-only unit test stays green.",
          "executed": false
        }
      ],
      "severity": "bypass",
      "priority": "P0",
      "repeat-of": "interrupted-fragment-has-no-hard-cap",
      "previous_round_relation": "Partial repair of the rev2 complete-item size finding; the same-class interrupted-fragment-unbounded-paths report is also relevant. The textual path interpolation portion is repaired, but the unbounded model-visible envelope survives.",
      "requested_change": "Bound the complete newly generated model input including author/recipient while preserving full internal routing identity and ordinary notices. Avoid silently changing the external AgentPath API as an incidental fix; make any necessary identity/representation tradeoff explicit. Add the public-entry long-path test above and a narrowing mutant that bounds content but leaves one envelope identity uncapped. Obtain exact revised-tree hosted evidence.",
      "sources": [
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/src/context/inter_agent_interrupted_message.rs:47",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/src/agent/control/completion.rs:117",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/protocol/src/protocol.rs:883",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/src/context_manager/history.rs:1081",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/src/client_common.rs:60"
      ]
    }
  ],
  "notes": [
    {
      "id": "evidence-identity",
      "text": "Replay equals 9ccda9214ac5b9f0ddb5533b77418d0f2045d74b. Attached rev3 validation log is 385 bytes, not truncated in this revision: mini-hosted-gate.sh reports [exit 0], exact_command_shard required=1 green=1, test_case_coverage=unknown. Hosted precheck 10 names candidate run 38053090893 and four successful lanes plus 8/8 kills. These are reused attached results, not independently rerun CI. Individual hosted process exit codes/mutant run IDs are not in that summary and are unknown. The local wip-10 ref lookup failed (128), so no independent snapshot-ref verification is claimed.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md",
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_change-request_rev3-validation.log"
      ]
    },
    {
      "id": "coverage-accounting",
      "text": "7/7 prescribed rows swept exactly once: 6 held within stated evidence bounds, 1 broken. This is not 9/9 fully executed AC coverage. AC5/8/9 include acknowledged gaps; proposed unexecuted tests are listed below."
    },
    {
      "id": "body-repair",
      "text": "Typed core/context ownership, short-notice wording, and both body path truncations are present. The derived body cap is 682 bytes. The hosted sender-uncapped mutant kills only the body interpolation defect; it never tests author/recipient in the delivered AgentMessage. The failure is beyond the fragment's render() boundary."
    },
    {
      "id": "lifecycle-interleaving-advisory",
      "text": "runtime.rs:436–450 applies old clear effects after reconciling potentially newer committed state, calls note_clear unconditionally, drops the permit, then removes any goal-wait prefix. api.rs:363–367 separates delete from effects. A concurrent new generation could lose its marker/timer; runtime inactive-status cleanup also drops the permit before asynchronous lookup. However app-server-protocol/common.rs:608–620 assigns set/clear the same per-thread serialization key, and app-server/request_serialization.rs enforces exclusive request execution. Therefore two ordinary same-thread RPCs are not a demonstrated reproduction. Direct service/ongoing tool/idle interactions need a deterministic production-entry latch test before promotion to a runtime finding. Prior rev2 advisory retained; not claimed reproduced."
    },
    {
      "id": "requested-coverage",
      "text": "Requested, not run: paused-clock live-child check-in removal/reinsertion, marker retention after all three check-ins plus late completion, disable/stop during registration, stale-clear/new-generation via a reachable production path, full resume_thread_with_history with a rendered SleepItem/unloaded child, two child results with the second arriving mid-turn, non-default inherited settings on native goal wake, and a second real Running→Interrupted transition. Release API has only one suite caller and no production service forwarding; its public API is tested, broader wiring remains advisory."
    },
    {
      "id": "size-and-bazel",
      "text": "Candidate delta is 29 files, 2,103 insertions/16 deletions; the new core integration file is 1,039 lines. This exceeds 800-line nonmechanical guidance. A coherent staging option remains atomic ExtensionData removal + typed child inspection, then goal integration/notice. Cargo adds only an existing workspace extension-items edge. BUILD.bazel uses codex_rust_crate/all_crate_deps and globs source files. MODULE.bazel.lock is unchanged; no bazel-lock-update execution is supplied by the attached evidence, so drift is unknown, not an asserted build failure."
    },
    {
      "id": "scope",
      "text": "No product source, test, config, dependency, branch or commit was changed by this panel. git status remains empty. All candidate reads were tree-pinned. No cargo, just, Rust build/test, nested worktree, archive attachment or background process ran. All board writes target TASK-261010-25dqo3 exclusively; none target TASK-260929-csyzcj."
    }
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "Hosted goal_wait_registers_marker_and_wakes_on_child_completion drives V2 spawn and actual parent model request; ignore_native_pending is killed. Static continue_if_idle→typed child inspection→atomic single SleepItem slot→recheck→handlers inter_agent_communication→tasks pending-work wake is connected. Body-only marker presence is not the wake proof.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/tests/suite/goal_native_wait.rs:247",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/goal/src/runtime.rs:703"
      ],
      "bound": "Running-child idle and completion wake exercised; no claim of every trigger-mail or registration concurrency permutation."
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Hosted pending_native_work_is_only_pending_init_and_running and owned_children_inspection_propagates_failed_lookups cover loaded statuses, known Unloaded, and unknown-child Err. skip_failed_lookups is killed. runtime_context.rs propagates edge/read and backend errors; runtime.rs maps inspection Err with ? rather than empty/proceed. Goal/status/host eligibility precedes registration.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/src/agent/control/runtime_context.rs:150",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/src/agent/control_tests.rs:5645",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/goal/src/runtime.rs:653"
      ],
      "bound": "Unknown/unloaded/error helper attacks are executed; a forced manager/backend error through an actual idle callback is not separately reported in hosted summary."
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Hosted goal_wait_latch_closes_completion_before_registration kills insert_after_mail_check. It confirms mail queued before gate release, retains a second Running child, forbids a masking second idle pass, asserts one model wake/no goal steering, and bounds all waits. Post-insert recheck shares the held goal permit through GoalTurnStartPermit/GoalTurnStartLease so the synchronous on_turn_start callback avoids semaphore self-deadlock.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/tests/suite/goal_native_wait.rs:366",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/goal/src/runtime.rs:722",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/goal/src/extension.rs:276"
      ],
      "bound": "Final-completion race covered; interruption before registration is a distinct unexecuted scenario."
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "Hosted insert_clobbers_one_foreign and unconditional_remove are killed by the real foreign-sleep registration/turn-start suite and small lease tests. insert_if/remove_if predicate and mutation share the ExtensionData mutex. Foreign clock-wait-1 is compared as a whole object through turn start. Candidate-wide source probe identifies no foreign production store that mints goal-wait: ids.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/goal/src/native_wait.rs:42",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/extension-api/src/state.rs:140",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/tests/suite/goal_native_wait.rs:623"
      ],
      "bound": "Prefix ownership protects foreign namespace values; isolation of different goal generations is not established by this test."
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "evidence": "Hosted clear/release/resume suite drives GoalService clear and runtime restoration after explicit registration. Admitted-turn removal is proved by the retained-latch test. Hosted native_pending_exhausts_checkins_then_waits_without_deadline proves three-ticket exhaustion policy. Static disable/stop/inactive/resume paths remove only owned markers; idle registration returns in Wait without deleting the marker after exhaustion.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/tests/suite/goal_native_wait.rs:731",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/goal/tests/native_wait.rs:142",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/goal/src/extension.rs:268"
      ],
      "bound": "Held for these attacks only. Live-child check-in reinsertion/late wake, disable/stop interleavings, full rendered-rollout resume, and a reachable stale-clear race remain unknown; explicit release lacks an internal production caller."
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "Hosted registration/wake test asserts a 500ms event-silence window and absence of goal-wait: and current_time text from the wake request. Static registration stores only ExtensionData, with no history/event/reminder API call. The separate goal scheduler owns timers and warnings.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/tests/suite/goal_native_wait.rs:326",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/ext/goal/src/native_wait.rs:42"
      ],
      "bound": "The fixture disables CurrentTimeReminder; preserving an enabled reminder schedule is source-inspected, not separately executed."
    },
    {
      "row": "child state transitions",
      "result": "broken",
      "evidence": "Hosted real Op::Interrupt registered/ordinary-parent tests prove one queue-only INTERRUPTED notice, one wake, no success claim, ordinary-parent silence. Duplicate/success mutants are killed; the global is_final match is unchanged. The typed fragment and body cap repairs hold, but the complete new AgentMessage carries unbounded author/recipient paths: interrupted-agent-message-envelope-unbounded. Static assay exits 1 at >10K estimated tokens while body remains 417/682 bytes.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-10.md",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/tests/suite/goal_native_wait.rs:774",
        "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b:codex-rs/core/src/context_manager/history.rs:1081"
      ],
      "bound": "Actual tokenizer count and long-name runtime request not executed. Reused/error helper states inspected; second-child-mid-turn, non-default wake settings and repeated interruption transitions lack dedicated reported execution."
    }
  ],
  "free_hunt": {
    "budget_minutes": 3,
    "started_at_utc": "2026-10-10 15:22:08 UTC",
    "ended_at_utc": "2026-10-10 15:24:29 UTC",
    "examined": [
      "new interruption body's size versus the full serialized/model-visible envelope",
      "AgentPath and V2 spawn name admission",
      "history estimator and request formatting",
      "namespace squatting and marker slot cardinality",
      "release callsites",
      "stale cleanup/new-generation and request serialization",
      "workspace dependency/Bazel/change-size footprint"
    ],
    "findings": [
      "interrupted-agent-message-envelope-unbounded"
    ],
    "unexecuted_suspicions": [
      "stale cleanup versus a reachable tool/service/idle generation change",
      "registration after synchronous disable/stop"
    ],
    "scope": "Static source attacks plus reused exact-tree hosted tests; no Rust/public-entry execution locally."
  }
}
```

Outcome-scoped logbook, 2026-10-10:
- Repeat bound finding: fragment text capped, delivery envelope still unrestricted; P0 manual review needed. A body-only test/mutant cannot attest the complete model-visible item.
- Do not promote stale-cleanup suspicion using a two-RPC race: those RPCs are serialized. Request a reachable service/tool/idle latch test and keep the limitation explicit.
- Surface accounting is 7/7 swept, 6 held within limits and 1 broken; it is not full execution of every AC variant.
- Only this panel's task receives evidence/status/checklist/handoff writes. Nothing is recorded on the reviewed task.

Static assay source follows so the only attached text artifact is self-contained. Save it at the command's path to reproduce the expected-red exit 1; it reads the pinned Git tree and does not execute Rust.


```python
"""Pinned-source size witness; no Rust, model request, or runtime test."""
import json
import re
import subprocess

TREE = "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b"


def read(path):
    result = subprocess.run(
        ["git", "show", f"{TREE}:{path}"], capture_output=True, text=True
    )
    print(f"git show {TREE}:{path}: exit {result.returncode}")
    result.check_returncode()
    return result.stdout


fragment = read("codex-rs/core/src/context/inter_agent_interrupted_message.rs")
protocol = read("codex-rs/protocol/src/protocol.rs")
history = read("codex-rs/core/src/context_manager/history.rs")
assert "let task_name = truncate_path(&self.task_name);" in fragment
assert "let sender = truncate_path(&self.sender);" in fragment
assert "author: self.author.to_string()," in protocol
assert "recipient: self.recipient.to_string()," in protocol
assert "text_bytes(author).saturating_add(text_bytes(recipient))" in history
cap = int(re.search(r"INTERRUPTED_PATH_MAX_BYTES: usize = (\d+);", fragment)[1])


def literal(name):
    return json.loads(re.search(rf'const {name}: &str = ("[^\n]*");', fragment)[1])


prefix, middle, suffix, marker = map(
    literal, ["BODY_PREFIX", "BODY_MIDDLE", "BODY_SUFFIX", "TRUNCATED_PATH_MARKER"]
)
max_body = sum(len(s.encode()) for s in [prefix, middle, suffix]) + 2 * (
    cap + len(marker.encode())
)


def truncate(path):
    return path if len(path) <= cap else path[:cap] + marker


estimates = []
for name_size in [4000, 80000]:
    recipient = "/root"
    author = "/root/" + "s" * name_size
    body = prefix + truncate(recipient) + middle + truncate(author) + suffix
    body_bytes = len(body.encode())
    assert body_bytes <= max_body
    model_bytes = len(author.encode()) + len(recipient.encode()) + body_bytes
    estimate = (model_bytes + 3) // 4
    estimates.append(estimate)
    print(
        f"name={name_size}; capped body={body_bytes}/{max_body} bytes; "
        f"whole-item model-visible bytes={model_bytes}; repo-estimated tokens={estimate}"
    )
assert max(estimates) <= 10000, (
    "expected-red: bounded body leaves author/recipient unbounded; "
    "the complete new AgentMessage exceeds the repository 10K estimate"
)

```
