# Panel A verdict — TASK-261002-1ugz6h CR-TASK-261002-1ugz6h-2 (rev 2), non-recording (tb-R141)

Verdict: **accept**

## Replay tree check
- Base `35af013b901ed4be1b88416068f140e9ca5cc85d` + resource `TASK-261002-1ugz6h_change-request_rev2.patch` applied through a temporary index (`GIT_INDEX_FILE`, no nested worktree).
- `git write-tree` printed `429a14a27a106f73b5907a0d830c4548cb3f1ea4` = expected candidate tree. **Match.**
- Leaf-1 snapshot check: `git diff ec6a7009d28c3f3ae954bd388600b3b9b80c4c70 429a14a2…` touches only `.github/workflows/relux-ci.yml` (178 insertions); `git diff --quiet ec6a700 429a14a2 -- codex-rs` exit 0, so both astra snapshot files are byte-identical to the leaf-1 checkpoint (ec6a700 tree 5c365d9a; its diff vs base is exactly those 2 snaps, 12+/12-).

## Commands run (all read-only; no cargo/just/build/test)
| Command | Exit |
| --- | ---: |
| `GIT_INDEX_FILE=… git read-tree 35af013…` | 0 |
| `task-board resource get TASK-261002-1ugz6h …rev2.patch` | 0 |
| `GIT_INDEX_FILE=… git apply --cached …rev2.patch` | 0 |
| `GIT_INDEX_FILE=… git write-tree` → 429a14a2… | 0 |
| `git diff --stat ec6a700 429a14a2` / `git diff --quiet … -- codex-rs` | 0 / 0 |
| `git show 0462dcc062:<3 baseline files>` + grep for the 3 imports | 0 |
| `gh api repos/<action>/commits/<sha>` for the 5 third-party pins + 3 tag refs | 0 |
| `git show 429a14a2:` test-name greps for the 3 excluded zsh-fork tests | 0 |
| `bash TASK-261002-xjtnso_gate-witness.sh` (text-pipeline replay, no cargo) | 0 |

## Round-1 findings re-attacked
- F1 (warnings not failing the lint lane): closed. Lines 114-135 parse `file:line:col: warning:` from clippy output and fail on any warning outside the 3-entry baseline. Witness A (new unused import) fails the gate. Hosted negative control run 36974565033 corroborates (lint lane failed on the injected import; baseline tolerated and counted).
- F2 (`inputs.sha` unverified): closed. Lines 59-66 require `^[0-9a-f]{40}$` and `git rev-parse HEAD == WANT_SHA`, run in every lane; `WANT_SHA` goes through `env:`, not into the script body. Abbreviated, uppercase, branch/tag names fail closed; an annotated-tag object id passes the regex but fails the HEAD compare.
- Push concurrency per ref: closed. Group is `relux-ci-${{ inputs.sha || github.sha }}` (line 27), so distinct push SHAs on one selftest ref no longer share a group.

## Baseline claim (3 KNOWN_WARNINGS)
Verified at upstream pin `0462dcc062`: `registry.rs` has `use crate::tools::context::ToolCallSource;` (line 16) and no other mention; `openai_file_mcp.rs` imports `wiremock::matchers::body_json` (line 47), other `body_json` hits are `set_body_json`; `scenarios.rs` imports `ReasoningEffort` (line 42) with no other use. The three files are byte-identical between the pin and the candidate (`git diff --stat` empty), so the warnings are upstream-baseline, not introduced here.

## Residual notes (not blocking)
1. The gate only sees warnings printed as `path:line:col: warning: …`. Witness B/D: cargo-level or build-script warnings without a span (`warning: unused manifest key`, `warning: pkg@ver: …`) are not parsed and pass. The comment on line 114 ("Any clippy or rustc warning fails the lane") overstates this; the stated bound should be "any spanned clippy/rustc warning".
2. Baseline dedup is by file+message (witness C): a second occurrence of an already-baselined warning in the same file passes. Narrow; the count line would still show the same totals.
3. The task's ACs 1 and 4 are stale against rev 2: AC1 names the blob of 7ae33a0 and "nothing else" (candidate is the rev-2 workflow plus, as the Story's cumulative final CR, the two leaf-1 snapshots); AC4 names run 36963367409 (rev-1 tree f380845). The rev-2 evidence is run 36974560859 (tree 429a14a2, same tree as the candidate, all four lanes green; ea8899e is not the CR commit but has an identical tree). The orchestrator should reconcile the AC text when recording.
4. NEXTEST_RETRIES=2 lets a test that fails once and passes on retry go green (app-server: 1 flaky disclosed). Deterministic failures still fail. Accepted risk, disclosed in the evidence.
5. Concurrency group names are case-insensitive on GitHub: a dispatch with an uppercase form of an in-flight SHA would cancel the legit run, then itself fail the 40-lower-hex check. Write-access dispatcher only; fail-safe.

Bound: static only. I did not run cargo, just, or any hosted dispatch. Hosted green/negative-control results are taken from the attached evidence resources, which I read; the run conclusions themselves were not re-queried this round (round-1 panel re-verified the rev-1 run via gh).

```verdict-findings
{
  "findings": [
    {
      "id": "P1",
      "row": "lane coverage",
      "invariant": "Any clippy or rustc warning outside the upstream baseline fails the lint lane",
      "mechanism": "The gate extracts warnings with sed -nE 's/^([^ :]+):[0-9]+:[0-9]+: (warning: .*)$/…/p'. Warnings without a file:line:col prefix (cargo manifest warnings, build-script cargo:warning output, summary lines) never reach warnings.txt, so they are neither counted nor failed on. The workflow comment claims all warnings fail the lane.",
      "reproductions": [
        {
          "test_file": "TASK-261002-xjtnso_gate-witness.sh (cases B, D)",
          "command": "bash TASK-261002-xjtnso_gate-witness.sh",
          "expected_failure": "A gate covering every warning would print GATE FAILS for case B and D; it prints GATE PASSES"
        }
      ],
      "severity": "note",
      "repeat-of": null
    },
    {
      "id": "P2",
      "row": "lane coverage",
      "invariant": "A warning outside the baseline fails the lint lane",
      "mechanism": "warnings.txt is `sort -u` over `file: warning: message`, dropping line numbers. A new occurrence of an already-baselined warning in the same file with the same message collapses into the baseline entry and passes.",
      "reproductions": [
        {
          "test_file": "TASK-261002-xjtnso_gate-witness.sh (case C)",
          "command": "bash TASK-261002-xjtnso_gate-witness.sh",
          "expected_failure": "A per-occurrence gate would fail case C; it prints GATE PASSES"
        }
      ],
      "severity": "note",
      "repeat-of": null
    }
  ],
  "notes": [
    "Replay: base 35af013b90 + rev2 patch via temporary index; write-tree = 429a14a27a106f73b5907a0d830c4548cb3f1ea4 (match). git diff ec6a700 vs candidate touches only .github/workflows/relux-ci.yml; codex-rs identical, so both astra snapshot files are byte-identical to the leaf-1 checkpoint.",
    "Round-1 F1, F2 and push-concurrency-cross-sha are each closed in rev 2 (lines 114-135, 59-66, 27) and corroborated by hosted run 36974560859 (all lanes green, 'clippy warnings: 3 distinct, 3 of them upstream baseline') and negative control run 36974565033 (lint lane fails on injected unused import).",
    "The 3 KNOWN_WARNINGS were verified as upstream-baseline: at pin 0462dcc062 each import exists and is unused (single mention in the file), and all three files are unchanged between the pin and the candidate.",
    "All 5 third-party action SHAs resolve via gh api to commits in their repos; checkout v6.0.2, setup-uv v8.1.0 and cache v5.0.4 tag refs point at the pinned SHAs. They equal the pins used in the in-tree upstream rust-ci-full.yml. The two local composites used (setup-ci, setup-rusty-v8) pin facebook/install-dotslash and taiki-e/install-action by SHA and reference no secrets.",
    "No inputs.* or github.* expression is interpolated into a run: body: inputs.sha reaches run only through env WANT_SHA; inputs.label appears only in run-name; matrix.lane is a literal list.",
    "AC1 and AC4 text is stale against rev 2 (names blob 7ae33a0 and run 36963367409 of the rev-1 tree); rev-2 evidence is run 36974560859 on tree 429a14a2. Orchestrator should reconcile at recording.",
    "NEXTEST_RETRIES=2 can turn a once-failing test green (1 disclosed flaky pass in app-server). Deterministic failures still fail.",
    "Static-only bound: no cargo/just/build/hosted dispatch by this panel; hosted run conclusions are from attached evidence resources, not re-queried this round."
  ],
  "surface_results": [
    {
      "row": "trigger and permission safety",
      "result": "held",
      "evidence": "on: workflow_dispatch + push branches ci/relux-ci-selftest/** only (a branches filter excludes tag pushes); no pull_request/pull_request_target/issues/schedule. permissions: contents: read, no job override. runs-on ubuntu-24.04 only ('self-hosted' occurs only in a comment). No secrets. references in the workflow or the two composites. All 5 third-party uses: are full-SHA pinned and resolve via gh api; no inputs/github expression in any run: body."
    },
    {
      "row": "evidence exactness",
      "result": "held",
      "evidence": "checkout ref = inputs.sha || github.sha; every lane then asserts 40-lower-hex and git rev-parse HEAD == WANT_SHA (fails closed for abbreviated, uppercase, branch/tag names and tag-object ids). run-name carries inputs.sha || github.sha. Concurrency group relux-ci-${{ inputs.sha || github.sha }} is per-SHA for both entry points. Only continue-on-error is on the cache-save step; || true only on disk cleanup and sccache stats; no test step masked. Residual note 5 (case-insensitive group) is fail-safe."
    },
    {
      "row": "lane coverage",
      "result": "held",
      "evidence": "lint: fmt-check + clippy -p on 6 crates, with a warning gate whose control case fails (witness A, hosted neg run 36974565033) and whose baseline is verified at the pin; blind spots recorded as P1/P2 (note). small: tools, goal-extension, extension-api, rollout-trace (4). core and app-server build helper binaries first, then run full suites; just test = cargo nextest run --no-fail-fast, so a failing test fails the step. Only exclusions: the 3 zsh-fork tests, each name confirmed present at the candidate (skill_approval.rs x1, unified_exec_zsh_fork_approvals.rs x2) and documented with run evidence in the workflow comment. Hosted run 36974560859: core 4854/4854 (11 skipped = 8 default + 3), app-server 1827/1827 (1 flaky on retry, disclosed)."
    }
  ],
  "free_hunt": [
    "Tag pushes and fork-originated events cannot trigger it: the push filter is branches-only and the file has no pull_request* events.",
    "Cache poisoning via restore-keys fallback: caches are scoped per ref (default-branch caches readable by all); sccache entries are content-addressed; the save step runs only under contents: read and cache runtime token. Low risk, not a finding.",
    "Dispatch on a given --ref runs the workflow file from that ref while testing inputs.sha; composites (setup-ci, setup-rusty-v8) are taken from the checked-out candidate, which is the intended behaviour for evidence on the exact tree. Dispatch requires write access.",
    "Verify step sits before every build step and has no working-directory dependency problem (git rev-parse HEAD works in codex-rs). Step order: checkout, verify, then everything else, so a mismatch stops the lane before any build.",
    "Free-hunt for set -o pipefail placement: fmt-check runs before it, but the default bash -e shell aborts on failure; the pipe clippy|tee is under pipefail, so a clippy error exits the step. No gap found."
  ]
}
```
