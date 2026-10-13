# TASK-260929-csyzcj: hand off the next CR revision on hosted precheck 15

Hosted precheck 15 (`TASK-260929-csyzcj_hosted-precheck-15.md`, precondition, run 38109158922) is fully green, and all 12 mutants are killed by their named tests.
It closes review rev4's legacy-agent-path-resume-regression / persisted-agent-path-caps-break-resume (caps only on new identities via join_new; legacy paths parse byte-identically; display-only truncation of the envelope).
Mention the orchestrator test-only fix (TASK-260929-csyzcj_orch-test-fix-13.md: the legacy resume test resumes with a ThreadSpawn source) and that precheck 15 ran from relux/ci-next, whose small lane adds codex-protocol and codex-rollout (precheck 14 had not run those crates).
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0. Do NOT change any file. If it fails, stop and add a note.
2. Check the open checklist items, citing precheck 15 and the findings it closes. Refresh and re-attach `TASK-260929-csyzcj_results.md`.
3. Run `task-board handoff TASK-260929-csyzcj --role developer`.
