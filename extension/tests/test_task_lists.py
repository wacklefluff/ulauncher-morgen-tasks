import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from task_lists import (
    build_container_name_maps,
    get_task_list_ref,
    group_tasks_by_list,
    matches_container_id,
    matches_list_name,
)


def test_get_task_list_ref_from_embedded_list_object():
    task = {"list": {"id": "l1", "name": "Inbox"}}
    ref = get_task_list_ref(task)
    assert ref.kind == "list"
    assert ref.list_id == "l1"
    assert ref.name == "Inbox"
    assert ref.key == "list:id:l1"


def test_get_task_list_ref_from_task_list_id_and_name_fields():
    task = {"taskListId": "tl2", "taskListName": "Inbox"}
    ref = get_task_list_ref(task)
    assert ref.kind == "list"
    assert ref.list_id == "tl2"
    assert ref.name == "Inbox"
    assert ref.key == "list:id:tl2"


def test_get_task_list_ref_from_integration_id_fallback():
    task = {"integrationId": "int-123"}
    ref = get_task_list_ref(task)
    assert ref.kind == "list"
    assert ref.list_id == "int-123"
    assert ref.name is None
    assert ref.key == "list:id:int-123"


def test_get_task_list_ref_from_embedded_project_and_space_objects():
    task = {"project": {"id": "p1", "name": "Work"}, "space": {"id": "s1", "name": "Personal"}}
    ref = get_task_list_ref(task)
    # Prefer project over space
    assert ref.kind == "project"
    assert ref.list_id == "p1"
    assert ref.name == "Work"


def test_get_task_list_ref_prefers_embedded_list_over_fallback_fields():
    task = {"list": {"id": "l1", "name": "Inbox"}, "integrationId": "int-1"}
    ref = get_task_list_ref(task)
    assert ref.kind == "list"
    assert ref.list_id == "l1"


def test_build_container_name_maps_extracts_space_project_list_names():
    api_response = {
        "data": {
            "lists": [{"id": "l1", "name": "Inbox"}],
            "taskLists": [{"id": "tl1", "name": "Inbox TL"}],
            "projects": [{"id": "p1", "name": "Work"}],
            "spaces": [{"id": "s1", "name": "Personal"}],
        }
    }
    maps = build_container_name_maps(api_response)
    assert maps["list"]["l1"] == "Inbox"
    assert maps["list"]["tl1"] == "Inbox TL"
    assert maps["project"]["p1"] == "Work"
    assert maps["space"]["s1"] == "Personal"


def test_get_task_list_ref_resolves_task_list_name_from_maps_when_only_id_present():
    maps = {"list": {"tl9": "Inbox"}}
    task = {"taskListId": "tl9"}
    ref = get_task_list_ref(task, name_maps=maps)
    assert ref.kind == "list"
    assert ref.list_id == "tl9"
    assert ref.name == "Inbox"


def test_get_task_list_ref_uses_integration_id_only_when_no_other_fields():
    task = {"integrationId": "int-1"}
    ref = get_task_list_ref(task)
    assert ref.kind == "list"
    assert ref.list_id == "int-1"


def test_group_tasks_by_list_counts_and_sorts():
    tasks = [
        {"id": "t1", "title": "a", "taskListId": "l2", "taskListName": "Work"},
        {"id": "t2", "title": "b", "taskListId": "l1", "taskListName": "Inbox"},
        {"id": "t3", "title": "c", "taskListId": "l2", "taskListName": "Work"},
        {"id": "t4", "title": "d"},  # ignored (no list metadata)
    ]
    grouped = group_tasks_by_list(tasks)
    # Sorted by name: Inbox, Work
    assert [(r.name, c) for r, c in grouped] == [("Inbox", 1), ("Work", 2)]


def test_group_tasks_by_list_can_group_by_embedded_space_or_project():
    tasks = [
        {"id": "t1", "space": {"id": "s1", "name": "Personal"}},
        {"id": "t2", "project": {"id": "p1", "name": "Work"}},
        {"id": "t3", "project": {"id": "p1", "name": "Work"}},
    ]
    maps = {"space": {"s1": "Personal"}, "project": {"p1": "Work"}, "list": {}}
    grouped = group_tasks_by_list(tasks, name_maps=maps)
    # Sorted by kind then name: project Work, space Personal
    assert [(r.kind, r.name, c) for r, c in grouped] == [("project", "Work", 2), ("space", "Personal", 1)]


def test_matches_list_name_is_case_insensitive_and_supports_substring():
    assert matches_list_name("Work", "work") is True
    assert matches_list_name("Holiday Planning", "holiday") is True
    assert matches_list_name("Groceries", "work") is False


def test_matches_container_id_is_case_insensitive_exact_match():
    assert matches_container_id("INBOX", "inbox") is True
    assert matches_container_id("abc-123@morgen.so", "ABC-123@MORGEN.SO") is True
    assert matches_container_id("abc-123", "abc") is False
