"""
Task query filter parsing and matching helpers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta


_PRIORITY_NAME_TO_VALUE = {
    "high": 1,
    "medium": 5,
    "low": 9,
    "normal": 0,
}

_SUPPORTED_DUE_FILTERS = {"today", "tomorrow", "overdue", "future", "week", "nodue"}


@dataclass(frozen=True)
class TaskFilterSpec:
    priority_values: set[int] = field(default_factory=set)
    due_values: set[str] = field(default_factory=set)

    @property
    def active(self) -> bool:
        return bool(self.priority_values or self.due_values)


def parse_query_filters(query: str) -> tuple[TaskFilterSpec, str]:
    tokens = (query or "").split()
    if not tokens:
        return TaskFilterSpec(), ""

    priority_values: set[int] = set()
    due_values: set[str] = set()
    remaining_tokens: list[str] = []

    for token in tokens:
        lower = token.lower()

        if lower.startswith("p:") or lower.startswith("priority:"):
            value = lower.split(":", 1)[1].strip()
            parsed = _parse_priority_filter_value(value)
            if parsed is None:
                remaining_tokens.append(token)
            else:
                priority_values.add(parsed)
            continue

        if lower.startswith("due:"):
            value = lower.split(":", 1)[1].strip()
            if value in _SUPPORTED_DUE_FILTERS:
                due_values.add(value)
            else:
                remaining_tokens.append(token)
            continue

        remaining_tokens.append(token)

    return TaskFilterSpec(priority_values=priority_values, due_values=due_values), " ".join(remaining_tokens).strip()


def matches_task_filters(task: dict, spec: TaskFilterSpec, *, now: datetime | None = None) -> bool:
    if not spec.active:
        return True

    if spec.priority_values and not _match_priority(task, spec.priority_values):
        return False

    if spec.due_values and not _match_due(task, spec.due_values, now=now):
        return False

    return True


def _parse_priority_filter_value(value: str) -> int | None:
    if not value:
        return None
    if value in _PRIORITY_NAME_TO_VALUE:
        return _PRIORITY_NAME_TO_VALUE[value]
    if value.isdigit():
        parsed = int(value)
        if 1 <= parsed <= 9:
            return parsed
    return None


def _match_priority(task: dict, allowed_values: set[int]) -> bool:
    raw = task.get("priority")
    try:
        priority = int(raw) if raw is not None else 0
    except Exception:
        priority = 0
    return priority in allowed_values


def _match_due(task: dict, due_filters: set[str], *, now: datetime | None = None) -> bool:
    now = now or datetime.now()
    due_text = (task.get("due") or "").strip()

    if not due_text:
        return "nodue" in due_filters

    try:
        due_dt = datetime.fromisoformat(due_text[:19])
    except Exception:
        # Keep malformed data visible unless strict due filter is used.
        return False

    due_date = due_dt.date()
    today = now.date()
    tomorrow = today + timedelta(days=1)

    if "today" in due_filters and due_date == today:
        return True
    if "tomorrow" in due_filters and due_date == tomorrow:
        return True
    if "overdue" in due_filters and due_dt < now:
        return True
    if "future" in due_filters and due_dt > now:
        return True
    if "week" in due_filters and today <= due_date <= (today + timedelta(days=7)):
        return True

    return False

