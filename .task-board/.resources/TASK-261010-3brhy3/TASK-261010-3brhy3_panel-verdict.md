# TASK-261010-3brhy3 — R141 DELTA panel, CR-TASK-260929-csyzcj-2 revision 2

changes_requested

Replay tree: **78b49cd71e2ccfc855069cc05f99ec294e383e85**, exactly the expected candidate.
Base: 39c264c34e61b5171ae13b0f756746c24ea5f51a.
Previous candidate: e8eef4f44743b4a6d256e610f91527e715ae042b.

Revalidation by RUN-261010-8fbfda: the prior type-ownership finding is fixed; the newly injected interruption item still has no hard size cap. All seven surface rows received exactly one result: six held within stated evidence bounds and one broken. Recommendation: enforce a documented complete-item cap in the owning leaf, then run a hosted long-valid-task-name interruption boundary test and a narrowing cap mutant. P0/manual size review is requested because unbounded paths can grow arbitrarily; no actual tokenizer threshold crossing or long-name runtime request is claimed.

An outcome already existed on this panel task. This run independently replayed and rechecked it and updates that registered resource. It did not reproduce every auxiliary command from the earlier run. Earlier source assay scripts remain embedded below for reproduction; their delta audit and missing-cap checks were both rerun here.

No accept/reject/withdraw/status/handoff/resource/note/checklist write on TASK-260929-csyzcj. No source code, normal Git index, branch or commit changed. Temporary-index replay and static inspection only; no cargo, just, Rust tests or builds.

## Current run commands and observed exit codes

Commands ran directly, without tee or gate pipelines. This ledger records current-run replay, attacks, identity checks, safe checkpoints and diagnostic failures.

| Command | Exit |
|---|---:|
| task-board m 'set_status(TASK-261010-3brhy3, status=analysis)' | 0 |
| git rev-parse --show-toplevel | 0 |
| mkdir -p .temp | 0 |
| python3 temporary-index unlink(missing_ok=True) | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3brhy3-replay.idx" git read-tree 39c264c34e61b5171ae13b0f756746c24ea5f51a` | 0 |
| `task-board resource get TASK-260929-csyzcj TASK-260929-csyzcj_change-request_rev2.patch --output .temp/TASK-260929-csyzcj_change-request_rev2.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3brhy3-replay.idx" git apply --cached .temp/TASK-260929-csyzcj_change-request_rev2.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3brhy3-replay.idx" git write-tree` | 0 |
| `git diff --stat 39c264c34e61b5171ae13b0f756746c24ea5f51a 78b49cd71e2ccfc855069cc05f99ec294e383e85` | 0 |
| `git status --short` | 0 |
| `task-board q 'get(TASK-260929-csyzcj) { description scope ac resources notes }'` | 1 |
| `task-board q 'get(TASK-261010-3brhy3) { title status checklist resources }'` | 1 |
| `cat /Users/administrator/.claude/skills/project-management/.roles/reviewer/role.md /Users/administrator/.claude/skills/project-management/references/negative-evidence.md` | 1 |
| `rg --files --hidden /Users/administrator/.claude/skills/project-management /Users/administrator/.codex/skills/project-management -g '*role.md'` | 1 |
| `task-board spawn directives RUN-261010-8fbfda` | 0 |
| `rg --files --hidden /Users/administrator/.claude/skills /Users/administrator/.codex/skills -g 'role.md' -g '*reviewer*'` | 1 |
| `git diff --stat e8eef4f44743b4a6d256e610f91527e715ae042b 78b49cd71e2ccfc855069cc05f99ec294e383e85` | 0 |
| `command -v logbook` | 1 |
| `task-board resource get TASK-260929-csyzcj TASK-260929-csyzcj_change-request_rev2-validation.log --output .temp/TASK-260929-csyzcj_change-request_rev2-validation.log` | 0 |
| `git diff --exit-code e8eef4f44743b4a6d256e610f91527e715ae042b 78b49cd71e2ccfc855069cc05f99ec294e383e85 -- codex-rs/core/src/agent/control/completion.rs codex-rs/core/src/agent/control/runtime_context.rs codex-rs/ext/goal/src/runtime.rs codex-rs/ext/goal/src/native_wait.rs codex-rs/ext/goal/src/background_wait.rs codex-rs/ext/goal/src/extension.rs codex-rs/core/src/session/mod.rs codex-rs/core/src/agent/status.rs codex-rs/protocol/src/protocol.rs` | 0 |
| `python3 scratch materialization (script included in run transcript)` | 1 |
| `python3 .temp/TASK-261010-3brhy3_static_attack.py` | 1 |
| `python3 .temp/TASK-261010-3brhy3_delta_audit.py` | 0 |
| `task-board spawn directives RUN-261010-8fbfda` | 0 |

The static_attack exit 1 is an expected-red contract check: six source reads succeeded, its exact formatter/validator assertions succeeded, then the explicit missing-hard-cap failure was reported. It is a failure, not a passing gate. It emits source-grammar witnesses of 8,345 and 65,689 bytes; any four-byte token estimate is only an estimate.

Other current-run reads: skill and focused research-workflow reads exit 0; resource and candidate source reads (git show/grep, cat, sed, rg) exit 0 unless a diagnostic failure is listed above. The first scratch materialization exited 1 because git show of the incorrect core/src/input_queue.rs path exited 128; the corrected core/src/session/input_queue.rs read and subsequent materialization exited 0. That failed lookup was not treated as absence. The reviewer role reference is missing (cat exit 1; searches exit 1), so the task-provided panel contract governed the sweep. Unsupported resource list commands exited 0 with help text, not inventories; the corrected preconditionResources/outcomeResources query exited 0. command -v logbook exited 1 (unavailable); the logbook entry is retained inside this sole outcome and recorded in own-task notes. The attempted rm -f was rejected before execution and has no process exit code; safe Python unlink replaced it.

`python3 .temp/TASK-261010-3brhy3_refresh_outcome.py` exited 0 (artifact written). `python3 .temp/TASK-261010-3brhy3_validate_verdict.py` exited 0: exactly one valid verdict-findings object, one standalone verdict, seven distinct required rows, six held/one broken, all mandatory finding fields present. `git status --porcelain=v1` exited 0 with empty output. Resource-update help and the focused resources-and-bugs skill reference reads exited 0. No Rust gate is marked locally green.

## Sources and evidence bounds

- TASK-260929-csyzcj/surface-table.md: exact seven-row expected set.
- TASK-260929-csyzcj/TASK-260929-csyzcj_review-verdict-rev1.md: one prior finding, plus disclosed residual notes.
- TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-8.md: exact tree, [hosted run 38017711768](https://github.com/ivanopcode/codex/actions/runs/38017711768), four successful lanes, core 5085/5085, seven killed mutants. This panel reused attached evidence; it did not rerun CI or fetch independent hosted logs. Numeric exits for hosted lane commands and individual mutant run IDs are not supplied by that report, so remain unknown.
- TASK-260929-csyzcj/TASK-260929-csyzcj_change-request_rev2-validation.log: 383 bytes; mini-hosted-gate.sh [exit 0], exact_command_shard 1/1, test_case_coverage unknown. This revision's log is not truncated.
- TASK-260929-csyzcj/TASK-260929-csyzcj_results.md and mutants.json: current coverage bounds and exact mutant patches; producer prose is context, not authority.
- AGENTS.md Model visible context rules 3–6: normative size/type obligations.
- Source citations below refer to git show CANDIDATE:path, never the control checkout.

Pinned blobs:
inter_agent_interrupted_message.rs d58f7b7a573f4a6ab569c202ffb1c8501c10c8ef;
session_prefix.rs eab87364f0e90f82d5c6357ef69f07bcf9035d60;
protocol/src/agent_path.rs c0ad8b734a94baedc96e93186ce6d8cc3d588ce3;
context-fragments/src/fragment.rs a81e6e395431e1e494f85cc9641af21bcda51ace;
context_manager/history.rs 2475e685ea12ff4f3d32cb00a1cfd877969f5673.

## Logbook — 2026-10-10, this panel only

Replay matched. Prior type-ownership bypass repaired and real interruption coverage added. The prior panel run promoted its context-size-bound suspicion into a source-contract finding: unbounded accepted AgentPaths reach the new fragment unchanged, with no subsequent item cap in the inspected delivery/history path. Assay exited 1 as expected. The arbitrary-length property is proven statically; actual long-name public-entry behavior and tokenizer counts were not executed. Requested follow-up stays within the owning leaf: enforce a documented item cap, add hosted public-entry boundary coverage and a narrowing mutant. No source-task board write; verdict is for independent review/merge by the orchestrator.


Current-run logbook addendum: exact replay reverified; prior type fix and existing missing-cap finding independently rechecked, with delta_audit exit 0 and missing-cap source assay exit 1. No new runtime failure inferred. Hosted evidence reused only for its exact candidate tree.

```verdict-findings
{
  "findings": [
    {
      "id": "interrupted-fragment-has-no-hard-cap",
      "row": "child state transitions",
      "invariant": "AGENTS.md model-visible-context rules 3\u20135 require a bounded size and hard cap for every injected item, forbid items above 10K tokens, and require P0/manual review for a new individual item that can cross 1K tokens.",
      "mechanism": "The type-ownership repair is correct, but core/src/context/inter_agent_interrupted_message.rs:35\u201340 directly formats two unrestricted AgentPaths. protocol/src/agent_path.rs:125\u2013180 validates syntax, not length; V2 spawn args.task_name flows through multi_agents_common::thread_spawn_source -> AgentPath::join with no length check. session_prefix.rs:49 clones these paths into the fragment and calls render(); context-fragments/src/fragment.rs:96\u2013104 returns the complete body for empty markers. completion.rs:99,114\u2013130 sends the complete String; control.rs:159\u2013179,232\u2013294 forwards it to Op::InterAgentCommunication; session/handlers.rs:79\u201394 and session/input_queue.rs:297\u2013312 enqueue it unchanged. protocol.rs:883\u2013921 creates an AgentMessage with content self.content.clone(); session/mod.rs:3437\u20133478 prepares images/audio/IDs, not a text cap; context_manager/history.rs:545\u2013555 truncates only FunctionCallOutput/CustomToolCallOutput. Thus fixed prose plus two paths is not a hard bound. This is a static source-contract bypass, not an observed Rust/model runtime failure.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/src/context/inter_agent_interrupted_message_tests.rs",
          "command": "python3 .temp/TASK-261010-3brhy3_static_attack.py",
          "exit_code": 1,
          "expected_failure": "Observed exit 1 at the explicit missing-hard-cap source-contract check, after every pinned source read exited 0 and the exact straight-line formatter shape matched. Source-grammar analogues with 8,192/65,536-byte lowercase/digit/underscore task names produce 8,345/65,689-byte bodies. Four-byte coarse estimates are 2,087/16,423; these are estimates, not actual tokenizer counts or executed requests. Full assay source is included below for reproduction."
        },
        {
          "test_file": "codex-rs/core/src/context/inter_agent_interrupted_message.rs",
          "command": "git grep -n -E 'truncate|MAX.*TOKENS|MAX.*LEN' 78b49cd71e2ccfc855069cc05f99ec294e383e85 -- codex-rs/core/src/context/inter_agent_interrupted_message.rs",
          "exit_code": 1,
          "expected_failure": "Observed exit 1: no local cap/truncation reference. This absence probe is corroboration only; the finding relies on the exact formatter, validator and delivery dataflow above, rather than grep completeness."
        }
      ],
      "severity": "bypass",
      "repeat-of": "none",
      "priority": "P0",
      "manual_review": "Required for the potential >1K-token item; no exact model-token threshold crossing was executed. Arbitrary path length and absent item cap are established statically.",
      "previous_round_relation": "Rev1 note context-size-bound-unverified identified this suspicion but was not a finding. Rev1 finding interrupted-fragment-outside-context is fixed; this mechanism is different, so repeat-of is none.",
      "requested_change": "Establish and enforce a documented hard bound on the complete newly injected interruption item, accounting for path fields/envelope as well as prose. Add a goal_native_wait public-entry boundary case using a long valid task name through collaboration/spawn_agent and Op::Interrupt, assert bounded output with unchanged routing/no-success semantics, and add a narrowing size-cap mutant. Run these on the exact revised candidate in hosted CI. Avoid assuming fixed prose makes variable-length paths bounded."
    }
  ],
  "notes": [
    {
      "id": "previous-round-disposition",
      "text": "Checked all 1/1 prior findings. interrupted-fragment-outside-context is fixed by private core/context struct + ContextualUserFragment + formatter .render() delegation. Its requested real-interruption coverage is present: registered and ordinary parent fixtures submit Op::Interrupt to a live Running V2 child. Global is_final implementation is byte-identical to rev1; in-crate interrupted_stays_non_final pins its semantics. The production double-delivery mutant is reported killed by the scoped count assertion."
    },
    {
      "id": "delta-and-same-class-sweep",
      "text": "Rev1 -> rev2 changes only five files, +385/-11 lines: context type/test/module, session_prefix formatter delegation, and goal_native_wait tests/latch synchronization. Every other registration/inspection/lifecycle/delivery surface was checked byte-identical with git diff --exit-code (exit 0). The existing completion and ordinary message context types already implement the trait; no second newly introduced raw interruption formatter was found. Typed ownership does not solve variable-length context size."
    },
    {
      "id": "execution-evidence-bound",
      "text": "Reused attached hosted precheck 8 on exact tree 78b49cd71e2ccfc855069cc05f99ec294e383e85: run 38017711768, four successful lanes, core 5085/5085 with no flakes, 7/7 mutants killed. No cargo/just/build/Rust test/mutant was run locally. The hosted report supplies success/failure results but no numeric per-command exit codes or individual mutant run IDs; those codes/IDs are unknown to this panel, not inferred as 0/1. The CR rev2 validation log is 383 bytes, untruncated, and explicitly records mini-hosted-gate.sh exit 0 with coverage_unit=exact_command_shard, required=1 green=1 failed=0 missing=0, test_case_coverage=unknown."
    },
    {
      "id": "lifecycle-residuals",
      "text": "Previous nonblocking lifecycle suspicions remain unexecuted: registration racing synchronous disable/stop, and old clear asynchronous cleanup after dropping its permit racing new-goal registration. Request deterministic goal_wait_registration_racing_disable_and_stop and goal_wait_old_clear_preserves_new_generation fixtures; no runtime bug is claimed. Full live native check-in reinsertion, exhausted retention with late wake, and full resume_thread_with_history with rendered SleepItem/unloaded child remain unknown; helper/state-machine tests do not establish those integrations."
    },
    {
      "id": "side-effect-and-settings-bound",
      "text": "No UI/history/reminder calls exist in marker insertion itself; hosted AC1 drives no-event/history absence checks. Its fixture disables CurrentTimeReminder, so enabled-reminder schedule preservation is not established. Existing queue_only_agent_mail_wakes_sleeping_root_with_previous_turn_context exercises inherited settings on the shared wake scheduler; goal_native_wait itself sets no explicit non-default setting. Request enabled-reminder and native-specific non-default-settings variants if those guarantees must be executed."
    },
    {
      "id": "size-and-dependency-bound",
      "text": "Full base -> candidate diff is +2039/-16 across 29 files, over 800-line guidance; the delta under review is +385/-11, below 500 lines. The integration fixture is now 1039 lines; splitting test setup is advisable. Rust dependency/lock changes are inherited byte-identically from rev1; MODULE.bazel.lock is unchanged. Whether bazel-lock-update ran is unknown, not a reproduced Bazel failure. Explicit wait-release production wiring remains absent beyond public handle/tests as already disclosed in rev1."
    },
    {
      "id": "evidence-correction",
      "text": "Producer results mention an is_final export, but this exact candidate keeps it pub(crate); the integration tests assert Interrupted status and the separate in-crate unit test asserts !is_final. Reviewed evidence uses those actual assertions, not the claimed public export. Auxiliary first template-equivalence audit exited 1 because it compared Rust named placeholders with positional placeholders literally; corrected audit compares rendered fixture text and exits 0. This was a reviewer scratch-check error, not a candidate defect."
    },
    {
      "id": "skill-reference-bound",
      "text": "Read project-management SKILL.md, negative-evidence.md and focused CR references. The SKILL's .roles/reviewer/role.md link is unavailable in installed skill roots (read exit 1); task-provided panel-brief contains the operative sweep/free-hunt contract used here. No approval or work stop was inferred from the missing reference."
    },
    {
      "id": "current-run-revalidation",
      "text": "RUN-261010-8fbfda revalidated the existing task-scoped outcome on the unchanged CR rev2 candidate. Replayed patch again through a fresh temporary index (all replay commands exit 0); reran delta_audit (exit 0) and static_attack (expected-red exit 1); reread exact-tree hosted precheck 8 and CR validation log. Seven rows remain six held within stated bounds and one broken. No Rust gates executed, no source-task writes. Existing outcome is updated via resource update rather than silently overwritten or attached as a duplicate."
    }
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "Exact-tree hosted goal_wait_registers_marker_and_wakes_on_child_completion drives goal service -> continue_if_idle -> real V2 child completion -> mailbox wake and asserts an outbound model request. ignore_native_pending is killed by this fixture and others. SleepItem's TypeId slot prevents multiple stored markers. Production source identical to rev1.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-8.md"
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Exact-tree hosted owned_children_inspection_propagates_failed_lookups kills skip_failed_lookups; current-state predicate admits only loaded PendingInit/Running. Non-goal/host capability checks precede registration; inspection Err propagates. Bound: unknown/unloaded failures driven through the inspection API, not a whole-goal injected backend-error fixture. Production source identical to rev1.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-8.md"
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Exact-tree hosted goal_wait_latch_closes_completion_before_registration passes on try 1 and kills insert_after_mail_check. It uses two live children, confirms mail enqueue before releasing registration once, forbids second idle recovery and asserts a real mail-wake/no goal continuation. Revised retained gate only pauses later idle reinsertion until turn-start-removal assertion; it does not inject mail or provide the missing wake. Insert/recheck and permit-share production ordering is unchanged.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-8.md"
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "Exact-tree hosted goal_wait_preserves_foreign_sleep_across_register_and_turn_start plus lease helper tests kill insert_clobbers_one_foreign and unconditional_remove. insert_if/remove_if evaluate predicate and modify the slot under one mutex; foreign clock-wait-1 survives both registration and admitted turn start. Production source identical to rev1.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-8.md"
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "evidence": "Exact-tree hosted goal_wait_removed_on_clear_release_and_resume drives release/clear/runtime restore; AC1/latch pin turn-start removal; native_pending_exhausts_checkins_then_waits_without_deadline pins three-ticket evaluation. Static removal callers cover disable/stop/inactive states. Held only for those attacks; full native live check-in reinsertion/exhaustion-late-wake, concurrent disable/stop/old-clear and full persisted rollout resume are not established. Production source identical to rev1.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-8.md"
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "Exact-tree hosted AC1 asserts 500 ms no parent event and no goal-wait:/current_time string in the wake body. Static try_register_goal_wait_sleep only inserts data: no UI/history/timer/reminder emission. Bound: reminder disabled in fixture; no enabled-reminder schedule attack. Production source identical to rev1.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-8.md"
    },
    {
      "row": "child state transitions",
      "result": "broken",
      "evidence": "Prior typed-fragment finding is fixed; hosted registered/ordinary Op::Interrupt fixtures and interrupted_notice_delivered_twice/interrupted_claims_success kills establish the requested routing/wording coverage. The separate static missing-hard-cap assay fails (exit 1), reproducing interrupted-fragment-has-no-hard-cap. Interrupted remains globally non-final. Reused/error predicates and a second Running child during latch wake are covered, but second-child-mid-turn plus native-specific non-default inherited-settings fixture remain unknown.",
      "source": "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-8.md"
    }
  ],
  "free_hunt": [
    {
      "budget_minutes": 3,
      "started_at_utc": "2026-10-10 04:33:57",
      "ended_at_utc": "2026-10-10 04:36:36",
      "examined": [
        "typed-fragment render and same-class completion/message siblings",
        "path validation and V2 spawn name admission",
        "communication mailbox/history truncation boundary",
        "retained latch gate versus actual wake",
        "is_final claimed export versus candidate",
        "prior lifecycle suspicions and dependency/size delta"
      ],
      "findings": [
        "interrupted-fragment-has-no-hard-cap"
      ],
      "unexecuted_suspicions": [
        "registration versus disable/stop",
        "old-clear versus new-goal registration"
      ],
      "scope": "Static source attack and reused exact-tree hosted evidence only; no Rust/public-entry execution by this panel."
    },
    {
      "budget_minutes": 3,
      "started_at_utc": "2026-10-10 05:00:10",
      "ended_at_utc": "2026-10-10 05:00:39",
      "examined": [
        "V2 task_name admission through thread_spawn_source and AgentPath::join",
        "completion delivery through Op/mailbox to AgentMessage model input",
        "history preparation and truncation scope",
        "same-class fragment trait ownership",
        "unchanged registration/ownership/permit serialization"
      ],
      "findings": [
        "interrupted-fragment-has-no-hard-cap"
      ],
      "scope": "Bounded static revalidation; no additional finding and no public-entry runtime execution."
    }
  ]
}
```



## Reproducible source assay — TASK-261010-3brhy3_static_attack.py

Save the following as .temp/TASK-261010-3brhy3_static_attack.py and invoke the exact command in the ledger. This is a Python source inspection, not a Rust test.

```python
import ast
import json
import re
import subprocess
import sys

TREE = "78b49cd71e2ccfc855069cc05f99ec294e383e85"


def source(path):
    result = subprocess.run(["git", "show", f"{TREE}:{path}"], capture_output=True, text=True)
    print(json.dumps({"command": result.args, "exit_code": result.returncode}))
    result.check_returncode()
    return result.stdout


fragment_path = "codex-rs/core/src/context/inter_agent_interrupted_message.rs"
fragment = source(fragment_path)
prefix = source("codex-rs/core/src/session_prefix.rs")
agent_path = source("codex-rs/protocol/src/agent_path.rs")
trait = source("codex-rs/context-fragments/src/fragment.rs")
protocol = source("codex-rs/protocol/src/protocol.rs")
history = source("codex-rs/core/src/context_manager/history.rs")

# Source shape checks bound this assay to the exact straight-line formatter.
# This does not execute Rust, a model, or a production entry point.
assert "impl ContextualUserFragment for InterAgentInterruptedMessage" in fragment
assert "InterAgentInterruptedMessage::new(task_name.clone(), sender.clone()).render()" in prefix
body = re.search(r"fn body\(&self\) -> String \{(.*?)\n    \}", fragment, re.S).group(1)
match = re.fullmatch(r'\s*format!\(\s*("(?:[^"\\]|\\.)*")\s*,\s*self.task_name, self.sender,\s*\)\s*', body)
assert match, "formatter shape changed; no absence claim is valid"
template = ast.literal_eval(match.group(1))
assert '("", "")' in fragment
assert "if start_marker.is_empty() && end_marker.is_empty() {\n            return body;" in trait
validator = agent_path.split("fn validate_agent_name", 1)[1].split("fn validate_absolute_path", 1)[0]
assert "is_ascii_lowercase() || ch.is_ascii_digit() || ch == '_'" in validator
assert "len(" not in validator and "count(" not in validator
assert "validate_agent_name(agent_name)?;" in agent_path
assert "text: self.content.clone()" in protocol
assert "if let ResponseItem::FunctionCallOutput { output, .. }\n        | ResponseItem::CustomToolCallOutput" in history

for n in (8192, 65536):
    name = ("zq7_v9p2" * ((n + 7) // 8))[:n]
    # These predicates reproduce the inspected name grammar, not Rust execution.
    allowed_by_source_grammar = bool(name) and name not in {"root", ".", ".."} and "/" not in name and all(c in "abcdefghijklmnopqrstuvwxyz0123456789_" for c in name)
    assert allowed_by_source_grammar
    rendered = template.format("/root", "/root/" + name)
    print(json.dumps({"static_witness_name_bytes": n, "allowed_by_inspected_source_grammar": allowed_by_source_grammar, "rendered_body_bytes": len(rendered.encode()), "coarse_four_bytes_per_token_estimate": (len(rendered.encode()) + 3) // 4, "runtime_executed": False}))

print("FAIL: source-contract assay: variable-length accepted AgentPaths reach the interrupted body unchanged; no hard item cap exists in the inspected formatter/render/model-item path.")
sys.exit(1)
```

## Reproducible source assay — TASK-261010-3brhy3_delta_audit.py

Save the following as .temp/TASK-261010-3brhy3_delta_audit.py and invoke the exact command in the ledger. This is a Python source inspection, not a Rust test.

```python
import ast
import json
import re
import subprocess
from pathlib import Path

TREE = "78b49cd71e2ccfc855069cc05f99ec294e383e85"
PREV = "e8eef4f44743b4a6d256e610f91527e715ae042b"


def read(tree, path):
    result = subprocess.run(["git", "show", f"{tree}:{path}"], capture_output=True, text=True)
    result.check_returncode()
    return result.stdout


prefix = read(TREE, "codex-rs/core/src/session_prefix.rs")
fragment = read(TREE, "codex-rs/core/src/context/inter_agent_interrupted_message.rs")
old = read(PREV, "codex-rs/core/src/session_prefix.rs")
old_function = old.split("pub(crate) fn format_inter_agent_interrupted_message", 1)[1].split("#[cfg(test)]", 1)[0]
old_template = ast.literal_eval(re.search(r'format!\(\s*("(?:[^"\\]|\\.)*")', old_function).group(1))
new_template = ast.literal_eval(re.search(r'format!\(\s*("(?:[^"\\]|\\.)*")', fragment).group(1))
assert old_template.format(task_name="/root", sender="/root/worker") == new_template.format("/root", "/root/worker")
assert "InterAgentInterruptedMessage::new(task_name.clone(), sender.clone()).render()" in prefix
assert "impl ContextualUserFragment for InterAgentInterruptedMessage" in fragment
board_resources = Path("/Users/administrator/Developer/ReluxWorks/codex-fix-board/.task-board/.resources/TASK-260929-csyzcj")
previous_verdict = json.loads(re.findall(r"```verdict-findings\n(.*?)\n```", (board_resources / "TASK-260929-csyzcj_review-verdict-rev1.md").read_text(), re.S)[0])
assert [f["id"] for f in previous_verdict["findings"]] == ["interrupted-fragment-outside-context"]
print(json.dumps({"previous_findings": 1, "type_ownership_fix_verified": 1, "notice_rendering_unchanged_for_named_fixture": True, "runtime_execution": False}))
for path in ["codex-rs/core/src/context/inter_agent_interrupted_message.rs", "codex-rs/core/src/session_prefix.rs", "codex-rs/protocol/src/agent_path.rs", "codex-rs/context-fragments/src/fragment.rs", "codex-rs/core/src/context_manager/history.rs"]:
    result = subprocess.run(["git", "rev-parse", f"{TREE}:{path}"], capture_output=True, text=True)
    result.check_returncode()
    print(path, result.stdout.strip())
```

## Artifact validator

```python
import json
import re
from pathlib import Path

path = Path(".temp/TASK-261010-3brhy3_panel-verdict.md")
text = path.read_text()
blocks = re.findall(r"^```verdict-findings\n(.*?)\n```$", text, re.M | re.S)
assert len(blocks) == 1
result = json.loads(blocks[0])
surface = Path("/Users/administrator/Developer/ReluxWorks/codex-fix-board/.task-board/.resources/TASK-260929-csyzcj/surface-table.md").read_text()
expected = json.loads(re.findall(r"```surface-table\n(.*?)\n```", surface, re.S)[0])["rows"]
actual = [row["row"] for row in result["surface_results"]]
assert len(actual) == len(set(actual)) == len(expected) == 7
assert set(actual) == set(expected)
assert all(row["result"] in {"held", "broken", "not-attacked"} for row in result["surface_results"])
assert all(row.get("evidence") for row in result["surface_results"])
assert re.findall(r"^(accept|changes_requested)$", text, re.M) == ["changes_requested"]
for finding in result["findings"]:
    assert {"id", "row", "invariant", "mechanism", "reproductions", "severity", "repeat-of"} <= finding.keys()
    assert finding["severity"] in {"bypass", "regression", "robustness", "note"}
    assert finding["row"] in expected
    for reproduction in finding["reproductions"]:
        assert {"test_file", "command", "expected_failure", "exit_code"} <= reproduction.keys()
assert "78b49cd71e2ccfc855069cc05f99ec294e383e85" in text
assert "Logbook" in text
assert "sys.exit(1)" in text
print(json.dumps({"verdict_blocks": 1, "expected_surface_rows": 7, "actual_unique_surface_rows": 7, "held": 6, "broken": 1, "findings": len(result["findings"]), "one_word_verdict": "changes_requested"}))
```
