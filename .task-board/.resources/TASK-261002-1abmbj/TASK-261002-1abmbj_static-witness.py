"""Bounded immutable-source witness, not a Rust execution or runtime test."""
import subprocess
import sys

TREE = 'd401bcff58f9724a36966053dde5386be1af7882'
EXPECTED = {
    'api.rs': 'a4512db548378bcdf499cd47eca670d366a8f9a3',
    'runtime.rs': '87849af544305d6d8897a382e62a746d9f6d4e8e',
    'extension.rs': '153d947f523890868dac9554c9a84393800f4869',
}
sources = {}
for name, expected in EXPECTED.items():
    ref = f'{TREE}:codex-rs/ext/goal/src/{name}'
    oid = subprocess.check_output(['git', 'rev-parse', ref], text=True).strip()
    assert oid == expected, (name, oid)
    sources[name] = subprocess.check_output(['git', 'show', ref], text=True)

api = sources['api.rs'].split('pub async fn set_thread_goal(', 1)[1].split('pub async fn clear_thread_goal(', 1)[0]
before_publish = api.split('.reconcile_live_activity(permit)', 1)[0]
assert before_publish.count('.get_thread_goal(thread_id)') == 2
assert before_publish.count('failed to read thread goal: {err}') == 2
assert '})?;' in before_publish
assert 'revoke_activity_on_read_failure' not in before_publish
assert '.reconcile_live_activity' not in before_publish
assert 'failed to prepare external goal mutation: {err}' in before_publish
runtime = sources['runtime.rs']
metrics = runtime.split('async fn current_goal_status_for_metrics(', 1)[1]
assert '.get_thread_goal(self.thread_id())' in metrics
assert '.map_err(|err| err.to_string())?;' in metrics
locked = runtime.split('async fn account_active_goal_progress_locked(', 1)[1].split('async fn account_idle_goal_progress(', 1)[0]
assert locked.index('.current_goal_status_for_metrics(') < locked.index('.reconcile_live_activity(permit)')
tool = sources['extension.rs'].split('fn on_tool_finish', 1)[1].split('impl<C> ToolContributor', 1)[0]
error_arm = tool.split('Err(err) => {', 1)[1].split('};', 1)[0]
assert 'failed to account active goal progress after tool finish' in error_arm
assert 'return;' in error_arm
assert 'revoke_activity_on_read_failure' not in error_arm
assert 'reconcile_activity' not in error_arm
print('Pinned candidate blobs verified. Static failure paths:')
print('1. GoalService::set_thread_goal: preparation failure is warn-only; either get_thread_goal error returns via ? before the sole post-read reconciliation. Known marker has no removal/Unknown publication on that path.')
print('2. on_tool_finish: successful leading reconciliation can be followed by accounting metrics read failure; Err arm warns and returns without publication. This needs a failure between reads; not dynamically executed here.')
print('EXPECTED RED: AC7/rework every-read-failure revocation is not structurally satisfied. This is a source control-flow witness, not proof of a runtime fault injection.')
sys.exit(1)
