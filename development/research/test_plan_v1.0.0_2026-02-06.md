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
- [X] Ensure you have a valid Morgen API key configured
- [X] Have at least 5-10 tasks in your Morgen account for testing
- [X] Include tasks with different priorities (high, medium, low, none)
- [X] Include tasks with different due dates (past, today, tomorrow, future)
- [X] Clear cache before starting: `mg clear`
- [X] Note your current task count: 39

---

## Category 1: Basic Functionality

### T01: Extension Loads
**Test**: Type `mg` in Ulauncher
**Expected**: Extension loads without errors in console
**Result**: [X] PASS [ ] FAIL
**Notes**:
```
2026-02-06 13:25:11,384 | DEBUG | ulauncher.api.server.ExtensionController: handleMessage() | Incoming response (KeywordQueryEvent, RenderResultListAction) from "ulauncher-morgen-tasks"
2026-02-06 13:25:11,398 | DEBUG | ulauncher.ui.windows.UlauncherWindow: show_results() | render 9 results
```

### T02: Welcome Screen (No Query)
**Test**: Type just `mg` with no additional text
**Expected**: Shows welcome message with log access options
**Result**: [ ] PASS [X] FAIL
**Notes**: even though it did not work, I also do not need it
log after typung `mg`
```
2026-02-06 13:27:14,940 | DEBUG | ulauncher.ui.windows.UlauncherWindow: show_results() | render 3 results
```

### T03: List All Tasks
**Test**: Type `mg ` (with space)
**Expected**: Shows up to 7 tasks with "... and X more" if >7 tasks exist
**Result**: [X] PASS [ ] FAIL
**Count shown**: 7
**Notes**: remove the last message stating "... and X more" no need for that. Also add to todo list, if the number of tasks which match search query is higher than 5 then show up to 15 tasks in condensed mode (check how fzf extensions results are presented in one line), if not show only 5 in non condensed mode

### T04: Task Display Format
**Test**: Review task display in T03
**Expected**: Each task shows:
- Task title (truncated if long)
- Due date (relative if today/tomorrow, e.g., "Today 14:00")
- Priority icon (`!!` for high, `!` for medium)
- Priority label in subtitle ("High", "Medium", "Low", "Normal")
- Overdue indicator if past due ("OVERDUE" prefix, "(overdue!)" in subtitle)

**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T05: Copy Task ID
**Test**: Click on any task in the list
**Expected**: Ulauncher window closes, task ID copied to clipboard
**Verify**: Paste clipboard - should be a UUID
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

---

## Category 2: Search Functionality

### T06: Search by Title (Single Word)
**Test**: Type `mg meeting` (or any word from your task titles)
**Expected**: Shows only tasks containing "meeting" (case-insensitive)
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T07: Search by Title (Multiple Words)
**Test**: Type `mg team sync` (or any multi-word phrase)
**Expected**: Shows tasks containing "team" AND "sync"
**Result**: [X] PASS [ ] FAIL
**Notes**: order matters, if inverted it did not work

### T08: Search No Results
**Test**: Type `mg xyzabc123nonexistent`
**Expected**: Shows "No tasks found matching 'xyzabc123nonexistent'"
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T09: Search Case Insensitivity
**Test**: Type `mg MEETING` (all caps)
**Expected**: Same results as T06
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T10: Search Performance
**Test**: Type `mg <search term>` - observe response time
**Expected**: Results appear within ~1ms (check console if verbose mode shows timing)
**Result**: [X] PASS [ ] FAIL
**Observed time**: 0.61ms
**Notes**: log
```
ulauncher-morgen-tasks | 2026-02-06 13:39:26,664 | DEBUG | __main__: _timed() | PERF cache_lookup: 0.37ms
ulauncher-morgen-tasks | 2026-02-06 13:39:26,664 | INFO | __main__: _get_tasks() | Using cached tasks: 39 tasks (age=3m ago)
ulauncher-morgen-tasks | 2026-02-06 13:39:26,665 | DEBUG | __main__: _timed() | PERF filter_tasks: 0.11ms
ulauncher-morgen-tasks | 2026-02-06 13:39:26,665 | DEBUG | __main__: _timed() | PERF format_2_tasks: 0.13ms
```


---

## Category 3: Task Creation

### T11: Create Basic Task
**Test**: Type `mg new Buy groceries`
**Expected**: Shows preview "Create: Buy groceries | Due: None | Priority: Normal"
**Action**: Press Enter
**Expected**: Shows "Task created successfully!"
**Verify**: Check Morgen app - task should appear
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T12: Create Task with Due Date (Absolute)
**Test**: Type `mg new Submit report @2026-02-15`
**Expected**: Preview shows "Due: Feb 15"
**Action**: Press Enter and verify in Morgen
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T13: Create Task with Due Date (Relative - Today)
**Test**: Type `mg new Call client @today`
**Expected**: Preview shows today's date
**Action**: Press Enter and verify in Morgen
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T14: Create Task with Due Date (Relative - Tomorrow)
**Test**: Type `mg new Review PR @tomorrow`
**Expected**: Preview shows tomorrow's date
**Action**: Press Enter and verify in Morgen
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T15: Create Task with Due Date (Day of Week)
**Test**: Type `mg new Team meeting @friday`
**Expected**: Preview shows next Friday's date
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [X] FAIL
**Notes**: cannot create task
Log
```
2026-02-06 13:45:16,522 | DEBUG | ulauncher.api.server.ExtensionController: _send_event() | Send event KeywordQueryEvent to "ulauncher-morgen-tasks"
ulauncher-morgen-tasks | 2026-02-06 13:45:16,530 | DEBUG | ulauncher.api.client.Client: on_message() | Incoming event KeywordQueryEvent
ulauncher-morgen-tasks | 2026-02-06 13:45:16,530 | INFO | __main__: on_event() | Keyword triggered with query: 'new Team meeting @friday'
ulauncher-morgen-tasks | 2026-02-06 13:45:16,531 | INFO | __main__: on_event() | Showing create-task preview
ulauncher-morgen-tasks | 2026-02-06 13:45:16,532 | DEBUG | ulauncher.api.client.Client: send() | Send message
2026-02-06 13:45:16,537 | DEBUG | ulauncher.api.server.ExtensionController: handleMessage() | Incoming response (KeywordQueryEvent, RenderResultListAction) from "ulauncher-morgen-tasks"
2026-02-06 13:45:16,545 | DEBUG | ulauncher.ui.windows.UlauncherWindow: show_results() | render 1 results
```

### T16: Create Task with High Priority
**Test**: Type `mg new Urgent fix !high`
**Expected**: Preview shows "Priority: High"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [x] FAIL
**Notes**: but it works with `mg new Urgent fix !1`

### T17: Create Task with Medium Priority
**Test**: Type `mg new Important task !medium`
**Expected**: Preview shows "Priority: Medium"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [ ] FAIL
**Notes**: but it works with `mg new Important task !5`  

### T18: Create Task with Low Priority
**Test**: Type `mg new Nice to have !low`
**Expected**: Preview shows "Priority: Low"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [X] FAIL
**Notes**: but it works with `mg new Nice to have !9`

### T19: Create Task with Priority Shorthand (!!)
**Test**: Type `mg new Critical bug !!`
**Expected**: Preview shows "Priority: High"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [x] FAIL
**Notes**: no priority, normal

### T20: Create Task with Priority Shorthand (!)
**Test**: Type `mg new Regular task !`
**Expected**: Preview shows "Priority: Medium"
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [X] FAIL
**Notes**: no priority, normal

### T21: Create Task with Due + Priority
**Test**: Type `mg new Deploy app @tomorrow !high`
**Expected**: Preview shows both due date and priority
**Action**: Press Enter and verify in Morgen
**Result**: [ ] PASS [X] FAIL
**Notes**: task created as `Deploy app !high`, no priority was set

### T22: Create Task - Cache Invalidation
**Test**: After creating task in T21, type `mg ` (list all)
**Expected**: New task appears in the list immediately
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T23: Create Task - Empty Title
**Test**: Type `mg new ` (just "new" with nothing after)
**Expected**: Shows error "Usage: mg new <title> [@due] [!priority]"
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T24: Create Task - Special Characters
**Test**: Type `mg new "Fix bug #123 & test"`
**Expected**: Creates task with title including #, &
**Verify**: Check Morgen app for correct title
**Result**: [X] PASS [ ] FAIL
**Notes**: it also includes  quotes ""

### T25: Create Task - Long Title
**Test**: Type `mg new This is a very long task title that exceeds normal length to test how the system handles it`
**Expected**: Preview shows full title or truncated version
**Action**: Press Enter and verify full title in Morgen
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

Random Error
```
2026-02-06 13:54:35,895 | DEBUG | ulauncher.api.server.ExtensionController: handleMessage() | Incoming response (ItemEnterEvent, RenderResultListAction) from "ulauncher-morgen-tasks"
2026-02-06 13:54:35,907 | DEBUG | ulauncher.ui.windows.UlauncherWindow: show_results() | render 1 results
zsh: segmentation fault (core dumped)  ulauncher -v
```

---

## Category 4: Cache Management

### T26: Cache Age Indicator (Fresh Cache)
**Test**: Type `mg clear` then `mg ` (list all)
**Expected**: Shows "Cache: <1s old" or similar fresh indicator
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T27: Cache Age Indicator (Older Cache)
**Test**: Wait 30 seconds, then type `mg ` (list all)
**Expected**: Shows "Cache: 30s old" or similar
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T28: Cache Persistence Across Restarts
**Test**: Type `mg ` (list all), then restart Ulauncher, then `mg ` again
**Expected**: Cache still valid, shows tasks without API call
**Verify**: Check console - should not see "Fetching tasks from API"
**Result**: [X] PASS [ ] FAIL
**Notes**: Logs
```
2026-02-06 14:01:21,818 | DEBUG | ulauncher.api.server.ExtensionController: handleMessage() | Incoming response (KeywordQueryEvent, RenderResultListAction) from "ulauncher-morgen-tasks"
2026-02-06 14:01:21,865 | DEBUG | ulauncher.ui.windows.UlauncherWindow: show_results() | render 9 results
```

### T29: Clear Cache Command
**Test**: Type `mg clear`
**Expected**: Shows "Cache cleared" confirmation
**Action**: Type `mg ` (list all)
**Expected**: Fresh API call, cache age resets
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T30: Force Refresh (!)
**Test**: Type `mg !`
**Expected**: Triggers immediate refresh, shows updated task list
**Verify**: Cache age resets to <1s
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T31: Force Refresh (refresh keyword)
**Test**: Type `mg refresh`
**Expected**: Same as T30 - triggers immediate refresh
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T32: One-Shot Refresh (Typing After !)
**Test**: Type `mg !m` (! followed by other text)
**Expected**: Does NOT trigger refresh, searches for tasks matching "m"
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T33: Cache Expiry (10 Minutes)
**Test**: After cache is >10 minutes old, type `mg `
**Expected**: Automatically fetches fresh data from API
**Note**: This test requires waiting 10+ minutes or manually editing cache timestamp
**Result**: [X] PASS [ ] FAIL [ ] SKIP
**Notes**: ___________

---

## Category 5: Help & Documentation

### T34: Help Command (help)
**Test**: Type `mg help`
**Expected**: Shows comprehensive help with all commands listed
**Verify**: Help includes: list, search, create, refresh, clear, help, log access
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T35: Help Command (?)
**Test**: Type `mg ?`
**Expected**: Same help screen as T34
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T36: Log Access - Open
**Test**: In help screen or error screen, find "Open runtime log" option
**Expected**: Clicking it opens log file in default text editor
**Result**: [X] PASS [ ] FAIL
**Notes**: I think it is unecessary. it could this could be either in ulauncher extension settings, or under a different command like `mg debug` 

### T37: Log Access - Copy Path
**Test**: In help screen or error screen, find "Copy log path" option
**Expected**: Clicking it copies log path to clipboard
**Verify**: Paste clipboard - should be path to `extension/logs/runtime.log`
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

---

## Category 6: Error Handling

### T38: Missing API Key
**Test**: Remove API key from preferences, type `mg `
**Expected**: Shows welcome screen with instructions to set API key
**Verify**: Includes log access options
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T39: Invalid API Key
**Test**: Set API key to "invalid-key-12345", type `mg `
**Expected**: Shows error "Authentication failed" with helpful tip
**Verify**: Error mentions checking API key and links to log
**Result**: [ X PASS [ ] FAIL
**Notes**: ___________

### T40: Invalid API Key - Log Access
**Test**: In error screen from T39, verify log access options present
**Expected**: Shows "Open runtime log" and "Copy log path" options
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T41: Network Error (Simulated)
**Test**: Disconnect network, type `mg !` (force refresh)
**Expected**: Shows network error with helpful message
**Verify**: Error message mentions checking connection
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T42: Network Error - Fallback to Cache
**Test**: After T41, reconnect network but don't refresh. Type `mg `
**Expected**: Shows cached tasks with warning about staleness
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T43: Invalid Date Format
**Test**: Type `mg new Task @notadate`
**Expected**: Shows error "Invalid date: notadate"
**Result**: [X] PASS [ ] FAIL
**Notes**: even though it worked it gives too much information, simplify it.
Current result `Invalid due date 'notadate'; Unreco... 026-02-10, 2026-02-10T15:30, 15:30`

### T44: Invalid Priority
**Test**: Type `mg new Task !invalid`
**Expected**: Shows error "Invalid priority: invalid" or ignores invalid priority
**Result**: [ ] PASS [X] FAIL
**Notes**: it allows me to create a task

---

## Category 7: Edge Cases & Performance

### T45: Empty Task List
**Test**: If possible, test with Morgen account that has zero tasks
**Expected**: Shows message "No tasks found. Create one with: mg new <title>"
**Result**: [ ] PASS [ ] FAIL [X] SKIP (no empty account available)
**Notes**: ___________

### T46: Large Task Count (>100)
**Test**: With many tasks, type `mg ` to list all
**Expected**: Shows first 7 tasks with "... and X more"
**Verify**: UI remains responsive
**Result**: [X] PASS [ ] FAIL [ ] SKIP (not enough tasks)
**Notes**: ___________

### T47: Search in Large Dataset
**Test**: With many tasks, search for specific term
**Expected**: Search completes quickly (<10ms based on optimization)
**Result**: [X] PASS [ ] FAIL [ ] SKIP (not enough tasks)
**Notes**: i think This optimisation should only occur if 200+ tasks are found, otherwise it should be ignored. 

### T48: Very Long Task Title Display
**Test**: Create task with 200+ character title, then list
**Expected**: Title is truncated with "..." in display
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T49: Tasks with Same Title
**Test**: Create 2-3 tasks with identical titles
**Expected**: All tasks appear in list, distinguishable by due date/priority
**Result**: [X] PASS [ ] FAIL
**Notes**: maybe when no due date is available show date created instead

### T50: Rapid Consecutive Commands
**Test**: Quickly type `mg `, then `mg search`, then `mg !`
**Expected**: Extension handles rapid queries without crashing
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

---

## Category 8: Overdue & Priority Highlighting

### T51: Overdue Task Display
**Test**: Find or create a task with due date in the past
**Expected**: Task title prefixed with "OVERDUE", subtitle shows "(overdue!)"
**Result**: [X] PASS [ ] FAIL
**Notes**: I had to type the whole date, @yesterday does not work

### T52: High Priority Icon
**Test**: Find or create task with high priority
**Expected**: Title prefixed with `!! ` icon
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T53: Medium Priority Icon
**Test**: Find or create task with medium priority
**Expected**: Title prefixed with `! ` icon
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T54: Low/Normal Priority (No Icon)
**Test**: Find or create task with low or normal priority
**Expected**: No priority icon in title
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T55: Today/Tomorrow Relative Dates
**Test**: Find or create tasks due today and tomorrow
**Expected**: Due dates show "Today HH:mm" and "Tomorrow HH:mm"
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

---

## Category 9: Runtime Logging

### T56: Runtime Log File Exists
**Test**: Check if `extension/logs/runtime.log` exists
**Expected**: File exists and contains recent log entries
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T57: Runtime Log Content
**Test**: Open runtime log, check for useful information
**Expected**: Log contains timestamps, API calls, cache operations, errors
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T58: Runtime Log - Cache Operations
**Test**: Type `mg clear`, then check runtime log
**Expected**: Log shows "Cache cleared" entry with timestamp
**Result**: [X] PASS [ ] FAIL
**Notes**: not sure if logs state it is okay
Log
```
ulauncher-morgen-tasks | 2026-02-06 14:53:43,454 | DEBUG | ulauncher.api.client.Client: on_message() | Incoming event KeywordQueryEvent
ulauncher-morgen-tasks | 2026-02-06 14:53:43,454 | INFO | __main__: on_event() | Keyword triggered with query: 'clear'
ulauncher-morgen-tasks | 2026-02-06 14:53:43,455 | INFO | src.cache: invalidate() | Cache invalidated
ulauncher-morgen-tasks | 2026-02-06 14:53:43,456 | INFO | __main__: on_event() | Cache clear requested
ulauncher-morgen-tasks | 2026-02-06 14:53:43,457 | DEBUG | ulauncher.api.client.Client: send() | Send message
2026-02-06 14:53:43,461 | DEBUG | ulauncher.api.server.ExtensionController: handleMessage() | Incoming response (KeywordQueryEvent, RenderResultListAction) from "ulauncher-morgen-tasks"
2026-02-06 14:53:43,469 | DEBUG | ulauncher.ui.windows.UlauncherWindow: show_results() | render 1 results
```


### T59: Runtime Log - API Calls
**Test**: Type `mg !`, then check runtime log
**Expected**: Log shows "Fetching tasks from API" with timestamp
**Result**: [X] PASS [ ] FAIL
**Notes**: ___________

### T60: Runtime Log - Errors
**Test**: Trigger an error (e.g., invalid API key), check log
**Expected**: Error details logged with timestamp
**Result**: [X] PASS [ ] FAIL
**Notes**: not sure if this is what you expected
Log
```
2026-02-06 14:55:22,628 INFO __main__: Fetching tasks from API...
2026-02-06 14:55:22,629 INFO src.morgen_api: Fetching tasks from Morgen API (limit=100)
2026-02-06 14:55:22,961 WARNING __main__: Authentication failed (invalid API key)
```

---

## Test Summary

**Total Tests**: 60
**Passed**: 47
**Failed**: 12
**Skipped**: 1

**Critical Issues** (tests that MUST pass for v1.0.0):
- List all functionality: [X] PASS
- Search functionality: [X] PASS (T07 has order-sensitivity bug)
- Create task: [ ] FAIL (T15-T21 — priority/date parsing broken)
- Cache management: [X] PASS
- Error handling: [X] PASS (T44 minor — invalid priority accepted)

---

## Fix TODO List

### BUGS (Must Fix for v1.0.0)

- [ ] **FIX-01** (T07): Search word order matters — should be order-independent
  - `mg team sync` works but `mg sync team` does not
- [ ] **FIX-02** (T15): Day-of-week date parsing (`@friday`) doesn't work for task creation
- [ ] **FIX-03** (T16-T18): Named priorities (`!high`, `!medium`, `!low`) don't work
  - Only numeric priorities (`!1`, `!5`, `!9`) work
- [ ] **FIX-04** (T19-T20): Priority shorthands (`!!` and `!`) don't work
  - `!!` should map to High, `!` should map to Medium
- [ ] **FIX-05** (T21): Due date + priority combo fails
  - `@tomorrow !high` → title becomes "Deploy app !high", priority not set
  - Priority text is included in the title instead of being parsed
- [ ] **FIX-06** (T44): Invalid priority (`!invalid`) silently accepted
  - Should show error or warning instead of creating task
- [ ] **FIX-07** (T51 note): `@yesterday` not supported in date parser

### ENHANCEMENTS (Should Fix for v1.0.0)

- [ ] **ENH-01** (T03): Remove "... and X more" truncation message
- [ ] **ENH-02** (T03): Adaptive display mode
  - If results > 5: show up to 15 tasks in condensed one-line mode (like fzf)
  - If results ≤ 5: show up to 5 tasks in normal (current) mode
- [ ] **ENH-03** (T43): Simplify invalid date error message
  - Current: `Invalid due date 'notadate'; Unreco... 026-02-10, 2026-02-10T15:30, 15:30`
  - Should be shorter and clearer
- [ ] **ENH-04** (T24 note): Strip surrounding quotes from task title
  - `mg new "Fix bug"` creates title `"Fix bug"` with quotes included

### SUGGESTIONS (Nice to Have / Post v1.0.0)

- [ ] **SUG-01** (T02): Fix welcome screen when typing `mg` with no space
  - User noted: "I do not need it" — non-blocker
- [ ] **SUG-02** (T36 note): Move log access to `mg debug` command
  - Currently clutters help screen; could be separate command
- [ ] **SUG-03** (T47 note): Only enable search optimization for 200+ tasks
  - Pre-computed lowercase index overhead not needed for small sets
- [ ] **SUG-04** (T49 note): Show creation date when no due date available
  - Helps distinguish tasks with identical titles

### NON-ISSUES (Noted but not actionable)

- **T25 note**: Ulauncher segfault (`zsh: segmentation fault`) — upstream Ulauncher bug, not our code
- **T58 note**: Cache clear log says "Cache invalidated" — correct behavior, just different wording

---

## Post-Test Actions

After completing all tests:

1. [ ] Fix all BUGS (FIX-01 through FIX-07)
2. [ ] Implement ENHANCEMENTS (ENH-01 through ENH-04)
3. [ ] Re-test failed items after fixes
4. [ ] Update `CHANGELOG.md` with changes
5. [ ] Update `extension/logs/dev_log.md` with test results
6. [ ] Update `manifest.json` to v1.0.0 if all re-tests pass
7. [ ] Prepare release commit
