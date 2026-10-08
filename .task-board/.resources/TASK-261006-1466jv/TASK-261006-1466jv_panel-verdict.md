# TASK-261006-1466jv — R141 panel A, revision 2

accept

Replay check: **MATCH**. Base `4a27941d383ba8cdc2575bafdfeeef497b402a25` plus `TASK-260929-csnn3a_change-request_rev2.patch` yields exactly `f0cf63cd9fc511340d23e680f43e846403157f62`. Reviewed candidate blobs, not the worktree HEAD. Non-recording panel; no mutation, note, outcome, status or verdict was written to TASK-260929-csnn3a.

Plan: decide whether CR-TASK-260929-csnn3a-2 can be accepted; frozen input is the supplied patch/base/tree (no new grammar); budget 30 minutes including packaging, one text outcome, no serial research prerequisites. Consuming slice is the recording review of D2. Exit: replay match, 3/3 rows classified, bounded static free hunt, schema-valid verdict attached. No builds, cargo or just commands run locally.

Commands executed directly (exit codes are real; retrieval is not execution of tests):

| Command | Exit | Result |
|---|---:|---|
| `task-board m 'set_status(TASK-261006-1466jv, status=analysis)'` | 0 | Panel lifecycle only |
| `task-board resource get TASK-260929-csnn3a TASK-260929-csnn3a_change-request_rev2.patch --output .temp/TASK-260929-csnn3a_change-request_rev2.patch` | 0 | Patch materialized |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-1466jv-replay.idx" git read-tree 4a27941d383ba8cdc2575bafdfeeef497b402a25` | 0 | Temporary index initialized |
| Same temporary index: `git apply --cached .temp/TASK-260929-csnn3a_change-request_rev2.patch` | 0 | Patch applied only to index |
| Same temporary index: `git write-tree` | 0 | Exact expected tree |
| `git diff --check 4a27941d383ba8cdc2575bafdfeeef497b402a25 f0cf63cd9fc511340d23e680f43e846403157f62` | 0 | Whitespace check |
| `git rev-parse '53c4e843^{tree}'` | 0 | Exact candidate tree |
| `git archive --format=tar --output=.temp/TASK-261006-1466jv/candidate.tar f0cf63cd9fc511340d23e680f43e846403157f62 <scoped core paths>`; `tar -xf ... -C .temp/TASK-261006-1466jv/candidate` | 0 each | Candidate source inspection; archive never attached |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261006-1466jv-mutants.idx" git read-tree f0cf63cd9fc511340d23e680f43e846403157f62` | 0 | Separate mutation-check index |
| `git apply --cached --check .temp/TASK-261006-1466jv/<mutant>.patch`, with the mutation-check index | 0 each, 9/9 | All raw attached patches apply, including final-LF repairs |
| `gh run view 37441567186 --repo relux-works/codex --json headSha,conclusion,jobs,url` | 0 | Four lanes success |
| `gh run view <run> --repo relux-works/codex --log`, baseline and each of the nine rows below | 0 each, 10/10 | Raw hosted logs retrieved |
| `python3` progress/log-extraction/document generation | 0 each | Structured evidence, no product execution |
| `task-board q 'get(TASK-260929-csnn3a) { description scope ac notes }'`; own checklist query; spawn directives reads | 0 each | Read-only context; no directives |

Artifact validation: Python JSON/row/verdict assertions and git status check exited 0: exactly one verdict-findings block, 3/3 unique held rows, one-word accept verdict, no blocking findings, clean tracked/untracked repository status. No product source modified.

Auxiliary recovery failures (not gates): initial skill inventory `rg` exits 2 for missing directories; two projections using unsupported `resources` exit 1; positional `schema(element)` exits 1. A `cat` of the stale reviewer-role link failed and the incorrect `git show ...:codex-rs/core/src/review_session.rs` lookup failed (Git fatal; combined read call's last command exited 0, so it does **not** establish success of that lookup). Both reads were corrected. Git/rg/Python/gh readiness produced expected versions; scratch evidence lives in `.temp/TASK-261006-1466jv/`.

Evidence fact-check: [baseline hosted run](https://github.com/relux-works/codex/actions/runs/37441567186). Its dispatch `headSha` is the base; its actual checkout is snapshot `53c4e8435e251ce090b24b5875a4a5e16bd77d0c`, tree verified locally equal to replay. Raw logs confirm each named baseline attack PASS. Baseline summaries: core 4999 passed/11 skipped; app-server 1829 passed/2 skipped; small 260 passed/0 skipped; lint success. Core command reused, never executed locally:

`INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-core -E 'not ( test(=suite::skill_approval::shell_zsh_fork_skill_scripts_ignore_declared_permissions) | test(=suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_guardian_reviews_persistent_terminal_in_current_turn) | test(=suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_parent_approval_preserves_denied_reads))'`

Every mutant uses that hosted command. These are **failing expected-red gates**, exit **100**, not passes: the named narrowed behavior must fail its regression test. Nine kills, zero survivors among the nine supplied mutants. Apply-checks prove portability only, not mutant kills.

| Mutant | Hosted evidence | Terminal killing tests (exec_completion prefix omitted) | Test exit |
|---|---|---|---:|
| `ack_skipped_when_websockets_enabled` | [run 37441591474](https://github.com/relux-works/codex/actions/runs/37441591474) | exec_completion_sampling_ack, http_fallback_submission_acknowledges, websocket_submission_acknowledges | 100 |
| `acknowledge_on_recording` | [run 37441615109](https://github.com/relux-works/codex/actions/runs/37441615109) | aborted_submission_retries_and_samples_once, exec_completion_finishing_task_gets_sampling_wake, exec_completion_sampling_ack, failed_submission_retries_once_without_second_history_append, persistent_failures_suspend_visibly_without_spin | 100 |
| `backoff_skips_post_failback_rewake` | [run 37441638357](https://github.com/relux-works/codex/actions/runs/37441638357) | exec_completion_lost_reservation_after_winner_idle_rewakes | 100 |
| `compact_acks_staged` | [run 37441663087](https://github.com/relux-works/codex/actions/runs/37441663087) | exec_completion_compaction_omission_keeps_receipt_pending | 100 |
| `fail_first_tracked_only` | [run 37441688497](https://github.com/relux-works/codex/actions/runs/37441688497) | exec_completion_finishing_task_gets_sampling_wake | 100 |
| `guardian_prep_drops_exec_fragments` | [run 37441714373](https://github.com/relux-works/codex/actions/runs/37441714373) | exec_completion_guardian_prompt_preserves_receipt | 100 |
| `reserved_claim_ignores_identity` | [run 37441739252](https://github.com/relux-works/codex/actions/runs/37441739252) | tasks::tests::reserved_start_backs_off_when_turn_replaced | 100 |
| `reserved_claim_ignores_task` | [run 37441762646](https://github.com/relux-works/codex/actions/runs/37441762646) | tasks::tests::reserved_start_backs_off_when_turn_busy | 100 |
| `retain_only_task_present` | [run 37441786360](https://github.com/relux-works/codex/actions/runs/37441786360) | exec_completion_survives_cleared_idle_reservation | 100 |

Static sweep: F1a recovery serializes on active_turn; stale lease-token failures are no-ops; suspended entries do not count as pending and cannot spin the re-wake. F1b recording at hook_runtime.rs:785 tracks rather than acknowledges, and tasks/mod.rs:836 fails unsubmitted before idle scheduling. The submitted prompt is checked at session/turn.rs:2676-2678 against trusted exact fragment text; fallback follows the actual response stream, not WebSocket configuration. Guardian source citations and test-scope bounds are retained below.

Free hunt: bounded static examination of between-claim replacement, repeated fail-back/token staleness, active-winner double-wake, suspended-entry termination, test gate effects, transport membership, API/config/rollout compatibility, and full CR size. No additional reproduced blocking mechanism; `free_hunt` is empty. The between-claim suspicion remains a note with a proposed concrete attack, not a finding. Held means these named attacks held, not proof of absence. Row outcomes were persisted incrementally in review-progress.json.

Logbook entry (task-scoped, no control-root edit): revision 2 closes R141-A-1 with an exact-tree baseline pass and narrowing-mutant kill. Raw hosted verification also establishes that the dispatch SHA is not the checkout SHA. All nine raw mutant patches now apply without newline normalization. Guardian omission and literal F1b leftovers remain explicit coverage bounds. Only this panel task receives board writes.

References read: source-task `surface-table.md`, `producer-brief.md`, `TASK-260929-csnn3a_results.md`, `TASK-260929-csnn3a_mutants.json`, `TASK-260929-csnn3a_hosted-precheck-3.md`, `TASK-260929-csnn3a_review-verdict-rev1.md`, and candidate paths pinned to the tree above. No primary-goal mutation or recording-review operation performed.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "rev1-fix-verified",
      "text": "R141-A-1 is addressed: tasks/mod.rs:642-652 fails leases then schedules a new pass; the exact-tree hosted baseline passes exec_completion_lost_reservation_after_winner_idle_rewakes and the narrowing mutant 37441638357 fails only that test (exit 100). No local execution of Rust tests."
    },
    {
      "id": "guardian-bound",
      "text": "Held uses preservation, not literal omission: guardian/request_budget.rs:67-174 extends prompt.input or returns an error, never removes existing fragments. guardian/input_budget.rs:81-98 accepts only a single UserInput when PendingReviewContext exists. guardian/review_session.rs:677,711,739 installs/removes that context on the private review session. The supplied surface table explicitly permits this source-cited bound."
    },
    {
      "id": "f1b-literal-gap",
      "text": "exec_completion_finishing_task_gets_sampling_wake drives failed submission of two recorded leases, teardown fail-back, autonomous retry and two-item history dedup. It does not force literal unrecorded leftover input at task finish. Keep this as a coverage bound; no failing candidate reproduction established."
    },
    {
      "id": "mid-start-claim-gap",
      "text": "Unexecuted suspicion retained from rev1: tasks/mod.rs:364-391 checks the reservation, releases active_turn, mutates plugin selection and turn state, awaits BeforeTaskRegistration, then checks again. Replacement between checks can leave intermediate effects. The new test pauses before the first claim and does not cover this interval. Requested attack: a latch contributor at BeforeTaskRegistration, real exec wake, replace/interrupt while latched, release, assert winner plugin state, balanced lifecycle and eventual sampling with no duplicate. Suggested test exec_completion_reserved_start_replaced_between_claims in core/tests/suite/exec_completion.rs; command just test -p codex-core -E test(exec_completion_reserved_start_replaced_between_claims), not run. No blocking finding inferred."
    },
    {
      "id": "review-size",
      "text": "Full CR versus supplied base is 16 paths +2727/-44, including inherited D1; rev2 delta over 3e3f73576ad3ed852711023df46ad5bd2dccda6c is 4 paths +223/-0. Preserve staged boundaries: acknowledgment/tracking/retry plus D1 tests first, TurnStartClaim plus D2 regression suite next, then post-back-off re-wake plus this new public-entry test. No new wire/schema/config/CLI changes found."
    },
    {
      "id": "test-api-surface",
      "text": "TestWakeLeaseGate and arm/disarm hooks add public hidden test API and production hook checks (codex_thread.rs:229-272,507-535; tasks/mod.rs:557,1030). They are inert without an explicitly inserted gate; no observed production failure. Consider consolidating with existing test-support APIs in a later cleanup; do not treat doc(hidden) as an access restriction."
    },
    {
      "id": "hosted-evidence-bound",
      "text": "Actual workflow dispatch headSha is the base, not the test checkout. Raw checkout logs pin 53c4e8435e251ce090b24b5875a4a5e16bd77d0c in all four jobs; its Git tree is the exact candidate. Core lane runs 4999 tests, 11 skipped and three explicitly excluded zsh tests. All named panel attacks ran. Mutant runs may contain transient failures that pass on retry; only terminal TRY 3 failures below are counted. acknowledge_on_recording has five terminal exec-completion failures (the attachment lists three), including failed_submission_retries_once_without_second_history_append and persistent_failures_suspend_visibly_without_spin."
    },
    {
      "id": "readiness-and-storage",
      "text": "Missing agents/skills and .claude/skills make the initial multi-path rg exit 2; available .codex skills were read. The project-management skill link to its reviewer role is stale; the role body was read from /Users/iv/.agents/skills/project-management/.roles/reviewer/role.md. Unknown resources field queries exited 1 and were recovered with direct read-only resource inventory. Initial review_session lookup omitted guardian/ and failed; corrected candidate path was read successfully. Artifact staged in ignored run-worktree .temp to obey the explicit run write boundary; only resource CRUD writes to the control root."
    }
  ],
  "surface_results": [
    {
      "row": "F1a cleared reservation",
      "result": "held",
      "evidence": "Exact-tree hosted baseline + retain_only_task_present 37441786360, reserved_claim_ignores_identity 37441739252, reserved_claim_ignores_task 37441762646 and backoff_skips_post_failback_rewake 37441638357. New latches force winner idle before fail-back; tasks/mod.rs:642-652 schedules after lease failure, active turn/pending checks serialize recovery."
    },
    {
      "row": "F1b finishing task",
      "result": "held",
      "evidence": "Hosted baseline PASS of exec_completion_finishing_task_gets_sampling_wake, plus acknowledge_on_recording (37441615109) and fail_first_tracked_only (37441688497), both real test commands exit 100. Failed request records two fragments; later request resubmits two; history remains two; fail_unsubmitted precedes teardown scheduler (tasks/mod.rs:837-839). Bound: literal leftover-at-finish shape not forced."
    },
    {
      "row": "compaction, guardian and transport",
      "result": "held",
      "evidence": "Hosted exact-tree baseline PASS for compaction, guardian preservation, sampling_ack and persistent_failures_suspend_visibly_without_spin; narrowing mutants compact_acks_staged 37441663087, guardian_prep_drops_exec_fragments 37441714373 and ack_skipped_when_websockets_enabled 37441591474 exit 100. Compaction request omits staged fragment and later wake contains it; transport failure leaves pending and HTTP fallback acceptance clears it, history count one. Guardian preservation bound is source-cited, not an executed literal omission."
    }
  ],
  "free_hunt": []
}
```
