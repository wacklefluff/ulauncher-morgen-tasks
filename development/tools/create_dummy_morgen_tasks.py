#!/usr/bin/env python3
"""
Create real dummy tasks in Morgen for manual testing.

Defaults:
  - 90 tasks
  - title prefix: "#dev Testing "
  - API key from MORGEN_API_KEY env var (or --api-key)
"""

from __future__ import annotations

import argparse
import os
import sys
import time


def _repo_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _load_modules():
    src_dir = os.path.join(_repo_root(), "extension", "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    from morgen_api import (  # pylint: disable=import-error
        MorgenAPIClient,
        MorgenAPIError,
        MorgenAuthError,
        MorgenNetworkError,
        MorgenRateLimitError,
    )
    from dev_dummy_tasks import (  # pylint: disable=import-error
        DEFAULT_DUMMY_TASK_COUNT,
        DEFAULT_DUMMY_TITLE_PREFIX,
        build_dummy_task_specs,
    )
    return (
        MorgenAPIClient,
        MorgenAPIError,
        MorgenAuthError,
        MorgenNetworkError,
        MorgenRateLimitError,
        DEFAULT_DUMMY_TASK_COUNT,
        DEFAULT_DUMMY_TITLE_PREFIX,
        build_dummy_task_specs,
    )


def main(argv: list[str]) -> int:
    (
        MorgenAPIClient,
        MorgenAPIError,
        MorgenAuthError,
        MorgenNetworkError,
        MorgenRateLimitError,
        default_count,
        default_prefix,
        build_dummy_task_specs,
    ) = _load_modules()

    parser = argparse.ArgumentParser(description="Create real dummy tasks in Morgen.")
    parser.add_argument("--api-key", default=os.environ.get("MORGEN_API_KEY", ""), help="Morgen API key")
    parser.add_argument("--count", type=int, default=default_count, help=f"Number of tasks (default: {default_count})")
    parser.add_argument("--prefix", default=default_prefix, help=f"Title prefix (default: {default_prefix!r})")
    parser.add_argument(
        "--sleep-ms",
        type=int,
        default=0,
        help="Optional delay between requests in milliseconds (default: 0)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print first 5 generated tasks and exit without API calls",
    )
    args = parser.parse_args(argv)

    count = max(1, int(args.count))
    specs = build_dummy_task_specs(count=count, title_prefix=args.prefix)

    if args.dry_run:
        print(f"Dry run: would create {count} tasks")
        for item in specs[:5]:
            print(f"- {item['title']} | priority={item['priority']} | due={item['due'] or '(none)'}")
        return 0

    api_key = (args.api_key or "").strip()
    if not api_key:
        print("Error: missing API key. Use --api-key or MORGEN_API_KEY.", file=sys.stderr)
        return 2

    client = MorgenAPIClient(api_key)
    sleep_seconds = max(0, int(args.sleep_ms)) / 1000.0

    created = 0
    failed = 0
    first_error = ""

    print(f"Creating {count} tasks in Morgen with prefix {args.prefix!r}...")
    for idx, spec in enumerate(specs, start=1):
        try:
            client.create_task(
                title=spec["title"],
                description=spec["description"],
                due=spec["due"],
                priority=spec["priority"],
            )
            created += 1
            if idx % 10 == 0 or idx == count:
                print(f"  Progress: {idx}/{count} (created={created}, failed={failed})")
        except (MorgenAuthError, MorgenRateLimitError, MorgenNetworkError) as exc:
            failed += 1
            first_error = first_error or str(getattr(exc, "message", exc))
            print(f"Stopped at task {idx}: {first_error}", file=sys.stderr)
            break
        except MorgenAPIError as exc:
            failed += 1
            first_error = first_error or str(getattr(exc, "message", exc))
            print(f"Task {idx} failed: {str(getattr(exc, 'message', exc))}", file=sys.stderr)
        except Exception as exc:  # pragma: no cover - safety
            failed += 1
            first_error = first_error or str(exc)
            print(f"Task {idx} failed unexpectedly: {exc}", file=sys.stderr)

        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    print("Done.")
    print(f"Created: {created}")
    print(f"Failed:  {failed}")
    if first_error:
        print(f"First error: {first_error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
