# Merged review verdict — TASK-260929-2snjbb CR revision 2 (tb-R141 / R132 merge)

Verdict: **changes_requested**

Panel outcomes: `TASK-261007-3virnu_panel-verdict.md` (changes_requested), `TASK-261007-uct3ql_panel-verdict.md` (changes_requested), `TASK-261007-3j9xpd_panel-verdict.md` (changes_requested)

Merge rules (R132): identical findings (same row, file and class) collapse; everything else is unioned; each surface row takes its worst panel result; any changes_requested sends the CR back to rework.

```verdict-findings
{
  "findings": [
    {
      "id": "timer-aborts-own-admission",
      "row": "check-in tickets and warning",
      "invariant": "AC4/AC5 scheduled check-ins must reach task registration and subsequent warning; timer invalidation must not cancel an already firing admission.",
      "mechanism": "codex-rs/ext/goal/src/check_in_clock.rs:85-89 keeps the firing JoinHandle in slot while on_fire is awaited. runtime.rs:577 awaits continue_if_idle inside that same timer task. GoalExtension::on_turn_start (extension.rs:248) calls note_turn_start, which fires abort_hook (background_wait.rs:198-204; check_in_clock.rs:50-52). The extension does not override turn_start_phase; contributors.rs:219-220 defaults to BeforeTaskRegistration. Core tasks/mod.rs:383-389 awaits that hook inline before tokio::spawn at line 422. Thus the continuation aborts its own task before registration; if reconcile_activity or later setup yields Pending, cancellation drops start_task with an ownerless reservation and no registered sampling task. Ticket was already consumed. This is a source-established cancellation path, not a claimed executed Tokio failure. Detach the fired timer from the cancellable sleeping slot before invoking the continuation, using identity-safe ownership.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3virnu/static_attack.py (source included below)",
          "command": "python3 .temp/TASK-261007-3virnu/static_attack.py timer",
          "expected_failure": "Actual exit 1, expected-red static source witness. No Rust execution. Request runtime fake-clock test with a deliberately pending turn-start reconciliation; assert all three check-ins register tasks and no bare reservation remains. Add a narrowing mutant retaining the fired handle through its callback.",
          "pinned_blobs": [
            "git-blob:2a4707c2de74d96c1113beedf6972355b56db946",
            "git-blob:8647c6005bf6131884dc395aa59914d1be4a2182",
            "git-blob:38e3444d2446f7710aa98231c61284ac13429e1a",
            "git-blob:1272dcfbf6129a715e5053f5c79aff1f8b8339ea",
            "git-blob:92f3f4c4f9f21461fbb229930470308b08f6b84f"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261007-3virnu"
      ]
    },
    {
      "id": "revision-recheck-before-await-window",
      "row": "admission recheck and invalidation",
      "invariant": "AC7 catches receipt transitions between continuation check and turn start, by serialization or revision rejection.",
      "mechanism": "core/src/session/turn_input.rs:459-464 performs the sole goal admission check, then awaits PreparedTurnInputSettings::prepare (469), apply_started (479), context input processing, and start_task (530). ReceiptStore transitions use their own mutex and atomic revision (core/src/unified_exec/completion_receipt.rs:320,337-338), not the goal semaphore or reservation lock. Schedule a reserve/arm after the last check while preparation is pending: admission observed empty at revision R, receipt moves to Armed at R+1, then the automatic goal still starts without another revision comparison. Existing goal_background_wait_revision_recheck_catches_transition (turn_input_tests.rs:1419) arms before calling handle and installs an inline checker, so it does not exercise this interval.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3virnu/static_attack.py (source included below)",
          "command": "python3 .temp/TASK-261007-3virnu/static_attack.py race",
          "expected_failure": "Actual exit 1, expected-red static ordering witness; no live race executed. Request a barrier in preparation after the real goal checker, arm a receipt through the production store, resume and assert NotSubmitted rather than Started. Serialize transitions with commit or revalidate coherently at commit; narrowing mutant skips only that final recheck.",
          "pinned_blobs": [
            "git-blob:9758d2fe88491d17da265ad4eae55736670d6df7",
            "git-blob:be9f60e63f1b4e36006fb3424ee09a2429f5325e"
          ]
        }
      ],
      "severity": "bypass",
      "repeat-of": "rev1 note post-recheck-race-unexecuted / snapshot-coherence-followup",
      "reported_by": [
        "TASK-261007-3virnu"
      ]
    },
    {
      "id": "scheduled-checkin-regression-not-exercised",
      "row": "check-in tickets and warning",
      "invariant": "AC4-AC5 and Evidence That Counts: scheduled check-ins must be exercised through the real timer/continuation entry point, with fake time alone driving 30/60/120 minutes and the warning; a manually called helper does not establish runtime behavior.",
      "mechanism": "codex-rs/ext/goal/tests/background_wait.rs:884-971 is a synchronous #[test]. At :906 it calls require_claimed_ticket, whose definition at :69-90 manually calls claim_due_deadline, evaluate_continuation and check_admission. It manually calls note_turn_start and require_wait too. No CheckInClock, CheckInTimer or GoalRuntimeHandle is instantiated. Thus the newly added runtime.rs:568-580 callback and check_in_clock.rs:78-88 scheduler are outside this regression. The drop_check_in_registration mutant attacks state registration, not timer spawning or runtime re-entry. The required rework regression remains a simulation, while results/coverage claim actual scheduled firing. This is an observed coverage/attestation defect, not an assertion that the production scheduler has been executed and failed.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-uct3ql/static_attack.py (source embedded below)",
          "command": "python3 .temp/TASK-261007-uct3ql/static_attack.py scheduled-test",
          "expected_failure": "Observed exit 1: the exact candidate test uses synchronous manual state calls and does not exercise an injected clock, timer, or runtime continuation. Static pinned-source coverage reproduction only; no Rust test or runtime mutant was executed.",
          "candidate_tree": "3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214",
          "pinned_blobs": [
            "git-blob:38e3444d2446f7710aa98231c61284ac13429e1a",
            "git-blob:92f3f4c4f9f21461fbb229930470308b08f6b84f",
            "git-blob:1565f2015b557885d7c8ec717da87bae17ee6522"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "requested_regression": "Replace or supplement stalled_subscription_fires_scheduled_checkins with an enabled runtime fixture and injectable manual clock: initiate one real idle evaluation with an unchanged Armed receipt, advance fake time without manual evaluate/claim/admit calls, observe actual starts at 30/60/120, then exactly one warning and an active/wakeable goal. Retain the current state tests.",
      "requested_narrowing_mutant": "Keep BackgroundWaitState deadline registration intact but suppress the runtime Wait-arm spawn_check_in_timer call, or allow only its first spawn. The real scheduled regression must fail. NOT RUN in this panel; requires the serialized hosted lane. No new research leaf is needed.",
      "reported_by": [
        "TASK-261007-uct3ql"
      ]
    },
    {
      "id": "fired-timer-aborted-before-admission-reply",
      "row": "check-in tickets and warning",
      "invariant": "Scheduled check-ins must preserve the existing automatic-turn admission/accounting lifecycle; invalidating a consumed ticket must not cancel the admitted continuation before its Started reply is accounted.",
      "mechanism": "codex-rs/ext/goal/src/check_in_clock.rs:84-88 keeps the timer JoinHandle in the cancellable slot throughout on_fire().await. runtime.rs:574-582 runs continue_if_idle inside that same task. Its start_turn_if_idle awaits the Core reply (runtime.rs:688-700; core/src/session/mod.rs:1023), while the before-registration on_turn_start hook (extension.rs:248) invalidates state and aborts that slot (background_wait.rs:193-204; check_in_clock.rs:48-50). If cancellation is processed while the session callback awaits reconciliation, Core continues its already-queued turn, but the timer waiter drops before mark_goal_continuation at runtime.rs:700. The turn is not marked automatic for accounting.rs:219-228, so the existing empty-response guard can miss it. This is a new scheduler ownership regression, not proof that every check-in is lost.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3j9xpd/static_attack.py (full source in this outcome)",
          "command": "python3 .temp/TASK-261007-3j9xpd/static_attack.py timer-ownership",
          "expected_failure": "Executed exit 1: exact-source ownership/call-chain witness finds the fired task still cancellable while awaiting Core reply. Static only, not Rust/Tokio execution. Requested production regression: inject fake clock into GoalRuntimeHandle, latch the before-registration reconciliation after note_turn_start, process cancellation, finish Core start, and assert automatic-goal bookkeeping is recorded. Existing stalled_subscription_fires_scheduled_checkins never creates CheckInTimer.",
          "pinned_blobs": [
            "git-blob:38e3444d2446f7710aa98231c61284ac13429e1a",
            "git-blob:92f3f4c4f9f21461fbb229930470308b08f6b84f",
            "git-blob:8647c6005bf6131884dc395aa59914d1be4a2182",
            "git-blob:1272dcfbf6129a715e5053f5c79aff1f8b8339ea",
            "git-blob:8414dcfa10c4733b08f8cf7e55fbce6b5c2d700d",
            "git-blob:94c47023ead7ab1100ade55d75bb26f30d3c0c05",
            "git-blob:2a4707c2de74d96c1113beedf6972355b56db946",
            "git-blob:bb2b162ce0aee7bfee48f253708828508c5df858"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261007-3j9xpd"
      ]
    },
    {
      "id": "stale-timer-install-clobbers-current-registration",
      "row": "admission recheck and invalidation",
      "invariant": "AC4/AC9: invalidated or superseded waits cannot replace the live generation timer and prevent its fallback check-in.",
      "mechanism": "codex-rs/ext/goal/src/runtime.rs:656-659 captures generation, drops the goal permit, then installs a timer without validating the registration atomically with installation. check_in_clock.rs:82-88 unconditionally cancels the current slot. On a multithread executor A can be preempted after dropping the permit; invalidation increments generation, and B can evaluate/register/spawn the new generation deadline. A resumes and cancels B to install the old generation timer. At fire, background_wait.rs:380-395 rejects A against B’s newer registration; no timer is left for B, so a stalled subscription does not check in until another event arrives. Generation checks reject the stale callback but do not protect the current timer from stale installation.",
      "reproductions": [
        {
          "test_file": ".temp/TASK-261007-3j9xpd/static_attack.py (full source in this outcome)",
          "command": "python3 .temp/TASK-261007-3j9xpd/static_attack.py stale-install",
          "expected_failure": "Executed exit 1: source-pinned legal interleaving leaves registration=(1800,g1), slot=(1800,g0); g0 claim is false and g1 has no timer. Static interleaving witness, not Rust execution. Requested runtime latch after permit drop/before install: invalidate, install g1 through a second continuation, resume g0 install, advance fake clock, and assert g1 still fires. No existing hosted mutant exercises timer installation ordering.",
          "pinned_blobs": [
            "git-blob:38e3444d2446f7710aa98231c61284ac13429e1a",
            "git-blob:92f3f4c4f9f21461fbb229930470308b08f6b84f",
            "git-blob:8647c6005bf6131884dc395aa59914d1be4a2182"
          ]
        }
      ],
      "severity": "regression",
      "repeat-of": "none",
      "reported_by": [
        "TASK-261007-3j9xpd"
      ]
    }
  ],
  "notes": [
    "[TASK-261007-3virnu] {'id': 'execution-bound', 'text': 'Read-only replay and static attacks only. No builds, cargo, just, new Rust tests or executed runtime mutants. Hosted evidence is accepted from the attached precheck-3 report, not independently rerun or queried. Report supplies lane success and killed outcomes, not numeric command exit codes; these are not invented.'}",
    "[TASK-261007-3virnu] {'id': 'rework-and-coverage', 'text': 'Rev1 epoch reset removed; actual production timer spawning is now present. Nevertheless stalled_subscription_fires_scheduled_checkins at tests/background_wait.rs:884 is a synchronous state model invoking require_claimed_ticket/note_turn_start/require_wait manually; it neither instantiates CheckInTimer nor calls continue_if_idle. Reported 9/9 mutant kills cover state/helper and Core entry attacks, not end-to-end scheduled launches. drop_check_in_registration is listed killed by three state tests in the hosted report; the producer also claims stalled test, which the supplied kill table does not establish.'}",
    "[TASK-261007-3virnu] {'id': 'release-and-snapshot-bounds', 'text': 'note_release has no production caller in the candidate scope, only definition/tests; external control activation belongs to the subsequent slice. State empty reassessment tests do not prove a real late completion/release wake. Snapshot contents and revision are copied separately in pending_work.rs:51-65; coherent sampling needs a transition-during-read barrier test. No additional reproduced live failure claimed.'}",
    "[TASK-261007-3virnu] {'id': 'size-api-context', 'text': 'Full replay includes checkpointed E1 prerequisites: 28 files, 3583 insertions/40 deletions. Producer states E2 rev2 delta is 7 goal files +567/-26. Smallest corrective slice is timer ownership and admission commit race with real vertical regressions, not a generalized research chain. No new model context fragment is injected (contributor returns empty Vec), nor established breaking wire/config/rollout change. New internal NotSubmittedReason has exhaustive app-server handling.'}",
    "[TASK-261007-uct3ql] {'id': 'epoch-and-wiring-fix-present', 'text': 'The prior turn-start-resets-check-in-origin/checkin-epoch-reset-on-turn-start mechanism is corrected: background_wait.rs:480-484 only invalidates tickets and preserves epoch/count. Runtime :662-665 drops the goal permit before spawning the timer. Static epoch probe exited 0. The prior discarded-deadline implementation is replaced by a real spawn call. These source fixes are acknowledged; the finding concerns the required regression evidence, not a claim that either original source defect is unchanged.'}",
    "[TASK-261007-uct3ql] {'id': 'timer-self-cancellation-followup', 'text': 'Unexecuted concern, not a blocking finding: CheckInTimer keeps the fired callback task in its abort slot. A runtime callback awaits start_turn_if_idle; on_turn_start calls note_turn_start, whose installed hook aborts that slot. A real scheduled runtime test should verify turn-start cancellation does not cancel the awaiting continuation before mark_goal_continuation or strand lifecycle/accounting work. The direct state test cannot exercise this interaction. No behavioral failure was reproduced.'}",
    "[TASK-261007-uct3ql] {'id': 'snapshot-and-post-check-window', 'text': 'Retained unexecuted bound from rev1: pending_work.rs:51-64 takes receipt/mailbox snapshots separately and loads revision last; turn_input.rs:459-484 rechecks before asynchronous settings preparation and later task start. Existing tests exercise a transition before handle with a test-double checker, not a latch through the real BackgroundWaitState and admission/start window. Request a barrier-based test if this race is investigated; no failing behavior established by this panel.'}",
    "[TASK-261007-uct3ql] {'id': 'release-and-late-completion-bound', 'text': 'note_release still has no production caller in this preparatory stage. State tests show empty-snapshot reassessment and reset; core public handle tests show release/cancellation opens admission. They do not prove a production late-completion or release event wakes the runtime. Activation/control wiring is deferred to stage 2e and is not a new blocking finding here.'}",
    "[TASK-261007-uct3ql] {'id': 'evidence-provenance', 'text': 'Reused only attached precheck 3, which names the exact replayed tree and snapshot ce274182. Base run 37539907712 records success in app-server/small/lint/core; nine mutant runs record kills. Those hosted results are accepted as attached execution evidence, not rerun locally or independently fetched from GitHub. The truncated local CR log is not counted as proof of an unseen command. Attached producer reports local just fmt exit 1 (environmental stable/nightly setting mismatch); it is not presented as green.'}",
    "[TASK-261007-3j9xpd] Prior round 4/4 finding records checked: both epoch-reset IDs are fixed by note_turn_start retaining wait_started_at, confirmed by static fixed probe exit 0 and hosted reset_epoch_on_turn_start 37540019902. Both discarded-deadline IDs have production timer/claim/re-entry wiring now, confirmed by fixed probe; runtime ownership and concurrent installation are newly broken, not the old missing-registration mechanism. No repeat-of class carried forward.",
    "[TASK-261007-3j9xpd] Execution boundary: this panel ran no cargo, just, builds, Rust tests, or new hosted mutants. Reused attached TASK-260929-2snjbb_hosted-precheck-3.md: exact tree 3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214, snapshot ce274182, base run 37539907712 reports small/lint/core/app-server success and 9/9 killed mutants, 0 survivors. Provider job exit codes are not present in that summary; they are not fabricated here.",
    "[TASK-261007-3j9xpd] Coverage: 3/3 surface rows swept, 9/9 reported narrowing mutants killed; 0 tests in ext/goal/tests construct CheckInTimer or inject CheckInClock. stalled_subscription_fires_scheduled_checkins and invalidation_cancels_armed_check_in drive state/helper calls and a counter hook, not production timer/idle re-entry. drop_check_in_registration narrows state registration, not runtime spawning. Request real timer lifecycle/ordering regressions in this implementation leaf, not another research prerequisite.",
    "[TASK-261007-3j9xpd] Existing bounds retained: snapshot coherence across independent locks and post-Core-recheck async start window have no new runtime reproduction; do not infer they are safe from the sequential test-double latch-named test. note_release still has no production caller; external activation/release controls are stage 2e. Policy remains intentionally disabled by default; no missing-activation finding.",
    "[TASK-261007-3j9xpd] No new model-visible fragment: contributor returns an empty vector. No new breaking app-server wire/config/CLI/rollout change established. Rework is 7 files +567/-26 (285 logic plus 282 tests); base replay includes checkpointed E1 (+3583/-40 total) and is not the isolated E2 review size.",
    "[TASK-261007-3j9xpd] Tokio cancellation fact checked against official JoinHandle::abort documentation: https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html#method.abort. Abort targets the task attached to the handle; it is not limited to its initial sleep. Cancellation timing is schedule-dependent, hence the requested latch tests and explicit static-only witness limit."
  ],
  "surface_results": [
    {
      "row": "gate scope and fairness",
      "result": "held",
      "evidence": "Attached exact-tree precheck-3 base 37539907712 reports four lanes success. Core public-entry fairness tests listed in coverage map; overgate_non_goal_triggers 37539976644 killed by both; Armed-only 37539955446 and read-error 37540085008 killed. Static goal_admission gate restricts Automatic + goal. Held for these attacks, not a claim of complete runtime composition.",
      "reported_by": "TASK-261007-3virnu"
    },
    {
      "row": "check-in tickets and warning",
      "result": "broken",
      "findings": [
        "timer-aborts-own-admission"
      ],
      "evidence": "Static timer witness exit 1. State-model hosted reuse_ticket_id 37540043763, warning_repeats 37540106313, reset_epoch_on_turn_start 37540019902, drop_check_in_registration 37539932669 killed. They do not exercise the timer-task cancellation path.",
      "reported_by": "TASK-261007-3virnu"
    },
    {
      "row": "admission recheck and invalidation",
      "result": "broken",
      "findings": [
        "revision-recheck-before-await-window"
      ],
      "evidence": "Static ordering witness exit 1. Hosted skip_revision_recheck 37540065393 and preserve_ticket_across_invalidation 37539997698 killed. Existing core transition is sequential before handle, not AC7 latch after the last checker.",
      "reported_by": "TASK-261007-3virnu"
    }
  ],
  "free_hunt": [
    "[TASK-261007-3virnu] {\"budget_minutes\": 5, \"scope\": \"Timer ownership/cancellation, receipt snapshot coherence, lifecycle release/resume/disable, API/context and change size.\", \"result\": \"All three rows swept. Two static mechanisms elevated; snapshot coherence and external release/late wake remain bounded notes. No live behavioral reproduction claimed.\"}",
    "[TASK-261007-uct3ql] {\"budget_minutes\": 5, \"method\": \"Bounded static hunt after surface sweep; no builds or additional runtime executions.\", \"scope\": [\"timer callback/abort ownership\", \"snapshot coherence and post-check awaits\", \"release callers\", \"protocol/app-server/context surface\"], \"additional_blocking_findings\": [], \"notes\": [\"timer-self-cancellation-followup\", \"snapshot-and-post-check-window\", \"release-and-late-completion-bound\"], \"result\": \"No additional reproduced blocking mechanism. New NotSubmittedReason has an exhaustive app-server handling arm; no serialized API/config/rollout break established. TurnInputContributor returns an empty context-fragment vector.\"}",
    "[TASK-261007-3j9xpd] Bounded free hunt (5-minute ceiling): inspected runtime cancellation/registration ordering, timer ownership, semaphore drop, lifecycle callers, snapshot/recheck windows, context/wire exposure and delta size. Two scheduler regressions recorded in existing rows; no additional blocking mechanism. Existing snapshot/race/release limits remain notes."
  ]
}
```


## Recording reviewer attestation

# Recording review verification — TASK-260929-2snjbb revision 2

Verdict: changes_requested. Authoritative verdict: TASK-260929-2snjbb_review-verdict-rev2.md.

Recording-only scope per recording-brief-rev2.md. All three named panel outcomes were read; no new review, finding, code edit, build or runtime reproduction was performed. CR candidate tree: 3e27108f9d8ec8aaa0520e4619ea8ceb3a7cf214; repository_delta=present.

Merge audit: 5 of 5 panel finding records retained, including every original field and reproduction; merged reproduction records additionally carry blob pins. 15 of 15 notes retained. All 3 of 3 surface rows retained with worst panel result: gate scope and fairness held; check-in tickets and warning broken; admission recheck and invalidation broken. All three panel verdicts are changes_requested. Existing five finding IDs and repeat-of fields remain unchanged. No acceptance is authorized by these panel results.

CLI readiness: task-board --help exited 0, saved under .temp/recording-review-rev2/tool-readiness-01.log. All four resource downloads exited 0. task-board spawn goal reported no active goal for this run. Python merge verification exited 0 after allowing the merged reproduction records' additional blob pins; the initial exact-equality probe rejected those added fields and did not establish a lost finding.

## Input integrity

- `TASK-260929-2snjbb_review-verdict-rev2.md`: sha256 `2b1d84cd93a2ed03f929319132eb483022db0e2327d38eceff0fe5cc62fe6a38`
- `TASK-261007-3virnu_panel-verdict.md`: sha256 `227c812f373a3f7789f97c8560fe0e0a50a27f8207f82708a50bb854cfd398a2`
- `TASK-261007-uct3ql_panel-verdict.md`: sha256 `cd9c2020c478d5bfe5486a2c516c5ec8775330ae465c7d8f3593ba3a15603add`
- `TASK-261007-3j9xpd_panel-verdict.md`: sha256 `8edbe3aea0d64830074337879ecc3df61b88f2c9be262aa77236b08dd7526197`

## Logbook

2026-10-07: Recording reviewer confirmed complete union of three panels for rev2. Rework remains in this leaf: timer callback ownership, stale timer installation, late admission revision check, and real scheduled runtime regression coverage. Findings rely on panel-labelled static witnesses and attached hosted evidence; no live race reproduction is claimed by this recording run. Route to to-dev using the existing merged verdict.

Recording provenance: unchanged-byte reattachment was refused twice as change_request_evidence_missing; this appended attestation records this run’s merge verification without modifying any panel finding or surface verdict.
