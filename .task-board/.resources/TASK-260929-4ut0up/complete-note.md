# Integration run for STORY-260929-wg1ya0 (p5-completion-receipts): run `worktree complete` yourself (tb-R144)

Standing ruling tb-R144 (tb-arbiter, 2026-10-02 03:55Z) covers every landed codex-fix story until BUG-261002-whijfm is
fixed. This board is separate-owner (board repository relux-works/codex-fix-board). The runner's automatic landing runs
`worktree integrate`, which is refused with `board_owner_separate`. So in THIS run you execute `worktree complete`
yourself, once. This overrides the generic integration text that says "the runner lands; do not invoke landing yourself".

The accepted story_final candidate, TASK-261002-1ugz6h CR rev 2 with tree 7de6b3c2ed82f07002c613263cd650cc16b20108,
landed on relux/main of relux-works/codex as the signed commit 729f259e62a8d11d9e17398e487790e1ee5d8b8c (fork PR #2,
exact-head fast-forward at 07:38:29Z).

Do exactly this, with no file edits and no builds:
1. Re-check the landing:
   - `git fetch origin relux/main` and `git merge-base --is-ancestor 729f259e62a8d11d9e17398e487790e1ee5d8b8c origin/relux/main` (exit 0);
   - `git rev-parse 729f259e62a8d11d9e17398e487790e1ee5d8b8c^{tree}` must print `7de6b3c2ed82f07002c613263cd650cc16b20108`;
   - `git verify-commit 729f259e62a8d11d9e17398e487790e1ee5d8b8c` must report a good signature.
   If any check fails, do NOT run complete: attach the output (step 3) and exit.
2. Run exactly:
   `task-board worktree complete STORY-260929-wg1ya0 --cr TASK-260929-4ut0up --revision 1 --landed-commit 729f259e62a8d11d9e17398e487790e1ee5d8b8c`
3. Attach a task-scoped outcome `TASK-260929-4ut0up_complete-log.md` with the check outputs, complete's full output and its
   exit code. Then exit.
Do not run `task-board handoff`, `worktree integrate`, `worktree checkpoint` or any other landing or status command. If
complete refuses, attach the refusal verbatim and exit. If it reports a resumable phase (for example
`code_landed_board_pending` or `cleanup_pending`), re-run the same command once and report both outputs.
