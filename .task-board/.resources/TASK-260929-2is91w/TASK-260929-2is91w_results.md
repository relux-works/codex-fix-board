# TASK-260929-2is91w — waiting-capabilities-snapshot: precheck 14 review handoff

Candidate tree: `afb8c830d764ba489a9f2f922c0babdf1dbe036e`. Worktree remains UNCOMMITTED. No repository files were edited during this handoff run.

## Current evidence

Hosted precheck 14 (`TASK-260929-2is91w_hosted-precheck-14.md`), run 38191980780, ref relux/ci-next: lint, small, app-server and core lanes green; 15/15 mutants killed, 0 survivors. This is accepted hosted evidence, not tests rerun locally by this producer.

The first snapshot-core job 114628508769 failed `encrypted_parent_reply_survives_incremental_guardian_reviews` at its event timeout on all three retries. Same-snapshot rerun job 114648017069 passed that test in 1.6s and core 5122/5122. The orchestrator records this as a base flake. The failed first attempt remains part of the evidence.

Precheck 12 actually killed 14/15 mutants: the remote replacement mutant survived despite the initial summary saying all killed. The surviving path gap is now closed. Precheck 13 stopped at lint, before mutant validation.

## Review refusal closed

AC5 now has attacks for 5/5 configuration families. `remote_catalog_replacement_changes_waiting_snapshot` drives the real ModelsManager fetch and `apply_remote_models` into a real session. Four cases cover List remote-only and Hide same-slug merge, each adding/removing clock support. Each case asserts one /models GET and one /responses POST: 4 + 4 total. Hide cases assert catalog size, bundled-only slug survival, and replaced visibility/tools, proving the merge branch ran.

The Hide cases kill `snapshot_ignores_remote_catalog_replacement`; List cases cannot, because that mutant changes only the merge assignment. The mutant touches ModelsManager because that assignment resides there; candidate production code in ModelsManager is unchanged. This closes the rev4 recording refusal on configuration coverage; recording reviewer must assess the new revision.

Preserved orchestrator fixes:
- Test fix 10: the post-discovery recorder runs on a second turn with changed approval policy; contributors run only on turn-context changes. No product re-emission change.
- Lint fix 14: clone the snapshot inside a scoped MutexGuard before awaiting get_remote_models, resolving await_holding_lock without changing assertions.
Earlier provenance, normalizer parity (including server/client null IDs), tool exposure and clippy fixes are preserved.

## Scope and size for reviewers

21 changed files, 2,619 additions and 6 deletions (2,625 changed lines), including 1,483 lines in waiting_capabilities_tests.rs. This exceeds the repository's normal 800-line guidance; no scope expansion/refactor was made in this evidence-only handoff. Production snapshot module is 309 lines, extension-api contract 59 lines.

Changed paths are core session/mod.rs, step_context.rs and tests.rs; core tools/mod.rs, multi_agent_tool.rs, registry.rs, router.rs, waiting_capabilities.rs and waiting_capabilities_tests.rs; V1/V2 wait handlers; core suite exec_notification.rs and search_tool.rs; extension-api contributors/context.rs, lib.rs, waiting_capabilities.rs and tests/registry.rs plus tests/waiting_capabilities.rs; goal extension.rs, steering.rs and tests/steering.rs.

The snapshot remains bounded/transient and shared through both context paths. Goal receives it without new prompt text. Existing update_plan_enabled continuation rendering is retained for the separate prompt leaf; this is an explicit scope limit from prior results.

## Verification performed in this run

- `bash /Users/administrator/Developer/ReluxWorks/codex/.temp/goal-token-burn/impl/mini-hosted-gate.sh`: exit 0; exact candidate tree matches hosted precheck 14.
- Initial `cargo fmt -- --config imports_granularity=Item --check` lookup: exit 127 (cargo absent from shell PATH). Resolved existing guarded executable; no install or bypass.
- `/Users/administrator/.cargo/bin/cargo fmt -- --config imports_granularity=Item --check` from codex-rs: exit 0; expected stable-channel imports_granularity warnings. Read-only check, no formatting edits.
- Each of the 15 existing mutant patches ran as standalone `git apply --check -`: exit 0 for each; Python orchestration exit 0. No mutant applied.
- `git diff --check`: exit 0.
- All 11 checklist items were already checked; refreshed attribution is hosted precheck 14 and the evidence above. No unexecuted command was checked as green.
- No local Rust builds, checks, clippy or tests executed (Mac mini R194/R223); those results are solely hosted precheck evidence.
- No temporary directories created by this run. Hosted gate's temporary index is removed by its exit trap. No CODEX_HOME copied, installed codex run, commit, push or branch operation.

The prior coverage map and implementation rationale below are retained as historical context. Its precheck-13 request and tree are superseded by the evidence above.

---

## Historical producer results: TASK-260929-2is91w results: waiting-capabilities-snapshot — precheck-12 survivor rework (merge branch) requesting precheck 13

## Rework scope

Precheck 12 (run 38177362699, tree `b9982d792cb1c0a956377a5ea2845b1b46055d80`): all four lanes green, 14/15 mutants killed. `snapshot_ignores_remote_catalog_replacement` SURVIVED: in mutant-14 core the integration test `suite::search_tool::remote_catalog_replacement_changes_waiting_snapshot` ran and PASSED with the mutant applied.

Cause (confirmed from `models-manager/src/manager.rs:672-702`): `apply_remote_models` only executes the same-slug merge (`models[index] = model;`) when `remote_only` is false. `remote_only` is true when any remote model has `ModelVisibility::List` AND (API-key discovery OR a ChatGPT account). The precheck-12 helper used `CodexAuth::create_dummy_chatgpt_auth_for_testing()` plus a same-slug remote cloned from bundled (visibility `List`), so the remote catalog REPLACED the whole list and the mutated line never ran. The test proved the snapshot follows the remote entry on the remote-only path; it did not touch the merge path the mutant narrows.

Required fix (`a1-rework-brief-precheck12.md`): keep the existing remote-only cases, add merge-path case(s) with `remote_only` false through a real configuration, assert the snapshot follows the REMOTE entry plus request counts, and prove the merge branch ran so the test cannot silently fall back to remote-only again. Keep the mutant as is; all 15 mutants must apply to the final tree.

## Changes this round (test only, 1 file)

`codex-rs/core/tests/suite/search_tool.rs`:

- `remote_catalog_replacement_case` gains `visibility: ModelVisibility`. The remote entry sets `remote.visibility = visibility` before serving. `List` keeps the remote-only path; `Hide` makes `remote_only` false (no `List` entry) while dummy ChatGPT auth keeps `should_refresh_models` true, so `apply_remote_models` takes the merge branch. Session resolution is unaffected: explicit `.with_model(slug)` returns as-is via `get_default_model`, and `get_model_info` uses longest-prefix match with no visibility check.
- Merge proof (only when `visibility != List`), via `test.thread_manager.get_models_manager().get_remote_models().await`:
  - `remote_models.len() == catalog.models.len()` (merge keeps bundled size; remote-only would be 1).
  - A bundled-only slug (first bundled slug != replaced slug) is still listed alongside the replaced one.
  - The replaced entry carries the remote `visibility` (`Hide`, not bundled `List`) and the remote `experimental_supported_tools` (exact `Vec` equality against the cloned expectation). With the mutant (`let _ = (index, model);`) the replaced entry keeps bundled visibility/tools, so this fails.
- The test function keeps the two `List` cases (remote-only, both directions) and adds two `Hide` cases (merge, both directions) with identical slugs/tools/expectations:
  - `gpt-5.5` + `clock` → `sleep: true, stdin: true` (adds; bundled lacks clock).
  - `gpt-6-astra` − `clock` → `sleep: false, stdin: false` (removes; bundled has clock; `code_mode_only` keeps `stdin` nested).
- New import: `codex_protocol::openai_models::ModelVisibility` (item-granularity line, ordered before `ModelsResponse`).

No production, `Cargo.toml`/`Cargo.lock`, Bazel, schema, or template changes.

## Killer for the surviving mutant

`snapshot_ignores_remote_catalog_replacement` (one-line: `models[index] = model;` → `let _ = (index, model);` in `apply_remote_models`):

- Killers: the two new `Hide` (merge) cases inside `remote_catalog_replacement_changes_waiting_snapshot`. Both drive the merge branch; either alone kills. Primary: `gpt-5.5` + `Hide` (remote adds `clock`; mutant keeps bundled `[]`, so snapshot `sleep` is `false` vs expected `true`, request tools lack `clock.sleep`, and the replaced-entry tools/visibility assertions fail). The `gpt-6-astra` + `Hide` case kills symmetrically (mutant keeps `clock`, snapshot `sleep` is `true` vs expected `false`).
- Why the remote-only (`List`) cases cannot kill: with `List` + ChatGPT auth, `remote_only` is true, `apply_remote_models` skips the merge entirely (`*current = entry` with the single remote model), so the mutated line never executes. The snapshot still follows the remote entry, and the test passes with or without the mutant.

## Changed files vs precheck-12 tree

1 file vs `b9982d792cb1c0a956377a5ea2845b1b46055d80`.
Final candidate tree: `eac03387046423d643c4d201896940787a7f8bfa` (temp index: `GIT_INDEX_FILE=$TMP git read-tree HEAD`, `GIT_INDEX_FILE=$TMP git add -A`, `GIT_INDEX_FILE=$TMP git write-tree`); worktree remains UNCOMMITTED.

- `codex-rs/core/tests/suite/search_tool.rs` — `visibility` param, merge-proof block, two new `Hide` cases, one import (~60 lines added).

## Coverage map (AC rows to tests)

AC1 — flags with exact derivation (unchanged): `direct_sleep_counts`, `nested_only_sleep_does_not_count`, `deferred_sleep_does_not_count_until_discovered`, `discovered_deferred_sleep_counts`, `direct_write_stdin_counts`, `nested_only_write_stdin_does_not_count`, `v1_wait_agent_carries_its_namespaced_name`, `v2_wait_agent_carries_its_configured_name`, `v1_wait_tool_reports_its_namespaced_name`, `v2_wait_tool_reports_its_configured_name`, `custom_v2_namespace_reports_its_configured_name`, `nested_only_wait_agent_does_not_count`, `foreign_dynamic_wait_agent_does_not_claim_native_wait`, `foreign_dynamic_wait_agent_with_native_disabled_yields_none`, `v2_wait_disabled_with_namespaced_decoy_yields_none`, `discovered_deferred_v1_wait_counts_with_native_provenance`, `exec_notify_true_with_host_opt_in_and_controls`, `available_host_with_policy_enables_notification_flags`, `exec_notify_requires_available_host`, `exec_notify_requires_notify_opt_in`, `exec_notify_requires_write_stdin`, `exec_notify_requires_receipt_control`, `missing_exec_command_schema_disables_exec_notify`, `excluded_receipt_tool_disables_exec_notify`, `excluded_exec_command_disables_exec_notify`, `native_mail_wait_requires_host_and_installed_policy`, `native_mail_wait_requires_available_host`, `native_mail_wait_requires_installed_policy`.

AC2 — final-router derivation (unchanged): prior tests plus `server_tool_search_output_counts_without_call`, `client_tool_search_output_without_call_id_counts_like_normalizer`, `server_null_id_discovery_updates_waiting_capabilities`, `discovered_native_wait_updates_waiting_capabilities`, `discovered_v1_wait_updates_next_step_snapshot`.

AC3 — subscriptions are not capabilities (unchanged): `pending_and_acknowledged_work_does_not_flip_flags` + `acknowledged_subscription_does_not_flip_waiting_capabilities`.

AC4 — one snapshot, both paths (unchanged): `same_snapshot_instance_reaches_both_context_paths`.

AC5 — configurations, 5/5 families (remote leg extended this round):

- Remote catalog → `remote_catalog_replacement_changes_waiting_snapshot` (real `/models` same-slug replacement through `apply_remote_models` into a real session; now 4 cases: remote-only `List` add/remove + merge `Hide` add/remove, each with merge-proof assertions on the `Hide` legs). The prior `snapshot_follows_catalog_clock_support` remains as the resolved-`ModelInfo` unit control.
- Hard/reminder off → `snapshot_follows_sleep_switches`.
- Headless/exec → `headless_exec_host_keeps_exec_but_disables_notification_flags`.
- Code-mode → `code_mode_only_hides_nested_waits_but_keeps_direct_sleep`.
- Excluded receipt tool → `excluded_receipt_tool_disables_exec_notify`.

AC6 — bounded and transient (unchanged): `waiting_snapshot_does_not_persist_to_history_or_rollout`; struct is 4 bools + 1 `Option<ToolName>`, no collections, not persisted.

AC7 — narrowing mutants: same 15 as precheck 12 (no new mutant; the survivor now has a merge-path killer). All verified `git apply --check` clean against tree `eac03387046423d643c4d201896940787a7f8bfa`. Prior killers in `TASK-260929-2is91w_hosted-precheck-11.md` and `TASK-260929-2is91w_hosted-precheck-12.md` unchanged, except the survivor's killer is now the `Hide` merge cases.

## Validation

- `cargo fmt -- --config imports_granularity=Item` — exit **0** (nightly-only warnings expected).
- `cargo fmt -- --config imports_granularity=Item --check` — exit **0**.
- 15/15 mutant patches `git apply --check` clean against the final tree (verified via loop over `TASK-260929-2is91w_mutants.json`).
- Local Rust builds/checks/clippy/tests were **not run**, as prohibited on this host (Mac mini R194/R223). Hosted precheck 13 must run lint, small, core, and app-server lanes plus all 15 mutants with the precheck-12 filter (already includes `test(remote_catalog)`).
- Hand-read for recurring hosted lint failures: no redundant closures (field-access closures only), inlined format args (`{slug}`, `{bundled_only}`), no `vec!` where an array works (all `vec!` move into `Vec`-typed sinks), no single-arm match, no cfg(test)-only helpers used from production, no unused imports, no opaque positional literals needing `/*param*/` comments (only `&str` literals which are exempt, plus `ModelVisibility::List/Hide` enum variants and `BodyPrintLimit::Limited(80_000)` matching existing usage).

Request counts (asserted in code): each of the 4 cases performs exactly 1 `/models` GET and 1 `/responses` POST (single assistant-message turn). The test function as a whole therefore performs 4 `/models` + 4 `/responses` across 4 isolated mock servers/builds. No second turn is needed because contributors run on the first step's full initial context.

## Outcome-scoped logbook

The precheck-12 survivor is a path-coverage gap, not a product defect: `apply_remote_models` has two same-slug behaviors (remote-only replace vs merge), and only the remote-only path was exercised. `Hide` visibility is the minimal real configuration forcing the merge: it keeps ChatGPT refresh (`should_refresh_models` true) while making `remote_only` false (no `List`), and session resolution ignores visibility (explicit model + prefix match). The merge-proof assertions (catalog size, bundled-only survival, replaced visibility + tools) pin the branch so a future fallback to remote-only fails loudly instead of silently passing. No temporary directories were created; the one `/tmp` results scratch file is deleted before ending the turn. No real CODEX_HOME copied, no installed `codex` used, no commit/push/branch operation performed. Worktree remains UNCOMMITTED.

## Precheck 13 request

Candidate tree `eac03387046423d643c4d201896940787a7f8bfa` (worktree uncommitted).
Run: fmt-check, clippy, small-crate tests, codex-core unit tests `tools::waiting_capabilities_tests`, suite `search_tool::remote_catalog_replacement_changes_waiting_snapshot` (now 4 cases) plus the two prior waiting/discovery suite tests, suite `exec_notification::acknowledged_subscription_does_not_flip_waiting_capabilities`, and the 15 mutants in `TASK-260929-2is91w_mutants.json` with killers per this results file (survivor killer: the `Hide` merge cases). Hosted filter is the precheck-12 filter (already includes `test(remote_catalog)`).
