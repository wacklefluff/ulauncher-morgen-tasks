"""
Ulauncher Morgen Tasks Extension
Manage Morgen tasks from Ulauncher - list, search, and create tasks
"""

import logging
import os
import time
from logging.handlers import RotatingFileHandler
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

try:
    from ulauncher.api.shared.action.OpenAction import OpenAction
except Exception:  # pragma: no cover - optional Ulauncher action
    OpenAction = None

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

_LOG_FILE_NAME = "runtime.log"
_RUNTIME_LOG_HINT = "extension/logs/runtime.log"


def _setup_file_logging():
    """
    Attach a rotating file handler so logs persist outside `ulauncher -v`.

    Safe to call multiple times; it will only add one handler per log file path.
    """
    try:
        base_dir = os.path.dirname(__file__)
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, _LOG_FILE_NAME)

        root = logging.getLogger()

        for handler in root.handlers:
            if isinstance(handler, RotatingFileHandler) and getattr(handler, "baseFilename", None) == log_path:
                return

        handler = RotatingFileHandler(
            log_path,
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
        )
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        root.addHandler(handler)

        if root.level > logging.INFO:
            root.setLevel(logging.INFO)

        logger.info("File logging enabled: %s", log_path)
    except Exception:
        # Logging should never break extension execution.
        pass


class MorgenTasksExtension(Extension):
    """Main extension class for Morgen Tasks"""

    def __init__(self):
        super(MorgenTasksExtension, self).__init__()
        _setup_file_logging()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.cache = None
        self.api_client = None
        self.last_manual_refresh_at = 0.0
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
            logger.warning("Missing API key (showing welcome screen)")
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Welcome to Morgen Tasks!',
                    description=f'Configure your API key in extension preferences. Logs: {_RUNTIME_LOG_HINT}',
                    on_enter=HideWindowAction()
                ),
                *self._runtime_log_access_items(),
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
            logger.info("Showing help view")
            return RenderResultListAction(help_items)

        clear_items = self._maybe_clear_cache_flow(raw_query, extension)
        if clear_items is not None:
            logger.info("Cache clear requested")
            return RenderResultListAction(clear_items)

        # Phase 4: create task flow (mg new ...)
        create_items = self._maybe_build_create_flow(raw_query)
        if create_items is not None:
            logger.info("Showing create-task preview")
            return RenderResultListAction(create_items)

        force_refresh, query, refresh_prefix_used = self._parse_query(raw_query)

        try:
            tasks, cache_status = self._get_tasks(extension, force_refresh=force_refresh)

            # Search filtering (title + description)
            filtered_tasks = self._filter_tasks(tasks, query)

            if refresh_prefix_used:
                items.append(self._refresh_prefix_notice(extension))

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
            logger.warning("Authentication failed (invalid API key)")
            items.extend(self._error_items(
                title="Authentication Failed",
                description="Your API key was rejected by Morgen.",
                suggestions=[
                    "Open extension preferences and set a valid API key.",
                    'Then run "mg refresh" (one-shot) to fetch tasks.',
                    f"See logs: {_RUNTIME_LOG_HINT}",
                ],
            ))

        except MorgenRateLimitError:
            logger.warning("Rate limit exceeded (429)")
            items.extend(self._fallback_to_cache(
                extension,
                "Rate limit exceeded",
                query=query,
                suggestions=[
                    "Wait a minute and try again.",
                    "Avoid using refresh repeatedly; refresh is one-shot.",
                    'Use cached results, or increase "Cache Duration" preference.',
                ],
            ))

        except MorgenNetworkError as e:
            logger.warning("Network error: %s", e)
            items.extend(self._fallback_to_cache(
                extension,
                "Cannot reach Morgen API",
                query=query,
                suggestions=[
                    "Check your internet connection/VPN.",
                    'Try "mg" again, or use cached results if available.',
                    f"See logs: {_RUNTIME_LOG_HINT}",
                ],
            ))

        except MorgenAPIError as e:
            logger.warning("API error: %s", getattr(e, "message", e))
            items.extend(self._error_items(
                title="Morgen API Error",
                description=str(getattr(e, "message", e)),
                suggestions=[f"See logs: {_RUNTIME_LOG_HINT}"],
            ))

        except Exception as e:
            logger.exception("Unexpected error")
            items.extend(self._error_items(
                title="Unexpected Error",
                description=str(e),
                suggestions=[
                    'Try "mg clear" then "mg refresh".',
                    f"See logs: {_RUNTIME_LOG_HINT}",
                ],
            ))

        return RenderResultListAction(items)

    def _maybe_build_help_flow(self, raw_query: str):
        if not raw_query:
            return None

        normalized = raw_query.strip().lower()
        # Only trigger help when it's the entire query, so searches like
        # "help regression test" still behave like normal search.
        if normalized not in {"help", "?", "h"}:
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

        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Runtime logs",
            description=_RUNTIME_LOG_HINT,
            on_enter=HideWindowAction(),
        ))

        items.extend(self._runtime_log_access_items())

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
          - "!" (force refresh; one-shot)
          - "refresh" (force refresh; one-shot)
          - Any extra text after "!" / "refresh" is treated as normal search,
            to avoid accidentally force-refreshing on every keystroke.
          - otherwise: search query (or empty to list all)
        """
        if not raw_query:
            return False, "", False

        stripped = raw_query.strip()
        if stripped == "!":
            return True, "", False

        if stripped.startswith("!"):
            # Do not force refresh if user keeps typing after "!"
            return False, stripped[1:].strip(), True

        parts = stripped.split(None, 1)
        if parts and parts[0].lower() == "refresh":
            if len(parts) == 1:
                return True, "", False
            # Do not force refresh if user keeps typing after "refresh"
            return False, parts[1].strip(), True

        return False, raw_query, False

    def _get_tasks(self, extension, force_refresh: bool):
        # Cache-first: check cache before making API call
        if force_refresh and extension.cache:
            logger.info("Force refresh requested (invalidating cache)")
            extension.cache.invalidate()

        tasks = extension.cache.get_tasks() if extension.cache and not force_refresh else None
        if tasks is not None:
            cache_status = f"cached {extension.cache.get_age_display()}"
            logger.info("Using cached tasks: %d tasks (age=%s)", len(tasks), extension.cache.get_age_display())
            return tasks, cache_status

        logger.info("Fetching tasks from API%s...", " (force refresh)" if force_refresh else "")
        response = extension.api_client.list_tasks(limit=100)
        if extension.cache:
            extension.cache.set_tasks(response)
            cache_status = "refreshed" if force_refresh else "fresh"
        else:
            cache_status = "fresh"
        if force_refresh:
            extension.last_manual_refresh_at = time.time()
        tasks = response.get("data", {}).get("tasks", [])
        logger.info("API tasks loaded: %d tasks", len(tasks))
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

    def _fallback_to_cache(self, extension, error_msg, query="", suggestions=None):
        """Try to show cached data on network/rate-limit errors."""
        items = []
        cached = extension.cache.get_full_response() if extension.cache else None
        formatter = TaskFormatter()

        if not cached:
            logger.info("No cached response available for fallback")
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=error_msg,
                description='No cached data available. Try again later.',
                on_enter=HideWindowAction()
            ))
            items.extend(self._runtime_log_access_items())
            items.extend(self._suggestion_items(suggestions))
            return items

        tasks = cached.get("data", {}).get("tasks", [])
        filtered_tasks = self._filter_tasks(tasks, query)
        age = extension.cache.get_age_display() if extension.cache else "unknown"
        logger.info("Fallback to cached response: %d tasks (cache age=%s)", len(tasks), age)

        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f'{error_msg} — showing cached data',
            description=f'{len(filtered_tasks)} tasks (cache: {age})',
            on_enter=HideWindowAction()
        ))
        items.extend(self._suggestion_items(suggestions))

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

    def _error_items(self, title: str, description: str, suggestions=None):
        items = [
            ExtensionResultItem(
                icon="images/icon.png",
                name=title,
                description=description,
                on_enter=HideWindowAction(),
            )
        ]
        items.extend(self._runtime_log_access_items())
        items.extend(self._suggestion_items(suggestions))
        return items

    def _suggestion_items(self, suggestions):
        if not suggestions:
            return []
        items = []
        for suggestion in suggestions:
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name="Tip",
                description=str(suggestion),
                on_enter=HideWindowAction(),
            ))
        return items

    def _runtime_log_access_items(self):
        items = []
        abs_path = os.path.join(os.path.dirname(__file__), "logs", _LOG_FILE_NAME)

        if OpenAction is not None:
            try:
                items.append(ExtensionResultItem(
                    icon="images/icon.png",
                    name="Open runtime log",
                    description=abs_path,
                    on_enter=OpenAction(abs_path),
                ))
            except Exception:
                pass

        if CopyToClipboardAction is not None:
            try:
                items.append(ExtensionResultItem(
                    icon="images/icon.png",
                    name="Copy log path",
                    description=abs_path,
                    on_enter=CopyToClipboardAction(abs_path),
                ))
            except Exception:
                pass

        return items

    def _refresh_prefix_notice(self, extension):
        now = time.time()
        recently_refreshed = bool(extension.last_manual_refresh_at and (now - extension.last_manual_refresh_at) < 15)
        if recently_refreshed:
            return ExtensionResultItem(
                icon='images/icon.png',
                name='Cache refreshed (one-shot)',
                description='You kept typing after "refresh"/"!": now searching without refreshing each keystroke.',
                on_enter=HideWindowAction()
            )
        return ExtensionResultItem(
            icon='images/icon.png',
            name='Refresh is one-shot',
            description='Only exact "mg refresh" or "mg !" refreshes. Remove the prefix to search normally.',
            on_enter=HideWindowAction()
        )


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
            items = [ExtensionResultItem(
                icon='images/icon.png',
                name='Cannot create task',
                description=f'Missing API key. Set it in extension preferences. Logs: {_RUNTIME_LOG_HINT}',
                on_enter=HideWindowAction()
            )]

            abs_path = os.path.join(os.path.dirname(__file__), "logs", _LOG_FILE_NAME)
            if OpenAction is not None:
                try:
                    items.append(ExtensionResultItem(
                        icon="images/icon.png",
                        name="Open runtime log",
                        description=abs_path,
                        on_enter=OpenAction(abs_path),
                    ))
                except Exception:
                    pass

            if CopyToClipboardAction is not None:
                try:
                    items.append(ExtensionResultItem(
                        icon="images/icon.png",
                        name="Copy log path",
                        description=abs_path,
                        on_enter=CopyToClipboardAction(abs_path),
                    ))
                except Exception:
                    pass

            return RenderResultListAction(items)

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
            logger.info("Task created (id=%s)", task_id or "unknown")
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Task created',
                description=description,
                on_enter=HideWindowAction()
            )])

        except MorgenAuthError:
            logger.warning("Create task failed: auth error")
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Authentication Failed',
                description='Invalid API key. Check extension preferences.',
                on_enter=HideWindowAction()
            )])

        except MorgenRateLimitError:
            logger.warning("Create task failed: rate limit")
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Rate limit exceeded',
                description=f'Try again later. Logs: {_RUNTIME_LOG_HINT}',
                on_enter=HideWindowAction()
            )])

        except (MorgenNetworkError, MorgenAPIError) as e:
            logger.warning("Create task failed: %s", getattr(e, "message", e))
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Create failed',
                description=f'{str(getattr(e, "message", e))} (see {_RUNTIME_LOG_HINT})',
                on_enter=HideWindowAction()
            )])

        except Exception as e:
            logger.exception("Create task failed: unexpected error")
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Unexpected error',
                description=f'{str(e)} (see {_RUNTIME_LOG_HINT})',
                on_enter=HideWindowAction()
            )])


if __name__ == '__main__':
    MorgenTasksExtension().run()
