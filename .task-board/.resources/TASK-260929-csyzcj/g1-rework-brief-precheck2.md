# TASK-260929-csyzcj (G1): one hanging latch test and one surviving mutant on hosted precheck 2. Fix, then request precheck 3

Hosted precheck 2 (snapshot run 37664186944; see g1-p2.ok). Progress: the marker now registers in production, and
`goal_wait_registers_marker_and_wakes_on_child_completion` passes. core: 5081 of 5082 passed. small and lint are GREEN.
app-server was cancelled by the runner during "Linux build dependencies" (infrastructure; it will be re-run). Remaining (R169):

1. `suite::goal_native_wait::goal_wait_latch_closes_completion_before_registration` TIMES OUT on all 3 tries (TMT at 60 s,
   with SLOW at 30 s first). The test hangs: most likely the latch or barrier waits for the idle path to reach the
   registration gate, and production never pauses there (or the release side is never signalled), so the test blocks
   forever. Make the gate reachable and observable deterministically through the real idle path. Give every latch wait a
   bounded timeout with a clear panic message (for example 5-10 s) instead of hanging the harness. Then prove that the
   completion-before-registration race is closed: a child finishing between the idle inspection and the marker insert
   still wakes the parent.
2. Mutant `insert_after_mail_check` SURVIVED: all lanes on its run are green, because its intended killer is the hanging
   test above. Once item 1 passes on the candidate, this mutant must make that test fail with a clear assertion, not a
   timeout.
LOCAL VERIFICATION (local-build-allowance.md, all gates; check df right before, because disk is tight):
`cd codex-rs && RUST_MIN_STACK=33554432 cargo nextest run -p codex-core --test all -E 'test(goal_native_wait)'`, trim afterwards,
record readings. Update and re-attach the results and mutants files. Leave the candidate UNCOMMITTED and add the note
"HOSTED-PRECHECK-REQUESTED: precheck 3". Do NOT hand off. Follow R176 and R174.
