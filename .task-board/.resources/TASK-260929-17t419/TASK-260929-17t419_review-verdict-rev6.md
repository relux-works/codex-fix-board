# Review verdict — TASK-260929-17t419 CR rev 6 (reviewer claude-sonnet-5-5)

Verdict: **accepted** (accept_cr). Candidate tree ece69834ba82a0aa95440f5ecc4eedf9f894b9ab; worktree diff vs candidate tree was empty (44 files).

## Previous verdict (rev 2) check
Finding `sibling-arg-parser-not-adapted` (guardian permissions `as_i64`, rollout-trace typed ints) is fixed:
guardian/permissions.rs now parses `session_id` via `codex_tools::arguments::i32`; rollout-trace `DispatchedWriteStdinArgs` uses the exact adapters.
Driving tests pass: `write_stdin_integral_decimal_session_id_keeps_lifecycle_and_hook_arguments_exact` (session_id 1000.0 permission context == 1000) and the rollout-trace reducer tests (123.0/250.0/2000.0, fractions refused).

## Surface table
| Row | Result |
|---|---|
| error surface | **held** |

Attacks run through public entry points that did NOT reproduce:
- Differential fuzz of the adapter (u64/i64/i32/usize + option_usize) against an exact Python `Decimal` oracle: 47,764 lexemes (random sign/int/fraction/exponent incl. +/- exponents, leading/trailing zeros, >20 digits, exponent 99999999999999999999, -0, boundaries 2^63/2^64/2^31, 0.0000000000000000000001e22, 1.0000000000000001, 9007199254740993[.0]): 0 mismatches. Harness `.temp/rev6-scratch/{src/main.rs,fuzz.py}`.
- Fractional / string / boolean on every annotated field via real handlers: exec_command (yield/timeout/max_output), write_stdin (session_id/yield/max_output), wait_agent V1+V2, sleep, create_goal token_budget, code-mode nested exec — existing `failed to parse function arguments:` envelope asserted (goal: no row created).
- Accepted decimals through the production entry: sleep 1000.0 (suite), exec/write_stdin clamp tests, one-shot exec timeout, wait V1/V2 30000.0, create_goal 20000000.0.
- Borrowed-input proof re-verified: every production parse of the annotated structs is `serde_json::from_str` (parse_arguments, parse_arguments_with_base_path, memory_usage.rs:46, ext/goal tool.rs:419, guardian, rollout-trace); no from_value/from_reader/flatten/untagged on these structs.
- Consumer sweep: grep of Value-style accessors (`["key"]`, `.get("key")`, `as_i64/as_u64`) for the six keys: no remaining production reader of the waiting-tool arguments besides the adapted ones (other hits are state/thread-store rows and config).
- Hook `updatedInput` rewrite (`rewrite_function_string_argument`, single caller exec_command.rs:544): raw-lexeme map preserves untouched numbers; non-object / invalid JSON errors unchanged; covered by lifecycle test (9007199254740993.0 preserved).
- Advertised schemas: only annotated params switched to integer; snapshots contain hash/args lines of clock/collaboration/exec_command/write_stdin only; no .snap.new/.pending-snap.
- AC 6: dynamic tool payload 1.0 remains f64 (`tool_search_returns_deferred_dynamic_tool_and_routes_follow_up_call`).

## Commands (real exit codes, my own runs, INSTA_UPDATE=no)
| Command | Exit | Result |
|---|---:|---|
| just test -p codex-tools | 0 | 122/122 (.temp/rev6-review/tools-01.log) |
| just test -p codex-rollout-trace -p codex-goal-extension | 0 | 99/99 |
| just test -p codex-core --retries 3 -E (integral/fractional/wrong_typed/sleep/dynamic/code-mode nested/spec/lifecycle/clamp filters) | 0 | 23/23 |
| cargo fmt --all -- --check | 0 | clean |
| git diff --check (base..candidate) | 0 | clean |

Reused from producer (not rerun by me): M1/M6/G1/R1 narrowing-mutant kills, clippy (`just fix`), scenarios snapshot suite (two quarantined astra tests known-baseline), app-server suite (gate, guardian_v2 websocket test quarantined). Not run: Windows/foreign-exec lanes, full core suite.

AC coverage: 6 of 6 rows driven.

## Findings (prose copy)
```json
{"findings": [], "notes": [
 "rewrite_function_string_argument now collects into BTreeMap<String, Box<RawValue>>: key order is sorted; previously serde_json::Map, which is insertion-ordered when any crate in the build enables preserve_order (tui does). Semantically irrelevant for JSON arguments.",
 "wait_agent V1 acceptance test asserts only that 30000.0 is accepted (not timed_out), not that the parsed value is the one applied; adapter-level exactness is covered by the tools unit tests and the fuzz.",
 "R1 mutant was not rerun after the test rename (producer disclosed).",
 "Change size 948 lines exceeds the 800 guidance; producer justified as one coherent stage (handlers + sibling readers must agree).",
 "did not reproduce: n/a (no analyst reproductions supplied)."
]}
```

## Machine-readable verdict

```verdict-findings
{
  "findings": [],
  "notes": [
    "rewrite_function_string_argument collects into BTreeMap<String, Box<RawValue>>: keys sorted; the old serde_json::Map is insertion-ordered only when a crate in the build enables preserve_order. Semantically irrelevant for JSON arguments.",
    "wait_agent V1 acceptance test asserts only that 30000.0 is accepted, not that the parsed value is applied; exactness is covered by the tools adapter tests and the differential fuzz.",
    "R1 mutant was not rerun after the producer renamed its test (disclosed by the producer).",
    "Change size 948 lines exceeds the 800-line guidance; producer justified one coherent stage."
  ],
  "surface_results": [
    {"row": "error surface", "result": "held"}
  ],
  "free_hunt": []
}
```
