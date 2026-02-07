# Implementation Plan — Support for Task Lists (Inbox/Work/Groceries) (v1.1.x)

**Date**: 2026-02-07  
**Repo**: Ulauncher Morgen Tasks Extension (`develop`)  
**Status**: Plan only (needs API confirmation)

## Goal

Add first-class “task lists” support so users can:

- View available lists (with counts)
- Filter/search tasks within a specific list
- See which list a task belongs to in results (when available)

**Definition (confirmed)**: by “task lists” we mean user-created organizational lists like *Inbox* (default), *Work*, *Holidays*, *Groceries*, etc.

## Key Unknown (Needs Confirmation)

Morgen’s API/model can represent “lists” in different ways. Before implementing UX, confirm which one is correct for your account:

1. **Spaces/Projects/Lists endpoint exists** (preferred): API provides a list container object with `id` + `name`, and tasks reference it via a field like `listId`/`spaceId`/`projectId`.
2. **Lists are inferred from integrations** (e.g., Todoist project, Notion DB, etc.): tasks include provider metadata that can be used as a list key.
3. **No list concept in the tasks API response**: will require a separate API call (and caching) to map tasks → lists.

Important note (2026-02-07):
- Don’t assume the on-disk cache reflects the full API payload; local runs/tests can populate the cache with synthetic task objects.
- We should treat “what fields exist on tasks” as **unknown until verified via real API responses** for this account.

This plan is written to support (1) or (3) with minimal UX churn.

## UX Proposal (Ulauncher Commands)

### List discovery
- `mg lists` (alias: `mg ls`)
  - Shows all lists + task counts
  - Selecting a list shows tasks in that list (same UI as normal task list)

### List filtering
- `mg in <list> [query]`
  - Example: `mg in Personal pay rent`

### Quality-of-life
- Header reflects active list filter: `Morgen Tasks (Personal) (12)`
- Subtitle includes list name if known: `List: Personal | Due: ... | Priority: ...`

Notes:
- Keep syntax unambiguous with existing commands (`new`, `d`, `refresh`, `help`, `debug`, `clear`).
- Avoid “settings buttons” in Ulauncher prefs (not supported).

## Data Model

Add a lightweight internal representation:

- `TaskList`:
  - `id: str`
  - `name: str`
  - `task_count: int`

Determine the task→list link field after API confirmation (examples):
- `task["listId"]`
- `task["spaceId"]`
- `task["projectId"]`

## API & Caching Strategy

### Step A — Confirm API behavior
Add a one-time developer note/test to inspect raw API responses (since we can’t reliably extract text from the bundled PDF in this minimal environment):

- Add an item under `mg debug` that logs:
  - top-level response keys from `list_tasks()`
  - `data` keys (if present)
  - first task keys
  - any list-ish fields found (best-effort: keys containing `list`, `space`, `project`, `inbox`)
- If a dedicated lists endpoint exists, confirm its point cost and response size.

This yields the concrete field/endpoint we need without guessing.

### Step B — Implement API methods (after confirmation)
In `extension/src/morgen_api.py`:

- `list_task_lists()` (name TBD once endpoint is known)
- Optionally extend `list_tasks()` to request list metadata if the API supports an “include” parameter.

### Step C — Cache lists
Add a small cache alongside tasks (same TTL by default):

- New cache file: `lists_cache.json` (or embed in current cache payload under a new key)
- Store mapping `{list_id: list_name}` and `timestamp`
- Reuse `TaskCache` patterns (TTL, disk persistence, invalidate on refresh)

Performance notes:
- Prefer *not* adding extra API calls to the main `mg` flow.
- If lists require an extra call, load lists only when user runs `mg lists` / `mg in ...`, and cache aggressively.

## Main Flow Changes (`extension/main.py`)

1. **Parsing**
   - Add `_parse_lists_command(raw_query)` for `lists/ls`
   - Add `_parse_in_list_command(raw_query)` for `in <list> ...`

2. **`mg lists` view**
   - Show:
     - Header item (“Task Lists (cached/fresh)”)
     - List items with counts
   - Enter on a list triggers an `ExtensionCustomAction` like:
     - `{"action": "open_list", "list_id": "...", "list_name": "..."}`
   - The action handler renders the filtered tasks view (same as normal).

3. **Filtered tasks view**
   - Reuse existing filtering + condensed display logic, but pre-filter to `list_id`.
   - Continue to support:
     - `refresh` one-shot behavior
     - `done` mode (`mg d ...`) inside list view (optional; may be Phase 2 of this feature)

## Formatter Changes (`extension/src/formatter.py`)

- Add optional list label support:
  - `format_subtitle(task, list_name: str | None = None)` (or keep signature and compute outside)
- Keep current due/created/priority behavior unchanged.

## Testing Plan

### Unit tests
Add/extend tests for:
- Parsing (`lists`, `in <list>`)
- Filtering by list id
- Correct list name shown in subtitle

### Manual test plan
Create: `development/research/test_plan_v1.1.0_task_lists_2026-02-07.md`

Suggested tests:
- L01 `mg lists` shows lists
- L02 selecting a list shows only tasks in that list
- L03 `mg in <list> <query>` filters correctly
- L04 list metadata cached (repeat is fast / no extra API call)
- L05 graceful fallback when list metadata missing (still shows tasks)

## Rollout / Backward Compatibility

- If API doesn’t expose list metadata, feature should:
  - Hide `mg lists` and `mg in ...` (or show a single error item explaining it’s unsupported for this account/API).
- Keep `mg` behavior unchanged if lists are unavailable.

## Implementation Order (Concrete Steps)

1. Confirm list concept in Morgen API (what field links tasks to lists, and what endpoint returns list definitions).
2. Implement list API method(s) in `extension/src/morgen_api.py`.
3. Add list caching (new cache object or extend `TaskCache` cleanly).
4. Add `mg lists` UI and list selection flow in `extension/main.py`.
5. Add `mg in <list> ...` filter flow.
6. Update formatter subtitle to include list name (when known).
7. Add unit tests + manual test plan + update `TODO.md` and `CHANGELOG.md`.

## Decision Needed From You

When you’re ready to implement, answer these so the UX matches your mental model:

1. Should `mg lists` show **all lists** (even empty) or only lists that currently have tasks?
2. Should list selection also apply to **done mode** (e.g. `mg d in Work <query>`) in this iteration, or later?
3. Should `mg new ...` support choosing a list in v1.1.x (e.g. `mg new ... #Work`), or is browse/filter enough for now?
