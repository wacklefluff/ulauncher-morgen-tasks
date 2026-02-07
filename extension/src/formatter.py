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
            parts.append("⚠")
        if priority_icon:
            parts.append(priority_icon)
        parts.append(title)

        return " ".join(parts)

    def format_subtitle(self, task: dict) -> str:
        due = task.get("due")
        overdue = is_overdue(due)
        due_display = self._format_due(due, overdue)

        prefix_label = "Due"
        prefix_value = due_display
        if not due:
            created_display = self._format_created(task.get("created"))
            if created_display:
                prefix_label = "Created"
                prefix_value = created_display

        priority = task.get("priority", 0)
        priority_display = get_priority_label(priority)

        description = (task.get("description") or "").strip()
        if description:
            description = self._truncate(description, 80)
            return f"{prefix_label}: {prefix_value} | Priority: {priority_display} — {description}"

        return f"{prefix_label}: {prefix_value} | Priority: {priority_display}"

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

    def _format_created(self, created) -> str | None:
        if not created:
            return None
        if isinstance(created, str):
            try:
                created_dt = datetime.fromisoformat(created[:19])
                return created_dt.strftime("%Y-%m-%d")
            except ValueError:
                if len(created) >= 10 and created[4] == "-" and created[7] == "-":
                    return created[:10]
                if "T" in created:
                    return created[:19].replace("T", " ")
                return created
        return str(created)

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
