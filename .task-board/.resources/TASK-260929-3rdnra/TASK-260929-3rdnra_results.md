# V1 subagent notification bridge — review handoff on hosted precheck 4

Task: TASK-260929-3rdnra — v1-subagent-notification-bridge.
Checkpoint: `8a9cf9c2af0e815cb25893a1fbb21524dc0f3147`.
Candidate tree: `c57fb1b76d54fff5816a1a264a76d497bb80b50d`.
Hosted snapshot: `f1dd5d5a4d34`, `ci/TASK-260929-3rdnra/wip-4`.
Authoritative supplied evidence: `TASK-260929-3rdnra_hosted-precheck-4.md`, relux-ci run `38690480458`.

The exact unchanged candidate is ready for review: hosted lint, small, core and app-server succeeded; 10 of 10 narrowing mutants were killed by named behavioral failures, with no compile failures or survivors. This handoff pass made no candidate edits and ran no local builds, tests, formatter, or mutations of product code. A temporary Git index independently reproduced the hosted tree, including untracked candidate source files, without staging the real index. The candidate remains UNCOMMITTED for the managed Story snapshot; publication/integration belongs to the orchestrator.

## Behavior and scope

V1 completion watchers enqueue the bounded SubagentNotification fragment as runtime mailbox data. Idle mailbox recording persists the notice without sampling or granting wake permission; its recorded mailbox entry remains available for G1's registration recheck and retires without another history append. A registered goal-owned SleepItem permits wake; ordinary parents receive data without an autonomous request. No AgentPath or inter-agent event is fabricated. V2 retains its existing inter-agent terminal routing and deferred delivery behavior.

Twelve changed paths, all within `codex-rs/core`:

- `src/agent/control.rs`, `src/agent/control/completion.rs`, `src/agent/control_tests.rs`, new `src/agent/control_bridge_tests.rs`.
- `src/codex_thread.rs`, `src/context/subagent_notification.rs`, `src/session/input_queue.rs`, `src/tasks/mod.rs`, new `src/tasks/mailbox.rs`.
- `tests/suite/pending_input.rs`, new `tests/suite/pending_input_subagent_bridge.rs`, `tests/suite/goal_background_wait.rs`.

No dependencies, generated schemas, README, docs, CI, or control-root source files changed. All prior reviewer test names are retained. Upstream `subagent_notification_is_included_without_wait` and G1 `goal_native_wait.rs` are unchanged. The existing P4a scheduled-check-in test is the only addition outside the initial bridge-file set: the precheck-3 brief explicitly required its synchronization repair, with its name, counts and deadlines preserved. No goal policy production code changed.

The previously measured candidate is 936 changed lines (674 lines in the two new bridge test files), an explicit exception to the usual 800-line guidance. The precheck-4 rework changed only three test files; production files are byte-identical to precheck 3. Splitting off mandatory regression repairs would leave a known red baseline or omit required AC evidence.

## Acceptance coverage

**7 of 7 AC rows driven through named production entry points and green in hosted precheck 4.** These are reused exact-tree hosted results, not tests rerun by this handoff session. The AC1–AC7 table was provided in the assignment before this run. Tests are in the managed uncommitted candidate and in the orchestrator's hosted snapshot; no producer commit is created.

| AC | Production call site | Driving and negative tests | Killed narrowing mutants |
|---|---|---|---|
| AC1 queue-only V1 delivery | `maybe_start_completion_watcher` → `queue_runtime_fragment` → `enqueue_runtime_fragment` | `native_status_mailbox_fragment::v1_completed` asserts mailbox data, empty active-reservation history and no inter-agent operation | `v1_direct_inject` |
| AC2 registered wake / ordinary silence and retention | `maybe_start_turn_for_pending_work_with_sub_id`; `record_idle_runtime_fragments` | `native_completion_mailbox_history_and_wake::{v1_registered_wait,v1_without_wait}`; `native_interrupted_wait_wakes_once::{v1_registered,v1_unregistered}`; unchanged `subagent_notification_is_included_without_wait` | `v1_ordinary_wake`, `v1_interrupt_without_goal`, `v1_drop_without_wait` |
| AC3 real child identity, no fabricated path/events | V1 watcher runtime-fragment submission | V1 status matrix and `native_completion_mailbox_history_and_wake::v1_registered_wait` check UUID, absence of `/root` and absence of inter-agent operations | `v1_fabricated_path` |
| AC4 both-version status matrix and bounds | watcher status events; `notify_parent_of_terminal_turn` | `native_status_mailbox_fragment::{v1_completed,v1_error,v1_closed,v1_interrupted,v2_completed,v2_error,v2_closed,v2_interrupted}`; `native_v1_fragment_bounds_payload::{completed_escaped,error_unicode,error_escaped}` | `v1_direct_inject`, `v1_unbounded_error` |
| AC5 second child mid-turn, once | active mailbox activity → sleep interruption → sampling drain | `native_second_child_finishes_mid_turn_once::{v1,v2}` checks both results, exactly once | `v1_drop_midturn`, `v1_duplicate_fragment` |
| AC6 before/after V1 transcript | idle mailbox claim → annotated history recorder → normal drain | `native_completion_mailbox_history_and_wake::v1_without_wait`; `native_runtime_fragment_records_idle_history_once_and_retains_wake` checks unchanged prefix, exactly one fragment, matching role/content/phase and the exact stamped item on re-read | `v1_idle_fragment_reappended`, `v1_drop_without_wait`, `v1_direct_inject` |
| AC7 V2 preserved | existing terminal router and queue delivery phases | V2 status/HTTP cases, especially `native_completion_mailbox_history_and_wake::v2_without_wait`, assert no autonomous wake and exact subsequent explicit-user-turn requests; unchanged pending_input/G1 regressions | `v2_result_wakes_ordinary` |

## Coverage map

All **6 of 6** rows from the attached `surface-table.md` are mapped below in brief order. No surface or AC row is declared out of contract.

| Surface row | Attacking tests | Killed narrowing mutants | Out-of-contract inputs (AC clause) |
|---|---|---|---|
| V1 delivery channel | `native_status_mailbox_fragment::v1_completed`; `native_runtime_fragment_records_idle_history_once_and_retains_wake` | `v1_direct_inject` → both named tests; `v1_duplicate_fragment` → idle-history regression | none claimed |
| wake permission | both-version `native_completion_mailbox_history_and_wake`; `native_interrupted_wait_wakes_once::v1_unregistered`; unchanged upstream no-wait test | `v1_ordinary_wake` → idle-history regression; `v1_interrupt_without_goal` → `v1_unregistered`; `v1_drop_without_wait` → upstream no-wait test; `v2_result_wakes_ordinary` → hosted `after_final` | none claimed |
| identity and paths | V1 status cases and `native_completion_mailbox_history_and_wake::v1_registered_wait`; V2 status/HTTP controls | `v1_fabricated_path` → `v1_registered_wait` and `v1_closed`/`v1_completed`/`v1_error`/`v1_interrupted` | none claimed |
| status matrix and bounds | all eight `native_status_mailbox_fragment` cases; `native_v1_fragment_bounds_payload` cases | `v1_unbounded_error` → `error_escaped`, `error_unicode`; `v1_direct_inject` → V1 completed/error/closed cases | none claimed |
| mid-turn and idle history | both-version `native_second_child_finishes_mid_turn_once`; `native_runtime_fragment_records_idle_history_once_and_retains_wake` | `v1_drop_midturn` → mid-turn `v1`; `v1_duplicate_fragment` → mid-turn `v1`; `v1_idle_fragment_reappended` → idle-history regression | none claimed |
| transcript change and regressions | `native_completion_mailbox_history_and_wake::v1_without_wait`; idle-history regression; upstream no-wait, pending_input, G1 native wait and `scheduled_checkins_fire_through_production_runtime_under_paused_time` | `v1_drop_without_wait` → upstream no-wait and `v1_without_wait`; `v1_idle_fragment_reappended` → idle-history regression and `v1_without_wait` | none claimed |

## Mutation results

Source: supplied hosted precheck-4 evidence. Every mutant failed behaviorally in the core lane on all three nextest tries; no compile errors. **10 of 10 killed; 0 survivors.** The evidence supplies named failing tests and job conclusions, not numeric mutant-process exit codes; no numeric exits are invented here. Short case names below are those reported in the hosted resource, qualified where their owning test is unambiguous.

| Mutant | What it narrows the gate to | Named observed failing test | Result / surviving bound |
|---|---|---|---|
| `v1_direct_inject` | V2 remains queued, V1 alone directly injects | `native_status_mailbox_fragment::v1_completed`; idle-history regression | killed; no survivor |
| `v1_drop_midturn` | Idle delivery remains, active-task V1 arrival is dropped | `native_second_child_finishes_mid_turn_once::v1` | killed; no survivor |
| `v1_drop_without_wait` | Registered parents retain data, ordinary parents lose it | unchanged `subagent_notification_is_included_without_wait` | killed; no survivor |
| `v1_duplicate_fragment` | V1 enqueues twice, V2 unchanged | `native_second_child_finishes_mid_turn_once::v1`; idle-history regression | killed; no survivor |
| `v1_fabricated_path` | V1 alone synthesizes `/root/worker` | `native_completion_mailbox_history_and_wake::v1_registered_wait` | killed; no survivor |
| `v1_idle_fragment_reappended` | Active delivery remains, idle item is appended again | `native_runtime_fragment_records_idle_history_once_and_retains_wake` | killed; no survivor |
| `v1_interrupt_without_goal` | Only Interrupted bypasses goal-wait permission | `native_interrupted_wait_wakes_once::v1_unregistered` | killed; no survivor |
| `v1_ordinary_wake` | Runtime entries alone gain autonomous trigger authority | `native_runtime_fragment_records_idle_history_once_and_retains_wake` | killed; no survivor |
| `v1_unbounded_error` | Completed remains bounded, Errored bypasses cap | `native_v1_fragment_bounds_payload::{error_escaped,error_unicode}` | killed; no survivor |
| `v2_result_wakes_ordinary` | V1 stays queue-only, V2 results gain trigger authority | `after_final`; `bounded_retained_root_messages` | killed; no survivor |

No source-text-inspecting gate is introduced. The source-token-control checklist is therefore inapplicable, not a claim of an executed static-checker mutant. Hosted behavioral suites, rather than patch applicability or lint, establish the reported kills.

## Validation and identity reuse

| Evidence or command | Result | Attribution |
|---|---|---|
| Hosted relux-ci run `38690480458`, snapshot `f1dd5d5a4d34` | lint, small, core, app-server all success | supplied authoritative precheck-4 resource; no local rerun |
| Hosted ten mutants | all killed by named behavioral failures, three tries each | supplied precheck-4 resource; no numeric process exits supplied |
| `git read-tree HEAD` using temporary index | exit 0 | this session |
| `git add -A` using that temporary index | exit 0 | this session; real index untouched |
| `git write-tree` using that temporary index | exit 0; `c57fb1b76d54fff5816a1a264a76d497bb80b50d` | this session; exact hosted tree equality |
| `python3 …/codex-fix-suite-busy.py --any` | exit 0, FREE | this session; no local build launched |
| Local cargo/just build, test, clippy, fmt, mutants | NOT RUN | explicitly forbidden/unnecessary for unchanged exact-tree handoff |

Prior pass command records remain in `TASK-260929-3rdnra_precheck4-validation.log`: `just fmt`, target guard, static identity checks, diff whitespace and ten patch applicability checks exited 0. Those are historical records, not commands rerun in this session. Earlier red prechecks do not substitute for the now-green baseline. The handoff session corrected one exploratory board query (`task` is not an operation; exit 1) to `get` (exit 0); optional skill-directory search returned exit 2 for absent directories. Neither is a validation result.

## Root causes and bounds retained

- Idle stamps match the existing no-new-turn injection path: both recording contexts call `new_default_turn_for` and allocate a fresh `next_internal_sub_id`, whose established spelling is `auto-compact-N`. This is fresh internal recording provenance, not a stale previous turn. Normal history preparation stamps the item ID, turn ID and create time. The regression checks exactly one added item and the exact same stamped object after another scheduler pass, as well as fragment role/content/phase.
- New HTTP tests use server captures filtered by thread instead of ResponseMock capture counts. The recorder matcher runs before custom predicates, so the old count included requests that did not match that mock. All request/count assertions remain exact.
- The P4a check-in test previously advanced paused time before the post-TurnComplete asynchronous idle lifecycle had registered its next deadline, and used a yield count to await a warning emitted after DB work. It now waits for real deadline registration and the actual sink warning, bounded by timeouts. Exact 30/60/120-minute deadlines, three requests/check-ins and one warning remain asserted. Production code is unchanged; precheck-4 core is green. This does not claim a separate stress/repeat run beyond the supplied evidence.
- No AC row or surface row is excluded. Error/closed cases enter the production status router rather than exercising the entire V2 shutdown lifecycle. G1 owns wait registration/removal; the bridge's HTTP tests install its SleepItem, while existing G1 regressions remain in the green core suite.
- V1 keeps its existing single-final-status watcher lifetime; reused child turns are not newly guaranteed. V2 successful-output sizing remains unchanged. V1 child reference is capped at 64 Unicode scalars and status text at 384 plus suffix; serialized fragment is below 3 KiB. This is not a tokenizer-specific 1,000-token guarantee: adversarial escaping may require the repository's additional manual context review. It remains below the 10K ceiling.
- No new cross-platform run is claimed here. The precheck resource does not list OS/foreign-exec lane detail; Windows and foreign-exec behavior beyond supplied hosted coverage remains unverified. Live mailbox bookkeeping is not restored as wake authority from transcript text.

## Outcome-scoped logbook and handoff

The resumed handoff session verified the unchanged hosted tree before accepting evidence, retained the uncommitted Story checkpoint, and refreshed the task-scoped results with the newly supplied six-row surface table. All seven AC rows, six surfaces, negative tests, and ten named mutant failures are now backed by green exact-tree hosted evidence. Source-text gate checklist is explicitly inapplicable. No local build was attempted, no candidate file changed, no direct control-root/logbook file was edited, and no commit, push, branch switch or PR was made. This resource carries the logbook record. The existing results resource is refreshed and a new task-scoped handoff outcome is attached before requesting developer handoff.

Disposition requested: **ready for review**, subject to the board's synchronous handoff gate. This is not reviewer acceptance or Story landing.
