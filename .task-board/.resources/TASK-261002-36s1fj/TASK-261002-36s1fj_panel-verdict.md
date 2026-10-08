# R141 panel A — goal-activity publisher, CR revision 1

changes_requested

## Identity, scope and replay

Non-recording panel for `CR-TASK-260929-2gp04j-1`; outcome belongs only to
`TASK-261002-36s1fj`. No mutation, acceptance, rejection, status change or
handoff was made on `TASK-260929-2gp04j`. No repository source was changed,
no build/test was launched, and no branch, commit or nested worktree was created.
Scratch artifacts were written inside the run worktree; the board CLI copies
the outcome into its managed resource storage outside that worktree. No direct
control-root writes were made.

Replay used a fresh alternate index, `.temp/TASK-261002-36s1fj-replay-v1.idx`.
Base: `ea8899e6f97aea64136159286840c28c955243e8`.
Patch: `TASK-260929-2gp04j_change-request_rev1.patch`.
`git write-tree` returned **`4d289590739432aa55c2a3868c2b4a5472b07c92`**, exactly
the expected candidate. The accepted G1 implementation and coverage paths
(`core/src/tools/spec_plan.rs`, `core/tests/suite/current_time_reminder.rs`,
and `ext/extension-api/**`) are byte-identical to checkpoint
`58042581a0b507ae62e7b1d8381c429baea1f689`. The shared suite index additionally
registers G2's tests; it does not alter G1's test registration.

## Commands and evidence ownership

Commands below ran directly; the archive pipeline enabled `pipefail`.
The source-path witness is deliberately **failing**, not a passing gate.

| Command | Exit | Result |
| --- | ---: | --- |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-36s1fj-replay-v1.idx" git read-tree ea8899e6f97aea64136159286840c28c955243e8` | 0 | Load CR base into an alternate index |
| `task-board resource get TASK-260929-2gp04j TASK-260929-2gp04j_change-request_rev1.patch --output .temp/TASK-260929-2gp04j_change-request_rev1.patch` | 0 | Materialize patch read-only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-36s1fj-replay-v1.idx" git apply --cached .temp/TASK-260929-2gp04j_change-request_rev1.patch` | 0 | Apply to alternate index only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-36s1fj-replay-v1.idx" git write-tree` | 0 | Exact expected candidate tree |
| `git diff --exit-code 58042581a0b507ae62e7b1d8381c429baea1f689 4d289590739432aa55c2a3868c2b4a5472b07c92 -- codex-rs/core/src/tools/spec_plan.rs codex-rs/core/tests/suite/current_time_reminder.rs codex-rs/ext/extension-api` | 0 | Accepted G1 paths unchanged |
| `git diff --check ea8899e6f97aea64136159286840c28c955243e8 4d289590739432aa55c2a3868c2b4a5472b07c92` | 0 | No whitespace errors |
| `git rev-parse 016a4248cf1984b97e786ce8573ad40c9438dfbf^{tree}` | 0 | Hosted snapshot tree equals candidate |
| `git diff --numstat 58042581 4d289590` | 0 | G2: 1309 insertions, 76 deletions |
| `python3 .temp/TASK-261002-36s1fj/TASK-261002-36s1fj_static-witness.py > .temp/TASK-261002-36s1fj/TASK-261002-36s1fj_static-witness.log 2>&1` | **1** | Expected-red static witness: metrics read error skips publisher revocation |
| `gh run view 37002709023 --repo relux-works/codex --job 110823834434 --log > .temp/TASK-261002-36s1fj/hosted-lint-job.log 2>&1` | 0 | Actual checkout is snapshot `016a4248cf1984b97e786ce8573ad40c9438dfbf` |
| `gh run view 37002709023 --repo relux-works/codex --json status,conclusion,jobs > .temp/TASK-261002-36s1fj/hosted-status.json` | 0 | Hosted run and all four lane jobs report success |
| `tar -xOf .temp/TASK-261002-36s1fj/producer-logs.tar.gz bazel-lock-update-01.log` | 0 | Inspect existing lock-refresh log; did not execute Bazel |
| `python3 .temp/TASK-261002-36s1fj/TASK-261002-36s1fj_validate-packet.py` | 0 | Validate JSON shape, exact row coverage and pinned CI identity; not a runtime behavior gate |

Git, task-board, Python and gh readiness outputs were captured under this
task's `.temp/` directory. An initial `rm -f` index initialization was refused
by the executor before execution; using a new index path resolved it without
deletion. Reconnaissance encountered unsupported `resources`, `artifacts` and
`attachments` projection fields and a missing installed reviewer-role file;
these reads were not validation gates or evidence of absence. The supplied
panel brief and installed `references/file-formats.md` supplied the explicit
review/findings contract. No failed read was used to infer missing evidence.

**Reused, not rerun:** `TASK-260929-2gp04j_change-request_rev1-validation.log`
records target guard, fmt-check, scoped clippy and small-crate tests, each
`[exit 0]`. `TASK-260929-2gp04j_hosted-precheck-2.md` records run 37002709023
and all 13/13 narrowing mutants killed by their named tests. I independently
read the hosted run/jobs via GitHub and gh; lint/small/core/app-server jobs
all report success. The lint job log proves checkout of the exact snapshot;
the workflow-dispatch metadata's `head_sha` instead refers to the workflow's
base and must not be mistaken for the tested source SHA. Individual mutant
job logs were **not** reaudited; their 13/13 result is accepted attached
evidence, not my own mutant execution. Hosted statuses do not supply numeric
process exit codes; none are invented here. No cargo, just, rustc or Bazel
command ran in this panel.

## Finding: accounting read failure leaves a known capability

**F1 / robustness / AC 7 / static confidence high.** The newly installed
publication at `codex-rs/ext/goal/src/runtime.rs:676` is after fallible reads.
`current_goal_status_for_metrics` calls `get_thread_goal` and propagates its
error at `runtime.rs:783–785`. Its caller propagates that error at
`runtime.rs:660–662`, before reaching publication. `GoalExtension::on_turn_abort`
(`extension.rs:405–417`) logs an accounting error and returns, without calling
the publisher or invalidating the marker. The analogous turn-stop accounting
error branch (`extension.rs:360–375`) also returns without revocation.

Concrete adversarial sequence: start an Active goal turn with a valid
accounting snapshot and published marker; make the committed goal row
unreadable (the already-shipped read-failure fixture uses an invalid
`updated_at_ms` timestamp); abort that turn. The metrics read errors; Rust's
`?` exits before `reconcile_live_activity`. The hook warns and returns while
the prior GoalActivity remains present and the publisher still records Known,
not Unknown. A subsequent legitimate reconciliation can recover, but that
does not meet the immediate failure-revocation contract. This is a stale
sleep capability, **not** evidence that automatic continuation is admitted;
continuation separately rereads the database and refuses a read error.

The attached witness executes only immutable-source identity and control-flow
checks, returning 1 for this exact reachable error edge. It does **not** run
Rust, inject a live DB failure or simulate the application. The proposed
behavioral regression is: adapt
`ext/goal/tests/goal_extension_backend/goal_activity_tests.rs::read_failure_revokes_activity_and_next_turn_recovers`
to call `start_turn` **before** corrupting the row, then record token usage,
invoke `on_turn_abort`, and assert GoalActivity is absent immediately after
the callback. Run it later in the authorized hosted small lane. That runtime
probe is **not run** here. The existing test corrupts before `on_turn_start`
and therefore covers a different, correctly reconciled path.

Recommended focused repair: route goal-read failures on accounting/abort/stop
paths through the same publisher's Unknown/removal operation while retaining
the goal-state permit; add this lifecycle regression and a narrowing mutant
which revokes only turn-start read failures. Do not merely add another log,
infer absence, or alter automatic-continuation policy.

## Surface sweep and final-plan section 4

The surface table has **1 row**, not eight. It receives exactly one result:
**goal activity publisher → broken**, by F1. All seven section-4 transitions
and all eight AC entries were statically attacked; behavioral executions are
the attached producer/hosted evidence, not panel executions.

| Transition / AC | Attack and source-grounded result |
| --- | --- |
| Successful create / AC 1, 8 | Tool executor holds goal permit through mutation and publication before result; failure also rereads. Finish hook reads committed state rather than trusting tool name. Core and v2 request-tool assertions cover created/refused cases. Held except the general accounting-read failure below. |
| Turn start / AC 2 | `extension.rs:248–270` reconciles before missing-baseline and Plan-mode returns. Cleared-goal leg removes stale state. Held. |
| Resume / external set / AC 3 | Resume reconciles Active and BudgetLimited before Active-only accounting setup; set reconciles under mutation permit and delayed effects reread and compare committed snapshot. Six status variants are tested. Held. |
| Update / automatic stop / accounting limit / AC 4 | Update executor reconciles before result; stop and budget-accounting successful mutations publish; BudgetLimited marker retained but continuation requires Active. Held for successful mutations; error path contributes F1. |
| Clear / AC 5 | Service clears under permit, then unconditionally revokes even while disabled. Late effects reread; clear increments publisher revision. Latch test covers real executor publication followed by disabled clear and stale callback. Held. |
| Thread stop / feature disable / AC 6 | Publisher invalidates revision, removes marker and pending turn options/permit. Re-enable starts Unknown, reconciles at next lifecycle event. Disable is exercised by directly invoking production ConfigContributor, not by session-static refresh. Held within this extension-hook contract. |
| Read failure / AC 7 | Publisher error branch removes marker, increments revision and records Unknown; turn-start/tool-finish direct reconciliation reaches it. Accounting metrics errors escape before that branch; abort/stop can leave Known marker. **Broken, F1.** |

Measured coverage bounds: **1/1 surface rows swept; 7/7 transition families
inspected; 8/8 AC entries mapped; 0/8 runtime AC tests rerun by this panel**.
Attached exact-candidate unmutated execution covers the named tests; its
13/13 mutant kills do not cover accounting/abort read-failure narrowing.

## Additional required judgments and bounded free hunt

- **Change size:** cumulative CR is 1603 additions + 77 deletions = 1680 changed
  lines across 22 files. The independently relevant G2 delta is **1385**
  changed lines across 17 files, not the pre-rework estimate of ~1334.
  Both exceed the 800-line guidance; G2 also exceeds the preferred 500-line
  complex-logic bound. The producer's first stage (inactive publisher,
  property test and wiring, ~225 lines) is a sensible smallest independently
  reviewable foundation and does not pretend to satisfy the feature alone.
  Its second stage remains ~1160 lines, so the proposed two-stage split does
  not by itself put every stage under 800. Recommend foundation, hook
  activation with essential lifecycle tests, then expanded sampling/v2
  adversarial coverage, retaining behavioral regression coverage in the
  activation stage. This is staging guidance, not a second blocking finding.
- **Dev-dependency cycle:** `core/Cargo.toml:143` adds a test-only dependency
  on goal, whose normal dependency points to core. This is not a new
  production core-to-goal dependency; integration-test targets depend on the
  ordinary core library and goal library. `defs.bzl:336` versus its test
  `all_crate_deps(normal = True, normal_dev = True)` sites preserve that
  distinction. Hosted Cargo tests/clippy succeeded. I did not execute Bazel
  compilation, so Bazel target resolution is not newly attested.
- **Lock refresh:** repository instructions require `just bazel-lock-update`
  when Cargo dependencies change, even if no external package version changed.
  The producer's claim that it was not needed is imprecise: it **was required
  and reportedly run**, exit 0, no MODULE.bazel.lock delta. The attached
  `bazel-lock-update-01.log` actually contains `bazel mod deps --lockfile_mode=update`
  and normal dependency output. The candidate has only the two new Cargo.lock
  dependency edges. No missing lockfile update is established; no Bazel build
  pass is inferred from a dependency-refresh log.
- **Bounded free hunt (three probes):** normal/dev build graph; shared automatic
  turn-start permit lease and disable invalidation; model context/API scope.
  No additional demonstrated defect. The lease shares only the read permit
  with the before-registration callback and is removed by a Drop guard;
  continuation still checks committed Active state. No new model-message
  fragment or API payload/config shape is added by G2. G1 sleep-precedence
  policy is unchanged. Cross-platform execution beyond attached evidence is
  unverified, not inferred from Linux success.

## Outcome-scoped logbook

2026-10-02: replay exactly matched the candidate. G1 was unchanged. Hosted
checkout identity and four successful lanes were verified independently.
The sole surfaced defect is a missing read-failure revocation on accounting
error exits (F1); the existing fault injection attacks turn start only.
The size estimate increased after test-only rework; two-stage splitting leaves
an oversized second stage. No source edits or writes on the reviewed task.
This review packet is ready for review by the orchestrator/recording reviewer;
it is not an acceptance or rejection mutation of the reviewed CR.

```verdict-findings
{
  "findings": [
    {
      "id": "accounting-read-failure-retains-capability",
      "row": "goal activity publisher",
      "invariant": "A goal-store read failure removes GoalActivity, records reconciliation Unknown, and is retried by the next legitimate lifecycle event.",
      "mechanism": "codex-rs/ext/goal/src/runtime.rs:660-676 propagates the metrics goal read error before publication; current_goal_status_for_metrics at :783-785 propagates get_thread_goal errors, and ext/goal/src/extension.rs:405-417 logs/returns on abort without revoking the previously Known marker.",
      "reproductions": [
        {
          "test_file": "TASK-261002-36s1fj_static-witness.py",
          "command": "python3 .temp/TASK-261002-36s1fj/TASK-261002-36s1fj_static-witness.py",
          "expected_failure": "Exit 1: immutable-source control-flow witness finds an actual get_thread_goal error propagation path from on_turn_abort that bypasses the sole publisher's Unknown/removal branch. Static witness only; dynamic Rust regression not run because builds/tests are prohibited for this panel.",
          "pinned_blobs": [
            "git-blob:625003a79fbdd9bb54f9287d1b800e2162636097",
            "git-blob:b3070a3a4ad155a6a0525980adec4042648c91f5"
          ]
        }
      ],
      "severity": "robustness",
      "repeat-of": "none"
    }
  ],
  "notes": [
    "No builds/tests or mutant executions were rerun by this panel; expected-red static witness exit 1 is not presented as a passing runtime gate.",
    "Hosted baseline success was independently checked; 13/13 mutant kills are reused attached evidence and do not cover accounting/abort read-failure narrowing.",
    "G2 is 1385 changed lines; inactive ~225-line foundation is the smallest proposed coherent stage, but the remaining ~1160-line stage still exceeds the 800-line guidance.",
    "The test-only core->goal->core graph is not a production dependency cycle. Lock refresh was required and producer evidence says it ran with no lock delta; no Bazel build was executed here.",
    "Re-enable and mid-turn disable coverage exercises production extension hooks directly; no production session path dynamically flips Goals via refresh_runtime_config today."
  ],
  "surface_results": [
    {
      "row": "goal activity publisher",
      "result": "broken",
      "detail": "All seven transition families inspected; accounting goal-read errors bypass Unknown/removal on abort and turn-stop error exits (F1)."
    }
  ],
  "free_hunt": []
}
```
