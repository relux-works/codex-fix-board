# TASK-261002-1ugz6h: relux-ci-workflow-and-fork-settings

## Description
relux-ci.yml (lint, small crates, codex-core, codex-app-server on ubuntu-24.04; dispatch by exact SHA; selftest push on ci/relux-ci-selftest/**), all 29 upstream workflows disabled in the fork, Actions enabled with a read-only default token. Orchestrator inline work, validated by a selftest run on relux/main code, landed on relux/main via a fork PR.

## Scope
One new file .github/workflows/relux-ci.yml (fork-only; never upstream). No other repository change.

## Acceptance Criteria
1. The candidate adds exactly .github/workflows/relux-ci.yml with the blob of signed commit 7ae33a0 and nothing else. 2. Triggers are only workflow_dispatch (exact sha input) and push on ci/relux-ci-selftest/**; permissions contents: read; hosted ubuntu-24.04 runners only; every third-party action pinned by SHA. 3. Jobs check out exactly inputs.sha or github.sha; failing suites fail their job; the only exclusions are the 3 documented zsh-fork tests in the core lane. 4. The hosted selftest of this exact tree (run 36963367409) is green on all four lanes.
