# R141 panel B — TASK-261005-3pxhfy

accept

CR-TASK-260929-4ut0up-1 revision 1; non-recording panel. Ready for review.

Replay: base `ea8899e6f97aea64136159286840c28c955243e8` plus the attached patch produced exactly `7de6b3c2ed82f07002c613263cd650cc16b20108`. Snapshot `9e692fdcd16a373a59f7d262159b377d588163d0` resolves to that same tree. No candidate code or task-under-review state was changed.

Review contract: one surface row, 7 AC rows, sequential static sweep, then bounded free hunt of publication/retention lock ordering and stdin-before-watcher ordering. Budget selected because brief gives none: 30 minutes total, 5 minutes free hunt; no serial prerequisite or build. One text outcome. Recommendation: accept under the executed-reproduction rule, with the two unconfirmed race notes retained for the recording reviewer. This is not proof that those races are safe.

## Commands and real exit codes

- Required start mutation on **this panel task**: exit 0.
- Tool readiness (`command -v task-board git rg`, `git --version`, `rg --version`, `task-board --help`): successful output; scratch logs under `.temp/TASK-261005-3pxhfy/`. Initial skill inventory returned exit 2 because `agents/` and `.claude/` are absent; `.codex/skills` was found. No workflow depended on the absent directories.
- `task-board resource get TASK-260929-4ut0up TASK-260929-4ut0up_change-request_rev1.patch --output .temp/TASK-260929-4ut0up_change-request_rev1.patch`: exit 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-3pxhfy-replay.idx" git read-tree ea8899e6f97aea64136159286840c28c955243e8`: exit 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-3pxhfy-replay.idx" git apply --cached .temp/TASK-260929-4ut0up_change-request_rev1.patch`: exit 0.
- `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-3pxhfy-replay.idx" git write-tree`: exit 0, expected tree above.
- Resource downloads of surface-table, producer-brief, results, mutants, hosted-precheck-2, CR validation log: exit 0.
- AC read `task-board q 'get(TASK-260929-4ut0up) { description scope ac }'`: exit 0. An initial combined query with unknown `resources` field failed exit 1; repaired with `outcomeResources`. `schema(Element)` returned an error object despite shell exit 0; not treated as success. Scoped `schema(operation="get")` succeeded exit 0. `resource list` only printed help and was not used as evidence.
- `git archive <candidate-tree> codex-rs/core/src/unified_exec` and `tar -xf ... -C ...`: exit 0 each. Static reads/diff and Git status: exit 0; worktree clean.
- `gh --version`: exit 0; `gh run view 37219783600 --repo relux-works/codex --json headSha,conclusion,jobs`: exit 0; `gh run view 37219783600 --repo relux-works/codex --log`: exit 0.
- `git rev-parse '9e692fdcd16a373a59f7d262159b377d588163d0^{tree}'`: exit 0, candidate tree.
- Python evidence assertions: exit 0; 4/4 lane logs checkout snapshot, 16/16 mutant records contain runtime core failures, named entry tests appear PASS. Python tool readiness: exit 0.
- No cargo, just, build, test or mutant execution run locally. Hosted lanes reused: snapshot success; mutant core failures are expected-red, not passing tests. Numeric hosted command exit codes are not present in the summary and are not invented.

## Sources and scope

- [Hosted snapshot run](https://github.com/relux-works/codex/actions/runs/37219783600): actual checkout ref verified in each lane. Workflow metadata `headSha` names the dispatch base, so it was not used as the checkout identity.
- Read-only task resources: `surface-table.md`, `producer-brief.md`, `TASK-260929-4ut0up_results.md`, `TASK-260929-4ut0up_mutants.json`, `TASK-260929-4ut0up_hosted-precheck-2.md`, `TASK-260929-4ut0up_change-request_rev1-validation.log`.
- Per-mutant runtime evidence: `/Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/p5/b2-precheck-2-results.json`; named runs and runtime failures below. Accepted attached execution evidence, not rerun by this panel.
- Candidate source citations below refer to Git tree `7de6b3c2ed82f07002c613263cd650cc16b20108`, paths under `codex-rs/core/src/unified_exec/`.

## Logbook

Replay identity verified. Hosted checkout identity independently verified despite dispatch headSha differing. AC4 attribution corrected. Two lock-order race suspicions preserved as nonblocking notes with exact requested hosted tests; no executed reproduction, so no blocking finding asserted. Nothing recorded on TASK-260929-4ut0up; only this panel task receives this text artifact and lifecycle mutations.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "stdin-before-publication-unconfirmed",
      "mechanism": "process_manager.rs:1043 holds the interaction lock throughout write_stdin; async_watcher.rs:191 acquires that lock before publication. receipt_hooks.rs:330-345 silently declines a stdin claim unless already Queued. Both existing stdin race tests await Queued before calling write_stdin (receipt_hooks_tests.rs:1236,1296). A poll already holding the interaction lock when the child exits may return terminal output and unbind before the watcher queues its completion.",
      "requested_attack": "Add terminal_stdin_before_watcher_publication_consumes_claim in receipt_hooks_tests.rs: launch opted-in process; begin write_stdin while alive, latch exit during the poll, allow poll to return before watcher lock acquisition; assert no later pushed completion. Run just test -p codex-core -E test(terminal_stdin_before_watcher_publication_consumes_claim) on exact candidate in hosted CI.",
      "status": "unconfirmed; not executed; nonblocking under reviewer reproduction rule"
    },
    {
      "id": "publication-retention-interleaving-unconfirmed",
      "mechanism": "async_watcher.rs:208-227 publishes under the receipt-store lock, then awaits output-buffer and hooks locks before insert_pending. acknowledge_pushed_completion (receipt_hooks.rs:312-323), release, inline settle and shutdown hold hooks lock but can run after publication and before insertion. Sampling may move no pending output, or cancellation may drop nothing, followed by late pending insertion. This may leave retained bytes outside capacity accounting or restore output after cancellation.",
      "requested_attack": "Add receipt_publication_retention_atomic_with_sampling_and_release in receipt_hooks_tests.rs: hold output_buffer lock, let watcher reach Queued, acknowledge a pushed lease or release/shutdown, then unlock buffer; assert sampled capacity is held or cancelled output is absent. Run just test -p codex-core -E test(receipt_publication_retention_atomic_with_sampling_and_release) on exact candidate in hosted CI.",
      "status": "unconfirmed; not executed; nonblocking under reviewer reproduction rule"
    },
    {
      "id": "evidence-bound",
      "text": "Hosted core command excludes three named unrelated zsh approval tests. It is not an unqualified full-suite pass. Local validation is bounded; terminal shard footer says required=4 green=4 failed=0 missing=0 and test_case_coverage=unknown. No local builds were run by this panel."
    },
    {
      "id": "ac4-killing-test-correction",
      "text": "ac4-capacity-counts-active-only was killed by new_reservation_retires_least_recently_sampled_output in run 37219891134, not receipt_capacity_refuses_65th_unsampled_reservation as the producer table states. Runtime kill exists; this is an attribution correction."
    }
  ],
  "surface_results": [
    {
      "row": "receipt hooks in unified exec",
      "result": "held",
      "reason": "Reused executed attacks on exact candidate snapshot: positive snapshot run 37219783600, all four lanes success; 16 narrowing mutants have core runtime failures. Static path sweep covered all 7 ACs; held applies only to the named attacks, not every possible interleaving.",
      "coverage": {
        "surface_rows": "1/1",
        "ac_rows_with_named_tests": "7/7",
        "runtime_mutants_killed": "16/16"
      },
      "attacks": [
        {
          "mutant": "ac1-publish-on-exit-token-before-drain",
          "run": "37219813126",
          "runtime_failures": [
            "new_reservation_retires_least_recently_sampled_output",
            "receipt_exit_publishes_only_after_drain_denial_and_classification",
            "retained_output_over_cap_keeps_head_tail_and_omitted_count",
            "retained_output_read_refuses_unknown_and_foreign_receipts",
            "retained_output_survives_process_entry_removal",
            "shutdown_cancels_all_receipts_and_frees_slots"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac1-failed-exit-reports-minus-one",
          "run": "37219798755",
          "runtime_failures": [
            "receipt_failed_exit_maps_to_failed_completion"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac1-timed-out-dropped-to-false",
          "run": "37219827165",
          "runtime_failures": [
            "receipt_exit_preserves_timed_out"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac2-success-inline-weakened-to-arm",
          "run": "37219852315",
          "runtime_failures": [
            "opted_in_exit_before_decision_returns_inline_and_frees_slot"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac2-capacity-refusal-proceeds-as-default",
          "run": "37219840746",
          "runtime_failures": [
            "opted_in_exec_refuses_65th_before_spawning"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac3-retention-cap-doubled",
          "run": "37219878306",
          "runtime_failures": [
            "retained_bytes_never_exceed_cap",
            "retained_output_over_cap_keeps_head_tail_and_omitted_count"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac3-omitted-count-subtracted",
          "run": "37219864294",
          "runtime_failures": [
            "retained_bytes_never_exceed_cap",
            "retained_output_over_cap_keeps_head_tail_and_omitted_count"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac4-retire-most-recently-sampled",
          "run": "37219903827",
          "runtime_failures": [
            "new_reservation_retires_least_recently_sampled_output",
            "pending_output_moves_to_sampled_and_retires_least_recently_sampled",
            "retention_drop_removes_output_in_every_state"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac4-capacity-counts-active-only",
          "run": "37219891134",
          "runtime_failures": [
            "new_reservation_retires_least_recently_sampled_output"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac5-stdin-claim-leases-without-acknowledge",
          "run": "37219915882",
          "runtime_failures": [
            "terminal_stdin_and_pushed_claims_race_exactly_once",
            "terminal_stdin_claim_consumes_the_single_claim_first"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac6-terminate-cancels-with-released",
          "run": "37219979093",
          "runtime_failures": [
            "terminate_process_cancels_before_killing"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac6-interrupt-cancels-with-released",
          "run": "37219929238",
          "runtime_failures": [
            "interrupt_cancels_before_signalling"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac6-shutdown-cancels-with-released",
          "run": "37219967266",
          "runtime_failures": [
            "shutdown_cancels_all_receipts_and_frees_slots"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac6-release-cancels-with-owner-stopped",
          "run": "37219942496",
          "runtime_failures": [
            "release_cancels_receipt_and_keeps_process_running",
            "release_frees_active_and_sampled_slots"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac6-release-leaks-retained-output",
          "run": "37219954998",
          "runtime_failures": [
            "opted_in_decision_before_exit_queues_exactly_one_completion",
            "release_frees_active_and_sampled_slots"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        },
        {
          "mutant": "ac7-default-launch-forced-opt-in",
          "run": "37219999698",
          "runtime_failures": [
            "default_launches_reserve_no_receipts"
          ],
          "core_result": "failure (expected-red; reused evidence, numeric process exit unavailable)"
        }
      ]
    }
  ],
  "free_hunt": []
}
```
