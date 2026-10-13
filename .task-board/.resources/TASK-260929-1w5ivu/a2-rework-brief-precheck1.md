# TASK-260929-1w5ivu (P3-2): hosted precheck 1 is red. Fix 4 waiting_guidance suite tests, then request precheck 2

Precheck 1: run 38223961011 on tree `907fa97b499fbd66e5f784792667cab98b5ed76a`, filter
`test(waiting) | test(guidance) | test(continuation) | test(goal)`.
- lint, small and app-server are green.
- core is red: 4 tests in `core/tests/suite/waiting_guidance.rs` fail on all 3 tries, so they are deterministic, not flakes.
- `suite::hooks::permission_request_hook_allows_exec_command_without_user_approval` failed once and passed on retry. It is
  a base flake; ignore it.
- All 7 mutant lanes failed. That proves nothing while the snapshot itself is red, so re-establish every kill at precheck 2.

You cannot run tests on the mini, which is why each expectation below must be justified from the code. In the results,
for every changed expectation, cite the `file:line` that decides it. Another blind CI round costs about 35 minutes.

## F1 `waiting_guidance_post_create_carries_fragment_matching_tools` (line 354)

`assert!(request.tool_by_name("clock", "sleep").is_none())` fails inside the `requests[..2]` loop. `assert_no_fragment`
passed on the same request just before, so this request has the sleep tool but no fragment. That is exactly the AC6
disagreement this leaf exists to prevent.
- The most likely request is `requests[1]`, the sampling request right after `create_goal` in turn 1.
- ModelDriven sleep exposure follows goal activity (`core/src/tools/spec_plan.rs:1259-1268`:
  `model_has_clock || context.goal_activity_present`). Once the goal exists, `clock.sleep` is advertised on the next
  request, while the fragment is still suppressed (the "creation deferral" the test comment relies on).
- AC5 also says the post-create next sampling request carries the fragment.

Required: the fragment and the request's tools must agree on every request, including the one right after
`create_goal`. Prefer gating the fragment on the same goal-activity signal that tool planning uses for that step, so
`requests[1..]` carry it, rather than keeping the deferral. Do not change tool exposure in this leaf. If you find
`requests[0]` is the failing one instead, explain why with code references and fix accordingly. Update the test so it
asserts per request that `SLEEP_MARKER` count == `tool_by_name("clock","sleep").is_some() as usize`, plus the exact
expected split.

## F2 `waiting_guidance_code_mode_omits_sleep_sentence` (line 414)

The fragment carries the sleep sentence (count 1, expected 0). The snapshot's `sleep` is
`is_callable(router, model_visible_specs, ..., clock.sleep)` (`core/src/tools/waiting_capabilities.rs:49`), so the
sentence means `clock.sleep` was callable as a direct tool in that request. The test premise is likely wrong:
- `configure` switches the model to `test-gpt-5.1-codex` after the fixture's `with_model_info_override("gpt-5.5", ...)`.
  The clock strip therefore does not apply, and `model_has_clock` may be true.
- Check whether code mode keeps `clock.sleep` direct (its exposure) for that model.

Fix the setup so that sleep is reachable only as a nested code-mode tool, for example by stripping `clock` from the
model actually used, or by using `with_model_info_override` for the code-mode slug. Then assert that the request has no
direct sleep tool AND no sleep sentence. If code mode can never hide `clock.sleep` here, say so with references and turn
the case into an agreement assertion. Do not weaken it to "no assertion".

## F3 `waiting_guidance_headless_host_gives_negative_exec_sentence` (line 624) and `..._unchanged_capabilities_stable_across_sampling_steps` (line 698)

Both fail on `NATIVE_WAIT_MARKER` count 0 (expected 1). Under the default fixture (gpt-5.5, no extra features), the
snapshot's `native_wait` is `None`, so the native agent wait tool is not callable there. Two possible reasons:
- `router.native_wait_tool()` returns nothing because the multi-agent tool is not registered by default;
- it is deferred behind tool search and not discovered (`find_native_wait_agent`, `waiting_capabilities.rs:245-253`).

Determine which. Then either enable what registers `multi_agent_v1.wait_agent` directly in these fixtures (and keep the
tool-presence asserts), or change the expectations to the absent case (no native sentence AND `wait_agent` absent from
the request). The `requests[2..]` loop of F1 expects the native wait sentence too; it is masked by F1 and will hit the
same issue. Apply the same decision there.

## Keep

- AC1–AC10 as set on the task. Fixes stay in test code unless F1 needs the contributor gate change in `ext/goal`.
- No new code in codex-core.
- Every mutant in `p3/a2-mutants-1.json` must still apply to the final tree and be killed by a named, filter-selected
  test. If a fix moves the killing assertion, update the mutant notes.
- Report the changed-line count again (it was 1270 against the 600 target). Do not grow it without need.
- `mini-producer-addendum.md` applies: `cargo fmt -- --config imports_granularity=Item`, then `--check` exit 0; no other
  cargo; no CODEX_HOME copies; delete temp dirs.
- Leave everything UNCOMMITTED, report the final tree id after fmt, add the note
  `HOSTED-PRECHECK-REQUESTED: precheck 2`, and end your turn without handing off.
