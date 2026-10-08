"""Pinned-source control-flow witness; no builds and no runtime simulation."""
import subprocess
import sys
TREE = 'd401bcff58f9724a36966053dde5386be1af7882'
def source(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)
a = source('codex-rs/ext/goal/src/api.rs')
r = source('codex-rs/ext/goal/src/runtime.rs')
e = source('codex-rs/ext/goal/src/extension.rs')
set_body = a.split('pub async fn set_thread_goal(', 1)[1].split('pub async fn clear_thread_goal(', 1)[0]
before_publish = set_body.split('.reconcile_live_activity(permit)', 1)[0]
assert 'failed to prepare external goal mutation' in before_publish
assert before_publish.count('.get_thread_goal(thread_id)') == 2
assert 'failed to read thread goal: {err}' in before_publish
assert '})?;' in before_publish
assert 'revoke_activity_on_read_failure' not in before_publish
flush = a.split('pub async fn flush_thread_goal_progress_for_fork(', 1)[1].split('pub async fn get_thread_goal(', 1)[0]
assert '.prepare_external_goal_mutation_locked(&goal_state_permit)' in flush
assert '.map_err(GoalServiceError::Internal)' in flush
assert 'reconcile' not in flush and 'revoke' not in flush
account = r.split('async fn account_active_goal_progress_locked(', 1)[1].split('async fn account_idle_goal_progress(', 1)[0]
assert account.index('.current_goal_status_for_metrics(') < account.index('.reconcile_live_activity(permit)')
metrics = r.split('async fn current_goal_status_for_metrics(', 1)[1]
assert '.get_thread_goal(self.thread_id())' in metrics
assert '.map_err(|err| err.to_string())?;' in metrics
finish = e.split('fn on_tool_finish', 1)[1].split('impl<C> ToolContributor', 1)[0]
error = finish.split('Ok(None) => return,', 1)[1].split('let goal = progress.goal;', 1)[0]
assert error.index('return;') < error.index('.reconcile_activity(')
assert 'revoke_activity_on_read_failure' not in error
print('FAIL: set/fork accounting reads can propagate before Unknown/removal; tool-finish also has an unrevoked post-reconcile read-error exit.')
print('Static control-flow evidence only; runtime regressions not executed.')
sys.exit(1)
