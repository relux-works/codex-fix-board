import json
import re
import subprocess
import sys
from pathlib import Path
import yaml

TREE = 'f38084559bf0a082e724b5daf3edc5bed6981026'
def source(path):
    return subprocess.check_output(['git', 'show', f'{TREE}:{path}'], text=True)
text = source('.github/workflows/relux-ci.yml')
w = yaml.safe_load(text)
steps = w['jobs']['lanes']['steps']
mode = sys.argv[1]
if mode == 'safety':
    events = w.get('on', w.get(True))
    assert set(events) == {'workflow_dispatch', 'push'}
    assert events['push'] == {'branches': ['ci/relux-ci-selftest/**']}
    assert w['permissions'] == {'contents': 'read'}
    assert set(w['jobs']) == {'lanes'}
    assert w['jobs']['lanes']['runs-on'] == 'ubuntu-24.04'
    assert 'permissions' not in w['jobs']['lanes']
    all_steps = steps.copy()
    for path in ['.github/actions/setup-ci/action.yml', '.github/actions/setup-rusty-v8/action.yml']:
        all_steps += yaml.safe_load(source(path))['runs']['steps']
    pins = [s['uses'] for s in all_steps if 'uses' in s and not s['uses'].startswith('./')]
    assert all(re.fullmatch(r'[^@]+@[0-9a-f]{40}', p) for p in pins)
    assert 'secrets.' not in text
    assert all(not re.search(r'\$\{\{[^}]*(?:inputs|github)\.', s.get('run', '')) for s in all_steps)
    print(json.dumps({'events': list(events), 'permissions': w['permissions'], 'runner': w['jobs']['lanes']['runs-on'], 'pinned_action_sites': len(pins), 'untrusted_run_interpolations': 0}, indent=2))
elif mode == 'concurrency':
    expr = w['concurrency']['group']
    # Evaluate only the exact string-or expression present in the candidate, not arbitrary Actions syntax.
    def group(context):
        def substitute(m):
            names = [n.strip() for n in m.group(1).split('||')]
            assert all(re.fullmatch(r'(inputs|github)\.[a-z_]+', n) for n in names)
            return next((context.get(n, '') for n in names if context.get(n, '')), '')
        return re.sub(r'\$\{\{(.*?)\}\}', substitute, expr)
    sha_a = '7ae33a059056dad776bd0b81fb2b4883615b9b5a'
    sha_b = '35af013b901ed4be1b88416068f140e9ca5cc85d'
    ref = 'refs/heads/ci/relux-ci-selftest/stack-2'
    witnesses = [
        {'event': 'push', 'github.sha': sha_a, 'github.ref': ref},
        {'event': 'push', 'github.sha': sha_b, 'github.ref': ref},
        {'event': 'workflow_dispatch', 'inputs.sha': sha_a, 'github.ref': ref},
    ]
    for c in witnesses:
        c['group'] = group(c)
    print(json.dumps({'expression': expr, 'cancel-in-progress': w['concurrency']['cancel-in-progress'], 'witnesses': witnesses}, indent=2))
    if witnesses[0]['group'] == witnesses[1]['group']:
        print('FAIL per-SHA isolation: distinct push SHAs share a cancellation group')
        sys.exit(1)
elif mode == 'lanes':
    assert set(w['jobs']['lanes']['strategy']['matrix']['lane']) == {'lint', 'small', 'core', 'app-server'}
    byname = {s.get('name'): s for s in steps}
    mapping = {'Lint (fmt + clippy)': 'lint', 'Small crates tests': 'small', 'codex-core tests': 'core', 'codex-app-server tests': 'app-server'}
    for name, lane in mapping.items():
        s = byname[name]
        assert s['if'] == f"matrix.lane == '{lane}'"
        assert not s.get('continue-on-error')
        assert '||' not in s['run'] and 'exit 0' not in s['run']
    assert not w['jobs']['lanes'].get('continue-on-error')
    helpers = byname['Helper binaries for integration tests']
    assert helpers['if'] == "matrix.lane == 'core' || matrix.lane == 'app-server'"
    assert steps.index(helpers) < steps.index(byname['codex-core tests']) < steps.index(byname['codex-app-server tests'])
    expected = {'test_stdio_server', 'test_streamable_http_server', 'codex-execve-wrapper', 'codex-app-server', 'codex-app-server-test-notify-capture', 'exec-server', 'codex-code-mode-host', 'codex', 'codex-exec', 'codex-linux-sandbox'}
    assert set(re.findall(r'--bin (\S+)', helpers['run'])) == expected
    four = {'codex-tools', 'codex-goal-extension', 'codex-extension-api', 'codex-rollout-trace'}
    assert set(re.findall(r'-p (\S+)', byname['Small crates tests']['run'])) == four
    assert set(re.findall(r'-p (\S+)', byname['Lint (fmt + clippy)']['run'])) == four | {'codex-core', 'codex-app-server'}
    core = byname['codex-core tests']['run']
    excluded = ['suite::skill_approval::shell_zsh_fork_skill_scripts_ignore_declared_permissions', 'suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_guardian_reviews_persistent_terminal_in_current_turn', 'suite::unified_exec_zsh_fork_approvals::unified_exec_zsh_fork_parent_approval_preserves_denied_reads']
    expected_core = 'INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-core -E \'not ( ' + ' | '.join(f'test(={n})' for n in excluded) + ")'"
    assert ' '.join(core.split()) == expected_core
    assert byname['codex-app-server tests']['run'] == 'INSTA_WORKSPACE_ROOT="$PWD" just test -p codex-app-server'
    assert w['env']['NEXTEST_RETRIES'] == '2'
    hosted = json.loads(Path('.temp/TASK-261002-umkkoj/hosted-run.json').read_text())
    assert hosted['headSha'] == '7ae33a059056dad776bd0b81fb2b4883615b9b5a'
    assert hosted['conclusion'] == 'success' and hosted['status'] == 'completed'
    assert {j['name'] for j in hosted['jobs']} == {'lint', 'small', 'core', 'app-server'}
    assert all(j['conclusion'] == 'success' for j in hosted['jobs'])
    for name, lane in mapping.items():
        job = next(j for j in hosted['jobs'] if j['name'] == lane)
        assert next(s for s in job['steps'] if s['name'] == name)['conclusion'] == 'success'
    print(json.dumps({'lanes': mapping, 'helpers': sorted(expected), 'explicit_exclusions': excluded, 'hosted_head': hosted['headSha'], 'green_hosted_lanes': 4}, indent=2))
else:
    raise SystemExit('unknown mode')
