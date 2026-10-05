# TASK-260929-2gp04j (G2): close the one precheck-7 survivor, then request precheck 8

Hosted precheck 7 ran your rev-4 worktree tree as snapshot 101fb595 (run 37256859867), and every lane is green.
24 of the 25 mutants are killed by their intended tests. One mutant SURVIVED, with all four lanes green (run 37257091901):

- `set_replace_bypasses_guard`: in codex-rs/ext/goal/src/api.rs (~line 233), the `replace_thread_goal` branch passes
  `None` instead of `runtime.as_ref()` to `Self::guard_live_store_result`. No test covers a store failure on the
  set/replace path, so a set that replaces an existing goal can bypass the structural guard.

Do this:
1. Add a focused test that fails exactly when the replace-path store call errors but the active marker and activity
   are not revoked. Follow the pattern of `external_set_prepare_failure_revokes_activity_and_next_turn_recovers`,
   and include the recovery on the next turn. Do not change production code unless the test shows a real bug.
2. Add a row for this mutant to TASK-260929-2gp04j_mutants.json (keep all 25 existing rows), and re-attach it.
3. Leave the candidate UNCOMMITTED and add the note "HOSTED-PRECHECK-REQUESTED: precheck 8". Do NOT hand off. Rules:
   R176 (evidence is text only), R174 (never use the lite context profile), and the disk rules (no local workspace
   builds; the orchestrator runs CI on GitHub).
