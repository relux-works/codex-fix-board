# Rework note for TASK-260929-17t419 — republish as revision 2

Revision 1's gate failed in `just test -p codex-core` on 11 request-history snapshot tests, all of them in
`suite::scenarios::*`. This is the expected consequence of AC row 5 (integer schemas). For example,
`multi_agent_catalog_parameters` now differs only in the tool-namespace hashes of `clock` and `collaboration`,
whose parameter schemas you changed. The gate runs with `INSTA_UPDATE=no`, so no `.snap.new` was written.
(`suite::git_enrichment::…::ambient_background_thread` also failed there but passes alone; it is a load flake and
needs no change.)

Do:
1. Regenerate exactly the affected snapshots on purpose. Run the scenario tests with `INSTA_UPDATE=always`, or run
   `cargo insta test -p codex-core --accept -- <filter>` scoped to them:
   astra_asks_an_async_question_and_receives_the_answer_while_working, astra_continues_after_a_stream_is_interrupted,
   astra_continues_after_input_yields_a_code_mode_cell, astra_omits_disabled_executor_skills_from_model_context,
   astra_reads_code_mode_call_timing, astra_settings_release_check_with_direct_and_code_mode_tools,
   astra_switches_environments_for_the_rest_of_the_active_turn, code_mode_catalog_messages,
   mcp_resource_messages::code_mode, multi_agent_catalog_parameters,
   skill_catalog_dedup::cloud_preference_preserves_executor_aliases_and_description_budget.
   Do NOT regenerate the two quarantined astra scenarios (see known-baseline-failures.md). They leak this host's
   global skills and must stay as they are on main.
2. Inspect every changed `.snap` hunk. Allowed: hash or schema lines of tools whose integer parameters you changed
   (clock.sleep, exec_command, write_stdin, wait_agent v1/v2, and the one-shot exec timeout). Anything else, for
   example local skills, paths, or unrelated tools, means host leakage or a regression. Revert it and fix the cause.
   List every changed snapshot and why in your results.
3. Keep `INSTA_UPDATE=no` for all other runs. Make sure no `*.snap.new` or `*.pending-snap` files remain in the
   worktree.
4. Re-run `just test -p codex-core -E 'test(suite::scenarios::)'` (expect green apart from the two quarantined astra
   tests), `just test -p codex-tools`, `just fmt` and `just fix -p codex-core -p codex-tools`, then hand off.
