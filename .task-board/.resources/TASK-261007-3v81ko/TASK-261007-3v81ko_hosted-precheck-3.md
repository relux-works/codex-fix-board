# TASK-261007-3v81ko hosted precheck 3 (review rev2 rework)

CI ivanopcode/codex, slim relux-ci run 38038510297: snapshot = worktree tree 2f7ec5e30babb9dff4f00132ad9fd384663930b0. Lanes: {'lint': 'success', 'small': 'success', 'app-server': 'success', 'core': 'success'}. All green; small 932 passed, including cli_exec_stderr_failure_preserves_exit_code and exec_ordinary_error_stderr_failure_preserves_exit_code.

Mutants: 5 total, 5 killed, 0 survivors.

| mutant | failing lanes | killing tests |
|---|---|---|
| empty_stdin_error_prefix | small | exec_empty_stdin_preserves_stderr |
| empty_stdin_process_exit | small | exec_empty_stdin_leaves_no_tmpdirs, exec_empty_stdin_preserves_stderr |
| error_seen_process_exit | small | exec_server_error_leaves_no_tmpdirs, exec_server_error_preserves_stderr |
| exec_parse_exit | small | exec_help_leaves_no_tmpdirs, exec_invalid_args_leave_no_tmpdirs |
| stderr_failure_eprintln | small | cli_exec_stderr_failure_preserves_exit_code, exec_ordinary_error_stderr_failure_preserves_exit_code |
