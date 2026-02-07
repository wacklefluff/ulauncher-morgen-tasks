import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dev_dummy_tasks import (  # noqa: E402
    DEFAULT_DUMMY_TITLE_PREFIX,
    build_dummy_task_specs,
)


def test_build_dummy_task_specs_respects_count_and_prefix():
    specs = build_dummy_task_specs(count=90, title_prefix=DEFAULT_DUMMY_TITLE_PREFIX)
    assert len(specs) == 90
    assert specs[0]["title"].startswith(DEFAULT_DUMMY_TITLE_PREFIX)
    assert specs[-1]["title"].startswith(DEFAULT_DUMMY_TITLE_PREFIX)


def test_build_dummy_task_specs_varies_priority_and_due():
    specs = build_dummy_task_specs(count=30)
    priorities = {item["priority"] for item in specs}
    assert priorities == {0, 1, 5, 9}

    due_values = [item["due"] for item in specs]
    assert any(d is None for d in due_values)
    assert any(isinstance(d, str) and len(d) == 19 for d in due_values if d is not None)
