# TASK-260929-3ld28o (P4b-1): review rev2 changes_requested. Bind the V1 spawn observation to the spawn RESULT, then request precheck 7

Verdict `TASK-260929-3ld28o_review-verdict-rev2.md`: panel B accepted. Panel A and the delta reviewer found the same remaining issue.
It is the sibling of the rev1 send_input fix, and it is conservative: it MISSES a reset, it never invents one.

V1 spawn: `control/spawn.rs:849-870` admits the initial input, commits the reservation and disarms rollback, then `:890-894` samples
`get_status` into `LiveAgent.status`, and `:914` returns Ok. A child can error right after admission (`agent/status.rs:10-20` maps it
to Errored). `handlers/multi_agents/spawn.rs:150-152, 179-201` keeps Ok with a child id, but derives the completed item's status from
that sampled liveness (`collab_tool_call_status`, `multi_agents.rs:90-93` maps Errored to Failed). `accounting.rs:296-306` counts
SpawnAgent only when Completed, so an ACCEPTED spawn yields 0 observations.

Required:
1. Do it exactly as rev2 did for send_input: base the V1 spawn's completed-item status (or at least the observation) on
   `result.is_ok()`, the delivery and acceptance result, and keep child liveness only for presentation. V2 spawn already uses a
   receipt-success Started activity; leave it.
2. Test: an accepted V1 spawn whose child is already Errored when status is sampled still sets exactly one observation; a refused
   spawn sets none. Add a narrowing mutant (back to the sampled-status proxy) killed by that test.
3. Keep every other line byte-identical; this is a small, focused fix.
`mini-producer-addendum.md` applies. Run cargo fmt plus `--check` (exit 0). All mutants must apply to your final tree. Leave everything
UNCOMMITTED, report the final tree id, add the note `HOSTED-PRECHECK-REQUESTED: precheck 7`, and end your turn without handing off.
