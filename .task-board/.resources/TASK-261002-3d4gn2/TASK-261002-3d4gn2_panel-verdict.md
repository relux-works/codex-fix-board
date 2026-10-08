# TASK-261002-3d4gn2 — R141 panel B, receipt-state-machine rev4

accept

This is the non-recording static-panel recommendation for `CR-TASK-260929-u2i5rr-4`, not CR acceptance, integration, or hosted-CI certification. Nothing was written on TASK-260929-u2i5rr. No product files were modified. No builds or tests were launched.

## Replay identity

Base: `0462dcc062b822bb8fff16cc31ce6eeab69823b9`.
Expected candidate: `e9a8095f146dd156b09351cc2af473781aa37272`.
Observed `git write-tree`: `e9a8095f146dd156b09351cc2af473781aa37272` — exact match.
A second temporary-index replay of revision 2 produced the same tree, independently verifying unchanged-candidate reuse. Neither replay used a nested worktree or touched the real index.

Candidate blob SHA-256:

- completion_receipt.rs: `0bb4312c83c60758045bd34dc5dab69c3bd28832b4544eec082751bb88716981`
- completion_receipt_tests.rs: `efa40ae812e1b2a44a3373e6d6ea38cc3083f1ffce4051022182d715ad50ace5`

## Commands I ran and observed exits

All paths below are relative to the assigned Story worktree unless absolute. `BASE` and `TREE` denote the exact OIDs above. `RES` denotes `/Users/iv/Developer/IV/codex-fix-board/.task-board/.resources/TASK-260929-u2i5rr`. Each replay command ran as a standalone process; there were no tee pipelines or hidden gate statuses.

| Command | Exit | Observation |
|---|---:|---|
| `task-board m 'set_status(TASK-261002-3d4gn2, status=analysis)'` | 0 | Only panel task lifecycle changed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3d4gn2-replay.idx" git read-tree BASE` | 0 | Base loaded |
| `task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_change-request_rev4.patch --output .temp/TASK-260929-u2i5rr_change-request_rev4.patch` | 0 | Patch retrieved read-only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3d4gn2-replay.idx" git apply --cached .temp/TASK-260929-u2i5rr_change-request_rev4.patch` | 0 | Applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3d4gn2-replay.idx" git write-tree` | 0 | Exact candidate tree above |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3d4gn2-rev2.idx" git read-tree BASE` | 0 | Independent reuse check |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3d4gn2-rev2.idx" git apply --cached RES/TASK-260929-u2i5rr_change-request_rev2.patch` | 0 | Applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3d4gn2-rev2.idx" git write-tree` | 0 | Same candidate tree |
| `git diff --check BASE TREE` | 0 | No whitespace errors |
| `git diff --stat BASE TREE` and scoped diff of module export/three imports | 0 | Six paths reviewed |
| `git show TREE:codex-rs/core/src/unified_exec/completion_receipt.rs` and sibling tests | 0 each | Exact blobs inspected and copied only to task scratch |
| `git grep -n -E 'CompletionReceiptStore\|completion_receipt' TREE -- codex-rs/core/src ':!codex-rs/core/src/unified_exec/completion_receipt*'` | 0 | Only module export remains outside implementation/tests |
| `task-board q 'get(TASK-260929-u2i5rr) { description scope ac }'` | 0 | AC/description inspected |
| `task-board resource get TASK-260929-u2i5rr TASK-260929-u2i5rr_change-request_rev4-validation.log --output .temp/TASK-261002-3d4gn2/rev4-validation.log` | 0 | CR gate log read |
| Python tarfile inspection of `RES/TASK-260929-u2i5rr_validation-logs.tar.gz` | 0 | Index, baseline summary, all nine mutant failure tails inspected, no extraction outside scratch |
| Python hashlib/re source inspection | 0 | Both hashes above; 17 test names; all three removed import identifiers have zero remaining exact uses |
| `git status --short` (initial and after static review) | 0 each | Empty tracked/untracked report; only ignored scratch generated |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0 | No directives; run not goal-bound |
| `task-board q 'get(TASK-261002-3d4gn2) { checklist }'` | 0 | Panel-only checklist read |

Exploratory failures are not successful gates: the initial projection containing unsupported `resources` returned exit 1; the narrower supported query above succeeded. The initially advertised reviewer-role file under `/Users/iv/.claude/skills/project-management/.roles/` was missing; that combined read/skill-discovery call exited 2. The role contract was subsequently located and successfully read at `/Users/iv/.agents/skills/project-management/.roles/reviewer/role.md` (exit 0). `task-board resource list` returned CLI help with exit 0, not a resource listing; actual directory inspection and resource get supplied the evidence. Tool readiness versions were stored in `.temp/TASK-261002-3d4gn2/tool-readiness.log`.

## Evidence accepted from attachments, not rerun

The CR revision 4 validation log has four command records, each ending `[exit 0]`, and ends with `coverage_unit=exact_command_shard required=4 green=4 failed=0 missing=0 test_case_coverage=unknown`:

1. `/Users/iv/Developer/IV/codex/.temp/goal-token-burn/impl/codex-target-guard.sh` — exit 0.
2. `cd codex-rs && just fmt-check` — exit 0.
3. `cd codex-rs && just clippy -p codex-tools -p codex-core -p codex-goal-extension -p codex-extension-api -p codex-app-server -p codex-rollout-trace` — exit 0.
4. `cd codex-rs && NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no INSTA_WORKSPACE_ROOT=$PWD just test -p codex-tools -p codex-goal-extension -p codex-extension-api -p codex-rollout-trace` — exit 0, 218 passed, 0 skipped.

The archived revision 2 validation index reports `NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-core -E 'test(completion_receipt)'` exit 0. Its attached log ends with 17 passed, 4881 skipped. Source/test byte identity is verified above; this is historical execution evidence, not a fresh environment-equivalence or hosted-CI claim.

Nine archived isolated `cargo test --offline` mutant runs each report exit **101**, expected red, and their log tails contain the named assertion failure: M1/M2 foreign owner resolve/lease; M4 stale failed lease; M5 stale acknowledgement; M6 replacement of an active claim; M7 duplicate Reserved exit; M9 capacity widened to 65; M10/M11 foreign-owner fail/acknowledge. These are failing mutant runs, not passing tests. The index also discloses an earlier dependency-resolution attempt with exit 101 and no tests run; that attempt supplies no behavioral evidence.

The hosted-CI rev4 artifact was absent at the successful resource-directory inspection. No hosted result is inferred from the absence. The recording reviewer must obtain the exact-candidate hosted result before recording acceptance, as the panel brief requires.

## Surface sweep and F1–F3 closure

Coverage: **1/1 surface rows, 6/6 AC rows statically mapped**. Runtime execution in this panel: **0 tests**. Reused executed store-API attacks: **17 tests**, with nine expected-red mutant logs.

All source citations refer to the exact candidate tree above under `codex-rs/core/src/unified_exec/`.

| AC | Static attack and driving evidence | Conclusion |
|---|---|---|
| 1 | Happy path and repeated lease after sampling: tests lines 70, 110; `acknowledge_sampled` line 464 retires under the same lock | One claim, subsequent lease refused |
| 2 | Exit before InlineResult; exit before Arm; Arm before exit, using barriers: test line 128; resolve line 302 and publish line 375 use the same mutex | Early exit retained; InlineResult cannot generate a queued claim |
| 3 | Fail/release/re-lease with the old token: tests lines 299 and 331; fail line 441 checks token and source before requeue | Stale fail cannot revoke the live lease; stale ack refused |
| 4 | Reserved/Armed/Queued/Leased cancellation: test line 363; cancel line 492 and retire line 251 remove active entry while retaining reason | Unsampled states retire; future claim refused |
| 5 | 64 reservations, rejected 65th, cancel/reuse: test line 453; reserve line 274 checks active count before inserting | Capacity enforced within store; before-launch integration is explicitly deferred |
| 6 | Sequential competing sources and concurrent two-barrier race: tests lines 594, 623; lease line 404 serializes on one phase | Competing sources cannot obtain independent claims |

F1: tests at lines 523 and 560 separately attack thread, runtime-generation and call mismatches. The resolve/lease assertions exercise those exact entry points and preserve Reserved/Queued state. The fail/ack test constructs a foreign-owner lease inside the child test module while retaining the genuine token, so it isolates the owner check. This is a deliberately adversarial internal fixture; production lease fields remain private.

F2: test at line 331 fails an old lease, obtains a new lease, calls fail on the old lease, asserts StaleLease and the still-leased state, then acknowledges the current lease. Removing only token equality permits the wrong requeue and violates the assertion.

F3: test at line 724 publishes distinct first/second exit values while Reserved, demands InvalidTransition on the second publish, then verifies the first value survives both InlineResult and queued/acknowledged branches. Removing only the stored-is-none condition violates the refusal and retained value.

Other attacks traced: duplicate Queued publication, cancel followed by ack, repeated terminal operations, foreign-owner status/publish/cancel, private claim construction, bounded call ID, poisoned mutex returning LockPoisoned (test line 812), and bounded terminal history. No behavioral defect was reproduced or established statically.

## Bounded free hunt and logbook

After recording the surface result on this panel task, the bounded free hunt inspected the three extra import removals, terminal-history reuse/eviction, private token ownership, scope/caller reachability, source size and validation provenance. No additional blocking mechanism emerged. The extra import removals have no remaining exact identifier use in the corresponding candidate files. The implementation adds no model-visible fragment or external API/config/rollout surface.

Logbook entry, 2026-10-02: replay exactly matches the candidate and independently matches revision 2; F1–F3 have targeted refusal assertions and archived expected-red evidence; hosted CI remains unknown here; extra import/size observations are nonblocking notes. Persisted on the panel outcome and panel notes only, with no direct control-root/logbook edit and no original-task mutation.

Research boundary: decide this one static panel verdict; frozen base/candidate above; 25-minute worker ceiling, 3-minute maximum free hunt, one outcome under 30 KiB, zero serial prerequisite. Consumer is the recording reviewer for B1; B2 remains the next integration slice. No new grammar or implementation decision is introduced.

## Sources

- Read-only original-task AC, description and scope query recorded above.
- `RES/surface-table.md`, `RES/final-plan.md` sections 5.1 and 5.4, and producer brief (context).
- `RES/TASK-260929-u2i5rr_results.md`, `RES/TASK-260929-u2i5rr_coverage-map.md`, `RES/TASK-260929-u2i5rr_review-verdict-rev1.md`.
- Exact candidate Git blobs and both replayed CR patch resources.
- Retrieved revision 4 validation log and attached revision 2 validation archive identified above.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "execution-bound",
      "text": "Panel B ran replay and static checks only, as explicitly required. Reused executed attacks are identified below; no cargo, just, build, test, or mutant was executed in this panel. The hosted-ci-rev4 artifact was absent at the successful directory inspection. Current hosted execution remains unknown and is a required recording-reviewer gate, not a passing result inferred from local lint."
    },
    {
      "id": "inactive-api-bound",
      "text": "The candidate exports the module but has no runtime callers outside its tests. This is explicitly required by the B1 description; launch-before-reserve, process watchers, mailbox delivery and sampling integration belong to B2/later leaves. Public entry point here means the crate-visible CompletionReceiptStore API."
    },
    {
      "id": "retention-bound",
      "text": "Terminal history evicts its oldest entry at 64; old handles return UnknownReceipt. Reserved slots require caller cancellation if no decision arrives. Neither bounded history nor caller-driven cleanup proves eventual completion for an abandoned reservation."
    },
    {
      "id": "scope-and-size",
      "text": "The six-path patch includes three unused-import removals outside the declared three-path scope; no remaining exact identifier use exists in any affected file. The overall diff is 1367 insertions and 3 deletions, above repository review-size guidance. Implementation is 532 physical lines before cfg(test), or 466 nonblank/noncomment lines; producer reports 468 using a different count. These are scope/maintainability notes, not reproduced behavior defects."
    }
  ],
  "surface_results": [
    {
      "row": "concurrency state machine",
      "result": "held",
      "reason": "Static adversarial sweep plus explicitly reused executed attacks through CompletionReceiptStore; 1/1 surface rows and 6/6 AC rows mapped. Single mutex linearizes exit/decision, cancellation and competing leases. Owner checks cover every externally usable operation; retry preserves completion and binds owner/token/source. Four F1-F3 regression tests assert the actual refusals and retained state. Archived baseline is 17/17 passed and nine named mutants fail. Held is limited to these attacks, not proof of absence or newly executed runtime coverage.",
      "evidence": [
        "candidate completion_receipt.rs:251-529",
        "candidate completion_receipt_tests.rs:70-831",
        "TASK-260929-u2i5rr_validation-logs.tar.gz:validation-index.md, core-tests-01.log, mutant-M*.log",
        "TASK-260929-u2i5rr_change-request_rev4-validation.log"
      ]
    }
  ],
  "free_hunt": []
}
```
