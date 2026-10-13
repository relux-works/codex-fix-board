# Merged review verdict — TASK-260929-1w5ivu CR revision 2 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261012-x39dh9_panel-verdict.md` (changes_requested), `TASK-261012-b3ql0q_panel-verdict.md` (accept), `TASK-261012-1ubigw_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "A2-F1",
      "row": "placement and size",
      "invariant": "New integration tests must compile under the repository Bazel targets as well as Cargo; all #[path] source inputs must be declared.",
      "mechanism": "codex-rs/ext/goal/tests/waiting_world_state.rs:11 imports ../src/waiting_world_state.rs. ext/goal/BUILD.bazel:9-13 supplies accounting.rs, activity.rs and steering.rs only. defs.bzl:606-613 creates goal-waiting_world_state-test with srcs=[test] and compile_data=tests/** + integration_compile_data_extra. The new source file is neither. The goal library compiling that file does not declare it as a source input to this separate integration-test compile action. A hermetic Bazel action therefore cannot resolve the path import. Hosted relux-ci small uses just test/Cargo, so its green does not cover this regression. Add src/waiting_world_state.rs to integration_compile_data_extra.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/waiting_world_state.rs:11",
          "command": "python3 .temp/TASK-261012-x39dh9-bazel-input-audit.py",
          "expected_failure": "Observed exit 1: src/waiting_world_state.rs absent from integration_compile_data_extra (static input audit; source included below).",
          "pinned_blobs": [
            "786339645058198ba030dffbba8ed1cfbf1e36a9:codex-rs/ext/goal/tests/waiting_world_state.rs (candidate file) blob 75550cef1fa8784564678e9b7bd24dad06379542"
          ]
        },
        {
          "test_file": "codex-rs/ext/goal/tests/waiting_world_state.rs",
          "command": "bazel test //codex-rs/ext/goal:goal-waiting_world_state-test",
          "expected_failure": "Requested hosted attack, NOT RUN here because builds are prohibited: rustc cannot read tests/../src/waiting_world_state.rs inside the hermetic compile action. Run after declaring the input to verify the repair.",
          "pinned_blobs": [
            "786339645058198ba030dffbba8ed1cfbf1e36a9:codex-rs/ext/goal/tests/waiting_world_state.rs (candidate file) blob 75550cef1fa8784564678e9b7bd24dad06379542"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-x39dh9"
      ]
    },
    {
      "id": "A2-N1",
      "row": "mutants and measurement",
      "invariant": "Reported maximal sizes must describe the entire tested input class, not just the ASCII fixture.",
      "mechanism": "results.md claims a worst-case serialized snapshot <=512 B, but waiting_world_state.rs:65-75 stores a name capped by characters and the snapshot unit at tests/waiting_world_state.rs:253 uses ASCII only. The renderer explicitly supports wide names. A 128-character four-byte name plus ellipsis produces a 602 B snapshot with all Boolean flags true. Across the static model including escaped controls, the largest snapshot is 862 B (all flags false). The actual markers are 47 bytes and ContextualUserFragment::render concatenates them directly: maximal body 1724 B yields 1771 B / 443 estimated tokens, not the reported 1769 B. These are evidence inaccuracies, not an unbounded item or a violation of the 3072 B / 1000-token fragment requirement. Configured production native namespaces are ASCII and <=64 chars (core/config/mod.rs:3150-3198), so the wide-name counterexample concerns the renderer/test input class, not an established production tool name. Correct the report and broaden the snapshot measurement fixture if retaining a universal bound.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/tests/waiting_world_state.rs:250",
          "command": "python3 .temp/TASK-261012-x39dh9-measurement-audit.py",
          "expected_failure": "Observed exit 1: 602 >512, disproving the universal measurement claim; static serialization counterexample, not an executed Rust test.",
          "pinned_blobs": [
            "786339645058198ba030dffbba8ed1cfbf1e36a9:codex-rs/ext/goal/tests/waiting_world_state.rs (candidate file) blob 75550cef1fa8784564678e9b7bd24dad06379542"
          ]
        },
        {
          "test_file": "codex-rs/context-fragments/src/fragment.rs:91",
          "command": "python3 .temp/TASK-261012-x39dh9-static-audit.py",
          "expected_failure": "No expected failure: observed exit 0 and independently measured max body=1724, wire=1771, snapshot=862; actual fragment bound still holds.",
          "pinned_blobs": [
            "786339645058198ba030dffbba8ed1cfbf1e36a9:codex-rs/context-fragments/src/fragment.rs (candidate file) blob a81e6e395431e1e494f85cc9641af21bcda51ace"
          ]
        }
      ],
      "severity": "note",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-x39dh9"
      ]
    }
  ],
  "notes": [
    "[TASK-261012-x39dh9] Review of CR-TASK-260929-1w5ivu-2 only. No writes or lifecycle operations on TASK-260929-1w5ivu; all board mutations target TASK-261012-x39dh9.",
    "[TASK-261012-x39dh9] Replay matches 786339645058198ba030dffbba8ed1cfbf1e36a9. No cargo, just, Bazel build/test, commit, branch operation or nested worktree used. Temporary index remained exact after eight apply --check attacks.",
    "[TASK-261012-x39dh9] Hosted evidence accepted: TASK-260929-1w5ivu_hosted-precheck-5.md run38265238386 (lint/small/core/app-server success;8/8 mutants killed); CR rev2 validation log contains mini-hosted-gate exit0, coverage_unit=exact_command_shard required1/green1 and test_case_coverage=unknown. Hosted raw lane command exit codes are not supplied; success is not presented as an observed local exit0.",
    "[TASK-261012-x39dh9] Measured coverage:9/9 surface rows have one result;8/8 supplied mutants apply;8/8 hosted kills;11 request scenarios (28 responses +1 models). No claim of9/9 mutated surface coverage or executed goal-compaction/positive-host/mail/BudgetLimited scenarios.",
    "[TASK-261012-x39dh9] Source-derived Python models are static attacks only. They do not execute Rust or replace public-entry testing. Expected-red audit exit1 values are recorded as failures, not passing gates.",
    "[TASK-261012-x39dh9] free-hunt: {\"scope\": \"Bounded extra hunt across four cases: Bazel path-input reachability; merged developer-content recognition; compaction/resume baseline loss; Unicode/JSON-escape size accounting.\", \"result\": \"Bazel compile-input regression A2-F1 and measurement note A2-N1. No additional source-backed regression found. Partial/client-forged marker text is not an attestation: matcher is a presence heuristic against a persisted snapshot; no supported compaction path retaining only an obsolete harness fragment was established. Do not infer a production bypass from synthetic marker matching.\"}",
    "[TASK-261012-b3ql0q] Results prose reports 45-byte section markers / 1769-byte maximal wire; recomputed markers are 47 bytes (<goal_waiting_guidance> 23 + </goal_waiting_guidance> 24), so maximal wire is 1771 bytes, 443 tokens unchanged. Bound holds with margin either way; the retraction-wire figure (135 = 88+47) already uses 47. Reporting slip only, no invariant affected.",
    "[TASK-261012-b3ql0q] Remote-catalog sleep absence is determined by the reminder gate (sleep_tool:false), not the catalog (disclosed in results and test comment, as rev1); catalog load-bearing rests on /models x1 + merged-entry assert + P3-1 matrix. Sentence<->snapshot agreement is what the leaf owns.",
    "[TASK-261012-b3ql0q] BudgetLimited gate scope has no dedicated suite test (disclosed since rev1); marker publish for Active|BudgetLimited only verified in candidate ext/goal/src/activity.rs.",
    "[TASK-261012-b3ql0q] Positive exec-notify and native-mail-wait sentences are unit-covered only (disclosed); no suite flow installs the admission marker or capable host. The always-negative direction has no mutant (AC8 enumerates always-positive only); the positive direction is pinned by unit selects_sentences_per_flag, executed in the hosted small lane.",
    "[TASK-261012-b3ql0q] No-wait/end-turn paragraph deliberately not emitted; absence pinned by unit test (plan defers to P4b).",
    "[TASK-261012-b3ql0q] Reactivation (active render against Known(false)) is unit-pinned only; it shares the identical Known arm comparison as the suite-covered discovery change, and AC5 does not list reactivation. Same disclosure class as the other unit-only arms.",
    "[TASK-261012-b3ql0q] Compaction retained-matcher behavior is unit-level (disclosed); this panel additionally traced every core path statically (replacement history drops developer fragments; kept/replaced/stale baselines all converge; resume resets at Compaction).",
    "[TASK-261012-b3ql0q] Size 1950 = 1921 insertions + 29 deletions verified from tree diff; production 254 (242+12), tests 1696, matching the disclosed split vs the 600 target.",
    "[TASK-261012-b3ql0q] Request counts per scenario 2/4/1/1+models/2/1/1/3/3/5/5 = 28 responses + 1 /models verified against test bodies; sizes 1724B/431t maximal, 1234B/309t realistic, 133B/34t minimal, 88B/22t retraction independently recomputed and matching.",
    "[TASK-261012-b3ql0q] free-hunt: Swept beyond the rows: (1) round-trip mismatch class per orchestrator note — enumerated every snapshot shape (active object with/without name, inactive false) against core strip/serialize/merge-patch/resume paths, no second divergence found; (2) matcher misfire — real render format is exactly {start}{body}{end} (ContextualUserFragment::render), identical to the unit reconstruction; assistant/user echo and tool outputs cannot match (role + Message-variant checks); (3) compaction convergence — replacement history carries user messages + summary only, so all baseline cases (kept/replaced/stale) converge to exactly-once render or silence, mid-turn race fails visible with one retraction; (4) double-emission/dead-code sweep — no turn-context path left, single section id, PromptFragment only as renderer vehicle; (5) core-leakage sweep — all 22 WorldStateContributionInput sites (1 prod + 21 skills tests) covered, 13-file diff has no other core/app-server/P4b touch; (6) measurement recompute — found a 2-byte wire-marker arithmetic slip in results prose (notes), bound unaffected. No additional findings.",
    "[TASK-261012-1ubigw] Previous merged F1 fixed: ext/goal/src/waiting_world_state.rs:106-129 emits one static active-to-inactive correction. core/tests/suite/waiting_guidance.rs:862-929 verifies first post-stop request and later-turn silence; hosted no-retraction mutant fails with exit 100.",
    "[TASK-261012-1ubigw] Previous merged F2 fixed: waiting_world_state.rs:80-99 compares every step snapshot; extension.rs:654-674 owns only the World State path. waiting_guidance.rs:812-859 verifies three unchanged turns. Hosted always-renders mutant fails with exit 100.",
    "[TASK-261012-1ubigw] Measurement correction, non-blocking: maximal body 1724B, markers 47B, maximal wire 1771B/443 estimated tokens (producer reports 1769B). Retraction wire 135B/34t is correct. Bound remains below 3072B/1000t.",
    "[TASK-261012-1ubigw] Snapshot measurement correction, non-blocking: <=512B test uses ASCII. Unicode worst case is 606B; escaped-control upper shape is 862B. Snapshot is still hard-bounded by the 128-character name cap plus ellipsis and fixed schema; no universal 512B AC exists.",
    "[TASK-261012-1ubigw] Coverage bounds: positive exec_notify and native_mail_wait production claims remain unit-only; BudgetLimited has no dedicated request scenario. Waiting-specific compaction has unit/static coverage rather than its own public-entry integration run, expressly permitted by the rework brief. Do not infer those runtime claims from 8/8 mutant kills.",
    "[TASK-261012-1ubigw] Workflow head is not snapshot checkout. Independently verified snapshot 225718e8 tree 78633964. Snapshot lanes pass; aggregate workflow fails because expected-red mutants fail. All eight mutant patches apply to the candidate; two new regression kills independently verified in raw logs.",
    "[TASK-261012-1ubigw] Goal-less core paragraph remains explicitly out of scope. The no-wait/end-turn paragraph remains deferred. AC3 permits one transition retraction; AC9 permits only the one core production pass-through. No reviewed-task write occurred.",
    "[TASK-261012-1ubigw] Exact request count total is 28 responses + 1 models across 11 scenarios. Diff size is 1950 changed lines, 254 production/template and 1696 tests; overrun disclosed and unchanged by review. No dependency/config/schema/CLI/app-server wire change. Extension-api struct construction sites have mechanical field updates.",
    "[TASK-261012-1ubigw] free-hunt: {\"bounded_scope\": \"Six additional static attack families after the nine-row sweep; no local build/test or product-code mutation.\", \"attacks\": [{\"family\": \"snapshot persistence equivalence\", \"result\": \"Audited null stripping and RFC7386 false/object/name-removal transitions in core/context/world_state/mod.rs. New snapshot uses only Booleans and a bounded optional string; 81/81 modeled shapes and 6561/6561 transitions stable. Real hosted no-churn tests exercise core persistence. No additional defect.\"}, {\"family\": \"retained matcher narrowing and retraction identity\", \"result\": \"Wrong role, missing markers, bare markers and marker-sharing retraction rejected; either exec variant accepted. Unknown unreachable without legacy matcher and fails visible. Matcher attests active-section presence rather than exact body identity: arbitrary replacement preserving an older active fragment with a newer baseline is not independently executed; no reachable compaction path doing that was established.\"}, {\"family\": \"compaction replacement and baseline retention\", \"result\": \"compact.rs:87-106,367-383 and session/mod.rs:4173-4195 install current full initial context plus matching baseline for mid-turn compaction, or clear goal baseline for DoNotInject. Goal registers no retain_world_state_after_compaction override. New active context rebuilds, inactive history no longer contains the old section. Unit/static bound accepted per brief; no full waiting-specific compaction suite run claimed.\"}, {\"family\": \"Unicode and serialized bounds\", \"result\": \"Character-safe 128 cap plus ellipsis survives Unicode/control-character JSON escaping and round trips. Source-derived corrected maximal wire 1771B/443t; snapshot upper shape 862B. Reported 1769B and universal512B measurements need editorial correction, with no AC bound violation.\"}, {\"family\": \"resuming rollouts and external surfaces\", \"result\": \"Stable section id and false/object snapshots use existing rollout World State protocol; no new protocol variant or history rewrite. Old rev1 unmarked turn fragments lack a legacy matcher, but rejected unlanded rev1 is not a supported persisted rollout migration in this delta. No CLI/config/app-server wire change found.\"}, {\"family\": \"P4b and gate provenance\", \"result\": \"Only fixture continuation_pacing adapts to base P4b. No pacing implementation changed; hosted snapshot core/app-server lanes green. Checked snapshot commit/tree independently rather than workflow head; no evidence substitution.\"}], \"additional_findings\": [], \"coverage\": \"9/9 surface rows attacked: 9 held, 0 broken, 0 not-attacked. 6/6 bounded free-hunt families inspected. Runtime unknowns and non-blocking measurement corrections stated explicitly.\"}"
  ],
  "surface_results": [
    {
      "row": "contract text",
      "result": "held",
      "reason": "Source-derived static audit confirms only template line 24 changes, byte-exact final-plan §9 paragraph and all six sentence constants. With/without update_plan derive from one template. Hosted continuation_prompt_carries_section_nine_verified_wait_contract kills waiting_old_verified_wait_text_restored.",
      "reported_by": "TASK-261012-x39dh9"
    },
    {
      "row": "sentence selection",
      "result": "held",
      "reason": "Static Rust branches select exactly one exec sentence, then optional sleep/stdin/native/mail in fixed order; actual names use dotted/default-name rendering and a 128-character cap plus ellipsis. Deferred no-wait paragraph absent. Hosted flag/fixed-order tests and exec-always-positive, sleep-unconditional, native-name-hardcoded mutants kill these attacks. Positive exec/mail paths remain unit-only.",
      "reported_by": "TASK-261012-x39dh9"
    },
    {
      "row": "scope and gating",
      "result": "held",
      "reason": "GoalExtension::contribute_world_state gates on GoalActivity. Existing activity.rs publisher admits Active/BudgetLimited and removes the marker for paused/blocked/complete/UsageLimited/read error. Never-active threads add no section; ever-active threads emit the authorized one transition retraction. Hosted non-goal public-entry test plus non-goal mutant cover the negative gate. Dedicated BudgetLimited and every inactive-status request case are not claimed executed.",
      "reported_by": "TASK-261012-x39dh9"
    },
    {
      "row": "bounded",
      "result": "held",
      "reason": "Four Boolean flags plus optional capped string have no unbounded member; no nulls exist in either active snapshot or inactive false. Static audit crosses 128 active inputs and inactive false, including wide and escaped names; wire <=1771 B /443 estimated tokens. Hosted renderer test covers 80/80 combinations; cap mutant killed. Static retraction is 88 B /135 B wire. Existing WorldStateContextFragment in core/context owns the envelope and ContextualUserFragment implementation. The inaccurate <=512 snapshot measurement is A2-N1; snapshot remains hard-bounded.",
      "reported_by": "TASK-261012-x39dh9"
    },
    {
      "row": "incremental, no churn",
      "result": "held",
      "reason": "Source trace: turn.rs:509 records per-step World State before input assembly, extension gate uses persisted previous entry, snapshot omits absent native_wait, and active Known(equal) renders None. Static source-derived model verifies 16641/16641 RFC7386 transitions restore current shape, including name present->absent and object<->false. No remaining persistence normalization mismatch found. Hosted same-step and cross-turn stability, discovery one-update and stop retraction tests kill always_renders/no_retraction mutants. Merged developer messages preserve separate InputText chunks (updates.rs), so markers still match. Active matcher rejects retraction/wrong role/bare markers; inactive section has no retained matcher and does not repeat correction. Core compaction removes harness developer guidance and either reinjects full context or renders missing active guidance; no legacy matcher makes Unknown unreachable. End-to-end goal compaction is not executed; section-specific units plus static generic-path trace only.",
      "reported_by": "TASK-261012-x39dh9"
    },
    {
      "row": "request agreement",
      "result": "held",
      "reason": "Accepted exact-tree hosted attacks execute 11 real /responses scenarios with 28 responses +1 /models and exact per-scenario counts. Tool-created follow-up receives new guidance immediately; first post-stop request receives one retraction and next turn adds none. Discovery receives exactly one updated fragment. Static production trace uses same StepContext router/capabilities in section and request; no earlier turn-boundary exception retained. Code-mode sleep remains direct (SleepHandler DirectModelOnly); nested stdin omitted. Remote clock suppression also depends on reminder-off as disclosed. Positive exec/mail and BudgetLimited public-entry coverage remain explicit limits.",
      "reported_by": "TASK-261012-x39dh9"
    },
    {
      "row": "tool descriptions",
      "result": "held",
      "reason": "Read shell_spec.rs:25-31,75-81,147-180; sleep.rs:39-89; multi_agents_spec.rs:268-292,849-887. Exec requires acknowledged receipt; empty stdin can wait up to300000 ms; sleep is interruptible and direct-only; V1 supports multiple targets while V2 mailbox wait has no targets, matching the sentence qualification where supported. No contradiction or unnecessary description edit found.",
      "reported_by": "TASK-261012-x39dh9"
    },
    {
      "row": "mutants and measurement",
      "result": "broken",
      "reason": "All eight patches apply to exact replay index (8/8 exit0); hosted precheck5 names filter-selected behavioral killers and reports8/8 killed. These are accepted hosted results, not independently rerun tests. Request counts agree with the11 scenarios. A2-N1 disproves reported universal <=512 B snapshot and corrects wire byte count; it is a nonblocking evidence note, while fragment bounds still hold.",
      "reported_by": "TASK-261012-x39dh9"
    },
    {
      "row": "placement and size",
      "result": "broken",
      "reason": "A2-F1: new #[path] test source missing from Bazel integration compile inputs. Otherwise only core production delta is authorized one-line snapshot pass-through; extension-api adds field, ext/goal owns renderer/gate/140-line section, old turn-context emission removed. Exact diff is1950 changed lines (254 production/1696 tests), disclosed test-size overrun. No dependency/config/schema/API/tool-description delta found.",
      "reported_by": "TASK-261012-x39dh9"
    }
  ],
  "free_hunt": []
}
```
