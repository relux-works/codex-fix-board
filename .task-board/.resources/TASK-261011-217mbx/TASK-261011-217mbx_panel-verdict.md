# R141 DELTA panel — revision 4 of waiting-capabilities-snapshot

Panel task: TASK-261011-217mbx — r141-panel-delta-task-260929-2is91w-rev4.
Reviewed CR-TASK-260929-2is91w-4, implementation task TASK-260929-2is91w — waiting-capabilities-snapshot.

accept

Replay tree check: **MATCH**, `523385e2bb27c606bd1cd7241b0825c77b7569e5`.
Base `e0eff057620104a416080da616256ee7f32bda1b` plus the resource patch gives exactly the expected candidate tree. A temporary index was used; no nested worktree, real-index mutation, source edit, build, test, commit, branch operation, or implementation-task write was performed.

## Commands and observed exit codes

Commands below ran directly as standalone processes. `IDX` below abbreviates `$PWD/.temp/TASK-261011-217mbx-replay.idx`.

| Command actually run | Exit | Observation |
|---|---:|---|
| `task-board m 'set_status(TASK-261011-217mbx, status=analysis)'` | 0 | Panel lifecycle only |
| `git rev-parse --show-toplevel` | 0 | Assigned Story worktree |
| `python3 -c 'from pathlib import Path; p=Path(".temp"); p.mkdir(exist_ok=True); (p/"TASK-261011-217mbx-replay.idx").unlink(missing_ok=True)'` | 0 | Prepare temporary index |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-217mbx-replay.idx" git read-tree e0eff057620104a416080da616256ee7f32bda1b` | 0 | Load prescribed base |
| `task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev4.patch --output .temp/TASK-260929-2is91w_change-request_rev4.patch` | 0 | Read-only patch retrieval |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-217mbx-replay.idx" git apply --cached .temp/TASK-260929-2is91w_change-request_rev4.patch` | 0 | Replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261011-217mbx-replay.idx" git write-tree` | 0 | Exact candidate OID above |
| `git diff --check e0eff057620104a416080da616256ee7f32bda1b 523385e2bb27c606bd1cd7241b0825c77b7569e5` | 0 | No whitespace errors |
| `git diff f8ae85582d54c47b237476e8d88742f942961f3f 523385e2bb27c606bd1cd7241b0825c77b7569e5` | 0 | Three-file rev3-to-rev4 delta |
| `git diff --stat` / `git diff --numstat` with prescribed base and candidate | 0 each | 21 paths, +2398/-6 |
| Python materialization using `git show <candidate>:<path>` | 0 | 31 pinned text files read into ignored scratch directory |
| `task-board q 'get(TASK-260929-2is91w) { description scope ac }'` | 0 | All AC read |
| `task-board resource get` for `surface-table.md`, `producer-brief.md`, results, mutants, merged rev3 verdict, hosted-precheck-11, and rev4-validation.log | 0 each | Read-only resources, all successfully materialized |
| `gh api repos/ivanopcode/codex/actions/runs/38152963091 --jq '{id,head_sha,status,conclusion,html_url}'` | 0 | Completed; overall conclusion failure (expected-red mutant jobs) |
| `gh api --paginate repos/ivanopcode/codex/actions/runs/38152963091/jobs --jq '.jobs[] \| {id,name,conclusion}'` | 0 | Plan/lint/three snapshot lanes success; 14/14 mutant core jobs failure |
| `gh api repos/ivanopcode/codex/actions/jobs/<ID>/logs > .temp/TASK-261011-217mbx-<name>.log` for IDs 114510035901, 114512075377, 114512075552, 114512075475 | 0 each | Plan, snapshot core, pairing mutant, null-ID mutant logs fetched |
| `gh api repos/ivanopcode/codex/git/commits/<SHA> --jq '{sha,tree:.tree.sha,message}'` for a27e1de3597943f045afd513179f352158983ea8, e4dd40c26eae9987e6957a4003ba9bd8c958e14c, 561cf29e354047178d3b77040be975aa4ea1ca52 | 0 each | Snapshot tree equals candidate; mutant names mapped independently |
| Python ANSI-stripped raw-log summaries | 0 | Counts and expected-red exits read without truncated-output inference |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` (guarded by nonempty run ID) | 0 | No directives; no active goal |

Routine `cat`, `sed`, `rg` source reads and successful compact board reads returned 0. Recovery diagnostics: the initial `mkdir -p .temp && rm -f ...` call was rejected before process creation (no exit code); the Python preparation above succeeded. The query with unknown field `resources` and `schema(operation=resources)` each exited 1, then exact resource reads succeeded. `task-board resource list` returned help with exit 0 and is not inventory evidence. The combined skill-reference `cat` exited 1 because the installed skill lacks `.roles/reviewer/role.md`; its negative-evidence reference was readable. Focused role-file searches returned 1 (no matches), and `command -v logbook` returned 1. These are not passing gates; the supplied panel review contract governs this review, and the logbook is recorded in this outcome and panel notes. No missing/truncated read is treated as green execution evidence.

Artifact verification: `python3 .temp/TASK-261011-217mbx-validate.py` ran directly and exited **0**: exactly one valid verdict-findings JSON object, one-word verdict, 7/7 unique surface rows in prescribed order, and 2/2 previous finding IDs accounted for. `git status --short` exited **0** with empty output; repository files are unchanged. No build or fmt requirement is triggered by this read-only panel.

## Execution evidence attribution

Accepted attached resource `TASK-260929-2is91w_hosted-precheck-11.md`, independently cross-checked against [hosted run 38152963091](https://github.com/ivanopcode/codex/actions/runs/38152963091). Its plan logs pin snapshot commit `a27e1de3597943f045afd513179f352158983ea8`; the Git commit API reports its tree as the exact candidate. The workflow dispatch head is a different commit and is not used as candidate identity.

No Rust command or mutant was rerun here. Snapshot core raw log reports **5121/5121 passed**, 11 skipped, 3 flaky tests recovered by configured retries. It independently shows PASS for the new null-server test, client-null control, server-ID control, orphan/mismatched refusals, both-path identity, receipt integration, and non-persistence checks. Successful hosted shell numeric exits are not printed in the inspected summary; their job conclusions are success, not invented exit codes. Local rev4 validation records the mini-hosted-gate command **exit 0**, `exact_command_shard` 1/1, and explicitly unknown test-case coverage; that command was not rerun here.

Both inspected mutant core commands were `INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-core -E "$expr" "${extra[@]}"` with the plan's waiting/search/orphan filter excluding three named quarantine tests. The `discovery_ignores_call_pairing` commit e4dd40c... yields **exit 100**, 419/424 passed and 5 failed. The `discovery_requires_server_call_id` commit 561cf29... yields **exit 100**, 421/424 passed and 3 failed. Those failures are expected mutant kills, not passing commands. The three null-ID mutant failures are exactly the client-null unit test, server-control unit test, and `suite::search_tool::server_null_id_discovery_updates_waiting_capabilities`; all three attempts fail. Pairing-mutant failures additionally include the two orphan refusals. The other 12 kills are accepted from the attached named table plus independently checked failing job conclusions; their raw logs and numeric exits were not fetched.

## Prior findings and logbook

**A3-F1 and D3-F1: addressed (2/2).** They describe one null-server discrepancy. Candidate discovery now uses the same two-pass call-ID set and exact orphan predicate as the pinned normalizer. Server Some/None, client None, paired client Some (any order), and non-server Some without a matching call agree with normalization. Hosted null-server entry-point and narrowing-mutant evidence establishes the requested regression proof. Earlier native provenance and orphan-client fixes remain in force. No new production defect established.

**Coverage bound:** 7/7 surface rows swept, 6 held, 0 broken, 1 not-attacked; 14/14 attached mutants killed; 2/14 mutant raw logs inspected. Four of five required configuration families have attached router attacks. Remote ModelsManager replacement-to-snapshot behavior remains unknown: its existing test directly edits resolved ModelInfo. This is the same explicitly bounded gap as the previous round, not a new regression or a claim that tests were skipped because local builds are prohibited.

Retain the size concern: 2404 changed lines, 1483-line test module. No size exception is granted. The smallest coherent staging remains snapshot/wiring/direct flags and receipt coverage first, with deferred discovery, provenance and real-search integration together subsequently; splitting this validated candidate is outside this read-only panel. Public Rust struct-literal compatibility changes remain noted; wire/config/rollout shapes do not change. Installed GoalExtension pointer identity is statically traced, not independently attacked through an installed-goal runtime test.

Only this panel's task receives the outcome, checklist, notes and handoff. No accept/reject/withdraw/status/handoff/resource/note write is made on the implementation task.

Primary source links use the tested snapshot commit: [discovery and callable checks](https://github.com/ivanopcode/codex/blob/a27e1de3597943f045afd513179f352158983ea8/codex-rs/core/src/tools/waiting_capabilities.rs#L96), [normalizer](https://github.com/ivanopcode/codex/blob/a27e1de3597943f045afd513179f352158983ea8/codex-rs/core/src/context_manager/normalize.rs#L156), [public-entry null-server regression](https://github.com/ivanopcode/codex/blob/a27e1de3597943f045afd513179f352158983ea8/codex-rs/core/tests/suite/search_tool.rs#L1073).

```verdict-findings
{
  "findings": [],
  "notes": [
    "Independent non-recording DELTA panel; one-word verdict accept. No writes on TASK-260929-2is91w.",
    "Previous merged rev3 findings A3-F1 and D3-F1 are both addressed by exact normalization parity, server-null public-entry regression, and a killed null-ID narrowing mutant. Earlier orphan/provenance defenses persist.",
    "Execution identity independently checked: snapshot a27e1de3597943f045afd513179f352158983ea8 tree 523385e2bb27c606bd1cd7241b0825c77b7569e5. Four green lanes and 14/14 failing mutant core jobs. Overall workflow failure is expected for mutant kills.",
    "Raw snapshot core: 5121 passed, 11 skipped, 3 flaky recovered tests. Two inspected mutant core commands actually failed with exit 100. Other 12 kills rely on attached named summary and checked job conclusions. Zero new Rust runtime commands executed locally.",
    "Remote-catalog entry-point configuration leg remains unknown (4/5 configuration families attacked); no claim based on edited ModelInfo substitutes for remote replacement. Requested attack retained.",
    "Change-size guidance exceeded: 21 files +2398/-6, 1483 test-module lines. Retain staging/consolidation concern; this panel grants no exception and establishes no additional functional blocker.",
    "Adding waiting_capabilities to public TurnContextContributionInput is an external Rust source compatibility change. No wire/config/CLI/rollout change observed. update_plan_enabled replacement and capability-only in-turn contributor re-emission remain staged to guidance leaf; goal renders no fragments.",
    "Logbook: exact replay, 2/2 previous findings addressed, 7/7 rows swept, no new defect, remote-catalog blind spot and oversized diff retained. Outcome and notes only on panel task. Installed reviewer-role file and logbook executable were unavailable; supplied panel/negative-evidence contracts used and this outcome carries the logbook."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "attack": "Drop each host/opt-in/control/policy conjunct; narrow native backend identity; add foreign wait decoys.",
      "evidence": "waiting_capabilities.rs:46-83; router.rs:224-235. Exact-tree precheck 11 named kills for four exec_notify conjuncts, two native_mail_wait conjuncts, native V1/V2/provenance, sleep and stdin. Runtime provenance defaults false and only native wait handlers/wrapper enable it. No new flag-derivation defect.",
      "finding_ids": []
    },
    {
      "row": "final-router derivation",
      "result": "held",
      "attack": "Undiscovered/deferred/nested/excluded tools; orphan, mismatched, null-server, null-client and out-of-order discovery; stale names and native decoys.",
      "evidence": "waiting_capabilities.rs:102-153 matches normalize.rs:156-208; current registry exposure and native provenance still required at :209-217 and :256-259. Rev3 A3-F1/D3-F1 addressed. Raw snapshot PASS and exact mutant exit 100 prove server-null public-entry regression; pairing mutant exit 100 preserves orphan refusals. Discovered_native_wait_updates_waiting_capabilities also passes. No same-class sibling mismatch established.",
      "finding_ids": []
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "attack": "Real exec_command notify_on_exit receipt, idle wake and later sampling; pending/acknowledged provider data without support.",
      "evidence": "exec_notification.rs:756-844 drives launch and requires an armed receipt, then compares all snapshots; raw hosted core PASS. pending_and_acknowledged_work_does_not_flip_flags adds refusal control. Production reads support/policy markers only, not receipts. Windows skip in this POSIX test remains a platform bound.",
      "finding_ids": []
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "attack": "Look for recomputation, copied instances, disconnected goal contributor or speculative capture divergence.",
      "evidence": "session/mod.rs:3971-4001 owns one snapshot; :4315 and :4413 borrow it. Raw hosted same_snapshot_instance_reaches_both_context_paths PASS; test drives capture and both builders and compares pointers/values. goal/extension.rs:620-626 forwards reference; :766 registers prompt contributor. Installed-goal pointer identity is static evidence, not a separately executed attack.",
      "finding_ids": []
    },
    {
      "row": "configuration coverage",
      "result": "not-attacked",
      "attack": "Check remote replacement entry point versus resolved-model fixture; hard/reminder off, headless, code mode, excluded receipt controls.",
      "evidence": "waiting_capabilities_tests.rs:883-999, :1235-1350 and precheck 11 cover 4/5 required configuration families. snapshot_follows_catalog_clock_support passes but edits ModelInfo directly (:964-999). models-manager/src/manager.rs:685-700 shows real replacement; no attached replacement-to-snapshot entry-point attack.",
      "finding_ids": [],
      "reason": "Remote catalog replacement through ModelsManager with snapshot observation has no attached entry-point proof; resolved-model fixture is insufficient.",
      "requested_attack": {
        "test_file": "codex-rs/core/tests/suite/search_tool.rs or dedicated waiting_capabilities integration suite (requested, not added)",
        "command": "just test -p codex-core -E 'test(remote_catalog_replacement_changes_waiting_snapshot)'",
        "expected_failure": "NOT EXECUTED. Mock remote entries replacing the same bundled slug with clock support added/removed; sample a real session and record snapshot; mutant ignoring ModelsManager remote replacement must fail. Preserve hard/reminder/headless/code-mode/exclusion controls."
      }
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "attack": "Inspect heap names, serialization, history/rollout persistence, and prompt rewriting instead of trusting size_of alone.",
      "evidence": "extension-api/src/waiting_capabilities.rs:27-59 has four bools and Option<ToolName>, no collections/serde. Native wait name is fixed and V2 namespace config validation is capped at 64 ASCII characters (config/mod.rs:3148-3202). Raw hosted non-persistence test PASS; no goal text emitted. Bound applies to core-derived snapshots, not arbitrary externally constructed public strings. Transient history-parser scratch collections are not snapshot/model-context payloads.",
      "finding_ids": []
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "attack": "Trace all contributor constructors, plan-enabled behavior, dependency direction, Bazel sources and external compatibility.",
      "evidence": "One exported extension-api type and one borrowed contributor input field; in-tree constructors updated. Goal consumes extension API; no core-to-goal dependency. New focused core derivation is 309 lines; Rust source globs include files. No dependency/config/schema/build-time resource changes. update_plan_enabled staging to later guidance leaf remains as earlier review accepted. Required public field breaks out-of-tree Rust struct-literal construction; no app-server/CLI/config/rollout wire break established.",
      "finding_ids": []
    }
  ],
  "free_hunt": {
    "budget": "After prior findings and all seven rows, six adjacent checks: search-normalization shapes/order, stale discovery/current registry, runtime provenance/name bounds, stream/history retention, context/persistence/goal wiring, and API/Bazel/change size. Read-only; no build, mutation attack or delegation.",
    "checks": [
      {
        "area": "Search evidence normalization",
        "result": "Server Some/None, client None, paired/nonpaired Some and output-before-call all align with two-pass normalizer. Null-ID restriction mutant fails real stream integration. No new same-class defect."
      },
      {
        "area": "Stale discovered names and exclusions",
        "result": "Discovery names alone cannot activate absent or nested entries; deferred exposure is checked against current finalized registry. Native identity additionally requires native runtime provenance."
      },
      {
        "area": "Bounds and allocation",
        "result": "Production snapshot heap name bounded by existing V2 config and fixed native name. Extra Vec of raw history references is transient parser scratch, not injected model content. No new history/context payload."
      },
      {
        "area": "Stream recording and history retention",
        "result": "Protocol supports server/null; stream records output and for_prompt retains it. New public-entry regression asserts next input holds definition and contributor observes None-to-Some after second-turn policy change; raw hosted pass/kill checked."
      },
      {
        "area": "Contributor and persistence",
        "result": "Same captured value feeds both builders; registered goal renderer receives borrow and emits zero fragments. No history rewrite. Installed-goal pointer identity lacks separate runtime attack."
      },
      {
        "area": "API/build/size",
        "result": "Rust input compatibility and oversized diff noted; no new wire/dependency/schema/build-time asset surface. Source globs include new Rust files."
      }
    ],
    "coverage": {
      "surface_rows_swept": 7,
      "surface_rows_total": 7,
      "held": 6,
      "broken": 0,
      "not_attacked": 1,
      "previous_findings_addressed": 2,
      "previous_findings_total": 2,
      "attached_mutants_killed": 14,
      "attached_mutants_total": 14,
      "mutant_core_job_conclusions_checked": 14,
      "mutant_raw_logs_inspected": 2,
      "snapshot_core_passed": 5121,
      "snapshot_core_run": 5121,
      "snapshot_core_skipped": 11,
      "configuration_families_attacked": 4,
      "configuration_families_total": 5,
      "new_local_rust_runtime_attacks": 0
    },
    "blind_spots": [
      "Remote-catalog replacement-to-snapshot entry-point coverage absent.",
      "No independent installed-goal pointer runtime test.",
      "12 mutant raw logs and new macOS/Windows execution not inspected; skipped/quarantined tests are outside measured scope.",
      "In-turn guidance emission remains subsequent-leaf scope; discovery integration observes contributor on a changed-policy second turn."
    ],
    "stop_condition": "Prior findings assessed, all rows exactly once, six adjacent concerns swept; no new supported production defect. Ready for recording-review merge."
  }
}
```
