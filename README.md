# Ulauncher Morgen Tasks Extension

A comprehensive Ulauncher extension for managing Morgen tasks directly from your Linux desktop. List, search, and create tasks without leaving your workflow.

## Project Overview

This project integrates Morgen's task management system with Ulauncher, a fast application launcher for Linux. The extension allows you to quickly interact with your Morgen tasks using keyboard shortcuts and natural language commands.

## Features

### Current (v0.3.0 - Phase 3 Complete)
- ✅ Basic Ulauncher extension structure
- ✅ Keyword trigger (`mg` by default)
- ✅ API key configuration
- ✅ Morgen API integration with caching (cache-first to minimize API points)
- ✅ List all tasks (shows cached vs fresh status)
- ✅ Search tasks by title/description
- ✅ Force refresh (`mg refresh` or `mg !`) to bypass cache
- ✅ Copy task ID on Enter (for debugging)

### Planned
- ✅ **Phase 2**: API Integration & Authentication
- ✅ **Phase 3**: List and search tasks
- 🔄 **Phase 4**: Create tasks with natural language dates
- 🔄 **Phase 5**: Caching & performance optimization
- 🔄 **Phase 6**: Polish & error handling
- 🔄 **Phase 7**: Testing & v1.0.0 release

## Repository Structure

```
/home/user/Documents/AI/Morgen-Tasks/
│
├── README.md                      # This file - project overview
├── TODO.md                        # Current tasks and next steps
├── CLAUDE.md                      # Guide for AI agents working on this project
├── AGENTS.md                      # Quick reference for AI agents
├── CHANGELOG.md                   # Version history
├── .gitignore                     # Git ignore rules
│
├── extension/                     # Main extension code (symlinked to Ulauncher)
│   ├── main.py                    # Extension entry point
│   ├── manifest.json              # Extension metadata & preferences
│   ├── versions.json              # API version mapping
│   ├── README.md                  # User-facing documentation
│   │
│   ├── images/
│   │   └── icon.png              # Extension icon
│   │
│   ├── src/                      # Source modules (Phase 2+)
│   │   ├── morgen_api.py         # Morgen API client (planned)
│   │   ├── task_manager.py       # Task business logic (planned)
│   │   ├── cache.py              # Task caching (planned)
│   │   ├── formatter.py          # Display formatting (planned)
│   │   └── date_parser.py        # Natural language dates (planned)
│   │
│   ├── logs/                     # Development tracking
│   │   ├── dev_log.md           # Daily development journal
│   │   ├── issues.md            # Known issues and bugs
│   │   └── improvements.md      # Future enhancement ideas
│   │
│   ├── tests/                    # Test files (Phase 7)
│   │   ├── test_api.py          # API tests (planned)
│   │   └── test_date_parser.py  # Date parser tests (planned)
│   │
│   └── docs/                     # Additional documentation
│       ├── API_REFERENCE.md     # Morgen API quick reference (planned)
│       └── USER_GUIDE.md        # Detailed user guide (planned)
│
└── development/                  # Development workspace
    ├── research/                 # Research notes and findings
    ├── prototypes/               # Experimental code
    └── scratch/                  # Temporary testing files

Additional files:
├── (Morgen) Tasks - Morgen Developer Documentation.pdf
└── .git/                        # Git repository
```

## Installation

### For Users

1. **Clone or download this repository**:
   ```bash
   git clone <repository-url> /home/user/Documents/AI/Morgen-Tasks/
   cd /home/user/Documents/AI/Morgen-Tasks/
   ```

2. **The extension is already symlinked** to Ulauncher's extensions directory:
   ```
   ~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks
   → /home/user/Documents/AI/Morgen-Tasks/extension
   ```

3. **Get your Morgen API key**:
   - Visit https://platform.morgen.so
   - Sign up or log in
   - Request API access
   - Copy your API key

4. **Configure the extension**:
   - Open Ulauncher (Ctrl+Space)
   - Go to Preferences → Extensions
   - Find "Morgen Tasks"
   - Enter your API key
   - Customize keyword if desired (default: `mg`)

5. **Restart Ulauncher**:
   ```bash
   pkill ulauncher
   ulauncher &
   ```

### For Developers

See **CLAUDE.md** for detailed development setup and workflow.

## Usage

### Current Commands (Phase 1)

- `mg` - Trigger the extension (shows welcome message)

### Planned Commands (Future Phases)

- `mg` - List all tasks
- `mg search term` - Search tasks
- `mg new Task title` - Create task
- `mg new Task @tomorrow` - Create task with due date
- `mg new Task @tomorrow !1` - Create task with priority
- `mg help` - Show help

## Development Status

**Current Version**: v0.3.0 (Phase 3 Complete)
**Current Branch**: `develop`

### Completed Phases

- ✅ **Phase 0** (v0.0.1): Project structure and git setup
- ✅ **Phase 1** (v0.1.0): Basic extension structure
- ✅ **Phase 2** (v0.2.0): Morgen API integration and caching
- ✅ **Phase 3** (v0.3.0): List/search tasks + force refresh

### Next Phase

- 🔄 **Phase 4**: Create tasks

For detailed progress, see `extension/logs/dev_log.md`.

## Technology Stack

- **Language**: Python 3.6+
- **Framework**: Ulauncher Extension API v2
- **API**: Morgen REST API v3
- **Tools**: Git, ImageMagick

## Important Notes

### Morgen API Considerations

- **Rate Limiting**: List tasks endpoint costs 10 points per request
- **Caching Required**: Extension will cache tasks for 10 minutes by default
- **Date Format**: Morgen requires dates in format: `YYYY-MM-DDTHH:mm:ss` (exactly 19 characters)
- **Authentication**: API key required in header: `Authorization: ApiKey <API_KEY>`

### Development Workflow

1. Work on `develop` branch
2. Make small, frequent commits
3. Update `CHANGELOG.md` for each version
4. Log issues in `extension/logs/issues.md`
5. Log ideas in `extension/logs/improvements.md`
6. Keep `extension/logs/dev_log.md` updated

## Documentation

- **User Guide**: `extension/README.md` - End-user documentation
- **Development Guide**: `CLAUDE.md` - AI agent/developer guide
- **Agent Quick Reference**: `AGENTS.md` - Quick start for AI agents
- **Implementation Plan**: `.claude/plans/buzzing-waddling-fiddle.md` - Detailed implementation plan
- **Morgen API Docs**: `(Morgen) Tasks - Morgen Developer Documentation.pdf`
- **Development Log**: `extension/logs/dev_log.md`

## Testing

```bash
# Run Ulauncher in verbose mode for debugging
pkill ulauncher
ulauncher -v

# Type 'mg' to trigger the extension
```

## Contributing

This is currently a personal project. For development by AI agents, see `CLAUDE.md` and `AGENTS.md`.

## Versioning

This project uses [Semantic Versioning](https://semver.org/):
- `0.x.y` - Pre-release development
- `1.0.0` - First stable release
- `1.x.y` - Minor features and patches
- `2.0.0` - Breaking changes

## License

MIT

## Resources

- [Ulauncher Extension API](https://docs.ulauncher.io/en/stable/extensions/tutorial.html)
- [Morgen API Documentation](https://docs.morgen.so/)
- [Morgen Platform](https://platform.morgen.so)

## Contact

See `extension/logs/issues.md` for known issues and bugs.
