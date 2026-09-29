# Republish brief — Change Request revision 3 of TASK-260929-1srn2y (mechanical)

Revision 2 (the consolidated final plan, outcome `TASK-260929-1srn2y_goal-token-burn-final-plan.md`,
SHA-256 `e25bfd07e8e2559570b67e37d98653c3537a1cac34039ffee938796bd6e0f4a0`, 44720 bytes) went `stale` for a
reason unrelated to its content: the Story workspace record kept `current_base_oid` at `88e9a83` while
publication moved the checkpoint to trunk `bfdb157`, so the CR counted 44 upstream trunk paths
(`git diff 88e9a83..bfdb157`) as producer delta. The research producer changed no repository file. The
orchestrator ran `task-board worktree converge STORY-260929-2jpu1q`; base and checkpoint are now the same trunk
commit and the worktree is clean.

Your only job is to republish the unchanged candidate as revision 3 with an empty repository delta:

1. Do not edit the final plan and do not change any repository file. Confirm `git status --porcelain` is empty
   in your worktree before and after.
2. Confirm the final plan resource on this task still has the SHA-256 above (`task-board resource get` to a
   scratch path outside tracked sources, then `shasum -a 256`).
3. Attach one new short outcome, `TASK-260929-1srn2y_republish-rev3-note.md`, stating: revision 3 republishes the
   revision-2 final plan unchanged (give the digest), why revision 2 went stale (above), and the two checks you
   ran with their exit codes.
4. Hand off: `task-board handoff TASK-260929-1srn2y --role researcher`.

Budget: 10 minutes. English.
