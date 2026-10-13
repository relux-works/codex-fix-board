# TASK-260929-309h9n: hand off the next CR revision on hosted precheck 9

The base refresh succeeded. The Story checkpoint is now `4649d6571` on trunk `67789e1ee` (P3-1 landed), with the one import
conflict in `ext/goal/src/extension.rs` resolved by `p4b/b2-replay-extension.rs`. The candidate tree is
`3c5cbffcc73270bec86364ab42550441c87f933c`, exactly the orchestrator's prediction. Product content is unchanged from
precheck 8; only the base moved.

Hosted precheck 9 (`TASK-260929-309h9n_hosted-precheck-9.md`, precondition, run 38232681612, ref relux/ci-next,
tree 3c5cbffc) is fully green: lint, small, core and app-server, with all 7 mutants killed by their named tests. It
supersedes precheck 8 as the evidence for this tree.
1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the worktree; it must exit 0 for tree 3c5cbffc. Do NOT change any file. If it fails, stop and add a note.
2. Check validation items 3/4/5/10, citing precheck 9. Refresh and re-attach `TASK-260929-309h9n_results.md`:
   - provenance: new base 67789e1ee, checkpoint 4649d6571, replay resolution;
   - precheck 9 replaces 8 as the exact-tree evidence;
   - keep the production-policy bounds paragraph and the orchestrator lint fix 8 mention.
3. Run `task-board handoff TASK-260929-309h9n --role developer`.
