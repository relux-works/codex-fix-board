# Brief: independent research of a patch series that fixes Codex goal-mode token burn

You are an independent second-opinion researcher. The primary session (Claude Opus 5.5) already produced a
patch plan. Your job is to form your own view from the primary sources and the code, then confront the existing
plan: confirm, correct, replace, or extend it. Do not rubber-stamp it.

## Inputs (precondition resources on this task)

| Resource | What it is |
|---|---|
| `article.md` | Full text of the source article, https://relux.works/en/blog/codex-goal-token-burn/ (fetched 2026-09-29). Primary source for the defect. |
| `tekacs-9ffcf8d.trimmed.patch` | Third-party fork commit that adds background exec completion notifications. `models.json` hunk summarized in its header. |
| `tekacs-fork-analysis.md` | Prior verdict: the fork does NOT fix the article's defect, and why. |
| `research.md` | The primary session's current patch plan for upstream (P1-P6 + config). This is the thing to challenge. |

Repository: upstream `openai/codex`, pinned at `33a0f766a647208b471cfbcad889c67fd324ee04` (main, 2026-09-28).
The Rust workspace is under `codex-rs/`. Follow `AGENTS.md` / `codex-rs` conventions when proposing code.

Recommended order: read `article.md` and the relevant code first and write down your own problem list and fix
ideas; only then open `research.md` and compare.

## Decision to unblock

Which exact patch series to implement against upstream `openai/codex` main so that every token-burn mechanism
described in the article is fixed: the set of patches, the design of each (files, functions, data flow), their
order, and the tests that prove each one. Concretely: a verdict on each of P1-P6 in `research.md`
(agree / modify / reject, with reasons) plus anything the plan missed.

- Frozen precondition: not applicable. No wire format or grammar is frozen by this research. The proposed
  `<exec-command-completed>` fragment is a suggestion, not a contract.
- Worker-time budget: 90 minutes wall clock, including writing the outcome.
- Artifact budget: one outcome Markdown document (target under 40 KB). Code sketches inline. No archives, no
  copied corpora.
- Serial-prerequisite budget: this is the only research leaf. The next leaf is implementation. Do not propose
  another research leaf. Put open points as stated bounds for implementation instead.
- Exit criteria: every question below answered with evidence, or explicitly marked unresolved with the reason
  and the cheapest way to resolve it during implementation. A final recommended patch series table.
- First production slice (consumer of this research): P1 (integral-float argument normalization), then the
  P5 + P4a pair (completion notification plus goal continuation gating) as the first vertical slice.

## Questions to answer

1. **Article coverage.** Build your own table: every token-burn mechanism and every proposed fix in
   `article.md` -> its current state in upstream at the pinned commit, with `file:line` evidence. Flag anything
   `research.md` got wrong or missed. Check for relevant upstream changes after the article date (2026-09-11)
   via `git log`, e.g. #44320 "Block goals after three empty automatic continuation turns".
2. **P1 float normalization.** Is `core/src/tools/handlers/mod.rs` `parse_arguments` the right single choke
   point? Which handlers bypass it (for example `plan.rs`, `mcp.rs`, `mcp_resource.rs`, dynamic/extension tools,
   multi-agent tools)? Any field where turning `60000.0` into `60000` would change semantics? Should integer
   parameters advertise `integer` instead of `number` in the tool JSON schema? Check whether `codex_tools::JsonSchema` supports it.
3. **P2 sleep exposure.** Is gating `clock.sleep` on `turn_trigger == "goal"` reliable? Is the trigger set
   before the tool router is built? What about the first user turn that creates the goal? Is there a cleaner
   "goal is active" signal reachable from `core/src/tools/spec_plan.rs` without coupling core to the goal
   extension crate? Compare with "always_on when goals are enabled".
4. **P4a gating: the most important design point.** Where should "do not start a goal continuation while
   notified background work is pending" live? Options: in the goal extension (it queries the thread), or in core
   (`emit_thread_idle_lifecycle_if_idle` suppresses or annotates idle while such work exists, which also affects
   other idle contributors such as the queue extension). Handle long-lived processes that never exit (dev
   servers, watchers, `tail -f`): they must not park a goal forever. Should waking be opt-in per call (for
   example a `notify_on_exit` / background flag on `exec_command`) instead of implicit on every yield? What
   fallback timer is right?
5. **P5 delivery on upstream.** Upstream has no `Session::inject_or_start`. What is the correct way for the
   unified-exec exit watcher to deliver model input to an active turn or start a turn when idle? Options include
   `inject_if_running` plus `CodexThread::start_turn_if_idle` via `agent_control`, or a new session-level
   submission. Enumerate the races: a turn starting concurrently; the process exiting during the initial yield
   window; user-initiated terminate/kill; session shutdown; subagent threads; resume after restart; many
   processes finishing at once. Say how each is handled.
6. **P4b backoff.** Define "low-activity automatic turn" precisely using data already recorded in
   `ext/goal/src/accounting.rs`. Define the interaction with the existing 3-empty-turn blocker. Define how a
   scheduled delayed continuation is cancelled or pre-empted (user input, goal update/clear, thread stop,
   exec completion) and whether the backoff state survives resume. Compare with Claude Code (first check-in
   after 30 min, doubling, at most 3 check-ins without a human, stop after several tool-less turns).
7. **Subagents.** The article's source session was an orchestrator waiting on child work. When a Codex
   subagent finishes, does the parent get woken (see `core/src/agent/control/completion.rs` and `trigger_turn`
   usage)? If a goal-mode parent waiting on subagents also spins, what patch covers it?
8. **Prompt channel.** Does the remote model catalog fetched at runtime override the bundled `models.json`
   `base_instructions` / `instructions_template` (for example gpt-5.5's "Do not end your turn while
   `exec_command` sessions ... are still running")? If yes, which channel reliably reaches the model: tool
   descriptions, the continuation template, developer instructions?
9. **Contract rewrite (P3).** Propose the exact replacement text for the "verified wait" rules in
   `ext/goal/templates/goals/continuation.md`. It must be consistent with P2, P4 and P5: never tell the model to
   use a tool that may not exist in that turn.
10. **Anything else.** Missed mechanisms, simpler alternatives, risks to upstream acceptance, tests that must
    exist (unit + `core/tests/suite` integration), and a rough size per patch.

## Constraints

- Read-only with respect to repository sources: do not modify tracked files, do not commit, do not push, do not
  open PRs, do not contact external services beyond reading public pages if your sandbox allows it.
- Builds are optional and bounded. Use `cargo check -p <crate>` or a single targeted test only to settle a
  factual question. No full-workspace build or test run.
- Evidence: cite `path:line` at the pinned commit for every code claim. Mark anything not verified as
  "unverified".
- Write the outcome in English. Write it to a scratch file outside tracked sources, for example
  `$TMPDIR` or a gitignored `.temp/` path, then attach it with
  `task-board resource add <TASK-ID> <file> --type outcome --name <TASK-ID>_goal-token-burn-astra-review.md`.

## Outcome document structure

1. Summary: your verdict in ten lines or fewer.
2. Article coverage table (Q1).
3. Per-patch verdicts P1-P6, with corrected designs where you disagree.
4. Answers to Q2-Q10.
5. Final recommended patch series: order, files, tests, size, risk.
6. Unresolved points as stated bounds for the implementation leaf.
