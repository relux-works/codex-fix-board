# TASK-260929-3ld28o: republish the accepted tree as CR rev4 (lifecycle repair, no code change)

CR rev3 (tree 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7) was unanimously accepted by 3/3 panels, but the first recording run refused
an incomplete merge (r141-merge.py flattened note findings) and left rev3 at changes_requested, which is immutable
(TASK-260929-3ld28o_recording-lifecycle-refusal-rev3.md). The merge is fixed and verified
(TASK-260929-3ld28o_recording-review-audit-rev3.md). Republish the SAME tree so the corrected verdict can be recorded on an admissible revision.
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must
   exit 0, and your temp-index tree must equal 486ebfe55fd1df2cbb3d4744e15150ef2c85e9c7. Do NOT change any file. If not, stop and add a note.
2. Re-attach `TASK-260929-3ld28o_results.md` unchanged except a line: "rev4 = rev3 tree republished for lifecycle repair; evidence:
   TASK-260929-3ld28o_hosted-precheck-7.md, TASK-260929-3ld28o_review-verdict-rev3.md".
3. Run `task-board handoff TASK-260929-3ld28o --role developer` (CR rev4).
