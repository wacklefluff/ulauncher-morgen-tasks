"""
Task Formatter

Helpers for formatting Morgen tasks for display in Ulauncher.
"""

from __future__ import annotations

from datetime import datetime


def is_overdue(due: str | None, now: datetime | None = None) -> bool:
    """Check if a due date string is in the past."""
    if not due:
        return False
    now = now or datetime.now()
    try:
        # Morgen format: YYYY-MM-DDTHH:mm:ss
        due_dt = datetime.fromisoformat(due[:19])
        return due_dt < now
    except (ValueError, TypeError):
        return False


class TaskFormatter:
    """Format Morgen task dicts for display."""

    def format_for_display(self, task: dict) -> str:
        title = (task.get("title") or "Untitled").strip() or "Untitled"
        priority = task.get("priority", 0)
        priority_icon = get_priority_icon(priority)
        due = task.get("due")
        overdue = is_overdue(due)

        parts = []
        if overdue:
            parts.append("OVERDUE")
        if priority_icon:
            parts.append(priority_icon)
        parts.append(title)

        return " ".join(parts)

    def format_subtitle(self, task: dict) -> str:
        due = task.get("due")
        overdue = is_overdue(due)
        due_display = self._format_due(due, overdue)

        priority = task.get("priority", 0)
        priority_display = get_priority_label(priority)

        description = (task.get("description") or "").strip()
        if description:
            description = self._truncate(description, 80)
            return f"Due: {due_display} | Priority: {priority_display} — {description}"

        return f"Due: {due_display} | Priority: {priority_display}"

    def format_condensed_subtitle(self, task: dict) -> str:
        """Compact one-line subtitle for condensed display mode."""
        due = task.get("due")
        overdue = is_overdue(due)
        due_display = self._format_due(due, overdue)

        priority = task.get("priority", 0)
        priority_label = get_priority_label(priority)

        parts = []
        if due:
            parts.append(due_display)
        if priority_label not in {"Normal", ""}:
            parts.append(priority_label)

        return " · ".join(parts) if parts else "No due date"

    def _format_due(self, due, overdue: bool = False) -> str:
        if not due:
            return "No due date"
        try:
            from datetime import timedelta

            due_dt = datetime.fromisoformat(due[:19])
            now = datetime.now()
            today = now.date()
            tomorrow = today + timedelta(days=1)
            due_date = due_dt.date()
            time_str = due_dt.strftime("%H:%M")

            # Relative labels
            if due_date == today:
                label = f"Today {time_str}"
            elif due_date == tomorrow:
                label = f"Tomorrow {time_str}"
            else:
                label = due_dt.strftime("%Y-%m-%d %H:%M")

            if overdue:
                return f"{label} (overdue!)"
            return label
        except (ValueError, TypeError):
            if isinstance(due, str) and "T" in due:
                return due.replace("T", " ")
            return str(due)

    def _truncate(self, text: str, max_len: int) -> str:
        if len(text) <= max_len:
            return text
        return text[: max_len - 1].rstrip() + "…"


def get_priority_icon(priority) -> str:
    """
    Return a visual priority marker.

    Morgen API normalizes priorities:
      - High (1,2,3) → returns 1
      - Medium (4,5) → returns 5
      - Low (6,7,8,9) → returns 9
      - Normal → returns None/0

    Icons:
      - 1: !!  (high)
      - 5: !   (medium)
      - 9: (none, low)
    """
    try:
        priority_int = int(priority or 0)
    except (TypeError, ValueError):
        return ""

    if priority_int <= 0:
        return ""
    if priority_int == 1:
        return "!!"
    if priority_int == 5:
        return "!"
    return ""


def get_priority_label(priority) -> str:
    """
    Return a human-readable priority label for subtitle display.

    Morgen API normalizes priorities:
      - High (1,2,3) → returns 1
      - Medium (4,5) → returns 5
      - Low (6,7,8,9) → returns 9
      - Normal → returns None/0
    """
    try:
        priority_int = int(priority or 0)
    except (TypeError, ValueError):
        return "Normal"

    if priority_int <= 0:
        return "Normal"
    if priority_int == 1:
        return "High"
    if priority_int == 5:
        return "Medium"
    if priority_int == 9:
        return "Low"
    # Fallback for unexpected values
    return f"Priority {priority_int}"

