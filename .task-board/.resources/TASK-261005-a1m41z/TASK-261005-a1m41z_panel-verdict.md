# TASK-261005-a1m41z panel A verdict — CR-TASK-260929-1rcgsj-1 rev1

accept

Replay: **MATCH**. Base `47f7a80476eb78f27f7ce97c8bf7eb9236c40b47` plus the attached rev1 patch yields exactly candidate tree `37fad741767c46d11094adb9be747d5aae83c145`. Locally available hosted snapshot `f2bf01a5^{tree}` independently resolves to the same tree. No build, test, commit, branch operation, or mutation of TASK-260929-1rcgsj was performed.

Commands personally executed (standalone replay/gates, real exit codes):

| Command | Exit | Evidence |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261005-a1m41z, status=analysis)'` | 0 | This panel lifecycle only |
| `git --version`; `rg --version`; `python3 --version` | 0 each | Tool readiness logs in run-local .temp/TASK-261005-a1m41z |
| `git status --short` | 0 | Empty before and after review |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-a1m41z-replay.idx" git read-tree 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47` | 0 | Temporary index only |
| `task-board resource get TASK-260929-1rcgsj TASK-260929-1rcgsj_change-request_rev1.patch --output .temp/TASK-260929-1rcgsj_change-request_rev1.patch` | 0 | Read-only materialization |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-a1m41z-replay.idx" git apply --cached .temp/TASK-260929-1rcgsj_change-request_rev1.patch` | 0 | Patch replay |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-a1m41z-replay.idx" git write-tree` | 0 | 37fad741767c46d11094adb9be747d5aae83c145 |
| `git rev-parse 'f2bf01a5^{tree}'` | 0 | Same tree |
| `git diff --check 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47 37fad741767c46d11094adb9be747d5aae83c145` | 0 | No whitespace errors |
| `git diff --stat` / `git diff --numstat` with the same two OIDs | 0 each | 9 files, 1012 insertions, 6 deletions |
| `git grep -n 'lease_runtime_notifications\|enqueue_runtime_notification\|cancel_runtime_notification\|fail_runtime_lease\|acknowledge_runtime_lease' 37fad741767c46d11094adb9be747d5aae83c145 -- codex-rs/core` | 0 | Queue call-site audit |
| `task-board q 'get(TASK-260929-1rcgsj) { description scope ac }'` | 0 | Five AC rows read |
| `task-board q 'get(TASK-261005-a1m41z) { overview }'`; checklist projection; spawn directives | 0 each | Only own task/read-only run queries |

Artifact checks personally run: `python3 .temp/TASK-261005-a1m41z/write-verdict.py` exited 0; `python3 .temp/TASK-261005-a1m41z/validate-verdict.py` exited 0 (one JSON block, exactly 3 unique rows, valid verdict, empty findings/free hunt). The validator is run-local packaging tooling, not a Rust behavior test. Source file is in ignored run-local `.temp/` so it creates no managed repository delta; board attachment is the durable outcome.

Source/evidence reads (`cat`, pinned `git show`, bounded `sed`, `rg`) succeeded; they were inspection, not execution of the Rust behavior. Discovery mistakes are not green gates: queries using unknown `resources` and `artifacts` fields exited 1; `schema(get)` exited 2; corrected `schema(operation="get")` exited 0. Search of nonexistent board `/resources` exited 2; corrected `.resources` search exited 0. Global skill search returned 1 (no matching files); relevant role references were subsequently found under ~/.agents/skills/project-management. `task-board resource list` printed help, so it is not treated as a resource inventory. Initial skill catalog probe reported missing agents/skills and .claude/skills; .codex/skills was read successfully.

Accepted execution evidence, **not rerun by this panel**: [hosted precheck 1](../TASK-260929-1rcgsj/TASK-260929-1rcgsj_hosted-precheck-1.md), candidate snapshot run `37278001051` (lint/small/core/app-server success), plus the ten expected-red mutant runs listed below. The attached precheck records lane results but no numeric per-command exits, so those exits are **unknown**, not invented as 0/1. Mutant runs are failures as expected, not passing gates. The local rev1 validation log records exit 0 for target guard, fmt-check and clippy, plus visible small-lane commands; its known 64-KiB truncation prevents attesting anything beyond the visible records. Hosted exact-tree evidence is used for the missing local tail.

Review contract/budget: one non-recording decision for this CR revision; immutable patch/base/tree is the frozen precondition; 30-minute self-imposed review ceiling (brief supplies no numeric budget), bounded free hunt of at most five minutes, one plain-text outcome, no serial research prerequisites. Exit criterion: replay plus three row results plus verdict. Consumer: recording reviewer, then owning C1/C2 implementation tasks. Broad future harness research is excluded.

Sources: read-only board resources [surface table](../TASK-260929-1rcgsj/surface-table.md), [producer results](../TASK-260929-1rcgsj/TASK-260929-1rcgsj_results.md), [mutant patches](../TASK-260929-1rcgsj/TASK-260929-1rcgsj_mutants.json), [plan §5.2 / stage 2b](../TASK-260929-1rcgsj/final-plan.md), and exact-tree code paths cited in JSON. Plan is context; the task's explicit C2/D exclusions bound this review. Repository supports Linux/macOS/Windows and foreign exec hosts; local platform is macOS, but no execution lane was used.

Free hunt: audited external API/config/rollout changes (none), model-visible injection (none added), unchanged inter-agent drain/settings precedence, token ownership at wake, busy-thread scheduling, test-support API, and actual diff size. No additional reproduced blocker. Notes below do not claim behavioral proof or absence of defects.

Logbook entry, 2026-10-05, panel A: replay and hosted snapshot agree. Inactive-stage lease-token loss and two-entry observability limit are carried forward explicitly; do not reuse these tests as sampled-delivery proof during activation. Diff size exceeds guidance. This task-scoped outcome carries the entry; no control-root file or original-task note was edited.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "N1-staged-lease-carrier",
      "row": "runtime mailbox lease lifecycle",
      "text": "tasks/mod.rs:487 leases entries but only tests vector emptiness at :499; tokens are not retained in TurnState or passed to start_task. input_queue.rs:273 drain stays inter-agent-only. The producer explicitly states this C1 bound in results Bounds 4: C2 supplies TurnInput carrier, D supplies sampling acknowledgement, E supplies production enqueue/cancel. Do not treat this leaf as proof of sampled delivery, failed-transport retry, or receipt-store cancellation propagation. No external production enqueue exists at this tree: git grep locates only the public test hook and tests. Before activation, require a real submitted-prompt test, token retention through interruption/compaction, and receipt cancellation wiring. This is a stated inactive-stage bound, not a reproduced in-contract transport defect."
    },
    {
      "id": "N2-two-entry-observability",
      "row": "idle wake",
      "text": "core/tests/suite/runtime_mailbox.rs:126-140 calls the helper twice, and each helper invokes maybe_start immediately (codex_thread.rs:389). First call leases before returning. Thus the test does not deterministically queue two receipts before a single drain, nor inspect both receipt IDs in the same turn. The pending-admits-leased mutant is killed by queue units, not by this suite test according to hosted precheck. Requested next attack: a barrier-controlled two-receipt enqueue-before-wake fixture and a mutant that leases only the first eligible entry. Run just test -p codex-core runtime_mailbox on hosted CI. Not executed here; no behavioral failure asserted."
    },
    {
      "id": "N3-change-size",
      "row": "free hunt",
      "text": "git diff --numstat reports 1012 insertions plus 6 deletions, 1018 changed lines. This exceeds the 800-line guidance; roughly 365 changed production lines are below the preferred 500-line logic limit. A smaller coherent split would isolate RuntimeMailbox + sibling tests, then InputQueue/query/wake integration + integration tests. Do not claim size compliance merely because logic is small."
    },
    {
      "id": "N4-coverage-bounds",
      "row": "free hunt",
      "text": "3/3 surface rows have named hosted attacks; 10/10 supplied mutants are reported killed. These ratios describe the supplied catalog, not all schedules or all gates. Hosted evidence gives lane conclusions and killing test names, not individual process exit numbers. Quota object does not exist at this stage; no new user input is verified, quota non-reset is a construction argument. Public doc-hidden test hook increases CodexThread API surface and should stay test-support-only when a real enqueue path replaces it."
    }
  ],
  "surface_results": [
    {
      "row": "runtime mailbox lease lifecycle",
      "result": "held",
      "attacks": [
        "Hosted run 37278001051: InputQueue drain/lease/ack, fail/retry/stale-token, mixed-mail and cancel tests; RuntimeMailbox duplicate/double-ack tests.",
        "Narrowing mutants: stale ack 37278019338, leased cancellation 37278038094, duplicate enqueue 37278056447, stale fail 37278078920, leased re-admission 37278122457, pending leased 37278142989."
      ],
      "reason": "No reproduced failure at the queue API boundary. Static inspection confirms FIFO leasing, UUID token comparison, removal by receipt, and unchanged inter-agent drain. Sampling delivery and production receipt cancellation remain explicitly deferred; see N1."
    },
    {
      "row": "trigger and suspension semantics",
      "result": "held",
      "attacks": [
        "Hosted run 37278001051: runtime_entry_suppresses_automatic_goal_continuation; suspended_runtime_entry_does_not_block_start_if_idle; runtime_suspended_while_leased_stops_suppressing.",
        "Suspension mutants 37278101178 and 37278163468 fail named core tests."
      ],
      "reason": "Static call-path attack: turn_input.rs:395 and :449 both consult the extended trigger query; tasks/lifecycle.rs:71 consults the same query. RuntimeMailbox::has_trigger includes live leased entries and excludes suspended ones; lease_available and has_pending exclude suspended entries. Mixed entries are existentially selected, not first-entry selected. No reproduced failure."
    },
    {
      "row": "idle wake",
      "result": "held",
      "attacks": [
        "Hosted run 37278001051: pending_runtime_entry_starts_one_wake_turn_with_exec_completion; two_runtime_entries_still_start_one_wake_turn; queue_only_inter_agent_mail_still_never_starts_a_turn_alone.",
        "Wake trigger mutant 37278203959 and fake-agent-mail mutant 37278183811 fail the public CodexThread injection suite tests."
      ],
      "reason": "Public test hook calls real maybe_start_turn_for_pending_work. Static busy-path attack finds active_turn reservation before leasing; the busy return leaves entries unleased. Non-trigger mail alone requires durable sleep; trigger inter-agent mail retains precedence/settings. Runtime-only wake uses current default thread settings plus preserved cyber access, sets exec_completion, and creates no UserInput or agent lineage. Hosted two-entry result is accepted as bounded request-count evidence, not proof both receipts entered that wake; see N2."
    }
  ],
  "free_hunt": []
}
```
