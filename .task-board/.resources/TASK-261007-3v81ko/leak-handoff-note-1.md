# TASK-261007-3v81ko: hand off on hosted precheck 1

Hosted precheck 1 (`TASK-261007-3v81ko_hosted-precheck-1.md`, precondition) ran your exact worktree tree
73c75aedfa7434b0d04cd54c83b062532d9d24dd. All four lanes are green, the 3 new codex-exec tests pass, and both mutants are killed.
The tree includes the orchestrator's whitespace-only rustfmt pass (`leak-orch-fmt.md`); mention it in your results.
1. Confirm the worktree tree still equals 73c75aedfa7434b0d04cd54c83b062532d9d24dd (temp index: `git read-tree HEAD`, `git add -A`,
   `git write-tree`). Do NOT change any file. If it differs, stop and add a note.
2. Check the open checklist items, citing precheck 1. Refresh and re-attach `TASK-261007-3v81ko_results.md` (a new outcome is
   required). AC2: state the signal/abort path bound explicitly.
3. Mac mini: no busy check, no local build. Run `task-board handoff TASK-261007-3v81ko --role developer`. The landing gate is
   mini-hosted-gate.sh, and it passes for this recorded green tree.
