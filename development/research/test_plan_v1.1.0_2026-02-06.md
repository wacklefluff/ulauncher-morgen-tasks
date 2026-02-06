# Test Plan — v1.1.0

**Date**: 2026-02-06
**Prereq**: Restart Ulauncher: `pkill ulauncher && ulauncher -v`

---

## SUG-04 — Show creation date when no due date

### S04-01: No due date shows Created
**Test**: Find a task with no due date and run `mg` (or search it by title).
**Expected**: Task subtitle shows `Created: YYYY-MM-DD` (not `Due: No due date`).
**Result**: [X] PASS  [ ] FAIL

### S04-02: Due date still shows Due
**Test**: Find a task with a due date and run `mg` (or search it by title).
**Expected**: Task subtitle starts with `Due: ...` and uses relative labels when applicable.
**Result**: [X] PASS  [ ] FAIL

### S04-03: Missing created falls back
**Test**: (Edge case) If any task is missing `created`, check its subtitle.
**Expected**: Subtitle falls back to `Due: No due date`.
**Result**: [ ] PASS  [ ] FAIL  [X] SKIP

