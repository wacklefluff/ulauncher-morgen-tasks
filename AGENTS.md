# AI Agent Quick Reference

Quick reference guide for AI agents working on the Ulauncher Morgen Tasks Extension.

## TL;DR

**Project**: Ulauncher extension for managing Morgen tasks
**Location**: `/home/user/Documents/AI/Morgen-Tasks/`
**Status**: Phase 1 complete ✅ → Phase 2 next 🔄
**Branch**: `develop`

## Handoff Protocol

### When to Write a Handoff
Write a handoff file at **natural break points**:
- After completing a sub-task (e.g., finished one file, moving to next)
- Before starting a large/risky change
- When user says "pause", "stop", or "switch agents"
- If you receive a rate limit error
- Before context compaction/conversation restart

### Ask User to Check Rate Limits
At natural break points, ask: *"Should I continue or would you like to check rate limits first?"*

**How users check rate limits:**
- **Claude Code**: Run `/status` or check "Account and usage..." in settings
- **Codex CLI**: Run `codex --usage` or check OpenAI dashboard
- **Gemini CLI**: Check Google AI Studio usage dashboard
- **GitHub Copilot**: GitHub settings → Copilot → Usage

### Handoff File Format
Create `development/handoff/handoff_YYYY-MM-DD_HHmm.md`:

```markdown
# AI Agent Handoff

**Agent**: [Model name]
**Timestamp**: YYYY-MM-DD HH:mm
**Reason**: [Natural break / User request / Rate limit / Context limit]

## Current Task
[What you were working on]

## Progress Made
- [Completed items]

## Next Steps
1. [Immediate next action]
2. [Following actions]

## Files Modified (uncommitted)
- [List any uncommitted changes]

## Notes for Next Agent
[Context, gotchas, important information]
```

### For Continuing Agents
1. Check `development/handoff/` for recent handoff files
2. Read the most recent handoff to understand context
3. Continue from where previous agent stopped
4. Archive completed handoff file to `development/handoff/archive/`

---

## What to Do First

1. **Read these files** (in order):
   ```bash
   cat README.md                           # Project overview
   cat TODO.md                              # Current tasks
   cat extension/logs/dev_log.md            # Recent progress
   ls development/research/                                  # Implementation plans
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
- ✅ Phase 2: API integration (v0.2.0)
- 🔄 **Phase 3: List/search tasks (v0.3.0) ← YOU ARE HERE**
- ⏳ Phase 4: Create tasks
- ⏳ Phase 5: Performance
- ⏳ Phase 6: Polish
- ⏳ Phase 7: Release

## Next Steps (Phase 3)

Create/update these files:

1. **`extension/src/formatter.py`** - Display formatting
   - Class: `TaskFormatter`
   - Methods: `format_for_display(task)`, `format_subtitle(task)`
   - Helper: `get_priority_icon(priority)`

2. **Update `extension/main.py`**
   - Show all tasks when no query provided
   - Implement search filtering by query
   - Add force refresh command (`mg refresh` or `mg !`)
   - Handle empty task list gracefully

3. **Test list/search functionality**
   - Test listing all tasks
   - Test search by title/description
   - Test force refresh bypasses cache

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

### Plans & Research
- `development/research/` - Implementation plans (always write new plans here as `<name>_<date>.md`)

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

## Package Management (NixOS)

This is a **NixOS** system. Use `shell.nix` for all dependencies.

- **Never use `pip install`** — it won't persist on NixOS
- Edit `shell.nix` to add packages, then run `nix-shell`
- Python packages: `python3Packages.<name>` in `buildInputs`
- System tools: `pkgs.<name>` in `buildInputs`

```bash
# Enter dev environment
nix-shell

# Add a package: edit shell.nix, then re-enter
nix-shell
```

## Essential Commands

```bash
# Navigate to project
cd /home/user/Documents/AI/Morgen-Tasks/

# Enter dev environment (NixOS)
nix-shell

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
   - Update `TODO.md` (check off tasks + refresh context)
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

### Manual Test Requests (Protocol)

When asking the user to run manual tests:

1. Always provide a **numbered** test list with stable IDs (e.g. `T01`, `T02`, ...).
2. Always write the test plan to a `.md` file for reference:
   - `development/research/test_plan_<version>_<YYYY-MM-DD>.md`
3. In follow-ups, reference failures by **test ID** so issues are easy to report and reproduce.

### Updating `TODO.md` (Protocol)

Whenever you modify `TODO.md`, also update the file’s *context*:

1. Check off any tasks that are now completed (including manual test items).
2. Update **Immediate Next Steps** so it reflects what the user should do *next* (not already-finished phases).
3. Keep the version/status lines accurate (current version/phase, last updated date).
4. Use the **Release Checklist** in `TODO.md` for every feature/fix (don’t treat “logs + commit” as a one-time per-phase step).
5. Append a version tag when a task is completed, e.g. `(+v0.6.0)`.

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

## Phase 3 Checklist

- [ ] Create `extension/src/formatter.py`
- [ ] Update `extension/main.py` to display all tasks
- [ ] Implement search filtering by query
- [ ] Add force refresh command
- [ ] Handle empty task list
- [ ] Test listing all tasks
- [ ] Test search functionality
- [ ] Test force refresh
- [ ] Update `extension/logs/dev_log.md`
- [ ] Update `TODO.md`
- [ ] Update `CHANGELOG.md` to v0.3.0
- [ ] Commit: `git commit -m "feat: list and search tasks"`

## Resources

**Full Guide**: Read `CLAUDE.md` for detailed information

**Implementation Plans**: `development/research/`

**Git Maintenance Protocol**: `development/protocols/git_maintenance_protocol_2026-02-07.md`

**Morgen API Docs**: `(Morgen) Tasks - Morgen Developer Documentation.pdf`

**Ulauncher API**: https://docs.ulauncher.io/

## Questions?

1. Check `CLAUDE.md` for detailed explanations
2. Check `extension/logs/issues.md` for known problems
3. Check implementation plans in `development/research/`
4. Review Morgen API PDF documentation

---

**Remember**:
- Update logs every session
- Test after each change
- Commit frequently
- Read the implementation plan!

Good luck! 🚀
