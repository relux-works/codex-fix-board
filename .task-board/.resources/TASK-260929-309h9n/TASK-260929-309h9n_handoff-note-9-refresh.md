# TASK-260929-309h9n (P4b-2): scoped base refresh. Run refresh-candidate, then stop for precheck 9

This answers `TASK-260929-309h9n_recovery-logbook-8.md` with option (2). The orchestrator explicitly authorizes this run to
perform the supported base recovery. It does NOT authorize anything else.

Why: P3-1 landed on trunk (`relux/main` = `67789e1ee29e766e446c7f33feb61561d51f94db`, PR #15). The Story checkpoint
`ba7249177` (P4b-1) forks from the old trunk `e0eff0576`, so CR construction refuses with
`change_request_base_authority_mismatch`. The product content is unchanged; only the base moves.

## Authorized steps (in order; stop at the first unexpected result and report it)

1. Preconditions. Verify `git rev-parse HEAD` = `ba7249177b414c71ac277ae41fa3dc5dc5b1f16b` and that the current candidate
   (index plus worktree) is tree `eb655488b22ff6bb17a3a3a6250fd60e3a202209`; `mini-hosted-gate.sh` reports it.
2. Unstage only. refresh-candidate refuses staged changes, so run `git reset -q` (mixed: the index returns to HEAD and every
   worktree file stays as it is). Do not use `--hard`, `checkout`, `restore` on files, `stash` or `clean`.
   - Afterwards `git diff --cached --quiet` must exit 0.
   - The four added files must show as untracked: `app-server/tests/suite/v2/goal_continuation_pacing.rs`,
     `core/tests/suite/goal_continuation_pacing.rs`, `ext/goal/src/continuation_schedule.rs` and
     `ext/goal/tests/continuation_schedule.rs`.
3. Run `task-board worktree refresh-candidate TASK-260929-309h9n` from the codex root.
4. Expected checkpoint-replay conflict. The orchestrator pre-computed the replay: there is exactly one conflict, in
   `codex-rs/ext/goal/src/extension.rs`, adjacent imports
   (`use codex_extension_api::PromptFragment;` from trunk vs `use codex_extension_api::PlanCommitInput;` from P4b-1).
   - The resolution keeps both, sorted: `PlanCommitInput` then `PromptFragment`.
   - The full replacement content is in `p4b/b2-replay-extension.rs` (impl directory), sha256
     `cefdd1fd6376d19b3240a30fd52cb70777201e1949f62ba26c4863b94799cf27`.
   - Prepare `--replay-resolutions` from the retained replay worktree's `resolution-template.json` (bind to REBASE_HEAD,
     that path and that sha256, exactly as the help describes) and re-run refresh-candidate with it.
   - Before using the file, verify that it equals the conflicted file with only that hunk resolved.
   - If the tool reports a different conflict set, stop and report it; do not improvise a resolution.
5. The candidate delta is expected to merge without conflict; the orchestrator's 3-way simulation was clean. If
   refresh-candidate nevertheless reports a candidate-delta conflict, stop and report it.
6. Postconditions (report actual exit codes and values):
   - new `HEAD`: a signed checkpoint descending from `67789e1ee` (`git merge-base --is-ancestor 67789e1ee HEAD` exit 0);
   - new candidate tree id. The orchestrator predicts `3c5cbffcc73270bec86364ab42550441c87f933c`; say whether it matches;
   - `cargo fmt -- --config imports_granularity=Item --check` exit 0 (if fmt changes anything, run it without `--check`,
     report the new tree, and keep the change uncommitted);
   - `git diff --check` exit 0;
   - `git grep -n CODEX_GOAL_PACING_DISABLED -- codex-rs` empty.

## Not authorized

No other source, test or config edit. No commit, rebase, merge or cherry-pick by hand. No branch switch, `converge`,
`checkpoint` or registry edits. No local cargo build/test/check/clippy. No CODEX_HOME copies. Delete any temp files you
create (the replay worktree is the tool's; leave it to the tool or `worktree gc`).

## Finish

Precheck 8 evidence covers only tree `eb655488`, so do NOT hand off and do not claim hosted evidence for the new tree.
Add the note `HOSTED-PRECHECK-REQUESTED: precheck 9` with the new tree id, update the results' provenance section (new
base 67789e1ee, new checkpoint, replay resolution), and end your turn without handing off. The orchestrator runs precheck 9
on the exact new tree and then queues the handoff.
