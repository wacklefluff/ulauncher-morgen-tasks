# Ulauncher Morgen Tasks Extension

Manage your Morgen tasks directly from Ulauncher - list, search, and create tasks quickly without leaving your workflow.

## Features

- List and search your Morgen tasks
- Create new tasks with natural language date parsing
- Smart caching to minimize API calls
- Priority and due date display

## Installation

### Development Installation

The extension is currently symlinked from this development directory:

```bash
~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks -> /home/user/Documents/AI/Morgen-Tasks/extension
```

### Configuration

1. Open Ulauncher preferences
2. Go to Extensions tab
3. Find "Morgen Tasks" extension
4. Configure your preferences:
   - **Keyword**: `mg` (or customize)
   - **API Key**: Your Morgen API key from https://platform.morgen.so
   - **Cache Duration**: How long to cache tasks (default: 600 seconds)

## Usage

### Phase 1 (Current - v0.1.0)

Basic extension that responds to keyword:
- Type `mg` to test the extension
- Shows welcome message if API key not configured
- Shows success message if API key is configured

### Planned Features

**Phase 2** - API Integration
- Connect to Morgen API
- Fetch and cache tasks

**Phase 3** - List/Search Tasks
- `mg` - Show all tasks
- `mg search term` - Search tasks

**Phase 4** - Create Tasks
- `mg new Buy milk` - Create task
- `mg new Buy milk @tomorrow` - Create with due date
- `mg new Buy milk @tomorrow !1` - Create with priority

## Development

### Testing

Restart Ulauncher in verbose mode to see extension output:

```bash
# Kill Ulauncher
pkill ulauncher

# Start in verbose mode
ulauncher -v
```

Then type `mg` to trigger the extension.

### Project Structure

```
extension/
├── main.py                # Main extension code
├── manifest.json          # Extension metadata
├── versions.json          # API version mapping
├── images/
│   └── icon.png          # Extension icon
├── src/                  # Source modules (Phase 2+)
├── logs/                 # Development logs
├── tests/                # Test files
└── docs/                 # Documentation
```

### Git Workflow

- `develop` branch - active development
- `main` branch - stable releases
- Semantic versioning (0.x.y → 1.0.0)

### Development Log

See `logs/dev_log.md` for detailed development progress.

## Requirements

- Ulauncher 5.x
- Python 3.6+
- Morgen API key (get from https://platform.morgen.so)

## Current Status

**Version**: 0.1.0 (Phase 1 complete)
**Status**: Basic extension structure working

## Resources

- [Morgen API Documentation](https://docs.morgen.so/)
- [Ulauncher Extension API](https://docs.ulauncher.io/en/stable/extensions/tutorial.html)

## License

MIT

## Support

For issues or questions, see `logs/issues.md` in the development directory.
