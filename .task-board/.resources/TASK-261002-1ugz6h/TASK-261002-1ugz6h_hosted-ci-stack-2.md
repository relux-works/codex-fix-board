# relux-ci evidence: ci/relux-ci-selftest/stack-2

- commit: `7ae33a059056dad776bd0b81fb2b4883615b9b5a` = relux/main 35af013 + fc22281 (astra snapshot refresh) + relux-ci.yml (final: zsh-fork exclusions, sccache disk cache via actions/cache)
- tree: `f38084559bf0a082e724b5daf3edc5bed6981026`
- run: https://github.com/relux-works/codex/actions/runs/36963367409 (push event)
- conclusion: success (whole run 31m)

| job | conclusion | wall time |
| --- | --- | ---: |
| lint | success | 6m29s |
| core | success | 31m1s |
| small | success | 11m35s |
| app-server | success | 23m34s |

- core: 4854 run, 4854 passed, 11 skipped (8 default + 3 zsh-fork exclusions); both astra scenario snapshot tests pass.
- app-server: 1827 run, 1827 passed (1 flaky passed on retry: suite::v2::account::login_account_chatgpt_uses_oauth_overrides, also flaky in run 36959934198), 2 skipped.
- sccache: disk cache saved for all four lanes (keys sccache-relux-<lane>-<Cargo.lock sha256>-36963367409), 0 cache write errors (runs before this one: 1310/1310 write errors on the GitHub Actions cache backend). Hits start on the next run that can read these caches (same branch, or default-branch caches once runs dispatch on relux/main).
