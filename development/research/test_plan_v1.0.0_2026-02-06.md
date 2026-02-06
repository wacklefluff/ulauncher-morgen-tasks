# Manual Test Plan v1.0.0

**Date**: 2026-02-06
**Version**: v1.0.0
**Tester**: [User to fill in]
**Environment**: NixOS, Ulauncher

## Test Execution Instructions

1. Start Ulauncher in verbose mode: `pkill ulauncher && ulauncher -v`
2. For each test, record result as **PASS** or **FAIL**
3. If FAIL, note the error message and behavior
4. Test in order - some tests depend on previous ones

## Pre-Test Setup

**Setup Tasks**:
- [ ] Ensure you have a valid Morgen API key configured
- [ ] Have at least 5-10 tasks in your Morgen account for testing
- [ ] Include tasks with different priorities (high, medium, low, none)
- [ ] Include tasks with different due dates (past, today, tomorrow, future)
- [ ] Clear cache before starting: `mg clear`
- [ ] Note your current task count: ___________

---

## Category 1: Basic Functionality

### T01: Extension Loads
**Test**: Type `mg` in Ulauncher
**Expected**: Extension loads without errors in console
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T02: Welcome Screen (No Query)
**Test**: Type just `mg` with no additional text
**Expected**: Shows welcome message with log access options
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T03: List All Tasks
**Test**: Type `mg ` (with space)
**Expected**: Shows up to 7 tasks with "... and X more" if >7 tasks exist
**Result**: [ ] PASS [ ] FAIL
**Count shown**: ___________
**Notes**: ___________

### T04: Task Display Format
**Test**: Review task display in T03
**Expected**: Each task shows:
- Task title (truncated if long)
- Due date (relative if today/tomorrow, e.g., "Today 14:00")
- Priority icon (`!!` for high, `!` for medium)
- Priority label in subtitle ("High", "Medium", "Low", "Normal")
- Overdue indicator if past due ("OVERDUE" prefix, "(overdue!)" in subtitle)

**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T05: Copy Task ID
**Test**: Click on any task in the list
**Expected**: Ulauncher window closes, task ID copied to clipboard
**Verify**: Paste clipboard - should be a UUID
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

---

## Category 2: Search Functionality

### T06: Search by Title (Single Word)
**Test**: Type `mg meeting` (or any word from your task titles)
**Expected**: Shows only tasks containing "meeting" (case-insensitive)
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T07: Search by Title (Multiple Words)
**Test**: Type `mg team sync` (or any multi-word phrase)
**Expected**: Shows tasks containing "team" AND "sync"
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T08: Search No Results
**Test**: Type `mg xyzabc123nonexistent`
**Expected**: Shows "No tasks found matching 'xyzabc123nonexistent'"
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T09: Search Case Insensitivity
**Test**: Type `mg MEETING` (all caps)
**Expected**: Same results as T06
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T10: Search Performance
**Test**: Type `mg <search term>` - observe response time
**Expected**: Results appear within ~1ms (check console if verbose mode shows timing)
**Result**: [ ] PASS [ ] FAIL
**Observed time**: ___________
**Notes**: ___________

---

## Category 3: Task Creation

### T11: Create Basic Task
**Test**: Type `mg new Buy groceries`
**Expected**: Shows preview "Create: Buy groceries | Due: None | Priority: Normal"
**Action**: Press Enter
**Expected**: Shows "Task created successfully!"
**Verify**: Check Morgen app - task should appear
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T12: Create Task with Due Date (Absolute)
**Test**: Type `mg new Submit report @2026-02-15`
**Expected**: Preview shows "Due: Feb 15"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T13: Create Task with Due Date (Relative - Today)
**Test**: Type `mg new Call client @today`
**Expected**: Preview shows today's date
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T14: Create Task with Due Date (Relative - Tomorrow)
**Test**: Type `mg new Review PR @tomorrow`
**Expected**: Preview shows tomorrow's date
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T15: Create Task with Due Date (Day of Week)
**Test**: Type `mg new Team meeting @friday`
**Expected**: Preview shows next Friday's date
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T16: Create Task with High Priority
**Test**: Type `mg new Urgent fix !high`
**Expected**: Preview shows "Priority: High"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T17: Create Task with Medium Priority
**Test**: Type `mg new Important task !medium`
**Expected**: Preview shows "Priority: Medium"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T18: Create Task with Low Priority
**Test**: Type `mg new Nice to have !low`
**Expected**: Preview shows "Priority: Low"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T19: Create Task with Priority Shorthand (!!)
**Test**: Type `mg new Critical bug !!`
**Expected**: Preview shows "Priority: High"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T20: Create Task with Priority Shorthand (!)
**Test**: Type `mg new Regular task !`
**Expected**: Preview shows "Priority: Medium"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T21: Create Task with Due + Priority
**Test**: Type `mg new Deploy app @tomorrow !high`
**Expected**: Preview shows both due date and priority
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T22: Create Task - Cache Invalidation
**Test**: After creating task in T21, type `mg ` (list all)
**Expected**: New task appears in the list immediately
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T23: Create Task - Empty Title
**Test**: Type `mg new ` (just "new" with nothing after)
**Expected**: Shows error "Usage: mg new <title> [@due] [!priority]"
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T24: Create Task - Special Characters
**Test**: Type `mg new "Fix bug #123 & test"`
**Expected**: Creates task with title including #, &
**Verify**: Check Morgen app for correct title
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T25: Create Task - Long Title
**Test**: Type `mg new This is a very long task title that exceeds normal length to test how the system handles it`
**Expected**: Preview shows full title or truncated version
**Action**: Press Enter and verify full title in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

---

## Category 4: Cache Management

### T26: Cache Age Indicator (Fresh Cache)
**Test**: Type `mg clear` then `mg ` (list all)
**Expected**: Shows "Cache: <1s old" or similar fresh indicator
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T27: Cache Age Indicator (Older Cache)
**Test**: Wait 30 seconds, then type `mg ` (list all)
**Expected**: Shows "Cache: 30s old" or similar
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T28: Cache Persistence Across Restarts
**Test**: Type `mg ` (list all), then restart Ulauncher, then `mg ` again
**Expected**: Cache still valid, shows tasks without API call
**Verify**: Check console - should not see "Fetching tasks from API"
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T29: Clear Cache Command
**Test**: Type `mg clear`
**Expected**: Shows "Cache cleared" confirmation
**Action**: Type `mg ` (list all)
**Expected**: Fresh API call, cache age resets
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T30: Force Refresh (!)
**Test**: Type `mg !`
**Expected**: Triggers immediate refresh, shows updated task list
**Verify**: Cache age resets to <1s
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T31: Force Refresh (refresh keyword)
**Test**: Type `mg refresh`
**Expected**: Same as T30 - triggers immediate refresh
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T32: One-Shot Refresh (Typing After !)
**Test**: Type `mg !m` (! followed by other text)
**Expected**: Does NOT trigger refresh, searches for tasks matching "m"
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T33: Cache Expiry (10 Minutes)
**Test**: After cache is >10 minutes old, type `mg `
**Expected**: Automatically fetches fresh data from API
**Note**: This test requires waiting 10+ minutes or manually editing cache timestamp
**Result**: [ ] PASS [ ] FAIL [ ] SKIP
**Notes**: ___________

---

## Category 5: Help & Documentation

### T34: Help Command (help)
**Test**: Type `mg help`
**Expected**: Shows comprehensive help with all commands listed
**Verify**: Help includes: list, search, create, refresh, clear, help, log access
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T35: Help Command (?)
**Test**: Type `mg ?`
**Expected**: Same help screen as T34
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T36: Log Access - Open
**Test**: In help screen or error screen, find "Open runtime log" option
**Expected**: Clicking it opens log file in default text editor
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T37: Log Access - Copy Path
**Test**: In help screen or error screen, find "Copy log path" option
**Expected**: Clicking it copies log path to clipboard
**Verify**: Paste clipboard - should be path to `extension/logs/runtime.log`
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

---

## Category 6: Error Handling

### T38: Missing API Key
**Test**: Remove API key from preferences, type `mg `
**Expected**: Shows welcome screen with instructions to set API key
**Verify**: Includes log access options
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T39: Invalid API Key
**Test**: Set API key to "invalid-key-12345", type `mg `
**Expected**: Shows error "Authentication failed" with helpful tip
**Verify**: Error mentions checking API key and links to log
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T40: Invalid API Key - Log Access
**Test**: In error screen from T39, verify log access options present
**Expected**: Shows "Open runtime log" and "Copy log path" options
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T41: Network Error (Simulated)
**Test**: Disconnect network, type `mg !` (force refresh)
**Expected**: Shows network error with helpful message
**Verify**: Error message mentions checking connection
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T42: Network Error - Fallback to Cache
**Test**: After T41, reconnect network but don't refresh. Type `mg `
**Expected**: Shows cached tasks with warning about staleness
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T43: Invalid Date Format
**Test**: Type `mg new Task @notadate`
**Expected**: Shows error "Invalid date: notadate"
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T44: Invalid Priority
**Test**: Type `mg new Task !invalid`
**Expected**: Shows error "Invalid priority: invalid" or ignores invalid priority
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

---

## Category 7: Edge Cases & Performance

### T45: Empty Task List
**Test**: If possible, test with Morgen account that has zero tasks
**Expected**: Shows message "No tasks found. Create one with: mg new <title>"
**Result**: [ ] PASS [ ] FAIL [ ] SKIP (no empty account available)
**Notes**: ___________

### T46: Large Task Count (>100)
**Test**: With many tasks, type `mg ` to list all
**Expected**: Shows first 7 tasks with "... and X more"
**Verify**: UI remains responsive
**Result**: [ ] PASS [ ] FAIL [ ] SKIP (not enough tasks)
**Notes**: ___________

### T47: Search in Large Dataset
**Test**: With many tasks, search for specific term
**Expected**: Search completes quickly (<10ms based on optimization)
**Result**: [ ] PASS [ ] FAIL [ ] SKIP (not enough tasks)
**Notes**: ___________

### T48: Very Long Task Title Display
**Test**: Create task with 200+ character title, then list
**Expected**: Title is truncated with "..." in display
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T49: Tasks with Same Title
**Test**: Create 2-3 tasks with identical titles
**Expected**: All tasks appear in list, distinguishable by due date/priority
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T50: Rapid Consecutive Commands
**Test**: Quickly type `mg `, then `mg search`, then `mg !`
**Expected**: Extension handles rapid queries without crashing
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

---

## Category 8: Overdue & Priority Highlighting

### T51: Overdue Task Display
**Test**: Find or create a task with due date in the past
**Expected**: Task title prefixed with "OVERDUE", subtitle shows "(overdue!)"
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T52: High Priority Icon
**Test**: Find or create task with high priority
**Expected**: Title prefixed with `!! ` icon
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T53: Medium Priority Icon
**Test**: Find or create task with medium priority
**Expected**: Title prefixed with `! ` icon
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T54: Low/Normal Priority (No Icon)
**Test**: Find or create task with low or normal priority
**Expected**: No priority icon in title
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T55: Today/Tomorrow Relative Dates
**Test**: Find or create tasks due today and tomorrow
**Expected**: Due dates show "Today HH:mm" and "Tomorrow HH:mm"
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

---

## Category 9: Runtime Logging

### T56: Runtime Log File Exists
**Test**: Check if `extension/logs/runtime.log` exists
**Expected**: File exists and contains recent log entries
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T57: Runtime Log Content
**Test**: Open runtime log, check for useful information
**Expected**: Log contains timestamps, API calls, cache operations, errors
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T58: Runtime Log - Cache Operations
**Test**: Type `mg clear`, then check runtime log
**Expected**: Log shows "Cache cleared" entry with timestamp
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T59: Runtime Log - API Calls
**Test**: Type `mg !`, then check runtime log
**Expected**: Log shows "Fetching tasks from API" with timestamp
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

### T60: Runtime Log - Errors
**Test**: Trigger an error (e.g., invalid API key), check log
**Expected**: Error details logged with timestamp
**Result**: [ ] PASS [ ] FAIL
**Notes**: ___________

---

## Test Summary

**Total Tests**: 60
**Passed**: _____
**Failed**: _____
**Skipped**: _____

**Critical Issues** (tests that MUST pass for v1.0.0):
- List all functionality: [ ]
- Search functionality: [ ]
- Create task: [ ]
- Cache management: [ ]
- Error handling: [ ]

**Blocker Issues** (prevent release):
_____________________________________________
_____________________________________________

**Minor Issues** (can be fixed in v1.0.1):
_____________________________________________
_____________________________________________

**Notes for Developers**:
_____________________________________________
_____________________________________________

---

## Post-Test Actions

After completing all tests:

1. [ ] Update `CHANGELOG.md` with any changes
2. [ ] Update `extension/logs/dev_log.md` with test results
3. [ ] Fix any critical/blocker issues
4. [ ] Re-test failed items after fixes
5. [ ] Update `manifest.json` to v1.0.0 if all tests pass
6. [ ] Prepare release commit
