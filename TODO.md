# TODO - Ulauncher Morgen Tasks Extension

Current task list and development roadmap.

**Last Updated**: 2026-02-05
**Current Version**: v0.1.0 (Phase 1 Complete)
**Current Branch**: `develop`

## Immediate Next Steps

### Phase 2: API Integration & Authentication (NEXT)

- [ ] Create `src/morgen_api.py` - Morgen API client
  - [ ] Implement `__init__(api_key)`
  - [ ] Implement `list_tasks(limit=100)` method
  - [ ] Implement `create_task(title, **kwargs)` method
  - [ ] Add error handling for network errors
  - [ ] Add error handling for auth errors (401)
  - [ ] Add error handling for rate limit errors (429)
  - [ ] Add error handling for validation errors (400)

- [ ] Create `src/cache.py` - Task caching system
  - [ ] Implement `TaskCache` class
  - [ ] Add `get_tasks()` method with TTL check
  - [ ] Add `set_tasks(tasks)` method with timestamp
  - [ ] Add `invalidate()` method
  - [ ] Test cache expiration

- [ ] Update `main.py` to test API connection
  - [ ] Import MorgenAPIClient
  - [ ] Retrieve API key from preferences
  - [ ] Call `list_tasks()` on keyword trigger
  - [ ] Display error messages for API failures
  - [ ] Log raw API responses for debugging

- [ ] Test API integration
  - [ ] Test with valid API key
  - [ ] Test with invalid API key
  - [ ] Test with no internet connection
  - [ ] Test cache behavior

- [ ] Update logs
  - [ ] Log progress in `extension/logs/dev_log.md`
  - [ ] Log any issues in `extension/logs/issues.md`
  - [ ] Update `CHANGELOG.md` to v0.2.0

- [ ] Git commit
  - [ ] Commit with message: "feat: Morgen API integration"

## Phase 3: List/Search Tasks (After Phase 2)

- [ ] Create `src/formatter.py` - Display formatting
  - [ ] Implement `TaskFormatter` class
  - [ ] Create `format_for_display(task)` method
  - [ ] Create `format_subtitle(task)` method (due date, priority)
  - [ ] Create `get_priority_icon(priority)` helper

- [ ] Update `main.py` to display tasks
  - [ ] Show all tasks when no query provided
  - [ ] Implement search filtering by query
  - [ ] Return `RenderResultListAction` with task items
  - [ ] Handle empty task list
  - [ ] Show cache status in results

- [ ] Add task actions
  - [ ] Copy task ID on click (for debugging)
  - [ ] Consider opening Morgen app (if feasible)

- [ ] Test list/search functionality
  - [ ] Test listing all tasks
  - [ ] Test searching by title
  - [ ] Test searching by description
  - [ ] Test with no tasks
  - [ ] Test cache indicators

- [ ] Update logs and commit
  - [ ] Update `CHANGELOG.md` to v0.3.0
  - [ ] Git commit: "feat: list and search tasks"

## Phase 4: Create Tasks (After Phase 3)

- [ ] Create `src/date_parser.py` - Natural language date parsing
  - [ ] Implement `DateParser` class
  - [ ] Parse "today", "tomorrow", "next week"
  - [ ] Parse specific dates
  - [ ] Parse times (3pm, 15:00)
  - [ ] Convert to Morgen format: `YYYY-MM-DDTHH:mm:ss`
  - [ ] Handle invalid dates

- [ ] Implement task creation command syntax
  - [ ] Parse `mg new <title>` command
  - [ ] Parse `@<date>` for due dates
  - [ ] Parse `!<priority>` for priority (1-9)
  - [ ] Future: Parse `#<tag>` for tags

- [ ] Update `main.py` for task creation
  - [ ] Detect "new" keyword in query
  - [ ] Parse task components (title, date, priority)
  - [ ] Show preview before creation
  - [ ] Use `ExtensionCustomAction` for confirmation
  - [ ] Subscribe to `ItemEnterEvent`
  - [ ] Create task via API
  - [ ] Show success/error message
  - [ ] Invalidate cache after creation

- [ ] Test task creation
  - [ ] Create task with title only
  - [ ] Create task with due date
  - [ ] Create task with priority
  - [ ] Create task with date and priority
  - [ ] Test invalid date inputs
  - [ ] Verify cache invalidation

- [ ] Update logs and commit
  - [ ] Update `CHANGELOG.md` to v0.4.0
  - [ ] Git commit: "feat: create tasks with date parsing"

## Phase 5: Caching & Performance (After Phase 4)

- [ ] Optimize caching strategy
  - [ ] Implement 10-minute cache by default
  - [ ] Add cache age indicators
  - [ ] Add manual refresh option
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
