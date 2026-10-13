# TASK-261012-2x08jb — R141 DELTA panel, CR-TASK-260929-309h9n-2 revision 2

accept

Replay check: base `e0eff057620104a416080da616256ee7f32bda1b` plus the attached revision-2 patch gives tree `af312067fcd2392b78deb95d3f71925e739622b7`, exactly the expected candidate. Temporary indexes only; no nested worktree, source edit, commit, build or test execution.

This independent panel is ready for review. It records no acceptance, rejection, status, resource, note or handoff on TASK-260929-309h9n — continuation-schedule. The recording reviewer owns the merged decision.

## Commands and exit codes

Commands below ran as standalone processes. Shell redirection only saved logs; no gate was piped through tee. Hosted executions are reused evidence, explicitly distinguished from this panel's own commands.

| Own replay command | Exit | Result |
|---|---:|---|
| `mkdir -p .temp` | 0 | Staging directory |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-2x08jb-replay.idx" git read-tree e0eff057620104a416080da616256ee7f32bda1b` | 0 | Base loaded |
| `task-board resource get TASK-260929-309h9n TASK-260929-309h9n_change-request_rev2.patch --output .temp/TASK-260929-309h9n_change-request_rev2.patch` | 0 | Patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-2x08jb-replay.idx" git apply --cached .temp/TASK-260929-309h9n_change-request_rev2.patch` | 0 | Patch applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261012-2x08jb-replay.idx" git write-tree` | 0 | af312067fcd2392b78deb95d3f71925e739622b7 |
| `git diff --check e0eff057620104a416080da616256ee7f32bda1b af312067fcd2392b78deb95d3f71925e739622b7` | 0 | Patch whitespace check |
| `git diff --quiet 181cc48fbd0b927f134ba39d268882a52551e776 af312067fcd2392b78deb95d3f71925e739622b7 -- codex-rs/ext/goal/src codex-rs/core/tests/suite/goal_background_wait.rs` | 0 | Production goal code and P4a core test unchanged from rev1 |
| `git status --short` | 0 | Clean tracked worktree; review staging ignored |

Each mutant used its own index `.temp/TASK-261012-2x08jb-mutants/<name>.idx` and its materialized `<name>.patch`. For EACH of the six names below, these four standalone commands ran, each exit 0:
`GIT_INDEX_FILE="<absolute index>" git read-tree af312067fcd2392b78deb95d3f71925e739622b7`;
`GIT_INDEX_FILE="<absolute index>" git apply --cached --check .temp/TASK-261012-2x08jb-mutants/<name>.patch`;
`GIT_INDEX_FILE="<absolute index>" git apply --cached .temp/TASK-261012-2x08jb-mutants/<name>.patch`;
`GIT_INDEX_FILE="<absolute index>" git write-tree`.
All six replayed trees equal the corresponding hosted commit trees. No mutant was applied to the working tree.

| Mutant name | Replayed/hosted tree | Hosted commit | Named killer |
|---|---|---|---|
| pacing_blocker_skipped_for_paced_turns | a1dba7bba00fa63c16e628849fbee252365a9e9e | 954a2cbb649e6d396bbd626c50ef366ea06d87d7 | goal_pacing_empty_blocker_runs_before_rescheduling |
| pacing_first_continuation_paced_after_human_turn | 25517a1db738240b778a36286a860de579dba140 | 0cf0ca15d677a55dc254fc4e1486679244ebbbba | pacing_first_continuation_after_human_turn_proceeds_immediately |
| pacing_missing_cap | 116680a7a4f27a2ca92989096cfb2ef9c6188947 | 875b0f0199350510d876d4f10891a12bfe7e300d | pacing_delay_n1_n2_n3_and_cap |
| pacing_stale_ticket_admission_skip_revision | a5e0d35485f205d418617f301fe1fc7d2a63e6a3 | b5ab61ebb9c0debc69c79841b3e38cc7c39cb1f9 | pacing_stale_ticket_rejected_on_revision_change |
| pacing_streak_reset_on_non_state_change | 38d5bb7671c9cea6d0be138f4da897a52f1c72ef | d71f19eb51698a7b442838d1e161e4a7947cce36 | pacing_two_polls_grow_streak |
| pacing_timer_not_cancelled_on_invalidation | 5ceec086eb384524d6ff6792b46d74e825ef9fb1 | ed969ad2969dbaaba920570c578d892e979c12b8 | pacing_invalidation_cancels_armed_timer |

Own hosted reads: `gh run view 38188455502 --repo ivanopcode/codex --json jobs,headSha,conclusion,url` exit 0; repeated with a compact jq projection and output redirection, exit 0. For EACH job id 114615812434, 114615834923, 114617661286, 114617661821, 114617661332, 114617661324, 114617661353, 114617661351, 114617661382, 114617661349, 114617661390, 114617661290, `gh run view 38188455502 --repo ivanopcode/codex --job <id> --log > .temp/hosted-<id>.log` exited 0. Successful log retrieval does not mean a mutant test passed.

Own `git rev-parse <snapshot-or-mutant-commit>^{tree}` comparison exited 0. The inline Python evidence audit exited 0: snapshot 1/1 exact-tree matches, mutants 6/6 exact-tree matches, named killers 6/6 visibly FAIL, each selected mutant runner visibly exits 100. Candidate inventory/read audit exited 0 and counted 23 pacing unit tests. No claim of executing Rust tests locally.

Diagnostic failures are not passing gates: initial board projection used unknown `resources` field (exit 1), repaired with `outcomeResources preconditionResources` (exit 0). `schema(get)` used unsupported positional syntax (exit 1); ordinary scoped get succeeded without needing schema. A skill-relative reviewer role did not exist (`cat` exit 1); read `/Users/administrator/.roles/reviewer/role.md` exit 0. Role-file searches had no matches (exit 1) / one missing directory (exit 2). Two speculative `git show` paths, ext/goal/src/host.rs and ext/goal/src/goal_admission.rs, exited 128 inside the materialization script; no absence inference was made from them. Subsequent symbol search located admission in core/src/session/turn_input.rs. `command -v logbook` exit 1: the logbook record is included below. Resource retrievals for surface-table, merged rev1 verdict, producer brief, entry-rule decision, results, mutants, rev2-validation and hosted precheck 6 all exited 0. `task-board spawn directives RUN-261012-d09b93` exit 0: no directives or bound goal.

Own artifact gate: `python3 .temp/TASK-261012-2x08jb-validate-verdict.py` exited 0. It parsed the sole JSON block, checked all required finding/reproduction fields, and compared nine unique ordered result rows to the source surface-table.

## Reused hosted execution evidence

[Run 38188455502](https://github.com/ivanopcode/codex/actions/runs/38188455502) uses snapshot commit `a921adbbdf13ac8327478dc15274dc160e5bedad`, whose tree was independently checked equal to the replayed candidate. The workflow's head SHA `9f8fdf9...` is the workflow revision, not the candidate. Plan-job output names each matrix checkout; the mutant trees above match it.

Snapshot lanes are green: small 1486/1486 passed (1 skipped), core 5083/5083 passed (11 skipped, 1 flaky), app-server 1834/1834 passed (2 skipped), and lint succeeded. These are hosted results; successful snapshot steps do not print numeric exit telemetry, so this panel does not invent it. The entire workflow conclusion is FAILURE because the deliberate mutant jobs fail. Their observed runner exits are 100, expected-red evidence, not green gates.

The direct blocker mutant is [mutant-1 core, job 114617661324](https://github.com/ivanopcode/codex/actions/runs/38188455502/job/114617661324): its ONLY failing test is goal_pacing_empty_blocker_runs_before_rescheduling, failing all three attempts at the expected Active versus Blocked assertion (core test line 384); runner exit 100. Other named killers are observed in mutant-2 small (114617661290), mutant-3 small (114617661349), mutant-4 small (114617661351), mutant-5 small (114617661390), and mutant-6 small (114617661382), all runner exit 100.

The stored CR validation log is 402 bytes, not a full local test log. It contains the exact-tree mini-hosted-gate command, [exit 0], and coverage_unit=exact_command_shard required=1 green=1 failed=0 missing=0 test_case_coverage=unknown. This attests the hosted binding; test coverage comes from the independently retrieved hosted logs. General 64 KiB truncation warnings are not a reason to imagine missing commands ran.

## Previous findings and delta

A-F1 is closed: candidate core/tests/suite/goal_continuation_pacing.rs:294-416 drives GoalService::apply_runtime_effects, the real timer/runtime/admission path, and production idle teardown with pacing enabled. Three truly empty responses yield Blocked, no armed deadline after idle, and exactly three requests even after +241 seconds. Its selective mutant skips EmptyResponse blocking only for pacing-enabled automatic goal turns, leaving the blocker intact elsewhere. The hosted killer fails on that exact mechanism. Source on_turn_stop still executes the blocker before note_turn_completed (ext/goal/src/extension.rs:380-429).

A-N1 is closed: app-server/tests/suite/v2/goal_background_wait.rs:175-200 only adds the process override when requested; notified-exit and user-burst callers pass false, unopted and headless callers pass true. All four pass in the exact snapshot app-server job. This repairs switch scope; it does not convert those two wake tests into a public attack with an already armed pacing timer.

F1-blocker-mutant-proxy is superseded by A-F1's direct production-path proof. The old inactive-status proxy is absent from the six supplied mutants.

Revision delta changes only two test files. No goal production file changed from rev1, as the standalone diff-quiet check confirms. The core rework removes manual idle emits, pauses before polling for the production arm with a real 10-second bound, and uses ThreadIdle after the blocker. Hosted candidate pacing tests pass first attempt (0.581s and 0.945s); app-server two-poll test passes first attempt (69.314s). This supports the correction without claiming broad flake elimination.

All source references in the JSON below refer to tree af312067fcd2392b78deb95d3f71925e739622b7, never ambient HEAD.

```verdict-findings
{
  "findings": [
    {
      "id": "D-N1",
      "row": "one live timer",
      "invariant": "An executed public-entry check-in attack must not be described as reliably green when it retries; diagnose its relation to pacing without inventing a cause.",
      "mechanism": "The exact snapshot check-in test times out waiting for an event on TRY 1 (10.516s), then passes TRY 2 (1.222s). Its real Armed receipt is never completed or released, so every evaluation takes the nonempty-snapshot background-wait branch; it cannot enter evaluate_pacing_locked or install a pacing deadline. CheckInTimer, that test, and the goal production code are identical to rev1. However, TurnComplete precedes active-turn cleanup/idle and this P4a test still manually emits idle and advances time without waiting for a fresh arm. That pre-existing race is a plausible diagnostic lead, not an established root cause. Pacing adds turn-stop bookkeeping compared with the original pre-pacing base and may alter timing; direct slot interference is statically excluded for this fixture, timing-induced exposure is unknown. Recommend a focused hosted synchronized run with teardown/arm tracing before classifying the flake as unrelated.",
      "reproductions": [
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs:199-320",
          "command": "gh run view 38188455502 --repo ivanopcode/codex --job 114617661821 --log",
          "expected_failure": "Observed TRY 1 FAIL at core/tests/common/lib.rs:393, timeout waiting for event; TRY 2 PASS. Log retrieval exits 0; successful hosted step has no printed numeric exit. No deterministic local reproduction or root-cause assertion."
        },
        {
          "test_file": "codex-rs/core/tests/suite/goal_background_wait.rs::scheduled_checkins_fire_through_production_runtime_under_paused_time",
          "command": "HOSTED PROPOSAL: just test -p codex-core -E 'test(scheduled_checkins_fire_through_production_runtime_under_paused_time)' with arm/idle tracing and teardown synchronization, compared with the unsynchronized exact candidate",
          "expected_failure": "Not run in this panel. Require explicit per-phase arm/generation observations and repeated results; distinguish teardown race from an unexpected pending snapshot becoming empty. No failure is presumed."
        }
      ],
      "severity": "note",
      "repeat-of": "none"
    },
    {
      "id": "D-N2",
      "row": "placement and size",
      "invariant": "AGENTS.md prefers avoiding test-only implementation helpers and ambient test inputs; crate API should remain small.",
      "mechanism": "pacing_disabled_by_env and its exported environment-name constant exist solely for test compatibility according to their own docs. The reader runs in normal on_thread_start, so a real production process with CODEX_GOAL_PACING_DISABLED=1 also disables pacing. It is therefore a shipped opt-out, not a test-isolated hook, and 'pacing always active in production' is not enforced. No test here mutates the parent process environment; app-server overrides are child-process inputs. The entry-rule rework decision explicitly retained this switch for legacy tests, and rev2 narrows its scope as requested. This panel accepts that recorded compatibility exception for this delta; it does not declare the hook an ideal API or a blanket exception to AGENTS. Prefer typed dependency/config injection and reduce the exported testing API, or explicitly describe the production opt-out. The unit assertion that ambient env is not disabled remains an avoidable test determinism issue.",
      "reproductions": [
        {
          "test_file": "codex-rs/ext/goal/src/continuation_schedule.rs:42-53; codex-rs/ext/goal/src/extension.rs:184-188; codex-rs/ext/goal/tests/continuation_schedule.rs:841-849",
          "command": "git grep -n 'CODEX_GOAL_PACING_DISABLED\\|pacing_disabled_by_env\\|PACING_DISABLED_ENV_VAR\\|disable_pacing()' af312067fcd2392b78deb95d3f71925e739622b7 -- codex-rs",
          "expected_failure": "Static inventory command exits 0. The exact string 1 bypasses enable_pacing at normal thread start; the ambient-env assertion can fail under that setting. No process environment mutation, production launch, or new runtime failure was executed."
        }
      ],
      "severity": "note",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "Previous merged findings reviewed 3/3: A-F1 closed by direct blocker test and selective mutant; A-N1 closed by per-caller switch scope; F1-blocker-mutant-proxy superseded. Their source and exact hosted evidence were inspected independently.",
    "The explicit entry-rule decision in b2-rework-brief-precheck3.md is honored: first after human/goal mutation/resume is immediate; consecutive quiet turns subsequently wait 60s,120s,... capped at 1800s. The public tests require that behavior. The stale documentation calling n the completed streak while runtime passes completed streak+1 is unchanged advisory debt; do not infer a requested reversal of the approved rule.",
    "Sources: source-task surface-table.md, TASK-260929-309h9n_review-verdict-rev1.md, producer-brief.md, b2-rework-brief-precheck3.md, TASK-260929-309h9n_results.md, TASK-260929-309h9n_mutants.json, TASK-260929-309h9n_change-request_rev2-validation.log and TASK-260929-309h9n_hosted-precheck-6.md, plus candidate git objects and independently fetched hosted logs.",
    "Request counts asserted by hosted public-entry tests: core quiet turns=2; core blocker=3, still 3 after +241s; app-server two polls=4; pacing-enabled notified-exit=4, user-burst=6. Goal helper/unit tests issue 0 requests. Mutant-job aggregate model request count is unknown, not reconstructed from baseline assertions.",
    "Pacing unit inventory is 23, not the results' 22. Hosted snapshot jobs run full selected package lanes; the pacing/goal filter applies to mutant jobs, not snapshot lanes.",
    "Cumulative CR against its supplied base is 31 files, +3900/-34, including the inherited observations stage. Results' 17-file scheduler slice is not the cumulative CR. New continuation_schedule.rs is 148 lines, while background_wait.rs is 923; the size/extraction advisory from rev1 remains. Revision delta adds tests only and does not worsen production module size.",
    "No cargo, just, build, local Rust test, full workspace, Windows or foreign-exec execution occurred. Hosted results are Linux evidence. Static source reasoning supplements executed hosted attacks; it does not become a newly executed public test.",
    "note_release has no production caller in this candidate (also noted in rev1). Normal receipt changes are rechecked via pending-work revision and event turn-start invalidation; direct note_release unit coverage is not claimed as production-dispatch proof.",
    "Logbook command unavailable (exit 1); the task-scoped outcome embeds the important anomaly, decisions and bounds below. No write was made on TASK-260929-309h9n."
  ],
  "surface_results": [
    {
      "row": "spacing and streak math",
      "result": "held",
      "attack": "Try completed/upcoming index drift, overflow, missing cap, repeated read-only polls and text/tool-success resets.",
      "evidence": "continuation_schedule.rs:62-70 clamps shift, checked multiplication and cap; background_wait.rs:490 uses streak+1 under the approved upcoming-continuation rule. on_turn_stop consumes the existing P4b-1 observed-state classifier, not model text or generic success. Exact hosted units cover n=0/1/2/3, u32::MAX, reset and non-change; reset/cap selective mutants fail named killers (runner 100). Core actual runtime waits ~60s after the first quiet turn; docs-index discrepancy disclosed."
    },
    {
      "row": "polls grow the streak end to end",
      "result": "held",
      "attack": "Attempt read-only get_goal polls resetting activity or a helper-only proof without requests.",
      "evidence": "app-server/tests/suite/v2/goal_continuation_pacing.rs:143-218 drives thread/start and thread/goal/set with two real get_goal tool dispatches. Candidate hosted app-server test passes first try; asserts first immediate, second >=58s, exactly four requests and no early third within 8s. Core counterpart=2 requests. Streak-reset mutant kills the matching small test and both core tests. Third-turn full 120s boundary is covered by fake-time units/core, not this 8s window."
    },
    {
      "row": "one live timer",
      "result": "held",
      "attack": "Try a second timer, replacement leaks, event wake leaving an old timer, and pacing overwriting a governing pending-work deadline.",
      "evidence": "BackgroundWaitState has one pending_deadline and runtime.rs:616-634 always uses its existing CheckInTimer; timer owns one abortable slot and detaches before callback. Nonempty pending snapshot selects background waits, with no pacing evaluation. Exact small tests check shared registration replacement, event invalidation and hook invocation; uncancelled-hook mutant fails. Pacing-enabled app-server notification/user-burst attacks pass. D-N1 records the P4a flaky execution and its unknown timing cause. Public wake while an already armed pacing timer is pending remains a named coverage bound."
    },
    {
      "row": "ticket invalidation and admission",
      "result": "held",
      "attack": "Try revision/predecessor/generation mismatch, fast human turn, ticket reuse, newly pending mail and failed reads between evaluation and publication.",
      "evidence": "background_wait.rs:569-665 takes the attempt once under its lock, rechecks generation, goal, revision, predecessor, outstanding/reuse and empty pending snapshot. Lifecycle input/start hooks invalidate; runtime goal mutation/clear/stop/resume reset. Existing Core admission retains mailbox and revision checks around publication; goal permit spans read/start. Exact small stale/fast-human/reuse/pending/read-error tests pass; skip-revision mutant kills pacing_stale_ticket_rejected_on_revision_change. Those detailed attacks are state-machine entries; public pacing admission itself runs in the core/app-server tests. Standalone note_release production dispatch is not claimed."
    },
    {
      "row": "blocker order and waiting turns",
      "result": "held",
      "attack": "Narrow empty blocking specifically for paced automatic turns and require the production third empty response to block before rescheduling.",
      "evidence": "A-F1 closed. extension.rs:380 invokes EmptyResponse blocker before :424 note_turn_completed. New core test goal_pacing_empty_blocker_runs_before_rescheduling reaches the real timer and teardown, asserts Blocked, no arm, three requests and continued silence; baseline passes first attempt. Corresponding hosted mutant-1 core fails only this test all 3 attempts at Blocked assertion, runner exit 100. Nonempty waiting get_goal poll turns remain paced, proven by app-server four-request test."
    },
    {
      "row": "transient state",
      "result": "held",
      "attack": "Try serializing streak/timer, restoring stale subscriptions, resetting human allowance on completion, or resume keeping an old pacing claim.",
      "evidence": "All pacing fields are in ephemeral WaitState; no rollout/config/API serialization was added. note_resume clears generation-bound waits, streak, predecessor, ticket and quota; runtime reconciles goal first. Exact small resume/quota/late-completion tests pass. Empty-snapshot reassessment does not renew check_ins_used; reset-on-restart is disclosed. No public restart with an accumulated nonzero pacing streak or independent persistence mutant was run."
    },
    {
      "row": "no model-visible change",
      "result": "held",
      "attack": "Look for timer/context/history fragments, warnings or scheduling markers added to outbound requests.",
      "evidence": "Source path changes scheduler state and returns before constructing the same continuation_steering_item; no pacing context/prompt/history builder added. Exact hosted app-server inspects all four request bodies for pacing/PacingTicket/continuation_schedule/streak and absence of unrelated completion fragments; hosted small warning tests pass. Marker absence alone is not whole-history equality; source diff supplies complementary evidence."
    },
    {
      "row": "mutants and measurement",
      "result": "held",
      "attack": "Replay every mutant against the exact candidate and compare hosted checkout trees, named failing tests, runner exits and request assertions.",
      "evidence": "6/6 apply-check/apply/write-tree success in separate indexes, 6/6 hosted tree matches and named kills; five required semantic families reset/cap/stale-ticket/cancel/blocker now covered 5/5, plus entry rule. All selected failing runners exit 100, expected-red. Candidate lanes green with disclosed check-in retry. Requests=2/3/4 for the three pacing public scenarios, 4/6 for the enabled wake scenarios, 0 for units. Aggregate mutant request total unknown."
    },
    {
      "row": "placement and size",
      "result": "held",
      "attack": "Check scheduler ownership, core dependency direction, oversized module growth and unnecessary exported testing APIs.",
      "evidence": "Goal owns math/tickets (148-line private module with explicit exports), state/admission remains in existing goal wait state and shared slot. No new core->goal scheduling dependency. Thin core observation hooks in cumulative CR are inherited from the prior observation stage; revision delta is two test files. Existing 923-line background_wait and +3900/-34 cumulative size debt are explicitly disclosed, not falsely certified below guidance. D-N2 records the production test-switch/export advisory and accepted scoped compatibility exception."
    }
  ],
  "free_hunt": {
    "budget": "Four bounded static families beyond the required sweep; reuse exact hosted execution, no new builds.",
    "results": [
      {
        "family": "precheck-6 check-in flake",
        "result": "D-N1 advisory; direct pacing-slot overwrite excluded by permanently nonempty receipt branch, exact cause/timing contribution unknown. Proposed hosted arm/teardown trace named."
      },
      {
        "family": "test-only production env reader",
        "result": "D-N2 advisory; exported helper is compatibility-only by intent but live in release code. Parent environment is not mutated by tests; ambient assertion remains fragile."
      },
      {
        "family": "rework teardown safety",
        "result": "Core tests now use production sole armer and bounded pause/yield observation. Blocked tail uses registered ThreadIdle. Both exact candidate tests pass first try and blocker mutant fails the intended status assertion. No production rework to regress."
      },
      {
        "family": "evidence identity and scope",
        "result": "Independently matched snapshot 1/1 and mutant trees 6/6; workflow FAILURE expected from mutant jobs; package green counts and one flaky test read from real logs. Corrected 23-vs-22 unit count and cumulative-versus-scheduler-only diff claims."
      }
    ]
  }
}
```

## Logbook — 2026-10-12

TASK-261012-2x08jb — R141 DELTA panel rev2: replay tree exact; previous findings 3/3 addressed; nine rows swept 9/9, held 9/9 within stated bounds; required mutant families 5/5, supplied mutants killed 6/6. Verdict accept with two non-blocking notes. The P4a TRY-1 failure is preserved as real evidence; direct pacing branch interference does not fit this fixture, and its precise cause remains unknown. The environment opt-out is a shipped compatibility hook, not compile-time test isolation; the prior explicit rework decision is accepted for this delta, with AGENTS preference and ambient-test weakness disclosed.

Only the panel task receives this new text outcome, checklist updates and researcher handoff. No source-task mutation, local build, source code change or commit. Local command exit codes and hosted runner failures are recorded above. The next owner is the orchestrator merging independent panels, then the recording reviewer.

