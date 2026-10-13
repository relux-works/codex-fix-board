# TASK-260929-2is91w orchestrator lint fix after precheck 6

Precheck 6 (run 38090998667) failed clippy redundant_closure at core/src/tools/waiting_capabilities.rs:178 and :253 (`.is_some_and(|exposure| exposure.is_deferred())`). Fix: `.is_some_and(ToolExposure::is_deferred)` plus `use codex_tools::ToolExposure;`. Nothing else. fmt --check exit 0, all 12 mutants still apply. New tree f11d3770f8997f0e41bccbc82c5c57a1dc0e08e7; precheck 7 runs on it.
