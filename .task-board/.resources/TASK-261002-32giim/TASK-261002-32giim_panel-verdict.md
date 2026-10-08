# TASK-261002-32giim — R141 panel B, revision 1

accept

Read-only, non-recording review of CR-TASK-260929-2fa1hy-1 (goal-activity marker and sleep gate). No writes, status changes, acceptance/rejection or handoff were made on TASK-260929-2fa1hy. This panel supplies an advisory verdict; the orchestrator owns merged recording.

## Replay and identity

Base: `ea8899e6f97aea64136159286840c28c955243e8`.
Expected candidate: `403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd`.
Actual temporary-index `git write-tree`: **`403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd`**, exact match.
The locally available hosted snapshot `dc09022358edd7d4f59c13c8f282b5b9df2cd1e5^{tree}` independently resolves to the same tree. Review reads use that candidate tree, not worktree HEAD. No nested worktree, branch operation, source change, build or test execution occurred. `git status --short` was empty; `git rev-list --count HEAD..relux/main` printed 0 (cached comparison only, not fresh remote attestation).

## Commands executed by this panel

Commands below ran directly; gate exits were not hidden by pipelines. Paths are relative to the assigned worktree unless absolute. The initial replay used `git read-tree --index-output`, which writes the named temporary index and leaves the normal index intact.

| Command | Exit | Result |
| --- | ---: | --- |
| `git read-tree --index-output=.temp/TASK-261002-32giim-replay.idx ea8899e6f97aea64136159286840c28c955243e8` | 0 | Loaded base into temporary index |
| `task-board resource get TASK-260929-2fa1hy TASK-260929-2fa1hy_change-request_rev1.patch --output .temp/TASK-260929-2fa1hy_change-request_rev1.patch` | 0 | Read-only resource retrieval |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-32giim-replay.idx" git apply --cached .temp/TASK-260929-2fa1hy_change-request_rev1.patch` | 0 | Patch applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-32giim-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git rev-parse dc09022358edd7d4f59c13c8f282b5b9df2cd1e5^{tree}` | 0 | Same candidate as hosted snapshot |
| `git diff --check ea8899e6f97aea64136159286840c28c955243e8 403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd` | 0 | No whitespace errors |
| `git diff --stat ea8899e6f97aea64136159286840c28c955243e8 403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd` | 0 | 5 paths, 294 insertions, 1 deletion |
| `git diff --unified=4 dc09022358edd7d4f59c13c8f282b5b9df2cd1e5 859b052 -- codex-rs/core/src/tools/spec_plan.rs` | 0 | Hard-disable narrowing patch verified |
| Same command with mutant commit `c53f17d` | 0 | Reminder-false narrowing patch verified |
| Same command with mutant commit `1eb8590` | 0 | No-marker narrowing patch verified |
| `git status --short` | 0 | Clean tracked/untracked status (ignored scratch only) |
| `git rev-list --count HEAD..relux/main` | 0 | 0 |
| `python3 .temp/TASK-261002-32giim/validate-verdict.py` | 0 | One JSON block, required fields, exact surface row, accept with no findings, source citations and replay identity |

Read operations: `task-board resource get` succeeded (exit 0 each) for surface-table.md, producer-brief.md, final-plan.md, TASK-260929-2fa1hy_hosted-precheck-1.md, TASK-260929-2fa1hy_results.md, TASK-260929-2fa1hy_coverage-map.md, TASK-260929-2fa1hy_mutants.json and TASK-260929-2fa1hy_change-request_rev1-validation.log. Corrected task projections (`description scope ac notes`, `outcomeResources`, and this panel's `ac checklist`) exited 0. `git show` candidate source reads and successful caller/exposure searches exited 0. Python source-range and validation-log extraction exited 0. Tool-readiness outputs are retained in `.temp/TASK-261002-32giim/*readiness-01.log` and `task-board-help-01.log`.

Exploratory failures are not greens: two board queries using unknown projection `resources` failed with exit 1; recovered with scoped `schema(operation=get)` and `outcomeResources`. The initial reviewer-role path under `.claude` was missing (cat error; its combined read returned nonzero before subsequent shell commands), then the installed `.agents/skills/project-management/.roles/reviewer/role.md` was located and read. `rg --files` reported missing agents/skills and .claude/skills directories; the available .codex catalog was read. Early combined discovery calls ended with successful trailing commands, so their overall exit 0 is not attributed to failed intermediate reads. Searches for guessed `prepare_sampling_step`/`prepare_step`, `sampling_step` and `create_step|new_step|build_step|prepare.*step` had no matches (git grep exit 1); following `capture_step_context` resolved the real call chain. None was treated as proof of absence.

## AC sweep and static attacks

Coverage: **6/6 AC rows assessed; 1/1 surface rows held; 0 broken; 0 not-attacked; 3/3 supplied narrowing mutants reported killed in accepted hosted evidence; 0 runtime tests rerun by this panel.** Held uses the brief's permitted combination of exact-tree public-entry execution evidence and this panel's static attack, not a claim that this panel ran Rust.

All code citations below are relative to `codex-rs/` at candidate tree `403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd`, readable with `git show TREE:codex-rs/PATH`.

| AC | Adversarial check and result | Candidate evidence |
| --- | --- | --- |
| 1 | Absent marker plus unrelated String cannot expose sleep; Active exposes it with reminder off and no model clock | `core/src/tools/spec_plan.rs:145-149,1242-1258`; `core/tests/suite/current_time_reminder.rs:595-699` |
| 2 | Both enum states are present markers; removal is observed on the next constructed request router | Same request sequence asserts `[false,true,true,false]`; typed map uses TypeId in `ext/extension-api/src/state.rs:79-85,108-114,136-141` |
| 3 | Tried marker present with hard disable: outer SleepTool condition prevents reaching either mode branch | `spec_plan.rs:1242`; `current_time_reminder.rs:701-755`; hard_disable_bypass hosted kill |
| 4 | Tried reminder enabled with explicit false and absent config: neither can fall through to marker path; explicit true retains curr_time and sleep | `spec_plan.rs:1246-1253`; `current_time_reminder.rs:757-797`; reminder_false_bypass hosted kill; final-plan.md section 4 precedence |
| 5 | AlwaysOn retains its override under the hard gate; model clock fallback unchanged; marker does not add curr_time or other tools; sleep remains direct-only | `spec_plan.rs:1233-1258`; existing matrix `current_time_reminder.rs:484-592`; whole remaining-catalog assertion at 691-697; `core/src/tools/handlers/sleep.rs:75-76`; `core/src/tools/spec_plan_tests.rs:1414-1458` |
| 6 | New documented type and both variants exported; insertion test drives actual typed map | `ext/extension-api/src/goal_activity.rs:1-27`; `lib.rs:3,11-12`; `tests/state.rs:13-24` |

Production path traced to defeat a disconnected/test-only gate: `core/src/session/turn.rs:461-498` captures each next request step, `core/src/session/mod.rs:3761-3777,3796-3803,3921-3930` builds its router, `core/src/session/turn.rs:1863-1872` calls production `build_tool_router`, and `core/src/tools/spec_plan.rs:145-158` reads typed thread data and registers core tools. The false default at spec_plan.rs:295 belongs to the cfg(test) builder, not a production bypass. New integration tests use `test_codex().build_with_auto_env`, submit real user turns and assert captured Responses requests.

The gate is identical to final-plan.md section 4: `SleepTool && (AlwaysOn || (ModelDriven && (reminder ? configured_sleep : (model_clock || marker))))`. No equality check on Active alone accidentally excludes BudgetLimited. No goal ID, revision, or state bytes enter model context. No CLI/config/API/rollout serialization shape changed. The diff stays under 500 changed lines; the tiny existing core gate edit does not introduce goal implementation into core.

## Execution evidence accepted, not rerun

`TASK-260929-2fa1hy_change-request_rev1-validation.log` is readable through its terminal line 517. It records target guard exit 0 (line 3), fmt-check exit 0 (line 5), scoped six-crate clippy exit 0 (line 164), and four-small-crate `just test` exit 0 (line 516). It reports **233/233 tests passed, 0 skipped**, including the new API insertion test (line 289), and command-shard coverage **4/4**. This is not inferred full test-case coverage: the log explicitly says `test_case_coverage=unknown`.

`TASK-260929-2fa1hy_hosted-precheck-1.md` reports [36983853906](https://github.com/relux-works/codex/actions/runs/36983853906) green for lint/small/core/app-server on snapshot dc09022, with all six new G1 request instances PASS. Core reports 4,860 passed, 11 skipped, with two retries. The three expected-red mutant core lanes are **failures**, not green checks:

| Mutant | Hosted run | Reported failure |
| --- | --- | --- |
| hard_disable_bypass | [36983895784](https://github.com/relux-works/codex/actions/runs/36983895784) | 1 failed, disabled_sleep_tool_feature_wins_over_goal_activity |
| reminder_false_bypass | [36983937144](https://github.com/relux-works/codex/actions/runs/36983937144) | 1 failed, current_time_reminder_sleep_setting_overrides_goal_activity::explicit_false |
| no_marker_admitted | [36983916432](https://github.com/relux-works/codex/actions/runs/36983916432) | 27 failed including goal_activity_controls_model_driven_sleep_on_each_sampling_request; lint also fails but is not the behavioral kill |

Numeric hosted process exits are **unknown in the supplied record**. No broader OS/foreign-executor coverage is inferred. The local Git object equality verifies candidate source identity; hosted outcomes remain explicitly attributed to the owner-provided resource.

## Bounded free hunt and logbook

After persisting the surface row result, inspected alternative router construction, per-step freshness, typed-data spoofing, code-mode exposure, unchanged curr_time gating, crate exports and Bazel source inclusion. `defs.bzl:315` uses `src/**/*.rs`; the extension-api BUILD invokes that macro, so the new module needs no explicit file enumeration. No blocking mechanism reproduced; free_hunt is empty. This is not proof of absence.

Research decision: advise accept versus changes_requested for this exact CR revision. Grammar precondition: not applicable (no external format changes). Consuming slice: orchestrator's merged G1 recording, then sibling G2 publisher work. Scope budget: one 30-minute static review, at most 5 minutes free hunt, one outcome below 32 KiB, no archive or serial research prerequisite. Exit: exact replay, one result per supplied row, AC assessment and a structured advisory verdict. No budget expansion or extra research leaf was needed.

Outcome-scoped logbook: replay matched; exact hosted snapshot equality checked independently; precedence and typed spoof refusal held; inherited mutant metadata is historical, resolved by the later owner report. The installed reviewer-role reference was recovered without modifying runtime files. All source and control-root files remain untouched; task-scoped scratch stays under the worktree's ignored .temp. This attachment is staged in a task-scoped system temporary directory as explicitly required by the assignment, and attached only through resource CRUD to the panel task. The source task receives no mutation. No independent GitHub review, accept_cr, reject_cr or publication was attempted.

## Structured verdict

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "execution-evidence-bound",
      "text": "Panel B ran replay and read-only static checks only. Runtime and mutant outcomes are accepted from the explicitly supplied exact-tree hosted-precheck resource; no hosted jobs were independently rerun or queried. Hosted numeric process exits are unknown, not assumed zero. CR validation log has four explicit exit-0 command shards and a terminal summary."
    },
    {
      "id": "publisher-and-same-turn-bound",
      "text": "Goal publishers, reconciliation, stale callbacks, create/clear/resume hooks and automatic continuation admission belong to sibling G2 and are excluded here. The new sequence covers four separate submitted turns in one thread; same-turn post-create mutation is supported by the static per-step router trace, not newly exercised by this leaf. Do not treat this panel as accepting G2 lifecycle behavior."
    },
    {
      "id": "historical-mutant-metadata",
      "text": "TASK-260929-2fa1hy_mutants.json still labels execution as pending. The later hosted-precheck and handoff results explicitly supersede that historical status. Exact mutant commit diffs match the three attached narrowing patches. This is an evidence chronology note, not a surviving mutant."
    }
  ],
  "surface_results": [
    {
      "row": "capability gate",
      "result": "held",
      "basis": "Static adversarial trace against exact replay tree, combined with accepted exact-tree hosted public-entry tests and narrowing-mutant failures. No runtime attacks rerun by panel B.",
      "findings": [],
      "attacks": [
        {
          "family": "absent / unrelated typed entry / Active / BudgetLimited / removal",
          "evidence": "core/tests/suite/current_time_reminder.rs:595-699; hosted 36983853906 direct_tools and code_mode PASS, expected request sequence [false,true,true,false]; no_marker_admitted killed in 36983916432",
          "static_result": "Typed get::<GoalActivity>() excludes unrelated String entries; marker is read on router construction, not cached on Session creation."
        },
        {
          "family": "hard disable / reminder explicit false or absent",
          "evidence": "core/tests/suite/current_time_reminder.rs:701-797; hosted 36983853906 PASS; hard_disable_bypass killed in 36983895784 and reminder_false_bypass killed in 36983937144",
          "static_result": "Feature::SleepTool dominates the match. Reminder branch cannot reach goal_activity_present, and is_some_and rejects missing config."
        },
        {
          "family": "AlwaysOn / model catalog / code-mode exposure / other tools",
          "evidence": "core/tests/suite/current_time_reminder.rs:484-592, 683-697; core/src/tools/spec_plan_tests.rs:1390-1458; core/src/tools/handlers/sleep.rs:75-76",
          "static_result": "AlwaysOn and model_has_clock paths are unchanged; SleepHandler still DirectModelOnly. New request tests compare the whole catalog after removing sleep. Hosted full core lane green; code-mode leaf dispatch is not newly exercised."
        }
      ]
    }
  ],
  "free_hunt": []
}
```
