"""
Development helpers for generating dummy Morgen tasks.
"""

from __future__ import annotations

from datetime import datetime, timedelta

DEFAULT_DUMMY_TASK_COUNT = 90
DEFAULT_DUMMY_TITLE_PREFIX = "#dev Testing "


def build_dummy_task_specs(
    count: int = DEFAULT_DUMMY_TASK_COUNT,
    title_prefix: str = DEFAULT_DUMMY_TITLE_PREFIX,
) -> list[dict]:
    """
    Build synthetic task payloads for bulk create testing.

    Each item includes:
      - title (always prefixed with `title_prefix`)
      - description
      - priority (varies across 0/1/5/9)
      - due (YYYY-MM-DDTHH:mm:ss or None)
    """
    count = max(1, int(count))
    now = datetime.now().replace(second=0, microsecond=0)
    priorities = [0, 1, 5, 9]

    specs: list[dict] = []
    for idx in range(1, count + 1):
        priority = priorities[(idx - 1) % len(priorities)]

        # Include some tasks with no due date to mimic realistic payload variety.
        due = None
        if idx % 6 != 0:
            day_offset = ((idx - 1) % 21) - 5  # mix of overdue, today, and future
            hour_offset = (idx * 3) % 24
            due_dt = now + timedelta(days=day_offset, hours=hour_offset)
            due = due_dt.strftime("%Y-%m-%dT%H:%M:%S")

        title = f"{title_prefix}{idx:03d}"
        description = (
            f"Dummy seed task {idx:03d} for local search/cache performance testing."
        )

        specs.append(
            {
                "title": title,
                "description": description,
                "priority": priority,
                "due": due,
            }
        )

    return specs
