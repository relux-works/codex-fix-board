# TASK-260929-2is91w orchestrator lint fix after precheck 7

Precheck 7 (run 38091745251) failed the clippy baseline check with two new test warnings in core/src/tools/waiting_capabilities_tests.rs: useless_vec at :338 (`vec![...]` -> array, used only via `.iter()`) and infallible_destructuring_match at :469 (`match` -> `let DynamicToolNamespaceTool::Function(tool) = &namespace.tools[0];`). Nothing else. fmt --check exit 0, all 12 mutants still apply. New tree ef4eb6ff644eee2a950b493b675fb86f7b3301c2; precheck 8 runs on it.
