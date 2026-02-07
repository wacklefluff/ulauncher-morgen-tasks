# Ulauncher Morgen Tasks Extension

Manage your Morgen tasks directly from Ulauncher - list, search, and create tasks quickly without leaving your workflow.

![New Task Screenshot](images/screenshots/v1.0-New-Task-bg.jpg)

## Features

- **List tasks** - View all your Morgen tasks at a glance
- **Search tasks** - Filter by title or description
- **Create tasks** - Quick task creation with natural language dates
- **Priority indicators** - Visual markers for high (`!!`) and medium (`!`) priority
- **Overdue highlighting** - Tasks past due are clearly marked
- **Smart caching** - Minimizes API calls with 10-minute cache (configurable)
- **Force refresh** - Bypass cache when you need fresh data

## Installation

1. Clone or symlink this extension to Ulauncher's extensions directory:
   ```bash
   ln -s /path/to/extension ~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks
   ```

2. Restart Ulauncher

3. Open Ulauncher preferences (Extensions tab) and configure:
   - **Keyword**: `mg` (default, customizable)
   - **New Task Shortcut Keyword**: `mgn` (optional; creates tasks directly)
   - **API Key**: Your Morgen API key from https://platform.morgen.so
   - **Cache Duration**: Seconds to cache tasks (default: 600)

### Where Your API Key Is Stored

Ulauncher stores extension preferences (including the API key) **unencrypted** in a local SQLite DB. On this system the path is:

- `~/.config/ulauncher/ext_preferences/ulauncher-morgen-tasks.db`

This extension reads the key via `extension.preferences` at runtime and does not store it in this repository.

## Usage

### List & Search Tasks

| Command | Description |
|---------|-------------|
| `mg` | List all tasks |
| `mg <term>` | Search tasks by title/description |
| `mg !` | Force refresh (bypass cache) |
| `mg refresh` | Force refresh (alternative) |
| `mg lists` | Show all detected containers (list/project/space) |
| `mg list` | Show list-kind containers only |
| `mg project` | Show project-kind containers only |
| `mg space` | Show space-kind containers only |
| `mg in <list> [term]` | Filter/search within a list (when available) |
| `mg list <name> [term]` | Filter/search within a specific list-kind container |
| `mg project <name> [term]` | Filter/search within a specific project-kind container |
| `mg space <name> [term]` | Filter/search within a specific space-kind container |
| `mg d <term>` | Search tasks and press Enter to mark as done |

### Create Tasks

| Command | Description |
|---------|-------------|
| `mg new Buy milk` | Create task with title only |
| `mgn Buy milk` | Create task (shortcut keyword; configurable in preferences) |
| `mg new Buy milk @tomorrow` | Create with due date |
| `mg new Buy milk @tomorrow !1` | Create with due date and high priority |
| `mg new Meeting @next-mon 3pm` | Due next Monday at 3pm |

**Due date formats**: `today`, `tomorrow`, `next-week`, `next-mon`, `2026-02-15`, `3pm`, `15:30`

**Priority**: `!1` (high), `!5` (medium), `!9` (low)

### Utility Commands

| Command | Description |
|---------|-------------|
| `mg help` or `mg ?` | Show command reference |
| `mg clear` | Clear cached tasks |
| `mg debug` | Debug/log screen (open/copy runtime log path) |
| `mg dev dummy-tasks` | Dev helper: choose 10/50/90 create or bulk-complete dummy tasks (`#dev Testing ...`) |

### Task Actions

- `Enter` on a task (normal mode): No action
- `Alt+Enter` on a task: Copy task ID (if supported by your Ulauncher version)
- `Enter` in done mode (`mg d ...`): Mark task as done

### Task Display

- `!! Task Name` - High priority task
- `! Task Name` - Medium priority task
- `OVERDUE !! Task Name` - Overdue high priority task
- Subtitle shows: `Due: Today 14:00 | Priority: High`

## Troubleshooting

### View Runtime Logs

Run `mg debug`, then select "Open runtime log" or "Copy log path".

Log location: `logs/runtime.log` (relative to extension root)

### Common Issues

- **No tasks showing**: Check API key in preferences
- **Rate limit errors**: Wait a few minutes, Morgen API has usage limits
- **Stale data**: Run `mg !` to force refresh

### Testing

```bash
pkill ulauncher && ulauncher -v
```

Then type `mg` to trigger the extension.

## Requirements

- Ulauncher 5.x
- Python 3.10+
- Morgen API key

## Current Version

**v1.1.0** - Task completion, task lists, debug command, shortcut keywords

## Roadmap

Planned for future releases:

- Filter tasks by priority or due date
- Background cache refresh
- Subtask creation
- Recurring tasks support
- Desktop notifications for upcoming tasks

See the full backlog in the [development TODO](https://github.com/wacklefluff/ulauncher-morgen-tasks/tree/develop).

## Resources

- [Morgen API Documentation](https://docs.morgen.so/)
- [Ulauncher Extension API](https://docs.ulauncher.io/)
- [User Guide](docs/USER_GUIDE.md)

## License

MIT
