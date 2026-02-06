# SUG-02: Move log access to `mg debug` command

**Date**: 2026-02-06
**Status**: Planned

## Goal
Remove log access items ("Open runtime log", "Copy log path") from help and error screens. Add a dedicated `mg debug` command that shows them instead.

## File to modify
- `extension/main.py`

## Changes

### 1. Add `mg debug` to the command router
In `on_event()`, add a check for the debug command alongside the existing help/clear/new checks. Trigger on: `debug`, `log`, `logs`.

### 2. Create `_maybe_build_debug_flow()` method
Similar to `_maybe_build_help_flow()`. Shows:
- Header: "Morgen Tasks — Debug"
- "Open runtime log" item (existing logic from `_runtime_log_access_items`)
- "Copy log path" item (existing logic)
- Runtime log path hint

### 3. Remove `_runtime_log_access_items()` calls from:
- `_maybe_build_help_flow()` (line ~346) — remove both the "Runtime logs" hint item and the `_runtime_log_access_items()` call. Replace with a single item pointing users to `mg debug`.
- `_error_items()` (line ~709) — remove the call. Add a text hint "Run `mg debug` for logs" in the error description instead.
- `_fallback_to_cache()` no-cache branch (line ~650) — same: remove call, add text hint.
- Welcome/missing API key screen (line ~138) — same: remove call, add text hint.

### 4. Add `mg debug` to help screen examples
Add a line in the help examples list: `("Debug / logs", "mg debug")`.

## Verification
- `mg debug` → shows log access items
- `mg help` → no longer shows log access items, shows "mg debug" in examples
- Error screens → no longer show log items, mention `mg debug` in description
- Restart Ulauncher and test: `pkill ulauncher && ulauncher -v`
