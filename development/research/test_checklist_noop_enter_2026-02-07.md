# Short Test Checklist — No-op Enter (v1.1.0)

**Date**: 2026-02-07
**Scope**: Confirm normal task Enter does nothing and related settings cleanup is visible.

## Preconditions

- Restart Ulauncher:
  - `pkill ulauncher && ulauncher -v`
- Ensure Morgen Tasks extension is enabled with API key configured.

## Checklist

- **E01** — Normal mode Enter does nothing
  1. Type: `mg`
  2. Select any task
  3. Press Enter
  - **Expected**: No open action; window closes/no-op behavior only.

- **E02** — Alt+Enter still copies task id (if supported)
  1. Type: `mg`
  2. Select any task
  3. Press Alt+Enter
  - **Expected**: Task id copied to clipboard.

- **E03** — Done mode Enter still works
  1. Type: `mg d <query>`
  2. Select a matching task
  3. Press Enter
  - **Expected**: Task is marked done.

- **E04** — Preference removed from settings
  1. Open Ulauncher Preferences -> Extensions -> Morgen Tasks
  - **Expected**: `Task Open URL Template` field is not shown.

- **E05** — Help text reflects no-op Enter
  1. Type: `mg help`
  - **Expected**: Help line states normal mode Enter does nothing.
