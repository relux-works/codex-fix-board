# Panel B verdict — TASK-261002-umkkoj: r141-panel-b-task-261002-1ugz6h-rev1

changes_requested

Non-recording static review of CR-TASK-261002-1ugz6h-1 revision 1. No accept/reject/status/handoff, resource, or note was written on the source task. No tracked repository files were changed. The attached verdict is a researcher handoff, not an acceptance or landing.

## Replay and candidate identity

- Base: `35af013b901ed4be1b88416068f140e9ca5cc85d`.
- Temporary-index replay tree: `f38084559bf0a082e724b5daf3edc5bed6981026`, exactly the expected candidate tree.
- Accepted leaf checkpoint: `ec6a7009d28c3f3ae954bd388600b3b9b80c4c70`. Its diff to the candidate names only `.github/workflows/relux-ci.yml`. The two astra snapshots are byte-identical; they were not re-reviewed.
- Candidate workflow blob and signed-source commit `7ae33a059056dad776bd0b81fb2b4883615b9b5a` workflow blob both resolve to `aa604b6c3da32a8a030053c8953eeb176159701e`. That commit's tree is the exact candidate. Signature validation was not independently rerun.
- Hosted [run 36963367409](https://github.com/relux-works/codex/actions/runs/36963367409) was independently read through `gh run view`: push event, matching head SHA, completed/success. All four named lanes and their matching suite steps succeeded. No lane conclusion was inferred from a skipped suite step.

## Scope, budget and coverage

Decision: whether this exact CR satisfies its stated review surfaces. Frozen input is the replayed tree above. Budget: 25 wall-clock minutes including packaging; free hunt up to 3 minutes; one verdict plus small reproduction/API evidence (under 64 KiB total); no serial prerequisite. Consumer is the existing recording reviewer, not a new research or implementation leaf. Exit is a swept table and attached verdict.

Surface coverage: **3/3 rows statically attacked; 2 held, 1 broken, 0 not-attacked**. Rows were walked in supplied order. One blocking mechanism was identified. AC coverage: 4/4 assessed: one-file delta relative to accepted checkpoint, workflow safety, checkout/failure/filter behavior, exact-tree hosted run. All four AC facts hold at the stated bound; the additional per-SHA concurrency surface is broken.

Safety attack traced both referenced local composite actions as well as the workflow: only allowed events, `contents: read`, `ubuntu-24.04`, 8/8 third-party action sites pinned by full SHA, and no untrusted inputs/github interpolation inside shell run text. Lane attack checked exact matrix predicates, six clippy crates, four small crates, ten helper binaries in the right order, and the exact negated union of three fully qualified core exclusions. The three test names resolve to actual candidate functions. `justfile` and `scripts/just-shell.py` were read to trace invocation/exit propagation; no failure masking was found on suite paths.

Free hunt covered composite-action permission/pin propagation, nextest local/default configuration, just shell argument/exit propagation, helper ordering, and cache/error-tolerant steps. No additional blocking mechanism. Existing nextest skips and flaky retry behavior were not re-executed. This is static review under the explicit no-build/no-test brief, not a fresh dynamic certification.

## Blocking finding and concrete witness

At `.github/workflows/relux-ci.yml:26`, the group is `relux-ci-${{ inputs.sha || github.ref }}`. Line 27 sets `cancel-in-progress: true`.

| Input event | SHA | Resolved concurrency group |
|---|---|---|
| push on `ci/relux-ci-selftest/stack-2` | `7ae33a059056dad776bd0b81fb2b4883615b9b5a` | `relux-ci-refs/heads/ci/relux-ci-selftest/stack-2` |
| push on the same branch | `35af013b901ed4be1b88416068f140e9ca5cc85d` | `relux-ci-refs/heads/ci/relux-ci-selftest/stack-2` |
| dispatch with the first SHA | `7ae33a059056dad776bd0b81fb2b4883615b9b5a` | `relux-ci-7ae33a059056dad776bd0b81fb2b4883615b9b5a` |

The attached probe parses the exact candidate, resolves only the simple string-or expression it contains, and exits **1** on the first two witnesses. It does not simulate a build or claim to trigger GitHub cancellation. The operational consequence follows from GitHub's documented [concurrency behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency): matching groups with cancellation enabled allow a newer run to cancel the running one. Thus this workflow can cancel validation of one SHA because another SHA was pushed. The green single-run evidence cannot establish isolation between overlapping runs.

Recommendation: use `inputs.sha || github.sha` if the supplied per-SHA invariant is authoritative, and retain a two-SHA/same-branch witness plus push/dispatch same-SHA equality. If branch-scoped selftest cancellation is intended, explicitly amend/reconcile the surface invariant before acceptance. The producer already notes the distinction, but the surface table does not grant that exception. No external blocker or additional research is needed.

## Commands and real exit codes

All validation/probe commands below ran directly, without `tee` or a status-masking pipeline. Paths are relative to the run worktree; `IDX` denotes `$PWD/.temp/TASK-261002-umkkoj-replay.idx` and `C` denotes the full candidate tree above.

| Command | Exit | Observed evidence |
|---|---:|---|
| `task-board m 'set_status(TASK-261002-umkkoj, status=analysis)'` | 0 | Own task lifecycle started |
| `task-board resource get TASK-261002-1ugz6h TASK-261002-1ugz6h_change-request_rev1.patch --output .temp/TASK-261002-1ugz6h_change-request_rev1.patch` | 0 | Patch materialized read-only from source task |
| `GIT_INDEX_FILE="$IDX" git read-tree 35af013b901ed4be1b88416068f140e9ca5cc85d` | 0 | Base index initialized |
| `GIT_INDEX_FILE="$IDX" git apply --cached .temp/TASK-261002-1ugz6h_change-request_rev1.patch` | 0 | Patch replayed |
| `GIT_INDEX_FILE="$IDX" git write-tree` | 0 | `f38084559bf0a082e724b5daf3edc5bed6981026` |
| `git diff --name-only ec6a7009d28c3f3ae954bd388600b3b9b80c4c70 C` | 0 | Only `.github/workflows/relux-ci.yml` |
| `git rev-parse '7ae33a059056dad776bd0b81fb2b4883615b9b5a^{tree}' '7ae33a059056dad776bd0b81fb2b4883615b9b5a:.github/workflows/relux-ci.yml' 'C:.github/workflows/relux-ci.yml'` (C expanded) | 0 | Matching tree and blobs listed above |
| `gh run view 36963367409 --repo relux-works/codex --json headSha,event,status,conclusion,name,displayTitle,jobs,url` | 0 | Stored API result, 4/4 lanes green |
| `python3 .temp/TASK-261002-umkkoj/static-probe.py safety` | 0 | Allowed triggers/permissions/runner; 8 pinned action sites |
| `python3 .temp/TASK-261002-umkkoj/static-probe.py concurrency` | **1** | Expected-red finding: different SHA push runs share group; not a pass |
| `python3 .temp/TASK-261002-umkkoj/static-probe.py lanes` (initial probe) | **1** | Reviewer probe had an extra whitespace constraint at `not (`; probe construction error, not a candidate defect |
| `python3 .temp/TASK-261002-umkkoj/static-probe.py lanes` (corrected probe) | 0 | 4 lane predicates, exact crates/helpers/filter, 4 hosted matching suite steps |
| `git diff --exit-code ec6a7009d28c3f3ae954bd388600b3b9b80c4c70 C -- ':! .github/workflows/relux-ci.yml'` | **1** | Reviewer pathspec typo contained a space, so workflow diff remained; not evidence of snapshot drift |
| `git diff --exit-code ec6a7009d28c3f3ae954bd388600b3b9b80c4c70 C -- . ':!.github/workflows/relux-ci.yml'` | 0 | Corrected comparison: no other changed bytes |
| `git diff --check 35af013b901ed4be1b88416068f140e9ca5cc85d C` | 0 | No whitespace errors |
| `git grep -n -E '<three exact excluded function names>' C -- codex-rs/core/tests` | 0 | All three definitions located |
| `git status --short` | 0 | Empty; no tracked/untracked repository delta outside ignored scratch |

Readiness (`git --version`, `rg --version`, `python3 --version`, `gh --version`, Python `import yaml`) succeeded; readiness output is in ignored `.temp/TASK-261002-umkkoj/`. Supporting `git show`, AC/resource reads and candidate inspections succeeded. Discovery failures were not treated as absence: two initial projections used unsupported `resources` (exit 1); `resource list` printed usage (exit 0, no inventory); one combined skill read ended exit 1 because the curator role path was absent. The installed role was then located and read. Resource retrievals for surface-table, producer-brief and hosted evidence each exited 0. No cargo/just/build/test suite or producer audit/mutant rerun occurred.

Artifact schema audit: standalone `python3` JSON/row validator exited **0**; exactly one `verdict-findings` block, all 3 rows exactly once, all required finding/reproduction keys, valid severity and the `changes_requested` verdict were checked.

## Evidence reused, not rerun

- Source task outcome `TASK-261002-1ugz6h_results.md`: reported local fmt-check/actionlint/static audit and seven killed mutants. Read for context; these checks were not rerun by this panel. A source-token audit is not treated as proof of the concurrency property.
- `TASK-261002-1ugz6h_hosted-ci-stack-2.md`: reported core 4854 passing and app-server 1827 passing. This panel independently checked API run/job/step identity and success, not raw per-test logs or the underlying historical quarantine failures.
- The explicit orchestrator brief permits replay/static review and identifies prior accepted leaf snapshots. Byte equality was independently verified; prior acceptance was reused.

## Logbook entry — 2026-10-02

Independent panel replay matched the supplied candidate and previous snapshot checkpoint. Static sweep found a contract mismatch in concurrency fallback: branch-scoped push cancellation versus unqualified per-SHA surface invariant. The hosted exact-tree green result remains valid, but does not resolve this cross-run property. Route the single mechanism to the recording reviewer; make no writes on the source task. All scratch/reproduction files were staged under the run's ignored `.temp/` to respect the run write boundary; durable outcomes are attached via board resource CRUD outside the managed source tree.

## Sources

- Source task `surface-table.md`, evidence-exactness row; `task-board q 'get(TASK-261002-1ugz6h) { description scope ac notes }'`.
- Candidate `.github/workflows/relux-ci.yml:8,26,27,44,56,107,112,116,133,140,144` at `f38084559bf0a082e724b5daf3edc5bed6981026`.
- Candidate `.github/actions/setup-ci/action.yml`, `.github/actions/setup-rusty-v8/action.yml`, `justfile`, `scripts/just-shell.py`, `codex-rs/.config/nextest.toml`, `codex-rs/rust-toolchain.toml`.
- Attached `TASK-261002-umkkoj_static-probe.py` and `TASK-261002-umkkoj_hosted-run.json` preserve the executable static witness and read-only provider evidence.

```verdict-findings
{
  "findings": [
    {
      "id": "push-concurrency-cross-sha",
      "row": "evidence exactness",
      "invariant": "The surface table requires one concurrency group per SHA across the declared dispatch and selftest-push entry points.",
      "mechanism": ".github/workflows/relux-ci.yml:26 uses inputs.sha || github.ref, while line 27 enables cancel-in-progress. Distinct push SHAs on the same allowed selftest branch resolve to one group; a later push can cancel the earlier SHA validation. A push and dispatch of the same SHA also resolve to different groups. The producer audit checks only presence of inputs.sha, so its passing result does not enforce the fallback half of this invariant.",
      "reproductions": [
        {
          "test_file": "TASK-261002-umkkoj_static-probe.py (read-only static witness, concurrency mode)",
          "command": "python3 TASK-261002-umkkoj_static-probe.py concurrency",
          "expected_failure": "Exit 1: FAIL per-SHA isolation: distinct push SHAs share a cancellation group. Candidate bytes are read using git show f38084559bf0a082e724b5daf3edc5bed6981026:.github/workflows/relux-ci.yml. Both push witnesses produce relux-ci-refs/heads/ci/relux-ci-selftest/stack-2.",
          "observed_exit_code": 1,
          "log": "The command transcript and witness values are recorded above this block; no hosted cancellation experiment was run."
        }
      ],
      "severity": "regression",
      "repeat-of": "none"
    }
  ],
  "notes": [
    {
      "id": "static-only-bound",
      "text": "Per the explicit panel brief, held means the named static attacks found no defect, corroborated where available by existing hosted execution. This panel ran no cargo, just, build, suite, hosted dispatch or live negative workflow. It does not claim the generic reviewer contract public-entry dynamic attack was executed."
    },
    {
      "id": "producer-scope-qualification",
      "text": "The producer results explicitly describe branch-scoped cancellation for push and per-SHA cancellation for dispatch. The supplied surface-table invariant has no such qualification; producer context cannot silently amend it. If branch cancellation is intentional, the recording reviewer/orchestrator must explicitly reconcile the surface contract; otherwise change the fallback to github.sha and retain a two-SHA/same-ref regression witness."
    },
    {
      "id": "exact-sha-input-domain",
      "text": "The required sha input is an unrestricted string, and checkout receives it unchanged. Valid immutable SHA dispatches satisfy AC3. Runtime rejection of branch/tag strings was not demonstrated; no extra malformed-input requirement is inferred beyond the stated AC."
    },
    {
      "id": "execution-evidence-bound",
      "text": "GitHub API independently confirms success for all four matching suite steps and the exact commit/tree. Producer-reported counts, negative mutants, local fmt/actionlint/audit and CR validation are accepted as attached reports, not rerun or independently attested from raw local gate logs."
    }
  ],
  "surface_results": [
    {
      "row": "trigger and permission safety",
      "result": "held",
      "reason": "Static attack of exact candidate and both local composite actions found only the two allowed events, read-only token, one hosted runner, 8/8 action sites SHA-pinned and no untrusted context interpolated into run. No hosted negative dispatch was executed, per panel scope."
    },
    {
      "row": "evidence exactness",
      "result": "broken",
      "findings": [
        "push-concurrency-cross-sha"
      ],
      "reason": "Exact candidate group resolves two distinct push SHAs on the allowed selftest branch to the same cancellation key; the one-group-per-SHA invariant fails. Checkout and suite failure propagation otherwise hold statically."
    },
    {
      "row": "lane coverage",
      "result": "held",
      "reason": "Static attack confirms 4/4 reachable matrix lane predicates, six lint/four small crates, ten helper binaries before core/app-server, the exact complement of only three fully qualified excluded names, and unmasked suite exits. Read-only GitHub API confirms the matching suite steps actually succeeded in all 4 exact-tree hosted jobs. No suite rerun in this panel."
    }
  ],
  "free_hunt": []
}
```
