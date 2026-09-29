# Revision 3 republish note

Revision 3 republishes the revision-2 consolidated plan unchanged. Its SHA-256 is `e25bfd07e8e2559570b67e37d98653c3537a1cac34039ffee938796bd6e0f4a0` (44,720 bytes).

Revision 2 went stale because the Story workspace record retained `current_base_oid` at `88e9a83` after publication moved the checkpoint to trunk `bfdb157`; the resulting producer delta incorrectly included 44 upstream trunk paths. The orchestrator converged the workspace base and checkpoint before this republish.

Checks:

- `task-board resource get TASK-260929-1srn2y TASK-260929-1srn2y_goal-token-burn-final-plan.md --output .temp/republish-rev3/final-plan.md` — exit 0; `shasum -a 256 .temp/republish-rev3/final-plan.md` — exit 0, digest matched the expected value.
- `git status --porcelain` before and after materializing the resource — exit 0 both times, empty output both times.
