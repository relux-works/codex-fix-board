# Panel B verdict — CR-TASK-260929-1w5ivu-1 rev1 (non-recording review)

Verdict: accept

## Replay tree check

Base `67789e1ee29e766e446c7f33feb61561d51f94db` + patch
`TASK-260929-1w5ivu_change-request_rev1.patch` through a temporary index
produces tree `3685fd24cebba08c08ef741f928c58610983abf9`, which matches the
expected candidate tree exactly. Delta is 6 files, all in `ext/goal` or
`core/tests/suite`; no `codex-core` production code.

## Commands run (with exit codes)

| Command | Exit |
|---|---|
| `task-board m 'set_status(TASK-261012-36sw2s, status=analysis)'` | 0 |
| `GIT_INDEX_FILE=$IDX git read-tree 67789e1e…` | 0 |
| `task-board resource get TASK-260929-1w5ivu TASK-260929-1w5ivu_change-request_rev1.patch` | 0 |
| `GIT_INDEX_FILE=$IDX git apply --cached <patch>` | 0 |
| `GIT_INDEX_FILE=$IDX git write-tree` → `3685fd24…` (match) | 0 |
| `git archive 3685fd24… <6 paths>` extract | 0 |
| `git apply --cached --check` × 7 mutant patches vs candidate tree | 0 each |
| byte-exact verification scripts (template §9, 6 sentences, sizes) | 0 |
| `cargo` / `just` builds or tests | not run (forbidden; hosted evidence cited) |

No `accept_cr`, `reject_cr`, `set_status`, or `handoff` was run on
`TASK-260929-1w5ivu`, and nothing was written there. All reads on that task
were `q` queries and `resource get`.

## Review basis

Static attack on the candidate tree plus hosted execution evidence accepted
from the board: precheck 2 run 38239371527 on exactly tree `3685fd24`, all
four lanes green, 7/7 mutants killed with named killing tests
(`TASK-260929-1w5ivu_hosted-precheck-2.md`), and the CR validation log
(mini-hosted-gate exit 0). Every surface-table row was attacked once; then a
bounded free hunt (third-window search, cap/name edge cases, description
cross-check, measurement recompute, mechanism-reference verification).
Result: no findings. The two mid-turn windows are pinned and disclosed per
the recorded orchestrator decision (turn-boundary contract); no third window,
no turn-start claim mismatch, and no misdescribed bound was found.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Remote-catalog sleep absence is determined by the reminder gate, not the catalog: spec_plan ModelDriven branch uses current_time_reminder.sleep_tool alone when the reminder is enabled (verified in base tree). Catalog load-bearing rests on /models x1 + merged-entry assert + P3-1 matrix. Disclosed in results; sentence<->snapshot agreement is what the leaf owns.",
    "BudgetLimited gate scope has no dedicated suite test (disclosed); marker publish for Active|BudgetLimited only verified in base ext/goal/src/activity.rs.",
    "Positive exec-notify and native-mail-wait sentences are unit-covered only (disclosed); no suite flow installs the admission marker or capable host.",
    "No-wait/end-turn paragraph deliberately not emitted; absence pinned by unit test (plan defers to P4b).",
    "Size 1376 = 1353 insertions + 23 deletions verified from tree diff; production ~90 lines, rest mandated tests (disclosed vs 600 target).",
    "Request counts per scenario 2/4/1/1/2/1/1/3/5/5 = 25 responses + 1 /models verified against test bodies; sizes 1724B/431t maximal, 1234B/309t realistic, 133B/34t minimal independently recomputed and matching."
  ],
  "surface_results": [
    {
      "row": "contract text",
      "result": "held",
      "evidence": "Tree diff: only continuation.md line 24 of 56 changed; line 24 == '- ' + plan §9 paragraph byte-exact (script-verified). Single include_str feeds both template variants; unit test renders both, asserts the full exact bullet and absence of two removed-text substrings. Old-text mutant killed by continuation test on hosted run 38239371527."
    },
    {
      "row": "sentence selection",
      "result": "held",
      "evidence": "All 6 renderer constants byte-exact vs §9 table (script-verified). Fixed code order exec/sleep/stdin/native/mail; exact-join test; per-flag iff test incl. custom-namespace actual name and plain bare name; no-wait absence pinned. Native suffix '(Tool name: X.)' implements plan's 'render actual tool name alongside'. Exec-ignores-flag, sleep-unconditional, hardcoded-name mutants killed by named tests on hosted run."
    },
    {
      "row": "scope and gating",
      "result": "held",
      "evidence": "Gate is GoalActivity-presence in goal's ContextContributor; base publisher emits the marker only for Active|BudgetLimited and removes it otherwise (activity.rs). Non-goal suite test + pre-goal requests in 4 tests pin absence; non-goal mutant killed by non-goal test. No core production changes (core delta is tests only); no core goal-less paragraph, out of scope per recorded orchestrator decision and stated in results."
    },
    {
      "row": "bounded",
      "result": "held",
      "evidence": "80-combination test (16 flag bits x 5 native names incl. overlong ASCII and wide); inline div_ceil(4) matches repo estimator codex_utils_string::approx_tokens_from_byte_count (APPROX_BYTES_PER_TOKEN=4, verified). Cap test covers truncation, multibyte boundary, at-cap untouched. Maximal 1724B/431t recomputed independently. Existing PromptFragment::developer_capability path only (present in base). Cap-removed mutant killed."
    },
    {
      "row": "incremental, no churn",
      "result": "held",
      "evidence": "No-churn: 3 in-turn requests x occurrences==1; emitted-twice mutant killed by it. Post-create 0->1, discovery next-turn update, goal-stop frozen count + intact history + turn-3 update recorded. Turn-boundary mechanism verified in base (first_step_context recorded at turn start; per-request router rebuild; on_tool_finish reconcile). Both mid-turn windows pinned in tool_created_goal_reacts_at_next_turn as disclosed bounds; free hunt found no third window (goal-stop req[4], discovery req[1], excluded req[1] are the same two mechanisms)."
    },
    {
      "row": "request agreement",
      "result": "held",
      "evidence": "10 suite tests each assert exact request counts (sum 25+1). Every turn-start request asserted to agree, incl. full agreement on tool-created req[2]. Sleep/stdin/native covered in both directions with tool_by_name/schema asserts; exec negative in 6 tests. Sleep-unconditional mutant killed by remote-catalog test (hosted). Only disagreements are the two disclosed mid-turn windows; no turn-start mismatch found."
    },
    {
      "row": "tool descriptions",
      "result": "held",
      "evidence": "Read all four descriptions in base tree: exec_command (+capable-host wake suffix), write_stdin (+yield semantics), clock.sleep (input-interruptible, DirectModelOnly), wait_agent v1 (agents/children scope). Each is consistent with its fragment sentence; none contradicts. Nothing changed, correctly no rewrite."
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "evidence": "7/7 mutant patches verified git-apply---check-clean against the candidate tree by this panel. Hosted run 38239371527 on exact tree 3685fd24: 4/4 lanes green, 7/7 killed, 0 survivors, each with named killing tests matching test(waiting)|test(guidance)|test(continuation)|test(goal). Per-scenario request counts and fragment sizes reported and independently reproduced."
    },
    {
      "row": "placement and size",
      "result": "held",
      "evidence": "Production in ext/goal only (steering.rs renderer+cap, extension.rs gate, template line 24); no codex-core production; tests in ext/goal/tests + core/tests/suite (+1 mod line). No renderer duplication. 1376 vs 600 target verified and disclosed as mandated test coverage."
    }
  ],
  "free_hunt": "Swept beyond the rows: searched all 10 suite tests for a third undisclosed agreement window (none; every mid-turn discrepancy traces to the two disclosed turn-boundary mechanisms); checked native-name rendering branches (namespaced/dotted, default-namespace/bare) and cap boundary conditions against tests; confirmed ContentItemKind uses the existing PromptFragment path with no new item type; confirmed killer-test names match the hosted filter; recomputed all size/token/request measurements; cross-checked all four tool descriptions against fragment sentences; verified cited base-tree mechanism references (turn recording, sleep OR-grant, hiding rules, deferred discovery, P3-1 pins). No additional findings."
}
```
