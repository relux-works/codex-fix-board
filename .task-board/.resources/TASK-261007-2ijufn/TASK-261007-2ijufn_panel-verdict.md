# Panel verdict — R141 panel B, CR-TASK-260929-3f6hfg-1 rev1 (TASK-261007-2ijufn)

Scope: read-only review of F2 (goal-background-wait vertical test). F2's own
delta is exactly 2 files vs the accepted F1 checkpoint `aa2768db7f`
(`git diff --cached aa2768db7f` on the replayed index): the new
`codex-rs/app-server/tests/suite/v2/goal_background_wait.rs` (638 lines,
4 tests) plus a 1-line `mod` registration. The other 31 CR-patch paths are
accepted F1 work, used as context only.

## Replay tree check

Replayed through a temporary index per the brief (base
`2f522b9dc9d639fe5195d93d61431a0caff662d5`):

- `GIT_INDEX_FILE="$IDX" git read-tree <base>` → exit 0
- `GIT_INDEX_FILE="$IDX" git apply --cached <patch>` → exit 0
- `GIT_INDEX_FILE="$IDX" git write-tree` → `c83869e576d1e024cfdbb5f63cfe8b83c6e969cb`

Tree matches the expected candidate exactly. No mismatch, review proceeded.
Candidate files were read from that tree (`git show` / `git archive`).

## Commands and exit codes

| Command | Exit |
|---|---|
| replay: `read-tree` + `apply --cached` + `write-tree` | 0 |
| `git archive`/extraction of candidate blobs for static attack | 0 |
| `git diff --cached aa2768db7f` (F2 delta = 2 files) | 0 |
| `git apply --check --cached` on each of the 5 mutant patches | 0 × 5 |
| `gh run view --json conclusion` (base 37633617318 + 3 mutant runs) | 0 × 4 |
| `gh run view --log-failed` (all 5 mutant runs) + grep analysis | 0 × 5 |
| cargo / just / any build or test | not run (brief forbids; shared target serialized) |

Base run 37633617318: `success`. All 5 mutant runs: `failure` (killed, 0 survivors).
Raw failed logs were pulled first-hand; every vertical-killer claim below was
confirmed in the log text (test name, file, line, 3/3 tries), not taken from
the precheck summary table.

## Verdict

accept

```verdict-findings
{
  "findings": [],
  "notes": [
    "silence-ignores-armed kills notified_exec at :357 via fragment displacement, not at the :338 pre-release count: the stray continuation lands after the check and displaces the wake request. This empirically confirms the test docstring's own race analysis (inflate pre-release count / displace wake / inflate final count); the gated base tree has no stray continuation, so no flakiness.",
    "drop-wake mutant inverts queue_wake rather than purely narrowing (retention/inline outcomes now also enqueue). The kill mechanism on the named tests is exactly the dropped Queued wake; mutant-description imprecision only, no effect on the kill.",
    "AC6 queue-API shape (thread/queue/*) is not driven; the burst shape is. The AC allows 'queued or burst' and the queue API is an experimental separate surface, so this is out-of-contract per the AC wording, not a gap.",
    "The Windows PowerShell barrier variant is written but unproven on hosted CI (no Windows app-server lane); disclosed in the results. AC7 targets the hosted Linux lane, where all 4 tests demonstrably execute.",
    "The local CR validation log is truncated at the 64 KiB board cap (known BUG-260917-38ob0v); its tail is green (exit 0, 267 small-crate tests, 4/4 coverage shards). The hosted lint and small lanes re-ran the same commands on the same tree (base run success)."
  ],
  "surface_results": [
    {
      "row": "controlled-exit vertical",
      "result": "held",
      "attacks": [
        "drop-wake executed on hosted run 37633707303: notified_exec + user_burst FAILED 3/3 via ~32s wake turn/started timeout (AC3 stalled runtime fails)",
        "wake-without-fragment executed on hosted run 37633768227: notified_exec FAILED 3/3 at :357 (fragment marker), user_burst FAILED 3/3 at :458 (receipt line)",
        "silence-ignores-armed executed on hosted run 37633736582: notified_exec FAILED 3/3 at :357 ('wake request should carry the completion fragment'); mechanism verified statically: evaluate_continuation consults snapshot.is_empty() (background_wait.rs) so Armed-blind snapshots force ProceedNormal",
        "wrong-receipt static attack: ack receipt is UUID-shape-validated (fail-closed on missing marker) and the wake must contain the identical receipt_id line plus exit_code: 0; markers verified in ExecCompletionFragment rendering (core/src/context/exec_completion.rs)",
        "extra-continuation race static attack: a continuation landing anywhere (before :338, between :338 and release, after release) fails the test via count 3, fragment displacement, or count 5; over-count requests fail closed (mount_sse_sequence responder panics + up_to_n_times + exact .expect); ResponseMock records every POST to */responses"
      ]
    },
    {
      "row": "negatives",
      "result": "held",
      "attacks": [
        "allow-notify-on-incapable-host executed on hosted run 37633645894: headless_host_refuses_notify_on_exit_and_promises_no_wake FAILED 3/3 at :612 (refusal-text assertion); mutant verified narrowing in candidate exec_command.rs (one-shot refusal kept, schema gating untouched)",
        "always-subscribe executed on hosted run 37633676266: unopted_server_process_does_not_gate_goal_continuation FAILED 3/3 at :540 (no-receipt-ack assertion); mutant verified narrowing (refusals and inline-settle paths unchanged)",
        "user input loss/duplication: burst test asserts exact per-turn request counts (3, 4), per-request input carriage, and thread/read texts exactly ['wait-user-one', 'wait-user-two']; user_burst is additionally killed by drop-wake and wake-without-fragment, proving the wake-follows assertion is live",
        "headless static attack: refusal precedes execution (no child spawned), exec_notification absent from schema, continuation ungated with no fragment, goal completes; driven through the production binary via --session-source exec (no test seam)"
      ]
    },
    {
      "row": "harness quality",
      "result": "held",
      "attacks": [
        "sleep hunt: grep over the candidate test file finds sleeps only inside the child barrier commands (the barrier mechanism itself, documented); all test waits are turn notifications, RPC round-trips, or 30s bounded timeouts",
        "skip hunt: the 3 barrier tests carry skip_if_remote!/skip_if_wine_exec! with stated reasons; the macros eprint the reason (core/tests/common/lib.rs); the headless test runs on every lane",
        "execution proof: all 4 tests demonstrably RUN on the hosted app-server lane (each FAILED under at least one mutant there); base run 37633617318 success means they ran green, not skipped",
        "mutant-quality hunt: all 5 patches touch production files only (pending_work.rs, async_watcher.rs, hook_runtime.rs, exec_command.rs x2), apply cleanly to the exact candidate tree (apply --check exit 0 x5), and narrow rather than delete (gate stays, admits exactly one reject-class member)"
      ]
    }
  ],
  "free_hunt": "Swept beyond the table: mod.rs delta is exactly +1 line; candidate tree equals accepted F1 checkpoint aa2768db7f plus the 2 F2 files; barrier determinism argument holds (fresh release path, spawn-before-yield-before-completion ordering, fail-closed 'Process running' assertions); post-completion count assertions cannot pass with a late wake (exact script counts + fail-closed responder); goal/get round-trips need no flush guarantee (late continuations fail via displacement/count, confirmed empirically). No blocking findings; 5 non-blocking notes recorded above."
}
```
