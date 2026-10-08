# R141 panel A — goal-background-wait vertical test, revision 1

accept

Read-only panel review of CR-TASK-260929-3f6hfg-1. This is a recommendation for the recording reviewer, not acceptance of the Change Request. No mutation targeted TASK-260929-3f6hfg. No build or test ran locally; hosted execution below is reused evidence, independently checked from raw provider logs.

Replay: base `2f522b9dc9d639fe5195d93d61431a0caff662d5` plus the attached revision-1 patch produced exactly `c83869e576d1e024cfdbb5f63cfe8b83c6e969cb` through a temporary index. `read-tree`, `apply --cached`, and `write-tree` each exited 0. The regular index and tracked worktree were untouched. `git status --short` was empty before and after inspection; `git rev-list --count HEAD..main` returned 0 (this is local-main information, not a fresh-upstream attestation). Review evidence is anchored to the named CR tree, not to workspace freshness.

## Research contract

Decision: recommend accept or changes_requested for this exact candidate and its three surface rows. Frozen precondition: the supplied CR base, patch, candidate tree and surface-table rows; no grammar research applies. Worker-time ceiling: 30 minutes for the sweep plus a five-minute bounded static free hunt. Artifact ceiling: one text verdict, no archive. Serial prerequisites: zero. Exit: replay matches, each row has one result, findings schema validates, evidence attached, researcher handoff. Consumer: the orchestrator's merged-panel recording review; no implementation leaf is requested.

## Independently checked hosted evidence

The run metadata `headSha` is the workflow-dispatch base, NOT the source tree under test. The raw checkout and WANT_SHA lines prove the snapshot below was used. `git show -s --format='%H %T' 542a2e5c` exited 0 and maps full snapshot `542a2e5c7c678fee054465420cd3dca9896b5409` to the exact candidate tree. Workflow `.github/workflows/relux-ci.yml` uses `inputs.sha` for checkout and verifies it before execution; hosted runner is Ubuntu 24.04, Rust 1.95.0, native Linux exec.

[Base run 37633617318](https://github.com/relux-works/codex/actions/runs/37633617318): all four lanes success. Raw app-server job 112833987130 lines 4962/4964/4966/4967 explicitly PASS all four new tests; line 6027 reports 1833/1833 passed, two unrelated tests skipped. This is not an inference from a green summary alone.

Every attached mutant was replayed through its own temporary index starting at the candidate, with read-tree/apply/write-tree exiting 0 independently. Resulting trees equal the corresponding hosted checked-out commit's tree, established with git show (exit 0). Thus these runs attack the candidate plus exactly the supplied production mutation, not a different revision.

| Mutant | Hosted commit / replay tree | Raw app-server job / observed kill | Hosted gate exit |
| --- | --- | --- | ---: |
| silence-ignores-armed | 6beee2ca4fe66eac6270982f4616e90e3224b780 / 588f5262b8b7977395702b0c772d161179608be7 | 112834409439: notified_exec_exit_wakes_gated_goal_with_receipt_fragment, line 357, 3/3 attempts | 100 |
| drop-wake | 75e9fc11d8d4ad7b14180a26438ee713a1fa15b1 / d5641931b233eb2fa4001c765931765d23847a14 | 112834297848: notified_exec_exit_wakes_gated_goal_with_receipt_fragment and user_burst…, 3/3 attempts; missing wake ultimately surfaces as wiremock drop verification (expected four requests, received two for notified_exec) after the bounded wait | 100 |
| wake-without-fragment | 28fd63d548cb2f67be861e8b67778a3af33b9780 / 2d1194c2bd55e1af3bd6b5d719bdd54a91ec46b4 | 112834507515: notified_exec… line 357 and user_burst… line 458, 3/3 attempts each | 100 |
| allow-notify-on-incapable-host | 5db647b45a27c971e7032d4b9e50102c2c63a134 / 106d2525caed2051fede8630958c406ddb91acfe | 112834087576: headless_host_refuses_notify_on_exit_and_promises_no_wake, line 612, 3/3 attempts | 100 |
| always-subscribe | 15feabdd885141da20554ffd323fdd5eee0a4a71 / 80356922a071ebf8d2ed3ad7b173724434c6a3f8 | 112834193749: unopted_server_process_does_not_gate_goal_continuation, line 540, 3/3 attempts | 100 |

Expected-red mutant runs genuinely failed; exit 100 is not reported as a pass. Each retains behavior for another class while weakening the named production gate. Coverage: 3/3 surface rows attacked, 4/4 added tests executed on the base, 5/5 supplied mutants killed, 0/5 survivors. AC1–AC7 have named driving tests in the attached coverage map; the concurrency and silence bounds below limit what those observations establish.

## Commands and exit codes in this panel

All validation commands ran as standalone processes without tee. Readiness probes were saved under `.temp/TASK-261007-3f3rcp/` before using tools for substantive work. Repeated commands are shown as explicit parameter sets, not implied additional execution.

| Command | Exit / scope |
| --- | --- |
| task-board m 'set_status(TASK-261007-3f3rcp, status=analysis)' | 0; own panel task only |
| command -v task-board/git/rg; git --version; task-board --version | 0 readiness shell; output in readiness-01.log |
| git rev-parse --show-toplevel; git status --short; git rev-list --count HEAD..main | 0 |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3f3rcp-replay.idx" git read-tree 2f522b9dc9d639fe5195d93d61431a0caff662d5 | 0 |
| task-board resource get TASK-260929-3f6hfg TASK-260929-3f6hfg_change-request_rev1.patch --output .temp/TASK-260929-3f6hfg_change-request_rev1.patch | 0; read-only |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3f3rcp-replay.idx" git apply --cached .temp/TASK-260929-3f6hfg_change-request_rev1.patch | 0 |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3f3rcp-replay.idx" git write-tree | 0; exact candidate printed |
| task-board q 'get(TASK-260929-3f6hfg) { description scope ac notes }'; get(TASK-261007-3f3rcp) { ac checklist } | 0 each |
| gh --version; python3 --version | 0 readiness, persisted logs |
| gh run view RUN --repo relux-works/codex --json headSha,conclusion,jobs,url | 0 each: RUN=37633617318,37633645894,37633676266,37633707303,37633736582,37633768227 |
| gh run view RUN --job JOB --repo relux-works/codex --log | 0 each: 37633617318/112833987130, 37633645894/112834087576, 37633676266/112834193749, 37633707303/112834297848, 37633736582/112834409439, 37633768227/112834507515 |
| git show -s --format='%H %T' SNAPSHOT; git show -s --format='%H %T' MUTANT_COMMITS | 0; all six commits listed above |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3f3rcp/NAME.idx" git read-tree c83869e576d1e024cfdbb5f63cfe8b83c6e969cb | 0 each; NAME=all five named mutants |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3f3rcp/NAME.idx" git apply --cached .temp/TASK-261007-3f3rcp/NAME.patch | 0 each, same five NAME values |
| GIT_INDEX_FILE="$PWD/.temp/TASK-261007-3f3rcp/NAME.idx" git write-tree | 0 each, exact hosted mutant trees printed |
| git diff --stat/--name-only BASE CANDIDATE; git show CANDIDATE:PATH; bounded sed/rg and Python log projections | 0, static reads only |
| task-board spawn directives "$TASK_BOARD_RUN_ID" | 0; no directives |
| git status --short (after review) | 0; empty |
| Python outcome verification: parse exactly one fenced JSON object; compare row names/order to surface-table.md; require 3/3 held, empty findings/free_hunt and one accept verdict; check base PASS lines and clean git status | 0; PASS; 4/4 base test PASS lines independently found |

Read/discovery failures, not gates: the initial get projection with `resources` exited 1 (unknown field), repaired with the compact supported projection and resource-path inventory. Reading the stale `/Users/iv/.claude/skills/project-management/.roles/reviewer/role.md` path exited 1, repaired by locating and reading `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md` (0). `schema(kind=element)` exited 1 (unknown scope); `schema(operation=get)` exited 0. `task-board resource list` printed resource help with exit 0; it provided no inventory and was not treated as evidence. Skill-search rg reported missing agents/skills and .claude/skills directories; .codex/skills was inspected. No failed read was interpreted as absence or success.

Accepted evidence, not rerun here: local fmt/clippy/fix results described in TASK-260929-3f6hfg_results.md. They are supplementary only; hosted lint/small green and raw app-server logs protect against reliance on truncated local validation output. No cargo, just, local suite, new hosted dispatch, PR operation, source-task status, accept/reject, or source-task handoff command was executed.

## Bounded free hunt and logbook

After the surface sweep, static inspection checked test registration, auto-env defaults, notification buffering/timeout wrappers, receipt extraction and cross-link assertions, schema hiding plus direct execution refusal, and the production continue_if_idle branch. No reproduced blocking mechanism was found. The receipt string is derived from the actual exec acknowledgement and checked against the wake payload; test registration is present in v2/mod.rs. The first goal must remain Active before release and become Complete after wake. Tests release only after the relevant positive/negative observation.

Logbook observations: hosted metadata's base headSha would falsely suggest stale evidence without reading checkout logs; checkout identity plus replay resolves it. Two summary mutant rows omitted their app-server killers, but raw logs confirm them. The drop-wake timeout is masked in printed failure output by wiremock's destructor assertion; the observed kill remains valid, while the producer's specific failure-site description is imprecise. These are recorded here as a task-scoped outcome rather than editing a control-root logbook.

Bounds: held means the named attacks held, not absence of all defects. The user test submits two turns consecutively while the receipt remains armed; it does not prove overlapping queued submissions or the experimental thread/queue API. The barrier's child polls with sleep; test-side ordering does not depend on an arbitrary sleep. Silence is observed at finite RPC/count checkpoints and by displacing the required completion-fragment request under the armed-state mutant; this is not an indefinite quiescence proof. Remote/Wine barrier cases are explicitly skipped because release files are not shared and shell assumptions differ; no remote-exec execution is attested.

## Sources

Read-only task resources: surface-table.md, producer-brief.md, TASK-260929-3f6hfg_results.md, TASK-260929-3f6hfg_coverage-map.md, TASK-260929-3f6hfg_mutants.json, TASK-260929-3f6hfg_hosted-precheck-1.md under `/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-3f6hfg/`. ACs read via the compact task query.

Exact-tree code citations: `codex-rs/app-server/tests/suite/v2/goal_background_wait.rs:78,174,219,261,322,357,426,458,540,612`; `app-server/tests/suite/v2/mod.rs:61`; `app-server/tests/common/test_app_server.rs:1683,1735,2017`; `ext/goal/src/runtime.rs:616`; `ext/extension-api/src/async_notification.rs:51`; `.github/workflows/relux-ci.yml:59`.

Raw logs remain task-scoped scratch at `.temp/TASK-261007-3f3rcp/job-JOB.log`; immutable hosted references:
- [incapable-host mutant](https://github.com/relux-works/codex/actions/runs/37633645894/job/112834087576)
- [unopted mutant](https://github.com/relux-works/codex/actions/runs/37633676266/job/112834193749)
- [drop-wake mutant](https://github.com/relux-works/codex/actions/runs/37633707303/job/112834297848)
- [armed-state mutant](https://github.com/relux-works/codex/actions/runs/37633736582/job/112834409439)
- [fragment mutant](https://github.com/relux-works/codex/actions/runs/37633768227/job/112834507515)

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "user-input-concurrency-bound",
      "row": "negatives",
      "text": "Consecutive turn/start admissions while waiting are exercised, not overlapping submissions or thread/queue. No failing reproduction established; do not infer concurrent-queue coverage."
    },
    {
      "id": "silence-observation-bound",
      "row": "controlled-exit vertical",
      "text": "Armed narrowing mutant is killed by the required wake-fragment assertion at line 357, not the pre-release count. This covers extra continuation through request ordering, with finite observation checkpoints."
    },
    {
      "id": "drop-wake-diagnostic-bound",
      "row": "harness quality",
      "text": "The raw failure reports the wiremock destructor count assertion after the bounded missing-wake wait, not a directly printed timeout. This is a valid kill with less precise diagnostics."
    }
  ],
  "surface_results": [
    {
      "row": "controlled-exit vertical",
      "result": "held",
      "evidence": "Exact candidate hosted base passes notified_exec_exit_wakes_gated_goal_with_receipt_fragment. Candidate+narrowing mutants silence-ignores-armed, drop-wake, wake-without-fragment all kill that public JSON-RPC/tool-dispatch test (raw jobs and exact mutant replay trees above). Assertions check Active/2 requests before release, receipt/source/exit code after release, 4 requests and Complete; held only for these named attacks."
    },
    {
      "row": "negatives",
      "result": "held",
      "evidence": "Hosted base passes headless_host_refuses_notify_on_exit_and_promises_no_wake, unopted_server_process_does_not_gate_goal_continuation, user_burst_during_background_wait_admitted_without_loss_or_duplication. Headless direct-call refusal narrowed and killed at line 612; default subscription mutant killed at line 540. User turns are accepted before release and reconstructed exactly once through thread/read. Concurrent submission is outside measured coverage."
    },
    {
      "row": "harness quality",
      "result": "held",
      "evidence": "All four tests execute in native hosted Linux app-server lane; registration and auto-env defaults checked. Five production-only mutants replay to hosted trees and each is killed by a named vertical public-entry test, not solely collateral suites. Release-file barriers and bounded notification/RPC waits avoid timing-based test sleeps. Remote/Wine skips carry reasons; headless test has no skip. Drop-wake diagnostic limitation recorded as a note."
    }
  ],
  "free_hunt": []
}
```
