#!/usr/bin/env python3
"""
Fill the extension runtime log close to the rotation threshold.

Purpose:
  Helps manually test RotatingFileHandler rollover for `extension/logs/runtime.log`.

Default behavior:
  - Appends to the existing log until it reaches ~990 KiB (just under 1 MiB),
    so the next log line written by the extension should trigger rotation.

Examples:
  python development/tools/fill_runtime_log.py
  python development/tools/fill_runtime_log.py --truncate
  python development/tools/fill_runtime_log.py --target-kib 1010  # intentionally exceed
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime


def _repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _default_log_path() -> str:
    return os.path.join(_repo_root(), "extension", "logs", "runtime.log")


def _format_kib(num_bytes: int) -> str:
    return f"{num_bytes / 1024:.1f} KiB"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Fill runtime.log close to 1 MiB for rotation testing.")
    parser.add_argument("--log-path", default=_default_log_path(), help="Path to runtime.log")
    parser.add_argument(
        "--target-kib",
        type=int,
        default=990,
        help="Target size in KiB (default: 990 KiB, just under 1 MiB)",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Truncate runtime.log before writing",
    )
    parser.add_argument(
        "--line-bytes",
        type=int,
        default=512,
        help="Approx bytes per appended line (default: 512)",
    )
    args = parser.parse_args(argv)

    log_path = os.path.abspath(args.log_path)
    target_bytes = max(0, int(args.target_kib) * 1024)
    line_bytes = max(64, int(args.line_bytes))

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    if args.truncate:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("")

    current_size = os.path.getsize(log_path) if os.path.exists(log_path) else 0
    if current_size >= target_bytes:
        print(f"runtime.log already at {_format_kib(current_size)} (target {_format_kib(target_bytes)}); nothing to do.")
        return 0

    prefix = f"{datetime.now().isoformat(timespec='seconds')} INFO filler: "
    padding_len = max(0, line_bytes - len(prefix) - 1)  # -1 for "\n"
    payload = "x" * padding_len
    line = f"{prefix}{payload}\n"
    line_len = len(line.encode("utf-8"))

    current_size = os.path.getsize(log_path) if os.path.exists(log_path) else 0
    with open(log_path, "a", encoding="utf-8") as f:
        while current_size + line_len <= target_bytes:
            f.write(line)
            current_size += line_len

    final_size = os.path.getsize(log_path)
    print(f"Wrote runtime.log to {_format_kib(final_size)} (target {_format_kib(target_bytes)}).")
    print("Next: trigger the extension (e.g. run `mg`) to write one more entry and check rotation:")
    print("  - extension/logs/runtime.log.1")
    print("  - extension/logs/runtime.log.2")
    print("  - extension/logs/runtime.log.3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
