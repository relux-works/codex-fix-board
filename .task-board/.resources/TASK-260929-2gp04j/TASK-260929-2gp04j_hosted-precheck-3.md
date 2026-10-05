# Hosted pre-handoff evidence: TASK-260929-2gp04j (G2), precheck 3 (for CR revision 2)

- snapshot commit `10bc26b11571a85b738ba8a84569fc33f56ffc1f` (signed, never landed), tree `d401bcff58f9724a36966053dde5386be1af7882` = the rev-2 rework worktree
- run https://github.com/relux-works/codex/actions/runs/37014493254: **success on all lanes** (lint, small, core, app-server)
- narrowing mutants: **15 of 15 killed by their intended tests**. These are the 13 from precheck 2 plus 2 new ones for
  the round-1 finding:
  - turn_stop_read_failure_keeps_marker, killed by goal_activity::turn_stop_accounting_read_failure_revokes_activity_and_next_turn_recovers (small lane);
  - abort_read_failure_keeps_marker, killed by goal_activity::turn_abort_accounting_read_failure_revokes_activity_and_next_turn_recovers (small lane).
- mutant runs (lanes beyond the needed one cancelled): 37014519273 37014547082 37014571388 37014599262 37014624368 37014648924 37014672993 37014697102 37014721886 37014747235 37014771251 37014798370 37014823430 37014849131 37014874521 
