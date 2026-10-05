# TASK-260929-2gp04j (G2): rebase the Story onto the new trunk, then request precheck 6

The rev-3 handoff failed with `change_request_base_authority_mismatch`: trunk moved to 729f259e62a8d11d9e17398e487790e1ee5d8b8c (P5-B landed), and the Story checkpoint 58042581 (G1) is not contained in it.
1. First, inside this run, execute `task-board worktree refresh-candidate TASK-260929-2gp04j`. It replays the G1 checkpoint onto the new trunk and keeps your working candidate exactly. If it reports conflicts, follow its resolution-template instructions exactly; never hand-commit.
2. Confirm the worktree still holds the G2 changes. Run the fast lane: busy check, guard, `just fmt`, clippy for the touched crates, `just test -p codex-goal-extension -p codex-extension-api`.
3. The tree changed, so hosted precheck 5 no longer matches it. Add the note `HOSTED-PRECHECK-REQUESTED: precheck 6 (rebased on 729f259)` and end your turn without handing off.
