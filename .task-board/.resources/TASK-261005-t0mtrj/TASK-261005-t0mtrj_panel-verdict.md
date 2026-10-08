# TASK-261005-t0mtrj — R141 panel B, watcher and output retention hooks rev1

changes_requested

## Replay and decision

Temporary-index replay of CR-TASK-260929-4ut0up-1 on base `ea8899e6f97aea64136159286840c28c955243e8` produced exactly `7de6b3c2ed82f07002c613263cd650cc16b20108`; read-tree, patch materialization, cached apply and write-tree each exited **0**. The patch is authentic to the candidate tree. No normal index, branch, source file or reviewed-task state was mutated.

This is an **evidence-limited static panel**, not a runtime rejection of the implementation. The brief forbids builds/tests, while the reviewer role defines held by public-entry execution and blocking findings by a failing reproduction. Consequently the single surface row is explicitly not-attacked for executable verification, findings is empty, and the three concrete static race/path concerns below remain notes. Acceptance cannot be asserted under that role definition. Recommendation: the recording reviewer should confirm these focused schedules, using the existing hooks test fixtures, before accepting; do not treat notes as reproduced failures or route a new generalized research/harness prerequisite.

## Sources and execution evidence

All candidate citations below refer to `git show 7de6b3c2ed82f07002c613263cd650cc16b20108:<path>`, extracted under `.temp/TASK-261005-t0mtrj-cand/`. Read-only board sources: `surface-table.md`, `producer-brief.md`, `b2-fix-note-1.md`, `TASK-260929-4ut0up_results.md`, `TASK-260929-4ut0up_hosted-precheck-2.md`, `TASK-260929-4ut0up_change-request_rev1-validation.log`, and the 16-entry precheck results JSON referenced by the hosted resource.

- Snapshot commit `9e692fdcd16a373a59f7d262159b377d588163d0^{tree}` resolves locally to the exact candidate tree (exit 0).
- [Hosted run 37219783600](https://github.com/relux-works/codex/actions/runs/37219783600) independently reports completed/success for lint, small, core and app-server. GitHub's run head_sha is the dispatcher base `ea8899e6…`, NOT the tested snapshot. Workflow dispatch explicitly checks out inputs.sha; downloaded logs for all four lanes show `HEAD is now at 9e692fd` and WANT_SHA equal to the full snapshot commit. This resolves the apparent identity discrepancy.
- Hosted summaries: core 4903 passed, 11 skipped, including one flaky/retried test; app-server 1827 passed, 2 skipped; small 232 passed, 0 skipped. These are accepted hosted evidence, not checks rerun by this panel.
- Precheck 2 reports 16/16 intended mutant kills. The local results JSON contains 16 killed=true entries. This panel did not rerun mutant jobs or independently inspect all 16 mutant logs; their result is attributed to that resource, not claimed as fresh verification.
- The CR validation log shows guard and fmt-check with exit 0, but has an explicit truncation marker at line 812 (42796 bytes omitted). It contains a final exit 0 and a 232-test small-crate summary, then required=4 green=4 failed=0 missing=0 and test_case_coverage=unknown. The clippy boundary and intervening exact commands are not fully observable; their green status is not independently verified from this truncated log. Hosted lint/small lane results are separate exact-tree evidence. No local or hosted test was launched here.
- B1 preservation: completion_receipt_tests.rs is byte-identical to checkpoint 3431fef (`git diff --exit-code`, exit 0). completion_receipt.rs is NOT byte-identical: B2 adds 34 lines for docs, ExecCompletionMode, Retired, SamplingLease::receipt_id and active_len. Existing B1 transition bodies remain unchanged. Literal “all B1 paths unchanged” is therefore false, but these additions are expressly allowed by B2 scope. The full story patch includes B1; do not confuse its size with B2-only edits.
- Scope: CR delta is confined to unified_exec; no new tool schema, mailbox, context fragment, app-server API or config change. B2-only delta remains much larger than the generic 800-line guidance, mainly 1675 lines of hooks tests; flag as reviewability guidance, not a reproduced runtime defect.

## Static sweep (9/9 named attack families inspected; 0/9 executed here)

| Family | Static observation / evidence bound |
|---|---|
| Exit around initial yield | reserve-before-spawn and Arm/InlineResult transitions traced; existing two tests exercise timing-separated orders but do not force the boundary with barriers. |
| Drain/denial/final classification | watcher awaits exit, drain, monitor, then interaction lock; failure maps to None and timed_out preserved. Synthetic watcher tests inspected; early stdin ordering remains unverified. |
| 3 MiB retained output | transcript copies into a second cap; head/tail and omitted-byte arithmetic inspected; named 3 MiB test asserts 1 MiB and 2 MiB omitted. |
| 64/65 and LRU | unsampled refusal happens before open_session_with_sandbox; active + sampled count and min sample_seq inspected. Publication/retention gap can escape this count (note). |
| Stdin/pushed race | existing tests start stdin only after Queued; interaction-lock trace identifies the untested pre-publication order (note). |
| Release/terminate/interrupt/shutdown | matching reasons traced in non-TTY paths; release avoids killing; shutdown clears hooks. TTY interrupt and late retention insert are unverified concerns. |
| Unknown/foreign reads | retention and store paths compare owner; supplied tests cover foreign thread/generation/call and unknown ID. No forged-owner execution run. |
| Default >64 | public exec_command selects Default, oneshot also selects Default; 70 default launches and a live default launch are tested in supplied sources. No fresh byte-equivalence measurement. |
| Process-store removal before read | receipt-owned transcript survives release_process_id; named test removes process before read. Publication/retention gap is a separate concern. |

## Command ledger (panel execution, not producer execution)

All replay/check commands ran as standalone processes with no tee/pipeline. Other read commands were batched; an exit attached to a batch is its shell exit, not a claimed exit for every intermediate read.

| Command | Exit | Result |
|---|---:|---|
| task-board m set_status on this panel task | 0 | analysis |
| command -v task-board; git --version; rg --version; skill-file search | 2 | tools ready; search included absent directories, not a validation pass |
| task-board q get reviewed task with resources | 1 | unsupported field; repaired by direct read-only resource discovery |
| task-board q get reviewed task description scope ac | 0 | 7 AC rows read |
| task-board q schema(get) | 0 | response contains positional-argument error, not successful schema read |
| task-board q schema(operation="get") | 0 | signature read |
| task-board q get reviewed task with artifacts | 1 | unsupported field; no evidence inferred absent |
| task-board resource get reviewed-task patch --output .temp/TASK-260929-4ut0up_change-request_rev1.patch | 0 | materialized read-only input |
| GIT_INDEX_FILE=$PWD/.temp/TASK-261005-t0mtrj-replay.idx git read-tree ea8899e6f97aea64136159286840c28c955243e8 | 0 | base loaded |
| GIT_INDEX_FILE=$PWD/.temp/TASK-261005-t0mtrj-replay.idx git apply --cached .temp/TASK-260929-4ut0up_change-request_rev1.patch | 0 | applied |
| GIT_INDEX_FILE=$PWD/.temp/TASK-261005-t0mtrj-replay.idx git write-tree | 0 | exact expected tree |
| git archive --format=tar --output=.temp/TASK-261005-t0mtrj-cand.tar TREE codex-rs/core/src/unified_exec; tar extraction and candidate read batch | 0 | local scratch only; no archive attached |
| git rev-parse 9e692fdcd16a373a59f7d262159b377d588163d0^{tree}; git diff --exit-code 3431fef TREE -- codex-rs/core/src/unified_exec/completion_receipt_tests.rs | 0 | candidate identity and B1 test identity |
| git diff --check ea8899e6f97aea64136159286840c28c955243e8 TREE | 0 | whitespace check |
| gh --version | 0 | 2.97.0 |
| gh api repos/relux-works/codex/actions/runs/37219783600 --jq run projection | 0 | completed/success |
| gh api repos/relux-works/codex/actions/runs/37219783600/jobs --jq job projection | 0 | 4/4 lanes success |
| gh run view 37219783600 --repo relux-works/codex --log | 0 | downloaded .temp/TASK-261005-t0mtrj/hosted.log |
| git show TREE:codex-rs/core/src/unified_exec/process_manager.rs | 0 | static-stdin-trace.txt |
| git show TREE:codex-rs/core/src/unified_exec/async_watcher.rs | 0 | static-publication-trace.txt |
| git show TREE:codex-rs/core/src/unified_exec/receipt_hooks.rs | 0 | static-claims-trace.txt |
| task-board spawn directives current run | 0 | none |
| remaining cat/sed/nl/rg/git status and diff read batches | 0 | source/evidence inspections, no executable adversarial checks |

TREE in the ledger means the full candidate OID above. No expected-red runtime gate was run. The two query parse failures and failed search are reported as failures, not passing gates.

## Task-scoped logbook entry

2026-10-05: Exact replay and hosted checkout identities agree. Identified three source-level schedules missing from current evidence: terminal stdin before watcher publication; receipt publication before retention installation; TTY Ctrl-C bypassing cancellation. No runtime reproduction under the explicit no-build/no-test panel constraint; retain these as notes per the role evidence rule. The local CR log explicitly omits 42796 bytes; do not reuse it as complete per-command evidence. Sweep and bounded free hunt performed without writes to TASK-260929-4ut0up. This artifact is the only attached outcome; all control-root persistence uses task-board on the panel task.

```verdict-findings
{
  "findings": [],
  "notes": [
    {
      "id": "stdin-before-publication",
      "row": "receipt hooks in unified exec",
      "severity": "note",
      "sources": [
        "codex-rs/core/src/unified_exec/process_manager.rs:1043",
        "codex-rs/core/src/unified_exec/process_manager.rs:1228",
        "codex-rs/core/src/unified_exec/receipt_hooks.rs:332",
        "codex-rs/core/src/unified_exec/async_watcher.rs:191"
      ],
      "observation": "Static interleaving: write_stdin holds the process interaction lock while polling. If the process exits during that poll, the watcher cannot acquire the same lock to publish. Terminal stdin attempts lease_for_sampling while the receipt is Armed, gets InvalidTransition, silently returns from the claim helper, unbinds, and still returns terminal output. After stdin drops the interaction lock, the watcher publishes Queued; a pushed lease can then succeed. This appears to violate AC5 single-claim delivery.",
      "confirmation_needed": "Drive write_stdin before exit, wait until it holds interaction_lock, then send exit and close output. Require terminal stdin to consume or deliberately defer the receipt claim and require no later pushed completion. Existing terminal_stdin_claim_consumes_the_single_claim_first and terminal_stdin_and_pushed_claims_race_exactly_once both wait for Queued BEFORE invoking write_stdin, excluding this order. No runtime reproduction run in this panel."
    },
    {
      "id": "publication-retention-nonatomic",
      "row": "receipt hooks in unified exec",
      "severity": "note",
      "sources": [
        "codex-rs/core/src/unified_exec/async_watcher.rs:211",
        "codex-rs/core/src/unified_exec/async_watcher.rs:215",
        "codex-rs/core/src/unified_exec/async_watcher.rs:221",
        "codex-rs/core/src/unified_exec/receipt_hooks.rs:313",
        "codex-rs/core/src/unified_exec/receipt_hooks.rs:242",
        "codex-rs/core/src/unified_exec/receipt_output.rs:93",
        "codex-rs/core/src/unified_exec/receipt_hooks.rs:153"
      ],
      "observation": "Static interleavings: watcher publishes Queued under the store mutex, then awaits output_buffer and later receipt_hooks before inserting pending output. A pushed lease/acknowledgment can occur in that gap: acknowledge_sampled removes the active slot, move_to_sampled finds no output, then the watcher inserts pending output. Combined capacity counts active_len + sampled_count, so this output is not counted and cannot be LRU-retired. Alternatively, release cancels and drops output in the gap, then the watcher inserts output after release; read_retained_output prioritizes retention over Cancelled status. Shutdown/inline settlement have the same late-insertion risk. This appears to violate AC3/4/6.",
      "confirmation_needed": "Hold output_buffer after watcher classification, observe Queued, then separately exercise acknowledge_pushed_completion and release_completion_receipt before allowing insert_pending. Require capacity_used == 1 after sampling nonempty output, and require no readable output after release/shutdown. No runtime reproduction run. Fix should coordinate publication and retention under the combined-state lock, with consistent lock ordering and a focused regression for each schedule."
    },
    {
      "id": "tty-interrupt-cancellation",
      "row": "receipt hooks in unified exec",
      "severity": "note",
      "sources": [
        "codex-rs/core/src/unified_exec/process_manager.rs:1127",
        "codex-rs/core/src/unified_exec/process_manager.rs:1136",
        "codex-rs/core/src/unified_exec/receipt_hooks_tests.rs:1504"
      ],
      "observation": "Static alternate entry: Interrupted cancellation is only in the !tty branch for input == INTERRUPT. With tty=true the same Ctrl-C input goes to process.write with no cancellation hook. A normal PTY SIGINT exit can therefore queue a completion instead of cancelling with Interrupted. The named interrupt_cancels_before_signalling test supplies tty=false. This appears to leave AC6 interrupt coverage incomplete.",
      "confirmation_needed": "Launch opted-in tty=true process through exec_command_with_completion_mode; drive write_stdin with Ctrl-C under ordinary terminal ISIG settings. Require Cancelled { Interrupted } before the interrupt can end the child, and no pushed lease afterward. Clarify intended handling of embedded Ctrl-C if it is part of the supported input contract. No runtime reproduction run."
    },
    {
      "id": "coverage-ordering-bound",
      "severity": "note",
      "observation": "All 7 AC rows name tests (7/7 documentation coverage). This is not measured coverage of every race. AC2 tests use echo with a long yield and sleep 2 with a short yield rather than the requested barriers forcing both initial-response orders. AC1 invokes the watcher directly with a synthetic process and a manually armed receipt rather than driving opted-in exec_command as the AC driving-test column says. The 16 mutant results do not cover the three static schedules above."
    },
    {
      "id": "retired-metadata-bound",
      "severity": "note",
      "sources": [
        "codex-rs/core/src/unified_exec/receipt_output.rs:117",
        "codex-rs/core/src/unified_exec/receipt_hooks.rs:156"
      ],
      "observation": "Free-hunt observation: retired markers and surviving ReceiptHooksState bindings have no bound/automatic eviction during repeated sample-and-retire cycles. Output bytes per receipt are capped, but long-runtime metadata can grow. No explicit retained-marker history limit is stated in the AC; this is a nonblocking design note, not a demonstrated contract violation."
    },
    {
      "id": "truncated-local-validation",
      "severity": "note",
      "source": "TASK-260929-4ut0up_change-request_rev1-validation.log:812",
      "observation": "Explicit 42796-byte truncation prevents verifying all four exact command exits from this log. Do not infer green from aggregate coverage text. Exact-tree hosted lint and small successes are independently read, so this is not a proven build failure."
    }
  ],
  "surface_results": [
    {
      "row": "receipt hooks in unified exec",
      "result": "not-attacked",
      "reason": "Missing executable reproduction fixture within this panel: the brief expressly prohibits builds/tests. All listed families were statically traced and supplied test evidence inspected, but no adversarial public-entry execution ran here. The role contract defines held by an actual public-entry attack and requires a failing reproduction for broken; neither label is asserted from source inspection alone. Static suspected failures are notes, not blocking findings.",
      "families_swept": [
        "exit before/after initial yield",
        "held output drain and denial monitor",
        "3 MiB head/tail retention",
        "64/65 capacity and LRU",
        "terminal stdin versus pushed claim",
        "release/terminate/interrupt/shutdown",
        "foreign/unknown reads",
        "more than 64 default launches",
        "process-store removal before receipt read"
      ]
    }
  ],
  "free_hunt": {
    "budget_minutes": 3,
    "mode": "bounded static inspection only",
    "scope": [
      "B1 identity and B2-only additions",
      "retired metadata lifetime",
      "external API/context/tool-schema scope",
      "hosted exact-tree evidence"
    ],
    "blocking_findings": [],
    "notes": [
      "retired-metadata-bound"
    ],
    "runtime_attacks_run": 0
  }
}
```

Artifact creation and revision scripts exited 0. Standalone JSON/shape verification exited 0: exactly one verdict-findings block, one valid JSON object, one surface result matching the input row, and one one-word verdict. This check validates the report format only, not the suspected runtime failures. Repository status inspection showed no tracked or untracked repository delta; scratch files remain under gitignored .temp. Review budget: 25 minutes for static sweep and evidence inspection, plus a bounded 3-minute free hunt; no new serial prerequisite or build lane introduced.
