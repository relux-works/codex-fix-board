# TASK-261012-1xa3sr — R141 DELTA panel, waiting-capabilities snapshot rev5

accept

Replay check: base `e0eff057620104a416080da616256ee7f32bda1b` plus `TASK-260929-2is91w_change-request_rev5.patch`, applied through a temporary index, writes exactly `afb8c830d764ba489a9f2f922c0babdf1dbe036e`. No nested worktree, builds or tests used.

This is a non-recording review of `CR-TASK-260929-2is91w-5`. Nothing was written on the original task. The verdict is ready for review, not recording-reviewer acceptance.

## Commands and real exit codes

These are my executions. Commands ran as direct processes without tee or status-hiding pipes. Ordinary source reads are grouped; no test result is inferred from a successful log-download command.

| Command | Exit | Observed result |
|---|---:|---|
| `task-board m 'set_status(TASK-261012-1xa3sr, status=analysis)'` | 0 | Own-task lifecycle only |
| `mkdir -p .temp` | 0 | Temporary evidence directory |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1xa3sr-replay.idx" git read-tree e0eff057620104a416080da616256ee7f32bda1b` | 0 | Replay base loaded |
| `task-board resource get TASK-260929-2is91w TASK-260929-2is91w_change-request_rev5.patch --output .temp/TASK-260929-2is91w_change-request_rev5.patch` | 0 | Patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1xa3sr-replay.idx" git apply --cached .temp/TASK-260929-2is91w_change-request_rev5.patch` | 0 | Patch applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-1xa3sr-replay.idx" git write-tree` | 0 | Exact candidate tree printed |
| `git diff --check e0eff057620104a416080da616256ee7f32bda1b afb8c830d764ba489a9f2f922c0babdf1dbe036e` | 0 | No whitespace errors |
| `task-board q 'get(TASK-260929-2is91w) { description scope ac }'` | 0 | AC1–AC7 and scope inspected |
| `task-board resource get TASK-260929-2is91w surface-table.md --output .temp/panel-surface-table.md` | 0 | Seven-row source table |
| `task-board resource get TASK-260929-2is91w TASK-260929-2is91w_review-verdict-rev4.md --output .temp/panel-previous-verdict.md` | 0 | Prior merged verdict |
| `gh api repos/ivanopcode/codex/actions/runs/38191980780` with scoped jq projection | 0 | Workflow failure, attempt2; expected mutant failures |
| `gh api 'repos/ivanopcode/codex/actions/runs/38191980780/jobs?per_page=100'` with job projection | 0 | Four green candidate lanes, 15 failing mutant core jobs |
| `gh api repos/ivanopcode/codex/git/commits/<sha>` for workflow head, snapshot, mutant14, mutant15, and precheck11 snapshot | 0 each | Exact commit/tree identities checked |
| `gh api repos/ivanopcode/codex/actions/jobs/<id>/logs > .temp/<panel-log>` for 114648013941, 114648017069, 114628508769, 114648017723, 114648018238, 114510035901, 114512075377 | 0 each | Raw logs fetched; runtime results stated separately below |
| `gh api 'repos/ivanopcode/codex/actions/runs/38152963091/jobs?per_page=100'` with scoped projection | 0 | Prior snapshot job identified |
| `GIT_INDEX_FILE="$PWD/.temp/panel-remote-mutant.idx" git read-tree afb8c830d764ba489a9f2f922c0babdf1dbe036e` | 0 | Remote mutant replay base |
| `GIT_INDEX_FILE="$PWD/.temp/panel-remote-mutant.idx" git apply --cached .temp/panel-remote-mutant.patch` | 0 | Attached narrowing patch applied |
| `GIT_INDEX_FILE="$PWD/.temp/panel-remote-mutant.idx" git write-tree` | 0 | `c97365f8dd61f7537832d712424dd55997cb07a9`, matches hosted mutant14 |
| `git diff --stat`, `--numstat`, and rev4/precheck12-to-candidate diffs; candidate `git show` reads; resource `cat` reads; raw-log parsing Python scripts | 0 each | Static review and evidence counts; subordinate git-show return codes checked |
| `task-board spawn directives RUN-261012-5f1916` | 0 | No directives |
| `task-board q 'get(TASK-261012-1xa3sr) { checklist }'` | 0 | Seven handoff checklist items read |
| `git status --short` | 0 | Clean source worktree before artifact attachment |

Exploratory failures, not gates and not passing evidence: get projections with `resources` / `outcomes` exited **1** (unknown fields; corrected via scoped AC query and resource reads); `cat` of missing skill reviewer-role plus negative-evidence reference exited **1** (negative-evidence content read; reviewer-role missing); an `rg` search including nonexistent `/Users/administrator/.agents/project-management` exited **2**; focused role-path search exited **1** (no matches); `command -v logbook` exited **1** (unavailable). `task-board resource list` printed resource help with exit **0** and did not enumerate resources; hidden-resource `rg --files` was used instead. Skill body and CLI/schema help reads exited **0**.

Accepted hosted execution, not rerun by this panel: core snapshot command `INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-core -E "$expr" "${extra[@]}"` succeeds on rerun (job114648017069; 5122/5122, 11 skipped). Initial snapshot command fails with exit **100** (job114628508769, guardian timeout). The identical hosted command on remote mutant14 fails with exit **100** (job114648017723), an expected failure because the narrowed merge drops remote clock support; raw negative result is not a green gate. Nested-stdin mutant15 also fails with exit **100** (job114648018238). Other thirteen mutant failures and lint/small/app-server greens are accepted from the attached precheck14 plus job conclusions, not independent raw command-exit verification.

## Sources

- Original-task read-only resources: `surface-table.md`, `producer-brief.md`, `TASK-260929-2is91w_results.md`, `TASK-260929-2is91w_review-verdict-rev4.md`, `TASK-260929-2is91w_hosted-precheck-{11,12,14}.md`, `TASK-260929-2is91w_mutants.json`, and precheck14 outcome-scoped logbook. Local 64-KiB-capped validation log is not used to infer an unseen pass.
- [Exact-candidate hosted workflow](https://github.com/ivanopcode/codex/actions/runs/38191980780), [snapshot rerun](https://github.com/ivanopcode/codex/actions/runs/38191980780/job/114648017069), [initial core failure](https://github.com/ivanopcode/codex/actions/runs/38191980780/job/114628508769), [remote narrowing attack](https://github.com/ivanopcode/codex/actions/runs/38191980780/job/114648017723), [prior guardian flake](https://github.com/ivanopcode/codex/actions/runs/38152963091/job/114512075377).
- Candidate-tree code citations appear in each row below; all were read from Git objects, not the ambient checkout.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Previous merged rev4 verdict has zero findings; there is no unclosed prior finding to repeat. The outstanding remote-catalog not-attacked row is now directly held by exact-tree public-entry positive and narrowing-negative evidence. Earlier rev3 A3-F1/D3-F1 server-null fixes persist with normalization parity and exact-candidate passing/killed discovery cases.",
    "Execution evidence identity: workflow head 9f8fdf9aa3f7b28ded9e62fd628b2206c2c76a8b is orchestration code, not the source snapshot. Raw plan points snapshot lanes to f9228fb4c7377cd21da403621dd6b3a5960d1b7a; GitHub commit API confirms its tree is exactly afb8c830d764ba489a9f2f922c0babdf1dbe036e. Never equate the workflow head tree a2b4fea02f7ed8b67a41f0d0020a213712de8ea3 with the candidate.",
    "Raw hosted snapshot rerun: 5122 tests run, 5122 passed (8 slow, 1 recovered flaky), 11 skipped. Initial core attempt is genuinely red: exit 100, 5121 passed, 1 failed, 11 skipped; guardian event timeout on 3/3 attempts. Rerun on the same source snapshot passes guardian in 1.588s. Raw precheck11 snapshot a27e1de3597943f045afd513179f352158983ea8 / tree523385e2bb27c606bd1cd7241b0825c77b7569e5 has the identical guardian timeout at core/tests/common/lib.rs:393 followed by a 1.223s pass. Rev4-to-rev5 and precheck12-to-rev5 touch only search_tool.rs. Evidence supports a pre-existing intermittent failure, not a new rev5 regression; this does not establish the underlying cause or prove the bare base commit was executed. Literal unpatched-base attribution remains unverified.",
    "Precheck12 headline incorrectly claims 15/15 kills, while its remote mutant table row is empty. Results/outcome correct this to 14/15 with one survivor. That stale summary is not used as passing negative evidence. Precheck14 reports 15/15 named kills; job API independently shows 15 failing mutant core jobs. Two raw mutant logs inspected (remote replacement and nested stdin), other 13 killer attributions accepted from precheck14, not independently rerun. Overall workflow conclusion failure is expected from mutant failures and is not described as green.",
    "All seven rows are freshly swept; 7/7 held, 0 broken, 0 not-attacked. Five AC5 families covered, remote path/direction cases 4/4. Exact remote-mutant tree identity independently reconstructed. No local Rust build/test, no hosted rerun or CI mutation by this panel. Hosted lane results and attacks are accepted evidence, not my executions.",
    "Bounded free hunt after the seven rows: six adjacent checks: normalizer Some/None/server/client parity; stale/foreign name provenance; installed-goal routing and renderer scope; actual ToolName heap bound and persistence; external Rust vs wire compatibility/Bazel source inclusion; revision delta, evidence identity and flaky attribution. No new defect established. These coverage notes do not populate free_hunt, which holds real findings only.",
    "Cumulative diff is 21 files +2619/-6 (2625 changed lines), above 800-line and complex-logic 500-line guidance; 1483 lines are a new unit-test module. Rev4-to-rev5 adds only remote catalog integration coverage in search_tool.rs. Prior size concern retained, no exception granted. Smallest coherent staging option: extension-api snapshot/input plus core capture/derivation and behavioral tests first; goal empty renderer registration/forwarding next, preserving existing plan behavior; any split requires new exact-tree validation.",
    "No product/source edits, commits, branch operations or original-task writes. Source references in this outcome always refer to candidate tree afb8c830d764ba489a9f2f922c0babdf1dbe036e; the original task and its resources were read-only inputs. Only the plain-text verdict is attached to this panel task.",
    "Installed project-management skill was read. Its referenced reviewer-role file is absent; supplied full-surface panel and negative-evidence contracts govern this review. No logbook executable or callable logbook tool exists in this environment; the outcome-scoped logbook below persists the important decisions/anomalies, with an own-task board note."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "attack": "Drop each host/opt-in/stdin/receipt/policy conjunct; substitute V1-only/V2-only native identities; admit foreign same-name waits or nested tools.",
      "evidence": "Candidate core/src/tools/waiting_capabilities.rs:46-83,208-309 derives AC1 predicates; native provenance is reported only by V1/V2 handlers and forwarded by the V2 wrapper. Precheck14 names killers for 12 flag mutants; all corresponding core jobs fail. Snapshot core passes the direct/nested, host/control/policy and configured-native-name cases. Mutant15 raw core fails nested stdin and the public remote-catalog test (exit 100).",
      "finding_ids": []
    },
    {
      "row": "final-router derivation",
      "result": "held",
      "attack": "Feed orphan/mismatched client discovery, null-ID server/client discovery, stale names, deferred native waits and foreign decoys; trace exclusions and collisions before capture.",
      "evidence": "Candidate waiting_capabilities.rs:104-146 matches normalize.rs:156-208: only Some(id)+non-server+unpaired is dropped. is_callable at 208-223 requires direct visibility or discovery plus current deferred registry exposure; native_wait_tool requires native runtime provenance. Session capture occurs after prepared_tools resolves (session/mod.rs:3971-3998). Raw snapshot core passes server_null_id_discovery_updates_waiting_capabilities and native discovery cases. Precheck14 discovery_ignores_call_pairing and discovery_requires_server_call_id are killed by named unit/public-entry tests. Excluded receipt/exec production-router tests pass. Collision/stale-name protection is source-traced through the finalized registry; no new independently executed collision mutant is claimed.",
      "finding_ids": []
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "attack": "Drive exec_command notify_on_exit, require an armed receipt and idle completion wake, then compare snapshots across subsequent samples; add pending/acknowledged work with no policy.",
      "evidence": "core/tests/suite/exec_notification.rs:756-835 drives the production tool entry and observes unchanged whole snapshots. Raw snapshot core PASS 2.966s for acknowledged_subscription_does_not_flip_waiting_capabilities; pending_and_acknowledged_work_does_not_flip_flags also passes. Derivation reads only host/policy markers, not receipts or mailbox state; native_mail_wait_ignores_policy is killed. POSIX receipt test skips Windows and sandbox configurations, so this execution proof is hosted Linux.",
      "finding_ids": []
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "attack": "Search for recomputation, copies, path-specific derivation or missing goal contributor registration; compare pointer and values through production capture and both context builders.",
      "evidence": "session/mod.rs:3971-3998 derives once into StepContext; contributor calls at 4315 and 4413 borrow that field. waiting_capabilities_tests.rs:1413-1444 drives capture_step_context, initial-context builder and contribution builder, asserts two captures with identical pointer and values; raw snapshot PASS 0.089s. Installed GoalExtension registration at extension.rs:767 and forwarding at 625 pass the same borrowed input to the renderer. Goal forwarding is static proof; no installed-goal pointer-recorder execution is claimed.",
      "finding_ids": []
    },
    {
      "row": "configuration coverage",
      "result": "held",
      "attack": "Attack all five AC5 families afresh. Remote /models same-slug additions/removals through both List remote-only and Hide merge paths; ignore only the merge replacement assignment. Also hard/reminder switches, headless exec, code-mode-only and excluded receipt.",
      "evidence": "search_tool.rs:1196-1407 uses a real mock /models endpoint, dummy ChatGPT authentication, explicit model selection, build_with_auto_env and submit_turn. Four cases assert one /models GET and one /responses POST each, outbound clock.sleep presence and full WaitingCapabilities equality; Hide cases also require bundled catalog size, bundled-only slug survival, replaced visibility and tools. models-manager/src/manager.rs:671-707 makes List remote-only and Hide merge; get_default_model preserves explicit slug and metadata lookup ignores picker visibility. Raw snapshot core PASS 2.698s. Applying the one-line remote merge mutant to this candidate gives c97365f8dd61f7537832d712424dd55997cb07a9, exactly the hosted mutant14 tree. Raw job114648017723 fails all three attempts at search_tool.rs:1290, outbound clock.sleep false vs expected true for gpt-5.5; command exits 100, 424/425 pass and one named failure. Other four configuration families pass their named raw snapshot tests. Measured coverage: 5/5 families; remote path/direction cases 4/4 on the positive candidate. The negative run stops on first Hide/add failure, so separate Hide/remove mutant execution is not claimed.",
      "finding_ids": []
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "attack": "Account for native ToolName heap payload instead of size_of headers; trace persistence, history and renderer output.",
      "evidence": "extension-api/src/waiting_capabilities.rs:24-59 holds four booleans and Option<ToolName>, with no collections or serialization derive. Production native name is fixed wait_agent with fixed V1 namespace or validated V2 namespace of at most 64 ASCII characters (core/src/config/mod.rs:3148-3202, called at 3873); foreign runtime names cannot satisfy native provenance. StepContext::to_turn_context_item (step_context.rs:51-55) omits the snapshot. waiting_snapshot_does_not_persist_to_history_or_rollout passes in raw snapshot core (0.089s), comparing both context builders and persisted turn item before/after snapshot-only changes. Goal renderer returns no fragments. Public manual construction is not intrinsically string-bounded; the established bound is core-derived snapshots. Discovery scratch scans existing history and is not model-injected/persisted.",
      "finding_ids": []
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "attack": "Trace all input constructors, exported type, core/goal dependency direction, existing plan signal, wire surfaces and Bazel source inclusion.",
      "evidence": "One exported WaitingCapabilities type and one borrowed TurnContextContributionInput field; in-tree constructors updated. Derivation isolated in a private 309-line core module, no core->goal dependency. Goal registration/forwarding adds no prompt bytes and preserves update_plan_enabled pending the separate guidance leaf, as prior accepted reviews explicitly scoped. Hosted lint/small/app-server/snapshot-core jobs are successful. No changes to app-server API, CLI, ConfigToml, raw events, Cargo dependencies, schemas or rollout shape; core BUILD.bazel src/**/*.rs includes new source files. Required Rust input field is source-breaking for external struct-literal users, retained as prior disclosed nonblocking note; no external compatibility execution claimed.",
      "finding_ids": []
    }
  ],
  "free_hunt": []
}
```

## Outcome-scoped logbook

2026-10-12 — Independent DELTA review: exact replay and remote-mutant tree verified; 7/7 surfaces held, 5/5 configuration families attacked. Rev4 had no findings, but its remote catalog gap now has a real /models session attack and a killed merge-path mutant. Preserve precheck12 summary anomaly and initial guardian exit100 alongside successful rerun. Classify guardian behavior as pre-existing intermittency supported by rev4 logs; bare-base causality remains unknown. Keep prior change-size and external Rust-source compatibility notes. No original-task write, no builds, no delegation. Persist verdict before own-task researcher handoff.

Artifact verification: the standalone Python JSON/shape check exited **0**; exactly one valid verdict-findings object, seven unique source-table rows all held, one-word accept, and replay/exit-code evidence were asserted. Artifact creation Python exited **0**.
