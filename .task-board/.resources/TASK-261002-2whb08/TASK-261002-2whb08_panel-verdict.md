# R141 DELTA panel verdict — TASK-261002-1ugz6h CR-TASK-261002-1ugz6h-2 rev 2 (non-recording; panel TASK-261002-2whb08)

Verdict: accept

## Replay tree check
- Base `35af013b901ed4be1b88416068f140e9ca5cc85d`, patch `TASK-261002-1ugz6h_change-request_rev2.patch` (3 files: relux-ci.yml + 2 astra snapshots).
- `GIT_INDEX_FILE=<tmp idx> git read-tree <base>` exit 0; `task-board resource get ... --output` exit 0; `git apply --cached` exit 0; `git write-tree` exit 0 -> `429a14a27a106f73b5907a0d830c4548cb3f1ea4` = expected candidate tree. MATCH.
- Cumulative-diff check: `git diff --stat ec6a7009d2 429a14a27a` touches only `.github/workflows/relux-ci.yml` (178 insertions); `git rev-parse` of both snapshot blobs at ec6a700 and at the candidate are equal (3d2590e2..., deb77545...), ec6a700 tree is 5c365d9a, base is an ancestor of ec6a700. Snapshots are byte-identical to the leaf-1 checkpoint.
- ea8899e (hosted push commit) has tree 429a14a (equal to candidate).

## Commands run (no cargo/just/build/test)
| Command | Exit |
| --- | ---: |
| read-tree / resource get / apply --cached / write-tree (replay) | 0 / 0 / 0 / 0 |
| git diff --stat ec6a700 429a14a | 0 |
| git show 0462dcc:codex-rs/<3 files> \| grep (baseline imports present) | 0 |
| git diff --stat 0462dcc 429a14a -- <3 baseline files> (empty) | 0 |
| gh run list / gh run view (read-only, runs 36974560859, 36974565033) | 0 |
| synthetic sed/grep witness of the lint gate (.temp/TASK-261002-2whb08-gate) | 0 |
| bash witness of the Verify step regex (4 inputs) | 1,1,1,0 (as designed) |

## Round-1 findings: fixed correctly?
- F1 lint warnings not failing — FIXED. `--message-format=short --color never` + `tee` under `set -o pipefail`; warnings parsed as `path: warning: msg`, distinct set diffed against KNOWN_WARNINGS (exact-line `grep -x -F`). Hosted: stack-5 lint job (success) logs `clippy warnings: 3 distinct, 3 of them upstream baseline`; negative control run 36974565033 lint job `failure` with `clippy warnings outside the upstream baseline: tools/src/lib.rs: warning: unused import ...ReluxCiGateNegativeControl` and exit code 1 (other lanes cancelled on purpose; whole-run conclusion `cancelled`, lint job `failure`). Synthetic witness: a new `unused variable` warning is surfaced, the known one is tolerated, empty known/warnings sets do not crash (rc=1 absorbed by `|| true`). The 3 KNOWN_WARNINGS lines exist at upstream pin 0462dcc (registry.rs:16, openai_file_mcp.rs:47, scenarios.rs:42) and those 3 files are unchanged between 0462dcc and the candidate (empty diff stat), so they are upstream baseline, not introduced by the series.
- F2 inputs.sha not verified — FIXED. New step "Verify the checked-out commit" (every lane, before any build step): `WANT_SHA` passed via env (no injection), must match `^[0-9a-f]{40}$` and `git rev-parse HEAD` must equal it. Bash witness: branch name, 7-char abbrev and uppercase hex are rejected with exit 1; a full lowercase sha is accepted. Hosted: step passed in all 4 lanes of run 36974560859 (WANT_SHA=ea8899e...).
- push-concurrency-cross-sha — FIXED. Group is `relux-ci-${{ inputs.sha || github.sha }}`; push resolves to the exact commit, so distinct SHAs on one selftest ref no longer share a group and push+dispatch of one SHA share one. No other `github.ref` fallback remains in a gating position (`github.ref_name` appears only in run-name label).

## Same class elsewhere / rework regressions
- grep of the candidate for `github.ref`, `inputs.`, `continue-on-error`, `|| true`, `self-hosted`, `secrets.`, `pull_request`, `uses:`: only run-name (label), concurrency, checkout ref, WANT_SHA env use inputs/github; the only masking is the cache-save step and the two `|| true` on disk cleanup and `sccache --show-stats`. All 6 third-party `uses:` are 40-hex SHAs. No new interpolation into `run:` bodies. The rework did not touch the lane/matrix/nextest filter definitions (diff vs round 1 is only concurrency, Verify step, lint env+script).

```verdict-findings
{
  "findings": [],
  "notes": [
    "[2whb08] static-only bound: no cargo/just/build/hosted dispatch run by this panel; execution evidence is the attached hosted runs 36974560859 (push, ea8899e, tree 429a14a, all 4 lanes success; core 4854/4854 with 11 skipped = 8 default + 3 exclusions; app-server 1827/1827) and 36974565033 (negative control), both read back via gh read-only and matching the producer's tables.",
    "[2whb08] gate parse bound (unproven, not a finding): the warning extractor matches only `path:L:C: warning: ...`. Synthetic input shows `path:L:C: warning[E0133]: ...` (coded rustc warning) and span-less warnings (cargo:warning lines) do not enter the distinct set and cannot fail the lane. Clippy lint warnings carry no code, and no hosted evidence of a coded warning in this tree exists, so reachability is unproven; stated as a coverage bound. A hardened regex would be `warning(\\[[A-Z0-9]+\\])?: `.",
    "[2whb08] baseline identity is path+message, not line: a second new warning with an identical message in the same file as a baseline entry is deduplicated by `sort -u` and tolerated. Negligible for the three current entries.",
    "[2whb08] workflow_dispatch path has no hosted execution: gh run list shows only push-triggered runs (stack-1..5, neg-1, bootstrap/uv). The dispatch-specific expressions (inputs.sha in checkout ref, concurrency, WANT_SHA) are the same expressions exercised via the github.sha fallback; the full-40-hex checkout-by-SHA is standard actions/checkout behaviour but was not exercised here. Orchestrator should make the first real evidence run a dispatch and check the run-name/Verify step.",
    "[2whb08] AC text on TASK-261002-1ugz6h is stale for rev 2: AC1 says the candidate adds only relux-ci.yml with the blob of 7ae33a0 and AC4 cites run 36963367409. The rev-2 file blob is e79341df (7ae33a0 has aa604b6c) because of the round-1 fixes, and the story-final candidate is cumulative (2 astra snapshots from leaf 1 + the workflow). The proper evidence is run 36974560859 for tree 429a14a. Recording reviewer should judge AC1/AC4 against the cumulative scope and the new run, not the literal old text.",
    "[2whb08] a second dispatch of the same SHA (different label) or a push+dispatch of one SHA cancels the in-flight run (cancel-in-progress, shared group). Fail-safe (cancelled is not green) and matches the 'one group per SHA' invariant.",
    "[2whb08] composite actions ./.github/actions/* execute from the checked-out candidate tree, while the workflow file comes from the dispatched/pushed ref; inherent to the design, reviewed in round 1, not part of this delta."
  ],
  "surface_results": [
    {
      "row": "trigger and permission safety",
      "result": "held",
      "evidence": "on: workflow_dispatch + push branches ci/relux-ci-selftest/** only; permissions contents: read; runs-on ubuntu-24.04; no secrets. reference; no pull_request/pull_request_target/issue events; 6/6 third-party uses pinned to 40-hex SHAs; inputs.sha/inputs.label/github.* only reach run-name, concurrency group, checkout ref, cache key and an env var (WANT_SHA), never a run: body. The delta added only the Verify step (env-passed) and the lint script (no expression interpolation)."
    },
    {
      "row": "evidence exactness",
      "result": "held",
      "evidence": "checkout ref = inputs.sha || github.sha; Verify step rejects non-40-hex/uppercase/branch inputs (witness exits 1,1,1; full sha exit 0) and asserts HEAD == WANT_SHA in every lane; run-name carries the SHA; concurrency group relux-ci-<inputs.sha||github.sha> (round-1 cross-SHA collision fixed); no continue-on-error or || true on any test/build/lint step; lint gate fails the job on new warnings (negative control run 36974565033: lint job failure, exit code 1)."
    },
    {
      "row": "lane coverage",
      "result": "held",
      "evidence": "unchanged from round 1 except the lint step: lint = fmt-check + clippy on exactly the 6 crates, now gated on warnings outside the 3-entry upstream baseline (entries verified at pin 0462dcc, files unchanged since); small = 4 crates; core = just test -p codex-core with only the 3 zsh-fork exact-name exclusions after helper binaries; app-server = full suite after helper binaries; matrix/if names match; NEXTEST_RETRIES=2 only reruns failures. Hosted counts for the exact tree match the producer's table. Coverage bound: see gate parse bound note."
    }
  ],
  "free_hunt": [
    "bash -e (no pipefail by default on GitHub): the lint script sets pipefail only after fmt-check, and clippy|tee runs under pipefail, so a clippy compile error fails the step; the gate pipeline's grep non-matches are guarded with || true and the sed/sort chain cannot return non-zero. Held.",
    "known-warnings file built with `printf '%s\\n' | sed '/^$/d'`; an empty KNOWN_WARNINGS would not crash grep -f (empty pattern file matches nothing) — witnessed.",
    "grep -c ... || true prints `0` once on no match (grep -c prints the count, `true` only masks the exit status), so the count line is well-formed.",
    "snapshots: byte-identical blobs to checkpoint ec6a700; checkpoint is a descendant of the base; candidate diff against the checkpoint is exactly the workflow file.",
    "cache keys use github.run_id plus lane/Cargo.lock hash, restore-keys fall back by lane; sccache is content-addressed; permissions stay contents: read. Nothing new in the delta."
  ]
}
```
