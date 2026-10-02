# TASK-261002-1ugz6h results (rev 2) — fork-only relux-ci workflow

## Summary

Applied the reviewed rev-2 workflow file from orchestrator commit
`ea8899e6f97aea64136159286840c28c955243e8` as the single uncommitted new file
`.github/workflows/relux-ci.yml` (blob `e79341df…`, equal to `ea8899e`'s).
Rev 2 answers all three round-1 findings (F1, F2, push-concurrency-cross-sha).
The hosted selftest of this exact tree (run 36974560859) is green on all four
lanes, and the negative control (run 36974565033) fails the lint lane on the
injected warning as required.

## Changed files

Exactly one new file, left UNCOMMITTED:

- `.github/workflows/relux-ci.yml` (178 lines, blob `e79341df18d478c650667ab663cb1ae2c5fb7f44`)

`git status --short` shows only `?? .github/workflows/relux-ci.yml`.
Tree proof: `ea8899e^` tree == worktree `HEAD` tree (`5c365d9a…`), and the
uncommitted file blob == `ea8899e`'s file blob, so the candidate tree equals
the selftested tree `429a14a2…`.

## Round-1 findings → fixing lines (rev 2)

File: `.github/workflows/relux-ci.yml` (rev-2 line numbers).

- F1 (lint lane ignored plain warnings) → lines 114–135. The `Lint (fmt +
  clippy)` step runs clippy with `--message-format=short --color never`,
  strips ANSI codes, normalizes `file: warning: msg` lines, and fails on any
  warning outside the 3-line upstream baseline in `KNOWN_WARNINGS` (lines
  119–122). Count line at line 131.
- F2 (`inputs.sha` free text) → lines 59–66. The `Verify the checked-out
  commit` step takes the SHA through env `WANT_SHA` (never interpolated),
  requires full 40-hex (line 64), and requires `git rev-parse HEAD` equal to
  it (lines 65–66).
- push-concurrency-cross-sha → lines 25–28. Concurrency group is
  `relux-ci-${{ inputs.sha || github.sha }}`: one group per exact commit for
  dispatch and push alike (rev 1 used `github.ref` as the push fallback).

Rev1→rev2 diff verified: only these three hunks differ between `7ae33a0` and
`ea8899e` for this file.

## AC coverage — 4 of 4 AC rows driven

| AC | Driven by (production call site) |
|---|---|
| AC1: exactly `.github/workflows/relux-ci.yml` with `ea8899e`'s blob, nothing else | `git status --short` (only `??` file) + `git hash-object` == `git rev-parse ea8899e:.github/workflows/relux-ci.yml` (`e79341df…`) |
| AC2: dispatch-exact-sha + selftest-push triggers only; `contents: read`; hosted ubuntu-24.04; SHA-pinned actions | static S1/S1b/S1c, S2, S3, S4, S5/S5b on the file; `actionlint` exit 0; YAML parse OK. Production sites: `on:` (L10–20), `permissions:` (L22–23), `runs-on:` (L45), `uses:` pins (L55,83,87,95,110,171) |
| AC3: checkout exactly `inputs.sha`/`github.sha`; failing suites fail jobs; only the 3 zsh-fork exclusions | static S6, S7, S7b, S8, S9; verify-sha harness T1–T4 executing the exact L64–66 gate; hosted: `Verify the checked-out commit` success in all 4 jobs, `ref: ${{ inputs.sha \|\| github.sha }}` (L57) |
| AC4: hosted selftest of this exact tree green on all four lanes | run 36974560859 (`push`, `ci/relux-ci-selftest/stack-5`, head `ea8899e`): success ×4, table below |

## Coverage map (surface table → tests → killed mutants)

Harness sources: `TASK-261002-1ugz6h_harness.tar.gz` (attached; also replayable
from `/tmp/relux-static-checks.py`, `/tmp/relux-verify-sha-test.sh`,
`/tmp/relux-warning-gate-test.sh`, `/tmp/relux-mut/*.yml` on this machine).

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| trigger and permission safety | S1/S1b/S1c triggers, S2 permissions, S3 runs-on, S4 pins, S5 no-secrets, S5b no-expression-in-run, actionlint | M-trg (+pull_request) → S1 fails; M-perm (contents:write) → S2 fails; M-pin (checkout@v6) → S4 fails; M-interp (`${{ inputs.sha }}` in run:) → S5b fails | pull_request/pull_request_target/issue/fork events → AC2 "Triggers are only…"; self-hosted runners → AC2 "hosted ubuntu-24.04 runners only"; unpinned/tag-pinned actions → AC2 "every third-party action pinned by SHA"; non-default-token secrets → AC2 "read-only default token" |
| evidence exactness | S6 checkout-ref, S7 run-name, S7b concurrency, S8 no-masking; T1–T4 verify-sha harness (exact L64–66 gate); hosted `Verify the checked-out commit` ×4 + run-name/concurrency | M-ref (ref:github.ref) → S6 fails; M-conc (group …github.ref, the rev1 shape) → S7b fails; M-mask (`\|\| true` on small suite) → S8 fails; M-sha-eq (40-hex regex + equality weakened to 7–40-hex + prefix match) → T4 fails (admits short prefix, still rejects non-prefix `deadbee`) | branch/tag/short-SHA dispatch inputs → AC3 "check out exactly inputs.sha" + rev-2 40-hex gate (rejected, never checked out as a moving ref) |
| lane coverage | S9 (6 clippy crates, 4 small crates, helper-bin step present, 3 zsh exclusions); hosted 4-lane green + count line; W1/W2 warning-gate harness (exact L127–135 pipeline on fixture logs) | M-warn-allowlist (new warning added to KNOWN_WARNINGS) → W2 fails; M-no-strip (ANSI-strip sed removed, token `warning` preserved — the c1ace00 shape) → W1 fails; hosted end-to-end narrowing mutant 694b0ed (ea8899e + 1 unused import) → `Lint (fmt + clippy)` step FAILS run 36974565033 naming `tools/src/lib.rs` | the 3 zsh-fork core exclusions → AC3 "the only exclusions are the 3 documented zsh-fork tests"; further clippy-baseline growth → refused (any 4th warning fails the lane) |

## Mutant evidence

Zero survivors. Every mutant below was executed; each names its killing test.

| Mutant | What it narrows the gate to | Named test that fails |
|---|---|---|
| M-trg | trigger set + exactly `pull_request` | S1 triggers exact |
| M-perm | `contents: write` | S2 permissions |
| M-pin | one tag-pinned action (`actions/checkout@v6`) | S4 third-party pins |
| M-interp | one `${{ inputs.sha }}` interpolation in a `run:` block | S5b no expression in run: |
| M-ref | checkout of moving `github.ref` | S6 checkout ref |
| M-conc | per-ref concurrency group (rev1 shape) | S7b concurrency |
| M-mask | `|| true` on the small-crate suite | S8 no masking on test steps |
| M-sha-eq | 7–40-hex + prefix match (admits short-SHA prefixes only) | T4 short-sha prefix rejected |
| M-warn-allowlist | baseline + exactly the new warning line | W2 new warning fails the gate |
| M-no-strip | parser without ANSI stripping, `warning` token preserved | W1 baseline-only log (colored) passes |
| 694b0ed (hosted) | ea8899e tree + 1 unused import | `Lint (fmt + clippy)` in run 36974565033 (FAILED) |

## Hosted selftest of this exact tree — run 36974560859

<https://github.com/relux-works/codex/actions/runs/36974560859>
`push` of `ea8899e6f97aea64136159286840c28c955243e8` to
`ci/relux-ci-selftest/stack-5`. Run conclusion: **success**.

| Lane | Conclusion | Wall time (started → completed UTC) |
|---|---|---|
| lint | success | 10m06s (06:38:56 → 06:49:02) |
| small | success | 10m02s (06:38:56 → 06:48:58) |
| core | success | 24m18s (06:38:57 → 07:03:15) |
| app-server | success | 28m13s (06:38:56 → 07:07:09) |

Lint warning-gate count line (from the completed run log):
`clippy warnings: 3 distinct, 3 of them upstream baseline` — no
"outside the upstream baseline" error. `Verify the checked-out commit`
succeeded in all 4 jobs.

## Negative control — run 36974565033

<https://github.com/relux-works/codex/actions/runs/36974565033>
`push` of `694b0edb1aa2782f0b67c1ba8e94c0ce4cb647ac` (= `ea8899e` + one
`use std::collections::HashMap as ReluxCiGateNegativeControl;` in
`codex-rs/tools/src/lib.rs`; parent verified `ea8899e`, 1 file +1 line).

- lint lane: **failure** (expected). Other lanes cancelled on purpose; run
  conclusion `cancelled`.
- Lint step output (from the run log):
  `tools/src/lib.rs:4:5: warning: unused import:
  \`std::collections::HashMap as ReluxCiGateNegativeControl\``,
  `clippy warnings: 4 distinct, 3 of them upstream baseline`,
  `##[error]clippy warnings outside the upstream baseline:`,
  `tools/src/lib.rs: warning: unused import: …`, exit code 1.

## Commands with real exit codes

| Command | Exit |
|---|---|
| `git checkout ea8899e -- .github/workflows/relux-ci.yml && git reset -q` + blob equality check | 0 (blobs equal `e79341df…`) |
| `python3 -c "import yaml;…safe_load…"` | 0, `YAML OK` |
| `actionlint .github/workflows/relux-ci.yml` | 0, no findings |
| `codex-fix-suite-busy.py --any` (before local validation) | 0, `FREE` |
| `codex-target-guard.sh` | 0, same checkout, cache kept |
| `just fmt-check` (from `codex-rs/`) | 0 |
| `/tmp/relux-verify-sha-test.sh` (T1–T4 + M-sha-eq) | 0, 6 pass / 0 fail |
| `/tmp/relux-warning-gate-test.sh` (W1–W2 + 2 mutants) | 0, 7 pass / 0 fail |
| `/tmp/relux-static-checks.py` on the file (S1–S9) | 0, 0 failures |
| `/tmp/relux-static-checks.py` on each of 7 `/tmp/relux-mut/*.yml` | 1 each, killed by the expected named check |
| `gh run view 36974560859 …` / `--log` | 0 |
| `gh run view 36974565033 …` | 0 |
| `codex-fix-suite-busy.py --any` (pre-handoff) | 0, `FREE` (see below) |

Note: `git fetch origin relux/hosted-ci` failed (ssh publickey in this
environment), but both `ea8899e` and `7ae33a0` objects were already present
locally and every identity used here was verified by hash (`rev-parse`,
`hash-object`, tree OIDs), not by the fetch.

## Stated bounds (not silently waived)

1. No committed repo tests: the leaf scope is exactly one new workflow file,
   so the S/T/W harnesses cannot live in the repo. They are attached as
   `TASK-261002-1ugz6h_harness.tar.gz` for reviewer replay (paths and
   expected exits above).
2. `workflow_dispatch` entry not executed on hosted: GitHub resolves the
   workflow file from the default branch, where it does not exist until this
   leaf lands. The dispatch-only logic (40-hex gate) was executed locally as
   the exact gate body (T1–T4); the push entry was executed hosted in all 4
   jobs.
3. Cross-SHA concurrency cancellation was not executed as a live two-push
   experiment (requires pushing; orchestrator-only). Covered statically: S7b
   asserts the per-SHA group and M-conc (the rev1 `github.ref` shape) is
   killed by S7b.
4. `just clippy`/`just test` suites were not run locally (brief forbids the
   heavy lanes locally; the file change is YAML-only). Evidence for suite
   behavior is the hosted selftest above.

## Out-of-contract rows

None beyond the coverage-map column: every surface row above carries killed
narrowing mutants, and no AC row was left undriven (4 of 4).
