# TASK-261002-ifa91r: p1-astra-snapshot-refresh

## Description
P1 follow-up found by hosted CI: the integral-decimal waiting-tool schema change (35af013, STORY-260929-2urftk) changed the clock and collaboration namespace fingerprints recorded by two astra scenario snapshots (all__suite__scenarios__astra_kickoff_remote_compaction_windows.snap, all__suite__scenarios__astra_plugin_refresh.snap). Both tests were in the local quarantine (the host global-skills root leaks into them), so the stale fingerprints slipped past the local gate; hosted runs 36959471910 and 36959934198 fail them 3/3 with exactly 6 hash lines per snapshot. Fix: signed commit fc22281 updates those 12 lines; it lands on relux/main before relux-ci.yml. Must be squashed into P1's upstream PR when the series is cut.

## Scope
codex-rs/core/tests/suite/snapshots: the two astra scenario snapshots only (12 hash lines)

## Acceptance Criteria
Hosted core lane runs both astra scenario tests green on the fixed tree; no other snapshot or code change.
