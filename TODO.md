# TODO - Ulauncher Morgen Tasks Extension

Current task list and development roadmap.

**Last Updated**: 2026-02-06
**Current Version**: v0.6.6 (Phase 6 Complete)
**Current Branch**: `develop`

## Release Checklist (Repeat Every Feature/Fix)

Use this checklist **every time** you implement a feature or fix (not just once per phase).

- [ ] Update `CHANGELOG.md` (add/move items into the correct version section)
- [ ] Update `extension/logs/dev_log.md` (include test IDs + PASS/FAIL)
- [ ] Update `TODO.md` context
  - [ ] Check off completed tasks
  - [ ] Refresh **Immediate Next Steps** to reflect what's next
- [ ] Write/update a numbered manual test plan: `development/research/test_plan_vX.Y.Z_YYYY-MM-DD.md`
- [ ] Run manual tests and record results by test ID
- [ ] Commit (and include the version in the commit message when appropriate)

**Version tags**: When marking a task done, append the version it shipped in, e.g. `(+v0.6.0)`.

## Release History

- v0.3.0 — list/search/refresh tasks
- v0.4.0 — create tasks + due parsing
- v0.5.0 — disk-persistent cache
- v0.6.0 — help + clear cache commands
- v0.6.1 — file-based runtime logging
- v0.6.2 — one-shot refresh
- v0.6.3 — improved errors + runtime logging tips
- v0.6.4 — open/copy runtime log from UI
- v0.6.5 — show log access on welcome/error fallbacks
- v0.6.6 — better priority icons + overdue highlighting
- (Unreleased) — documentation (README, USER_GUIDE, API_REFERENCE)

---

## Immediate Next Steps

### Phase 7: Testing & Release

- [x] Manual testing — 60 tests executed, results in `development/research/test_plan_v1.0.0_2026-02-06.md`
  - [x] Test all commands
  - [x] Test error scenarios
  - [x] Test offline behavior
  - [ ] Test with empty task list (skipped — no empty account)
  - [x] Follow manual test plan protocol

#### Bugs (Must Fix for v1.0.0)

- [x] **FIX-01** (T07): Search word order matters — should be order-independent
- [x] **FIX-02** (T15): Day-of-week date parsing (`@friday`) doesn't work
- [x] **FIX-03** (T16-T18): Named priorities (`!high`, `!medium`, `!low`) don't work
- [x] **FIX-04** (T19-T20): Priority shorthands (`!!` and `!`) don't work
- [x] **FIX-05** (T21): Due date + priority combo fails (priority included in title)
- [x] **FIX-06** (T44): Invalid priority (`!invalid`) silently accepted
- [x] **FIX-07** (T51 note): `@yesterday` not supported in date parser

#### Enhancements (Should Fix for v1.0.0)

- [x] **ENH-01** (T03): Remove "... and X more" truncation message
- [x] **ENH-02** (T03): Adaptive display mode (>5 results → fzf-style compact single-line via `ExtensionSmallResultItem`, ≤5 → normal with subtitles)
- [x] **ENH-03** (T43): Simplify invalid date error message
- [x] **ENH-04** (T24): Strip surrounding quotes from task title

#### After Fixes

- [ ] Re-test all failed items (T07, T15-T21, T44)
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

#### Suggestions (Post v1.0.0)

- [ ] **SUG-01** (T02): Fix welcome screen when typing `mg` with no space
- [ ] **SUG-02** (T36): Move log access to `mg debug` command
- [ ] **SUG-03** (T47): Only enable search optimization for 200+ tasks
- [ ] **SUG-04** (T49): Show creation date when no due date available

### Optional: Performance Improvements

- [ ] Consider background refresh
- [x] Optimize search in cached data (+v0.6.7)
- [ ] Lazy load task details
- [x] Profile performance (+v0.6.7)
- [x] Limit rendered results to 7 for performance (+v0.6.7)
- [ ] Add pagination for large result sets (Ulauncher lacks native scroll)

---

## Future Enhancements (Post v1.0.0)

See `extension/logs/improvements.md` for detailed ideas.

### High Priority
- [ ] Mark tasks as complete from Ulauncher

- [ ] Filter tasks by priority/due date
- [ ] Support for task lists
- [ ] Ulauncher settings
	- [ ] additional shortcut to add a new task
	- [ ] open log file button
- use ALT to turn into 'VIM like mode', that way using J,K to go up and down the list, move word to next word or last

### Medium Priority
- [ ] Subtask creation
- [ ] Recurring tasks support
- [ ] Better keyboard shortcuts (Alt+Enter actions)
- [ ] Open Morgen app on task click
- [ ] Desktop notifications for upcoming tasks
- [ ] Parse `#<tag>` for tags

### Low Priority / Nice-to-Have
- [ ] when shwoing a lot of results, next page option could be on top message 
- [ ] Integration with system notifications
- [ ] Quick scheduling (time blocking)
- [ ] Task templates
- [ ] Bulk operations

- [ ] Update task details (title, due date, priority)

---

## Completed Phases

### Phase 0: Project Setup (v0.0.1)
- [x] Initialize git repository
- [x] Create .gitignore and directory structure
- [x] Create CHANGELOG.md and development logs
- [x] Set up extension symlink
- [x] Create placeholder icon

### Phase 1: Basic Extension (v0.1.0)
- [x] Create manifest.json with preferences
- [x] Create main.py with Extension class
- [x] Create versions.json
- [x] Test extension loads in Ulauncher

### Phase 2: API Integration (v0.2.0)
- [x] Create `src/morgen_api.py` - Morgen API client
- [x] Create `src/cache.py` - Task caching system
- [x] Update `main.py` with API integration
- [x] Test with real Morgen account

### Phase 3: List/Search Tasks (v0.3.0)
- [x] Create `src/formatter.py` - Display formatting
- [x] Update `main.py` to display and search tasks
- [x] Add force refresh command (`mg !`, `mg refresh`)
- [x] Copy task ID on click

### Phase 4: Create Tasks (v0.4.0)
- [x] Create `src/date_parser.py` - Natural language date parsing
- [x] Implement `mg new <title> [@due] [!priority]` command
- [x] Show preview before creation
- [x] Invalidate cache after creation

### Phase 5: Caching & Performance (v0.5.0)
- [x] Implement 10-minute cache by default
- [x] Add cache age indicators
- [x] Persist cache to disk across restarts

### Phase 6: Polish & Error Handling (v0.6.x)
- [x] Enhance error messages with tips (+v0.6.3)
- [x] Add help command (`mg help`, `mg ?`) (+v0.6.0)
- [x] Add clear cache command (`mg clear`) (+v0.6.0)
- [x] File-based runtime logging (+v0.6.1)
- [x] One-shot refresh to prevent rate limit burn (+v0.6.2)
- [x] Open/copy runtime log from UI (+v0.6.4)
- [x] Show log access on welcome/errors (+v0.6.5)
- [x] Better priority icons (`!!`, `!`) (+v0.6.6)
- [x] Overdue task highlighting (+v0.6.6)
- [x] Relative due dates (Today, Tomorrow) (+v0.6.6)
- [x] Complete documentation (README, USER_GUIDE, API_REFERENCE)

---

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
pkill ulauncher && ulauncher -v

# Commit changes
git add -A
git commit -m "feat: description"

# View logs
cat extension/logs/dev_log.md
```
