# Phase 2: Morgen API Integration Plan

**Date**: 2026-02-05
**Target Version**: v0.2.0
**Branch**: develop

## Summary

Create API client and cache modules, then wire them into the existing extension. Uses `urllib.request` (stdlib) to avoid external dependencies.

## Files to Create

### 1. `extension/src/__init__.py`
Empty package marker (docstring only).

### 2. `extension/src/morgen_api.py` (~200 lines)

**Custom exceptions** (all inherit from `MorgenAPIError`):
- `MorgenAuthError` — 401 invalid API key
- `MorgenRateLimitError` — 429 rate limit
- `MorgenValidationError` — 400 bad request
- `MorgenNetworkError` — connection/timeout failures

**`MorgenAPIClient` class:**
- `__init__(self, api_key)` — store key, set base URL `https://api.morgen.so/v3`, 10s timeout
- `_make_request(self, endpoint, method="GET", data=None)` — centralized HTTP using `urllib.request`, maps HTTP status codes to custom exceptions
- `list_tasks(self, limit=100, updated_after=None)` — `GET /v3/tasks/list?limit=100&updatedAfter=...`, returns full response dict
- `create_task(self, title, description=None, due=None, time_zone=None, priority=0)` — `POST /v3/tasks/create`, validates due date format (19 chars, `YYYY-MM-DDTHH:mm:ss`) and priority (0-9) before calling API

### 3. `extension/src/cache.py` (~120 lines)

**`TaskCache` class:**
- `__init__(self, ttl=600)` — default 10 min TTL
- `get_tasks()` — return cached task list if fresh, else `None`
- `get_full_response()` — return full API response if fresh
- `set_tasks(api_response)` — store response + timestamp, track `last_updated` from newest task
- `is_fresh()` — check age < TTL
- `get_age()` — seconds since last fetch
- `get_age_display()` — human-readable: "fresh", "45s ago", "2m ago", "expired"
- `invalidate()` — clear cache
- `get_last_updated()` — for future incremental `updatedAfter` queries

## File to Modify

### 4. `extension/main.py`

**New imports:** `MorgenAPIClient`, exception classes, `TaskCache`

**`MorgenTasksExtension.__init__`:** Add `self.cache = None` and `self.api_client = None`

**`KeywordQueryEventListener.on_event` rewrite:**
1. Read preferences (`api_key`, `cache_ttl`)
2. Lazy-init API client + cache (re-create if API key changed)
3. If no API key → show welcome message (unchanged)
4. Cache-first: try `cache.get_tasks()`, on miss call `api_client.list_tasks()`
5. Show task count + cache status header item
6. Show first 5 tasks (title, due, priority) as proof-of-concept
7. Error handling:
   - `MorgenAuthError` → "Authentication Failed" message
   - `MorgenRateLimitError` / `MorgenNetworkError` → show cached data if available, else error message
   - `MorgenAPIError` → generic error message
   - `Exception` → catch-all with logging

## Implementation Order

1. Create `src/__init__.py`
2. Create `src/morgen_api.py` (exceptions + client)
3. Create `src/cache.py`
4. Update `main.py` to integrate both
5. Test in Ulauncher
6. Update logs, CHANGELOG, commit

## Key Design Decisions

- **`urllib.request` over `requests`**: No external dependency needed; stdlib is sufficient
- **Cache-first**: Always check cache before API call (list costs 10 points!)
- **Lazy init**: Client created on first keyword trigger, allowing API key changes without restart
- **Graceful degradation**: Network/rate-limit errors fall back to stale cached data

## Morgen API Reference

### Authentication
```
Authorization: ApiKey <API_KEY>
Accept: application/json
```

### List Tasks (10 points per call!)
```
GET /v3/tasks/list?limit=100&updatedAfter=<ISO_DATE>
Response: {"data": {"tasks": [...], "labelDefs": [...], "spaces": [...]}}
```

### Create Task
```
POST /v3/tasks/create
Body: {"title": "...", "due": "YYYY-MM-DDTHH:mm:ss", "timeZone": "...", "priority": 0-9}
Response: {"data": {"id": "..."}}
```

### Task Object Fields
- `id`, `title`, `description`, `due` (19-char format), `timeZone`
- `priority` (0=undefined, 1=highest, 9=lowest)
- `progress` (needs-action, in-process, completed, failed, cancelled)
- `created`, `updated`, `tags`, `taskListId`, `accountId`

### Date Format (CRITICAL)
- Exactly 19 characters: `YYYY-MM-DDTHH:mm:ss`
- NO timezone suffix (no Z, no +00:00)
- Use separate `timeZone` field

## Verification

```bash
pkill ulauncher && ulauncher -v
```

Test these scenarios by typing `mg`:
1. No API key → welcome message
2. Invalid API key → auth error message
3. Valid API key → tasks load, shows count + first 5
4. Type `mg` again → cache hit, shows "cached Xs ago"
5. Disconnect network → shows cached data with network error note
