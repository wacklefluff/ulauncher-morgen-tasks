"""
Ulauncher Morgen Tasks Extension
Manage Morgen tasks from Ulauncher - list, search, and create tasks
"""

import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

try:
    from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
except Exception:  # pragma: no cover - optional Ulauncher action
    CopyToClipboardAction = None

from src.morgen_api import (
    MorgenAPIClient,
    MorgenAPIError,
    MorgenAuthError,
    MorgenRateLimitError,
    MorgenNetworkError,
)
from src.cache import TaskCache
from src.formatter import TaskFormatter

logger = logging.getLogger(__name__)


class MorgenTasksExtension(Extension):
    """Main extension class for Morgen Tasks"""

    def __init__(self):
        super(MorgenTasksExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.cache = None
        self.api_client = None
        logger.info("Morgen Tasks Extension initialized")


class KeywordQueryEventListener(EventListener):
    """Handles keyword query events"""

    def on_event(self, event, extension):
        """Handle keyword query event"""
        raw_query = (event.get_argument() or "").strip()
        logger.info("Keyword triggered with query: '%s'", raw_query)

        # Get preferences
        api_key = extension.preferences.get("api_key", "").strip()
        cache_ttl_str = extension.preferences.get("cache_ttl", "600")

        try:
            cache_ttl = int(cache_ttl_str)
        except ValueError:
            cache_ttl = 600

        # No API key → welcome message
        if not api_key:
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Welcome to Morgen Tasks!',
                    description='Please configure your API key in extension preferences',
                    on_enter=HideWindowAction()
                )
            ])

        # Lazy-init client and cache; re-create if API key changed
        if extension.api_client is None or extension.api_client.api_key != api_key:
            extension.api_client = MorgenAPIClient(api_key)
            extension.cache = TaskCache(ttl=cache_ttl)
            logger.info("API client initialized (cache TTL: %ds)", cache_ttl)

        items = []
        formatter = TaskFormatter()

        force_refresh, query = self._parse_query(raw_query)

        try:
            tasks, cache_status = self._get_tasks(extension, force_refresh=force_refresh)

            # Search filtering (title + description)
            filtered_tasks = self._filter_tasks(tasks, query)

            # Header item: task count + cache status (+ quick help)
            enter_hint = "Enter: copy task ID" if CopyToClipboardAction is not None else "Enter: close"
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=f'Morgen Tasks ({len(filtered_tasks)})',
                description=f'Cache: {cache_status} | {enter_hint} | "refresh" or "!" to refresh',
                on_enter=HideWindowAction()
            ))

            if not filtered_tasks:
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name='No tasks found',
                    description='Try a different search term, or run "mg refresh" to fetch latest tasks.',
                    on_enter=HideWindowAction()
                ))
            else:
                for task in filtered_tasks:
                    task_id = task.get("id") or ""
                    on_enter = self._get_task_action(task_id)
                    items.append(ExtensionResultItem(
                        icon='images/icon.png',
                        name=formatter.format_for_display(task),
                        description=formatter.format_subtitle(task),
                        on_enter=on_enter
                    ))

        except MorgenAuthError:
            logger.error("Authentication error")
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Authentication Failed',
                description='Invalid API key. Check extension preferences.',
                on_enter=HideWindowAction()
            ))

        except MorgenRateLimitError:
            logger.warning("Rate limit exceeded")
            items.extend(self._fallback_to_cache(extension, "Rate limit exceeded", query=query))

        except MorgenNetworkError as e:
            logger.error("Network error: %s", e)
            items.extend(self._fallback_to_cache(extension, "Cannot reach Morgen API", query=query))

        except MorgenAPIError as e:
            logger.error("API error: %s", e)
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Morgen API Error',
                description=str(e.message),
                on_enter=HideWindowAction()
            ))

        except Exception as e:
            logger.error("Unexpected error: %s", e, exc_info=True)
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Unexpected Error',
                description=str(e),
                on_enter=HideWindowAction()
            ))

        return RenderResultListAction(items)

    def _parse_query(self, raw_query: str):
        """
        Parse user query for force refresh and search term.

        Supported:
          - "!" or "! <query>" (force refresh)
          - "refresh" or "refresh <query>" (force refresh)
          - otherwise: search query (or empty to list all)
        """
        if not raw_query:
            return False, ""

        if raw_query.startswith("!"):
            return True, raw_query[1:].strip()

        parts = raw_query.split(None, 1)
        if parts and parts[0].lower() == "refresh":
            return True, parts[1].strip() if len(parts) > 1 else ""

        return False, raw_query

    def _get_tasks(self, extension, force_refresh: bool):
        # Cache-first: check cache before making API call
        if force_refresh and extension.cache:
            extension.cache.invalidate()

        tasks = extension.cache.get_tasks() if extension.cache and not force_refresh else None
        if tasks is not None:
            cache_status = f"cached {extension.cache.get_age_display()}"
            logger.info("Using cached tasks: %d tasks", len(tasks))
            return tasks, cache_status

        logger.info("Fetching tasks from API%s...", " (force refresh)" if force_refresh else "")
        response = extension.api_client.list_tasks(limit=100)
        if extension.cache:
            extension.cache.set_tasks(response)
            cache_status = "refreshed" if force_refresh else "fresh"
        else:
            cache_status = "fresh"
        tasks = response.get("data", {}).get("tasks", [])
        return tasks, cache_status

    def _filter_tasks(self, tasks, query: str):
        if not query:
            return tasks

        q = query.lower()
        filtered = []
        for task in tasks:
            title = (task.get("title") or "").lower()
            description = (task.get("description") or "").lower()
            if q in title or q in description:
                filtered.append(task)
        return filtered

    def _get_task_action(self, task_id: str):
        if task_id and CopyToClipboardAction is not None:
            try:
                return CopyToClipboardAction(task_id)
            except Exception:
                return HideWindowAction()
        return HideWindowAction()

    def _fallback_to_cache(self, extension, error_msg, query=""):
        """Try to show cached data on network/rate-limit errors."""
        items = []
        cached = extension.cache.get_full_response() if extension.cache else None
        formatter = TaskFormatter()

        if not cached:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=error_msg,
                description='No cached data available. Try again later.',
                on_enter=HideWindowAction()
            ))
            return items

        tasks = cached.get("data", {}).get("tasks", [])
        filtered_tasks = self._filter_tasks(tasks, query)
        age = extension.cache.get_age_display() if extension.cache else "unknown"

        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f'{error_msg} — showing cached data',
            description=f'{len(filtered_tasks)} tasks (cache: {age})',
            on_enter=HideWindowAction()
        ))

        if not filtered_tasks:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='No tasks found',
                description='Try a different search term, or run "mg refresh" later.',
                on_enter=HideWindowAction()
            ))
            return items

        for task in filtered_tasks:
            task_id = task.get("id") or ""
            on_enter = self._get_task_action(task_id)
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=formatter.format_for_display(task),
                description=formatter.format_subtitle(task),
                on_enter=on_enter
            ))

        return items


if __name__ == '__main__':
    MorgenTasksExtension().run()
