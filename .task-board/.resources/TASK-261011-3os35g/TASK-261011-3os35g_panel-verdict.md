# Panel B verdict — TASK-260929-2is91w CR-TASK-260929-2is91w-4 rev4 (R141, non-recording)

Replay: `git read-tree e0eff057620104a416080da616256ee7f32bda1b` + `git apply --cached`
of `TASK-260929-2is91w_change-request_rev4.patch` through a temporary index, then
`git write-tree` prints `523385e2bb27c606bd1cd7241b0825c77b7569e5` — exactly the
expected candidate tree. All candidate sources below were read from that pinned
tree (`git show` / `git archive`).

Commands run (all read-only; no cargo, just, build or test per the panel brief):

| Command | Exit |
|---|---:|
| `GIT_INDEX_FILE=$IDX git read-tree e0eff057…bda1b` | 0 |
| `GIT_INDEX_FILE=$IDX git apply --cached .temp/…_rev4.patch` | 0 |
| `GIT_INDEX_FILE=$IDX git write-tree` (= `523385e2…7569e5`) | 0 |
| `task-board resource get` ×9 (patch, surface-table, results, rev4-validation.log, hosted-precheck-11, producer-brief, rev3-verdict, mutants, handoff-note-11) | 0 |
| `git diff --stat` / `--shortstat` base..candidate (21 files, +2398/-6) | 0 |
| `git diff --stat f8ae8558..523385e2` (rev3→rev4: exactly 3 files) | 0 |
| `git diff --check` base..candidate (clean) | 0 |
| `git diff --name-only … \| grep Cargo/lock/schema/template/prompts/md` (no match) | 1 |
| `git grep codex_goal/goal` over new core paths (no match) | 1 |
| 14/14 mutant patches `git apply --check` vs candidate file | 0 |
| `git archive` extractions of candidate sources/tests | 0 |

Verdict: accept

```verdict-findings
{
  "findings": [],
  "notes": [
    "[TASK-261011-3os35g] Independent non-recording panel B for CR-TASK-260929-2is91w-4 rev4. Replay is exact (see header). No accept/reject/status/handoff/note/resource write was made on TASK-260929-2is91w; all board reads and the single outcome attach in this run target TASK-261011-3os35g. No build or test command ran locally.",
    "[TASK-261011-3os35g] Execution attribution: accepted TASK-260929-2is91w_hosted-precheck-11.md (CI ivanopcode/codex run 38152963091, exact candidate tree 523385e2, lanes lint/small/core/app-server success, 14/14 named mutants killed, 0 survivors) and TASK-260929-2is91w_change-request_rev4-validation.log (mini-hosted-gate.sh exit 0, green hosted run on the exact tree). No hosted suite or mutant was rerun by this panel; raw hosted logs and per-test skip counts were not independently fetched. Mutant patch applicability (14/14 git apply --check clean) WAS verified locally against the extracted candidate file.",
    "[TASK-261011-3os35g] Rev3 findings A3-F1 (robustness) / D3-F1 (regression) are closed by this revision: discovered_waiting_tools_from_history now mirrors the normalizer ToolSearchOutput arm exactly (verified line-by-line against remove_orphan_outputs: whole-history Some-ID call set, drop only Some+non-server+unpaired, None always counts), with an extended server test, a new client-None unit test, a new server-null-ID integration test asserting for_prompt retention in the outbound request plus a None-to-Some capture transition, and a dedicated discovery_requires_server_call_id mutant killed on the exact tree by exactly those three tests.",
    "[TASK-261011-3os35g] Static source checks corroborate predicates and production routes, not executed Rust behavior. The remote-catalog entry-point attack and any further narrowing mutants beyond the attached 14 remain unexecuted. Hosted Linux conclusions do not independently establish macOS/Windows coverage; suite skips (notably skip_if_target_windows on the ack test) remain outside measured coverage.",
    "[TASK-261011-3os35g] Size: 21 changed files, +2398/-6, exceeding the 800-line guidance; the 1483-line unit-test module is the AC-mandated named-test matrix and the rev3-to-rev4 delta is confined to 3 files (+181/-37). Recorded as a note, not a blocking finding, consistent with prior rounds; no size exception is granted here.",
    "[TASK-261011-3os35g] TurnContextContributionInput gains a required public Rust reference field: source-breaking for out-of-tree struct-literal constructors. All in-repo constructors are updated and hosted lint on the exact tree is green. No app-server wire, CLI, config-schema, lockfile, template, prompt-text, or rollout change found in the 21-file diff. Noted, non-blocking, same as rev2/rev3.",
    "[TASK-261011-3os35g] update_plan_enabled replacement remains staged to the guidance leaf as the merged rev1/rev2 reviews accepted: runtime.rs call sites are untouched (file not in diff), steering.rs gains only the zero-fragment emitter, and no prompt bytes change in this leaf."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "attack": "Drop each host/opt-in/control/policy conjunct; force V1-only or V2-only native identity; substitute bare-name matching and nested/deferred counting.",
      "evidence": "derive_waiting_capabilities (waiting_capabilities.rs:43-81) matches the AC1 conjunctions line-for-line: sleep/stdin via is_callable, native_wait via registry identity plus provenance plus callability, exec_notify as host AND notify_on_exit schema AND stdin AND receipt control, native_mail_wait as host AND installed GoalBackgroundWaitAdmission. Exact-tree hosted precheck 11 kills all 10 flag/conjunct mutants with named tests (exec_notify_ignores_host/opt_in/stdin/receipt, native_mail_wait_ignores_host/policy, native_wait_v1_only/v2_only/bare_name_match, sleep_counts_nested_or_deferred, stdin_counts_nested); inspected mutant patches are genuine single-condition narrowings.",
      "finding_ids": [],
      "reported_by": "TASK-261011-3os35g"
    },
    {
      "row": "final-router derivation",
      "result": "held",
      "attack": "Attack undiscovered/deferred/nested/excluded tools, foreign wait provenance, orphan/mismatched discovery, stale discovery after exclusion, and supported server output with null call ID.",
      "evidence": "Discovery mirrors remove_orphan_outputs exactly (whole-history Some-ID set; drop only Some+non-server+unpaired; None counts), verified against normalize.rs:201-208. Exact-tree hosted kills: discovery_requires_server_call_id by server_tool_search_output_counts_without_call (Some+None loop), client_tool_search_output_without_call_id_counts_like_normalizer, and server_null_id_discovery_updates_waiting_capabilities (real Responses stream, asserts the null-ID definition inside outbound request 2 plus None-to-Some captures); regenerated discovery_ignores_call_pairing by the orphan/mismatched refusal tests. is_callable re-checks finalized deferred exposure so excluded/shadowed tools stay false (discovered_names_not_in_registry_still_yield_none); native_wait additionally requires registry provenance (foreign decoy tests).",
      "finding_ids": [],
      "reported_by": "TASK-261011-3os35g"
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "attack": "Arm a receipt through a real exec_command with notify_on_exit, observe the idle wake and subsequent sampling; inject pending/acknowledged providers without host controls.",
      "evidence": "Derivation reads AsyncNotificationSupport and GoalBackgroundWaitAdmission markers only — no receipt, mailbox, or pending-work state. Hosted suite acknowledged_subscription_does_not_flip_waiting_capabilities launches real exec with notify_on_exit=true, requires an armed receipt, waits for the completion wake, and asserts every captured snapshot equals the first with exec_notify true throughout; pending_and_acknowledged_work_does_not_flip_flags covers receipt-only refusal at unit level. native_mail_wait_ignores_policy is killed by the ack suite test among others.",
      "finding_ids": [],
      "reported_by": "TASK-261011-3os35g"
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "attack": "Look for recomputation, copies, independent initial/diff derivation, speculative-path divergence, and disconnected goal registration.",
      "evidence": "capture_step_context_inner derives once from the final router plus history scan and stores the value on StepContext (session/mod.rs:3973-3998); speculative capture delegates to the same inner function; both contributor call sites borrow &step_context.waiting_capabilities (session/mod.rs:4315 and 4413). Hosted same_snapshot_instance_reaches_both_context_paths drives real capture_step_context plus both production builders and asserts pointer identity (std::ptr::from_ref) and value equality across the two captures. GoalExtension registers as a prompt contributor and forwards the same borrowed reference to waiting_capability_fragments, which returns zero fragments.",
      "finding_ids": [],
      "reported_by": "TASK-261011-3os35g"
    },
    {
      "row": "configuration coverage",
      "result": "not-attacked",
      "attack": "Compare model catalog entry-point replacement with the snapshot tests; inspect hard/reminder off, headless, code-mode and receipt exclusions.",
      "evidence": "Four of five AC5 families have executed production-path attacks on the exact tree: snapshot_follows_sleep_switches (hard off, reminder off/on, goal-active), headless_exec_host_keeps_exec_but_disables_notification_flags, code_mode_only_hides_nested_waits_but_keeps_direct_sleep, excluded_receipt_tool_disables_exec_notify and excluded_exec_command_disables_exec_notify. snapshot_follows_catalog_clock_support drives production build_tool_router from resolved ModelInfo with/without clock, but edits the resolved state directly: no attached test fetches/replaces a remote entry through ModelsManager (apply_remote_models, pre-existing code outside this diff) and observes the snapshot.",
      "finding_ids": [],
      "reason": "Remote-catalog replacement through its actual entry point remains unknown; this is a fixture coverage bound, not the prohibition on local builds. The snapshot reads the catalog only via the final router, so the untested link is replacement-to-resolved-state, not snapshot derivation.",
      "requested_attack": {
        "test_file": "codex-rs/core/tests/suite/search_tool.rs or a dedicated waiting_capabilities suite (requested)",
        "command": "just test -p codex-core -E 'test(remote_catalog_replacement_changes_waiting_snapshot)'",
        "expected_failure": "NOT EXECUTED. Mock remote entries for the same bundled model slug removing/adding clock support through the real ModelsManager path, sample through the real session, record the snapshot, and require a mutant ignoring the remote replacement to fail. Other configuration legs have attached execution evidence."
      },
      "reported_by": "TASK-261011-3os35g"
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "attack": "Trace native ToolName heap bounds rather than trusting size_of; inspect persistence, serialization and prompt-history rewrites.",
      "evidence": "WaitingCapabilities is four booleans plus Option<ToolName> with no collections and no serde derives; snapshot_stays_small_and_bounded asserts size_of <= 128. Core-derived native names are bounded: fixed wait_agent/V1 names plus V2 namespace validated to at most 64 ASCII [a-zA-Z0-9_-] (config validate_multi_agent_v2_tool_namespace); foreign names cannot enter via the provenance gate, so the bound covers core-derived snapshots (the public type itself permits manual construction). Hosted waiting_snapshot_does_not_persist_to_history_or_rollout drives both production builders plus to_turn_context_item with a flipped snapshot and asserts byte equality; to_turn_context_item carries no snapshot field; goal emits no text.",
      "finding_ids": [],
      "reported_by": "TASK-261011-3os35g"
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "attack": "Trace contributor construction, plan-enabled behavior, dependency direction, module size and build wiring.",
      "evidence": "One exported extension-api type plus one borrowed input field; all in-tree constructors updated (registry.rs test, both session builders). Goal consumes the existing contributor contract; no core->goal dependency (grep-clean over new core paths). Core derivation is a focused 309-line module; registry tool_exposure widened from cfg(test) to pub(crate) is the only visibility change. No dependency/config/schema/template/wire change (name-only grep clean; diff --check clean). update_plan_enabled call sites untouched, preserving the existing prompt signal per the accepted staged scope.",
      "finding_ids": [],
      "reported_by": "TASK-261011-3os35g"
    }
  ],
  "free_hunt": [
    "[TASK-261011-3os35g] {\"budget\": \"After all seven rows: six adjacent concerns (rev3-fix sibling shapes, V1/V2 coexistence, stale discovery, loadable-spec parser gaps, speculative-path divergence, API/size/prompt wiring). No builds, product changes, or delegation.\", \"result\": \"No finding. Rev3 A3-F1/D3-F1 verified fixed with executed mutant proof; sibling shapes dismissed on inspected production constraints.\", \"coverage\": {\"surface_rows_swept\": 7, \"surface_rows_total\": 7, \"held\": 6, \"broken\": 0, \"not_attacked\": 1, \"hosted_named_mutants_killed\": 14, \"hosted_named_mutants_total\": 14, \"local_mutant_apply_check_clean\": 14, \"new_rust_runtime_attacks_executed_by_panel\": 0}, \"checks\": [\"None-ID outputs cannot desync from the normalizer (its arm requires Some, so it always retains them); the Some-ID pairing rule is unchanged from reviewed rev3 and now matches the normalizer's whole-history pass.\", \"native_wait_tool first-match has no realistic ambiguity: MultiAgentVersion is a single exclusive value (Disabled/V1/V2), so V1 and V2 native waits cannot co-register.\", \"Stale discovery is refused by the deferred-exposure re-check with a dedicated test (discovered_names_not_in_registry_still_yield_none); foreign wait_agent names in the discovered set are harmless via the provenance gate.\", \"Speculative capture delegates to capture_step_context_inner, so no independent derivation path exists.\", \"Waiting-relevant spec parsing covers function and namespace-child shapes; no supported production trigger was found for a missed waiting-tool shape (native waits are function handlers), so no finding is inferred.\", \"No new dependencies, schemas, wire payloads, templates, or compile-time assets; prompt bytes unchanged (goal emits zero fragments).\"], \"blind_spots\": [\"Remote replacement-to-snapshot observation has no attached entry-point test (row-level not-attacked with requested attack).\", \"Untested loadable-spec edge shapes and the deferred-exec_command-with-schema positive path have inspection evidence only, no dedicated narrowing mutants beyond the attached 14.\", \"Hosted outcomes are attached evidence; no raw logs, per-test skip audit, or new macOS/Windows execution.\", \"Discovery scans raw history per capture (linear); performance under very large histories was not measured — correctness only is claimed.\"], \"stop_condition\": \"Seven rows each have exactly one result, rev3 findings verified closed with executed proof, six adjacent concerns swept; no first-finding exit.\"}"
  ]
}
```
