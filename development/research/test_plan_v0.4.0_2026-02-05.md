# Test Plan (v0.4.0) — Morgen Tasks Ulauncher Extension

**Date**: 2026-02-05  
**Version under test**: v0.4.0 (Phase 4 implemented)  
**Goal**: Verify Phase 3 list/search/refresh + Phase 4 create-task flow end-to-end in Ulauncher.

If something fails, report the **test ID** (e.g. `T12`) so we can pinpoint it quickly.

---

## Setup

- **T01** — Ensure API key is set in extension preferences.
- **T02** — Restart Ulauncher in verbose mode: `pkill ulauncher && ulauncher -v`.
- **T03** (Optional) — Tail logs: `tail -f ~/.local/share/ulauncher/last.log`.

---

## Phase 3 Regression: List / Search / Refresh

- **T04** — Run `mg` (no query).
  - Expected: header shows task count; tasks render with title + subtitle; no errors in `ulauncher -v`.
- **T05** — Run `mg <common-word-from-title>`.
  - Expected: results filter by title/description substring; header count changes.
- **T06** — Run `mg gibberishthatmatchesnothing`.
  - Expected: “No tasks found” item appears; no exception.

### Cache behavior

- **T07** — Run `mg` twice within cache TTL.
  - Expected: second run shows cached status (e.g. `Cache: cached …`).

### Force refresh behavior

- **T08** — Run `mg !`.
  - Expected: refresh occurs; header shows `Cache: refreshed` (or similar); no errors.
- **T09** — Run `mg refresh`.
  - Expected: refresh occurs; header shows refreshed/fresh status; no errors.
- **T10** — Run `mg ! <query>` (or `mg refresh <query>`).
  - Expected: refresh occurs *and* results are filtered by `<query>`.

---

## Phase 4: Create Tasks (Happy Paths)

### Title-only

- **T11** — Run `mg new Codex test task`.
  - Expected: preview item + “Create: …” item + “Cancel” item.
- **T12** — Press Enter on “Create: Codex test task”.
  - Expected: “Task created” appears; then `mg Codex test task` finds the new task.

### Due parsing (keywords)

- **T13** — Run `mg new Due today @today` → create it.
  - Expected: created; search shows due in subtitle as `YYYY-MM-DD HH:MM` (default `09:00`).
- **T14** — Run `mg new Due tomorrow @tomorrow` → create it.
  - Expected: created; due reflects tomorrow at default time.
- **T15** — Run `mg new Due next mon @next-mon` → create it.
  - Expected: created; due reflects the next Monday at default time.

### Due parsing (specific date/time)

- **T16** — Run `mg new ISO date @2026-02-10` → create it.
  - Expected: due is `2026-02-10 09:00` (default time).
- **T17** — Run `mg new ISO datetime @2026-02-10T15:30` → create it.
  - Expected: due is `2026-02-10 15:30`.
- **T18** — Run `mg new Time only @15:30` → create it.
  - Expected: if 15:30 already passed today, due is tomorrow; otherwise today (time reflects 15:30).
- **T19** — Run `mg new Time ampm @3pm` → create it.
  - Expected: due time resolves to 15:00 (today or tomorrow depending on current time).

### Priority

- **T20** — Run `mg new Priority high !1` → create it.
  - Expected: list formatting shows `[P1]` prefix; subtitle shows `Priority: 1`.
- **T21** — Run `mg new Priority low !9` → create it.
  - Expected: list formatting shows `[P9]` prefix; subtitle shows `Priority: 9`.

### Combined

- **T22** — Run `mg new Combined @tomorrow !3` → create it.
  - Expected: due and priority both appear in subtitle; task is searchable immediately.

---

## Phase 4: Create Tasks (Validation / Edge Cases)

- **T23** — Run `mg new` (no title).
  - Expected: “missing title” usage message; nothing created.
- **T24** — Run `mg new Bad due @yesterday`.
  - Expected: “Cannot create task” with invalid due error; nothing created.
- **T25** — Run `mg new Bad due @2026-13-40`.
  - Expected: “Cannot create task” with date validation error; nothing created.
- **T26** — Run `mg new Bad time @25:99`.
  - Expected: “Cannot create task” with time validation error; nothing created.
- **T27** — Run `mg new Bad priority !10`.
  - Expected: `!10` is treated as part of the title (only `!0..9` are parsed); preview title contains `!10`.
- **T28** — Run `mg new Multi due @tomorrow @15:30`.
  - Expected: only the first `@...` is treated as due; second token is treated as part of the title (current behavior).

---

## Create Flow Correctness

- **T29** — Cancel path: run `mg new Cancel test @tomorrow`, select “Cancel”.
  - Expected: no task created; searching `mg Cancel test` should not find it.
- **T30** — Cache invalidation after create:
  1) Run `mg` (should use cache if within TTL).  
  2) Create a new task.  
  3) Immediately search `mg <new-title>`.  
  - Expected: new task is found without manual refresh.

---

## Error Handling (Optional / If You Can Simulate)

- **T31** — Bad API key: set an invalid key; run `mg new Test`.
  - Expected: “Authentication Failed”; no traceback.
- **T32** — Offline mode: disable network; run `mg`.
  - Expected: list falls back to cached tasks (if available); otherwise a clear error.
- **T33** — Offline create: disable network; run `mg new Offline test`.
  - Expected: “Create failed” with network error; no traceback.

