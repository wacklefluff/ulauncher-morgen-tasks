# Ulauncher Morgen Tasks Extension

Manage your [Morgen](https://morgen.so) tasks directly from [Ulauncher](https://ulauncher.io/) — list, search, create, and complete tasks without leaving your workflow.

**Current Version**: v1.1.0
**GitHub**: https://github.com/wacklefluff/ulauncher-morgen-tasks

> This is the `develop` branch (development workspace). For user-facing docs, see [extension/README.md](extension/README.md).

## Features

- **List & search tasks** — word-order independent search, adaptive display (detailed or compact)
- **Create tasks** — `mg new <title> [@due] [!priority]` with natural language dates
- **Mark tasks done** — `mg d <query>` to find and complete tasks
- **Task lists** — `mg lists`, `mg in <list>`, `mg project <name>`
- **Priority indicators** — `!!` (high), `!` (medium), overdue highlighting
- **Smart caching** — disk-persistent, 10-minute TTL, force refresh with `mg !`
- **Debug & help** — `mg help`, `mg debug` for runtime log access
- **Shortcut keyword** — `mgn` to create tasks directly

## Repository Structure

```
develop branch:
├── README.md                 # This file (project overview)
├── CHANGELOG.md              # Version history
├── TODO.md                   # Current tasks and roadmap
├── CLAUDE.md                 # AI agent development guide
├── AGENTS.md                 # AI agent quick reference
├── shell.nix                 # NixOS development environment
├── .gitignore
│
├── extension/                # Extension code (symlinked to Ulauncher)
│   ├── main.py               # Entry point
│   ├── manifest.json          # Extension metadata & preferences
│   ├── versions.json          # API version mapping
│   ├── README.md              # User-facing documentation
│   ├── images/                # Icon and screenshots
│   ├── src/
│   │   ├── morgen_api.py      # Morgen API client
│   │   ├── cache.py           # Disk-persistent task cache
│   │   ├── formatter.py       # Display formatting
│   │   ├── date_parser.py     # Natural language date parsing
│   │   └── task_lists.py      # Task list/container extraction
│   ├── tests/                 # Unit tests
│   ├── docs/                  # USER_GUIDE.md, API_REFERENCE.md
│   └── logs/                  # dev_log.md, issues.md, improvements.md
│
└── development/               # Development workspace (not on main)
    ├── research/              # Implementation plans and test plans
    ├── protocols/             # Git maintenance, release, handoff protocols
    └── handoff/               # AI agent handoff files
```

Note: `main` branch has a **flat layout** (extension files at root) required by Ulauncher's installer. See [release protocol](development/protocols/git_release_protocol_v1.0_2026-02-07.md).

## Development Setup

### Prerequisites

- NixOS (or Nix package manager)
- Ulauncher 5.x
- Morgen API key from https://platform.morgen.so

### Getting Started

```bash
cd /home/user/Documents/AI/Morgen-Tasks/
git checkout develop
nix-shell                    # enter dev environment

# Run tests
pytest -q

# Test extension manually
pkill ulauncher && ulauncher -v
# Type 'mg' in Ulauncher
```

### Extension Symlink

```
~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks
→ /home/user/Documents/AI/Morgen-Tasks/extension
```

## Development Workflow

1. Work on `develop` branch
2. Make small, frequent commits (`feat:`, `fix:`, `docs:`, etc.)
3. Update `CHANGELOG.md`, `TODO.md`, and `extension/logs/dev_log.md`
4. Test after each change: `pkill ulauncher && ulauncher -v`
5. Release to `main` using the [release protocol](development/protocols/git_release_protocol_v1.0_2026-02-07.md)

For AI agents: see `CLAUDE.md` for detailed guidelines.

## Release History

| Version | Highlights |
|---------|-----------|
| v1.1.0 | Task completion, task lists, debug command, shortcut keywords |
| v1.0.0 | First public release — list/search/create, caching, help, tests |
| v0.6.x | Polish: priority icons, overdue highlighting, runtime logging |
| v0.5.0 | Disk-persistent cache |
| v0.4.0 | Create tasks with due date parsing |
| v0.3.0 | List/search/refresh tasks |

See [CHANGELOG.md](CHANGELOG.md) for full details.

## Roadmap

Planned for future releases:

- Filter tasks by priority or due date
- Background cache refresh
- Subtask creation
- Recurring tasks support
- Desktop notifications for upcoming tasks

See [TODO.md](TODO.md) for the full backlog.

## Technology Stack

- **Language**: Python 3.10+ (stdlib only — no external dependencies)
- **Framework**: Ulauncher Extension API v2
- **API**: Morgen REST API v3
- **Environment**: NixOS / nix-shell

## Documentation

| Document | Purpose |
|----------|---------|
| [extension/README.md](extension/README.md) | User-facing installation and usage |
| [extension/docs/USER_GUIDE.md](extension/docs/USER_GUIDE.md) | Detailed user guide |
| [extension/docs/API_REFERENCE.md](extension/docs/API_REFERENCE.md) | Technical reference for developers |
| [CLAUDE.md](CLAUDE.md) | AI agent development guide |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [TODO.md](TODO.md) | Tasks and roadmap |

## License

MIT

## Resources

- [Morgen API Documentation](https://docs.morgen.so/)
- [Ulauncher Extension API](https://docs.ulauncher.io/)
- [Morgen Platform](https://platform.morgen.so)
