# TASK-261007-3v81ko: landed-tree rework (CR rev3 -> rev4) so the Story can complete

Why: CR rev3 (tree 2f7ec5e3 on base 07c018be) was accepted and landed on ivanopcode/codex relux/main as the signed commit
e0eff057620104a416080da616256ee7f32bda1b. The landing commit's parent is trunk 25431940, which carries one more CI-only commit, so
the landed tree is bde782b8, which differs from the accepted tree ONLY in `.github/workflows/relux-ci.yml`. `worktree complete` refused
with `code_landing_tree_mismatch` and named this recovery. You are the tracked developer run it requires. Make NO code changes of
your own.

Do exactly this, with no builds (Mac mini: no cargo except `cargo fmt`):
1. `task-board worktree prepare-landed-review STORY-261007-1cpzdo --cr TASK-261007-3v81ko --revision 3 --landed-commit e0eff057620104a416080da616256ee7f32bda1b --json > /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/leak-landed-review.json`
   Attach that JSON as the outcome `TASK-261007-3v81ko_landed-review-export.json`. Check that its update patch touches only
   `.github/workflows/relux-ci.yml`. If it touches anything else, stop and add a note.
2. `task-board worktree start-landed-rework STORY-261007-1cpzdo --cr TASK-261007-3v81ko --revision 3 --landed-commit e0eff057620104a416080da616256ee7f32bda1b --export <that JSON path>`
3. Apply the export's update_patch to the previous candidate in the Story worktree, exactly as the command output instructs. Then
   verify that the worktree snapshot tree (temp index: `git read-tree HEAD`, `git add -A`, `git write-tree`) equals the export's
   observed_landing.tree_oid (expected bde782b85ddbc8536536d0747b3917d0f24e1951).
4. Refresh `TASK-261007-3v81ko_results.md` with a short "rev4 = landed tree" section: the only change versus rev3 is the CI-only
   relux-ci.yml hunk from trunk. Hosted evidence: precheck 3 on the rev3 tree, plus exact-head relux-ci on e0eff057 (all green).
   Leave the checklist items as they are.
5. Run `task-board handoff TASK-261007-3v81ko --role developer`. The mini gate accepts this tree, because it differs from a recorded
   green tree only under `.github/`.
If any command refuses, attach its output verbatim and stop. Do not run complete, integrate or checkpoint.
