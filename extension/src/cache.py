"""
Task Cache

In-memory cache for Morgen tasks with TTL-based expiration.
Minimizes API calls since the list endpoint costs 10 points per request.
"""

from __future__ import annotations

import json
import os
import time
import logging

logger = logging.getLogger(__name__)

_DEFAULT_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "ulauncher-morgen-tasks")
_DEFAULT_CACHE_FILE = os.path.join(_DEFAULT_CACHE_DIR, "tasks_cache.json")


class TaskCache:
    """In-memory cache for Morgen tasks with TTL."""

    def __init__(self, ttl=600, cache_path: str | None = None):
        """
        Args:
            ttl: Time-to-live in seconds (default 600 = 10 minutes).
            cache_path: Optional path to persist cache to disk (JSON).
        """
        self.ttl = ttl
        self.cache_path = cache_path or _DEFAULT_CACHE_FILE
        self._cache = None
        self._timestamp = None
        self._last_updated = None  # newest task's 'updated' field, for updatedAfter

        self._load_from_disk()

    def get_tasks(self):
        """Return cached task list if fresh, else None."""
        if self._cache is None:
            logger.debug("Cache miss: empty")
            return None

        if not self.is_fresh():
            logger.debug("Cache expired (age: %.1fs, TTL: %ds)", self.get_age(), self.ttl)
            return None

        tasks = self._cache.get("data", {}).get("tasks", [])
        logger.debug("Cache hit: %d tasks (age: %.1fs)", len(tasks), self.get_age())
        return tasks

    def get_full_response(self):
        """Return full cached API response if any data exists (even if expired)."""
        return self._cache

    def get_container_name_maps(self) -> dict[str, dict[str, str]]:
        """
        Best-effort mapping of container ids -> names.

        Expected (but not guaranteed) in Morgen API responses:
          - data.lists:    [{id, name}, ...]
          - data.projects: [{id, name}, ...]
          - data.spaces:   [{id, name}, ...]
        """
        try:
            from src.task_lists import build_container_name_maps
        except Exception:  # pragma: no cover - test/import environment differences
            from task_lists import build_container_name_maps

        return build_container_name_maps(self._cache or {})

    def set_tasks(self, api_response):
        """
        Store an API response in the cache.

        Args:
            api_response: Full response dict from MorgenAPIClient.list_tasks().
        """
        self._cache = api_response
        self._timestamp = time.time()

        tasks = api_response.get("data", {}).get("tasks", [])
        updated_times = [t.get("updated") for t in tasks if t.get("updated")]
        if updated_times:
            self._last_updated = max(updated_times)

        logger.info("Cache updated: %d tasks stored", len(tasks))
        self._save_to_disk()

    def is_fresh(self):
        """True if cache exists and is within TTL."""
        if self._cache is None or self._timestamp is None:
            return False
        return (time.time() - self._timestamp) < self.ttl

    def get_age(self):
        """Cache age in seconds, or 0 if empty."""
        if self._timestamp is None:
            return 0.0
        return time.time() - self._timestamp

    def get_age_display(self):
        """Human-readable cache age: 'fresh', '45s ago', '2m ago', 'expired'."""
        if self._cache is None or self._timestamp is None:
            return "expired"
        if not self.is_fresh():
            return "expired"

        age = self.get_age()
        if age < 10:
            return "fresh"
        elif age < 60:
            return f"{int(age)}s ago"
        elif age < 3600:
            return f"{int(age / 60)}m ago"
        else:
            return f"{int(age / 3600)}h ago"

    def invalidate(self):
        """Clear the cache (call after creating/updating tasks)."""
        logger.info("Cache invalidated")
        self._cache = None
        self._timestamp = None
        self._last_updated = None
        self._delete_from_disk()

    def get_last_updated(self):
        """Newest task 'updated' timestamp, for use with updatedAfter param."""
        return self._last_updated

    def _load_from_disk(self):
        if not self.cache_path:
            return
        try:
            if not os.path.exists(self.cache_path):
                return
            with open(self.cache_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            cached = payload.get("cache")
            timestamp = payload.get("timestamp")
            if not isinstance(cached, dict) or not isinstance(timestamp, (int, float)):
                return
            self._cache = cached
            self._timestamp = float(timestamp)

            tasks = cached.get("data", {}).get("tasks", [])
            updated_times = [t.get("updated") for t in tasks if t.get("updated")]
            self._last_updated = max(updated_times) if updated_times else None

            logger.info("Loaded cache from disk: %d tasks", len(tasks))
        except Exception as e:
            logger.debug("Failed to load cache from disk: %s", e)

    def _save_to_disk(self):
        if not self.cache_path or self._cache is None or self._timestamp is None:
            return
        try:
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            payload = {"timestamp": self._timestamp, "cache": self._cache}
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(payload, f)
        except Exception as e:
            logger.debug("Failed to save cache to disk: %s", e)

    def _delete_from_disk(self):
        if not self.cache_path:
            return
        try:
            if os.path.exists(self.cache_path):
                os.remove(self.cache_path)
        except Exception as e:
            logger.debug("Failed to delete cache file: %s", e)
