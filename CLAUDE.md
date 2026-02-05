# Claude AI Agent Guide - Morgen Tasks Extension

This document explains how AI agents (like Claude) should work on this project. It provides context, guidelines, and workflows for contributing effectively.

## Project Context

**What**: Ulauncher extension for managing Morgen tasks
**Goal**: Allow users to list, search, and create Morgen tasks from Ulauncher
**Current Status**: Phase 1 complete (v0.1.0) - Basic extension structure working
**Next Phase**: Phase 2 - Morgen API integration

## Quick Start for AI Agents

### 1. Understand the Current State

**Read these files first**:
1. `/home/user/Documents/AI/Morgen-Tasks/README.md` - Project overview
2. `/home/user/Documents/AI/Morgen-Tasks/TODO.md` - Current tasks
3. `/home/user/Documents/AI/Morgen-Tasks/extension/logs/dev_log.md` - Development progress
4. `/home/user/.claude/plans/buzzing-waddling-fiddle.md` - Detailed implementation plan

**Current directory**:
```bash
Working directory: /home/user/Documents/AI/Morgen-Tasks/
```

**Git status**:
```bash
Branch: develop
Latest commit: 53ce2b2 - docs: update dev log with Phase 0 and Phase 1 completion
```

### 2. Development Workflow

#### Starting a Session

1. **Check git status**:
   ```bash
   git status
   git log --oneline -5
   ```

2. **Review current TODO**:
   ```bash
   cat TODO.md
   ```

3. **Check recent development log**:
   ```bash
   cat extension/logs/dev_log.md
   ```

4. **Review any issues**:
   ```bash
   cat extension/logs/issues.md
   ```

#### During Development

1. **Make incremental changes**:
   - Work on ONE feature at a time
   - Test frequently
   - Commit working code even if incomplete

2. **Update logs**:
   - Add session notes to `extension/logs/dev_log.md`
   - Log bugs to `extension/logs/issues.md`
   - Log ideas to `extension/logs/improvements.md`

3. **Test changes**:
   ```bash
   # Restart Ulauncher in verbose mode
   pkill ulauncher
   ulauncher -v

   # Type 'mg' to test extension
   ```

4. **Commit frequently**:
   ```bash
   git add -A
   git commit -m "type: description"
   ```

   Commit types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

#### Ending a Session

1. **Update development log**:
   - Add what was accomplished
   - Note any issues encountered
   - List next steps

2. **Update TODO.md**:
   - Check off completed tasks
   - Add new tasks if discovered

3. **Commit all changes**:
   ```bash
   git add -A
   git commit -m "docs: update session log and TODO"
   ```

4. **Update CHANGELOG.md** (when version changes):
   - Add new version section
   - List changes under Added/Changed/Fixed

### 3. File Locations Reference

#### Core Extension Files
```
extension/
├── main.py              # Main extension code - EDIT THIS
├── manifest.json        # Extension metadata - EDIT THIS
├── versions.json        # API version mapping - RARELY EDIT
└── README.md           # User documentation
```

#### Source Modules (Phase 2+)
```
extension/src/
├── morgen_api.py       # Morgen API client - CREATE IN PHASE 2
├── cache.py            # Task caching - CREATE IN PHASE 2
├── task_manager.py     # Business logic - CREATE IN PHASE 3
├── formatter.py        # Display formatting - CREATE IN PHASE 3
└── date_parser.py      # Date parsing - CREATE IN PHASE 4
```

#### Development Tracking
```
extension/logs/
├── dev_log.md          # Daily development journal - UPDATE EVERY SESSION
├── issues.md           # Known bugs and issues - UPDATE AS NEEDED
└── improvements.md     # Future ideas - UPDATE AS NEEDED
```

#### Documentation
```
/home/user/Documents/AI/Morgen-Tasks/
├── README.md           # Project overview - UPDATE WHEN MAJOR CHANGES
├── TODO.md             # Task list - UPDATE FREQUENTLY
├── CHANGELOG.md        # Version history - UPDATE ON VERSION CHANGES
├── CLAUDE.md           # This file - for AI agents
├── AGENTS.md           # Quick reference for AI agents
└── .claude/plans/      # Implementation plans
```

#### Important External Files
```
~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks/
  → Symlink to extension/ directory
```

### 4. Implementation Phases

**Phase 0** ✅ Complete (v0.0.1)
- Project structure setup
- Git repository initialization
- Development logs created

**Phase 1** ✅ Complete (v0.1.0)
- Basic extension structure
- Manifest with preferences
- Extension responds to keyword

**Phase 2** 🔄 NEXT (Target: v0.2.0)
- Morgen API client (`src/morgen_api.py`)
- Task caching (`src/cache.py`)
- API integration test
- Error handling

**Phase 3** (Target: v0.3.0)
- Task formatting (`src/formatter.py`)
- List all tasks
- Search tasks by query
- Display in Ulauncher

**Phase 4** (Target: v0.4.0)
- Date parser (`src/date_parser.py`)
- Create task command
- Natural language dates
- Priority setting

**Phase 5** (Target: v0.5.0)
- Cache optimization
- Performance improvements
- Manual refresh option

**Phase 6** (Target: v0.6.0)
- Error message improvements
- UI polish
- Help command
- Documentation

**Phase 7** (Target: v1.0.0)
- Unit tests
- Manual testing
- Release preparation
- GitHub publication (optional)

### 5. Critical Technical Details

#### Morgen API

**Base URL**: `https://api.morgen.so/v3`

**Authentication**:
```python
headers = {
    "Authorization": f"ApiKey {api_key}",
    "accept": "application/json"
}
```

**Critical Endpoints**:

1. **List Tasks** (costs 10 points - MUST CACHE!)
   ```
   GET /v3/tasks/list?limit=100&updatedAfter=<ISO_DATE>
   ```

2. **Create Task**
   ```
   POST /v3/tasks/create
   Body: {"title": "Task title", "due": "2023-03-15T17:00:00", ...}
   ```

3. **Get Task**
   ```
   GET /v3/tasks?id=<TASK_ID>
   ```

**Date Format** (CRITICAL!):
- Must be exactly 19 characters: `YYYY-MM-DDTHH:mm:ss`
- NO timezone suffix (no Z, no +00:00)
- Use separate `timeZone` field

**Priority Values**:
- 0 = undefined
- 1 = highest
- 9 = lowest

**Task Progress States**:
- `needs-action`
- `in-process`
- `completed`
- `failed`
- `cancelled`

#### Ulauncher Extension API

**Extension Class**:
```python
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener

class MyExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, MyListener())
```

**Event Listener**:
```python
class MyListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        # Process query
        return RenderResultListAction(items)
```

**Result Items**:
```python
ExtensionResultItem(
    icon='images/icon.png',
    name='Task title',
    description='Due: tomorrow | Priority: High',
    on_enter=HideWindowAction()  # or ExtensionCustomAction
)
```

**Preferences**:
```python
api_key = extension.preferences.get("api_key", "")
```

### 6. Testing Guidelines

**Always test after making changes**:

```bash
# 1. Kill existing Ulauncher
pkill ulauncher

# 2. Start in verbose mode
ulauncher -v

# 3. Watch console output for errors

# 4. Type 'mg' in Ulauncher to trigger extension

# 5. Check for:
#    - Extension loads without errors
#    - Keyword triggers correctly
#    - Results display properly
#    - No Python exceptions in console
```

**Common Issues**:
- Syntax errors in Python → Check console output
- Extension not loading → Check manifest.json syntax
- Changes not appearing → Restart Ulauncher
- API errors → Check logs and error messages

### 7. Git Workflow

**Branch Strategy**:
- `develop` - Active development (work here)
- `main` - Stable releases only

**Commit Message Format**:
```
type: short description

Optional longer description

Optional breaking changes note
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Add tests
- `chore`: Maintenance
- `perf`: Performance

**Example**:
```bash
git add -A
git commit -m "feat: implement Morgen API client with error handling

- Created src/morgen_api.py with MorgenAPIClient class
- Added list_tasks() and create_task() methods
- Implemented error handling for network, auth, and rate limits
- Added unit tests for API client"
```

### 8. Common Commands

```bash
# Navigate to project
cd /home/user/Documents/AI/Morgen-Tasks/

# Check git status
git status
git log --oneline -10

# View development log
cat extension/logs/dev_log.md

# View TODO
cat TODO.md

# Test extension
pkill ulauncher && ulauncher -v

# Check symlink
ls -la ~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks/

# View API documentation
ls -la "(Morgen) Tasks - Morgen Developer Documentation.pdf"
```

### 9. What to Do Next

**If starting Phase 2**:

1. Read the Phase 2 section in `.claude/plans/buzzing-waddling-fiddle.md`
2. Create `extension/src/morgen_api.py`:
   - MorgenAPIClient class
   - __init__(api_key)
   - list_tasks() method
   - create_task() method
   - Error handling
3. Create `extension/src/cache.py`:
   - TaskCache class
   - get_tasks() with TTL
   - set_tasks()
   - invalidate()
4. Update `extension/main.py` to test API
5. Test with Ulauncher
6. Update logs
7. Commit changes

**Reference implementation plan**:
```bash
cat /home/user/.claude/plans/buzzing-waddling-fiddle.md
```

### 10. Important Reminders

✅ **DO**:
- Read dev_log.md before starting
- Make small, incremental commits
- Test after each change
- Update logs during session
- Handle errors gracefully
- Follow existing code style
- Check TODO.md for current tasks

❌ **DON'T**:
- Make large changes without testing
- Commit without testing
- Skip updating logs
- Forget to handle errors
- Hard-code API keys
- Ignore the implementation plan
- Work on multiple phases at once

### 11. Getting Help

**Documentation Locations**:
- Implementation plan: `.claude/plans/buzzing-waddling-fiddle.md`
- Morgen API docs: `(Morgen) Tasks - Morgen Developer Documentation.pdf`
- Ulauncher API: https://docs.ulauncher.io/
- Development issues: `extension/logs/issues.md`

**Debugging**:
- Run Ulauncher in verbose mode: `ulauncher -v`
- Check console output for Python errors
- Check `~/.local/share/ulauncher/last.log`
- Add logging: `logger.info("Debug message")`

### 12. Success Criteria

**For Each Phase**:
- [ ] Feature works as described
- [ ] Code is committed to git
- [ ] CHANGELOG.md updated
- [ ] Logs updated (dev_log.md)
- [ ] Extension still loads and runs
- [ ] No Python errors in console

**For v1.0.0 Release**:
- [ ] List/search tasks works
- [ ] Create tasks works
- [ ] Caching implemented
- [ ] Error handling robust
- [ ] Documentation complete
- [ ] Tested on real Morgen account
- [ ] No critical bugs

---

## Quick Reference Card

```
Project: Ulauncher Morgen Tasks Extension
Location: /home/user/Documents/AI/Morgen-Tasks/
Branch: develop
Current: Phase 1 complete (v0.1.0)
Next: Phase 2 - API integration (v0.2.0)

Essential Files:
- TODO.md - What to do next
- extension/logs/dev_log.md - Session notes
- extension/main.py - Main code
- .claude/plans/*.md - Implementation plan

Test Command:
  pkill ulauncher && ulauncher -v

Commit Template:
  git add -A
  git commit -m "feat: description"
```

---

Good luck with development! 🚀
