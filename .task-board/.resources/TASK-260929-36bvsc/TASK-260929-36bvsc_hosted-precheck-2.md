# TASK-260929-36bvsc hosted precheck 2

Worktree tree: 0edaf3a0edd354ef941f7e5d0f92bd0e44ed8f1d. Snapshot commit 84aa9a3f, run 37463583436: lanes {'app-server': 'success', 'lint': 'success', 'core': 'success', 'small': 'success'}. All green. Precheck 1 had a red base, so its mutant results are void.

Mutants: 4 total, 4 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| provider_missing_mapped_to_empty | 37463609295 | core,small | read_failure_returns_explicit_error_not_empty_snapshot, goal_read_failure_is_explicit_error_not_empty |
| store_queued_excluded_from_snapshot | 37463635217 | core | armed_to_queued_is_atomic_for_concurrent_readers, snapshot_reports_armed_queued_and_leased_only |
| suspend_skips_revision_bump | 37463660857 | core | revision_increases_on_suspend |
| suspended_queued_admitted | 37463702577 | core | snapshot_excludes_suspended_acknowledged_and_cancelled |
