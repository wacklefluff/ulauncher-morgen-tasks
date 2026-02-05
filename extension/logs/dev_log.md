# Development Log

## 2026-02-05 (Session 5)

**Goals**:
- Housekeeping after Phase 3

**Accomplished**:
- Archived completed AI handoff to `development/handoff/archive/`
- Synced `TODO.md` to reflect Phase 3 commit completion

**Notes**:
- Manual Ulauncher testing still recommended (`pkill ulauncher && ulauncher -v`)

---

## 2026-02-05 (Session 6)

**Goals**:
- Implement Phase 4: create tasks

**Accomplished**:
- Added `extension/src/date_parser.py` (`DateParser`) for due parsing
- Updated `extension/main.py` with create flow:
  - `mg new <title> [@due] [!priority]` (preview + confirmation)
  - Handles custom action via `ItemEnterEvent`
  - Invalidates cache after successful creation
- Updated docs for v0.4.0 (`CHANGELOG.md`, `README.md`, `extension/README.md`, `TODO.md`)

**Notes**:
- Manual testing needed in Ulauncher:
  - `mg new Test task`
  - `mg new Test @tomorrow`
  - `mg new Test @next-mon !3`

---

## 2026-02-05 (Session 7)

**Goals**:
- Phase 6 polish: fix help/search edge case

**Accomplished**:
- Fixed `mg help <query>` so it searches instead of opening help (help now triggers only on `mg help`, `mg ?`, or `mg h`)
- Updated `development/research/test_plan_v0.6.0_2026-02-05.md` with regression test `H10`
- Verified `H10` manually (PASS)

---

## 2026-02-05 (Session 8)

**Goals**:
- Phase 6 polish: add file-based runtime logging

**Accomplished**:
- Added rotating file logging to `extension/logs/runtime.log`

**Notes**:
- Add a numbered manual test plan for v0.6.1 to verify runtime log creation and content.

---

## 2026-02-05 (Session 9)

**Goals**:
- Prevent accidental rate limiting when using `mg refresh` / `mg !`

**Accomplished**:
- Made force refresh one-shot: only exact `mg refresh` or `mg !` triggers refresh
- Added a UI notice when the refresh prefix is detected with extra text (to clarify behavior)

**Notes**:
- Add a numbered test plan for v0.6.2 that covers one-shot refresh while typing.

---

## 2026-02-05 (Session 10)

**Goals**:
- Verify v0.6.1 and v0.6.2 manual test plans

**Accomplished**:
- v0.6.1 manual tests: PASS (`L01`–`L08`)
- v0.6.2 manual tests: PASS (`R01`–`R08`)

---

## 2026-02-05 (Session 11)

**Goals**:
- Phase 6 polish: improve error messages and runtime logging

**Accomplished**:
- Added more actionable UI error messages (auth/network/rate limit/unexpected) with tips and a pointer to `extension/logs/runtime.log`
- Added additional runtime log lines around cache/API actions and create-task outcomes

---

## 2026-02-05 (Session 12)

**Goals**:
- Phase 6 polish: quick access to runtime logs

**Accomplished**:
- Added UI items to open/copy the runtime log path from help and error screens

**Notes**:
- Add a numbered test plan for v0.6.4 to verify OpenAction/CopyToClipboardAction availability in the user environment.

---

## 2026-02-05 (Session 4)

**Goals**:
- Implement Phase 3: list/search tasks UX
- Add force refresh command to bypass cache

**Accomplished**:
- Created `extension/src/formatter.py`
  - Added `TaskFormatter` with `format_for_display()` and `format_subtitle()`
  - Added `get_priority_icon()` helper
- Updated `extension/main.py` (Phase 3)
  - Lists all tasks when no query is provided
  - Filters tasks by query (title/description)
  - Force refresh via `mg refresh` or `mg !` (supports `!<query>` and `refresh <query>`)
  - Handles empty result sets gracefully
  - Shows cache status in header item
  - Enter on a task copies its ID when supported (fallbacks to close)
  - Improved fallback behavior to show cached tasks on rate-limit/network errors
- Updated `TODO.md` and `CHANGELOG.md` for v0.3.0

**Notes**:
- Manual testing still needed in Ulauncher (`pkill ulauncher && ulauncher -v`)

---

## 2026-02-05 (Session 3)

**Goals**:
- Test Phase 1 extension in Ulauncher
- Implement Phase 2: Morgen API integration

**Accomplished**:
- Phase 1 testing: PASSED
  - Extension loads in Ulauncher without errors
  - Keyword `mg` triggers correctly
  - Welcome message displays when no API key set
  - "Morgen Tasks is working!" displays when API key configured
  - Cache TTL preference shown correctly
- Phase 1 officially verified and complete

- Phase 2 implementation: COMPLETE
  - Updated `CLAUDE.md` with NixOS package management section and plans location
  - Updated `AGENTS.md` with NixOS section and updated plan references
  - Created `shell.nix` for NixOS development environment (Python 3 + dev tools)
  - Created `src/__init__.py` (package marker)
  - Created `src/morgen_api.py`:
    - Custom exceptions: `MorgenAPIError`, `MorgenAuthError`, `MorgenRateLimitError`, `MorgenValidationError`, `MorgenNetworkError`
    - `MorgenAPIClient` class with `list_tasks()` and `create_task()` methods
    - Full error handling for network, auth, rate limit, and validation errors
    - Uses `urllib.request` (stdlib) — no external dependencies
  - Created `src/cache.py`:
    - `TaskCache` class with TTL-based expiration (default 10 min)
    - Methods: `get_tasks()`, `set_tasks()`, `invalidate()`, `is_fresh()`, `get_age_display()`
    - Tracks `last_updated` for future incremental updates
  - Updated `main.py`:
    - Integrated API client and cache
    - Cache-first strategy (check cache before API call)
    - Lazy initialization (re-create client if API key changes)
    - Shows task count + first 5 tasks
    - Comprehensive error handling with fallback to cached data
  - Tested with real Morgen account — tasks load correctly, cache works

**Issues**:
- None

**Next Steps**:
- Phase 3: Task formatting and search
  - Create `src/formatter.py`
  - Implement search filtering
  - Better task display

---

## 2026-02-05 (Session 2)

**Goals**:
- Create comprehensive documentation for the repository
- Add guides for AI agents
- Create TODO list

**Accomplished**:
- Created `/home/user/Documents/AI/Morgen-Tasks/README.md`:
  - Complete project overview
  - Repository structure explanation
  - Installation and usage instructions
  - Technology stack and important notes
- Created `/home/user/Documents/AI/Morgen-Tasks/TODO.md`:
  - Detailed task list for all 7 phases
  - Immediate next steps (Phase 2)
  - Completed tasks checklist
  - Quick command reference
- Created `/home/user/Documents/AI/Morgen-Tasks/CLAUDE.md`:
  - Comprehensive guide for AI agents
  - Development workflow
  - File locations and purposes
  - Technical details (Morgen API, Ulauncher API)
  - Testing guidelines
  - Git workflow
  - Common commands
- Created `/home/user/Documents/AI/Morgen-Tasks/AGENTS.md`:
  - Quick reference card for AI agents
  - TL;DR section with essential info
  - Phase 2 checklist
  - Common issues and solutions
- Committed all documentation files (commit a1a9eaa)

**Issues**:
- None

**Next Steps**:
- User to test Phase 1 extension in Ulauncher
- Begin Phase 2: API integration
  - Create src/morgen_api.py
  - Create src/cache.py
  - Update main.py

**Notes**:
- Documentation is now comprehensive for any developer or AI agent
- Log files in `extension/logs/` were created earlier (dev_log.md, issues.md, improvements.md)
- All essential project information is now documented

---

## 2026-02-05 (Session 1)

**Goals**:
- Initialize project structure (Phase 0)
- Create basic Ulauncher extension (Phase 1)
- Test extension loads in Ulauncher

**Accomplished**:
- Created git repository in `/home/user/Documents/AI/Morgen-Tasks/`
- Initialized with main branch
- Created `.gitignore` for Python, logs, and sensitive data
- Created directory structure:
  - `extension/` - holds extension code
  - `development/` - research, prototypes, scratch work
  - Subdirectories: src, images, logs, tests, docs
- Created CHANGELOG.md with v0.1.0 entry
- Created this development log

**Issues**:
- None yet

**Next Steps**:
- ~~Create logs/issues.md and logs/improvements.md~~ ✓
- ~~Set up Ulauncher extension directory~~ ✓
- ~~Create placeholder icon~~ ✓
- ~~Create manifest.json with preferences~~ ✓
- ~~Create main.py with basic Extension class~~ ✓
- Test extension in Ulauncher (user needs to restart Ulauncher)
- Phase 2: API integration with Morgen

**Completed**:
- Phase 0 complete - Project structure established
- Phase 1 complete - Basic extension created
- Git commits made:
  - fa54568: Phase 0 - project structure
  - 2d44fb7: Phase 1 - basic extension
  - 731644d: Documentation updates

**Notes**:
- Using semantic versioning (0.x.y for pre-release)
- Morgen API list endpoint costs 10 points - caching is critical!
- Due dates must be exactly 19 characters: YYYY-MM-DDTHH:mm:ss
- Extension symlinked to: ~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks/

## Testing Instructions

To test the extension:

1. Restart Ulauncher in verbose mode:
   ```bash
   pkill ulauncher
   ulauncher -v
   ```

2. Type `mg` (or your configured keyword) to trigger the extension

3. You should see:
   - "Welcome to Morgen Tasks!" if no API key configured
   - "Morgen Tasks is working!" if API key is configured

4. Configure API key:
   - Open Ulauncher preferences (Ctrl+,)
   - Go to Extensions tab
   - Find "Morgen Tasks"
   - Add your Morgen API key from platform.morgen.so
