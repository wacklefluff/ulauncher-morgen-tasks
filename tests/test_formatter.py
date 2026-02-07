import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from formatter import TaskFormatter, get_priority_icon, get_priority_label, is_overdue


def test_priority_icon_mapping():
    assert get_priority_icon(0) == ""
    assert get_priority_icon(None) == ""
    assert get_priority_icon(1) == "!!"
    assert get_priority_icon(5) == "!"
    assert get_priority_icon(9) == ""


def test_priority_label_mapping():
    assert get_priority_label(0) == "Normal"
    assert get_priority_label(None) == "Normal"
    assert get_priority_label(1) == "High"
    assert get_priority_label(5) == "Medium"
    assert get_priority_label(9) == "Low"


def test_is_overdue_handles_invalid_strings():
    assert is_overdue(None) is False
    assert is_overdue("") is False
    assert is_overdue("not-a-date") is False


def test_format_for_display_includes_overdue_and_priority():
    formatter = TaskFormatter()
    task = {"title": "Pay rent", "priority": 1, "due": "2000-01-01T00:00:00"}
    s = formatter.format_for_display(task)
    assert s.startswith("OVERDUE !! ")
    assert s.endswith("Pay rent")


def test_format_subtitle_truncates_description():
    formatter = TaskFormatter()
    long_desc = "x" * 200
    task = {"title": "Task", "priority": 0, "due": "2100-01-01T00:00:00", "description": long_desc}
    subtitle = formatter.format_subtitle(task)
    assert subtitle.startswith("Due: 2100-01-01 00:00 | Priority: Normal — ")
    assert subtitle.endswith("…")
    assert len(subtitle) < 200


def test_format_subtitle_shows_created_when_no_due():
    formatter = TaskFormatter()
    task = {"title": "Task", "priority": 0, "due": None, "created": "2026-02-05T10:20:30"}
    subtitle = formatter.format_subtitle(task)
    assert subtitle == "Created: 2026-02-05 | Priority: Normal"
