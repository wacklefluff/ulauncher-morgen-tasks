import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cache import TaskCache


def test_cache_extracts_container_name_maps_from_full_response(tmp_path):
    cache_path = tmp_path / "cache.json"
    c = TaskCache(ttl=600, cache_path=str(cache_path))
    api_response = {
        "data": {
            "tasks": [{"id": "t1", "title": "Task", "listId": "l1"}],
            "lists": [{"id": "l1", "name": "Inbox"}],
            "projects": [{"id": "p1", "name": "Work"}],
            "spaces": [{"id": "s1", "name": "Personal"}],
        }
    }
    c.set_tasks(api_response)
    maps = c.get_container_name_maps()
    assert maps["list"]["l1"] == "Inbox"
    assert maps["project"]["p1"] == "Work"
    assert maps["space"]["s1"] == "Personal"

