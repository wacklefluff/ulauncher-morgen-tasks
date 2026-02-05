# Test Plan (v0.6.3) — Error UX + Richer Logging

**Date**: 2026-02-05  
**Version under test**: v0.6.3  
**Goal**: Verify improved error messages and confirm runtime log contains useful signals.

Report failures by **test ID** (e.g. `E04`).

---

## Setup

- **E01** — Restart Ulauncher: `pkill ulauncher && ulauncher -v`.
- **E02** — Ensure `extension/logs/runtime.log` exists (run `mg` once if needed).

---

## Normal Flow Smoke (ensures no regressions)

- **E03** — Run `mg`.
  - Expected: tasks list loads; header looks normal.
- **E04** — Run `mg help`.
  - Expected: help view includes a “Runtime logs” item pointing to `extension/logs/runtime.log`.
- **E05** — Run `mg clear`.
  - Expected: “Cache cleared” message appears; no error.

---

## Error UX (Optional / Requires Simulation)

- **E06** — Missing API key:
  1) Temporarily remove API key in preferences.  
  2) Run `mg`.  
  - Expected: welcome screen mentions where to find logs (`extension/logs/runtime.log`).
- **E07** — Network error:
  1) Disconnect network (or block Morgen API).  
  2) Run `mg`.  
  - Expected: clear message with tips; cached tasks shown if available; includes log hint.
- **E08** — Rate limit:
  - Expected: message suggests waiting and using cache; includes log hint (if triggered in real use).
- **E09** — Create failure (network offline):
  1) While offline, run `mg new Log error test` and confirm.  
  - Expected: “Create failed … (see extension/logs/runtime.log)”.

---

## Runtime Log Signals

- **E10** — After running `mg` and `mg refresh`, check `extension/logs/runtime.log`.
  - Expected: entries indicating cache usage vs API fetch (e.g. “Using cached tasks …” / “Fetching tasks from API …”).
- **E11** — Create task:
  - Run `mg new Log success test` and confirm.
  - Expected: runtime log contains “Task created”.

