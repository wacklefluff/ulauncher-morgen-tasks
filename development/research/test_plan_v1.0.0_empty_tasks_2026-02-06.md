# Manual Test Plan v1.0.0 — Empty Task List (Dev Toggle)

**Date**: 2026-02-06
**Version**: v1.0.0
**Purpose**: Validate UI behavior when there are 0 tasks, without needing an empty Morgen account.

## Setup

1. Open extension preferences
2. Set `Dev: Simulate empty task list (0/1)` to `1`
3. Start Ulauncher in verbose mode: `pkill ulauncher && ulauncher -v`

---

## Tests

### E01: List All Tasks (Empty)
**Test**: Type `mg ` (with space)
**Expected**:
- Header shows `Morgen Tasks (0)`
- Shows a `No tasks found` item
- No API call is made (runtime log should NOT show “Fetching tasks from API...”)
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### E02: Search (Empty)
**Test**: Type `mg anything`
**Expected**:
- Header shows `Morgen Tasks (0)`
- Shows a `No tasks found` item
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### E03: Refresh (Empty)
**Test**: Type `mg refresh`
**Expected**:
- Still shows 0 tasks
- No API call is made (dev-empty is a no-op even with refresh)
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

---

## Cleanup

1. Set `Dev: Simulate empty task list (0/1)` back to `0`
