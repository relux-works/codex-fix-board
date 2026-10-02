# Merged review verdict — TASK-261002-1ugz6h CR revision 1 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261002-2l3mn9_panel-verdict.md` (changes_requested), `TASK-261002-umkkoj_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "F1",
      "row": "lane coverage",
      "invariant": "the lint lane gates clippy on the 6 series crates",
      "mechanism": "The lint step runs `just clippy -p ...` = `cargo clippy --tests -p ...` with no `-- -D warnings`. Only the workspace-denied lints in codex-rs/Cargo.toml [workspace.lints.clippy] fail it; plain rustc/clippy warnings pass. Upstream rust-ci-full.yml runs clippy with `-D warnings`. Hosted run 36963367409 lint job logged 3 rustc `unused import` warnings in codex-core (lib and tests) and still concluded success. Those warnings already exist on base 35af013, so adding -D warnings now would turn the lane red; it is a documented-by-behavior gap, not a regression of this CR.",
      "reproductions": [
        {
          "test_file": ".github/workflows/relux-ci.yml (Lint step, line 108)",
          "command": "gh run view 36963367409 -R relux-works/codex --job 110701706479 --log | grep 'unused import'",
          "expected_failure": "a gate equal to upstream's would fail the job on the unused-import warnings; the lane stays green"
        }
      ],
      "severity": "robustness",
      "repeat-of": null,
      "reported_by": [
        "TASK-261002-2l3mn9"
      ]
    },
    {
      "id": "F2",
      "row": "evidence exactness",
      "invariant": "every dispatched run validates exactly the SHA it names",
      "mechanism": "`inputs.sha` is free text passed to actions/checkout `ref:`. Nothing requires a full 40-hex SHA or asserts `git rev-parse HEAD == inputs.sha` after checkout. A branch or tag name is accepted, checks out the moving tip, and run-name/concurrency then carry the name, not an immutable SHA. The orchestrator's discipline (dispatch with a full SHA) is the only guard; the pass is also never tied to a tree OID inside the run.",
      "reproductions": [
        {
          "test_file": ".github/workflows/relux-ci.yml (checkout step, lines 54-56)",
          "command": "gh workflow run relux-ci -R relux-works/codex -f sha=ci/relux-ci-selftest/stack-2",
          "expected_failure": "a strict gate would reject a non-SHA input; the run proceeds and validates whatever the branch tip is at checkout time"
        }
      ],
      "severity": "robustness",
      "repeat-of": null,
      "reported_by": [
        "TASK-261002-2l3mn9"
      ]
    },
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
      "repeat-of": "none",
      "reported_by": [
        "TASK-261002-umkkoj"
      ]
    }
  ],
  "notes": [
    "[TASK-261002-2l3mn9] Hosted evidence verified independently via gh: run 36963367409, push event, head 7ae33a0 whose tree is the candidate tree f380845, all four lanes success. AC4 holds.",
    "[TASK-261002-2l3mn9] Script injection: inputs.sha, inputs.label, github.ref and github.ref_name appear only in run-name, concurrency.group, checkout `with.ref` and actions/cache `key`; none is interpolated into a `run:` body. matrix.lane is a literal list. No injection path found.",
    "[TASK-261002-2l3mn9] Action pinning: all six third-party `uses:` in the file (checkout, rust-toolchain, install-action x1, cache/restore, setup-uv, cache/save) are full 40-hex SHAs and equal the pins already used in the upstream workflows in this tree; setup-uv SHA resolves via the GitHub API. The two local composites pin facebook/install-dotslash and taiki-e/install-action by SHA; setup-rusty-v8 verifies downloaded archives against the in-tree trusted manifest checksums. No `secrets.` reference anywhere in the workflow or the two composites.",
    "[TASK-261002-2l3mn9] Concurrency: group is `relux-ci-<inputs.sha>` on dispatch and `relux-ci-<ref>` on push, with cancel-in-progress. A second dispatch of the same SHA with a different label cancels the first (cancelled, not green) and two pushes to one selftest ref cancel the older SHA. Fail-safe, but the 'one group per SHA' wording holds only for dispatch.",
    "[TASK-261002-2l3mn9] Masking: the only `continue-on-error` is on the cache-save step; `|| true` appears only on the disk-cleanup `rm` and `sccache --show-stats`. No test or build step is masked. NEXTEST_RETRIES=2 overrides the profile retries (default profile has retries=1); retries only rerun failures, so a deterministic failure still fails. The app-server lane's one flaky pass on retry (login_account_chatgpt_uses_oauth_overrides) is disclosed in the evidence.",
    "[TASK-261002-2l3mn9] Cache scope: actions/cache/save under a dispatched run writes into the dispatching ref's cache scope; sccache entries are content-addressed so poisoning risk is low. permissions stay contents: read (the cache action uses the runtime token, not GITHUB_TOKEN).",
    "[TASK-261002-umkkoj] {'id': 'static-only-bound', 'text': 'Per the explicit panel brief, held means the named static attacks found no defect, corroborated where available by existing hosted execution. This panel ran no cargo, just, build, suite, hosted dispatch or live negative workflow. It does not claim the generic reviewer contract public-entry dynamic attack was executed.'}",
    "[TASK-261002-umkkoj] {'id': 'producer-scope-qualification', 'text': 'The producer results explicitly describe branch-scoped cancellation for push and per-SHA cancellation for dispatch. The supplied surface-table invariant has no such qualification; producer context cannot silently amend it. If branch cancellation is intentional, the recording reviewer/orchestrator must explicitly reconcile the surface contract; otherwise change the fallback to github.sha and retain a two-SHA/same-ref regression witness.'}",
    "[TASK-261002-umkkoj] {'id': 'exact-sha-input-domain', 'text': 'The required sha input is an unrestricted string, and checkout receives it unchanged. Valid immutable SHA dispatches satisfy AC3. Runtime rejection of branch/tag strings was not demonstrated; no extra malformed-input requirement is inferred beyond the stated AC.'}",
    "[TASK-261002-umkkoj] {'id': 'execution-evidence-bound', 'text': 'GitHub API independently confirms success for all four matching suite steps and the exact commit/tree. Producer-reported counts, negative mutants, local fmt/actionlint/audit and CR validation are accepted as attached reports, not rerun or independently attested from raw local gate logs.'}"
  ],
  "surface_results": [
    {
      "row": "trigger and permission safety",
      "result": "held",
      "evidence": "on: workflow_dispatch + push branches [ci/relux-ci-selftest/**] only; no pull_request, pull_request_target, issues or schedule events. permissions: contents: read at workflow level, no job override. runs-on ubuntu-24.04 only (the word 'self-hosted' appears only in a comment). No secrets reference. All third-party actions SHA-pinned. No expression from inputs/github is interpolated into a run: script.",
      "reported_by": "TASK-261002-2l3mn9"
    },
    {
      "row": "evidence exactness",
      "result": "broken",
      "findings": [
        "push-concurrency-cross-sha"
      ],
      "reason": "Exact candidate group resolves two distinct push SHAs on the allowed selftest branch to the same cancellation key; the one-group-per-SHA invariant fails. Checkout and suite failure propagation otherwise hold statically.",
      "reported_by": "TASK-261002-umkkoj"
    },
    {
      "row": "lane coverage",
      "result": "held",
      "evidence": "lint = `just fmt-check` + clippy on exactly the 6 crates (tools, core, goal-extension, extension-api, app-server, rollout-trace). small = exactly 4 (tools, goal-extension, extension-api, rollout-trace). core runs `just test -p codex-core` with only the 3 named zsh-fork exclusions (exact `=` test() matches, no wildcards); app-server runs `just test -p codex-app-server` unfiltered; both lanes build helper binaries first. Hosted counts: core 4854/4854 with 11 skipped = 8 default + 3 exclusions; app-server 1827/1827. Caveat F1: clippy admits non-denied warnings, unlike upstream -D warnings.",
      "reported_by": "TASK-261002-2l3mn9"
    }
  ],
  "free_hunt": [
    "[TASK-261002-2l3mn9] Checked: env ordering (RUSTC_WRAPPER=sccache is set workflow-wide but only cargo steps follow the sccache install); just `{args}` token handled by scripts/just-shell.py so `-p` forwarding works; INSTA_UPDATE=no prevents snapshot auto-accept; INSTA_WORKSPACE_ROOT set for snapshot lanes; fmt-check lane installs uv only in the lint lane; the matrix `if:` conditions match step names so no lane silently runs zero test steps (small/core/app-server each have exactly one test step, lint has the lint step). Two robustness items found (F1, F2); nothing at bypass or regression level."
  ]
}
```
