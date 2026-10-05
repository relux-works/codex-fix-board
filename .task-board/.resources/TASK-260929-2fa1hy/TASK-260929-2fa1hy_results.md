# TASK-260929-2fa1hy — goal activity marker and sleep gate

## Review handoff

Added and documented exported `GoalActivity { goal_id, revision, state: Active | BudgetLimited }` in extension-api. The thread-scoped ephemeral marker grants tool capability, not continuation admission. Core reads typed marker presence each time it builds the sampling router. The hard SleepTool gate and AlwaysOn behavior remain intact; ModelDriven with reminders enabled consults only the reminder sleep setting; with reminders disabled it accepts model clock support or the marker.

The uncommitted candidate is based on `ea8899e6f97aea64136159286840c28c955243e8`, equal to local `relux/main` (distance 0). No commits, branch operations, PRs, goal-extension changes, dependency/schema changes, README or docs changes were made. Changes remain in five scoped files:

- `core/src/tools/spec_plan.rs`
- `core/tests/suite/current_time_reminder.rs`
- `ext/extension-api/src/lib.rs`
- `ext/extension-api/src/goal_activity.rs` (new)
- `ext/extension-api/tests/state.rs`

Existing upstream changes since plan pin `33a0f766a6` were inspected: `35af013b90` adds integral wait-argument support; `f53f5a6fed` changes lifecycle error reporting. The resumed work extends the existing producer tests for missing/true reminder configuration and code mode; it preserves all previously committed tests. No previously committed reviewer test was removed or renamed. The parameterized names replace only earlier uncommitted producer tests.

## Acceptance coverage

**6 of 6 AC rows driven and green on the unchanged candidate. 1 of 1 supplied surface rows verified; 3 of 3 narrowing mutants killed.** Current-candidate core evidence is accepted from orchestrator-run hosted precheck 1 under the explicit ownership decision in `g1-handoff-note.md`, not inferred from compilation or historical local tests.

Snapshot `dc09022358edd7d4f59c13c8f282b5b9df2cd1e5` has tree `403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd`. This resume independently recomputed the working tree with a temporary index (`git read-tree HEAD`, `git add -A`, `git write-tree`), exit 0, and confirmed exact equality. No source/test/configuration file was changed in this resume. The ordinary index and Story branch remain untouched; the candidate remains uncommitted.

Hosted [run 36983853906](https://github.com/relux-works/codex/actions/runs/36983853906) succeeded in all lanes: lint, small, core, app-server. Core ran 4,860 tests, all passed (2 flaky passed on retry), 11 skipped. All six G1 request test instances PASS. Existing committed reviewer tests retain their original names; the full hosted suites are green apart from the explicitly reported skips.

| AC | Driving test | Refusal or control | Production call site | Evidence |
| ---: | --- | --- | --- | --- |
| 1 | `goal_activity_controls_model_driven_sleep_on_each_sampling_request::{direct_tools,code_mode}`, request 2 | Request 1: no marker and unrelated String entry => absent | `core/src/tools/spec_plan.rs::build_tool_router` → `add_core_utility_tools` → sampled tools | Hosted 36983853906 PASS; no-marker mutant killed in 36983916432 |
| 2 | Same test, request 3: BudgetLimited | Request 4: marker removed => absent | Same per-sample production router | Hosted 36983853906 PASS |
| 3 | `disabled_sleep_tool_feature_wins_over_goal_activity` | Active marker + SleepTool disabled => absent | Same router hard gate | Hosted 36983853906 PASS; hard-disable mutant killed in 36983895784 |
| 4 | `current_time_reminder_sleep_setting_overrides_goal_activity::explicit_true` | `::explicit_false` and `::missing_config`: marker cannot override; curr_time remains present | Same router ModelDriven reminder branch | Hosted 36983853906 PASS; reminder-false mutant killed in 36983937144 |
| 5 | Existing `sleep_tool_configuration_controls_registration`, `client_feature_map_can_disable_sleep_tool`, `sleep_tool_follows_current_time_config`, `sleep_tool_stays_direct_and_outside_code_mode` | AlwaysOn/hard-off/model clock matrix; marker test compares complete non-sleep catalogs | `build_tool_router` and `build_core_tool_registry` | Full hosted core lane green in 36983853906; direct-only dispatch bound below |
| 6 | `state::goal_activity_can_be_inserted_as_typed_thread_data` | No refusal applicable to typed construction/insertion/read | Exported `ExtensionData::insert/get` | Local exit 0, 12 passed; hosted small lane green in 36983853906 |

The supplied surface row and all current mutant evidence are mapped in `TASK-260929-2fa1hy_coverage-map.md`. The installed catalog lacks the supplied `capability gate` label; the owner's explicit row is retained verbatim rather than silently waived.

## Commands and real exit codes

All validation commands were standalone processes with redirected stdout/stderr, without tee or pipe chains. Logs are in the attached fast-lane archive. Current source identity, toolchain, platform and non-secret configuration hashes are attached in `TASK-260929-2fa1hy_candidate-identity.json`. The target was FREE before builds. The required target guard ran first and cleaned workspace-member artifacts. No cargo target/jobs/incremental/V8 variables were overridden. Just commands used `NEXTEST_TEST_THREADS=4`, `INSTA_UPDATE=no`, and `INSTA_WORKSPACE_ROOT=$PWD` from this worktree's `codex-rs`.

| Command | Exit | Log / result |
| --- | ---: | --- |
| `python3 …/codex-fix-suite-busy.py --any` (initial) | 0 | FREE |
| `…/codex-target-guard.sh` | 0 | `target-guard-06.log` |
| `just fmt` | 0 | `fmt-08.log` |
| `just fix -p codex-core -p codex-extension-api` | 0 | `fix-09.log`, 4m18s; only three unrelated unused imports were auto-deleted; exact deletions restored |
| `just fmt` after restoration/documentation/argument comments | 0 | `fmt-13.log` |
| `just clippy -p codex-core -p codex-extension-api` | 0 | `clippy-14.log`, 2m28s; tests type-check. Three pre-existing unused-import warnings in out-of-scope registry.rs, openai_file_mcp.rs and scenarios.rs are preserved; no warnings in leaf files |
| `just test -p codex-extension-api` | 0 | `extension-api-test-17.log`: 12 passed, 0 skipped, including typed marker test |
| `git diff --check` (three standalone invocations) | 0 | `diff-check-10.log`, `diff-check-15.log`, `diff-check-18.log` |

No local `just test -p codex-core`, app-server test command, full suite or integration-helper build ran, as expressly prohibited by updated `producer-brief.md` and `g1-resume-note.md`. Hosted `relux-ci` runs the core/app-server suites against the published exact candidate. The board handoff runs the configured fast landing gate; its result is independent of these producer checks.

## Narrowing mutants — current candidate hosted evidence

Each patch from the attached mutant JSON was applied to the exact snapshot. Evidence is `TASK-260929-2fa1hy_hosted-precheck-1.md`; no local core suite or mutant replay ran in this resume. Expected-red core lanes are failures, not passing gates. The supplied hosted precheck reports actual lane outcomes and named failures, but does not expose numeric process exit codes; those codes are unknown here and are not fabricated.

| Mutant | Narrowed rejection boundary / wrongly admitted class | Named failing test | Hosted evidence | Survivor bound |
| --- | --- | --- | --- | --- |
| `hard_disable_bypass` | Retains mode/reminder gates but admits marker despite SleepTool disabled | `disabled_sleep_tool_feature_wins_over_goal_activity` | [36983895784](https://github.com/relux-works/codex/actions/runs/36983895784), commit 859b052: core failure, 1 failed | Killed; none |
| `reminder_false_bypass` | Retains reminder branch but admits marker when configured sleep=false | `current_time_reminder_sleep_setting_overrides_goal_activity::explicit_false` | [36983937144](https://github.com/relux-works/codex/actions/runs/36983937144), commit c53f17d: core failure, 1 failed | Killed; none |
| `no_marker_admitted` | Retains hard/reminder gates but admits Goals-enabled no-clock/no-marker sessions | `goal_activity_controls_model_driven_sleep_on_each_sampling_request` (plus spec_plan/code_mode tests) | [36983916432](https://github.com/relux-works/codex/actions/runs/36983916432), commit 1eb8590: core failure, 27 failed; lint also fails on an unused field | Killed by behavioral tests, not merely lint; none |

No source-text gate exists here, so token-preserving source-checker mutation is inapplicable. No current mutant remains unexecuted or surviving according to the accepted hosted evidence. Historical 17-test evidence remains attached for audit but is not the identity basis for this handoff.

## Out-of-contract rows and bounds

- Goal publisher lifecycle, committed-state reconciliation, stale callback handling, resume and clear hooks: excluded by task scope, “This leaf only adds the type, the gate and tests that insert/remove the marker directly. No goal-extension changes (sibling leaf).”
- Goal states beyond Active and BudgetLimited: AC 6 defines the representable marker states.
- Linux, Windows and foreign-executor execution: no such local execution on this macOS arm64 host. Hosted lane success is accepted as reported; no broader platform coverage is inferred from the precheck summary.
- New code-mode request case checks sampled direct exposure and unchanged remaining catalog; actual code-mode leaf dispatch is not newly exercised. Existing `sleep_tool_stays_direct_and_outside_code_mode` checks direct-only registration and code-mode exclusion.
- Previously committed reviewer tests are kept under original names. Hosted full suites are green; 11 core skips are reported explicitly rather than claimed executed.

No production rework escaped the named scope. No forced-fit workaround or product/platform assumption was introduced. Compilation proves build validity at the permitted type-check boundary, not execution of the deferred core tests.

## Outcome-scoped logbook

Resumed from the earlier HOLD-BUILD. Initial busy check FREE; target guard cleaned stale member artifacts. Filled reminder missing-config and true-setting controls and code-mode sampled-request coverage. Clippy fix repeated the predecessor's three unrelated import deletions; restored all three to keep the leaf diff bounded. Current scoped compilation and small-crate suite pass. Reopened command-dependent checklist entries for core tests/mutants to avoid carrying old green claims across a changed candidate. The pre-handoff busy result and board gate verdict are recorded by the final handoff command; a BUSY result holds handoff under tb-R58/tb-R64.

Exploratory board query failures (`task` unknown operation and `resources` unknown projection) were repaired through schema guidance and `get`/`outcomeResources`. A missing support-file path was re-located; none of these exploratory failures is validation evidence. Outcome files were staged in a task-scoped temporary directory outside the managed worktree for resource attachment, as required; no control-root files were edited directly.

## Outcome-scoped logbook — ownership resolution and resume

The previous handoff refusal (exit 1, unchecked items 3/6/8/9/10) remains attached as historical evidence. `g1-handoff-note.md` resolves the ownership conflict explicitly: the owner ran exact-tree hosted pre-handoff core suites and narrowing mutants. This resume verified tree equality, accepted that evidence, and updated those checklist items with the run/test citations. No gate was weakened, no code changed, no required core execution was replaced by a compile proxy, and no production rework escaped the scope.

This resume reran only the temporary-index identity verification (exit 0). It accepts the earlier attached local fmt/fix/clippy/API greens and the owner's current-snapshot hosted evidence; it did not rerun Cargo/Just or the full suite. Outcomes are staged outside the managed worktree in a task-scoped system temporary directory and attached using the board CLI; no control-root files were edited directly. The busy check and handoff command results are attached as a separate task-scoped resume log.
