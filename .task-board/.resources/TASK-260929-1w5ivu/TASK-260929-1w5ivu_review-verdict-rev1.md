# Merged review verdict — TASK-260929-1w5ivu CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261012-1jy4pd_panel-verdict.md` (changes_requested), `TASK-261012-36sw2s_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "F1",
      "row": "request agreement",
      "invariant": "At the first request of a later turn, waiting guidance must agree with that request's tools; the accepted post-completion mismatch is bounded to the same-turn follow-up.",
      "mechanism": "When the goal completes, GoalExtension::contribute_turn_context returns Vec::new(). The old unqualified developer fragment remains in append-only history with its positive clock.sleep sentence and no correction. In waiting_guidance_goal_stop_adds_no_new_fragment, requests[4] is the first request of turn 3 and lacks clock.sleep while retaining the turn-2 fragment. The test checks only its negative exec marker and tool absence, not sleep agreement. This is a turn-start mismatch beyond the accepted requests[3] same-turn window; waiting_guidance.rs:461 also describes next-turn staleness rather than the claimed resynchronization bound.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/waiting_guidance.rs:810",
          "command": "just test -p codex-core -E 'test(waiting_guidance_goal_stop_adds_no_new_fragment)'",
          "expected_failure": "After adding the request[4] SLEEP_MARKER/tool-presence equality described above, expected failure is left 1 versus right 0. Not run locally. The original test ran PASS in exact-tree hosted snapshot core job 114781620277; the strengthened expectation is established by the static append/gate trace, not by an observed red Rust execution.",
          "pinned_blobs": [
            "3685fd24cebba08c08ef741f928c58610983abf9:codex-rs/core/tests/suite/waiting_guidance.rs (candidate file) blob 0c1cef2261a01a36b00e36769e70c0005379aa62"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-1jy4pd"
      ]
    },
    {
      "id": "F2",
      "row": "incremental, no churn",
      "invariant": "Identical waiting capabilities on consecutive sampling requests add no new guidance item, including across turn boundaries; append an updated item only on a capability change.",
      "mechanism": "Every new turn changes TurnContextItem.turn_id, so Session::record_context_updates_and_set_reference_context_item calls build_turn_context_contribution_items again. GoalExtension has no last-emitted capability baseline and calls the always-one-fragment renderer on every active-goal contribution. Recording appends the developer item and history normalization does not deduplicate it. Consequently two unchanged active-goal turns retain two identical guidance fragments. The no-churn test covers only three samples within one turn, and the emitted-twice mutant duplicates one renderer call rather than disabling a comparison across turns.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/waiting_guidance.rs:756",
          "command": "just test -p codex-core -E 'test(waiting_guidance_unchanged_capabilities_stable_across_sampling_steps)'",
          "expected_failure": "Extend the existing dead-manager service-set fixture with a second user turn and one additional mocked response, preserving the active goal and all flags; keep an exact total of four requests and expect one guidance occurrence in the last request. Static expected failure is count 2 versus 1. This extension was not implemented or run in this read-only panel. The current three-request same-turn version ran PASS on the exact candidate tree.",
          "pinned_blobs": [
            "3685fd24cebba08c08ef741f928c58610983abf9:codex-rs/core/tests/suite/waiting_guidance.rs (candidate file) blob 0c1cef2261a01a36b00e36769e70c0005379aa62"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261012-1jy4pd"
      ]
    }
  ],
  "notes": [
    "[TASK-261012-1jy4pd] Reviewed only the six-file CR delta, not the already-landed P3-1 snapshot implementation. No mutation, acceptance, rejection, withdrawal, handoff, note, status or resource write was made on TASK-260929-1w5ivu.",
    "[TASK-261012-1jy4pd] Replay read-tree/apply/write-tree all exit 0; exact candidate match. Seven cached-index mutant applicability checks exit 0; the candidate index tree remains unchanged.",
    "[TASK-261012-1jy4pd] Hosted lint and snapshot small/core/app-server jobs are successful; aggregate workflow conclusion is failure because expected-red mutant jobs fail. Kill ratio is 7/7 according to the attached hosted report. Full core log independently confirms all ten new scenarios ran PASS on the candidate tree.",
    "[TASK-261012-1jy4pd] Literal byte-bound recomposition covers 80/80 shapes and gives 1724 bytes / 431 estimated tokens. This is a reviewer static calculation, not local Rust execution. Runtime/unit bound coverage is reused from hosted evidence.",
    "[TASK-261012-1jy4pd] BudgetLimited is intentionally in GoalActivity scope. Initially goal-less, paused, blocked, complete and UsageLimited states contribute no new fragment. Positive exec-notify and native-mail-wait request agreement remain unit-only coverage as disclosed; native-mail host-policy wiring is outside this delta.",
    "[TASK-261012-1jy4pd] The code-mode-only sleep-present agreement and the remote clock-off fixture's explicit reminder suppression are accepted disclosed semantics. The goal-less core paragraph and no-wait/end-turn paragraph remain out of scope/deferred.",
    "[TASK-261012-1jy4pd] Changed-line count is exactly 1353 insertions + 23 deletions = 1376. Production/template delta is 93 changed lines; tests/module registration account for 1283. No core production, dependency, schema or public API delta.",
    "[TASK-261012-1jy4pd] The two accepted same-turn windows are preserved. F1 is the additional turn-start mismatch after completion; F2 is unconditional repetition across unchanged turns. Both are static findings, with explicitly unexecuted strengthened-test requests.",
    "[TASK-261012-1jy4pd] free-hunt: {\"bounded_scope\": \"Four additional static attack families after the nine-row sweep; no build/test or product-code edits.\", \"attacks\": [{\"family\": \"history replacement and classification metadata\", \"result\": \"No hidden replacement or duplicate suppression: content_kind is annotation; PromptFragment converts to ordinary developer text and history appends. This corroborates F1/F2 rather than creating another finding.\"}, {\"family\": \"goal lifecycle and unknown reconciliation\", \"result\": \"Existing GoalActivityPublisher removes the marker on read failure, feature disable and teardown, and admits BudgetLimited consistently. No new gate bypass in this CR. Fresh request agreement for every inactive status is not independently executed here.\"}, {\"family\": \"native identity and Unicode bounds\", \"result\": \"Namespaced/default identities and Unicode-safe truncation reviewed; effective capped display is 128 characters plus an ellipsis. Individual fragment remains bounded. Claim agreement for a configured overlong native namespace has no public-entry execution in this review and is reported unknown, not a held runtime claim.\"}, {\"family\": \"public API and candidate/evidence provenance\", \"result\": \"No CLI/config/API/rollout shape change in the six-file delta. Replay and hosted checkout tree match exactly; all ten new core scenarios have explicit PASS records. No additional finding.\"}], \"additional_findings\": [], \"coverage\": \"9/9 surface rows attacked; 7 held, 2 broken, 0 not-attacked. Four bounded free-hunt families reviewed. New adversarial Rust assertions requested above remain unrun.\"}",
    "[TASK-261012-36sw2s] Remote-catalog sleep absence is determined by the reminder gate, not the catalog: spec_plan ModelDriven branch uses current_time_reminder.sleep_tool alone when the reminder is enabled (verified in base tree). Catalog load-bearing rests on /models x1 + merged-entry assert + P3-1 matrix. Disclosed in results; sentence<->snapshot agreement is what the leaf owns.",
    "[TASK-261012-36sw2s] BudgetLimited gate scope has no dedicated suite test (disclosed); marker publish for Active|BudgetLimited only verified in base ext/goal/src/activity.rs.",
    "[TASK-261012-36sw2s] Positive exec-notify and native-mail-wait sentences are unit-covered only (disclosed); no suite flow installs the admission marker or capable host.",
    "[TASK-261012-36sw2s] No-wait/end-turn paragraph deliberately not emitted; absence pinned by unit test (plan defers to P4b).",
    "[TASK-261012-36sw2s] Size 1376 = 1353 insertions + 23 deletions verified from tree diff; production ~90 lines, rest mandated tests (disclosed vs 600 target).",
    "[TASK-261012-36sw2s] Request counts per scenario 2/4/1/1/2/1/1/3/5/5 = 25 responses + 1 /models verified against test bodies; sizes 1724B/431t maximal, 1234B/309t realistic, 133B/34t minimal independently recomputed and matching.",
    "[TASK-261012-36sw2s] free-hunt: Swept beyond the rows: searched all 10 suite tests for a third undisclosed agreement window (none; every mid-turn discrepancy traces to the two disclosed turn-boundary mechanisms); checked native-name rendering branches (namespaced/dotted, default-namespace/bare) and cap boundary conditions against tests; confirmed ContentItemKind uses the existing PromptFragment path with no new item type; confirmed killer-test names match the hosted filter; recomputed all size/token/request measurements; cross-checked all four tool descriptions against fragment sentences; verified cited base-tree mechanism references (turn recording, sleep OR-grant, hiding rules, deferred discovery, P3-1 pins). No additional findings."
  ],
  "surface_results": [
    {
      "row": "contract text",
      "result": "held",
      "reason": "Static byte comparison with final-plan §9 confirms only line 24 changes. Both update_plan variants derive from the same template; continuation_prompt_carries_section_nine_verified_wait_contract checks both renderings. Hosted old-text mutant is killed by that test.",
      "reported_by": "TASK-261012-1jy4pd"
    },
    {
      "row": "sentence selection",
      "result": "held",
      "reason": "Six literal texts match §9; Rust branches select exactly one exec sentence and optional sleep/stdin/native/mail sentences in fixed order. Native identity is dotted for non-default namespaces and bare for default namespace; deferred no-wait text is absent. Hosted per-flag/fixed-order tests and always-positive, unconditional-sleep and hardcoded-name mutants cover selection.",
      "reported_by": "TASK-261012-1jy4pd"
    },
    {
      "row": "scope and gating",
      "result": "held",
      "reason": "New contribution is gated exclusively on GoalActivity presence. Existing activity publisher admits Active/BudgetLimited, removes marker for other states/read failure; the non-goal public-entry test and non-goal mutant execute the new production gate. No goal-less core paragraph or alternate injection path was added. Historical retention is evaluated separately under request agreement, F1. Dedicated BudgetLimited/inactive-state request scenarios remain a disclosed coverage bound.",
      "reported_by": "TASK-261012-1jy4pd"
    },
    {
      "row": "bounded",
      "result": "held",
      "reason": "Existing PromptFragment path only. Cap limits the variable display name to 128 Unicode characters plus ellipsis; exact-limit, over-limit and multibyte cases are tested. All 16 Boolean combinations crossed with five name shapes are covered (80/80); maximum 1724 bytes / 431 estimated tokens is within 3072/1000. Hosted cap-removal mutant is killed.",
      "reported_by": "TASK-261012-1jy4pd"
    },
    {
      "row": "incremental, no churn",
      "result": "broken",
      "reason": "F2: new turn_id re-invokes the contributor, which unconditionally emits unchanged guidance again; same-turn no-churn coverage misses this boundary. Append-only history is preserved. The accepted mid-turn windows are not findings; F1 additionally shows resynchronization after completion is not achieved at the next turn.",
      "reported_by": "TASK-261012-1jy4pd"
    },
    {
      "row": "request agreement",
      "result": "broken",
      "reason": "F1: requests[4] in the hosted goal-stop scenario is a later turn-start request without clock.sleep but retains the uncorrected sleep sentence. The strengthened iff assertion is absent. Other named fresh-turn scenarios have exact request counts and hosted execution; code-mode/remote/excluded/headless/discovery semantics were checked against source rather than the obsolete precheck-1 expectations.",
      "reported_by": "TASK-261012-1jy4pd"
    },
    {
      "row": "tool descriptions",
      "result": "held",
      "reason": "Checked unchanged shell_spec.rs:75-136,147-180 (receipt acknowledgment, write_stdin waits), sleep.rs:39-77 (input interruption and direct-only exposure), and multi_agents_spec.rs:268-292,845-887 (V1 targets/V2 mailbox). None contradict the selected text; V2 lacks targets and the fragment explicitly qualifies multiple identifiers with 'where that tool supports them'. No description churn.",
      "reported_by": "TASK-261012-1jy4pd"
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "reason": "All seven source-resource mutant patches apply against the replayed candidate (7/7 checks exit 0). Hosted report supplies filter-selected named killers and 7/7 kills. Exact request counts sum to 25 responses plus one /models request. Size measurements independently recomputed. This satisfies the enumerated mutants; their coverage does not extend to the new F1/F2 strengthened assertions.",
      "reported_by": "TASK-261012-1jy4pd"
    },
    {
      "row": "placement and size",
      "result": "held",
      "reason": "Only renderer/gate/template production changes in ext/goal, 93 changed lines. Core changes are integration tests plus module registration. Total 1376 changed lines is the expressly disclosed test-driven overrun; no production expansion into core, dependencies, generated schemas or external integration surfaces.",
      "reported_by": "TASK-261012-1jy4pd"
    }
  ],
  "free_hunt": []
}
```
