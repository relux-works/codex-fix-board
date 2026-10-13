# TASK-260929-309h9n — continuation-schedule: base refreshed, awaiting hosted precheck 9

## Current provenance

The scoped recovery in TASK-260929-309h9n_handoff-note-9-refresh.md succeeded.
Protected base: 67789e1ee29e766e446c7f33feb61561d51f94db.
Old checkpoint: ba7249177b414c71ac277ae41fa3dc5dc5b1f16b.
Old candidate: eb655488b22ff6bb17a3a3a6250fd60e3a202209.
New signed checkpoint: 4649d6571e09fb755c8f204931a6020a40605951.
New uncommitted candidate: 3c5cbffcc73270bec86364ab42550441c87f933c.
The new tree exactly matches the orchestrator's prediction, including after formatting verification.
Ancestry from the protected base was verified with exit 0; the new checkpoint contains a signature.

Only the authorized supported refresh was performed. No manual commit, rebase, merge, branch switch,
registry edit, or product/test/config edit was performed. The real index is at the new checkpoint;
the four candidate additions remain untracked.

## Replay resolution and logbook

The first refresh returned exit 1 at the expected checkpoint-replay conflict. The only unmerged path was
codex-rs/ext/goal/src/extension.rs at REBASE_HEAD ba7249177b414c71ac277ae41fa3dc5dc5b1f16b.
The conflict was exactly the adjacent PlanCommitInput versus PromptFragment imports.
The replacement keeps both, in that order. A byte-for-byte Python check verified the supplied file
equals the conflicted file with only that hunk resolved.
Replacement SHA-256: cefdd1fd6376d19b3240a30fd52cb70777201e1949f62ba26c4863b94799cf27.

The v1 resolution packet was based on the retained tool template and bound the original branch,
protected trunk, old candidate tree, checkpoint OID, path, base64 replacement bytes and digest.
The second refresh returned exit 0, Outcome refresh_advanced. There was no candidate-delta conflict.
The tool signed and installed the new checkpoint and preserved the candidate delta.

## Personally run checks and actual exit codes

| Command / verification | Exit | Result |
| --- | --- | --- |
| git rev-parse HEAD (before recovery) | 0 | ba7249177b414c71ac277ae41fa3dc5dc5b1f16b |
| bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh (before recovery) | 0 | Old tree eb655488 matches hosted precheck 8, run 38217778118 |
| shasum -a 256 …/impl/p4b/b2-replay-extension.rs | 0 | Authorized digest matches |
| git reset -q | 0 | Unstage only; candidate files preserved |
| git diff --cached --quiet (before and after recovery) | 0 | Index at checkpoint |
| task-board worktree refresh-candidate TASK-260929-309h9n | 1 | Expected replay conflict; no successful recovery claimed |
| Python exact-conflict/content/digest verification | 0 | Only authorized import hunk resolved |
| task-board worktree refresh-candidate TASK-260929-309h9n --replay-resolutions /Users/administrator/Developer/ReluxWorks/codex/.temp/TASK-260929-309h9n_replay-resolutions-9.json | 0 | refresh_advanced |
| git rev-parse HEAD (after recovery) | 0 | 4649d6571e09fb755c8f204931a6020a40605951 |
| git merge-base --is-ancestor 67789e1ee29e766e446c7f33feb61561d51f94db HEAD | 0 | Required ancestry |
| Temporary-index git read-tree HEAD / git add -A / git write-tree via Python | 0 | New candidate 3c5cbffcc73270bec86364ab42550441c87f933c; matches prediction |
| cargo fmt -- --config imports_granularity=Item --check | 127 | cargo absent from shell PATH; check did not run in this invocation |
| /Users/administrator/.cargo/bin/cargo fmt -- --config imports_granularity=Item --check (codex-rs) | 0 | Expected stable-channel warning only; no changes |
| git diff --check | 0 | Clean |
| git grep -n CODEX_GOAL_PACING_DISABLED -- codex-rs | 1 | Expected no matches |

No local build/check/clippy/test was run, as required by the mini addendum.
No model requests were made in this recovery run. The historical request-count scenarios and switch
inventory below are retained; they have not been rerun on this new candidate.

## Evidence boundary and next step

Precheck 8's 4/4 green lanes and 7/7 killed mutants apply only to eb655488, not the recovered tree.
No hosted test or mutant result is claimed for 3c5cbffc. Checklist items 3, 4, 5 and 10 were unchecked
pending exact-tree hosted precheck 9. All other checklist evidence is retained.
HOSTED-PRECHECK-REQUESTED: precheck 9, tree 3c5cbffcc73270bec86364ab42550441c87f933c.
No handoff or new Change Request publication was attempted.

The temporary resolution packet and both temporary indexes created by this run were deleted.
No temporary directory was created manually; retained replay worktrees are tool-owned and left to
the supported tool lifecycle. No CODEX_HOME copy and no running background command remain.

---

## Historical precheck-8 report (old tree only)

The following prior report is preserved for AC/test/mutant mappings, request measurements,
production-policy bounds, review findings and earlier recovery evidence. Its old-tree handoff and
checklist statements are historical and superseded by the current provenance above.

