# TASK-260929-csnn3a: f1-regressions-and-failure-paths

## Description
F1a/F1b and failure-path regression suite for sampling acknowledgment (final plan 5.4 race table; stage 2c, leaf 2 of STORY p5-sampling-acknowledgment). Intra-story order: runs after sibling TASK-260929-34a6ls (D1) is accepted and checkpointed. Add public-entry suite tests (core/tests/suite, real requests with latches or fake time, no sleeps): (1) exec_completion_survives_cleared_idle_reservation (F1a): inject_if_running accepts a bare ActiveTurn and a settings failure drops the reservation; the retained runtime mail is still eventually sampled exactly once. Narrowing mutant: retain only task-present input. (2) exec_completion_finishing_task_gets_sampling_wake (F1b): pending input recorded into history by a finishing task is NOT acknowledgment; the mailbox scheduler still produces a sampling request containing it. Narrowing mutant: acknowledge on recording. (3) exec_completion_sampling_ack: compaction or guardian omission leaves the receipt pending; a transport failure keeps it pending with bounded retries; the HTTP/WS fallback acknowledges only on the transport that submitted it; no history duplicates. Fix any production defect these tests expose, inside D's scope. Each gate gets a narrowing mutant that its named test kills. Out of scope: exit-before-arm, stdin, capacity, burst and owner/host races (story E/F).

## Scope
(define task scope)

## Acceptance Criteria
AC1 F1a test passes on the candidate and fails under the retain-only-task-present mutant. AC2 F1b test passes and fails under the acknowledge-on-recording mutant. AC3 Compaction omission and guardian omission each leave the receipt pending, and it is sampled by a later request. AC4 A transport failure keeps the receipt pending. Retries are bounded (asserted request count), followed by visible suspension. AC5 HTTP/WS fallback acknowledges only the transport that submitted it. AC6 No fragment is appended to history twice across retries.
