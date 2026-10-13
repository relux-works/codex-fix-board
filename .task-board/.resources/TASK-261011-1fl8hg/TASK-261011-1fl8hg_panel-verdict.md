# Panel B verdict — TASK-260929-2is91w CR revision 3 (R141, non-recording)

Verdict: accept

Reviewer task: TASK-261011-1fl8hg. Change Request CR-TASK-260929-2is91w-3,
base e0eff057620104a416080da616256ee7f32bda1b, candidate
f8ae85582d54c47b237476e8d88742f942961f3f.

## Replay tree check

Replayed the CR patch on its base through a temporary index (never a nested
worktree). write-tree printed f8ae85582d54c47b237476e8d88742f942961f3f,
exactly the expected candidate tree. Match.

Commands run (all reads; no cargo, just, build, or test; no writes on
TASK-260929-2is91w):

- task-board m set_status(TASK-261011-1fl8hg, status=analysis) — exit 0
- task-board q get(TASK-260929-2is91w) projections (description/scope/ac,
  outcome+precondition resources, notes) — exit 0
- task-board resource get (surface-table.md, producer-brief.md, results.md,
  mutants.json, hosted-precheck-10.md, handoff-note-10.md, rev2 recorded
  verdict, rev3 validation log, rework-brief-review2, rev3 patch) — exit 0
- GIT_INDEX_FILE=temp.idx git read-tree e0eff057... — exit 0
- GIT_INDEX_FILE=temp.idx git apply --cached rev3.patch — exit 0
- GIT_INDEX_FILE=temp.idx git write-tree — exit 0, printed f8ae8558...
- git archive f8ae8558... (candidate file reads) — exit 0
- git diff-tree --stat/--numstat/--name-only (base..candidate and
  rev2-candidate..candidate) — exit 0
- git show (candidate sources) — exit 0
- git apply --check of each of the 13 mutant patches against the extracted
  candidate tree — exit 0 for all 13 (13 pass, 0 fail)
- gh api run/jobs/commit/log reads for hosted run 38142174620 — exit 0
  (one composite scan loop reported exit 1 from a trailing zero-match grep
  count; all 12 log fetches inside it returned data)

## One-word verdict

accept

## Verdict findings

```verdict-findings
{
  "findings": [],
  "notes": [
    "[TASK-261011-1fl8hg] Replay is exact: write-tree on base e0eff057 plus the rev3 patch prints f8ae85582d54c47b237476e8d88742f942961f3f. Candidate sources were read from that pinned tree with git show / git archive.",
    "[TASK-261011-1fl8hg] Hosted identity independently verified: run 38142174620 plan job records snapshot commit d772e5c0357c2ae4e00c2e207c16b4a122507f79, and the commit API reports its tree as f8ae85582d54c47b237476e8d88742f942961f3f, the reviewed candidate. The workflow head 9f8fdf9a is the dispatch head, not the tested tree. Overall run conclusion failure is expected: 13 mutant core jobs fail red while plan, lint, snapshot small, snapshot core and snapshot app-server are success.",
    "[TASK-261011-1fl8hg] All 13 mutant core jobs were mapped by their ci commit messages (mutant-1 discovery_ignores_call_pairing through mutant-13 stdin_counts_nested) and all 13 conclusions are failure, i.e. expected-red kills. Raw logs independently inspected for mutant-1 (exactly orphan_client_tool_search_output_does_not_count plus mismatched_call_id_tool_search_output_does_not_count fail, 3 attempts each), mutant-9 native_wait_ignores_discovered (exactly the 3 discovery tests fail, including the new integration test), mutant-7 native_mail_wait_ignores_policy (ack suite test fails) and mutant-13 stdin (code_mode plus nested_stdin fail). Remaining kills are accepted from the attached precheck-10 table plus independently checked job conclusions.",
    "[TASK-261011-1fl8hg] Snapshot core log shows 5119 tests, exactly 5115 plus the 4 new tests (3 orphan unit tests plus the real-search integration test). The new integration test discovered_native_wait_updates_waiting_capabilities PASSES on snapshot (4669/5119) and FAILS under native_wait_ignores_discovered, proving it observes the discovery transition rather than direct visibility. Precheck-9 red to precheck-10 green on the integration premise is further negative evidence that the test executes its assertions.",
    "[TASK-261011-1fl8hg] Rev2 findings A2-F1/D-F1 are closed by this revision: the pairing rule mirrors remove_orphan_outputs in the safe direction, the capture test records a call plus output pair and pins for_prompt survival, the real-search integration test asserts the paired output inside the outbound request plus a None to Some transition, and the 13th mutant is exactly the pairing narrowing, killed by exactly the 2 orphan tests on this tree.",
    "[TASK-261011-1fl8hg] Results-doc prose nit (no code impact): the results claim +276 insertions versus the precheck-8 tree, but git diff-tree --numstat ef4eb6ff..f8ae8558 measures +290/-26 (35/7 plus 121/19 plus 134/0). The file set matches and tree identity is verified independently, so this is a reporting error only.",
    "[TASK-261011-1fl8hg] Change size is 2254 insertions / 6 deletions across 21 files, exceeding the 800-line guidance; the 1461-line test module is the AC-mandated named-test matrix. No split was performed in this exact-tree revision. Recording reviewer should assess the size exception, as in rev2; no blocking finding is added here.",
    "[TASK-261011-1fl8hg] TurnContextContributionInput still gains a required public Rust field, source-breaking for out-of-tree struct-literal constructors. All in-repo constructors are updated and hosted lint on the exact tree is green. No app-server wire, CLI, config-schema, lockfile, rollout, or prompt-text change was found in the 21-file diff. Noted, non-blocking, same as rev2.",
    "[TASK-261011-1fl8hg] All board reads and the single outcome attach in this run target TASK-261011-1fl8hg. Nothing was accepted, rejected, status-changed, handed off, noted, or attached on TASK-260929-2is91w. No build or test command ran locally."
  ],
  "surface_results": [
    {
      "row": "flag derivation",
      "result": "held",
      "finding_ids": [],
      "attack": "Traced every conjunct (sleep, stdin, native_wait with provenance, exec_notify 4-way AND, native_mail_wait) against the final router plus thread-store markers, and verified every flag mutant dies on the exact candidate tree.",
      "evidence": "Candidate waiting_capabilities.rs:43-81 derive, :195-246 is_callable plus find_native_wait_agent, :255-299 notify_on_exit opt-in. The rev2 to rev3 production delta is pairing-only (verified 3-file diff), so all rev2 conjunct reasoning carries. Exact-tree run 38142174620: snapshot lint/small/core/app-server success; all 13 mutant core jobs failure (expected-red); mutant jobs mapped 1:1 by commit message; raw kill sets verified for the pairing, discovery, policy and stdin mutants.",
      "reported_by": "TASK-261011-1fl8hg"
    },
    {
      "row": "final-router derivation",
      "result": "held",
      "finding_ids": [],
      "attack": "Verified the A2-F1/D-F1 closure end to end: pairing rule versus normalizer orphan rule, orphan refusal unit tests, paired capture plus for_prompt diagnostic, real-search integration test with outbound-request pairing assertion, and the 13th narrowing mutant.",
      "evidence": "Pairing rule waiting_capabilities.rs:92-136 mirrors normalize.rs remove_orphan_outputs (remove iff Some call_id, non-server execution, unmatched call); the two strictness deltas (call must be earlier; None never counts) under-advertise only. Capture scans ordered raw_items at session/mod.rs:3971-3979. Orphan, mismatched and server unit tests; capture test records the call plus output pair and asserts for_prompt survival; suite discovered_native_wait_updates_waiting_capabilities drives a real search (request 1 hides wait_agent, request 2 input carries the paired multi_agent_v1.wait_agent output, captures go None to Some), PASSES on snapshot and FAILS under native_wait_ignores_discovered. Mutant discovery_ignores_call_pairing is exactly paired-equals-call_id.is_some() (patch text plus apply --check verified) and is killed by exactly the 2 orphan tests on this tree.",
      "reported_by": "TASK-261011-1fl8hg"
    },
    {
      "row": "subscriptions are not capabilities",
      "result": "held",
      "finding_ids": [],
      "attack": "Checked receipt and pending-work independence of every flag and proved the public user-turn ack test is live by watching it fail under the policy-dropping mutant.",
      "evidence": "Derive reads only host and policy markers (waiting_capabilities.rs:62-73); derivation inputs are router plus thread store plus discovered names. Mutant-7 native_mail_wait_ignores_policy raw log shows suite exec_notification acknowledged_subscription_does_not_flip_waiting_capabilities FAILED, while the same test PASSES in snapshot core (3506/5119). Synthetic pending_and_acknowledged_work_does_not_flip_flags is a listed killer for the same mutant.",
      "reported_by": "TASK-261011-1fl8hg"
    },
    {
      "row": "one snapshot, both paths",
      "result": "held",
      "finding_ids": [],
      "attack": "Followed single capture into StepContext ownership, both contribution inputs, and the installed goal contributor; checked the pointer-identity test on the exact tree.",
      "evidence": "Single derive stored on StepContext at session/mod.rs:3977-3998; both context paths borrow the same instance at :4315 and :4413; goal implements ContextContributor at ext/goal/src/extension.rs:616-630. same_snapshot_instance_reaches_both_context_paths PASSES in snapshot core. Session and goal files are untouched by the rev2 to rev3 delta. Residual, non-blocking and unchanged from rev2: installed-goal pointer identity is statically wired rather than independently exercised end to end.",
      "reported_by": "TASK-261011-1fl8hg"
    },
    {
      "row": "configuration coverage",
      "result": "not-attacked",
      "finding_ids": [],
      "reason": "Exact-tree legs cover sleep switches, headless markers, code-mode nesting and excluded receipt/exec tools (all in the snapshot-core PASS set or killer lists), but snapshot_follows_catalog_clock_support mutates an already resolved ModelInfo, bypassing remote catalog fetch and replacement. No execution on any tree chains a mocked remote catalog entry into a sampling snapshot. This is an entry-point coverage limitation, not the local-build prohibition.",
      "attack": "Compared the catalog test against ModelsManager apply_remote_models and final-router consumption; confirmed the 3-file rev3 delta and the 21-file CR add no remote-chained snapshot test.",
      "requested_attack": {
        "test_file": "codex-rs/core/tests/suite/search_tool.rs or a waiting-capabilities suite (requested)",
        "command": "just test -p codex-core -E test(remote_catalog_replacement_changes_waiting_snapshot)",
        "expected_failure": "Requested, NOT EXECUTED. Mock a remote catalog entry for a bundled slug that removes clock, plus the reverse control; capture the waiting snapshot in real sampling. A mutant ignoring remote replacement must fail; note such a mutant would live in models-manager code this CR does not touch."
      },
      "reported_by": "TASK-261011-1fl8hg"
    },
    {
      "row": "bounded and transient",
      "result": "held",
      "finding_ids": [],
      "attack": "Read the snapshot struct for shape, serialization and collections; traced heap ownership of the native name; checked turn conversion, prompt construction and the non-persistence tests on the exact tree.",
      "evidence": "Candidate ext/extension-api/src/waiting_capabilities.rs: 4 bools plus Option ToolName, derives Clone/Debug/Eq/PartialEq only, no serde, no collections. The V2 namespace 64-char config cap persists (config files are outside the 21-file diff). waiting_snapshot_does_not_persist_to_history_or_rollout PASSES in snapshot core; snapshot_stays_small_and_bounded is green in the small lane. Goal renders no fragments for any snapshot value (steering file untouched by the rev2 to rev3 delta); no prompt text, template, history or rollout shape changed.",
      "reported_by": "TASK-261011-1fl8hg"
    },
    {
      "row": "API surface and placement",
      "result": "held",
      "finding_ids": [],
      "attack": "Checked public constructor changes, dependency direction, module placement, the staged plan-signal replacement and build wiring across the full 21-file diff.",
      "evidence": "The rev2 to rev3 delta touches none of the API files. One extension-api snapshot type plus one borrowed contributor field; goal consumes the type through existing contributor registration; no core to goal dependency (Cargo manifests untouched; full name list verified: only core session/tools, extension-api, goal and tests). update_plan_enabled call sites unchanged (runtime.rs outside the CR; steering.rs untouched in delta), so the staged replacement to TASK-260929-1w5ivu holds with zero behavior loss. No Bazel, schema, template, CI or docs changes.",
      "reported_by": "TASK-261011-1fl8hg"
    }
  ],
  "free_hunt": [
    "[TASK-261011-1fl8hg] {area: pairing strictness deltas, outcome: dismissed} Call-must-be-earlier and None-never-counts both under-advertise only: a genuinely delivered tool could read false, but an undelivered tool can never read true. History is append-ordered (call then output) and resume/fork replays in order; no history rewrite exists in this leaf, so output-before-call has no realistic trigger. None call_id outputs carrying wait specs are degenerate (the server positive control uses Some). Safe direction, documented in code.",
    "[TASK-261011-1fl8hg] {area: duplicate call ids across searches, outcome: dismissed} calls is a set and discovered is a set of names, so a repeated call id can only re-add an already counted name; pairing existence is monotone and order-stable. No double-count or cross-search leak shape.",
    "[TASK-261011-1fl8hg] {area: non-client non-server execution values, outcome: dismissed} Candidate counts iff execution equals server or the call is paired; the normalizer removes iff execution differs from server and the call is missing. The two rules agree on every Some call_id row; they differ only on None, which is the documented safe-direction delta above.",
    "[TASK-261011-1fl8hg] {area: integration second-turn premise, outcome: held} The changed approval policy reruns contributors for the post-discovery sample; first-equals-None plus last-equals-Some is robust to mid-turn reruns because recording is append-ordered. The ignores-discovered kill proves the Some flows through the discovery path, not direct visibility.",
    "[TASK-261011-1fl8hg] {area: skip_if_no_network on the new integration test, outcome: dismissed} The test demonstrably ran: PASS in snapshot core and kills in the ignores-discovered mutant job. No skip occurred on the evidence path.",
    "[TASK-261011-1fl8hg] {area: orphan diagnostic never ran red, outcome: noted} The for_prompt diagnostic was added together with the paired fix, so its tripwire property is established statically (normalizer code path plus the existing should_panic orphan test) rather than by a red run. The 13th mutant kill on the exact tree supplies the executed negative proof for the pairing rule itself.",
    "[TASK-261011-1fl8hg] {coverage: 7/7 rows swept once (6 held, 1 not-attacked), 13/13 mutant patches apply --check clean, 13/13 mutant core jobs confirmed failure with 1:1 name mapping, 4 raw mutant logs plus snapshot core log inspected, 0 local builds or tests, 0 findings, verdict accept}"
  ]
}
```
