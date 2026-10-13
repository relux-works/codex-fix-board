# TASK-261012-3laumx — R141 DELTA panel, CR-TASK-260929-309h9n-3 revision 3

accept

Replay tree check: **MATCH**. Temporary-index replay of base
`67789e1ee29e766e446c7f33feb61561d51f94db` plus resource
`TASK-260929-309h9n_change-request_rev3.patch` produced exactly
`3c5cbffcc73270bec86364ab42550441c87f933c`.

Ready for review. Nine rows swept, no blocking defect established. One non-blocking
note preserves the recurring P4a retry; fixture isolation is verified, a flake cure is not.

## Successor verification and handoff recovery (2026-10-12)

The detailed review and original command ledger below were produced by predecessor
RUN-261012-2bc7f1. Successor RUN-261012-6f9aaf read that attached evidence,
independently replayed rev3, audited the prior five findings and production-policy
rework, and independently replayed all seven mutant trees. No hosted tests were
rerun; full saved hosted logs and a fresh GitHub job-conclusion read were accepted
as execution evidence on exactly the same trees. The verdict and nine row results
are retained unchanged.

The predecessor's handoff triggered a repository validation failure because its
untracked research file was included as a one-path repository delta. The recorded
validation log reports mini-hosted-gate exit **1** (no hosted result for research
artifact tree f3f5009df85fad9cfd0315fe39c60108970f68b7); this is a real failing gate,
not a passing check. That tree is not the reviewed scheduler tree. The report is
preserved under ignored `.temp/.research/` and attached as the existing panel
outcome. The workspace now carries no repository delta; no gate/config bypass,
new build request, source edit, commit or branch operation is needed.

Successor commands personally run (each direct or an individually status-checked
subprocess; numeric exits observed):

| Command | Exit | Result |
|---|---:|---|
| task-board m 'set_status(TASK-261012-3laumx, status=analysis)' | 0 | Own lifecycle resumed |
| GIT_INDEX_FILE=$IDX git read-tree B | 0 | Same private replay index |
| task-board resource get TASK-260929-309h9n TASK-260929-309h9n_change-request_rev3.patch --output .temp/TASK-260929-309h9n_change-request_rev3.patch | 0 | Fresh patch retrieval |
| GIT_INDEX_FILE=$IDX git apply --cached .temp/TASK-260929-309h9n_change-request_rev3.patch | 0 | Mandatory replay |
| GIT_INDEX_FILE=$IDX git write-tree | 0 | Exact C match |
| git diff --check B C | 0 | Whitespace check |
| git diff af312067fcd2392b78deb95d3f71925e739622b7 eb655488b22ff6bb17a3a3a6250fd60e3a202209 -- codex-rs/ext/goal codex-rs/app-server/src/extensions.rs codex-rs/features/src/lib.rs codex-rs/core/tests/suite/goal_background_wait.rs | 0 | Old-base rework inspected |
| git grep -n -E 'CODEX_GOAL_PACING_DISABLED|pacing_disabled_by_env|PACING_DISABLED_ENV_VAR' C -- . | 1 | Expected no match; not green |
| git grep for GoalExtensionConfig/goal_continuation_pacing/continuation_pacing C | 0 | Production mapping, schema and start-only read |
| gh run view 38232681612 --repo ivanopcode/codex --json headSha,conclusion,jobs,url | 0 | Read succeeded; displayed result truncated, followed by compact projection below |
| gh run view 38232681612 --repo ivanopcode/codex --json conclusion,jobs --jq '{conclusion: .conclusion, jobs: [.jobs[] | {id: .databaseId, name: .name, conclusion: .conclusion}]}' | 0 | 4/4 exact snapshot lanes success, mutant failures, overall failure |
| git rev-parse de3883cbfe2018457b9d34ee8f4b5469ebe7ff2e^{tree} | 0 | Exact C |
| rg -n 'scheduled_checkins_fire_through_production_runtime_under_paused_time|timeout waiting for event|5131 passed' .temp/TASK-261012-3laumx-job-114758681056.log | 0 | First failure/retry preserved |
| rg start-only/config-update bounds in saved results | 0 | Explicit lifecycle disclosure verified |
| python3 .temp/TASK-261012-3laumx-successor-audit.py | 0 | 5/5 prior IDs, 7/7 mutant identities/red logs, 2/2 exact schema additions |
| Per mutant: git read-tree C; git apply --cached --check -; git apply --cached -; git write-tree; git rev-parse SHA^{tree} (35 separate processes using a private successor index) | 0 each | Exact executed mutant identities; existing hosted test exits 100 remain expected red |
| git show B:codex-rs/core/config.schema.json; git show C:codex-rs/core/config.schema.json | 0 each | Only two added boolean fields |
| git check-ignore .temp/TASK-261012-3laumx_panel-verdict.md | 0 | Scratch artifact excluded from repository delta |
| python3 .temp/TASK-261012-3laumx-validate-verdict.py | 0 | One block, nine unique rows, required finding keys; source/index/status clean |

Successor exploratory read errors: two initial `get` projections exited **1** for
unknown `resources`; corrected `outcomeResources` projection exited **0**. The
installed reviewer role reference and delivery-validation document were absent
(`cat` exit **1**); explicit task contract governs the review. Role-file discovery
`rg` exited **1** (no match). Unsupported resource-list invocations exited **0**
but printed help, not inventory; they are not used as evidence. Other resource
reads, skill/CLI reads, JSON inspection and artifact preparation exited **0**.
`task-board spawn directives RUN-261012-6f9aaf` exited **0**, with no directives.

Recovery logbook: original research outcome and scheduler verdict are preserved;
only report placement caused the failed panel CR validation. Report relocation
removes that unrelated repository delta. Recurring P4a first-attempt failure
remains informational with attribution unknown. No mutations were sent to the
reviewed task. This panel's outcome update precedes researcher handoff.

## Predecessor commands and observed exit codes

Commands ran directly or as individually checked subprocesses; no tee or status-hiding pipeline.
`C` below is the candidate tree above; `B` is the base above. `$IDX` is
`$PWD/.temp/TASK-261012-3laumx-replay.idx`, never the repository index.

| Command actually run | Exit | Evidence |
|---|---:|---|
| task-board m 'set_status(TASK-261012-3laumx, status=analysis)' | 0 | Own task only |
| mkdir -p .temp; GIT_INDEX_FILE=$IDX git read-tree B (newline-separated setup) | 0 | Base loaded into private index |
| task-board resource get TASK-260929-309h9n TASK-260929-309h9n_change-request_rev3.patch --output .temp/TASK-260929-309h9n_change-request_rev3.patch | 0 | Patch materialized read-only from reviewed task |
| GIT_INDEX_FILE=$IDX git apply --cached .temp/TASK-260929-309h9n_change-request_rev3.patch | 0 | Replay applied |
| GIT_INDEX_FILE=$IDX git write-tree | 0 | C, exact expected tree |
| git diff --check B C | 0 | No patch whitespace errors |
| git diff af312067fcd2392b78deb95d3f71925e739622b7 eb655488b22ff6bb17a3a3a6250fd60e3a202209 -- codex-rs | 0 | Rev2 rework examined independently of refresh |
| git diff --stat B C; git show C:path; candidate cat/sed/rg inspections | 0 | Git reads plus extracted text; no candidate mutation |
| git grep -n -E 'CODEX_GOAL_PACING_DISABLED\|pacing_disabled_by_env\|PACING_DISABLED_ENV_VAR' C -- . | 1 | Expected no-match, **not a green gate**: removed switch absent |
| git grep -n -E 'std::env\|env::var\|with_env_overrides' C -- codex-rs/ext/goal/src | 1 | Expected no-match: no ambient reader in goal production source |
| task-board q 'get(TASK-260929-309h9n) { description scope ac }' | 0 | AC and scope read |
| task-board resource get TASK-260929-309h9n NAME --output .temp/TASK-261012-3laumx-INPUT | 0 each | surface-table.md, review-verdict-rev2.md, hosted-precheck-9.md, results.md, producer-brief.md and mutants.json; exact task-prefixed names for outcomes |
| Python JSON extraction / static schema-and-mutant replay inspection | 0 | Two exact boolean schema additions, registry default/stage; 7/7 mutation applicability and write-tree checks |
| Per mutant: GIT_INDEX_FILE=private-mutant.idx git read-tree C; git apply --cached --check -; git apply --cached -; git write-tree | 0 each, 28 processes | Independent reset/check/apply/tree, no builds; trees below |
| gh run view 38232681612 --repo ivanopcode/codex --json headSha,conclusion,jobs,url | 0 | Snapshot job statuses and distinct dispatcher head |
| gh run view 38232681612 --repo ivanopcode/codex --job JOB --log | 0 each after retries | Four snapshot/lint jobs and seven failed mutant jobs below |
| git rev-parse de3883cbfe2018457b9d34ee8f4b5469ebe7ff2e^{tree} | 0 | C, matching snapshot checkout in all four lane logs |
| git rev-parse MUTANT_SHA^{tree} | 0 each, 7 processes | Every executed mutant checkout matches locally replayed mutation tree |
| Python hosted-log filtering / mutation identity verification | 0 after recovery | Checks, log excerpts and no pass-by-truncated-proxy claim |
| git grep for config constructors/installers/schema generator; Python source extraction/counting | 0 | Host inventory, generator branch, module sizes and 22 unit-pass records |
| task-board spawn directives RUN-261012-2bc7f1 | 0 | No directives recorded |
| task-board q schema/get/checklist/resource projections and CLI help | 0 after corrected projection | Own lifecycle/resource contract inspection |

No local cargo/just/tests/generator run. No code/config edits; formatting and build
rules are satisfied through the read-only scope and accepted exact-tree hosted evidence.
Report-shape validation `python3 .temp/TASK-261012-3laumx-validate-verdict.py`
exited **0**: one JSON block, nine unique rows, valid findings and one accept verdict.
Its `git diff --quiet` and `git diff --cached --quiet` subprocesses each exited **0**,
confirming no tracked source or real-index edits. Resource attachment follows before role handoff.

### Failed reads/setup retained honestly

- Supplied setup containing `rm -f` was rejected by the command runner before execution:
  no process exit code exists. Retried with read-tree resetting the private index; exit 0.
- Initial `get(...){ description scope ac resources notes }` query exited 1 (unknown field
  resources); valid projections/resource get commands exited 0.
- Initial skill reference `cat .../.roles/reviewer/role.md .../negative-evidence.md`
  exited 1: reviewer reference missing, negative-evidence body was read. Skill-discovery
  rg scans exited 1 (one nonexistent search root, then no matches); direct reviewer-path
  ls exited 1. No absence of obligations inferred.
- Initial concurrent hosted-log read script exited 1: small/app-server gh retrievals
  each exited 1; lint/core retrievals each exited 0. Sequential retries both exited 0
  and retrieved full logs. No failed retrieval counted as execution evidence.
- `schema(mutation=add_logbook_entry)` exited 1, unknown mutation; schema recovery
  exited 0 and showed no free-text logbook mutation. Logbook is preserved below and
  in own-task notes, with no manually written board activity.
- Additional exploratory git greps for obsolete symbol locations / literal test names
  in BUILD files / model-visible persistence text returned no matches (exit 1). Bazel
  macro source discovery and current admission module were then read directly.
- `task-board resource list ...` exits 0 but prints help (no such listing subcommand);
  this was not treated as a resource inventory. Resource projections later exited 0.

## Hosted execution provenance and measured attacks

[Hosted run 38232681612](https://github.com/ivanopcode/codex/actions/runs/38232681612)
checks snapshot commit `de3883cbfe2018457b9d34ee8f4b5469ebe7ff2e`, whose tree is C.
Dispatcher head `9f8fdf9aa3f7b28ded9e62fd628b2206c2c76a8b` is not that tested snapshot.
Overall workflow conclusion **failure** is expected from killed-mutant lanes;
never describe the whole workflow as green. Snapshot lint/small/core/app-server:
**4/4 success**. Successful job/step conclusions establish aggregate success;
no separately printed numeric successful command exit is invented.

| Lane / log retrieval | Job | Observed result |
|---|---:|---|
| lint | 114755743238 | success |
| snapshot small | 114758681058 | 1489 passed, 1 skipped; 22 pacing units pass |
| snapshot core | 114758681056 | 5131 passed, 2 flaky, 11 skipped; pacing tests pass, P4a retry retained |
| snapshot app-server | 114758681075 | 1834 passed, 2 skipped; two-poll test PASS 69.430s |

All seven supplied mutations independently apply to C and match the respective
hosted checkout tree. Each failing lane below prints **exit 100**, an expected
failure because its named test detects the injected scheduling/policy defect.
These are red executed attacks, not green test suites. Coverage **7/7**, survivors **0/7**.

| Mutation | Hosted job / exit | Replayed tree | Observed killer (selected) |
|---|---|---|---|
| pacing_blocker_skipped_for_paced_turns | 114758681018 / 100 | `ba4692f59f12d98b76d4075c933453570772a5e7` | goal_pacing_empty_blocker_runs_before_rescheduling |
| pacing_feature_flag_ignored | 114758681110 / 100 | `0c66358f598d6ac269fdefb155a514e95d7221cc` | background_wait_inactive_on_unavailable_host_auto_continues |
| pacing_first_continuation_paced_after_human_turn | 114758681053 / 100 | `d9f77e79c8b83d195897cde7654e5269de2ad2e5` | pacing_first_continuation_after_human_turn_proceeds_immediately |
| pacing_missing_cap | 114758681059 / 100 | `e3af1102343b8f078c61aff4ce7b5a4309f4954d` | pacing_delay_n1_n2_n3_and_cap |
| pacing_stale_ticket_admission_skip_revision | 114758681055 / 100 | `aa17d54057a6150571a1c808d9907515f28353f9` | pacing_stale_ticket_rejected_on_revision_change |
| pacing_streak_reset_on_non_state_change | 114758682845 / 100 | `a2a3437f199ad48957145579dddba91b556ea973` | goal_pacing_first_immediate_second_at_60s |
| pacing_timer_not_cancelled_on_invalidation | 114758682859 / 100 | `30878f83dfa67efe5a972f7472b865bcb8abf519` | pacing_invalidation_cancels_armed_timer / pacing_event_wake_preempts_timer |

## Sources and logbook (2026-10-12)

- Normative inputs: reviewed task description/scope/AC, `surface-table.md`, and
  `TASK-260929-309h9n_review-verdict-rev2.md` (five distinct findings).
- Context/evidence: `TASK-260929-309h9n_results.md`,
  `TASK-260929-309h9n_hosted-precheck-9.md`, `TASK-260929-309h9n_mutants.json`.
  These are resources on the reviewed task; reads only.
- Implementation citations in JSON are pinned to tree C. Key files:
  `ext/goal/src/{continuation_schedule,background_wait,extension,runtime}.rs`,
  `app-server/src/extensions.rs`, `features/src/lib.rs`,
  `config/src/schema.rs`, `core/config.schema.json`, and named test suites
  under `codex-rs/`. The P3-1 base is not a review finding.
- Independent logbook anomaly: precheck-9 report omits retry detail; retrieved core
  log demonstrates the same P4a TRY 1 FAIL / TRY 2 PASS despite pacing-off fixture.
  Record DELTA3-N1 and request targeted synchronized hosted diagnostic; do not claim
  a proven cause or ask for local shared-target builds.
- Decision: accept scheduler policy rework with this note and stated evidence bounds.
  All five prior findings addressed individually; no blocking new mechanism found.
  Only this panel task receives the verdict, notes, checklist and researcher handoff.

```verdict-findings
{
  "findings": [
    {
      "id": "DELTA3-N1",
      "row": "one live timer",
      "invariant": "B2-N1 / D-N1: retain failed first attempts and bound attribution; aggregate green is not evidence of reliable first-try check-in behavior.",
      "mechanism": "Precheck 9 still retries scheduled_checkins_fire_through_production_runtime_under_paused_time: TRY 1 FAIL 10.515s, panic core/tests/common/lib.rs:393 timeout waiting for event; TRY 2 PASS 1.321s. The candidate fixture supplies continuation_pacing:false, so removal of pacing from this fixture did not eliminate the flake. It keeps a stalled Armed receipt throughout, and CheckInTimer is unchanged by the scheduler delta. The fixture advances paused time after TurnComplete/manual idle without awaiting the next arm; teardown synchronization remains a plausible lead, not a proven cause. The report claims only aggregate lane success and explicitly avoids a precheck-9 first-try claim. No deterministic production defect or new pacing regression established. Keep this as an informational reliability follow-up, not grounds to reject this delta.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs:115-119,199-320 at 3c5cbffcc73270bec86364ab42550441c87f933c",
          "command": "gh run view 38232681612 --repo ivanopcode/codex --job 114758681056 --log",
          "expected_failure": "Executed retrieval exit 0. Observed hosted TRY 1 FAIL (10.515s), TRY 2 PASS (1.321s); individual failed test process numeric exit is not printed, so unknown. Snapshot core aggregate success: 5131 passed, 2 flaky, 11 skipped. No local tests run."
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs::scheduled_checkins_fire_through_production_runtime_under_paused_time",
          "command": "HOSTED REQUEST, NOT RUN: just test -p codex-core -E 'test(scheduled_checkins_fire_through_production_runtime_under_paused_time)' with retries disabled and arm/teardown tracing; compare a fixture variant awaiting the fresh arm after each TurnComplete",
          "expected_failure": "No failure presumed; record per-attempt failure rate and identical 3-request/quota/warning assertions. Requested diagnostic exit unknown."
        }
      ],
      "severity": "note",
      "repeat-of": "D-N1"
    }
  ],
  "notes": [
    "Non-recording DELTA review. Every finding in merged rev2 was examined before same-class and regression sweeps. No write of any kind was made to TASK-260929-309h9n; no accept_cr/reject_cr/withdraw_cr/status/handoff there.",
    "A2-F1 fixed through its explicit-production-policy alternative: default-on Stable feature plus ordinary config opt-out, removed test-only env reader and ambient unit assumption. B2-N2 and D-N2 same switch/API concerns separately checked and resolved; not collapsed into the flake. B2-N1 fixture isolation implemented; D-N1 attribution remains unknown and is carried as DELTA3-N1. Rev1 direct blocker proof and narrow app-server opt-outs retained.",
    "Policy bounds: [features] goal_continuation_pacing=false restores immediate consecutive automatic continuations. Read at runtime thread creation/on_thread_start; in-place config updates and on_thread_resume do not apply a new pacing value. A new resumed runtime may run on_thread_start with its loaded config before on_thread_resume. Results Production policy and bounds / Disclosed bounds state start-only, no mid-thread toggle. Feature API field docs could repeat that lifecycle for host implementers; this is a documentation recommendation, not an alleged unsupported toggle.",
    "Scope pinned to base 67789e1e and candidate 3c5cbffc. Trunk P3-1 is excluded. Old-base rework diff af312067 -> eb655488 checked separately; import-only refresh preserved PlanCommitInput and PromptFragment and production flag mapping. No candidate code was edited.",
    "Execution distinction: this panel executed temporary-index replay, static Git/JSON checks, mutation applicability/tree binding and hosted metadata/log retrieval. No cargo, just, build, Rust test, new hosted run or new mutation execution. Hosted evidence was accepted after independently verifying exact identities, not rerun locally.",
    "Coverage 9/9 surface rows, one result each; 7/7 supplied mutation trees bound to executed red hosted lanes. Hosted snapshot core 5131 passed (2 flaky), 11 skipped; small 1489 passed, 1 skipped; app-server 1834 passed, 2 skipped. 22 pacing unit functions/pass records after removal of the ambient-env test (rev2 had 23). Snapshot core other retry: permission_request_hook_allows_exec_command_without_user_approval. No additional first-try reliability claim.",
    "Blind spots retained: no dedicated public-entry quiet-timer wake/stale-ticket attack, full-history equality, Windows/foreign-exec replay, clock rollback experiment or public saved-streak restart in this panel. note_release has no production caller; receipt/mail revision checks provide indirect stale-admission refusal. Generator was inspected statically; just write-config-schema was not executed.",
    "Available project-management SKILL.md was read; its referenced .roles/reviewer/role.md is absent from that installed package. Used the explicit panel/task review-round contract (sweep all rows, bounded free hunt, truthful evidence), without treating missing file as absent review obligations."
  ],
  "surface_results": [
    {
      "row": "spacing and streak math",
      "result": "held",
      "attack": "Attack off-by-one, overflow/cap, resets on poll/tool success/text, classifier divergence.",
      "evidence": "continuation_schedule.rs:47-54 bounds shift, uses checked multiplication and caps at 1800s; background_wait.rs:483-485 uses pacing_delay(completed_streak+1). State-change observation is read from P4b-1 accounting before finish_turn, not tool success. Hosted 22 pacing units pass, including n=0/1/2/3, cap and reset. Missing-cap mutation fails small with exit 100; non-change-reset mutation fails core with exit 100. Immediate-first/60s-second entry rule is the prior authorized decision; completed-count vs upcoming-index wording discrepancy remains disclosed, not a requested behavior reversal."
    },
    {
      "row": "polls grow the streak end to end",
      "result": "held",
      "attack": "Drive actual app-server thread/goal/set and two get_goal poll turns; inspect request and delay assertions.",
      "evidence": "Hosted snapshot app-server job 114758681075 executes goal_pacing_two_polls_first_immediate_second_60s, PASS 69.430s. Candidate asserts first delay <28s, second >=58s, 4 requests (2 per turn), no third within 8s and still Active. Default feature remains enabled in this fixture. Reset mutation independently kills core two-turn test. Request counts are passing-test assertions, not CI-wide request totals."
    },
    {
      "row": "one live timer",
      "result": "held",
      "attack": "Attack second timers, leaked replacements, event preemption, known-work priority and shared-slot regression.",
      "evidence": "One CheckInTimer slot, generation-guarded replacement, abort hook and claim_due_deadline; runtime releases the goal permit when returning Wait. Known nonempty work selects existing check-in path before pacing. Hosted units cover replacement, event wake, cancellation and known-work precedence; uncancelled-invalidation mutation fails small with exit 100. Pacing-enabled public notified-exec and user-burst tests pass (1.998s and 3.071s), asserting 4 and 6 requests. Dedicated public wake while a quiet pacing timer is proven armed is not supplied; units drive note_turn_start directly. P4a is now configured pacing-off; recurring hosted retry is DELTA3-N1, not silently green."
    },
    {
      "row": "ticket invalidation and admission",
      "result": "held",
      "attack": "Attack changed revision/generation/predecessor, reuse, fast intervening human turn, pending mail/read failure and publication race.",
      "evidence": "background_wait.rs:581-659 consumes one attempt under Mutex and rechecks generation, outstanding identity, goal, revision, predecessor and emptiness. Runtime publishes the existing admission checker; core/session/goal_admission.rs rechecks revision at publication under receipt/mailbox locks. Turn start invalidates before enabled check, human contribution calls note_human_input, steering/mutation/clear/stop/resume invalidate. Hosted stale-revision mutation fails small with exit 100. Fast-human, predecessor, reused-ticket and wrong-generation units pass; these are helper-level attacks with static production wiring, not newly executed public stale-ticket injections."
    },
    {
      "row": "blocker order and waiting turns",
      "result": "held",
      "attack": "Attack scheduling before blocker, changed threshold, successful waiting-text turns classified empty.",
      "evidence": "extension.rs:380-436 invokes unchanged EmptyResponse stop before note_turn_completed and finish_turn. Hosted core goal_pacing_empty_blocker_runs_before_rescheduling PASS 1.039s asserts Blocked, no armed wait and requests remain 3 after +241s. Selective blocker-skipping mutation fails this production-runtime test with exit 100. Waiting-text unit passes; public poll turns send nonempty waiting text and remain Active while paced."
    },
    {
      "row": "transient state",
      "result": "held",
      "attack": "Attack persisted streak/subscription/deadline, resume reconstruction and quota renewal on completion.",
      "evidence": "WaitState has no serialization; note_resume clears generation-bound waits/streak/predecessor and check-in quotas, without changing pacing_enabled. Extension resume reconciles then restore_after_resume calls note_resume. Empty completion clears wait episode without resetting check_ins_used. Hosted pacing_resume_restarts_at_floor_and_resets_quotas passes. Restart resets transient quotas and loses live observation, disclosed in results. No public saved-streak restart test newly executed; resume behavior is unit evidence plus static lifecycle trace."
    },
    {
      "row": "no model-visible change",
      "result": "held",
      "attack": "Attack prompt fragments, scheduling history events and cache-busting context.",
      "evidence": "Candidate scheduler creates no contextual fragment or history event; runtime reuses existing continuation steering. Hosted app-server two-poll test scans all four request bodies for pacing/streak/ticket markers and unexpected exec-completion fragments; no-warning unit passes. Existing PromptFragment import was retained during P3-1 refresh; no scheduler prompt introduced. Marker scans are bounded evidence, not full-history equality."
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "attack": "Independently replay every supplied mutation and bind hosted failing commit trees; inspect killer selection and counts.",
      "evidence": "7/7 patches apply to candidate temporary index; each independently computed mutant tree equals the commit checked out by its retrieved failing hosted job. All 7 failed lanes print exit 100 and named killer failures, covering 5/5 required families plus entry rule and feature policy. Snapshot lanes are 4/4 success. Counts asserted: core quiet turns 2, empty blocker 3, app-server polls 4, public wakes 4/6, units 0. Aggregate mutant-lane model requests unknown. Hosted mutation filters select small/core; mutant app-server execution is not claimed."
    },
    {
      "row": "placement and size",
      "result": "held",
      "attack": "Attack ambient production opt-out, all config constructors, schema drift, feature lifecycle/API and ownership/size.",
      "evidence": "A2-F1/B2-N2/D-N2 closure: removed switch/reader/exports absent whole-tree, and no env access in ext/goal/src. Stable default-on GoalContinuationPacing maps in app-server/extensions.rs:84-89 to required continuation_pacing field; all eight literal constructors accounted for (one production, seven test fixture insertions/mappers). Tests explicitly choose false/true. Both global/profile schema maps add exactly the boolean key; config/src/schema.rs:163-165 derives this shape from FEATURES. Thread-start captures bool before config move; resume/config-update do not reread policy, accurately disclosed in task results. Public config-field doc is terse and does not itself state start-only. 135-line new scheduler module, no core scheduler/dependency growth. Existing background_wait 908 lines and extension 820 lines remain size advisories, already noted in rev2; no new unrelated API or dependency found."
    }
  ],
  "free_hunt": [
    {
      "family": "ambient switches / host coverage / schema",
      "result": "No surviving ambient pacing production input found. Required typed field forces literal callers to choose policy; the sole production mapper uses feature config. Profile/global schema exact additions match generator boolean branch. No missed host bypass established."
    },
    {
      "family": "mid-thread config / resume / API breakage",
      "result": "Start-only policy matches results disclosure. on_config_changed updates Goals enablement and stored config but leaves live pacing policy; no silent dynamic toggle promised. Added public GoalExtensionConfig field requires source caller adaptation; all in-tree constructors accounted for; no app-server wire/rollout/CLI-parameter breaking shape found."
    },
    {
      "family": "wall-clock / release / read failure",
      "result": "SystemCheckInClock wall-clock rollback may reject a single fired claim without rearming; timer code predates and is unchanged by this delta, so inherited unverified risk, not new proven regression. Requested future attack: pacing_clock_rollback_rearms_until_deadline through production timer/runtime. Read failures return WaitOnReadFailure/Wait, never empty fallback. No release caller claimed."
    },
    {
      "family": "P4a rework reliability / synchronized teardown",
      "result": "Exact snapshot repeats timeout with pacing off; DELTA3-N1 preserves the anomaly and unknown attribution. Desired hosted diagnostic is specified in reproductions. No new build run or speculative causal assertion."
    }
  ]
}
```
