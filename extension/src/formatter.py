"""
Task Formatter

Helpers for formatting Morgen tasks for display in Ulauncher.
"""

from __future__ import annotations


class TaskFormatter:
    """Format Morgen task dicts for display."""

    def format_for_display(self, task: dict) -> str:
        title = (task.get("title") or "Untitled").strip() or "Untitled"
        priority = task.get("priority", 0)
        priority_icon = get_priority_icon(priority)
        if priority_icon:
            return f"{priority_icon} {title}"
        return title

    def format_subtitle(self, task: dict) -> str:
        due = task.get("due")
        due_display = self._format_due(due)

        priority = task.get("priority", 0)
        priority_display = "None" if not priority else str(priority)

        description = (task.get("description") or "").strip()
        if description:
            description = self._truncate(description, 80)
            return f"Due: {due_display} | Priority: {priority_display} — {description}"

        return f"Due: {due_display} | Priority: {priority_display}"

    def _format_due(self, due) -> str:
        if not due:
            return "No due date"
        if isinstance(due, str) and "T" in due:
            return due.replace("T", " ")
        return str(due)

    def _truncate(self, text: str, max_len: int) -> str:
        if len(text) <= max_len:
            return text
        return text[: max_len - 1].rstrip() + "…"


def get_priority_icon(priority) -> str:
    """
    Return a small priority marker.

    Morgen priority: 1 (highest) .. 9 (lowest), 0/None = undefined.
    """
    try:
        priority_int = int(priority or 0)
    except (TypeError, ValueError):
        return ""

    if priority_int <= 0:
        return ""
    if 1 <= priority_int <= 3:
        return f"[P{priority_int}]"
    return f"[P{priority_int}]"

