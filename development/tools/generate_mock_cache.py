#!/usr/bin/env python3
"""
Generate a synthetic Morgen cache file for search/performance testing.

By default this writes 500 tasks to:
  ~/.cache/ulauncher-morgen-tasks/tasks_cache.json

Examples:
  python development/tools/generate_mock_cache.py
  python development/tools/generate_mock_cache.py --count 800 --backup
  python development/tools/generate_mock_cache.py --cache-path /tmp/tasks_cache.json --count 500
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timedelta


DEFAULT_CACHE_PATH = os.path.join(
    os.path.expanduser("~"),
    ".cache",
    "ulauncher-morgen-tasks",
    "tasks_cache.json",
)


def _build_task(i: int) -> dict:
    now = datetime.now().replace(microsecond=0)
    due = now + timedelta(days=(i % 14), hours=i % 6)
    created = now - timedelta(days=(i % 30) + 1)
    updated = now - timedelta(minutes=i % 120)

    list_id = "inbox" if i % 5 == 0 else f"list-{(i % 12) + 1}@morgen.so"
    priority_cycle = [1, 5, 9]

    return {
        "id": f"mock-task-{i:04d}",
        "title": f"Mock task {i:04d} planning sync",
        "description": f"Synthetic task {i:04d} for cache search performance validation.",
        "priority": priority_cycle[i % len(priority_cycle)],
        "progress": "notStarted",
        "taskListId": list_id,
        "integrationId": "morgen",
        "due": due.strftime("%Y-%m-%dT%H:%M:%S"),
        "created": created.strftime("%Y-%m-%dT%H:%M:%S"),
        "updated": updated.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def _build_payload(count: int) -> dict:
    tasks = [_build_task(i) for i in range(1, count + 1)]
    return {
        "timestamp": time.time(),
        "cache": {
            "data": {
                "tasks": tasks,
                "spaces": [],
                "labelDefs": [],
            }
        },
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Generate synthetic tasks cache for local performance testing.")
    parser.add_argument("--count", type=int, default=500, help="Number of tasks to generate (default: 500)")
    parser.add_argument("--cache-path", default=DEFAULT_CACHE_PATH, help="Destination cache file path")
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create '<cache>.bak' before overwrite if destination exists",
    )
    args = parser.parse_args(argv)

    if args.count < 1:
        print("Error: --count must be >= 1", file=sys.stderr)
        return 2

    cache_path = os.path.abspath(os.path.expanduser(args.cache_path))
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)

    if args.backup and os.path.exists(cache_path):
        backup_path = f"{cache_path}.bak"
        shutil.copy2(cache_path, backup_path)
        print(f"Backup created: {backup_path}")

    payload = _build_payload(args.count)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(payload, f)

    print(f"Wrote {args.count} tasks to cache:")
    print(f"  {cache_path}")
    print("Next:")
    print("  1) Restart Ulauncher: pkill ulauncher && ulauncher -v")
    print('  2) Trigger extension: type "mg"')
    print("  3) Run search tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
