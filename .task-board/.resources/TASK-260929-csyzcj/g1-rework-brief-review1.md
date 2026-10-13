# TASK-260929-csyzcj (G1): review rev1 changes_requested. One blocking finding, then request precheck 6

The verdict is `TASK-260929-csyzcj_review-verdict-rev1.md` (precondition). Panel A (codex sol high) requested changes and panel
B (muse max) accepted. The merged verdict is changes_requested on surface row "child state transitions". Every other row held,
and precheck 5 was fully green with 6/6 mutants killed. Keep everything else byte-identical unless this finding requires a change.
`g1-rework-mini-addendum.md` still applies: no local cargo or just. Your candidate is already in the worktree.

## Finding `interrupted-fragment-outside-context` (severity bypass)
AGENTS.md, "Model visible context" rule 6: every injected fragment must be defined as a struct in `core/context` and implement
`ContextualUserFragment`. Your new `format_inter_agent_interrupted_message` (`core/src/session_prefix.rs:44-51`) builds the
INTERRUPTED text with a raw `format!`. `core/src/agent/control/completion.rs:95-122` sends that String as queue-only
InterAgentCommunication, so it reaches model input with no typed fragment.

Required:
1. Add a typed fragment in `core/context`. Model it on `core/src/context/inter_agent_completion_message.rs`
   (`InterAgentCompletionMessage`): either a new `InterAgentInterruptedMessage` struct in its own module, or a variant of
   the existing type if that stays clean. Implement `ContextualUserFragment` with its own `content_kind`, matching the
   completion message's role and markers. Keep the exact current text, `Message Type: INTERRUPTED` and no `FINAL_ANSWER`,
   and keep it bounded (fixed text plus two paths). Register the module in `core/context/mod.rs` like its siblings.
   `format_inter_agent_interrupted_message` must render via that fragment (`.render()`), as
   `format_inter_agent_completion_message` already does. Put a unit test for the fragment body in a sibling `*_tests.rs` via
   `#[path]`, with a whole-string `assert_eq!`.
2. Real-interruption integration coverage in `core/tests/suite/goal_native_wait.rs`, driven through the production path.
   Interrupt a real Running native child of a goal parent that holds the marker, using the real interrupt entry point that
   the existing suites use (find how `interrupt_agent` / `TurnAbortReason` are driven in `core/tests/suite`). Assert:
   (a) the registered parent gets exactly ONE queue-only interrupted notice and exactly one wake model request for that
   transition, with the notice body containing `Message Type: INTERRUPTED` and never `FINAL_ANSWER`;
   (b) an ordinary parent (no goal, no marker) gets no notice and no wake request;
   (c) the child's global `is_final` is unchanged.
   Use bounded waits that panic with clear messages (no hangs) and match mocks to exactly one request each (the precheck-3
   lesson).
3. A narrowing mutant on the PRODUCTION delivery guard in `completion.rs`, not on the string formatter. For example: deliver the
   interrupted notice to an ordinary parent too, or deliver it twice per transition. Name the test from item 2 that must
   kill it. Keep the 6 existing mutants and make sure every patch applies to your final tree with correct hunks.

Formatting: there is still no rustfmt on this host. Format every new line by hand to rustfmt style: 100 columns, method
chains broken one call per line once they don't fit, closures in block form when they break, trailing commas. Precheck 3 and
precheck 4 both failed on exactly this. Then update `TASK-260929-csyzcj_results.md` (coverage map, now with the real-interruption
rows) and `TASK-260929-csyzcj_mutants.json`, leave everything UNCOMMITTED, add the note `HOSTED-PRECHECK-REQUESTED: precheck 6`,
and end your turn without handing off. Text-only evidence (R176).
