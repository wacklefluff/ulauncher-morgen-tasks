# API Reference - Ulauncher Morgen Tasks

Technical reference for developers working on or extending this project.

## Architecture

```
extension/
├── main.py              # Entry point, Ulauncher integration
├── manifest.json        # Extension metadata
├── versions.json        # API version mapping
└── src/
    ├── morgen_api.py    # Morgen API client
    ├── cache.py         # Task caching system
    ├── formatter.py     # Display formatting
    └── date_parser.py   # Natural language date parsing
```

---

## Module: morgen_api.py

### MorgenAPIClient

HTTP client for Morgen's REST API.

```python
from src.morgen_api import MorgenAPIClient

client = MorgenAPIClient(api_key="your-api-key")
```

#### Methods

**list_tasks(limit=100)**

Fetch tasks from Morgen.

```python
tasks = client.list_tasks(limit=50)
# Returns: list of task dicts
```

**create_task(title, due=None, priority=None, description=None)**

Create a new task.

```python
task = client.create_task(
    title="Buy groceries",
    due="2026-02-15T14:00:00",  # Morgen format
    priority=1
)
# Returns: created task dict
```

### Exceptions

| Exception | Description |
|-----------|-------------|
| `MorgenAPIError` | Base exception |
| `MorgenAuthError` | Invalid/expired API key |
| `MorgenRateLimitError` | API quota exceeded |
| `MorgenValidationError` | Invalid request data |
| `MorgenNetworkError` | Connection failed |

---

## Module: cache.py

### TaskCache

In-memory + disk-persistent task cache with TTL.

```python
from src.cache import TaskCache

cache = TaskCache(ttl_seconds=600)
```

#### Methods

**get_tasks()**

Get cached tasks if not expired.

```python
tasks = cache.get_tasks()
# Returns: list of tasks or None if expired/empty
```

**set_tasks(tasks)**

Store tasks in cache.

```python
cache.set_tasks(task_list)
```

**invalidate()**

Clear the cache.

```python
cache.invalidate()
```

**is_fresh()**

Check if cache was updated recently (< 60 seconds).

```python
if cache.is_fresh():
    print("Cache is fresh")
```

**get_age_display()**

Human-readable cache age.

```python
age = cache.get_age_display()
# Returns: "fresh", "2m ago", "1h ago", etc.
```

---

## Module: formatter.py

### TaskFormatter

Format task dicts for Ulauncher display.

```python
from src.formatter import TaskFormatter

formatter = TaskFormatter()
```

#### Methods

**format_for_display(task)**

Format task title with priority icon and overdue prefix.

```python
title = formatter.format_for_display(task)
# Returns: "!! Buy groceries" or "OVERDUE !! Buy groceries"
```

**format_subtitle(task)**

Format task subtitle with due date and priority.

```python
subtitle = formatter.format_subtitle(task)
# Returns: "Due: Tomorrow 14:00 | Priority: High"
```

### Helper Functions

**get_priority_icon(priority)**

```python
from src.formatter import get_priority_icon

icon = get_priority_icon(1)  # Returns: "!!"
icon = get_priority_icon(5)  # Returns: "!"
icon = get_priority_icon(9)  # Returns: ""
```

**get_priority_label(priority)**

```python
from src.formatter import get_priority_label

label = get_priority_label(1)  # Returns: "High"
label = get_priority_label(5)  # Returns: "Medium"
label = get_priority_label(9)  # Returns: "Low"
label = get_priority_label(0)  # Returns: "Normal"
```

**is_overdue(due, now=None)**

```python
from src.formatter import is_overdue

overdue = is_overdue("2026-02-01T09:00:00")  # Returns: True/False
```

---

## Module: date_parser.py

### DateParser

Parse natural language dates into Morgen format.

```python
from src.date_parser import DateParser

parser = DateParser()
```

#### Methods

**parse(text, now=None)**

Parse a date string.

```python
result = parser.parse("tomorrow")
# Returns: ParsedDue(due="2026-02-07T09:00:00", display="2026-02-07 09:00")

result = parser.parse("next-mon 3pm")
# Returns: ParsedDue(due="2026-02-10T15:00:00", display="2026-02-10 15:00")
```

### ParsedDue

Dataclass returned by `parse()`.

| Field | Type | Description |
|-------|------|-------------|
| `due` | str | Morgen format: `YYYY-MM-DDTHH:mm:ss` |
| `display` | str | Human-readable: `YYYY-MM-DD HH:mm` |

### DateParseError

Raised when parsing fails.

```python
from src.date_parser import DateParseError

try:
    parser.parse("invalid-date")
except DateParseError as e:
    print(f"Parse error: {e}")
```

### Supported Formats

| Input | Interpretation |
|-------|----------------|
| `today`, `tod` | Today at 9:00 |
| `tomorrow`, `tmr`, `tmrw` | Tomorrow at 9:00 |
| `next-week`, `nextweek` | 7 days from now |
| `next-mon` ... `next-sun` | Next occurrence of weekday |
| `YYYY-MM-DD` | Specific date at 9:00 |
| `YYYY-MM-DDTHH:mm` | Specific date and time |
| `MM-DD`, `MM/DD` | Date this year (or next) |
| `HH:mm`, `Hpm`, `Ham` | Time today (or tomorrow if passed) |
| `noon` | 12:00 |
| `midnight` | 00:00 |

---

## Morgen API Details

### Base URL

```
https://api.morgen.so/v3
```

### Authentication

```python
headers = {
    "Authorization": f"ApiKey {api_key}",
    "accept": "application/json"
}
```

### Date Format

Morgen requires exactly 19 characters, no timezone:

```
YYYY-MM-DDTHH:mm:ss
```

Example: `2026-02-15T14:00:00`

### Priority Values

| Morgen UI | API Value |
|-----------|-----------|
| High | 1 |
| Medium | 5 |
| Low | 9 |
| Normal | None/0 |

### Task Progress States

- `needs-action`
- `in-process`
- `completed`
- `failed`
- `cancelled`

---

## Ulauncher Integration

### Extension Class

```python
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent

class MorgenTasksExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
```

### Preferences

Access via `extension.preferences`:

| ID | Type | Description |
|----|------|-------------|
| `mg_keyword` | keyword | Trigger keyword |
| `api_key` | input | Morgen API key |
| `cache_ttl` | input | Cache duration (seconds) |

Note: Ulauncher persists extension preferences (including `api_key`) in the user's local Ulauncher configuration (typically under `~/.config/ulauncher/`). The extension reads values via `extension.preferences` at runtime and does not store secrets in this repository.

### Result Items

```python
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

item = ExtensionResultItem(
    icon='images/icon.png',
    name='Task title',
    description='Due: Tomorrow | Priority: High',
    on_enter=HideWindowAction()
)
```

---

## Logging

Runtime logs are written to `extension/logs/runtime.log` using Python's `RotatingFileHandler`.

```python
import logging

logger = logging.getLogger(__name__)
logger.info("API call successful")
logger.error("Failed to fetch tasks", exc_info=True)
```

---

## Testing

### Compile Check

```bash
python -m compileall extension
```

### Manual Testing

```bash
pkill ulauncher && ulauncher -v
```

### Test Plans

Located in `development/research/test_plan_vX.Y.Z_YYYY-MM-DD.md`
