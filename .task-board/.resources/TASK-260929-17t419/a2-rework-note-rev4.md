# Rework note for TASK-260929-17t419 — republish as revision 4

Revision 3 passed commands 1-6 (fmt, helpers, clippy incl. rollout-trace, codex-tools/goal/extension-api/
rollout-trace tests, all codex-core tests including code_mode) and 1821/1822 app-server tests. The single failure,
`suite::v2::guardian_v2::resumed_thread_does_not_wait_for_guardian_websocket_warmup`, fails only inside the full
concurrent app-server run; the orchestrator ran it alone on the clean baseline (pass, 10.6 s) and on your candidate
(pass, 9.0 s). It is now quarantined as concurrency-sensitive (see known-baseline-failures.md).

Your revision-3 changes stay as they are. Re-verify quickly (`just test -p codex-rollout-trace`, the guardian/
lifecycle tests you added, `just fmt`), keep the sweep table in your results, and hand off to publish revision 4.
