# AI Agent Quick Reference

Quick reference guide for AI agents working on the Ulauncher Morgen Tasks Extension.

## TL;DR

**Project**: Ulauncher extension for managing Morgen tasks
**Location**: `/home/user/Documents/AI/Morgen-Tasks/`
**Status**: Phase 1 complete ✅ → Phase 2 next 🔄
**Branch**: `develop`

## What to Do First

1. **Read these files** (in order):
   ```bash
   cat README.md                           # Project overview
   cat TODO.md                              # Current tasks
   cat extension/logs/dev_log.md            # Recent progress
   cat /home/user/.claude/plans/buzzing-waddling-fiddle.md  # Detailed plan
   ```

2. **Check git status**:
   ```bash
   cd /home/user/Documents/AI/Morgen-Tasks/
   git status
   git log --oneline -5
   ```

3. **Start working on next task** in `TODO.md`

## Current Status

- ✅ Phase 0: Project setup (v0.0.1)
- ✅ Phase 1: Basic extension (v0.1.0)
- 🔄 **Phase 2: API integration (v0.2.0) ← YOU ARE HERE**
- ⏳ Phase 3: List/search tasks
- ⏳ Phase 4: Create tasks
- ⏳ Phase 5: Performance
- ⏳ Phase 6: Polish
- ⏳ Phase 7: Release

## Next Steps (Phase 2)

Create these files:

1. **`extension/src/morgen_api.py`** - Morgen API client
   - Class: `MorgenAPIClient`
   - Methods: `list_tasks()`, `create_task()`
   - Error handling: network, auth, rate limits

2. **`extension/src/cache.py`** - Task caching
   - Class: `TaskCache`
   - TTL: 600 seconds (10 minutes)
   - Methods: `get_tasks()`, `set_tasks()`, `invalidate()`

3. **Update `extension/main.py`**
   - Import API client
   - Test API connection
   - Display results or errors

## Key Files

### Code
- `extension/main.py` - Main extension logic
- `extension/manifest.json` - Extension metadata
- `extension/src/` - Source modules (create in Phase 2)

### Documentation
- `README.md` - Project overview
- `TODO.md` - Task list
- `CLAUDE.md` - Detailed guide (read this for more info)
- `CHANGELOG.md` - Version history
- `extension/README.md` - User guide

### Logs
- `extension/logs/dev_log.md` - Development journal ← **UPDATE EVERY SESSION**
- `extension/logs/issues.md` - Known bugs
- `extension/logs/improvements.md` - Future ideas

### Plans
- `/home/user/.claude/plans/buzzing-waddling-fiddle.md` - Implementation plan

## Critical Information

### Morgen API
- **Base URL**: `https://api.morgen.so/v3`
- **Auth Header**: `Authorization: ApiKey <API_KEY>`
- **List endpoint**: Costs 10 points → **MUST CACHE!**
- **Date format**: `YYYY-MM-DDTHH:mm:ss` (exactly 19 chars, no timezone)

### File Structure
```
/home/user/Documents/AI/Morgen-Tasks/
├── extension/              # ← Main extension code (symlinked to Ulauncher)
│   ├── main.py
│   ├── manifest.json
│   ├── src/               # ← Create modules here
│   └── logs/              # ← Update these!
├── development/            # Research and experiments
├── README.md
├── TODO.md
├── CLAUDE.md              # ← Read this for detailed info
└── .git/
```

### Symlink
```
~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks/
→ /home/user/Documents/AI/Morgen-Tasks/extension/
```

## Essential Commands

```bash
# Navigate to project
cd /home/user/Documents/AI/Morgen-Tasks/

# Test extension
pkill ulauncher && ulauncher -v

# Commit changes
git add -A
git commit -m "feat: description"

# View logs
cat extension/logs/dev_log.md
cat TODO.md
```

## Workflow

1. **Start Session**:
   - Read `dev_log.md` and `TODO.md`
   - Check git status

2. **During Work**:
   - Make small changes
   - Test frequently: `pkill ulauncher && ulauncher -v`
   - Update `dev_log.md` with progress

3. **End Session**:
   - Update `dev_log.md` with accomplishments
   - Update `TODO.md` (check off tasks)
   - Commit: `git add -A && git commit -m "type: description"`

## Testing

```bash
# 1. Restart Ulauncher
pkill ulauncher
ulauncher -v

# 2. Type 'mg' to trigger extension

# 3. Watch console for errors

# 4. Check logs
cat ~/.local/share/ulauncher/last.log
```

## Git Commits

Format: `type: description`

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code restructuring
- `test` - Tests
- `chore` - Maintenance
- `perf` - Performance

Example:
```bash
git commit -m "feat: implement Morgen API client with caching"
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Extension not loading | Check `ulauncher -v` console output |
| Changes not appearing | Restart Ulauncher |
| Python errors | Check syntax, imports, and console |
| API errors | Verify API key in preferences |
| Import errors | Check file paths and module names |

## Phase 2 Checklist

- [ ] Create `extension/src/morgen_api.py`
- [ ] Create `extension/src/cache.py`
- [ ] Update `extension/main.py` to use API client
- [ ] Test with valid API key
- [ ] Test with invalid API key
- [ ] Test error handling
- [ ] Update `extension/logs/dev_log.md`
- [ ] Update `TODO.md`
- [ ] Update `CHANGELOG.md` to v0.2.0
- [ ] Commit: `git commit -m "feat: Morgen API integration"`

## Resources

**Full Guide**: Read `CLAUDE.md` for detailed information

**Implementation Plan**: `/home/user/.claude/plans/buzzing-waddling-fiddle.md`

**Morgen API Docs**: `(Morgen) Tasks - Morgen Developer Documentation.pdf`

**Ulauncher API**: https://docs.ulauncher.io/

## Questions?

1. Check `CLAUDE.md` for detailed explanations
2. Check `extension/logs/issues.md` for known problems
3. Check implementation plan in `.claude/plans/`
4. Review Morgen API PDF documentation

---

**Remember**:
- Update logs every session
- Test after each change
- Commit frequently
- Read the implementation plan!

Good luck! 🚀
