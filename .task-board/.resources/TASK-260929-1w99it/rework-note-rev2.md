# Rework note for TASK-260929-1w99it — republish as revision 2

Revision 1's landing-gate suite failed at `just test -p codex-core` (226 failures, exit 100). The orchestrator
reproduced the same failures on a clean `relux/main` checkout without your change: they are environmental.
Core integration tests spawn helper binaries from other packages (`test_stdio_server`, `codex-code-mode-host`,
...) that `-p codex-core` does not build, and the v8 dependency needs openai's prebuilt rusty_v8 archive. The
board's validation suite now builds those helpers and sets the required environment (see the updated
`producer-brief.md`), and the previously failing tests pass on the baseline.

Your leaf only touches `codex-rs/tools` (arguments.rs, arguments_tests.rs, lib.rs). Do NOT change codex-core or
anything outside the leaf scope to address revision 1's validation log.

Do:
1. Review your own diff against the AC table and the surface table (`text grammar`); fix anything missing.
2. Re-run `just test -p codex-tools`, `just fmt`, and `just fix -p codex-tools` with the environment from
   `producer-brief.md`; report real exit codes.
3. Update `TASK-260929-1w99it_results.md` and hand off again (`task-board handoff TASK-260929-1w99it --role developer`).
   The suite reruns automatically and publishes revision 2.
