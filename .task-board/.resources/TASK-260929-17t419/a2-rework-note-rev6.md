# Rework note for TASK-260929-17t419 — revision 6 (republish unchanged)

Revision 5's only failures (two `thread_fork_multi_agent::fork_before_first_turn_preserves_model_selected_multi_agent_version`
variants) were caused by stale artifacts in the shared cargo target: another worktree's build was reused for this
checkout. After the orchestrator cleaned the workspace members, all four variants pass on your candidate. The gate now
starts with `codex-target-guard.sh`, and so must your builds (see producer-brief.md). Keep your code unchanged: run the
guard, re-verify quickly, keep README.md at base, and hand off.
