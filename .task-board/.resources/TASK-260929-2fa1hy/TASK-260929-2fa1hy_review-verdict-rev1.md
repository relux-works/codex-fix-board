# Merged review verdict — TASK-260929-2fa1hy CR revision 1 (tb-R141 / R132 merge)

Verdict: **accept**

Panel outcomes: `TASK-261002-zrjn0l_panel-verdict.md` (accept), `TASK-261002-32giim_panel-verdict.md` (accept)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [],
  "notes": [
    "[TASK-261002-zrjn0l] Request tests flip the marker between turns, not between sampling steps inside one turn. Production builds the router per step (turn.rs:1863 via built_tools), so mid-turn removal is covered by construction, not by a direct test. Not a defect; relevant to G2 publisher hooks.",
    "[TASK-261002-zrjn0l] build_core_tool_registry hardcodes goal_activity_present=false. It is a non-production helper entry (router_tests/spec_plan_tests); no marker-driven sleep spec test exists at that layer, coverage is via the suite request tests.",
    "[TASK-261002-zrjn0l] Precedence verified as stated in verdict rev3 note 2: reminder feature on + sleep_tool false/absent keeps sleep hidden even with an active marker (explicit_false, missing_config).",
    "[TASK-261002-32giim] {'id': 'execution-evidence-bound', 'text': 'Panel B ran replay and read-only static checks only. Runtime and mutant outcomes are accepted from the explicitly supplied exact-tree hosted-precheck resource; no hosted jobs were independently rerun or queried. Hosted numeric process exits are unknown, not assumed zero. CR validation log has four explicit exit-0 command shards and a terminal summary.'}",
    "[TASK-261002-32giim] {'id': 'publisher-and-same-turn-bound', 'text': 'Goal publishers, reconciliation, stale callbacks, create/clear/resume hooks and automatic continuation admission belong to sibling G2 and are excluded here. The new sequence covers four separate submitted turns in one thread; same-turn post-create mutation is supported by the static per-step router trace, not newly exercised by this leaf. Do not treat this panel as accepting G2 lifecycle behavior.'}",
    "[TASK-261002-32giim] {'id': 'historical-mutant-metadata', 'text': 'TASK-260929-2fa1hy_mutants.json still labels execution as pending. The later hosted-precheck and handoff results explicitly supersede that historical status. Exact mutant commit diffs match the three attached narrowing patches. This is an evidence chronology note, not a surviving mutant.'}"
  ],
  "surface_results": [
    {
      "row": "capability gate",
      "result": "held",
      "evidence": "Gate expression statically matches the invariant exactly; hard-disable, AlwaysOn, reminder-on arms unchanged; marker keyed by TypeId (String spoof test); Active and BudgetLimited both admit; removal drops sleep on the next request; sleep stays DirectModelOnly in code mode; hosted run 36983853906 green with all 6 G1 tests and 3 narrowing mutants killed by named tests.",
      "reported_by": "TASK-261002-zrjn0l"
    }
  ],
  "free_hunt": [
    "[TASK-261002-zrjn0l] Checked: other consumers of the sleep gate/duplicate registrations (only add_core_utility_tools registers SleepHandler); other build_tool_router call sites (single production site); ExtensionData::get cost/locking per step (mutex + Arc clone, negligible); lib.rs export/mod ordering; marker doc claims (ephemeral, not persisted, no continuation admission) vs code (pure data type, no behavior); test helper tool_catalog_without_sleep correctness (strips only clock.sleep, drops clock namespace only if empty). No defects found."
  ]
}
```
