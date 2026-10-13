# R141 panel A — waiting-guidance fragment, revision 1

changes_requested

Non-recording review of CR-TASK-260929-1w5ivu-1, restricted to its delta against
`67789e1ee29e766e446c7f33feb61561d51f94db`. Replay through a temporary index
produced exactly `3685fd24cebba08c08ef741f928c58610983abf9`. The same tree was
printed again after all seven read-only mutant applicability checks.

Two regressions need review: guidance survives completion into a later
turn-start request without correcting its sleep claim, and identical
guidance is appended again on each new active-goal turn. The accepted
mid-turn creation and completion windows are not findings. F1 concerns the
next turn after that completion window; F2 concerns unchanged capabilities
across turns, which the same-turn no-churn test does not exercise.

## Predecessor commands and observed exit codes

All replay and validation commands below ran as standalone processes, without
`tee` or status-hiding pipes. `IDX` denotes the exact environment assignment
`GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay.idx"` preceding each Git
index command; the ordinary worktree index was not changed.

| Command | Exit | Observation |
|---|---:|---|
| `task-board m 'set_status(TASK-261012-1jy4pd, status=analysis)'` | 0 | Panel task lifecycle started |
| `git rev-parse --show-toplevel` | 0 | Assigned Story worktree |
| `mkdir -p .temp` | 0 | Replay scratch directory |
| `IDX git read-tree 67789e1ee29e766e446c7f33feb61561d51f94db` | 0 | Base loaded into temporary index |
| `task-board resource get TASK-260929-1w5ivu TASK-260929-1w5ivu_change-request_rev1.patch --output .temp/TASK-260929-1w5ivu_change-request_rev1.patch` | 0 | Patch materialized read-only from source task |
| `IDX git apply --cached .temp/TASK-260929-1w5ivu_change-request_rev1.patch` | 0 | CR patch replayed |
| `IDX git write-tree` | 0 | Exact expected candidate tree |
| `git diff --check 67789e1ee29e766e446c7f33feb61561d51f94db 3685fd24cebba08c08ef741f928c58610983abf9` | 0 | Whitespace check |
| `python3 .temp/TASK-261012-1jy4pd-static-review.py` — first attempt | 1 | Reviewer script selected a plan table outside §9; IndexError, not a product failure |
| Same Python command, after restricting the lookup to §9 | 0 | Exact paragraph/only line 24 changed; six literal texts; branch ordering; 80/80 literal-bound recompositions; source traces for F1/F2 |
| `IDX git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-1.patch` | 0 | Exec-flag mutant applies |
| `IDX git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-2.patch` | 0 | Sleep mutant applies |
| `IDX git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-3.patch` | 0 | Native-name mutant applies |
| `IDX git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-4.patch` | 0 | Non-goal mutant applies |
| `IDX git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-5.patch` | 0 | Old-text mutant applies |
| `IDX git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-6.patch` | 0 | Name-cap mutant applies |
| `IDX git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-7.patch` | 0 | Duplicate-fragment mutant applies |
| `IDX git write-tree` — after checks | 0 | Still exactly `3685fd24cebba08c08ef741f928c58610983abf9` |
| `gh run view 38239371527 --repo ivanopcode/codex --json headSha,status,conclusion,jobs,url` | 0 | Read hosted job statuses; repeated with a compact `--jq` projection |
| `gh run view 38239371527 --repo ivanopcode/codex --job 114777933172 --log > .temp/TASK-261012-1jy4pd-hosted-lint.log` | 0 | Read full lint log |
| `gh run view 38239371527 --repo ivanopcode/codex --job 114781620277 --log > .temp/TASK-261012-1jy4pd-hosted-core.log` | 0 | Read full snapshot core log |
| `gh api repos/ivanopcode/codex/git/commits/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6 --jq '{sha,tree:.tree.sha,message}'` | 0 | Hosted checkout commit has exactly the candidate tree |
| `python3 .temp/TASK-261012-1jy4pd-validate-verdict.py` | 0 | Exactly one valid JSON block, all nine source-table rows once, required finding fields, one verdict, replay/commands/logbook present |
| `cmp .research/261012_TASK-261012-1jy4pd_panel-verdict.md .temp/TASK-261012-1jy4pd-attached-verdict.md` | 0 | Downloaded task-scoped outcome matches the local artifact byte-for-byte |

The initial combined setup containing `rm -f` was refused before execution;
it has no process exit code. Setup was retried as the standalone commands
above without deletion. Diagnostic discovery failures were not validation:
the first task query used an unsupported `resources` field (exit 1), the
`schema(operation=resources)` probe exited 1, and a missing reviewer-role
path caused `cat` to exit 1. The installed role was subsequently read at
`/Users/administrator/.roles/reviewer/role.md` (exit 0). Searches including
nonexistent directories exited 2; a `command -v logbook` probe exited 1.
One exploratory `git show` of nonexistent `core/src/context/developer.rs`
failed with Git exit 128 while the enclosing read-only shell ended 0 from
its later reads; it is not counted as successful evidence.

No Rust build, lint, format, test, or mutant execution was run locally. No
production/test source was changed. Proposed strengthened Rust tests below
were not run; their expected failures are static deductions, not observed
failing executions.

## Hosted evidence accepted and independently checked

[Run 38239371527](https://github.com/ivanopcode/codex/actions/runs/38239371527)
has successful lint, snapshot small, snapshot core, and snapshot app-server
jobs. The overall run conclusion is **failure**, as expected from its
deliberately failing mutant jobs; it must not be described as an overall
green workflow. Attached `TASK-260929-1w5ivu_hosted-precheck-2.md` reports
7/7 mutants killed, 0 survivors; the job inventory agrees that each mutant
has at least one failing test lane. The per-mutant killer map is accepted
from that attachment rather than independently rerunning the mutants.

The full core log names checkout `3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6`;
the GitHub Git-commit API reports its tree as the exact replay tree. The run's
workflow head `9f8fdf9aa3f7b28ded9e62fd628b2206c2c76a8b` is not the source
checkout. Core-log lines 9508–9519 show PASS for all ten new
`suite::waiting_guidance` scenarios, including goal-stop and same-turn
no-churn. Line 9549 reports 5,132 tests passed, 11 skipped. This is execution
evidence for existing assertions, not for the strengthened assertions below.

The CR's `TASK-260929-1w5ivu_change-request_rev1-validation.log` contains only
the mini-hosted-gate command, its tree/run identity and `[exit 0]`, with
`coverage_unit=exact_command_shard required=1 green=1 failed=0 missing=0
test_case_coverage=unknown`. This review does not infer unlisted local test
results from that gate or from truncated logs.

## Source references and requested regressions

All source references below are to the snapshot commit whose tree was
independently verified, not to the reviewing worktree's checkout.

- [Contributor gate, extension.rs:618](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/ext/goal/src/extension.rs#L618): an inactive goal returns no fragments; an active goal always calls the renderer. There is no previous-capabilities comparison or inactive-state correction.
- [Renderer, steering.rs:92](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/ext/goal/src/steering.rs#L92): one complete developer fragment, with no validity-turn label or baseline.
- [Turn-start context routing, session/mod.rs:4722](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/core/src/session/mod.rs#L4722): unequal TurnContextItem values invoke the contribution path and record its messages. [turn_context.rs:777](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/core/src/session/turn_context.rs#L777) includes the new turn ID; [step_context.rs:51](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/core/src/session/step_context.rs#L51) preserves it. A fresh turn therefore triggers this path even when all waiting flags are identical.
- [History append, history.rs:534](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/core/src/context_manager/history.rs#L534): developer messages are retained and appended. `normalize_history` at line 933 repairs tool pairing/media; it does not replace or deduplicate capability fragments. PromptFragment's content kind is classification metadata, not a replacement key (`ext/extension-api/src/contributors/prompt.rs:58`).
- [Goal-stop public-entry scenario, waiting_guidance.rs:810](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/core/tests/suite/waiting_guidance.rs#L810): create, complete, then a third turn, with five requests. Request 4 retains the fragment while sleep is absent. Its checks omit SLEEP_MARKER. The turn-2 request's full fragment contains the sleep sentence, as asserted by the corresponding [tool-created scenario at line 437](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/core/tests/suite/waiting_guidance.rs#L437). The comment at line 461 explicitly mentions staleness next turn, contradicting the brief's bound ending at that next turn.
- [No-churn scenario, waiting_guidance.rs:756](https://github.com/ivanopcode/codex/blob/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6/codex-rs/core/tests/suite/waiting_guidance.rs#L756): three samples are within one turn. It cannot detect an unconditional extra contribution on the next turn.

For F1, strengthen the existing goal-stop test with
`assert_eq!(developer_occurrences(&requests[4], SLEEP_MARKER), requests[4].tool_by_name("clock", "sleep").is_some() as usize)`.
Static expectation on this candidate is `1 != 0`. Preserve the old history,
but make the current capability statement explicitly valid only for its
own turn or append an explicit correction at the transition. The exact
approach must respect the inactive-goal scope rule; silently treating old
unqualified guidance as current cannot meet request agreement.

For F2, add another user turn to the service-set, dead-manager no-churn
fixture without changing capabilities. Assert one retained waiting fragment
across both turns. Static expectation on the second turn is count 2, not 1.
Maintain a capability baseline on the existing extension/context path, with
correct full-context reinjection behavior; do not rewrite history. Add a
narrowing mutant that suppresses deduplication only across turn IDs. The
existing emitted-twice mutant tests duplication inside one renderer call
and does not cover this mechanism.

## Logbook entry — 2026-10-12, panel A

Exact patch replay and hosted checkout identity agree on tree `3685fd24`.
All nine surfaces swept: 7 held, 2 broken, 0 not-attacked. Static findings
F1/F2 identify turn-boundary stale guidance and repeated unchanged
contributions. The accepted two same-turn windows, BudgetLimited scope,
unit-only positive exec/native-mail coverage, deferred no-wait paragraph,
and disclosed size overrun remain accepted bounds. This logbook entry
travels as this task-scoped outcome; the source task receives no write.

## Successor verification and handoff recovery — 2026-10-12

This continuation independently reconfirmed the replay and the two static
findings; it preserves the predecessor's nine-row sweep and bounded free hunt.
The predecessor command ledger above is retained evidence, not a claim that
all those commands were rerun by this successor. Hosted test and mutant
execution remains reused exact-tree evidence; no Rust execution was added.

The prior panel handoff validation really failed (exit **1**): the untracked
`.research` artifact was included in the candidate code tree
`9f6f331d758149ca76313bcee874a3ab61d6ff1a`, which had no hosted green entry.
This was a panel evidence-placement failure, not a source CR failure. The
verdict file was preserved under ignored `.temp/.research/` and remains
attached to this panel task. The resulting research-only repository delta is
empty. The existing mini-hosted gate then exited **0**, explicitly reporting
`afb8c830d764ba489a9f2f922c0babdf1dbe036e = HEAD tree; nothing to validate`.
This green attests the empty panel delta; it is not a rerun of candidate tests.
No gate configuration or source-task state was changed.

| Successor standalone command | Exit | Observation |
|---|---:|---|
| `task-board m 'set_status(TASK-261012-1jy4pd, status=analysis)'` | 0 | Resumed own panel lifecycle |
| `mkdir -p .temp` | 0 | Scratch directory |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git read-tree 67789e1ee29e766e446c7f33feb61561d51f94db` | 0 | Fresh successor temporary index |
| `task-board resource get TASK-260929-1w5ivu TASK-260929-1w5ivu_change-request_rev1.patch --output .temp/TASK-260929-1w5ivu_change-request_rev1.patch` | 0 | Source patch read only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git apply --cached .temp/TASK-260929-1w5ivu_change-request_rev1.patch` | 0 | Replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git write-tree` | 0 | Exactly `3685fd24cebba08c08ef741f928c58610983abf9` |
| `cmp .research/261012_TASK-261012-1jy4pd_panel-verdict.md .temp/panel-verdict-attached-predecessor.md` | 0 | Existing board outcome equals predecessor local artifact, before relocation |
| `git diff --check 67789e1ee29e766e446c7f33feb61561d51f94db 3685fd24cebba08c08ef741f928c58610983abf9` | 0 | Source CR whitespace |
| `python3 .temp/TASK-261012-1jy4pd-static-review.py` | 0 | Exact §9 texts, template-only line 24, 80/80 bounds, 1724 B / 431 estimated tokens, F1/F2 source traces |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-1.patch` | 0 | Applicability, not execution |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-2.patch` | 0 | Applicability, not execution |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-3.patch` | 0 | Applicability, not execution |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-4.patch` | 0 | Applicability, not execution |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-5.patch` | 0 | Applicability, not execution |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-6.patch` | 0 | Applicability, not execution |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git apply --cached --check .temp/TASK-261012-1jy4pd-mutant-7.patch` | 0 | Applicability, not execution |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1jy4pd-replay-successor.idx" git write-tree` (after checks) | 0 | Candidate index still exactly matches |
| `gh run view 38239371527 --repo ivanopcode/codex --json status,conclusion,jobs,url --jq '{status,conclusion,url,jobs:[.jobs[]\|{name,conclusion,databaseId}]}'` | 0 | Four snapshot/lint lanes successful; aggregate failure includes expected-red mutant jobs |
| `gh api repos/ivanopcode/codex/git/commits/3e6fcab24eabc12505fbc4a279b9ca95cebcf5f6 --jq '{sha,tree:.tree.sha}'` | 0 | Reconfirms exact hosted checkout tree |
| `mkdir -p .temp/.research` | 0 | Ignored artifact storage |
| `mv .research/261012_TASK-261012-1jy4pd_panel-verdict.md .temp/.research/261012_TASK-261012-1jy4pd_panel-verdict.md` | 0 | Preserved artifact outside repository delta |
| `git status --short` | 0 | Empty status after relocation |
| `/Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` | 0 | Empty panel delta; no code to validate |

Successor source reads checked candidate lines 397–465 and 750–910 in
`waiting_guidance.rs`, the contributor, renderer, turn-ID comparison and
append-only history. They confirm that the comment at line 461 explicitly
extends staleness to the next turn, beyond the accepted same-turn window.
The existing same-turn no-churn fixture still makes only one user turn.
The requested stronger Rust assertions in F1/F2 remain unimplemented and
unrun under the read-only/no-build contract.

Successor diagnostic discovery: two queries using unsupported `resources`
exited 1 and were retried with supported projections; missing role/search
paths exited 1/2 and were replaced with the installed reviewer role path.
`task-board resource list` only printed help with exit 0 and was not treated
as resource-inventory evidence. Resource reads, source reads and directive
checks exited 0. No source-task mutation was attempted.

Successor logbook: preserved the panel outcome, reconfirmed F1/F2 and exact
candidate identity, diagnosed the failed research-file gate, and recovered
an empty research-only delta without changing product code or validation
policy. Successor outcome structure validation (`python3
.temp/TASK-261012-1jy4pd-validate-verdict.py`) exited 0: exactly one JSON
block, all nine rows once, two findings, required reproduction fields and
one verdict. The stored-byte comparison is performed during attachment. This entry travels in the panel's task-scoped outcome.

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
          "expected_failure": "After adding the request[4] SLEEP_MARKER/tool-presence equality described above, expected failure is left 1 versus right 0. Not run locally. The original test ran PASS in exact-tree hosted snapshot core job 114781620277; the strengthened expectation is established by the static append/gate trace, not by an observed red Rust execution."
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
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
          "expected_failure": "Extend the existing dead-manager service-set fixture with a second user turn and one additional mocked response, preserving the active goal and all flags; keep an exact total of four requests and expect one guidance occurrence in the last request. Static expected failure is count 2 versus 1. This extension was not implemented or run in this read-only panel. The current three-request same-turn version ran PASS on the exact candidate tree."
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Reviewed only the six-file CR delta, not the already-landed P3-1 snapshot implementation. No mutation, acceptance, rejection, withdrawal, handoff, note, status or resource write was made on TASK-260929-1w5ivu.",
    "Replay read-tree/apply/write-tree all exit 0; exact candidate match. Seven cached-index mutant applicability checks exit 0; the candidate index tree remains unchanged.",
    "Hosted lint and snapshot small/core/app-server jobs are successful; aggregate workflow conclusion is failure because expected-red mutant jobs fail. Kill ratio is 7/7 according to the attached hosted report. Full core log independently confirms all ten new scenarios ran PASS on the candidate tree.",
    "Literal byte-bound recomposition covers 80/80 shapes and gives 1724 bytes / 431 estimated tokens. This is a reviewer static calculation, not local Rust execution. Runtime/unit bound coverage is reused from hosted evidence.",
    "BudgetLimited is intentionally in GoalActivity scope. Initially goal-less, paused, blocked, complete and UsageLimited states contribute no new fragment. Positive exec-notify and native-mail-wait request agreement remain unit-only coverage as disclosed; native-mail host-policy wiring is outside this delta.",
    "The code-mode-only sleep-present agreement and the remote clock-off fixture's explicit reminder suppression are accepted disclosed semantics. The goal-less core paragraph and no-wait/end-turn paragraph remain out of scope/deferred.",
    "Changed-line count is exactly 1353 insertions + 23 deletions = 1376. Production/template delta is 93 changed lines; tests/module registration account for 1283. No core production, dependency, schema or public API delta.",
    "The two accepted same-turn windows are preserved. F1 is the additional turn-start mismatch after completion; F2 is unconditional repetition across unchanged turns. Both are static findings, with explicitly unexecuted strengthened-test requests."
  ],
  "surface_results": [
    {
      "row": "contract text",
      "result": "held",
      "reason": "Static byte comparison with final-plan §9 confirms only line 24 changes. Both update_plan variants derive from the same template; continuation_prompt_carries_section_nine_verified_wait_contract checks both renderings. Hosted old-text mutant is killed by that test."
    },
    {
      "row": "sentence selection",
      "result": "held",
      "reason": "Six literal texts match §9; Rust branches select exactly one exec sentence and optional sleep/stdin/native/mail sentences in fixed order. Native identity is dotted for non-default namespaces and bare for default namespace; deferred no-wait text is absent. Hosted per-flag/fixed-order tests and always-positive, unconditional-sleep and hardcoded-name mutants cover selection."
    },
    {
      "row": "scope and gating",
      "result": "held",
      "reason": "New contribution is gated exclusively on GoalActivity presence. Existing activity publisher admits Active/BudgetLimited, removes marker for other states/read failure; the non-goal public-entry test and non-goal mutant execute the new production gate. No goal-less core paragraph or alternate injection path was added. Historical retention is evaluated separately under request agreement, F1. Dedicated BudgetLimited/inactive-state request scenarios remain a disclosed coverage bound."
    },
    {
      "row": "bounded",
      "result": "held",
      "reason": "Existing PromptFragment path only. Cap limits the variable display name to 128 Unicode characters plus ellipsis; exact-limit, over-limit and multibyte cases are tested. All 16 Boolean combinations crossed with five name shapes are covered (80/80); maximum 1724 bytes / 431 estimated tokens is within 3072/1000. Hosted cap-removal mutant is killed."
    },
    {
      "row": "incremental, no churn",
      "result": "broken",
      "reason": "F2: new turn_id re-invokes the contributor, which unconditionally emits unchanged guidance again; same-turn no-churn coverage misses this boundary. Append-only history is preserved. The accepted mid-turn windows are not findings; F1 additionally shows resynchronization after completion is not achieved at the next turn."
    },
    {
      "row": "request agreement",
      "result": "broken",
      "reason": "F1: requests[4] in the hosted goal-stop scenario is a later turn-start request without clock.sleep but retains the uncorrected sleep sentence. The strengthened iff assertion is absent. Other named fresh-turn scenarios have exact request counts and hosted execution; code-mode/remote/excluded/headless/discovery semantics were checked against source rather than the obsolete precheck-1 expectations."
    },
    {
      "row": "tool descriptions",
      "result": "held",
      "reason": "Checked unchanged shell_spec.rs:75-136,147-180 (receipt acknowledgment, write_stdin waits), sleep.rs:39-77 (input interruption and direct-only exposure), and multi_agents_spec.rs:268-292,845-887 (V1 targets/V2 mailbox). None contradict the selected text; V2 lacks targets and the fragment explicitly qualifies multiple identifiers with 'where that tool supports them'. No description churn."
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "reason": "All seven source-resource mutant patches apply against the replayed candidate (7/7 checks exit 0). Hosted report supplies filter-selected named killers and 7/7 kills. Exact request counts sum to 25 responses plus one /models request. Size measurements independently recomputed. This satisfies the enumerated mutants; their coverage does not extend to the new F1/F2 strengthened assertions."
    },
    {
      "row": "placement and size",
      "result": "held",
      "reason": "Only renderer/gate/template production changes in ext/goal, 93 changed lines. Core changes are integration tests plus module registration. Total 1376 changed lines is the expressly disclosed test-driven overrun; no production expansion into core, dependencies, generated schemas or external integration surfaces."
    }
  ],
  "free_hunt": {
    "bounded_scope": "Four additional static attack families after the nine-row sweep; no build/test or product-code edits.",
    "attacks": [
      {
        "family": "history replacement and classification metadata",
        "result": "No hidden replacement or duplicate suppression: content_kind is annotation; PromptFragment converts to ordinary developer text and history appends. This corroborates F1/F2 rather than creating another finding."
      },
      {
        "family": "goal lifecycle and unknown reconciliation",
        "result": "Existing GoalActivityPublisher removes the marker on read failure, feature disable and teardown, and admits BudgetLimited consistently. No new gate bypass in this CR. Fresh request agreement for every inactive status is not independently executed here."
      },
      {
        "family": "native identity and Unicode bounds",
        "result": "Namespaced/default identities and Unicode-safe truncation reviewed; effective capped display is 128 characters plus an ellipsis. Individual fragment remains bounded. Claim agreement for a configured overlong native namespace has no public-entry execution in this review and is reported unknown, not a held runtime claim."
      },
      {
        "family": "public API and candidate/evidence provenance",
        "result": "No CLI/config/API/rollout shape change in the six-file delta. Replay and hosted checkout tree match exactly; all ten new core scenarios have explicit PASS records. No additional finding."
      }
    ],
    "additional_findings": [],
    "coverage": "9/9 surface rows attacked; 7 held, 2 broken, 0 not-attacked. Four bounded free-hunt families reviewed. New adversarial Rust assertions requested above remain unrun."
  }
}
```
