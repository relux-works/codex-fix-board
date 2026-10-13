# TASK-260929-1w5ivu: hand off CR revision 3 on hosted precheck 6

Review rev2 was changes_requested on one finding, A2-F1: the new `#[path]` source was missing from the Bazel integration
compile data. Panels B and delta accepted. The orchestrator fixed A2-F1 mechanically (`TASK-260929-1w5ivu_orch-bazel-fix-6.md`,
precondition): `ext/goal/BUILD.bazel` now lists `src/waiting_world_state.rs`. That is the only change from the rev2 tree
78633964.

Hosted precheck 6 (`TASK-260929-1w5ivu_hosted-precheck-6.md`, precondition, run 38286079342, ref relux/ci-next, tree
0909471501a910f604164a2bba7b586e2ebf9ba8) is fully green: lint, small, core and app-server. All 8 mutants are killed.

1. Run `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh` from the
   worktree. It must exit 0 for tree 09094715. Do NOT change any file. If it fails, stop and add a note.
2. Refresh and re-attach `TASK-260929-1w5ivu_results.md` for CR revision 3, citing precheck 6:
   - record the A2-F1 Bazel fix;
   - correct the A2-N1 snapshot size claim: at most 512 B holds for ASCII names only. A name capped at 128 four-byte
     characters plus the ellipsis gives about 602 B. The fragment bounds (3 KiB / 1,000 tokens) are unaffected;
   - change nothing else.
3. Run `task-board handoff TASK-260929-1w5ivu --role developer`.
