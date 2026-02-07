"""
Task Lists

Helpers for extracting and grouping "task list" information from Morgen tasks.

The Morgen API payload can evolve, and integrations may represent list-like
containers differently. This module uses conservative heuristics and only
enables list UX when it can reliably derive a list id/name.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TaskListRef:
    """A reference to the list/container a task belongs to."""

    kind: str | None  # "list" | "project" | "space" | None
    list_id: str | None
    name: str | None

    @property
    def key(self) -> str | None:
        """Stable grouping key (includes kind; prefer id, else lowercase name)."""
        kind = (self.kind or "").strip().lower() or "unknown"
        if self.list_id:
            return f"{kind}:id:{self.list_id}"
        if self.name:
            return f"{kind}:name:{self.name.strip().lower()}"
        return None


def build_container_name_maps(api_response: dict) -> dict[str, dict[str, str]]:
    """
    Build name lookup maps from a Morgen API response.

    Expected shapes (best-effort):
      api_response["data"]["lists"]    = [{"id": "...", "name": "..."}, ...]
      api_response["data"]["taskLists"] = [{"id": "...", "name": "..."}, ...]
      api_response["data"]["projects"] = [{"id": "...", "name": "..."}, ...]
      api_response["data"]["spaces"]   = [{"id": "...", "name": "..."}, ...]
    """
    maps: dict[str, dict[str, str]] = {"list": {}, "project": {}, "space": {}}
    if not isinstance(api_response, dict):
        return maps
    data = api_response.get("data")
    if not isinstance(data, dict):
        return maps

    def _ingest(kind: str, items):
        if not isinstance(items, list):
            return
        for it in items:
            if not isinstance(it, dict):
                continue
            item_id = (it.get("id") or "").strip()
            name = (it.get("name") or "").strip()
            if item_id and name:
                maps[kind][item_id] = name

    _ingest("list", data.get("lists"))
    _ingest("list", data.get("taskLists"))
    _ingest("list", data.get("tasklists"))
    _ingest("project", data.get("projects"))
    _ingest("space", data.get("spaces"))
    return maps


def get_task_list_ref(task: dict, *, name_maps: dict[str, dict[str, str]] | None = None) -> TaskListRef:
    """
    Best-effort extraction of list/container identity from a task dict.

    Supported patterns (in priority order):
      - task["list"] = {"id": "...", "name": "..."}
      - task["project"] / task["space"] = {"id": "...", "name": "..."}
      - task["taskListId"] (name resolved via maps only)
      - task["integrationId"] (fallback only)
      - If the task has an id but no name, and `name_maps` includes a mapping,
        the name will be resolved from `name_maps`.

    Returns TaskListRef(list_id=None, name=None) when no list info is available.
    """
    if not isinstance(task, dict):
        return TaskListRef(kind=None, list_id=None, name=None)

    name_maps = name_maps or {}

    # Prefer explicit embedded objects in order of "list" -> "project" -> "space"
    for obj_key in ("list", "project", "space"):
        obj = task.get(obj_key)
        if isinstance(obj, dict):
            list_id = (obj.get("id") or "").strip() or None
            name = (obj.get("name") or "").strip() or None
            if list_id or name:
                if not name and list_id:
                    name = (name_maps.get(obj_key) or {}).get(list_id)
                return TaskListRef(kind=obj_key, list_id=list_id, name=name)

    list_id = (task.get("taskListId") or "").strip() if isinstance(task.get("taskListId"), str) else task.get("taskListId")
    list_id = str(list_id).strip() if list_id else None
    if list_id:
        name = (name_maps.get("list") or {}).get(list_id)
        return TaskListRef(kind="list", list_id=list_id, name=name or None)

    # Final fallback for payloads that expose only integration/account-level ids.
    integration_id = task.get("integrationId")
    if integration_id:
        list_id = str(integration_id).strip()
        if list_id:
            return TaskListRef(kind="list", list_id=list_id, name=None)

    return TaskListRef(kind=None, list_id=None, name=None)


def group_tasks_by_list(
    tasks: list[dict],
    *,
    name_maps: dict[str, dict[str, str]] | None = None,
) -> list[tuple[TaskListRef, int]]:
    """
    Group tasks into lists, returning [(TaskListRef, count), ...] sorted by name.

    Tasks without list metadata are ignored.
    """
    counts: dict[str, int] = {}
    refs: dict[str, TaskListRef] = {}

    for task in tasks or []:
        ref = get_task_list_ref(task, name_maps=name_maps)
        key = ref.key
        if not key:
            continue
        counts[key] = counts.get(key, 0) + 1
        refs.setdefault(key, ref)

    def sort_key(item: tuple[str, int]) -> tuple[str, int]:
        key, count = item
        ref = refs.get(key)
        name = (ref.name or "").strip().lower() if ref else ""
        kind = (ref.kind or "").strip().lower() if ref else ""
        return (kind, name, -count)

    grouped = []
    for key, count in sorted(counts.items(), key=sort_key):
        grouped.append((refs[key], count))
    return grouped


def matches_list_name(list_name: str, user_input: str) -> bool:
    """
    Return True when `user_input` looks like it refers to `list_name`.

    Matching is case-insensitive and allows substring matching.
    """
    if not list_name or not user_input:
        return False
    ln = list_name.strip().lower()
    ui = user_input.strip().lower()
    return ln == ui or ui in ln


def matches_container_id(container_id: str, user_input: str) -> bool:
    """
    Return True when `user_input` matches a container id, case-insensitively.
    """
    if not container_id or not user_input:
        return False
    return container_id.strip().lower() == user_input.strip().lower()
