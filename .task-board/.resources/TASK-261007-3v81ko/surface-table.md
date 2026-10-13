# Surface table — TASK-261007-3v81ko fix-exec-tmpdir-cleanup

| Row | Invariant | Attack families |
|---|---|---|
| tmpdir cleanup on every exit | every TempDir/tempdir created on the codex exec path (temporary CODEX_HOME/state, thread-writer-locks, sqlite state runtime) is dropped or removed on success, error and empty-stdin exits; N runs with an isolated TMPDIR leave 0 .tmp* dirs (AC1, AC2) | a remaining process::exit that skips destructors; into_path/keep/forget leaks; a TempDir owned by a detached task or static; an early return path not covered by a test |
| exit status and observable behavior | removing the process::exit calls preserves every exit code, stdout/stderr output and ordering, including error exits and empty stdin (no behavior change besides cleanup) | an exit path that now returns 0 instead of non-zero; error text lost or reordered; buffered output not flushed; a path that now hangs instead of exiting |
| signal and abort bound | the signal/abort path is either covered or stated as an explicit bound in the results (AC2) | an unstated SIGINT/SIGTERM leak; a claim of coverage without a test |
| persistent state unchanged | nothing under CODEX_HOME moves or is deleted; only temporary dirs are cleaned (AC4) | cleanup deleting persistent state; a temp dir that is actually a persistent location |
| regression test and mutants | the regression tests fail on the old behavior; each narrowing mutant re-introduces the leak at one site and is killed (AC3) | a test that passes on both; an isolated TMPDIR not actually used by the child; a mutant killed for an unrelated reason |

```surface-table
{"rows": ["tmpdir cleanup on every exit", "exit status and observable behavior", "signal and abort bound", "persistent state unchanged", "regression test and mutants"]}
```
