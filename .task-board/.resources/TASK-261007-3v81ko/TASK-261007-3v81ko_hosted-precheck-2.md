# TASK-261007-3v81ko hosted precheck 2 (review rev1 rework)

CI ivanopcode/codex, slim relux-ci run 38021154057: snapshot = worktree tree ca07d336e99eb0ddcb15a180bbaaaf2a45388835. Lanes: {'lint': 'success', 'core': 'success', 'app-server': 'success', 'small': 'success'}. All green (the small lane now includes codex-exec, codex-arg0 and codex-cli).

Mutants: 4 total, 4 killed, 0 survivors.

| mutant | failing lanes | killing tests |
|---|---|---|
| empty_stdin_error_prefix | small | exec_empty_stdin_preserves_stderr |
| empty_stdin_process_exit | small | exec_empty_stdin_leaves_no_tmpdirs, exec_empty_stdin_preserves_stderr |
| error_seen_process_exit | small | exec_server_error_leaves_no_tmpdirs, exec_server_error_preserves_stderr |
| exec_parse_exit | small | exec_help_leaves_no_tmpdirs, exec_invalid_args_leave_no_tmpdirs |
