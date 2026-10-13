# Panel B verdict — TASK-260929-2is91w CR-TASK-260929-2is91w-2 revision 2 (R141, non-recording)

Verdict: accept

Reviewer task: TASK-261011-2yj58v. This panel performed a read-only review: replay through a
temporary index plus a static attack over every surface-table row, with exact-candidate hosted
execution evidence cited per row. Nothing was written to TASK-260929-2is91w (reads only).

## Replay tree check

Base commit e0eff057620104a416080da616256ee7f32bda1b plus resource
TASK-260929-2is91w_change-request_rev2.patch writes tree ef4eb6ff644eee2a950b493b675fb86f7b3301c2,
which matches the expected candidate tree exactly. MATCH. Candidate files were read from that
tree only (git show / git archive); no worktree source was modified.

## Commands run (with exit codes)

- task-board m 'set_status(TASK-261011-2yj58v, status=analysis)' — exit 0
- task-board q 'get(TASK-260929-2is91w) { description scope ac }' — exit 0
- task-board q 'get(TASK-260929-2is91w) { outcomeResources preconditionResources }' — exit 0
- task-board resource get TASK-260929-2is91w surface-table.md — exit 0
- task-board resource get TASK-260929-2is91w producer-brief.md — exit 0
- task-board resource get TASK-260929-2is91w TASK-260929-2is91w_results.md — exit 0
- task-board resource get TASK-260929-2is91w TASK-260929-2is91w_mutants.json — exit 0
- task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev2.patch — exit 0
- task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev2-validation.log — exit 0
- task-board resource get TASK-260929-2is91w TASK-260929-2is91w_hosted-precheck-8.md — exit 0
- task-board resource get TASK-260929-2is91w TASK-260929-2is91w_handoff-note-8.md — exit 0
- task-board resource get TASK-260929-2is91w TASK-260929-2is91w_review-verdict-rev1.md — exit 0
- git rev-parse --show-toplevel (HEAD equals the CR base) — exit 0
- GIT_INDEX_FILE=$IDX git read-tree e0eff057620104a416080da616256ee7f32bda1b — exit 0
- GIT_INDEX_FILE=$IDX git apply --cached .temp/TASK-260929-2is91w_change-request_rev2.patch — exit 0
- GIT_INDEX_FILE=$IDX git write-tree (printed ef4eb6ff644eee2a950b493b675fb86f7b3301c2) — exit 0
- git archive ef4eb6ff644eee2a950b493b675fb86f7b3301c2 <10 candidate paths> | tar -x -C .temp/TASK-261011-2yj58v-cand — exit 0
- git show / git diff / git grep read-only inspection of the candidate tree — exit 0
- No cargo, just, build, or test command was run (forbidden by the panel brief; the shared
  build target is serialized). Execution evidence is the CR validation log (mini-hosted-gate
  exit 0 in TASK-260929-2is91w_change-request_rev2-validation.log) and hosted precheck 8
  (relux-ci run 38092565667 on the exact candidate tree, all lanes green, 12/12 mutants killed).
- No accept_cr, reject_cr, withdraw_cr, set_status, or handoff was run on TASK-260929-2is91w.

## Review method

Every surface-table row received exactly one attack result. Hosted precheck 8 executed on the
EXACT candidate tree (snapshot worktree tree ef4eb6ff, confirmed by mini-hosted-gate exit 0),
so its lane results and mutant kills count as executed public-entry attacks and are cited as
such. Static attacks below trace the production mechanism end to end; no row was marked
not-attacked on build-availability grounds.

```verdict-findings
{
  "findings": [],
  "notes": [
    "[TASK-261011-2yj58v] Evidence identity: replay is exact (ef4eb6ff), and hosted precheck 8 ran on that exact tree: run 38092565667, lanes lint/small/core/app-server success, 12/12 mutants killed with named killers. This closes the rev1 evidence-identity limitation; 7/7 rows have exact-candidate runtime support where a runtime leg exists.",
    "[TASK-261011-2yj58v] Rev1 regressions closed: A-F1 (bare-name native wait) is fixed by registry-provenance selection (CoreToolRuntime::is_native_wait_tool, true only in V1/V2 handlers plus the delegating V2 wrapper) and killed on the exact tree by native_wait_bare_name_match via three foreign/decoy tests. A-F2 (discovered tools invisible) is fixed by discovered_waiting_tools_from_history plus deferred-aware is_callable and killed by native_wait_ignores_discovered via the synthetic and production-capture discovered-V1 tests, including a false-before/true-after production-capture leg built through the real to_loadable_spec conversion.",
    "[TASK-261011-2yj58v] Change size 1990 insertions / 6 deletions across 20 paths exceeds the 800-line guidance; 1359 lines are the AC-mandated named-test matrix in waiting_capabilities_tests.rs and 275 are the new derivation module. Mechanical-test overrun in the same accepted pattern as rev1; production deltas outside the new module are small and additive.",
    "[TASK-261011-2yj58v] update_plan_enabled replacement staged: runtime.rs call sites are byte-identical to base and steering.rs continuation rendering is untouched (only additive waiting_capability_fragments returning empty). Zero behavior loss; the literal scope replacement stays deferred to the guidance leaf TASK-260929-1w5ivu per the boundary both rev1 panels accepted.",
    "[TASK-261011-2yj58v] Remote-catalog residual: snapshot_follows_catalog_clock_support proves both ModelInfo clock legs through the production router builder, and remote/bundled replacement itself is pre-existing models-manager behavior with its own suite (manager_tests.rs) untouched by this CR, but no single test chains a mocked remote fetch into a sampling snapshot. The candidate has no catalog input and no mechanism to ignore remote entries, so the row holds; the chained test is named here as a non-blocking evidence gap.",
    "[TASK-261011-2yj58v] V2 namespace length bound: tool_namespace config validates charset plus the reserved functions name but sets no length cap, so native_wait heap is bounded by operator config rather than a constant. Accepted: single transient string, never persisted, operator-controlled input only; foreign/dynamic namespaces can no longer reach the snapshot after the A-F1 fix.",
    "[TASK-261011-2yj58v] No model-context injection: the goal contributor returns an empty fragment list for every snapshot value (steering test covers none() and full), both session paths push only returned fragments, and no prompt text, template, or rollout/history schema changed. No item over 1k tokens is introduced.",
    "[TASK-261011-2yj58v] TurnContextContributionInput gains a required waiting_capabilities reference: source-breaking for Rust struct-literal constructors. All in-repo constructors are updated (both session paths, extension-api registry test, core recording tests) and hosted lint on the exact tree is green. No app-server wire, CLI, config, or session-resume surface changes: the 20-path diff touches only core session/tools, extension-api, goal, and tests."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "finding_ids": [],
      "reason": "All five AC1 derivations match exactly: sleep/stdin are callable (direct or deferred-plus-discovered); native_wait requires registry native provenance plus callability and carries the actual ToolName; exec_notify conjoins host, notify_on_exit schema (with deferred-registry fallback), stdin, and receipt control; native_mail_wait conjoins host and installed policy. Foreign wait_agent decoys and disabled-V2 decoys yield None.",
      "attack": "Conjunct-by-conjunct narrowing review plus provenance substitution (foreign dynamic wait_agent with native disabled; namespaced decoy with V2 wait disabled; custom V2 namespace positive control).",
      "evidence": "waiting_capabilities.rs:43-81,167-271; router.rs:225-236 native_wait_tool; registry.rs:91 default-false provenance with true only in V1/V2 handlers and the delegating wrapper. Hosted exact-tree: 12/12 mutants killed, including bare_name_match (5 killers), ignores_discovered, v1_only, v2_only, all four exec_notify narrowings, both mail narrowings, and both sleep/stdin nested narrowings.",
      "reported_by": "TASK-261011-2yj58v"
    },
    {
      "row": "final-router derivation",
      "result": "held",
      "finding_ids": [],
      "reason": "Derivation reads the finalized router after exclusions and collisions: excluded or shadowed tools are absent from the registry and yield false even when named in discovery history; deferred tools count only when discovered; nested-only code-mode tools never count. Discovery parsing mirrors the handler normalization (namespace wrap, default-namespace plain names, malformed values yield nothing).",
      "attack": "Exclusion/collision substitution (ToolPolicy-allowed lists; history names without registry entries), deferred boundary in both directions (undiscovered false, discovered true), and nested-only code-mode routers.",
      "evidence": "waiting_capabilities.rs:91-202; tool_search.rs normalize_search_spec (Function/Freeform wrapped in default namespace) matching tool_names_from_loadable_value. Hosted exact-tree: discovered_v1_wait_updates_next_step_snapshot (production capture false-before/true-after via real to_loadable_spec), discovered_names_not_in_registry_still_yield_none, deferred_sleep legs, excluded_exec_command/excluded_receipt tests, and the ignores_discovered plus sleep/stdin narrowing kills.",
      "reported_by": "TASK-261011-2yj58v"
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "finding_ids": [],
      "reason": "derive_waiting_capabilities inputs are the final router, model-visible specs, discovered history names, and the thread-store host/policy markers only. No PendingWorkProvider, receipt, mailbox, or acknowledgement state is read, so arming or acknowledging a subscription cannot flip any flag.",
      "attack": "Input/data-flow audit of derive plus armed-versus-unarmed comparison: synthetic provider-present/provider-absent snapshots and a real end-to-end exec launch with notify_on_exit asserting an armed receipt and equal pre/post-arm snapshots.",
      "evidence": "waiting_capabilities.rs:43-81 (input list); pending_and_acknowledged_work_does_not_flip_flags; suite acknowledged_subscription_does_not_flip_waiting_capabilities (exec_notification.rs). Hosted exact-tree core green, and the suite test kills the native_mail_wait_ignores_policy mutant, proving it executes rather than skips.",
      "reported_by": "TASK-261011-2yj58v"
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "finding_ids": [],
      "reason": "capture_step_context_inner derives once per step (history scan under a block-scoped lock, released before derive) and stores the result on StepContext; both build_turn_context_contribution_items and build_initial_context_with_world_state borrow &step_context.waiting_capabilities. GoalExtension is registered as a prompt_contributor and forwards that same reference to its renderer. No per-path recomputation or clone exists.",
      "attack": "Allocation-to-borrow trace through capture, StepContext ownership, both contribution constructors, prompt_contributor registration, and the goal renderer; pointer-identity plus value-equality assertion across both paths.",
      "evidence": "session/mod.rs capture block plus both waiting_capabilities borrow sites; step_context.rs field; extension-api registry.rs:113-114 prompt_contributor push; goal extension.rs ContextContributor impl. Hosted exact-tree: same_snapshot_instance_reaches_both_context_paths green.",
      "reported_by": "TASK-261011-2yj58v"
    },
    {
      "row": "configuration coverage",
      "result": "held",
      "finding_ids": [],
      "reason": "Hard sleep disable wins; reminder on/off legs plus goal-active leg behave; catalog clock support flows both directions through the production router builder; headless/exec (missing or Unavailable host) keeps stdin while disabling both notification flags; code-mode nests write_stdin (false) while keeping direct sleep (true); ToolPolicy-excluded receipt and exec tools disable exec_notify. Remote replacement is upstream pre-existing behavior the candidate consumes via ModelInfo with no bypass mechanism.",
      "attack": "Production-router matrix over sleep switches, catalog clock legs, host markers, code-mode nesting, and ToolPolicy exclusions; mechanism check that the candidate has no catalog input to ignore.",
      "evidence": "snapshot_follows_sleep_switches, snapshot_follows_catalog_clock_support, headless_exec_host_keeps_exec_but_disables_notification_flags, available_host_with_policy_enables_notification_flags, code_mode_only_hides_nested_waits_but_keeps_direct_sleep, excluded_receipt_tool_disables_exec_notify, excluded_exec_command_disables_exec_notify. Hosted exact-tree core green. Residual chained remote-fetch test named in notes, non-blocking.",
      "reported_by": "TASK-261011-2yj58v"
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "finding_ids": [],
      "reason": "Four bools plus Option<ToolName>, no collections, size_of<=128 asserted; native_wait is restricted to genuine native identities (fixed V1 name or operator-configured V2 namespace) after the A-F1 fix. Nothing persists: to_turn_context_item is untouched, the type has no Serialize, and changing only the snapshot leaves both context outputs and the turn item identical.",
      "attack": "Heap-ownership follow (ToolName sources into native_wait), size assertion, and persistence-diff test flipping every snapshot field while running both production context paths plus turn-item conversion.",
      "evidence": "extension-api waiting_capabilities.rs struct; snapshot_stays_small_and_bounded; waiting_snapshot_does_not_persist_to_history_or_rollout; app-server 64-char dynamic-namespace cap no longer reachable via the snapshot. Hosted exact-tree small and core lanes green. V2 operator-config length bound accepted in notes.",
      "reported_by": "TASK-261011-2yj58v"
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "finding_ids": [],
      "reason": "Minimal extension-api surface (one snapshot type plus one input reference); derivation isolated in a 275-line core module; goal receives the snapshot through ContextContributor with no core-to-goal dependency (no Cargo.toml changes) and no wire/CLI/config/rollout changes; update_plan_enabled behavior is untouched with zero loss while its replacement stays explicitly staged.",
      "attack": "Changed-path audit (20 paths, all within core session/tools, extension-api, goal, tests), dependency-direction check, contributor-registration verification, and call-site byte comparison for the staged pass-through.",
      "evidence": "Diff stat 20 files; runtime.rs untouched; steering.rs additive-only renderer returning empty; install_with_backend_and_clock prompt_contributor registration; goal renderer test for none() and full snapshots. Hosted exact-tree lint/small/app-server green.",
      "reported_by": "TASK-261011-2yj58v"
    }
  ],
  "free_hunt": [
    {
      "area": "exec_command namespace shadow",
      "outcome": "dismissed",
      "detail": "specs.find(spec.name() == exec_command) could theoretically match a same-named namespace before the function and return false. Requires a namespace literally named exec_command surviving finalization alongside the function; no realistic trigger. Same conclusion as rev1 panel B."
    },
    {
      "area": "ToolSearchOutput status unchecked in history scan",
      "outcome": "dismissed",
      "detail": "discovered_waiting_tools_from_history scans every ToolSearchOutput item without checking status. Handler error paths return Err or empty tools (tool_search.rs: empty query, zero limit, empty index), so only successful searches emit spec-carrying outputs; the deferred-registry re-check backstops any stray name."
    },
    {
      "area": "stale discovery across plan changes",
      "outcome": "dismissed",
      "detail": "Old ToolSearchOutput items persist in history across model or config changes, but every discovered name is re-checked against the current finalized registry exposure, so post-discovery exclusions, collisions, and removals still yield false. Covered by discovered_names_not_in_registry_still_yield_none."
    },
    {
      "area": "dual V1 plus V2 native registration",
      "outcome": "dismissed",
      "detail": "native_wait_tool uses registry .find(); multi_agent_version is a single enum (Disabled/V1/V2) and collab registration branches on it, so at most one native wait runtime exists per plan and selection is deterministic."
    },
    {
      "area": "history lock scope during capture",
      "outcome": "held",
      "detail": "The state lock is held only for the synchronous raw_items scan inside a block scope and released before derive_waiting_capabilities runs; no await under the held guard and no deadlock shape."
    },
    {
      "area": "prompt-byte neutrality of the new contributor",
      "outcome": "held",
      "detail": "Both session paths push only per returned fragment with no per-contributor markers, and goal waiting_capability_fragments returns empty for every snapshot value. Registration cannot change prompt bytes; confirmed by the steering renderer test and the non-persistence test."
    },
    {
      "area": "speculative step contexts",
      "outcome": "held",
      "detail": "capture_speculative_step_context funnels through capture_step_context_inner, so speculative steps derive the same way and share the same StepContext ownership; no second derivation path exists."
    }
  ]
}
```
