#!/usr/bin/env python3
"""relux_ci_static_audit: static gate for .github/workflows/relux-ci.yml (TASK-261002-1ugz6h).

Usage: python3 relux_ci_static_audit.py <workflow.yml>
Exit 0 when every check passes; exit 1 naming the failed checks otherwise.
Each check maps to an AC row / surface-table row (see results note).
"""
import re
import sys

import yaml

FAILURES = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f" -- {detail}" if detail and not cond else ""))
    if not cond:
        FAILURES.append(name)


def main(path):
    with open(path) as f:
        text = f.read()
    try:
        wf = yaml.safe_load(text)
    except Exception as e:  # noqa: BLE001
        print(f"FAIL yaml-parses -- {e}")
        return 1
    check("yaml-parses", isinstance(wf, dict))

    on = wf.get("on", wf.get(True, {}))  # PyYAML reads YAML 1.1 `on:` as boolean True
    check("triggers-only-dispatch-and-push", set(on) == {"workflow_dispatch", "push"}, f"on={sorted(on)}")
    check("push-branches-selftest-only",
          on.get("push", {}).get("branches") == ["ci/relux-ci-selftest/**"],
          f"branches={on.get('push', {}).get('branches')}")
    inputs = on.get("workflow_dispatch", {}).get("inputs", {})
    check("dispatch-sha-required", inputs.get("sha", {}).get("required") is True)

    check("permissions-contents-read", wf.get("permissions") == {"contents": "read"},
          f"permissions={wf.get('permissions')}")
    check("no-secrets-refs", "secrets." not in text)

    jobs = wf.get("jobs", {})
    runs_on = {name: j.get("runs-on") for name, j in jobs.items()}
    check("runs-on-ubuntu-24.04-only", set(runs_on.values()) == {"ubuntu-24.04"}, f"{runs_on}")

    uses = re.findall(r"uses:\s*(\S+)", text)
    third_party = [u for u in uses if not u.startswith("./")]
    unpinned = [u for u in third_party if not re.search(r"@[0-9a-f]{40}\b", u)]
    check("third-party-actions-sha-pinned", not unpinned, f"unpinned={unpinned}")

    steps_early = [s for j in jobs.values() for s in j.get("steps", [])]
    interp = [s.get("name", s.get("uses")) for s in steps_early
              if "inputs." in str(s.get("run", "")) or "github." in str(s.get("run", ""))]
    check("no-context-interpolation-in-run", not interp, f"steps={interp}")

    steps = [s for j in jobs.values() for s in j.get("steps", [])]
    checkout = [s for s in steps if str(s.get("uses", "")).startswith("actions/checkout@")]
    check("checkout-exact-sha",
          len(checkout) == 1 and checkout[0].get("with", {}).get("ref") == "${{ inputs.sha || github.sha }}",
          f"ref={[s.get('with', {}).get('ref') for s in checkout]}")
    run_name = wf.get("run-name", "")
    check("run-name-carries-sha", "inputs.sha" in run_name and "github.sha" in run_name, run_name)
    check("concurrency-keyed-on-sha", "inputs.sha" in str(wf.get("concurrency", {}).get("group", "")))

    coe = [s.get("name", s.get("uses")) for s in steps if s.get("continue-on-error") is True]
    check("continue-on-error-only-cache-save", coe == ["Save sccache cache"], f"{coe}")

    def step_text(name):
        return "\n".join(str(s.get("run", "")) for s in steps if s.get("name") == name)

    for name in ("Free runner disk", "sccache stats"):
        pass  # allowed `|| true`: cleanup of optional dirs, stats reporting
    test_steps = ["Lint (fmt + clippy)", "Small crates tests", "codex-core tests", "codex-app-server tests"]
    masked = [n for n in test_steps if "|| true" in step_text(n)]
    check("test-exits-unmasked", not masked, f"{masked}")

    lint = step_text("Lint (fmt + clippy)")
    six = {"codex-tools", "codex-core", "codex-goal-extension",
           "codex-extension-api", "codex-app-server", "codex-rollout-trace"}
    m = re.search(r"just clippy((?:\s+-p\s+\S+)+)", lint)
    check("lint-six-series-crates",
          "just fmt-check" in lint and m and {p for p in m.group(1).split() if p != "-p"} == six,
          lint.splitlines()[-1] if lint else "missing lint step")

    small = step_text("Small crates tests")
    four = {"codex-tools", "codex-goal-extension", "codex-extension-api", "codex-rollout-trace"}
    m = re.search(r"just test((?:\s+-p\s+\S+)+)", small)
    check("small-four-crates",
          bool(m) and {p for p in m.group(1).split() if p != "-p"} == four,
          small.strip().splitlines()[-1] if small else "missing small step")

    core = step_text("codex-core tests")
    excl = re.findall(r"test\(=([\w:]+)\)", core)
    check("core-three-documented-exclusions",
          core.lstrip().startswith("INSTA_WORKSPACE_ROOT=") and "-E 'not (" in core and len(excl) == 3
          and all("zsh_fork" in e for e in excl),
          f"exclusions={excl}")
    check("core-exclusions-documented-with-evidence",
          "36959471910" in text and "36959934198" in text)

    app = step_text("codex-app-server tests")
    check("app-server-full-suite-no-exclusion",
          "just test -p codex-app-server" in app and "-E" not in app, app.strip()[:120])

    helpers = step_text("Helper binaries for integration tests")
    need = ["test_stdio_server", "test_streamable_http_server", "codex-execve-wrapper",
            "codex-app-server", "codex-app-server-test-notify-capture", "exec-server",
            "codex-code-mode-host", "codex-linux-sandbox"]
    check("helper-binaries-built", all(b in helpers for b in need),
          f"missing={[b for b in need if b not in helpers]}")
    order = [s.get("name", "") for s in steps]
    hi = order.index("Helper binaries for integration tests") if "Helper binaries for integration tests" in order else 9**9
    check("helpers-before-test-lanes",
          hi < order.index("codex-core tests") and hi < order.index("codex-app-server tests"))

    check("nextest-retries-rerun-only", wf.get("env", {}).get("NEXTEST_RETRIES") == "2")

    print(f"--- {len(FAILURES)} failures ---")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
