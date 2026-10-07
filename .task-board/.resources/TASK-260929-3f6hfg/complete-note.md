# Integration run for STORY-260929-2opthd (p5-p4a-activation): run `worktree complete` yourself (tb-R144)

Standing ruling tb-R144 (tb-arbiter, 2026-10-02 03:55Z) covers every landed codex-fix story until BUG-261002-whijfm is
fixed. This board is separate-owner (board repository relux-works/codex-fix-board). The runner's automatic landing runs
`worktree integrate`, which is refused with `board_owner_separate`. So in THIS run you execute `worktree complete`
yourself, once. This overrides the generic integration text that says "the runner lands; do not invoke landing yourself".

The accepted story_final candidate, TASK-260929-3f6hfg CR rev 1 with tree c83869e576d1e024cfdbb5f63cfe8b83c6e969cb,
landed on relux/main of relux-works/codex as the signed commit 39c264c34e61b5171ae13b0f756746c24ea5f51a (fork PR #2,
exact-head fast-forward at 07:38:29Z).

Do exactly this, with no file edits and no builds:
1. Re-check the landing:
   - `git fetch origin relux/main` and `git merge-base --is-ancestor 39c264c34e61b5171ae13b0f756746c24ea5f51a origin/relux/main` (exit 0);
   - `git rev-parse 39c264c34e61b5171ae13b0f756746c24ea5f51a^{tree}` must print `c83869e576d1e024cfdbb5f63cfe8b83c6e969cb`;
   - `git verify-commit 39c264c34e61b5171ae13b0f756746c24ea5f51a` must report a good signature.
   If any check fails, do NOT run complete: attach the output (step 3) and exit.
2. Run exactly:
   `task-board worktree complete STORY-260929-2opthd --cr TASK-260929-3f6hfg --revision 1 --landed-commit 39c264c34e61b5171ae13b0f756746c24ea5f51a`
3. Attach a task-scoped outcome `TASK-260929-3f6hfg_complete-log.md` with the check outputs, complete's full output and its
   exit code. Then exit.
Do not run `task-board handoff`, `worktree integrate`, `worktree checkpoint` or any other landing or status command. If
complete refuses, attach the refusal verbatim and exit. If it reports a resumable phase (for example
`code_landed_board_pending` or `cleanup_pending`), re-run the same command once and report both outputs.
