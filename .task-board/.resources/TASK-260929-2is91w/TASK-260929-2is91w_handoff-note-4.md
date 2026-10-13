# TASK-260929-2is91w: hand off CR rev1 on hosted precheck 4

Hosted precheck 4 (`TASK-260929-2is91w_hosted-precheck-4.md`, precondition, run 38040774172) is fully green, and every mutant is killed by its named tests.
Mention the orchestrator's edits (a1-orch-compile-fix.md: is_some_and and a rustfmt pass). Note the change size for reviewers.
1. From your Story worktree root, run `/Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh`.
   It must exit 0. It accepts the exact green tree, a .github-only difference, or the same candidate patch replayed on a newer
   trunk that did not touch your paths, which is your case after the refresh onto e0eff057. Do NOT change any file. If it refuses,
   stop and add a note with its output.
2. Check the open checklist items, citing precheck 4 and the findings it closes. Refresh and re-attach `TASK-260929-2is91w_results.md`.
3. Run `task-board handoff TASK-260929-2is91w --role developer` (CR rev1).
