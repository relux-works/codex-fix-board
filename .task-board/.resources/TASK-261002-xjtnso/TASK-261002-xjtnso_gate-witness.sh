#!/usr/bin/env bash
# Replays the gate's text pipeline (relux-ci.yml lines 127-135 @429a14a) on synthetic clippy --message-format=short output. No cargo.
set -o pipefail
RUNNER_TEMP=$(mktemp -d)
KNOWN_WARNINGS='core/src/tools/registry.rs: warning: unused import: `crate::tools::context::ToolCallSource`
core/tests/suite/scenarios.rs: warning: unused import: `codex_protocol::openai_models::ReasoningEffort`
'
run() {
  printf '%s' "$1" > "$RUNNER_TEMP/clippy.log"
  printf '%s\n' "$KNOWN_WARNINGS" | sed '/^$/d' > "$RUNNER_TEMP/known-warnings.txt"
  sed -E 's/\x1b\[[0-9;]*[A-Za-z]//g' "$RUNNER_TEMP/clippy.log" \
    | sed -nE 's/^([^ :]+):[0-9]+:[0-9]+: (warning: .*)$/\1: \2/p' | sort -u > "$RUNNER_TEMP/warnings.txt"
  new="$(grep -v -x -F -f "$RUNNER_TEMP/known-warnings.txt" "$RUNNER_TEMP/warnings.txt" || true)"
  if [ -n "$new" ]; then echo "  GATE FAILS: $new"; else echo "  GATE PASSES"; fi
}
echo "A) control: new unused import in tools/src/lib.rs"; run $'tools/src/lib.rs:4:5: warning: unused import: `std::fmt`\n'
echo "B) cargo-level warning with no file:line:col span"; run $'warning: unused manifest key: package.foo\nwarning: `codex-core` (lib) generated 1 warning\n'
echo "C) 2nd occurrence of a baseline warning (same file+message, other line)"; run $'core/src/tools/registry.rs:16:5: warning: unused import: `crate::tools::context::ToolCallSource`\ncore/src/tools/registry.rs:900:5: warning: unused import: `crate::tools::context::ToolCallSource`\n'
echo "D) build-script warning (cargo:warning=)"; run $'warning: codex-core@0.0.0: something suspicious\n'
