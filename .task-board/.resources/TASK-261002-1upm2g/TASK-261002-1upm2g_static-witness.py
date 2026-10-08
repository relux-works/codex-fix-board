import subprocess
import sys

TREE = 'd401bcff58f9724a36966053dde5386be1af7882'
def source(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)
def between(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]

runtime = source('codex-rs/ext/goal/src/runtime.rs')
extension = source('codex-rs/ext/goal/src/extension.rs')
api = source('codex-rs/ext/goal/src/api.rs')
processor = source('codex-rs/app-server/src/request_processors/thread_processor.rs')
accounting = between(runtime, 'async fn account_active_goal_progress_locked(', 'async fn account_idle_goal_progress(')
metrics = between(runtime, 'async fn current_goal_status_for_metrics(', '\n}')
prepare = between(runtime, 'async fn prepare_external_goal_mutation_locked(', 'pub async fn apply_external_goal_set(')
flush = between(api, 'pub async fn flush_thread_goal_progress_for_fork(', 'pub async fn get_thread_goal(')
tool_finish = between(extension, 'fn on_tool_finish', '\nimpl<C> ToolContributor')
error_exit = between(tool_finish, 'Err(err) => {', '\n            };')
assert '.get_thread_goal(self.thread_id())' in metrics
assert '.map_err(|err| err.to_string())?;' in metrics
assert '.current_goal_status_for_metrics(Some(snapshot.expected_goal_id.as_str()))\n            .await?;' in accounting
assert accounting.index('.await?;') < accounting.index('self.reconcile_live_activity(permit).await?;')
assert 'revoke_activity_on_read_failure' not in accounting + metrics + prepare + flush
assert '.account_active_goal_progress_locked(' in prepare and '.await?;' in prepare
assert '.prepare_external_goal_mutation_locked(&goal_state_permit)' in flush
assert '.map_err(GoalServiceError::Internal)' in flush
assert '.flush_goal_progress_for_fork(source_thread_id)' in processor
assert 'failed to flush source thread goal' in processor
assert '.reconcile_activity(input.thread_store, &permit)' in tool_finish
assert '.account_active_goal_progress(' in tool_finish
assert 'return;' in error_exit
assert 'revoke_activity_on_read_failure' not in error_exit
assert 'reconcile' not in error_exit
print('Expected-red STATIC witness: fork flush -> prepare -> progress accounting -> metrics get_thread_goal error propagates without Unknown/removal publication.')
print('Expected-red STATIC witness: successful initial on_tool_finish reconcile -> later metrics read error -> warn/return bypasses post-account reconcile and preserves prior marker.')
print('This checks immutable Rust source/control-flow prerequisites. No Rust runtime execution or fault injection is claimed.')
sys.exit(1)
