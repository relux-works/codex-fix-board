# R141 panel B — CR-TASK-260929-2gp04j-1, revision 1

Verdict: accept

## Replay and review boundary

On October 2, 2026, the patch replayed from base
`ea8899e6f97aea64136159286840c28c955243e8` through a temporary index to
`4d289590739432aa55c2a3868c2b4a5472b07c92`, exactly the expected candidate tree.
The five G1 paths are byte-unchanged against checkpoint
`58042581a0b507ae62e7b1d8381c429baea1f689`.

This is a non-recording panel, not CR acceptance. No mutation, note, resource,
accept/reject, status change, or handoff was issued on TASK-260929-2gp04j.
No Cargo, just, build, product test, formatting, or mutant execution ran locally.
Candidate code was read from the pinned tree, not assumed from the Story HEAD.
Only task-scoped scratch files were written in the managed run worktree;
the latest run-write boundary takes precedence over the generic instruction to
prepare an artifact outside it. The board receives artifacts via its CLI only.

## Bounded review plan

Decision: whether this panel recommends this exact revision to the recording
reviewer. Frozen precondition: the base, patch and candidate tree above; no new
grammar is involved. Budget: 30 minutes including evidence packaging, with a
three-minute bounded free hunt after the single-row sweep. Artifact budget:
this verdict and one compact evidence outcome; no attached source archive or
duplicate CI corpus. Serial prerequisites: zero. Exit: exact replay, one result
per surface row, seven transition judgments and the additional architecture/
size judgments recorded. Next implementation slice: none required by a
reproduced blocking finding. This is not a recursive research prerequisite.

## Commands and real exit codes

All replay/check commands ran directly, without tee or a status-masking pipe.
The index path is `.temp/TASK-261002-3k97mc-replay.idx`.

| Command | Exit | Evidence/result |
|---|---:|---|
| `task-board m 'set_status(TASK-261002-3k97mc, status=analysis)'` | 0 | Only this panel task activated |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3k97mc-replay.idx" git read-tree ea8899e6f97aea64136159286840c28c955243e8` | 0 | Base loaded into a fresh temporary index |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev1.patch --output .temp/TASK-260929-2gp04j_change-request_rev1.patch` | 0 | Patch materialized read-only from source task |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3k97mc-replay.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev1.patch` | 0 | Exact patch applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3k97mc-replay.idx" git write-tree` | 0 | `4d289590739432aa55c2a3868c2b4a5472b07c92` |
| `git diff --exit-code 58042581a0b507ae62e7b1d8381c429baea1f689 4d289590739432aa55c2a3868c2b4a5472b07c92 -- codex-rs/core/src/tools/spec_plan.rs codex-rs/core/tests/suite/current_time_reminder.rs codex-rs/ext/extension-api/src/goal_activity.rs codex-rs/ext/extension-api/src/lib.rs codex-rs/ext/extension-api/tests/state.rs` | 0 | All G1 paths unchanged |
| `git diff --check ea8899e6f97aea64136159286840c28c955243e8 4d289590739432aa55c2a3868c2b4a5472b07c92` | 0 | Patch whitespace check |
| `git rev-parse '016a4248cf1984b97e786ce8573ad40c9438dfbf^{tree}'` | 0 | Hosted snapshot has the identical candidate tree |
| `gh api repos/relux-works/codex/actions/runs/37002709023 --jq '{id,head_sha,status,conclusion,event,created_at,updated_at}'` | 0 | Completed/success; dispatch head differs from checked-out snapshot |
| `gh api repos/relux-works/codex/actions/runs/37002709023/jobs --jq '.jobs[] \| {name,status,conclusion,steps: [.steps[] \| {name,conclusion}]}'` | 0 | Four success lanes; intended test/lint steps actually ran |
| `gh run view 37002709023 --repo relux-works/codex --log` | 0 | Logs verify checkout `016a4248...` and named tests passing |

Input retrieval for `surface-table.md`, `producer-brief.md`, results and
hosted-precheck-2 on the source task, and `final-plan.md` on that same task,
each succeeded (exit 0). An attempted plan lookup on the parent Story failed
(`resource not found`, exit 1); it was not treated as absence of a plan.
An initial unsupported `resources` projection failed (exit 1); corrected
compact task projection succeeded. An initial candidate archive with an
incorrect optional path failed (exit 128); the narrower archive command
succeeded (exit 0). An attempted shell containing `rm -f` was rejected before
execution (no process exit code); no removal ran. A stale reviewer-reference
path was unreadable; the actual installed reviewer contract was subsequently
read from `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md`.
None of these recovery steps is presented as a green validation gate.

The evidence outcome records each of the thirteen hosted-mutant retrieval
commands and their exit codes, plus the actual failing hosted-test exit codes.
Retrieval success is not test success. Expected-red mutants remain failing.

## Surface sweep and transition coverage

Surface table: **1/1 rows assigned a result**. `goal activity publisher`: held
for the attacks listed below, using existing exact-tree execution evidence
and this panel's independent static call-site review. Public-entry attacks
were executed in hosted precheck 2, not re-executed by this panel. This is a
bounded observation, not a proof that every interleaving or error is covered.

| Final-plan section 4 transition | Candidate production path | Exact-tree attack/evidence | Judgment |
|---|---|---|---|
| Successful create, before tool result | `ext/goal/src/tool.rs:185` reconciles under the permit after handler execution; `extension.rs:493` rereads committed state independently of tool name | Core `create_goal_changes_the_next_sampling_tools::{complete,paused,blocked,refused}`; backend `tool_finish_reconciles_committed_state_independently_of_tool_name`; v2 created/refused | Held: next request reflects committed creation, not a forged successful name |
| Turn start before accounting/Plan early returns | `ext/goal/src/extension.rs:252` reconciles before the token-baseline check and Plan branch | `turn_start_before_missing_baseline_and_plan_then_removes_cleared_goal` | Held for both early-return paths and cleared state |
| Resume / external set across statuses | `runtime.rs:495`, `runtime.rs:276`, `api.rs:280` reread; publisher maps Active/BudgetLimited only | Six `external_set_and_resume_reconcile_first_request` status cases, plus external-set and resume narrowing mutants | Held for 6/6 specified statuses; marker visibility does not admit BudgetLimited continuation |
| Update / automatic stop / accounting limit | `tool.rs:261`, `runtime.rs:369`, `runtime.rs:644`, `runtime.rs:708` | Complete/paused/blocked cases; backend automatic-stop errors/usage limit; `accounting_budget_keeps_sleep_without_automatic_continuation` | Held for observed terminal mutations and BudgetLimited retention/refusal |
| Clear including disabled feature and stale callbacks | `api.rs:300` clears after committed deletion while holding permit; `activity.rs:117` invalidates old reads | `clear_revokes_before_late_create_finish_and_stale_set_effects`; publisher stale-revision test | Held: late tool/API callbacks reread committed state; old read revision rejected |
| Stop / disable / re-enable | `extension.rs:205`, `extension.rs:219`, `runtime.rs:124`, `runtime.rs:134` | `disable_and_stop_revoke_activity_and_pending_options`; `disable_mid_turn_removes_sleep_from_next_request` | Held for contributor hook behavior; re-enable reconciles at the next lifecycle event, not synchronously |
| Read failure and recovery | `runtime.rs:144` / `activity.rs:80` unknown/error branch | `read_failure_revokes_activity_and_next_turn_recovers`; timestamp-error narrowing mutant | Held for an actual malformed GoalStore row at turn start; other timing windows remain a stated bound |

Coverage: **7/7 transition categories** and **8/8 AC categories** mapped to
production paths and attached execution evidence. The sole-writer claim is
production-scoped: test fixtures deliberately insert/remove GoalActivity to
attack stale and disabled-clear cases. There is no source-text gate in scope.
Disable tests invoke the actual contributor because Goals is session-static;
they do not establish an existing user-config route that flips Goals mid-turn.

## Additional judgments and bounded free hunt

1. **Size:** against the CR base, the cumulative diff is **1603 additions + 77
   deletions = 1680 changed lines in 22 files**. After the accepted G1 checkpoint,
   G2 is **1309 + 76 = 1385 lines in 17 files**. Both exceed the 800-line guidance;
   the brief's approximately 1334 count is stale. G2 production-source delta is
   475 lines; the larger total predominantly reflects integration coverage.
   The proposed inactive-publisher first stage (~225 lines) is separable, but
   leaves ~1160 lines and therefore does not itself achieve the stated limit.
   For upstream delivery, prefer accepted G1 separately, then inactive publisher,
   then staged hook activation with its matching tests (create/update; external
   set/resume/clear; lifecycle/error handling). Repartitioning the 530-line core
   test file must follow those behavior boundaries, not detach tests from hooks.
   This guidance issue is recorded as a note, not a fabricated runtime failure.

2. **Dev dependency:** `core/Cargo.toml:143` adds a dev edge to goal-extension;
   goal-extension has a normal edge to core. This is a package-level dev cycle,
   not a core-library runtime dependency cycle: core integration-test target →
   goal library → core library. Hosted core compilation and tests really passed.
   `defs.bzl:336` uses normal dependencies for the library and integration test
   rules add dev dependencies. No new normal core→goal dependency was found.
   This supports the G1 separation rather than undoing it.

3. **Bazel lock:** the exact source changes two Cargo.lock dependency edges,
   adds no new external version and wires activity.rs as Bazel compile data.
   `MODULE.bazel` consumes Cargo.lock, so "test-only" is not sufficient by itself
   to waive the repository instruction to run `just bazel-lock-update`.
   Producer results explicitly report a prior run of that command with exit 0
   and no lock delta. Accepted as attributed producer evidence, not a panel run.
   No independent Bazel lock check ran; the hosted fast lanes are Cargo lanes,
   not proof of Bazel lock freshness. The process command was required; an
   actual lockfile delta is not established as required by this panel.

4. **Free-hunt error window:** accounting's
   `runtime.rs:775 current_goal_status_for_metrics` can return a DB read error
   before `reconcile_live_activity` is reached. A failure that first appears
   during progress accounting, rather than during the preceding lifecycle
   reconcile, deserves a dedicated regression test. The existing malformed-row
   test attacks turn start, not this window. No permitted failing public-entry
   reproduction was executed here; this is a nonblocking suspicion, not a
   finding or a claim that a gate was reproduced broken.

5. **Free-hunt lease race:** the automatic-start read permit is stored in
   thread-wide ExtensionData (`runtime.rs:570`) and consumed by the next
   turn-start callback without binding to its submission (`extension.rs:254`).
   A user turn overtaking automatic submission, or disable/re-enable removing
   the lease, merits a scheduler-controlled attack before extending this
   mechanism. A normal automatic-start path is already covered by hosted tests;
   a blocking race was not reproduced, so this remains a note.

No wire payload, CLI argument, config schema or rollout format was changed in
G2. No new model-visible contextual fragment was introduced. The G1 sleep-router
changes were accepted previously and are unchanged, including switch precedence.

## Outcome-scoped logbook

- Exact replay and G1 preservation verified independently by this panel.
- Hosted workflow metadata's head SHA is the dispatch/base SHA, not the tested
  snapshot. Actual checkout logs and local snapshot tree identity establish the
  evidence link; treating the metadata head as the candidate would be wrong.
- Size counts corrected; the producer's two-stage suggestion still leaves an
  oversized second stage. No product code changed and no source task was written.
- Read-error and lease-race notes are unverified interleavings, not blocking
  findings. Follow-up work belongs to the orchestrator, not a hidden scope expansion.

```verdict-findings
{
  "findings": [],
  "notes": [
    {"id": "oversize-delivery-staging", "severity": "note", "text": "Cumulative CR is 1680 changed lines; G2 is 1385. Proposed ~225-line first stage leaves ~1160 lines. Keep G1 separate and stage hook groups with their tests for upstream delivery."},
    {"id": "dev-cycle-target-bound", "severity": "note", "text": "Core dev-dep on goal and goal normal-dep on core forms a package-level dev cycle, not a normal core-library cycle. Exact-tree hosted compilation passed."},
    {"id": "bazel-lock-evidence-bound", "severity": "note", "text": "Producer reports just bazel-lock-update exit 0 with no delta. Panel did not run Bazel; Cargo-only hosted success cannot prove Bazel lock freshness."},
    {"id": "accounting-read-error-window", "severity": "note", "text": "runtime.rs:775 may return a read failure before publisher reconciliation in progress-accounting paths. Not reproduced through a permitted public-entry test; investigate transient failure after the preceding successful reconcile."},
    {"id": "unbound-turn-start-lease", "severity": "note", "text": "runtime.rs:570 and extension.rs:254 share a thread-wide permit lease without submission identity. Overtaking user turn and disable/re-enable interleavings were not dynamically attacked here."},
    {"id": "execution-provenance", "severity": "note", "text": "Panel independently ran replay and static checks only; public-entry executions and mutation failures are reused hosted evidence. Workflow dispatch head is not the tested checkout; logs pin checkout 016a4248 and tree 4d289590."}
  ],
  "surface_results": [
    {"row": "goal activity publisher", "result": "held", "reason": "Exact candidate replay; static sweep of all seven section-4 transitions; reused and source-verified hosted public-entry attacks for all eight AC categories. No reproduced blocking finding. Held is bounded to the named attacks, not all schedules or read-error locations.", "evidence": "TASK-261002-3k97mc_panel-evidence.md; hosted run 37002709023; source task results and hosted-precheck-2 resources"}
  ],
  "free_hunt": []
}
```
