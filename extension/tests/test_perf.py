"""Performance tests for search optimization."""

import sys
import time
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


def test_search_with_index():
    """Test search performance with pre-computed index."""
    cache = TaskCache(ttl=600, cache_path=None)

    # Generate enough tasks to cross the indexing threshold.
    mock_response = generate_mock_tasks(250)
    cache.set_tasks(mock_response)

    tasks = cache.get_tasks()
    search_index = cache.get_search_index()

    assert tasks is not None, "Tasks should be cached"
    assert search_index is not None, "Search index should exist"
    assert len(search_index) == 250, "Search index should have 250 entries"

    # Verify index content
    assert "task-0" in search_index
    title, desc = search_index["task-0"]
    assert "task number 0" in title
    assert "description for task 0" in desc

    print(f"✓ Search index built correctly with {len(search_index)} entries")


def test_search_index_skipped_below_threshold():
    """Search index should be skipped for small task sets (<200)."""
    cache = TaskCache(ttl=600, cache_path=None)
    cache.set_tasks(generate_mock_tasks(100))

    tasks = cache.get_tasks()
    search_index = cache.get_search_index()

    assert tasks is not None, "Tasks should be cached"
    assert len(tasks) == 100
    assert search_index is None, "Search index should be disabled below threshold"


def test_search_performance():
    """Compare search performance with and without index."""
    cache = TaskCache(ttl=600, cache_path=None)

    # Generate 500 tasks
    mock_response = generate_mock_tasks(500)
    cache.set_tasks(mock_response)

    tasks = cache.get_tasks()
    search_index = cache.get_search_index()
    query = "task number 42"
    q = query.lower()

    iterations = 1000

    # Without index (computing lowercase each time)
    start = time.perf_counter()
    for _ in range(iterations):
        filtered = []
        for task in tasks:
            title = (task.get("title") or "").lower()
            description = (task.get("description") or "").lower()
            if q in title or q in description:
                filtered.append(task)
    without_index_ms = (time.perf_counter() - start) * 1000

    # With index
    start = time.perf_counter()
    for _ in range(iterations):
        filtered = []
        for task in tasks:
            task_id = task.get("id")
            indexed = search_index.get(task_id)
            if indexed:
                title, description = indexed
            else:
                title = (task.get("title") or "").lower()
                description = (task.get("description") or "").lower()
            if q in title or q in description:
                filtered.append(task)
    with_index_ms = (time.perf_counter() - start) * 1000

    improvement = ((without_index_ms - with_index_ms) / without_index_ms) * 100

    print(f"Search performance ({iterations} iterations, {len(tasks)} tasks):")
    print(f"  Without index: {without_index_ms:.2f}ms")
    print(f"  With index:    {with_index_ms:.2f}ms")
    print(f"  Improvement:   {improvement:.1f}%")

    # The indexed version should be faster (or at least not slower)
    assert with_index_ms <= without_index_ms * 1.1, "Indexed search should not be significantly slower"
    print("✓ Performance test passed")


if __name__ == "__main__":
    test_search_with_index()
    test_search_performance()
    print("\n✓ All performance tests passed!")
