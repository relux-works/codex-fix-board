# R141 panel A — CR-TASK-260929-4ut0up-1 revision 1

changes_requested

Replay: base `ea8899e6f97aea64136159286840c28c955243e8` plus the attached revision-1 patch gives exactly candidate tree `7de6b3c2ed82f07002c613263cd650cc16b20108`. Read-tree, cached apply and write-tree each exited **0**. The locally resolved precheck-2 snapshot tree also equals that candidate.

This is a non-recording panel. Nothing was written on TASK-260929-4ut0up; no accept/reject/status/handoff action was attempted there. No repository code, branches or commits changed. No build, Cargo, just, product test or mutant was run. The blocking verdict concerns the explicitly truncated CR validation evidence. Code-race observations remain notes under the no-runtime scope; no claimed failing Rust reproduction.

## Bounded plan

Decision: whether rev1 has admissible evidence for the recording reviewer. Frozen input: CR rev1 patch/base/candidate tuple above. Budget: 25 minutes including packaging; one text outcome, no archives; zero serial prerequisites. Exit: replay identity, one result for every surface row, bounded free hunt and attached verdict. Consumer: the orchestrator/recording reviewer for B2's already-written receipt hooks. No new implementation/research leaf requested.

## Static sweep (one table row, ten named attack families)

| Family | Static observation and candidate sources |
| --- | --- |
| Exit before/after initial yield | reserve-before-spawn and initial Arm/Inline branches present; completion_receipt.rs:329-431 serializes the state transitions. AC2 tests use delays rather than forcing decision boundaries (note). |
| Held drain/denial | async_watcher.rs:182-191 waits for exit, drain, denial join and interaction lock. Test at receipt_hooks_tests.rs:550 drives watcher directly, not exec_command's wiring. |
| 3 MiB output | HeadTailBuffer plus receipt_output.rs:176-188 enforce 1 MiB head/tail and add omitted bytes; watcher copies transcript plus omission count. No arithmetic defect found statically. |
| 64/65 capacity and LRU | receipt_hooks.rs:147-166 counts active+sampled; receipt_output.rs:128-145 retires minimum sample sequence. Publication/retention split can escape this accounting (note). |
| Stdin vs pushed claim | Store leases serialize Queued claims; live-Armed stdin ordering is absent from tests and potentially bypasses delivery consumption (note). |
| Release/terminate/interrupt/shutdown | Hooks cancel before corresponding termination/signal calls; explicit release leaves process alive. Late retention insertion races cancellation (note). TTY input writes are distinct from the non-TTY explicit interrupt branch; no broader cancellation claim proved. |
| Foreign/unknown reads | read_retained_output checks retention owners, then store status; release checks binding/retention owner before dropping. No static ownership bypass identified. |
| Default launches beyond 64 | exec_command passes Default; reservation branch executes only NotifyOnExit; oneshot uses Default. Existing default responses and event branches kept. |
| Removal before receipt read | Retention is independent of process_store; release_process_id unbinds process without dropping receipt output. |
| Slot freeing inline/release/stop | Inline settle drops retention/binding; release and shutdown clear output. Watcher insertion is outside the same lock (note). |

Static families inspected: **10/10**. Panel public-entry runtime attacks executed: **0/10**. Surface results: **1/1** rows represented, with no unsupported held claim. The no-build rule is a measurement bound, not an absence-of-defects claim.

## Commands and exit codes

These are this panel's commands, not producer execution:

| Command | Exit / evidence |
| --- | --- |
| `task-board m 'set_status(TASK-261005-2hw1ki, status=analysis)'` | 0 |
| Initial readiness/discovery shell (`mkdir`, `command -v task-board`, `git --version`, `rg --version`, `git status`, scoped `rg --files`) | 2 overall because optional skills directories were absent; git/task-board readiness succeeded. Not a passing gate. |
| Query with unsupported `resources` field | 1, query parse error; replaced with the scoped description/scope/ac query (0). |
| `task-board resource list TASK-260929-4ut0up` | 0 but printed help, not an inventory; inventory subsequently read from the resource directory (0). |
| `task-board q 'schema(resource)'` | 1, unsupported positional schema argument; not used as evidence of absence. |
| `task-board resource get TASK-260929-4ut0up TASK-260929-4ut0up_change-request_rev1.patch --output .temp/TASK-260929-4ut0up_change-request_rev1.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2hw1ki-replay.idx" git read-tree ea8899e6f97aea64136159286840c28c955243e8` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2hw1ki-replay.idx" git apply --cached .temp/TASK-260929-4ut0up_change-request_rev1.patch` | 0 |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-2hw1ki-replay.idx" git write-tree` | 0; exact expected tree |
| `git rev-parse '9e692fdcd16a373a59f7d262159b377d588163d0^{tree}'` | 0; exact candidate tree |
| `git diff --quiet 3431fef 7de6b3c2ed82f07002c613263cd650cc16b20108 -- codex-rs/core/src/unified_exec/completion_receipt_tests.rs` | 0; B1 tests unchanged |
| Python materialization via `git ls-tree` and pinned `git show`; B1 blob-comparison script | 0 each; 26 candidate unified_exec blobs; B1 path comparison reported two changed and one unchanged |
| Read-only `cat`, `sed`, `nl`, `rg`, and `git diff` source/resource inspections | 0 (except initial optional-directory discovery noted above); terminal display of large reads truncated, followed by narrow reads and full-file Python evidence parsing |
| `task-board spawn directives "$TASK_BOARD_RUN_ID"` | 0; no directives |
| `task-board q 'get(TASK-261005-2hw1ki) { checklist }'` | 0 |
| Full-file Python CR-validation-log inspection | 0; 65,536-byte artifact; 1,081 lines; explicit omission at 812; footer claims four green shards |
| `task-board resource get TASK-260929-4ut0up TASK-260929-4ut0up_change-request_rev1-validation.log --output .temp/TASK-261005-2hw1ki/cr-validation.log` | 0 |
| Evidence-integrity Python command in the reproduction below | **1**, expected-red: explicit truncation marker. Failing evidence check; not passing and not a Rust test. |

The reused CR log explicitly records target guard 0 and fmt-check 0. Its intervening omissions prevent verification of the complete clippy/small-suite command/status transcript. Precheck 2 reports four hosted lanes green and 16/16 mutants killed on the matching snapshot; these were **not rerun by this panel**.

## Task-scoped logbook

2026-10-05: exact replay and snapshot identity established. B1 tests unchanged; B1 source has documented B2 API additions, so literal path preservation is partial. Validation artifact explicitly truncated; incomplete execution evidence remains unknown. Two unexecuted race schedules and missing forced-yield barriers are handed to recording review as notes. Recommendation: obtain an untruncated plain-text validation transcript for this exact candidate; validate the two schedules in the serialized hosted lane before treating them as reproduced defects. No extra research/harness stage requested. No control-root logbook file edited.

Artifact structure check: exit 0 (exactly one valid verdict-findings JSON block, 1/1 surface rows, required finding fields and verdict). `git diff --exit-code`: exit 0; no tracked repository delta. Outcome attachment/checklist/lifecycle commands follow this check and are recorded by the board.

## Structured verdict

```verdict-findings
{
  "findings": [
    {
      "id": "truncated-cr-validation-evidence",
      "row": "free_hunt: validation attestation",
      "invariant": "Reused validation logs must preserve every command and exit status; a truncated log is unverified, not passing.",
      "mechanism": "TASK-260929-4ut0up_change-request_rev1-validation.log:812 explicitly omits 42,796 bytes. Only three command headers and three exit markers survive, while the final coverage line claims required=4 green=4. The clippy termination and small-suite invocation are not available as a complete command/status pair.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261005-2hw1ki/cr-validation.log (downloaded evidence fixture; not a Rust test)",
          "command": "python3 - <<'PY'\nfrom pathlib import Path\np=Path('.temp/TASK-261005-2hw1ki/cr-validation.log')\ns=p.read_text()\nfor n,line in enumerate(s.splitlines(),1):\n    if 'validation log truncated' in line:\n        print(f'{p}:{n}: {line}',flush=True)\n        raise SystemExit(1)\nprint('No explicit truncation marker')\nPY",
          "expected_failure": "Exit 1; prints line 812: ... validation log truncated; 42796 bytes omitted ... . Observed exit 1. Expected-red evidence-integrity check, not a product test."
        }
      ],
      "severity": "bypass",
      "repeat-of": "none"
    }
  ],
  "notes": [
    {
      "id": "publication-retention-split",
      "text": "Static race candidate, NOT runtime reproduced: async_watcher.rs:209-226 publishes to the store before awaiting the output-buffer lock and hooks lock. acknowledge_pushed_completion (receipt_hooks.rs:313-319) can acknowledge and move_to_sampled while there is no pending output; later watcher insertion creates a pending output for an already-Sampled receipt. Capacity counts active_len + sampled_count, so this pending entry is not counted or LRU-retired. Likewise release/cancel/inline settle can drop retention before the late insertion resurrects it. Proposed regression: hold the output-buffer lock, let watcher publish Queued, acknowledge or release through manager entry points, then release the buffer lock; require exact capacity/read disposition. No such test was added or run."
    },
    {
      "id": "stdin-before-watcher-publication",
      "text": "Static race candidate, NOT runtime reproduced: write_stdin_inner holds interaction_lock from process_manager.rs:1043 through its terminal branch at 1228-1229. The watcher needs the same lock before publish_exit at async_watcher.rs:191-211. If the child exits during the stdin poll, the receipt can still be Armed when claim_terminal_stdin_output runs; lease_for_sampling only accepts Queued, so receipt_hooks.rs:332-337 returns without consuming and the caller unbinds. Once stdin returns and releases the interaction lock, watcher can queue a pushed completion despite already-returned terminal output. Existing stdin tests wait for Queued BEFORE invoking write_stdin (receipt_hooks_tests.rs:1236,1296), so they do not force this order. Proposed regression: invoke write_stdin while Armed, force exit during its held interaction lock, assert one delivery/consumed claim. No Rust reproduction run."
    },
    {
      "id": "initial-yield-test-shape",
      "text": "AC2 requires both orders forced with barriers through exec_command. Tests at receipt_hooks_tests.rs:763-845 use echo with 30000ms and sleep 2 with 250ms, rather than barriers around the response decision. Hosted success establishes those runs only, not the mandated forced race."
    },
    {
      "id": "b1-preservation",
      "text": "Checkpoint 3431fef introduces completion_receipt.rs, completion_receipt_tests.rs and mod.rs. Blob comparison: completion_receipt_tests.rs unchanged; completion_receipt.rs changed (TerminalCompletion documentation, ExecCompletionMode, Retired error, SamplingLease::receipt_id, active_len); mod.rs changed for hooks/store ownership. Therefore B1 paths are NOT literally all unchanged; B1 test bytes are unchanged and B2 brief expressly permits necessary API hooks. No B1 transition implementation was changed in that diff."
    },
    {
      "id": "hosted-evidence-bound",
      "text": "Attached hosted-precheck-2 reports all four lanes successful and 16/16 intended mutant kills. Its declared tree matches replay, and local git rev-parse of snapshot 9e692fdcd16a373a59f7d262159b377d588163d0 independently returns the same tree. This panel did not query GitHub live or rerun tests/mutants. Hosted reports are accepted as attached evidence only; they do not repair the omitted local command transcript."
    },
    {
      "id": "retired-marker-growth",
      "text": "Bounded static free hunt: receipt_output.rs:66-70,128-141 keeps retired markers in an unbounded HashMap; repeated LRU retirement can grow metadata until release/shutdown. B2 AC caps retained output and live slots but does not specify a marker-history bound, so this is an out-of-contract note, not a blocking finding."
    }
  ],
  "surface_results": [
    {
      "row": "receipt hooks in unified exec",
      "result": "not-attacked",
      "reason": "All attack families were statically swept (matrix below), but no public-entry runtime attack was run because the panel brief explicitly forbids cargo/just/build/test execution. The reviewer role defines held as an attack run through a public entry point; this panel does not relabel static inspection or producer results as its own executed attack. Runtime confidence remains bounded; two concrete schedules are recorded as notes, not reproduced findings."
    }
  ],
  "free_hunt": {
    "budget_minutes": 3,
    "scope": "Evidence-integrity and retention metadata beyond the table; static only.",
    "findings": [
      "truncated-cr-validation-evidence"
    ],
    "notes": [
      "retired-marker-growth"
    ],
    "runtime_execution": "none"
  }
}
```
