# TASK-261007-3v81ko hosted precheck 1

CI: ivanopcode/codex, slim relux-ci (one run per precheck). Run 38009138137, snapshot wip-1 bd805b90 = worktree tree
73c75aedfa7434b0d04cd54c83b062532d9d24dd (includes the orchestrator's rustfmt pass, see leak-orch-fmt.md).
Snapshot lanes: lint success, small success (codex-exec 433/433, including suite::tmpdir_cleanup::exec_success_leaves_no_tmpdirs,
exec_empty_stdin_leaves_no_tmpdirs and exec_server_error_leaves_no_tmpdirs), core success, app-server success.

Mutants: 2 total, 2 killed, 0 survivors (lanes small+core, test filter `test(tmpdir_cleanup) | test(tmpdir)`).

| mutant | failing lane | killing test |
|---|---|---|
| empty_stdin_process_exit | small | exec_empty_stdin_leaves_no_tmpdirs |
| error_seen_process_exit | small | exec_server_error_leaves_no_tmpdirs |
