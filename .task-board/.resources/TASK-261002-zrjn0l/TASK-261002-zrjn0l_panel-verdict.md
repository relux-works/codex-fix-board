# R141 panel A verdict — CR-TASK-260929-2fa1hy-1 rev1 (non-recording)

Reviewer: researcher run on TASK-261002-zrjn0l. Nothing written on TASK-260929-2fa1hy.

## Replay tree check
Base `ea8899e6f97aea64136159286840c28c955243e8`, patch `TASK-260929-2fa1hy_change-request_rev1.patch` (405 lines) applied via temporary index.
`git write-tree` = `403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd` — **matches** the expected candidate tree.

## Commands run (no cargo/just/build)
| Command | Exit |
| --- | ---: |
| `GIT_INDEX_FILE=$IDX git read-tree ea8899e6…` | 0 |
| `task-board resource get TASK-260929-2fa1hy …change-request_rev1.patch --output …` | 0 |
| `GIT_INDEX_FILE=$IDX git apply --cached <patch>` | 0 |
| `GIT_INDEX_FILE=$IDX git write-tree` (prints 403dbe80…) | 0 |
| `task-board resource get` for surface-table.md, producer-brief.md, hosted-precheck-1.md | 0 |
| static reads: spec_plan.rs gate, sleep.rs, turn.rs/startup_prewarm.rs router build sites, state.rs | 0 |

Execution evidence accepted (not rerun): hosted-precheck-1 — relux-ci run 36983853906 green on all lanes, 6 G1 request tests pass; mutants hard_disable_bypass / reminder_false_bypass / no_marker_admitted killed by their named tests (runs 36983895784, 36983937144, 36983916432).

## Static attack summary
- Gate (spec_plan.rs ~1241-1256): `features.enabled(SleepTool) && match mode { AlwaysOn => true, ModelDriven => if reminder_enabled { config.sleep_tool } else { model_has_clock || goal_activity_present } }`. Only the final `else` arm changed. Hard gate outermost, so disable wins; AlwaysOn untouched; reminder-on branch consults only `current_time_reminder.sleep_tool` (explicit_true/explicit_false/missing_config tests cover all three).
- Marker lookup is `thread_extension_data.get::<GoalActivity>()` keyed by `TypeId`, so an unrelated entry (the test inserts a `String`) cannot spoof it; `Some` for both Active and BudgetLimited, as required (AC 2).
- Evaluated per sampling request: the sole production caller of `build_tool_router` is `turn::built_tools` (turn.rs:1863), reached from session/mod.rs:3921 and the step-context capture path; the router is not cached across steps, so removal takes effect on the next request (test asserts [false,true,true,false]).
- Code mode: `SleepHandler::exposure()` is `DirectModelOnly` (sleep.rs:75), unchanged; code_mode test case asserts it in the request tools while the non-sleep tool catalog is identical across all four requests.
- `build_core_tool_registry` (test/helper entry) hardcodes `goal_activity_present: false`; production path is `build_tool_router` only, so no production gap.
- Type is documented, exported (`GoalActivity`, `GoalActivityState`), unit-tested via ExtensionData; no goal-extension or core->goal dependency added. Scope matches the task (5 paths).

```verdict-findings
{
  "findings": [],
  "notes": [
    "Request tests flip the marker between turns, not between sampling steps inside one turn. Production builds the router per step (turn.rs:1863 via built_tools), so mid-turn removal is covered by construction, not by a direct test. Not a defect; relevant to G2 publisher hooks.",
    "build_core_tool_registry hardcodes goal_activity_present=false. It is a non-production helper entry (router_tests/spec_plan_tests); no marker-driven sleep spec test exists at that layer, coverage is via the suite request tests.",
    "Precedence verified as stated in verdict rev3 note 2: reminder feature on + sleep_tool false/absent keeps sleep hidden even with an active marker (explicit_false, missing_config)."
  ],
  "surface_results": [
    {"row": "capability gate", "result": "held", "evidence": "Gate expression statically matches the invariant exactly; hard-disable, AlwaysOn, reminder-on arms unchanged; marker keyed by TypeId (String spoof test); Active and BudgetLimited both admit; removal drops sleep on the next request; sleep stays DirectModelOnly in code mode; hosted run 36983853906 green with all 6 G1 tests and 3 narrowing mutants killed by named tests."}
  ],
  "free_hunt": "Checked: other consumers of the sleep gate/duplicate registrations (only add_core_utility_tools registers SleepHandler); other build_tool_router call sites (single production site); ExtensionData::get cost/locking per step (mutex + Arc clone, negligible); lib.rs export/mod ordering; marker doc claims (ephemeral, not persisted, no continuation admission) vs code (pure data type, no behavior); test helper tool_catalog_without_sleep correctness (strips only clock.sleep, drops clock namespace only if empty). No defects found."
}
```

Verdict: accept
