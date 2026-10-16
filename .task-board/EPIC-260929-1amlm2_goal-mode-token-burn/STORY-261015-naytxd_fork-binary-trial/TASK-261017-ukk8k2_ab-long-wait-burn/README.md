# TASK-261017-ukk8k2: ab-long-wait-burn

## Description
Reproduce the goal-mode token burn on upstream before more patch work. Two scenarios, codex-relux f52f28f vs codex-base 0462dcc, gpt-6-astra medium, TUI, run in parallel: (A) goal waits for a 40-minute shell job; (B) goal must spawn one sub-agent that runs a 20-minute job and wait for its report. Measure requests, tokens (cached/uncached), wall time across parent and child rollouts. Decision input: if base does not burn materially more than relux, most patches have no value and BUG-261016-ujfuxq should not be pursued.

## Scope
(define task scope)

## Acceptance Criteria
(define acceptance criteria)
