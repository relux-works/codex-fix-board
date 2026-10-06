# Recording confirmation — TASK-260929-csnn3a f1-regressions-and-failure-paths, CR revision 1

Read the merged verdict and both complete panel outcomes. Merge check passed: 1/1 findings retained with every reproduction; 11/11 panel notes retained; 3/3 surface rows retained in required order with the worst panel result. Panel A requests changes, panel B recommends acceptance; the merged changes_requested branch is correct under recording-brief-rev1.md.

Results: F1a cleared reservation broken (R141-A-1); F1b finishing task held; compaction, guardian and transport held within the panels' stated bounds. R141-A-1 remains a static concurrency finding with a proposed, unexecuted reproduction; this recording run does not claim an observed failure. No new findings, code modifications, builds or tests. Hosted evidence is reused only as described by the panels.

Required rework: guarantee scheduling after returned leases when the winning turn has already gone idle, without duplicate wake or spin; add exec_completion_lost_reservation_after_winner_idle_rewakes and its narrowing mutant. The merged verdict is the recording evidence; repeat-of null is normalized to the explicit value none, with no change to mechanism or verdict.

Commands: three resource downloads exited 0; python3 .temp/reviewer-csnn3a/check_merge.py exited 0. Initial unsupported resource projections failed and were replaced with named resource downloads; no absence inferred. Spawn goal reports this run is not goal-bound; directives reports none.

Logbook: 2026-10-06 — recording merge verified; route CR revision 1 to rework once using reject_cr. The supplied revision-2 rework brief does not change the revision handed to this recording run. This task-scoped outcome carries the logbook entry; no control-root files were edited.
