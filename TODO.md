# TODO - Ulauncher Morgen Tasks Extension

Current task list and development roadmap.

**Last Updated**: 2026-02-06
**Current Version**: v1.0.0 (Published)
**Current Branch**: `develop`

## Release Checklist (Repeat Every Feature/Fix)

Use this checklist **every time** you implement a feature or fix (not just once per phase).

- [ ] Update `CHANGELOG.md` (add/move items into the correct version section)
- [ ] Update `extension/logs/dev_log.md` (include test IDs + PASS/FAIL)
- [ ] Update `TODO.md` context
  - [ ] Check off completed tasks
  - [ ] Refresh **v1.1.0 Roadmap** to reflect what's next
- [ ] Write/update a numbered manual test plan: `development/research/test_plan_vX.Y.Z_YYYY-MM-DD.md`
- [ ] Run manual tests and record results by test ID
- [ ] Commit (and include the version in the commit message when appropriate)

**Version tags**: When marking a task done, append the version it shipped in, e.g. `(+v1.1.0)`.

## Release History

- v1.0.0 — published to GitHub + Ulauncher directory
- v0.6.6 — better priority icons + overdue highlighting
- v0.6.5 — show log access on welcome/error fallbacks
- v0.6.4 — open/copy runtime log from UI
- v0.6.3 — improved errors + runtime logging tips
- v0.6.2 — one-shot refresh
- v0.6.1 — file-based runtime logging
- v0.6.0 — help + clear cache commands
- v0.5.0 — disk-persistent cache
- v0.4.0 — create tasks + due parsing
- v0.3.0 — list/search/refresh tasks

---

## v1.1.0 Roadmap

- [x] **SUG-02**: `mg debug` command — dedicated screen for runtime log access (+v1.1.0)
- [x] `mg help` and `mg debug` work without API key (+v1.1.0)
- [ ] **SUG-04**: Show creation date when no due date available
- [ ] **Mark tasks as complete** from Ulauncher (Enter on task → complete via API)
- [ ] **Open Morgen app** on task click (Alt+Enter or secondary action)
- [ ] **VIM-like mode**: ALT to navigate with J/K, move between words

### Implementation notes

**SUG-04** — `extension/src/formatter.py`
- When a task has no `due` date, show `Created: <date>` from the `created` field instead of "No due date"

**Mark tasks as complete** — `extension/src/morgen_api.py` + `extension/main.py`
- API: `POST /v3/tasks/close` with `{"id": "<TASK_ID>"}` → 204 No Content
- Change task `on_enter` from `CopyToClipboardAction(task_id)` to `ExtensionCustomAction({"action": "complete_task", ...})`
- Add handler in `ItemEnterEventListener` for `complete_task` action
- Invalidate cache after completion

---

## Backlog

Items not scheduled for v1.1.0. May be picked up in future versions.

- [x] **SUG-01** (T02): Fix welcome screen when typing `mg` with no space — **won't fix** (Ulauncher limitation)
- [ ] **SUG-03** (T47): Only enable search optimization for 200+ tasks
- [ ] Background refresh
- [ ] Lazy load task details
- [ ] Pagination for large result sets (Ulauncher lacks native scroll)

---

## Future Enhancements

See `extension/logs/improvements.md` for detailed ideas.

### High Priority
- [ ] Filter tasks by priority/due date
- [ ] Support for task lists
- [ ] Ulauncher settings
	- [ ] additional shortcut to add a new task
	- [ ] open log file button

### Medium Priority
- [ ] Subtask creation
- [ ] Recurring tasks support
- [ ] Better keyboard shortcuts (Alt+Enter actions)
- [ ] Desktop notifications for upcoming tasks
- [ ] Parse `#<tag>` for tags

### Low Priority / Nice-to-Have
- [ ] when showing a lot of results, next page option could be on top message
- [ ] Integration with system notifications
- [ ] Quick scheduling (time blocking)
- [ ] Task templates
- [ ] Bulk operations
- [ ] Update task details (title, due date, priority)

---

## Publish (v1.0.0) — Complete

Reference: `development/research/publish_plan_v1.0.0_2026-02-06.md`

- [x] **P01** Repo metadata (manifest `developer_url`, etc.) (+v1.0.0)
- [x] **P02** Icon + screenshots (+v1.0.0)
- [x] **P03** Branch/tag policy: `main` stable, `develop` includes `development/` (+v1.0.0)
- [x] **P04** Create GitHub repo + push (+v1.0.0)
- [x] **P05** Verify install from GitHub URL (+v1.0.0)
- [x] **P06** Submit to Ulauncher directory (+v1.0.0)

Testing:
- [x] Manual testing: `development/research/test_plan_v1.0.0_2026-02-06.md` (+v1.0.0)
- [x] Empty-task-list manual tests: `development/research/test_plan_v1.0.0_empty_tasks_2026-02-06.md` (+v1.0.0)
- [x] Unit tests: `nix-shell --run "pytest -q"` (+v1.0.0)

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
- [x] Optimized search with pre-computed lowercase index (+v0.6.7)
- [x] Performance profiling (+v0.6.7)
- [x] Adaptive display mode: ≤5 detailed, >5 compact (+v0.6.7)

---

## Notes

- Remember to update `extension/logs/dev_log.md` during each session
- Log issues in `extension/logs/issues.md` as they arise
- Log improvement ideas in `extension/logs/improvements.md`
- Make small, frequent git commits
- Test after each feature implementation

## Reminders

- **P07** Post-publish cleanup (ongoing, not version-tied)
  - Keep troubleshooting accurate (API key, rate limit, runtime log)
  - Use GitHub Releases for binaries/archives (avoid committing zips into repo)

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
