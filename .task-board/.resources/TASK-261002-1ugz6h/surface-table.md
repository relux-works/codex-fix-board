# Surface table — TASK-261002-1ugz6h relux-ci-workflow-and-fork-settings

| Row | Invariant | Attack families |
|---|---|---|
| trigger and permission safety | runs only on workflow_dispatch and on push to ci/relux-ci-selftest/**; never on pull_request, pull_request_target, issue or fork events; `permissions: contents: read`; uses no secrets beyond the default token; GitHub-hosted runners only (public fork); every third-party action pinned by full SHA | event list, permissions, `runs-on` labels, secrets/env references, unpinned `uses:`, script injection through `inputs.*` or `github.*` interpolated into `run:` |
| evidence exactness | every job checks out exactly `inputs.sha` (dispatch) or `github.sha` (push); run-name carries that SHA so a dispatched run can be found; one concurrency group per SHA; a failing suite fails its job | checkout `ref`, run-name, concurrency key collisions, `continue-on-error` or `|| true` masking test exits |
| lane coverage | lint = fmt-check + clippy on the 6 series crates; small = the 4 small crates; core and app-server run their full suites after building the helper binaries; the only exclusions are the 3 zsh-fork tests in the core lane, each documented with evidence | nextest filter expression scope, missing helper binaries, matrix/if mismatches, retries hiding deterministic failures (NEXTEST_RETRIES=2 only reruns failures) |

```surface-table
{"rows": ["trigger and permission safety", "evidence exactness", "lane coverage"]}
```
