# Merged review verdict — TASK-260929-csyzcj CR revision 5 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261011-36tdcg_panel-verdict.md` (accept), `TASK-261011-2aph8r_panel-verdict.md` (accept), `TASK-261011-10zwvx_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "interrupted-item-token-threshold-unreviewed",
      "row": "child state transitions",
      "priority": "P0",
      "invariant": "AGENTS.md Model visible context rule 5 requires highlighting new individual items that can cross >1K tokens as P0 and obtaining additional manual review. A four-bytes/token heuristic cannot establish that the full new AgentMessage is below this threshold.",
      "mechanism": "The new interrupted body renders the two paths, and to_model_input_item repeats them in author/recipient. Each of the four path occurrences can keep 256 bytes plus a marker. Restored parent /root/ + a1 repeated 150 times and its /worker child pass the unchanged grammar. The rendered item is 1222 bytes but encodes to 1057 tokens with cl100k_base and 1056 with o200k_base/o200k_harmony. Even a newly allocated /root/<a1 repeated 64>/<b2 repeated 64> parent (263 bytes) and /worker child (270 bytes), with all segments <=128 and total <=1024, encodes to 1053/1052 tokens. Both are above 1000 and 1024. The producer outcome explicitly derives ~306 tokens using bytes/4 and claims the item is under the P0 threshold, so the required manual-review classification is missed. History accounting itself labels its byte heuristic a coarse lower bound. The 10K hard ceiling and byte caps still hold; this is a review-threshold/evidence finding, not an unbounded item or a demonstrated runtime delivery failure.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261011-10zwvx-token-assay.py (full script embedded in this outcome)",
          "command": "uv run --no-project --with tiktoken==0.14.0 python .temp/TASK-261011-10zwvx-token-assay.py",
          "expected_failure": "Observed expected-red exit 1: assertion falsifying the under-1K claim fails at 1057 tokens after short controls pass. Three tree-pinned git-show reads exit 0. Runs a static rendering/tokenizer assay only; no Rust build or test.",
          "exit_code": 1,
          "executed": true,
          "pinned_blobs": [
            "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/context/inter_agent_interrupted_message.rs (rendered body)",
            "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/protocol.rs (to_model_input_item author/recipient)",
            "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/agent_path.rs (truncated_for_display)"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_native_wait.rs (requested dense-path integration; not added/run)",
          "command": "Hosted only, requested: just test -p codex-core -E 'test(goal_wait_dense_paths_token_threshold)'",
          "expected_failure": "With agent_max_depth >=3, spawn 128-character alternating letter/digit segments, hold the parent goal wait, interrupt its child, capture the outbound agent_message and tokenize author+recipient+content. An assertion of <=1K must fail on the current candidate. Or restore the legacy dense parent fixture. Numeric exit code unknown; test does not yet exist.",
          "pinned_blobs": [
            "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/context/inter_agent_interrupted_message.rs (rendered body)",
            "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/protocol.rs (to_model_input_item author/recipient)",
            "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/agent_path.rs (truncated_for_display)"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "none; same model-visible-size class as prior envelope findings, new token-threshold witness",
      "fix_request": "Correct the under-1K claim and explicitly route this item as P0 for the required additional manual review. Alternatively, reduce the display/body path budget enough to establish a conservative full-item token bound and cover the dense-name case at the actual delivery entry. Preserve legacy routing identities and the closed resume fixes. Exceeding 1K is not itself forbidden by the rule; manual review is the required action.",
      "sources": [
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/context/inter_agent_interrupted_message.rs:25",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/agent_path.rs:102",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/protocol.rs:883",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/session/mod.rs:4001",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/context_manager/history.rs:623",
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_results.md",
        "https://github.com/openai/tiktoken/blob/main/tiktoken_ext/openai_public.py"
      ],
      "reported_by": [
        "TASK-261011-10zwvx"
      ]
    }
  ],
  "notes": [
    "[TASK-261011-36tdcg] {'id': 'coverage', 'text': \"7/7 prescribed rows swept, each exactly once: held 7, broken 0, not-attacked 0. Held denotes the named attack and stated bound, not exhaustive AC subcase coverage. Producer's 9/9 AC ratio counts rows with driving tests. Hosted 12/12 mutant kills are accepted evidence; independently checked 12/12 patch applicability is a separate ratio.\"}",
    "[TASK-261011-36tdcg] {'id': 'execution-identity', 'text': 'Replay equals the expected candidate. Readable CR rev5 validation log ends [exit 0], names tree b91072a5 and run 38109158922, and reports exact_command_shard required=1 green=1 failed=0 missing=0 test_case_coverage=unknown. Precheck 15 binds four successful hosted lanes and 12 named kills to this exact tree. No Rust, cargo, just, build, suite or mutant execution was rerun here. Individual mutant run IDs and numeric hosted test-command exits are not supplied and remain unknown. Small lane explicitly adds protocol and rollout on relux/ci-next 9f8fdf9a.', 'sources': ['board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-15.md', 'board-resource://TASK-260929-csyzcj/outcome/TASK-260929-csyzcj_change-request_rev5-validation.log']}",
    "[TASK-261011-36tdcg] {'id': 'prior-round-disposition', 'text': 'Rev4 legacy-agent-path-resume-regression / persisted-agent-path-caps-break-resume is addressed: 3/3 shared grammar validators and from_string compare byte-identically with CR base; persisted/routing identities are preserved. New-path limits live only in join_new and are reached from the V2 tool before creation. The legacy-resume test passes agent_path=None on resume, forcing stored restoration; the rollout fixture writes raw legacy JSON. Legacy segment and total-path parser mutants are killed hosted. Display-only envelope caps prevent reopening the earlier unbounded-envelope class.', 'sources': ['b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/agent_path.rs:91', 'b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/agent/control_tests.rs:4751', 'b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/rollout/src/recorder_tests.rs:362', 'board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-15.md']}",
    "[TASK-261011-36tdcg] {'id': 'manual-context-review', 'text': \"Manually inspected the complete new plaintext interruption item: typed core/context fragment, 256-byte path truncation plus 14-byte marker in both body and envelope, and production history conversion through to_model_input_item. Hard payload field budget is 270+270+682=1222 bytes, rather than the previous unbounded legacy paths. No history replacement is introduced. Actual tokens were not measured; the producer's approximate under-1K-token claim is not treated as evidence. Encrypted payload length and existing completion content are carried bounds outside the new plaintext Interrupted fragment.\", 'sources': ['b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/context/inter_agent_interrupted_message.rs:26', 'b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/session/mod.rs:4001', 'b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/protocol.rs:883']}",
    "[TASK-261011-36tdcg] {'id': 'requested-targeted-attacks', 'text': 'Requested, not run: goal_wait_checkin_reinserts_with_live_child; goal_wait_exhausted_checkins_late_child_completion_wakes; goal_wait_disable_stop_during_registration; goal_wait_resume_rendered_sleep_with_unloaded_child; goal_wait_wake_preserves_nondefault_turn_settings; goal_wait_second_child_completes_mid_turn; goal_wait_second_interruption_transition; goal_wait_preserves_enabled_reminder_schedule. For total new-path admission, narrow/remove only validate_new_path_length while preserving segment grammar/cap, then require a real nested V2 spawn to accept exactly 1024 bytes and refuse 1025. None of these requests is marked green or represented as an observed failure.'}",
    "[TASK-261011-36tdcg] {'id': 'scope', 'text': 'All source-task operations were read-only queries/resource gets/direct resource reads. No accept_cr, reject_cr, withdraw_cr, set_status, handoff, notes, resources or checklist write on TASK-260929-csyzcj. Own lifecycle/outcome/checklist/notes/handoff target TASK-261011-36tdcg only. No product edit, nested worktree, commit, branch switch, rebase, merge, archive or binary attachment.'}",
    "[TASK-261011-36tdcg] {'id': 'review-logbook', 'text': \"2026-10-11: exact replay established; latest hosted identity checked; rev4 shared-parser regression repaired without reopening unbounded interruption envelopes; no new demonstrated failure in bounded sweep. Important evidence limits and follow-up attacks are recorded in this task-scoped outcome and own-task board note. command -v logbook exited 1 (no standalone tool); no separate external logbook write is claimed. Role installation lacks the linked review-round section; the panel brief's explicit attack/sweep/free-hunt contract was applied.\"}",
    "[TASK-261011-36tdcg] {'id': 'successor-recovery-logbook', 'text': '2026-10-11 RUN-261011-1907d8: reproduced source CR tree exactly; rechecked seven-row verdict structure and key production wiring; accepted exact-tree hosted evidence without rerunning builds. Predecessor own-task validation exit 1 was caused by an untracked research outcome becoming a code delta. Preserved text in ignored scratch and existing board outcome; empty-delta gate then exited 0. No hosted-green registry edit, validator bypass, commit or source-task write. Retained accept panel opinion with explicitly stated unexecuted bounds. Own-task outcome update and role handoff carry this recovery evidence.'}",
    "[TASK-261011-2aph8r] [rev4-findings-closed] Both rev3/rev4 bypass/regression findings are closed. (1) Legacy resume: the shared AgentPath parser (validate_agent_name, validate_absolute_path, validate_relative_reference) is byte-identical to base 39c264c (verified by diff); join/try_from/FromStr/serde accept every pre-cap identity unchanged. Length caps live only in join_new, called from exactly one production site (thread_spawn_source, multi_agents_common.rs:146). V1 spawn and resume_agent pass task_name None; V2 spawn builds spawn_source with ? (multi_agents_v2/spawn.rs:148) before agent_control.spawn, so refusal precedes thread creation. Real entry-point regressions drive resume_agent_from_rollout (resume_agent_preserves_legacy_overlong_path) and load_rollout_items/get_rollout_history with a raw-JSONL legacy fixture (get_rollout_history_preserves_legacy_agent_path). Narrowing mutants legacy_paths_rejected_by_shared_parser and legacy_long_path_rejected_by_shared_parser are killed hosted. (2) Model-context bound: to_model_input_item renders author/recipient through truncated_for_display in both plaintext and encrypted branches; stored routing identities asserted unchanged; whole-object assert_eq pins both branches (agent_message_envelope_truncates_legacy_paths_for_display); envelope_author_display_uncapped killed. Worst case independently recomputed: 270+270+682 = 1222 bytes (~306 tokens), under the 1K P0 threshold.",
    "[TASK-261011-2aph8r] [delta-scope] rev4 candidate 5a51cf52 to rev5 candidate b91072a is exactly 6 files (+364/-43): protocol agent_path.rs (uncapped parser + join_new + display truncation + 7 tests), protocol.rs (envelope render + 1 test), multi_agents_common.rs (one-word join to join_new), control_tests.rs (+72 resume test), recorder_tests.rs (+69 rollout test), goal_native_wait.rs (comment-only). All goal-wait mechanism files are byte-identical to rev4, so rev4 held-row mechanism evidence still applies; every row was re-swept against precheck-15 evidence anyway.",
    "[TASK-261011-2aph8r] [render-audit] All production model-visible AgentMessage renders funnel through to_model_input_item (session delivery session/mod.rs:4001, rollout_reconstruction.rs:427, rollout list.rs:1285, rollout_input.rs:47, memories phase1.rs). to_response_input_item has test-only callers. history.rs:1081 is a byte estimator (destructures author/recipient/content), confirming the 270+270+682 accounting basis. No production expect/unwrap on AgentPath parsing (input_queue.rs expects are inside mod tests at line 715+). resolve() callsites (target.rs, root_handoff.rs, control.rs:360, agent_message_board.rs) are routing lookups with mapped errors, never identity minting or persistence.",
    "[TASK-261011-2aph8r] [breaking-change-scan] No app-server API, CLI, or config change (no such paths in the 34-file CR). Serde schemas unchanged: AgentPath still try_from String, SessionSource/ThreadSpawn shapes unchanged, AgentMessage author/recipient still strings (values display-truncated only past 256 bytes). Resume of legacy rollouts is preserved, not broken. status.rs delta is tests-only (is_final untouched). Cargo.lock delta is the single intra-workspace codex-extension-items edge; MODULE.bazel.lock untouched (bazel-lock-update execution unknown, not reproduced — carried advisory).",
    "[TASK-261011-2aph8r] [coverage-ratio] Surface sweep 7/7 with exactly one result per row: held 7/7, broken 0/7, not-attacked 0/7. Hosted shipped mutants killed 12/12 per attached summary; local patch coherence 12/12. These are distinct measured ratios, not full AC subcase coverage. Producer-stated partial bounds stand: no dedicated live-child check-in reinsertion test, no exhausted-retention plus late-wake live test, no disable/stop interleave test, no full resume_thread_with_history with rendered SleepItem, no second-child-mid-turn or repeated-interrupt integration, no explicit non-default inherited-settings assert on the native path, AC6 reminder-enabled schedule by source inspection only, restore_persisted_v2_agent_metadata shares the uncapped parser without a dedicated legacy test, and completion-message content stays unbounded out of scope. None is a reproduced failure.",
    "[TASK-261011-2aph8r] [carried-advisories] release_native_wait still has exactly 2 tree references (definition runtime.rs:178 + one suite call): mechanism tested, no production caller. Full CR is 34 files over the 800-line guidance (~half is the integration suite plus tests); the rev4-to-rev5 delta under review is +364/-43.",
    "[TASK-261011-2aph8r] [scope] Read-only on TASK-260929-csyzcj: only q and resource get were used there. No builds/tests/cargo/just, no source edits, no commits/branch operations, no nested worktree. All board writes target TASK-261011-2aph8r exclusively. No logbook executable exists on this host (carried); this outcome plus own-task notes are the record.",
    "[TASK-261011-10zwvx] {'id': 'prior-round-disposition', 'text': 'legacy-agent-path-resume-regression: fixed. persisted-agent-path-caps-break-resume: fixed. Both describe the retroactive shared-parser cap class; source equality and hosted legacy resume/rollout plus segment/total narrowing kills establish the repair.'}",
    "[TASK-261011-10zwvx] {'id': 'exact-evidence-reuse', 'text': 'Accepted precheck 15 only: candidate tree b91072a51501101110a4e13061a8c07a242aad6a, snapshot run 38109158922, lint/small/core/app-server success, 12/12 mutants killed, 0 survivors. Dispatch workflow relux/ci-next 9f8fdf9a includes protocol and rollout in small lane. Resource provides lane conclusions/test names but no individual mutant run IDs or numeric shell exit codes. Those values remain unknown; no local Rust execution or fresh remote execution claimed.'}",
    "[TASK-261011-10zwvx] {'id': 'coverage', 'text': '7/7 surface rows swept exactly once: 6 held within stated bounds, 1 broken by P0 review classification. 9/9 AC rows have named driving evidence; this does not imply all subcases executed. Neither hosted green nor the 12/12 selected mutant ratio proves total negative-shape coverage.'}",
    "[TASK-261011-10zwvx] {'id': 'requested-attacks', 'text': 'Unrun hosted requests: goal_wait_checkin_reinserts_with_live_child; goal_wait_exhausted_checkins_late_child_completion_wakes; goal_wait_disable_stop_during_registration; goal_wait_resume_rendered_sleep_with_unloaded_child; goal_wait_wake_preserves_nondefault_turn_settings; goal_wait_second_child_completes_mid_turn; goal_wait_second_interruption_transition; goal_wait_dense_paths_token_threshold. Total new-path gate mutant should remove only MAX_PATH_BYTES check, preserve segment checks, and be killed by real nested spawn at 1024/past-1024. None is claimed passing.'}",
    "[TASK-261011-10zwvx] {'id': 'carried-advisories', 'text': 'release_native_wait has a definition and suite caller but no production forwarding. Goal-wait removal checks namespace, not an expected generation; stale-cleanup interleavings remain unproven. Cargo adds an existing workspace extension-items edge; no MODULE.bazel.lock change or bazel-lock-update execution is supplied, so drift is unknown. Base delta is 34 files, 2639 additions/21 deletions, including a new 1083-line suite. Delta from rev4 is only 6 files, 364 additions/43 deletions. Staging advisory remains primitive inspection/atomic removal followed by goal integration and notices.'}",
    "[TASK-261011-10zwvx] {'id': 'scope', 'text': 'No builds, cargo, just, Rust tests, commits, branch changes, nested worktrees or source-task writes. Python source/token assays are static review attacks. A prebuilt tiktoken 0.14.0 environment was obtained with uv; no repository dependency was changed. Only this task-scoped plain-text outcome is attached.'}",
    "[TASK-261011-10zwvx] {'id': 'skill-routing', 'text': 'Required project-management SKILL.md and negative-evidence/research-workflow references read. Its .roles/reviewer/role.md reference is absent at the installed path and focused searches found no copy. The explicit user panel brief supplies the applicable sweep/review contract; no review step waived.'}",
    "[TASK-261011-10zwvx] {'id': 'logbook', 'text': 'No standalone logbook executable (command -v exit 1) or enabled logbook tool exists. The timestamped review logbook is preserved in this outcome and own-task notes. No external logbook write is claimed.'}",
    "[TASK-261011-10zwvx] {'id': 'successor-recovery', 'text': 'RUN-261011-b7b1ad independently replayed and repeated the expected-red tokenizer assay, verified 42/42 candidate copies and 4/4 authoritative inputs, and checked the seven surface rows. Preserved task-specific report as outcome only to repair predecessor failed handoff; git-only empty-delta gate exit 0. No source-task writes or local Rust builds/tests.'}"
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "invariant": "AC1: one goal-owned marker at eligible idle; queue-only child completion produces a real parent model request.",
      "attack": "Marker-only false wake, double attachment, queue-only delivery without scheduler admission, and ignored native pending.",
      "evidence": "Hosted goal_wait_registers_marker_and_wakes_on_child_completion asserts silence before completion and an actual completion-bearing request. ignore_native_pending is killed. A single type-keyed SleepItem slot is atomically refreshed by insert_if; core mailbox enqueue and the post-insert recheck both reach the existing scheduler.",
      "bound": "Executed public-entry attack is hosted evidence accepted from the exact-tree precheck; no local runtime execution. Exhausted-check-in late wake has no dedicated live integration.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:699",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:42",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/session/handlers.rs:90",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/tasks/mod.rs:551",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/tests/suite/goal_native_wait.rs:248"
      ],
      "reported_by": "TASK-261011-36tdcg"
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "invariant": "AC2: only directly owned, loaded PendingInit/Running children enable registration; failed inspection propagates rather than becoming absence.",
      "attack": "Foreign/descendant membership, unknown and unloaded identities, terminal/reused states, and skipped lookup errors.",
      "evidence": "Production selects direct ThreadSpawn edges, checks active goal and persistent-host wait support before inspection, and propagates Err with ?. inspect_owned_child_ids distinguishes known unloaded children from unknown ids. Hosted owned_children_inspection_propagates_failed_lookups and pending_native_work_is_only_pending_init_and_running cover the distinctions; skip_failed_lookups is killed. The ordinary-parent interruption integration remains quiet.",
      "bound": "The failed-lookup attack enters the internal inspection method, not the full idle entry. Forced backend failure and an existing marker at that failure are not independently exercised. The outer lifecycle logs propagated errors; it does not report them as an empty set.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/agent/control/runtime_context.rs:64",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/agent/control/runtime_context.rs:172",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/agent/owned_children.rs:65",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:683",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/tests/suite/goal_native_wait.rs:989"
      ],
      "reported_by": "TASK-261011-36tdcg"
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "invariant": "AC3: insertion precedes mailbox recheck and completion in the inspection/insert window is not lost.",
      "attack": "Recheck-before-insert, completion in the latch window, self-deadlock on the goal-state semaphore, and a second idle pass masking the fault.",
      "evidence": "Hosted goal_wait_latch_closes_completion_before_registration kills insert_after_mail_check. The fixture confirms queued mail before gate release, retains a second Running child, uses bounded waits, and proves a real mail wake without goal steering or a masking second idle pass. Candidate inserts first, then shares the held permit with on_turn_start through a scoped GoalTurnStartLease.",
      "bound": "This establishes the final-completion latch scenario; interruption before registration is a distinct unexecuted scenario. Local checks prove patch coherence only.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:722",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/tests/suite/goal_native_wait.rs:367",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/tests/suite/goal_native_wait.rs:485",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/extension.rs:278"
      ],
      "reported_by": "TASK-261011-36tdcg"
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "invariant": "AC4: registration and removal preserve another contributor's SleepItem.",
      "attack": "Allow exactly one foreign id through insertion, unconditional removal, and stale attachment checks outside the map lock.",
      "evidence": "Hosted register_never_clobbers_foreign_sleep, conditional_remove_only_removes_owned_id, and goal_wait_preserves_foreign_sleep_across_register_and_turn_start attack the actual helpers and register/turn-start path. insert_clobbers_one_foreign and unconditional_remove are killed. Both predicates and mutations run under ExtensionData's same map lock.",
      "bound": "Ownership means the goal-wait contributor prefix, including refresh of its older generations; this is not compare-and-remove of one exact generation. No reachable stale-clear/new-generation failure was established.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/extension-api/src/state.rs:140",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:42",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:58",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/items/src/sleep.rs:31",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/tests/suite/goal_native_wait.rs:624"
      ],
      "reported_by": "TASK-261011-36tdcg"
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "invariant": "AC5/AC9: remove on admitted start, clear/inactive/disable/stop/release/resume; reinsert at eligible idle; retain while check-ins are exhausted.",
      "attack": "Uncalled cleanup, marker revival from history, omitted reinsertion, exhausted-wait removal, and foreign marker destruction during lifecycle paths.",
      "evidence": "Hosted wake tests check turn-start removal; goal_wait_removed_on_clear_release_and_resume drives clear/resume service entries and the release API. Hosted empty_exec_with_native_pending_waits_and_uses_checkins and native_pending_exhausts_checkins_then_waits_without_deadline exercise ticket exhaustion; ignore_native_pending is killed. Static tracing reaches cleanup from on_thread_stop, enable=false, inactive/clear and restore_after_resume. Registration occurs before evaluation returns Wait with no deadline, so exhausted check-ins do not remove the marker.",
      "bound": "Not full subcase execution: live-child reinsertion, exhausted-retention plus late completion, disable/stop interleavings, and resume_thread_with_history with rendered SleepItem/unloaded child lack dedicated integrations. release_native_wait has two tree references (definition and suite call), with no production caller in this snapshot.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/extension.rs:176",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/extension.rs:226",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/extension.rs:265",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:143",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:178",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:590",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/runtime.rs:766",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/tests/suite/goal_native_wait.rs:732",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/tests/native_wait.rs:146"
      ],
      "reported_by": "TASK-261011-36tdcg"
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "invariant": "AC6: storing the marker emits no sleep UI event/history item and does not change current-time reminder scheduling.",
      "attack": "Insertion emits events, contributes history, schedules a timer, or silently rewrites reminder state.",
      "evidence": "Hosted registration test asserts a silent idle interval and no goal-wait marker text in the wake body. Static insertion constructs only SleepItem and calls ExtensionData::insert_if; it has no event/history/reminder/timer calls. Goal check-in timing is owned by the existing BackgroundWaitState/runtime, independently of the marker store.",
      "bound": "CurrentTimeReminder is disabled in the fixture: absence of current_time is not proof of enabled-reminder schedule preservation. That part is source-established only. No dedicated side-effect mutant is supplied.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/precondition/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/ext/goal/src/native_wait.rs:42",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/tests/suite/goal_native_wait.rs:119",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/tests/suite/goal_native_wait.rs:320"
      ],
      "reported_by": "TASK-261011-36tdcg"
    },
    {
      "row": "child state transitions",
      "result": "broken",
      "evidence": "Hosted Op::Interrupt tests prove one queue-only INTERRUPTED notice/request, ordinary-parent silence and no success claim; duplicate/success-wording mutants die. Global is_final body is unchanged. New-spawn refusal/at-cap tests and spawn-name mutant hold. However the new model-visible INTERRUPTED item crosses the >1K-token manual-review threshold with valid dense path names: static tokenizer witness is 1056/1057 tokens for restored legacy paths and 1052/1053 for paths within new limits. The handoff instead claims ~306 tokens and below that threshold. See interrupted-item-token-threshold-unreviewed.",
      "bound": "No Rust/public-entry execution of the dense-path witness; source-transcribed rendering and actual tokenizer execution only. Live delivery reaches the same render via record_inter_agent_communication. Repeated interrupt transitions, non-default inherited settings, reused/error end-to-end and second-child-mid-turn remain unexecuted; existing scheduler preserves queue-only wake settings.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-15.md",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/protocol/src/protocol.rs:883",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/context/inter_agent_interrupted_message.rs:73",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/session/mod.rs:4001",
        "b91072a51501101110a4e13061a8c07a242aad6a:codex-rs/core/src/tasks/mod.rs:610"
      ],
      "reported_by": "TASK-261011-10zwvx"
    }
  ],
  "free_hunt": [
    "[TASK-261011-36tdcg] {\"budget\": \"Five bounded classes after the seven-row sweep; static review plus exact-tree hosted evidence only.\", \"results\": [{\"class\": \"legacy persistence compatibility\", \"result\": \"held\", \"evidence\": \"Base/candidate shared-validator equality (3/3), from_string equality, resumed stored-path test and raw legacy JSON rollout test. Rev5 rework changes six paths (+364/-43) from rev4; no product edit outside those paths in that delta. Total legacy-path parsing has a hosted unit kill; full resume with >1024-byte identity is still unexecuted.\"}, {\"class\": \"creation and model-context bypass\", \"result\": \"held\", \"evidence\": \"V2 handle_spawn_agent calls thread_spawn_source with ? before agent_control.spawn; only that minting site uses join_new. Both plaintext and encrypted envelope display paths are capped without changing stored routing identities. Production record and rollout reconstruction call to_model_input_item. Full-fidelity to_response_input_item has only test callers in the searched core tree. Actual tokenizer measurement and total-cap public-entry mutant are named unknowns.\"}, {\"class\": \"cleanup concurrency and ownership\", \"result\": \"held within stated bound\", \"evidence\": \"Atomic contributor predicates preserve foreign sleep; scoped permit share closes latch self-deadlock. Several clear/restore paths drop the goal permit before live-thread cleanup, and prefix cleanup does not compare generations. No reachable stale-clear/new-generation bypass was established; this remains a targeted interleaving request, not a finding. Explicit release has no production caller.\"}, {\"class\": \"dependency and build metadata\", \"result\": \"unknown outside supplied lanes\", \"evidence\": \"Only dependency addition is existing workspace codex-extension-items in goal Cargo.toml/Cargo.lock. BUILD.bazel uses codex_rust_crate; no include_str/include_bytes/resource read added. MODULE.bazel.lock unchanged; bazel-lock-update execution and Bazel drift are not attested by precheck 15. No build run and no fabricated failure.\"}, {\"class\": \"change size and staging\", \"result\": \"advisory\", \"evidence\": \"Base..candidate: 34 files, 2639 additions/21 deletions; new integration module is 1083 lines. Exceeds 800-line guidance. Small coherent first stage: atomic ExtensionData removal and typed direct-child inspection with their tests, independently of runtime behavior. Then goal lease/scheduler/Interrupted delivery, followed by protocol admission/display changes with legacy compatibility tests. Current rev4..rev5 repair is bounded at 364 additions/43 deletions and six files.\"}], \"findings_found\": 0}",
    "[TASK-261011-2aph8r] {\"probe\": \"AgentPath constructor audit\", \"result\": \"no-finding (closes rev4 regression)\", \"evidence\": \"Shared validate_* fns byte-identical to base by diff; join/try_from/FromStr/serde grammar-only. join_new is the only capped constructor with exactly one production callsite (thread_spawn_source). No production .join( on AgentPath remains (test fixtures only).\"}",
    "[TASK-261011-2aph8r] {\"probe\": \"spawn refusal ordering\", \"result\": \"no-finding\", \"evidence\": \"V2 spawn builds spawn_source with ? before agent_control.spawn (spawn.rs:148 vs ~184); join_new errors map to RespondToModel in the shared helper. V1 spawn and resume_agent pass task_name None. Refusal-before-creation asserted by list_thread_ids equality in the hosted test.\"}",
    "[TASK-261011-2aph8r] {\"probe\": \"resolve-site model reachability\", \"result\": \"no-finding\", \"evidence\": \"All AgentPath::resolve production uses (target.rs:51, root_handoff.rs:143, control.rs:360, agent_message_board.rs) are routing lookups or predicates with mapped errors; none mints, persists, or model-renders a new identity.\"}",
    "[TASK-261011-2aph8r] {\"probe\": \"model-visible render paths\", \"result\": \"no-finding\", \"evidence\": \"Every production AgentMessage render goes through the now-truncating to_model_input_item (4+ callsites); to_response_input_item is test-only; history.rs:1081 is a byte estimator confirming the author+recipient+content accounting. Max item 270+270+682=1222 bytes recomputed independently (python3 exit 0).\"}",
    "[TASK-261011-2aph8r] {\"probe\": \"production panic grep\", \"result\": \"no-finding\", \"evidence\": \"No expect/unwrap on AgentPath parse/join/resolve in production; input_queue.rs expects sit inside mod tests (line 715+). Model-supplied long names become tool errors, never panics.\"}",
    "[TASK-261011-2aph8r] {\"probe\": \"release wiring\", \"result\": \"no-finding (carried advisory)\", \"evidence\": \"release_native_wait has exactly 2 tree references (def + one suite call): mechanism tested, no production trigger wiring. Same as rev4.\"}",
    "[TASK-261011-2aph8r] {\"probe\": \"breaking-change scan\", \"result\": \"no-finding\", \"evidence\": \"CR touches no app-server/CLI/config paths; serde schemas unchanged; legacy resume preserved; is_final untouched; Cargo delta is the intra-workspace items edge only.\"}",
    "[TASK-261011-10zwvx] {\"budget_minutes\": 3, \"started_at_utc\": \"2026-10-11 06:42:19 UTC\", \"ended_at_utc\": \"2026-10-11 06:43:40 UTC\", \"examined\": [\"live and replay model render callsites\", \"dense path tokenizer counts and short/new/legacy controls\", \"goal-wait namespace minters and release forwarding\", \"generation cleanup limits\", \"Cargo/Bazel footprint and staging\"], \"findings\": [\"interrupted-item-token-threshold-unreviewed\"], \"bound\": \"Static hunt with actual tokenizer execution; no Rust/build/test execution. Does not establish unrelated completion-content bounds, generation race reachability or Bazel lock freshness.\"}",
    "[TASK-261011-10zwvx] {\"probe\": \"successor bounded static pass\", \"examined\": [\"production model render forwarding\", \"release_native_wait callsites\", \"goal-wait namespace minters\", \"restored AgentPath parsing and new-only admission\"], \"result\": \"No additional demonstrated defect; prior advisories and execution bounds retained. Token-threshold witness independently rerun, expected-red exit 1.\"}"
  ]
}
```

## Recording reviewer audit — revision 5, 2026-10-11

Recording branch: **changes_requested**. Reviewed CR-TASK-260929-csyzcj-5, revision 5, candidate tree b91072a51501101110a4e13061a8c07a242aad6a.

Read all three authoritative panel outcomes through task-board resource get --output - (each exit 0): TASK-261011-36tdcg_panel-verdict.md (accept), TASK-261011-2aph8r_panel-verdict.md (accept), TASK-261011-10zwvx_panel-verdict.md (changes_requested). Read this merged verdict the same way (exit 0). The latest recording brief governs; no new technical review or additional findings were introduced.

Merge completeness: **1 of 1 findings preserved** field-for-field, including priority P0, severity, repeat-of, mechanisms, reproduction commands/execution limits, sources and requested repair. Additive source pins/report attribution retained. **21 of 21 panel row results accounted for; 7 of 7 merged surface rows** occur exactly once, in the prescribed order, with the worst panel verdict: held, held, held, held, held, held, broken. Panel notes **24 of 24** and free-hunt records **10 of 10** retained verbatim after decoding their merge representation. An in-memory JSON/ast comparison executed through python3 exited 0; it checked all note/free-hunt records. Structured finding and row comparisons also passed.

| Surface row | Recorded result |
|---|---|
| registration and wake | held |
| eligibility and inspection errors | held |
| completion-before-registration race | held |
| foreign sleep ownership | held |
| marker lifecycle | held |
| side-effect silence | held |
| child state transitions | broken |

The sole P0 finding is interrupted-item-token-threshold-unreviewed: dense valid identities produce a bounded 1222-byte item measured by the delta panel at 1052–1057 tokens, invalidating the handoff's bytes/4 estimate of about 306 tokens. This recording audit accepts that panel evidence within its stated static-assay bound; it does not claim a new Rust/public-entry reproduction. Prior legacy-parser/resume findings remain closed. The attached rework brief selects a conservative whole-item byte cap and delivery coverage; routing is to implementation rework, with no human-only blocker asserted.

Evidence reuse: hosted precheck 15, run 38109158922, and 12/12 selected mutant kills remain the panels' accepted exact-tree evidence. No builds, tests, fmt, mutants, tokenizer assays or hosted checks were rerun by this recording reviewer. No repository files, index, branches or commits were changed. Resources were read to stdout; no temporary files or directories were created.

Reviewer goal query: task-board spawn goal "$TASK_BOARD_RUN_ID" exited 0 and reported no active goal / run not goal-bound. Directive checkpoint exited 0: none recorded.

Logbook fallback: command -v logbook exited 1 (no standalone executable). This timestamped task-scoped outcome records the important merge decision and evidence limits; no separate external logbook write is claimed. The installed skill's linked reviewer role file was absent; the explicit recording brief supplies the complete applicable recording contract.
