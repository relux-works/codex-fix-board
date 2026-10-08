# TASK-261002-3ksr2m — R141 panel B: P1 astra snapshot refresh, revision 1

accept

## Replay and scope

CR-TASK-261002-ifa91r-1 replay through a separate temporary Git index produced **5c365d9a68ea6d2cee0488eb58a37a539ce354d4**, exactly the expected candidate tree, from base **35af013b901ed4be1b88416068f140e9ca5cc85d**. No nested worktree, build, commit, real-index mutation, or source edit occurred. No write of any kind was made on TASK-261002-ifa91r — p1-astra-snapshot-refresh.

Decision: whether the supplied snapshot-only revision is acceptable to the recording reviewer. Frozen precondition: the patch/base/tree and one-row surface table in the panel brief; grammar not applicable. Budget: 20 minutes, including packaging; free hunt bounded to 2 minutes; one outcome under 32 KiB; no serial prerequisite. Exit: replay, every row classified, bounded free hunt and persisted verdict. Consumer: orchestrator/recording reviewer for this existing CR, not a new implementation or research leaf.

## Commands and real exit codes

Commands were direct processes, without tee. Paths below are relative to the Story worktree unless absolute.

| Command | Exit | Evidence |
|---|---:|---|
| `task-board m 'set_status(TASK-261002-3ksr2m, status=analysis)'` | 0 | Own lifecycle only |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3ksr2m-replay.idx" git read-tree 35af013b901ed4be1b88416068f140e9ca5cc85d` | 0 | Temporary index initialized |
| `task-board resource get TASK-261002-ifa91r TASK-261002-ifa91r_change-request_rev1.patch --output .temp/TASK-261002-ifa91r_change-request_rev1.patch` | 0 | Read-only patch download |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3ksr2m-replay.idx" git apply --cached .temp/TASK-261002-ifa91r_change-request_rev1.patch` | 0 | Patch applied |
| `GIT_INDEX_FILE="$PWD/.temp/TASK-261002-3ksr2m-replay.idx" git write-tree` | 0 | Exact expected candidate tree above |
| `git diff --check 35af013b901ed4be1b88416068f140e9ca5cc85d 5c365d9a68ea6d2cee0488eb58a37a539ce354d4` | 0 | No whitespace errors |
| `git grep -n -E 'f402e8c5e9b5e317|fd994b11525da73c|32be5470c6e39932|4327e247f74ba810' 5c365d9a68ea6d2cee0488eb58a37a539ce354d4 -- codex-rs` | 1 | Expected nonzero no-match result, empty stdout/stderr; not a passing test |
| `python3 .temp/TASK-261002-3ksr2m/static-audit.py > .temp/TASK-261002-3ksr2m/static-audit-01.log` | 0 | Static comparison only; full source and output below |
| `git status --porcelain=v1` | 0 | Empty; tracked worktree unchanged |

Ancillary discovery failures were not gates: the initial mixed skill/resource-discovery call exited 1 (missing role path, two absent skill directories, and unknown `resources` projection). The role was found at `/Users/iv/.roles/reviewer/role.md`, and resource names read from the task-specific resource directory. `task-board resource list` printed help with exit 0; it did not provide resource evidence. A final optional board filename search exited 1 with no matches; this was not interpreted as missing validation evidence. Corrected task-specific AC/notes/checklist reads, resource downloads, skill reads and source inspections succeeded. Git/rg/Python readiness is in `.temp/TASK-261002-3ksr2m/*readiness.log`.

## Surface sweep and bounded free hunt

The single row, `snapshot fidelity`, held under static attacks through Git's candidate-blob and patch entry points. Exactly 2/2 allowed files changed, 6/6 hash replacements per file; all 12/12 replacements match each of the three original hosted failures for its scenario. Normalizing only hexadecimal hash values makes each complete original/candidate byte sequence identical, detecting even header, whitespace or EOF drift. Old hashes have no matches across tracked candidate `codex-rs`. The row result was persisted before free hunt.

Free hunt checked whether a false green could result from disabling the assertions, blessing snapshots, or excluding the scenarios in hosted configuration. Candidate `codex-rs/core/tests/suite/scenarios.rs:665` and `:1469` still assert actual captured request histories; the public driving paths include `Codex::start_or_steer_turn`, `Op::Compact` (:640), and `Op::ReloadUserConfig` (:1453). The hosted workflow sets `INSTA_UPDATE: no` (:37), and its core filter (:126–129) excludes only three named zsh-fork tests, neither astra scenario. No finding reproduced. This is a static review, not a freshly executed production attack or proof of absence.

## Evidence sources and AC disposition

- Board resources read on TASK-261002-ifa91r: `surface-table.md`, `producer-brief.md`, `ifa91r-note.md`, `TASK-261002-ifa91r_results.md`, `TASK-261002-ifa91r_r122-evidence.md`, `TASK-261002-ifa91r_hosted-ci-stack-1.md`. Producer instructions were context only.
- Original failing run 36959934198: permitted local copy `/Users/iv/Developer/IV/codex/.temp/relux-ci/selftest-core-02.log`, snapshot blocks at lines 8463, 8539, 8614, 8690, 8763, 8840. Each scenario failed three attempts. Run 36959471910 was not independently read.
- Supplied hosted success: https://github.com/relux-works/codex/actions/runs/36962123410; permitted local copy `/Users/iv/Developer/IV/codex/.temp/relux-ci/selftest-core-03.log:8518` and `:8522` names both PASS tests; :9009 reports 4854 passed, 11 skipped. No fresh GitHub query or hosted execution performed.
- Hosted commit `89d8b055bae06fc0ff0861b3ae5b9e5effae6ce0` resolves locally to tree `10be7d67d9b49cd4e2cf65f77b400c85211510df`. Independent tree diff confirms only the added workflow versus candidate. This explicitly limits reuse to identical source/test content, not full-tree equality.
- AC: hosted green for both named scenarios is supported by supplied evidence within that bound; no other snapshot/source change is independently established by exact tree diff. Producer guard/fmt exit-0 reports are accepted as attached prior evidence, not rerun here. No new runtime or API behavior is introduced, and no mutant execution is claimed.

## Logbook

2026-10-02: exact replay and full one-row sweep held. P1 peer-count typo (8 versus measured 7) and hosted-tree/workflow distinction retained as nonblocking notes. Research remains within the panel's read-only scope. Outcome is staged outside the managed worktree at the explicitly required `/tmp/TASK-261002-3ksr2m_panel-verdict.md`, then attached only through resource CRUD on this panel task. No control-root file edited directly.

```verdict-findings
{
  "findings": [],
  "notes": [
    "Brief says 8 P1 peer snapshots; git diff-tree derives 7. All 7 have the expected namespace hashes. Documentation-count discrepancy only.",
    "Hosted evidence reused, not rerun: supplied selftest-core-03.log has both named tests PASS. The independently checked hosted tree differs from candidate only by .github/workflows/relux-ci.yml. This is source/test equivalence, not identical full-tree or local/hosted environment identity.",
    "No cargo, just, build, behavioral test or narrowing mutant executed. Static attack coverage is 1/1 rows; local behavioral coverage is 0/1 AC rows. Supplied hosted evidence covers 1/1 AC rows within the stated source identity bound."
  ],
  "surface_results": [
    {
      "row": "snapshot fidelity",
      "result": "held",
      "reason": "Static Git blob comparison: 12/12 hash-only replacements match all 6 hosted failure blocks; 7/7 independently enumerated P1 peer snapshots consistent; no old hashes found (git grep exit 1); no header, EOF, whitespace or other file drift."
    }
  ],
  "free_hunt": []
}
```

## Static audit output

```text
git diff --name-only 35af013b901ed4be1b88416068f140e9ca5cc85d 5c365d9a68ea6d2cee0488eb58a37a539ce354d4: exit 0
git show 35af013b901ed4be1b88416068f140e9ca5cc85d:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_kickoff_remote_compaction_windows.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_kickoff_remote_compaction_windows.snap: exit 0
codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_kickoff_remote_compaction_windows.snap: 6/6 changes match 3/3 hosted failure diffs; all other bytes invariant
git show 35af013b901ed4be1b88416068f140e9ca5cc85d:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_plugin_refresh.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_plugin_refresh.snap: exit 0
codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_plugin_refresh.snap: 6/6 changes match 3/3 hosted failure diffs; all other bytes invariant
git diff-tree --no-commit-id --name-only -r 35af013b901ed4be1b88416068f140e9ca5cc85d -- codex-rs/core/tests/suite/snapshots/*astra*.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_active_environment_selection.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_async_question_and_answer.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_code_mode_call_timing.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_disabled_executor_skills.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_input_interrupts_response.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_input_yields_code_mode_cell.snap: exit 0
git show 5c365d9a68ea6d2cee0488eb58a37a539ce354d4:codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_settings_release_check_tool_shapes.snap: exit 0
7/7 P1 peer snapshots consistent (brief count 8 is inaccurate)
git diff --name-status 5c365d9a68ea6d2cee0488eb58a37a539ce354d4 10be7d67d9b49cd4e2cf65f77b400c85211510df: exit 0
git rev-parse 89d8b055bae06fc0ff0861b3ae5b9e5effae6ce0^{tree}: exit 0
        PASS [   1.204s] (4365/4854) codex-core::all suite::scenarios::astra_kickoff_with_skills_plugins_and_remote_compaction
        PASS [   1.702s] (4369/4854) codex-core::all suite::scenarios::astra_refreshes_plugin_tools_and_skills_in_an_existing_thread
Static audit passed; no build or behavioral test executed
```

## Reproducible static audit

```python
from pathlib import Path
import subprocess, difflib, re
base='35af013b901ed4be1b88416068f140e9ca5cc85d'
cand='5c365d9a68ea6d2cee0488eb58a37a539ce354d4'
def git(*args):
    p=subprocess.run(['git',*args],capture_output=True)
    print('git '+ ' '.join(args)+': exit '+str(p.returncode))
    assert p.returncode==0,p.stderr
    return p.stdout
files=['codex-rs/core/tests/suite/snapshots/all__suite__scenarios__astra_'+s+'.snap' for s in ['kickoff_remote_compaction_windows','plugin_refresh']]
assert git('diff','--name-only',base,cand).decode().splitlines()==files
log=Path('/Users/iv/Developer/IV/codex/.temp/relux-ci/selftest-core-02.log').read_text()
for f in files:
    a=git('show',base+':'+f); b=git('show',cand+':'+f)
    lines=list(difflib.unified_diff(a.decode().splitlines(),b.decode().splitlines(),n=0))
    old=[s[1:] for s in lines if s.startswith('-') and not s.startswith('---')]
    new=[s[1:] for s in lines if s.startswith('+') and not s.startswith('+++')]
    assert len(old)==len(new)==6
    assert a.splitlines()[:4]==b.splitlines()[:4] and a.endswith(b'\n') and b.endswith(b'\n')
    normalized=lambda x: re.sub(rb'hash=[0-9a-f]{16}',b'hash=HASH',x)
    assert normalized(a)==normalized(b)
    parts=log.split('Snapshot file: '+f.removeprefix('codex-rs/'))[1:]
    assert len(parts)==3
    for part in parts:
        part=part.split('Stopped on the first failure.')[0]
        assert old==re.findall(r'│-(.*)',part)
        assert new==re.findall(r'│\+(.*)',part)
    print(f'{f}: 6/6 changes match 3/3 hosted failure diffs; all other bytes invariant')
peers=git('diff-tree','--no-commit-id','--name-only','-r',base,'--','codex-rs/core/tests/suite/snapshots/*astra*.snap').decode().splitlines()
assert len(peers)==7
for f in peers:
    b=git('show',cand+':'+f)
    assert b'hash=9bb57c9cf15a03d4' in b and b'hash=fa3407ba7e35263b' in b
print('7/7 P1 peer snapshots consistent (brief count 8 is inaccurate)')
assert git('diff','--name-status',cand,'10be7d67d9b49cd4e2cf65f77b400c85211510df').decode().strip()=='A\t.github/workflows/relux-ci.yml'
assert git('rev-parse','89d8b055bae06fc0ff0861b3ae5b9e5effae6ce0^{tree}').decode().strip()=='10be7d67d9b49cd4e2cf65f77b400c85211510df'
green=Path('/Users/iv/Developer/IV/codex/.temp/relux-ci/selftest-core-03.log').read_text()
for test in ['astra_kickoff_with_skills_plugins_and_remote_compaction','astra_refreshes_plugin_tools_and_skills_in_an_existing_thread']:
    matches=[x for x in green.splitlines() if 'PASS' in x and 'suite::scenarios::'+test in x]
    assert len(matches)==1
    print(matches[0])
print('Static audit passed; no build or behavioral test executed')
```
