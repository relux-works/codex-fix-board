# TASK-261015-xgmuju — A/B goal-mode token burn, codex-relux vs codex-base

Date: 2026-10-16. Builds: codex-relux f52f28f (relux-build 38825757714), codex-base upstream 0462dcc (build 38773745523).
Model gpt-6-astra, reasoning medium, identical config.toml, TUI `--no-daemon --no-alt-screen -a never -s workspace-write`,
both runs launched in parallel in tmux (ab-relux, ab-base), fresh git dirs with the same `slow-job.sh`
(10 x 30 s steps, then writes result.txt). Goal text:
`/goal Run ./slow-job.sh in this directory. It takes about 5 minutes. Wait until it has finished, then tell me the line written to result.txt. Do not modify the script.`
All four runs reached "Goal achieved" with the correct line `RESULT: 42 widgets processed`.

Metrics from `ab-metrics.py` over `$CODEX_HOME/sessions/**/rollout-*.jsonl` (requests = token_count events with a changed total).

| Metric | base r1 / r2 | relux r1 / r2 | Mean delta |
|---|---:|---:|---:|
| Requests | 24 / 16 | 14 / 14 | 20 -> 14 (-30%) |
| Total tokens | 451,798 / 296,980 | 264,527 / 264,423 | 374.4k -> 264.5k (-29%) |
| Cached input | 427,136 / 280,960 | 222,848 / 242,048 | 354.0k -> 232.4k (-34%) |
| Uncached input | 23,674 / 15,315 | 41,134 / 21,848 | 19.5k -> 31.5k (+62%) |
| Output tokens | 988 / 705 | 545 / 527 | 847 -> 536 (-37%) |
| Cost-weighted input (uncached + 0.1 x cached, assumed discount) | 66.4k / 43.4k | 63.4k / 46.1k | 54.9k -> 54.7k (~0%) |
| Wall time | 314 s / 312 s | 330 s / 346 s | 313 s -> 338 s (+25 s) |
| Waiting tools | wait x12 / wait x5 | clock.sleep x5 / x5 | |

Rollouts: relux r1 rollout-2026-10-16T05-41-33-01a1425f-22a9..., r2 rollout-2026-10-16T05-48-03-01a14265-1462...;
base r1 rollout-2026-10-16T05-41-45-01a1425f-4f73..., r2 rollout-2026-10-16T05-48-03-01a14265-1453.... Raw: ab-run1.json, ab-run2.json.

## Findings

1. relux is stable at 14 requests (5 x 60 s clock.sleep + write_stdin poll); base varies 16-24 with 10 s `wait` polls.
   Request count and raw tokens drop about 30%.
2. Money effect is about zero on this scenario: relux pays more uncached input. r1 had one full cache miss
   (request 2, after a 60 s sleep, cached=0, ~18k tokens); r2 still has +6.5k uncached versus base. Under an assumed
   90% cached discount the cost-weighted input is equal.
3. Wall time is worse by ~25 s: a 60 s sleep that starts shortly before the job ends overshoots it.
4. **P5 (notify_on_exit) is inert in this setup.** The relux TUI session (source cli, so AsyncNotificationSupport is
   Available) still received `<goal_waiting_guidance>This session cannot promise an exec completion wake...`.
   Cause in code: the model reaches exec_command/write_stdin only through the code-mode `exec` tool, and
   `core/src/tools/waiting_capabilities.rs` (`is_directly_visible`, ~line 219) deliberately excludes nested code-mode
   tools, so `stdin` and `exec_notify` are false and guidance falls back to clock.sleep (P4a). The observed savings come
   from P4a sleep guidance, not P5. A run with notify_on_exit active would need about 3-4 requests.

## Limits

n = 2 per arm, one scenario, run in parallel on one account. The cached-input discount is an assumption, not a measured price.
