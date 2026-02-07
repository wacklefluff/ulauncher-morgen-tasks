# Changelog

All notable changes to the Ulauncher Morgen Tasks extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Dev seed flow: `mg dev dummy-tasks` now creates 90 real test tasks in Morgen (title prefix `#dev Testing `) with varied priorities and due dates.
- `mg dev dummy-tasks` now includes a bulk-complete action to close dummy tasks by prefix in repeated 100-task batches.
- New extension preference: `Dev Tools Enabled (1/0)` (default `1`) to show/hide dev commands.
- New tooling for seeding test data:
  - `development/tools/create_dummy_morgen_tasks.py` (creates real tasks via API key)
  - `extension/src/dev_dummy_tasks.py` (shared dummy payload generator)
- API-cap warning item in task results when exactly 100 tasks are loaded (`tasks/list` may be truncated by endpoint limit).

### Changed
- Removed precomputed search-index optimization; search now always uses on-the-fly matching.
- Dummy-task bulk-complete now processes up to 30 tasks per run (instead of trying to process all matches at once).

## [1.1.0] - 2026-02-07

### Added
- `mg debug` command: dedicated screen for runtime log access (open/copy log path)
- `mg d <query>` / `mg done <query>`: search tasks and press Enter to mark selected task as done
- Optional shortcut keyword preference `mg_new_keyword` (default: `mgn`) to create tasks without typing `new`
- Task lists (when available from API/task fields): `mg lists` and `mg in <list> [query]`
- Kind-specific container commands for payload discovery/testing:
  - `mg list` / `mg project` / `mg space` (browse by container kind)
  - `mg list <name> [query]` / `mg project <name> [query]` / `mg space <name> [query]`
- Task-list field compatibility for real payloads using `taskListId` / `taskListName`
- Fallback container extraction via `integrationId` when no explicit list/project/space field exists
- Case-insensitive container-id matching for filters and list selection (e.g. `Inbox` == `inbox`)
- `mg debug` field dump now logs sample `taskListId` and `integrationId` values

### Changed
- Log access items ("Open runtime log", "Copy log path") moved from help/error screens to `mg debug`
- Error and welcome screens now reference `mg debug` instead of showing log actions inline
- Tasks without a due date now show `Created: YYYY-MM-DD` in the subtitle
- Selecting a task now opens Morgen (Alt+Enter copies task ID when supported)
- Morgen API client now handles empty (204 No Content) responses
- Task list extraction now prioritizes `taskListId`/`taskListName` and `integrationId` fallback; legacy `listId`/`projectId`/`spaceId` field parsing was removed
- Normal-mode task Enter now performs no action (done mode Enter still marks task complete; Alt+Enter still copies task id when supported)

## [1.0.0] - 2026-02-06

### Added
- User Guide (`extension/docs/USER_GUIDE.md`)
- API Reference (`extension/docs/API_REFERENCE.md`)
- Performance profiling with `_timed()` context manager for debugging
- Performance test suite (`extension/tests/test_perf.py`)
- Named priority support: `!high`, `!medium`, `!low` (+ aliases `!hi`, `!med`, `!lo`, `!urgent`)
- Priority shorthands: `!!` (high) and `!` (medium)
- Bare weekday date parsing: `@friday`, `@mon`, etc. (not just `@next-friday`)
- `@yesterday` support in date parser
- Adaptive display mode: ≤5 results show detailed view, >5 results show up to 15 in fzf-style compact single-line mode (using `ExtensionSmallResultItem`)
- Comprehensive manual test plan with 60 tests (`development/research/test_plan_v1.0.0_2026-02-06.md`)
- Unit tests for date parser, formatter, and mocked API client (`extension/tests/`)
- Updated extension icon (`extension/images/icon.png`)
- Screenshots added to extension README (`extension/images/screenshots/`)

### Changed
- Updated README with current features and usage examples
- Optimized search with pre-computed lowercase index (~25% faster search)
- Search is now word-order independent: `mg sync team` matches same as `mg team sync`
- Simplified invalid date error messages (shorter, more actionable)

### Fixed
- Named priorities (`!high`, `!medium`, `!low`) now work in task creation
- Priority shorthands (`!!`, `!`) now work in task creation
- Due date + priority combo (`@tomorrow !high`) no longer puts priority text in title
- Invalid priority tokens (`!invalid`) now show error instead of silently creating task
- Surrounding quotes stripped from task titles (`mg new "Fix bug"` → title is `Fix bug`)

### Removed
- "... and X more" truncation message (replaced by adaptive display mode)

## [0.6.6] - 2026-02-06

### Changed
- Better priority icons matching Morgen's normalized values: `!!` (high/1), `!` (medium/5), none for low/normal
- Priority labels in subtitle now show human-readable text: "High", "Medium", "Low", "Normal"
- Due dates show relative labels ("Today 14:00", "Tomorrow 09:00") when applicable

### Added
- Overdue task highlighting: title prefixed with "OVERDUE", subtitle shows "(overdue!)"

## [0.6.5] - 2026-02-05

### Fixed
- Log access actions now also appear on the welcome/missing-API-key screen and other fallback error screens.

## [0.6.4] - 2026-02-05

### Added
- Quick access to logs from the UI (open/copy runtime log path) in help and error screens.

## [0.6.3] - 2026-02-05

### Added
- More actionable error messages with tips and a pointer to `extension/logs/runtime.log`.
- Additional runtime log entries for cache/API actions.

## [0.6.2] - 2026-02-05

### Fixed
- Force refresh is now one-shot: only exact `mg !` / `mg refresh` triggers refresh (prevents accidental rate-limit burn while typing).

## [0.6.1] - 2026-02-05

### Added
- File-based runtime logging (`extension/logs/runtime.log`) with rotation.

### Fixed
- Help command no longer overrides searches when the query starts with “help” (e.g. `mg help regression` now searches).

## [0.6.0] - 2026-02-05 (Phase 6 Started)

### Added
- Help and cache housekeeping commands in `extension/main.py`
  - `mg help` / `mg ?` — show command reference
  - `mg clear` — clear local task cache

## [0.5.0] - 2026-02-05 (Phase 5 Started)

### Added
- Disk-persistent task cache (`extension/src/cache.py`)
  - Loads cached tasks across Ulauncher restarts
  - Clears persisted cache on manual invalidate/refresh

## [0.4.0] - 2026-02-05 (Phase 4 Implemented)

### Added
- Task creation flow in `extension/main.py`
  - `mg new <title> [@due] [!priority]` (with confirmation prompt)
  - Invalidates task cache after successful creation
- Date parsing helper (`extension/src/date_parser.py`)
  - Supports `today`, `tomorrow`, `next-<weekday>`, ISO dates, and simple times (e.g. `15:30`, `3pm`)

## [0.3.0] - 2026-02-05 (Phase 3 Complete)

### Added
- Task display formatter (`extension/src/formatter.py`)
  - `TaskFormatter.format_for_display()` and `TaskFormatter.format_subtitle()`
  - `get_priority_icon()` helper
- Task listing and search in `extension/main.py`
  - Shows all tasks when no query is provided
  - Filters tasks by title/description when a query is provided
  - Force refresh command via `mg refresh` or `mg !` (bypasses cache)
  - Enter on a task copies its ID (when supported by Ulauncher)

## [0.2.0] - 2026-02-05 (Phase 2 Complete)

### Added
- Morgen API client (`src/morgen_api.py`)
  - `MorgenAPIClient` class with `list_tasks()` and `create_task()` methods
  - Custom exceptions for auth, rate limit, validation, and network errors
  - Uses `urllib.request` (stdlib) — no external dependencies
- Task caching system (`src/cache.py`)
  - `TaskCache` class with TTL-based expiration (default 10 minutes)
  - Cache age display ("fresh", "2m ago", etc.)
  - Fallback to cached data on network/rate-limit errors
- `shell.nix` for NixOS development environment
- Implementation plan in `development/research/`

### Changed
- Updated `main.py` to fetch and display tasks from Morgen API
- Shows task count and first 5 tasks (proof-of-concept for Phase 3)
- Updated `CLAUDE.md` and `AGENTS.md` with NixOS package management instructions

## [0.1.0] - 2026-02-05 (Phase 1 Complete)

### Added
- Basic Ulauncher extension structure
- manifest.json with keyword and API key preferences
- main.py with Extension and EventListener classes
- versions.json for API version mapping
- Extension responds to keyword trigger
- Welcome message display
- API key configuration detection

## [0.0.1] - 2026-02-05 (Phase 0 Complete)

### Added
- Initial project structure
- Git repository with develop and main branches
- .gitignore for Python, logs, and sensitive data
- Directory structure for extension and development tracking
- Placeholder icon
- Development logs (dev_log.md, issues.md, improvements.md)
- Symlink to Ulauncher extensions directory
