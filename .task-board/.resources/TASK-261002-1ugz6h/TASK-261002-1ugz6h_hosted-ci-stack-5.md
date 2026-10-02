# relux-ci evidence: ci/relux-ci-selftest/stack-5

- commit: `ea8899e6f97aea64136159286840c28c955243e8` = relux/main 35af013 + fc22281 (astra snapshot refresh) + relux-ci.yml rev 2 (per-SHA concurrency, exact-SHA verification, baseline warning gate)
- tree: `429a14a27a106f73b5907a0d830c4548cb3f1ea4`
- run: https://github.com/relux-works/codex/actions/runs/36974560859 (push event)
- conclusion: success (whole run 28m)

| job | conclusion | wall time |
| --- | --- | ---: |
| small | success | 10m2s |
| lint | success | 10m6s |
| core | success | 24m18s |
| app-server | success | 28m13s |

- lint: "clippy warnings: 3 distinct, 3 of them upstream baseline" (the gate parsed the warnings and tolerated exactly the 3 listed); "Verify the checked-out commit" passed in all lanes.
- core: 4854 run, 4854 passed, 11 skipped (8 default + 3 zsh-fork exclusions).
- app-server: 1827 run, 1827 passed (1 flaky passed on retry: suite::v2::mcp_tool::mcp_server_tool_call_declines_full_access_elicitation_for_automation_thread), 2 skipped.
- Negative control for the gate: run 36974565033 (resource TASK-261002-1ugz6h_hosted-ci-neg-1.md).
