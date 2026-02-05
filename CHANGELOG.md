# Changelog

All notable changes to the Ulauncher Morgen Tasks extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.2] - 2026-02-05

### Added
- File-based runtime logging (`extension/logs/runtime.log`) with rotation.

### Fixed
- Help command no longer overrides searches when the query starts with “help” (e.g. `mg help regression` now searches).
- Force refresh is now one-shot: only exact `mg !` / `mg refresh` triggers refresh (prevents accidental rate-limit burn while typing).

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
