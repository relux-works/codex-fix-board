# TASK-260929-1w5ivu (P3-2): CR revision 3 — hosted precheck 6 review handoff

## Summary

Revision 1 was rejected with F1 (stale sleep sentence after goal stop, no
correction) and F2 (~1.2 KB per-turn churn: the turn-context path has no
baseline). Both share one cause, and this revision fixes both by moving the
waiting guidance into a goal-owned World State section, per
`a2-rework-brief-review1.md`:

- New `ext/goal/src/waiting_world_state.rs`: section `goal_waiting_guidance`
  (developer role, own markers), snapshot = five flags + capped native wait
  name while `GoalActivity` is present, `false` after it lapses, no section
  at all for threads that never had an active goal. Active→inactive renders
  exactly one static retraction; unchanged snapshots render nothing.
- `GoalExtension` now implements `contribute_world_state` instead of
  `contribute_turn_context` (fragment path removed; no double emission).
  Renderer, sentences, order, cap, and the AC1 template are byte-identical.
- Thin orchestrator-authorized core touch: `waiting_capabilities` added to
  `WorldStateContributionInput` (extension-api), passed at its single
  production construction site (core `world_state.rs`, 1 line), plus the 21
  skills-test constructions `git grep` finds. Nothing else in codex-core
  changes; no P4b code touched.

The old turn-boundary bound is SUPERSEDED: World State runs on every sampling
step, so the post-create follow-up carries the fragment and the
post-completion follow-up carries the retraction. Agreement now holds on
every request. AC3 is amended to allow exactly the one transition retraction.

## Hosted verification and orchestrator fixes

Hosted precheck 6, run `38286079342` on `ivanopcode/codex`, ref
`relux/ci-next`, verified tree `0909471501a910f604164a2bba7b586e2ebf9ba8`.
Lint, small, core and app-server lanes are green. All 8/8 supplied mutants
were killed; 0 survivors. Evidence: `TASK-260929-1w5ivu_hosted-precheck-6.md`.
This handoff session accepted that attached hosted evidence; it did not rerun
Rust builds, lint or test suites locally (Mac mini R194/R223).

Three orchestrator fixes are included, with no suite assertion changes:

- Precheck 3 failed lint (run 38255143212). P4b added
  `GoalExtensionConfig.continuation_pacing`; the test fixture now sets it from
  `Feature::GoalContinuationPacing` at `core/tests/suite/waiting_guidance.rs:216`,
  matching `app-server/src/extensions.rs:87`. Evidence:
  `TASK-260929-1w5ivu_orch-lint-fix-4.md`.
- Precheck 4 failed 9 of 11 waiting-guidance tests (run 38256663093).
  Core strips null object fields before persisting World State snapshots
  (`core/src/context/world_state/mod.rs`, `remove_null_object_fields`).
  Writing `native_wait: null` made fresh and restored snapshots unequal and
  appended duplicate guidance. The renderer snapshot now omits an absent
  native wait name (`ext/goal/src/waiting_world_state.rs:63`); the unit pin
  was updated accordingly. The earlier units compared an unstripped
  contribution snapshot against itself, so only the real core persistence
  exercised by the suite caught the round-trip defect. Evidence:
  `TASK-260929-1w5ivu_orch-test-fix-5.md`.

- Review revision 2 requested A2-F1: the new `#[path]`-included source was
  absent from Bazel's integration compile inputs. `ext/goal/BUILD.bazel:13`
  now lists `src/waiting_world_state.rs` in `integration_compile_data_extra`.
  This is the only candidate change since revision 2; no test assertion
  changed. Evidence: `TASK-260929-1w5ivu_orch-bazel-fix-6.md`.
  Precheck 6 verifies the corrected tree through the hosted Cargo lanes;
  a Bazel execution was not run locally or claimed by that evidence.
- A2-N1 measurement correction: the ≤512 B snapshot unit pin covers its ASCII
  fixture, not every supported name. Static JSON measurements across 16 flag
  combinations per name class give ASCII 218–222 B, four-byte Unicode
  602–606 B, and escaped controls 858–862 B (128 capped characters plus
  ellipsis). This broadens the measurement report without changing the
  frozen candidate or claiming additional Rust tests. Section markers total
  47 B; maximal wire is 1771 B / 443 estimated tokens.

The recorded orchestrator decision supersedes the former turn-boundary bound:
World State provides per-request agreement, one transition retraction (AC3
amendment), and minimal core snapshot plumbing (AC9 exception). No decision
is pending. The revision-1 changes_requested verdict and reject routing are
already recorded in `TASK-260929-1w5ivu_review-verdict-rev1.md` and
`TASK-260929-1w5ivu_recording-review-rev1.md`; F1/F2 regressions and their
mutants are verified by precheck 6.

## Base verification (before editing)

- `git rev-parse HEAD` = `7e4289e21fab653fea8c0089a7ffd790145e5686` (P4b trunk).
- Temp-index tree before edits = `9ff1a412eb6cf6a74f0ebf44ae92631ccc01b882`
  (matches the brief's starting candidate).
- `ext/goal/src/extension.rs` keeps both `GoalActivity` and `PlanCommitInput`
  imports (3-way merge conflict resolved as briefed).

## Changed files

| File | Change |
|---|---|
| `ext/goal/BUILD.bazel` | Declare the new path-included source for Bazel integration tests (A2-F1) |
| `ext/goal/src/waiting_world_state.rs` (new, 140 lines) | Section, snapshot, retraction, retained matcher |
| `ext/goal/src/extension.rs` | `contribute_turn_context` → `contribute_world_state` + import swap |
| `ext/goal/src/steering.rs` | `render_native_wait_tool_name` → `pub(crate)` (1 word; renderer untouched) |
| `ext/goal/src/lib.rs` | `mod waiting_world_state;` |
| `ext/extension-api/src/contributors/world_state.rs` | New `waiting_capabilities` field + doc + import |
| `core/src/session/world_state.rs` | Pass `&step_context.waiting_capabilities` (1 line) |
| `ext/skills/tests/skills_extension.rs` + `presentation_dedup_tests.rs` | 21 mechanical field insertions + 1 import (compile fixups) |
| `ext/goal/tests/waiting_world_state.rs` (new, 320 lines) | 9 unit tests: zero footprint, all diff arms, retraction pin, matcher, snapshot bounds |
| `core/tests/suite/waiting_guidance.rs` | Bound pins flipped to presence/retraction; new F2 cross-turn test; retraction assertions in stop/discovery/excluded-receipt/tool-created |
| `ext/goal/tests/steering.rs`, `templates/goals/continuation.md`, `core/tests/suite/mod.rs` | Unchanged from rev1 (carried) |

Changed lines against HEAD: 422 additions + 29 deletions tracked, plus
1500 untracked lines (1040 suite + 140 module + 320 unit) = **1951**
versus the 600 target. Production is 255 changed lines (including removals);
1696 are tests. The overrun remains disclosed; no repository file was edited
in this handoff session. Counts include untracked files, which ordinary
`git diff --stat` omits.

## Fix map (every changed expectation with its deciding file:line)

### F1 → retraction on the first request after the stop

- `on_tool_finish` reconciles and removes the marker without needing a live
  manager (`ext/goal/src/extension.rs:552-571` → `runtime.rs:198-214`
  `reconcile_activity` → `activity.rs` publisher removal), so the follow-up
  step's world-state build sees inactive + a recorded active entry and
  renders the retraction (`waiting_world_state.rs:106-130`).
- Recording precedes input assembly on every sampling step
  (`core/src/session/turn.rs:509` → `mod.rs:3701-3738`), so the retraction is
  in the follow-up request's history.
- `waiting_guidance_goal_stop_adds_no_new_fragment`: requests[1..3] share one
  fragment (sleep tool present); requests[3] carries the retraction exactly
  once with no new fragment (sleep tool absent); requests[4] adds nothing
  (retraction still 1, fragment still 1) while its context update is recorded.
- Same shape pinned in `waiting_guidance_tool_created_goal_reacts_at_next_turn`
  (requests[3]) and `waiting_guidance_excluded_receipt_tool_gives_negative_exec_sentence`
  (requests[1]).

### F2 → diffed section, no per-turn duplication

- Unchanged snapshot renders `None` (`waiting_world_state.rs:93-100`); the
  turn boundary only rebuilds the same snapshot, so no new item is appended.
  The verdict's `record_context_updates` re-invocation now diffs instead of
  duplicating (`core/src/context_manager/history.rs:446-463`).
- New `waiting_guidance_unchanged_capabilities_stable_across_turns`: 3 turns,
  1 request each, preset active goal → every request shows each marker exactly
  once (one fragment total in history).
- `waiting_guidance_discovered_native_wait_updates_fragment` pins
  exactly-one-more on change: requests[1] fragment without native; requests[2]
  adds one updated fragment (shared sentences 1→2, native 0→1, dotted name 1);
  requests[3] (turn 2) adds nothing; requests[4] retracts.

### Render-diff arms (all exhaustive, Unknown justified)

- Active + Known(equal) → None; Known(different, incl. `false`) → full
  fragment; Absent → full fragment (activation, or re-render after compaction
  evicted the fragment while the snapshot survived — core maps that to Absent
  via the retained matcher, `core/src/context/world_state/mod.rs:420-435`).
- Active + Unknown → full fragment. Unreachable (no legacy matcher
  registered), pinned to fail visible: unlike the template's boolean policy,
  an untyped history hit cannot prove the five flags and tool name match.
- Inactive + Known(object) → one retraction; Known(false)/Absent → None;
  Unknown → retraction (mirrors the template; corrects possibly-stale
  history; unreachable today).
- Retained matcher requires markers + one exec sentence, so the
  marker-sharing retraction never counts as retained guidance.

### Rollout effect

Threads that never activate a goal contribute no section: no
`goal_waiting_guidance` entry anywhere (zero footprint, verified by the
non-goal suite test and the zero-footprint unit test). Ever-active threads
carry a small entry: the flag object while active, a stable `false` after the
retraction. No `retain_world_state_after_compaction` override: every
compaction path converges to exactly-once re-render (baseline kept →
retained-miss → Absent → render; baseline dropped → Absent → render), and the
retraction needs no re-render once both it and the old guidance left history.
Covered by unit tests (Absent arm + matcher); a full compaction integration
test is disproportionate because the re-render trigger is core's generic
mechanism, already covered by core's own world-state tests — the
section-specific surface is exactly the pinned arms.

## AC coverage map (deltas vs rev1; unchanged rows condensed)

- AC1 Contract text — unchanged (template + unit pin carried).
- AC2 Sentences — unchanged renderer; world-state body reuses
  `waiting_capability_fragments` text (slot/kind envelope replaced by the
  section envelope). Deferred no-wait paragraph still absent (unit pin).
- AC3 Scope — same `GoalActivity` gate (Active + BudgetLimited); amended to
  allow exactly the one transition retraction. No-goal/paused/blocked/
  complete/UsageLimited contribute no active guidance; a previously recorded
  section contributes the one transition retraction and then remains silent. No core goal-less paragraph
  (orchestrator decision, out of scope).
- AC4 Bounded — renderer bounds carried (80-combination + cap tests); added
  snapshot-shape test (exact 5-key object, capped ASCII name, ≤512 serialized
  bytes for that fixture; general static upper shape 862 B) and beyond-cap-equality test. Only variable datum still the capped
  name. Existing World State path only; no new item type.
- AC5 Incremental — per-step diff: no-churn same-turn (carried), new
  cross-turn stability, tool-created per-request agreement, discovery
  exactly-one-more, goal-stop retraction + silence. No history rewrite.
- AC6 Request agreement — every test asserts the exact request count;
  "matches the same request's tools" now means the most recent guidance or
  retraction in that request's history (exact per-request count tuples).
  Cases: post-create iff loop, tool-created, code-mode-only, remote catalog,
  excluded receipt (+retraction), headless, post-create, non-goal.
- AC7 Tool descriptions — unchanged from rev1 (checked, no contradictions,
  nothing changed; panel A re-verified the same files).
- AC8 Mutants — 8/8 below (6 kept/rewritten + 2 new; emitted-twice retired:
  the renderer is still called once and the unit `len() == 1` asserts remain,
  while cross-turn duplication is now attacked by always_renders).
- AC9 Size/placement — logic in ext/goal; core production delta is the
  authorized 1-line pass-through (+ extension-api field, not core); tests in
  ext/goal/tests + core/tests/suite (+ skills compile fixups). 1951 lines
  disclosed above.
- AC10 Measurement — below.

## Mutant → killer → filter map

Filter for every killer:
`test(waiting) | test(guidance) | test(continuation) | test(goal)`.
Suite killers live in `suite::waiting_guidance`; unit killers are
`waiting_guidance_*` / `continuation_*` in `ext/goal/tests`.

| Mutant | Primary killer (must fail with mutant applied) | Needs |
|---|---|---|
| `waiting_exec_sentence_ignores_flag` (always positive) | `waiting_guidance_post_create_carries_fragment_matching_tools` + tool-created requests[1..3] negatives; co-killers: headless, excluded, no-churn ×2, stop, discovery | `test(waiting)` on codex-core |
| `waiting_sleep_sentence_unconditional` | `waiting_guidance_remote_catalog_without_clock_omits_sleep_sentence`; co-killers: post-create requests[0] (iff), tool-created requests[0], non-goal, stop/discovery pre-goal requests | `test(waiting)` on codex-core |
| `waiting_native_wait_name_hardcoded` (literal `wait_agent`) | `waiting_guidance_discovered_native_wait_updates_fragment`; co-killer: unit `waiting_guidance_selects_sentences_per_flag` (custom namespace) | `test(waiting)` on codex-core (unit: codex-goal-extension) |
| `waiting_fragment_emitted_for_non_goal_thread` (rewritten: gate + active/inactive branch in `waiting_world_state.rs`) | `waiting_guidance_non_goal_thread_has_no_fragment`; co-killers: unit zero-footprint test, every pre-goal `assert_no_fragment` | `test(waiting)` on codex-core |
| `waiting_old_verified_wait_text_restored` | unit `continuation_prompt_carries_section_nine_verified_wait_contract` (both variants) | `test(continuation)` on codex-goal-extension |
| `waiting_tool_name_cap_removed` | unit `waiting_guidance_native_wait_tool_name_is_capped` (+ bound overlong cases + snapshot cap test) | `test(waiting)` on codex-goal-extension |
| `waiting_world_state_always_renders` (Known arm ignores comparison) | suite `waiting_guidance_unchanged_capabilities_stable_across_turns` (F2's test: requests[0] alone shows 2); co-killers: no-churn same-turn, unit unchanged-renders-nothing | `test(waiting)` on codex-core |
| `waiting_world_state_no_retraction` (active→inactive arm returns None) | suite `waiting_guidance_goal_stop_adds_no_new_fragment` (requests[3] retraction 0 vs 1); co-killers: tool-created requests[3], excluded requests[1], unit retracts test | `test(waiting)` on codex-core |

## AC10 measurements

Model requests per suite scenario (each asserted with `assert_eq!`):

| Scenario | Requests |
|---|---|
| post-create / sleep-iff (service-driven) | 2 |
| tool-created goal per-step agreement (test retains its original name) | 4 |
| code-mode-only agreement | 1 |
| remote catalog clock-off | 1 responses + 1 /models |
| excluded receipt tool | 2 |
| headless host | 1 |
| non-goal thread | 1 |
| no-churn (3 in-turn steps) | 3 |
| no-churn across turns (new) | 3 |
| goal stop | 5 |
| native-wait discovery | 5 |
| Total | 28 responses + 1 /models |

Fragment sizes (renderer unchanged, so body sizes are rev1's; wire adds the
47-byte section markers):

| Fragment | Bytes | Tokens (ceil/4) |
|---|---|---|
| Maximal body (all flags + 128×4-byte-char capped name) | 1724 | 431 |
| Maximal wire (+ markers) | 1771 | 443 |
| Realistic maximal body (all flags + `multi_agent_v1.wait_agent`) | 1234 | 309 |
| Minimal body (all flags off) | 133 | 34 |
| Retraction body (static) | 88 | 22 |
| Retraction wire (+ markers) | 135 | 34 |
| Comparison snapshot (ASCII unit fixture) | 218 (≤512 test-bound) | — |
| Comparison snapshot (128 four-byte characters + ellipsis, all flags true) | 602 (static) | — |
| Comparison snapshot (four-byte names, maximal Boolean widths) | 606 (static) | — |
| Comparison snapshot (escaped controls, maximal Boolean widths) | 862 (static upper shape) | — |

Bounds hold with margin (1771/3072 bytes, 443/1000 tokens).

## Design notes and honest bounds

- Turn-start marker publication precedes context builds
  (`ext/goal/src/extension.rs:273-294` `on_turn_start` → reconcile), so
  first-turn preset-goal requests render through `render_full`
  (`core/src/session/mod.rs:4482`); later turns diff
  (`history.rs:446-463`); follow-ups diff per step (`turn.rs:509`).
- The verdict's accepted same-turn windows are gone (closed, not re-accepted):
  requests[1]-style follow-ups now carry the fragment and post-completion
  follow-ups carry the retraction.
- Gate scope still Active + BudgetLimited with no dedicated BudgetLimited
  suite test (disclosed, as rev1). Positive exec-notify and native-mail-wait
  sentences still unit-covered only (no suite flow installs a capable host
  with full controls or the admission marker for a goal turn). The no-wait/
  end-turn paragraph is still deferred (absence pinned).
- P4b suites (`goal_continuation_pacing`, core + app-server) assert timing and
  request counts, not developer texts (checked); the additive section cannot
  add requests. Their selected tests remain green in precheck 6 under `test(goal)`.
- Existing goal suites unaffected: activity tests assert tools only;
  background-wait asserts counts/warnings/markers the section does not
  perturb; turn_start developer asserts are existence/emptiness checks on
  goal-less threads (checked).

## Commands and exit codes

Directly run in this handoff session:

- `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh`
  → exit **0**, confirming exact uncommitted tree
  `0909471501a910f604164a2bba7b586e2ebf9ba8` against green hosted run
  `38286079342` (precheck 6).
- `git diff --check` → exit **0**.
- `/Users/administrator/.cargo/bin/cargo fmt -- --config imports_granularity=Item --check`
  → exit **0** (expected stable-channel imports_granularity warnings).
- Standalone `python3` static JSON measurement over 48 cases (16 flag
  combinations each for ASCII, four-byte Unicode, escaped controls)
  → exit **0**; sizes listed above. This models the serialized shape;
  it does not execute Rust or count as an additional passing Rust test.

Earlier producer/orchestrator evidence (accepted here, not rerun): rustfmt
and fmt-check exit 0; all 8 mutant patches apply cleanly. Hosted lint,
small-crate tests, core tests and app-server tests are green in precheck 6.
Raw hosted command exit codes are not supplied by the attached summary;
its recorded lane statuses and named mutant killers are the evidence used.
No local build/check/clippy/test or Bazel execution was attempted; fresh
binaries are prohibited on the mini by R194/R223. No commit, push or
repository edit was made. No temporary files or directories were created
by this session; the gate removes its own temporary index. The earlier
producer deleted its temp dir.

## Handoff logbook

Precheck 6 verifies the Bazel compile-data correction after review revision 2.
A2-F1 is addressed by the declared source input; A2-N1 is addressed by the
corrected and broadened static size measurements. Prior P4b fixture drift
and the null-snapshot persistence defect remain documented above. The retained-matcher/compaction claim is
unit-level, the positive exec-notify and native-mail-wait claims are unit-only,
and BudgetLimited has no dedicated suite case. The no-wait paragraph stays
deferred. These bounds remain visible for review; hosted 8/8 mutant coverage
is not claimed to be 9/9 independently mutated surface rows.
