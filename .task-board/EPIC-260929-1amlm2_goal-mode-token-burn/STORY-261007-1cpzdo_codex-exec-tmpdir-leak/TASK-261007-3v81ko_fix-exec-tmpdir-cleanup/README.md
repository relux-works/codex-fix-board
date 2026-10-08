# TASK-261007-3v81ko: fix-exec-tmpdir-cleanup

## Description
Fix: `codex exec` leaves .tmpXXXXXX directories in $TMPDIR after every run (codex-cli 0.159.0, macOS arm64). PRIORITY: start right after the current 10-PR goal-burn series (P4c, P4b, P3) is landed. Verified on ivmbp 2026-10-07: one `codex exec --skip-git-repo-check "Reply with exactly: ok" </dev/null` leaves 8 new dirs (5 with an empty thread-writer-locks/, 1 with goals_1/logs_2/memories_1/queue_1/state_5 sqlite and their wal/shm, about 2.6 MB, 2 empty), none held open. Host totals: 38,145 .tmp* dirs, 29,459 with thread-writer-locks, 1,186 with sqlite, 2.87 GiB allocated; another host has 36,245 dirs and 5.6 GiB. Upstream-style issue draft: .temp/goal-token-burn/impl/codex-exec-tmpdir-leak-issue.md (also ~/Downloads). Scope: find every tempfile TempDir/tempdir() created on the exec path (temporary CODEX_HOME/state dir, thread-writer-locks, sqlite state runtime) and make sure each is dropped or removed on every exit path: success, error and signal where feasible. No into_path/keep/forget leaks, and no early process::exit that skips destructors. Add a regression test that runs the exec entry point in-process (or the binary in a test) with an isolated TMPDIR and asserts it is empty afterwards. Fork-only landing first; the upstream PR is Ivan's decision.

## Scope
(define task scope)

## Acceptance Criteria
AC1 Repro: N exec runs with an isolated TMPDIR leave 0 .tmp* dirs (was 8 per run). AC2 The cleanup covers success and error exits (and a signal or abort path where feasible; state a bound otherwise). AC3 A regression test fails on the current behavior (narrowing mutant: re-introduce the leak at one site). AC4 No change to where persistent state lives under CODEX_HOME. AC5 The hosted relux-ci lanes are green.
