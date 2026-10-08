# Panel A verdict: CR-TASK-261002-1ugz6h-1 rev1 (story_final)

Reviewer: researcher panel A (non-recording). Nothing was written on TASK-261002-1ugz6h.

## Replay tree check
- `GIT_INDEX_FILE=.temp/TASK-261002-2l3mn9-replay.idx git read-tree 35af013b901ed4be1b88416068f140e9ca5cc85d` exit 0
- `task-board resource get TASK-261002-1ugz6h TASK-261002-1ugz6h_change-request_rev1.patch --output ...` exit 0
- `git apply --cached <patch>` exit 0
- `git write-tree` exit 0, printed `f38084559bf0a082e724b5daf3edc5bed6981026` = expected candidate tree. MATCH.

## Other commands (all exit 0)
- `git diff --stat ec6a7009d28c3f3ae954bd388600b3b9b80c4c70 f380845...` touches only `.github/workflows/relux-ci.yml` (151 insertions). The two astra snapshots are byte-identical to leaf-1 checkpoint ec6a700.
- `git rev-parse f380845:.github/workflows/relux-ci.yml` = `aa604b6c3da32a8a030053c8953eeb176159701e`, equal to the blob in signed commit 7ae33a0 (AC1 blob identity).
- Static read of the workflow plus the two local composite actions it uses (setup-ci, setup-rusty-v8), justfile, scripts/just-shell.py, nextest.toml, workspace lint config.
- `gh run view 36963367409 -R relux-works/codex --json ...` (read-only): conclusion success, event push, headSha 7ae33a0 (tree f380845), jobs lint/core/small/app-server all success. Matches the attached hosted-ci-stack-2 evidence.
- `gh run view ... --job <lint> --log` (read-only) grepped for clippy output (source of the F1 finding).
- No cargo/just/build/test was run.

## Verdict
accept

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
      "repeat-of": null
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
      "repeat-of": null
    }
  ],
  "notes": [
    "Hosted evidence verified independently via gh: run 36963367409, push event, head 7ae33a0 whose tree is the candidate tree f380845, all four lanes success. AC4 holds.",
    "Script injection: inputs.sha, inputs.label, github.ref and github.ref_name appear only in run-name, concurrency.group, checkout `with.ref` and actions/cache `key`; none is interpolated into a `run:` body. matrix.lane is a literal list. No injection path found.",
    "Action pinning: all six third-party `uses:` in the file (checkout, rust-toolchain, install-action x1, cache/restore, setup-uv, cache/save) are full 40-hex SHAs and equal the pins already used in the upstream workflows in this tree; setup-uv SHA resolves via the GitHub API. The two local composites pin facebook/install-dotslash and taiki-e/install-action by SHA; setup-rusty-v8 verifies downloaded archives against the in-tree trusted manifest checksums. No `secrets.` reference anywhere in the workflow or the two composites.",
    "Concurrency: group is `relux-ci-<inputs.sha>` on dispatch and `relux-ci-<ref>` on push, with cancel-in-progress. A second dispatch of the same SHA with a different label cancels the first (cancelled, not green) and two pushes to one selftest ref cancel the older SHA. Fail-safe, but the 'one group per SHA' wording holds only for dispatch.",
    "Masking: the only `continue-on-error` is on the cache-save step; `|| true` appears only on the disk-cleanup `rm` and `sccache --show-stats`. No test or build step is masked. NEXTEST_RETRIES=2 overrides the profile retries (default profile has retries=1); retries only rerun failures, so a deterministic failure still fails. The app-server lane's one flaky pass on retry (login_account_chatgpt_uses_oauth_overrides) is disclosed in the evidence.",
    "Cache scope: actions/cache/save under a dispatched run writes into the dispatching ref's cache scope; sccache entries are content-addressed so poisoning risk is low. permissions stay contents: read (the cache action uses the runtime token, not GITHUB_TOKEN)."
  ],
  "surface_results": [
    {
      "row": "trigger and permission safety",
      "result": "held",
      "evidence": "on: workflow_dispatch + push branches [ci/relux-ci-selftest/**] only; no pull_request, pull_request_target, issues or schedule events. permissions: contents: read at workflow level, no job override. runs-on ubuntu-24.04 only (the word 'self-hosted' appears only in a comment). No secrets reference. All third-party actions SHA-pinned. No expression from inputs/github is interpolated into a run: script."
    },
    {
      "row": "evidence exactness",
      "result": "held",
      "evidence": "The single job (matrix of 4 lanes) checks out `inputs.sha || github.sha`; run-name embeds the same expression plus label; concurrency group is per-SHA on dispatch; fail-fast false and no masking of test exits (see notes). Residual: input format is not validated or asserted post-checkout (F2, robustness)."
    },
    {
      "row": "lane coverage",
      "result": "held",
      "evidence": "lint = `just fmt-check` + clippy on exactly the 6 crates (tools, core, goal-extension, extension-api, app-server, rollout-trace). small = exactly 4 (tools, goal-extension, extension-api, rollout-trace). core runs `just test -p codex-core` with only the 3 named zsh-fork exclusions (exact `=` test() matches, no wildcards); app-server runs `just test -p codex-app-server` unfiltered; both lanes build helper binaries first. Hosted counts: core 4854/4854 with 11 skipped = 8 default + 3 exclusions; app-server 1827/1827. Caveat F1: clippy admits non-denied warnings, unlike upstream -D warnings."
    }
  ],
  "free_hunt": "Checked: env ordering (RUSTC_WRAPPER=sccache is set workflow-wide but only cargo steps follow the sccache install); just `{args}` token handled by scripts/just-shell.py so `-p` forwarding works; INSTA_UPDATE=no prevents snapshot auto-accept; INSTA_WORKSPACE_ROOT set for snapshot lanes; fmt-check lane installs uv only in the lint lane; the matrix `if:` conditions match step names so no lane silently runs zero test steps (small/core/app-server each have exactly one test step, lint has the lint step). Two robustness items found (F1, F2); nothing at bypass or regression level."
}
```
