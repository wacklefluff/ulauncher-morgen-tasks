# TODO - Ulauncher Morgen Tasks Extension

Current task list and development roadmap.

**Last Updated**: 2026-02-05
**Current Version**: v0.5.0 (Phase 5 Started)
**Current Branch**: `develop`

## Immediate Next Steps

### Phase 3: List/Search Tasks (COMPLETE)

- [x] Create `src/formatter.py` - Display formatting
  - [x] Implement `TaskFormatter` class
  - [x] Create `format_for_display(task)` method
  - [x] Create `format_subtitle(task)` method (due date, priority)
  - [x] Create `get_priority_icon(priority)` helper

- [x] Update `main.py` to display tasks
  - [x] Show all tasks when no query provided
  - [x] Implement search filtering by query
  - [x] Return `RenderResultListAction` with task items
  - [x] Handle empty task list
  - [x] Show cache status in results

- [x] Add force refresh command
  - [x] Implement `mg refresh` or `mg !` to bypass cache
  - [x] Invalidate cache and fetch fresh data
  - [x] Show "Refreshed" confirmation

- [ ] Add task actions
  - [x] Copy task ID on click (for debugging)
  - [ ] Consider opening Morgen app (if feasible)

- [ ] Test list/search functionality
  - [x] Test listing all tasks
  - [x] Test searching by title
  - [x] Test searching by description
  - [x] Test with no tasks
  - [x] Test cache indicators

- [ ] Update logs and commit
  - [x] Update `CHANGELOG.md` to v0.3.0
  - [x] Git commit: "feat: list and search tasks"

## Phase 4: Create Tasks (After Phase 3)

- [x] Create `src/date_parser.py` - Natural language date parsing
  - [x] Implement `DateParser` class
  - [x] Parse "today", "tomorrow", "next week"
  - [x] Parse specific dates
  - [x] Parse times (3pm, 15:00)
  - [x] Convert to Morgen format: `YYYY-MM-DDTHH:mm:ss`
  - [x] Handle invalid dates

- [x] Implement task creation command syntax
  - [x] Parse `mg new <title>` command
  - [x] Parse `@<date>` for due dates
  - [x] Parse `!<priority>` for priority (1-9)
  - [ ] Future: Parse `#<tag>` for tags

- [x] Update `main.py` for task creation
  - [x] Detect "new" keyword in query
  - [x] Parse task components (title, date, priority)
  - [x] Show preview before creation
  - [x] Use `ExtensionCustomAction` for confirmation
  - [x] Subscribe to `ItemEnterEvent`
  - [x] Create task via API
  - [x] Show success/error message
  - [x] Invalidate cache after creation

- [ ] Test task creation
  - [x] Create task with title only
  - [x] Create task with due date
  - [x] Create task with priority
  - [x] Create task with date and priority
  - [x] Test invalid date inputs
  - [x] Verify cache invalidation

- [ ] Update logs and commit
  - [x] Update `CHANGELOG.md` to v0.4.0
  - [x] Git commit: "feat: create tasks with date parsing"

## Phase 5: Caching & Performance (After Phase 4)

- [ ] Optimize caching strategy
  - [x] Implement 10-minute cache by default
  - [x] Add cache age indicators
  - [x] Add manual refresh option
  - [x] Persist cache to disk across restarts
  - [ ] Consider background refresh

- [ ] Add performance optimizations
  - [ ] Optimize search in cached data
  - [ ] Lazy load task details
  - [ ] Profile performance

- [ ] Update logs and commit
  - [ ] Update `CHANGELOG.md` to v0.5.0
  - [ ] Git commit: "perf: improve caching and performance"

## Phase 6: Polish & Error Handling (After Phase 5)

- [ ] Enhance error messages
  - [ ] Network errors
  - [ ] Auth errors
  - [ ] Rate limit errors
  - [ ] Empty results

- [ ] Improve UI
  - [ ] Better icons for priority levels
  - [ ] Color-code overdue tasks
  - [ ] Show task count
  - [ ] Add help command

- [ ] Write documentation
  - [ ] Complete README.md
  - [ ] Create docs/USER_GUIDE.md
  - [ ] Create docs/API_REFERENCE.md

- [ ] Add logging
  - [ ] Log API errors to file
  - [ ] Log cache hits/misses

- [ ] Update logs and commit
  - [ ] Update `CHANGELOG.md` to v0.6.0
  - [ ] Git commit: "docs: add user guide and polish UX"

## Phase 7: Testing & Release (After Phase 6)

- [ ] Manual testing
  - [ ] Test all commands
  - [ ] Test error scenarios
  - [ ] Test offline behavior
  - [ ] Test with empty task list
  - [ ] Follow manual test plan protocol (numbered tests + saved `.md` plan in `development/research/`)

- [ ] Write unit tests
  - [ ] Tests for date parser
  - [ ] Tests for formatter
  - [ ] Mock API tests

- [ ] Prepare v1.0.0 release
  - [ ] Update `manifest.json` to v1.0.0
  - [ ] Update `CHANGELOG.md`
  - [ ] Merge to `main` branch
  - [ ] Tag release: `v1.0.0`

- [ ] Optional: Publish
  - [ ] Create GitHub repository
  - [ ] Add screenshots to README
  - [ ] Submit to Ulauncher extensions directory

## Future Enhancements (Post v1.0.0)

See `extension/logs/improvements.md` for detailed ideas.

### High Priority
- [ ] Mark tasks as complete from Ulauncher
- [ ] Update task details (title, due date, priority)
- [ ] Filter tasks by priority/due date
- [ ] Support for task lists

### Medium Priority
- [ ] Subtask creation
- [ ] Recurring tasks support
- [ ] Better keyboard shortcuts (Alt+Enter actions)
- [ ] Desktop notifications for upcoming tasks

### Low Priority / Nice-to-Have
- [ ] Integration with system notifications
- [ ] Quick scheduling (time blocking)
- [ ] Task templates
- [ ] Bulk operations

## Completed Tasks

### Phase 0: Project Setup ✅ (v0.0.1)
- [x] Initialize git repository
- [x] Create .gitignore
- [x] Create directory structure
- [x] Create CHANGELOG.md
- [x] Create development logs
- [x] Set up extension symlink
- [x] Create placeholder icon
- [x] Make initial commit

### Phase 1: Basic Extension ✅ (v0.1.0)
- [x] Create manifest.json
- [x] Create main.py with Extension class
- [x] Create versions.json
- [x] Test extension loads in Ulauncher
- [x] Add README.md
- [x] Update CHANGELOG

### Phase 2: API Integration ✅ (v0.2.0)
- [x] Create `src/morgen_api.py` - Morgen API client
  - [x] Implement `__init__(api_key)`
  - [x] Implement `list_tasks(limit=100)` method
  - [x] Implement `create_task(title, **kwargs)` method
  - [x] Add error handling for network, auth, rate limit, validation errors
- [x] Create `src/cache.py` - Task caching system
  - [x] Implement `TaskCache` class with TTL
  - [x] Add `get_tasks()`, `set_tasks()`, `invalidate()` methods
- [x] Update `main.py` with API integration
  - [x] Cache-first strategy
  - [x] Error handling with fallback to cached data
  - [x] Display task count and first 5 tasks
- [x] Test with real Morgen account
- [x] Update logs and CHANGELOG

## Notes

- Remember to update `extension/logs/dev_log.md` during each session
- Log issues in `extension/logs/issues.md` as they arise
- Log improvement ideas in `extension/logs/improvements.md`
- Make small, frequent git commits
- Test after each feature implementation

## Quick Commands

```bash
# Start development session
cd /home/user/Documents/AI/Morgen-Tasks/
git checkout develop

# Test extension
pkill ulauncher
ulauncher -v

# Commit changes
git add -A
git commit -m "feat: description"

# View logs
cat extension/logs/dev_log.md
```
