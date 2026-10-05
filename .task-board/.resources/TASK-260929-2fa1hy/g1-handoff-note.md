# TASK-260929-2fa1hy — resume and hand off: the hosted pre-handoff evidence resolves your Stop-The-Line

Ownership decision (orchestrator, 2026-10-02): under the fast local lane, current-candidate codex-core execution and
narrowing-mutant replay come from orchestrator-run hosted pre-handoff checks on the EXACT worktree tree, not from local
core suites. For this candidate, that evidence is `TASK-260929-2fa1hy_hosted-precheck-1.md` (precondition):
- snapshot commit dc09022 has tree 403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd, equal to your current worktree tree. Hosted
  run 36983853906 is green on all lanes, and all 6 G1 request tests PASS;
- mutants hard_disable_bypass, reminder_false_bypass and no_marker_admitted are each killed by their named tests
  (runs 36983895784, 36983937144, 36983916432).

Do this:
1. Confirm the worktree tree still equals 403dbe80e514c6ae09fe8f41721e50a6b8a9dcdd: temp index, `git read-tree HEAD`,
   `git add -A`, `git write-tree`. Do NOT change any file. A code change would invalidate the evidence; if you believe
   one is needed, stop and say why, without handing off.
2. Check checklist items 3, 6, 8, 9 and 10, citing the hosted runs and test names above. Update
   `TASK-260929-2fa1hy_results.md` and the coverage map so each AC row and mutant points to its hosted evidence.
3. Run the busy check. When it prints FREE, hand off: `task-board handoff TASK-260929-2fa1hy --role developer`. Only a
   printed `BUSY ...` line means HOLD.
