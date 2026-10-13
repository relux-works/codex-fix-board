# TASK-260929-csyzcj (G1): review rev2 changes_requested. Hard-cap the INTERRUPTED fragment, then request precheck 9

The verdict is `TASK-260929-csyzcj_review-verdict-rev2.md` (precondition). Panels A, B and the delta reviewer agree that your
rev1 fix (the typed `InterAgentInterruptedMessage` in core/context) is correct. The one remaining finding, from A and from the delta
reviewer, is about bounds:

`core/src/context/inter_agent_interrupted_message.rs:35-40` formats two UNRESTRICTED `AgentPath`s (task name and sender) into
model-visible text. `protocol/src/agent_path.rs:125-180` validates syntax only, not length, and the V2 spawn `task_name` flows through
`multi_agents_common::thread_spawn_source` (tools/handlers/multi_agents_common.rs:133-156) into the path. AGENTS.md
"Model visible context" rule 3: everything injected must have a bounded size and a hard cap.

Required:
1. Give the fragment a hard cap. Truncate each path to a fixed maximum (for example 256 chars, with a clear truncation marker),
   using the repo's existing truncation helpers where they fit (`truncate_text` / `TruncationPolicy` are already used in
   session_prefix.rs). Then the whole body has a fixed upper bound. Keep the exact current text for normal-length paths, so
   the existing exact-body test still passes unchanged.
2. Tests (in `inter_agent_interrupted_message_tests.rs`): a path far over the cap renders truncated with the marker, and the
   rendered body length is <= the stated bound (whole-string `assert_eq` on the expected truncated body). Add a narrowing mutant
   that removes the cap for ONE of the two paths, with this test as its killer.
3. Do not change the completion-message type in this leaf. If you notice the pre-existing `InterAgentCompletionMessage` has the
   same issue, say so in your results as an out-of-scope observation.
`mini-producer-addendum.md` applies. Run cargo fmt plus `--check` (exit 0). All mutant patches must apply to your final tree. Leave
everything UNCOMMITTED, report the final tree id, add the note `HOSTED-PRECHECK-REQUESTED: precheck 9`, and end your turn
without handing off. The mutant filter adds `test(inter_agent_interrupted)`.
