# Panel B verdict — TASK-260929-2is91w CR-TASK-260929-2is91w-5 rev5 (R141, non-recording)

Panel task: TASK-261012-r3lg2l. Review target: revision 5 of TASK-260929-2is91w, base e0eff057620104a416080da616256ee7f32bda1b, expected candidate tree afb8c830d764ba489a9f2f922c0babdf1dbe036e.
No accept/reject/status/handoff/note/resource write was made on TASK-260929-2is91w in this run. No cargo, just, or any build or test command ran locally (shared-target prohibition in the panel brief).

Replay tree check: PASS. Temporary-index replay of TASK-260929-2is91w_change-request_rev5.patch on the base prints afb8c830d764ba489a9f2f922c0babdf1dbe036e, exactly the expected candidate tree.

Commands run with exit codes (all read-only; no builds):

- task-board m 'set_status(TASK-261012-r3lg2l, status=analysis)' — exit 0
- GIT_INDEX_FILE=$IDX git read-tree e0eff057620104a416080da616256ee7f32bda1b — exit 0
- task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev5.patch — exit 0
- GIT_INDEX_FILE=$IDX git apply --cached rev5.patch — exit 0
- GIT_INDEX_FILE=$IDX git write-tree → afb8c830d764ba489a9f2f922c0babdf1dbe036e — exit 0
- task-board resource get (surface-table, producer-brief, results, mutants, rev5-validation.log, hosted-precheck-14/12/11, handoff-note-14/11, handoff-precheck-14-logbook, rev4 verdicts, rework briefs, loop-response, orch fixes, rev4 patch) — exit 0 each
- rev4 control replay: read-tree base + apply rev4 patch + write-tree → 523385e2bb27c606bd1cd7241b0825c77b7569e5 (matches recorded rev4 tree) — exit 0
- git diff rev4-tree rev5-tree --stat → 1 file, search_tool.rs +221 — exit 0
- git diff precheck12-tree(b9982d79) precheck14-tree(afb8c830) --stat → 1 file, search_tool.rs +80/-7 — exit 0
- git diff base candidate --stat → 21 files +2619/-6; models-manager diff empty; scenarios diff empty; grep -ci guardian rev5.patch → 0 matches — exit 0/1-as-expected
- git apply --stat rev5.patch piped to grep for Cargo/BUILD/bazel/schema/github/docs/README → no match — exit 1-as-expected
- 15/15 mutant patches GIT_INDEX_FILE=candidate-tree git apply --cached --check — exit 0 each
- git archive extracts of candidate files + git show of candidate config/mod.rs — exit 0
- gh run view 38152963091 (precheck 11) jobs + snapshot-core log grep for encrypted_parent_reply — exit 0
- gh run view 38191980780 (precheck 14) jobs + mutant-15 core log grep for remote_catalog_replacement — exit 0

One-word verdict: accept

Row sweep (7/7, every row attacked afresh on this revision; full detail in the verdict-findings block below):

- flag derivation: held — AC1 conjunctions in source; all 10 flag/conjunct narrowing mutants killed on the exact tree.
- final-router derivation: held — normalizer orphan rule matched line-by-line; both discovery mutants killed incl. server-null-ID public-entry tests.
- subscriptions are not capabilities: held — real-exec armed-receipt attack with whole-snapshot equality; derivation reads host/policy markers only.
- one snapshot, both paths: held — single derive, both paths borrow the same instance; pointer-identity test over both production builders.
- configuration coverage: held — 5/5 families; remote leg drives real /models fetch + apply_remote_models + real session on both branches, with merge-proof assertions and a raw-log-verified mutant kill.
- bounded and transient: held — 4 bools + Option<ToolName>, no serde/collections; V2 namespace ≤64 ASCII validated; non-persistence proven over both production builders.
- API surface and placement: held — one new type + one borrowed input field; no core→goal dep; additive-only goal change; no wire/build/schema surface.

```verdict-findings
{
  "findings": [],
  "notes": [
    "[TASK-261012-r3lg2l] Independent non-recording panel B for CR-TASK-260929-2is91w-5 rev5. Replay is exact (see header). No write of any kind was made on TASK-260929-2is91w; all board reads served this review and the single outcome attach targets TASK-261012-r3lg2l. No build or test command ran locally.",
    "[TASK-261012-r3lg2l] Execution attribution: accepted TASK-260929-2is91w_hosted-precheck-14.md (CI ivanopcode/codex run 38191980780, exact candidate tree afb8c830, lanes lint/small/core/app-server success, 15/15 named mutants killed) and TASK-260929-2is91w_change-request_rev5-validation.log (mini-hosted-gate.sh exit 0 on the exact tree). Independently verified via gh: 4/4 snapshot lane jobs success on the rerun (snapshot core job 114648017069), 15/15 mutant core jobs failure with 15/15 mutant small jobs success, mutant-15 core raw log shows remote_catalog_replacement_changes_waiting_snapshot TRY 1 FAIL panicking at search_tool.rs:1303 (whole-snapshot assert) with TRY 2 FAIL (deterministic kill, not flaky). No hosted suite or mutant was rerun by this panel. Mutant patch applicability (15/15 git apply --cached --check clean) WAS verified locally against the exact candidate tree.",
    "[TASK-261012-r3lg2l] Guardian flake attribution CONFIRMED from primary evidence, not inferred: (1) rev5 patch contains zero guardian bytes and base→candidate diff touches no scenarios/ file; (2) precheck12→precheck14 delta is test-only search_tool.rs +80/-7, so no production or guardian change sits between the pass and the first-attempt failure; (3) precheck-14 record: same-snapshot rerun passed the guardian test in 1.6s with core 5122/5122, and rerun job 114648017069 is success; (4) raw precheck-11 snapshot-core log (job 114512075377) shows the identical signature on this base: encrypted_parent_reply_survives_incremental_guardian_reviews TRY 1 FAIL at 10.338s, RETRY, TRY 2 PASS at 1.223s, FLAKY 2/3. Same-tree fail-then-pass plus a prior identical flake on this base establishes a base flake; the CR is exonerated.",
    "[TASK-261012-r3lg2l] Rev4→rev5 delta is exactly codex-rs/core/tests/suite/search_tool.rs +221 (test-only; verified by tree diff). All rev4 production-code conclusions carry over unchanged, and prior merged findings A3-F1/D3-F1 (server-null discovery parity) remain closed: the production files they cover are byte-identical to the unanimously accepted rev4, and precheck 14 re-kills discovery_requires_server_call_id with the same three tests.",
    "[TASK-261012-r3lg2l] Configuration row direct attack (the rev4 recording refusal, now closed): Hide visibility forces remote_only false (verified against apply_remote_models source: no List entry means the any-List conjunct is false, so the merge branch runs while dummy ChatGPT auth keeps refresh true), and the merge-proof assertions (catalog size equals bundled size, bundled-only slug survives, replaced entry carries remote Hide visibility plus exact remote tools) pin the branch so a silent fallback to remote-only fails loudly. The mutant (merge assignment → let _ = (index, model)) is killed through two independent paths: the whole-snapshot assert at :1303 and the replaced-entry visibility/tools asserts. The List (remote-only) legs cannot kill this mutant by construction — the mutated line never executes there — which is correct narrowing behavior, not a gap; those legs carry their own narrowing proof via stdin_counts_nested (remote test listed as killer) and passing snapshot-follows-remote plus request-tools asserts. Request counts asserted: exactly 1 /models GET + 1 /responses POST per case (4+4 total). Candidate production code in ModelsManager is unchanged (tree diff empty).",
    "[TASK-261012-r3lg2l] Static source checks corroborate predicates and production routes, not executed Rust behavior beyond the cited hosted evidence. Hosted Linux conclusions do not independently establish macOS/Windows execution; the ack suite test skips Windows/sandbox/no-network by design, so the subscriptions row is Linux hosted evidence with a stated platform bound.",
    "[TASK-261012-r3lg2l] Size: 21 files, +2619/-6, exceeding the 800-line guidance; the 1483-line unit-test module is the AC-mandated named-test matrix and the rev4→rev5 delta is a confined +221 test-only addition. Recorded as a note, not a blocking finding, consistent with prior rounds; no size exception is granted here.",
    "[TASK-261012-r3lg2l] TurnContextContributionInput gains a required public Rust reference field: source-breaking for out-of-tree struct-literal constructors. All in-repo constructors are updated and hosted lint on the exact tree is green. No app-server wire, CLI, config-schema, lockfile, template, prompt-text, or rollout change found in the 21-file diff. update_plan_enabled replacement remains staged to the guidance leaf as previously accepted: runtime.rs untouched (not in diff), steering.rs gains only the zero-fragment emitter. Noted, non-blocking, same as prior rounds.",
    "[TASK-261012-r3lg2l] Free-hunt coverage record (kept in notes per the panel brief; free_hunt holds only real findings, of which there are none): (a) six adjacent concerns swept after all seven rows — V1/V2 native-identity coexistence via exclusive MultiAgentVersion plus V1-only/V2-only killed mutants, stale-discovery refusal via the deferred-exposure re-check with its dedicated test, foreign wait_agent names refused by the runtime-provenance gate (default false, true only in the three native runtimes), speculative-capture delegation to capture_step_context_inner (single derivation path), loadable-spec parser shapes (function + namespace children; malformed values yield nothing), and discovery history-scan scratch (transient Vec/HashSets, not persisted or model-injected); (b) no new narrowing-mutant shape or bypass established in any of them; (c) no prompt-text change anywhere (goal emits zero fragments), so no model-visible item crosses token bounds; (d) no second derivation, persistence, or contributor path found. Coverage: 7/7 rows swept, held 7, broken 0, not-attacked 0; 15/15 mutants killed on the exact tree with 1 raw kill log inspected for the decisive mutant; 0 new local Rust attacks executed. Blind spots: installed-GoalExtension pointer identity is source-traced (registration + forwarding) rather than runtime-recorded; 14 mutant raw logs and small/app-server detailed logs accepted from the attached precheck record with job conclusions independently verified; no new macOS/Windows execution. Stop condition: every surface row attacked afresh with exactly one result, prior mechanism reassessed, six adjacent concerns swept; no first-finding exit. Logbook executable unavailable in this environment; this note carries the logbook-equivalent record.",
    "[TASK-261012-r3lg2l] Read-only original-task boundary maintained. All source, results, prechecks, and previous reviewer conclusions are inputs only. Panel attaches exactly one plain-text outcome to its own task."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "attack": "Drop each AND-conjunct (host, opt-in, stdin, receipt, policy); substitute V1-only/V2-only native identities; count nested-only tools, foreign wait decoys, or bare-name matches as native.",
      "evidence": "derive_waiting_capabilities (waiting_capabilities.rs:43-81) encodes the exact AC1 conjunctions; native_wait comes from registry runtime provenance (router.rs:231-236 first native runtime; registry.rs:91 default false, true only in V1/V2 wait handlers and the V2 namespace wrapper). Exact-tree precheck 14 kills all 10 flag/conjunct mutants (sleep, stdin, V1-only, V2-only, 4x exec_notify, 2x native_mail_wait) with named refusal/actual-name/decoy tests; bare-name and ignores-discovered native mutants killed by the provenance/discovery test set.",
      "finding_ids": [],
      "reported_by": "TASK-261012-r3lg2l"
    },
    {
      "row": "final-router derivation",
      "result": "held",
      "attack": "Feed unpaired/mismatched client outputs, server outputs with null/non-null IDs, client-null outputs, stale discovered names absent from the current registry, and deferred native tools; derive from a pre-exclusion list.",
      "evidence": "discovered_waiting_tools_from_history (waiting_capabilities.rs:101-142) collects whole-history Some-ID calls then drops exactly Some(id)+non-server+unpaired with None always counting — verified line-by-line identical to the remove_orphan_outputs ToolSearchOutput arm (normalize.rs:201-208). is_callable (:201-214) requires direct visibility or discovered-plus-current-deferred exposure, excluding nested-only and removed entries. Both discovery mutants killed on the exact tree by 5/3 named tests including the server-null-ID public-entry integration. Prior A3-F1/D3-F1 remain closed; production byte-identical to accepted rev4.",
      "finding_ids": [],
      "reported_by": "TASK-261012-r3lg2l"
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "attack": "Arm notify_on_exit through the real exec_command tool, acknowledge a receipt, wait for the idle wake, and compare snapshots before/after; install pending/acknowledged providers without capability controls.",
      "evidence": "acknowledged_subscription_does_not_flip_waiting_capabilities (exec_notification.rs:756-853) launches a real process with notify_on_exit, asserts an armed receipt handle, waits through the completion wake, and asserts whole-snapshot equality across all samples; pending_and_acknowledged_work_does_not_flip_flags covers the unit leg. Derivation reads only AsyncNotificationSupport and GoalBackgroundWaitAdmission, never receipt/mailbox state. Snapshot lane green on the exact tree; the ack test is also a listed killer for native_mail_wait_ignores_policy, proving it executes and asserts. POSIX-only by design (skips Windows/sandbox): Linux hosted evidence.",
      "finding_ids": [],
      "reported_by": "TASK-261012-r3lg2l"
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "attack": "Search for recomputation, copies, path-specific derivation, or missing goal registration; drive production capture plus both context builders with a pointer recorder.",
      "evidence": "capture_step_context_inner derives once after prepared tools (session/mod.rs:3971-3979, discovered scanned from raw history then derived from the final router); both context paths borrow &step_context.waiting_capabilities (:4315, :4413). same_snapshot_instance_reaches_both_context_paths drives production capture_step_context plus both production builders and asserts pointer identity (from_ref as usize) and value equality; green on the exact tree. GoalExtension::contribute_turn_context forwards input.waiting_capabilities (extension.rs:620-627) and registers as prompt_contributor (:767); goal forwarding is source-traced.",
      "finding_ids": [],
      "reported_by": "TASK-261012-r3lg2l"
    },
    {
      "row": "configuration coverage",
      "result": "held",
      "attack": "Drive the remote catalog through real fetch + apply_remote_models + real session on BOTH same-slug branches (remote-only replace and merge), asserting the snapshot follows the remote entry in both clock directions with request counts and merge-branch proof; attack hard/reminder switches, headless host, code-mode exposure, and receipt/exec exclusions.",
      "evidence": "remote_catalog_replacement_changes_waiting_snapshot (search_tool.rs:1342-1407) runs 4 cases: List remote-only add/remove plus Hide merge add/remove, each asserting 1 /models GET + 1 /responses POST, request tools following the remote entry, and whole-snapshot equality. Hide forces remote_only false (verified against manager.rs:672-702: no List entry defeats the any-List conjunct) and merge-proof asserts (bundled catalog size kept, bundled-only slug survives, replaced entry carries remote Hide visibility + exact remote tools) pin the branch. snapshot_ignores_remote_catalog_replacement killed on the exact tree by this test; raw mutant-15 core log shows TRY 1 FAIL panicking at :1303 with TRY 2 FAIL (deterministic). Other families: snapshot_follows_sleep_switches, headless_exec_host_keeps_exec_but_disables_notification_flags, code_mode_only_hides_nested_waits_but_keeps_direct_sleep, excluded_receipt_tool_disables_exec_notify — all green on the exact tree. 5/5 families attacked; AC5 row closed.",
      "finding_ids": [],
      "reported_by": "TASK-261012-r3lg2l"
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "attack": "Account for ToolName heap storage rather than trusting size_of; inspect serialization, turn persistence, and prompt/history emission for snapshot leakage.",
      "evidence": "WaitingCapabilities (extension-api/src/waiting_capabilities.rs:27-46) is four bools plus Option<ToolName> with no serde, no collections, and Clone/Debug/Eq only. Production native names are bounded: V1 namespace fixed, V2 custom namespace validated to at most 64 ASCII alnum/_/- characters (config/mod.rs:3148-3200). StepContext::to_turn_context_item omits the field (step_context.rs:51-56). waiting_snapshot_does_not_persist_to_history_or_rollout flips every snapshot field and asserts both production builder outputs unchanged; green on the exact tree. Goal emits zero fragments (steering.rs waiting_capability_fragments returns empty), so no new model-visible fragment exists.",
      "finding_ids": [],
      "reported_by": "TASK-261012-r3lg2l"
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "attack": "Trace in-tree contributor construction, native runtime wrappers, dependency direction, plan-enabled preservation, and external integration surfaces (wire, CLI, config, rollout, build).",
      "evidence": "One new exported extension-api type plus one borrowed contributor input field (context.rs:23); all in-repo constructors updated with hosted lint green on the exact tree. No core→goal dependency (derivation is a 309-line core-internal module; goal depends inward). update_plan_enabled call sites untouched: runtime.rs not in the 21-file diff, steering.rs diff is additive-only (zero-fragment emitter). No Cargo/BUILD/bazel/schema/CI/docs/README bytes in the patch (verified). Public Rust struct-field addition is source-breaking for out-of-tree literal constructors (noted, non-blocking, same as prior rounds).",
      "finding_ids": [],
      "reported_by": "TASK-261012-r3lg2l"
    }
  ],
  "free_hunt": []
}
```