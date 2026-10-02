# Integration run for STORY-261002-hep79y (relux-hosted-ci-lanes): run `worktree complete` yourself (tb-R144)

Standing ruling tb-R144 (tb-arbiter, 2026-10-02 03:55Z) covers every landed codex-fix story until BUG-261002-whijfm is
fixed. This board is separate-owner (board repository relux-works/codex-fix-board). The runner's automatic landing runs
`worktree integrate`, which is refused with `board_owner_separate`. So in THIS run you execute `worktree complete`
yourself, once. This overrides the generic integration text that says "the runner lands; do not invoke landing yourself".

The accepted story_final candidate, TASK-261002-1ugz6h CR rev 2 with tree 429a14a27a106f73b5907a0d830c4548cb3f1ea4,
landed on relux/main of relux-works/codex as the signed commit ea8899e6f97aea64136159286840c28c955243e8 (fork PR #2,
exact-head fast-forward at 07:38:29Z).

Do exactly this, with no file edits and no builds:
1. Re-check the landing:
   - `git fetch origin relux/main` and `git merge-base --is-ancestor ea8899e6f97aea64136159286840c28c955243e8 origin/relux/main` (exit 0);
   - `git rev-parse ea8899e6f97aea64136159286840c28c955243e8^{tree}` must print `429a14a27a106f73b5907a0d830c4548cb3f1ea4`;
   - `git verify-commit ea8899e6f97aea64136159286840c28c955243e8` must report a good signature.
   If any check fails, do NOT run complete: attach the output (step 3) and exit.
2. Run exactly:
   `task-board worktree complete STORY-261002-hep79y --cr TASK-261002-1ugz6h --revision 2 --landed-commit ea8899e6f97aea64136159286840c28c955243e8`
3. Attach a task-scoped outcome `TASK-261002-1ugz6h_complete-log.md` with the check outputs, complete's full output and its
   exit code. Then exit.
Do not run `task-board handoff`, `worktree integrate`, `worktree checkpoint` or any other landing or status command. If
complete refuses, attach the refusal verbatim and exit. If it reports a resumable phase (for example
`code_landed_board_pending` or `cleanup_pending`), re-run the same command once and report both outputs.
