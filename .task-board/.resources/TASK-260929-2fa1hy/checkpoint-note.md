# Integration (checkpoint) run — TASK-260929-2fa1hy (G1), accepted CR rev 1

CR-TASK-260929-2fa1hy-1 (candidate tree 403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd) was accepted under tb-R141. G1 is NOT
the Story's final leaf (TASK-260929-2gp04j / G2 follows), so the runner CHECKPOINTS it onto the Story branch after you exit.
Do this, with no file edits and no builds:
1. Confirm `git status --short` shows exactly the 5 G1 paths, and that a temporary-index `git write-tree` of the worktree
   equals 403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd.
2. Attach a short outcome `TASK-260929-2fa1hy_checkpoint-preconditions.md` with those outputs, then exit.
Do not run `task-board handoff`, `worktree checkpoint` or `worktree integrate` yourself.
