# TASK-260929-csyzcj (G1): review rev4 changes_requested. Keep the AgentPath cap for NEW identities only, then request precheck 13

The verdict is `TASK-260929-csyzcj_review-verdict-rev4.md`. Panel A and the delta reviewer independently found one regression
(legacy-agent-path-resume-regression / persisted-agent-path-caps-break-resume); panel B accepted.

Problem: rev4 put the 128-byte segment / 1024-byte path limits inside `validate_absolute_path`/`validate_agent_name`, which ALL
AgentPath constructors share, including `Deserialize` (try_from String) and `from_string`. Paths that were valid before rev4
(e.g. `/root/` + 129 chars) are already persisted in rollouts (SessionMeta.source ThreadSpawn.agent_path, SessionMeta.agent_path).
With rev4, `resume_single_agent_from_rollout` returns `invalid stored agent path`, `restore_persisted_v2_agent_metadata` skips the
child, and `decode_rollout_line`/`load_rollout_items` drop the SessionMeta, so `get_rollout_history` loses the thread id.
AGENTS.md forbids breaking "resuming sessions from existing rollouts".

Required approach:
1. Move the length limits OUT of the shared parser. Parsing/deserializing an AgentPath must accept every path the pre-rev4 grammar
   accepted, byte-identically (no truncation, no migration of routing keys).
2. Enforce the limits only where NEW identities are minted: the V2 spawn entry (task_name -> AgentPath::join for a new child), with
   the same clear tool error. Keep MAX_SEGMENT_BYTES/MAX_PATH_BYTES in protocol and expose a small explicit check (for example
   `AgentPath::validate_new_segment` or a `join_new` constructor) used by spawn; do not add a bool parameter.
3. Model context stays bounded independently of the source: keep your fragment truncation (rev3) as the hard cap, because legacy
   over-cap paths can now still reach the INTERRUPTED notice and the AgentMessage author/recipient. If the author/recipient envelope
   is model-visible, bound it at render time too (truncate for DISPLAY only; never change the stored/routing identity). State in the
   results which render paths are capped and the worst-case byte bound.
4. Tests (hosted only):
   - deserialize/try_from of a legacy 129-byte-segment path and a >1024-byte valid path succeed and round-trip unchanged
     (protocol agent_path tests, name containing `agent_path`);
   - the resume regression the panels requested, e.g. `resume_agent_preserves_legacy_overlong_path` (core) and/or
     `get_rollout_history_preserves_legacy_agent_path` (rollout);
   - keep the V2 spawn refusal and at-cap acceptance tests and the fragment hard-cap test;
   - mutants: one that re-adds the cap to the shared parser (killed by the legacy round-trip/resume test), and keep
     `spawn_task_name_length_unchecked` killed by the refusal test.
5. Small scope: protocol agent_path.rs, the spawn handler, tests. No routing refactor.
`mini-producer-addendum.md` applies (cargo fmt required; no other cargo; no real CODEX_HOME copies; delete your temp dirs). All
mutant patches must apply to your final tree. Leave everything UNCOMMITTED, report the final tree id AFTER fmt, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 13`, and end your turn without handing off. The mutant filter adds `test(legacy) | test(rollout_history) | test(resume_agent)`.
