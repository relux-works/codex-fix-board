# Panel B verdict — CR-TASK-260929-3r7peh-1 rev1 (TASK-260929-3r7peh)

Reviewer task: TASK-261007-j2lf0k. Non-recording review; nothing was written on TASK-260929-3r7peh (no accept/reject/status/handoff there). No cargo/just/build/test command was run, per the panel brief.

## Replay tree check: MATCH

Base 2f522b9dc9d639fe5195d93d61431a0caff662d5 + resource TASK-260929-3r7peh_change-request_rev1.patch through a temporary index (never a nested worktree) yields exactly the expected candidate tree dbd39ab8c59adabe27ebb25838003680214c8d14.

## Commands and exit codes

- task-board m 'set_status(TASK-261007-j2lf0k, status=analysis)' → exit 0
- task-board resource get TASK-260929-3r7peh × 8 (patch, surface-table.md, results, mutants.json, producer-brief.md, hosted-precheck-3.md, validation log, handoff note) → all OK
- GIT_INDEX_FILE=$PWD/.temp/TASK-261007-j2lf0k-replay.idx git read-tree 2f522b9d… → exit 0
- GIT_INDEX_FILE=… git apply --cached .temp/TASK-261007-j2lf0k/TASK-260929-3r7peh_change-request_rev1.patch → exit 0
- GIT_INDEX_FILE=… git write-tree → exit 0, printed dbd39ab8c59adabe27ebb25838003680214c8d14 (MATCH)
- git archive dbd39ab8… | tar -x -C .temp/TASK-261007-j2lf0k-cand → exit 0
- git diff/git show/git grep read-only inspections of the candidate tree → exit 0

Candidate files were read via git show and the extracted archive only. The CR validation log (local fast lane) is green: target guard exit 0, fmt-check exit 0, clippy exit 0, small-crate tests 267/267 exit 0. Hosted precheck 3 (snapshot 74434fa5, run 37618361186) ran this exact candidate tree with lanes lint/core/app-server/small all green and 9/9 narrowing mutants killed, 0 survivors; those hosted runs are cited below as the executed public-entry attacks.

## Verdict

accept

```verdict-findings
{
  "findings": [],
  "notes": [
    "Residual release-between-recheck-and-wake window in enqueue_published_completion is shared with the pre-existing wake race (producer-stated bound). Worst case is a spurious idle turn with no fragment, not a missed or ghost wake: release still cancels the mailbox entry, and the mailbox dedupes by receipt id. No CR-introduced hazard.",
    "Interrupt/terminate/shutdown cancel store receipts but not mailbox entries; only release cancels the mailbox entry. Pre-existing deferred behavior, producer-stated; post-exit terminate is moot and the interrupt-after-enqueue window delivers an already-occurred exit.",
    "Goal background_wait enables at thread start regardless of the goal enabled flag; dormant while disabled, already correct if enabled later. Producer-stated, no hazard.",
    "MCP/Custom/Unknown hosts stay Unavailable (fail closed) until persistence is verified. Intended, covered by async_notification_roots_follow_host_session_source.",
    "Candidate diff is 31 files, ~3188 insertions / 37 deletions, exceeding the 800-line guidance; the leaf is an atomic activation (schema + tool + delivery + policy must land together; sibling F2 stacks on it) and cannot be staged without shipping a half-promise. Accepted as justified."
  ],
  "surface_results": [
    {
      "row": "host capability",
      "result": "held",
      "evidence": "Default Unavailable via #[default] + read_from unwrap_or_default. for_host_session_source enables only Cli/VSCode (exhaustive match; Exec/Mcp/Custom/Internal/SubAgent/Unknown unavailable). spawn_thread inherits the parent stored value explicitly, fails closed on unknown parent, never consults the child source. thread/start seeds roots from the manager session source. Registration + schema property gated on is_available() && Interactive; Unavailable description byte-identical. Executed: m2 killed by async_notification_child_of_headless_parent_stays_unavailable + roots Mcp arm; m3 killed by notify_on_exit_refused_before_execution_on_unavailable_host + suite exec_notification_opt_in_refused_on_headless_exec; listing/schema tests green on the exact tree (precheck 3, all lanes green)."
    },
    {
      "row": "opt-in and receipts",
      "result": "held",
      "evidence": "notify_on_exit #[serde(default)] false; m1 killed by exec_command_args_default_notify_on_exit_to_false + suite default-launch no-arm/no-wake (sentinel silence proof). Handler maps opt-in to NotifyOnExit; m6 killed by 3 suite tests. One-shot/to-completion path hardcodes Default but is unreachable with notify=true (OneShot refused pre-execution at exec_command.rs:262; completion_timeout is Some only for OneShot at :338-340). Reserve-before-spawn with ReceiptCapacityExceeded mapped to a clear model error and process-id release; sixty_fifth test asserts refusal + empty process list + default still runs with no receipt; MAX_COMPLETION_RECEIPTS=64 with used>=64 refuse (no off-by-one). Only production Arm/reserve sites are exec_command_inner under NotifyOnExit; codex_thread Arm sites are test-only helpers; no arming on yield/stdin poll. Executed: precheck 3 core lane green incl. capacity + default suites."
    },
    {
      "row": "exec_notification read and release",
      "result": "held",
      "evidence": "Tool entry refuses on Unavailable hosts (defense in depth). notification_owner_for_receipt resolves the binding then verifies thread+generation; m5 killed by read_rejects_foreign_receipt + owner-across-calls test. read clamps budget 1..9000 (default 2000), indicates truncation, asserts <10K tokens incl. a 1M-token arm; pre-exit read rejected without waiting (InvalidTransition Reserved/Armed). Unknown/malformed/foreign/stale-after-release/retired/consumed each rejected with dedicated tests + suite unknown test. release = store cancel + binding/retention drop + cancel_runtime_notification, touches no process state; m4 killed by release_disarms_frees_slot_and_cancels_pending_wake; alive-poll + stale-read + sentinel no-wake proofs in lib and suite. Ghost retention: single post-enqueue recheck drops retention + cancels entry; m9 killed by drops_ghost_retention with narrowness proven by skips_disarmed still passing. Executed: precheck 3 core lane green."
    },
    {
      "row": "activation",
      "result": "held",
      "evidence": "Goal on_thread_start enables background_wait_state only where read_from is Available. m7 killed by background_wait_activates_only_on_available_hosts (Available arm) + suite gates-goal-but-admits-user-input (0 requests while gated, then exactly 1 user request carrying 'continue please' in user input text). m8 killed by the Unavailable arm + suite inactive-on-unavailable auto-continues. End-to-end receipt->mailbox->wake->fragment proven by the suite asserting EXEC_COMPLETION_WRAPPER via body_contains_text in the wake request. Executed: precheck 3 small/lint/core lanes green on the exact tree."
    }
  ],
  "free_hunt": [
    {
      "id": "FH1",
      "area": "to-completion path drops completion_mode (handler computes NotifyOnExit but Some(timeout) branch calls exec_command_to_completion which hardcodes Default)",
      "result": "not a bug: unreachable with notify_on_exit=true because OneShot lifetime is refused pre-execution before that branch (exec_command.rs:262 vs :338-340). Layered defense holds."
    },
    {
      "id": "FH2",
      "area": "release racing the single post-enqueue recheck (release lands after recheck passes, before maybe_start_turn_for_pending_work)",
      "result": "benign residual shared with the pre-existing wake race; at most a spurious idle turn, no ghost wake or leaked retention. Recorded as a note, not a finding."
    },
    {
      "id": "FH3",
      "area": "capacity accounting with retire_least_recently_sampled (used = active + sampled; retire path could admit a 65th reservation)",
      "result": "correct: retirement frees a real sampled slot, so admission after retire is capacity-consistent; with 64 active + 0 sampled the 65th is refused, as the lib test proves."
    },
    {
      "id": "FH4",
      "area": "model-supplied receipt handle parsing (whitespace, non-UUID, foreign UUID)",
      "result": "from_model_handle trims and returns None for non-UUID (rejected as unknown); parsed ids are lookup keys only with ownership verified separately. Covered by malformed/unknown/foreign tests."
    },
    {
      "id": "FH5",
      "area": "mailbox double-enqueue (watcher + raced arm both calling enqueue_published_completion)",
      "result": "structurally impossible: publish/arm-to-Queued succeeds at most once per receipt id (Queued carries the TerminalCompletion through the rendezvous), and the mailbox dedupes by receipt id."
    }
  ]
}
```
