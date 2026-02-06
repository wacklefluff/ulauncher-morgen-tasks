# ENH-02: Condensed Display Mode (fzf-style)

**Date**: 2026-02-06
**Status**: Plan
**Related**: ENH-02 (T03), adaptive display mode

## Problem

When >5 results are returned, the current "condensed" mode still shows a subtitle
under each task. This looks identical to normal mode — just with shorter text.
The user wants condensed mode to look like the fzf Ulauncher extension: one line
per result, no subtitle at all.

## Research: How fzf Does It

The [ulauncher-fzf extension](https://github.com/hillaryychan/ulauncher-fzf)
uses **`ExtensionSmallResultItem`** instead of `ExtensionResultItem` for search
results. This is a built-in Ulauncher widget that renders without a description
line, allowing more items to fit on screen.

Source: [`src/results.py`](https://github.com/hillaryychan/ulauncher-fzf/blob/master/src/results.py)

```python
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem

# Used like:
ExtensionSmallResultItem(
    icon=icon,
    name=display_name,
    on_enter=OpenAction(path),
    on_alt_enter=alt_enter_action,
)
```

Key differences from `ExtensionResultItem`:
- No `description` parameter — the widget simply doesn't render a subtitle row
- Results take up ~50% less vertical space, fitting more items on screen
- Same `icon`, `name`, `on_enter` parameters

**Note**: In Ulauncher v6, `ExtensionSmallResultItem` is replaced by
`Result(compact=True)`. Our extension targets v5, so we use the v5 API.

## Plan

### What to Change

**File: `extension/main.py`**

1. Add import for `ExtensionSmallResultItem`:
   ```python
   from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
   ```

2. In the main display loop (~line 195-212), when `condensed=True`, use
   `ExtensionSmallResultItem` instead of `ExtensionResultItem`:
   ```python
   if condensed:
       items.append(ExtensionSmallResultItem(
           icon='images/icon.png',
           name=formatter.format_for_display(task),
           on_enter=on_enter
       ))
   else:
       items.append(ExtensionResultItem(
           icon='images/icon.png',
           name=formatter.format_for_display(task),
           description=formatter.format_subtitle(task),
           on_enter=on_enter
       ))
   ```

3. Same change in `_fallback_to_cache` (~line 624-639).

**File: `extension/src/formatter.py`**

4. Remove `format_condensed_subtitle` method — no longer needed since condensed
   mode won't show any subtitle.

### What Stays the Same

- `_MAX_NORMAL = 5` threshold (>5 triggers condensed)
- `_MAX_CONDENSED = 15` max items in condensed mode
- `format_for_display()` — title still includes `!!`, `!`, and `OVERDUE` prefix
- `format_subtitle()` — still used for normal mode (<=5 results)

### Display Behavior Summary

| Condition       | Widget                     | Max Items | Title                          | Subtitle          |
|-----------------|----------------------------|-----------|--------------------------------|--------------------|
| Results <= 5    | ExtensionResultItem        | 5         | `OVERDUE !! Task title`        | Full due/priority  |
| Results > 5     | ExtensionSmallResultItem   | 15        | `OVERDUE !! Task title`        | (none)             |

### Risk / Fallback

- `ExtensionSmallResultItem` has been in Ulauncher since v5.x — well-established
- If the import fails (unlikely), we can wrap it in a try/except and fall back to
  `ExtensionResultItem` with `description=""` as a degraded fallback

## Test Plan

1. `mg ` (list all, >5 tasks) — should show up to 15 tasks, single-line each
2. `mg <search>` returning <=5 results — should show normal mode with subtitles
3. `mg <search>` returning >5 results — should show condensed single-line mode
4. Verify priority icons and OVERDUE prefix still visible in condensed mode
5. Verify click-to-copy-ID still works in condensed mode
