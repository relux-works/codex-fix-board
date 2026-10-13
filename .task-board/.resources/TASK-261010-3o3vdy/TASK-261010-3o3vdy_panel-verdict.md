# R141 DELTA panel — CR-TASK-260929-csyzcj-3 revision 3

changes_requested

Replay: base `39c264c34e61b5171ae13b0f756746c24ea5f51a` + attached rev3 patch, using a temporary index, yields **exactly** `9ccda9214ac5b9f0ddb5533b77418d0f2045d74b` (expected candidate). The real worktree index and branch were not changed.

The body-only size repair holds, but the complete interruption item still has unbounded model-visible `author` and `recipient`. One P0 source-contract finding repeats rev2. Six other surface rows hold only for the named attacks and stated coverage bounds.

Commands executed by this panel (actual process status):

| Command | Exit | Evidence |
|---|---:|---|
| `task-board m 'set_status(TASK-261010-3o3vdy, status=analysis)'` | 0 | Panel lifecycle only |
| `python3 -c 'from pathlib import Path; p=Path(".temp/TASK-261010-3o3vdy-replay.idx"); p.parent.mkdir(exist_ok=True); p.unlink(missing_ok=True)'` | 0 | Temporary index preparation |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o3vdy-replay.idx" git read-tree 39c264c34e61b5171ae13b0f756746c24ea5f51a` | 0 | Pinned base |
| `task-board resource get TASK-260929-csyzcj TASK-260929-csyzcj_change-request_rev3.patch --output .temp/TASK-260929-csyzcj_change-request_rev3.patch` | 0 | Read-only resource materialization |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o3vdy-replay.idx" git apply --cached .temp/TASK-260929-csyzcj_change-request_rev3.patch` | 0 | Replay apply |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261010-3o3vdy-replay.idx" git write-tree` | 0 | Expected tree exactly |
| `task-board q 'get(TASK-260929-csyzcj) { description scope ac }'` | 0 | AC source |
| `git diff --exit-code 78b49cd71e2ccfc855069cc05f99ec294e383e85 9ccda9214ac5b9f0ddb5533b77418d0f2045d74b -- . ':!codex-rs/core/src/context/inter_agent_interrupted_message.rs' ':!codex-rs/core/src/context/inter_agent_interrupted_message_tests.rs'` | 0 | All other rev2 paths unchanged |
| `python3 .temp/TASK-261010-3o3vdy-envelope-attack.py` | **1** | Expected-red: missing complete-item hard cap; not a passing test |
| `python3 .temp/TASK-261010-3o3vdy-package.py` | 0 | Pinned reads, rows persisted sequentially, 7/7 row/schema checks |
| `task-board spawn directives RUN-261010-d2101c` | 0 | No directives; no goal binding |

Read-only discovery errors, not gates: query with unsupported `resources` field exited 1 (recovered using direct read-only resource paths); missing installed reviewer-role file `cat` exited 1 (read canonical source at `/Users/administrator/Developer/ReluxWorks/task-board/skill-project-management/.roles/reviewer/role.md`, exit 0); `git rev-parse 'TASK-260929-csyzcj/wip-10^{tree}'` exited 128 (no local ref; not inferred absent hosted evidence); nonexistent `agent/control/communication.rs` source read exited 128 (correct call located in `agent/control.rs`). A scoped-role/logbook filename search exited 1 with no matching filenames. Initial `rm -f` replay preparation was rejected before execution, so has no process exit; safe Python replacement succeeded. Other successful pinned-source reads, diff/stat, resource reads and scoped grep checks exited 0. A broad filesystem filename search was noisy and supplied no review evidence.

No compiled gates ran locally. Reused execution source: `TASK-260929-csyzcj_hosted-precheck-10.md` (run 38053090893, exact tree, four successful lanes, eight killed mutants) and `TASK-260929-csyzcj_change-request_rev3-validation.log` (hosted attestation command exit 0). Individual hosted mutant exits are **unknown**, not invented non-zero numbers. Sources are board read-only resources on the producer task, plus the candidate-tree path/line citations in the finding.

## Successor revalidation — RUN-261010-ebcfa0

This run independently repeated the temporary-index replay: preparation, read-tree, resource get, cached apply and write-tree each exited 0; write-tree again printed exactly `9ccda9214ac5b9f0ddb5533b77418d0f2045d74b`. It reread the surface table, rev2 merged verdict, exact-tree precheck 10 and rev3 validation log (exit 0). The two-file rev2-to-rev3 diff read exited 0; `git diff --exit-code` excluding those two files exited 0. The static envelope witness was rerun directly and exited **1**, as expected: 5/5 body controls held, body 417 bytes, author 80006 bytes, recipient 5 bytes, total 80428 bytes. This is a failing static bound check, not runtime or tokenizer evidence. The predecessor's full surface sweep and bounded free hunt are retained with their original limits; no compiled tests or mutants were rerun.

Recovery discovery: unsupported `resources` query field twice exited 1; missing installed reviewer role read exited 1; an optional-directory filename search exited 2. `task-board resource list` printed help with exit 0 and supplied no resource inventory. Canonical reviewer contract and existing board resource payloads were then read successfully (exit 0). Current-run directive read exited 0: no directives. These discovery commands are not validation gates.

The predecessor's panel CR validation log records a real exit **1**: the research file made the panel tree `958c76f8fa527a5b30c2e9c28d3fb9c88f7e04bb`, which has no green hosted attestation. This is a handoff packaging failure, not candidate validation evidence. The configured mini-hosted-gate explicitly permits an empty delta for evidence-only review panels. Preserve the outcome through resource update and keep the local copy in ignored `.temp`; remove only this run's research file from the source snapshot. No validation policy or hosted-green ledger is changed. No source-task mutations are performed.

Logbook continuation: confirmed the repeated uncapped envelope finding; recovered the panel handoff by using a board-attached outcome with an empty source delta, as supported by the existing gate. The full replay and expected-red static witness were rerun by this successor; hosted execution evidence remains reused only.

Successor gate and packaging commands (standalone processes):

| Command | Exit | Evidence |
|---|---:|---|
| `/Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` | 0 | Empty source delta: `bde782b85ddbc8536536d0747b3917d0f24e1951` equals HEAD tree; no build executed |
| `git status --short` | 0 | Empty output confirms unchanged source worktree |
| `python3 .temp/TASK-261010-3o3vdy-validate.py` | 0 | Exactly one JSON block, required finding/reproduction fields, one-word verdict and 7/7 unique surface rows |

```verdict-findings
{
  "findings": [
    {
      "id": "interrupted-fragment-unbounded-paths",
      "row": "child state transitions",
      "invariant": "AGENTS.md model-context rules 3-5 and rev2 requested repair: hard-bound the complete new interruption item, including model-visible envelope fields; no unbounded item and no item above 10K tokens; potential >1K requires P0/manual review.",
      "mechanism": "The rev3 body cap is correct but incomplete. core/src/context/inter_agent_interrupted_message.rs:73-79 truncates only prose paths. agent/control/completion.rs:114-119 still supplies full child_agent_path and parent_agent_path to InterAgentCommunication::new. protocol/src/protocol.rs:907-911 copies those identities without truncation into ResponseItem::AgentMessage author/recipient; protocol/src/models.rs:1037-1043 serializes both String fields. core/src/session/mod.rs:4001 records that item; context_manager/history.rs:533-580 only truncates tool outputs and :1081-1101 explicitly counts author+recipient as model-visible bytes. client_common.rs:60-67 clones the item into request input; client.rs:989-1005 assigns that input into ResponsesApiRequest. AgentPath grammar has no length bound (protocol/src/agent_path.rs:125-180); thread_spawn_source accepts the valid long task_name through join (tools/handlers/multi_agents_common.rs:133-156). Thus the new INTERRUPTED item remains unbounded after the body-only fix. The full-item repair and public-entry long-path test requested by BOTH rev2 findings are absent; the new unit test/mutant inspect only body rendering.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261010-3o3vdy-envelope-attack.py",
          "command": "python3 .temp/TASK-261010-3o3vdy-envelope-attack.py",
          "exit_code": 1,
          "expected_failure": "Observed exit 1 at complete-item bound assertion after all pinned source checks and 5/5 body controls pass. Source-transcribed valid /root/<80000 lowercase a> sender: body=417 bytes (within 682), author=80006, recipient=5, model-visible sum=80428, four-byte repository estimate=20107, JSON wire analogue=80537 bytes. Static contract/dataflow witness, not executed Rust, tokenizer output, live spawn, or outbound long-item request. Full script and observed output embedded below."
        }
      ],
      "severity": "bypass",
      "priority": "P0",
      "repeat-of": "rev2:interrupted-fragment-unbounded-paths",
      "also_repeats": "rev2:interrupted-fragment-has-no-hard-cap (same mechanism; deduplicated)",
      "requested_change": "Establish a documented hard bound for the entire outgoing interruption item, accounting for author/recipient as well as content while preserving full identity for internal routing. Do not silently narrow the external AgentPath contract or create ambiguous routing aliases. Add a real long valid collaboration/spawn_agent -> registered goal wait -> Op::Interrupt -> captured outbound agent_message boundary case to core/tests/suite/goal_native_wait.rs, with both long sender and long parent cases, exact whole-item size assertions and unchanged short-name/no-success/routing controls. Add a narrowing mutant which keeps the body cap but omits one envelope-field budget; it must fail this PUBLIC-ENTRY test on the exact revised hosted tree."
    }
  ],
  "notes": [
    {
      "id": "prior-round-disposition",
      "text": "Checked 2/2 rev2 findings. Both have their direct body-interpolation symptom fixed by release-effective truncate_path on both values; debug_assert is supplementary, not the enforcing mechanism. Complete-item envelope bounding is still missing; retain one blocking repeated mechanism rather than duplicate IDs. Earlier rev1 struct ownership repair remains present and unchanged."
    },
    {
      "id": "exact-evidence",
      "text": "Replay matches expected tree. Attached precheck 10 and CR rev3 validation log both name this exact tree and run 38053090893. Four hosted lanes reported success, 8/8 mutants reported killed. CR validation log is 385 bytes, ends [exit 0], coverage_unit=exact_command_shard required=1 green=1 failed=0 missing=0 test_case_coverage=unknown. No truncation observed in this log. These hosted results are accepted attached evidence, not checks rerun by this panel. Raw lane commands, individual run IDs, mutant process exit codes, and exact test-case totals are not supplied in the summary; they remain unknown. No local wip-10 ref was available for independent commit-to-tree verification."
    },
    {
      "id": "coverage-bound",
      "text": "Surface sweep 7/7 (6 held on named reused attacks, 1 broken by pinned-source contract witness). This is not full AC coverage. AC5/8/9 remain partial: no dedicated live-child check-in removal/reinsert or exhausted/late-wake test, disable/stop concurrency test, non-default inherited-settings assertion, second-child-mid-turn test, or full resume_thread_with_history with a rendered SleepItem. The marker lifecycle fixture seeds markers manually. AC2 failure propagation is attacked via inspect_owned_child_ids, an internal helper, not a failing registry read through the complete goal service path; the ordinary-parent interrupt test supplies a public non-goal negative. AC6 reminder is disabled, so enabled-reminder stability is supported by source inspection only."
    },
    {
      "id": "release-entry",
      "text": "Candidate-wide release_native_wait search finds the public GoalRuntimeHandle method and one suite invocation only. No internal production service forwarding was found. Public handle release is exercised; broader trigger wiring stays an advisory carried from prior rounds."
    },
    {
      "id": "lifecycle-interleavings",
      "text": "Carried suspicion: asynchronous clear/status cleanup drops the state permit before manager lookup and removes by goal-owned prefix, potentially touching a later generation. Stop/disable can interleave with registration after inspection. No failing production reproduction was executed; request targeted old-cleanup/new-generation and paused-registration stop tests, not a new blocking finding."
    },
    {
      "id": "same-class-sweep",
      "text": "Pre-existing completion and ordinary message fragments also interpolate unrestricted paths/payloads and share the uncapped AgentMessage envelope. Neither fragment changed in rev2->rev3; record follow-up scope rather than blocking this leaf with a new pre-existing mechanism. Do not treat the body cap as evidence that the common envelope is bounded."
    },
    {
      "id": "delta-and-size",
      "text": "git diff --exit-code confirms every path other than the interruption fragment and its sibling tests is byte-identical to rev2. Rework has +68/-4 across these two files (verified with git diff --numstat). Full CR: 29 files, +2103/-16, including 1039-line new suite; exceeds 800-line nonmechanical guidance. Cargo dependency edge changes but MODULE.bazel.lock does not; no bazel-lock-update execution identified, drift unknown. No new include_str!/compile-data resource introduced."
    },
    {
      "id": "scope",
      "text": "No source/test/build/config edits, cargo/just/build/test execution, nested worktree, commits, branch changes or writes to TASK-260929-csyzcj. Only panel TASK-261010-3o3vdy receives outcome/checklist/notes/handoff mutations."
    }
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "attack": "Hosted public V2 spawn -> set_goal/idle -> completion -> captured model request; duplicate idle entry and one wake are asserted. ignore_native_pending mutant killed by this test. Production continue_if_idle inserts the lease before scheduler recheck.",
      "evidence": "TASK-260929-csyzcj_hosted-precheck-10.md; candidate core/tests/suite/goal_native_wait.rs::goal_wait_registers_marker_and_wakes_on_child_completion",
      "bound": "Only the named Running-child/ordinary completion sequence; no universal double-registration proof."
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "attack": "Hosted public ordinary-parent Op::Interrupt negative stays quiet without a marker. skip_failed_lookups mutant killed by owned_children_inspection_propagates_failed_lookups. Static trace: goal/service eligibility precedes typed inspection; lookup errors use ? and do not become empty.",
      "evidence": "TASK-260929-csyzcj_hosted-precheck-10.md; candidate core/tests/suite/goal_native_wait.rs::goal_wait_ordinary_parent_stays_quiet_on_child_interrupt",
      "bound": "Failed-read mutation is helper-level, not end-to-end goal service fault injection; unloaded/current-state helper controls are complementary."
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "attack": "Hosted public two-child latch pauses registration, confirms mail enqueue, then releases before captured mail wake. insert_after_mail_check killed by the bounded named latch assertion. Same-permit sharing prevents the previous self-deadlock.",
      "evidence": "TASK-260929-csyzcj_hosted-precheck-10.md; candidate core/tests/suite/goal_native_wait.rs::goal_wait_latch_closes_completion_before_registration",
      "bound": "This one completion/register interleaving; stop/disable concurrent interleavings remain requested."
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "attack": "Hosted public set_goal/idle and admitted turn preserve foreign clock-wait-1. insert_clobbers_one_foreign and unconditional_remove killed by this test plus small helper assertions. insert_if/remove_if operate under extension-data lock.",
      "evidence": "TASK-260929-csyzcj_hosted-precheck-10.md; candidate core/tests/suite/goal_native_wait.rs::goal_wait_preserves_foreign_sleep_across_register_and_turn_start",
      "bound": "Foreign ownership class asserted for named marker; generation races outside this foreign-id attack remain advisory."
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "attack": "Hosted GoalService clear/resume and public runtime release remove seeded goal markers; captured wake in registration/latch tests proves turn-start removal. ignore_native_pending killed; native_pending_exhausts_checkins_then_waits_without_deadline proves evaluator exhaustion policy.",
      "evidence": "TASK-260929-csyzcj_hosted-precheck-10.md; candidate core/tests/suite/goal_native_wait.rs::goal_wait_removed_on_clear_release_and_resume",
      "bound": "Seeded marker lifecycle is not full history resume; live-child check-in/reinsert and exhausted/late-wake, stop/disable tests absent."
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "attack": "Hosted public idle/register asserts 500ms no parent events, then captured wake body lacks goal-wait/history text. Reused exact-tree suite passes; lease storage has no UI/history/reminder scheduling calls.",
      "evidence": "TASK-260929-csyzcj_hosted-precheck-10.md; candidate core/tests/suite/goal_native_wait.rs::goal_wait_registers_marker_and_wakes_on_child_completion",
      "bound": "CurrentTimeReminder disabled in fixture. Enabled-reminder behavior not executed; no side-effect mutant was claimed."
    },
    {
      "row": "child state transitions",
      "result": "broken",
      "attack": "Hosted real Op::Interrupt yields one scoped queue-only INTERRUPTED wake without success, and ordinary-parent negative stays quiet. interrupted_notice_delivered_twice/interrupted_claims_success killed. New sender-path body mutant killed only by formatter unit test; the pinned-source full-item witness exits 1 on uncapped envelope.",
      "evidence": "TASK-260929-csyzcj_hosted-precheck-10.md; candidate core/tests/suite/goal_native_wait.rs::goal_wait_registered_parent_gets_single_interrupted_notice",
      "bound": "No live long-name boundary request. Whole envelope unbounded: repeated finding interrupted-fragment-unbounded-paths; state/settings subcases remain partial."
    }
  ],
  "free_hunt": [
    {
      "scope": "Bounded static hunt (approximately five minutes): complete-item envelope, sibling fragments, client serialization/history path, release callers, generation cleanup and build metadata.",
      "result": "One blocking repeated envelope mechanism already recorded in child-state row; no additional reproduced defect. Pre-existing sibling caps, lifecycle interleavings, release wiring and lock drift remain notes."
    }
  ]
}
```

## Observed static witness

Pinned reads all exited 0. Body controls held at path lengths 255, 256, 257, 2006, 80006. Body hard cap = 682 bytes. Long sender with ordinary recipient: body 417 bytes, author 80006 bytes, recipient 5 bytes, model-visible total 80428 bytes, four-byte coarse estimate 20107, wire analogue 80537 bytes. The complete-item assertion exited **1** with `complete interruption item remains unbounded via author/recipient; body cap alone does not establish a 10K-token item bound`. Byte growth and missing cap are established; actual tokenizer count and a live outbound long-name interruption were not measured.

To replay the source witness, save this script at `.temp/TASK-261010-3o3vdy-envelope-attack.py` and run the command above. It reads only pinned candidate blobs and reconstructs the straight-line formatter/envelope, not the runtime.

```python
"""Pinned-source static witness; does not run Rust or a model request."""
import json
import re
import subprocess

TREE = "9ccda9214ac5b9f0ddb5533b77418d0f2045d74b"
PATHS = {
    "fragment": "codex-rs/core/src/context/inter_agent_interrupted_message.rs",
    "protocol": "codex-rs/protocol/src/protocol.rs",
    "models": "codex-rs/protocol/src/models.rs",
    "history": "codex-rs/core/src/context_manager/history.rs",
    "client": "codex-rs/core/src/client_common.rs",
    "path": "codex-rs/protocol/src/agent_path.rs",
    "completion": "codex-rs/core/src/agent/control/completion.rs",
}
sources = {}
for key, path in PATHS.items():
    sources[key] = subprocess.check_output(["git", "show", f"{TREE}:{path}"], text=True)
    blob = subprocess.check_output(["git", "rev-parse", f"{TREE}:{path}"], text=True).strip()
    print(f"source {path} blob={blob} read_exit=0")

fragment = sources["fragment"]
cap = int(re.search(r"const INTERRUPTED_PATH_MAX_BYTES: usize = (\d+);", fragment)[1])
def rust_literal(name):
    return json.loads(re.search(rf'const {name}: &str = (".*");', fragment)[1])
prefix, middle, suffix, marker = map(rust_literal, ["BODY_PREFIX", "BODY_MIDDLE", "BODY_SUFFIX", "TRUNCATED_PATH_MARKER"])
assert "let task_name = truncate_path(&self.task_name);" in fragment
assert "let sender = truncate_path(&self.sender);" in fragment
assert 'format!("{BODY_PREFIX}{task_name}{BODY_MIDDLE}{sender}{BODY_SUFFIX}")' in fragment
assert "take_bytes_at_char_boundary(rendered, INTERRUPTED_PATH_MAX_BYTES)" in fragment
assert "author: self.author.to_string()," in sources["protocol"]
assert "recipient: self.recipient.to_string()," in sources["protocol"]
assert "text: self.content.clone()," in sources["protocol"]
assert "author: String," in sources["models"] and "recipient: String," in sources["models"]
assert "text_bytes(author).saturating_add(text_bytes(recipient))" in sources["history"]
assert "let mut input = self.input.clone();" in sources["client"]
assert "| ResponseItem::AgentMessage { .. }\n" in sources["client"]
assert "child_agent_path.clone(),\n            parent_agent_path," in sources["completion"]
validator = sources["path"].split("fn validate_agent_name", 1)[1].split("fn validate_absolute_path", 1)[0]
assert "ch.is_ascii_lowercase() || ch.is_ascii_digit() || ch == '_'" in validator
assert ".len()" not in validator

def notice(task, sender):
    # All witness paths are ASCII; this exactly transcribes the pinned body.
    def truncate(path):
        return path if len(path.encode()) <= cap else path[:cap] + marker
    return prefix + truncate(task) + middle + truncate(sender) + suffix

body_bound = len((prefix + middle + suffix).encode()) + 2 * (cap + len(marker.encode()))
assert body_bound == 682
for length in [255, 256, 257, 2006, 80006]:
    path = "/root/" + "a" * (length - 6)
    rendered = notice(path, path)
    assert len(rendered.encode()) <= body_bound
    if length <= cap:
        assert rendered == prefix + path + middle + path + suffix
print("body controls: 5/5 lengths held; both-path body bound=682")

recipient = "/root"
author = "/root/" + "a" * 80000
assert re.fullmatch(r"/root/[a-z0-9_]+", author)
body = notice(recipient, author)
item = {"type": "agent_message", "author": author, "recipient": recipient,
        "content": [{"type": "input_text", "text": body}]}
visible_bytes = len(author.encode()) + len(recipient.encode()) + len(body.encode())
print(json.dumps({"witness": "source-transcribed plaintext interruption item",
                  "body_bytes": len(body.encode()), "body_cap": body_bound,
                  "author_bytes": len(author), "recipient_bytes": len(recipient),
                  "model_visible_bytes": visible_bytes,
                  "four_byte_token_estimate": (visible_bytes + 3) // 4,
                  "serialized_bytes": len(json.dumps(item, ensure_ascii=False).encode())}))
assert visible_bytes <= 40000, "complete interruption item remains unbounded via author/recipient; body cap alone does not establish a 10K-token item bound"
```

## Logbook — 2026-10-10, panel-local

Rev3 repairs body text while preserving uncapped full paths in the outbound model-visible envelope. Both rev2 findings explicitly requested accounting for envelope fields; this is one repeated mechanism, not a new generalized prerequisite. The next rework should add the full-item boundary case and envelope-narrowing mutant to this implementation leaf. No producer-task write was made. The hosted summary demonstrates body regression coverage, with unknown raw mutant exit codes and partial lifecycle coverage kept explicit.
