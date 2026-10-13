# TASK-260929-2is91w (P3-1): precheck 12 mutant survived. Drive the same-slug merge branch, then request precheck 13

Precheck 12 (run 38177362699, snapshot 53cb9e42, tree b9982d79; ref relux/ci-next): all four lanes green, 14/15 mutants killed.
`snapshot_ignores_remote_catalog_replacement` SURVIVED: in mutant-14 core (job 114584674038)
`suite::search_tool::remote_catalog_replacement_changes_waiting_snapshot` ran and PASSED with the mutant applied.

## Cause (orchestrator diagnosis from the source; confirm it)

`ModelsManager::apply_remote_models` (`models-manager/src/manager.rs:672-702`) only merges same-slug entries into the bundled
fallback when `remote_only` is false. `remote_only` is true when any remote model has `ModelVisibility::List` AND (API-key
discovery OR a ChatGPT account). Your helper `remote_catalog_replacement_case` uses
`CodexAuth::create_dummy_chatgpt_auth_for_testing()` and a remote entry copied from the bundled one (List visibility), so the
remote catalog REPLACES the whole list and the mutated line `models[index] = model;` never runs. The test proves the snapshot
follows the remote entry on the remote-only path; it does not touch the same-slug merge path the mutant narrows.

## Required

1. Keep the existing remote-only cases (they are valid coverage of the ChatGPT path).
2. Add the merge-path case(s) so the same-slug replacement actually executes: make `remote_only` false through a real
   configuration (e.g. a remote entry whose visibility is not `List`, or an auth/provider setup without ChatGPT account and
   without API-key discovery) while the session still resolves that slug. Assert the snapshot flag follows the REMOTE entry
   (both directions if the fixture allows) and the request counts, as now. Add one assertion that proves the merge branch ran
   (e.g. a bundled-only slug is still listed alongside the replaced one) so the test cannot silently fall back to the
   remote-only path again.
3. Keep mutant `snapshot_ignores_remote_catalog_replacement` as is; its killer is the new merge-path case. Results: name which
   case kills it and why the remote-only cases cannot.

## Keep

Every other file, test and mutant unchanged; all 15 mutants must apply to the final tree. Filter for precheck 13 = precheck 12's.

`mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item` then `--check` exit 0; no other cargo; no
CODEX_HOME copies; delete temp dirs. Leave everything UNCOMMITTED, report the final tree id after fmt, add the note
`HOSTED-PRECHECK-REQUESTED: precheck 13`, and end your turn without handing off.
