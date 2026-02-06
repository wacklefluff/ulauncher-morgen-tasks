# Test Plan — SUG-02: `mg debug` command

**Date**: 2026-02-06
**Prereq**: Restart Ulauncher: `pkill ulauncher && ulauncher -v`

---

## Debug command

### T01: `mg debug` triggers debug screen
**Test**: Type `mg debug`
**Expected**: Shows header "Morgen Tasks — Debug" with log path, plus "Open runtime log" and "Copy log path" items
**Result**: [X] PASS  [ ] FAIL

### T02: `mg log` alias
**Test**: Type `mg log`
**Expected**: Same debug screen as T01
**Result**: [X] PASS  [ ] FAIL

### T03: `mg logs` alias
**Test**: Type `mg logs`
**Expected**: Same debug screen as T01
**Result**: [X] PASS  [ ] FAIL

### T04: Open runtime log action
**Test**: In debug screen, click "Open runtime log"
**Expected**: Opens the log file in default text editor
**Result**: [X] PASS  [ ] FAIL

### T05: Copy log path action
**Test**: In debug screen, click "Copy log path"
**Expected**: Log file path copied to clipboard
**Result**: [X] PASS  [ ] FAIL

---

## Help screen (log items removed)

### T06: `mg help` — no log items
**Test**: Type `mg help`
**Expected**: Help screen shows commands, due date formats, Enter behavior — but NO "Open runtime log" / "Copy log path" / "Runtime logs" items
**Result**: [X] PASS  [ ] FAIL

### T07: `mg help` — debug in examples
**Test**: Type `mg help`
**Expected**: "Debug / logs" appears in the command examples list with `mg debug`
**Result**: [X] PASS  [ ] FAIL

---

## Error screens (log items removed)

### T08: Welcome screen (no API key)
**Test**: Clear API key in preferences, restart, type `mg`
**Expected**: Welcome message says `Run "mg debug" for logs.` — no "Open runtime log" / "Copy log path" items
**Result**: [X] PASS  [ ] FAIL  [ ] SKIP

### T09: Error screens mention `mg debug`
**Test**: Trigger any error (e.g. invalid API key), check error items
**Expected**: Error suggestions say `Run "mg debug" for logs.` — no log action items inline
**Result**: [] PASS  [X] FAIL  [ ] SKIP
**Note**: only shows welcome screen

---

## Non-interference

### T10: `mg debug` doesn't match partial
**Test**: Type `mg debugging` or `mg debug something`
**Expected**: Normal search, NOT the debug screen
**Result**: [X] PASS  [ ] FAIL

### T11: Normal flows unaffected
**Test**: `mg ` (list), `mg <search>`, `mg new Test`, `mg clear`, `mg refresh`
**Expected**: All work as before
**Result**: [X] PASS  [ ] FAIL
