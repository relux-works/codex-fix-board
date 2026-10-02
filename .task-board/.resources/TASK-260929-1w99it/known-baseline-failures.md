# Known environment-caused codex-core test failures (quarantined in the landing gate)

Evidence: reproduced on a clean `relux/main` (0462dcc) checkout without any series change,
log `.temp/goal-token-burn/impl/baseline-core-six-08.log` (2026-09-29), plus CR rev2 validation log of TASK-260929-1w99it.

| Test | Cause on this workstation | Baseline |
|---|---|---|
| suite::scenarios::astra_kickoff_with_skills_plugins_and_remote_compaction | snapshot picks up the operator's real global skills directory (extra `r1` skills root) | FAIL |
| suite::scenarios::astra_refreshes_plugin_tools_and_skills_in_an_existing_thread | same skills-root leak | FAIL |
| suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_parent_approval_preserves_denied_reads | "unexpected approval request: /bin/cat …/secret.env" (host zsh/sandbox differs from CI) | FAIL |
| suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_guardian_reviews_persistent_terminal_in_current_turn | same zsh-fork host difference | FAIL |
| suite::skill_approval::shell_zsh_fork_skill_scripts_ignore_declared_permissions | same zsh-fork host difference | FAIL |
| suite::mcp_optional_startup_grace::optional_mcp_startup_grace_controls_initial_turn_tool_catalog::zero_grace_respects_server_startup_timeout | timing-sensitive; passes on baseline, failed twice under host load ~70 | flaky |

Upstream PR branches must be re-validated where these run correctly (they are not signal on this host).

## codex-app-server (evidence: `.temp/goal-token-burn/impl/baseline-appserver-four-10.log`, CR rev4 validation log)

| Test | Cause on this workstation | Baseline |
|---|---|---|
| suite::v2::turn_start_zsh_fork::turn_start_shell_zsh_fork_subcommand_decline_marks_parent_declined_v2 | host zsh-fork difference (same class as the core zsh-fork tests) | FAIL |
| suite::v2::skills_list::skills_changed_notification_is_emitted_after_skill_change | skills watcher on this host (operator's global skills directory) | FAIL |
| suite::v2::thread_fork::thread_fork_surfaces_cloud_config_bundle_load_errors | ~10 s timer race: passes at 10.10 s alone, fails at 10.25 s under suite load | flaky |
| suite::v2::thread_resume::thread_resume_surfaces_cloud_config_bundle_load_errors | same ~10 s timer race | flaky |

## Retry policy (2026-09-30)
Timing-sensitive tests fail at random under shared-host load (rev5: four ~5 s unit tests in agent::control /
multi_agents that passed in rev3/rev4 on the same code). Core, code_mode and app-server gate commands run with
`--retries 3`: a deterministic regression still fails every attempt, a timing race is reported as FLAKY.
