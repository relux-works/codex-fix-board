# TASK-260929-csyzcj: orchestrator test fix before precheck 12

Precheck 11 (run 38072245794): green except one core test, `interrupted_fragment_truncates_overlong_paths_to_hard_cap`, which panicked at
`AgentPath::try_from(...).expect("valid agent path")`: "absolute agent path must be at most 1024 bytes, got 2006". The new source bound
(MAX_SEGMENT_BYTES 128, MAX_PATH_BYTES 1024) makes the old 2006-byte fixture invalid. The fragment cap (256 bytes per path) stays reachable, so
the test now builds source-valid paths from nine 100-byte segments (914 bytes). The expected output uses the same formula. Test-only; cargo fmt clean.
