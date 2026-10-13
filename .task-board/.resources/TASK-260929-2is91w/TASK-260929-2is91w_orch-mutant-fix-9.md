# TASK-260929-2is91w orchestrator mutant fix before precheck 9

Mutant discovery_ignores_call_pairing (RUN-261011-3f5e28) was a corrupt patch (hunk header 13/9 did not match its body; git apply: corrupt patch at line 17). Regenerated from the identical intended edit (drop the `execution` binding; `let paired = call_id.is_some();`) against tree 092dfe4b3e209b74aa322755c1ff137bd19ae650. No worktree change. All 13 mutants apply.
