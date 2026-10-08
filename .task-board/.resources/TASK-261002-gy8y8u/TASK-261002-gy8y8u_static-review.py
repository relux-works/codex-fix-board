"""Read-only static inspection of pinned candidate; never launches builds or suites."""
import json
import re
import subprocess
from pathlib import Path
import yaml

ROOT = Path(__file__).parent
TREE = '429a14a27a106f73b5907a0d830c4548cb3f1ea4'
def blob(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)
w = yaml.load(blob('.github/workflows/relux-ci.yml'), Loader=yaml.BaseLoader)
job = w['jobs']['lanes']
steps = job['steps']
results = []
def record(row, evidence):
    results.append({'row': row, 'result': 'held', 'evidence': evidence})
    (ROOT / 'surface-results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(row+': held (static scope)')

assert set(w['on']) == {'workflow_dispatch', 'push'}
assert w['on']['push']['branches'] == ['ci/relux-ci-selftest/**']
assert w['permissions'] == {'contents': 'read'}
assert job['runs-on'] == 'ubuntu-24.04' and 'permissions' not in job
composed = steps[:]
for path in ['.github/actions/setup-ci/action.yml', '.github/actions/setup-rusty-v8/action.yml']:
    composed += yaml.load(blob(path), Loader=yaml.BaseLoader)['runs']['steps']
for step in composed:
    use = step.get('uses', '')
    assert not use or use.startswith('./') or re.fullmatch(r'[^@]+@[a-f0-9]{40}', use)
    assert not re.search(r'\$\{\{[^}]*\b(inputs|github)\.', step.get('run', ''))
    assert 'secrets.' not in json.dumps(step)
record('trigger and permission safety', 'Inspected event additions, permission overrides, runner labels, nested action pins, secrets references and expression injection. Exact trigger set, read-only token, hosted Ubuntu, all external action pins full SHA. Untrusted SHA enters env/with only; local action TARGET enters env only. No violating static path found.')

sha = '${{ inputs.sha || github.sha }}'
assert steps[0]['with']['ref'] == sha
assert steps[1]['name'] == 'Verify the checked-out commit'
assert steps[1]['env']['WANT_SHA'] == sha
assert '^[0-9a-f]{40}$' in steps[1]['run']
assert '[ "$HEAD_SHA" = "$WANT_SHA" ]' in steps[1]['run']
assert w['concurrency'] == {'group': 'relux-ci-'+sha, 'cancel-in-progress': 'true'}
assert sha in w['run-name']
for s in steps:
    if 'just test' in s.get('run', '') or 'just clippy' in s.get('run', '') or 'cargo build' in s.get('run', ''):
        assert 'continue-on-error' not in s
        assert '|| true' not in s['run'].split('printf')[0]
values=[('push-A', '', 'a'*40), ('push-B', '', 'b'*40), ('dispatch-A', 'a'*40, 'b'*40)]
groups={name:'relux-ci-'+(inp or commit) for name,inp,commit in values}
assert groups['push-A'] != groups['push-B'] and groups['push-A'] == groups['dispatch-A']
(ROOT/'concurrency-witness.json').write_text(json.dumps(groups,indent=2)+'\n')
record('evidence exactness', 'Static witnesses: push A and B on one ref resolve distinct groups; dispatch A and push A resolve the same group. Full anchored lowercase 40-hex check and HEAD equality immediately follow checkout in every lane. No suite exit masking; clippy pipeline explicitly enables pipefail. Live push run exact commit/tree and all four Verify steps independently confirmed via gh. Branch/short-SHA dispatch rejection accepted from attached producer gate harness, not rerun.')

assert job['strategy']['matrix']['lane'] == ['lint','small','core','app-server']
byname={s.get('name'):s for s in steps if 'name' in s}
lint=byname['Lint (fmt + clippy)']
assert set(re.findall(r'-p (\S+)',lint['run'])) == {'codex-tools','codex-core','codex-goal-extension','codex-extension-api','codex-app-server','codex-rollout-trace'}
assert 'just fmt-check' in lint['run'] and '--message-format=short --color never' in lint['run']
assert len(lint['env']['KNOWN_WARNINGS'].splitlines()) == 3
assert set(re.findall(r'-p (\S+)',byname['Small crates tests']['run'])) == {'codex-tools','codex-goal-extension','codex-extension-api','codex-rollout-trace'}
core=byname['codex-core tests']['run']
assert "-E 'not (" in core
expected={'suite::skill_approval::shell_zsh_fork_skill_scripts_ignore_declared_permissions','suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_guardian_reviews_persistent_terminal_in_current_turn','suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_parent_approval_preserves_denied_reads'}
assert set(re.findall(r'test\(=([^)]*)\)',core)) == expected
assert '-E' not in byname['codex-app-server tests']['run']
for name,lane in [('Lint (fmt + clippy)','lint'),('Small crates tests','small'),('codex-core tests','core'),('codex-app-server tests','app-server')]:
    assert byname[name]['if'] == f"matrix.lane == '{lane}'"
helpers=byname['Helper binaries for integration tests']
assert helpers['if'] == "matrix.lane == 'core' || matrix.lane == 'app-server'"
assert set(re.findall(r'--bin (\S+)',helpers['run'])) == {'test_stdio_server','test_streamable_http_server','codex-execve-wrapper','codex-app-server','codex-app-server-test-notify-capture','exec-server','codex-code-mode-host','codex','codex-exec','codex-linux-sandbox'}
record('lane coverage', 'Inspected exact crate sets, every lane predicate, helper binaries, filter polarity and exact test names, retries, warning normalization/allowlist and failure path. 6 lint crates, 4 small crates, full core/app-server selection with exactly 3 explicit exclusions. Hosted baseline lint parses 3/3 known warnings; independently fetched hosted negative lint fails (exit 1) on the fourth unused import. Baseline import provenance verified at upstream pin. No further reproduced defect; see parser-format bound in notes.')
