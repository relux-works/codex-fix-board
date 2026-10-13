# Panel verdict — R141 panel B, CR-TASK-260929-2is91w-1 rev1 (TASK-261010-3syszw)

Verdict: accept

## Replay tree check: MATCH

Base e0eff057620104a416080da616256ee7f32bda1b + patch
TASK-260929-2is91w_change-request_rev1.patch through a temporary index
reproduces exactly the candidate tree
fc18da8f7415a89029a6a0e7bc539e107749984a.

## Commands run (all read-only; no cargo/just/build per brief) with exit codes

- GIT_INDEX_FILE read-tree <base> → exit 0
- GIT_INDEX_FILE apply --cached <patch> → exit 0
- GIT_INDEX_FILE write-tree → fc18da8f7415a89029a6a0e7bc539e107749984a, exit 0
- git diff --stat <base> <candidate> → 15 files, +1448/-4, exit 0
- git archive <candidate> (production + test files) → exit 0
- git diff --name-only <green-09975fe> <candidate> → exactly 8 trunk files
  (arg0/cli/exec), exit 0; same diff scoped to codex-rs/core + codex-rs/ext
  → empty, exit 0
- git log -1 d124f818544fdf41b5e5fb2c29e4bcbd27571bca → tree 09975fe…, exit 0
- 10/10 mutant patches git apply --check clean against candidate bytes, exit 0
- 36/36 coverage-map test names present in candidate, no missing, exit 0
- structural greps: codex_goal in core diff → 0; Serialize in snapshot → 0;
  runtime.rs in patch → 0, exit 0

## Key aspects

Every surface-table row held. The derivation matches AC1 conjunct-for-conjunct
and reads the finalized router after exclusions/collisions; subscriptions
cannot reach any flag (inputs are router + thread store only); one stored
instance is shared by reference at both context paths with pointer-equality
proof; the update_plan_enabled signal is untouched so there is no behavior
loss, with call-site migration explicitly deferred to the guidance leaf.
Hosted precheck 4 (run 38040774172, all lanes green, 10/10 narrowing mutants
killed) executed on byte-identical task files; the only in-build-closure
dependency delta versus the candidate is additive-only arg0 code.

```verdict-findings
{
  "findings": [],
  "notes": [
    "update_plan_enabled replacement deferred: the scope asks to replace the pre-sampling pass-through, but the snapshot carries no plan-enabled field and replacement would change prompt text, which the same scope forbids. The producer documented the deferral to TASK-260929-1w5ivu with the vehicle and receiving end in place and zero behavior loss (call sites byte-identical). Treated as an accepted scope boundary, not a defect.",
    "Hosted evidence transfer: precheck 4 (run 38040774172) executed on snapshot tree 09975fe220479764649c9eb740f6d71f209d457e (commit d124f818544fdf41b5e5fb2c29e4bcbd27571bca verified locally); the candidate differs by exactly 8 committed-trunk files under arg0/cli/exec with an empty core/ext delta, so all 15 task files are byte-identical to the green run. The only in-build-closure dependency delta is codex-arg0 (via core/tests/common and app-server), whose delta is additive-only (new silent_exit module plus re-exports); no existing API behavior changed. Residual risk negligible.",
    "Change size +1448/-4 across 15 files exceeds the 800-line guidance; about 1012 lines are the AC-mandated named-test matrix plus refusal tests and mutant killers, with production logic around 200 lines. Mechanical-test overrun, accepted."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "evidence": "Derivation (core/src/tools/waiting_capabilities.rs:35-60) matches AC1 conjunct-for-conjunct: sleep is direct clock.sleep, stdin is direct write_stdin, native_wait carries Some(actual ToolName) for wait_agent in Function/Freeform/any-namespace specs (covers V1 multi_agent_v1 and V2 configured-or-plain), exec_notify is host AND notify_on_exit schema AND stdin AND exec_notification, native_mail_wait is host AND installed GoalBackgroundWaitAdmission. Hosted core lane green with named driving and refusal tests per flag; 10/10 narrowing mutants killed, one AND-condition dropped each. Static check: is_directly_visible mirrors the direct branch of ToolRouter::exposes_tool exactly."
    },
    {
      "row": "final-router derivation",
      "result": "held",
      "evidence": "Production chain capture_step_context (session/mod.rs:3971) via turn::built_tools and build_tool_router into finalize_tool_router (ToolPolicy allowlist plus collision resolution) runs before the model_visible_specs read, so excluded and shadowed tools are absent at derivation. Nested-only and deferred tools are excluded structurally (code_mode_tool_names and the deferred registry are never consulted; ToolSearch specs return false). Covered by deferred/nested/excluded tests on synthetic and production routers plus the nested/deferred mutant kills. Hosted core lane green."
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "evidence": "Derivation inputs are (&ToolRouter, &ExtensionData) only, so receipts, mailbox entries, and pending-work state cannot flip any flag. Unit test pending_and_acknowledged_work_does_not_flip_flags plus suite end-to-end acknowledged_subscription_does_not_flip_waiting_capabilities (real notified exec, acknowledged receipt, idle wake; every captured snapshot equal with exec_notify true). Hosted core lane green."
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "evidence": "One instance derived at capture, stored on StepContext, shared by reference at both context paths (session/mod.rs:4308 and 4406). same_snapshot_instance_reaches_both_context_paths drives production capture_step_context and both production builders and asserts pointer-address equality plus value equality. Goal ContextContributor is registered (prompt_contributor takes Arc<dyn ContextContributor>) and the goal renderer test proves receipt with no prompt text. Hosted green."
    },
    {
      "row": "configuration coverage",
      "result": "held",
      "evidence": "Five production-router matrix tests through build_tool_router: snapshot_follows_catalog_clock_support (remote catalog), snapshot_follows_sleep_switches (hard/reminder off), headless_exec_host_keeps_exec_but_disables_notification_flags (absent marker and explicit Unavailable), code_mode_only_hides_nested_waits_but_keeps_direct_sleep, excluded_receipt_tool_disables_exec_notify. Hosted core lane green."
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "evidence": "Five small fields (bool, bool, Option<ToolName>, bool, bool), no Serialize impl, size_of below 128 asserted. waiting_snapshot_does_not_persist_to_history_or_rollout flips none() to all-true and asserts both context paths plus to_turn_context_item byte-identical (to_turn_context_item untouched). StepContext-scoped and dropped after the request. Hosted green."
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "evidence": "extension-api delta is additive (new module, re-export, one reference field; input stays Copy). No core-to-goal reference in the core diff. update_plan_enabled call sites byte-identical (runtime.rs untouched, steering.rs additive-only new function), so no behavior loss and no prompt-text change; call-site migration is explicitly deferred to the guidance leaf. Goal contributes empty fragments at every contribution point and both context paths push per-fragment with no per-contributor artifacts, so registration is prompt-byte-neutral. Hosted lint/small/app-server/core lanes green."
    }
  ],
  "free_hunt": [
    {
      "area": "goal contributor wiring",
      "outcome": "held",
      "detail": "prompt_contributor pushes Arc<dyn ContextContributor> into context_contributors (registry.rs:113), so goal contribute_turn_context runs at both paths; verified, not assumed."
    },
    {
      "area": "prompt-byte neutrality of the new contributor",
      "outcome": "held",
      "detail": "Both paths push only per returned fragment with no separators or per-contributor markers; goal returns empty at thread, turn, and world-state points (trait defaults plus the empty renderer). Registration cannot change prompt bytes."
    },
    {
      "area": "native_wait namespace breadth",
      "outcome": "held",
      "detail": "Any-namespace matching is required because V2 namespaces are dynamically configured (spec_plan.rs:737), and the actual ToolName is carried so guidance names a real callable tool. V1/V2 distinction is pinned by namespaced-name tests plus the v1_only/v2_only mutant kills."
    },
    {
      "area": "exec_command shadow order",
      "outcome": "dismissed",
      "detail": "find() on spec.name() could theoretically hit a same-named namespace before the function; requires an MCP namespace literally named exec_command surviving finalization. No realistic trigger."
    },
    {
      "area": "native_mail_wait production reachability",
      "outcome": "held",
      "detail": "Goal runtime inserts admission_checker into the thread store on background-wait continuation (runtime.rs:668), enabled only when the host is available (extension.rs:183). The flag can be true in production and is false without an installed goal (suite asserts)."
    },
    {
      "area": "test-helper consistency",
      "outcome": "held",
      "detail": "StepContext::for_test uses none() matching its empty router; with_tool_router_for_test re-derives tool flags with default-off markers. Test-only; production capture untouched."
    }
  ]
}
```
