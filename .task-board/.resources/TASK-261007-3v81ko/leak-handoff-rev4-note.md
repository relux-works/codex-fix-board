# TASK-261007-3v81ko: publish CR rev4 (the landed tree) by handoff only

The landed-tree rework is applied: the Story worktree tree is bde782b85ddbc8536536d0747b3917d0f24e1951, the tree of the landed
commit e0eff057, which equals the accepted rev3 tree plus the CI-only relux-ci.yml hunk. CR rev4 has not been published yet.
1. Verify: from the Story worktree root, `/Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh`
   exits 0, and the temp-index tree equals bde782b85ddbc8536536d0747b3917d0f24e1951. Change NO files.
2. Run `task-board handoff TASK-261007-3v81ko --role developer`. Expect CR rev4.
3. Stop. Do not run integrate, complete or checkpoint. If the handoff refuses, attach its output verbatim.
