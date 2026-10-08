# Local verification allowance (tb-arbiter gates, standing for this campaign)

One targeted local test run per producer pass is allowed, only if ALL gates pass right before: `df -g /` >= 50 GiB free;
CPU idle >= 25% (`top -l 2 -n 0 | grep 'CPU usage' | tail -1`); `memory_pressure | tail -1` free >= 30%. Abort (kill cargo)
if memory free falls under 30% during the build. Run only the narrowest nextest filter that covers your new tests
(for example `cd codex-rs && RUST_MIN_STACK=33554432 cargo nextest run -p <crate> --test <target> -E 'test(<filter>)'`).
Then trim with `rm -rf /Users/iv/Developer/IV/codex-target/debug`. Record disk before and after, CPU and memory in the results.
Nothing in parallel. R205: no load generators; at most 4 named busy workers, and only if a stress repro is truly needed.
Hosted precheck remains the authoritative evidence.
