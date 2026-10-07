# TASK-260929-36bvsc hosted precheck 3 (CR rev 2)

Worktree tree: cf567d98480d05428ed9dea58f66306dbf030ff6. Snapshot commit 9ac368c5, run 37473988733: lanes {'core': 'success', 'app-server': 'success', 'lint': 'success', 'small': 'success'}. All green.

Mutants: 5 total, 5 killed, 0 survivors.

| mutant | run | lanes failing | killing tests |
|---|---|---|---|
| production_ack_skips_store_retirement | 37474019570 | core,lint | production_acknowledgement_removes_pending_work |
| provider_missing_mapped_to_empty | 37474048117 | small,core | goal_read_failure_is_explicit_error_not_empty, read_failure_returns_explicit_error_not_empty_snapshot |
| store_queued_excluded_from_snapshot | 37474077806 | core | armed_to_queued_is_atomic_for_concurrent_readers, snapshot_reports_armed_queued_and_leased_only |
| suspend_skips_revision_bump | 37474108222 | core | revision_increases_on_suspend |
| suspended_queued_admitted | 37474137228 | core | snapshot_excludes_suspended_and_cancelled |
