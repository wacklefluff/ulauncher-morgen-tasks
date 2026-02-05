"""
Task Cache

In-memory cache for Morgen tasks with TTL-based expiration.
Minimizes API calls since the list endpoint costs 10 points per request.
"""

import time
import logging

logger = logging.getLogger(__name__)


class TaskCache:
    """In-memory cache for Morgen tasks with TTL."""

    def __init__(self, ttl=600):
        """
        Args:
            ttl: Time-to-live in seconds (default 600 = 10 minutes).
        """
        self.ttl = ttl
        self._cache = None
        self._timestamp = None
        self._last_updated = None  # newest task's 'updated' field, for updatedAfter

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

    def get_last_updated(self):
        """Newest task 'updated' timestamp, for use with updatedAfter param."""
        return self._last_updated
