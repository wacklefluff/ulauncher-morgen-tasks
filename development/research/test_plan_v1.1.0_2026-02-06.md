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

---

## Mark task as done — `mg d [taskname]`

### D01: Done mode search
**Test**: Type `mg d <some task word>`
**Expected**: List of matching tasks; header shows "Morgen Tasks — Done".
**Result**: [X] PASS  [ ] FAIL

### D02: Enter marks task done
**Test**: In `mg d <query>` results, select a task and press Enter.
**Expected**: Task is marked as done in Morgen; UI shows confirmation "Task marked as done".
**Result**: [X] PASS  [ ] FAIL

### D03: Task disappears from normal list
**Test**: After D02, run `mg refresh` and search for the task.
**Expected**: Completed task no longer appears in the active task list (or is shown as completed if Morgen returns completed tasks).
**Result**: [X] PASS  [ ] FAIL

### D04: `mg d` with no query lists tasks
**Test**: Type `mg d`
**Expected**: Shows tasks (same as `mg`, but Enter marks done).
**Result**: [X] PASS  [ ] FAIL

### D05: Done mode supports one-shot refresh
**Test**: Type `mg d refresh` (or `mg d !`)
**Expected**: Cache invalidated and tasks fetched from API once; header still shows Done mode.
**Result**: [X] PASS  [ ] FAIL

### D06: Normal mode Enter still copies ID
**Test**: Type `mg <query>`, select a task, press Enter.
**Expected**: Task ID is copied to clipboard (if supported by your Ulauncher version); task is not completed.
**Result**: [X] PASS  [ ] FAIL  [ ] SKIP

---

## Open task on Enter (default)

### O02: Alt+Enter copies task ID (if supported)
**Test**: Type `mg <query>`, select a task, press Alt+Enter.
**Expected**: Task ID is copied to clipboard (if your Ulauncher version supports Alt+Enter actions).
**Result**: [X] PASS  [ ] FAIL  [ ] SKIP

**Note**: "Task Open URL Template" opens Morgen, but Morgen does not currently offer an official way to deep-link to a specific task.
