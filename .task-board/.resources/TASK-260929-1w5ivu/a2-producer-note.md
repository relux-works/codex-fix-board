# TASK-260929-1w5ivu (P3-2 continuation contract and guidance): producer note for precheck 1

Read in this order: `final-plan.md` (§9 P3 exact wait contract, §10 stage 5 and the deferral sentence under the stage table,
§12 row p2-p3-capability-consistency), the AC on this task (AC1-AC10), `producer-brief.md`, then `mini-producer-addendum.md`.
The addendum OVERRIDES producer-brief.md wherever they conflict: no local cargo except `cargo fmt`, nothing committed,
mutants as JSON.

## Base

P3-1 (TASK-260929-2is91w, the WaitingCapabilities snapshot) LANDED on trunk as 67789e1e (PR #15, closed with tree_carried).
This is the Story's final leaf, so the spawn refreshes the Story branch onto that trunk. The worktree
`/Users/administrator/Developer/ReluxWorks/codex/.temp/STORY-260929-40trfs/worktree` must end up at trunk 67789e1e with no
P3-1 leftovers as uncommitted changes. Check `git status --short` first. If P3-1 paths still show as modified while equal to
HEAD, stop and add a note; do not commit, reset or stash.

## Design constraints (decided by the orchestrator; do not redesign)

1. Fill the existing hook `waiting_capability_fragments` in `ext/goal/src/steering.rs`. It already receives the snapshot on
   both context paths (initial and post-discovery) through goal's ContextContributor. Do not add a second plumbing path.
2. The sentences are the exact §9 table texts. Copy them byte-exact from final-plan.md; a test compares against the same
   constants.
3. The no-wait/end-turn "none of the positive flags" paragraph is deferred (AC2). Do not emit it.
4. Goal-active threads only (AC3). No core fragment for goal-less threads.
5. Keep `update_plan_enabled` template selection as it is. This leaf changes only the verified-wait bullet in the template
   text.
6. Bounded (AC4) and incremental (AC5). Re-emission follows the contributor path P3-1 established: contributors run only on
   turn-context changes. Prove "no new item on unchanged capabilities" and "exactly one on change" with real requests.

## Tests and mutants

AC6 integration tests go in core/tests/suite: reuse the helpers in `search_tool.rs` and the waiting-capabilities suites P3-1
added, including the remote-catalog helper `remote_catalog_replacement_case` for the clock-off case. Unit tests for the
renderer and the AC4 combination bound go in ext/goal/tests. Mutants are AC8, each `git apply --check`-clean against your
FINAL tree and naming its killer. Name the killers so that the filter `test(waiting) | test(guidance) | test(continuation) |
test(goal)` selects every one, and say in the results which filter they need. Report AC10 numbers.

## Lint hygiene (recurring hosted failures)

Watch for:
- redundant closures (use method paths), uninlined format args, collapsible ifs, needless borrows;
- `vec![` where an array works, single-arm `match`;
- `#[cfg(test)]` on anything production calls, unused imports;
- `/*param*/` comments on opaque positional literals;
- `await_holding_lock` (scope MutexGuards before any `.await`).

## Finish

Run `cargo fmt -- --config imports_granularity=Item`, then `--check` (exit 0). Leave everything UNCOMMITTED. Report the tree
id after the last edit, using the temp index method from the addendum. Attach `TASK-260929-1w5ivu_mutants.json`. Add the
note `HOSTED-PRECHECK-REQUESTED: precheck 1`. Delete any temp dir you made, and end your turn without handing off.
