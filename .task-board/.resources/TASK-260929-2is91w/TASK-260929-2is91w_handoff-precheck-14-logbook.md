# TASK-260929-2is91w — waiting-capabilities-snapshot handoff logbook (precheck 14)

Run RUN-261012-48671c. Evidence-only handoff; candidate preserved as tree afb8c830d764ba489a9f2f922c0babdf1dbe036e.

Decision: use hosted precheck 14 (38191980780) for compile/lint/test evidence; do not rerun Rust suites on the Mac mini. Four lanes green; 15/15 mutants killed. Record initial guardian timeout and same-snapshot core rerun rather than concealing the failure.

Finding resolved: AC5 remote catalog attacks now reach both remote-only and merge branches. Hide merge cases in remote_catalog_replacement_changes_waiting_snapshot kill the survivor from precheck 12; four cases assert 4 /models and 4 /responses requests total. Recording reviewer owns acceptance of this new revision.

Preserve orchestrator test fix 10 and lint fix 14. The candidate exceeds size guidance at 2,625 changed lines in 21 files; this is disclosed in results, with no new code edits during handoff.

Local verification: hosted gate exit 0; fmt-check via guarded absolute cargo path exit 0 (initial PATH lookup exit 127); git diff --check exit 0; every one of 15 mutant git apply --check processes exit 0. Rust build/test/clippy not run locally. CLI exploratory reads failed for unknown element operation and absent reference path; corrected using get and resource get, not interpreted as missing evidence.

All eleven checklist items already checked when queried; latest supporting evidence recorded in refreshed results. Updated TASK-260929-2is91w_results.md and attached this new outcome before handoff. No temporary directories created; gate index removed by trap; no repository edits or commits.
