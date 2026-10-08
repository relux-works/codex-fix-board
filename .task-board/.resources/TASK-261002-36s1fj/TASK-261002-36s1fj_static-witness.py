import subprocess
import sys

tree = "4d289590739432aa55c2a3868c2b4a5472b07c92"
paths = {
    "runtime": "codex-rs/ext/goal/src/runtime.rs",
    "extension": "codex-rs/ext/goal/src/extension.rs",
}
expected_blobs = {
    "runtime": "625003a79fbdd9bb54f9287d1b800e2162636097",
    "extension": "b3070a3a4ad155a6a0525980adec4042648c91f5",
}
sources = {}
for name, path in paths.items():
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{tree}:{path}"], text=True
    ).strip()
    if blob != expected_blobs[name]:
        raise RuntimeError(f"unexpected candidate blob: {path}")
    sources[name] = subprocess.check_output(
        ["git", "show", f"{tree}:{path}"], text=True
    )

runtime = sources["runtime"]
extension = sources["extension"]
active_accounting = runtime.split("async fn account_active_goal_progress_locked(", 1)[1]
active_accounting = active_accounting.split("async fn account_idle_goal_progress(", 1)[0]
metrics_read = runtime.split("async fn current_goal_status_for_metrics(", 1)[1]
abort_hook = extension.split("fn on_turn_abort", 1)[1].split("fn on_turn_error", 1)[0]

if ".get_thread_goal(self.thread_id())" not in metrics_read:
    raise RuntimeError("metrics read path changed; re-review required")
if ".map_err(|err| err.to_string())?;" not in metrics_read:
    raise RuntimeError("metrics error propagation changed; re-review required")
before_publication = active_accounting.split("self.reconcile_live_activity(permit).await?;", 1)[0]
if ".current_goal_status_for_metrics(Some(snapshot.expected_goal_id.as_str()))\n            .await?;" not in before_publication:
    raise RuntimeError("accounting path changed; re-review required")
if ".account_active_goal_progress(" not in abort_hook or "return;" not in abort_hook:
    raise RuntimeError("abort caller changed; re-review required")
if any(token in before_publication + metrics_read + abort_hook for token in (
    "reconcile_activity(", "clear_activity(", "remove::<GoalActivity>", ".publish(",
)):
    raise RuntimeError("a failure revocation path appeared; re-review required")

print("STATIC CONTROL-FLOW WITNESS ONLY; no Rust execution or runtime simulation")
print(f"candidate tree: {tree}")
print("on_turn_abort -> account_active_goal_progress -> account_active_goal_progress_locked")
print("current_goal_status_for_metrics -> get_thread_goal -> Err propagated by ?")
print("The Err skips reconcile_live_activity; the abort hook warns and returns without revocation.")
print("FAIL: this read-error path cannot reach the publisher's Unknown/removal branch.")
sys.exit(1)
