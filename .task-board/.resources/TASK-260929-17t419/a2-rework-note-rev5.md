# Rework note for TASK-260929-17t419 — revision 5

Revision 4 differs from revision 3 only by a README.md "Development tools" section. That is out of scope for this
upstream-bound leaf: revert README.md to its base content (`git checkout -- README.md` is fine for that single
path; nothing else). The 15 scenario snapshot failures in revision 4 were a gate artefact: insta resolved the
control root instead of this worktree and compared against the control root's unchanged snapshots. The gate now
pins INSTA_WORKSPACE_ROOT; your snapshots are correct (orchestrator verified multi_agent_catalog_parameters passes
with the pin). Keep all revision-3 code. Re-verify with the updated producer-brief environment (INSTA_WORKSPACE_ROOT
set), run the tb-R58 suite check, and hand off.
