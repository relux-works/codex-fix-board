# TASK-260929-309h9n (P4b-2): review rev2 changes_requested. Replace the env kill switch with a typed feature flag, then request precheck 7

The verdict is `TASK-260929-309h9n_review-verdict-rev2.md`. Panel B and the delta panel accepted; panel A requested changes on
one row, `placement and size` (A2-F1, with the delta's D-N2 as the same observation). Every other row is held: spacing and
streak math, polls grow the streak, one live timer, ticket invalidation, blocker order, transient state, no model-visible
change, mutants. Keep all of that exactly as it is.

## 1. A2-F1: the production start path reads an ambient env var

`continuation_schedule.rs:42-52` declares `CODEX_GOAL_PACING_DISABLED` "test-only", but `GoalExtension::on_thread_start`
(`extension.rs:184-188`) reads it unconditionally, and `lib.rs:36,39` exports the constant and `pacing_disabled_by_env()`.
So a released app-server/CLI that inherits `CODEX_GOAL_PACING_DISABLED=1` silently turns pacing off. The panel's remedy is
either to remove the test plumbing or to make the opt-out an explicit production policy. Do the latter, the codex way: a
feature flag that the host maps into the extension config.

- `features/src/lib.rs`: add `Feature::GoalContinuationPacing`. Give it a doc comment saying it spaces consecutive automatic
  goal continuations on quiet threads. Spec: key `goal_continuation_pacing`, `Stage::Stable`, `default_enabled: true`. Place
  the variant and spec next to `Goals`, following the file's ordering.
- `core/config.schema.json`: add `"goal_continuation_pacing": { "type": "boolean" }` in BOTH features maps (next to `"goals"`
  at about lines 882 and 6918, alphabetical). You cannot run `just write-config-schema` on the mini, so edit by hand and match
  the generated shape exactly; the hosted core lane checks the fixture.
- `ext/goal/src/extension.rs`: add `pub continuation_pacing: bool` to `GoalExtensionConfig`, with a doc line.
  `on_thread_start` enables pacing only when `config.continuation_pacing` is set; replace the "always active in production;
  kill switch" comment with one that names the feature flag.
- `app-server/src/extensions.rs`: map
  `continuation_pacing: config.features.enabled(codex_features::Feature::GoalContinuationPacing)`.
- Every other `GoalExtensionConfig { .. }` construction must compile: the core suites `goal_background_wait.rs`,
  `goal_activity_tests.rs`, `goal_continuation_pacing.rs`, plus any others `git grep` finds.
  - Pacing suites set `true`.
  - The P4a `goal_background_wait.rs` fixture sets `false`. This is the non-blocking hardening the panels suggested for the
    check-in flake (B2-N1): it decouples that suite from pacing. The explicit `disable_pacing()` at line ~447 then becomes
    redundant; remove it. Keep `true` anywhere a test there genuinely needs pacing, and say which.
- Remove `PACING_DISABLED_ENV_VAR`, `pacing_disabled_by_env`, their `lib.rs` exports, and the unit test
  `pacing_disabled_by_default_with_env_kill_switch`, whose env assertion goes away. Do not add a negative test for the removed
  env var.
  - If `enable_pacing`/`disable_pacing` toggling still needs unit coverage, keep only the toggle part.
  - `disable_pacing()` stays pub only if a test still uses it; otherwise delete it (keep the crate API small).
- App-server tests: replace every `with_env_overrides(&[("CODEX_GOAL_PACING_DISABLED", Some("1"))])` with
  `.disable_feature(Feature::GoalContinuationPacing)` on the `MockResponsesConfig` (or `goal_continuation_pacing = false`
  under `[features]` where a suite writes its own config.toml). The four sites are `goal_background_wait.rs` (harness),
  `code_mode_host.rs:422`, `thread_goal_empty_responses.rs:71` and `thread_resume.rs:3485`.
  - Keep the harness parameter shape; the existing `/*pacing_disabled*/` comments stay valid.
  - Update its doc comment: "Production never sets this switch" becomes "users can opt out with `[features]
    goal_continuation_pacing = false`".
- After the change, `git grep -n CODEX_GOAL_PACING_DISABLED -- codex-rs` must be empty.

Production policy and its bounds (put this in the results; it is the "accurate bounds" the panel asked for):
- Pacing is on by default.
- `[features] goal_continuation_pacing = false` restores immediate back-to-back automatic continuations.
- The flag is read at thread start (`on_thread_start`). Say explicitly whether `on_thread_resume` and the config-update path
  (`extension.rs:~253`) re-read it; do not add a new mid-thread toggle in this rework.

## 2. Mutant for the new policy

Add `pacing_feature_flag_ignored`: in `on_thread_start`, call `enable_pacing()` unconditionally, ignoring
`config.continuation_pacing`. The expected killers are the app-server cases that now disable the feature and need
back-to-back continuations. `unopted_server_process_does_not_gate_goal_continuation` must have `goal` in its name so the
filter selects it. Report which tests kill the mutant. The existing six mutants must still apply to the final tree.

## 3. B2-N1 (note): no further action beyond the fixture decoupling in section 1.

## Keep

The filter `test(pacing) | test(continuation_schedule) | test(goal)` must still select every killer.

`mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item` then `--check` exit 0; no other cargo; no
CODEX_HOME copies; delete temp dirs. Watch for redundant closures, uninlined format args, `vec!` where an array works, and
`/*param*/` comments on positional literals. Update the results' switch inventory: the env var is gone and the feature flag
sites replace it. Leave everything UNCOMMITTED, report the final tree id after fmt, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 7`, and end your turn without handing off.
