# Rework note for TASK-260929-1w99it — republish as revision 4

Revision 3's suite passed fmt-check, helper builds, clippy and the codex-tools/goal/extension-api tests; in
`just test -p codex-core` 4848 of 4854 passed. The 6 failures are environment-caused on this workstation and
reproduce on a clean `relux/main` without your change (skills-root leak into two astra scenario snapshots,
host zsh-fork differences in three approval tests, one timing-sensitive MCP startup test). The board's gate now
excludes exactly those 6 tests with recorded evidence.

Your leaf only touches `codex-rs/tools`. Do NOT change codex-core or anything outside the leaf scope. Re-run
`just test -p codex-tools`, `just fmt`, `just fix -p codex-tools` with the environment in `producer-brief.md`
(note CARGO_BUILD_JOBS=4 / NEXTEST_TEST_THREADS=4 while the host is under load), refresh
`TASK-260929-1w99it_results.md`, and hand off again. The suite reruns and publishes revision 4.

Update for revision 4: revision 3 got 4847 of 4848 core tests green; the only failure was
`suite::code_mode::code_mode_excludes_mcp_servers_using_their_configured_identity` hitting the 60 s nextest
timeout under host load (it passes in 25 s alone on the baseline). The gate now runs the heavy
`suite::code_mode::` tests in a separate command with 2 threads and extra retries. Nothing to change in your
leaf; re-verify and hand off.
