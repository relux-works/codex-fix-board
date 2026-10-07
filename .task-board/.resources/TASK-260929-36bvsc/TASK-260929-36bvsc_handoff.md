# TASK-260929-36bvsc handoff note — CR rev 2 (E1)

## Top finding

Hosted precheck 3 ran the exact worktree tree and is fully green with all
5 narrowing mutants killed. The rev-1 review defect (sampled B receipt never
retired → snapshot resurrected finished work as Queued) is fixed by joint
B+mailbox retirement in `acknowledge_submitted`, proven by the new
production-path regression test and its killed narrowing mutant. Ready for
review.

## Evidence pinned

- Worktree tree `cf567d98480d05428ed9dea58f66306dbf030ff6`, re-verified
  `TREE_MATCH` in this run; no file changed; candidate UNCOMMITTED on tip
  `812b8037a8` (12 candidate paths).
- Precheck 3 base run 37473988733 (snapshot 9ac368c5): core, app-server,
  lint, small all `success`.
- Mutant kills: 37474019570 (`production_ack_skips_store_retirement` →
  `production_acknowledgement_removes_pending_work`), 37474048117
  (`provider_missing_mapped_to_empty` →
  `read_failure_returns_explicit_error_not_empty_snapshot`,
  `goal_read_failure_is_explicit_error_not_empty`), 37474077806
  (`store_queued_excluded_from_snapshot` →
  `armed_to_queued_is_atomic_for_concurrent_readers`,
  `snapshot_reports_armed_queued_and_leased_only`), 37474108222
  (`suspend_skips_revision_bump` → `revision_increases_on_suspend`),
  37474137228 (`suspended_queued_admitted` →
  `snapshot_excludes_suspended_and_cancelled`). 5/5 killed, 0 survivors.
- Full AC map (5 of 5 driven), surface-table coverage map (3 of 3 rows,
  each with a killed mutant), and command log: refreshed
  `TASK-260929-36bvsc_results.md` (updated in this run).

## Checklist basis (items 13–17 checked this run; 1–12 already checked)

13. Implementation matches AC — 5/5 AC rows driven, precheck 3 green.
14. Solution fits project architecture — extension-api contracts, no
    core→goal edge, no `list_processes`.
15. Tests green — run 37473988733, all 4 lanes success.
16. Attacked, not read — 5/5 narrowing mutants killed by named tests.
17. Verdict routed — rev-1 findings answered with fix + regression test +
    mutant; this handoff publishes CR rev 2.

## Out of contract

The consuming goal waiting policy (TASK-260929-2snjbb, E2) — explicitly out
of scope per the task description. All 5 AC rows covered; no silent gaps.

## Logbook

- Rev 2 (prior run): review defect was real — mailbox acceptance never
  retired the B receipt. Fixed with joint retirement (`RuntimeLease` carries
  the B owner); old hand-ack fixture and its false comment removed.
- This run: tree re-verified identical to precheck-3 snapshot; handoff
  with zero code changes. No new findings, anomalies, or regressions.
