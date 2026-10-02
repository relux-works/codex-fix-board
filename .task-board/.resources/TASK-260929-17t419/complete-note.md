# Integration run for STORY-260929-2urftk (P1) — R140: run `worktree complete` yourself

Ruling tb-R140 (tb-arbiter, 2026-10-02 03:27Z) — a one-time workaround for the separate-owner complete gap.

This board is separate-owner: the code repository is relux-works/codex, and the board lives in its own
repository (relux-works/codex-fix-board). Last time the runner's automatic landing ran `worktree integrate` and was
refused with `board_owner_separate` (RUN-260930-e0c3b9), because the runner never routes to `worktree complete`.
So in THIS run, ignore the generic integration text "the runner lands; do not invoke landing yourself" as far as
`worktree complete` goes: per the ruling, you run it yourself, once, inside this tracked run.

The accepted story_final candidate (TASK-260929-17t419 CR rev 6, tree ece69834ba82a0aa95440f5ecc4eedf9f894b9ab)
already landed on the protected default `relux/main` of relux-works/codex as the signed commit
35af013b901ed4be1b88416068f140e9ca5cc85d (fork PR #1, exact-head fast-forward).

Do exactly this (no file edits, no builds, no tests):
1. Re-check the landing, from your worktree:
   - `git fetch origin relux/main` and `git merge-base --is-ancestor 35af013b901ed4be1b88416068f140e9ca5cc85d origin/relux/main` (exit 0);
   - `git rev-parse 35af013b901ed4be1b88416068f140e9ca5cc85d^{tree}` must print `ece69834ba82a0aa95440f5ecc4eedf9f894b9ab`;
   - `git verify-commit 35af013b901ed4be1b88416068f140e9ca5cc85d` must report a good signature.
   If any check fails, do NOT run complete: attach the output (step 3) and exit.
2. Run exactly:
   `task-board worktree complete STORY-260929-2urftk --cr TASK-260929-17t419 --revision 6 --landed-commit 35af013b901ed4be1b88416068f140e9ca5cc85d`
3. Attach a task-scoped outcome `TASK-260929-17t419_complete-log.md` with the check outputs, the full output of
   complete and its exit code. Then exit.

Do not run `task-board handoff`, `worktree integrate`, `worktree checkpoint` or any other landing or status command.
If complete refuses, do not work around it: attach the refusal verbatim and exit. If it reports a resumable phase
(for example `code_landed_board_pending` after a refused push), re-run the same command once and report both outputs.
