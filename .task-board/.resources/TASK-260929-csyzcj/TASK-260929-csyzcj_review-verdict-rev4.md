# Merged review verdict — TASK-260929-csyzcj CR revision 4 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261011-3l5dnu_panel-verdict.md` (changes_requested), `TASK-261011-297lwc_panel-verdict.md` (accept), `TASK-261011-3dpjl3_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "legacy-agent-path-resume-regression",
      "row": "marker lifecycle",
      "priority": "P1",
      "invariant": "New spawn limits must preserve the ability to resume existing rollouts and restore already persisted agent identities, or provide an explicit compatibility/migration path (repository breaking-change review rule).",
      "mechanism": "AgentPath derives Deserialize via try_from String, and from_string uses the same validate_absolute_path/validate_agent_name as new allocation. The newly added length guards therefore apply retroactively. /root/ plus 129 lowercase a characters was valid at the pinned base (135-byte total path), is reachable through V2 thread_spawn_source -> AgentPath::join, and is written into both SessionMeta.source ThreadSpawn.agent_path and SessionMeta.agent_path. Candidate resume_single_agent_from_rollout parses the stored path with AgentPath::try_from and returns InvalidRequest(\"invalid stored agent path: agent_name must be at most 128 bytes, got 129\") before loading the agent. restore_persisted_v2_agent_metadata likewise skips that child after its parse error. For file-backed history, decode_rollout_line deserializes source through the tightened type; load_rollout_items drops the previously valid SessionMeta as a parse error, and get_rollout_history cannot obtain its thread ID if there is no later valid SessionMeta. No grandfathering/migration is present. This is a static deterministic breaking-change witness, not a claimed runtime test failure.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261011-3l5dnu-legacy-path-assay.py (full source embedded above)",
          "command": "python3 .temp/TASK-261011-3l5dnu-legacy-path-assay.py",
          "expected_failure": "Observed exit 1: source-contract witness requires a previously admitted 129-byte legacy segment to fit the new 128-byte shared-parser cap. This intentionally failing static assertion demonstrates the incompatible acceptance sets; it does not execute Rust.",
          "pinned_blobs": [
            "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:.temp/TASK-261011-3l5dnu-legacy-path-assay.py (full source embedded above)"
          ]
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_native_wait.rs (requested new test resume_agent_preserves_legacy_overlong_path; not added or run)",
          "command": "just test -p codex-core -E 'test(resume_agent_preserves_legacy_overlong_path)'",
          "expected_failure": "Requested hosted attack: persist a base-valid /root/<129 lowercase chars> child via a legacy fixture, unload it, drive the public resume-agent operation and require successful restoration with the original routing identity. Candidate should instead return invalid stored agent path. Numeric exit code unknown; test does not yet exist.",
          "pinned_blobs": [
            "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs (requested new test resume_agent_preserves_legacy_overlong_path; not added or run)"
          ]
        },
        {
          "test_file": "codex-rs/rollout/src/recorder_tests.rs (requested new test get_rollout_history_preserves_legacy_agent_path; not added or run)",
          "command": "just test -p codex-rollout -E 'test(get_rollout_history_preserves_legacy_agent_path)'",
          "expected_failure": "Requested hosted attack: feed get_rollout_history a valid old SessionMeta whose source contains the 129-byte segment and require unchanged session/history identity. Candidate skips its metadata line and reports failed to parse thread ID. Numeric exit code unknown; test does not yet exist.",
          "pinned_blobs": [
            "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/rollout/src/recorder_tests.rs (requested new test get_rollout_history_preserves_legacy_agent_path; not added or run)"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "sources": [
        "39c264c34e61b5171ae13b0f756746c24ea5f51a:codex-rs/protocol/src/agent_path.rs:125",
        "39c264c34e61b5171ae13b0f756746c24ea5f51a:codex-rs/core/src/tools/handlers/multi_agents_common.rs:133",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/agent_path.rs:12",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/agent_path.rs:145",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control/spawn.rs:245",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control/spawn.rs:1342",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/protocol.rs:2915",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/rollout/src/lib.rs:52",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/rollout/src/recorder.rs:952",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/rollout/src/recorder.rs:1124"
      ],
      "fix_request": "Keep the new-allocation bounds, but preserve or explicitly migrate historical identities without silently truncating their routing keys. Add real entry-point resume/rollout regressions for old-valid over-cap identities, and retain the new-spawn refusal/at-cap assertions and model-context hard bound.",
      "reported_by": [
        "TASK-261011-3l5dnu"
      ]
    },
    {
      "id": "persisted-agent-path-caps-break-resume",
      "row": "marker lifecycle",
      "invariant": "AGENTS.md breaking-change review includes resuming sessions from existing rollouts. Bounding newly created spawn identities must not silently invalidate identities already stored by the base implementation.",
      "mechanism": "The new >128-byte segment and >1024-byte total checks are in AgentPath::from_string validation, not only new-spawn admission. AgentPath uses serde(try_from=\"String\"), so every deserialization gets the new restrictions. Both /root/ plus 129 lowercase a characters (135 bytes total) and an old-valid 1025-byte multi-segment path are accepted on the CR base and rejected on the candidate. SessionMeta.source contains SubAgentSource::ThreadSpawn.agent_path: Option<AgentPath>; the canonical rollout decoder calls serde_json::from_value without a legacy-path migration. Thus a previously valid V2 child SessionMeta line now fails decoding. load_rollout_items skips that line as a parse error, loses the canonical thread id in an ordinary one-header child rollout, and get_rollout_history returns failed to parse thread ID from rollout file. Independently, resume_single_agent_from_rollout parses stored_thread.agent_path with AgentPath::try_from and returns InvalidRequest(invalid stored agent path ...); restore_v2_agent_metadata warns and omits metadata for the same identities. This is a source-established compatibility regression, not an observed Rust/live-resume run. New-spawn limits were explicitly requested by the rework brief; applying them retroactively to persisted identities without a migration was not covered by its new-spawn tests.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261011-3dpjl3-path-assay.py (full script embedded in this outcome)",
          "command": "python3 .temp/TASK-261011-3dpjl3-path-assay.py --legacy",
          "expected_failure": "Observed expected-red exit 1: the source-transcribed compatibility assertion fails for a previously valid 129-byte segment. Seven tree-pinned git-show subprocesses each exit 0; exact-cap, short-name, invalid-syntax and 1025-byte-path controls pass first. This executes Python source-contract checks only; Rust, Serde and public resume are not executed.",
          "exit_code": 1,
          "executed": true,
          "pinned_blobs": [
            "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:.temp/TASK-261011-3dpjl3-path-assay.py (full script embedded in this outcome)"
          ]
        },
        {
          "test_file": "codex-rs/core/src/agent/control_tests.rs (requested: resume_v2_child_preserves_legacy_long_agent_path)",
          "command": "Hosted only, requested and not run: just test -p codex-core -E 'test(resume_v2_child_preserves_legacy_long_agent_path)'",
          "expected_failure": "Persist base-format V2 child metadata with a 129-byte segment and, separately, a 1025-byte valid multi-segment path. Drive the actual resume_agent entry into LocalAgentControl::resume_agent_from_rollout -> resume_single_agent_from_rollout; require restored child identity/routing rather than invalid stored agent path or missing metadata. Current candidate should refuse these legacy identities. Add a rollout parser control in codex-rollout recorder_tests.rs requiring the same legacy header to preserve thread_id with zero parse errors. Keep 128-byte fresh-spawn acceptance and 129-byte fresh-spawn refusal controls. None of these requested Rust tests was added or run by this panel.",
          "executed": false,
          "pinned_blobs": [
            "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control_tests.rs (requested: resume_v2_child_preserves_legacy_long_agent_path)"
          ]
        }
      ],
      "severity": "regression",
      "priority": "P1",
      "repeat-of": "none",
      "requested_change": "Separate new-spawn admission from legacy persistence compatibility, or provide an explicit compatible migration that preserves routing identity and readable old rollouts. Keep the full outgoing interruption item bounded when legacy paths are restored; merely admitting legacy unbounded AgentPaths would reopen the previous envelope finding. Obtain exact revised-tree hosted legacy-resume/rollout-decoder evidence, including a narrowing mutant that incorrectly applies fresh-spawn caps to legacy restoration.",
      "sources": [
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/agent_path.rs:12",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/agent_path.rs:141",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/agent_path.rs:171",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/protocol.rs:2915",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/protocol.rs:3153",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/rollout/src/lib.rs:52",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/rollout/src/recorder.rs:1124",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/rollout/src/recorder.rs:1156",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control/spawn.rs:1342",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control/spawn.rs:241"
      ],
      "reported_by": [
        "TASK-261011-3dpjl3"
      ]
    }
  ],
  "notes": [
    "[TASK-261011-3l5dnu] Exact evidence reused: CR rev4 validation log names candidate 5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8 and hosted run 38077935582, ends [exit 0], coverage_unit=exact_command_shard required=1 green=1 failed=0 missing=0 test_case_coverage=unknown. Its 385-byte log is readable; no inference from older/truncated logs. Hosted precheck 12 reports lint/small/core/app-server success and 9/9 killed mutants. Neither suite nor mutant execution was rerun here. Per-test numeric exit codes, individual mutant run IDs and exact test-case totals are not supplied and remain unknown.",
    "[TASK-261011-3l5dnu] Prior-round disposition: the typed interruption fragment, 256-byte prose-path truncation and release-effective 682-byte body cap hold. New allocations now bound author/recipient at their source; spawn refusal test kills the source-length mutant. The rev3 unbounded-new-identity mechanism is repaired. This round identifies a distinct introduced historical-read regression, not repeat-of the old envelope bypass.",
    "[TASK-261011-3l5dnu] P0 manual context review flag: conservative author+recipient+body byte budget is 2730 excluding fixed framing (1024+1024+682). This is a hard byte bound, not proof of <1K actual model tokens. Actual tokenizer count on adversarial maximum-length random names was not executed; producer under-1K estimate must not substitute for the additional manual review required for potentially >1K-token items. Body alone is at most 682 bytes.",
    "[TASK-261011-3l5dnu] Coverage measured as 7/7 surface rows swept: 6 held under stated bounds, 1 broken by a static compatibility witness, 0 not-attacked. Nine shipped mutant patches apply-check green; hosted summary reports nine killed. This does not claim one dedicated mutant per row or exhaustive AC coverage. AC5/8/9 remain partial; AC6 enabled-reminder behavior is static-only.",
    "[TASK-261011-3l5dnu] Carried lifecycle suspicion, not an additional reproduced finding: async clear/status cleanup drops the goal permit before looking up the thread and removes by owned prefix; old cleanup may touch a newer generation. Disable/stop may interleave with post-inspection registration. Request old-cleanup/new-generation and stop-at-registration tests if these interleavings need certification.",
    "[TASK-261011-3l5dnu] Carried release advisory: candidate-wide release_native_wait search finds one public runtime method and one suite invocation, no internal production trigger/service forwarder. The mechanism is exercised but broader trigger wiring is unknown.",
    "[TASK-261011-3l5dnu] Full CR is 31 files +2313/-16, beyond the 800-line nonmechanical guideline; the new integration suite is 1082 lines. Rev4 source-bound repair is small, but overall staging remains a reviewer concern. Cargo.toml/Cargo.lock add the codex-extension-items dependency edge; MODULE.bazel.lock is unchanged. Whether bazel-lock-update ran is not established; no lock drift reproduced.",
    "[TASK-261011-3l5dnu] Global installed reviewer role was read at /Users/administrator/.roles/reviewer/role.md; it lacks the referenced review-round section. Applied the explicit panel brief surface-sweep/bounded-hunt rules. Skill-relative reviewer role path was missing, not assumed to exist.",
    "[TASK-261011-3l5dnu] Scope: no builds/tests/cargo/just, source edits, commits, branch operations or nested worktree. Candidate read only via pinned git blobs. Temporary index ordinary worktree index untouched. Source task received only reads (q/resource get); no accept/reject/status/handoff/notes/resource/checklist write there.",
    "[TASK-261011-3l5dnu] Logbook: no standalone logbook command or board logbook mutation is installed. The portable logbook entry in this outcome and panel-scoped board notes record the new regression, evidence limitations and decision; no control-root logbook edited.",
    "[TASK-261011-297lwc] [replay-identity] Patch replayed through temp index: read-tree exit 0, apply --cached exit 0, write-tree exit 0 printing 5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8, exactly the expected candidate tree. Hosted precheck 12 run 38077935582 snapshotted that tree (lint/small/core/app-server success, 9/9 mutants killed). CR rev4 validation log (385 bytes, untruncated) records mini-hosted-gate.sh exit 0 with coverage_unit=exact_command_shard.",
    "[TASK-261011-297lwc] [rev3-findings-closed] Both rev3 bypass findings (interrupted-agent-message-envelope-unbounded, interrupted-fragment-unbounded-paths; repeat-of rev2 cap findings) are closed at identity creation, per g1-rework-brief-review3.md. All AgentPath constructors (join/resolve/try_from/FromStr/serde) funnel through from_string into validate_absolute_path; the tuple field is module-private and root()/morpheus() are short consts, so no value can exceed 128-byte segments or 1024-byte paths. InterAgentCommunication.author/recipient are typed AgentPath (protocol.rs struct), so the envelope is bounded wherever it is built. The rev3 fragment truncation is retained as defense in depth with byte-identical logic (comment-only delta). Full new item: author/recipient <= 1024 each + body <= 682 = <= 2730 bytes, ~683 tokens at the repo 4-bytes/token estimate: under the 1K P0/manual-review threshold and far under the 10K ceiling (AGENTS.md rules 3-5 satisfied for the new item). Independently recomputed by this panel (python3 exit 0): prose 142 + 2*(256+14) = 682; source-valid 914-byte fixtures render exactly 682.",
    "[TASK-261011-297lwc] [refusal-chain] No spawn-handler edit was needed and none was made: thread_spawn_source (multi_agents_common.rs) already maps join errors to FunctionCallError::RespondToModel, and the V2 spawn entry calls it with ? before agent_control.spawn, so refusal precedes thread creation. spawn_agent_v2_rejects_overlong_task_name asserts the exact length error AND unchanged list_thread_ids; spawn_agent_v2_accepts_task_name_at_cap asserts success plus exactly one new thread. The narrowing mutant spawn_task_name_length_unchecked (segment check removed, charset/reserved/total checks kept) is killed by the refusal test on the exact tree. V1 spawn and resume_agent pass task_name None and are unaffected. Default max spawn depth is 1 (typical path <= 134 bytes); only ~8-deep all-max-length chains approach 1024, refused with an explicit tool error, never silently truncated, with no routing aliases.",
    "[TASK-261011-297lwc] [mutant-coverage] 9/9 hosted narrowing mutants killed by named tests on the exact tree. The total-cap check (MAX_PATH_BYTES) has no dedicated narrowing mutant, but both of its branches are pinned by boundary unit tests (1205-byte multi-segment path rejected with the exact error; constructed exactly-1024-byte path accepted), which is delete-equivalent coverage; the segment check has both boundary tests and the narrowing mutant. Not a finding.",
    "[TASK-261011-297lwc] [breaking-change-scan] No app-server API, CLI, or config change. Resume is fail-soft: rollout decode errors skip the line and increment parse_errors (recorder.rs), so a hypothetical pre-existing overlong path degrades to one skipped record, never a resume failure; SessionMeta.agent_path stays Option String and cannot break deserialization. No production expect/unwrap on AgentPath parsing of model-supplied input (only test helpers and constant paths). AgentStatus::is_final match is unchanged (status.rs delta is tests only). The AgentPath grammar narrowing is explicit, documented, and tested per the rework brief; it rejects rather than aliases identities.",
    "[TASK-261011-297lwc] [delta-scope] rev3 (9ccda921) to rev4 (5a51cf52) touches exactly 5 files (+216/-6): protocol agent_path.rs (the bound + 4 boundary tests), multi_agents_tests.rs (refusal/at-cap tests), goal_native_wait.rs (envelope identity + cap asserts in the interrupt test), and the fragment file plus its tests (comment refresh + source-valid 914-byte fixtures). All other 26 CR paths are byte-identical to rev3, so rev3 held-row evidence on unchanged code still applies; every row was re-swept against precheck-12 evidence anyway.",
    "[TASK-261011-297lwc] [carried-bounds-and-advisories] Producer-stated partial coverage stands, unchanged by this delta: no dedicated live-child check-in reinsertion test, no exhausted-retention plus late-wake live test, no disable/stop interleave test, no full resume_thread_with_history with a rendered SleepItem, no second-child-mid-turn or repeated-interrupt-transition integration, no explicit non-default inherited-settings assert on the native path, and the AC6 fixture disables CurrentTimeReminder (enabled-reminder preservation by source inspection only). release_native_wait still has exactly 2 tree references (definition + one suite call): mechanism tested, no production caller. Stale-clear/new-generation interleaving remains mitigated by per-thread request serialization with no demonstrated reproduction. None is a reproduced failure.",
    "[TASK-261011-297lwc] [size-and-deps] Base..rev4: 31 files, +2313/-16 (over the 800-line guidance; ~half is the integration suite plus tests; the rev3->rev4 delta under review is +216/-6). Cargo delta is exactly the intra-workspace codex-extension-items edge; MODULE.bazel.lock unchanged. Whether bazel-lock-update ran is unknown from the gate summary, not a reproduced failure. No new include_str/compile-data resources.",
    "[TASK-261011-297lwc] [scope] Read-only on TASK-260929-csyzcj: only q and resource get were used there. No accept_cr, reject_cr, withdraw_cr, set_status, handoff, notes, resource, or checklist write on that task. No cargo/just/build/test, no nested worktree, no commit/branch operations. All board writes target TASK-261011-297lwc exclusively.",
    "[TASK-261011-3dpjl3] {'id': 'delta-order', 'text': 'Reviewed all 2/2 merged rev3 findings first, then the same-class creation/serialization/persistence routes, then rework regressions and all 7/7 prescribed surfaces. rev3->rev4 is exactly five paths: protocol agent_path, spawn tests, interrupted integration envelope assertions, fragment doc, and source-valid fragment test fixture. Registration/race/cleanup implementation is byte-identical to rev3.'}",
    "[TASK-261011-3dpjl3] {'id': 'evidence-identity', 'text': 'Temporary-index replay equals expected candidate 5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8. Precheck 12 summary binds run 38077935582 to this tree with lint/small/core/app-server success and 9/9 named mutant kills. All 9 attached patches independently pass git apply --cached --check against the candidate index. This proves patch coherence, not locally rerun mutant kills. The CR validation log is 385 bytes, untruncated for this revision, and records mini-hosted-gate exit 0, exact_command_shard required=1 green=1, test_case_coverage=unknown. Individual hosted command exit codes and mutant run IDs are not supplied and remain unknown. No CI was independently rerun by this panel.', 'sources': ['board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md', 'board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_results.md', 'board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_change-request_rev4-validation.log']}",
    "[TASK-261011-3dpjl3] {'id': 'coverage-ratio', 'text': 'Surface sweep 7/7; exactly one result per row: held 6/7, broken 1/7, not-attacked 0/7. Prior merged findings addressed 2/2 for new identities. Hosted shipped mutants killed 9/9 per attached summary; local patch coherence 9/9. These are distinct measured ratios, not full AC subcase coverage. Producer says 9/9 AC rows have driving tests with partial AC5/8/9 coverage. Unexecuted tests below are requests, not successes.'}",
    "[TASK-261011-3dpjl3] {'id': 'requested-tests', 'text': 'Beyond the required legacy-resume/rollout controls in the finding: requested but not run goal_wait_checkin_reinserts_with_live_child, goal_wait_exhausted_checkins_late_child_completion_wakes, goal_wait_disable_stop_during_registration, goal_wait_resume_rendered_sleep_with_unloaded_child, goal_wait_wake_preserves_nondefault_turn_settings, goal_wait_second_child_completes_mid_turn, goal_wait_second_interruption_transition, and goal_wait_bounds_max_nested_agent_message. For total-path source gate narrowing, remove only MAX_PATH_BYTES rejection while retaining 128-byte segment checks and require a real nested spawn at 1024/past-1024 boundary to kill it.'}",
    "[TASK-261011-3dpjl3] {'id': 'carried-advisories', 'text': 'Explicit release_native_wait is public but has only a suite caller and no production service forwarding; unchanged advisory. Prefix-only cleanup is atomic against foreign sleep but not proof against newer own generations after an asynchronous lookup; no reachable deterministic stale-clear reproduction established here. Pre-existing completion payload text remains outside this leaf. Cargo adds an existing workspace extension-items edge; MODULE.bazel.lock unchanged and bazel-lock-update execution is not attached, so lock drift is unknown. Base->candidate delta is 31 files, 2313 additions/16 deletions, including a new 1082-line integration module; unchanged staging advisory is primitive inspection/atomic removal first, then goal integration/notice behavior.'}",
    "[TASK-261011-3dpjl3] {'id': 'scope', 'text': 'No builds, Rust tests, cargo/just, product edits, nested worktrees, archives, commits, branch operations or source-task mutations ran. Candidate blobs are tree-pinned; local scratch copies only aid static reads. Researcher writes and outcome attachment target TASK-261011-3dpjl3 only. No recording-review action is taken on TASK-260929-csyzcj.'}",
    "[TASK-261011-3dpjl3] {'id': 'logbook', 'text': 'No logbook executable is available (command -v logbook exit 1), and enabled tools expose no logbook writer. The task-scoped review logbook entry is preserved in this single plain-text outcome and own-task notes; no external logbook write is claimed.'}"
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "Hosted goal_wait_registers_marker_and_wakes_on_child_completion drives V2 spawn, goal idle and an actual parent model request carrying child completion. ignore_native_pending is killed. The single ExtensionData SleepItem slot prevents double attachment; queue-only mail reaches the shared scheduler after registration.",
      "bound": "Running-child wake executed hosted, not locally. Does not establish every mail/registration concurrency permutation.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:247",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/runtime.rs:699",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/session/handlers.rs:76",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/tasks/mod.rs:521"
      ],
      "reported_by": "TASK-261011-3l5dnu"
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Hosted pending_native_work_is_only_pending_init_and_running and owned_children_inspection_propagates_failed_lookups attack terminal states, known Unloaded and unknown-child Err; skip_failed_lookups is killed. Non-goal ordinary-parent interruption stays quiet. Production idle checks active goal/host before inspection; inspect_owned_child_ids distinguishes ThreadNotFound+known membership from unknown and propagates other errors.",
      "bound": "Error attack is an internal inspection helper test, not forced registry/backend failure through the entire idle entry. No new marker is inserted after an Err; existing-marker retention on a transient Err is not independently attacked.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control/runtime_context.rs:150",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/owned_children.rs:65",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/runtime.rs:683"
      ],
      "reported_by": "TASK-261011-3l5dnu"
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Hosted goal_wait_latch_closes_completion_before_registration kills insert_after_mail_check. It releases the gate only after confirmed mailbox enqueue, keeps a second Running child, forbids a masking second idle pass, bounds waits and asserts the actual mail-wake request without goal steering. Candidate inserts before recheck and shares its held semaphore permit with on_turn_start using the existing scoped lease.",
      "bound": "Final-completion interleaving is executed; interruption before registration is a separate unexecuted scenario. No local Rust execution.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:366",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:485",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/runtime.rs:722"
      ],
      "reported_by": "TASK-261011-3l5dnu"
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "Hosted goal_wait_preserves_foreign_sleep_across_register_and_turn_start compares the complete foreign item during registration and admitted turn start. insert_clobbers_one_foreign and unconditional_remove are killed by that suite plus named lease tests. insert_if/remove_if perform predicate and mutation under the ExtensionData lock. Candidate-wide search finds no other production minter of goal-wait IDs.",
      "bound": "Foreign namespace protection established. Cleanup of a newer goal-owned generation by older async cleanup is not covered by these attacks.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:623",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/native_wait.rs:42",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/extension-api/src/state.rs:140"
      ],
      "reported_by": "TASK-261011-3l5dnu"
    },
    {
      "row": "marker lifecycle",
      "result": "broken",
      "evidence": "New legacy-agent-path-resume-regression: the shared AgentPath parser now refuses pre-cap identities during stored-child restoration and rollout decoding. A base-valid 129-byte segment fails the candidate 128-byte check. Static compatibility assay exit 1 (expected red). Hosted clear/release/restore and turn-start tests still hold for short identities; exhausted check-in evaluation is exercised by small tests.",
      "bound": "Static source witness, not an executed Rust resume. Request hosted legacy-session/closed-child resume regressions. Existing coverage also lacks live-child paused-clock check-in reinsertion, exhausted-retention plus late wake, disable/stop races and a full rendered-SleepItem history resume.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/agent_path.rs:145",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control/spawn.rs:1342",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/rollout/src/recorder.rs:1124",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:731"
      ],
      "reported_by": "TASK-261011-3l5dnu"
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "Hosted registration/wake test asserts 500ms parent event silence and absence of goal-wait history text/current_time from the wake request. Static try_register_goal_wait_sleep only stores ExtensionData; it calls no UI, rollout/history or reminder API. Check-in timing remains with the goal scheduler.",
      "bound": "CurrentTimeReminder is disabled in this fixture. An enabled reminder schedule is source-inspected, not independently executed; no dedicated side-effect mutant is supplied.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:326",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/native_wait.rs:42"
      ],
      "reported_by": "TASK-261011-3l5dnu"
    },
    {
      "row": "child state transitions",
      "result": "held",
      "evidence": "Hosted real Op::Interrupt registered/ordinary-parent tests prove one queue-only INTERRUPTED notice/wake, no success claim and ordinary-parent silence; duplicate and success-wording mutants are killed. Global is_final remains unchanged. Typed ContextualUserFragment truncates each prose path; rev4 rejects newly allocated paths over 128 bytes/segment or 1024 bytes total before spawning. Hosted SpawnAgentHandlerV2 refusal/at-cap tests and spawn_task_name_length_unchecked kill establish the new allocation gate.",
      "bound": "These attacks cover one interruption transition, short envelope identities and new-name boundaries. Reused/error state classification is helper-level; second-child-mid-turn, repeated-interruption transitions and non-default inherited-settings assertions are not independently reported. Scheduler code preserves the existing settings path. Legacy parser regression is reported once in lifecycle row.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:774",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control/completion.rs:92",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/context/inter_agent_interrupted_message.rs:73",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/tasks/mod.rs:604"
      ],
      "reported_by": "TASK-261011-3l5dnu"
    }
  ],
  "free_hunt": [
    "[TASK-261011-3l5dnu] {\"budget_minutes\": 3, \"started_at_utc\": \"2026-10-10 20:24:38 UTC\", \"ended_at_utc\": \"2026-10-10 20:26:09 UTC\", \"examined\": [\"shared AgentPath deserialize/resolve versus create admission\", \"persisted V2 registry restoration and real resume_agent call chain\", \"canonical rollout decoder/SessionMeta persistence\", \"new interruption body and envelope arithmetic\", \"foreign namespace/generation cleanup\", \"explicit release callsites\", \"dependency/Bazel/size footprint\"], \"findings\": [\"legacy-agent-path-resume-regression\"], \"unexecuted_suspicions\": [\"old cleanup versus new goal generation\", \"stop/disable during registration\", \"maximum-name actual tokenizer count\"], \"scope\": \"Bounded static hunt plus exact-tree hosted attacks already attached. No local Rust execution.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"cap-arithmetic recompute\", \"result\": \"no-finding\", \"evidence\": \"Independent python3 recomputation (exit 0): prose 142 + 2*(256+14) = 682; source-valid 914-byte fixtures render exactly 682; worst-case full item 1024+1024+682 = 2730 bytes, ~683 tokens. Matches the const derivation and producer claims.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"AgentPath constructor audit\", \"result\": \"no-finding (closes rev3 bypass)\", \"evidence\": \"Full-file read: join/resolve/try_from/FromStr/serde all funnel through from_string into validate_absolute_path (total + per-segment caps); tuple field is module-private; root()/morpheus() are short consts. No unchecked construction site exists on the tree.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"spawn refusal ordering\", \"result\": \"no-finding\", \"evidence\": \"V2 spawn calls thread_spawn_source with ? (multi_agents_v2/spawn.rs:148) before agent_control.spawn; join errors map to RespondToModel in the shared helper. Refusal-before-creation is asserted by list_thread_ids equality in the new test.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"production panic grep\", \"result\": \"no-finding\", \"evidence\": \"No expect/unwrap on AgentPath parse/join/resolve in production code; hits are test helpers and constant paths. Model-supplied long names become tool errors, never panics.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"resume with pre-existing overlong paths\", \"result\": \"no-finding\", \"evidence\": \"Rollout decode errors skip the line and count parse_errors (recorder.rs); resume continues. Old overlong paths would degrade to skipped records, not failed resumes; SessionMeta.agent_path is Option String and cannot break parsing.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"V1 and resume spawn paths\", \"result\": \"no-finding\", \"evidence\": \"V1 spawn and resume_agent both pass task_name None to thread_spawn_source: unaffected by the new bound.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"depth versus total cap\", \"result\": \"no-finding\", \"evidence\": \"DEFAULT_AGENT_MAX_DEPTH is 1, so default-config paths stay <= 134 bytes; approaching 1024 needs ~8-deep all-max-length chains, refused with an explicit error. No realistic regression.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"wake-gate and namespace squat\", \"result\": \"no-finding\", \"evidence\": \"has_outstanding_durable_sleep (tasks/mod.rs:521) grants queue-only mail a turn for any stored SleepItem, which the recheck path calls; goal_wait_sleep_id is the sole minter of the goal-wait: prefix, and insert_if never overwrites foreign ids.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"turn_finished fan-out for Interrupted\", \"result\": \"no-finding\", \"evidence\": \"turn_finished routes solely to notify_parent_of_terminal_turn (control/api.rs), which early-returns for ordinary parents; the only new effect of Interrupted reaching it is the marker-gated notice.\"}",
    "[TASK-261011-297lwc] {\"probe\": \"release wiring and dependency footprint\", \"result\": \"no-finding (advisories carried)\", \"evidence\": \"release_native_wait still has exactly 2 tree references (def + suite call); Cargo delta is the intra-workspace codex-extension-items edge only; MODULE.bazel.lock unchanged; no new file-level resources.\"}",
    "[TASK-261011-3dpjl3] {\"budget_minutes\": 3, \"started_at_utc\": \"2026-10-10 20:43:46 UTC\", \"ended_at_utc\": \"2026-10-10 20:44:11 UTC\", \"examined\": [\"all production goal-wait prefix mint/removal callsites\", \"explicit release forwarding\", \"shared AgentPath construction and persistence compatibility\", \"source-valid body-cap fixture\", \"Cargo dependency/lock and Bazel metadata\", \"exhausted check-in policy and cleanup wiring\"], \"result\": \"No additional finding beyond persisted-agent-path-caps-break-resume. Generation interleavings/release reachability/lock drift stay bounded advisories. Static hunt ended within budget; no Rust execution.\"}"
  ]
}
```
