# Panel B verdict — TASK-260929-csyzcj CR revision 5 (R141, non-recording)

Verdict: accept

## Replay tree check

Replayed `TASK-260929-csyzcj_change-request_rev5.patch` on base
`39c264c34e61b5171ae13b0f756746c24ea5f51a` through a temporary index
(`.temp/TASK-261011-2aph8r-replay.idx`; ordinary worktree index untouched).
`git write-tree` printed `b91072a51501101110a4e13061a8c07a242aad6a`, exactly the
expected candidate tree. No mismatch; review proceeded. Candidate files were read
via `git show <tree>:<path>` and a `git archive` extraction to
`.temp/TASK-261011-2aph8r-cand` (read-only; no nested worktree, no builds).

## Commands run with exit codes

- `task-board m 'set_status(TASK-261011-2aph8r, status=analysis)'` → exit 0
- `GIT_INDEX_FILE="$IDX" git read-tree 39c264c…` → exit 0
- `task-board resource get TASK-260929-csyzcj TASK-260929-csyzcj_change-request_rev5.patch` → exit 0 (132071 bytes)
- `GIT_INDEX_FILE="$IDX" git apply --cached <patch>` → exit 0
- `GIT_INDEX_FILE="$IDX" git write-tree` → exit 0, printed `b91072a51501101110a4e13061a8c07a242aad6a` (match)
- `git archive b91072a… | tar -x -C .temp/TASK-261011-2aph8r-cand` → exit 0
- `git apply --cached --check` for each of the 12 mutant patches against the candidate tree → all exit 0 (12/12 cohere)
- `python3` byte-bound recompute (marker 14 bytes; 270+270+682=1222) → exit 0
- `diff` of shared-parser grammar (base vs candidate) → identical apart from no functional line (exit 0 after trimming the capture artifact)
- No `cargo`, `just`, build or test command was run (panel brief forbids local builds; execution evidence is the hosted precheck cited below).
- No `accept_cr`, `reject_cr`, `withdraw_cr`, `set_status`, `handoff`, notes, resource, or checklist write was made on `TASK-260929-csyzcj` (reads only: `q` + `resource get`).

## Evidence identity

Hosted precheck 15 (`TASK-260929-csyzcj_hosted-precheck-15.md`): CI run 38109158922
snapshotted tree `b91072a51501101110a4e13061a8c07a242aad6a` with lint/small/core/app-server
all success and 12/12 narrowing mutants killed by named tests. The CR rev5 validation log
(404 bytes, untruncated) records `mini-hosted-gate.sh` exit 0 against that run with
`coverage_unit=exact_command_shard required=1 green=1`. Individual hosted command exit codes
and per-mutant run IDs are not supplied and remain unknown; no CI was rerun by this panel.
All 21 test names cited as killers in the precheck-15 table were verified present (`fn <name>`)
in the candidate tree.

```verdict-findings
{
  "findings": [],
  "notes": [
    "[rev4-findings-closed] Both rev3/rev4 bypass/regression findings are closed. (1) Legacy resume: the shared AgentPath parser (validate_agent_name, validate_absolute_path, validate_relative_reference) is byte-identical to base 39c264c (verified by diff); join/try_from/FromStr/serde accept every pre-cap identity unchanged. Length caps live only in join_new, called from exactly one production site (thread_spawn_source, multi_agents_common.rs:146). V1 spawn and resume_agent pass task_name None; V2 spawn builds spawn_source with ? (multi_agents_v2/spawn.rs:148) before agent_control.spawn, so refusal precedes thread creation. Real entry-point regressions drive resume_agent_from_rollout (resume_agent_preserves_legacy_overlong_path) and load_rollout_items/get_rollout_history with a raw-JSONL legacy fixture (get_rollout_history_preserves_legacy_agent_path). Narrowing mutants legacy_paths_rejected_by_shared_parser and legacy_long_path_rejected_by_shared_parser are killed hosted. (2) Model-context bound: to_model_input_item renders author/recipient through truncated_for_display in both plaintext and encrypted branches; stored routing identities asserted unchanged; whole-object assert_eq pins both branches (agent_message_envelope_truncates_legacy_paths_for_display); envelope_author_display_uncapped killed. Worst case independently recomputed: 270+270+682 = 1222 bytes (~306 tokens), under the 1K P0 threshold.",
    "[delta-scope] rev4 candidate 5a51cf52 to rev5 candidate b91072a is exactly 6 files (+364/-43): protocol agent_path.rs (uncapped parser + join_new + display truncation + 7 tests), protocol.rs (envelope render + 1 test), multi_agents_common.rs (one-word join to join_new), control_tests.rs (+72 resume test), recorder_tests.rs (+69 rollout test), goal_native_wait.rs (comment-only). All goal-wait mechanism files are byte-identical to rev4, so rev4 held-row mechanism evidence still applies; every row was re-swept against precheck-15 evidence anyway.",
    "[render-audit] All production model-visible AgentMessage renders funnel through to_model_input_item (session delivery session/mod.rs:4001, rollout_reconstruction.rs:427, rollout list.rs:1285, rollout_input.rs:47, memories phase1.rs). to_response_input_item has test-only callers. history.rs:1081 is a byte estimator (destructures author/recipient/content), confirming the 270+270+682 accounting basis. No production expect/unwrap on AgentPath parsing (input_queue.rs expects are inside mod tests at line 715+). resolve() callsites (target.rs, root_handoff.rs, control.rs:360, agent_message_board.rs) are routing lookups with mapped errors, never identity minting or persistence.",
    "[breaking-change-scan] No app-server API, CLI, or config change (no such paths in the 34-file CR). Serde schemas unchanged: AgentPath still try_from String, SessionSource/ThreadSpawn shapes unchanged, AgentMessage author/recipient still strings (values display-truncated only past 256 bytes). Resume of legacy rollouts is preserved, not broken. status.rs delta is tests-only (is_final untouched). Cargo.lock delta is the single intra-workspace codex-extension-items edge; MODULE.bazel.lock untouched (bazel-lock-update execution unknown, not reproduced — carried advisory).",
    "[coverage-ratio] Surface sweep 7/7 with exactly one result per row: held 7/7, broken 0/7, not-attacked 0/7. Hosted shipped mutants killed 12/12 per attached summary; local patch coherence 12/12. These are distinct measured ratios, not full AC subcase coverage. Producer-stated partial bounds stand: no dedicated live-child check-in reinsertion test, no exhausted-retention plus late-wake live test, no disable/stop interleave test, no full resume_thread_with_history with rendered SleepItem, no second-child-mid-turn or repeated-interrupt integration, no explicit non-default inherited-settings assert on the native path, AC6 reminder-enabled schedule by source inspection only, restore_persisted_v2_agent_metadata shares the uncapped parser without a dedicated legacy test, and completion-message content stays unbounded out of scope. None is a reproduced failure.",
    "[carried-advisories] release_native_wait still has exactly 2 tree references (definition runtime.rs:178 + one suite call): mechanism tested, no production caller. Full CR is 34 files over the 800-line guidance (~half is the integration suite plus tests); the rev4-to-rev5 delta under review is +364/-43.",
    "[scope] Read-only on TASK-260929-csyzcj: only q and resource get were used there. No builds/tests/cargo/just, no source edits, no commits/branch operations, no nested worktree. All board writes target TASK-261011-2aph8r exclusively. No logbook executable exists on this host (carried); this outcome plus own-task notes are the record."
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "Hosted goal_wait_registers_marker_and_wakes_on_child_completion drives V2 spawn, goal idle and an actual parent model request carrying child completion; ignore_native_pending killed on the exact tree. Candidate runtime.rs:719-741 inserts before the mail recheck under the shared goal-state permit; the single ExtensionData SleepItem slot plus insert_if predicate prevents double attachment.",
      "bound": "Executed hosted, not locally. Does not establish every mail/registration concurrency permutation.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:719",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:42"
      ]
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Hosted owned_children_inspection_propagates_failed_lookups kills skip_failed_lookups; pending_native_work_is_only_pending_init_and_running pins PendingInit/Running-only eligibility. Candidate inspect_owned_child_ids (runtime_context.rs:177-210) returns InspectionFailed/UnknownChild errors instead of skipping; runtime.rs:697-707 maps inspection Err to a goal error before any registration; non-goal ordinary-parent interruption stays quiet per hosted test.",
      "bound": "Error attack includes an internal inspection helper test plus hosted suite; not a forced registry/backend failure through the entire idle entry. Existing-marker retention on a transient Err is not independently attacked.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/agent/control/runtime_context.rs:177",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/agent/owned_children.rs:64"
      ]
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Hosted goal_wait_latch_closes_completion_before_registration kills insert_after_mail_check: deterministic gate pauses between Running observation and insert, completes the child in the window, releases, and asserts the actual mail-wake request. Candidate inserts before recheck_pending_work_for_goal_wait under the same serialization (runtime.rs:725-741).",
      "bound": "Final-completion interleaving executed hosted; interruption-before-registration is a separate unexecuted scenario. No local Rust execution.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:725",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:66"
      ]
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "Hosted goal_wait_preserves_foreign_sleep_across_register_and_turn_start compares the complete foreign item across registration and admitted turn start; insert_clobbers_one_foreign and unconditional_remove killed by that suite plus register_never_clobbers_foreign_sleep and conditional_remove_only_removes_owned_id. Candidate insert_if/remove_if run predicate and mutation under the ExtensionData lock (native_wait.rs:42-60); tree-wide audit finds goal_wait_sleep_id the sole minter of the goal-wait: prefix.",
      "bound": "Foreign namespace protection established. Async-cleanup/newer-own-generation interleaving has no demonstrated reproduction and stays a bounded advisory.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:42",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:56"
      ]
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "evidence": "Rev4 regression closed: shared parser byte-identical to base (diff-verified), so legacy 129-byte-segment and >1024-byte identities parse/deserialize byte-identically; hosted resume_agent_preserves_legacy_overlong_path drives the real resume_agent_from_rollout entry and get_rollout_history_preserves_legacy_agent_path drives load_rollout_items/get_rollout_history with zero parse errors; both legacy_parser narrowing mutants killed. Removal wiring verified present: admitted turn start (extension.rs:268), disable/stop (runtime.rs:141-157), release (runtime.rs:178), resume-restore removes without reviving (runtime.rs:589-597), plus idle reinsertion (runtime.rs:725-748). Hosted goal_wait_removed_on_clear_release_and_resume and check-in/exhaustion small tests green.",
      "bound": "No dedicated live-child check-in reinsertion, exhausted-retention plus late-wake, disable/stop interleave, or full rendered-SleepItem history-resume test; restore_persisted_v2_agent_metadata shares the uncapped parser without a dedicated legacy test. Stated bounds, not reproduced failures.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/agent_path.rs:171",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:589",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/extension.rs:268"
      ]
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "Hosted registration/wake and latch tests assert parent event silence and absence of goal-wait history text and disabled current-time reminder content from the wake request. try_register_goal_wait_sleep (native_wait.rs:42) only calls ExtensionData insert_if: no UI, rollout/history, or reminder API in its body or imports; check-in timing stays with the goal scheduler.",
      "bound": "CurrentTimeReminder disabled in the fixture; enabled-reminder preservation by source inspection only. No dedicated side-effect mutant supplied.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:42"
      ]
    },
    {
      "row": "child state transitions",
      "result": "held",
      "evidence": "Hosted real Op::Interrupt registered/ordinary-parent tests prove one queue-only INTERRUPTED notice and wake with no success claim and ordinary-parent silence; interrupted_notice_delivered_twice and interrupted_claims_success killed; is_final match untouched (status.rs delta tests-only). Typed fragment truncates each prose path (256+marker, 682-byte body; interrupted_sender_path_uncapped killed). New identities length-gated at spawn (join_new; spawn_task_name_length_unchecked killed; refusal and at-cap tests assert list_thread_ids effects). Legacy over-cap identities reaching the envelope render truncated display copies (envelope_author_display_uncapped killed); worst-case full item 1222 bytes.",
      "bound": "One interruption transition covered; reused/error classification helper-level; second-child-mid-turn, repeated-interruption, and non-default inherited-settings asserts not independently reported. Scheduler preserves the existing settings path by inspection.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/agent/control/completion.rs:92",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/context/inter_agent_interrupted_message.rs:73",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/protocol.rs:883"
      ]
    }
  ],
  "free_hunt": [
    "{\"probe\": \"AgentPath constructor audit\", \"result\": \"no-finding (closes rev4 regression)\", \"evidence\": \"Shared validate_* fns byte-identical to base by diff; join/try_from/FromStr/serde grammar-only. join_new is the only capped constructor with exactly one production callsite (thread_spawn_source). No production .join( on AgentPath remains (test fixtures only).\"}",
    "{\"probe\": \"spawn refusal ordering\", \"result\": \"no-finding\", \"evidence\": \"V2 spawn builds spawn_source with ? before agent_control.spawn (spawn.rs:148 vs ~184); join_new errors map to RespondToModel in the shared helper. V1 spawn and resume_agent pass task_name None. Refusal-before-creation asserted by list_thread_ids equality in the hosted test.\"}",
    "{\"probe\": \"resolve-site model reachability\", \"result\": \"no-finding\", \"evidence\": \"All AgentPath::resolve production uses (target.rs:51, root_handoff.rs:143, control.rs:360, agent_message_board.rs) are routing lookups or predicates with mapped errors; none mints, persists, or model-renders a new identity.\"}",
    "{\"probe\": \"model-visible render paths\", \"result\": \"no-finding\", \"evidence\": \"Every production AgentMessage render goes through the now-truncating to_model_input_item (4+ callsites); to_response_input_item is test-only; history.rs:1081 is a byte estimator confirming the author+recipient+content accounting. Max item 270+270+682=1222 bytes recomputed independently (python3 exit 0).\"}",
    "{\"probe\": \"production panic grep\", \"result\": \"no-finding\", \"evidence\": \"No expect/unwrap on AgentPath parse/join/resolve in production; input_queue.rs expects sit inside mod tests (line 715+). Model-supplied long names become tool errors, never panics.\"}",
    "{\"probe\": \"release wiring\", \"result\": \"no-finding (carried advisory)\", \"evidence\": \"release_native_wait has exactly 2 tree references (def + one suite call): mechanism tested, no production trigger wiring. Same as rev4.\"}",
    "{\"probe\": \"breaking-change scan\", \"result\": \"no-finding\", \"evidence\": \"CR touches no app-server/CLI/config paths; serde schemas unchanged; legacy resume preserved; is_final untouched; Cargo delta is the intra-workspace items edge only.\"}"
  ]
}
```
