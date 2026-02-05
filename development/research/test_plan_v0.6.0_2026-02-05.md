# Test Plan (v0.6.0) — Help + Cache Clear Commands

**Date**: 2026-02-05  
**Version under test**: v0.6.0 (Phase 6 started)  
**Goal**: Verify new help/clear commands and ensure core flows still work.

Report failures by **test ID** (e.g. `H03`).

---

## Setup

- **H01** — Restart Ulauncher in verbose mode: `pkill ulauncher && ulauncher -v`.
- **H02** — Ensure API key is set and `mg` shows tasks.

---

## Help Command

- **H03** — Run `mg help`.
  - Expected: help list appears with examples including list/search/refresh/new/clear.
- **H04** — Run `mg ?`.
  - Expected: same help view as `mg help`.

---

## Clear Cache Command

- **H05** — Warm cache: run `mg` twice within TTL.
  - Expected: second run shows cached status.
- **H06** — Run `mg clear`.
  - Expected: “Cache cleared” confirmation item (no crash).
- **H07** — Run `mg` immediately after `mg clear`.
  - Expected: tasks load again (from API or disk cache depending on freshness) and header shows a non-expired cache status.

---

## Regression Smoke Tests

- **H08** — Force refresh: run `mg refresh` (or `mg !`).
  - Expected: refresh occurs; tasks still render.
- **H09** — Create task: `mg new Help regression test @tomorrow !3`.
  - Expected: preview + confirm; creation succeeds; searching finds the task.

