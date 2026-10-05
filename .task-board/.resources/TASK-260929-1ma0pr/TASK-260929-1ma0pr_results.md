# TASK-260929-1ma0pr results — exec-completion fragment + TurnInput (rev 4, CR rev 2 handoff on hosted precheck 3)

Status: ready for review — handing off CR rev 2.
Worktree tree `5b2ea16af484965b3dd34f6ca4198dd903732541` confirmed by
temp-index `git read-tree HEAD` + `git add -A` + `git write-tree` (exit 0,
hash matches the precheck-3 tree exactly). Candidate left UNCOMMITTED.
No file changed since the precheck-3 snapshot.

Hosted precheck 3 (`TASK-260929-1ma0pr_hosted-precheck-3.md`) ran this exact
tree three times from snapshot a743b625 on CI branch ci/relux-ci-queue
(which adds `codex-queue-extension` to the small and lint lanes): runs
37317650053, 37349767142, 37352331583 — all four lanes green every time.
Core: 4967 passed, 0 flaky (run 37349767142). Small: 260/260 including both
queue regression tests. All 10 narrowing mutants killed, 0 survivors
(runs 37317381008–37317628533). Precheck-2 evidence (tree `808000cb`,
base run 37302805027) is superseded for the base; every mutant re-ran and
re-killed on this tree.

## Summary

New `core/src/context/exec_completion.rs` implements `ContextualUserFragment`
for background exec completions: receipt/process ids, exit/failure/timeout and
retention state, no command, no raw output. Every rendered fragment is wrapped
in the recognized `<codex_internal_context source="exec_completion">` wrapper,
escaped, and capped at 768 UTF-8 bytes with an explicit `[truncated]` marker.
At most 8 fragments go into one sampling request; the remainder stays retained
in the runtime mailbox.

New internal `TurnInput::ExecCompletion(Vec<RuntimeLease>)` variant in
`core/src/session/input_queue.rs` carries leased completions (snapshot +
sampling token) from idle wake to the record path. Serialization is refused
(manual `Serialize` impl returns an error; `skip_deserializing` rejects the
variant on the way in), and existing variants serialize byte-identically
(pinned by shadow-enum + literal tests). The record path renders only
contextual `ResponseItem`s, so the rollout holds no receipt/lease/trigger
metadata and resume replays data without rearming.

Public `protocol::TurnInput` is intentionally unchanged (final plan 5.2: keep
public protocol/RPC variants unchanged). The app-server/queue persistence paths
already reject non-user payloads without panic; this leaf adds a regression
test proving a forged `ExecCompletion` queue payload is discarded.

## Changed files

Production:

- `codex-rs/core/src/context/exec_completion.rs` (new, 197 LoC):
  `ExecCompletion` snapshot, `ExecOutputRetention`, `ExecCompletionFragment`
  (`ContextualUserFragment`), 768-byte cap, 8-per-request cap, escaping.
- `codex-rs/core/src/context/mod.rs`: module + exports.
- `codex-rs/core/src/session/input_queue.rs`: `TurnInput::ExecCompletion`
  variant, manual `Serialize` (refusal + byte-identical existing arms),
  `enqueue_runtime_notification` carries the snapshot,
  `lease_runtime_notifications_up_to(limit)`, Mailbox activity for the variant,
  plus the `has_pending_input` production fix (see below).
- `codex-rs/core/src/session/runtime_mailbox.rs`: entries/leases carry the
  admission snapshot, `lease_available_up_to(limit)`, uncapped lease kept as
  `#[cfg(test)]`.
- `codex-rs/core/src/session/turn.rs`, `tasks/review.rs`: totality arms
  (completions are not user input).
- `codex-rs/core/src/hook_runtime.rs`: inspect arm (no hooks for completions),
  record arm (leases render to contextual `ResponseItem`s via
  `record_conversation_items`; no metadata persisted).
- `codex-rs/core/src/tasks/mod.rs`: idle wake leases up to 8 and extends
  pending input with one `TurnInput::ExecCompletion`.
- `codex-rs/core/src/unified_exec/completion_receipt.rs`: `ReceiptId::model_handle`
  (hyphenated UUID for model context; `Debug` stays opaque).
- `codex-rs/core/src/codex_thread.rs`: test helper builds a matching snapshot
  (round 2: shared inner + `test_enqueue_..._without_wake(count)` staging
  hook; test-only, no production behavior change).

Tests:

- `core/src/context/exec_completion_tests.rs` (new): AC1–AC3 unit tests.
- `core/src/session/input_queue.rs` tests: AC2 batching, AC4 serde/byte-identity,
  activity; existing runtime tests updated for the new enqueue signature.
- `core/src/session/runtime_mailbox_tests.rs`: signature updates + snapshot
  carriage + capped-lease primitive.
- `core/src/session/turn_input_tests.rs`: enqueue signature updates.
- `core/tests/suite/exec_completion.rs` (new) + `suite/mod.rs`: AC5 resume/rearm
  suite tests + AC2 end-to-end batching (round 2: 9-batch stages pre-turn;
  assertions unchanged).
- `core/tests/suite/runtime_mailbox.rs` (leaf 1): wake assertions updated —
  the wake now records fragment(s) instead of recording nothing (round 2:
  two-entry test stages pre-turn; assertions byte-identical).
- `ext/queue/tests/queue_service.rs`: forged `ExecCompletion` queue payload
  regression test (AC4 persistence half).

No app-server or protocol production-code changes (audited, see design notes).

## C2 rework record, round 2 (review rev 1 + racy wake test -> precheck 3 green)

Review round 1 (`TASK-260929-1ma0pr_review-verdict-rev1.md`) is
changes_requested with one finding, `queue-test-coverage-attestation`
(severity bypass, repeat-of none). Answer:

- The finding is CORRECT: base run 37302805027 never selected
  `codex-queue-extension`, so the rev-2 results file wrongly attributed the AC4
  queue regression test to it. Corrected evidence: queue tests are cited from
  runs that select the queue crate (run 37312042951 small job 111769562161
  first proved it on tree `808000cb`; precheck 3's run 37349767142 small lane
  re-proves it on THIS tree — 260/260 including
  `codex-queue-extension::queue_service forged_exec_completion_payload_is_skipped_without_panic`
  and `drain_leaves_persisted_queued_message_for_a_later_start`). The AC4
  and surface-table rows below cite the precheck-3 run.
- Kept reviewer notes (both panels agree): the "<= 8 fragments" AC is read
  as incremental admission per sampling request, not a cumulative-history
  cap (final plan 5.2 permits normal history repetition; the suite asserts
  9 cumulative fragments on the second wake). Review size is ~2310 lines;
  the suggested coherent split is: (1) mailbox foundation, (2) bounded
  fragment + serde, (3) record/wake wiring with integration coverage.

Race fix (`two_runtime_entries_still_start_one_wake_turn` failed 3/3 in run
37312042951's core job 111769561926 with left=1, right=2):

- Root cause (test bug, not production): the test enqueued each entry
  post-idle with its own wake call. `on_task_finished` emits TurnComplete
  BEFORE clearing `active_turn` and running its trailing `maybe_start`
  (`tasks/mod.rs`, with a `flush_rollout` await in between), so each
  per-enqueue wake raced that trailing wake across a millisecond window.
  When the first wake won, it leased 1 of 2 entries and the "one wake
  records both" assertion flaked. (Precheck 2 passed by timing luck.)
- Fix, no sleeps, no loosened assertions: new test-only staging hook
  `CodexThread::test_enqueue_exec_completion_notifications_without_wake(count)`
  (shared inner `test_reserve_and_enqueue_exec_completion` with the
  existing single-entry helper; same production
  `InputQueue::enqueue_runtime_notification` call site). Both multi-entry
  suite tests now stage the full batch BEFORE the initial turn: no wake
  can fire mid-batch (no turn lifecycle, mail, or abort exists yet — all
  six `maybe_start` call sites need one), the busy initial user turn gates
  every wake (`start_or_steer` never consults trigger-mailbox state and
  never leases runtime entries — production leases happen only in
  `maybe_start_turn_for_pending_work_with_sub_id`), and the single
  post-turn idle wake leases the whole batch (2, or capped 8+1). The
  `two_runtime...` assertions are byte-identical; the `nine_pending...`
  assertions are unchanged (its 1..=8 ranges already tolerate every split;
  staging additionally removes its latent 3-wake flake).
- No production change: a completion that arrives mid-wake riding the next
  wake is the specified retain-without-loss behavior (pinned by the
  batching unit test + rollout-history assertions), so no enqueue
  coalescing was added. The test's "exactly ONE wake" invariant is about
  entries pending before the wake starts, which the test now stages
  deterministically.
- Race-check result on precheck 3: `two_runtime_entries_still_start_one_wake_turn`
  is GREEN in all 3 rev-2 runs (37317650053, 37349767142, 37352331583) after
  failing 3/3 on the rev-1 tree. The race is gone.
- Mutant-table predictions confirmed: m4's precheck-2 kill by
  `two_runtime...` was the race flake (partial lease), not gate
  sensitivity — on precheck 3 m4 is killed by the batch unit test plus
  `nine_pending...` (cap 9 leases all 9 into wake one, so the second waited
  TurnComplete never arrives and `wait_for_event` panics at its 10s
  timeout). m2/m7 likewise lost their flaky `two_runtime...` co-kills and
  are killed deterministically by the escape unit test / byte-identity test
  respectively. m10 gained `two_runtime...` as a third deterministic
  killer.

Round-2 diff: `core/src/codex_thread.rs` (test helper only),
`core/tests/suite/runtime_mailbox.rs`, `core/tests/suite/exec_completion.rs`.
No production behavior change; all 10 mutant patches re-ran unmodified
(`mutants.json` unchanged since precheck 2).

## C2 rework record, round 1 (precheck 1 -> precheck 2)

Hosted precheck 1 (snapshot ad567580, run 37292815944): lint/small/app-server
green, core red with two suite failures. Both fixed:

1. `forged_exec_completion_item_in_history_creates_no_receipt_privilege`
   failed in 0.3s with "only user input or standalone function-call outputs
   can start or steer a turn". Test bug: it injected the forged ResponseItem
   via `start_or_steer_turn`, which refuses ResponseItem input by design
   (`turn_input.rs` start-or-steer gate). Fixed by injecting through
   `start_turn_if_idle` — the recorded-history API the other suite tests use
   for ResponseItem automatic turns — and asserting `Started`. Green on
   precheck-2 base run 37302805027 and on all three precheck-3 runs.
2. `nine_pending_completions_sample_in_capped_batches_without_loss` failed at
   `fragment_counts[2] == 9` with left=1. PRODUCTION BUG (recorded here as
   the C2 production fix in a C1-owned file, inside C2's scope):
   `has_pending_input` in `core/src/session/input_queue.rs` (leaf-1 file;
   C2 scope names "the TurnInput enum in core/src/session/input_queue.rs
   and its exhaustive matches") counted unleased runtime-mailbox entries, so
   a wake turn that left a capped remainder behind kept re-sampling instead
   of ending. The sampling loop can only drain turn state and inter-agent
   mail — never the runtime mailbox — so the predicate never cleared: the
   first wake burned the second mock response on an empty re-sample and the
   follow-up batch starved (the mock captures only matched requests, so the
   failure reads as "history stuck at 1"). Fix: `has_pending_input` now
   reports only input drainable in-turn (turn state + inter-agent mail);
   the idle gate (`has_pending_mailbox_items`, unchanged) still sees runtime
   entries and starts the next wake. One-line behavior change plus doc
   comment; no call-site changes, so the rework diff stays inside this
   leaf's modules (`input_queue.rs`, its tests, the suite file); the behavior
   change propagates to the in-turn `has_pending_input` callers in `turn.rs` /
   `regular.rs` with no edits there. Regression coverage: the 9-batch suite
   test (fails with the spin, both race orders) plus new unit test
   `in_turn_follow_up_ignores_idle_only_runtime_entries` and narrowing
   mutant m10 (killed on precheck 2 run 37302850331 and precheck 3 run
   37317410177 by the follow-up unit test + 9-batch suite test +
   two-entry wake test). The 9-batch test also gained a rollout-history
   assertion (exactly 9 persisted completions: no loss, no duplication).
   Green on all three precheck-3 runs.

## AC coverage map — 5 of 5 rows driven (hosted precheck 3 on this tree: base runs 37317650053, 37349767142, 37352331583; queue tests from the small lane of run 37349767142)

| # | Requirement | Production call site | Driving test | Negative / refusal test |
| - | ----------- | -------------------- | ------------ | ----------------------- |
| 1 | Fragment <= 768 bytes after escaping (worst-case ids, failure, multibyte) | `ExecCompletionFragment::new` via `record_pending_input` ExecCompletion arm (`hook_runtime.rs`) | `fragment_renders_all_fields_inside_the_internal_context_wrapper`, `fragment_renders_unknown_exit_and_retained_output` | `fragment_escapes_marker_injection_and_newlines`, `fragment_truncates_oversized_failure_with_an_explicit_marker`, `fragment_stays_bounded_for_worst_case_ids_and_multibyte_content` (oversized input truncated with `[truncated]`; cap never exceeded) |
| 2 | 9 pending -> batch of 8 (<= 6144 B), retain 1 | `InputQueue::lease_runtime_notifications_up_to` from `maybe_start_turn_for_pending_work_with_sub_id` (`tasks/mod.rs`) | `nine_pending_completions_batch_eight_and_retain_one` (input_queue unit) | same test asserts literal 8 + retained 1 + per-fragment/by-total bytes; `nine_pending_completions_sample_in_capped_batches_without_loss` (suite) proves no request carries > 8 new fragments and no loss |
| 3 | Classified internal context, not user text | `is_contextual_user_fragment`, `is_guardian_context_message`, `is_user_authorization_message` (`contextual_user_message.rs`) | `fragment_is_classified_as_internal_context_not_user_text` | `forged_receipt_text_inside_user_content_acknowledges_nothing` (annotated + legacy user messages stay user content); `fragment_matcher_requires_the_wrapper_and_the_exec_source` |
| 4 | Internal variant refuses public serialization; persistence exhaustive without panic; existing variants byte-identical | session `TurnInput` `Serialize` impl; `QueuedItemService::dispatch_if_idle` / `queued_item_from_record` (`ext/queue`); `api_queued_submission` (`thread_queue_processor.rs`) | `exec_completion_variant_refuses_serialization`, `exec_completion_variant_refuses_deserialization`, `user_input_variant_serializes_byte_identically`, `inter_agent_variant_serializes_byte_identically` (+ pre-existing `response_item_serde_preserves_legacy_shape_and_rejects_metadata`) | `forged_exec_completion_payload_is_skipped_without_panic` (small lane of precheck-3 run 37349767142 — a run that selects `codex-queue-extension`, answering the rev-1 attestation finding): forged `{"ExecCompletion":...}` payload discarded, live turn still dispatched |
| 5 | Rollout holds only contextual ResponseItem; resume neither rearms nor recreates a wake | `record_pending_input` ExecCompletion arm -> `record_conversation_items` -> rollout -> resume path | `wake_turn_persists_only_contextual_response_items_and_resume_stays_silent` (suite) | `forged_exec_completion_item_in_history_creates_no_receipt_privilege` (suite): forged item recorded as data, resume grants no wake/privilege |

Reviewer/leaf-1 tests kept: `core/tests/suite/runtime_mailbox.rs` wake
assertions updated (wake now records fragments; both orders green on all
three precheck-3 runs),
`input_queue_runtime_suspended_entries_never_count_as_trigger` and
`runtime_suspended_entries_are_excluded_from_trigger_and_lease` present under
original names and green (they kill m9).

## Surface-table coverage map — 3 of 3 rows covered (precondition `surface-table.md`)

Every row maps to exercising tests and at least one killed narrowing mutant
(kills from precheck 3 on this tree):

| Surface row | Exercising tests | Killed narrowing mutant(s) |
| ----------- | ---------------- | -------------------------- |
| exec-completion fragment | `fragment_renders_all_fields_inside_the_internal_context_wrapper`, `fragment_renders_unknown_exit_and_retained_output`, `fragment_escapes_marker_injection_and_newlines`, `fragment_truncates_oversized_failure_with_an_explicit_marker`, `fragment_stays_bounded_for_worst_case_ids_and_multibyte_content`, `fragment_is_classified_as_internal_context_not_user_text`, `fragment_matcher_requires_the_wrapper_and_the_exec_source`, `forged_receipt_text_inside_user_content_acknowledges_nothing`, `forged_exec_completion_item_in_history_creates_no_receipt_privilege`, `two_runtime_entries_still_start_one_wake_turn` | m1 (cap 769, killed by batch unit test), m2 (escape drops `>`, killed by escape test), m3 (classifier rejects exec source, killed by classifier + escape + matcher tests), m5 (kind user-prefixed, killed by classifier + render tests) |
| batching and retention | `nine_pending_completions_batch_eight_and_retain_one`, `nine_pending_completions_sample_in_capped_batches_without_loss`, `in_turn_follow_up_ignores_idle_only_runtime_entries`, `two_runtime_entries_still_start_one_wake_turn`, `input_queue_runtime_suspended_entries_never_count_as_trigger`, `runtime_suspended_entries_are_excluded_from_trigger_and_lease` | m4 (batch cap 9, killed by batch unit + 9-batch suite tests), m10 (follow-up re-admits runtime, killed by follow-up unit + 9-batch suite + two-entry wake tests), m9 (pending admits suspended) |
| internal TurnInput variant and persistence | `exec_completion_variant_refuses_serialization`, `exec_completion_variant_refuses_deserialization`, `user_input_variant_serializes_byte_identically`, `inter_agent_variant_serializes_byte_identically`, `forged_exec_completion_payload_is_skipped_without_panic` (small lane, run 37349767142), `wake_turn_persists_only_contextual_response_items_and_resume_stays_silent` | m6 (serialize admits empty), m7 (user-input always emits order), m8 (record persists trigger metadata) |

## Mutant evidence — 10 of 10 killed, 0 survivors (hosted precheck 3 on this tree)

Patches in `TASK-260929-1ma0pr_mutants.json` (unchanged since precheck 2;
re-ran unmodified on this tree). Each mutant narrows its gate (weakens to
admit exactly one member of the rejected class); none is delete-only.

| Mutant | What it narrows the gate to | Named test(s) that fail (killing run) |
| ------ | --------------------------- | ------------------------------------- |
| m1-fragment-cap-769 | byte cap admits one extra byte | `nine_pending_completions_batch_eight_and_retain_one` (37317381008) |
| m2-escape-drops-gt | escaping admits `>` (keeps `&`, `<`) | `fragment_escapes_marker_injection_and_newlines` (37317438139) |
| m3-classifier-rejects-exec-source | existing classifier admits all-but-one source (unchanged gate; proves positive-test sensitivity; searched-for wrapper token preserved, behavior changed, killed by the behavioral core suite) | `fragment_escapes_marker_injection_and_newlines`, `fragment_is_classified_as_internal_context_not_user_text`, `fragment_matcher_requires_the_wrapper_and_the_exec_source` (37317464801) |
| m4-batch-cap-9 | batch cap admits one extra fragment | `nine_pending_completions_batch_eight_and_retain_one`, `nine_pending_completions_sample_in_capped_batches_without_loss` (37317490875) |
| m5-kind-user-prefixed | kind still classifies, but as user content (token preserved, classification changed) | `fragment_is_classified_as_internal_context_not_user_text`, `fragment_renders_all_fields_inside_the_internal_context_wrapper` (37317518170) |
| m6-serialize-admits-empty | refusal admits exactly empty batches | `exec_completion_variant_refuses_serialization` (37317545621, lint+core) |
| m7-user-input-always-emits-order | manual encoding admits null `acceptance_order` | `user_input_variant_serializes_byte_identically` (37317574233) |
| m8-record-persists-trigger-metadata | record admits ResponseItem plus one metadata class | `wake_turn_persists_only_contextual_response_items_and_resume_stays_silent` (37317600437, core+lint) |
| m9-pending-admits-suspended | pending admits exactly the suspended class | `input_queue_runtime_suspended_entries_never_count_as_trigger`, `runtime_suspended_entries_are_excluded_from_trigger_and_lease` (37317628533, core+lint) |
| m10-follow-up-readmits-runtime | in-turn follow-up re-admits exactly the idle-only runtime class (spin returns, follow-up batch starves) | `in_turn_follow_up_ignores_idle_only_runtime_entries`, `nine_pending_completions_sample_in_capped_batches_without_loss`, `two_runtime_entries_still_start_one_wake_turn` (37317410177) |

Survivors: none. Every mutant names its failing test(s); no survival bounds
to state.

Source-text gate (DoD item 8): the classifier/matcher gate is attacked by m3
and m5, which PRESERVE the searched-for wrapper/source token and change
behavior (reject exec source / classify as user content); the mutant harness
executed the full behavioral core suite (killed via core lane, including
suite-level `two_runtime_entries_still_start_one_wake_turn` for m10 and the
matcher/classifier unit tests), not only a static checker.

## Commands (exact, with real exit codes)

Local fast lane (from `codex-rs/`, with `NEXTEST_TEST_THREADS=4
INSTA_UPDATE=no INSTA_WORKSPACE_ROOT=$PWD`, after the target guard
(`codex-target-guard.sh`, exit 0, same checkout, cache kept) and a FREE
build-slot check) — recorded in rev 1, tree unchanged since:

- `just fmt` — exit 0 (run after edits; re-run before clippy; C2 re-run exit 0,
  no unrelated files touched).
- `just fix -p codex-core` — first run exit 101: 2 errors in new code
  (missing `&` for `serialize_newtype_variant` args), fixed. Second run
  exit 101: 1 error in new test (`None` needed `::<String>`), fixed; it
  also removed 2 pre-existing unused imports in untouched suite files,
  which were reverted. Final state verified by clippy instead to avoid
  re-dirtying the tree with unrelated fixes.
- `just fix -p codex-queue-extension` — exit 0. Reverted one unrelated
  pre-existing unused-import fix it applied to `core/src/tools/registry.rs`.
- `just clippy -p codex-core -p codex-queue-extension` — exit 0. Only
  remaining warnings are pre-existing unused imports in files this change
  does not touch (`tools/registry.rs`, `openai_file_mcp.rs`,
  `scenarios.rs`); zero warnings in changed files. C2 re-ran
  `just clippy -p codex-core` — exit 0 (3m57s; type-checks new/changed tests
  via `--tests`).
- `cargo fmt --check -p codex-core -p codex-queue-extension` — exit 0
  (nightly-option warnings are pre-existing config noise).
- `git diff --check` — exit 0.
- Mutant patch checks: `git apply --check` on all 10 patches after JSON
  roundtrip — clean (m10's first draft lost a trailing empty context line
  in JSON serialization and failed the roundtrip check; rewritten with a
  clean hunk boundary and re-verified).

Round-2 local fast lane (from `codex-rs/`, with
`NEXTEST_TEST_THREADS=4 INSTA_UPDATE=no INSTA_WORKSPACE_ROOT=$PWD`, after
the target guard and a FREE build-slot check):

- `codex-target-guard.sh` — exit 0 (same checkout, cache kept).
- `codex-fix-suite-busy.py --any` — `FREE`.
- `just fmt` — exit 0 (only the 3 touched files differ; no collateral).
- `just clippy -p codex-core` — exit 0, twice (2m58s; `--tests`
  type-checks the restaged suite tests). Only warnings are the 3
  pre-existing unused imports in untouched files (`tools/registry.rs`,
  `openai_file_mcp.rs`, `scenarios.rs`); zero warnings in changed files.
- Mutant roundtrip: `git apply --check` on all 10 `mutants.json` patches —
  9 clean as-is; m10 clean with a trailing newline (pre-existing stored
  form, unchanged since the precheck-2 kills; `git diff` of
  `input_queue.rs` untouched by round 2). `mutants.json` unchanged.
- `git diff --check` — exit 0.
- Temp-index tree verification — exit 0, hash
  `5b2ea16af484965b3dd34f6ca4198dd903732541`.
- `just fix` was NOT run (it previously dirtied unrelated files; clippy
  covers lints, fmt covers formatting).

Hosted precheck 3 on THIS tree (no local core/queue/app-server suites per
producer brief):

- Base runs 37317650053, 37349767142, 37352331583 (snapshot a743b625, CI
  branch ci/relux-ci-queue): app-server/core/lint/small all green in all
  three. Run 37349767142: core 4967 passed / 0 flaky (including every
  driving, negative, and reviewer test in the tables above, plus the
  deraced `two_runtime_entries_still_start_one_wake_turn`); small 260/260
  including `codex-queue-extension::queue_service
  forged_exec_completion_payload_is_skipped_without_panic` and
  `drain_leaves_persisted_queued_message_for_a_later_start`. (The first
  precheck-3 dispatch was cancelled by the per-SHA concurrency group and
  is superseded.)
- Mutant runs 37317381008, 37317410177, 37317438139, 37317464801,
  37317490875, 37317518170, 37317545621, 37317574233, 37317600437,
  37317628533: each red on its killing test(s) as tabulated (expected-red;
  proves the tests fail when the gate is narrowed). 10/10 killed,
  0 survivors.

Handoff run (this session): temp-index tree verification — exit 0, hash
`5b2ea16af484965b3dd34f6ca4198dd903732541` matches the precheck-3 tree
exactly. No file changed in this session.

Not run anywhere on this tree: nothing required remains unrun. Every AC
driving/negative test, both queue regression tests (on a queue-selecting
lane), and all 10 narrowing mutants executed on the exact candidate tree
via hosted precheck 3 (base x3 + mutants x10). Local core/app-server
suites were forbidden by the producer brief and are covered by the
hosted runs above.

## Out-of-contract rows (acceptance-criteria clauses)

- Sampling acknowledgement (story D; out of scope per task description):
  leases stay leased after the wake; ack/fail/suspend wiring is unchanged
  behind `#[allow(dead_code)]`.
- Tool exposure (story F; out of scope per task description):
  fragments carry the receipt handle but no tool guidance; no new tool.
- Active-turn delivery of runtime notifications (needs story-D admission
  semantics; explicitly deferred in-plan): the variant enables it, but only
  idle wake maps leases (leaf-1 comment updated accordingly).
- Rework diff bounded: round 1 touched only `input_queue.rs` (+ its unit
  tests) and `core/tests/suite/exec_completion.rs` — all inside the brief's
  scope ("the TurnInput enum in core/src/session/input_queue.rs and its
  exhaustive matches", fragment module with tests). The `has_pending_input`
  fix is a behavior change to a C1-owned function in a C2-scoped file,
  recorded above; no C1 test semantics were weakened (leaf-1 tests kept and
  green). Round 2 touched only the `codex_thread.rs` test helper and the 2
  multi-entry suite tests; no production behavior change, no weakened
  assertions.

## Design notes and bounds

- Snapshot-at-admission: the mailbox carries a point-in-time `ExecCompletion`
  snapshot captured at enqueue; the record path renders from it without store
  peeks (no TOCTOU against the sampling claim, which story D owns). Story E
  fills real process/failure/retention values at publication.
- The fragment reuses the existing internal-context wrapper and classifier
  verbatim (`InternalModelContextFragment` with source `exec_completion`);
  no matcher-list change was needed. Text matching stays syntactic (shared
  property of all internal fragments); authorization follows host
  annotations and acks follow lease tokens, so forged markers acknowledge
  nothing — pinned by the forged-text unit test and the forged-item suite test.
- `protocol::TurnInput` unchanged per final plan 5.2. Verdict note-4 touch
  points re-located at this base: `thread_queue_processor.rs`
  `api_queued_submission` (let-else returns error, no panic),
  `ext/queue` `prepare_queued_user_input` (let-else `InvalidInput`),
  `dispatch_if_idle` (warn + delete + continue on bad payload),
  `queued_item_from_record` (returns `InvalidPayload`, no panic). All are
  already exhaustive-safe; the new queue test pins the forged-variant case.
- Change size was estimated here at ~1340 lines (production ~440, tests
  ~900); the reviewer measured ~2310 additions across 18 files against the
  supplied base (includes the runtime-mailbox foundation). Over the 800-line
  review guidance because every AC row needs positive + negative + mutant
  coverage by this task's own DoD. Suggested split (reviewer's): (1) mailbox
  foundation; (2) bounded fragment + serde; (3) record/wake wiring with
  integration coverage.

## Findings and decisions (logbook-carrying section)

- Base reality vs plan citations: `TurnInput` split into public
  `protocol::turn_input::TurnInput` (3 variants, used by app-server/queue)
  and internal `session::input_queue::TurnInput` (4 variants). The new
  internal variant belongs to the latter; app-server needed audit + test,
  not code changes.
- Serde refusal uses a manual `Serialize` impl (runtime `Err`, narrowing
  mutants stay expressible) plus derived `Deserialize` with
  `skip_deserializing`. `skip_serializing` would also refuse, but every
  mutant touching it fails compilation (lease types have no Serialize),
  which would leave the gate without an executable narrowing mutant.
- `just fix` applies pre-existing unused-import removals in untouched files
  on every run; reverted twice (`tools/registry.rs`,
  `openai_file_mcp.rs`, `scenarios.rs`). Final tree contains only this
  task's files.
- `has_pending_input` must describe only in-turn-drainable input: counting
  idle-only runtime entries makes capped-remainder wakes spin on empty
  re-samples and starve the follow-up batch. The idle gate
  (`has_pending_mailbox_items`) is the runtime-mailbox trigger; the in-turn
  follow-up predicate must not see that class. Pinned by
  `in_turn_follow_up_ignores_idle_only_runtime_entries` + m10.
- TurnComplete is emitted before the turn is cleared: `on_task_finished`
  sends the terminal event, then flushes the rollout, then clears
  `active_turn` and runs the trailing `maybe_start`. Tests that enqueue
  per-item wakes after `wait_for_turn_complete` race that trailing wake
  across the whole flush window. Multi-entry wake tests must stage the
  batch where no wake can interleave (pre-turn staging), not enqueue
  post-idle item by item.
- Worktree left UNCOMMITTED; no commits, pushes, or branch operations.
