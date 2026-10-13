# TASK-261007-3v81ko: hand off CR rev3 on hosted precheck 3

Hosted precheck 3 (`TASK-261007-3v81ko_hosted-precheck-3.md`, precondition) is fully green, and 5/5 mutants are killed, including
stderr_failure_eprintln, by both stderr-failure regression tests.
1. Compute your tree (temp index), then run `git diff --name-only 2f7ec5e30babb9dff4f00132ad9fd384663930b0 <your tree>`. It must print nothing or only `.github/`
   paths. Do NOT change any file. If any other path appears, stop and add a note.
2. Check the open checklist items, citing precheck 3 (run 38038510297) and the review rev2 finding it closes. Refresh and re-attach
   `TASK-261007-3v81ko_results.md`.
3. Run `task-board handoff TASK-261007-3v81ko --role developer` (CR rev3).
