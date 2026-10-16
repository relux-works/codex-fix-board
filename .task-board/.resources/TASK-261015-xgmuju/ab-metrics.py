#!/usr/bin/env python3
"""Summarise one Codex rollout for the goal-mode token-burn A/B.

Requests are counted as token_count events whose cumulative total changed
(one per model response; duplicate re-emits of the same total are ignored).
"""
import json
import sys
from datetime import datetime


def ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def summarise(path):
    first = last_complete = None
    requests = 0
    prev_total = None
    final = None
    tool_calls = 0
    tool_names = {}
    for line in open(path):
        o = json.loads(line)
        t = o.get("timestamp")
        if t and first is None:
            first = ts(t)
        p = o.get("payload") or {}
        kind = p.get("type")
        if o.get("type") == "event_msg" and kind == "token_count" and p.get("info"):
            total = p["info"]["total_token_usage"]
            if total["total_tokens"] != prev_total:
                requests += 1
                prev_total = total["total_tokens"]
                final = total
        elif o.get("type") == "event_msg" and kind == "task_complete" and t:
            last_complete = ts(t)
        elif o.get("type") == "response_item" and kind in ("function_call", "custom_tool_call"):
            tool_calls += 1
            name = p.get("name", "?")
            tool_names[name] = tool_names.get(name, 0) + 1
    wall = (last_complete - first).total_seconds() if first and last_complete else None
    final = final or {}
    return {
        "rollout": path,
        "requests": requests,
        "input_tokens": final.get("input_tokens"),
        "cached_input_tokens": final.get("cached_input_tokens"),
        "uncached_input_tokens": (final.get("input_tokens") or 0) - (final.get("cached_input_tokens") or 0),
        "output_tokens": final.get("output_tokens"),
        "reasoning_output_tokens": final.get("reasoning_output_tokens"),
        "total_tokens": final.get("total_tokens"),
        "tool_calls": tool_calls,
        "tool_names": tool_names,
        "wall_seconds": wall,
    }


if __name__ == "__main__":
    print(json.dumps([summarise(p) for p in sys.argv[1:]], indent=2))
