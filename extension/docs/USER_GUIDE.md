# User Guide - Ulauncher Morgen Tasks

A complete guide to using the Morgen Tasks extension for Ulauncher.

## Getting Started

### 1. Get Your API Key

1. Go to https://platform.morgen.so
2. Sign in with your Morgen account
3. Navigate to API settings
4. Generate or copy your API key

### 2. Configure the Extension

1. Open Ulauncher (usually `Ctrl+Space`)
2. Open preferences (`Ctrl+,` or click the gear icon)
3. Go to the **Extensions** tab
4. Find **Morgen Tasks**
5. Enter your API key
6. Optionally adjust the cache duration (default: 600 seconds / 10 minutes)
7. (Optional) Set **Task Open URL Template** to control what opens when you press Enter on a task (opens Morgen; no official per-task deep link support)

#### Where Your API Key Is Stored

Ulauncher stores extension preferences (including your Morgen API key) **unencrypted** in a local SQLite DB. Typical path:

- `~/.config/ulauncher/ext_preferences/ulauncher-morgen-tasks.db`

The extension reads it via `extension.preferences` at runtime and does not store it in this repository.

### 3. Start Using

Type `mg` in Ulauncher to see your tasks!

---

## Commands Reference

### Viewing Tasks

**List all tasks:**
```
mg
```
Shows all your Morgen tasks. Uses cached data if available (faster, saves API quota).

**Search tasks:**
```
mg meeting
mg project review
```
Filters tasks by title or description. Case-insensitive.

**Mark task as done:**
```
mg d meeting
```
Shows matching tasks; pressing Enter marks the selected task as done in Morgen.

**Force refresh:**
```
mg !
mg refresh
```
Bypasses the cache and fetches fresh data from Morgen API.

### Creating Tasks

**Basic task:**
```
mg new Buy groceries
```

**Task with due date:**
```
mg new Buy groceries @tomorrow
mg new Call dentist @next-mon
mg new Submit report @2026-02-15
```

**Task with time:**
```
mg new Team meeting @tomorrow 3pm
mg new Standup @today 9:30
```

**Task with priority:**
```
mg new Urgent fix !1
mg new Normal task !5
mg new Low priority !9
```

**Combining options:**
```
mg new Client call @tomorrow 2pm !1
```

### Due Date Formats

| Format | Example | Result |
|--------|---------|--------|
| `today` | `@today` | Today at 9:00 AM |
| `tomorrow` | `@tomorrow` | Tomorrow at 9:00 AM |
| `next-week` | `@next-week` | 7 days from now |
| `next-<day>` | `@next-mon` | Next Monday |
| `YYYY-MM-DD` | `@2026-02-15` | Specific date |
| `MM-DD` | `@02-15` | Date this year (or next if passed) |
| Time only | `@3pm` | Today/tomorrow at that time |

**Weekday abbreviations:** `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`

### Priority Levels

Morgen uses four priority levels:

| Input | Level | Display |
|-------|-------|---------|
| `!1`, `!2`, `!3` | High | `!! Task Name` |
| `!4`, `!5` | Medium | `! Task Name` |
| `!6`, `!7`, `!8`, `!9` | Low | `Task Name` |
| (none) | Normal | `Task Name` |

### Utility Commands

**Show help:**
```
mg help
mg ?
```

**Clear cache:**
```
mg clear
```
Removes cached tasks. Next `mg` will fetch fresh data.

---

## Understanding the Display

### Task Title

```
!! Buy groceries
```
- `!!` = High priority
- `!` = Medium priority
- `OVERDUE` prefix = Task is past due

### Task Subtitle

```
Due: Tomorrow 14:00 | Priority: High
```

**Due date formats:**
- `Today 14:00` - Due today
- `Tomorrow 09:00` - Due tomorrow
- `2026-02-15 10:00` - Future date
- `2026-02-01 09:00 (overdue!)` - Past due
- `No due date` - No due date set

---

## Caching

The extension caches your tasks to:
- Reduce API calls (Morgen has rate limits)
- Speed up responses
- Work offline with stale data

**Default cache duration:** 10 minutes

**Cache indicators** appear in the task count header:
- `(fresh)` - Just fetched
- `(2m ago)` - Cached 2 minutes ago
- etc.

**To get fresh data:**
- Wait for cache to expire, or
- Run `mg !` or `mg refresh`

---

## Troubleshooting

### No Tasks Appearing

1. Check your API key in preferences
2. Run `mg !` to force refresh
3. Check the runtime log for errors

### "Rate limit exceeded"

Morgen's API has usage limits. Wait a few minutes and try again. The extension shows cached data as a fallback.

### "Authentication failed"

Your API key may be invalid or expired. Generate a new one at https://platform.morgen.so

### Viewing Logs

1. Run `mg debug`
2. Select "Open runtime log" or "Copy log path"

Log location: `extension/logs/runtime.log`

### Extension Not Loading

1. Restart Ulauncher: `pkill ulauncher && ulauncher -v`
2. Check terminal output for Python errors
3. Verify the symlink exists:
   ```bash
   ls -la ~/.local/share/ulauncher/extensions/ulauncher-morgen-tasks
   ```

---

## Tips

1. **Quick task capture**: Just type `mg new` followed by your task
2. **Natural dates**: Use `@tomorrow`, `@next-fri` instead of specific dates
3. **Search first**: Before creating, search to avoid duplicates
4. **Refresh sparingly**: Caching helps stay within API limits

---

## Keyboard Shortcuts

In Ulauncher:
- `Enter` on a task: Open in Morgen
- `Alt+Enter` on a task: Copy task ID (if supported by your Ulauncher version)
- `Enter` in done mode (`mg d ...`): Mark task as done
- `Escape`: Close Ulauncher
- `Ctrl+,`: Open preferences

---

## Version History

See [CHANGELOG.md](../../CHANGELOG.md) for full version history.

Current: **v1.0.0**
