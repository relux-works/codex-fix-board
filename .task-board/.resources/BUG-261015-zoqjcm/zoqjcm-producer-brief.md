# Producer brief — BUG-261015-zoqjcm reserved-tool-schema-rejected

Read `producer-brief.md` (precondition) for the general rules: worktree, AGENTS.md style, handoff, hosted
pre-handoff check. This brief overrides its build section, see "No local builds" below.

## The defect (confirmed live on 2026-10-15)

A release build of `relux/main` e063784 fails EVERY model request on a ChatGPT account:

```
400 invalid_request_error, param "tools":
Function 'collaboration.wait_agent' is reserved for use by this model and must match the configured schema.
```

The same request from a release build of the upstream base `0462dcc062b822bb8fff16cc31ce6eeab69823b9` succeeds
(`codex-base exec -m gpt-6-astra 'Reply with exactly: base-ok'` -> `base-ok`). The server pins the schema of
reserved functions and compares the advertised schema exactly.

Cause: P1 (commit 35af013, "Accept integral decimal integers in waiting-tool arguments") changed the ADVERTISED
JSON Schema type of these parameters from `number` to `integer`:

| Tool | File (relux/main) | Parameters |
| --- | --- | --- |
| collaboration.wait_agent v1 | `core/src/tools/handlers/multi_agents_spec.rs` `wait_agent_tool_parameters_v1` | `timeout_ms` |
| collaboration.wait_agent v2 | same file, `wait_agent_tool_parameters_v2` | `timeout_ms` |
| exec_command | `core/src/tools/handlers/shell_spec.rs` | `yield_time_ms`, `max_output_tokens` |
| write_stdin | same file, `create_write_stdin_tool` | `session_id`, `yield_time_ms`, `max_output_tokens` |
| clock.sleep | `core/src/tools/handlers/sleep.rs` `create_sleep_tool` | `duration_ms` |
| create_goal | `ext/goal/src/tool.rs` | `token_budget` (check the exact advertised type upstream) |

Commit fc22281 then refreshed the astra snapshot fingerprints instead of flagging the change. Today every one of
the 17 `*.snap` files that differ from upstream differs ONLY in `hash=` lines:
`git diff 0462dcc062b822bb8fff16cc31ce6eeab69823b9 HEAD -- '*.snap'`.

Verify this table yourself with `git show 35af013` and
`git diff 0462dcc062b822bb8fff16cc31ce6eeab69823b9 HEAD -- <spec files>`. Re-check for any OTHER advertised
schema change to an upstream tool that later patches introduced (the P5 `notify_on_exit` parameter and description
suffix on `exec_command` exist only on capable hosts, see "Out of scope").

## Required change (AC in the bug)

1. **AC1 — advertised schemas back to upstream.** For every tool and parameter above, the advertised schema
   (name, type, description, required, additionalProperties) must be byte-identical to upstream 0462dcc. Revert
   `JsonSchema::integer(...)` to exactly what upstream has. Revert the spec unit tests that P1 changed to expect
   `integer` (`shell_spec_tests.rs`, `multi_agents_spec_tests.rs`, and any other) to the upstream expectation.
   Restore every `*.snap` hash line so that `git diff 0462dcc062b822bb8fff16cc31ce6eeab69823b9 -- '*.snap'` is
   EMPTY. If you believe some snapshot line must still differ, stop and explain which patch causes it in your
   results instead of refreshing it.
2. **AC2 — keep the tolerant parsing.** Do NOT touch the deserializers (`codex-rs/tools/src/arguments.rs`, the
   `#[serde(deserialize_with = ...)]` attributes, the guardian and rollout-trace readers). `60000.0` and `6e4`
   stay accepted; fractions, overflow, sign errors and wrong types stay refused. Their tests stay unchanged and
   green. The value of P1 is the parsing, not the advertised type.
3. **AC3 — regression pin.** Add a test (sibling `*_tests.rs` per AGENTS.md) that pins the full advertised
   parameter JSON of each tool above to the literal upstream JSON (serialize the `ToolSpec`/`JsonSchema` with
   serde_json and compare whole objects with `pretty_assertions::assert_eq`). Comment it as a wire-contract pin:
   the server rejects requests when a reserved tool schema drifts, so a change here must be a deliberate decision,
   not a snapshot refresh. This is the one place where a test of a statically defined value is intended; say so
   in the comment. Pair it with a negative check: each pinned parameter is `"type": "number"` (or whatever upstream
   has), never `"integer"`.
4. **AC4** (live request on a release build) is done by the orchestrator after landing. Nothing to do here.

## Mutants

Attach `BUG-261015-zoqjcm_mutants.json` with at least these (unified diffs against your worktree):
- each spec file: flip one pinned parameter back to `JsonSchema::integer` (one mutant per file: multi_agents_spec
  v1, multi_agents_spec v2, shell_spec exec_command, shell_spec write_stdin, sleep.rs, ext/goal tool.rs). Each must
  be killed by the AC3 pin (name the test).
- change one pinned description string by one word. It must be killed by the pin.
- break the tolerant parser (for example, make the integral-decimal path refuse `60000.0`). It must be killed by an
  existing P1 parsing test.

## No local builds (overrides producer-brief.md)

The machine has about 14 GiB of free disk. Do NOT run cargo, `just fix`, `just clippy`, `just test` or the target
guard. You MAY run `just fmt` (rustfmt only, no build). Write the change carefully so it compiles: hosted CI
(relux-ci lanes lint / small / core / app-server, plus mutants) is the only build. When the code, tests and
mutants are ready, attach `BUG-261015-zoqjcm_results.md` (changed files, AC -> test map, mutant -> killing test,
what only hosted CI will verify), add the task note `HOSTED-PRECHECK-REQUESTED: lint, small, core, app-server and
all mutants`, and end your turn WITHOUT handing off.

## Out of scope

- Do not change parsing behaviour, guardian, rollout-trace, P4a/P4c/P5 logic or the `exec_notification` tool.
- The P5 `notify_on_exit` parameter on `exec_command` is advertised only on capable hosts (TUI). Whether the
  server also pins `exec_command` is not yet known; the orchestrator's live TUI trial (AC4) will tell. Do not
  remove it, but mention in your results where it is added so a follow-up can gate it if needed.
- No README, docs or CI changes.
