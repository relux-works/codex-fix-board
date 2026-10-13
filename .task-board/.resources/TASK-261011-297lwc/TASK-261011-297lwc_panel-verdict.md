# Panel B verdict — TASK-260929-csyzcj CR-TASK-260929-csyzcj-4 rev4 (R141, non-recording)

Panel task: TASK-261011-297lwc. Review target: TASK-260929-csyzcj CR revision 4.
Base commit 39c264c34e61b5171ae13b0f756746c24ea5f51a. Expected candidate tree
5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8.

Verdict: accept

## Replay tree check (mandatory, first)

Replay through temporary index .temp/TASK-261011-297lwc-replay.idx (no nested
worktree, no builds):

- GIT_INDEX_FILE read-tree of base 39c264c3 — exit 0
- task-board resource get of TASK-260929-csyzcj_change-request_rev4.patch — exit 0
- GIT_INDEX_FILE git apply --cached of the patch — exit 0
- GIT_INDEX_FILE git write-tree printed 5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8 — exit 0

Replay tree EQUALS the expected candidate tree. No mismatch, review proceeds.
Candidate files were read tree-pinned (git show / git archive of 5a51cf52).

## Commands run with exit codes (this panel)

- task-board m set_status(TASK-261011-297lwc, status=analysis) — exit 0
- task-board q get(TASK-260929-csyzcj) description/scope/ac — exit 0
- task-board q outcomeResources / preconditionResources name listings — exit 0
- task-board resource get, 12 input resources (surface-table, producer-brief,
  results, mutants, rev4 validation log, precheck-12, handoff notes, rev3
  recording brief, rev3 verdict, review3 rework brief, orch fix 11, rev4
  handoff) — all exit 0
- git read-tree / apply --cached / write-tree replay chain — all exit 0
- git diff --stat base..candidate (31 files, +2313/-16) — exit 0
- git diff --stat rev3..rev4 (5 files, +216/-6) — exit 0
- git archive candidate changed paths + tar extract — exit 0
- git show / git grep pinned reads (spawn handler, completion, protocol,
  rollout resume, depth config, release callers, wake gate) — all exit 0
- python3 cap-arithmetic recomputation — exit 0
- Discovery-only failure: one task-board q with unknown field resources —
  exit 1, corrected to outcomeResources, not evidence of anything
- No cargo, just, build, or test command was run (forbidden by the brief;
  one codex-fix build at a time). No commit, branch, or worktree operation.
  No accept/reject/status/handoff/notes/resource/checklist write on
  TASK-260929-csyzcj: only q and resource get touched it.

## Evidence posture

Execution evidence is reused attached evidence on the exact replayed tree:
hosted precheck 12 (run 38077935582: lint/small/core/app-server success,
9/9 narrowing mutants killed by named tests) and the CR rev4 validation log
(mini-hosted-gate.sh exit 0, exact_command_shard green). Nothing was rerun
by this panel. Per-test exit codes and per-mutant run IDs are not in the
attached summaries and are unknown, not inferred.

## Headline

Both rev3 bypass findings (interrupted-agent-message-envelope-unbounded,
interrupted-fragment-unbounded-paths, same mechanism) are closed at the
source: every AgentPath value is now bounded (128-byte segments, 1024-byte
absolute paths) by construction, the INTERRUPTED envelope carries only typed
AgentPath identities, and the full new item is at most 2730 bytes (~683
repo-estimated tokens), under the 1K P0 threshold and far under the 10K
ceiling. The public-entry refusal test and its narrowing mutant are green
and killed on the exact tree. All 7 surface rows held. No new findings.

```verdict-findings
{
  "findings": [],
  "notes": [
    "[replay-identity] Patch replayed through temp index: read-tree exit 0, apply --cached exit 0, write-tree exit 0 printing 5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8, exactly the expected candidate tree. Hosted precheck 12 run 38077935582 snapshotted that tree (lint/small/core/app-server success, 9/9 mutants killed). CR rev4 validation log (385 bytes, untruncated) records mini-hosted-gate.sh exit 0 with coverage_unit=exact_command_shard.",
    "[rev3-findings-closed] Both rev3 bypass findings (interrupted-agent-message-envelope-unbounded, interrupted-fragment-unbounded-paths; repeat-of rev2 cap findings) are closed at identity creation, per g1-rework-brief-review3.md. All AgentPath constructors (join/resolve/try_from/FromStr/serde) funnel through from_string into validate_absolute_path; the tuple field is module-private and root()/morpheus() are short consts, so no value can exceed 128-byte segments or 1024-byte paths. InterAgentCommunication.author/recipient are typed AgentPath (protocol.rs struct), so the envelope is bounded wherever it is built. The rev3 fragment truncation is retained as defense in depth with byte-identical logic (comment-only delta). Full new item: author/recipient <= 1024 each + body <= 682 = <= 2730 bytes, ~683 tokens at the repo 4-bytes/token estimate: under the 1K P0/manual-review threshold and far under the 10K ceiling (AGENTS.md rules 3-5 satisfied for the new item). Independently recomputed by this panel (python3 exit 0): prose 142 + 2*(256+14) = 682; source-valid 914-byte fixtures render exactly 682.",
    "[refusal-chain] No spawn-handler edit was needed and none was made: thread_spawn_source (multi_agents_common.rs) already maps join errors to FunctionCallError::RespondToModel, and the V2 spawn entry calls it with ? before agent_control.spawn, so refusal precedes thread creation. spawn_agent_v2_rejects_overlong_task_name asserts the exact length error AND unchanged list_thread_ids; spawn_agent_v2_accepts_task_name_at_cap asserts success plus exactly one new thread. The narrowing mutant spawn_task_name_length_unchecked (segment check removed, charset/reserved/total checks kept) is killed by the refusal test on the exact tree. V1 spawn and resume_agent pass task_name None and are unaffected. Default max spawn depth is 1 (typical path <= 134 bytes); only ~8-deep all-max-length chains approach 1024, refused with an explicit tool error, never silently truncated, with no routing aliases.",
    "[mutant-coverage] 9/9 hosted narrowing mutants killed by named tests on the exact tree. The total-cap check (MAX_PATH_BYTES) has no dedicated narrowing mutant, but both of its branches are pinned by boundary unit tests (1205-byte multi-segment path rejected with the exact error; constructed exactly-1024-byte path accepted), which is delete-equivalent coverage; the segment check has both boundary tests and the narrowing mutant. Not a finding.",
    "[breaking-change-scan] No app-server API, CLI, or config change. Resume is fail-soft: rollout decode errors skip the line and increment parse_errors (recorder.rs), so a hypothetical pre-existing overlong path degrades to one skipped record, never a resume failure; SessionMeta.agent_path stays Option String and cannot break deserialization. No production expect/unwrap on AgentPath parsing of model-supplied input (only test helpers and constant paths). AgentStatus::is_final match is unchanged (status.rs delta is tests only). The AgentPath grammar narrowing is explicit, documented, and tested per the rework brief; it rejects rather than aliases identities.",
    "[delta-scope] rev3 (9ccda921) to rev4 (5a51cf52) touches exactly 5 files (+216/-6): protocol agent_path.rs (the bound + 4 boundary tests), multi_agents_tests.rs (refusal/at-cap tests), goal_native_wait.rs (envelope identity + cap asserts in the interrupt test), and the fragment file plus its tests (comment refresh + source-valid 914-byte fixtures). All other 26 CR paths are byte-identical to rev3, so rev3 held-row evidence on unchanged code still applies; every row was re-swept against precheck-12 evidence anyway.",
    "[carried-bounds-and-advisories] Producer-stated partial coverage stands, unchanged by this delta: no dedicated live-child check-in reinsertion test, no exhausted-retention plus late-wake live test, no disable/stop interleave test, no full resume_thread_with_history with a rendered SleepItem, no second-child-mid-turn or repeated-interrupt-transition integration, no explicit non-default inherited-settings assert on the native path, and the AC6 fixture disables CurrentTimeReminder (enabled-reminder preservation by source inspection only). release_native_wait still has exactly 2 tree references (definition + one suite call): mechanism tested, no production caller. Stale-clear/new-generation interleaving remains mitigated by per-thread request serialization with no demonstrated reproduction. None is a reproduced failure.",
    "[size-and-deps] Base..rev4: 31 files, +2313/-16 (over the 800-line guidance; ~half is the integration suite plus tests; the rev3->rev4 delta under review is +216/-6). Cargo delta is exactly the intra-workspace codex-extension-items edge; MODULE.bazel.lock unchanged. Whether bazel-lock-update ran is unknown from the gate summary, not a reproduced failure. No new include_str/compile-data resources.",
    "[scope] Read-only on TASK-260929-csyzcj: only q and resource get were used there. No accept_cr, reject_cr, withdraw_cr, set_status, handoff, notes, resource, or checklist write on that task. No cargo/just/build/test, no nested worktree, no commit/branch operations. All board writes target TASK-261011-297lwc exclusively."
  ],
  "surface_results": [
    {
      "row": "registration and wake",
      "result": "held",
      "evidence": "Hosted goal_wait_registers_marker_and_wakes_on_child_completion on the exact tree: marker asserted present, then a real parent_wake model request carrying the completion text; ignore_native_pending is killed by it. Static chain is connected: continue_if_idle typed inspection, atomic single-slot insert_if, recheck via maybe_start_turn_for_pending_work, and the has_outstanding_durable_sleep gate (tasks/mod.rs:521) granting queue-only mail a turn. Wake is proven by an observed request, not marker presence.",
      "bound": "Running-child idle and completion wake exercised; no claim of every trigger-mail or registration concurrency permutation. Code byte-identical to rev3.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:248",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/tasks/mod.rs:521"
      ]
    },
    {
      "row": "eligibility and inspection errors",
      "result": "held",
      "evidence": "Hosted pending_native_work_is_only_pending_init_and_running and owned_children_inspection_propagates_failed_lookups; skip_failed_lookups is killed. Static: live ThreadSpawn edges inspected per child; ThreadNotFound goes through ensure_agent_known to Unloaded vs UnknownChild; other backend failures return InspectionFailed; continue_if_idle propagates Err with ? (no marker, error out) instead of reading empty. Goal/status/host eligibility precedes registration.",
      "bound": "Unknown/unloaded/error attacks executed via the inspect_owned_child_ids helper plus an ordinary-parent public negative; a forced backend error through a live idle callback is not separately reported. Code byte-identical to rev3.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/agent/control/runtime_context.rs:150",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/runtime.rs:700"
      ]
    },
    {
      "row": "completion-before-registration race",
      "result": "held",
      "evidence": "Hosted goal_wait_latch_closes_completion_before_registration kills insert_after_mail_check: mail confirmed enqueued before gate release, a second Running child retained, no masking second idle pass, one real model wake asserted with no goal steering, all waits bounded, removal-before-TurnStarted asserted. Static: insert-before-recheck under the held goal permit shared via GoalTurnStartPermit/GoalTurnStartLease, so the synchronous on_turn_start avoids semaphore self-deadlock.",
      "bound": "Final-completion race covered; interruption landing before registration is a distinct unexecuted scenario. Code byte-identical to rev3.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:367",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/runtime.rs:719"
      ]
    },
    {
      "row": "foreign sleep ownership",
      "result": "held",
      "evidence": "Hosted insert_clobbers_one_foreign and unconditional_remove killed by the small lease tests and the foreign-sleep suite (whole-object preservation across register and turn start). Static: insert_if predicate accepts only absent-or-own-prefix; remove_if removes only own-prefix; predicate and mutation share the ExtensionData mutex; candidate-wide grep shows goal_wait_sleep_id is the sole minter of the goal-wait: prefix.",
      "bound": "Prefix ownership protects the foreign namespace; isolation across goal generations is not separately established. Code byte-identical to rev3.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/native_wait.rs:42",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/extension-api/src/state.rs:140"
      ]
    },
    {
      "row": "marker lifecycle",
      "result": "held",
      "evidence": "Hosted clear/release/resume suite drives GoalService clear, release_native_wait, and restore_after_resume; admitted-turn removal is proved by the retained-latch test; native_pending_exhausts_checkins_then_waits_without_deadline proves the exhausted-check-in wait policy. Static removals cover turn start (extension.rs on_turn_start), disable/stop (runtime.rs), goal clear/inactive paths, release, and resume (remove_native_wait_marker; resume removes, never restores). Post-exhaustion idle returns Wait without deleting the marker.",
      "bound": "Held for these attacks only. Live-child check-in reinsertion/late wake, disable/stop interleavings, full rendered-rollout resume, and a reachable stale-clear race remain unknown; explicit release has no production caller. Code byte-identical to rev3.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:732",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/extension.rs:262"
      ]
    },
    {
      "row": "side-effect silence",
      "result": "held",
      "evidence": "Hosted registration/wake test asserts a 500ms event-silence window after the insert and the absence of goal-wait: and current_time text from the wake request. Static: registration stores only ExtensionData with no history/event/reminder API call; the goal scheduler owns timers and warnings.",
      "bound": "The fixture disables CurrentTimeReminder; preserving an enabled reminder schedule is source-inspected, not separately executed; no dedicated silence mutant. Code byte-identical to rev3.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:327",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/ext/goal/src/native_wait.rs:42"
      ]
    },
    {
      "row": "child state transitions",
      "result": "held",
      "evidence": "Hosted real Op::Interrupt tests on the exact tree: the registered parent gets exactly one queue-only INTERRUPTED notice plus one wake request (scoped agent_message asserts: no FINAL_ANSWER, no success claim); the ordinary parent stays quiet with no mail and no wake; wording and duplicate-delivery mutants are killed; the global is_final match is unchanged. The rev3 envelope bypass is closed at the source: author/recipient are typed AgentPath (<=1024 each), body <= 682, full new item <= 2730 bytes (~683 tokens); spawn refusal and at-cap public-entry tests are green and the refusal mutant is killed; the suite asserts the envelope carries exactly author /root/worker and recipient /root within the caps. Static: turn_finished routes only to the marker-gated notify; ordinary parents return early; the rsplit+try_from parent derivation cannot newly fail on valid children.",
      "bound": "Actual tokenizer count not measured (repo 4-bytes/token estimate used). Reused/error helper states inspected; second-child-mid-turn, repeated-interrupt transitions, and non-default inherited wake settings lack dedicated reported execution.",
      "sources": [
        "board-resource://TASK-260929-csyzcj/TASK-260929-csyzcj_hosted-precheck-12.md",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/tests/suite/goal_native_wait.rs:775",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/protocol/src/agent_path.rs:22",
        "5a51cf5296c78fc1693cb6e1cfd2e7f776e2e5c8:codex-rs/core/src/tools/handlers/multi_agents_tests.rs:499"
      ]
    }
  ],
  "free_hunt": [
    "{\"probe\": \"cap-arithmetic recompute\", \"result\": \"no-finding\", \"evidence\": \"Independent python3 recomputation (exit 0): prose 142 + 2*(256+14) = 682; source-valid 914-byte fixtures render exactly 682; worst-case full item 1024+1024+682 = 2730 bytes, ~683 tokens. Matches the const derivation and producer claims.\"}",
    "{\"probe\": \"AgentPath constructor audit\", \"result\": \"no-finding (closes rev3 bypass)\", \"evidence\": \"Full-file read: join/resolve/try_from/FromStr/serde all funnel through from_string into validate_absolute_path (total + per-segment caps); tuple field is module-private; root()/morpheus() are short consts. No unchecked construction site exists on the tree.\"}",
    "{\"probe\": \"spawn refusal ordering\", \"result\": \"no-finding\", \"evidence\": \"V2 spawn calls thread_spawn_source with ? (multi_agents_v2/spawn.rs:148) before agent_control.spawn; join errors map to RespondToModel in the shared helper. Refusal-before-creation is asserted by list_thread_ids equality in the new test.\"}",
    "{\"probe\": \"production panic grep\", \"result\": \"no-finding\", \"evidence\": \"No expect/unwrap on AgentPath parse/join/resolve in production code; hits are test helpers and constant paths. Model-supplied long names become tool errors, never panics.\"}",
    "{\"probe\": \"resume with pre-existing overlong paths\", \"result\": \"no-finding\", \"evidence\": \"Rollout decode errors skip the line and count parse_errors (recorder.rs); resume continues. Old overlong paths would degrade to skipped records, not failed resumes; SessionMeta.agent_path is Option String and cannot break parsing.\"}",
    "{\"probe\": \"V1 and resume spawn paths\", \"result\": \"no-finding\", \"evidence\": \"V1 spawn and resume_agent both pass task_name None to thread_spawn_source: unaffected by the new bound.\"}",
    "{\"probe\": \"depth versus total cap\", \"result\": \"no-finding\", \"evidence\": \"DEFAULT_AGENT_MAX_DEPTH is 1, so default-config paths stay <= 134 bytes; approaching 1024 needs ~8-deep all-max-length chains, refused with an explicit error. No realistic regression.\"}",
    "{\"probe\": \"wake-gate and namespace squat\", \"result\": \"no-finding\", \"evidence\": \"has_outstanding_durable_sleep (tasks/mod.rs:521) grants queue-only mail a turn for any stored SleepItem, which the recheck path calls; goal_wait_sleep_id is the sole minter of the goal-wait: prefix, and insert_if never overwrites foreign ids.\"}",
    "{\"probe\": \"turn_finished fan-out for Interrupted\", \"result\": \"no-finding\", \"evidence\": \"turn_finished routes solely to notify_parent_of_terminal_turn (control/api.rs), which early-returns for ordinary parents; the only new effect of Interrupted reaching it is the marker-gated notice.\"}",
    "{\"probe\": \"release wiring and dependency footprint\", \"result\": \"no-finding (advisories carried)\", \"evidence\": \"release_native_wait still has exactly 2 tree references (def + suite call); Cargo delta is the intra-workspace codex-extension-items edge only; MODULE.bazel.lock unchanged; no new file-level resources.\"}"
  ]
}
```
