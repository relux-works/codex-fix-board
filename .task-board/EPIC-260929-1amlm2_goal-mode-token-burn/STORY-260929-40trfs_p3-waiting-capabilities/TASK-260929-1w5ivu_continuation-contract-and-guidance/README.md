# TASK-260929-1w5ivu: continuation-contract-and-guidance

## Description
continuation.md verified-wait replacement and the conditional developer fragment (<= 3 KiB / 1K tokens). Detailed AC before spawn.

## Scope
ext/goal/templates/goals/continuation.md verified-wait paragraph replacement (line 24) plus a conditional developer fragment selected in Rust from the TASK-260929-2is91w snapshot. A core bounded fragment in core/context carries the exec capability paragraph even without a goal; the goal ContextContributor adds goal-specific DeveloperCapabilities. Exact texts are in final-plan.md section 9; do not reword them. Bundled models.json cleanup is optional and out of scope.

## Acceptance Criteria
AC1 Contract text. In ext/goal/templates/goals/continuation.md, replace the verified-wait bullet (line 24, "A verified wait polls a specific process...") with the exact final-plan §9 paragraph, prefixed by "- ". Apply the same change to every template variant that carries the bullet (with and without update_plan). Change no other line. A test asserts the rendered continuation prompt contains the exact new paragraph and none of the removed "confirmed live now" text.
AC2 Developer capabilities. `waiting_capability_fragments` (ext/goal/src/steering.rs, the hook P3-1 left empty) renders, from this step's WaitingCapabilities snapshot, exactly the §9 sentences, in a fixed order:
- exactly one of the exec_notify / not-exec_notify sentences;
- the sleep sentence iff sleep;
- the stdin sentence iff stdin;
- the native_wait sentence iff native_wait, together with the snapshot's ACTUAL tool name;
- the native_mail_wait sentence iff native_mail_wait.
Rust selects static strings; no new template syntax. The §9 "none of the positive flags" no-wait/end-turn paragraph is NOT emitted in this leaf: plan §10 defers it until P4b pacing is active, and a follow-up adds it after P4b-2 lands.
AC3 Scope. The fragment is contributed only while the thread's goal is active, through goal's ContextContributor. Threads with no goal, or a paused, blocked or complete goal, get nothing, and non-goal sessions see no model-visible change. Orchestrator decision: §9's core exec paragraph for goal-less threads is out of scope, because it would change model-visible context for every session. State this in the results.
AC4 Bounded. For the maximal flag set, the rendered fragment is at most 3 KiB and at most 1,000 tokens (test over every flag combination; use the repo's token estimator if one exists, else bytes/4). The only variable datum, the native wait tool name, is bounded by a hard cap with a test. Use only the existing PromptFragment/context path. If a new injected item type is unavoidable, it lives in core/context and implements ContextualUserFragment.
AC5 Incremental, no churn. Identical capabilities on consecutive sampling steps add no new context item. A capability change adds exactly one updated fragment on the next sampling request: a native wait discovered via tool search, a goal set mid-thread (post-create), or a goal that stops being active. No history rewrite.
AC6 Request agreement (core suite, real /responses requests via test_codex). The fragment's claims match the tools in the SAME request:
- sleep sentence iff the clock.sleep tool is present;
- code-mode-only gives no sleep sentence;
- a remote model catalog disabling clock support gives no sleep sentence;
- an excluded receipt tool gives the negative exec sentence;
- a headless host gives the negative exec sentence;
- post-create: the next request carries the fragment;
- a non-goal thread has no fragment.
Each test asserts the request count.
AC7 Tool descriptions. Check that the exec_command, write_stdin, clock.sleep and native wait descriptions do not contradict the fragment. Change one only if it does contradict, and report the check either way.
AC8 Mutants, each killed by a named test:
- the exec sentence ignores the flag (always positive);
- the sleep sentence is unconditional;
- the native wait name is hard-coded;
- the fragment is emitted for a non-goal thread;
- the old verified-wait text is restored;
- the tool-name cap is removed.
Plus any mutant the producer finds for AC5. Every killer must be selected by the filter.
AC9 Size and placement. Target under 600 changed lines including tests. No new code in codex-core unless AC4 forces it. Tests go in sibling *_tests.rs files, ext/goal/tests and core/tests/suite.
AC10 Measurement. Report model requests per test scenario and the byte and token size of the maximal fragment.
