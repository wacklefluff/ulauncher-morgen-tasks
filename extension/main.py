"""
Ulauncher Morgen Tasks Extension
Manage Morgen tasks from Ulauncher - list, search, and create tasks
"""

import logging
import os
import time
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
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
try:
    from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
except Exception:  # pragma: no cover - optional Ulauncher action
    SetUserQueryAction = None

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
from src.dev_dummy_tasks import (
    DEFAULT_DUMMY_TASK_COUNT,
    DEFAULT_DUMMY_TITLE_PREFIX,
    build_dummy_task_specs,
)
from src.task_lists import (
    build_manual_list_name_maps,
    group_tasks_by_list,
    get_task_list_ref,
    matches_list_name,
    matches_container_id,
)
from src.task_filters import (
    parse_query_filters,
    matches_task_filters,
    extract_due_filter_fragment,
    get_due_filter_suggestions,
    rewrite_due_filter_query,
)

logger = logging.getLogger(__name__)

_LOG_FILE_NAME = "runtime.log"
_MAX_NORMAL = 5       # Max results in normal (detailed) display mode
_MAX_CONDENSED = 15   # Max results in condensed (compact) display mode
_TASK_LIST_API_LIMIT = 100
_DUMMY_COMPLETE_BATCH_SIZE = 30
_DUE_AUTOCOMPLETE_MAX = 8
_DUE_FILTER_AUTOCOMPLETE_MAX = 6
_DUE_SUGGESTION_VALUES = (
    "today",
    "tomorrow",
    "yesterday",
    "next-week",
    "next-month",
    "mon",
    "tue",
    "wed",
    "thu",
    "fri",
    "sat",
    "sun",
    "next-mon",
    "next-tue",
    "next-wed",
    "next-thu",
    "next-fri",
    "next-sat",
    "next-sun",
    "09:00",
    "15:30",
    "3pm",
    "noon",
    "midnight",
    "2026-02-10",
    "2026-02-10T15:30",
)


@contextmanager
def _timed(label: str):
    """Context manager for timing code blocks. Logs at DEBUG level."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.debug("PERF %s: %.2fms", label, elapsed_ms)
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

        triggered_keyword = self._get_triggered_keyword(event)

        # Get preferences
        api_key = extension.preferences.get("api_key", "").strip()
        cache_ttl_str = extension.preferences.get("cache_ttl", "600")
        new_task_keyword = (extension.preferences.get("mg_new_keyword") or "").strip()

        try:
            cache_ttl = int(cache_ttl_str)
        except ValueError:
            cache_ttl = 600

        # Help and debug commands work without API key
        help_items = self._maybe_build_help_flow(raw_query, extension)
        if help_items is not None:
            logger.info("Showing help view")
            return RenderResultListAction(help_items)

        debug_items = self._maybe_build_debug_flow(raw_query)
        if debug_items is not None:
            logger.info("Showing debug view")
            return RenderResultListAction(debug_items)

        # No API key → welcome message
        if not api_key:
            logger.warning("Missing API key (showing welcome screen)")
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Welcome to Morgen Tasks!',
                    description='Configure your API key in extension preferences. Run "mg debug" for logs.',
                    on_enter=HideWindowAction()
                ),
            ])

        # Lazy-init client and cache; re-create if API key changed
        if extension.api_client is None or extension.api_client.api_key != api_key:
            extension.api_client = MorgenAPIClient(api_key)
            extension.cache = TaskCache(ttl=cache_ttl)
            logger.info("API client initialized (cache TTL: %ds)", cache_ttl)

        # Optional "new task" shortcut keyword (preference: mg_new_keyword)
        if triggered_keyword and new_task_keyword and triggered_keyword == new_task_keyword:
            logger.info("Quick-create keyword triggered: %s", triggered_keyword)
            create_items = self._build_create_flow_items(
                raw_query,
                usage=f"{new_task_keyword} <title> [@due] [!priority]",
            )
            return RenderResultListAction(create_items)

        items = []
        formatter = TaskFormatter()

        clear_items = self._maybe_clear_cache_flow(raw_query, extension)
        if clear_items is not None:
            logger.info("Cache clear requested")
            return RenderResultListAction(clear_items)

        container_items = self._maybe_build_container_view(raw_query, extension)
        if container_items is not None:
            logger.info("Showing container view")
            return RenderResultListAction(container_items)

        # Phase 4: create task flow (mg new ...)
        create_items = self._maybe_build_create_flow(raw_query)
        if create_items is not None:
            logger.info("Showing create-task preview")
            return RenderResultListAction(create_items)

        dev_items = self._maybe_build_dev_flow(raw_query, extension)
        if dev_items is not None:
            logger.info("Showing dev flow")
            return RenderResultListAction(dev_items)

        done_mode, done_raw = self._parse_done_command(raw_query)
        if done_mode:
            force_refresh, query, refresh_prefix_used = self._parse_query(done_raw)
        else:
            force_refresh, query, refresh_prefix_used = self._parse_query(raw_query)

        container_kind, list_filter, query = self._parse_container_filter_command(query)
        due_filter_fragment = extract_due_filter_fragment(query)
        due_filter_suggestions = []
        if due_filter_fragment is not None:
            due_filter_suggestions = get_due_filter_suggestions(
                due_filter_fragment,
                limit=_DUE_FILTER_AUTOCOMPLETE_MAX,
            )
        filter_spec, query = parse_query_filters(query)

        try:
            tasks, cache_status = self._get_tasks(extension, force_refresh=force_refresh)
            api_limit_reached = len(tasks) == _TASK_LIST_API_LIMIT

            list_match_notice = None
            if list_filter:
                name_maps = self._get_name_maps(extension)
                tasks, list_match_notice = self._filter_tasks_by_container(
                    tasks,
                    list_filter,
                    container_kind=container_kind,
                    name_maps=name_maps,
                )

            # Search filtering (title + description)
            with _timed("filter_tasks"):
                filtered_tasks = self._filter_tasks(tasks, query, filter_spec=filter_spec)

            if refresh_prefix_used:
                items.append(self._refresh_prefix_notice(extension))
            if list_match_notice is not None:
                items.append(list_match_notice)

            # Header item: task count + cache status (+ quick help)
            if done_mode:
                enter_hint = "Enter: mark task done"
            else:
                enter_hint = "Enter: no action"

            if list_filter and container_kind:
                list_suffix = f" — {self._container_label(container_kind)}: {list_filter}"
            elif list_filter:
                list_suffix = f" — {list_filter}"
            else:
                list_suffix = ""
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=f'{"Morgen Tasks — Done" if done_mode else "Morgen Tasks"}{list_suffix} ({len(filtered_tasks)})',
                description=f'Cache: {cache_status} | {enter_hint} | "help" for commands | "refresh"/"!" to refresh',
                on_enter=HideWindowAction()
            ))

            if due_filter_fragment is not None:
                items.append(ExtensionResultItem(
                    icon="images/icon.png",
                    name="Due filter suggestions",
                    description='Use `due:<value>` while searching (example: due:today)',
                    on_enter=HideWindowAction(),
                ))
                if due_filter_suggestions:
                    for suggestion in due_filter_suggestions:
                        rewritten = rewrite_due_filter_query(raw_query, suggestion)
                        action = HideWindowAction()
                        if SetUserQueryAction is not None:
                            mg_keyword = (extension.preferences.get("mg_keyword") or "mg").strip() or "mg"
                            action = SetUserQueryAction(f"{mg_keyword} {rewritten}".strip())
                        items.append(ExtensionResultItem(
                            icon="images/icon.png",
                            name=f"due:{suggestion}",
                            description="Enter: fill query with this due filter",
                            on_enter=action,
                        ))
                else:
                    items.append(ExtensionResultItem(
                        icon="images/icon.png",
                        name="No due filter suggestions",
                        description="Try: due:today due:tomorrow due:next-month due:week",
                        on_enter=HideWindowAction(),
                    ))

            if api_limit_reached:
                items.append(self._api_task_limit_notice())

            if not filtered_tasks:
                items.append(ExtensionResultItem(
                    icon='images/icon.png',
                    name='No tasks found',
                    description='Try a different search term, or run "mg refresh" to fetch latest tasks.',
                    on_enter=HideWindowAction()
                ))
            else:
                # Adaptive display: condensed mode for many results
                condensed = len(filtered_tasks) > _MAX_NORMAL
                max_display = _MAX_CONDENSED if condensed else _MAX_NORMAL
                display_tasks = filtered_tasks[:max_display]

                with _timed(f"format_{len(display_tasks)}_tasks"):
                    name_maps = self._get_name_maps(extension)
                    for task in display_tasks:
                        task_id = task.get("id") or ""
                        list_ref = get_task_list_ref(task, name_maps=name_maps)
                        if done_mode:
                            on_enter = self._get_complete_task_action(task)
                        else:
                            on_enter = self._get_task_action(task_id)

                        on_alt_enter = None
                        if (not done_mode) and task_id and CopyToClipboardAction is not None:
                            try:
                                on_alt_enter = CopyToClipboardAction(task_id)
                            except Exception:
                                on_alt_enter = None

                        if condensed:
                            display_name = formatter.format_for_display(task)
                            if list_ref.name and not list_filter:
                                display_name = f"[{list_ref.name}] {display_name}"
                            items.append(self._small_result_item(
                                icon='images/icon.png',
                                name=display_name,
                                on_enter=on_enter,
                                on_alt_enter=on_alt_enter,
                            ))
                        else:
                            items.append(self._result_item(
                                icon='images/icon.png',
                                name=formatter.format_for_display(task),
                            description=(
                                f"{self._container_label(list_ref.kind)}: {list_ref.name} | {formatter.format_subtitle(task)}"
                                if list_ref.name
                                else formatter.format_subtitle(task)
                            ),
                                on_enter=on_enter,
                                on_alt_enter=on_alt_enter,
                            ))

        except MorgenAuthError:
            logger.warning("Authentication failed (invalid API key)")
            items.extend(self._error_items(
                title="Authentication Failed",
                description="Your API key was rejected by Morgen.",
                suggestions=[
                    "Open extension preferences and set a valid API key.",
                    'Then run "mg refresh" (one-shot) to fetch tasks.',
                    'Run "mg debug" for logs.',
                ],
            ))

        except MorgenRateLimitError:
            logger.warning("Rate limit exceeded (429)")
            items.extend(self._fallback_to_cache(
                extension,
                "Rate limit exceeded",
                query=query,
                filter_spec=filter_spec,
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
                filter_spec=filter_spec,
                suggestions=[
                    "Check your internet connection/VPN.",
                    'Try "mg" again, or use cached results if available.',
                    'Run "mg debug" for logs.',
                ],
            ))

        except MorgenAPIError as e:
            logger.warning("API error: %s", getattr(e, "message", e))
            items.extend(self._error_items(
                title="Morgen API Error",
                description=str(getattr(e, "message", e)),
                suggestions=['Run "mg debug" for logs.'],
            ))

        except Exception as e:
            logger.exception("Unexpected error")
            items.extend(self._error_items(
                title="Unexpected Error",
                description=str(e),
                suggestions=[
                    'Try "mg clear" then "mg refresh".',
                    'Run "mg debug" for logs.',
                ],
            ))

        return RenderResultListAction(items)

    def _get_triggered_keyword(self, event) -> str:
        """
        Best-effort retrieval of the keyword used to trigger this event.

        Ulauncher versions may expose this as `get_keyword()` or an attribute.
        """
        try:
            kw = event.get_keyword()
            if isinstance(kw, str):
                return kw
        except Exception:
            pass

        kw = getattr(event, "keyword", None)
        if isinstance(kw, str):
            return kw
        return ""

    def _get_name_maps(self, extension) -> dict[str, dict[str, str]]:
        cache_maps = extension.cache.get_container_name_maps() if extension.cache else {"list": {}, "project": {}, "space": {}}
        manual_maps = build_manual_list_name_maps(getattr(extension, "preferences", {}) or {}, slots=5)

        merged = {
            "list": dict(cache_maps.get("list") or {}),
            "project": dict(cache_maps.get("project") or {}),
            "space": dict(cache_maps.get("space") or {}),
        }
        # Manual maps override cache/API names when both exist.
        merged["list"].update(manual_maps.get("list") or {})
        return merged

    def _maybe_build_help_flow(self, raw_query: str, extension):
        if not raw_query:
            return None

        normalized = raw_query.strip().lower()
        # Only trigger help when it's the entire query, so searches like
        # "help regression test" still behave like normal search.
        if normalized not in {"help", "?", "h"}:
            return None

        mg_keyword = (extension.preferences.get("mg_keyword") or "mg").strip() or "mg"
        new_task_keyword = (extension.preferences.get("mg_new_keyword") or "").strip()

        examples = [
            ("List tasks", "mg"),
            ("Search tasks", "mg <query>"),
            ("Filter by due", "mg due:today"),
            ("Filter by priority", "mg p:high"),
            ("Combine filters", "mg report due:week p:high"),
            ("Force refresh", "mg !   or   mg refresh"),
            ("Create task", "mg new <title> [@due] [!priority]"),
            ("Show lists", "mg lists"),
            ("Filter by list", "mg in Work <query>"),
            ("Filter by project", "mg project Work <query>"),
            ("Filter by space", "mg space Personal <query>"),
            ("Mark task done", "mg d <query>"),
            ("Clear cache", "mg clear"),
            ("Debug / logs", "mg debug"),
            ("Dev: create dummy tasks", "mg dev dummy-tasks"),
        ]
        if new_task_keyword:
            examples.insert(4, ("Create task (shortcut keyword)", f"{new_task_keyword} <title> [@due] [!priority]"))

        # Prefer showing actual configured keyword in the help header.
        def _swap_mg(example: str) -> str:
            # Examples contain the literal "mg". Replace all occurrences for consistency.
            return example.replace("mg", mg_keyword)

        examples = [(label, _swap_mg(example) if example.startswith("mg") else example) for label, example in examples]

        due_examples = [
            "@today",
            "@tomorrow",
            "@next-month",
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
                description=f'Commands and examples. Tip: type "{mg_keyword}" then the example.',
                on_enter=HideWindowAction(),
            )
        ]

        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Open extension settings",
            description="Manual: Ctrl+, -> Extensions -> Morgen Tasks",
            on_enter=HideWindowAction(),
        ))

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
            description='Normal mode: Enter does nothing (Alt+Enter copies ID, if supported). Done mode ("mg d"): Enter marks the task done.',
            on_enter=HideWindowAction(),
        ))

        return items

    def _container_label(self, kind: str | None) -> str:
        if kind == "project":
            return "Project"
        if kind == "space":
            return "Space"
        return "List"

    def _maybe_build_container_view(self, raw_query: str, extension):
        """
        Build container views for:
          - `mg lists` / `mg ls` (all containers)
          - `mg list` / `mg project` / `mg space` (kind-specific)
          - `mg projects` / `mg spaces`
        """
        if not raw_query:
            return None

        normalized = raw_query.strip().lower()
        container_kind = None
        if normalized in {"lists", "ls"}:
            container_kind = None
        elif normalized in {"list"}:
            container_kind = "list"
        elif normalized in {"project", "projects"}:
            container_kind = "project"
        elif normalized in {"space", "spaces"}:
            container_kind = "space"
        else:
            return None

        try:
            tasks, cache_status = self._get_tasks(extension, force_refresh=False)
        except Exception as e:
            return self._error_items(
                title="Cannot load tasks",
                description=str(e),
                suggestions=['Try "mg" first, or "mg refresh".', 'Run "mg debug" for logs.'],
            )

        name_maps = self._get_name_maps(extension)
        grouped = group_tasks_by_list(tasks, name_maps=name_maps)
        if container_kind:
            grouped = [(ref, count) for ref, count in grouped if ref.kind == container_kind]

        title = "Morgen Task Lists" if container_kind is None else f"Morgen {self._container_label(container_kind)}s"
        pick_label = "container" if container_kind is None else self._container_label(container_kind).lower()
        items = [
            ExtensionResultItem(
                icon="images/icon.png",
                name=title,
                description=f"Cache: {cache_status} | Select a {pick_label} to view tasks",
                on_enter=HideWindowAction(),
            )
        ]

        if not grouped:
            missing_label = "list metadata" if container_kind is None else f"{self._container_label(container_kind).lower()} metadata"
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name=f"No {missing_label} found",
                description='No matching fields found on tasks. Run "mg debug" for logs.',
                on_enter=HideWindowAction(),
            ))
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name="Tip",
                description='If this exists in Morgen, we may need a different endpoint or extra fields. Try "mg refresh" first.',
                on_enter=HideWindowAction(),
            ))
            return items

        for ref, count in grouped:
            label = ref.name or ref.list_id or "Unnamed list"
            payload = {
                "action": "show_list",
                "list_id": ref.list_id,
                "list_name": ref.name,
                "container_kind": ref.kind,
            }
            kind_label = self._container_label(ref.kind).lower()
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name=f"{label} ({count})",
                description=f"Enter: show tasks in this {kind_label}",
                on_enter=ExtensionCustomAction(payload, keep_app_open=True),
            ))

        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Tip",
            description='You can also type: mg in <list> <query> or mg project <name> <query>',
            on_enter=HideWindowAction(),
        ))

        return items

    def _parse_container_filter_command(self, query: str):
        """
        Parse container filtering commands:
          - `in <list> [query]`
          - `list <name> [query]`
          - `project <name> [query]`
          - `space <name> [query]`

        Returns (container_kind, container_filter, remaining_query).
        """
        if not query:
            return None, "", ""

        stripped = query.strip()
        parts = stripped.split(None, 2)
        if len(parts) >= 2 and parts[0].lower() == "in":
            list_name = parts[1].strip()
            remaining = parts[2].strip() if len(parts) == 3 else ""
            return None, list_name, remaining

        if len(parts) >= 2 and parts[0].lower() in {"list", "project", "space"}:
            container_kind = parts[0].lower()
            list_name = parts[1].strip()
            remaining = parts[2].strip() if len(parts) == 3 else ""
            return container_kind, list_name, remaining

        return None, "", query

    def _filter_tasks_by_container(
        self,
        tasks,
        list_filter: str,
        *,
        container_kind: str | None = None,
        name_maps: dict[str, dict[str, str]] | None = None,
    ):
        """
        Filter tasks down to the selected container name/id.

        Returns (filtered_tasks, optional_notice_item).
        """
        lf = (list_filter or "").strip()
        if not lf:
            return tasks, None

        filtered = []
        saw_any_list_metadata = False
        saw_matching_kind_metadata = False
        for task in tasks or []:
            ref = get_task_list_ref(task, name_maps=name_maps)
            if ref.key:
                saw_any_list_metadata = True
            if container_kind and ref.kind == container_kind:
                saw_matching_kind_metadata = True
            if container_kind and ref.kind != container_kind:
                continue
            if ref.list_id and matches_container_id(ref.list_id, lf):
                filtered.append(task)
                continue
            if ref.name and matches_list_name(ref.name, lf):
                filtered.append(task)

        if filtered:
            return filtered, None

        if (container_kind and not saw_matching_kind_metadata) or (not container_kind and not saw_any_list_metadata):
            if container_kind:
                unavailable_name = self._container_label(container_kind)
            else:
                unavailable_name = "List"
            notice = ExtensionResultItem(
                icon="images/icon.png",
                name=f"{unavailable_name} filtering unavailable",
                description='Tasks did not include matching metadata from the API. Try "mg refresh".',
                on_enter=HideWindowAction(),
            )
            return [], notice

        target = f"{self._container_label(container_kind).lower()} " if container_kind else ""
        notice = ExtensionResultItem(
            icon="images/icon.png",
            name=f'No tasks in {target}"{lf}"',
            description='Try "mg lists" (or mg project / mg space) to see available containers.',
            on_enter=HideWindowAction(),
        )
        return [], notice

    def _parse_done_command(self, raw_query: str):
        """
        Parse the 'done' command.

        Supported:
          - "d" / "done" (show all tasks, but Enter marks done)
          - "d <query>" / "done <query>" (search, but Enter marks done)
          - Allows refresh one-shot prefixes within the done query:
              - "d !" / "d refresh"
              - "d ! <query>" / "d refresh <query>" (no force-refresh)
        """
        if not raw_query:
            return False, ""

        parts = raw_query.strip().split(None, 1)
        if not parts:
            return False, ""

        head = parts[0].lower()
        if head not in {"d", "done"}:
            return False, ""

        rest = parts[1].strip() if len(parts) > 1 else ""
        return True, rest

    def _maybe_build_debug_flow(self, raw_query: str):
        if not raw_query:
            return None

        normalized = raw_query.strip().lower()
        if normalized not in {"debug", "log", "logs"}:
            return None

        return self._build_debug_view_items()

    def _build_debug_view_items(self):
        items = [
            ExtensionResultItem(
                icon="images/icon.png",
                name="Morgen Tasks — Debug",
                description=_RUNTIME_LOG_HINT,
                on_enter=HideWindowAction(),
            )
        ]
        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Dump cached task fields",
            description="Logs sample task keys (and list-like fields) to the runtime log",
            on_enter=ExtensionCustomAction({"action": "dump_task_fields"}, keep_app_open=True),
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
        return self._build_create_flow_items(rest, usage="mg new <title> [@due] [!priority]")

    def _dev_tools_enabled(self, extension) -> bool:
        raw_value = str(extension.preferences.get("dev_tools_enabled", "1") or "").strip().lower()
        if raw_value == "0":
            return False
        return True

    def _maybe_build_dev_flow(self, raw_query: str, extension):
        """
        Development-only helper flow.

        Supported:
          - `mg dev dummy-tasks`
        """
        if not raw_query:
            return None

        normalized = raw_query.strip().lower()
        if normalized not in {"dev dummy-tasks", "dev dummy tasks"}:
            return None

        if not self._dev_tools_enabled(extension):
            return [ExtensionResultItem(
                icon="images/icon.png",
                name="Dev tools are disabled",
                description='Set "Dev Tools Enabled (1/0)" to 1 in extension preferences to use this command.',
                on_enter=HideWindowAction(),
            )]

        items = [
            ExtensionResultItem(
                icon="images/icon.png",
                name="Dev: Dummy task tools",
                description="Create or complete dummy tasks in your Morgen account.",
                on_enter=HideWindowAction(),
            )
        ]
        for count in (10, 50, DEFAULT_DUMMY_TASK_COUNT):
            payload = {
                "action": "create_dummy_tasks",
                "count": count,
                "prefix": DEFAULT_DUMMY_TITLE_PREFIX,
            }
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name=f"Create {count} dummy tasks",
                description='Prefix: "#dev Testing " | Enter to run',
                on_enter=ExtensionCustomAction(payload, keep_app_open=True),
            ))
        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Mark dummy tasks complete",
            description='Closes up to 30 tasks with prefix "#dev Testing " per run.',
            on_enter=ExtensionCustomAction(
                {
                    "action": "complete_dummy_tasks",
                    "prefix": DEFAULT_DUMMY_TITLE_PREFIX,
                },
                keep_app_open=True,
            ),
        ))
        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Cancel",
            description="Close without creating dummy tasks",
            on_enter=HideWindowAction(),
        ))
        return items

    def _build_create_flow_items(self, rest: str, *, usage: str):
        items = []

        if not rest:
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name="Create task: missing title",
                description=f"Usage: {usage}",
                on_enter=HideWindowAction(),
            ))
            return items

        parse = self._parse_create_args(rest, usage=usage)
        if parse.get("error"):
            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name="Cannot create task",
                description=parse["error"],
                on_enter=HideWindowAction(),
            ))
            return items

        title = parse["title"]
        due = parse.get("due")
        due_display = parse.get("due_display")
        priority = parse.get("priority", 0)
        incomplete_due = bool(parse.get("incomplete_due"))

        if incomplete_due:
            due_fragment = parse.get("due_fragment", "")
            due_suggestions = parse.get("due_suggestions") or self._get_due_suggestion_values(due_fragment)
            if not due_suggestions:
                due_suggestions = self._get_due_suggestion_values("")

            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name=f'Create task: choose due for "{title}"',
                description='Pick a suggestion for the "@" due token.',
                on_enter=HideWindowAction(),
            ))

            for suggestion in due_suggestions[:_DUE_AUTOCOMPLETE_MAX]:
                try:
                    due_parsed = DateParser().parse(suggestion)
                except DateParseError:
                    continue

                payload = {
                    "action": "create_task",
                    "title": title,
                    "due": due_parsed.due,
                    "priority": priority,
                }
                priority_suffix = f" | Priority: {priority}" if priority else ""
                items.append(ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"Use due @{suggestion}",
                    description=f"Due: {due_parsed.display}{priority_suffix}",
                    on_enter=ExtensionCustomAction(payload, keep_app_open=True),
                ))

            items.append(ExtensionResultItem(
                icon="images/icon.png",
                name="Cancel",
                description="Close without creating a task",
                on_enter=HideWindowAction(),
            ))
            return items

        summary = []
        if due:
            summary.append(f"Due: {due_display}")
        if priority:
            summary.append(f"Priority: {priority}")
        if not summary:
            summary.append("No due date / priority")

        payload = {
            "action": "create_task",
            "title": title,
            "due": due,
            "priority": priority,
        }

        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name=f"Create: {title}",
            description=" | ".join(summary),
            on_enter=ExtensionCustomAction(payload, keep_app_open=True),
        ))

        items.append(ExtensionResultItem(
            icon="images/icon.png",
            name="Cancel",
            description="Close without creating a task",
            on_enter=HideWindowAction(),
        ))

        return items

    def _extract_active_due_fragment(self, rest: str) -> str | None:
        tokens = (rest or "").split()
        if not tokens:
            return None
        last_token = tokens[-1]
        if not last_token.startswith("@"):
            return None
        return last_token[1:]

    def _get_due_suggestion_values(self, fragment: str, *, limit: int = _DUE_AUTOCOMPLETE_MAX) -> list[str]:
        normalized = (fragment or "").strip().lower().replace("_", "-")
        if not normalized:
            return list(_DUE_SUGGESTION_VALUES[:limit])

        matches = [value for value in _DUE_SUGGESTION_VALUES if value.startswith(normalized)]
        return matches[:limit]

    _PRIORITY_NAMES = {
        "high": 1, "hi": 1, "h": 1, "urgent": 1,
        "medium": 5, "med": 5, "m": 5, "normal": 5,
        "low": 9, "lo": 9, "l": 9,
    }

    def _parse_priority_token(self, token: str):
        """
        Parse a !-prefixed priority token.

        Returns (priority_int, error_str|None).
        - "!" alone → medium (5)
        - "!!" → high (1)
        - "!3" → numeric 3
        - "!high" → named lookup
        - "!invalid" → (0, "Unknown priority ...")
        """
        body = token[1:]  # strip leading "!"

        # "!" alone → medium
        if not body:
            return 5, None

        # "!!" → high
        if body == "!":
            return 1, None

        # Numeric: "!1" .. "!9"
        if body.isdigit():
            p = int(body)
            if 1 <= p <= 9:
                return p, None
            return 0, f"Priority must be 1-9, got {p}"

        # Named: "!high", "!low", etc.
        name = body.lower()
        if name in self._PRIORITY_NAMES:
            return self._PRIORITY_NAMES[name], None

        return 0, f"Unknown priority '{body}'. Use: !high, !medium, !low, or !1-!9"

    def _parse_create_args(self, rest: str, *, usage: str = "mg new <title> [@due] [!priority]") -> dict:
        """
        Parse create args from the part after 'new' / 'add'.

        Supports:
          - @<due> (e.g. @today, @tomorrow, @friday, @2026-02-10, @15:30)
          - !<priority>: !high, !medium, !low, !1-!9, !!, !
          - -- shortcut: low priority (9)
        """
        tokens = rest.split()
        title_parts = []
        due_token = None
        priority = 0

        for token in tokens:
            if token.startswith("@") and due_token is None:
                due_token = token[1:]
                continue
            if token == "--":
                priority = 9
                continue
            if token.startswith("!"):
                p, err = self._parse_priority_token(token)
                if err:
                    return {"error": err}
                if p:
                    priority = p
                continue
            title_parts.append(token)

        title = " ".join(title_parts).strip()
        # Strip surrounding quotes (user may type: mg new "Fix bug")
        if len(title) >= 2 and title[0] == title[-1] and title[0] in ('"', "'"):
            title = title[1:-1].strip()
        if not title:
            return {"error": f"Missing title. Usage: {usage}"}

        parsed = {"title": title, "priority": priority}

        active_due_fragment = self._extract_active_due_fragment(rest)

        if due_token is not None:
            if not due_token:
                parsed["incomplete_due"] = True
                parsed["due_fragment"] = ""
                parsed["due_suggestions"] = self._get_due_suggestion_values("")
                return parsed

            try:
                due_parsed = DateParser().parse(due_token)
                parsed["due"] = due_parsed.due
                parsed["due_display"] = due_parsed.display
            except DateParseError:
                due_suggestions = self._get_due_suggestion_values(due_token)
                if due_suggestions and active_due_fragment is not None:
                    parsed["incomplete_due"] = True
                    parsed["due_fragment"] = due_token
                    parsed["due_suggestions"] = due_suggestions
                    return parsed
                return {"error": f"Invalid date '{due_token}'. Try: today, tomorrow, next-month, friday, 2026-02-10"}

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

        with _timed("cache_lookup"):
            tasks = extension.cache.get_tasks() if extension.cache and not force_refresh else None
        if tasks is not None:
            cache_status = f"cached {extension.cache.get_age_display()}"
            logger.info("Using cached tasks: %d tasks (age=%s)", len(tasks), extension.cache.get_age_display())
            return tasks, cache_status

        logger.info("Fetching tasks from API%s...", " (force refresh)" if force_refresh else "")
        with _timed("api_call"):
            response = extension.api_client.list_tasks(limit=_TASK_LIST_API_LIMIT)
        if extension.cache:
            with _timed("cache_store"):
                extension.cache.set_tasks(response)
            cache_status = "refreshed" if force_refresh else "fresh"
        else:
            cache_status = "fresh"
        if force_refresh:
            extension.last_manual_refresh_at = time.time()
        tasks = response.get("data", {}).get("tasks", [])
        logger.info("API tasks loaded: %d tasks", len(tasks))
        return tasks, cache_status

    def _filter_tasks(self, tasks, query: str, *, filter_spec=None):
        words = query.lower().split() if query else []
        has_text_query = bool(words)
        has_extra_filters = bool(filter_spec and filter_spec.active)
        if not has_text_query and not has_extra_filters:
            return tasks

        filtered = []

        for task in tasks:
            if has_extra_filters and not matches_task_filters(task, filter_spec):
                continue

            if has_text_query:
                title = (task.get("title") or "").lower()
                description = (task.get("description") or "").lower()
                text = title + " " + description
                if not all(w in text for w in words):
                    continue

            filtered.append(task)

        return filtered

    def _get_task_action(self, task_id: str):
        task_id = (task_id or "").strip()
        if not task_id:
            return HideWindowAction()

        # Requested behavior: task Enter in normal mode should be a no-op.
        return HideWindowAction()

    def _result_item(self, *, icon: str, name: str, description: str, on_enter, on_alt_enter=None):
        kwargs = {
            "icon": icon,
            "name": name,
            "description": description,
            "on_enter": on_enter,
        }
        if on_alt_enter is not None:
            kwargs["on_alt_enter"] = on_alt_enter
        try:
            return ExtensionResultItem(**kwargs)
        except TypeError:
            kwargs.pop("on_alt_enter", None)
            return ExtensionResultItem(**kwargs)

    def _small_result_item(self, *, icon: str, name: str, on_enter, on_alt_enter=None):
        kwargs = {
            "icon": icon,
            "name": name,
            "on_enter": on_enter,
        }
        if on_alt_enter is not None:
            kwargs["on_alt_enter"] = on_alt_enter
        try:
            return ExtensionSmallResultItem(**kwargs)
        except TypeError:
            kwargs.pop("on_alt_enter", None)
            return ExtensionSmallResultItem(**kwargs)

    def _get_complete_task_action(self, task: dict):
        task_id = (task.get("id") or "").strip()
        title = (task.get("title") or "Untitled").strip() or "Untitled"
        progress = (task.get("progress") or "").strip().lower()

        if not task_id:
            return HideWindowAction()

        if progress == "completed":
            return HideWindowAction()

        payload = {
            "action": "complete_task",
            "task_id": task_id,
            "task_title": title,
        }
        return ExtensionCustomAction(payload, keep_app_open=True)

    def _fallback_to_cache(self, extension, error_msg, query="", filter_spec=None, suggestions=None):
        """Try to show cached data on network/rate-limit errors."""
        items = []
        cached = extension.cache.get_full_response() if extension.cache else None
        formatter = TaskFormatter()

        if not cached:
            logger.info("No cached response available for fallback")
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name=error_msg,
                description='No cached data available. Try again later. Run "mg debug" for logs.',
                on_enter=HideWindowAction()
            ))
            items.extend(self._suggestion_items(suggestions))
            return items

        tasks = cached.get("data", {}).get("tasks", [])
        filtered_tasks = self._filter_tasks(tasks, query, filter_spec=filter_spec)
        age = extension.cache.get_age_display() if extension.cache else "unknown"
        logger.info("Fallback to cached response: %d tasks (cache age=%s)", len(tasks), age)

        items.append(ExtensionResultItem(
            icon='images/icon.png',
            name=f'{error_msg} — showing cached data',
            description=f'{len(filtered_tasks)} tasks (cache: {age})',
            on_enter=HideWindowAction()
        ))
        if len(tasks) == _TASK_LIST_API_LIMIT:
            items.append(self._api_task_limit_notice())
        items.extend(self._suggestion_items(suggestions))

        if not filtered_tasks:
            items.append(ExtensionResultItem(
                icon='images/icon.png',
                name='No tasks found',
                description='Try a different search term, or run "mg refresh" later.',
                on_enter=HideWindowAction()
            ))
            return items

        # Adaptive display: condensed mode for many results
        condensed = len(filtered_tasks) > _MAX_NORMAL
        max_display = _MAX_CONDENSED if condensed else _MAX_NORMAL
        display_tasks = filtered_tasks[:max_display]
        for task in display_tasks:
            task_id = task.get("id") or ""
            on_enter = self._get_task_action(task_id)
            if condensed:
                items.append(ExtensionSmallResultItem(
                    icon='images/icon.png',
                    name=formatter.format_for_display(task),
                    on_enter=on_enter
                ))
            else:
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

    def _api_task_limit_notice(self):
        return ExtensionResultItem(
            icon="images/icon.png",
            name="API list limit reached (100 tasks)",
            description="Morgen may have more tasks than shown. Current list endpoint response is capped at 100.",
            on_enter=HideWindowAction(),
        )

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

        action = data.get("action")
        if action not in {
            "create_task",
            "complete_task",
            "show_list",
            "dump_task_fields",
            "create_dummy_tasks",
            "complete_dummy_tasks",
        }:
            return HideWindowAction()

        title = (data.get("title") or "").strip()
        due = data.get("due")
        try:
            priority = int(data.get("priority") or 0)
        except Exception:
            priority = 0

        task_id = (data.get("task_id") or "").strip()
        task_title = (data.get("task_title") or "").strip()
        dummy_prefix = str(data.get("prefix") or DEFAULT_DUMMY_TITLE_PREFIX)
        try:
            dummy_count = max(1, int(data.get("count") or DEFAULT_DUMMY_TASK_COUNT))
        except Exception:
            dummy_count = DEFAULT_DUMMY_TASK_COUNT

        list_id = (data.get("list_id") or "").strip() or None
        list_name = (data.get("list_name") or "").strip() or None
        container_kind = (data.get("container_kind") or "").strip().lower() or None

        api_key = extension.preferences.get("api_key", "").strip()
        cache_ttl_str = extension.preferences.get("cache_ttl", "600")
        try:
            cache_ttl = int(cache_ttl_str)
        except ValueError:
            cache_ttl = 600

        if not api_key and action in {"create_task", "complete_task", "create_dummy_tasks", "complete_dummy_tasks"}:
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Cannot run action',
                description='Missing API key. Set it in extension preferences. Run "mg debug" for logs.',
                on_enter=HideWindowAction()
            )])

        # Ensure cache is initialized (needed for list view and for invalidation on actions)
        if extension.api_client is None or extension.api_client.api_key != api_key:
            if api_key:
                extension.api_client = MorgenAPIClient(api_key)
        if extension.cache is None:
            extension.cache = TaskCache(ttl=cache_ttl)

        try:
            if action == "dump_task_fields":
                cached = extension.cache.get_full_response() if extension.cache else None
                tasks = (cached or {}).get("data", {}).get("tasks", []) if isinstance(cached, dict) else []
                data_keys = sorted(((cached or {}).get("data") or {}).keys()) if isinstance(cached, dict) else []

                if not tasks:
                    return RenderResultListAction([
                        ExtensionResultItem(
                            icon="images/icon.png",
                            name="No cached tasks to inspect",
                            description='Run "mg" (or "mg refresh") to load tasks, then try again.',
                            on_enter=HideWindowAction(),
                        )
                    ])

                sample = tasks[0] if isinstance(tasks[0], dict) else {}
                keys = sorted(sample.keys()) if isinstance(sample, dict) else []
                listish = [k for k in keys if any(s in k.lower() for s in ("list", "space", "project", "inbox"))]
                task_list_ids = []
                integration_ids = []
                for t in tasks:
                    if not isinstance(t, dict):
                        continue
                    tl = t.get("taskListId")
                    if tl:
                        tl_s = str(tl).strip()
                        if tl_s and tl_s not in task_list_ids:
                            task_list_ids.append(tl_s)
                    ii = t.get("integrationId")
                    if ii:
                        ii_s = str(ii).strip()
                        if ii_s and ii_s not in integration_ids:
                            integration_ids.append(ii_s)
                    if len(task_list_ids) >= 5 and len(integration_ids) >= 5:
                        break

                try:
                    name_maps = KeywordQueryEventListener()._get_name_maps(extension)
                except Exception:
                    name_maps = {}

                logger.info("DEBUG cached task keys: %s", keys)
                logger.info("DEBUG cached task list-like keys: %s", listish)
                logger.info("DEBUG sample taskListId values: %s", task_list_ids or ["(none)"])
                logger.info("DEBUG sample integrationId values: %s", integration_ids or ["(none)"])
                logger.info("DEBUG cached data keys: %s", data_keys)
                logger.info(
                    "DEBUG container maps sizes: lists=%d projects=%d spaces=%d",
                    len((name_maps.get("list") or {})),
                    len((name_maps.get("project") or {})),
                    len((name_maps.get("space") or {})),
                )

                preview = ", ".join(listish) if listish else "(none found)"
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="Dumped cached task fields",
                        description=f"List-like keys: {preview} | taskListId samples: {len(task_list_ids)} | integrationId samples: {len(integration_ids)}",
                        on_enter=HideWindowAction(),
                    )
                ])

            if action == "show_list":
                cached = extension.cache.get_full_response() if extension.cache else None
                tasks = (cached or {}).get("data", {}).get("tasks", []) if isinstance(cached, dict) else []
                if not tasks:
                    return RenderResultListAction([
                        ExtensionResultItem(
                            icon="images/icon.png",
                            name="No cached tasks available",
                            description='Run "mg" (or "mg refresh") first, then try again.',
                            on_enter=HideWindowAction(),
                        )
                    ])

                kind_label = KeywordQueryEventListener()._container_label(container_kind)
                list_label = list_name or list_id or kind_label
                filtered = []
                name_maps = view._get_name_maps(extension)
                for t in tasks:
                    ref = get_task_list_ref(t, name_maps=name_maps)
                    if container_kind and ref.kind != container_kind:
                        continue
                    if list_id and matches_container_id(ref.list_id or "", list_id):
                        filtered.append(t)
                        continue
                    if list_name and ref.name and matches_list_name(ref.name, list_name):
                        filtered.append(t)

                formatter = TaskFormatter()
                view = KeywordQueryEventListener()
                items = [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name=f"Morgen Tasks — {list_label} ({len(filtered)})",
                        description='Enter: no action | Tip: type "mg lists", "mg project", or "mg space" to pick another container',
                        on_enter=HideWindowAction(),
                    )
                ]

                if not filtered:
                    items.append(ExtensionResultItem(
                        icon="images/icon.png",
                        name="No tasks in this list",
                        description='Try "mg refresh" then "mg lists".',
                        on_enter=HideWindowAction(),
                    ))
                    return RenderResultListAction(items)

                condensed = len(filtered) > _MAX_NORMAL
                max_display = _MAX_CONDENSED if condensed else _MAX_NORMAL
                display_tasks = filtered[:max_display]

                for t in display_tasks:
                    tid = (t.get("id") or "").strip()
                    on_enter = view._get_task_action(tid)
                    on_alt_enter = None
                    if tid and CopyToClipboardAction is not None:
                        try:
                            on_alt_enter = CopyToClipboardAction(tid)
                        except Exception:
                            on_alt_enter = None

                    if condensed:
                        items.append(view._small_result_item(
                            icon="images/icon.png",
                            name=formatter.format_for_display(t),
                            on_enter=on_enter,
                            on_alt_enter=on_alt_enter,
                        ))
                    else:
                        subtitle = formatter.format_subtitle(t)
                        ref = get_task_list_ref(t, name_maps=name_maps)
                        if ref.name:
                            subtitle = f"{view._container_label(ref.kind)}: {ref.name} | {subtitle}"
                        items.append(view._result_item(
                            icon="images/icon.png",
                            name=formatter.format_for_display(t),
                            description=subtitle,
                            on_enter=on_enter,
                            on_alt_enter=on_alt_enter,
                        ))

                return RenderResultListAction(items)

            if action == "create_task":
                resp = extension.api_client.create_task(title=title, due=due, priority=priority)
                created_id = resp.get("data", {}).get("id") or ""

                if extension.cache:
                    extension.cache.invalidate()

                description = f"Created (id: {created_id})" if created_id else "Created"
                logger.info("Task created (id=%s)", created_id or "unknown")
                return RenderResultListAction([ExtensionResultItem(
                    icon='images/icon.png',
                    name='Task created',
                    description=description,
                    on_enter=HideWindowAction()
                )])

            if action == "create_dummy_tasks":
                specs = build_dummy_task_specs(count=dummy_count, title_prefix=dummy_prefix)
                created = 0
                failed = 0
                first_error = ""

                for spec in specs:
                    try:
                        extension.api_client.create_task(
                            title=spec["title"],
                            description=spec["description"],
                            due=spec["due"],
                            priority=spec["priority"],
                        )
                        created += 1
                    except (MorgenAuthError, MorgenRateLimitError, MorgenNetworkError, MorgenAPIError) as e:
                        failed += 1
                        first_error = first_error or str(getattr(e, "message", e))
                        # Stop on hard API failures to avoid extra request spam.
                        break
                    except Exception as e:  # pragma: no cover - safety
                        failed += 1
                        first_error = first_error or str(e)
                        break

                if extension.cache:
                    extension.cache.invalidate()

                logger.info(
                    "Dummy task seeding finished (requested=%d created=%d failed=%d)",
                    dummy_count,
                    created,
                    failed,
                )
                items = [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="Dummy task seed complete",
                        description=f"Created: {created} | Failed: {failed} | Prefix: {dummy_prefix}",
                        on_enter=HideWindowAction(),
                    )
                ]
                if first_error:
                    items.append(ExtensionResultItem(
                        icon="images/icon.png",
                        name="First error",
                        description=f"{first_error}",
                        on_enter=HideWindowAction(),
                    ))
                items.append(ExtensionResultItem(
                    icon="images/icon.png",
                    name="Tip",
                    description='Run "mg refresh" once to reload from API.',
                    on_enter=HideWindowAction(),
                ))
                return RenderResultListAction(items)

            if action == "complete_dummy_tasks":
                closed = 0
                failed = 0
                first_error = ""
                likely_more = False

                response = extension.api_client.list_tasks(limit=_TASK_LIST_API_LIMIT)
                tasks = response.get("data", {}).get("tasks", [])

                to_close = []
                for t in tasks:
                    title_value = str(t.get("title") or "")
                    if not title_value.startswith(dummy_prefix):
                        continue
                    if str(t.get("progress") or "").strip().lower() == "completed":
                        continue
                    tid = str(t.get("id") or "").strip()
                    if tid:
                        to_close.append(tid)

                if len(tasks) == _TASK_LIST_API_LIMIT:
                    likely_more = True
                if len(to_close) > _DUMMY_COMPLETE_BATCH_SIZE:
                    likely_more = True

                for tid in to_close[:_DUMMY_COMPLETE_BATCH_SIZE]:
                    try:
                        extension.api_client.close_task(tid)
                        closed += 1
                    except (MorgenAuthError, MorgenRateLimitError, MorgenNetworkError, MorgenAPIError) as e:
                        failed += 1
                        first_error = first_error or str(getattr(e, "message", e))
                        break
                    except Exception as e:  # pragma: no cover - safety
                        failed += 1
                        first_error = first_error or str(e)
                        break

                if extension.cache:
                    extension.cache.invalidate()

                logger.info(
                    "Dummy task completion finished (closed=%d failed=%d likely_more=%s)",
                    closed,
                    failed,
                    likely_more,
                )
                items = [
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name="Dummy completion finished",
                        description=f"Closed: {closed} | Failed: {failed} | Prefix: {dummy_prefix}",
                        on_enter=HideWindowAction(),
                    )
                ]
                if likely_more:
                    items.append(ExtensionResultItem(
                        icon="images/icon.png",
                        name="Possible remaining dummy tasks",
                        description="Only 30 tasks are completed per run (and list API may cap at 100). Run again to continue.",
                        on_enter=HideWindowAction(),
                    ))
                if first_error:
                    items.append(ExtensionResultItem(
                        icon="images/icon.png",
                        name="First error",
                        description=first_error,
                        on_enter=HideWindowAction(),
                    ))
                items.append(ExtensionResultItem(
                    icon="images/icon.png",
                    name="Tip",
                    description='Run "mg refresh" once to reload from API.',
                    on_enter=HideWindowAction(),
                ))
                return RenderResultListAction(items)

            if not task_id:
                return RenderResultListAction([ExtensionResultItem(
                    icon='images/icon.png',
                    name='Cannot complete task',
                    description='Missing task id.',
                    on_enter=HideWindowAction()
                )])

            extension.api_client.close_task(task_id)
            if extension.cache:
                extension.cache.invalidate()

            completed_title = task_title or task_id
            logger.info("Task completed (id=%s)", task_id)
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Task marked as done',
                    description=completed_title,
                    on_enter=HideWindowAction(),
                ),
                ExtensionResultItem(
                    icon='images/icon.png',
                    name='Tip',
                    description='Run "mg" (or "mg refresh") to reload tasks.',
                    on_enter=HideWindowAction(),
                ),
            ])

        except MorgenAuthError:
            logger.warning("%s failed: auth error", action)
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Authentication Failed',
                description='Invalid API key. Check extension preferences.',
                on_enter=HideWindowAction()
            )])

        except MorgenRateLimitError:
            logger.warning("%s failed: rate limit", action)
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Rate limit exceeded',
                description='Try again later. Run "mg debug" for logs.',
                on_enter=HideWindowAction()
            )])

        except (MorgenNetworkError, MorgenAPIError) as e:
            logger.warning("%s failed: %s", action, getattr(e, "message", e))
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Request failed',
                description=f'{str(getattr(e, "message", e))} — run "mg debug" for logs.',
                on_enter=HideWindowAction()
            )])

        except Exception as e:
            logger.exception("%s failed: unexpected error", action)
            return RenderResultListAction([ExtensionResultItem(
                icon='images/icon.png',
                name='Unexpected error',
                description=f'{str(e)} — run "mg debug" for logs.',
                on_enter=HideWindowAction()
            )])


if __name__ == '__main__':
    MorgenTasksExtension().run()
