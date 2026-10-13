# Continuation-schedule successor recovery


## Successor recovery logbook \u2014 RUN-261012-89faf6

The candidate is validated but the next Change Request is NOT published. The predecessor's
terminal construction failed with `change_request_base_authority_mismatch` / `stale-anchor`.
Its recorded checkpoint `ba7249177b414c71ac277ae41fa3dc5dc5b1f16b` does not descend from
selected protected authority `67789e1ee29e766e446c7f33feb61561d51f94db`.
Current activity still shows revision 2 as changes_requested; no revision 3 publication is claimed.

Personally rerun during successor recovery (standalone commands):
- `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh`: exit 0;
  exact unchanged tree `eb655488b22ff6bb17a3a3a6250fd60e3a202209`, hosted run 38217778118.
- `/Users/administrator/.cargo/bin/cargo fmt -- --config imports_granularity=Item --check`
  from codex-rs: exit 0; expected stable-channel warnings only.
- `git diff --check`: exit 0; `git diff --cached --check`: exit 0.
- `git rev-parse HEAD`: exit 0, checkpoint ba7249177b414c71ac277ae41fa3dc5dc5b1f16b.
- `git ls-remote relux refs/heads/main`: exit 128, exploratory error: there is no remote named relux.
  This is not evidence that protected authority is absent.
- `git remote -v`: exit 0; actual remote origin is git@github.com:ivanopcode/codex.git.
- `git ls-remote --symref origin HEAD refs/heads/main`: exit 0, fresh default ref refs/heads/relux/main
  at 67789e1ee29e766e446c7f33feb61561d51f94db (no refs/heads/main entry).
- `git ls-remote origin refs/heads/relux/main`: exit 0, same fresh protected OID.
- `git merge-base --is-ancestor 67789e1ee29e766e446c7f33feb61561d51f94db HEAD`: exit 1,
  expected negative ancestry result; the checkpoint does not descend from current authority.
- `task-board worktree refresh-candidate --help` and `task-board worktree converge --help`: exit 0,
  read-only recovery-contract inspection. Neither mutating recovery command was run.

External boundary: the assignment forbids committing, rebasing, switching branches and changing
files in this handoff. The supported refresh-candidate recovery replays checkpoints with signing
and installs a new branch/index/candidate. Converge is operator-only and explicitly refuses tracked
runs; no guard or producer restriction was bypassed. Existing producer changes are also staged,
which refresh-candidate documents as a refusal. No manual Git or board-registry repair was attempted.

Options: (1) orchestrator performs the supported base recovery, preserves this uncommitted delta,
then validates the resulting exact candidate and resumes the producer (recommended); (2) explicitly
authorize a scoped producer refresh including checkpoint replay and staged-index handling, then
obtain fresh exact-tree hosted evidence. Repeating unchanged handoff cannot repair ancestry.
Do not treat precheck 8 as evidence for a different tree after recovery. Do not weaken authority
checks or synthesize a provenance record.

Required external action: orchestrator repair the Story base/checkpoint provenance against fresh
protected authority, preserve the candidate delta, and provide updated exact-tree hosted evidence
if the tree changes. Task routed blocked on that operation; developer handoff is withheld until it
can publish a valid CR. Existing checked validation items still refer only to the precheck-8 tree.

No source/config/test changes, commits, rebase, branch switches, local builds or tests this turn.
Hosted tests and 7/7 mutant kills are accepted from precheck 8, not personally rerun.
No temporary directory or file was created by this successor; the gate's temporary index is
removed by its EXIT trap. No CODEX_HOME copy. No long command remains running.
