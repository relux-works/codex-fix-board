# Integration run for STORY-261007-1cpzdo (codex-exec-tmpdir-leak): run `worktree complete` yourself (tb-R144)

Standing ruling tb-R144 covers every landed codex-fix story. This board is separate-owner (board repository
relux-works/codex-fix-board), so the runner's automatic `worktree integrate` is refused with `board_owner_separate`. In THIS
run you execute `worktree complete` yourself, once. This overrides the generic integration text.

The accepted story_final candidate, TASK-261007-3v81ko CR rev 3 (tree 2f7ec5e30babb9dff4f00132ad9fd384663930b0 on base 07c018be),
landed on relux/main of ivanopcode/codex (the fork's CI home since 2026-10-09; `origin` points there) as the signed commit
e0eff057620104a416080da616256ee7f32bda1b (PR #14, exact-head fast-forward). The landing tree is
bde782b85ddbc8536536d0747b3917d0f24e1951: the CR patch replayed on trunk 25431940, which carries one more CI-only commit
(.github/workflows/relux-ci.yml). The CR patch replays byte-exact on its own base.

Do exactly this, with no file edits and no builds:
1. Re-check the landing:
   - `git fetch origin relux/main` and `git merge-base --is-ancestor e0eff057620104a416080da616256ee7f32bda1b origin/relux/main` (exit 0);
   - `git rev-parse e0eff057620104a416080da616256ee7f32bda1b^{tree}` must print bde782b85ddbc8536536d0747b3917d0f24e1951 (the accepted CR rev4 tree);
   - `git verify-commit e0eff057620104a416080da616256ee7f32bda1b` must report a good signature.
   If any check fails, do NOT run complete: attach the output (step 3) and exit.
2. (CR rev4 = landed tree bde782b8, accepted.) Run exactly:
   `task-board worktree complete STORY-261007-1cpzdo --cr TASK-261007-3v81ko --revision 4 --landed-commit e0eff057620104a416080da616256ee7f32bda1b`
3. Attach a task-scoped outcome `TASK-261007-3v81ko_complete-log.md` with the check outputs, complete's full output and its exit
   code. Then exit.
Do not run `task-board handoff`, `worktree integrate`, `worktree checkpoint` or any other landing or status command. If complete
refuses (for example because the landed tree differs from the candidate tree only by the CI-only trunk commit), attach the refusal
verbatim and exit. If it reports a resumable phase, re-run the same command once and report both outputs.
