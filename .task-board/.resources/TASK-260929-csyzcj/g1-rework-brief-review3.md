# TASK-260929-csyzcj (G1): review rev3 changes_requested. Bound agent paths at their SOURCE, then request precheck 11

The verdict is `TASK-260929-csyzcj_review-verdict-rev3.md`. Panel B accepted; panel A and the delta reviewer found the same remaining
bypass. Your rev3 text cap is correct, but `core/src/agent/control/completion.rs:114-123` still passes the FULL child and parent
`AgentPath`s to `InterAgentCommunication::new`. `protocol/src/protocol.rs:883-920` copies them into `ResponseItem::AgentMessage`
`author`/`recipient` (serialized at `protocol/src/models.rs:1037-1047`), and `context_manager/history.rs:1081-1102` counts those
bytes as model-visible. Nothing truncates them, and `AgentPath` has no length bound (`protocol/src/agent_path.rs:125-180`). The V2
spawn `task_name` is an unrestricted String (`tools/handlers/multi_agents_common.rs:133-156`).

Required approach (it closes the INTERRUPTED notice, its envelope, and the same envelope on completion messages):
1. Bound agent paths where they are CREATED. Reject a V2 spawn whose `task_name` (or the resulting `AgentPath` segment) exceeds a
   fixed maximum, for example 128 bytes per segment and a total path cap, with a clear tool error to the model. Do NOT truncate
   silently, because the path is an identity used for routing. Keep the `AgentPath` grammar change minimal and in protocol, and
   reuse it at the spawn entry point. Existing valid short names must keep working byte-identically.
2. Keep your rev3 fragment truncation as defense in depth (it is harmless), or drop it if the source bound makes it unreachable.
   State which in the results. The fragment's hard-cap test must still hold.
3. Tests: a V2 spawn with an over-long task_name is refused with the error, and no child is created; a name exactly at the cap
   is accepted. A narrowing mutant that removes the length check must be killed by the refusal test. Also assert that the
   `author`/`recipient` of the INTERRUPTED AgentMessage in your integration test are the bounded paths.
4. Size and scope: this touches protocol/ (AgentPath) and the spawn handler. Keep it small; do not refactor the routing.
`mini-producer-addendum.md` applies (cargo fmt required; no other cargo; no real CODEX_HOME copies). All mutant patches must apply
to your final tree. Leave everything UNCOMMITTED, report the final tree id, add the note `HOSTED-PRECHECK-REQUESTED: precheck 11`, and
end your turn without handing off. The mutant filter adds `test(task_name) | test(agent_path) | test(spawn)`.
