# Development Log

## 2026-02-05

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
