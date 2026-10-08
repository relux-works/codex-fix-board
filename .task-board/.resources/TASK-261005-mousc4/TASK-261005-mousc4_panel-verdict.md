# R141 panel B — TASK-261005-mousc4

accept

Read-only panel opinion for CR-TASK-260929-1rcgsj-1 revision 1. Ready for review by the recording reviewer; this panel records no acceptance, rejection, status, notes, resources or handoff on TASK-260929-1rcgsj.

## Replay and commands

Base `47f7a80476eb78f27f7ce97c8bf7eb9236c40b47`. Expected and replayed tree both `37fad741767c46d11094adb9be747d5aae83c145`. The candidate was inspected by tree OID, not assumed to equal the Story worktree HEAD. No nested worktree, build, cargo, just or test invocation was made.

Executed directly by this panel (real exit codes):

| Command | Exit | Result |
| --- | ---: | --- |
| `task-board m 'set_status(TASK-261005-mousc4, status=analysis)'` | 0 | Panel task only |
| `git --version`, `rg --version`, `python3 --version` | 0 each | Readiness logs under `.temp/TASK-261005-mousc4/` |
| `task-board resource get TASK-260929-1rcgsj TASK-260929-1rcgsj_change-request_rev1.patch --output .temp/TASK-260929-1rcgsj_change-request_rev1.patch` | 0 | Read-only input fetch |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-mousc4-replay.idx" git read-tree 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47` | 0 | Base loaded |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-mousc4-replay.idx" git apply --cached .temp/TASK-260929-1rcgsj_change-request_rev1.patch` | 0 | Patch replayed |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261005-mousc4-replay.idx" git write-tree` | 0 | Exact expected tree |
| `git diff --check 47f7a80476eb78f27f7ce97c8bf7eb9236c40b47 37fad741767c46d11094adb9be747d5aae83c145` | 0 | Patch whitespace check |
| `task-board resource get TASK-260929-1rcgsj <name> --output .temp/TASK-261005-mousc4/<local-name>` for `surface-table.md`, `producer-brief.md`, `TASK-260929-1rcgsj_results.md`, `TASK-260929-1rcgsj_mutants.json`, `TASK-260929-1rcgsj_hosted-precheck-1.md` | 0 each | Source artifacts read |
| `git show <candidate-tree>:<path>`, `git diff <base> <candidate> -- <paths>`, `git grep -n -E <lease-caller-pattern> <candidate> -- codex-rs/core/src codex-rs/core/tests`, `git diff --numstat <base> <candidate>` | 0 each | Static source/caller/size inspection |
| `task-board spawn directives RUN-261005-28b4d0` | 0 | No directives |

Read/discovery errors, not validation gates: first `get ... { description scope ac resources notes }` query exited 1 (unknown resources field); `resources(...)` query exited 1 (unknown operation); `schema(get)` returned an error object despite process exit 0 and was corrected to `schema(operation="get")`; guessed resource-directory `ls` exited 2 (path absent); a skill search returned 1 (no matches), and an unmatched zsh roles glob prevented that search. None was treated as evidence of absence or a passing check.

## Evidence and scope

Sources are the five named task-attached input resources above and candidate files `core/src/session/{runtime_mailbox.rs,runtime_mailbox_tests.rs,input_queue.rs,turn_input.rs,turn_input_tests.rs}`, `core/src/tasks/{mod.rs,lifecycle.rs}`, `core/src/codex_thread.rs`, `core/tests/suite/runtime_mailbox.rs` at the exact tree. AC source: `task-board q 'get(TASK-260929-1rcgsj) { description scope ac }'` (exit 0).

Hosted precheck 1 explicitly binds snapshot `f2bf01a5` to the replayed tree. Snapshot run `37278001051` reports lint/small/core/app-server success. Its ten mutant runs report 10/10 killed, 0 survivors, with named core tests; three also fail lint. These are accepted attached execution evidence, not tests rerun by this panel. Expected-red mutant jobs are failures, not green gates. Their numeric command exit codes are absent from the attachment and remain unknown. Local producer fmt/clippy/fix reports are contextual only; no reliance on the truncated CR validation log.

Surface coverage: 3/3 rows held by at least one executed named attack; 0 broken; 0 not-attacked. AC coverage in supplied map: 5/5 have named driving tests; composed publication, cancellation and sampling acknowledgement remain staged out. Held means named attacks did not reproduce on the candidate, not universal absence of defects.

Bounded free hunt examined token loss, caller reachability, cancellation/suspension after leasing, concurrent wake admission, inter-agent precedence, external API/context exposure, and size. No reproduced blocking finding; nonblocking limits are recorded below. No protocol/config/rollout schema change and no new model-context fragment in this delta. Logbook record for this run: retained here as task-scoped outcome (no direct control-root logbook edit); the disclosed token-loss bound and evidence-description precision are the important observations for downstream review.

Plan: decide this rev1 only; frozen base/tree as above; 30-minute worker budget including packaging; one text outcome, no archives; zero serial prerequisites. Consumer is the existing C1 CR recording reviewer. Stop criterion is replay identity, the 3/3 sweep and bounded free hunt. Research grammar freezing is not applicable: no grammar or wire format is proposed.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Staging bound: tasks/mod.rs:487 leases entries but retains no tokens in turn state/input. They remain leased and suppress idle contributors after wake. Candidate results explicitly disclose this; C2 carrier and D acknowledgement wiring are excluded. Do not enable E production publication before these consumers exist. No end-to-end sampled acknowledgement or cancellation is certified here.",
    "Coverage bound: two_runtime_entries_still_start_one_wake_turn enqueues sequentially via a hook that also wakes; it does not synchronize two pending entries before the first wake. Busy-turn and concurrent-arrival timing coverage is not established by its name. Request a deterministic barrier-backed two-pending/busy-turn integration test when delivery is connected.",
    "Settings bound: suite asserts cyber access-program preservation, not changed model/cwd/approval values. Static default-settings path is preserved; direct execution coverage for those individual settings is unknown. Quota object does not exist in this stage; unchanged user texts do not independently prove future quota preservation.",
    "Free-hunt API note: codex_thread.rs:355 adds an unconditional public doc-hidden test enqueue method that arms/publishes real receipts. It is callable outside tests, although no production caller exists in this candidate. Prefer existing test-support boundaries or remove this hook once real publication is testable.",
    "Free-hunt size note: 1012 additions and 6 removals exceeds the 800-line total-change guidance. Smallest coherent split: mailbox module + InputQueue lease/query APIs and their state-machine tests (about 658 changed lines), followed by turn_input admission tests and idle-wake integration/hook (about 360). Current tightly related stage has only about 359 added non-test implementation lines; no reproduced behavioural defect from size alone.",
    "Mutant description precision: ack/fail/duplicate patches delete their entire guards; they are not all narrowing mutants despite producer prose. Suspension/leased-selection mutants genuinely narrow predicates and are behaviourally killed. Stronger future stale-token mutants should admit one stale class rather than remove all token validation.",
    "Accepted evidence is the task-attached hosted precheck, not a fresh live GitHub audit. It binds candidate tree explicitly and names test failures. Hosted process exit codes are not included in that summary: candidate jobs report success, mutants report expected failure; numeric statuses are unknown and are not fabricated."
  ],
  "surface_results": [
    {
      "row": "runtime mailbox lease lifecycle",
      "result": "held",
      "detail": "Exact-tree hosted core snapshot 37278001051; stale ack/fail, leased cancellation, duplicate and re-lease attacks in 37278019338/37278038094/37278056447/37278078920/37278122457/37278142989. InputQueue and mailbox entry tests plus static token/lock trace."
    },
    {
      "row": "trigger and suspension semantics",
      "result": "held",
      "detail": "Exact-tree hosted snapshot; runtime_entry_suppresses_automatic_goal_continuation and suspended_runtime_entry_does_not_block_start_if_idle drive turn_input::handle. Mutants 37278101178/37278163468 killed; leased suspension test green. Static lifecycle and admission callers verified."
    },
    {
      "row": "idle wake",
      "result": "held",
      "detail": "Exact-tree hosted suite one-wake/two-entry/queue-only tests drive CodexThread hook into Session::maybe_start_turn_for_pending_work_with_sub_id; mutants 37278183811/37278203959 killed. Static busy-lock/settings/input-reservation trace. Coverage limits in notes."
    }
  ],
  "free_hunt": []
}
```

Artifact checks: `python3 .temp/TASK-261005-mousc4/write-verdict.py` exit 0; inline Python JSON/fence/row/verdict assertions exit 0 (exactly one valid object, 3/3 unique held rows, one-word accept, no blocking findings). Artifact and scratch files remain under the run worktree's ignored `.temp/`; this follows the explicit run write boundary rather than the conflicting generic instruction to write outside the managed worktree.
