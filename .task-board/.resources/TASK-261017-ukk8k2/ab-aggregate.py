#!/usr/bin/env python3
"""Aggregate goal-mode A/B metrics per scenario directory, parent and sub-agent rollouts together.

Usage: ab-aggregate.py MARKER_FILE CODEX_HOME [CODEX_HOME ...]
Every rollout modified after MARKER_FILE is grouped by the cwd recorded in its session_meta.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ab_metrics = __import__("ab-metrics")

KEYS = ("requests", "input_tokens", "cached_input_tokens", "uncached_input_tokens",
        "output_tokens", "total_tokens", "tool_calls")


def session_meta(path):
    with open(path) as stream:
        first = json.loads(stream.readline())
    payload = first.get("payload") or {}
    return payload.get("cwd"), payload.get("source")


def main():
    marker = os.path.getmtime(sys.argv[1])
    groups = {}
    for home in sys.argv[2:]:
        for path in Path(home, "sessions").rglob("rollout-*.jsonl"):
            if path.stat().st_mtime <= marker:
                continue
            cwd, source = session_meta(path)
            summary = ab_metrics.summarise(str(path))
            summary["source"] = source
            groups.setdefault(cwd, []).append(summary)
    out = {}
    for cwd, rollouts in sorted(groups.items()):
        total = {key: sum(r[key] or 0 for r in rollouts) for key in KEYS}
        parents = [r for r in rollouts if r["source"] in ("cli", "vscode")]
        total["rollouts"] = len(rollouts)
        total["parent_wall_seconds"] = max((r["wall_seconds"] or 0) for r in parents) if parents else None
        tools = {}
        for r in rollouts:
            for name, count in r["tool_names"].items():
                tools[name] = tools.get(name, 0) + count
        total["tool_names"] = tools
        total["per_rollout"] = [
            {k: r[k] for k in ("rollout", "source", "requests", "total_tokens", "uncached_input_tokens", "wall_seconds")}
            for r in rollouts
        ]
        out[os.path.basename(cwd or "?")] = total
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
