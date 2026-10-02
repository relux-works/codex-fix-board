# relux-ci evidence: ci/relux-ci-selftest/stack-1

- commit: `89d8b055bae06fc0ff0861b3ae5b9e5effae6ce0` = relux/main 35af013 + fc22281 (astra snapshot refresh) + relux-ci.yml (zsh-fork exclusions)
- tree: `10be7d67d9b49cd4e2cf65f77b400c85211510df`; fc22281 tree `5c365d9a68ea6d2cee0488eb58a37a539ce354d4` (identical except the added workflow file)
- run: https://github.com/relux-works/codex/actions/runs/36962123410 (push event)
- conclusion: success (whole run 27m)

| job | conclusion | wall time |
| --- | --- | ---: |
| app-server | success | 22m4s |
| lint | success | 8m46s |
| small | success | 9m10s |
| core | success | 27m36s |

- core: 4854 run, 4854 passed (1 flaky passed on retry: suite::hooks::permission_request_hook_allows_exec_command_without_user_approval), 11 skipped (8 default + 3 zsh-fork exclusions); both astra scenario snapshot tests pass.
- app-server: 1827 run, 1827 passed, 2 skipped.
