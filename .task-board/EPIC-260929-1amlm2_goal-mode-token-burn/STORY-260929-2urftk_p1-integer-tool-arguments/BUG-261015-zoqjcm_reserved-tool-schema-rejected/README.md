# BUG-261015-zoqjcm: reserved-tool-schema-rejected

## Description
Every model request from the fork fails on a ChatGPT account (gpt-6-astra and gpt-5.6-sol tried) with 400 invalid_request_error: Function collaboration.wait_agent is reserved for use by this model and must match the configured schema. Cause: P1 (35af013) re-advertised waiting-tool parameters as JSON Schema integer (clock.sleep duration_ms, exec_command/write_stdin integer fields, wait_agent timeout_ms v1/v2, create_goal token_budget). The server pins reserved function schemas; fc22281 refreshed the changed astra snapshot fingerprints instead of flagging them. Found in the side-by-side trial (STORY-261015-naytxd), binary e063784.

## Scope
Advertised JSON Schema of the P1-touched tools (wait_agent v1/v2, exec_command, write_stdin, clock.sleep, create_goal) plus their spec tests and the 17 core scenario snapshots; parsing code untouched.

## Acceptance Criteria
AC1 advertised tool schemas (names, types, descriptions, required) for every tool P1 touched are byte-identical to upstream base 0462dcc; the astra/collaboration/clock snapshot fingerprints return to their upstream values. AC2 the integral-decimal tolerant parsing from P1 stays (60000.0 and 6e4 accepted, fractions refused) with its tests. AC3 a regression test pins the advertised schemas of reserved-candidate tools against upstream, so a future type change fails CI instead of refreshing snapshots. AC4 a release build of the fix passes a live request with gpt-6-astra on a ChatGPT account (manual trial).
