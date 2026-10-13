# TASK-260929-csyzcj (G1): hosted precheck 3 is RED (lint fmt plus one latch assertion). Fix both, then request precheck 4

Precheck 3: snapshot wip-3 4201cc4b (tree 88a9037a = your worktree), relux-ci run 37841534974. Progress: the latch test no
longer hangs. It now fails in ~4 s on a clear assertion, so the bounded waits work. small and app-server are GREEN.
core: 5081 of 5082 passed. A red snapshot voids every mutant result, so all 6 mutants have to run again.
The Mac mini addendum (`g1-rework-mini-addendum.md`) still applies: no local cargo or just. Your candidate is already in the
worktree, so do NOT re-apply wip-2.

1. lint (job 113531850152), `just fmt-check` fails in `core/tests/suite/goal_native_wait.rs` near line 535. rustfmt wants:
   ```rust
       assert!(
           inspections
               .iter()
               .any(OwnedChildInspection::is_pending_native_work),
           "slow child should still be pending native work, got {inspections:?}"
       );
   ```
   Clippy never ran, because fmt failed first. So re-read every line you changed for clippy issues too: redundant closures,
   uninlined format args, collapsible ifs, needless borrows. Format all your new code to rustfmt's 100-column style by hand.
2. core (job 113531850326), `suite::goal_native_wait::goal_wait_latch_closes_completion_before_registration` FAILS on all 3
   tries at `goal_native_wait.rs:510:5`: `assert_eq!(child_fast_final.requests().len(), 1)` got **2**. The parent's wake turn
   DID start and `parent_wake` matched, so the post-insert recheck works. But the fast child's final-response mock was hit
   twice. Find out why from the code path; do not just relax the assertion. Candidates:
   (a) the fast child really samples twice, a double-run or a retry: then that is a production bug you must fix;
   (b) the mock's matcher also matches a later request, for example the parent's wake turn or a second child turn: then
   tighten the matcher so each mock matches exactly one request;
   (c) the child's own mail or goal continuation starts a second child turn: then decide from the AC whether that is
   correct, and assert on that instead.
   State which one it was in `TASK-260929-csyzcj_results.md`, with the evidence (code citations).
3. Re-check `insert_after_mail_check`: once the test is green on the candidate, this mutant must fail it with an assertion.
   Make sure every mutant patch still applies to your FINAL tree with correct hunks (`git apply --check`), then re-attach
   `TASK-260929-csyzcj_mutants.json` and the results file.
Leave everything UNCOMMITTED, add the note `HOSTED-PRECHECK-REQUESTED: precheck 4`, and end your turn without handing off.
Text-only evidence (R176).
