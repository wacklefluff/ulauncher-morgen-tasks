"""
Ulauncher Morgen Tasks Extension
Manage Morgen tasks from Ulauncher - list, search, and create tasks
"""

import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

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
from src.date_parser import DateParser, DateParseError

logger = logging.getLogger(__name__)


class MorgenTasksExtension(Extension):
    """Main extension class for Morgen Tasks"""

    def __init__(self):
        super(MorgenTasksExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
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

        # Help / housekeeping commands
        help_items = self._maybe_build_help_flow(raw_query)
        if help_items is not None:
            return RenderResultListAction(help_items)

        clear_items = self._maybe_clear_cache_flow(raw_query, extension)
        if clear_items is not None:
            return RenderResultListAction(clear_items)

        # Phase 4: create task flow (mg new ...)
        create_items = self._maybe_build_create_flow(raw_query)
        if create_items is not None:
            return RenderResultListAction(create_items)

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
                description=f'Cache: {cache_status} | {enter_hint} | "help" for commands | "refresh"/"!" to refresh',
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

    def _maybe_build_help_flow(self, raw_query: str):
        if not raw_query:
            return None

        normalized = raw_query.strip().lower()
        parts = normalized.split(None, 1)
        head = parts[0] if parts else ""
        if head not in {"help", "?", "h"}:
            return None

        examples = [
            ("List tasks", "mg"),
            ("Search tasks", "mg <query>"),
            ("Force refresh", "mg !   or   mg refresh"),
            ("Create task", "mg new <title> [@due] [!priority]"),
            ("Clear cache", "mg clear"),
        ]

        due_examples = [
            "@today",
            "@tomorrow",
            "@next-mon",
            "@2026-02-10",
            "@2026-02-10T15:30",
            "@15:30",
            "@3pm",
        ]

        items = [
            ExtensionResultItem(
                icon="images/icon.png",
                name="Morgen Tasks — Help",
                description='Commands and examples. Tip: type "mg" then the example.',
                on_enter=HideWindowAction(),
            )
        ]

        for label, example in examples:
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name=label,
                description=example,
                on_enter=HideWindowAction(),
            ))

        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Due date formats",
            description=" ".join(due_examples),
            on_enter=HideWindowAction(),
        ))

        enter_hint = "copies task ID" if CopyToClipboardAction is not None else "closes the window"
        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Task item Enter behavior",
            description=f"Pressing Enter on a task {enter_hint}.",
            on_enter=HideWindowAction(),
        ))

        return items

    def _maybe_clear_cache_flow(self, raw_query: str, extension):
        if not raw_query:
            return None

        normalized = raw_query.strip().lower()
        if normalized in {"clear", "cache-clear", "cacheclear", "reset"} or normalized == "cache clear":
            if extension.cache:
                extension.cache.invalidate()
            return [ExtensionResultItem(
                icon="images/icon.png",
                name="Cache cleared",
                description='Run "mg" to reload tasks (or "mg refresh" to force an API fetch).',
                on_enter=HideWindowAction(),
            )]

        return None

    def _maybe_build_create_flow(self, raw_query: str):
        """
        If query starts with 'new' or 'add', return items for the create flow.
        Otherwise return None.
        """
        if not raw_query:
            return None

        parts = raw_query.split(None, 1)
        if not parts:
            return None

        head = parts[0].lower()
        if head not in {"new", "add"}:
            return None

        rest = parts[1].strip() if len(parts) > 1 else ""
        items = []

        if not rest:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Create task: missing title',
                description='Usage: mg new <title> [@due] [!priority]',
                on_enter=HideWindowAction()
            ))
            return items

        parse = self._parse_create_args(rest)
        if parse.get("error"):
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='Cannot create task',
                description=parse["error"],
                on_enter=HideWindowAction()
            ))
            return items

        title = parse["title"]
        due = parse.get("due")
        due_display = parse.get("due_display")
        priority = parse.get("priority", 0)

        summary = []
        if due:
            summary.append(f"Due: {due_display}")
        if priority:
            summary.append(f"Priority: {priority}")
        if not summary:
            summary.append("No due date / priority")

        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Create Morgen task',
            description=' | '.join(summary),
            on_enter=HideWindowAction()
        ))

        payload = {
            "action": "create_task",
            "title": title,
            "due": due,
            "priority": priority,
        }

        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f'Create: {title}',
            description='Press Enter to create this task',
            on_enter=ExtensionCustomAction(payload, keep_app_open=True)
        ))

        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name='Cancel',
            description='Close without creating a task',
            on_enter=HideWindowAction()
        ))

        return items

    def _parse_create_args(self, rest: str) -> dict:
        """
        Parse create args from the part after 'new' / 'add'.

        Supports:
          - @<due> (e.g. @today, @tomorrow, @next-mon, @2026-02-10, @2026-02-10T15:30, @15:30)
          - !<priority> (1..9), e.g. !3
        """
        tokens = rest.split()
        title_parts = []
        due_token = None
        priority = 0

        for token in tokens:
            if token.startswith("@") and len(token) > 1 and due_token is None:
                due_token = token[1:]
                continue
            if token.startswith("!") and len(token) > 1 and token[1:].isdigit():
                p = int(token[1:])
                if 0 <= p <= 9:
                    priority = p
                    continue
            title_parts.append(token)

        title = " ".join(title_parts).strip()
        if not title:
            return {"error": "Missing title. Usage: mg new <title> [@due] [!priority]"}

        parsed = {"title": title, "priority": priority}

        if due_token:
            try:
                due_parsed = DateParser().parse(due_token)
                parsed["due"] = due_parsed.due
                parsed["due_display"] = due_parsed.display
            except DateParseError as e:
                return {"error": f"Invalid due date '{due_token}': {e}"}

        return parsed

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


class ItemEnterEventListener(EventListener):
    """Handles item enter events for custom actions."""

    def on_event(self, event, extension):
        data = None
        try:
            data = event.get_data()
        except Exception:
            data = getattr(event, "data", None)

        if not isinstance(data, dict) or not data.get("action"):
            return HideWindowAction()

        if data.get("action") != "create_task":
            return HideWindowAction()

        title = (data.get("title") or "").strip()
        due = data.get("due")
        try:
            priority = int(data.get("priority") or 0)
        except Exception:
            priority = 0

        api_key = extension.preferences.get("api_key", "").strip()
        cache_ttl_str = extension.preferences.get("cache_ttl", "600")
        try:
            cache_ttl = int(cache_ttl_str)
        except ValueError:
            cache_ttl = 600

        if not api_key:
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Cannot create task',
                description='Missing API key. Set it in extension preferences.',
                on_enter=HideWindowAction()
            )])

        # Ensure client/cache are initialized
        if extension.api_client is None or extension.api_client.api_key != api_key:
            extension.api_client = MorgenAPIClient(api_key)
        if extension.cache is None:
            extension.cache = TaskCache(ttl=cache_ttl)

        try:
            resp = extension.api_client.create_task(title=title, due=due, priority=priority)
            task_id = resp.get("data", {}).get("id") or ""

            if extension.cache:
                extension.cache.invalidate()

            description = f"Created (id: {task_id})" if task_id else "Created"
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Task created',
                description=description,
                on_enter=HideWindowAction()
            )])

        except MorgenAuthError:
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Authentication Failed',
                description='Invalid API key. Check extension preferences.',
                on_enter=HideWindowAction()
            )])

        except MorgenRateLimitError:
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Rate limit exceeded',
                description='Try again later.',
                on_enter=HideWindowAction()
            )])

        except (MorgenNetworkError, MorgenAPIError) as e:
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Create failed',
                description=str(getattr(e, "message", e)),
                on_enter=HideWindowAction()
            )])

        except Exception as e:
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Unexpected error',
                description=str(e),
                on_enter=HideWindowAction()
            )])


if __name__ == '__main__':
    MorgenTasksExtension().run()
