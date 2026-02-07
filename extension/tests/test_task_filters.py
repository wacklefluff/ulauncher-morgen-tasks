import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task_filters import parse_query_filters, matches_task_filters


def test_parse_query_filters_extracts_priority_and_due_tokens():
    spec, remaining = parse_query_filters("report p:high due:today")
    assert remaining == "report"
    assert spec.priority_values == {1}
    assert spec.due_values == {"today"}


def test_parse_query_filters_supports_numeric_priority():
    spec, remaining = parse_query_filters("p:9")
    assert remaining == ""
    assert spec.priority_values == {9}


def test_parse_query_filters_unknown_values_fall_back_to_text():
    spec, remaining = parse_query_filters("due:later p:urgent monthly report")
    assert remaining == "due:later p:urgent monthly report"
    assert not spec.active


def test_matches_task_filters_priority_name():
    task = {"priority": 1, "due": None}
    spec, _ = parse_query_filters("p:high")
    assert matches_task_filters(task, spec)


def test_matches_task_filters_due_today():
    now = datetime(2026, 2, 7, 9, 0, 0)
    task = {"due": "2026-02-07T14:00:00"}
    spec, _ = parse_query_filters("due:today")
    assert matches_task_filters(task, spec, now=now)


def test_matches_task_filters_due_overdue():
    now = datetime(2026, 2, 7, 9, 0, 0)
    task = {"due": "2026-02-06T08:00:00"}
    spec, _ = parse_query_filters("due:overdue")
    assert matches_task_filters(task, spec, now=now)


def test_matches_task_filters_due_nodue():
    now = datetime(2026, 2, 7, 9, 0, 0)
    task = {"due": None}
    spec, _ = parse_query_filters("due:nodue")
    assert matches_task_filters(task, spec, now=now)


def test_matches_task_filters_combined_priority_and_due():
    now = datetime(2026, 2, 7, 9, 0, 0)
    task = {"priority": 1, "due": "2026-02-07T14:00:00"}
    spec, _ = parse_query_filters("p:high due:today")
    assert matches_task_filters(task, spec, now=now)

