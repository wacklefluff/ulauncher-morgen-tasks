"""Large dataset cache/search behavior tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cache import TaskCache


def generate_mock_tasks(n):
    """Generate n mock tasks for testing."""
    tasks = []
    for i in range(n):
        tasks.append({
            "id": f"task-{i}",
            "title": f"Task number {i} with some text",
            "description": f"Description for task {i} with more details and content",
            "due": "2026-02-10T09:00:00",
            "priority": i % 10,
        })
    return {"data": {"tasks": tasks}}


def _filter_tasks(tasks, query: str):
    words = query.lower().split()
    filtered = []
    for task in tasks:
        title = (task.get("title") or "").lower()
        description = (task.get("description") or "").lower()
        text = title + " " + description
        if all(w in text for w in words):
            filtered.append(task)
    return filtered


def test_cache_handles_500_tasks():
    """Cache should store and return large task lists."""
    cache = TaskCache(ttl=600, cache_path=None)
    mock_response = generate_mock_tasks(500)
    cache.set_tasks(mock_response)

    tasks = cache.get_tasks()
    assert tasks is not None, "Tasks should be cached"
    assert len(tasks) == 500


def test_on_the_fly_search_matches_expected_results():
    """On-the-fly search should still find the expected task."""
    cache = TaskCache(ttl=600, cache_path=None)
    cache.set_tasks(generate_mock_tasks(500))
    tasks = cache.get_tasks()
    assert tasks is not None

    result = _filter_tasks(tasks, "number 42")
    assert result
    assert all("42" in ((t.get("title") or "") + (t.get("description") or "")) for t in result)


if __name__ == "__main__":
    test_cache_handles_500_tasks()
    test_on_the_fly_search_matches_expected_results()
    print("\n✓ Large dataset tests passed!")
