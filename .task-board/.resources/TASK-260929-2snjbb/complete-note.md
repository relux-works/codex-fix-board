# Integration run for STORY-260929-qvqmw2 (p4a-goal-background-wait): run `worktree complete` yourself (tb-R144)

Standing ruling tb-R144 (tb-arbiter, 2026-10-02 03:55Z) covers every landed codex-fix story until BUG-261002-whijfm is
fixed. This board is separate-owner (board repository relux-works/codex-fix-board). The runner's automatic landing runs
`worktree integrate`, which is refused with `board_owner_separate`. So in THIS run you execute `worktree complete`
yourself, once. This overrides the generic integration text that says "the runner lands; do not invoke landing yourself".

The accepted story_final candidate, TASK-260929-2snjbb CR rev 5 with tree 13972f7d936f6280c9b0cae88749c6f5c1a56a9a,
landed on relux/main of relux-works/codex as the signed commit 2f522b9dc9d639fe5195d93d61431a0caff662d5 (fork PR #2,
exact-head fast-forward at 07:38:29Z).

Do exactly this, with no file edits and no builds:
1. Re-check the landing:
   - `git fetch origin relux/main` and `git merge-base --is-ancestor 2f522b9dc9d639fe5195d93d61431a0caff662d5 origin/relux/main` (exit 0);
   - `git rev-parse 2f522b9dc9d639fe5195d93d61431a0caff662d5^{tree}` must print `13972f7d936f6280c9b0cae88749c6f5c1a56a9a`;
   - `git verify-commit 2f522b9dc9d639fe5195d93d61431a0caff662d5` must report a good signature.
   If any check fails, do NOT run complete: attach the output (step 3) and exit.
2. Run exactly:
   `task-board worktree complete STORY-260929-qvqmw2 --cr TASK-260929-2snjbb --revision 5 --landed-commit 2f522b9dc9d639fe5195d93d61431a0caff662d5`
3. Attach a task-scoped outcome `TASK-260929-2snjbb_complete-log.md` with the check outputs, complete's full output and its
   exit code. Then exit.
Do not run `task-board handoff`, `worktree integrate`, `worktree checkpoint` or any other landing or status command. If
complete refuses, attach the refusal verbatim and exit. If it reports a resumable phase (for example
`code_landed_board_pending` or `cleanup_pending`), re-run the same command once and report both outputs.
