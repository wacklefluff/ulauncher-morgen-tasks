# Manual Test Plan — v1.1.0 (New-Task Shortcut Keyword)

**Date**: 2026-02-07  
**Scope**: `mg_new_keyword` preference (default `mgn`) for quick task creation

## Preconditions

- Ulauncher restarted in verbose mode:
  - `pkill ulauncher && ulauncher -v`
- Extension installed and enabled
- Morgen API key set (for creation tests)
- Preferences:
  - `mg_keyword`: `mg`
  - `mg_new_keyword`: `mgn` (or any chosen shortcut keyword)

## Tests

### Keyword / Create Flow

- **N01** — `mgn <title>` shows create preview and creates task
  1. Type: `mgn Test quick create`
  2. Confirm the UI shows the create preview and a `Create: Test quick create` item
  3. Press Enter on `Create: ...`
  4. Verify task exists in Morgen (web/app) and appears via `mg refresh`
  - **Expected**: Task is created; cache invalidated; task shows after refresh

- **N02** — `mgn` with no args shows correct usage
  1. Type: `mgn`
  - **Expected**: "Create task: missing title" with usage `mgn <title> [@due] [!priority]`

- **N03** — `mgn` supports due + priority parsing
  1. Type: `mgn Test due @tomorrow !high`
  2. Verify preview shows due + priority summary (and creates successfully)
  - **Expected**: Due is parsed (Tomorrow ...) and priority set (high)

### Help Screen

- **N04** — `mg help` shows shortcut keyword example when enabled
  1. Type: `mg help`
  - **Expected**: Help list includes "Create task (shortcut keyword)" with the configured shortcut keyword.
