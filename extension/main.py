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

from src.morgen_api import (
    MorgenAPIClient,
    MorgenAPIError,
    MorgenAuthError,
    MorgenRateLimitError,
    MorgenNetworkError,
)
from src.cache import TaskCache

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
        query = event.get_argument() or ""
        logger.info("Keyword triggered with query: '%s'", query)

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

        try:
            # Cache-first: check cache before making API call
            tasks = extension.cache.get_tasks()

            if tasks is not None:
                cache_status = f"cached {extension.cache.get_age_display()}"
                logger.info("Using cached tasks: %d tasks", len(tasks))
            else:
                logger.info("Cache miss, fetching from API...")
                response = extension.api_client.list_tasks(limit=100)
                extension.cache.set_tasks(response)
                tasks = response.get("data", {}).get("tasks", [])
                cache_status = "fresh"

            # Header item: task count + cache status
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=f'Morgen Tasks ({len(tasks)})',
                description=f'Cache: {cache_status}',
                on_enter=HideWindowAction()
            ))

            # Show first 5 tasks (Phase 2 proof-of-concept; full formatting in Phase 3)
            for task in tasks[:5]:
                title = task.get("title", "Untitled")
                due = task.get("due", "No due date")
                priority = task.get("priority", 0)

                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=title,
                    description=f'Due: {due} | Priority: {priority}',
                    on_enter=HideWindowAction()
                ))

            if len(tasks) > 5:
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name=f'... and {len(tasks) - 5} more tasks',
                    description='Full list and search coming in Phase 3',
                    on_enter=HideWindowAction()
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
            items.extend(self._fallback_to_cache(extension, "Rate limit exceeded"))

        except MorgenNetworkError as e:
            logger.error("Network error: %s", e)
            items.extend(self._fallback_to_cache(extension, "Cannot reach Morgen API"))

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

    def _fallback_to_cache(self, extension, error_msg):
        """Try to show cached data on network/rate-limit errors."""
        items = []
        cached = extension.cache.get_full_response() if extension.cache else None

        if cached:
            tasks = cached.get("data", {}).get("tasks", [])
            age = extension.cache.get_age_display()
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=f'{error_msg} — showing cached data',
                description=f'{len(tasks)} tasks (cached {age})',
                on_enter=HideWindowAction()
            ))
        else:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=error_msg,
                description='No cached data available. Try again later.',
                on_enter=HideWindowAction()
            ))

        return items


if __name__ == '__main__':
    MorgenTasksExtension().run()
