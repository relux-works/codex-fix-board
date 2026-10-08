# TASK-261002-150osq: warning-gate-notes-p1-p2

## Description
Two non-blocking notes from the R141 round-2 panel A on relux-ci.yml: (P1) the warning gate parses only file:line:col-prefixed warnings, so prefix-less cargo warnings (manifest, build-script cargo:warning, summary lines) are neither counted nor gated; (P2) baseline matching is line-number-insensitive (sort -u over file: warning: message), so a new occurrence of an already baselined warning in the same file with the same message passes. Decide per note: harden (for example count per file+message against a baseline multiplicity, add a prefix-less warning check) or record as an accepted bound.

## Scope
(define task scope)

## Acceptance Criteria
(define acceptance criteria)
