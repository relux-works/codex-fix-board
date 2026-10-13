# TASK-261007-3v81ko: hand off CR rev2 on hosted precheck 2

Hosted precheck 2 (`TASK-261007-3v81ko_hosted-precheck-2.md`, precondition) is fully green, and 4/4 mutants are killed, including
empty_stdin_error_prefix (stderr preserved) and exec_parse_exit (help and invalid args leave no tmpdirs).
1. Compute your tree (temp index), then run `git diff --name-only ca07d336e99eb0ddcb15a180bbaaaf2a45388835 <your tree>`. It must print nothing or only paths
   under `.github/` (CI-only trunk commits). Do NOT change any file. If any other path appears, stop and add a note.
2. Check the open checklist items, citing precheck 2 (run 38021154057) and each review rev1 finding it closes (A-F1..A-F4).
   Refresh and re-attach `TASK-261007-3v81ko_results.md`.
3. Run `task-board handoff TASK-261007-3v81ko --role developer` (CR rev2).
