# [CLI] `codex exec` leaves `.tmpXXXXXX` directories in `$TMPDIR` after every run

Template: 3-cli.yml (Codex CLI bug)

### What version of Codex CLI is running?

`codex-cli 0.159.0`

### What subscription do you have?

<!-- fill in -->

### Which model were you using?

Default model for `codex exec`, run with `-c model_reasoning_effort=low`. The leak does not seem to depend on the model.

### What platform is your computer?

macOS 27.0, arm64 (Apple Silicon)

### What terminal emulator and version are you using (if applicable)?

Not interactive. `codex exec` runs headless from automation (scripted agent runs) and from a plain zsh shell.

### Codex doctor report

<!-- fill in: output of `codex doctor` -->

### What issue are you seeing?

Every non-interactive `codex exec` run leaves several `.tmpXXXXXX` directories in `$TMPDIR` (on macOS `/var/folders/.../T/`). Nothing removes them when the process exits. They accumulate without bound on hosts that run `codex exec` often.

The leftovers look like a throw-away Codex home or state directory:

- several directories that contain only an empty `thread-writer-locks/`;
- one directory with a full set of state databases: `goals_1.sqlite`, `logs_2.sqlite`, `memories_1.sqlite`, `queue_1.sqlite`, `state_5.sqlite`, each with its `-wal` and `-shm`;
- some empty directories;
- on other leftovers, `sessions/`, `skills/`, `cache/` or `shell_snapshots/`.

No process holds any of them open after `codex exec` exits (`lsof +D` shows nothing).

**How we found it:** two machines running automated agent workloads lost free disk space faster than their workloads could explain. `$TMPDIR` turned out to hold tens of thousands of `.tmpXXXXXX` directories.

**Measurements.** These are counts of all `.tmp*` directories in `$TMPDIR`, so they may include directories from other sources. A controlled single-run reproduction is below.

| Host | `.tmp*` dirs | with `thread-writer-locks/` | with `*.sqlite` state | Allocated size | Period |
|---|---:|---:|---:|---:|---|
| A (macOS arm64) | 38,145 | 29,459 | 1,186 | 2.87 GiB | about 9 days (Sep 29 to Oct 7) |
| B (macOS arm64) | 36,245 | n/a | n/a | 5.6 GiB | about 2 weeks |

On host A, about 140 `codex exec` agent runs were made through our automation over the same period. At 8 directories per run (see the reproduction), that explains about 1,100 of the leftovers. The rest probably comes from other `codex exec` users on the same machine and from other code paths that create the same temporary home layout, such as interrupted test processes. We have not attributed them separately. The single-run reproduction below is unambiguous, though.

### What steps can reproduce the bug?

```sh
# 1. Snapshot the temporary directories
python3 -c "import os;t=os.environ['TMPDIR'];print('\n'.join(sorted(n for n in os.listdir(t) if n.startswith('.tmp'))))" > before.txt

# 2. Run one trivial non-interactive exec (stdin closed)
codex exec --skip-git-repo-check -c model_reasoning_effort=low "Reply with exactly: ok" </dev/null

# 3. Snapshot again and diff
python3 -c "import os;t=os.environ['TMPDIR'];print('\n'.join(sorted(n for n in os.listdir(t) if n.startswith('.tmp'))))" > after.txt
comm -13 before.txt after.txt          # new leftovers
for d in $(comm -13 before.txt after.txt); do ls -A "$TMPDIR/$d"; done
```

Observed after one successful run (exit 0; the model replied `ok`). 8 new directories were left behind and were still present 20+ seconds later, with no open handles:

```text
.tmpRLmWwe  thread-writer-locks
.tmpRLqT1u  thread-writer-locks
.tmpRLsJGR  thread-writer-locks
.tmpRLtOgN  thread-writer-locks
.tmpRLtTSi  thread-writer-locks
.tmpRLwjqY  goals_1.sqlite(+wal,shm) logs_2.sqlite(+wal,shm) memories_1.sqlite(+wal,shm)
            queue_1.sqlite(+wal,shm) state_5.sqlite(+wal,shm)   ~2.6 MB
.tmpRLXGK7  (empty)
.tmpXeQPPT  (empty)
```

Note: without `</dev/null`, `codex exec` waits for "additional input from stdin". This is unrelated, but it can confuse scripted reproductions.

### What is the expected behavior?

Temporary directories that `codex exec` creates for its own use should be removed when the process exits, whether it exits successfully, with an error, or on a signal where possible. Running `codex exec` N times should not leave N × 8 directories behind. If state in a temporary location is meant to persist, it should go to a documented location under `CODEX_HOME`, not into anonymous `$TMPDIR/.tmpXXXXXX` directories.

### Additional information

- The `.tmpXXXXXX` naming matches the Rust `tempfile` crate. This suggests `TempDir` or `tempdir()` handles are persisted, leaked or forgotten (for example `into_path()` / `keep()` / `mem::forget`) instead of being dropped, or that the process exits before destructors run.
- Each directory is small, but the inode count and the per-directory allocation add up. One host reached 5.6 GiB, another 2.87 GiB, and both have tens of thousands of entries, which slows down any tooling that lists `$TMPDIR`.
- macOS clears `/var/folders/.../T` only on some reboots, so long-running build or agent machines are affected the most.
- Current workaround: periodically delete stale `$TMPDIR/.tmp*` directories that contain `thread-writer-locks/` and are older than the longest expected run.
