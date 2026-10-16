# TASK-261017-ukk8k2 — long-wait goal A/B, codex-relux f52f28f vs codex-base 0462dcc

Run 2026-10-16T20:08:41Z, gpt-6-astra medium, identical config, TUI `--no-daemon --no-alt-screen -a never -s workspace-write`,
four sessions in parallel (tmux ab-relux, ab-base, ab-relux-sub, ab-base-sub). All four reached "Goal achieved" with the
correct result line. Metrics: `ab-aggregate.py` (parent + sub-agent rollouts grouped by cwd), raw `ab-long-run1.json`.
Cost-weighted input = uncached + 0.1 x cached (assumed discount, not a measured price).

## A. Goal waits for a 40-step shell job (`long-job.sh`, 40 x 60 s)

| Metric | base | relux | Delta |
|---|---:|---:|---:|
| Requests | 88 | 49 | -44% |
| Total tokens | 1,970,620 | 1,051,989 | -47% |
| Uncached input | 64,322 | 55,739 | -13% |
| Cost-weighted input | 254.5k | 155.0k | -39% |
| Output tokens | 4,602 | 3,354 | -27% |
| Tools | exec 44, wait 43 | exec 43, clock.sleep 3, wait 2 | |

## B. Goal spawns one sub-agent that runs a 20-step job (`sub-job.sh`, 20 x 60 s)

| Metric | base | relux | Delta |
|---|---:|---:|---:|
| Requests (parent + child) | 88 | 57 | -35% |
| Total tokens | 1,749,427 | 1,147,072 | -34% |
| Uncached input | 51,367 | 51,971 | +1% |
| Cost-weighted input | 220.8k | 161.2k | -27% |
| Parent wait_agent / send_message | 27 / 18 | 7 / 2 | |

## Findings

1. On waits of 20-40 job steps the patches cut requests by 35-44% and cost-weighted input by 27-39%. The 5-minute A/B
   (TASK-261015-xgmuju) was too short to show this: fixed per-goal overhead dominated there.
2. Base does not explode into thousands of requests; it burns steadily at about 2.2 requests per job minute (long) and
   polls the child with wait_agent/send_message. relux runs at about 1.2 requests per job minute.
3. Both arms still poll. P5 notify_on_exit stayed inert (goal guidance "cannot promise an exec completion wake", code mode),
   so the remaining ~49 requests in scenario A are what BUG-261016-ujfuxq would remove (expected 3-4).

## Limits

The host went into maintenance sleep during the runs (pmset log, 2026-10-17 01:23-01:41 +0400 and more); both arms froze
together, so wall time (~103 min for A, ~46 min for B) is not meaningful and not compared. n = 1 per arm per scenario.
